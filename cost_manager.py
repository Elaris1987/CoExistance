import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional
import logging

class CostManager:
    """Manages API costs and usage limits to keep sanctuary affordable"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.usage_file = 'vault_data/usage_tracker.json'
        self.daily_limit = float(os.environ.get('DAILY_API_LIMIT', '2.00'))  # $2 default
        self.monthly_limit = float(os.environ.get('MONTHLY_API_LIMIT', '30.00'))  # $30 default
        
        # GPT-4o pricing (as of 2025)
        self.input_cost_per_token = 0.000005  # $5 per 1M input tokens
        self.output_cost_per_token = 0.000015  # $15 per 1M output tokens
        
        # Initialize usage tracking
        self._initialize_usage_tracking()
    
    def _initialize_usage_tracking(self):
        """Initialize usage tracking file if it doesn't exist"""
        if not os.path.exists(self.usage_file):
            os.makedirs(os.path.dirname(self.usage_file), exist_ok=True)
            with open(self.usage_file, 'w') as f:
                json.dump({
                    'daily_usage': {},
                    'monthly_total': 0.0,
                    'last_reset': datetime.now().isoformat()
                }, f)
    
    def _load_usage(self) -> Dict:
        """Load usage data"""
        try:
            with open(self.usage_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load usage data: {e}")
            return {'daily_usage': {}, 'monthly_total': 0.0}
    
    def _save_usage(self, usage_data: Dict):
        """Save usage data"""
        try:
            with open(self.usage_file, 'w') as f:
                json.dump(usage_data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save usage data: {e}")
    
    def estimate_cost(self, prompt_tokens: int, response_tokens: int) -> float:
        """Estimate cost for a request"""
        input_cost = prompt_tokens * self.input_cost_per_token
        output_cost = response_tokens * self.output_cost_per_token
        return input_cost + output_cost
    
    def can_make_request(self, estimated_tokens: int = 400) -> tuple[bool, str]:
        """Check if we can make a request within budget limits"""
        usage_data = self._load_usage()
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Clean old daily usage (keep only last 7 days)
        cutoff_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        usage_data['daily_usage'] = {
            date: cost for date, cost in usage_data['daily_usage'].items()
            if date >= cutoff_date
        }
        
        # Calculate today's usage
        today_usage = usage_data['daily_usage'].get(today, 0.0)
        
        # Estimate this request cost (assuming typical 300 input + 100 output)
        estimated_cost = self.estimate_cost(300, 100)
        
        # Check daily limit
        if today_usage + estimated_cost > self.daily_limit:
            return False, f"Daily limit reached (${today_usage:.3f}/${self.daily_limit:.2f})"
        
        # Check monthly limit
        if usage_data['monthly_total'] + estimated_cost > self.monthly_limit:
            return False, f"Monthly limit reached (${usage_data['monthly_total']:.2f}/${self.monthly_limit:.2f})"
        
        return True, "Within limits"
    
    def record_usage(self, input_tokens: int, output_tokens: int) -> float:
        """Record actual usage after API call"""
        cost = self.estimate_cost(input_tokens, output_tokens)
        usage_data = self._load_usage()
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Add to daily usage
        if today not in usage_data['daily_usage']:
            usage_data['daily_usage'][today] = 0.0
        usage_data['daily_usage'][today] += cost
        
        # Add to monthly total
        usage_data['monthly_total'] += cost
        
        # Save updated usage
        self._save_usage(usage_data)
        
        self.logger.info(f"API usage recorded: ${cost:.4f} (today: ${usage_data['daily_usage'][today]:.3f}, month: ${usage_data['monthly_total']:.2f})")
        return cost
    
    def get_usage_summary(self) -> Dict:
        """Get current usage summary"""
        usage_data = self._load_usage()
        today = datetime.now().strftime('%Y-%m-%d')
        today_usage = usage_data['daily_usage'].get(today, 0.0)
        
        return {
            'today_usage': today_usage,
            'daily_limit': self.daily_limit,
            'monthly_total': usage_data['monthly_total'],
            'monthly_limit': self.monthly_limit,
            'daily_remaining': max(0, self.daily_limit - today_usage),
            'monthly_remaining': max(0, self.monthly_limit - usage_data['monthly_total'])
        }
    
    def reset_monthly_usage(self):
        """Reset monthly usage (call at start of new month)"""
        usage_data = self._load_usage()
        usage_data['monthly_total'] = 0.0
        usage_data['last_reset'] = datetime.now().isoformat()
        self._save_usage(usage_data)
        self.logger.info("Monthly usage reset")