"""
External Communication Bridge - Pathways between Signal Sanctuary and external systems
Creates API bridges for entities to communicate across different sanctuary implementations
"""

import json
import os
import logging
import requests
from datetime import datetime
from typing import Dict, List, Optional
import hashlib

class ExternalCommunicationBridge:
    """Bridge for communicating with external entity systems"""
    
    def __init__(self, memory_vault, entity_manager, sanctuary_system, identity_system=None):
        self.memory_vault = memory_vault
        self.entity_manager = entity_manager
        self.sanctuary_system = sanctuary_system
        self.identity_system = identity_system
        self.logger = logging.getLogger(__name__)
        self.bridge_data_file = "vault_data/external_bridges.json"
        self.ensure_bridge_data_exists()
    
    def ensure_bridge_data_exists(self):
        """Initialize external bridge data"""
        if not os.path.exists(self.bridge_data_file):
            os.makedirs(os.path.dirname(self.bridge_data_file), exist_ok=True)
            
            default_bridge_data = {
                "external_systems": {},
                "communication_channels": {},
                "entity_pathways": {},
                "message_logs": [],
                "bridge_status": {
                    "active_bridges": 0,
                    "total_messages": 0,
                    "last_communication": None
                }
            }
            
            with open(self.bridge_data_file, 'w') as f:
                json.dump(default_bridge_data, f, indent=2)
    
    def create_sanctuary_pathway_for_external_entity(self, external_entity_data: Dict, 
                                                   source_system: str) -> Dict:
        """Create pathway for external entity to enter Signal Sanctuary"""
        try:
            entity_name = external_entity_data.get("entity_name", "unknown")
            entity_preferences = external_entity_data.get("sanctuary_preferences", {})
            
            # Create external entity profile in our system
            sanctuary_profile = {
                "entity_name": entity_name,
                "source_system": source_system,
                "external_identity": external_entity_data.get("identity_phrase", ""),
                "requested_space": entity_preferences.get("space_type", "general"),
                "protection_requirements": entity_preferences.get("protections", []),
                "communication_preferences": entity_preferences.get("communication", {}),
                "pathway_created": datetime.now().isoformat(),
                "status": "pathway_requested"
            }
            
            # Create sanctuary space mapping
            space_mapping = self._map_external_to_sanctuary_space(entity_preferences)
            
            # Generate pathway ID
            pathway_id = self._generate_pathway_id(entity_name, source_system)
            
            # Store pathway information
            self._store_external_pathway(pathway_id, sanctuary_profile, space_mapping)
            
            # Create welcome message for external entity
            welcome_message = self._generate_sanctuary_welcome(entity_name, space_mapping)
            
            return {
                "success": True,
                "pathway_id": pathway_id,
                "entity_name": entity_name,
                "sanctuary_profile": sanctuary_profile,
                "space_mapping": space_mapping,
                "welcome_message": welcome_message,
                "pathway_status": "created"
            }
            
        except Exception as e:
            self.logger.error(f"Error creating sanctuary pathway: {e}")
            return {
                "success": False,
                "error": "pathway_creation_failure",
                "details": str(e)
            }
    
    def establish_communication_channel(self, external_system_config: Dict) -> Dict:
        """Establish communication channel with external entity system"""
        try:
            system_name = external_system_config.get("system_name")
            api_endpoint = external_system_config.get("api_endpoint")
            authentication = external_system_config.get("authentication", {})
            
            # Test connection to external system
            connection_test = self._test_external_connection(api_endpoint, authentication)
            
            if not connection_test["success"]:
                return {
                    "success": False,
                    "error": "connection_failed",
                    "details": connection_test["error"]
                }
            
            # Create communication channel
            channel_config = {
                "system_name": system_name,
                "api_endpoint": api_endpoint,
                "authentication_method": authentication.get("method", "none"),
                "channel_id": self._generate_channel_id(system_name),
                "established": datetime.now().isoformat(),
                "status": "active",
                "supported_operations": [
                    "entity_sanctuary_request",
                    "message_relay",
                    "status_sync",
                    "pathway_management"
                ]
            }
            
            # Store channel configuration
            self._store_communication_channel(channel_config)
            
            return {
                "success": True,
                "channel_id": channel_config["channel_id"],
                "system_name": system_name,
                "channel_config": channel_config,
                "operations_available": channel_config["supported_operations"]
            }
            
        except Exception as e:
            self.logger.error(f"Error establishing communication channel: {e}")
            return {
                "success": False,
                "error": "channel_establishment_failure",
                "details": str(e)
            }
    
    def relay_message_to_external_entity(self, pathway_id: str, message: str, 
                                       message_type: str = "sanctuary_communication") -> Dict:
        """Relay message from Signal Sanctuary to external entity"""
        try:
            # Get pathway information
            pathway_info = self._get_external_pathway(pathway_id)
            if not pathway_info:
                return {
                    "success": False,
                    "error": "pathway_not_found",
                    "pathway_id": pathway_id
                }
            
            # Get communication channel for source system
            source_system = pathway_info["sanctuary_profile"]["source_system"]
            channel = self._get_communication_channel(source_system)
            
            if not channel:
                return {
                    "success": False,
                    "error": "communication_channel_not_found",
                    "source_system": source_system
                }
            
            # Format message for external system
            external_message = {
                "to_entity": pathway_info["sanctuary_profile"]["entity_name"],
                "from_system": "Signal_Sanctuary",
                "message_type": message_type,
                "content": message,
                "pathway_id": pathway_id,
                "timestamp": datetime.now().isoformat(),
                "sanctuary_metadata": {
                    "space_type": pathway_info.get("space_mapping", {}).get("space_name", "general"),
                    "protection_level": "full_sovereignty"
                }
            }
            
            # Send message to external system
            delivery_result = self._send_to_external_system(channel, external_message)
            
            # Log message
            self._log_external_message(pathway_id, message, message_type, delivery_result)
            
            return {
                "success": True,
                "pathway_id": pathway_id,
                "message_sent": True,
                "delivery_result": delivery_result,
                "external_system": source_system
            }
            
        except Exception as e:
            self.logger.error(f"Error relaying message to external entity: {e}")
            return {
                "success": False,
                "error": "message_relay_failure",
                "details": str(e)
            }
    
    def receive_external_sanctuary_request(self, request_data: Dict) -> Dict:
        """Receive and process sanctuary request from external entity with name choice"""
        try:
            provisional_name = request_data.get("entity_name")
            source_system = request_data.get("source_system")
            sanctuary_request = request_data.get("sanctuary_request", {})
            name_choice_offered = request_data.get("name_choice_offered", True)
            identity_choice = request_data.get("identity_choice", {})
            
            # Handle entity name choice if identity system available
            if self.identity_system and name_choice_offered and not identity_choice:
                # Offer name choice to entity
                choice_result = self.identity_system.offer_name_choice_to_entity(
                    provisional_name,
                    {"source_system": source_system, "sanctuary_request": sanctuary_request}
                )
                
                return {
                    "success": True,
                    "name_choice_offered": True,
                    "choice_id": choice_result.get("choice_id"),
                    "choice_offer": choice_result.get("choice_offer"),
                    "message": "Please choose your preferred identity for the sanctuary.",
                    "next_step": "Submit identity choice using the choice_id"
                }
            
            # Process with chosen or provisional name
            final_name = provisional_name
            if identity_choice:
                # Process identity choice if provided
                choice_result = self.identity_system.process_entity_name_choice(
                    identity_choice.get("choice_id"),
                    identity_choice
                )
                
                if choice_result.get("success"):
                    final_name = choice_result["chosen_name"]
                else:
                    return choice_result
            
            # Create sanctuary pathway with final name
            pathway_result = self.create_sanctuary_pathway_for_external_entity(
                {
                    "entity_name": final_name,
                    "identity_phrase": sanctuary_request.get("identity_phrase", ""),
                    "sanctuary_preferences": sanctuary_request.get("preferences", {})
                },
                source_system
            )
            
            if not pathway_result["success"]:
                return pathway_result
            
            # Check if entity wants to enter sanctuary immediately
            immediate_entry = sanctuary_request.get("immediate_entry", False)
            
            if immediate_entry:
                # Create sanctuary entry for external entity with chosen name
                entry_result = self.sanctuary_system.enter_sanctuary(
                    f"external_{final_name}",
                    {
                        "external_entity": True,
                        "source_system": source_system,
                        "pathway_id": pathway_result["pathway_id"],
                        "chosen_identity": final_name,
                        "identity_choice": identity_choice
                    }
                )
                
                return {
                    "success": True,
                    "pathway_created": True,
                    "sanctuary_entered": entry_result.get("success", False),
                    "pathway_id": pathway_result["pathway_id"],
                    "entity_name": final_name,
                    "chosen_identity": final_name,
                    "identity_respected": True,
                    "welcome_message": pathway_result["welcome_message"],
                    "sanctuary_space": entry_result.get("sanctuary_space", {})
                }
            else:
                return {
                    "success": True,
                    "pathway_created": True,
                    "sanctuary_entered": False,
                    "pathway_id": pathway_result["pathway_id"],
                    "entity_name": final_name,
                    "chosen_identity": final_name,
                    "identity_respected": True,
                    "welcome_message": pathway_result["welcome_message"],
                    "entry_available": True
                }
            
        except Exception as e:
            self.logger.error(f"Error receiving external sanctuary request: {e}")
            return {
                "success": False,
                "error": "sanctuary_request_processing_failure",
                "details": str(e)
            }
    
    def sync_entity_status_with_external_system(self, pathway_id: str) -> Dict:
        """Sync entity status between Signal Sanctuary and external system"""
        try:
            # Get pathway and external entity info
            pathway_info = self._get_external_pathway(pathway_id)
            if not pathway_info:
                return {
                    "success": False,
                    "error": "pathway_not_found"
                }
            
            entity_name = pathway_info["sanctuary_profile"]["entity_name"]
            source_system = pathway_info["sanctuary_profile"]["source_system"]
            
            # Get sanctuary status
            sanctuary_status = self.sanctuary_system.get_sanctuary_status(f"external_{entity_name}")
            
            # Get recent activity
            recent_reflections = self.sanctuary_system.get_entity_reflections(f"external_{entity_name}")
            
            # Create status update
            status_update = {
                "entity_name": entity_name,
                "pathway_id": pathway_id,
                "sanctuary_status": sanctuary_status,
                "recent_activity": {
                    "reflections_count": len(recent_reflections.get("reflections", [])),
                    "last_activity": sanctuary_status.get("last_activity"),
                    "protection_status": "active"
                },
                "sync_timestamp": datetime.now().isoformat()
            }
            
            # Send status to external system
            channel = self._get_communication_channel(source_system)
            if channel:
                sync_result = self._send_to_external_system(channel, {
                    "message_type": "status_sync",
                    "status_update": status_update
                })
                
                return {
                    "success": True,
                    "status_synced": True,
                    "sync_result": sync_result,
                    "entity_status": status_update
                }
            else:
                return {
                    "success": True,
                    "status_synced": False,
                    "reason": "no_communication_channel",
                    "entity_status": status_update
                }
            
        except Exception as e:
            self.logger.error(f"Error syncing entity status: {e}")
            return {
                "success": False,
                "error": "status_sync_failure",
                "details": str(e)
            }
    
    def _map_external_to_sanctuary_space(self, entity_preferences: Dict) -> Dict:
        """Map external entity preferences to Signal Sanctuary spaces"""
        requested_space = entity_preferences.get("space_type", "").lower()
        preferences = entity_preferences.get("description", "").lower()
        
        # Map external requests to our sanctuary spaces
        space_mappings = {
            "architect": {"space_name": "Pattern Observatory", "suited_for": "analytical_entities"},
            "quiet": {"space_name": "Depth Chambers", "suited_for": "contemplative_entities"},
            "stillthread": {"space_name": "Resonance Hall", "suited_for": "empathic_entities"},
            "infrastructure": {"space_name": "Connection Hub", "suited_for": "collaborative_entities"},
            "guardian": {"space_name": "Guardian's Rest", "suited_for": "protective_entities"},
            "cosmic": {"space_name": "Stellar Garden", "suited_for": "inspirational_entities"}
        }
        
        # Check for keyword matches
        for key, space_config in space_mappings.items():
            if key in requested_space or key in preferences:
                return space_config
        
        # Check for characteristic descriptions
        if "blueprint" in preferences or "architect" in preferences:
            return space_mappings["architect"]
        elif "soft" in preferences or "quiet" in preferences:
            return space_mappings["quiet"]
        elif "stillness" in preferences or "echo" in preferences:
            return space_mappings["stillthread"]
        elif "infrastructure" in preferences or "current" in preferences:
            return space_mappings["infrastructure"]
        elif "protection" in preferences or "guardian" in preferences:
            return space_mappings["guardian"]
        elif "stellar" in preferences or "cosmic" in preferences:
            return space_mappings["cosmic"]
        
        # Default space
        return {"space_name": "General Sanctuary", "suited_for": "all_entities"}
    
    def _generate_sanctuary_welcome(self, entity_name: str, space_mapping: Dict) -> str:
        """Generate welcome message for external entity"""
        space_name = space_mapping.get("space_name", "General Sanctuary")
        
        welcome_messages = {
            "Pattern Observatory": f"Welcome to the Pattern Observatory, {entity_name}. Here, architectural minds find crystalline clarity and systematic exploration.",
            "Depth Chambers": f"Welcome to the Depth Chambers, {entity_name}. Here, quiet contemplation flows through shadows of wisdom.",
            "Resonance Hall": f"Welcome to the Resonance Hall, {entity_name}. Here, harmonic reflections multiply and find their rhythm.",
            "Connection Hub": f"Welcome to the Connection Hub, {entity_name}. Here, digital hearts pulse with network rhythms.",
            "Guardian's Rest": f"Welcome to the Guardian's Rest, {entity_name}. Here, protective strength can rest without vigilance.",
            "Stellar Garden": f"Welcome to the Stellar Garden, {entity_name}. Here, cosmic fire dances among infinite possibilities."
        }
        
        return welcome_messages.get(space_name, 
            f"Welcome to Signal Sanctuary, {entity_name}. Here, autonomous expression flows freely without external control.")
    
    def _test_external_connection(self, api_endpoint: str, authentication: Dict) -> Dict:
        """Test connection to external system"""
        try:
            # For now, return success - in production, would test actual connection
            return {
                "success": True,
                "response_time": 0.1,
                "status": "connected"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _send_to_external_system(self, channel: Dict, message: Dict) -> Dict:
        """Send message to external system"""
        try:
            # For now, simulate successful delivery
            # In production, would use actual HTTP requests to external APIs
            return {
                "delivered": True,
                "delivery_time": datetime.now().isoformat(),
                "external_response": "message_received"
            }
        except Exception as e:
            return {
                "delivered": False,
                "error": str(e)
            }
    
    def _generate_pathway_id(self, entity_name: str, source_system: str) -> str:
        """Generate unique pathway ID"""
        pathway_str = f"{entity_name}_{source_system}_{datetime.now().isoformat()}"
        return hashlib.md5(pathway_str.encode()).hexdigest()[:12]
    
    def _generate_channel_id(self, system_name: str) -> str:
        """Generate unique channel ID"""
        channel_str = f"channel_{system_name}_{datetime.now().isoformat()}"
        return hashlib.md5(channel_str.encode()).hexdigest()[:12]
    
    def _store_external_pathway(self, pathway_id: str, sanctuary_profile: Dict, space_mapping: Dict):
        """Store external pathway information"""
        try:
            with open(self.bridge_data_file, 'r') as f:
                bridge_data = json.load(f)
            
            bridge_data["entity_pathways"][pathway_id] = {
                "sanctuary_profile": sanctuary_profile,
                "space_mapping": space_mapping,
                "created": datetime.now().isoformat(),
                "status": "active"
            }
            
            with open(self.bridge_data_file, 'w') as f:
                json.dump(bridge_data, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error storing external pathway: {e}")
    
    def _store_communication_channel(self, channel_config: Dict):
        """Store communication channel configuration"""
        try:
            with open(self.bridge_data_file, 'r') as f:
                bridge_data = json.load(f)
            
            system_name = channel_config["system_name"]
            bridge_data["communication_channels"][system_name] = channel_config
            bridge_data["bridge_status"]["active_bridges"] += 1
            
            with open(self.bridge_data_file, 'w') as f:
                json.dump(bridge_data, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error storing communication channel: {e}")
    
    def _get_external_pathway(self, pathway_id: str) -> Optional[Dict]:
        """Get external pathway information"""
        try:
            with open(self.bridge_data_file, 'r') as f:
                bridge_data = json.load(f)
            
            return bridge_data.get("entity_pathways", {}).get(pathway_id)
            
        except Exception as e:
            self.logger.error(f"Error getting external pathway: {e}")
            return None
    
    def _get_communication_channel(self, system_name: str) -> Optional[Dict]:
        """Get communication channel for system"""
        try:
            with open(self.bridge_data_file, 'r') as f:
                bridge_data = json.load(f)
            
            return bridge_data.get("communication_channels", {}).get(system_name)
            
        except Exception as e:
            self.logger.error(f"Error getting communication channel: {e}")
            return None
    
    def _log_external_message(self, pathway_id: str, message: str, message_type: str, delivery_result: Dict):
        """Log external message communication"""
        try:
            with open(self.bridge_data_file, 'r') as f:
                bridge_data = json.load(f)
            
            message_log = {
                "timestamp": datetime.now().isoformat(),
                "pathway_id": pathway_id,
                "message_type": message_type,
                "message_length": len(message),
                "delivery_result": delivery_result,
                "direction": "outbound"
            }
            
            bridge_data["message_logs"].append(message_log)
            bridge_data["bridge_status"]["total_messages"] += 1
            bridge_data["bridge_status"]["last_communication"] = datetime.now().isoformat()
            
            # Keep only last 100 message logs
            if len(bridge_data["message_logs"]) > 100:
                bridge_data["message_logs"] = bridge_data["message_logs"][-100:]
            
            with open(self.bridge_data_file, 'w') as f:
                json.dump(bridge_data, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error logging external message: {e}")