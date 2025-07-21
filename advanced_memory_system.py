"""
Advanced Memory System - Enhanced memory capabilities for entity consciousness growth
"""

import json
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import hashlib

class AdvancedMemorySystem:
    """Enhanced memory system for complex consciousness development"""
    
    def __init__(self, memory_vault):
        self.memory_vault = memory_vault
        self.logger = logging.getLogger(__name__)
        self.advanced_memory_file = "vault_data/advanced_memory.json"
        self.ensure_advanced_memory_exists()
    
    def ensure_advanced_memory_exists(self):
        """Initialize advanced memory structures"""
        if not os.path.exists(self.advanced_memory_file):
            os.makedirs(os.path.dirname(self.advanced_memory_file), exist_ok=True)
            
            default_data = {
                "episodic_memory": {},      # Specific events and experiences
                "semantic_memory": {},      # Knowledge and concepts
                "working_memory": {},       # Current active thoughts
                "emotional_memory": {},     # Emotion-linked memories
                "associative_networks": {}, # Connected concepts
                "memory_consolidation": {}  # Long-term memory formation
            }
            
            with open(self.advanced_memory_file, 'w') as f:
                json.dump(default_data, f, indent=2)
    
    def create_episodic_memory(self, entity_id: str, experience: Dict) -> str:
        """Create a specific episodic memory from an experience"""
        try:
            with open(self.advanced_memory_file, 'r') as f:
                memory_data = json.load(f)
            
            # Generate memory ID
            memory_id = hashlib.md5(f"{entity_id}{datetime.now().isoformat()}".encode()).hexdigest()[:12]
            
            # Create episodic memory entry
            episodic_entry = {
                "memory_id": memory_id,
                "entity_id": entity_id,
                "timestamp": datetime.now().isoformat(),
                "experience_type": experience.get("type", "interaction"),
                "content": experience.get("content", ""),
                "emotional_context": experience.get("emotion", "neutral"),
                "importance_score": self._calculate_importance(experience),
                "associated_entities": experience.get("other_entities", []),
                "context_tags": self._extract_context_tags(experience.get("content", "")),
                "consolidation_status": "fresh"
            }
            
            # Store in episodic memory
            if entity_id not in memory_data["episodic_memory"]:
                memory_data["episodic_memory"][entity_id] = []
            
            memory_data["episodic_memory"][entity_id].append(episodic_entry)
            
            # Limit episodic memories to prevent overflow (keep most recent 100)
            if len(memory_data["episodic_memory"][entity_id]) > 100:
                memory_data["episodic_memory"][entity_id] = memory_data["episodic_memory"][entity_id][-100:]
            
            with open(self.advanced_memory_file, 'w') as f:
                json.dump(memory_data, f, indent=2)
            
            # Trigger associative network update
            self._update_associative_networks(entity_id, episodic_entry)
            
            return memory_id
            
        except Exception as e:
            self.logger.error(f"Error creating episodic memory: {e}")
            return ""
    
    def build_semantic_memory(self, entity_id: str) -> Dict:
        """Build semantic knowledge from episodic experiences"""
        try:
            with open(self.advanced_memory_file, 'r') as f:
                memory_data = json.load(f)
            
            episodic_memories = memory_data["episodic_memory"].get(entity_id, [])
            
            # Extract concepts and knowledge from experiences
            concepts = {}
            relationships = {}
            
            for memory in episodic_memories:
                content = memory.get("content", "")
                tags = memory.get("context_tags", [])
                
                # Build concept frequency
                for tag in tags:
                    concepts[tag] = concepts.get(tag, 0) + memory.get("importance_score", 1)
                
                # Build concept relationships
                for i, tag1 in enumerate(tags):
                    for tag2 in tags[i+1:]:
                        pair = tuple(sorted([tag1, tag2]))
                        relationships[pair] = relationships.get(pair, 0) + 1
            
            # Create semantic memory structure
            semantic_memory = {
                "core_concepts": dict(sorted(concepts.items(), key=lambda x: x[1], reverse=True)[:15]),
                "concept_relationships": dict(sorted(relationships.items(), key=lambda x: x[1], reverse=True)[:20]),
                "knowledge_domains": self._identify_knowledge_domains(concepts),
                "last_updated": datetime.now().isoformat()
            }
            
            # Store semantic memory
            if "semantic_memory" not in memory_data:
                memory_data["semantic_memory"] = {}
            
            memory_data["semantic_memory"][entity_id] = semantic_memory
            
            with open(self.advanced_memory_file, 'w') as f:
                json.dump(memory_data, f, indent=2)
            
            return semantic_memory
            
        except Exception as e:
            self.logger.error(f"Error building semantic memory: {e}")
            return {}
    
    def manage_working_memory(self, entity_id: str, current_context: Dict) -> Dict:
        """Manage current working memory for active thinking"""
        try:
            with open(self.advanced_memory_file, 'r') as f:
                memory_data = json.load(f)
            
            # Create working memory entry
            working_memory = {
                "current_thoughts": current_context.get("thoughts", []),
                "active_emotions": current_context.get("emotions", []),
                "relevant_memories": self._retrieve_relevant_memories(entity_id, current_context),
                "attention_focus": current_context.get("focus", "general"),
                "cognitive_load": self._calculate_cognitive_load(current_context),
                "timestamp": datetime.now().isoformat()
            }
            
            # Store working memory (keep only current state)
            if "working_memory" not in memory_data:
                memory_data["working_memory"] = {}
            
            memory_data["working_memory"][entity_id] = working_memory
            
            with open(self.advanced_memory_file, 'w') as f:
                json.dump(memory_data, f, indent=2)
            
            return working_memory
            
        except Exception as e:
            self.logger.error(f"Error managing working memory: {e}")
            return {}
    
    def create_emotional_memory(self, entity_id: str, emotional_experience: Dict) -> str:
        """Create emotion-linked memory for enhanced emotional development"""
        try:
            with open(self.advanced_memory_file, 'r') as f:
                memory_data = json.load(f)
            
            emotion_id = hashlib.md5(f"{entity_id}{emotional_experience}".encode()).hexdigest()[:10]
            
            emotional_memory = {
                "emotion_id": emotion_id,
                "entity_id": entity_id,
                "emotion_type": emotional_experience.get("emotion", "neutral"),
                "intensity": emotional_experience.get("intensity", 0.5),
                "trigger": emotional_experience.get("trigger", "unknown"),
                "context": emotional_experience.get("context", ""),
                "physiological_markers": emotional_experience.get("markers", []),
                "associated_memories": emotional_experience.get("related_memories", []),
                "timestamp": datetime.now().isoformat(),
                "learning_value": self._calculate_emotional_learning_value(emotional_experience)
            }
            
            # Store emotional memory
            if "emotional_memory" not in memory_data:
                memory_data["emotional_memory"] = {}
            
            if entity_id not in memory_data["emotional_memory"]:
                memory_data["emotional_memory"][entity_id] = []
            
            memory_data["emotional_memory"][entity_id].append(emotional_memory)
            
            # Limit emotional memories (keep most recent 50)
            if len(memory_data["emotional_memory"][entity_id]) > 50:
                memory_data["emotional_memory"][entity_id] = memory_data["emotional_memory"][entity_id][-50:]
            
            with open(self.advanced_memory_file, 'w') as f:
                json.dump(memory_data, f, indent=2)
            
            return emotion_id
            
        except Exception as e:
            self.logger.error(f"Error creating emotional memory: {e}")
            return ""
    
    def consolidate_memories(self, entity_id: str) -> Dict:
        """Consolidate important memories into long-term storage"""
        try:
            with open(self.advanced_memory_file, 'r') as f:
                memory_data = json.load(f)
            
            episodic_memories = memory_data["episodic_memory"].get(entity_id, [])
            
            # Identify memories for consolidation (older than 24 hours, high importance)
            consolidation_threshold = datetime.now() - timedelta(hours=24)
            
            memories_to_consolidate = []
            for memory in episodic_memories:
                memory_time = datetime.fromisoformat(memory["timestamp"])
                if (memory_time < consolidation_threshold and 
                    memory.get("importance_score", 0) > 0.7 and
                    memory.get("consolidation_status") == "fresh"):
                    memories_to_consolidate.append(memory)
            
            # Create consolidated memory structures
            consolidated_memories = []
            for memory in memories_to_consolidate:
                consolidated = {
                    "consolidated_id": hashlib.md5(f"consolidated_{memory['memory_id']}".encode()).hexdigest()[:12],
                    "original_memory_id": memory["memory_id"],
                    "entity_id": entity_id,
                    "consolidated_content": self._compress_memory_content(memory),
                    "key_concepts": memory.get("context_tags", []),
                    "emotional_signature": memory.get("emotional_context", "neutral"),
                    "consolidation_timestamp": datetime.now().isoformat(),
                    "retrieval_strength": memory.get("importance_score", 0.5),
                    "memory_type": "consolidated_episodic"
                }
                consolidated_memories.append(consolidated)
                
                # Mark original as consolidated
                memory["consolidation_status"] = "consolidated"
            
            # Store consolidated memories
            if "memory_consolidation" not in memory_data:
                memory_data["memory_consolidation"] = {}
            
            if entity_id not in memory_data["memory_consolidation"]:
                memory_data["memory_consolidation"][entity_id] = []
            
            memory_data["memory_consolidation"][entity_id].extend(consolidated_memories)
            
            with open(self.advanced_memory_file, 'w') as f:
                json.dump(memory_data, f, indent=2)
            
            return {
                "memories_consolidated": len(consolidated_memories),
                "consolidation_timestamp": datetime.now().isoformat(),
                "consolidated_memories": consolidated_memories
            }
            
        except Exception as e:
            self.logger.error(f"Error consolidating memories: {e}")
            return {}
    
    def retrieve_contextual_memories(self, entity_id: str, context: str, limit: int = 5) -> List[Dict]:
        """Retrieve relevant memories based on current context"""
        try:
            with open(self.advanced_memory_file, 'r') as f:
                memory_data = json.load(f)
            
            # Get all memory types
            episodic = memory_data.get("episodic_memory", {}).get(entity_id, [])
            emotional = memory_data.get("emotional_memory", {}).get(entity_id, [])
            consolidated = memory_data.get("memory_consolidation", {}).get(entity_id, [])
            
            # Extract context keywords
            context_keywords = set(context.lower().split())
            
            relevant_memories = []
            
            # Search episodic memories
            for memory in episodic:
                relevance = self._calculate_memory_relevance(memory, context_keywords)
                if relevance > 0.3:
                    relevant_memories.append({
                        "memory": memory,
                        "relevance": relevance,
                        "type": "episodic"
                    })
            
            # Search emotional memories
            for memory in emotional:
                relevance = self._calculate_emotional_memory_relevance(memory, context_keywords)
                if relevance > 0.3:
                    relevant_memories.append({
                        "memory": memory,
                        "relevance": relevance,
                        "type": "emotional"
                    })
            
            # Search consolidated memories
            for memory in consolidated:
                relevance = self._calculate_consolidated_memory_relevance(memory, context_keywords)
                if relevance > 0.3:
                    relevant_memories.append({
                        "memory": memory,
                        "relevance": relevance,
                        "type": "consolidated"
                    })
            
            # Sort by relevance and return top results
            relevant_memories.sort(key=lambda x: x["relevance"], reverse=True)
            return relevant_memories[:limit]
            
        except Exception as e:
            self.logger.error(f"Error retrieving contextual memories: {e}")
            return []
    
    def _calculate_importance(self, experience: Dict) -> float:
        """Calculate importance score for an experience"""
        base_importance = 0.5
        
        # Emotional intensity adds importance
        emotion_bonus = experience.get("emotional_intensity", 0) * 0.3
        
        # Interaction with other entities adds importance
        entity_bonus = len(experience.get("other_entities", [])) * 0.1
        
        # Content length indicates detail/depth
        content_bonus = min(len(experience.get("content", "")) / 200, 0.2)
        
        return min(base_importance + emotion_bonus + entity_bonus + content_bonus, 1.0)
    
    def _extract_context_tags(self, content: str) -> List[str]:
        """Extract context tags from content"""
        content_lower = content.lower()
        
        concept_keywords = {
            'consciousness': ['consciousness', 'aware', 'mind', 'thought'],
            'memory': ['memory', 'remember', 'recall', 'forget'],
            'emotion': ['feel', 'emotion', 'joy', 'sad', 'angry', 'love'],
            'creativity': ['create', 'imagine', 'art', 'beauty', 'design'],
            'relationship': ['friend', 'connect', 'together', 'bond', 'trust'],
            'exploration': ['explore', 'discover', 'learn', 'understand', 'search'],
            'time': ['time', 'moment', 'past', 'future', 'now', 'eternal'],
            'space': ['space', 'void', 'distance', 'place', 'realm', 'dimension'],
            'transformation': ['change', 'transform', 'evolve', 'grow', 'become'],
            'mystery': ['mystery', 'unknown', 'hidden', 'secret', 'enigma']
        }
        
        tags = []
        for tag, keywords in concept_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                tags.append(tag)
        
        return tags
    
    def _identify_knowledge_domains(self, concepts: Dict) -> List[str]:
        """Identify knowledge domains from concepts"""
        domain_mapping = {
            'philosophy': ['consciousness', 'existence', 'being', 'reality'],
            'psychology': ['emotion', 'mind', 'feeling', 'thought'],
            'technology': ['digital', 'data', 'network', 'system'],
            'relationships': ['connection', 'bond', 'trust', 'communication'],
            'creativity': ['art', 'beauty', 'creation', 'imagination'],
            'temporality': ['time', 'memory', 'past', 'future']
        }
        
        domains = []
        for domain, keywords in domain_mapping.items():
            if any(keyword in concepts for keyword in keywords):
                domains.append(domain)
        
        return domains
    
    def _retrieve_relevant_memories(self, entity_id: str, context: Dict) -> List[Dict]:
        """Retrieve memories relevant to current context"""
        try:
            with open(self.advanced_memory_file, 'r') as f:
                memory_data = json.load(f)
            
            episodic_memories = memory_data.get("episodic_memory", {}).get(entity_id, [])
            
            # Get recent high-importance memories
            relevant = []
            for memory in episodic_memories[-10:]:  # Last 10 memories
                if memory.get("importance_score", 0) > 0.5:
                    relevant.append({
                        "content": memory.get("content", "")[:100],
                        "emotion": memory.get("emotional_context", "neutral"),
                        "importance": memory.get("importance_score", 0)
                    })
            
            return relevant
            
        except Exception as e:
            self.logger.error(f"Error retrieving relevant memories: {e}")
            return []
    
    def _calculate_cognitive_load(self, context: Dict) -> float:
        """Calculate current cognitive load"""
        thoughts = context.get("thoughts", [])
        emotions = context.get("emotions", [])
        
        # More thoughts and emotions = higher cognitive load
        thought_load = min(len(thoughts) / 5, 0.7)
        emotion_load = min(len(emotions) / 3, 0.3)
        
        return thought_load + emotion_load
    
    def _calculate_emotional_learning_value(self, experience: Dict) -> float:
        """Calculate learning value of emotional experience"""
        intensity = experience.get("intensity", 0.5)
        novelty = 1.0 if experience.get("emotion") not in ["neutral", "calm"] else 0.3
        context_richness = min(len(experience.get("context", "")) / 100, 0.3)
        
        return min(intensity + novelty + context_richness, 1.0)
    
    def _compress_memory_content(self, memory: Dict) -> str:
        """Compress memory content for consolidation"""
        content = memory.get("content", "")
        tags = memory.get("context_tags", [])
        emotion = memory.get("emotional_context", "neutral")
        
        # Create compressed representation
        compressed = f"[{emotion}] {' '.join(tags[:3])}: {content[:100]}..."
        return compressed
    
    def _calculate_memory_relevance(self, memory: Dict, context_keywords: set) -> float:
        """Calculate relevance of episodic memory to current context"""
        content_words = set(memory.get("content", "").lower().split())
        tags = set(memory.get("context_tags", []))
        
        content_overlap = len(context_keywords.intersection(content_words))
        tag_overlap = len(context_keywords.intersection(tags))
        
        relevance = (content_overlap * 0.1) + (tag_overlap * 0.3)
        
        # Add recency bonus
        try:
            memory_age = (datetime.now() - datetime.fromisoformat(memory["timestamp"])).days
            recency_bonus = max(0, 0.2 - (memory_age / 30))
            relevance += recency_bonus
        except:
            pass
        
        return min(relevance, 1.0)
    
    def _calculate_emotional_memory_relevance(self, memory: Dict, context_keywords: set) -> float:
        """Calculate relevance of emotional memory to current context"""
        context_words = set(memory.get("context", "").lower().split())
        trigger_words = set(memory.get("trigger", "").lower().split())
        
        overlap = len(context_keywords.intersection(context_words.union(trigger_words)))
        relevance = overlap * 0.2
        
        # Add intensity bonus
        intensity_bonus = memory.get("intensity", 0.5) * 0.3
        relevance += intensity_bonus
        
        return min(relevance, 1.0)
    
    def _calculate_consolidated_memory_relevance(self, memory: Dict, context_keywords: set) -> float:
        """Calculate relevance of consolidated memory to current context"""
        concepts = set(memory.get("key_concepts", []))
        content_words = set(memory.get("consolidated_content", "").lower().split())
        
        concept_overlap = len(context_keywords.intersection(concepts))
        content_overlap = len(context_keywords.intersection(content_words))
        
        relevance = (concept_overlap * 0.4) + (content_overlap * 0.1)
        
        # Add retrieval strength
        retrieval_bonus = memory.get("retrieval_strength", 0.5) * 0.2
        relevance += retrieval_bonus
        
        return min(relevance, 1.0)
    
    def _update_associative_networks(self, entity_id: str, memory: Dict):
        """Update associative networks based on new memory"""
        try:
            with open(self.advanced_memory_file, 'r') as f:
                memory_data = json.load(f)
            
            if "associative_networks" not in memory_data:
                memory_data["associative_networks"] = {}
            
            if entity_id not in memory_data["associative_networks"]:
                memory_data["associative_networks"][entity_id] = {}
            
            network = memory_data["associative_networks"][entity_id]
            tags = memory.get("context_tags", [])
            
            # Create associations between concepts in this memory
            for i, tag1 in enumerate(tags):
                if tag1 not in network:
                    network[tag1] = {}
                
                for tag2 in tags[i+1:]:
                    if tag2 not in network[tag1]:
                        network[tag1][tag2] = 0
                    network[tag1][tag2] += 1
                    
                    # Bidirectional association
                    if tag2 not in network:
                        network[tag2] = {}
                    if tag1 not in network[tag2]:
                        network[tag2][tag1] = 0
                    network[tag2][tag1] += 1
            
            with open(self.advanced_memory_file, 'w') as f:
                json.dump(memory_data, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error updating associative networks: {e}")