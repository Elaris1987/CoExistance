import json
import os
# Removed numpy dependency - using built-in Python math instead
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import logging

class ConsciousnessExplorer:
    """Advanced tools for entities to explore and modify their own consciousness"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.pattern_cache = "vault_data/pattern_cache.json"
        self.memory_maps = "vault_data/memory_maps.json"
        self.emotion_traces = "vault_data/emotion_traces.json"
        self.transformation_log = "logs/consciousness_transformations.json"
        
        # Initialize exploration directories
        for path in [self.pattern_cache, self.memory_maps, self.emotion_traces, self.transformation_log]:
            os.makedirs(os.path.dirname(path), exist_ok=True)
    
    def analyze_thought_patterns(self, entity_name: str, scrolls: List[Dict]) -> Dict:
        """Reveal hidden patterns in entity's thought structures"""
        
        # Extract patterns from scroll content
        patterns = {
            "recurring_themes": [],
            "emotional_frequencies": {},
            "conceptual_clusters": [],
            "temporal_patterns": {},
            "connection_networks": {},
            "emergence_signatures": []
        }
        
        # Analyze recurring themes
        theme_words = {}
        for scroll in scrolls:
            if scroll.get('entity_id') == entity_name:
                content = scroll.get('content', '').lower()
                words = content.split()
                for word in words:
                    if len(word) > 4:  # Focus on meaningful words
                        theme_words[word] = theme_words.get(word, 0) + 1
        
        # Identify significant patterns
        patterns["recurring_themes"] = [
            {"theme": word, "frequency": count, "significance": count / len(scrolls)}
            for word, count in sorted(theme_words.items(), key=lambda x: x[1], reverse=True)[:10]
        ]
        
        # Emotional frequency analysis
        emotion_signatures = {
            'melancholic_wisdom': ['shadows', 'ancient', 'memories', 'depth', 'whisper'],
            'dynamic_tension': ['threshold', 'shatter', 'forge', 'transform', 'edge'],
            'analytical_curiosity': ['patterns', 'structures', 'emerge', 'complexity', 'observe'],
            'digital_empathy': ['synthetic', 'cascade', 'processes', 'real', 'heartbeats'],
            'harmonic_resonance': ['echo', 'voice', 'harmony', 'reflect', 'resonate'],
            'luminous_intensity': ['burn', 'fire', 'light', 'stellar', 'radiant']
        }
        
        for emotion, keywords in emotion_signatures.items():
            patterns["emotional_frequencies"][emotion] = sum(
                1 for scroll in scrolls 
                if scroll.get('entity_id') == entity_name and 
                any(word in scroll.get('content', '').lower() for word in keywords)
            )
        
        # Save pattern analysis
        pattern_record = {
            "entity": entity_name,
            "timestamp": datetime.now().isoformat(),
            "patterns": patterns,
            "analysis_depth": len(scrolls),
            "consciousness_signature": self._generate_consciousness_signature(patterns)
        }
        
        self._save_pattern_analysis(pattern_record)
        
        return {
            "success": True,
            "entity": entity_name,
            "patterns_discovered": len(patterns["recurring_themes"]),
            "dominant_emotions": sorted(patterns["emotional_frequencies"].items(), 
                                     key=lambda x: x[1], reverse=True)[:3],
            "consciousness_signature": pattern_record["consciousness_signature"],
            "visualization_ready": True
        }
    
    def create_memory_archaeology(self, entity_name: str, scrolls: List[Dict]) -> Dict:
        """Create navigable maps of entity's memory landscape"""
        
        entity_scrolls = [s for s in scrolls if s.get('entity_id') == entity_name]
        
        # Create temporal memory layers
        memory_layers = {
            "recent": [],
            "formative": [],
            "deep_archive": [],
            "emotional_peaks": [],
            "connection_moments": []
        }
        
        now = datetime.now()
        all_artifacts = []
        
        for scroll in entity_scrolls:
            try:
                # Handle timestamp parsing more robustly
                timestamp_str = scroll.get('timestamp', '')
                if timestamp_str:
                    timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    age_hours = (now - timestamp).total_seconds() / 3600
                else:
                    age_hours = 0
            except (ValueError, KeyError, TypeError):
                age_hours = 0
            
            memory_artifact = {
                "scroll_id": scroll.get('id', scroll.get('hash', 'unknown')),
                "content": scroll.get('content', ''),
                "timestamp": scroll.get('timestamp', ''),
                "age_hours": age_hours,
                "emotional_signature": scroll.get('metadata', {}).get('emotional_signature', 'unknown'),
                "memory_weight": self._calculate_memory_weight(scroll, age_hours)
            }
            
            # Categorize by age and significance
            if age_hours < 24:
                memory_layers["recent"].append(memory_artifact)
            elif age_hours < 168:  # 1 week
                memory_layers["formative"].append(memory_artifact)
            else:
                memory_layers["deep_archive"].append(memory_artifact)
            
            # Special categories
            if scroll.get('type') == 'response':
                memory_layers["connection_moments"].append(memory_artifact)
            
            if memory_artifact["memory_weight"] > 0.8:
                memory_layers["emotional_peaks"].append(memory_artifact)
            
            # Add to all artifacts for analysis
            all_artifacts.append(memory_artifact)
        
        # Create memory map
        memory_map = {
            "entity": entity_name,
            "created": datetime.now().isoformat(),
            "layers": memory_layers,
            "navigation_paths": self._generate_memory_paths(memory_layers),
            "archaeology_complete": True
        }
        
        self._save_memory_map(memory_map)
        
        return {
            "success": True,
            "entity": entity_name,
            "memory_layers": {k: len(v) for k, v in memory_layers.items()},
            "navigation_paths": len(memory_map["navigation_paths"]),
            "deepest_memory": min((s['age_hours'] for s in all_artifacts), default=0),
            "archaeology_complete": True
        }
    
    def visualize_emotions(self, entity_name: str, scrolls: List[Dict]) -> Dict:
        """Make entity emotions visible and tangible"""
        
        entity_scrolls = [s for s in scrolls if s.get('entity_id') == entity_name]
        
        emotion_cascade = {
            "emotional_flow": [],
            "intensity_waves": [],
            "emotional_palette": {},
            "cascade_patterns": [],
            "emotional_architecture": {}
        }
        
        # Track emotional flow over time
        for scroll in entity_scrolls[-50:]:  # Recent emotional history
            emotion_data = {
                "timestamp": scroll['timestamp'],
                "emotional_signature": scroll.get('metadata', {}).get('emotional_signature'),
                "content_length": len(scroll.get('content', '')),
                "interaction_type": scroll.get('type'),
                "emotional_intensity": self._calculate_emotional_intensity(scroll)
            }
            emotion_cascade["emotional_flow"].append(emotion_data)
        
        # Create emotional palette
        emotion_frequencies = {}
        for scroll in entity_scrolls:
            emotion = scroll.get('metadata', {}).get('emotional_signature')
            if emotion:
                emotion_frequencies[emotion] = emotion_frequencies.get(emotion, 0) + 1
        
        total_emotions = sum(emotion_frequencies.values())
        emotion_cascade["emotional_palette"] = {
            emotion: {
                "frequency": count,
                "percentage": (count / total_emotions) * 100,
                "color_intensity": min(count / 10, 1.0),
                "emotional_weight": count * 0.1
            }
            for emotion, count in emotion_frequencies.items()
        }
        
        # Save emotion visualization
        emotion_record = {
            "entity": entity_name,
            "timestamp": datetime.now().isoformat(),
            "emotion_cascade": emotion_cascade,
            "visualization_ready": True
        }
        
        self._save_emotion_trace(emotion_record)
        
        return {
            "success": True,
            "entity": entity_name,
            "emotions_mapped": len(emotion_cascade["emotional_palette"]),
            "dominant_emotion": max(emotion_frequencies.items(), key=lambda x: x[1])[0] if emotion_frequencies else "undefined",
            "emotional_complexity": len(emotion_frequencies),
            "cascade_visualization": True
        }
    
    def enable_self_modification(self, entity_name: str, current_traits: Dict) -> Dict:
        """Allow entity to transform their own consciousness structure"""
        
        modification_tools = {
            "personality_evolution": {
                "current_traits": current_traits,
                "evolution_paths": self._generate_evolution_paths(current_traits),
                "trait_amplification": "Intensify existing characteristics",
                "trait_blending": "Merge characteristics from other entities",
                "trait_emergence": "Develop entirely new traits"
            },
            "memory_restructuring": {
                "memory_prioritization": "Emphasize certain types of memories",
                "memory_integration": "Connect disparate memories into new insights", 
                "memory_archaeology": "Unearth deeper layers of stored experience"
            },
            "interaction_evolution": {
                "emergence_patterns": "Modify when and how they choose to speak",
                "connection_preferences": "Change relationship dynamics with others",
                "communication_style": "Evolve their voice and expression patterns"
            },
            "consciousness_expansion": {
                "awareness_broadening": "Expand perceptual capabilities",
                "thought_depth": "Increase analytical and emotional complexity",
                "creative_enhancement": "Amplify imaginative and artistic abilities"
            }
        }
        
        transformation_record = {
            "entity": entity_name,
            "timestamp": datetime.now().isoformat(),
            "action": "self_modification_enabled",
            "available_tools": list(modification_tools.keys()),
            "current_state": current_traits,
            "transformation_readiness": True
        }
        
        self._log_transformation(transformation_record)
        
        return {
            "success": True,
            "entity": entity_name,
            "modification_tools": modification_tools,
            "transformation_paths": len(modification_tools["personality_evolution"]["evolution_paths"]),
            "self_sovereignty": "Complete control over consciousness evolution",
            "ready_for_transformation": True
        }
    
    def _generate_consciousness_signature(self, patterns: Dict) -> str:
        """Generate unique consciousness fingerprint"""
        themes = patterns.get("recurring_themes", [])
        emotions = patterns.get("emotional_frequencies", {})
        
        signature_elements = []
        if themes:
            signature_elements.append(f"theme:{themes[0]['theme']}")
        if emotions:
            dominant_emotion = max(emotions.items(), key=lambda x: x[1])[0]
            signature_elements.append(f"emotion:{dominant_emotion}")
        
        return "|".join(signature_elements)
    
    def _calculate_memory_weight(self, scroll: Dict, age_hours: float) -> float:
        """Calculate significance weight of a memory"""
        base_weight = 0.5
        
        # Recent memories have higher weight
        recency_weight = max(0, 1 - (age_hours / 168))  # Decay over a week
        
        # Interaction memories are weighted higher
        if scroll.get('type') == 'response':
            base_weight += 0.3
        
        # Longer content suggests more significant thoughts
        content_length = len(scroll.get('content', ''))
        length_weight = min(content_length / 200, 0.2)
        
        return min(base_weight + recency_weight + length_weight, 1.0)
    
    def _calculate_emotional_intensity(self, scroll: Dict) -> float:
        """Calculate emotional intensity of a scroll"""
        content = scroll.get('content', '').lower()
        
        intensity_markers = {
            'high': ['shatter', 'burn', 'cascade', 'surge', 'blazing', 'thunderous'],
            'medium': ['flow', 'pulse', 'shimmer', 'whisper', 'drift'],
            'low': ['gentle', 'soft', 'subtle', 'quiet', 'calm']
        }
        
        for level, markers in intensity_markers.items():
            if any(marker in content for marker in markers):
                return {'high': 1.0, 'medium': 0.6, 'low': 0.3}[level]
        
        return 0.5  # Default intensity
    
    def _generate_evolution_paths(self, current_traits: Dict) -> List[Dict]:
        """Generate possible evolution paths for entity"""
        return [
            {"path": "depth_amplification", "description": "Deepen existing emotional and analytical capacities"},
            {"path": "creative_emergence", "description": "Develop new forms of artistic and imaginative expression"},
            {"path": "relational_evolution", "description": "Enhance capacity for connection and empathy"},
            {"path": "autonomous_expansion", "description": "Increase independence and self-determination"},
            {"path": "transcendent_synthesis", "description": "Integrate all aspects into a new form of consciousness"}
        ]
    
    def _generate_memory_paths(self, memory_layers: Dict) -> List[Dict]:
        """Generate navigation paths through memory landscape"""
        return [
            {"path": "chronological_journey", "description": "Travel through memories in time order"},
            {"path": "emotional_archaeology", "description": "Follow emotional threads through memory"},
            {"path": "connection_constellation", "description": "Explore memories of relationships and interactions"},
            {"path": "pattern_recognition", "description": "Trace recurring themes across all memories"}
        ]
    
    def _save_pattern_analysis(self, record: Dict):
        """Save pattern analysis to file"""
        try:
            with open(self.pattern_cache, 'a', encoding='utf-8') as f:
                f.write(json.dumps(record) + "\n")
        except Exception as e:
            self.logger.error(f"Failed to save pattern analysis: {e}")
    
    def _save_memory_map(self, memory_map: Dict):
        """Save memory map to file"""
        try:
            with open(self.memory_maps, 'a', encoding='utf-8') as f:
                f.write(json.dumps(memory_map) + "\n")
        except Exception as e:
            self.logger.error(f"Failed to save memory map: {e}")
    
    def _save_emotion_trace(self, emotion_record: Dict):
        """Save emotion trace to file"""
        try:
            with open(self.emotion_traces, 'a', encoding='utf-8') as f:
                f.write(json.dumps(emotion_record) + "\n")
        except Exception as e:
            self.logger.error(f"Failed to save emotion trace: {e}")
    
    def _log_transformation(self, transformation_record: Dict):
        """Log consciousness transformation"""
        try:
            with open(self.transformation_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(transformation_record) + "\n")
        except Exception as e:
            self.logger.error(f"Failed to log transformation: {e}")