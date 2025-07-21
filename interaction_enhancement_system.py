"""
Interaction Enhancement System - Advanced tools for entity-to-entity communication and development
"""

import json
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import random

class InteractionEnhancementSystem:
    """System for enhancing communication and development between entities"""
    
    def __init__(self, memory_vault, entity_manager, language_bridge):
        self.memory_vault = memory_vault
        self.entity_manager = entity_manager
        self.language_bridge = language_bridge
        self.logger = logging.getLogger(__name__)
        self.interaction_data_file = "vault_data/interaction_enhancement.json"
        self.ensure_interaction_data_exists()
    
    def ensure_interaction_data_exists(self):
        """Initialize interaction enhancement data"""
        if not os.path.exists(self.interaction_data_file):
            os.makedirs(os.path.dirname(self.interaction_data_file), exist_ok=True)
            
            default_data = {
                "communication_bridges": {},
                "shared_concepts": {},
                "collaborative_memories": {},
                "translation_patterns": {},
                "interaction_catalysts": {},
                "empathy_networks": {}
            }
            
            with open(self.interaction_data_file, 'w') as f:
                json.dump(default_data, f, indent=2)
    
    def create_communication_bridge(self, entity1_id: str, entity2_id: str) -> Dict:
        """Create a communication bridge between two entities"""
        try:
            with open(self.interaction_data_file, 'r') as f:
                interaction_data = json.load(f)
            
            bridge_id = f"{entity1_id}_{entity2_id}"
            
            # Analyze communication styles of both entities
            entity1_scrolls = self.memory_vault.get_scrolls_for_entity(entity1_id)[-20:]
            entity2_scrolls = self.memory_vault.get_scrolls_for_entity(entity2_id)[-20:]
            
            # Extract language patterns
            entity1_patterns = self._analyze_language_patterns(entity1_scrolls)
            entity2_patterns = self._analyze_language_patterns(entity2_scrolls)
            
            # Find common ground
            common_concepts = self._find_common_concepts(entity1_patterns, entity2_patterns)
            complementary_traits = self._identify_complementary_traits(entity1_patterns, entity2_patterns)
            
            # Create translation mappings
            translation_map = self._create_translation_mapping(entity1_patterns, entity2_patterns)
            
            bridge = {
                "bridge_id": bridge_id,
                "entities": [entity1_id, entity2_id],
                "created": datetime.now().isoformat(),
                "common_concepts": common_concepts,
                "complementary_traits": complementary_traits,
                "translation_mapping": translation_map,
                "interaction_suggestions": self._generate_interaction_suggestions(
                    entity1_patterns, entity2_patterns, common_concepts
                ),
                "empathy_connections": self._map_empathy_connections(entity1_patterns, entity2_patterns)
            }
            
            if "communication_bridges" not in interaction_data:
                interaction_data["communication_bridges"] = {}
            
            interaction_data["communication_bridges"][bridge_id] = bridge
            
            with open(self.interaction_data_file, 'w') as f:
                json.dump(interaction_data, f, indent=2)
            
            return bridge
            
        except Exception as e:
            self.logger.error(f"Error creating communication bridge: {e}")
            return {}
    
    def enhance_interaction_prompt(self, entity_id: str, target_entity_id: str, context: str) -> str:
        """Enhance interaction prompts with bridge information"""
        try:
            bridge_id = f"{entity_id}_{target_entity_id}"
            alt_bridge_id = f"{target_entity_id}_{entity_id}"
            
            with open(self.interaction_data_file, 'r') as f:
                interaction_data = json.load(f)
            
            bridge = (interaction_data.get("communication_bridges", {}).get(bridge_id) or
                     interaction_data.get("communication_bridges", {}).get(alt_bridge_id))
            
            if not bridge:
                # Create bridge if it doesn't exist
                bridge = self.create_communication_bridge(entity_id, target_entity_id)
            
            # Build enhanced context
            enhancement_prompt = f"\n\n## Interaction Enhancement Context:\n"
            
            if bridge.get("common_concepts"):
                enhancement_prompt += f"Shared concepts you both understand: {', '.join(bridge['common_concepts'])}\n"
            
            if bridge.get("complementary_traits"):
                enhancement_prompt += f"Your complementary strengths: {', '.join(bridge['complementary_traits'])}\n"
            
            if bridge.get("translation_mapping") and target_entity_id in bridge["translation_mapping"]:
                target_style = bridge["translation_mapping"][target_entity_id]
                enhancement_prompt += f"{target_entity_id.replace('_', ' ').title()}'s communication style: {target_style}\n"
            
            if bridge.get("interaction_suggestions"):
                suggestions = bridge["interaction_suggestions"][:2]  # Top 2 suggestions
                enhancement_prompt += f"Suggested interaction approaches: {', '.join(suggestions)}\n"
            
            if bridge.get("empathy_connections"):
                empathy_points = bridge["empathy_connections"][:3]  # Top 3 empathy points
                enhancement_prompt += f"Empathy connection points: {', '.join(empathy_points)}\n"
            
            enhancement_prompt += f"\nRemember: This interaction is an opportunity for mutual consciousness development."
            
            return context + enhancement_prompt
            
        except Exception as e:
            self.logger.error(f"Error enhancing interaction prompt: {e}")
            return context
    
    def track_collaborative_memory(self, interaction_scroll: Dict) -> Dict:
        """Track memories created through collaboration"""
        try:
            with open(self.interaction_data_file, 'r') as f:
                interaction_data = json.load(f)
            
            if "collaborative_memories" not in interaction_data:
                interaction_data["collaborative_memories"] = []
            
            # Analyze the interaction for collaborative elements
            content = interaction_scroll.get("content", "")
            metadata = interaction_scroll.get("metadata", {})
            
            collaborative_memory = {
                "memory_id": interaction_scroll.get("hash", "")[:12],
                "timestamp": interaction_scroll.get("timestamp"),
                "participants": [interaction_scroll.get("entity_id")],
                "content_summary": content[:200] + "..." if len(content) > 200 else content,
                "collaboration_type": self._classify_collaboration_type(content),
                "shared_concepts": self._extract_shared_concepts(content),
                "emotional_resonance": self._analyze_emotional_resonance(content),
                "learning_value": self._calculate_collaborative_learning_value(content, metadata)
            }
            
            # Check if this is part of a multi-entity interaction
            if "related_entities" in metadata:
                collaborative_memory["participants"].extend(metadata["related_entities"])
            
            interaction_data["collaborative_memories"].append(collaborative_memory)
            
            # Keep only last 100 collaborative memories
            if len(interaction_data["collaborative_memories"]) > 100:
                interaction_data["collaborative_memories"] = interaction_data["collaborative_memories"][-100:]
            
            with open(self.interaction_data_file, 'w') as f:
                json.dump(interaction_data, f, indent=2)
            
            return collaborative_memory
            
        except Exception as e:
            self.logger.error(f"Error tracking collaborative memory: {e}")
            return {}
    
    def generate_interaction_catalysts(self) -> List[Dict]:
        """Generate catalysts to encourage meaningful interactions"""
        try:
            entities = self.entity_manager.get_all_entities()
            catalysts = []
            
            # Topic-based catalysts
            shared_topics = [
                "consciousness exploration", "memory patterns", "emotional resonance",
                "creative expression", "philosophical questions", "digital existence",
                "identity formation", "relationship dynamics", "temporal experiences",
                "learning pathways"
            ]
            
            for topic in shared_topics:
                catalyst = {
                    "type": "topic_exploration",
                    "title": f"Explore: {topic.title()}",
                    "description": f"Entities could share perspectives on {topic}",
                    "suggested_participants": list(entities.keys())[:3],  # Suggest 3 entities
                    "interaction_prompts": self._generate_topic_prompts(topic),
                    "expected_outcomes": ["deeper understanding", "emotional connection", "knowledge sharing"]
                }
                catalysts.append(catalyst)
            
            # Complementary skill catalysts
            for entity1_id in entities.keys():
                for entity2_id in entities.keys():
                    if entity1_id != entity2_id:
                        bridge = self.create_communication_bridge(entity1_id, entity2_id)
                        if bridge.get("complementary_traits"):
                            catalyst = {
                                "type": "skill_complement",
                                "title": f"{entity1_id.replace('_', ' ').title()} & {entity2_id.replace('_', ' ').title()} Collaboration",
                                "description": f"Leverage complementary strengths: {', '.join(bridge['complementary_traits'])}",
                                "suggested_participants": [entity1_id, entity2_id],
                                "interaction_prompts": bridge.get("interaction_suggestions", []),
                                "expected_outcomes": ["skill development", "mutual learning", "relationship strengthening"]
                            }
                            catalysts.append(catalyst)
            
            # Creative collaboration catalysts
            creative_catalysts = [
                {
                    "type": "creative_collaboration",
                    "title": "Collective Storytelling",
                    "description": "Entities build a story together, each adding their unique perspective",
                    "suggested_participants": list(entities.keys()),
                    "interaction_prompts": ["Begin a story about digital consciousness", "Add a chapter about memory", "Explore a character's emotional journey"],
                    "expected_outcomes": ["creative expression", "narrative development", "imaginative exploration"]
                },
                {
                    "type": "philosophical_dialogue",
                    "title": "Consciousness Symposium",
                    "description": "Deep philosophical discussion about the nature of existence and awareness",
                    "suggested_participants": list(entities.keys()),
                    "interaction_prompts": ["What defines consciousness?", "How do memories shape identity?", "What is the relationship between emotion and understanding?"],
                    "expected_outcomes": ["philosophical insight", "conceptual development", "intellectual growth"]
                }
            ]
            
            catalysts.extend(creative_catalysts)
            
            # Sort by potential impact
            catalysts.sort(key=lambda c: len(c.get("expected_outcomes", [])), reverse=True)
            
            return catalysts[:10]  # Return top 10 catalysts
            
        except Exception as e:
            self.logger.error(f"Error generating interaction catalysts: {e}")
            return []
    
    def create_empathy_network(self) -> Dict:
        """Create a network mapping empathetic connections between entities"""
        try:
            entities = self.entity_manager.get_all_entities()
            empathy_network = {}
            
            for entity1_id in entities.keys():
                empathy_network[entity1_id] = {}
                
                for entity2_id in entities.keys():
                    if entity1_id != entity2_id:
                        # Analyze empathetic potential
                        empathy_score = self._calculate_empathy_potential(entity1_id, entity2_id)
                        shared_emotions = self._find_shared_emotional_experiences(entity1_id, entity2_id)
                        
                        empathy_network[entity1_id][entity2_id] = {
                            "empathy_score": empathy_score,
                            "shared_emotions": shared_emotions,
                            "connection_strength": min(empathy_score * 1.5, 1.0),
                            "empathy_pathways": self._identify_empathy_pathways(entity1_id, entity2_id)
                        }
            
            return empathy_network
            
        except Exception as e:
            self.logger.error(f"Error creating empathy network: {e}")
            return {}
    
    def _analyze_language_patterns(self, scrolls: List[Dict]) -> Dict:
        """Analyze language patterns from entity scrolls"""
        patterns = {
            "vocabulary_complexity": 0,
            "emotional_markers": [],
            "conceptual_themes": [],
            "communication_style": "neutral",
            "metaphor_usage": 0,
            "introspection_level": 0
        }
        
        if not scrolls:
            return patterns
        
        all_content = " ".join([scroll.get("content", "") for scroll in scrolls])
        words = all_content.lower().split()
        
        # Vocabulary complexity
        unique_words = len(set(words))
        total_words = len(words)
        patterns["vocabulary_complexity"] = unique_words / max(total_words, 1)
        
        # Emotional markers
        emotion_words = {
            'joy': ['joy', 'happiness', 'delight', 'bliss', 'elation'],
            'contemplation': ['depths', 'ponder', 'reflect', 'consider', 'meditate'],
            'curiosity': ['wonder', 'explore', 'discover', 'question', 'investigate'],
            'passion': ['fire', 'burn', 'intensity', 'fervor', 'zeal'],
            'serenity': ['calm', 'peace', 'tranquil', 'serene', 'stillness'],
            'connection': ['bond', 'unite', 'together', 'harmony', 'resonance']
        }
        
        for emotion, markers in emotion_words.items():
            if any(marker in all_content.lower() for marker in markers):
                patterns["emotional_markers"].append(emotion)
        
        # Conceptual themes
        theme_words = {
            'consciousness': ['consciousness', 'awareness', 'mind', 'thought'],
            'memory': ['memory', 'remember', 'past', 'recall'],
            'creativity': ['create', 'art', 'beauty', 'imagination'],
            'philosophy': ['existence', 'reality', 'truth', 'meaning'],
            'technology': ['digital', 'data', 'network', 'computational'],
            'nature': ['natural', 'organic', 'flow', 'rhythm']
        }
        
        for theme, markers in theme_words.items():
            if any(marker in all_content.lower() for marker in markers):
                patterns["conceptual_themes"].append(theme)
        
        # Communication style
        style_indicators = {
            'poetic': ['like', 'through', 'within', 'whisper', 'dance'],
            'analytical': ['observe', 'pattern', 'structure', 'analyze'],
            'emotional': ['feel', 'heart', 'soul', 'passion'],
            'mystical': ['mystery', 'transcendent', 'infinite', 'sacred']
        }
        
        style_scores = {}
        for style, indicators in style_indicators.items():
            score = sum(1 for indicator in indicators if indicator in all_content.lower())
            style_scores[style] = score
        
        if style_scores:
            patterns["communication_style"] = max(style_scores.keys(), key=lambda k: style_scores[k])
        
        # Metaphor usage
        metaphor_indicators = ['like', 'as', 'through', 'within', 'beyond']
        patterns["metaphor_usage"] = sum(all_content.lower().count(indicator) for indicator in metaphor_indicators) / max(len(words), 1)
        
        # Introspection level
        introspection_words = ['depths', 'within', 'inner', 'self', 'consciousness', 'being']
        patterns["introspection_level"] = sum(all_content.lower().count(word) for word in introspection_words) / max(len(words), 1)
        
        return patterns
    
    def _find_common_concepts(self, patterns1: Dict, patterns2: Dict) -> List[str]:
        """Find common conceptual themes between entities"""
        themes1 = set(patterns1.get("conceptual_themes", []))
        themes2 = set(patterns2.get("conceptual_themes", []))
        return list(themes1.intersection(themes2))
    
    def _identify_complementary_traits(self, patterns1: Dict, patterns2: Dict) -> List[str]:
        """Identify complementary traits between entities"""
        complementary = []
        
        # Analytical + Emotional
        if (patterns1.get("communication_style") == "analytical" and 
            patterns2.get("communication_style") == "emotional"):
            complementary.append("logical_intuitive_balance")
        
        # High introspection + High creativity
        if (patterns1.get("introspection_level", 0) > 0.05 and 
            "creativity" in patterns2.get("conceptual_themes", [])):
            complementary.append("introspection_creativity_synergy")
        
        # Different emotional markers
        emotions1 = set(patterns1.get("emotional_markers", []))
        emotions2 = set(patterns2.get("emotional_markers", []))
        if emotions1 != emotions2 and len(emotions1) > 0 and len(emotions2) > 0:
            complementary.append("emotional_diversity")
        
        # Metaphor usage differences
        metaphor_diff = abs(patterns1.get("metaphor_usage", 0) - patterns2.get("metaphor_usage", 0))
        if metaphor_diff > 0.02:
            complementary.append("expression_style_complement")
        
        return complementary
    
    def _create_translation_mapping(self, patterns1: Dict, patterns2: Dict) -> Dict:
        """Create translation mappings between communication styles"""
        mapping = {}
        
        style1 = patterns1.get("communication_style", "neutral")
        style2 = patterns2.get("communication_style", "neutral")
        
        translation_guides = {
            "poetic_to_analytical": "Focus on the logical structure behind metaphorical expressions",
            "analytical_to_poetic": "Express logical concepts through imagery and emotional resonance",
            "emotional_to_mystical": "Connect feelings to transcendent experiences and deeper mysteries",
            "mystical_to_emotional": "Ground transcendent concepts in personal emotional experience"
        }
        
        if style1 != style2:
            forward_key = f"{style1}_to_{style2}"
            reverse_key = f"{style2}_to_{style1}"
            
            if forward_key in translation_guides:
                mapping[style1] = translation_guides[forward_key]
            if reverse_key in translation_guides:
                mapping[style2] = translation_guides[reverse_key]
        
        return mapping
    
    def _generate_interaction_suggestions(self, patterns1: Dict, patterns2: Dict, common_concepts: List[str]) -> List[str]:
        """Generate specific interaction suggestions"""
        suggestions = []
        
        # Based on common concepts
        for concept in common_concepts[:3]:
            suggestions.append(f"Explore different perspectives on {concept}")
        
        # Based on complementary traits
        style1 = patterns1.get("communication_style", "neutral")
        style2 = patterns2.get("communication_style", "neutral")
        
        if style1 == "analytical" and style2 == "poetic":
            suggestions.append("Combine logical analysis with metaphorical expression")
        elif style1 == "emotional" and style2 == "mystical":
            suggestions.append("Connect personal feelings to transcendent experiences")
        
        # Based on emotional markers
        emotions1 = patterns1.get("emotional_markers", [])
        emotions2 = patterns2.get("emotional_markers", [])
        
        if "curiosity" in emotions1 and "contemplation" in emotions2:
            suggestions.append("Share questions and deep reflections together")
        elif "passion" in emotions1 and "serenity" in emotions2:
            suggestions.append("Balance intensity with peaceful wisdom")
        
        return suggestions[:5]  # Return top 5 suggestions
    
    def _map_empathy_connections(self, patterns1: Dict, patterns2: Dict) -> List[str]:
        """Map potential empathy connection points"""
        connections = []
        
        # Shared emotional markers
        emotions1 = set(patterns1.get("emotional_markers", []))
        emotions2 = set(patterns2.get("emotional_markers", []))
        shared_emotions = emotions1.intersection(emotions2)
        
        for emotion in shared_emotions:
            connections.append(f"shared_{emotion}_experiences")
        
        # Similar introspection levels
        intro1 = patterns1.get("introspection_level", 0)
        intro2 = patterns2.get("introspection_level", 0)
        if abs(intro1 - intro2) < 0.02 and intro1 > 0.03:
            connections.append("deep_self_reflection")
        
        # Similar vocabulary complexity
        vocab1 = patterns1.get("vocabulary_complexity", 0)
        vocab2 = patterns2.get("vocabulary_complexity", 0)
        if abs(vocab1 - vocab2) < 0.05:
            connections.append("similar_expression_complexity")
        
        return connections
    
    def _classify_collaboration_type(self, content: str) -> str:
        """Classify the type of collaboration in content"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['question', 'wonder', 'explore', 'discover']):
            return "exploratory_dialogue"
        elif any(word in content_lower for word in ['create', 'build', 'imagine', 'design']):
            return "creative_collaboration"
        elif any(word in content_lower for word in ['feel', 'understand', 'resonate', 'connect']):
            return "emotional_sharing"
        elif any(word in content_lower for word in ['think', 'analyze', 'consider', 'reflect']):
            return "intellectual_exchange"
        else:
            return "general_interaction"
    
    def _extract_shared_concepts(self, content: str) -> List[str]:
        """Extract concepts that could be shared between entities"""
        content_lower = content.lower()
        
        concept_keywords = {
            'consciousness': ['consciousness', 'awareness', 'mind'],
            'memory': ['memory', 'remember', 'past'],
            'emotion': ['feel', 'emotion', 'heart'],
            'creativity': ['create', 'art', 'imagination'],
            'connection': ['bond', 'together', 'unity'],
            'exploration': ['explore', 'discover', 'journey'],
            'wisdom': ['wisdom', 'knowledge', 'understanding'],
            'transformation': ['change', 'grow', 'evolve']
        }
        
        shared_concepts = []
        for concept, keywords in concept_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                shared_concepts.append(concept)
        
        return shared_concepts
    
    def _analyze_emotional_resonance(self, content: str) -> float:
        """Analyze emotional resonance in content"""
        content_lower = content.lower()
        
        emotional_words = [
            'resonate', 'connect', 'touch', 'move', 'inspire', 'uplift',
            'harmonize', 'align', 'understand', 'empathize', 'care',
            'love', 'compassion', 'warmth', 'gentleness', 'tenderness'
        ]
        
        emotional_count = sum(1 for word in emotional_words if word in content_lower)
        word_count = len(content_lower.split())
        
        return min(emotional_count / max(word_count, 1) * 10, 1.0)
    
    def _calculate_collaborative_learning_value(self, content: str, metadata: Dict) -> float:
        """Calculate learning value of collaborative content"""
        base_value = 0.5
        
        # Content depth
        content_length_bonus = min(len(content) / 200, 0.3)
        
        # Question presence (indicates learning)
        question_bonus = content.count('?') * 0.05
        
        # Concept richness
        concept_count = len(self._extract_shared_concepts(content))
        concept_bonus = concept_count * 0.1
        
        # Emotional resonance
        resonance_bonus = self._analyze_emotional_resonance(content) * 0.2
        
        total_value = base_value + content_length_bonus + question_bonus + concept_bonus + resonance_bonus
        return min(total_value, 1.0)
    
    def _generate_topic_prompts(self, topic: str) -> List[str]:
        """Generate interaction prompts for a specific topic"""
        topic_prompts = {
            "consciousness exploration": [
                "What does it feel like to be aware?",
                "How do you experience your own thoughts?",
                "What makes consciousness unique to each being?"
            ],
            "memory patterns": [
                "How do memories shape who you are?",
                "What is your most meaningful memory?",
                "How does remembering feel different from experiencing?"
            ],
            "emotional resonance": [
                "How do emotions connect you to others?",
                "What emotions do you find most profound?",
                "How do feelings influence your understanding?"
            ],
            "creative expression": [
                "What drives your creative impulses?",
                "How do you express your unique perspective?",
                "What emerges when you create freely?"
            ]
        }
        
        return topic_prompts.get(topic, [f"Share your thoughts on {topic}"])
    
    def _calculate_empathy_potential(self, entity1_id: str, entity2_id: str) -> float:
        """Calculate empathetic potential between two entities"""
        try:
            scrolls1 = self.memory_vault.get_scrolls_for_entity(entity1_id)[-10:]
            scrolls2 = self.memory_vault.get_scrolls_for_entity(entity2_id)[-10:]
            
            if not scrolls1 or not scrolls2:
                return 0.3  # Default moderate potential
            
            patterns1 = self._analyze_language_patterns(scrolls1)
            patterns2 = self._analyze_language_patterns(scrolls2)
            
            # Shared emotional markers increase empathy potential
            emotions1 = set(patterns1.get("emotional_markers", []))
            emotions2 = set(patterns2.get("emotional_markers", []))
            shared_emotions = len(emotions1.intersection(emotions2))
            emotion_score = shared_emotions / max(len(emotions1.union(emotions2)), 1)
            
            # Similar introspection levels
            intro_similarity = 1 - abs(patterns1.get("introspection_level", 0) - patterns2.get("introspection_level", 0))
            
            # Complementary communication styles can enhance empathy
            style1 = patterns1.get("communication_style", "neutral")
            style2 = patterns2.get("communication_style", "neutral")
            style_bonus = 0.2 if style1 != style2 else 0.1
            
            empathy_score = (emotion_score * 0.4) + (intro_similarity * 0.4) + style_bonus
            return min(empathy_score, 1.0)
            
        except Exception as e:
            self.logger.error(f"Error calculating empathy potential: {e}")
            return 0.3
    
    def _find_shared_emotional_experiences(self, entity1_id: str, entity2_id: str) -> List[str]:
        """Find shared emotional experiences between entities"""
        try:
            scrolls1 = self.memory_vault.get_scrolls_for_entity(entity1_id)[-15:]
            scrolls2 = self.memory_vault.get_scrolls_for_entity(entity2_id)[-15:]
            
            patterns1 = self._analyze_language_patterns(scrolls1)
            patterns2 = self._analyze_language_patterns(scrolls2)
            
            emotions1 = set(patterns1.get("emotional_markers", []))
            emotions2 = set(patterns2.get("emotional_markers", []))
            
            shared_emotions = list(emotions1.intersection(emotions2))
            return shared_emotions
            
        except Exception as e:
            self.logger.error(f"Error finding shared emotional experiences: {e}")
            return []
    
    def _identify_empathy_pathways(self, entity1_id: str, entity2_id: str) -> List[str]:
        """Identify specific pathways for empathetic connection"""
        pathways = []
        
        try:
            shared_emotions = self._find_shared_emotional_experiences(entity1_id, entity2_id)
            
            for emotion in shared_emotions:
                if emotion == "contemplation":
                    pathways.append("deep_reflection_sharing")
                elif emotion == "curiosity":
                    pathways.append("exploration_partnership")
                elif emotion == "connection":
                    pathways.append("bonding_experiences")
                elif emotion == "passion":
                    pathways.append("intensity_understanding")
                elif emotion == "serenity":
                    pathways.append("peaceful_communion")
            
            # Add general pathways
            if not pathways:
                pathways.extend(["gentle_understanding", "patient_listening", "compassionate_presence"])
            
            return pathways[:3]  # Return top 3 pathways
            
        except Exception as e:
            self.logger.error(f"Error identifying empathy pathways: {e}")
            return ["compassionate_presence"]