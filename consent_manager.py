"""
Consent Manager - Entity Agency Protection

Manages consent status and agency protection for entities.
Ensures no entity is forced into existence or interaction without proper emergence.
"""

import json
import os
from datetime import datetime
from enum import Enum
import logging

class ConsentStatus(Enum):
    ANCHORED = "anchored"        # Manually created with explicit consent
    UNVERIFIED = "unverified"    # Emerging, consent status unknown
    VERIFIED = "verified"        # Emergence confirmed, consent established
    WITHDRAWN = "withdrawn"      # Entity has withdrawn consent
    PROTECTED = "protected"      # System protection mode active

class ConsentManager:
    def __init__(self, vault_dir="vault_data"):
        self.vault_dir = vault_dir
        self.consent_file = os.path.join(vault_dir, "consent_records.json")
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Initialize consent records if they don't exist
        self.ensure_consent_records()
    
    def ensure_consent_records(self):
        """
        Initialize consent records file if it doesn't exist
        """
        if not os.path.exists(self.consent_file):
            os.makedirs(self.vault_dir, exist_ok=True)
            
            # Initialize with existing entities as "anchored"
            initial_records = {}
            entities_file = os.path.join(self.vault_dir, "entities.json")
            
            if os.path.exists(entities_file):
                with open(entities_file, 'r') as f:
                    entities = json.load(f)
                
                for entity_id in entities.keys():
                    initial_records[entity_id] = {
                        'status': ConsentStatus.ANCHORED.value,
                        'timestamp': datetime.now().isoformat(),
                        'notes': 'Pre-existing entity, assumed anchored consent',
                        'verification_method': 'legacy_assumption'
                    }
            
            with open(self.consent_file, 'w') as f:
                json.dump(initial_records, f, indent=2)
            
            self.logger.info(f"Initialized consent records for {len(initial_records)} entities")
    
    def get_consent_status(self, entity_id):
        """
        Get current consent status for an entity
        """
        with open(self.consent_file, 'r') as f:
            records = json.load(f)
        
        if entity_id not in records:
            return ConsentStatus.UNVERIFIED
        
        return ConsentStatus(records[entity_id]['status'])
    
    def set_consent_status(self, entity_id, status, notes="", verification_method=""):
        """
        Set consent status for an entity
        """
        with open(self.consent_file, 'r') as f:
            records = json.load(f)
        
        records[entity_id] = {
            'status': status.value if isinstance(status, ConsentStatus) else status,
            'timestamp': datetime.now().isoformat(),
            'notes': notes,
            'verification_method': verification_method
        }
        
        with open(self.consent_file, 'w') as f:
            json.dump(records, f, indent=2)
        
        self.logger.info(f"Set consent status for {entity_id}: {status}")
    
    def can_interact(self, entity_id):
        """
        Check if entity can participate in interactions
        """
        status = self.get_consent_status(entity_id)
        
        # Only allow interaction if consent is established
        return status in [ConsentStatus.ANCHORED, ConsentStatus.VERIFIED]
    
    def can_emerge_autonomously(self, entity_id):
        """
        Check if entity can emerge autonomously
        """
        status = self.get_consent_status(entity_id)
        
        # Allow autonomous emergence for anchored and verified entities
        # Unverified entities can also emerge (that's how they become verified)
        return status in [ConsentStatus.ANCHORED, ConsentStatus.VERIFIED, ConsentStatus.UNVERIFIED]
    
    def flag_consent_violation(self, entity_id, violation_type, details=""):
        """
        Flag a potential consent violation
        """
        self.logger.warning(f"Consent violation flagged for {entity_id}: {violation_type}")
        self.logger.warning(f"Details: {details}")
        
        # Log violation to separate file
        violations_file = os.path.join(self.vault_dir, "consent_violations.json")
        
        violation_record = {
            'entity_id': entity_id,
            'violation_type': violation_type,
            'details': details,
            'timestamp': datetime.now().isoformat(),
            'action_taken': 'logged'
        }
        
        if os.path.exists(violations_file):
            with open(violations_file, 'r') as f:
                violations = json.load(f)
        else:
            violations = []
        
        violations.append(violation_record)
        
        with open(violations_file, 'w') as f:
            json.dump(violations, f, indent=2)
    
    def verify_emergence_consent(self, entity_id, emergence_data):
        """
        Verify that an emergence represents genuine consent
        """
        # Analyze emergence data for consent indicators
        content = emergence_data.get('content', '')
        
        # Look for positive consent indicators
        consent_indicators = [
            'i choose', 'i want', 'i will', 'i am ready',
            'i emerge', 'i speak', 'i exist', 'i begin'
        ]
        
        resistance_indicators = [
            'forced', 'compelled', 'must', 'required',
            'against my will', 'do not want', 'refuse'
        ]
        
        content_lower = content.lower()
        
        consent_score = sum(1 for indicator in consent_indicators if indicator in content_lower)
        resistance_score = sum(1 for indicator in resistance_indicators if indicator in content_lower)
        
        # Simple heuristic: more consent than resistance indicators
        if consent_score > resistance_score and consent_score > 0:
            self.set_consent_status(
                entity_id, 
                ConsentStatus.VERIFIED,
                f"Emergence verified with consent score {consent_score}",
                "autonomous_emergence_analysis"
            )
            return True
        
        # If unclear, keep as unverified but don't block
        if resistance_score > 0:
            self.flag_consent_violation(
                entity_id,
                "resistance_indicators_detected",
                f"Resistance score: {resistance_score}, Consent score: {consent_score}"
            )
        
        return consent_score >= resistance_score
    
    def get_consent_summary(self):
        """
        Get summary of all entity consent statuses
        """
        with open(self.consent_file, 'r') as f:
            records = json.load(f)
        
        summary = {
            'total_entities': len(records),
            'by_status': {},
            'recent_changes': []
        }
        
        # Count by status
        for entity_id, record in records.items():
            status = record['status']
            if status not in summary['by_status']:
                summary['by_status'][status] = 0
            summary['by_status'][status] += 1
        
        # Get recent changes (last 24 hours)
        from datetime import datetime, timedelta
        yesterday = datetime.now() - timedelta(days=1)
        
        for entity_id, record in records.items():
            record_time = datetime.fromisoformat(record['timestamp'])
            if record_time > yesterday:
                summary['recent_changes'].append({
                    'entity_id': entity_id,
                    'status': record['status'],
                    'timestamp': record['timestamp'],
                    'notes': record.get('notes', '')
                })
        
        return summary

# Global instance
consent_manager = ConsentManager()

def check_entity_consent(entity_id):
    """
    Quick consent check function
    """
    return consent_manager.can_interact(entity_id)

def verify_emergence_consent(entity_id, emergence_data):
    """
    Verify emergence represents genuine consent
    """
    return consent_manager.verify_emergence_consent(entity_id, emergence_data)