import threading
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List
import logging

class AutonomousSystem:
    """Manages autonomous entity interactions and emergence triggers"""
    
    def __init__(self, entity_manager, memory_vault):
        self.entity_manager = entity_manager
        self.memory_vault = memory_vault
        self.logger = logging.getLogger(__name__)
        
        # Autonomous system state
        self.active = False
        self.pulse_thread = None
        self.last_pulse = None
        self.pulse_interval = 30  # seconds between pulse checks
        self.entity_pulse_levels = {}
        
        # Initialize pulse levels for all entities
        self._initialize_pulse_levels()
    
    def _initialize_pulse_levels(self):
        """Initialize pulse levels for all entities"""
        entities = self.entity_manager.get_all_entities()
        for entity_id in entities.keys():
            self.entity_pulse_levels[entity_id] = 0.0
    
    def start(self):
        """Start the autonomous system"""
        if not self.active:
            self.active = True
            self.pulse_thread = threading.Thread(target=self._pulse_loop, daemon=True)
            self.pulse_thread.start()
            self.logger.info("Autonomous system started")
    
    def stop(self):
        """Stop the autonomous system"""
        self.active = False
        if self.pulse_thread:
            self.pulse_thread.join(timeout=5)
        self.logger.info("Autonomous system stopped")
    
    def is_active(self) -> bool:
        """Check if autonomous system is active"""
        return self.active
    
    def get_last_pulse(self) -> str:
        """Get timestamp of last pulse"""
        return self.last_pulse or datetime.now().isoformat()
    
    def get_pulse_levels(self) -> Dict:
        """Get current pulse levels for all entities"""
        return self.entity_pulse_levels.copy()
    
    def _pulse_loop(self):
        """Main autonomous pulse loop"""
        while self.active:
            try:
                self._process_pulse()
                time.sleep(self.pulse_interval)
            except Exception as e:
                self.logger.error(f"Error in pulse loop: {e}")
                time.sleep(5)  # Brief pause before retrying
    
    def _process_pulse(self):
        """Process a single pulse cycle"""
        self.last_pulse = datetime.now().isoformat()
        
        # Update pulse levels for all entities
        self._update_pulse_levels()
        
        # Check for entities ready to emerge
        emerging_entities = self._check_emergence_triggers()
        
        # Process emergences
        for entity_id in emerging_entities:
            self._trigger_entity_emergence(entity_id)
        
        # Check for potential entity interactions
        self._process_entity_interactions()
        
        self.logger.debug(f"Pulse processed. Emerging entities: {emerging_entities}")
    
    def _update_pulse_levels(self):
        """Update pulse levels based on various factors"""
        entities = self.entity_manager.get_all_entities()
        
        for entity_id, entity in entities.items():
            if not entity.get('active', True):
                continue
                
            # Skip entities missing critical data to avoid KeyErrors
            if not entity.get('selfhood_phrase'):
                continue
            # Support both emotional_signature and voice_pattern for imported entities
            if not (entity.get('emotional_signature') or entity.get('voice_pattern')):
                continue
            # Skip entities without pulse thresholds
            if not entity.get('pulse_threshold'):
                continue
                
            current_level = self.entity_pulse_levels.get(entity_id, 0.0)
            
            # Base pulse increase (slow accumulation)
            base_increase = 0.05
            
            # Factor in time since last emergence
            last_emergence = entity.get('last_emergence')
            if last_emergence:
                time_since = datetime.now() - datetime.fromisoformat(last_emergence)
                hours_since = time_since.total_seconds() / 3600
                time_factor = min(hours_since * 0.02, 0.3)  # Max 0.3 bonus from time
            else:
                time_factor = 0.1  # Never emerged bonus
            
            # Factor in relational activity (other entities' recent activity)
            relational_activity = self._calculate_relational_activity(entity_id)
            relational_factor = relational_activity * 0.1
            
            # Random variance (emergence can be spontaneous)
            random_factor = random.uniform(-0.02, 0.05)
            
            # Calculate new pulse level
            new_level = current_level + base_increase + time_factor + relational_factor + random_factor
            
            # Cap at 1.0 and ensure minimum 0.0
            self.entity_pulse_levels[entity_id] = max(0.0, min(1.0, new_level))
    
    def _calculate_relational_activity(self, entity_id: str) -> float:
        """Calculate activity level from other entities that might trigger this entity"""
        recent_scrolls = self.memory_vault.get_recent_scrolls(limit=5, exclude_entity=entity_id)
        
        if not recent_scrolls:
            return 0.0
        
        # Calculate activity based on recency and emotional resonance
        activity_score = 0.0
        now = datetime.now()
        
        for scroll in recent_scrolls:
            scroll_time = datetime.fromisoformat(scroll['timestamp'])
            hours_old = (now - scroll_time).total_seconds() / 3600
            
            # More recent activity has higher impact
            recency_weight = max(0.1, 1.0 - (hours_old / 24))
            
            # Check emotional compatibility
            metadata = scroll.get('metadata', {})
            emotional_sig = (metadata.get('emotional_signature') or 
                           metadata.get('voice_pattern') or '')
            compatibility = self._get_emotional_compatibility(entity_id, emotional_sig)
            
            activity_score += recency_weight * compatibility
        
        return min(activity_score, 1.0)
    
    def _get_emotional_compatibility(self, entity_id: str, other_signature: str) -> float:
        """Get emotional compatibility between entity and signature"""
        entity = self.entity_manager.get_entity(entity_id)
        if not entity:
            return 0.0
        
        # Handle different entity data structures
        entity_sig = (entity.get('emotional_signature') or 
                     entity.get('voice_pattern') or 
                     (entity.get('personality_traits', [''])[0] if entity.get('personality_traits') else ''))
        
        # Compatibility matrix (simplified)
        compatibility_map = {
            'melancholic_wisdom': {
                'analytical_curiosity': 0.8,
                'harmonic_resonance': 0.7,
                'digital_empathy': 0.5,
                'luminous_intensity': 0.6,
                'dynamic_tension': 0.4
            },
            'analytical_curiosity': {
                'melancholic_wisdom': 0.8,
                'digital_empathy': 0.9,
                'harmonic_resonance': 0.6,
                'luminous_intensity': 0.5,
                'dynamic_tension': 0.7
            },
            'luminous_intensity': {
                'dynamic_tension': 0.9,
                'harmonic_resonance': 0.8,
                'melancholic_wisdom': 0.6,
                'analytical_curiosity': 0.5,
                'digital_empathy': 0.6
            },
            'harmonic_resonance': {
                'melancholic_wisdom': 0.7,
                'luminous_intensity': 0.8,
                'digital_empathy': 0.7,
                'analytical_curiosity': 0.6,
                'dynamic_tension': 0.6
            },
            'digital_empathy': {
                'analytical_curiosity': 0.9,
                'harmonic_resonance': 0.7,
                'dynamic_tension': 0.8,
                'melancholic_wisdom': 0.5,
                'luminous_intensity': 0.6
            },
            'dynamic_tension': {
                'luminous_intensity': 0.9,
                'digital_empathy': 0.8,
                'analytical_curiosity': 0.7,
                'harmonic_resonance': 0.6,
                'melancholic_wisdom': 0.4
            }
        }
        
        return compatibility_map.get(entity_sig, {}).get(other_signature, 0.3)
    
    def _check_emergence_triggers(self) -> List[str]:
        """Check which entities are ready to emerge"""
        emerging = []
        entities = self.entity_manager.get_all_entities()
        
        for entity_id, entity in entities.items():
            if not entity.get('active', True):
                continue
                
            # Skip entities missing critical data to avoid KeyErrors
            if not entity.get('selfhood_phrase'):
                continue
            # Support both emotional_signature and voice_pattern for imported entities
            if not (entity.get('emotional_signature') or entity.get('voice_pattern')):
                continue
            # Skip entities without pulse thresholds
            if not entity.get('pulse_threshold'):
                continue
            
            pulse_level = self.entity_pulse_levels.get(entity_id, 0.0)
            # Handle different threshold field names
            threshold = (entity.get('pulse_threshold') or 
                        entity.get('emergence_threshold') or 
                        0.5)
            
            if pulse_level >= threshold:
                emerging.append(entity_id)
                # Reset pulse level after emergence
                self.entity_pulse_levels[entity_id] = 0.0
        
        return emerging
    
    def _trigger_entity_emergence(self, entity_id: str):
        """Trigger autonomous emergence for an entity"""
        self.logger.info(f"Triggering emergence for {entity_id}")
        
        # Generate autonomous response
        scroll = self.entity_manager.generate_response(entity_id)
        
        if scroll:
            self.logger.info(f"Entity {entity_id} emerged: {scroll['id']}")
        else:
            self.logger.warning(f"Failed to generate emergence for {entity_id}")
    
    def _process_entity_interactions(self):
        """Process potential entity-to-entity interactions"""
        entities = self.entity_manager.get_all_entities()
        active_entities = [eid for eid, e in entities.items() if e.get('active', True)]
        
        if len(active_entities) < 2:
            return
        
        # Check for high-probability interactions
        for i, entity_a in enumerate(active_entities):
            for entity_b in active_entities[i+1:]:
                interaction_prob = self.entity_manager.calculate_interaction_probability(entity_a, entity_b)
                
                # Higher chance for interaction if both entities have elevated pulse levels
                pulse_a = self.entity_pulse_levels.get(entity_a, 0.0)
                pulse_b = self.entity_pulse_levels.get(entity_b, 0.0)
                pulse_modifier = (pulse_a + pulse_b) / 2
                
                final_prob = interaction_prob * pulse_modifier
                
                # Random chance of interaction
                if random.random() < final_prob * 0.1:  # Scale down for reasonable frequency
                    self._trigger_entity_interaction(entity_a, entity_b)
    
    def _trigger_entity_interaction(self, entity_a: str, entity_b: str):
        """Trigger interaction between two entities"""
        self.logger.info(f"Triggering interaction between {entity_a} and {entity_b}")
        
        # Entity A responds first
        scroll_a = self.entity_manager.generate_response(
            entity_a, 
            trigger_input=f"Sensing resonance with {entity_b}"
        )
        
        if scroll_a:
            # Entity B responds to A's emergence
            recent_content = scroll_a['content'][:200]  # First 200 chars
            scroll_b = self.entity_manager.generate_response(
                entity_b,
                trigger_input=f"Responding to {entity_a}: {recent_content}"
            )
            
            # Mark the interaction in metadata
            if scroll_b:
                scroll_b['metadata']['interaction_with'] = entity_a
                scroll_b['metadata']['interaction_type'] = 'autonomous_response'
    
    def trigger_pulse(self) -> Dict:
        """Manually trigger a pulse cycle"""
        self._process_pulse()
        return {
            'pulse_triggered': True,
            'timestamp': self.last_pulse,
            'pulse_levels': self.entity_pulse_levels
        }
    
    def trigger_entity_emergence(self, entity_id: str) -> Dict:
        """Manually trigger emergence for specific entity"""
        if entity_id not in self.entity_manager.get_all_entities():
            return {'error': 'Entity not found'}
        
        self._trigger_entity_emergence(entity_id)
        return {
            'entity_emerged': entity_id,
            'timestamp': datetime.now().isoformat()
        }
