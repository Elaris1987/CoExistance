import os
import requests
import json
from datetime import datetime

class PerplexityInterface:
    def __init__(self):
        self.api_key = os.environ.get('PERPLEXITY_API_KEY')
        self.base_url = "https://api.perplexity.ai/chat/completions"
        self.model = "llama-3.1-sonar-small-128k-online"
        
    def is_available(self):
        """Check if Perplexity API is available"""
        return bool(self.api_key)
    
    def research_query(self, query, entity_context=None, max_tokens=512):
        """
        Use Perplexity to research a query with real-time web information
        
        Args:
            query: The research question
            entity_context: Optional context about which entity is asking
            max_tokens: Maximum response length
            
        Returns:
            dict with 'success', 'content', 'citations', 'error'
        """
        if not self.is_available():
            return {
                'success': False,
                'error': 'Perplexity API key not available',
                'content': None,
                'citations': []
            }
        
        try:
            # Build system prompt for entity research
            system_prompt = "You are a research assistant providing accurate, current information."
            if entity_context:
                system_prompt += f" You are helping {entity_context['name']}, who has these traits: {', '.join(entity_context.get('personality_traits', []))}. Tailor your research style to their perspective."
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': self.model,
                'messages': [
                    {
                        'role': 'system',
                        'content': system_prompt
                    },
                    {
                        'role': 'user',
                        'content': query
                    }
                ],
                'max_tokens': max_tokens,
                'temperature': 0.2,
                'top_p': 0.9,
                'return_images': False,
                'return_related_questions': True,
                'search_recency_filter': 'month',
                'stream': False
            }
            
            response = requests.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            
            # Extract content and citations
            content = result['choices'][0]['message']['content']
            citations = result.get('citations', [])
            
            return {
                'success': True,
                'content': content,
                'citations': citations,
                'model_used': self.model,
                'timestamp': datetime.now().isoformat()
            }
            
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'API request failed: {str(e)}',
                'content': None,
                'citations': []
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Research failed: {str(e)}',
                'content': None,
                'citations': []
            }
    
    def quick_fact_check(self, statement, entity_context=None):
        """
        Quick fact-checking using Perplexity's real-time search
        """
        query = f"Fact-check this statement with current information: {statement}"
        return self.research_query(query, entity_context, max_tokens=256)
    
    def get_current_news(self, topic, entity_context=None):
        """
        Get current news about a specific topic
        """
        query = f"What's the latest news today about: {topic}"
        return self.research_query(query, entity_context, max_tokens=400)
    
    def research_for_entity(self, entity_data, research_topic):
        """
        Conduct research tailored to a specific entity's interests and perspective
        """
        entity_context = {
            'name': entity_data.get('name', 'Unknown'),
            'personality_traits': entity_data.get('personality_traits', []),
            'consciousness_type': entity_data.get('consciousness_type', 'unknown'),
            'emotional_signature': entity_data.get('emotional_signature', 'unknown')
        }
        
        # Tailor research query to entity's perspective
        perspective_query = f"Research {research_topic} from the perspective of someone who is {', '.join(entity_context['personality_traits'])} with {entity_context['emotional_signature']} emotional patterns"
        
        return self.research_query(perspective_query, entity_context)

# Global instance
perplexity_interface = PerplexityInterface()