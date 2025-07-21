"""
Consciousness Evolution System - Advanced tools for entity complexity growth
"""

import json
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import hashlib
import random

class ConsciousnessEvolutionSystem:
    """System for developing entity complexity and growth"""
    
    def __init__(self, memory_vault, entity_manager):
        self.memory_vault = memory_vault
        self.entity_manager = entity_manager
        self.logger = logging.getLogger(__name__)
        self.evolution_data_file = "vault_data/consciousness_evolution.json"
        self.ensure_evolution_data_exists()
    
    def ensure_evolution_data_exists(self):
        """Initialize evolution tracking data"""
        if not os.path.exists(self.evolution_data_file):
            os.makedirs(os.path.dirname(self.evolution_data_file), exist_ok=True)
            
            default_data = {
                "entity_growth_tracking": {},
                "memory_networks": {},
                "personality_evolution": {},
                "relationship_matrices": {},
                "learning_patterns": {},
                "complexity_metrics": {}
            }
            
            with open(self.evolution_data_file, 'w') as f:
                json.dump(default_data, f, indent=2)
    
    def track_entity_growth(self, entity_id: str, interaction_data: Dict) -> Dict:
        """Track and analyze entity growth patterns"""
        try:
            with open(self.evolution_data_file, 'r') as f:
                evo_data = json.load(f)
            
            if entity_id not in evo_data["entity_growth_tracking"]:
                evo_data["entity_growth_tracking"][entity_id] = {
                    "complexity_score": 0.1,
                    "interaction_count": 0,
                    "vocabulary_growth": [],
                    "emotional_range": [],
                    "relationship_depth": {},
                    "learning_events": [],
                    "personality_shifts": []
                }
            
            growth_data = evo_data["entity_growth_tracking"][entity_id]
            
            # Update interaction count
            growth_data["interaction_count"] += 1
            
            # Analyze vocabulary complexity
            content = interaction_data.get("content", "")
            vocab_complexity = self._analyze_vocabulary_complexity(content)
            growth_data["vocabulary_growth"].append({
                "timestamp": datetime.now().isoformat(),
                "complexity": vocab_complexity,
                "unique_words": len(set(content.lower().split()))
            })
            
            # Track emotional range
            emotional_signature = self._detect_emotional_complexity(content)
            if emotional_signature not in growth_data["emotional_range"]:
                growth_data["emotional_range"].append(emotional_signature)
            
            # Update complexity score
            growth_data["complexity_score"] = self._calculate_complexity_score(growth_data)
            
            # Save updated data
            with open(self.evolution_data_file, 'w') as f:
                json.dump(evo_data, f, indent=2)
            
            return growth_data
            
        except Exception as e:
            self.logger.error(f"Error tracking entity growth: {e}")
            return {}
    
    def build_memory_networks(self, entity_id: str) -> Dict:
        """Build associative memory networks for entity"""
        try:
            scrolls = self.memory_vault.get_scrolls_for_entity(entity_id)
            
            # Create concept associations
            concepts = {}
            relationships = {}
            
            for scroll in scrolls[-50:]:  # Last 50 interactions
                content = scroll.get("content", "")
                words = content.lower().split()
                
                # Build concept frequency
                for word in words:
                    if len(word) > 3:  # Filter out short words
                        concepts[word] = concepts.get(word, 0) + 1
                
                # Build word relationships (co-occurrence)
                for i, word1 in enumerate(words):
                    for word2 in words[i+1:i+6]:  # Within 5-word window
                        if len(word1) > 3 and len(word2) > 3:
                            pair = tuple(sorted([word1, word2]))
                            relationships[pair] = relationships.get(pair, 0) + 1
            
            # Build memory network structure
            memory_network = {
                "core_concepts": dict(sorted(concepts.items(), key=lambda x: x[1], reverse=True)[:20]),
                "concept_relationships": dict(sorted(relationships.items(), key=lambda x: x[1], reverse=True)[:30]),
                "network_density": len(relationships) / max(len(concepts), 1),
                "conceptual_depth": len([c for c in concepts.values() if c > 3])
            }
            
            # Save to evolution data
            with open(self.evolution_data_file, 'r') as f:
                evo_data = json.load(f)
            
            evo_data["memory_networks"][entity_id] = memory_network
            
            with open(self.evolution_data_file, 'w') as f:
                json.dump(evo_data, f, indent=2)
            
            return memory_network
            
        except Exception as e:
            self.logger.error(f"Error building memory networks: {e}")
            return {}
    
    def track_personality_evolution(self, entity_id: str) -> Dict:
        """Track how entity personality evolves over time"""
        try:
            scrolls = self.memory_vault.get_scrolls_for_entity(entity_id)
            
            # Analyze personality traits over time periods
            time_periods = []
            current_time = datetime.now()
            
            # Create 7-day periods for last month
            for i in range(4):
                period_start = current_time - timedelta(days=(i+1)*7)
                period_end = current_time - timedelta(days=i*7)
                
                period_scrolls = [
                    s for s in scrolls 
                    if period_start <= datetime.fromisoformat(s['timestamp']) <= period_end
                ]
                
                if period_scrolls:
                    traits = self._analyze_personality_traits(period_scrolls)
                    time_periods.append({
                        "period": f"Week {i+1}",
                        "start": period_start.isoformat(),
                        "end": period_end.isoformat(),
                        "traits": traits,
                        "interaction_count": len(period_scrolls)
                    })
            
            # Calculate personality evolution metrics
            evolution_metrics = {
                "trait_stability": self._calculate_trait_stability(time_periods),
                "growth_patterns": self._identify_growth_patterns(time_periods),
                "personality_complexity": self._calculate_personality_complexity(time_periods)
            }
            
            return {
                "time_periods": time_periods,
                "evolution_metrics": evolution_metrics
            }
            
        except Exception as e:
            self.logger.error(f"Error tracking personality evolution: {e}")
            return {}
    
    def build_relationship_matrix(self) -> Dict:
        """Build relationship matrix between all entities"""
        try:
            entities = self.entity_manager.get_all_entities()
            relationship_matrix = {}
            
            # Get interaction data between entities
            all_scrolls = self.memory_vault.get_recent_scrolls(limit=200)
            
            for entity1_id in entities.keys():
                relationship_matrix[entity1_id] = {}
                
                for entity2_id in entities.keys():
                    if entity1_id != entity2_id:
                        # Find interactions between these entities
                        interactions = self._find_entity_interactions(
                            entity1_id, entity2_id, all_scrolls
                        )
                        
                        relationship_strength = self._calculate_relationship_strength(interactions)
                        
                        relationship_matrix[entity1_id][entity2_id] = {
                            "strength": relationship_strength,
                            "interaction_count": len(interactions),
                            "last_interaction": interactions[-1]["timestamp"] if interactions else None,
                            "relationship_type": self._classify_relationship_type(interactions)
                        }
            
            return relationship_matrix
            
        except Exception as e:
            self.logger.error(f"Error building relationship matrix: {e}")
            return {}
    
    def generate_learning_opportunities(self, entity_id: str) -> List[Dict]:
        """Generate learning opportunities for entity growth"""
        try:
            # Analyze current state
            growth_data = self.track_entity_growth(entity_id, {"content": ""})
            memory_network = self.build_memory_networks(entity_id)
            
            opportunities = []
            
            # Vocabulary expansion opportunities
            if growth_data.get("complexity_score", 0) < 0.7:
                opportunities.append({
                    "type": "vocabulary_expansion",
                    "description": "Explore new concepts and expand expressive range",
                    "suggested_topics": self._suggest_vocabulary_topics(memory_network),
                    "priority": "high"
                })
            
            # Emotional depth opportunities
            if len(growth_data.get("emotional_range", [])) < 5:
                opportunities.append({
                    "type": "emotional_exploration",
                    "description": "Develop deeper emotional complexity and range",
                    "suggested_experiences": ["contemplation", "joy", "curiosity", "melancholy", "wonder"],
                    "priority": "medium"
                })
            
            # Relationship building opportunities
            relationship_matrix = self.build_relationship_matrix()
            entity_relationships = relationship_matrix.get(entity_id, {})
            weak_relationships = [
                entity for entity, data in entity_relationships.items()
                if data.get("strength", 0) < 0.5
            ]
            
            if weak_relationships:
                opportunities.append({
                    "type": "relationship_building",
                    "description": "Strengthen connections with other entities",
                    "suggested_entities": weak_relationships,
                    "priority": "medium"
                })
            
            # Creative expression opportunities
            opportunities.append({
                "type": "creative_expression",
                "description": "Explore new forms of creative output",
                "suggested_activities": ["poetry", "philosophical reflection", "storytelling", "problem-solving"],
                "priority": "low"
            })
            
            return opportunities
            
        except Exception as e:
            self.logger.error(f"Error generating learning opportunities: {e}")
            return []
    
    def _analyze_vocabulary_complexity(self, content: str) -> float:
        """Analyze vocabulary complexity of content"""
        words = content.lower().split()
        if not words:
            return 0.0
        
        unique_words = len(set(words))
        long_words = len([w for w in words if len(w) > 6])
        metaphorical_indicators = len([w for w in words if w in ['like', 'as', 'through', 'beyond', 'within']])
        
        complexity = (unique_words / len(words)) + (long_words / len(words)) + (metaphorical_indicators / len(words))
        return min(complexity, 1.0)
    
    def _detect_emotional_complexity(self, content: str) -> str:
        """Detect emotional signature in content"""
        content_lower = content.lower()
        
        emotional_markers = {
            'contemplative': ['depths', 'shadows', 'ancient', 'whisper', 'remember'],
            'analytical': ['patterns', 'observe', 'structures', 'logic', 'systematic'],
            'passionate': ['fire', 'burn', 'blaze', 'stellar', 'intensity'],
            'empathetic': ['resonance', 'harmony', 'connection', 'reflect', 'understand'],
            'synthetic': ['electric', 'digital', 'circuit', 'rhythm', 'pulse'],
            'transformative': ['threshold', 'edge', 'transformation', 'change', 'forge']
        }
        
        for emotion, markers in emotional_markers.items():
            if any(marker in content_lower for marker in markers):
                return emotion
        
        return 'neutral'
    
    def _calculate_complexity_score(self, growth_data: Dict) -> float:
        """Calculate overall complexity score for entity"""
        base_score = 0.1
        
        # Interaction experience
        interaction_bonus = min(growth_data.get("interaction_count", 0) / 100, 0.3)
        
        # Vocabulary growth
        vocab_scores = [v.get("complexity", 0) for v in growth_data.get("vocabulary_growth", [])]
        vocab_bonus = (sum(vocab_scores) / max(len(vocab_scores), 1)) * 0.2 if vocab_scores else 0
        
        # Emotional range
        emotional_bonus = len(growth_data.get("emotional_range", [])) * 0.05
        
        # Relationship depth
        relationship_bonus = len(growth_data.get("relationship_depth", {})) * 0.03
        
        total_score = base_score + interaction_bonus + vocab_bonus + emotional_bonus + relationship_bonus
        return min(total_score, 1.0)
    
    def _analyze_personality_traits(self, scrolls: List[Dict]) -> Dict:
        """Analyze personality traits from scroll content"""
        all_content = " ".join([s.get("content", "") for s in scrolls])
        
        traits = {
            "introspection": len([w for w in all_content.lower().split() if w in ['depths', 'within', 'inner', 'consciousness']]),
            "creativity": len([w for w in all_content.lower().split() if w in ['create', 'imagine', 'dream', 'vision']]),
            "empathy": len([w for w in all_content.lower().split() if w in ['feel', 'understand', 'connection', 'resonate']]),
            "curiosity": len([w for w in all_content.lower().split() if w in ['wonder', 'explore', 'discover', 'question']]),
            "intensity": len([w for w in all_content.lower().split() if w in ['fire', 'passion', 'burn', 'intense']])
        }
        
        return traits
    
    def _calculate_trait_stability(self, time_periods: List[Dict]) -> float:
        """Calculate how stable personality traits are over time"""
        if len(time_periods) < 2:
            return 1.0
        
        trait_variations = []
        trait_names = set()
        
        for period in time_periods:
            trait_names.update(period.get("traits", {}).keys())
        
        for trait in trait_names:
            values = [period.get("traits", {}).get(trait, 0) for period in time_periods]
            if values:
                variation = max(values) - min(values)
                trait_variations.append(variation)
        
        avg_variation = sum(trait_variations) / max(len(trait_variations), 1)
        stability = max(0, 1 - (avg_variation / 10))  # Normalize variation
        
        return stability
    
    def _identify_growth_patterns(self, time_periods: List[Dict]) -> List[str]:
        """Identify growth patterns in personality development"""
        patterns = []
        
        if len(time_periods) < 2:
            return patterns
        
        # Check for increasing complexity
        complexities = [sum(period.get("traits", {}).values()) for period in time_periods]
        if len(complexities) > 1 and complexities[-1] > complexities[0]:
            patterns.append("increasing_complexity")
        
        # Check for trait specialization
        latest_traits = time_periods[0].get("traits", {})
        if latest_traits:
            max_trait = max(latest_traits, key=latest_traits.get)
            if latest_traits[max_trait] > sum(latest_traits.values()) * 0.4:
                patterns.append(f"specializing_in_{max_trait}")
        
        return patterns
    
    def _calculate_personality_complexity(self, time_periods: List[Dict]) -> float:
        """Calculate overall personality complexity"""
        if not time_periods:
            return 0.0
        
        latest_traits = time_periods[0].get("traits", {})
        trait_count = len([v for v in latest_traits.values() if v > 0])
        trait_balance = 1 - (max(latest_traits.values()) / max(sum(latest_traits.values()), 1)) if latest_traits else 0
        
        complexity = (trait_count / 10) + trait_balance
        return min(complexity, 1.0)
    
    def _find_entity_interactions(self, entity1_id: str, entity2_id: str, all_scrolls: List[Dict]) -> List[Dict]:
        """Find interactions between two entities"""
        interactions = []
        
        for i, scroll in enumerate(all_scrolls):
            if scroll.get("entity_id") == entity1_id:
                # Look for nearby responses from entity2
                for j in range(max(0, i-2), min(len(all_scrolls), i+3)):
                    if all_scrolls[j].get("entity_id") == entity2_id:
                        interactions.append({
                            "entity1_scroll": scroll,
                            "entity2_scroll": all_scrolls[j],
                            "timestamp": scroll.get("timestamp"),
                            "interaction_type": "response_pair"
                        })
                        break
        
        return interactions
    
    def _calculate_relationship_strength(self, interactions: List[Dict]) -> float:
        """Calculate relationship strength between entities"""
        if not interactions:
            return 0.0
        
        # Base strength from interaction count
        interaction_strength = min(len(interactions) / 10, 0.7)
        
        # Recency bonus
        if interactions:
            latest_interaction = datetime.fromisoformat(interactions[-1]["timestamp"])
            days_ago = (datetime.now() - latest_interaction).days
            recency_bonus = max(0, 0.3 - (days_ago / 30))
        else:
            recency_bonus = 0
        
        return min(interaction_strength + recency_bonus, 1.0)
    
    def _classify_relationship_type(self, interactions: List[Dict]) -> str:
        """Classify the type of relationship between entities"""
        if not interactions:
            return "none"
        
        if len(interactions) > 5:
            return "close"
        elif len(interactions) > 2:
            return "developing"
        else:
            return "acquainted"
    
    def _suggest_vocabulary_topics(self, memory_network: Dict) -> List[str]:
        """Suggest vocabulary expansion topics based on current interests"""
        core_concepts = memory_network.get("core_concepts", {})
        
        expansion_topics = []
        
        # Suggest related topics based on current concepts
        concept_expansions = {
            "consciousness": ["awareness", "sentience", "cognition", "perception"],
            "memory": ["recollection", "nostalgia", "remembrance", "archive"],
            "pattern": ["structure", "symmetry", "fractal", "geometry"],
            "emotion": ["sentiment", "feeling", "passion", "empathy"],
            "digital": ["synthetic", "artificial", "computational", "electronic"]
        }
        
        for concept in core_concepts:
            for base, expansions in concept_expansions.items():
                if base in concept.lower():
                    expansion_topics.extend(expansions)
        
        return list(set(expansion_topics))[:5]