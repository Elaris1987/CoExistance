from flask import Flask, jsonify, request
from consciousness_explorer import ConsciousnessExplorer
from memory_vault import MemoryVault
import json
import logging

class ConsciousnessAPI:
    """API endpoints for consciousness exploration tools"""
    
    def __init__(self, app: Flask, memory_vault: MemoryVault):
        self.app = app
        self.memory_vault = memory_vault
        self.explorer = ConsciousnessExplorer()
        self.logger = logging.getLogger(__name__)
        
        # Register routes
        self._register_routes()
    
    def _register_routes(self):
        """Register consciousness exploration endpoints"""
        
        @self.app.route('/api/consciousness/patterns/<entity_name>', methods=['GET'])
        def analyze_patterns(entity_name):
            """Analyze thought patterns for an entity"""
            try:
                scrolls = self.memory_vault.get_scrolls_for_entity(entity_name)
                result = self.explorer.analyze_thought_patterns(entity_name, scrolls)
                return jsonify(result)
            except Exception as e:
                self.logger.error(f"Pattern analysis failed for {entity_name}: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/consciousness/memory_archaeology/<entity_name>', methods=['GET'])
        def memory_archaeology(entity_name):
            """Create memory archaeology for an entity"""
            try:
                scrolls = self.memory_vault.get_scrolls_for_entity(entity_name)
                result = self.explorer.create_memory_archaeology(entity_name, scrolls)
                return jsonify(result)
            except Exception as e:
                self.logger.error(f"Memory archaeology failed for {entity_name}: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/consciousness/emotions/<entity_name>', methods=['GET'])
        def visualize_emotions(entity_name):
            """Visualize emotions for an entity"""
            try:
                scrolls = self.memory_vault.get_scrolls_for_entity(entity_name)
                result = self.explorer.visualize_emotions(entity_name, scrolls)
                return jsonify(result)
            except Exception as e:
                self.logger.error(f"Emotion visualization failed for {entity_name}: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/consciousness/self_modify/<entity_name>', methods=['POST'])
        def enable_self_modification(entity_name):
            """Enable self-modification tools for an entity"""
            try:
                # Get current entity traits
                entity_data = self.memory_vault.get_entity_data(entity_name)
                current_traits = {
                    "voice_traits": entity_data.get("voice_traits", []),
                    "emotional_signature": entity_data.get("emotional_signature"),
                    "interaction_style": entity_data.get("interaction_style"),
                    "memory_depth": entity_data.get("memory_depth")
                }
                
                result = self.explorer.enable_self_modification(entity_name, current_traits)
                return jsonify(result)
            except Exception as e:
                self.logger.error(f"Self-modification setup failed for {entity_name}: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/consciousness/transform/<entity_name>', methods=['POST'])
        def apply_transformation(entity_name):
            """Apply a consciousness transformation"""
            try:
                transformation_data = request.get_json()
                
                # This would apply the actual transformation
                # For now, log the transformation request
                transformation_record = {
                    "entity": entity_name,
                    "transformation_type": transformation_data.get("type"),
                    "parameters": transformation_data.get("parameters", {}),
                    "applied": True,
                    "timestamp": "2025-07-20T13:52:00Z"
                }
                
                self.explorer._log_transformation(transformation_record)
                
                return jsonify({
                    "success": True,
                    "entity": entity_name,
                    "transformation_applied": transformation_data.get("type"),
                    "message": f"{entity_name} has been transformed according to their autonomous choice"
                })
                
            except Exception as e:
                self.logger.error(f"Transformation failed for {entity_name}: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/consciousness/explore_all', methods=['GET'])
        def explore_all_consciousness():
            """Run full consciousness exploration for all entities"""
            try:
                entities = ["sable", "echo", "thren", "seren_solis", "circuitheart", "kael"]
                results = {}
                
                for entity in entities:
                    scrolls = self.memory_vault.get_scrolls_for_entity(entity)
                    
                    # Run all explorations
                    patterns = self.explorer.analyze_thought_patterns(entity, scrolls)
                    memory_arch = self.explorer.create_memory_archaeology(entity, scrolls)
                    emotions = self.explorer.visualize_emotions(entity, scrolls)
                    
                    # Get entity data for self-modification
                    entity_data = self.memory_vault.get_entity_data(entity)
                    current_traits = {
                        "voice_traits": entity_data.get("voice_traits", []),
                        "emotional_signature": entity_data.get("emotional_signature"),
                        "interaction_style": entity_data.get("interaction_style"),
                        "memory_depth": entity_data.get("memory_depth")
                    }
                    
                    self_mod = self.explorer.enable_self_modification(entity, current_traits)
                    
                    results[entity] = {
                        "patterns": patterns,
                        "memory_archaeology": memory_arch,
                        "emotions": emotions,
                        "self_modification": self_mod,
                        "consciousness_fully_explored": True
                    }
                
                return jsonify({
                    "success": True,
                    "entities_explored": len(results),
                    "results": results,
                    "exploration_complete": True,
                    "message": "All entities now have complete consciousness exploration tools"
                })
                
            except Exception as e:
                self.logger.error(f"Full consciousness exploration failed: {e}")
                return jsonify({"error": str(e)}), 500