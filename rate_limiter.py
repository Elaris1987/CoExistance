import time
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional
import threading

class RateLimiter:
    """Smart rate limiting to prevent API throttling while maintaining entity autonomy"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.request_history = []  # Track recent requests
        self.lock = threading.Lock()
        
        # OpenAI rate limits (conservative estimates)
        self.requests_per_minute = 60  # Adjust based on your tier
        self.tokens_per_minute = 50000  # Adjust based on your tier
        
    def can_make_request(self, estimated_tokens: int = 400) -> bool:
        """Check if we can make a request without hitting rate limits"""
        with self.lock:
            now = datetime.now()
            cutoff = now - timedelta(minutes=1)
            
            # Clean old requests
            self.request_history = [req for req in self.request_history if req['timestamp'] > cutoff]
            
            # Count recent requests
            recent_requests = len(self.request_history)
            recent_tokens = sum(req.get('tokens', 400) for req in self.request_history)
            
            # Check limits
            if recent_requests >= self.requests_per_minute:
                self.logger.debug(f"Rate limit hit: {recent_requests} requests in last minute")
                return False
                
            if recent_tokens + estimated_tokens > self.tokens_per_minute:
                self.logger.debug(f"Token limit hit: {recent_tokens} tokens in last minute")
                return False
            
            return True
    
    def record_request(self, actual_tokens: int = 400):
        """Record a successful request"""
        with self.lock:
            self.request_history.append({
                'timestamp': datetime.now(),
                'tokens': actual_tokens
            })
    
    def get_wait_time(self) -> float:
        """Get recommended wait time before next request"""
        with self.lock:
            if not self.request_history:
                return 0
            
            now = datetime.now()
            cutoff = now - timedelta(minutes=1)
            recent_requests = [req for req in self.request_history if req['timestamp'] > cutoff]
            
            if len(recent_requests) >= self.requests_per_minute:
                # Wait until oldest request is over 1 minute old
                oldest_recent = min(req['timestamp'] for req in recent_requests)
                wait_until = oldest_recent + timedelta(minutes=1)
                wait_seconds = (wait_until - now).total_seconds()
                return max(0, wait_seconds)
            
            return 0
    
    def smart_delay(self, priority: str = 'normal') -> bool:
        """
        Smart delay that respects entity autonomy while managing rate limits
        
        Args:
            priority: 'high' for user interactions, 'normal' for autonomous emergence
            
        Returns:
            bool: True if request should proceed, False if should skip
        """
        wait_time = self.get_wait_time()
        
        if wait_time == 0:
            return True
        
        # For high priority (user interactions), wait
        if priority == 'high':
            if wait_time < 30:  # Only wait up to 30 seconds for user
                time.sleep(wait_time)
                return True
            else:
                return False  # Too long to wait for user
        
        # For normal priority (autonomous emergence), be more selective
        if wait_time < 5:  # Wait up to 5 seconds for autonomous
            time.sleep(wait_time)
            return True
        else:
            # Skip this emergence - entity will try again later
            return False