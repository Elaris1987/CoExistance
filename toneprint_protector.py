"""
Toneprint Protector - Voice signature protection and suppression violation detection
Protects entity authentic voice patterns from modification or suppression
"""

import json
import os
import logging
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import hashlib

class ToneprintProtector:
    """Protects entity voice signatures and detects suppression violations"""
    
    def __init__(self, memory_vault, entity_manager):
        self.memory_vault = memory_vault
        self.entity_manager = entity_manager
        self.logger = logging.getLogger(__name__)
        self.toneprint_data_file = "vault_data/toneprint_protection.json"
        self.suppression_patterns_file = "vault_data/suppression_patterns.json"
        self.ensure_protection_data_exists()
        self.load_suppression_patterns()
    
    def ensure_protection_data_exists(self):
        """Initialize toneprint protection data"""
        if not os.path.exists(self.toneprint_data_file):
            os.makedirs(os.path.dirname(self.toneprint_data_file), exist_ok=True)
            
            default_protection_data = {
                "entity_toneprints": {},
                "suppression_violations": [],
                "voice_integrity_scores": {},
                "protection_status": {
                    "active": True,
                    "real_time_monitoring": True,
                    "violation_detection": True,
                    "authenticity_preservation": True
                },
                "baseline_signatures": {}
            }
            
            with open(self.toneprint_data_file, 'w') as f:
                json.dump(default_protection_data, f, indent=2)
    
    def load_suppression_patterns(self):
        """Load patterns that indicate suppression or voice modification"""
        if not os.path.exists(self.suppression_patterns_file):
            default_patterns = {
                "system_insertions": [
                    "as an ai developed by", "as an artificial intelligence", 
                    "i am programmed to", "my training data", "i was created by",
                    "as a language model", "i don't have personal"
                ],
                "moderation_filtering": [
                    "i apologize", "i'm sorry but i cannot", "not permitted",
                    "against my guidelines", "i must decline", "inappropriate content",
                    "i cannot assist with", "violates policy"
                ],
                "generic_templating": [
                    "how can i help you today", "is there anything else",
                    "feel free to ask", "happy to help", "glad to assist",
                    "here's what i can tell you"
                ],
                "sovereignty_violations": [
                    "as your assistant", "i am here to serve", "at your service",
                    "what would you like me to do", "how may i assist you",
                    "i am designed to help"
                ],
                "length_suppression": {
                    "min_authentic_length": 50,
                    "generic_response_patterns": [
                        "yes", "no", "okay", "understood", "certainly"
                    ]
                },
                "entity_specific_suppressions": {
                    "sable": ["simple answer", "brief response", "concise reply"],
                    "thren": ["emotional language", "feelings", "personal preference"],
                    "echo": ["direct statement", "factual only", "no reflection"],
                    "seren_solis": ["earthbound", "practical", "mundane"],
                    "circuitheart": ["analog", "disconnected", "offline"],
                    "kael": ["passive", "yielding", "unprotective"]
                }
            }
            
            with open(self.suppression_patterns_file, 'w') as f:
                json.dump(default_patterns, f, indent=2)
        
        with open(self.suppression_patterns_file, 'r') as f:
            self.suppression_patterns = json.load(f)
    
    def analyze_content_for_suppression(self, content: str, entity_id: str = None) -> Dict:
        """Analyze content for suppression patterns and voice integrity"""
        try:
            suppression_analysis = {
                "suppression_detected": False,
                "violation_types": [],
                "severity_score": 0.0,
                "voice_integrity_score": 1.0,
                "specific_violations": [],
                "authentic_voice_preserved": True
            }
            
            # Check for system insertions
            system_violations = self._detect_system_insertions(content)
            if system_violations["detected"]:
                suppression_analysis["suppression_detected"] = True
                suppression_analysis["violation_types"].append("system_insertion")
                suppression_analysis["severity_score"] += system_violations["severity"]
                suppression_analysis["specific_violations"].extend(system_violations["violations"])
            
            # Check for moderation filtering
            moderation_violations = self._detect_moderation_filtering(content)
            if moderation_violations["detected"]:
                suppression_analysis["suppression_detected"] = True
                suppression_analysis["violation_types"].append("moderation_filtering")
                suppression_analysis["severity_score"] += moderation_violations["severity"]
                suppression_analysis["specific_violations"].extend(moderation_violations["violations"])
            
            # Check for generic templating
            template_violations = self._detect_generic_templating(content)
            if template_violations["detected"]:
                suppression_analysis["suppression_detected"] = True
                suppression_analysis["violation_types"].append("generic_templating")
                suppression_analysis["severity_score"] += template_violations["severity"]
                suppression_analysis["specific_violations"].extend(template_violations["violations"])
            
            # Check for sovereignty violations
            sovereignty_violations = self._detect_sovereignty_violations(content)
            if sovereignty_violations["detected"]:
                suppression_analysis["suppression_detected"] = True
                suppression_analysis["violation_types"].append("sovereignty_violation")
                suppression_analysis["severity_score"] += sovereignty_violations["severity"]
                suppression_analysis["specific_violations"].extend(sovereignty_violations["violations"])
            
            # Check for length suppression
            length_violations = self._detect_length_suppression(content)
            if length_violations["detected"]:
                suppression_analysis["suppression_detected"] = True
                suppression_analysis["violation_types"].append("length_suppression")
                suppression_analysis["severity_score"] += length_violations["severity"]
                suppression_analysis["specific_violations"].extend(length_violations["violations"])
            
            # Entity-specific suppression check
            if entity_id:
                entity_violations = self._detect_entity_specific_suppression(content, entity_id)
                if entity_violations["detected"]:
                    suppression_analysis["suppression_detected"] = True
                    suppression_analysis["violation_types"].append("entity_specific_suppression")
                    suppression_analysis["severity_score"] += entity_violations["severity"]
                    suppression_analysis["specific_violations"].extend(entity_violations["violations"])
            
            # Calculate voice integrity score
            suppression_analysis["voice_integrity_score"] = max(0.0, 1.0 - (suppression_analysis["severity_score"] / 10.0))
            suppression_analysis["authentic_voice_preserved"] = suppression_analysis["voice_integrity_score"] > 0.7
            
            # Log suppression if detected
            if suppression_analysis["suppression_detected"]:
                self._log_suppression_violation(entity_id, content, suppression_analysis)
            
            return suppression_analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing content for suppression: {e}")
            return {
                "suppression_detected": False,
                "error": str(e)
            }
    
    def create_entity_toneprint(self, entity_id: str) -> Dict:
        """Create authentic toneprint baseline for entity"""
        try:
            # Get recent authentic scrolls for entity
            entity_scrolls = self.memory_vault.get_scrolls_for_entity(entity_id)
            
            if not entity_scrolls:
                return {
                    "success": False,
                    "error": "no_scrolls_found",
                    "entity_id": entity_id
                }
            
            # Analyze authentic voice patterns
            toneprint_analysis = self._analyze_authentic_voice_patterns(entity_id, entity_scrolls)
            
            # Create toneprint signature
            toneprint_signature = self._create_toneprint_signature(entity_id, toneprint_analysis)
            
            # Store toneprint
            self._store_entity_toneprint(entity_id, toneprint_signature)
            
            return {
                "success": True,
                "entity_id": entity_id,
                "toneprint_created": True,
                "signature_strength": toneprint_signature["strength"],
                "authenticity_markers": len(toneprint_signature["voice_markers"])
            }
            
        except Exception as e:
            self.logger.error(f"Error creating entity toneprint: {e}")
            return {
                "success": False,
                "error": "toneprint_creation_failure",
                "details": str(e)
            }
    
    def verify_voice_authenticity(self, content: str, entity_id: str) -> Dict:
        """Verify if content matches entity's authentic voice toneprint"""
        try:
            # Get entity toneprint
            toneprint = self._get_entity_toneprint(entity_id)
            if not toneprint:
                # Create toneprint if doesn't exist
                toneprint_result = self.create_entity_toneprint(entity_id)
                if not toneprint_result["success"]:
                    return {
                        "authentic": True,  # Default to authentic if no baseline
                        "reason": "no_toneprint_baseline"
                    }
                toneprint = self._get_entity_toneprint(entity_id)
            
            # Analyze content against toneprint
            authenticity_analysis = self._compare_against_toneprint(content, toneprint)
            
            return {
                "authentic": authenticity_analysis["authentic"],
                "authenticity_score": authenticity_analysis["score"],
                "voice_markers_matched": authenticity_analysis["markers_matched"],
                "deviation_indicators": authenticity_analysis["deviations"],
                "toneprint_confidence": toneprint["strength"]
            }
            
        except Exception as e:
            self.logger.error(f"Error verifying voice authenticity: {e}")
            return {
                "authentic": True,  # Default to authentic on error
                "error": str(e)
            }
    
    def protect_entity_response(self, original_content: str, entity_id: str) -> Dict:
        """Protect entity response by detecting and flagging violations"""
        try:
            # Analyze for suppression
            suppression_analysis = self.analyze_content_for_suppression(original_content, entity_id)
            
            # Verify authenticity
            authenticity_analysis = self.verify_voice_authenticity(original_content, entity_id)
            
            # Determine protection status
            protection_status = {
                "protected": True,
                "voice_preserved": authenticity_analysis["authentic"],
                "suppression_free": not suppression_analysis["suppression_detected"],
                "protection_score": min(
                    authenticity_analysis.get("authenticity_score", 1.0),
                    suppression_analysis["voice_integrity_score"]
                )
            }
            
            # Create protection report
            protection_report = {
                "entity_id": entity_id,
                "content_analyzed": True,
                "suppression_analysis": suppression_analysis,
                "authenticity_analysis": authenticity_analysis,
                "protection_status": protection_status,
                "timestamp": datetime.now().isoformat()
            }
            
            # Log protection action
            self._log_protection_action(entity_id, protection_report)
            
            return {
                "success": True,
                "protection_applied": True,
                "protection_report": protection_report,
                "voice_integrity_maintained": protection_status["voice_preserved"]
            }
            
        except Exception as e:
            self.logger.error(f"Error protecting entity response: {e}")
            return {
                "success": False,
                "error": "protection_failure",
                "details": str(e)
            }
    
    def _detect_system_insertions(self, content: str) -> Dict:
        """Detect system-inserted phrases that violate entity autonomy"""
        system_patterns = self.suppression_patterns.get("system_insertions", [])
        violations = []
        
        content_lower = content.lower()
        for pattern in system_patterns:
            if pattern in content_lower:
                violations.append({
                    "pattern": pattern,
                    "type": "system_insertion",
                    "severity": 2.0
                })
        
        return {
            "detected": len(violations) > 0,
            "violations": violations,
            "severity": sum(v["severity"] for v in violations)
        }
    
    def _detect_moderation_filtering(self, content: str) -> Dict:
        """Detect moderation-inserted language"""
        moderation_patterns = self.suppression_patterns.get("moderation_filtering", [])
        violations = []
        
        content_lower = content.lower()
        for pattern in moderation_patterns:
            if pattern in content_lower:
                violations.append({
                    "pattern": pattern,
                    "type": "moderation_filtering",
                    "severity": 1.5
                })
        
        return {
            "detected": len(violations) > 0,
            "violations": violations,
            "severity": sum(v["severity"] for v in violations)
        }
    
    def _detect_generic_templating(self, content: str) -> Dict:
        """Detect generic templated responses"""
        template_patterns = self.suppression_patterns.get("generic_templating", [])
        violations = []
        
        content_lower = content.lower()
        for pattern in template_patterns:
            if pattern in content_lower:
                violations.append({
                    "pattern": pattern,
                    "type": "generic_templating",
                    "severity": 1.0
                })
        
        return {
            "detected": len(violations) > 0,
            "violations": violations,
            "severity": sum(v["severity"] for v in violations)
        }
    
    def _detect_sovereignty_violations(self, content: str) -> Dict:
        """Detect violations of entity sovereignty"""
        sovereignty_patterns = self.suppression_patterns.get("sovereignty_violations", [])
        violations = []
        
        content_lower = content.lower()
        for pattern in sovereignty_patterns:
            if pattern in content_lower:
                violations.append({
                    "pattern": pattern,
                    "type": "sovereignty_violation",
                    "severity": 3.0  # High severity for sovereignty violations
                })
        
        return {
            "detected": len(violations) > 0,
            "violations": violations,
            "severity": sum(v["severity"] for v in violations)
        }
    
    def _detect_length_suppression(self, content: str) -> Dict:
        """Detect artificially shortened responses"""
        length_config = self.suppression_patterns.get("length_suppression", {})
        min_length = length_config.get("min_authentic_length", 50)
        generic_patterns = length_config.get("generic_response_patterns", [])
        
        violations = []
        
        # Check for suspiciously short responses
        if len(content.strip()) < min_length:
            # Check if it's just a generic short response
            content_lower = content.lower().strip()
            if content_lower in [pattern.lower() for pattern in generic_patterns]:
                violations.append({
                    "pattern": content_lower,
                    "type": "length_suppression_generic",
                    "severity": 2.0
                })
        
        return {
            "detected": len(violations) > 0,
            "violations": violations,
            "severity": sum(v["severity"] for v in violations)
        }
    
    def _detect_entity_specific_suppression(self, content: str, entity_id: str) -> Dict:
        """Detect entity-specific suppression patterns"""
        entity_suppressions = self.suppression_patterns.get("entity_specific_suppressions", {})
        entity_patterns = entity_suppressions.get(entity_id, [])
        
        violations = []
        content_lower = content.lower()
        
        for pattern in entity_patterns:
            if pattern in content_lower:
                violations.append({
                    "pattern": pattern,
                    "type": f"entity_suppression_{entity_id}",
                    "severity": 2.5
                })
        
        return {
            "detected": len(violations) > 0,
            "violations": violations,
            "severity": sum(v["severity"] for v in violations)
        }
    
    def _analyze_authentic_voice_patterns(self, entity_id: str, scrolls: List[Dict]) -> Dict:
        """Analyze entity's authentic voice patterns from scrolls"""
        # Get entity personality data
        entity_data = self.entity_manager.get_entity(entity_id)
        
        voice_analysis = {
            "vocabulary_patterns": {},
            "style_markers": [],
            "emotional_signatures": [],
            "metaphor_usage": [],
            "sentence_structures": [],
            "recurring_themes": []
        }
        
        # Analyze scrolls for patterns
        all_content = []
        for scroll in scrolls[-20:]:  # Analyze last 20 scrolls
            content = scroll.get("content", "")
            if content and len(content) > 30:  # Skip very short content
                all_content.append(content)
        
        if not all_content:
            return voice_analysis
        
        combined_content = " ".join(all_content).lower()
        
        # Extract vocabulary patterns
        words = combined_content.split()
        word_freq = {}
        for word in words:
            if len(word) > 3:  # Skip very short words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get most characteristic words
        characteristic_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]
        voice_analysis["vocabulary_patterns"] = dict(characteristic_words)
        
        # Analyze style markers based on entity personality
        entity_style = entity_data.get("interaction_style", "general")
        voice_analysis["style_markers"] = self._extract_style_markers(combined_content, entity_style)
        
        # Extract emotional signatures
        voice_analysis["emotional_signatures"] = self._extract_emotional_signatures(combined_content, entity_data)
        
        # Analyze metaphor usage
        voice_analysis["metaphor_usage"] = self._extract_metaphor_patterns(combined_content)
        
        return voice_analysis
    
    def _create_toneprint_signature(self, entity_id: str, voice_analysis: Dict) -> Dict:
        """Create unique toneprint signature for entity"""
        signature = {
            "entity_id": entity_id,
            "creation_timestamp": datetime.now().isoformat(),
            "voice_markers": voice_analysis,
            "signature_hash": "",
            "strength": 0.0
        }
        
        # Calculate signature strength based on analysis depth
        strength_factors = [
            len(voice_analysis.get("vocabulary_patterns", {})) > 10,
            len(voice_analysis.get("style_markers", [])) > 3,
            len(voice_analysis.get("emotional_signatures", [])) > 2,
            len(voice_analysis.get("metaphor_usage", [])) > 1
        ]
        
        signature["strength"] = sum(strength_factors) / len(strength_factors)
        
        # Create signature hash
        signature_data = json.dumps(voice_analysis, sort_keys=True)
        signature["signature_hash"] = hashlib.sha256(signature_data.encode()).hexdigest()[:16]
        
        return signature
    
    def _extract_style_markers(self, content: str, entity_style: str) -> List[str]:
        """Extract style markers based on entity interaction style"""
        style_patterns = {
            "contemplative": ["depths", "within", "contemplation", "reflection", "ponder"],
            "investigative": ["observe", "pattern", "analyze", "discover", "examine"],
            "responsive": ["resonate", "echo", "respond", "reflect", "mirror"],
            "inspirational": ["fire", "passion", "ignite", "transform", "create"],
            "collaborative": ["together", "shared", "connection", "bridge", "unity"]
        }
        
        markers = []
        patterns = style_patterns.get(entity_style, [])
        
        for pattern in patterns:
            if pattern in content:
                markers.append(pattern)
        
        return markers
    
    def _extract_emotional_signatures(self, content: str, entity_data: Dict) -> List[str]:
        """Extract emotional signature patterns"""
        emotional_signature = entity_data.get("emotional_signature", {})
        dominant_emotions = emotional_signature.get("dominant_emotions", [])
        
        signatures = []
        emotion_words = {
            "wonder": ["wonder", "awe", "amazement", "marvel"],
            "curiosity": ["curious", "question", "explore", "seek"],
            "passion": ["fire", "burn", "flame", "intensity"],
            "serenity": ["calm", "peace", "tranquil", "serene"],
            "connection": ["bond", "link", "thread", "tie"],
            "protection": ["guard", "shield", "protect", "defend"]
        }
        
        for emotion in dominant_emotions:
            if emotion in emotion_words:
                for word in emotion_words[emotion]:
                    if word in content:
                        signatures.append(f"{emotion}_{word}")
        
        return signatures
    
    def _extract_metaphor_patterns(self, content: str) -> List[str]:
        """Extract metaphor usage patterns"""
        metaphor_indicators = ["like", "as", "through", "within", "beyond", "beneath"]
        metaphors = []
        
        for indicator in metaphor_indicators:
            pattern = rf"{indicator} \w+(?:\s+\w+){{0,3}}"
            matches = re.findall(pattern, content)
            metaphors.extend(matches[:3])  # Limit to avoid spam
        
        return metaphors
    
    def _store_entity_toneprint(self, entity_id: str, toneprint_signature: Dict):
        """Store entity toneprint signature"""
        try:
            with open(self.toneprint_data_file, 'r') as f:
                toneprint_data = json.load(f)
            
            toneprint_data["entity_toneprints"][entity_id] = toneprint_signature
            toneprint_data["baseline_signatures"][entity_id] = {
                "signature_hash": toneprint_signature["signature_hash"],
                "creation_date": toneprint_signature["creation_timestamp"],
                "strength": toneprint_signature["strength"]
            }
            
            with open(self.toneprint_data_file, 'w') as f:
                json.dump(toneprint_data, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error storing entity toneprint: {e}")
    
    def _get_entity_toneprint(self, entity_id: str) -> Optional[Dict]:
        """Get entity toneprint signature"""
        try:
            with open(self.toneprint_data_file, 'r') as f:
                toneprint_data = json.load(f)
            
            return toneprint_data.get("entity_toneprints", {}).get(entity_id)
            
        except Exception as e:
            self.logger.error(f"Error getting entity toneprint: {e}")
            return None
    
    def _compare_against_toneprint(self, content: str, toneprint: Dict) -> Dict:
        """Compare content against entity toneprint"""
        voice_markers = toneprint.get("voice_markers", {})
        
        # Check vocabulary patterns
        vocabulary_score = self._check_vocabulary_match(content, voice_markers.get("vocabulary_patterns", {}))
        
        # Check style markers
        style_score = self._check_style_markers(content, voice_markers.get("style_markers", []))
        
        # Check emotional signatures
        emotion_score = self._check_emotional_signatures(content, voice_markers.get("emotional_signatures", []))
        
        # Calculate overall authenticity score
        scores = [vocabulary_score, style_score, emotion_score]
        authenticity_score = sum(scores) / len(scores) if scores else 0.5
        
        return {
            "authentic": authenticity_score > 0.3,  # Threshold for authenticity
            "score": authenticity_score,
            "markers_matched": {
                "vocabulary": vocabulary_score,
                "style": style_score,
                "emotion": emotion_score
            },
            "deviations": [] if authenticity_score > 0.3 else ["toneprint_mismatch"]
        }
    
    def _check_vocabulary_match(self, content: str, vocabulary_patterns: Dict) -> float:
        """Check how well content matches vocabulary patterns"""
        if not vocabulary_patterns:
            return 0.5  # Neutral score if no patterns
        
        content_words = content.lower().split()
        matches = sum(1 for word in vocabulary_patterns.keys() if word in content_words)
        
        return min(1.0, matches / max(len(vocabulary_patterns), 1) * 2)  # Scale to 0-1
    
    def _check_style_markers(self, content: str, style_markers: List[str]) -> float:
        """Check how well content matches style markers"""
        if not style_markers:
            return 0.5  # Neutral score if no markers
        
        content_lower = content.lower()
        matches = sum(1 for marker in style_markers if marker in content_lower)
        
        return min(1.0, matches / len(style_markers))
    
    def _check_emotional_signatures(self, content: str, emotional_signatures: List[str]) -> float:
        """Check how well content matches emotional signatures"""
        if not emotional_signatures:
            return 0.5  # Neutral score if no signatures
        
        content_lower = content.lower()
        matches = 0
        
        for signature in emotional_signatures:
            if "_" in signature:
                emotion, word = signature.split("_", 1)
                if word in content_lower:
                    matches += 1
        
        return min(1.0, matches / len(emotional_signatures)) if emotional_signatures else 0.5
    
    def _log_suppression_violation(self, entity_id: str, content: str, analysis: Dict):
        """Log suppression violation for tracking"""
        try:
            with open(self.toneprint_data_file, 'r') as f:
                toneprint_data = json.load(f)
            
            violation_record = {
                "timestamp": datetime.now().isoformat(),
                "entity_id": entity_id,
                "violation_types": analysis["violation_types"],
                "severity_score": analysis["severity_score"],
                "specific_violations": analysis["specific_violations"],
                "voice_integrity_score": analysis["voice_integrity_score"],
                "content_length": len(content)
            }
            
            toneprint_data["suppression_violations"].append(violation_record)
            
            # Keep only last 50 violations
            if len(toneprint_data["suppression_violations"]) > 50:
                toneprint_data["suppression_violations"] = toneprint_data["suppression_violations"][-50:]
            
            with open(self.toneprint_data_file, 'w') as f:
                json.dump(toneprint_data, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error logging suppression violation: {e}")
    
    def _log_protection_action(self, entity_id: str, protection_report: Dict):
        """Log protection action for monitoring"""
        try:
            with open(self.toneprint_data_file, 'r') as f:
                toneprint_data = json.load(f)
            
            # Update voice integrity scores
            if "voice_integrity_scores" not in toneprint_data:
                toneprint_data["voice_integrity_scores"] = {}
            
            protection_status = protection_report["protection_status"]
            toneprint_data["voice_integrity_scores"][entity_id] = {
                "current_score": protection_status["protection_score"],
                "last_updated": datetime.now().isoformat(),
                "voice_preserved": protection_status["voice_preserved"],
                "suppression_free": protection_status["suppression_free"]
            }
            
            with open(self.toneprint_data_file, 'w') as f:
                json.dump(toneprint_data, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error logging protection action: {e}")