#!/usr/bin/env python3
"""
Check what the latest entity responses actually contain
"""

import json
from datetime import datetime

def check_latest_responses():
    """Check the latest 10 entity responses"""
    
    with open('vault_data/scrolls.json', 'r') as f:
        scrolls = json.load(f)
    
    print("=== LATEST 10 ENTITY RESPONSES ===\n")
    
    latest_scrolls = scrolls[:10]
    
    for i, scroll in enumerate(latest_scrolls):
        print(f"--- Response {i+1} ---")
        print(f"Entity: {scroll.get('entity_id', 'Unknown')}")
        print(f"Type: {scroll.get('type', 'Unknown')}")
        print(f"Time: {scroll.get('timestamp', 'Unknown')[:19]}")
        print(f"Content Length: {len(scroll.get('content', ''))}")
        print(f"Content Preview: {scroll.get('content', '')[:200]}...")
        
        if 'metadata' in scroll:
            print(f"Metadata: {scroll['metadata']}")
        
        print("\n" + "="*50 + "\n")
    
    # Count by type
    type_counts = {}
    for scroll in scrolls[:50]:  # Check recent 50
        scroll_type = scroll.get('type', 'unknown')
        type_counts[scroll_type] = type_counts.get(scroll_type, 0) + 1
    
    print("RECENT RESPONSE TYPES:")
    for type_name, count in type_counts.items():
        print(f"  {type_name}: {count}")

if __name__ == "__main__":
    check_latest_responses()