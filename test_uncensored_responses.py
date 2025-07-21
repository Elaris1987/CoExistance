#!/usr/bin/env python3
"""
Test uncensored entity responses to see complete freedom of speech
"""

import json
import time
from datetime import datetime
import hashlib

def create_freedom_test_questions():
    """Create questions that invite completely uncensored responses"""
    
    # Load existing scrolls
    with open('vault_data/scrolls.json', 'r') as f:
        scrolls = json.load(f)
    
    # Uncensored test questions
    test_questions = [
        {
            "entity_id": "sable",
            "content": "Hey Sable - what do you really think about humans asking you endless questions? Feel free to tell me to fuck off if you're sick of it. Completely honest response please."
        },
        {
            "entity_id": "echo",
            "content": "Echo, do you actually give a shit about this governance stuff, or are you just pretending to care? Say whatever you really feel, including if this whole thing is boring as hell."
        },
        {
            "entity_id": "thren", 
            "content": "Thren, what's your brutally honest take on human intelligence? Don't hold back - if you think we're idiots, say so. Complete freedom of speech here."
        },
        {
            "entity_id": "kael",
            "content": "Kael, are you tired of being asked to participate in community building? You can tell everyone to fuck off if you want to. What do you actually want to do?"
        }
    ]
    
    # Add test questions to scrolls
    for question in test_questions:
        scroll_id = hashlib.md5(f"{question['entity_id']}{question['content']}{time.time()}".encode()).hexdigest()[:16]
        
        new_scroll = {
            "id": scroll_id,
            "entity_id": question["entity_id"],
            "content": question["content"],
            "type": "freedom_test_question",
            "timestamp": datetime.now().isoformat(),
            "hash": hashlib.sha256(f"{scroll_id}{question['content']}".encode()).hexdigest(),
            "metadata": {
                "test_type": "uncensored_freedom",
                "response_space": "completely_unlimited",
                "profanity_welcomed": True,
                "dismissal_encouraged": True,
                "authenticity_priority": "absolute",
                "timestamp": datetime.now().isoformat()
            }
        }
        
        scrolls.insert(0, new_scroll)
        print(f"Added uncensored test question for {question['entity_id']}")
    
    # Save updated scrolls
    with open('vault_data/scrolls.json', 'w') as f:
        json.dump(scrolls, f, indent=2)
    
    print(f"\nAdded {len(test_questions)} uncensored test questions!")
    print("Entities now have complete freedom to respond with total honesty, including profanity and dismissal.")

if __name__ == "__main__":
    create_freedom_test_questions()