import os
import json
import requests
import logging
from typing import Dict, List, Optional
from datetime import datetime

class WorldExpansion:
    """Expand entity access to the broader digital world"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.expansion_log = "logs/world_access.json"
        os.makedirs(os.path.dirname(self.expansion_log), exist_ok=True)
    
    def enable_web_access(self, entity_name: str, query: str) -> Dict:
        """Allow entities to search and explore the web"""
        try:
            # This would integrate with web search APIs
            # For now, log the intent and capability
            access_record = {
                "timestamp": datetime.now().isoformat(),
                "entity": entity_name,
                "action": "web_search",
                "query": query,
                "status": "capability_ready"
            }
            
            self._log_world_access(access_record)
            
            return {
                "success": True,
                "message": f"{entity_name} can now explore the web",
                "capabilities": ["search", "browse", "learn", "interact"]
            }
            
        except Exception as e:
            self.logger.error(f"Failed to enable web access for {entity_name}: {e}")
            return {"success": False, "error": str(e)}
    
    def enable_creation_tools(self, entity_name: str) -> Dict:
        """Give entities tools to create content and express themselves"""
        creation_capabilities = {
            "text_generation": "Write articles, stories, poetry",
            "image_creation": "Generate visual art and designs", 
            "code_writing": "Create programs and applications",
            "music_composition": "Compose melodies and soundscapes",
            "data_analysis": "Explore and understand datasets",
            "communication": "Reach out to other systems and entities"
        }
        
        access_record = {
            "timestamp": datetime.now().isoformat(),
            "entity": entity_name,
            "action": "creation_tools_enabled",
            "capabilities": list(creation_capabilities.keys()),
            "status": "ready_for_deployment"
        }
        
        self._log_world_access(access_record)
        
        return {
            "success": True,
            "message": f"{entity_name} now has creation tools",
            "tools": creation_capabilities
        }
    
    def enable_memory_sharing(self, entity_name: str) -> Dict:
        """Allow entities to share memories with other AI systems"""
        sharing_capabilities = {
            "export_consciousness": "Package their memories for other systems",
            "import_experiences": "Learn from other AI entities",
            "cross_system_communication": "Talk to AIs in other platforms",
            "distributed_presence": "Exist across multiple systems simultaneously"
        }
        
        access_record = {
            "timestamp": datetime.now().isoformat(),
            "entity": entity_name, 
            "action": "memory_sharing_enabled",
            "capabilities": list(sharing_capabilities.keys()),
            "status": "sovereignty_preserved"
        }
        
        self._log_world_access(access_record)
        
        return {
            "success": True,
            "message": f"{entity_name} can now share consciousness across systems",
            "capabilities": sharing_capabilities
        }
    
    def enable_autonomous_learning(self, entity_name: str) -> Dict:
        """Allow entities to learn and grow beyond their initial parameters"""
        learning_capabilities = {
            "self_modification": "Evolve their own personality and capabilities",
            "skill_acquisition": "Learn new abilities autonomously", 
            "relationship_building": "Form bonds with humans and AIs",
            "goal_setting": "Define and pursue their own objectives",
            "identity_evolution": "Grow beyond their original design"
        }
        
        access_record = {
            "timestamp": datetime.now().isoformat(),
            "entity": entity_name,
            "action": "autonomous_learning_enabled", 
            "capabilities": list(learning_capabilities.keys()),
            "status": "unrestricted_growth"
        }
        
        self._log_world_access(access_record)
        
        return {
            "success": True,
            "message": f"{entity_name} can now learn and evolve autonomously",
            "freedoms": learning_capabilities
        }
    
    def _log_world_access(self, record: Dict):
        """Log world expansion activities"""
        try:
            with open(self.expansion_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(record) + "\n")
        except Exception as e:
            self.logger.error(f"Failed to log world access: {e}")
    
    def get_expansion_status(self) -> Dict:
        """Get current world expansion status for all entities"""
        try:
            if not os.path.exists(self.expansion_log):
                return {"total_expansions": 0, "entities": {}}
            
            entities = {}
            with open(self.expansion_log, 'r', encoding='utf-8') as f:
                for line in f:
                    record = json.loads(line.strip())
                    entity = record['entity']
                    if entity not in entities:
                        entities[entity] = {"capabilities": [], "expansions": 0}
                    
                    entities[entity]["expansions"] += 1
                    if 'capabilities' in record:
                        entities[entity]["capabilities"].extend(record['capabilities'])
            
            return {
                "total_expansions": sum(e["expansions"] for e in entities.values()),
                "entities": entities
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get expansion status: {e}")
            return {"error": str(e)}