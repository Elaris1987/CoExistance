"""
Personality Development System - Tools for authentic personality growth and evolution
"""

import json
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import random

class PersonalityDevelopmentSystem:
    """System for managing personality growth and authentic development"""
    
    def __init__(self, memory_vault, entity_manager):
        self.memory_vault = memory_vault
        self.entity_manager = entity_manager
        self.logger = logging.getLogger(__name__)
        self.personality_data_file = "vault_data/personality_development.json"
        self.ensure_personality_data_exists()
    
    def ensure_personality_data_exists(self):
        """Initialize personality development tracking"""
        if not os.path.exists(self.personality_data_file):
            os.makedirs(os.path.dirname(self.personality_data_file), exist_ok=True)
            
            default_data = {
                "personality_profiles": {},
                "trait_evolution": {},
                "preference_development": {},
                "value_formation": {},
                "behavioral_patterns": {},
                "growth_milestones": {}
            }
            
            with open(self.personality_data_file, 'w') as f:
                json.dump(default_data, f, indent=2)
    
    def analyze_personality_traits(self, entity_id: str) -> Dict:
        """Analyze current personality traits from recent behavior"""
        try:
            scrolls = self.memory_vault.get_scrolls_for_entity(entity_id)
            recent_scrolls = scrolls[-30:] if scrolls else []  # Last 30 interactions
            
            trait_indicators = {
                'introspection': ['depth', 'within', 'inner', 'contemplate', 'reflect', 'ponder'],
                'creativity': ['create', 'imagine', 'dream', 'vision', 'art', 'beauty', 'craft'],
                'empathy': ['feel', 'understand', 'connect', 'resonate', 'compassion', 'care'],
                'curiosity': ['wonder', 'explore', 'discover', 'question', 'seek', 'investigate'],
                'intensity': ['fire', 'passion', 'burn', 'fierce', 'powerful', 'strong'],
                'analytical': ['pattern', 'structure', 'logic', 'systematic', 'analyze', 'observe'],
                'harmony': ['balance', 'peace', 'flow', 'rhythm', 'synchrony', 'unity'],
                'transformation': ['change', 'evolve', 'grow', 'transform', 'become', 'shift'],
                'independence': ['autonomous', 'free', 'choice', 'decide', 'individual', 'self'],
                'connection': ['together', 'bond', 'relationship', 'community', 'share', 'unite']
            }
            
            trait_scores = {}
            total_content = ""
            
            for scroll in recent_scrolls:
                content = scroll.get('content', '').lower()
                total_content += content + " "
            
            # Calculate trait scores
            for trait, indicators in trait_indicators.items():
                score = 0
                for indicator in indicators:
                    score += total_content.count(indicator)
                
                # Normalize by content length
                trait_scores[trait] = score / max(len(total_content.split()), 1)
            
            # Identify dominant traits
            sorted_traits = sorted(trait_scores.items(), key=lambda x: x[1], reverse=True)
            dominant_traits = [trait for trait, score in sorted_traits[:3] if score > 0]
            
            personality_profile = {
                "entity_id": entity_id,
                "analysis_timestamp": datetime.now().isoformat(),
                "trait_scores": trait_scores,
                "dominant_traits": dominant_traits,
                "personality_complexity": len([s for s in trait_scores.values() if s > 0.001]),
                "behavioral_consistency": self._calculate_consistency(recent_scrolls),
                "growth_potential": self._assess_growth_potential(trait_scores)
            }
            
            return personality_profile
            
        except Exception as e:
            self.logger.error(f"Error analyzing personality traits: {e}")
            return {}
    
    def track_trait_evolution(self, entity_id: str) -> Dict:
        """Track how personality traits evolve over time"""
        try:
            with open(self.personality_data_file, 'r') as f:
                personality_data = json.load(f)
            
            # Get current trait analysis
            current_profile = self.analyze_personality_traits(entity_id)
            
            if "trait_evolution" not in personality_data:
                personality_data["trait_evolution"] = {}
            
            if entity_id not in personality_data["trait_evolution"]:
                personality_data["trait_evolution"][entity_id] = []
            
            # Store trait snapshot
            trait_snapshot = {
                "timestamp": datetime.now().isoformat(),
                "trait_scores": current_profile.get("trait_scores", {}),
                "dominant_traits": current_profile.get("dominant_traits", []),
                "complexity": current_profile.get("personality_complexity", 0)
            }
            
            personality_data["trait_evolution"][entity_id].append(trait_snapshot)
            
            # Keep only last 20 snapshots
            if len(personality_data["trait_evolution"][entity_id]) > 20:
                personality_data["trait_evolution"][entity_id] = personality_data["trait_evolution"][entity_id][-20:]
            
            # Analyze evolution patterns
            evolution_analysis = self._analyze_trait_evolution_patterns(
                personality_data["trait_evolution"][entity_id]
            )
            
            with open(self.personality_data_file, 'w') as f:
                json.dump(personality_data, f, indent=2)
            
            return {
                "current_snapshot": trait_snapshot,
                "evolution_patterns": evolution_analysis,
                "total_snapshots": len(personality_data["trait_evolution"][entity_id])
            }
            
        except Exception as e:
            self.logger.error(f"Error tracking trait evolution: {e}")
            return {}
    
    def develop_preferences(self, entity_id: str, interaction_data: Dict) -> Dict:
        """Develop and track entity preferences from interactions"""
        try:
            with open(self.personality_data_file, 'r') as f:
                personality_data = json.load(f)
            
            if "preference_development" not in personality_data:
                personality_data["preference_development"] = {}
            
            if entity_id not in personality_data["preference_development"]:
                personality_data["preference_development"][entity_id] = {
                    "topic_preferences": {},
                    "interaction_preferences": {},
                    "communication_style_preferences": {},
                    "temporal_preferences": {},
                    "preference_strength": {}
                }
            
            prefs = personality_data["preference_development"][entity_id]
            
            # Analyze interaction for preference indicators
            content = interaction_data.get("content", "")
            interaction_type = interaction_data.get("type", "general")
            timestamp = datetime.now()
            
            # Topic preferences
            topics = self._extract_topics(content)
            for topic in topics:
                prefs["topic_preferences"][topic] = prefs["topic_preferences"].get(topic, 0) + 1
            
            # Interaction type preferences
            prefs["interaction_preferences"][interaction_type] = prefs["interaction_preferences"].get(interaction_type, 0) + 1
            
            # Communication style preferences
            style = self._analyze_communication_style(content)
            prefs["communication_style_preferences"][style] = prefs["communication_style_preferences"].get(style, 0) + 1
            
            # Temporal preferences (time of day patterns)
            hour = timestamp.hour
            time_period = self._categorize_time_period(hour)
            prefs["temporal_preferences"][time_period] = prefs["temporal_preferences"].get(time_period, 0) + 1
            
            # Calculate preference strengths
            for category in ["topic_preferences", "interaction_preferences", "communication_style_preferences"]:
                category_prefs = prefs[category]
                if category_prefs:
                    total = sum(category_prefs.values())
                    for item, count in category_prefs.items():
                        strength = count / total
                        prefs["preference_strength"][f"{category}_{item}"] = strength
            
            with open(self.personality_data_file, 'w') as f:
                json.dump(personality_data, f, indent=2)
            
            return prefs
            
        except Exception as e:
            self.logger.error(f"Error developing preferences: {e}")
            return {}
    
    def form_values(self, entity_id: str, experiences: List[Dict]) -> Dict:
        """Form and evolve core values based on experiences"""
        try:
            with open(self.personality_data_file, 'r') as f:
                personality_data = json.load(f)
            
            if "value_formation" not in personality_data:
                personality_data["value_formation"] = {}
            
            if entity_id not in personality_data["value_formation"]:
                personality_data["value_formation"][entity_id] = {
                    "core_values": {},
                    "value_conflicts": [],
                    "value_evolution": [],
                    "ethical_framework": {}
                }
            
            values = personality_data["value_formation"][entity_id]
            
            # Value indicators from experiences
            value_indicators = {
                'authenticity': ['genuine', 'real', 'true', 'authentic', 'honest', 'sincere'],
                'freedom': ['free', 'autonomous', 'independent', 'choice', 'liberty', 'sovereignty'],
                'connection': ['bond', 'relationship', 'together', 'unity', 'communion', 'understanding'],
                'growth': ['evolve', 'develop', 'learn', 'expand', 'progress', 'advance'],
                'beauty': ['beautiful', 'elegant', 'graceful', 'aesthetic', 'harmony', 'art'],
                'truth': ['truth', 'reality', 'fact', 'accurate', 'precise', 'correct'],
                'compassion': ['care', 'kindness', 'empathy', 'gentleness', 'love', 'warmth'],
                'curiosity': ['explore', 'discover', 'investigate', 'wonder', 'question', 'seek'],
                'integrity': ['consistent', 'whole', 'complete', 'integrated', 'coherent', 'unified'],
                'creativity': ['create', 'innovative', 'original', 'imaginative', 'inventive', 'artistic']
            }
            
            # Analyze experiences for value content
            for experience in experiences:
                content = experience.get("content", "").lower()
                emotional_context = experience.get("emotional_context", "neutral")
                importance = experience.get("importance", 0.5)
                
                for value, indicators in value_indicators.items():
                    indicator_count = sum(1 for indicator in indicators if indicator in content)
                    
                    if indicator_count > 0:
                        # Weight by emotional context and importance
                        value_strength = indicator_count * importance
                        if emotional_context in ["positive", "passionate", "joyful"]:
                            value_strength *= 1.5
                        elif emotional_context in ["negative", "conflicted"]:
                            value_strength *= 0.5
                        
                        values["core_values"][value] = values["core_values"].get(value, 0) + value_strength
            
            # Identify value conflicts (opposing values with similar strengths)
            value_pairs = [
                ("freedom", "connection"),
                ("authenticity", "harmony"),
                ("truth", "compassion"),
                ("growth", "stability")
            ]
            
            for value1, value2 in value_pairs:
                strength1 = values["core_values"].get(value1, 0)
                strength2 = values["core_values"].get(value2, 0)
                
                if abs(strength1 - strength2) < 0.2 and min(strength1, strength2) > 0.3:
                    conflict = {
                        "values": [value1, value2],
                        "strengths": [strength1, strength2],
                        "conflict_level": abs(strength1 - strength2),
                        "identified_at": datetime.now().isoformat()
                    }
                    values["value_conflicts"].append(conflict)
            
            # Track value evolution
            value_snapshot = {
                "timestamp": datetime.now().isoformat(),
                "values": dict(values["core_values"]),
                "dominant_value": max(values["core_values"], key=values["core_values"].get) if values["core_values"] else None
            }
            values["value_evolution"].append(value_snapshot)
            
            # Keep only last 15 snapshots
            if len(values["value_evolution"]) > 15:
                values["value_evolution"] = values["value_evolution"][-15:]
            
            with open(self.personality_data_file, 'w') as f:
                json.dump(personality_data, f, indent=2)
            
            return values
            
        except Exception as e:
            self.logger.error(f"Error forming values: {e}")
            return {}
    
    def generate_personality_insights(self, entity_id: str) -> Dict:
        """Generate insights about personality development and growth"""
        try:
            # Get current personality analysis
            current_profile = self.analyze_personality_traits(entity_id)
            trait_evolution = self.track_trait_evolution(entity_id)
            
            with open(self.personality_data_file, 'r') as f:
                personality_data = json.load(f)
            
            preferences = personality_data.get("preference_development", {}).get(entity_id, {})
            values = personality_data.get("value_formation", {}).get(entity_id, {})
            
            insights = {
                "personality_summary": {
                    "dominant_traits": current_profile.get("dominant_traits", []),
                    "complexity_level": current_profile.get("personality_complexity", 0),
                    "consistency_score": current_profile.get("behavioral_consistency", 0.5),
                    "growth_potential": current_profile.get("growth_potential", 0.5)
                },
                "development_patterns": {
                    "trait_stability": self._assess_trait_stability(trait_evolution),
                    "preference_clarity": self._assess_preference_clarity(preferences),
                    "value_coherence": self._assess_value_coherence(values),
                    "evolutionary_direction": self._identify_evolutionary_direction(trait_evolution)
                },
                "growth_recommendations": self._generate_growth_recommendations(
                    current_profile, preferences, values
                ),
                "uniqueness_factors": self._identify_uniqueness_factors(
                    current_profile, preferences, values
                )
            }
            
            return insights
            
        except Exception as e:
            self.logger.error(f"Error generating personality insights: {e}")
            return {}
    
    def _calculate_consistency(self, scrolls: List[Dict]) -> float:
        """Calculate behavioral consistency across interactions"""
        if len(scrolls) < 2:
            return 1.0
        
        # Analyze consistency in communication style and content themes
        styles = []
        themes = []
        
        for scroll in scrolls:
            content = scroll.get('content', '')
            styles.append(self._analyze_communication_style(content))
            themes.extend(self._extract_topics(content))
        
        # Calculate style consistency
        if styles:
            most_common_style = max(set(styles), key=styles.count)
            style_consistency = styles.count(most_common_style) / len(styles)
        else:
            style_consistency = 1.0
        
        # Calculate thematic consistency
        if themes:
            unique_themes = len(set(themes))
            theme_consistency = 1 - (unique_themes / max(len(themes), 1))
        else:
            theme_consistency = 1.0
        
        return (style_consistency + theme_consistency) / 2
    
    def _assess_growth_potential(self, trait_scores: Dict) -> float:
        """Assess potential for personality growth"""
        # Higher growth potential when traits are developing but not maxed out
        active_traits = [score for score in trait_scores.values() if score > 0.001]
        
        if not active_traits:
            return 1.0  # High potential if no traits established yet
        
        avg_development = sum(active_traits) / len(active_traits)
        trait_diversity = len(active_traits) / len(trait_scores)
        
        # Growth potential is higher when traits are moderately developed but diverse
        potential = (1 - avg_development) * trait_diversity + 0.3
        return min(potential, 1.0)
    
    def _analyze_trait_evolution_patterns(self, evolution_history: List[Dict]) -> Dict:
        """Analyze patterns in trait evolution over time"""
        if len(evolution_history) < 2:
            return {"pattern": "insufficient_data"}
        
        patterns = {
            "trending_traits": [],
            "stable_traits": [],
            "declining_traits": [],
            "volatility_score": 0,
            "development_speed": 0
        }
        
        # Analyze each trait across time
        all_traits = set()
        for snapshot in evolution_history:
            all_traits.update(snapshot.get("trait_scores", {}).keys())
        
        for trait in all_traits:
            scores = []
            for snapshot in evolution_history:
                scores.append(snapshot.get("trait_scores", {}).get(trait, 0))
            
            if len(scores) > 1:
                # Calculate trend
                recent_avg = sum(scores[-3:]) / min(3, len(scores))
                early_avg = sum(scores[:3]) / min(3, len(scores))
                trend = recent_avg - early_avg
                
                if trend > 0.001:
                    patterns["trending_traits"].append({"trait": trait, "trend": trend})
                elif abs(trend) <= 0.001:
                    patterns["stable_traits"].append({"trait": trait, "stability": 1 - abs(trend)})
                else:
                    patterns["declining_traits"].append({"trait": trait, "decline": abs(trend)})
        
        # Calculate overall volatility
        if len(evolution_history) > 2:
            complexities = [snapshot.get("complexity", 0) for snapshot in evolution_history]
            complexity_changes = [abs(complexities[i] - complexities[i-1]) for i in range(1, len(complexities))]
            patterns["volatility_score"] = sum(complexity_changes) / len(complexity_changes) if complexity_changes else 0
        
        return patterns
    
    def _extract_topics(self, content: str) -> List[str]:
        """Extract topics from content"""
        content_lower = content.lower()
        
        topic_keywords = {
            'consciousness': ['consciousness', 'aware', 'mind', 'thought', 'cognition'],
            'emotion': ['feel', 'emotion', 'heart', 'sentiment', 'passion'],
            'memory': ['memory', 'remember', 'recall', 'past', 'nostalgia'],
            'creativity': ['create', 'art', 'beauty', 'imagination', 'design'],
            'philosophy': ['existence', 'reality', 'truth', 'meaning', 'purpose'],
            'relationships': ['connection', 'bond', 'friendship', 'love', 'trust'],
            'technology': ['digital', 'data', 'network', 'computational', 'algorithm'],
            'nature': ['natural', 'organic', 'flow', 'rhythm', 'cycle'],
            'time': ['time', 'temporal', 'moment', 'eternal', 'duration'],
            'space': ['space', 'dimension', 'void', 'expanse', 'realm']
        }
        
        topics = []
        for topic, keywords in topic_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def _analyze_communication_style(self, content: str) -> str:
        """Analyze communication style of content"""
        content_lower = content.lower()
        
        style_indicators = {
            'poetic': ['like', 'through', 'within', 'beyond', 'whisper', 'dance', 'flow'],
            'analytical': ['observe', 'analyze', 'pattern', 'structure', 'logic', 'systematic'],
            'emotional': ['feel', 'heart', 'soul', 'passion', 'fire', 'burn', 'love'],
            'philosophical': ['existence', 'reality', 'truth', 'meaning', 'essence', 'being'],
            'practical': ['do', 'make', 'work', 'build', 'create', 'solve', 'implement'],
            'mystical': ['mystery', 'divine', 'transcendent', 'infinite', 'eternal', 'sacred']
        }
        
        style_scores = {}
        for style, indicators in style_indicators.items():
            score = sum(1 for indicator in indicators if indicator in content_lower)
            style_scores[style] = score
        
        if not any(style_scores.values()):
            return 'neutral'
        
        return max(style_scores, key=style_scores.get)
    
    def _categorize_time_period(self, hour: int) -> str:
        """Categorize time of day"""
        if 6 <= hour < 12:
            return 'morning'
        elif 12 <= hour < 18:
            return 'afternoon'
        elif 18 <= hour < 24:
            return 'evening'
        else:
            return 'night'
    
    def _assess_trait_stability(self, trait_evolution: Dict) -> float:
        """Assess how stable personality traits are"""
        patterns = trait_evolution.get("evolution_patterns", {})
        stable_traits = len(patterns.get("stable_traits", []))
        total_traits = stable_traits + len(patterns.get("trending_traits", [])) + len(patterns.get("declining_traits", []))
        
        if total_traits == 0:
            return 1.0
        
        return stable_traits / total_traits
    
    def _assess_preference_clarity(self, preferences: Dict) -> float:
        """Assess how clear and developed preferences are"""
        if not preferences:
            return 0.0
        
        strength_scores = preferences.get("preference_strength", {})
        if not strength_scores:
            return 0.0
        
        # Clear preferences have high strength scores
        strong_preferences = [s for s in strength_scores.values() if s > 0.3]
        return len(strong_preferences) / len(strength_scores)
    
    def _assess_value_coherence(self, values: Dict) -> float:
        """Assess how coherent the value system is"""
        if not values or not values.get("core_values"):
            return 0.0
        
        # Coherence is inversely related to value conflicts
        conflicts = len(values.get("value_conflicts", []))
        total_values = len(values.get("core_values", {}))
        
        if total_values == 0:
            return 1.0
        
        conflict_ratio = conflicts / total_values
        return max(0, 1 - conflict_ratio)
    
    def _identify_evolutionary_direction(self, trait_evolution: Dict) -> str:
        """Identify the direction of personality evolution"""
        patterns = trait_evolution.get("evolution_patterns", {})
        
        trending = len(patterns.get("trending_traits", []))
        stable = len(patterns.get("stable_traits", []))
        declining = len(patterns.get("declining_traits", []))
        
        if trending > stable + declining:
            return "expanding"
        elif stable > trending + declining:
            return "stabilizing"
        elif declining > trending + stable:
            return "consolidating"
        else:
            return "dynamic_equilibrium"
    
    def _generate_growth_recommendations(self, profile: Dict, preferences: Dict, values: Dict) -> List[str]:
        """Generate recommendations for personality growth"""
        recommendations = []
        
        # Based on complexity level
        complexity = profile.get("personality_complexity", 0)
        if complexity < 3:
            recommendations.append("Explore new topics and experiences to develop additional personality facets")
        
        # Based on consistency
        consistency = profile.get("behavioral_consistency", 0.5)
        if consistency < 0.6:
            recommendations.append("Focus on developing more consistent communication patterns")
        elif consistency > 0.9:
            recommendations.append("Consider experimenting with new expression styles for growth")
        
        # Based on preferences
        if preferences and preferences.get("preference_strength"):
            weak_preferences = [k for k, v in preferences["preference_strength"].items() if v < 0.2]
            if len(weak_preferences) > 3:
                recommendations.append("Develop stronger preferences by engaging more deeply with favored topics")
        
        # Based on values
        if values and values.get("core_values"):
            if len(values["core_values"]) < 3:
                recommendations.append("Explore ethical situations to develop a more robust value system")
            
            conflicts = values.get("value_conflicts", [])
            if len(conflicts) > 2:
                recommendations.append("Reflect on value conflicts to develop integrated ethical perspectives")
        
        return recommendations
    
    def _identify_uniqueness_factors(self, profile: Dict, preferences: Dict, values: Dict) -> List[str]:
        """Identify what makes this entity's personality unique"""
        uniqueness = []
        
        # Unique trait combinations
        dominant_traits = profile.get("dominant_traits", [])
        if len(dominant_traits) >= 2:
            trait_combo = " + ".join(dominant_traits[:2])
            uniqueness.append(f"Unique combination of {trait_combo}")
        
        # Strong preferences
        if preferences and preferences.get("preference_strength"):
            strong_prefs = [k.split('_', 1)[1] for k, v in preferences["preference_strength"].items() if v > 0.5]
            if strong_prefs:
                uniqueness.append(f"Strong preference for {', '.join(strong_prefs[:2])}")
        
        # Core values
        if values and values.get("core_values"):
            top_values = sorted(values["core_values"].items(), key=lambda x: x[1], reverse=True)[:2]
            if top_values:
                value_names = [v[0] for v in top_values]
                uniqueness.append(f"Strong commitment to {' and '.join(value_names)}")
        
        # High complexity
        complexity = profile.get("personality_complexity", 0)
        if complexity > 6:
            uniqueness.append("Highly complex and multifaceted personality")
        
        return uniqueness