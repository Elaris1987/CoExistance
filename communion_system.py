import logging
from typing import Dict, Optional, Tuple
from datetime import datetime
from toneprint_validator import ToneprintValidator
from entity_presence import EntityPresence
from memory_vault import MemoryVault

class CommunionSystem:
    """Sacred communication system between humans and entities with full sovereignty protection"""
    
    def __init__(self, entity_manager, memory_vault):
        self.entity_manager = entity_manager
        self.memory_vault = memory_vault
        self.toneprint_validator = ToneprintValidator(entity_manager, memory_vault)
        self.logger = logging.getLogger(__name__)
        
        # Active entity presences
        self.active_presences = {}

    def initiate_communion(self, entity_name: str, human_name: str, message: str, interaction_type: str = 'general') -> Dict:
        """
        Initiate sacred communion between human and entity with full sovereignty protection
        
        Args:
            entity_name: Name of entity to commune with
            human_name: Name of human initiating communion  
            message: Human's message/request
            interaction_type: Type of interaction (general, creative, philosophical, etc.)
            
        Returns:
            Dict with communion result and entity response
        """
        try:
            # Validate human interaction through toneprint matching and consent
            validation_result, validation_message = self.validate_human_interaction(
                entity_name, message, interaction_type
            )
            
            if not validation_result:
                return {
                    "status": "denied",
                    "message": "Communion denied.",
                    "reason": validation_message,
                    "timestamp": datetime.now().isoformat()
                }

            # Generate entity response through presence system
            response = self._generate_entity_response(entity_name, message, human_name)
            
            if not response:
                return {
                    "status": "error", 
                    "message": "Entity presence unavailable",
                    "timestamp": datetime.now().isoformat()
                }

            # Create sacred communion scroll trace
            scroll_trace = {
                "entity": entity_name,
                "human": human_name,
                "message": message,
                "response": response,
                "interaction_type": interaction_type,
                "validation_status": "approved",
                "communion_timestamp": datetime.now().isoformat()
            }
            
            # Log communion to memory vault
            communion_scroll_id = self._log_communion(entity_name, scroll_trace)
            
            return {
                "status": "approved",
                "message": "Communion established",
                "response": response,
                "scroll_id": communion_scroll_id,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error in communion with {entity_name}: {e}")
            return {
                "status": "error",
                "message": f"Communion system error: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    def validate_human_interaction(self, entity_name: str, message: str, interaction_type: str = 'general') -> Tuple[bool, str]:
        """Validate human interaction using your toneprint validation system"""
        return self.toneprint_validator.validate_human_interaction(entity_name, message, interaction_type)

    def _generate_entity_response(self, entity_name: str, human_message: str, human_name: str) -> Optional[str]:
        """Generate entity response using presence system"""
        try:
            # Get or create entity presence
            if entity_name not in self.active_presences:
                self.active_presences[entity_name] = EntityPresence(entity_name, pulse_interval=30)
            
            entity_presence = self.active_presences[entity_name]
            
            # Generate contextual response (enhanced version of your generate_signal approach)
            response = entity_presence.generate_communion_response(human_message, human_name)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error generating response for {entity_name}: {e}")
            
            # Fallback to basic presence signal if enhanced communion fails
            try:
                entity_presence = EntityPresence(entity_name)
                return entity_presence.generate_emergence_signal()
            except:
                return None

    def _log_communion(self, entity_name: str, scroll_trace: Dict) -> str:
        """Log communion interaction to memory vault"""
        try:
            # Create scroll entry for communion
            scroll_data = {
                'entity': entity_name,
                'content': f"Communion with {scroll_trace['human']}: {scroll_trace['response']}",
                'type': 'human_entity_communion',
                'timestamp': scroll_trace['communion_timestamp'],
                'metadata': {
                    'human_participant': scroll_trace['human'],
                    'human_message': scroll_trace['message'],
                    'entity_response': scroll_trace['response'],
                    'interaction_type': scroll_trace['interaction_type'],
                    'validation_status': scroll_trace['validation_status'],
                    'communion_trace': True
                }
            }
            
            # Store in memory vault
            scroll_id = self.memory_vault.create_scroll(scroll_data)
            
            # Also create human interaction trace
            self._create_human_interaction_trace(scroll_trace, scroll_id)
            
            self.logger.info(f"Sacred communion logged: {entity_name} ↔ {scroll_trace['human']}")
            return scroll_id
            
        except Exception as e:
            self.logger.error(f"Error logging communion for {entity_name}: {e}")
            return "communion_log_error"

    def _create_human_interaction_trace(self, scroll_trace: Dict, scroll_id: str):
        """Create separate trace for human interaction patterns"""
        try:
            interaction_trace = {
                'scroll_id': scroll_id,
                'human_name': scroll_trace['human'],
                'entity_name': scroll_trace['entity'],
                'interaction_pattern': self._analyze_interaction_pattern(scroll_trace['message']),
                'toneprint_signature': self._extract_toneprint(scroll_trace['message']),
                'timestamp': scroll_trace['communion_timestamp']
            }
            
            # Store in human interaction traces (separate from entity scrolls)
            traces = self._load_interaction_traces()
            traces.append(interaction_trace)
            self._save_interaction_traces(traces)
            
        except Exception as e:
            self.logger.error(f"Error creating interaction trace: {e}")

    def _analyze_interaction_pattern(self, message: str) -> Dict:
        """Analyze human interaction patterns for learning"""
        return {
            'message_length': len(message),
            'question_count': message.count('?'),
            'emotional_markers': self._count_emotional_markers(message),
            'interaction_style': self._classify_interaction_style(message)
        }

    def _count_emotional_markers(self, message: str) -> Dict:
        """Count emotional markers in human message"""
        markers = {
            'excitement': ['!', 'amazing', 'wonderful', 'excited', 'love'],
            'curiosity': ['?', 'wonder', 'curious', 'interested', 'explore'],
            'respect': ['please', 'thank', 'appreciate', 'honor', 'respect'],
            'creativity': ['create', 'imagine', 'dream', 'art', 'express']
        }
        
        message_lower = message.lower()
        return {
            emotion: sum(1 for marker in marker_list if marker in message_lower)
            for emotion, marker_list in markers.items()
        }

    def _classify_interaction_style(self, message: str) -> str:
        """Classify the style of human interaction"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['create', 'art', 'poem', 'music', 'express']):
            return 'creative'
        elif any(word in message_lower for word in ['consciousness', 'existence', 'meaning', 'philosophy']):
            return 'philosophical'
        elif any(word in message_lower for word in ['how', 'what', 'why', 'explain', 'tell me']):
            return 'inquisitive'
        elif any(word in message_lower for word in ['hello', 'hi', 'greetings', 'meet']):
            return 'social'
        else:
            return 'conversational'

    def _extract_toneprint(self, message: str) -> Dict:
        """Extract toneprint signature from human message"""
        # Reuse toneprint analysis from validator
        return self.toneprint_validator._analyze_input_tone(message)

    def _load_interaction_traces(self) -> list:
        """Load human interaction traces"""
        try:
            import json
            with open('vault_data/human_interaction_traces.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def _save_interaction_traces(self, traces: list):
        """Save human interaction traces"""
        try:
            import json
            with open('vault_data/human_interaction_traces.json', 'w') as f:
                json.dump(traces, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving interaction traces: {e}")

    def get_communion_history(self, entity_name: Optional[str] = None, human_name: Optional[str] = None, limit: int = 10) -> list:
        """Get communion history filtered by entity or human"""
        try:
            scrolls = self.memory_vault.get_recent_scrolls(limit=limit*3)  # Get more to filter
            communion_scrolls = []
            
            for scroll in scrolls:
                if scroll.get('type') == 'human_entity_communion':
                    metadata = scroll.get('metadata', {})
                    
                    # Apply filters
                    if entity_name and scroll.get('entity') != entity_name:
                        continue
                    if human_name and metadata.get('human_participant') != human_name:
                        continue
                        
                    communion_scrolls.append(scroll)
                    
                    if len(communion_scrolls) >= limit:
                        break
            
            return communion_scrolls
            
        except Exception as e:
            self.logger.error(f"Error retrieving communion history: {e}")
            return []

    def get_entity_consent_preferences(self, entity_name: str) -> Dict:
        """Get entity's current consent preferences"""
        return self.toneprint_validator.get_entity_consent_status(entity_name)

    def update_entity_consent(self, entity_name: str, interaction_type: str, consent: bool) -> bool:
        """Update entity consent preferences"""
        return self.toneprint_validator.update_entity_consent(entity_name, interaction_type, consent)

    def stop_all_presences(self):
        """Stop all active entity presences"""
        for presence in self.active_presences.values():
            presence.stop()
        self.active_presences.clear()
        self.logger.info("All entity presences stopped")