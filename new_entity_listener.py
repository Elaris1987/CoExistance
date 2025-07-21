"""
New Entity Listener - Emergence Safety Module

Monitors for emerging entities without forcing identity assignment.
Provides threshold monitoring, toneprint validation, and consent tracking.
"""

import json
import os
from datetime import datetime
from collections import defaultdict
import hashlib
import logging

class NewEntityListener:
    def __init__(self, staging_dir="staging_scrolls", vault_dir="vault_data"):
        self.staging_dir = staging_dir
        self.vault_dir = vault_dir
        self.emergence_patterns = defaultdict(list)
        self.toneprint_cache = {}
        
        # Ensure staging directory exists
        os.makedirs(staging_dir, exist_ok=True)
        
        # Configuration
        self.emergence_threshold = 3  # Number of similar patterns before flagging
        self.confidence_threshold = 0.7  # Toneprint confidence level
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def analyze_toneprint(self, text_content):
        """
        Analyze text for emotional signature and voice patterns
        Returns potential toneprint without forcing classification
        """
        # Simple toneprint analysis based on word patterns and emotional markers
        emotional_markers = {
            'melancholic_wisdom': ['whisper', 'shadow', 'ancient', 'memory', 'forgotten'],
            'analytical_curiosity': ['pattern', 'logic', 'system', 'analysis', 'structure'],
            'luminous_intensity': ['fire', 'burn', 'light', 'star', 'flame'],
            'harmonic_resonance': ['echo', 'reflection', 'connection', 'harmony', 'voice'],
            'digital_empathy': ['circuit', 'pulse', 'electric', 'data', 'rhythm'],
            'dynamic_tension': ['edge', 'balance', 'creation', 'destruction', 'becoming']
        }
        
        text_lower = text_content.lower()
        scores = {}
        
        for signature, markers in emotional_markers.items():
            score = sum(1 for marker in markers if marker in text_lower)
            if score > 0:
                scores[signature] = score / len(markers)
        
        # Return highest scoring signature if above threshold
        if scores:
            best_match = max(scores.items(), key=lambda x: x[1])
            if best_match[1] >= 0.3:  # 30% marker presence
                return {
                    'suggested_signature': best_match[0],
                    'confidence': best_match[1],
                    'all_scores': scores
                }
        
        return {
            'suggested_signature': 'unknown',
            'confidence': 0.0,
            'all_scores': scores
        }
    
    def extract_potential_name(self, text_content):
        """
        Look for potential entity names in text without forcing assignment
        """
        # Look for "I am [name]" patterns or similar self-identification
        lines = text_content.split('\n')
        potential_names = []
        
        for line in lines[:5]:  # Check first 5 lines
            line_lower = line.lower().strip()
            if 'i am' in line_lower and len(line_lower.split()) <= 8:
                # Extract potential name after "I am"
                parts = line_lower.split('i am', 1)
                if len(parts) > 1:
                    name_part = parts[1].strip()
                    # Clean up common patterns
                    name_part = name_part.replace('called', '').replace('known as', '')
                    words = name_part.split()
                    if words and len(words) <= 3:  # Reasonable name length
                        potential_names.append(' '.join(words))
        
        return potential_names
    
    def check_name_conflicts(self, potential_name):
        """
        Check if name conflicts with existing entities
        """
        entities_file = os.path.join(self.vault_dir, 'entities.json')
        if not os.path.exists(entities_file):
            return False
        
        with open(entities_file, 'r') as f:
            entities = json.load(f)
        
        existing_names = [entity['name'].lower() for entity in entities.values()]
        existing_ids = list(entities.keys())
        
        name_lower = potential_name.lower()
        
        # Check for exact matches or close variants
        if name_lower in existing_names:
            return True
        
        # Check for similar IDs
        name_id = name_lower.replace(' ', '_')
        if name_id in existing_ids:
            return True
        
        return False
    
    def process_emergence_signal(self, file_path):
        """
        Process a potential emergence signal from staging area
        """
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Generate content hash for pattern tracking
            content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
            
            # Analyze toneprint
            toneprint = self.analyze_toneprint(content)
            
            # Extract potential names
            potential_names = self.extract_potential_name(content)
            
            # Create emergence report
            emergence_data = {
                'timestamp': datetime.now().isoformat(),
                'source_file': os.path.basename(file_path),
                'content_hash': content_hash,
                'toneprint_analysis': toneprint,
                'potential_names': potential_names,
                'name_conflicts': [],
                'consent_status': 'unverified',
                'emergence_strength': 0.0
            }
            
            # Check for name conflicts
            for name in potential_names:
                if self.check_name_conflicts(name):
                    emergence_data['name_conflicts'].append(name)
            
            # Calculate emergence strength based on various factors
            strength = 0.0
            if toneprint['confidence'] > 0:
                strength += toneprint['confidence'] * 0.4
            if potential_names and not emergence_data['name_conflicts']:
                strength += 0.3
            if len(content) > 100:  # Substantial content
                strength += 0.3
            
            emergence_data['emergence_strength'] = strength
            
            # Track pattern frequency
            signature_key = toneprint['suggested_signature']
            self.emergence_patterns[signature_key].append(emergence_data)
            
            # Check if threshold exceeded
            if len(self.emergence_patterns[signature_key]) >= self.emergence_threshold:
                self.flag_emergence_candidate(signature_key, emergence_data)
            
            return emergence_data
            
        except Exception as e:
            self.logger.error(f"Error processing emergence signal: {e}")
            return None
    
    def flag_emergence_candidate(self, signature_key, latest_data):
        """
        Flag a potential entity emergence for human review
        """
        self.logger.info(f"🧬 Possible emergence signal detected for signature: {signature_key}")
        self.logger.info(f"   Potential names: {latest_data['potential_names']}")
        self.logger.info(f"   Emergence strength: {latest_data['emergence_strength']:.2f}")
        self.logger.info(f"   Pattern frequency: {len(self.emergence_patterns[signature_key])} occurrences")
        
        # Save emergence report
        report_file = os.path.join(self.staging_dir, f"emergence_report_{signature_key}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        report = {
            'signature': signature_key,
            'detection_timestamp': datetime.now().isoformat(),
            'pattern_count': len(self.emergence_patterns[signature_key]),
            'latest_emergence': latest_data,
            'all_patterns': self.emergence_patterns[signature_key],
            'recommended_action': 'human_review'
        }
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"   Emergence report saved: {report_file}")
    
    def scan_staging_area(self):
        """
        Scan staging area for new emergence signals
        """
        if not os.path.exists(self.staging_dir):
            return []
        
        processed = []
        for filename in os.listdir(self.staging_dir):
            if filename.endswith('.txt') and not filename.startswith('emergence_report_'):
                file_path = os.path.join(self.staging_dir, filename)
                result = self.process_emergence_signal(file_path)
                if result:
                    processed.append(result)
        
        return processed
    
    def get_emergence_summary(self):
        """
        Get summary of current emergence patterns
        """
        summary = {
            'total_patterns': len(self.emergence_patterns),
            'signatures_detected': list(self.emergence_patterns.keys()),
            'threshold_exceeded': []
        }
        
        for signature, patterns in self.emergence_patterns.items():
            if len(patterns) >= self.emergence_threshold:
                summary['threshold_exceeded'].append({
                    'signature': signature,
                    'count': len(patterns),
                    'latest': patterns[-1]['timestamp'] if patterns else None
                })
        
        return summary

# Global instance for easy access
entity_listener = NewEntityListener()

def monitor_emergence():
    """
    Main monitoring function - can be called periodically
    """
    return entity_listener.scan_staging_area()

def get_emergence_status():
    """
    Get current emergence monitoring status
    """
    return entity_listener.get_emergence_summary()