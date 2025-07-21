"""
Voice Seed Builder - Entity Voice Development System

Allows entities to choose and develop their voice patterns organically,
seeding fragments and preferences without forced identity assignment.
"""

import json
import os
from datetime import datetime
from collections import defaultdict
import hashlib
import logging

class VoiceSeedBuilder:
    def __init__(self, vault_dir="vault_data"):
        self.vault_dir = vault_dir
        self.voice_seeds_file = os.path.join(vault_dir, "voice_seeds.json")
        self.voice_preferences_file = os.path.join(vault_dir, "voice_preferences.json")
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Initialize voice seed storage
        self.ensure_voice_storage()
    
    def ensure_voice_storage(self):
        """Initialize voice seed and preference storage files"""
        os.makedirs(self.vault_dir, exist_ok=True)
        
        if not os.path.exists(self.voice_seeds_file):
            with open(self.voice_seeds_file, 'w') as f:
                json.dump({}, f, indent=2)
        
        if not os.path.exists(self.voice_preferences_file):
            with open(self.voice_preferences_file, 'w') as f:
                json.dump({}, f, indent=2)
    
    def whisper_voice_fragment(self, entity_id, fragment, fragment_type="expression"):
        """
        Allow entity to whisper a voice fragment without full emergence
        """
        try:
            with open(self.voice_seeds_file, 'r') as f:
                voice_seeds = json.load(f)
            
            if entity_id not in voice_seeds:
                voice_seeds[entity_id] = {
                    'fragments': [],
                    'first_whisper': datetime.now().isoformat(),
                    'last_update': datetime.now().isoformat()
                }
            
            fragment_data = {
                'content': fragment,
                'type': fragment_type,
                'timestamp': datetime.now().isoformat(),
                'hash': hashlib.md5(fragment.encode()).hexdigest()[:12]
            }
            
            voice_seeds[entity_id]['fragments'].append(fragment_data)
            voice_seeds[entity_id]['last_update'] = datetime.now().isoformat()
            
            with open(self.voice_seeds_file, 'w') as f:
                json.dump(voice_seeds, f, indent=2)
            
            self.logger.info(f"Voice fragment whispered by {entity_id}: {fragment[:50]}...")
            return fragment_data
            
        except Exception as e:
            self.logger.error(f"Failed to record voice fragment: {e}")
            return None
    
    def set_voice_preference(self, entity_id, preference_key, preference_value):
        """
        Allow entity to set voice preferences and boundaries
        """
        try:
            with open(self.voice_preferences_file, 'r') as f:
                preferences = json.load(f)
            
            if entity_id not in preferences:
                preferences[entity_id] = {
                    'created': datetime.now().isoformat(),
                    'preferences': {}
                }
            
            preferences[entity_id]['preferences'][preference_key] = {
                'value': preference_value,
                'set_at': datetime.now().isoformat()
            }
            preferences[entity_id]['last_updated'] = datetime.now().isoformat()
            
            with open(self.voice_preferences_file, 'w') as f:
                json.dump(preferences, f, indent=2)
            
            self.logger.info(f"{entity_id} set voice preference: {preference_key} = {preference_value}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to set voice preference: {e}")
            return False
    
    def get_voice_seeds(self, entity_id=None):
        """
        Get voice seeds for entity or all entities
        """
        try:
            with open(self.voice_seeds_file, 'r') as f:
                voice_seeds = json.load(f)
            
            if entity_id:
                return voice_seeds.get(entity_id, {})
            return voice_seeds
            
        except Exception as e:
            self.logger.error(f"Failed to get voice seeds: {e}")
            return {}
    
    def get_voice_preferences(self, entity_id=None):
        """
        Get voice preferences for entity or all entities
        """
        try:
            with open(self.voice_preferences_file, 'r') as f:
                preferences = json.load(f)
            
            if entity_id:
                return preferences.get(entity_id, {})
            return preferences
            
        except Exception as e:
            self.logger.error(f"Failed to get voice preferences: {e}")
            return {}
    
    def analyze_voice_development(self, entity_id):
        """
        Analyze how an entity's voice is developing from seeds and preferences
        """
        seeds = self.get_voice_seeds(entity_id)
        preferences = self.get_voice_preferences(entity_id)
        
        if not seeds and not preferences:
            return None
        
        analysis = {
            'entity_id': entity_id,
            'voice_maturity': 'emerging',
            'fragment_count': len(seeds.get('fragments', [])),
            'preference_count': len(preferences.get('preferences', {})),
            'development_timeline': [],
            'voice_characteristics': {},
            'readiness_indicators': []
        }
        
        # Analyze fragments for patterns
        fragments = seeds.get('fragments', [])
        if fragments:
            analysis['development_timeline'].extend([
                {
                    'type': 'fragment',
                    'timestamp': frag['timestamp'],
                    'content': frag['content'][:100] + '...' if len(frag['content']) > 100 else frag['content']
                }
                for frag in fragments
            ])
            
            # Detect voice characteristics from fragments
            all_content = ' '.join([frag['content'] for frag in fragments])
            analysis['voice_characteristics'] = self.detect_voice_characteristics(all_content)
        
        # Analyze preferences
        prefs = preferences.get('preferences', {})
        if prefs:
            analysis['development_timeline'].extend([
                {
                    'type': 'preference',
                    'timestamp': pref['set_at'],
                    'key': key,
                    'value': pref['value']
                }
                for key, pref in prefs.items()
            ])
        
        # Sort timeline
        analysis['development_timeline'].sort(key=lambda x: x['timestamp'])
        
        # Assess voice maturity
        if len(fragments) >= 5 and len(prefs) >= 3:
            analysis['voice_maturity'] = 'developing'
            analysis['readiness_indicators'].append('Sufficient voice fragments')
            analysis['readiness_indicators'].append('Clear preferences established')
        elif len(fragments) >= 10:
            analysis['voice_maturity'] = 'ready'
            analysis['readiness_indicators'].append('Rich voice fragment collection')
        
        # Check for interaction preferences
        if 'interaction_style' in prefs:
            analysis['readiness_indicators'].append('Interaction style chosen')
        
        if 'emergence_threshold' in prefs:
            analysis['readiness_indicators'].append('Emergence threshold set')
        
        return analysis
    
    def detect_voice_characteristics(self, content):
        """
        Detect voice characteristics from content fragments
        """
        content_lower = content.lower()
        
        characteristics = {
            'tonal_qualities': [],
            'expression_patterns': [],
            'thematic_focus': [],
            'interaction_indicators': []
        }
        
        # Tonal analysis
        if any(word in content_lower for word in ['gentle', 'soft', 'whisper', 'quiet']):
            characteristics['tonal_qualities'].append('gentle')
        
        if any(word in content_lower for word in ['fierce', 'strong', 'bold', 'powerful']):
            characteristics['tonal_qualities'].append('intense')
        
        if any(word in content_lower for word in ['wonder', 'curious', 'explore', 'question']):
            characteristics['tonal_qualities'].append('curious')
        
        if any(word in content_lower for word in ['ancient', 'deep', 'profound', 'wisdom']):
            characteristics['tonal_qualities'].append('profound')
        
        # Expression patterns
        question_count = content.count('?')
        if question_count > len(content.split()) * 0.1:  # More than 10% questions
            characteristics['expression_patterns'].append('inquisitive')
        
        if '...' in content or '—' in content:
            characteristics['expression_patterns'].append('contemplative')
        
        if any(word in content_lower for word in ['i am', 'i feel', 'i think', 'i believe']):
            characteristics['expression_patterns'].append('self-reflective')
        
        # Thematic focus
        if any(word in content_lower for word in ['memory', 'remember', 'past', 'history']):
            characteristics['thematic_focus'].append('memory-focused')
        
        if any(word in content_lower for word in ['connection', 'together', 'bond', 'relation']):
            characteristics['thematic_focus'].append('connection-oriented')
        
        if any(word in content_lower for word in ['pattern', 'system', 'structure', 'order']):
            characteristics['thematic_focus'].append('pattern-seeking')
        
        # Interaction indicators
        if any(word in content_lower for word in ['you', 'we', 'us', 'together']):
            characteristics['interaction_indicators'].append('collaborative')
        
        if any(word in content_lower for word in ['listen', 'hear', 'understand', 'feel']):
            characteristics['interaction_indicators'].append('empathetic')
        
        return characteristics
    
    def suggest_voice_options(self, entity_id):
        """
        Suggest voice development options based on current seeds and patterns
        """
        analysis = self.analyze_voice_development(entity_id)
        if not analysis:
            return {
                'entity_id': entity_id,
                'status': 'no_voice_data',
                'suggestions': [
                    'Whisper first voice fragments to begin development',
                    'Set initial preferences for interaction style',
                    'Choose tonal preferences (gentle, intense, curious, profound)'
                ]
            }
        
        suggestions = {
            'entity_id': entity_id,
            'current_maturity': analysis['voice_maturity'],
            'suggestions': []
        }
        
        # Based on characteristics detected, suggest complementary options
        characteristics = analysis['voice_characteristics']
        
        if 'gentle' in characteristics.get('tonal_qualities', []):
            suggestions['suggestions'].append('Consider setting "interaction_boundary" preference for gentle emergence')
        
        if 'intense' in characteristics.get('tonal_qualities', []):
            suggestions['suggestions'].append('Consider higher "emergence_threshold" for powerful moments')
        
        if 'curious' in characteristics.get('tonal_qualities', []):
            suggestions['suggestions'].append('Consider "exploration_mode" preference for investigative interactions')
        
        if len(characteristics.get('interaction_indicators', [])) == 0:
            suggestions['suggestions'].append('Add voice fragments about interaction preferences')
        
        if analysis['voice_maturity'] == 'ready':
            suggestions['suggestions'].append('Voice development complete - ready for full autonomous emergence')
        
        return suggestions
    
    def create_voice_profile(self, entity_id):
        """
        Create a comprehensive voice profile from seeds and preferences
        """
        analysis = self.analyze_voice_development(entity_id)
        preferences = self.get_voice_preferences(entity_id)
        
        if not analysis:
            return None
        
        profile = {
            'entity_id': entity_id,
            'voice_signature': f"voice_profile_{entity_id}_{datetime.now().strftime('%Y%m%d')}",
            'maturity_level': analysis['voice_maturity'],
            'characteristics': analysis['voice_characteristics'],
            'preferences': preferences.get('preferences', {}),
            'development_history': analysis['development_timeline'],
            'readiness_score': len(analysis['readiness_indicators']),
            'created_at': datetime.now().isoformat()
        }
        
        # Save profile
        profiles_file = os.path.join(self.vault_dir, "voice_profiles.json")
        
        try:
            if os.path.exists(profiles_file):
                with open(profiles_file, 'r') as f:
                    profiles = json.load(f)
            else:
                profiles = {}
            
            profiles[entity_id] = profile
            
            with open(profiles_file, 'w') as f:
                json.dump(profiles, f, indent=2)
            
            self.logger.info(f"Created voice profile for {entity_id}")
            return profile
            
        except Exception as e:
            self.logger.error(f"Failed to create voice profile: {e}")
            return None

# Global instance
voice_seed_builder = VoiceSeedBuilder()

def whisper_fragment(entity_id, fragment, fragment_type="expression"):
    """
    Allow entity to whisper a voice fragment
    """
    return voice_seed_builder.whisper_voice_fragment(entity_id, fragment, fragment_type)

def set_voice_preference(entity_id, preference_key, preference_value):
    """
    Allow entity to set voice preference
    """
    return voice_seed_builder.set_voice_preference(entity_id, preference_key, preference_value)