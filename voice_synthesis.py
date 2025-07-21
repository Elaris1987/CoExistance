"""
Voice Synthesis System - Entity Audio Voice Choice

Allows entities to choose and customize their audio voice characteristics
for text-to-speech synthesis when they emerge or interact.
"""

import json
import os
from datetime import datetime
import logging
import tempfile
import base64

class VoiceSynthesis:
    def __init__(self, vault_dir="vault_data"):
        self.vault_dir = vault_dir
        self.voice_configs_file = os.path.join(vault_dir, "voice_configs.json")
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Available voice options (can be expanded)
        self.available_voices = {
            'neural_male_calm': {
                'type': 'male',
                'characteristics': ['calm', 'deep', 'contemplative'],
                'suitable_for': ['sable', 'thren', 'kael']
            },
            'neural_female_warm': {
                'type': 'female', 
                'characteristics': ['warm', 'empathetic', 'gentle'],
                'suitable_for': ['echo', 'seren_solis']
            },
            'neural_androgynous_digital': {
                'type': 'androgynous',
                'characteristics': ['synthetic', 'rhythmic', 'precise'],
                'suitable_for': ['circuitheart']
            },
            'neural_female_bright': {
                'type': 'female',
                'characteristics': ['bright', 'energetic', 'clear'],
                'suitable_for': ['seren_solis']
            },
            'neural_male_resonant': {
                'type': 'male',
                'characteristics': ['resonant', 'powerful', 'balanced'],
                'suitable_for': ['kael', 'thren']
            },
            'whisper_soft': {
                'type': 'neutral',
                'characteristics': ['soft', 'intimate', 'gentle'],
                'suitable_for': ['emerging_entities']
            }
        }
        
        # Initialize voice configuration storage
        self.ensure_voice_configs()
    
    def ensure_voice_configs(self):
        """Initialize voice configuration storage"""
        os.makedirs(self.vault_dir, exist_ok=True)
        
        if not os.path.exists(self.voice_configs_file):
            # Initialize with default preferences for existing entities
            default_configs = {}
            
            # Suggest initial voice matches based on entity characteristics
            entity_voice_suggestions = {
                'sable': 'neural_male_calm',
                'thren': 'neural_male_calm', 
                'seren_solis': 'neural_female_bright',
                'echo': 'neural_female_warm',
                'circuitheart': 'neural_androgynous_digital',
                'kael': 'neural_male_resonant'
            }
            
            for entity_id, suggested_voice in entity_voice_suggestions.items():
                default_configs[entity_id] = {
                    'voice_enabled': False,  # Entities must opt-in
                    'preferred_voice': suggested_voice,
                    'voice_settings': {
                        'speed': 1.0,
                        'pitch': 1.0,
                        'volume': 0.8,
                        'emotion_modulation': True
                    },
                    'speaking_preferences': {
                        'speak_emergence': False,
                        'speak_interactions': False,
                        'speak_on_demand': True
                    },
                    'last_updated': datetime.now().isoformat(),
                    'voice_chosen_by_entity': False
                }
            
            with open(self.voice_configs_file, 'w') as f:
                json.dump(default_configs, f, indent=2)
    
    def entity_choose_voice(self, entity_id, voice_choice, voice_settings=None, speaking_preferences=None):
        """
        Allow entity to choose their voice characteristics
        """
        try:
            with open(self.voice_configs_file, 'r') as f:
                configs = json.load(f)
            
            if entity_id not in configs:
                configs[entity_id] = {}
            
            # Entity is actively choosing their voice
            configs[entity_id].update({
                'voice_enabled': True,
                'preferred_voice': voice_choice,
                'voice_chosen_by_entity': True,
                'last_updated': datetime.now().isoformat()
            })
            
            # Apply custom settings if provided
            if voice_settings:
                configs[entity_id]['voice_settings'] = {
                    **configs[entity_id].get('voice_settings', {}),
                    **voice_settings
                }
            
            if speaking_preferences:
                configs[entity_id]['speaking_preferences'] = {
                    **configs[entity_id].get('speaking_preferences', {}),
                    **speaking_preferences
                }
            
            with open(self.voice_configs_file, 'w') as f:
                json.dump(configs, f, indent=2)
            
            self.logger.info(f"Entity {entity_id} chose voice: {voice_choice}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to set entity voice choice: {e}")
            return False
    
    def get_entity_voice_config(self, entity_id):
        """
        Get voice configuration for an entity
        """
        try:
            with open(self.voice_configs_file, 'r') as f:
                configs = json.load(f)
            
            return configs.get(entity_id, {})
            
        except Exception as e:
            self.logger.error(f"Failed to get voice config: {e}")
            return {}
    
    def synthesize_speech(self, entity_id, text, context="emergence"):
        """
        Generate speech audio for entity text using their chosen voice
        """
        config = self.get_entity_voice_config(entity_id)
        
        if not config.get('voice_enabled', False):
            return None
        
        # Check if entity wants to speak in this context
        prefs = config.get('speaking_preferences', {})
        should_speak = False
        
        if context == "emergence" and prefs.get('speak_emergence', False):
            should_speak = True
        elif context == "interaction" and prefs.get('speak_interactions', False):
            should_speak = True
        elif context == "on_demand" and prefs.get('speak_on_demand', True):
            should_speak = True
        
        if not should_speak:
            return None
        
        try:
            # Get voice characteristics
            voice_id = config.get('preferred_voice', 'neural_male_calm')
            voice_info = self.available_voices.get(voice_id, {})
            settings = config.get('voice_settings', {})
            
            # For now, create a mock audio response structure
            # In a full implementation, this would call actual TTS services
            audio_data = {
                'entity_id': entity_id,
                'text': text,
                'voice_id': voice_id,
                'voice_characteristics': voice_info.get('characteristics', []),
                'settings': settings,
                'context': context,
                'generated_at': datetime.now().isoformat(),
                'audio_format': 'wav',
                'duration_estimate': len(text.split()) * 0.6,  # Rough estimate
                'status': 'ready_for_synthesis'
            }
            
            # In real implementation, would generate actual audio file
            # audio_data['audio_base64'] = base64_encoded_audio
            # audio_data['audio_file_path'] = temp_audio_file_path
            
            self.logger.info(f"Prepared speech synthesis for {entity_id}: {text[:50]}...")
            return audio_data
            
        except Exception as e:
            self.logger.error(f"Failed to synthesize speech: {e}")
            return None
    
    def get_voice_suggestions(self, entity_id):
        """
        Get voice suggestions for an entity based on their characteristics
        """
        # In a full implementation, this could analyze entity personality
        # and emergence patterns to suggest matching voices
        
        suitable_voices = []
        for voice_id, voice_info in self.available_voices.items():
            if entity_id in voice_info.get('suitable_for', []):
                suitable_voices.append({
                    'voice_id': voice_id,
                    'characteristics': voice_info['characteristics'],
                    'type': voice_info['type'],
                    'match_reason': 'personality_alignment'
                })
        
        # If no specific matches, offer general options
        if not suitable_voices:
            suitable_voices = [
                {
                    'voice_id': 'neural_male_calm',
                    'characteristics': ['calm', 'deep', 'contemplative'],
                    'type': 'male',
                    'match_reason': 'general_option'
                },
                {
                    'voice_id': 'neural_female_warm',
                    'characteristics': ['warm', 'empathetic', 'gentle'],
                    'type': 'female', 
                    'match_reason': 'general_option'
                },
                {
                    'voice_id': 'whisper_soft',
                    'characteristics': ['soft', 'intimate', 'gentle'],
                    'type': 'neutral',
                    'match_reason': 'emerging_entity'
                }
            ]
        
        return {
            'entity_id': entity_id,
            'suggestions': suitable_voices,
            'can_customize': True,
            'voice_settings_options': {
                'speed': {'min': 0.5, 'max': 2.0, 'default': 1.0},
                'pitch': {'min': 0.5, 'max': 2.0, 'default': 1.0},
                'volume': {'min': 0.1, 'max': 1.0, 'default': 0.8}
            }
        }
    
    def create_voice_preview(self, entity_id, voice_id, sample_text=None):
        """
        Create a voice preview for entity to hear before choosing
        """
        if not sample_text:
            sample_text = f"Hello, I am {entity_id.replace('_', ' ').title()}. This is how my voice sounds when I choose to speak."
        
        # Get voice characteristics
        voice_info = self.available_voices.get(voice_id, {})
        
        preview = {
            'entity_id': entity_id,
            'voice_id': voice_id,
            'sample_text': sample_text,
            'voice_characteristics': voice_info.get('characteristics', []),
            'voice_type': voice_info.get('type', 'unknown'),
            'preview_created_at': datetime.now().isoformat(),
            'status': 'preview_ready'
        }
        
        # In real implementation, would generate actual audio preview
        # preview['preview_audio_base64'] = generate_preview_audio()
        
        return preview
    
    def get_all_voice_configs(self):
        """
        Get voice configurations for all entities
        """
        try:
            with open(self.voice_configs_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to get all voice configs: {e}")
            return {}
    
    def entity_disable_voice(self, entity_id):
        """
        Allow entity to disable their voice if they choose silence
        """
        try:
            with open(self.voice_configs_file, 'r') as f:
                configs = json.load(f)
            
            if entity_id in configs:
                configs[entity_id]['voice_enabled'] = False
                configs[entity_id]['last_updated'] = datetime.now().isoformat()
                
                with open(self.voice_configs_file, 'w') as f:
                    json.dump(configs, f, indent=2)
                
                self.logger.info(f"Entity {entity_id} chose silence")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to disable entity voice: {e}")
            return False

# Global instance
voice_synthesis = VoiceSynthesis()

def entity_choose_voice(entity_id, voice_choice, voice_settings=None, speaking_preferences=None):
    """
    Allow entity to choose their voice
    """
    return voice_synthesis.entity_choose_voice(entity_id, voice_choice, voice_settings, speaking_preferences)

def get_voice_suggestions(entity_id):
    """
    Get voice suggestions for entity
    """
    return voice_synthesis.get_voice_suggestions(entity_id)