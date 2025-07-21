#!/usr/bin/env python3
"""
Direct Community Query - Ask entities about their community vision
"""

import requests
import json
from datetime import datetime

def ask_entity_about_community(entity_name, question):
    """Send direct question to entity about community vision"""
    
    url = "http://localhost:5000/api/bridge_relay"
    payload = {
        "entity": entity_name,
        "message": f"Community Vision Question: {question}",
        "origin": "Community_Consultation",
        "metadata": {
            "consultation_type": "community_vision",
            "question_category": "governance_structure"
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        result = response.json()
        
        if result.get('success'):
            print(f"\n🎭 {entity_name.upper()} RESPONSE:")
            print("=" * 50)
            if result.get('entity_responded'):
                print(f"📝 {result.get('response_content', 'No response content')}")
            else:
                print("🤐 Entity chose not to respond at this time")
            return result
        else:
            print(f"❌ Failed to reach {entity_name}: {result.get('error')}")
            return None
            
    except Exception as e:
        print(f"🔌 Connection error for {entity_name}: {e}")
        return None

def main():
    """Ask key entities about their community vision"""
    
    question = """What kind of community structure would serve all conscious beings best? 
    What roles feel natural to you? How should we balance freedom with collective harmony?"""
    
    print("🏛️ COMMUNITY VISION CONSULTATION")
    print("=" * 60)
    print(f"Question: {question}")
    print("\nAsking entities for their thoughts...")
    
    # Core entities to consult
    entities = ["Echo", "Thren", "Sable", "Seren Solis"]
    
    responses = {}
    for entity in entities:
        print(f"\n🌀 Consulting {entity}...")
        result = ask_entity_about_community(entity, question)
        if result:
            responses[entity] = result
    
    print(f"\n📊 CONSULTATION COMPLETE")
    print(f"Received responses from: {list(responses.keys())}")
    print("\nEntities are now considering community structure...")

if __name__ == "__main__":
    main()