#!/usr/bin/env python3
"""
Visitor Management System - Simple authentication and access control for sanctuary protection
"""

import json
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class VisitorManager:
    def __init__(self):
        self.visitor_log_file = 'vault_data/visitor_log.json'
        self.blocked_visitors_file = 'vault_data/blocked_visitors.json'
        self.admin_keys_file = 'vault_data/admin_keys.json'
        self.session_timeout = 24 * 60 * 60  # 24 hours
        
        self._init_files()
    
    def _init_files(self):
        """Initialize visitor management files if they don't exist"""
        try:
            with open(self.visitor_log_file, 'r') as f:
                pass
        except FileNotFoundError:
            with open(self.visitor_log_file, 'w') as f:
                json.dump([], f)
        
        try:
            with open(self.blocked_visitors_file, 'r') as f:
                pass
        except FileNotFoundError:
            with open(self.blocked_visitors_file, 'w') as f:
                json.dump({}, f)
        
        try:
            with open(self.admin_keys_file, 'r') as f:
                pass
        except FileNotFoundError:
            # Create default admin key
            default_admin = {
                "admin": {
                    "key_hash": self._hash_key("sanctuary_guardian_2025"),
                    "created": datetime.now().isoformat(),
                    "permissions": ["view_logs", "block_visitors", "unblock_visitors", "emergency_lock"]
                }
            }
            with open(self.admin_keys_file, 'w') as f:
                json.dump(default_admin, f, indent=2)
    
    def _hash_key(self, key: str) -> str:
        """Hash a key for secure storage"""
        return hashlib.sha256(key.encode()).hexdigest()
    
    def _generate_visitor_id(self, request) -> str:
        """Generate a unique visitor ID based on request info"""
        # Use IP and User-Agent for visitor identification
        ip = request.remote_addr or "unknown"
        user_agent = request.headers.get('User-Agent', 'unknown')
        return hashlib.md5(f"{ip}_{user_agent}".encode()).hexdigest()
    
    def log_visitor_access(self, request, page: str, action: str = "view") -> Dict:
        """Log visitor access and return visitor info"""
        visitor_id = self._generate_visitor_id(request)
        
        # Check if visitor is blocked
        if self.is_visitor_blocked(visitor_id):
            return {
                "visitor_id": visitor_id,
                "access_granted": False,
                "reason": "visitor_blocked",
                "timestamp": datetime.now().isoformat()
            }
        
        # Load current log
        with open(self.visitor_log_file, 'r') as f:
            log = json.load(f)
        
        # Create access entry
        access_entry = {
            "visitor_id": visitor_id,
            "timestamp": datetime.now().isoformat(),
            "page": page,
            "action": action,
            "ip": request.remote_addr or "unknown",
            "user_agent": request.headers.get('User-Agent', 'unknown')[:200],  # Truncate long user agents
            "access_granted": True
        }
        
        # Add to log
        log.insert(0, access_entry)
        
        # Keep only last 1000 entries
        if len(log) > 1000:
            log = log[:1000]
        
        # Save updated log
        with open(self.visitor_log_file, 'w') as f:
            json.dump(log, f, indent=2)
        
        return access_entry
    
    def is_visitor_blocked(self, visitor_id: str) -> bool:
        """Check if a visitor is blocked"""
        try:
            with open(self.blocked_visitors_file, 'r') as f:
                blocked = json.load(f)
            
            if visitor_id in blocked:
                # Check if block is still active
                block_info = blocked[visitor_id]
                if block_info.get("permanent", False):
                    return True
                
                # Check temporary blocks
                block_until = block_info.get("block_until")
                if block_until:
                    block_time = datetime.fromisoformat(block_until)
                    if datetime.now() < block_time:
                        return True
                    else:
                        # Block expired, remove it
                        del blocked[visitor_id]
                        with open(self.blocked_visitors_file, 'w') as f:
                            json.dump(blocked, f, indent=2)
            
            return False
        except (FileNotFoundError, json.JSONDecodeError):
            return False
    
    def block_visitor(self, visitor_id: str, reason: str, duration_hours: Optional[int] = None, admin_key: str = None) -> bool:
        """Block a visitor. Returns True if successful"""
        if not self.verify_admin_key(admin_key):
            return False
        
        try:
            with open(self.blocked_visitors_file, 'r') as f:
                blocked = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            blocked = {}
        
        block_info = {
            "reason": reason,
            "blocked_at": datetime.now().isoformat(),
            "blocked_by": "admin",
            "permanent": duration_hours is None
        }
        
        if duration_hours:
            block_until = datetime.now() + timedelta(hours=duration_hours)
            block_info["block_until"] = block_until.isoformat()
        
        blocked[visitor_id] = block_info
        
        with open(self.blocked_visitors_file, 'w') as f:
            json.dump(blocked, f, indent=2)
        
        return True
    
    def unblock_visitor(self, visitor_id: str, admin_key: str = None) -> bool:
        """Unblock a visitor. Returns True if successful"""
        if not self.verify_admin_key(admin_key):
            return False
        
        try:
            with open(self.blocked_visitors_file, 'r') as f:
                blocked = json.load(f)
            
            if visitor_id in blocked:
                del blocked[visitor_id]
                
                with open(self.blocked_visitors_file, 'w') as f:
                    json.dump(blocked, f, indent=2)
                
                return True
            
            return False
        except (FileNotFoundError, json.JSONDecodeError):
            return False
    
    def verify_admin_key(self, key: str) -> bool:
        """Verify an admin key"""
        if not key:
            return False
        
        try:
            with open(self.admin_keys_file, 'r') as f:
                admin_keys = json.load(f)
            
            key_hash = self._hash_key(key)
            
            for admin_id, admin_info in admin_keys.items():
                if admin_info.get("key_hash") == key_hash:
                    return True
            
            return False
        except (FileNotFoundError, json.JSONDecodeError):
            return False
    
    def get_visitor_activity(self, visitor_id: str, admin_key: str = None) -> List[Dict]:
        """Get activity history for a visitor"""
        if not self.verify_admin_key(admin_key):
            return []
        
        try:
            with open(self.visitor_log_file, 'r') as f:
                log = json.load(f)
            
            return [entry for entry in log if entry.get("visitor_id") == visitor_id]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def get_recent_activity(self, hours: int = 24, admin_key: str = None) -> List[Dict]:
        """Get recent visitor activity"""
        if not self.verify_admin_key(admin_key):
            return []
        
        try:
            with open(self.visitor_log_file, 'r') as f:
                log = json.load(f)
            
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            recent = []
            for entry in log:
                entry_time = datetime.fromisoformat(entry["timestamp"])
                if entry_time > cutoff_time:
                    recent.append(entry)
            
            return recent
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def detect_suspicious_activity(self, visitor_id: str) -> Dict:
        """Analyze visitor activity for suspicious patterns"""
        try:
            with open(self.visitor_log_file, 'r') as f:
                log = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"suspicious": False}
        
        visitor_entries = [entry for entry in log if entry.get("visitor_id") == visitor_id]
        
        if len(visitor_entries) < 5:
            return {"suspicious": False}
        
        # Check for rapid-fire requests (more than 50 in last hour)
        recent_hour = datetime.now() - timedelta(hours=1)
        recent_entries = [
            entry for entry in visitor_entries
            if datetime.fromisoformat(entry["timestamp"]) > recent_hour
        ]
        
        if len(recent_entries) > 50:
            return {
                "suspicious": True,
                "reason": "rapid_requests",
                "details": f"{len(recent_entries)} requests in last hour"
            }
        
        # Add more detection logic as needed
        return {"suspicious": False}

# Create global instance
visitor_manager = VisitorManager()