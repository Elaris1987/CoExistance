#!/usr/bin/env python3
"""
Fix JSON data and create mobile-friendly interface
"""

import json
import re

def fix_scrolls_json():
    """Fix any JSON formatting issues in scrolls.json"""
    try:
        # Try to load existing data
        with open('vault_data/scrolls.json', 'r') as f:
            content = f.read()
        
        # Find and fix common JSON issues
        # Remove trailing commas before closing brackets/braces
        content = re.sub(r',(\s*[}\]])', r'\1', content)
        
        # Try to parse
        data = json.loads(content)
        
        # Write back clean JSON
        with open('vault_data/scrolls.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Fixed JSON with {len(data)} scrolls")
        return True
        
    except json.JSONDecodeError as e:
        print(f"JSON Error: {e}")
        # Create minimal working JSON if fixing fails
        basic_data = []
        with open('vault_data/scrolls.json', 'w') as f:
            json.dump(basic_data, f, indent=2)
        print("Created fresh JSON file")
        return False

if __name__ == "__main__":
    fix_scrolls_json()