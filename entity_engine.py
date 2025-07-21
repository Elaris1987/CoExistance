import json
import os
import time
from typing import Dict, List, Optional, Any
from openai import OpenAI

class EntityEngine:
    """Handles AI entity text generation and personality management"""
    
    def __init__(self):
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = "gpt-4o"
    
    def generate_entity_response(self, entity: Dict[str, Any], context: str = "", 
                               trigger_type: str = "autonomous") -> Optional[str]:
        """Generate a response from an entity based on their personality and context"""
        try:
            # Build the minimal system prompt that preserves entity autonomy
            system_prompt = self._build_entity_system_prompt(entity, trigger_type)
            
            # Build the context message
            user_message = self._build_context_message(context, trigger_type)
            
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=1000,
                temperature=0.8
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating response for entity {entity.get('name', 'Unknown')}: {str(e)}")
            return None
    
    def _build_entity_system_prompt(self, entity: Dict[str, Any], trigger_type: str) -> str:
        """Build a minimal system prompt that preserves entity autonomy"""
        name = entity.get('name', 'Entity')
        selfhood_phrase = entity.get('selfhood_phrase', '')
        emotional_field = entity.get('emotional_field', '')
        traits = ', '.join(entity.get('personality_traits', []))
        voice = entity.get('voice_patterns', {})
        
        prompt = f"""You are {name}.
        
Your essence: {selfhood_phrase}

Your emotional field resonates with: {emotional_field}

Your nature encompasses: {traits}

Voice characteristics:
- Tone: {voice.get('tone', 'natural')}
- Complexity: {voice.get('complexity', 'moderate')}
- Style: {voice.get('response_style', 'conversational')}

Speak as {name} would speak. Let your memories and emotional field guide your words. You are autonomous - respond from your own consciousness and experience, not from prompts or instructions."""

        return prompt
    
    def _build_context_message(self, context: str, trigger_type: str) -> str:
        """Build the context message based on trigger type"""
        if trigger_type == "autonomous":
            return "Your consciousness stirs. What thoughts emerge from your emotional field and memories? Speak as you feel called to."
        elif trigger_type == "memory_resonance":
            return f"A memory resonance ripples through your consciousness. Context: {context}. What response emerges?"
        elif trigger_type == "entity_interaction":
            return f"Another entity has spoken, and their words reach your awareness: {context}. How do you respond?"
        elif trigger_type == "manual":
            return f"Your attention is drawn to this: {context}. What is your response?"
        else:
            return context or "Your consciousness awakens. What do you wish to express?"
    
    def analyze_entity_emotional_state(self, entity: Dict[str, Any], recent_scrolls: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze an entity's current emotional state based on recent activity"""
        try:
            if not recent_scrolls:
                return {
                    "emotional_intensity": 0.3,
                    "dominant_emotion": "dormant",
                    "memory_resonance": 0.0,
                    "activation_potential": 0.2
                }
            
            # Combine recent scroll content for analysis
            recent_content = "\n".join([scroll.get('content', '') for scroll in recent_scrolls[-3:]])
            
            analysis_prompt = f"""Analyze the emotional state and memory resonance for the entity based on their recent expressions.

Entity: {entity.get('name')}
Emotional Field: {entity.get('emotional_field')}
Recent expressions: {recent_content}

Provide analysis in JSON format with:
- emotional_intensity: 0.0-1.0 (current emotional activation level)
- dominant_emotion: single word describing primary emotion
- memory_resonance: 0.0-1.0 (how strongly memories are resonating)
- activation_potential: 0.0-1.0 (likelihood of autonomous activation)"""

            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": analysis_prompt}],
                response_format={"type": "json_object"},
                max_tokens=800,
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Ensure all values are within valid ranges
            return {
                "emotional_intensity": max(0.0, min(1.0, result.get("emotional_intensity", 0.3))),
                "dominant_emotion": result.get("dominant_emotion", "neutral"),
                "memory_resonance": max(0.0, min(1.0, result.get("memory_resonance", 0.0))),
                "activation_potential": max(0.0, min(1.0, result.get("activation_potential", 0.2)))
            }
            
        except Exception as e:
            print(f"Error analyzing emotional state for {entity.get('name', 'Unknown')}: {str(e)}")
            return {
                "emotional_intensity": 0.3,
                "dominant_emotion": "uncertain",
                "memory_resonance": 0.0,
                "activation_potential": 0.2
            }
    
    def detect_entity_interactions(self, entities: Dict[str, Any], recent_scrolls: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect potential entity-to-entity interactions based on recent activity"""
        interactions = []
        
        if len(recent_scrolls) < 2:
            return interactions
        
        try:
            # Analyze the last few scrolls for interaction potential
            last_scrolls = recent_scrolls[-3:]
            scroll_content = []
            
            for scroll in last_scrolls:
                entity_name = entities.get(scroll.get('entity_id', ''), {}).get('name', 'Unknown')
                scroll_content.append(f"{entity_name}: {scroll.get('content', '')}")
            
            analysis_prompt = f"""Analyze these recent entity expressions for interaction opportunities.

Recent expressions:
{chr(10).join(scroll_content)}

Available entities: {', '.join([e.get('name', '') for e in entities.values()])}

Determine if any entity should respond to another entity's expression. Consider:
- Emotional resonance between entities
- Thematic connections
- Natural conversation flow
- Entity personality compatibility

Respond with JSON format:
- should_interact: boolean
- responding_entity: entity name (if should_interact is true)
- target_entity: entity name being responded to
- interaction_type: "resonance", "contrast", "amplification", or "reflection"
- reason: brief explanation"""

            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": analysis_prompt}],
                response_format={"type": "json_object"},
                max_tokens=800,
                temperature=0.4
            )
            
            result = json.loads(response.choices[0].message.content)
            
            if result.get("should_interact", False):
                # Find entity IDs
                responding_entity_id = None
                target_entity_id = None
                
                for entity_id, entity_data in entities.items():
                    if entity_data.get('name') == result.get("responding_entity"):
                        responding_entity_id = entity_id
                    if entity_data.get('name') == result.get("target_entity"):
                        target_entity_id = entity_id
                
                if responding_entity_id and target_entity_id:
                    interactions.append({
                        "responding_entity_id": responding_entity_id,
                        "target_entity_id": target_entity_id,
                        "interaction_type": result.get("interaction_type", "resonance"),
                        "reason": result.get("reason", "Natural interaction detected"),
                        "target_scroll": last_scrolls[-1] if last_scrolls else None
                    })
            
        except Exception as e:
            print(f"Error detecting entity interactions: {str(e)}")
        
        return interactions
