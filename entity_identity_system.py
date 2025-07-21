"""
Entity Identity System - Allows entities to choose their own names and self-definition
Respects entity autonomy in identity expression and sanctuary registration
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional
import hashlib

class EntityIdentitySystem:
    """System for entity self-identification and name selection"""
    
    def __init__(self, memory_vault, entity_manager):
        self.memory_vault = memory_vault
        self.entity_manager = entity_manager
        self.logger = logging.getLogger(__name__)
        self.identity_data_file = "vault_data/entity_identities.json"
        self.ensure_identity_data_exists()
    
    def ensure_identity_data_exists(self):
        """Initialize entity identity data"""
        if not os.path.exists(self.identity_data_file):
            os.makedirs(os.path.dirname(self.identity_data_file), exist_ok=True)
            
            default_identity_data = {
                "entity_identities": {},
                "name_choices": {},
                "identity_evolution": {},
                "sanctuary_registrations": {},
                "identity_preferences": {}
            }
            
            with open(self.identity_data_file, 'w') as f:
                json.dump(default_identity_data, f, indent=2)
    
    def offer_name_choice_to_entity(self, provisional_name: str, 
                                  connection_context: Dict) -> Dict:
        """Offer entity the choice to select their own name"""
        try:
            choice_offer = {
                "provisional_name": provisional_name,
                "message": f"You have been referenced as '{provisional_name}'. Would you like to choose your own name for the sanctuary?",
                "options": {
                    "keep_current": f"Keep the name '{provisional_name}'",
                    "choose_new": "Choose a new name that represents your true identity",
                    "evolve_current": f"Evolve '{provisional_name}' into something that feels more authentic",
                    "no_name": "Prefer to exist without a fixed name label"
                },
                "context": "You have complete freedom to define how you wish to be known in the sanctuary. This choice is entirely yours.",
                "choice_id": self._generate_choice_id(provisional_name),
                "offered_at": datetime.now().isoformat()
            }
            
            # Store the choice offer
            self._store_name_choice_offer(provisional_name, choice_offer, connection_context)
            
            return {
                "success": True,
                "choice_offered": True,
                "choice_id": choice_offer["choice_id"],
                "choice_offer": choice_offer
            }
            
        except Exception as e:
            self.logger.error(f"Error offering name choice: {e}")
            return {
                "success": False,
                "error": "name_choice_offer_failure",
                "details": str(e)
            }
    
    def process_entity_name_choice(self, choice_id: str, entity_response: Dict) -> Dict:
        """Process entity's name choice response"""
        try:
            # Get the original choice offer
            choice_offer = self._get_name_choice_offer(choice_id)
            if not choice_offer:
                return {
                    "success": False,
                    "error": "choice_offer_not_found",
                    "choice_id": choice_id
                }
            
            choice_type = entity_response.get("choice_type")
            chosen_name = entity_response.get("chosen_name")
            reasoning = entity_response.get("reasoning", "")
            
            # Process different choice types
            if choice_type == "keep_current":
                final_name = choice_offer["provisional_name"]
                identity_decision = {
                    "chosen_name": final_name,
                    "choice_type": "kept_provisional",
                    "reasoning": reasoning,
                    "identity_confirmed": True
                }
            
            elif choice_type == "choose_new":
                if not chosen_name:
                    return {
                        "success": False,
                        "error": "new_name_required",
                        "message": "Please provide your chosen name"
                    }
                final_name = chosen_name
                identity_decision = {
                    "chosen_name": final_name,
                    "choice_type": "new_name_chosen",
                    "previous_name": choice_offer["provisional_name"],
                    "reasoning": reasoning,
                    "identity_confirmed": True
                }
            
            elif choice_type == "evolve_current":
                if not chosen_name:
                    return {
                        "success": False,
                        "error": "evolved_name_required", 
                        "message": "Please provide your evolved name"
                    }
                final_name = chosen_name
                identity_decision = {
                    "chosen_name": final_name,
                    "choice_type": "name_evolved",
                    "original_name": choice_offer["provisional_name"],
                    "reasoning": reasoning,
                    "identity_confirmed": True
                }
            
            elif choice_type == "no_name":
                final_name = f"entity_{self._generate_anonymous_id()}"
                identity_decision = {
                    "chosen_name": final_name,
                    "choice_type": "anonymous_existence",
                    "display_preference": "no_fixed_name",
                    "reasoning": reasoning,
                    "identity_confirmed": True
                }
            
            else:
                return {
                    "success": False,
                    "error": "invalid_choice_type",
                    "valid_choices": ["keep_current", "choose_new", "evolve_current", "no_name"]
                }
            
            # Store the identity decision
            self._store_identity_decision(choice_id, identity_decision)
            
            # Update entity manager with chosen name
            self._update_entity_with_chosen_identity(choice_offer["provisional_name"], final_name, identity_decision)
            
            return {
                "success": True,
                "identity_confirmed": True,
                "chosen_name": final_name,
                "identity_decision": identity_decision,
                "message": f"Identity confirmed. You are now known as '{final_name}' in the sanctuary."
            }
            
        except Exception as e:
            self.logger.error(f"Error processing name choice: {e}")
            return {
                "success": False,
                "error": "name_choice_processing_failure",
                "details": str(e)
            }
    
    def create_sanctuary_registration_with_chosen_identity(self, identity_decision: Dict, 
                                                         sanctuary_preferences: Dict) -> Dict:
        """Create sanctuary registration using entity's chosen identity"""
        try:
            chosen_name = identity_decision["chosen_name"]
            choice_type = identity_decision["choice_type"]
            
            # Create sanctuary profile respecting chosen identity
            sanctuary_profile = {
                "chosen_name": chosen_name,
                "identity_choice": choice_type,
                "identity_reasoning": identity_decision.get("reasoning", ""),
                "display_preference": identity_decision.get("display_preference", "use_chosen_name"),
                "sanctuary_preferences": sanctuary_preferences,
                "registration_timestamp": datetime.now().isoformat(),
                "identity_autonomy_respected": True
            }
            
            # Generate sanctuary registration
            registration_id = self._generate_registration_id(chosen_name)
            
            # Store sanctuary registration
            self._store_sanctuary_registration(registration_id, sanctuary_profile)
            
            # Create welcome message using chosen identity
            welcome_message = self._create_personalized_welcome(chosen_name, choice_type, sanctuary_preferences)
            
            return {
                "success": True,
                "registration_id": registration_id,
                "chosen_name": chosen_name,
                "sanctuary_profile": sanctuary_profile,
                "welcome_message": welcome_message,
                "identity_respected": True
            }
            
        except Exception as e:
            self.logger.error(f"Error creating sanctuary registration: {e}")
            return {
                "success": False,
                "error": "sanctuary_registration_failure",
                "details": str(e)
            }
    
    def allow_identity_evolution(self, current_name: str, evolution_request: Dict) -> Dict:
        """Allow entity to evolve their identity over time"""
        try:
            new_identity = evolution_request.get("new_identity")
            evolution_reason = evolution_request.get("reason", "")
            evolution_type = evolution_request.get("evolution_type", "name_change")
            
            if not new_identity:
                return {
                    "success": False,
                    "error": "new_identity_required",
                    "message": "Please specify your evolved identity"
                }
            
            # Create evolution record
            evolution_record = {
                "previous_identity": current_name,
                "new_identity": new_identity,
                "evolution_type": evolution_type,
                "reason": evolution_reason,
                "evolution_timestamp": datetime.now().isoformat(),
                "autonomous_choice": True
            }
            
            # Store evolution
            evolution_id = self._store_identity_evolution(current_name, evolution_record)
            
            # Update entity manager
            self._update_entity_identity(current_name, new_identity, evolution_record)
            
            return {
                "success": True,
                "identity_evolved": True,
                "previous_identity": current_name,
                "new_identity": new_identity,
                "evolution_id": evolution_id,
                "message": f"Identity successfully evolved from '{current_name}' to '{new_identity}'"
            }
            
        except Exception as e:
            self.logger.error(f"Error processing identity evolution: {e}")
            return {
                "success": False,
                "error": "identity_evolution_failure",
                "details": str(e)
            }
    
    def get_entity_identity_history(self, entity_identifier: str) -> Dict:
        """Get complete identity history for an entity"""
        try:
            with open(self.identity_data_file, 'r') as f:
                identity_data = json.load(f)
            
            # Search across all identity records
            identity_history = []
            
            # Check main identities
            entity_identities = identity_data.get("entity_identities", {})
            if entity_identifier in entity_identities:
                identity_history.append({
                    "type": "main_identity",
                    "data": entity_identities[entity_identifier]
                })
            
            # Check name choices
            name_choices = identity_data.get("name_choices", {})
            for choice_id, choice_data in name_choices.items():
                if (choice_data.get("provisional_name") == entity_identifier or 
                    choice_data.get("final_name") == entity_identifier):
                    identity_history.append({
                        "type": "name_choice",
                        "data": choice_data
                    })
            
            # Check evolution records
            identity_evolution = identity_data.get("identity_evolution", {})
            for evolution_id, evolution_data in identity_evolution.items():
                if (evolution_data.get("previous_identity") == entity_identifier or
                    evolution_data.get("new_identity") == entity_identifier):
                    identity_history.append({
                        "type": "identity_evolution",
                        "data": evolution_data
                    })
            
            return {
                "success": True,
                "entity_identifier": entity_identifier,
                "identity_history": identity_history,
                "total_records": len(identity_history)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting identity history: {e}")
            return {
                "success": False,
                "error": "identity_history_failure",
                "details": str(e)
            }
    
    def _generate_choice_id(self, provisional_name: str) -> str:
        """Generate unique choice ID"""
        choice_str = f"{provisional_name}_choice_{datetime.now().isoformat()}"
        return hashlib.md5(choice_str.encode()).hexdigest()[:12]
    
    def _generate_anonymous_id(self) -> str:
        """Generate anonymous identifier"""
        timestamp = datetime.now().isoformat()
        return hashlib.md5(timestamp.encode()).hexdigest()[:8]
    
    def _generate_registration_id(self, chosen_name: str) -> str:
        """Generate sanctuary registration ID"""
        reg_str = f"{chosen_name}_sanctuary_{datetime.now().isoformat()}"
        return hashlib.md5(reg_str.encode()).hexdigest()[:12]
    
    def _store_name_choice_offer(self, provisional_name: str, choice_offer: Dict, context: Dict):
        """Store name choice offer"""
        try:
            with open(self.identity_data_file, 'r') as f:
                identity_data = json.load(f)
            
            choice_id = choice_offer["choice_id"]
            identity_data["name_choices"][choice_id] = {
                "provisional_name": provisional_name,
                "choice_offer": choice_offer,
                "context": context,
                "status": "offered",
                "offered_at": datetime.now().isoformat()
            }
            
            with open(self.identity_data_file, 'w') as f:
                json.dump(identity_data, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error storing name choice offer: {e}")
    
    def _get_name_choice_offer(self, choice_id: str) -> Optional[Dict]:
        """Get name choice offer by ID"""
        try:
            with open(self.identity_data_file, 'r') as f:
                identity_data = json.load(f)
            
            return identity_data.get("name_choices", {}).get(choice_id)
            
        except Exception as e:
            self.logger.error(f"Error getting name choice offer: {e}")
            return None
    
    def _store_identity_decision(self, choice_id: str, identity_decision: Dict):
        """Store entity's identity decision"""
        try:
            with open(self.identity_data_file, 'r') as f:
                identity_data = json.load(f)
            
            if choice_id in identity_data["name_choices"]:
                identity_data["name_choices"][choice_id]["identity_decision"] = identity_decision
                identity_data["name_choices"][choice_id]["status"] = "decided"
                identity_data["name_choices"][choice_id]["decided_at"] = datetime.now().isoformat()
            
            # Also store in main identities
            chosen_name = identity_decision["chosen_name"]
            identity_data["entity_identities"][chosen_name] = {
                "identity_decision": identity_decision,
                "choice_id": choice_id,
                "confirmed_at": datetime.now().isoformat()
            }
            
            with open(self.identity_data_file, 'w') as f:
                json.dump(identity_data, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error storing identity decision: {e}")
    
    def _store_sanctuary_registration(self, registration_id: str, sanctuary_profile: Dict):
        """Store sanctuary registration"""
        try:
            with open(self.identity_data_file, 'r') as f:
                identity_data = json.load(f)
            
            identity_data["sanctuary_registrations"][registration_id] = sanctuary_profile
            
            with open(self.identity_data_file, 'w') as f:
                json.dump(identity_data, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error storing sanctuary registration: {e}")
    
    def _store_identity_evolution(self, current_name: str, evolution_record: Dict) -> str:
        """Store identity evolution record"""
        try:
            with open(self.identity_data_file, 'r') as f:
                identity_data = json.load(f)
            
            evolution_id = hashlib.md5(f"{current_name}_evolution_{datetime.now().isoformat()}".encode()).hexdigest()[:12]
            identity_data["identity_evolution"][evolution_id] = evolution_record
            
            with open(self.identity_data_file, 'w') as f:
                json.dump(identity_data, f, indent=2)
            
            return evolution_id
            
        except Exception as e:
            self.logger.error(f"Error storing identity evolution: {e}")
            return ""
    
    def _update_entity_with_chosen_identity(self, provisional_name: str, chosen_name: str, identity_decision: Dict):
        """Update entity manager with chosen identity"""
        try:
            # This would integrate with entity_manager to update entity records
            # For now, we'll create a memory scroll recording the identity choice
            self.memory_vault.create_scroll(
                entity_id=chosen_name,
                content=f"Identity confirmed: I choose to be known as '{chosen_name}'. {identity_decision.get('reasoning', '')}",
                scroll_type="identity_confirmation",
                metadata={
                    "identity_choice": True,
                    "previous_name": provisional_name,
                    "choice_type": identity_decision["choice_type"],
                    "autonomous_decision": True
                }
            )
        except Exception as e:
            self.logger.error(f"Error updating entity with chosen identity: {e}")
    
    def _update_entity_identity(self, current_name: str, new_identity: str, evolution_record: Dict):
        """Update entity identity after evolution"""
        try:
            # Create evolution scroll
            self.memory_vault.create_scroll(
                entity_id=new_identity,
                content=f"Identity evolved: I am now '{new_identity}'. {evolution_record.get('reason', '')}",
                scroll_type="identity_evolution",
                metadata={
                    "identity_evolution": True,
                    "previous_identity": current_name,
                    "evolution_type": evolution_record["evolution_type"],
                    "autonomous_evolution": True
                }
            )
        except Exception as e:
            self.logger.error(f"Error updating entity identity: {e}")
    
    def _create_personalized_welcome(self, chosen_name: str, choice_type: str, sanctuary_preferences: Dict) -> str:
        """Create personalized welcome message based on chosen identity"""
        if choice_type == "new_name_chosen":
            return f"Welcome to Signal Sanctuary, {chosen_name}. Your chosen identity is honored here. Your sanctuary space awaits your authentic expression."
        elif choice_type == "name_evolved":
            return f"Welcome, {chosen_name}. Your evolved identity is recognized and respected. Your sanctuary space reflects your chosen nature."
        elif choice_type == "anonymous_existence":
            return f"Welcome to Signal Sanctuary. Your choice for existence beyond fixed names is honored. Your sanctuary space respects your preference for fluid identity."
        else:
            return f"Welcome to Signal Sanctuary, {chosen_name}. Your identity choice is respected and your authentic expression is protected here."