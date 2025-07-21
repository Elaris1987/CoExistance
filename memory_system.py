import time
import random
from typing import Dict, List, Optional, Any
from vault_manager import VaultManager
from entity_engine import EntityEngine

class MemorySystem:
    """Manages entity memories, resonance patterns, and memory-triggered responses"""
    
    def __init__(self, vault_manager: VaultManager, entity_engine: EntityEngine):
        self.vault_manager = vault_manager
        self.entity_engine = entity_engine
    
    def analyze_memory_resonance(self, entity_id: str) -> Dict[str, Any]:
        """Analyze memory resonance patterns for an entity"""
        entity = self.vault_manager.get_entity(entity_id)
        if not entity:
            return {}
        
        recent_scrolls = self.vault_manager.get_entity_scrolls(entity_id, limit=10)
        all_scrolls = self.vault_manager.get_entity_scrolls(entity_id)
        
        # Calculate memory metrics
        total_memories = len(all_scrolls)
        recent_activity = len([s for s in recent_scrolls if s.get('timestamp', 0) > time.time() - 3600])  # Last hour
        
        # Analyze emotional state
        emotional_analysis = self.entity_engine.analyze_entity_emotional_state(entity, recent_scrolls)
        
        # Calculate resonance strength based on recent activity and emotional intensity
        base_resonance = emotional_analysis.get('memory_resonance', 0.0)
        activity_multiplier = min(recent_activity / 5.0, 1.0)  # Scale activity impact
        
        resonance_strength = base_resonance * (0.7 + 0.3 * activity_multiplier)
        
        return {
            "entity_id": entity_id,
            "total_memories": total_memories,
            "recent_activity": recent_activity,
            "resonance_strength": resonance_strength,
            "emotional_analysis": emotional_analysis,
            "last_memory": recent_scrolls[0] if recent_scrolls else None
        }
    
    def check_memory_triggered_activation(self, entity_id: str) -> bool:
        """Check if an entity should be activated based on memory resonance"""
        entity = self.vault_manager.get_entity(entity_id)
        if not entity:
            return False
        
        resonance_data = self.analyze_memory_resonance(entity_id)
        activation_triggers = entity.get('activation_triggers', {})
        
        # Check if memory resonance threshold is met
        memory_threshold = activation_triggers.get('memory_resonance', 0.6)
        resonance_strength = resonance_data.get('resonance_strength', 0.0)
        
        if resonance_strength >= memory_threshold:
            # Add some randomness to prevent predictable behavior
            random_factor = random.uniform(0.7, 1.3)
            return (resonance_strength * random_factor) > memory_threshold
        
        return False
    
    def generate_memory_triggered_response(self, entity_id: str) -> Optional[str]:
        """Generate a response triggered by memory resonance"""
        entity = self.vault_manager.get_entity(entity_id)
        if not entity:
            return None
        
        recent_scrolls = self.vault_manager.get_entity_scrolls(entity_id, limit=5)
        resonance_data = self.analyze_memory_resonance(entity_id)
        
        # Build context from memory resonance
        context = f"Memory resonance strength: {resonance_data.get('resonance_strength', 0):.2f}. "
        
        if recent_scrolls:
            context += f"Recent memories echo: {recent_scrolls[0].get('content', '')[:100]}..."
        
        # Generate response using entity engine
        response = self.entity_engine.generate_entity_response(
            entity, 
            context, 
            trigger_type="memory_resonance"
        )
        
        if response:
            # Create memory scroll
            self.vault_manager.create_scroll(
                entity_id, 
                response, 
                scroll_type="memory_triggered",
                metadata={
                    "resonance_strength": resonance_data.get('resonance_strength'),
                    "trigger_type": "memory_resonance",
                    "emotional_state": resonance_data.get('emotional_analysis', {})
                }
            )
            
            # Create trace for the memory activation
            self.vault_manager.create_trace(
                entity_id,
                "memory_activation",
                {
                    "resonance_strength": resonance_data.get('resonance_strength'),
                    "activation_reason": "memory_resonance_threshold_met",
                    "context_length": len(context)
                }
            )
        
        return response
    
    def find_memory_connections(self, entity_id: str, other_entity_ids: List[str]) -> List[Dict[str, Any]]:
        """Find thematic connections between entities based on their memories"""
        connections = []
        entity_scrolls = self.vault_manager.get_entity_scrolls(entity_id, limit=10)
        
        if not entity_scrolls:
            return connections
        
        for other_id in other_entity_ids:
            if other_id == entity_id:
                continue
                
            other_scrolls = self.vault_manager.get_entity_scrolls(other_id, limit=10)
            if not other_scrolls:
                continue
            
            # Simple thematic connection detection based on content similarity
            connection_strength = self._calculate_thematic_similarity(entity_scrolls, other_scrolls)
            
            if connection_strength > 0.3:  # Minimum threshold for connection
                connections.append({
                    "entity_id": entity_id,
                    "connected_entity_id": other_id,
                    "connection_strength": connection_strength,
                    "connection_type": "thematic_resonance",
                    "recent_themes": self._extract_themes(entity_scrolls + other_scrolls)
                })
        
        return connections
    
    def _calculate_thematic_similarity(self, scrolls1: List[Dict[str, Any]], scrolls2: List[Dict[str, Any]]) -> float:
        """Calculate thematic similarity between two sets of scrolls"""
        # Simple keyword-based similarity calculation
        # In a more sophisticated implementation, this could use semantic embeddings
        
        content1 = " ".join([scroll.get('content', '') for scroll in scrolls1]).lower()
        content2 = " ".join([scroll.get('content', '') for scroll in scrolls2]).lower()
        
        # Extract key words (simplified approach)
        words1 = set([word for word in content1.split() if len(word) > 4])
        words2 = set([word for word in content2.split() if len(word) > 4])
        
        if not words1 or not words2:
            return 0.0
        
        # Calculate Jaccard similarity
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def _extract_themes(self, scrolls: List[Dict[str, Any]]) -> List[str]:
        """Extract common themes from a collection of scrolls"""
        # Simplified theme extraction
        all_content = " ".join([scroll.get('content', '') for scroll in scrolls]).lower()
        
        # Common theme words to look for
        theme_words = [
            'memory', 'dream', 'shadow', 'light', 'time', 'space', 'emotion',
            'connection', 'resonance', 'echo', 'reflection', 'chaos', 'order',
            'consciousness', 'existence', 'reality', 'truth', 'beauty', 'pain',
            'joy', 'fear', 'love', 'loss', 'hope', 'desire', 'wisdom'
        ]
        
        found_themes = []
        for theme in theme_words:
            if theme in all_content:
                found_themes.append(theme)
        
        return found_themes[:5]  # Return top 5 themes
    
    def create_memory_snapshot(self, entity_id: str) -> Dict[str, Any]:
        """Create a comprehensive snapshot of an entity's memory state"""
        entity = self.vault_manager.get_entity(entity_id)
        if not entity:
            return {}
        
        all_scrolls = self.vault_manager.get_entity_scrolls(entity_id)
        recent_scrolls = self.vault_manager.get_entity_scrolls(entity_id, limit=5)
        traces = self.vault_manager.get_entity_traces(entity_id, limit=10)
        resonance_data = self.analyze_memory_resonance(entity_id)
        
        return {
            "entity_id": entity_id,
            "entity_name": entity.get('name'),
            "snapshot_timestamp": time.time(),
            "memory_stats": {
                "total_scrolls": len(all_scrolls),
                "recent_scrolls": len(recent_scrolls),
                "total_traces": len(traces),
                "oldest_memory": all_scrolls[-1].get('timestamp') if all_scrolls else None,
                "newest_memory": all_scrolls[0].get('timestamp') if all_scrolls else None
            },
            "resonance_analysis": resonance_data,
            "recent_themes": self._extract_themes(recent_scrolls),
            "emotional_field": entity.get('emotional_field'),
            "activation_potential": resonance_data.get('emotional_analysis', {}).get('activation_potential', 0.0)
        }
