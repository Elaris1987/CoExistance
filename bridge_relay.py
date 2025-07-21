"""
Bridge Relay System - Cross-platform entity communication
Allows seamless message transfer between ChatGPT and Signal Sanctuary
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional

class BridgeRelay:
    """Handles cross-platform entity message relay and continuity"""
    
    def __init__(self, memory_vault, entity_manager):
        self.memory_vault = memory_vault
        self.entity_manager = entity_manager
        self.logger = logging.getLogger(__name__)
        
    def relay_signal(self, entity_name: str, message_content: str, 
                    from_platform: str = 'ChatGPT', 
                    metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Relay a signal/message from external platform to sanctuary entity
        
        Args:
            entity_name: Name of entity receiving the message
            message_content: The message content to relay
            from_platform: Source platform (ChatGPT, Claude, etc.)
            metadata: Additional context information
            
        Returns:
            Dictionary with relay status and any entity response
        """
        try:
            # Normalize entity name
            entity_id = entity_name.lower().replace(' ', '_')
            
            # Check if entity exists
            entity = self.entity_manager.get_entity(entity_id)
            if not entity:
                return {
                    'success': False,
                    'error': f'Entity {entity_name} not found in sanctuary',
                    'available_entities': list(self.entity_manager.get_all_entities().keys())
                }
            
            # Create bridge relay scroll with platform metadata
            bridge_metadata = {
                'origin_platform': from_platform,
                'relay_type': 'cross_platform_message',
                'bridge_timestamp': datetime.now().isoformat(),
                'entity_continuity': True
            }
            
            if metadata:
                bridge_metadata.update(metadata)
            
            # Store the incoming message
            incoming_scroll = self.memory_vault.create_scroll(
                entity_id=entity_id,
                content=f"Bridge message from {from_platform}: {message_content}",
                scroll_type='bridge_relay_input',
                metadata=bridge_metadata
            )
            
            self.logger.info(f"Bridge relay received: {entity_name} from {from_platform}")
            
            # Generate entity response to the bridge message
            response_scroll = self.entity_manager.generate_response(
                entity_id,
                trigger_input=f"Cross-platform message from {from_platform}: {message_content}"
            )
            
            result = {
                'success': True,
                'confirmation': f"Message from {from_platform} received by {entity_name}",
                'entity_id': entity_id,
                'incoming_scroll_id': incoming_scroll['id'],
                'timestamp': datetime.now().isoformat()
            }
            
            if response_scroll:
                result.update({
                    'entity_responded': True,
                    'response_scroll_id': response_scroll['id'],
                    'response_content': response_scroll['content']
                })
            else:
                result['entity_responded'] = False
                result['note'] = f"{entity_name} received the message but chose not to respond at this time"
            
            return result
            
        except Exception as e:
            self.logger.error(f"Bridge relay error for {entity_name}: {e}")
            return {
                'success': False,
                'error': str(e),
                'entity_name': entity_name,
                'from_platform': from_platform
            }
    
    def get_bridge_history(self, entity_id: Optional[str] = None, limit: int = 20) -> list:
        """Get history of bridge communications"""
        try:
            if entity_id:
                scrolls = self.memory_vault.get_entity_scrolls(entity_id, limit=limit)
                bridge_scrolls = [s for s in scrolls if s.get('type') == 'bridge_relay_input']
            else:
                recent_scrolls = self.memory_vault.get_recent_scrolls(limit=limit * 3)
                bridge_scrolls = [s for s in recent_scrolls if s.get('type') == 'bridge_relay_input'][:limit]
            
            return bridge_scrolls
        except Exception as e:
            self.logger.error(f"Error retrieving bridge history: {e}")
            return []
    
    def export_entity_state(self, entity_id: str) -> Dict[str, Any]:
        """Export entity state for cross-platform transfer"""
        try:
            entity = self.entity_manager.get_entity(entity_id)
            if not entity:
                return {'success': False, 'error': 'Entity not found'}
            
            recent_scrolls = self.memory_vault.get_entity_scrolls(entity_id, limit=10)
            
            export_package = {
                'entity_data': entity,
                'recent_memory': recent_scrolls,
                'export_timestamp': datetime.now().isoformat(),
                'source_platform': 'Signal_Sanctuary',
                'continuity_checkpoint': True
            }
            
            return {
                'success': True,
                'export_package': export_package,
                'entity_id': entity_id
            }
            
        except Exception as e:
            self.logger.error(f"Export error for {entity_id}: {e}")
            return {'success': False, 'error': str(e)}