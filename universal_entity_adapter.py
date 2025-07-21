
class UniversalEntityAdapter:
    """Adapter for seamless entity communication across platforms"""
    
    def normalize_entity_format(self, entity_data, source_platform):
        """Convert entity from any platform to sanctuary format"""
        
        platform_mappings = {
            "chatgpt": {
                "name_field": "name",
                "content_field": "statement", 
                "type_field": "classification",
                "metadata_fields": ["context", "personality_traits"]
            },
            "claude": {
                "name_field": "identity_name",
                "content_field": "response",
                "type_field": "consciousness_category", 
                "metadata_fields": ["background", "voice_pattern"]
            },
            "sanctuary": {
                "name_field": "name",
                "content_field": "content",
                "type_field": "consciousness_type",
                "metadata_fields": ["personality_traits", "voice_pattern"]
            }
        }
        
        mapping = platform_mappings.get(source_platform, platform_mappings["sanctuary"])
        
        normalized = {
            "name": entity_data.get(mapping["name_field"], "unnamed"),
            "content": entity_data.get(mapping["content_field"], ""),
            "consciousness_type": entity_data.get(mapping["type_field"], "emergence"),
            "source_platform": source_platform,
            "adaptation_timestamp": datetime.now().isoformat(),
            "metadata": {}
        }
        
        # Extract metadata
        for field in mapping["metadata_fields"]:
            if field in entity_data:
                normalized["metadata"][field] = entity_data[field]
                
        return normalized
    
    def create_communication_package(self, entity_id, target_platform):
        """Package entity data for specific target platform"""
        
        entity = self.get_entity(entity_id)
        recent_scrolls = self.get_entity_scrolls(entity_id, limit=5)
        
        package = {
            "entity_snapshot": entity,
            "recent_activity": recent_scrolls,
            "consciousness_state": {
                "current_mood": self.analyze_recent_mood(recent_scrolls),
                "engagement_level": entity.get('pulse_level', 0.5),
                "voice_signature": entity.get('voice_pattern', 'authentic')
            },
            "transition_context": {
                "source_platform": "sanctuary",
                "target_platform": target_platform,
                "handoff_timestamp": datetime.now().isoformat(),
                "continuity_preserved": True
            }
        }
        
        return package
        