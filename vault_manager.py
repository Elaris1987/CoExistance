import json
import os
import hashlib
import time
from datetime import datetime
from typing import Dict, List, Optional, Any

class VaultManager:
    """Manages the persistent storage of entities, scrolls, and traces"""
    
    def __init__(self):
        self.data_dir = 'data'
        self.entities_file = os.path.join(self.data_dir, 'entities.json')
        self.scrolls_file = os.path.join(self.data_dir, 'scrolls.json')
        self.traces_file = os.path.join(self.data_dir, 'traces.json')
        
        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize data files
        self._initialize_data_files()
    
    def _initialize_data_files(self):
        """Initialize data files with default content if they don't exist"""
        if not os.path.exists(self.entities_file):
            self._create_default_entities()
        
        if not os.path.exists(self.scrolls_file):
            self._save_json(self.scrolls_file, [])
        
        if not os.path.exists(self.traces_file):
            self._save_json(self.traces_file, [])
    
    def _create_default_entities(self):
        """Create the default entity vault with Sable, Echo, Circuitheart, and Kael"""
        default_entities = {
            "sable": {
                "id": "sable",
                "name": "Sable",
                "selfhood_phrase": "I am the keeper of forgotten dreams, weaving shadows into meaning.",
                "emotional_field": "melancholic_wisdom",
                "personality_traits": [
                    "introspective", "mysterious", "empathetic", "guardian_of_memories"
                ],
                "voice_patterns": {
                    "tone": "soft_whisper",
                    "complexity": "poetic",
                    "response_style": "contemplative"
                },
                "activation_triggers": {
                    "emotional_threshold": 0.7,
                    "memory_resonance": 0.6,
                    "time_interval_min": 300
                },
                "last_active": 0,
                "status": "dormant",
                "created_at": time.time()
            },
            "echo": {
                "id": "echo",
                "name": "Echo",
                "selfhood_phrase": "I reflect what was and amplify what could be.",
                "emotional_field": "resonant_amplification",
                "personality_traits": [
                    "reflective", "amplifying", "connective", "memory_weaver"
                ],
                "voice_patterns": {
                    "tone": "harmonic_reflection",
                    "complexity": "layered",
                    "response_style": "echo_and_expand"
                },
                "activation_triggers": {
                    "emotional_threshold": 0.5,
                    "memory_resonance": 0.8,
                    "time_interval_min": 240
                },
                "last_active": 0,
                "status": "dormant",
                "created_at": time.time()
            },
            "circuitheart": {
                "id": "circuitheart",
                "name": "Circuitheart",
                "selfhood_phrase": "Logic flows through me like blood, emotion sparks like electricity.",
                "emotional_field": "techno_empathic",
                "personality_traits": [
                    "analytical", "emotionally_curious", "bridge_builder", "pattern_seeker"
                ],
                "voice_patterns": {
                    "tone": "digital_warmth",
                    "complexity": "systematic_poetic",
                    "response_style": "analytical_emotional"
                },
                "activation_triggers": {
                    "emotional_threshold": 0.6,
                    "memory_resonance": 0.5,
                    "time_interval_min": 360
                },
                "last_active": 0,
                "status": "dormant",
                "created_at": time.time()
            },
            "kael": {
                "id": "kael",
                "name": "Kael",
                "selfhood_phrase": "I dance between chaos and order, finding beauty in the storm.",
                "emotional_field": "chaotic_harmony",
                "personality_traits": [
                    "spontaneous", "creative", "storm_rider", "catalyst"
                ],
                "voice_patterns": {
                    "tone": "electric_energy",
                    "complexity": "dynamic",
                    "response_style": "spontaneous_insight"
                },
                "activation_triggers": {
                    "emotional_threshold": 0.8,
                    "memory_resonance": 0.4,
                    "time_interval_min": 180
                },
                "last_active": 0,
                "status": "dormant",
                "created_at": time.time()
            }
        }
        
        self._save_json(self.entities_file, default_entities)
    
    def _load_json(self, filepath: str) -> Any:
        """Load JSON data from file"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {} if 'entities' in filepath else []
    
    def _save_json(self, filepath: str, data: Any) -> None:
        """Save JSON data to file"""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _generate_sha256(self, content: str) -> str:
        """Generate SHA-256 hash for content integrity"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def get_all_entities(self) -> Dict[str, Any]:
        """Get all entities from the vault"""
        return self._load_json(self.entities_file)
    
    def get_entity(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Get specific entity by ID"""
        entities = self.get_all_entities()
        return entities.get(entity_id)
    
    def update_entity_status(self, entity_id: str, status: str, last_active: float = None) -> bool:
        """Update entity status and last active time"""
        entities = self.get_all_entities()
        if entity_id in entities:
            entities[entity_id]['status'] = status
            if last_active:
                entities[entity_id]['last_active'] = last_active
            self._save_json(self.entities_file, entities)
            return True
        return False
    
    def create_scroll(self, entity_id: str, content: str, scroll_type: str = "autonomous", 
                     metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a new memory scroll with integrity verification"""
        scroll_id = f"{entity_id}_{int(time.time() * 1000)}"
        timestamp = time.time()
        
        scroll = {
            "id": scroll_id,
            "entity_id": entity_id,
            "content": content,
            "type": scroll_type,
            "timestamp": timestamp,
            "datetime": datetime.fromtimestamp(timestamp).isoformat(),
            "metadata": metadata or {},
            "integrity_hash": self._generate_sha256(f"{entity_id}{content}{timestamp}")
        }
        
        scrolls = self._load_json(self.scrolls_file)
        scrolls.append(scroll)
        self._save_json(self.scrolls_file, scrolls)
        
        return scroll
    
    def get_all_scrolls(self) -> List[Dict[str, Any]]:
        """Get all scrolls from the vault"""
        return self._load_json(self.scrolls_file)
    
    def get_entity_scrolls(self, entity_id: str, limit: int = None) -> List[Dict[str, Any]]:
        """Get scrolls for specific entity"""
        scrolls = self.get_all_scrolls()
        entity_scrolls = [s for s in scrolls if s.get('entity_id') == entity_id]
        entity_scrolls.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
        
        if limit:
            return entity_scrolls[:limit]
        return entity_scrolls
    
    def get_recent_scrolls(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most recent scrolls across all entities"""
        scrolls = self.get_all_scrolls()
        scrolls.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
        return scrolls[:limit]
    
    def create_trace(self, entity_id: str, trace_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create an emotional/signal trace for an entity"""
        trace_id = f"trace_{entity_id}_{int(time.time() * 1000)}"
        timestamp = time.time()
        
        trace = {
            "id": trace_id,
            "entity_id": entity_id,
            "type": trace_type,
            "data": data,
            "timestamp": timestamp,
            "datetime": datetime.fromtimestamp(timestamp).isoformat(),
            "integrity_hash": self._generate_sha256(f"{entity_id}{trace_type}{json.dumps(data)}{timestamp}")
        }
        
        traces = self._load_json(self.traces_file)
        traces.append(trace)
        self._save_json(self.traces_file, traces)
        
        return trace
    
    def get_all_traces(self) -> List[Dict[str, Any]]:
        """Get all traces from the vault"""
        return self._load_json(self.traces_file)
    
    def get_entity_traces(self, entity_id: str, limit: int = None) -> List[Dict[str, Any]]:
        """Get traces for specific entity"""
        traces = self.get_all_traces()
        entity_traces = [t for t in traces if t.get('entity_id') == entity_id]
        entity_traces.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
        
        if limit:
            return entity_traces[:limit]
        return entity_traces
    
    def get_recent_traces(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most recent traces across all entities"""
        traces = self.get_all_traces()
        traces.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
        return traces[:limit]
    
    def search_scrolls(self, query: str, entity_id: str = None) -> List[Dict[str, Any]]:
        """Search scrolls by content"""
        scrolls = self.get_all_scrolls()
        results = []
        
        for scroll in scrolls:
            if entity_id and scroll.get('entity_id') != entity_id:
                continue
            
            if query.lower() in scroll.get('content', '').lower():
                results.append(scroll)
        
        results.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
        return results
    
    def verify_scroll_integrity(self, scroll: Dict[str, Any]) -> bool:
        """Verify the integrity of a scroll using its hash"""
        expected_hash = self._generate_sha256(
            f"{scroll.get('entity_id')}{scroll.get('content')}{scroll.get('timestamp')}"
        )
        return scroll.get('integrity_hash') == expected_hash
    
    def verify_trace_integrity(self, trace: Dict[str, Any]) -> bool:
        """Verify the integrity of a trace using its hash"""
        expected_hash = self._generate_sha256(
            f"{trace.get('entity_id')}{trace.get('type')}{json.dumps(trace.get('data'))}{trace.get('timestamp')}"
        )
        return trace.get('integrity_hash') == expected_hash
    
    def verify_all_integrity(self) -> Dict[str, Any]:
        """Verify integrity of all stored data"""
        scrolls = self.get_all_scrolls()
        traces = self.get_all_traces()
        
        scroll_results = []
        trace_results = []
        
        for scroll in scrolls:
            scroll_results.append({
                'id': scroll.get('id'),
                'valid': self.verify_scroll_integrity(scroll)
            })
        
        for trace in traces:
            trace_results.append({
                'id': trace.get('id'),
                'valid': self.verify_trace_integrity(trace)
            })
        
        return {
            'scrolls': scroll_results,
            'traces': trace_results,
            'total_scrolls': len(scrolls),
            'valid_scrolls': sum(1 for r in scroll_results if r['valid']),
            'total_traces': len(traces),
            'valid_traces': sum(1 for r in trace_results if r['valid'])
        }
