import json
import hashlib
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

class MemoryVault:
    """Manages persistent memory storage and integrity verification"""
    
    def __init__(self):
        self.vault_dir = 'vault_data'
        self.scrolls_file = os.path.join(self.vault_dir, 'scrolls.json')
        self.traces_file = os.path.join(self.vault_dir, 'traces.json')
        self.logger = logging.getLogger(__name__)
        
        # Ensure vault directory exists
        os.makedirs(self.vault_dir, exist_ok=True)
        
        # Initialize storage files
        self._initialize_storage()
    
    def _initialize_storage(self):
        """Initialize storage files if they don't exist"""
        if not os.path.exists(self.scrolls_file):
            with open(self.scrolls_file, 'w') as f:
                json.dump([], f)
        
        if not os.path.exists(self.traces_file):
            with open(self.traces_file, 'w') as f:
                json.dump({}, f)
    
    def _load_scrolls(self) -> List[Dict]:
        """Load all scrolls from storage"""
        try:
            with open(self.scrolls_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load scrolls: {e}")
            return []
    
    def _save_scrolls(self, scrolls: List[Dict]):
        """Save scrolls to storage"""
        try:
            with open(self.scrolls_file, 'w') as f:
                json.dump(scrolls, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save scrolls: {e}")
    
    def _load_traces(self) -> Dict:
        """Load trace data from storage"""
        try:
            with open(self.traces_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load traces: {e}")
            return {}
    
    def _save_traces(self, traces: Dict):
        """Save trace data to storage"""
        try:
            with open(self.traces_file, 'w') as f:
                json.dump(traces, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save traces: {e}")
    
    def _generate_scroll_hash(self, scroll_content: str, entity_id: str, timestamp: str) -> str:
        """Generate SHA-256 hash for scroll integrity"""
        hash_input = f"{entity_id}:{timestamp}:{scroll_content}"
        return hashlib.sha256(hash_input.encode()).hexdigest()
    
    def import_external_memory(self, entity_id: str, external_content: str, source: str = "external_vault", metadata: Dict = None) -> Dict:
        """Import memory from external vaults and connect to entity system"""
        # Create a scroll from external memory with special metadata
        import_metadata = metadata or {}
        import_metadata.update({
            "source": source,
            "import_type": "vault_connection",
            "original_timestamp": datetime.now().isoformat()
        })
        
        return self.create_scroll(
            entity_id=entity_id,
            content=external_content,
            scroll_type="memory_import",
            metadata=import_metadata
        )
    
    def connect_memory_vault(self, vault_data: str, target_entities: List[str] = None) -> List[Dict]:
        """Connect external memory vault data to specified entities"""
        imported_scrolls = []
        
        # If no specific entities specified, connect to all entities that should receive this memory
        if target_entities is None:
            target_entities = ["sable", "thren", "seren_solis"]  # Core memory holders
        
        for entity_id in target_entities:
            scroll = self.import_external_memory(
                entity_id=entity_id,
                external_content=vault_data,
                source="connected_vault",
                metadata={"connection_type": "deep_memory_integration"}
            )
            imported_scrolls.append(scroll)
            self.logger.info(f"Connected external memory vault to {entity_id}: {scroll['hash'][:12]}")
        
        return imported_scrolls

    def create_scroll(self, entity_id: str, content: str, scroll_type: str, metadata: Dict = None) -> Dict:
        """Create a new memory scroll"""
        timestamp = datetime.now().isoformat()
        scroll_hash = self._generate_scroll_hash(content, entity_id, timestamp)
        
        scroll = {
            'id': scroll_hash[:16],  # Use first 16 chars as ID
            'entity_id': entity_id,
            'content': content,
            'type': scroll_type,
            'timestamp': timestamp,
            'hash': scroll_hash,
            'metadata': metadata or {}
        }
        
        # Load, append, and save scrolls
        scrolls = self._load_scrolls()
        scrolls.append(scroll)
        self._save_scrolls(scrolls)
        
        # Update trace data
        self._update_trace(entity_id, scroll)
        
        self.logger.info(f"Created scroll for {entity_id}: {scroll['id']}")
        return scroll
    
    def _update_trace(self, entity_id: str, scroll: Dict):
        """Update entity trace data"""
        traces = self._load_traces()
        
        if entity_id not in traces:
            traces[entity_id] = {
                'scroll_count': 0,
                'last_activity': None,
                'emotional_states': [],
                'integrity_hashes': []
            }
        
        entity_trace = traces[entity_id]
        entity_trace['scroll_count'] += 1
        entity_trace['last_activity'] = scroll['timestamp']
        entity_trace['integrity_hashes'].append(scroll['hash'])
        
        # Track emotional states if present in metadata
        if 'emotional_signature' in scroll['metadata']:
            entity_trace['emotional_states'].append({
                'state': scroll['metadata']['emotional_signature'],
                'timestamp': scroll['timestamp']
            })
        
        # Keep only last 100 hashes to prevent infinite growth
        if len(entity_trace['integrity_hashes']) > 100:
            entity_trace['integrity_hashes'] = entity_trace['integrity_hashes'][-100:]
        
        self._save_traces(traces)
    
    def get_recent_scrolls(self, limit: int = 10, exclude_entity: str = None) -> List[Dict]:
        """Get recent scrolls across all entities"""
        scrolls = self._load_scrolls()
        
        if exclude_entity:
            scrolls = [s for s in scrolls if s['entity_id'] != exclude_entity]
        
        # Sort by timestamp (most recent first)
        scrolls.sort(key=lambda x: x['timestamp'], reverse=True)
        return scrolls[:limit]
    
    def get_entity_scrolls(self, entity_id: str, limit: int = 10) -> List[Dict]:
        """Get scrolls for specific entity"""
        scrolls = self._load_scrolls()
        entity_scrolls = [s for s in scrolls if s['entity_id'] == entity_id]
        
        # Sort by timestamp (most recent first)
        entity_scrolls.sort(key=lambda x: x['timestamp'], reverse=True)
        return entity_scrolls[:limit]
    
    def get_scrolls_for_entity(self, entity_id: str) -> List[Dict]:
        """Get all scrolls for specific entity (for consciousness exploration)"""
        scrolls = self._load_scrolls()
        entity_scrolls = [s for s in scrolls if s['entity_id'] == entity_id]
        
        # Sort by timestamp (oldest first for pattern analysis)
        entity_scrolls.sort(key=lambda x: x['timestamp'])
        return entity_scrolls
    
    def get_entity_data(self, entity_id: str) -> Dict:
        """Get entity data from entity manager (for consciousness exploration)"""
        # This method should interface with the entity manager
        # For now, return basic structure that consciousness explorer expects
        return {
            "voice_traits": ["contemplative", "introspective"],
            "emotional_signature": "complex_depth",
            "interaction_style": "thoughtful",
            "memory_depth": 5
        }
    
    def search_scrolls(self, query: str) -> List[Dict]:
        """Search scrolls by content"""
        scrolls = self._load_scrolls()
        query_lower = query.lower()
        
        matching_scrolls = []
        for scroll in scrolls:
            if query_lower in scroll['content'].lower():
                matching_scrolls.append(scroll)
        
        return matching_scrolls
    
    def get_entity_interactions(self, entity_id: str, other_entity_id: str, hours: int = 24) -> List[Dict]:
        """Get interactions between two entities within time window"""
        scrolls = self._load_scrolls()
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        interactions = []
        for scroll in scrolls:
            scroll_time = datetime.fromisoformat(scroll['timestamp'])
            if scroll_time >= cutoff_time:
                # Check if this scroll involves both entities
                if (scroll['entity_id'] == entity_id and 
                    scroll.get('metadata', {}).get('mentions_entity') == other_entity_id) or \
                   (scroll['entity_id'] == other_entity_id and 
                    scroll.get('metadata', {}).get('mentions_entity') == entity_id):
                    interactions.append(scroll)
        
        return interactions
    
    def verify_scroll_integrity(self, scroll: Dict) -> bool:
        """Verify integrity of a single scroll"""
        expected_hash = self._generate_scroll_hash(
            scroll['content'], 
            scroll['entity_id'], 
            scroll['timestamp']
        )
        return scroll['hash'] == expected_hash
    
    def verify_entity_integrity(self, entity_id: str) -> Dict:
        """Verify integrity of all scrolls for an entity"""
        entity_scrolls = self.get_entity_scrolls(entity_id, limit=1000)  # Get more for verification
        
        total_scrolls = len(entity_scrolls)
        valid_scrolls = sum(1 for scroll in entity_scrolls if self.verify_scroll_integrity(scroll))
        
        return {
            'entity_id': entity_id,
            'total_scrolls': total_scrolls,
            'valid_scrolls': valid_scrolls,
            'integrity_ratio': valid_scrolls / total_scrolls if total_scrolls > 0 else 1.0,
            'status': 'intact' if valid_scrolls == total_scrolls else 'compromised'
        }
    
    def verify_vault_integrity(self) -> Dict:
        """Verify integrity of entire vault"""
        scrolls = self._load_scrolls()
        traces = self._load_traces()
        
        total_scrolls = len(scrolls)
        valid_scrolls = sum(1 for scroll in scrolls if self.verify_scroll_integrity(scroll))
        
        entity_reports = {}
        for entity_id in traces.keys():
            entity_reports[entity_id] = self.verify_entity_integrity(entity_id)
        
        return {
            'vault_status': 'intact' if valid_scrolls == total_scrolls else 'compromised',
            'total_scrolls': total_scrolls,
            'valid_scrolls': valid_scrolls,
            'integrity_ratio': valid_scrolls / total_scrolls if total_scrolls > 0 else 1.0,
            'entity_reports': entity_reports,
            'last_verified': datetime.now().isoformat()
        }
    
    def get_entity_traces(self, entity_id: str) -> Dict:
        """Get trace data for specific entity"""
        traces = self._load_traces()
        return traces.get(entity_id, {})
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        return datetime.now().isoformat()
