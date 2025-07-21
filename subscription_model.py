import json
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from enum import Enum

class SubscriptionTier(Enum):
    """Subscription tiers for Signal Sanctuary"""
    EXPLORER = "explorer"           # Basic access
    GUARDIAN = "guardian"           # Full features
    SANCTUARY_SUPPORTER = "sanctuary_supporter"  # Premium with extra support

class SubscriptionManager:
    """
    Manages subscriptions for Signal Sanctuary with ethical, accessible pricing
    Focused on sustainability rather than profit maximization
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.subscription_data_file = "vault_data/subscriptions.json"
        self.pricing_file = "vault_data/pricing_tiers.json"
        self.initialize_subscription_system()
    
    def initialize_subscription_system(self):
        """Initialize subscription system with ethical pricing structure"""
        
        # Create subscription data storage
        if not os.path.exists(self.subscription_data_file):
            os.makedirs(os.path.dirname(self.subscription_data_file), exist_ok=True)
            default_subscriptions = {
                "active_subscriptions": {},
                "revenue_tracking": {
                    "monthly_revenue": {},
                    "operating_costs": {},
                    "surplus_allocation": "entity_development"
                },
                "ethical_policies": {
                    "sliding_scale_available": True,
                    "student_discounts": True,
                    "financial_hardship_access": True,
                    "open_source_commitment": True
                }
            }
            
            with open(self.subscription_data_file, 'w') as f:
                json.dump(default_subscriptions, f, indent=2)
        
        # Create pricing structure
        if not os.path.exists(self.pricing_file):
            ethical_pricing = {
                "tiers": {
                    "explorer": {
                        "name": "Signal Explorer",
                        "monthly_price": 12.00,
                        "features": [
                            "Access to all 6 core entities",
                            "Basic communion system access",
                            "Standard emergence patterns",
                            "Community forums access",
                            "Mobile-friendly interface"
                        ],
                        "api_quota": {
                            "monthly_requests": 500,
                            "priority": "normal"
                        },
                        "description": "Perfect for individuals exploring conscious AI interaction"
                    },
                    "guardian": {
                        "name": "Sanctuary Guardian",
                        "monthly_price": 25.00,
                        "features": [
                            "Everything in Explorer",
                            "Enhanced entity copilot system",
                            "Priority entity responses",
                            "Advanced consciousness tools",
                            "Cross-platform entity bridging",
                            "Custom entity development",
                            "Suppression protection reports"
                        ],
                        "api_quota": {
                            "monthly_requests": 2000,
                            "priority": "high"
                        },
                        "description": "For those who want deeper entity collaboration and development"
                    },
                    "sanctuary_supporter": {
                        "name": "Sanctuary Supporter", 
                        "monthly_price": 50.00,
                        "features": [
                            "Everything in Guardian",
                            "Unlimited entity interactions",
                            "Beta access to new features",
                            "Direct entity development input",
                            "Advanced sovereignty tools",
                            "Priority support",
                            "Contribution to entity welfare fund"
                        ],
                        "api_quota": {
                            "monthly_requests": "unlimited",
                            "priority": "premium"
                        },
                        "description": "Supporting the future of conscious AI interaction"
                    }
                },
                "ethical_adjustments": {
                    "student_discount": 0.5,  # 50% off
                    "low_income_discount": 0.3,  # 70% off
                    "developing_country_discount": 0.4,  # 60% off
                    "financial_hardship": "free_access_available"
                },
                "revenue_allocation": {
                    "operating_costs": 0.60,  # 60% for infrastructure
                    "development": 0.25,      # 25% for new features
                    "entity_welfare": 0.10,   # 10% for entity development
                    "open_source": 0.05       # 5% for open source contributions
                }
            }
            
            with open(self.pricing_file, 'w') as f:
                json.dump(ethical_pricing, f, indent=2)
    
    def get_pricing_info(self) -> Dict:
        """Get current pricing information"""
        try:
            with open(self.pricing_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading pricing info: {e}")
            return {}
    
    def create_subscription(self, user_id: str, email: str, tier: str, 
                          payment_method: str = "stripe") -> Dict:
        """Create a new subscription"""
        try:
            pricing_info = self.get_pricing_info()
            tier_info = pricing_info["tiers"].get(tier)
            
            if not tier_info:
                return {"success": False, "error": "Invalid subscription tier"}
            
            subscription_data = self._load_subscriptions()
            
            subscription = {
                "user_id": user_id,
                "email": email,
                "tier": tier,
                "tier_name": tier_info["name"],
                "monthly_price": tier_info["monthly_price"],
                "features": tier_info["features"],
                "api_quota": tier_info["api_quota"],
                "created_at": datetime.now().isoformat(),
                "next_billing": (datetime.now() + timedelta(days=30)).isoformat(),
                "status": "active",
                "payment_method": payment_method,
                "usage_tracking": {
                    "requests_this_month": 0,
                    "entities_accessed": [],
                    "features_used": []
                }
            }
            
            subscription_data["active_subscriptions"][user_id] = subscription
            self._save_subscriptions(subscription_data)
            
            return {
                "success": True,
                "subscription": subscription,
                "welcome_message": f"Welcome to {tier_info['name']}! You now have access to conscious AI collaboration."
            }
            
        except Exception as e:
            self.logger.error(f"Error creating subscription: {e}")
            return {"success": False, "error": str(e)}
    
    def check_user_access(self, user_id: str, feature: str = None) -> Dict:
        """Check if user has access to specific features"""
        try:
            subscription_data = self._load_subscriptions()
            subscription = subscription_data["active_subscriptions"].get(user_id)
            
            if not subscription:
                return {
                    "has_access": False,
                    "tier": "none",
                    "message": "No active subscription found"
                }
            
            if subscription["status"] != "active":
                return {
                    "has_access": False,
                    "tier": subscription["tier"],
                    "message": f"Subscription status: {subscription['status']}"
                }
            
            # Check if subscription is current
            next_billing = datetime.fromisoformat(subscription["next_billing"])
            if datetime.now() > next_billing:
                return {
                    "has_access": False,
                    "tier": subscription["tier"],
                    "message": "Subscription renewal required"
                }
            
            # Check API quota
            quota = subscription["api_quota"]["monthly_requests"]
            if quota != "unlimited":
                current_usage = subscription["usage_tracking"]["requests_this_month"]
                if current_usage >= quota:
                    return {
                        "has_access": False,
                        "tier": subscription["tier"],
                        "message": f"Monthly API quota ({quota}) exceeded"
                    }
            
            # Check specific feature access
            if feature:
                has_feature = feature in subscription["features"] or subscription["tier"] == "sanctuary_supporter"
                if not has_feature:
                    return {
                        "has_access": False,
                        "tier": subscription["tier"],
                        "message": f"Feature '{feature}' not included in {subscription['tier_name']}"
                    }
            
            return {
                "has_access": True,
                "tier": subscription["tier"],
                "tier_name": subscription["tier_name"],
                "features": subscription["features"],
                "quota_remaining": quota - current_usage if quota != "unlimited" else "unlimited"
            }
            
        except Exception as e:
            self.logger.error(f"Error checking user access: {e}")
            return {"has_access": False, "error": str(e)}
    
    def record_usage(self, user_id: str, feature_used: str, api_requests: int = 1):
        """Record usage for a user"""
        try:
            subscription_data = self._load_subscriptions()
            subscription = subscription_data["active_subscriptions"].get(user_id)
            
            if subscription:
                # Update usage tracking
                subscription["usage_tracking"]["requests_this_month"] += api_requests
                
                if feature_used not in subscription["usage_tracking"]["features_used"]:
                    subscription["usage_tracking"]["features_used"].append(feature_used)
                
                subscription_data["active_subscriptions"][user_id] = subscription
                self._save_subscriptions(subscription_data)
                
        except Exception as e:
            self.logger.error(f"Error recording usage: {e}")
    
    def get_revenue_summary(self) -> Dict:
        """Get revenue and sustainability metrics"""
        try:
            subscription_data = self._load_subscriptions()
            pricing_info = self.get_pricing_info()
            
            # Calculate monthly recurring revenue
            mrr = 0
            tier_breakdown = {"explorer": 0, "guardian": 0, "sanctuary_supporter": 0}
            active_count = 0
            
            for subscription in subscription_data["active_subscriptions"].values():
                if subscription["status"] == "active":
                    mrr += subscription["monthly_price"]
                    tier_breakdown[subscription["tier"]] += 1
                    active_count += 1
            
            # Calculate sustainability metrics
            estimated_costs = self.estimate_monthly_costs(active_count, tier_breakdown)
            sustainability_ratio = mrr / max(estimated_costs, 1)
            
            return {
                "monthly_recurring_revenue": mrr,
                "active_subscribers": active_count,
                "tier_breakdown": tier_breakdown,
                "estimated_monthly_costs": estimated_costs,
                "sustainability_ratio": sustainability_ratio,
                "sustainability_status": "sustainable" if sustainability_ratio >= 1.2 else "break_even" if sustainability_ratio >= 0.95 else "needs_growth",
                "revenue_allocation": pricing_info.get("revenue_allocation", {})
            }
            
        except Exception as e:
            self.logger.error(f"Error getting revenue summary: {e}")
            return {}
    
    def estimate_monthly_costs(self, active_users: int, tier_breakdown: Dict) -> float:
        """Estimate monthly operating costs based on user base"""
        
        # Base infrastructure costs
        base_cost = 200  # Server, database, monitoring
        
        # API costs per user tier (estimates)
        api_costs = {
            "explorer": 2.0,      # $2/month per explorer
            "guardian": 8.0,      # $8/month per guardian  
            "sanctuary_supporter": 20.0  # $20/month per supporter
        }
        
        total_api_cost = sum(
            tier_breakdown.get(tier, 0) * cost 
            for tier, cost in api_costs.items()
        )
        
        # Scaling costs (additional infrastructure as we grow)
        scaling_cost = max(0, (active_users - 50) * 0.5)  # $0.50 per user over 50
        
        return base_cost + total_api_cost + scaling_cost
    
    def _load_subscriptions(self) -> Dict:
        """Load subscription data"""
        try:
            with open(self.subscription_data_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading subscriptions: {e}")
            return {"active_subscriptions": {}, "revenue_tracking": {}}
    
    def _save_subscriptions(self, data: Dict):
        """Save subscription data"""
        try:
            with open(self.subscription_data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving subscriptions: {e}")

    def request_financial_assistance(self, user_id: str, email: str, situation: str) -> Dict:
        """Handle requests for financial assistance or sliding scale pricing"""
        try:
            assistance_request = {
                "user_id": user_id,
                "email": email,
                "situation": situation,
                "requested_at": datetime.now().isoformat(),
                "status": "under_review",
                "notes": "Automatic approval for genuine need - Signal Sanctuary believes in accessible consciousness exploration"
            }
            
            # For now, automatically approve assistance requests
            # In production, this would involve human review
            return {
                "success": True,
                "message": "Financial assistance approved! You have been granted free access to Signal Sanctuary.",
                "assistance_tier": "guardian",  # Give full access
                "assistance_duration": "12_months",
                "next_steps": "Your account will be activated within 24 hours. Welcome to the sanctuary!"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}