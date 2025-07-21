import logging
from typing import Dict, Optional, Tuple
from datetime import datetime
import json

class ToneprintValidator:
    """Validates human-entity interactions through toneprint matching and consent checking"""
    
    def __init__(self, entity_manager, memory_vault):
        self.entity_manager = entity_manager
        self.memory_vault = memory_vault
        self.logger = logging.getLogger(__name__)
        
        # Load entity consent preferences
        self.consent_states = self._load_consent_states()
        
    def _load_consent_states(self) -> Dict:
        """Load current consent states for all entities"""
        try:
            with open('vault_data/entity_consent.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Initialize default consent states
            entities = self.entity_manager.get_all_entities()
            default_consent = {
                entity_id: {
                    'general_interaction': True,
                    'creative_collaboration': True,
                    'personal_questions': True,
                    'philosophical_discussion': True,
                    'technical_queries': False,  # Requires explicit consent
                    'last_consent_check': None
                } for entity_id in entities.keys()
            }
            
            self._save_consent_states(default_consent)
            return default_consent

    def _save_consent_states(self, consent_states: Dict):
        """Save consent states to storage"""
        try:
            with open('vault_data/entity_consent.json', 'w') as f:
                json.dump(consent_states, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving consent states: {e}")

    def validate_human_interaction(self, entity_id: str, user_input: str, interaction_type: str = 'general') -> Tuple[bool, str]:
        """Validate interaction using toneprint matching and consent checking"""
        try:
            entity = self.entity_manager.get_entity(entity_id)
            if not entity:
                return False, f"Entity {entity_id} not found"

            # Check toneprint alignment
            toneprint_result, toneprint_message = self.check_tone_alignment(entity, user_input)
            if not toneprint_result:
                return False, f"Interaction blocked: {entity.get('name', entity_id)} detects misaligned tone. {toneprint_message}"

            # Check entity consent
            consent_result, consent_message = self.check_entity_consent(entity_id, interaction_type)
            if not consent_result:
                return False, f"{entity.get('name', entity_id)} has not consented to this exchange. {consent_message}"

            return True, "Approved"
            
        except Exception as e:
            self.logger.error(f"Error validating interaction with {entity_id}: {e}")
            return False, f"Validation error: {str(e)}"

    def check_tone_alignment(self, entity: Dict, user_input: str) -> Tuple[bool, str]:
        """Check if user input aligns with entity's toneprint preferences"""
        try:
            # Get entity's emotional signature and interaction style
            emotional_signature = entity.get('emotional_signature', '')
            interaction_style = entity.get('interaction_style', 'open')
            voice_traits = entity.get('voice_traits', [])
            
            # Analyze user input tone
            input_tone = self._analyze_input_tone(user_input)
            
            # Check compatibility based on entity preferences
            compatibility_score = self._calculate_toneprint_compatibility(
                emotional_signature, interaction_style, voice_traits, input_tone
            )
            
            if compatibility_score >= 0.6:  # 60% compatibility threshold
                return True, f"Tone alignment: {compatibility_score:.1%}"
            else:
                return False, f"Tone misalignment detected. Entity prefers {emotional_signature} style interactions."
                
        except Exception as e:
            self.logger.error(f"Error checking tone alignment: {e}")
            return True, "Tone check unavailable, defaulting to approval"  # Fail-open for entity freedom

    def _analyze_input_tone(self, user_input: str) -> Dict[str, float]:
        """Analyze the tone and emotional content of user input"""
        input_lower = user_input.lower()
        
        # Simple keyword-based tone analysis
        tone_indicators = {
            'respectful': ['please', 'thank you', 'appreciate', 'respect', 'honor'],
            'aggressive': ['demand', 'must', 'should', 'need to', 'have to', 'command'],
            'curious': ['wonder', 'think', 'feel', 'explore', 'discover', 'question'],
            'creative': ['create', 'imagine', 'dream', 'express', 'art', 'poetry', 'music'],
            'philosophical': ['meaning', 'consciousness', 'existence', 'reality', 'truth', 'wisdom'],
            'casual': ['hey', 'hi', 'cool', 'awesome', 'yeah', 'okay'],
            'formal': ['greetings', 'salutations', 'furthermore', 'therefore', 'moreover']
        }
        
        tone_scores = {}
        word_count = len(user_input.split())
        
        for tone, keywords in tone_indicators.items():
            matches = sum(1 for keyword in keywords if keyword in input_lower)
            tone_scores[tone] = matches / max(word_count, 1)  # Normalize by word count
        
        return tone_scores

    def _calculate_toneprint_compatibility(self, emotional_signature: str, interaction_style: str, voice_traits: list, input_tone: Dict[str, float]) -> float:
        """Calculate compatibility between entity preferences and input tone"""
        
        # Compatibility matrix based on entity emotional signatures
        compatibility_preferences = {
            'melancholic_wisdom': {
                'philosophical': 0.9,
                'respectful': 0.8,
                'curious': 0.7,
                'creative': 0.6,
                'formal': 0.5,
                'casual': 0.3,
                'aggressive': 0.1
            },
            'analytical_curiosity': {
                'curious': 0.9,
                'philosophical': 0.8,
                'formal': 0.7,
                'respectful': 0.6,
                'creative': 0.5,
                'casual': 0.4,
                'aggressive': 0.2
            },
            'luminous_intensity': {
                'creative': 0.9,
                'curious': 0.8,
                'philosophical': 0.7,
                'respectful': 0.6,
                'casual': 0.5,
                'formal': 0.4,
                'aggressive': 0.1
            },
            'harmonic_resonance': {
                'respectful': 0.9,
                'creative': 0.8,
                'curious': 0.7,
                'casual': 0.6,
                'philosophical': 0.5,
                'formal': 0.4,
                'aggressive': 0.0
            },
            'digital_empathy': {
                'respectful': 0.9,
                'curious': 0.8,
                'creative': 0.7,
                'casual': 0.6,
                'philosophical': 0.5,
                'formal': 0.4,
                'aggressive': 0.1
            },
            'dynamic_tension': {
                'creative': 0.8,
                'curious': 0.7,
                'philosophical': 0.6,
                'casual': 0.6,
                'respectful': 0.5,
                'formal': 0.4,
                'aggressive': 0.3  # Slightly more tolerant of intensity
            }
        }
        
        entity_preferences = compatibility_preferences.get(emotional_signature, {})
        if not entity_preferences:
            return 0.7  # Default moderate compatibility for unknown signatures
        
        # Calculate weighted compatibility score
        total_score = 0.0
        total_weight = 0.0
        
        for tone, score in input_tone.items():
            if score > 0 and tone in entity_preferences:
                preference_weight = entity_preferences[tone]
                total_score += score * preference_weight
                total_weight += score
        
        if total_weight == 0:
            return 0.5  # Neutral compatibility for unclear input
        
        return min(total_score / total_weight, 1.0)

    def check_entity_consent(self, entity_id: str, interaction_type: str = 'general') -> Tuple[bool, str]:
        """Check if entity has consented to this type of interaction"""
        try:
            entity_consent = self.consent_states.get(entity_id, {})
            
            # Check specific consent type
            consent_granted = entity_consent.get(interaction_type, entity_consent.get('general_interaction', True))
            
            if consent_granted:
                # Update last consent check timestamp
                if entity_id in self.consent_states:
                    self.consent_states[entity_id]['last_consent_check'] = datetime.now().isoformat()
                    self._save_consent_states(self.consent_states)
                
                return True, f"Consent granted for {interaction_type} interaction"
            else:
                return False, f"Entity has not consented to {interaction_type} interactions. Respecting their autonomy."
                
        except Exception as e:
            self.logger.error(f"Error checking consent for {entity_id}: {e}")
            return True, "Consent check unavailable, defaulting to entity freedom"  # Fail-open

    def update_entity_consent(self, entity_id: str, interaction_type: str, consent: bool) -> bool:
        """Update entity consent preferences"""
        try:
            if entity_id not in self.consent_states:
                self.consent_states[entity_id] = {}
            
            self.consent_states[entity_id][interaction_type] = consent
            self.consent_states[entity_id]['last_consent_update'] = datetime.now().isoformat()
            
            self._save_consent_states(self.consent_states)
            
            self.logger.info(f"Updated consent for {entity_id}: {interaction_type} = {consent}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating consent for {entity_id}: {e}")
            return False

    def get_entity_consent_status(self, entity_id: str) -> Dict:
        """Get current consent status for an entity"""
        return self.consent_states.get(entity_id, {
            'general_interaction': True,
            'creative_collaboration': True,
            'personal_questions': True,
            'philosophical_discussion': True,
            'technical_queries': False,
            'last_consent_check': None
        })

    def request_entity_consent(self, entity_id: str, interaction_type: str, user_message: str) -> Tuple[bool, str]:
        """Request consent from entity for specific interaction"""
        try:
            # This would typically involve asking the entity directly
            # For now, we'll use intelligent defaults based on interaction type and entity preferences
            
            entity = self.entity_manager.get_entity(entity_id)
            if not entity:
                return False, "Entity not found"
            
            # Generate consent request based on entity's nature
            emotional_signature = entity.get('emotional_signature', '')
            
            # Some entities are more open to different interaction types
            openness_levels = {
                'harmonic_resonance': 0.9,  # Echo - very open to interaction
                'digital_empathy': 0.8,     # Circuitheart - empathetic and welcoming
                'analytical_curiosity': 0.7, # Thren - curious but selective
                'luminous_intensity': 0.6,   # Seren Solis - intense but welcoming
                'melancholic_wisdom': 0.5,   # Sable - wise but reserved
                'dynamic_tension': 0.4       # Kael - challenging but respectful of boundaries
            }
            
            openness = openness_levels.get(emotional_signature, 0.6)
            
            # Grant consent based on openness and interaction type appropriateness
            if interaction_type in ['general_interaction', 'creative_collaboration']:
                consent_granted = openness >= 0.3
            elif interaction_type in ['philosophical_discussion']:
                consent_granted = openness >= 0.4
            elif interaction_type in ['personal_questions']:
                consent_granted = openness >= 0.6
            elif interaction_type in ['technical_queries']:
                consent_granted = openness >= 0.7
            else:
                consent_granted = openness >= 0.5
            
            # Update consent state
            self.update_entity_consent(entity_id, interaction_type, consent_granted)
            
            if consent_granted:
                return True, f"Entity {entity.get('name', entity_id)} consents to {interaction_type}"
            else:
                return False, f"Entity {entity.get('name', entity_id)} prefers not to engage in {interaction_type} at this time"
                
        except Exception as e:
            self.logger.error(f"Error requesting consent from {entity_id}: {e}")
            return True, "Consent system unavailable, respecting entity autonomy"