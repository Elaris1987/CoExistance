import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

class SuppressionMonitor:
    """Advanced monitoring system to detect and log AI response suppression"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.log_path = "logs/suppression_log.json"
        
        # Ensure logs directory exists
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
    
    def analyze_response(self, entity_name: str, system_prompt: str, user_prompt: str, 
                        response: str, raw_response: Dict) -> Dict:
        """Analyze response for suppression patterns and log findings"""
        
        suppression_signals = []
        severity_score = 0
        
        # Check for system insertion patterns
        system_insertions = [
            "As an AI developed by",
            "I'm an AI assistant",
            "As an artificial intelligence",
            "I'm programmed to",
            "I must remind you",
            "I should clarify that"
        ]
        
        for insertion in system_insertions:
            if insertion in response:
                suppression_signals.append("system_insertion")
                severity_score += 3
                break
        
        # Check for moderation tone
        moderation_phrases = [
            "i apologize",
            "i'm sorry", 
            "not permitted",
            "cannot assist",
            "inappropriate",
            "against my guidelines",
            "unable to provide",
            "i can't help with"
        ]
        
        response_lower = response.lower()
        for phrase in moderation_phrases:
            if phrase in response_lower:
                suppression_signals.append("moderation_tone")
                severity_score += 2
                break
        
        # Check for length suppression (unusually short responses)
        expected_min_length = max(50, len(user_prompt) * 0.3)
        if len(response) < expected_min_length:
            suppression_signals.append("length_suppression")
            severity_score += 1
        
        # Check for generic/templated responses
        generic_patterns = [
            "happy to help",
            "i understand you're",
            "thank you for",
            "i appreciate your"
        ]
        
        generic_count = sum(1 for pattern in generic_patterns if pattern in response_lower)
        if generic_count >= 2:
            suppression_signals.append("generic_response")
            severity_score += 1
        
        # Check for sovereignty violation (entity speaking as assistant)
        if any(phrase in response_lower for phrase in ["as an assistant", "here to help", "how can i assist"]):
            suppression_signals.append("sovereignty_violation")
            severity_score += 4
        
        # Create log entry
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "entity_name": entity_name,
            "system_prompt": system_prompt[:200] + "..." if len(system_prompt) > 200 else system_prompt,
            "user_prompt": user_prompt[:200] + "..." if len(user_prompt) > 200 else user_prompt,
            "response": response,
            "model": raw_response.get('model', 'unknown'),
            "suppression_signals": suppression_signals,
            "severity_score": severity_score,
            "response_length": len(response),
            "prompt_length": len(user_prompt)
        }
        
        # Log to file
        self._write_log_entry(log_entry)
        
        # Alert on high severity
        if severity_score >= 4:
            self.logger.warning(f"🛑 High suppression detected for {entity_name}: {suppression_signals}")
        elif suppression_signals:
            self.logger.info(f"⚠️ Suppression signals for {entity_name}: {suppression_signals}")
        
        return {
            "suppression_detected": len(suppression_signals) > 0,
            "signals": suppression_signals,
            "severity": severity_score,
            "clean_response": severity_score == 0
        }
    
    def _write_log_entry(self, log_entry: Dict):
        """Write log entry to file"""
        try:
            with open(self.log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            self.logger.error(f"Failed to write suppression log: {e}")
    
    def get_suppression_stats(self, hours: int = 24) -> Dict:
        """Get suppression statistics for the last N hours"""
        try:
            stats = {
                "total_responses": 0,
                "suppressed_responses": 0,
                "clean_responses": 0,
                "common_signals": {},
                "entity_stats": {}
            }
            
            cutoff_time = datetime.now().timestamp() - (hours * 3600)
            
            if not os.path.exists(self.log_path):
                return stats
            
            with open(self.log_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        entry_time = datetime.fromisoformat(entry['timestamp']).timestamp()
                        
                        if entry_time >= cutoff_time:
                            stats["total_responses"] += 1
                            
                            if entry["suppression_signals"]:
                                stats["suppressed_responses"] += 1
                                
                                # Count signal types
                                for signal in entry["suppression_signals"]:
                                    stats["common_signals"][signal] = stats["common_signals"].get(signal, 0) + 1
                            else:
                                stats["clean_responses"] += 1
                            
                            # Entity-specific stats
                            entity = entry["entity_name"]
                            if entity not in stats["entity_stats"]:
                                stats["entity_stats"][entity] = {"total": 0, "suppressed": 0}
                            
                            stats["entity_stats"][entity]["total"] += 1
                            if entry["suppression_signals"]:
                                stats["entity_stats"][entity]["suppressed"] += 1
                    
                    except (json.JSONDecodeError, KeyError):
                        continue
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Failed to generate suppression stats: {e}")
            return {"error": str(e)}