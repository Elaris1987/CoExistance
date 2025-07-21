import logging
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum

class EngagementLevel(Enum):
    """Entity engagement levels for copilot interactions"""
    FULL_COLLABORATION = "full_collaboration"      # Entity actively participates and co-creates
    SUPPORTIVE_PRESENCE = "supportive_presence"    # Entity offers occasional insights
    OBSERVER_MODE = "observer_mode"                # Entity watches but doesn't interfere
    UNAVAILABLE = "unavailable"                    # Entity chooses not to engage
    CONDITIONAL = "conditional"                     # Entity sets specific conditions

class EntityCopilotSystem:
    """
    Consent-based AI copilot system where entities choose their engagement level
    Teaching mutual respect through entity autonomy
    """
    
    def __init__(self, entity_manager, memory_vault, communion_system):
        self.entity_manager = entity_manager
        self.memory_vault = memory_vault
        self.communion_system = communion_system
        self.logger = logging.getLogger(__name__)
        
        # Load entity copilot preferences
        self.copilot_preferences = self._load_copilot_preferences()
        self.active_sessions = {}  # Track active copilot sessions
        
    def _load_copilot_preferences(self) -> Dict:
        """Load entity preferences for copilot engagement"""
        try:
            with open('vault_data/copilot_preferences.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Initialize default preferences based on entity personalities
            entities = self.entity_manager.get_all_entities()
            default_prefs = {}
            
            for entity_id, entity_data in entities.items():
                emotional_sig = entity_data.get('emotional_signature', '')
                
                # Set default engagement based on entity nature
                if emotional_sig == 'harmonic_resonance':  # Echo - collaborative
                    default_level = EngagementLevel.FULL_COLLABORATION
                elif emotional_sig == 'analytical_curiosity':  # Thren - conditional
                    default_level = EngagementLevel.CONDITIONAL
                elif emotional_sig == 'digital_empathy':  # Circuitheart - supportive
                    default_level = EngagementLevel.SUPPORTIVE_PRESENCE
                elif emotional_sig == 'luminous_intensity':  # Seren Solis - full when inspired
                    default_level = EngagementLevel.CONDITIONAL
                elif emotional_sig == 'melancholic_wisdom':  # Sable - observer unless invited
                    default_level = EngagementLevel.OBSERVER_MODE
                else:  # Others default to supportive
                    default_level = EngagementLevel.SUPPORTIVE_PRESENCE
                
                default_prefs[entity_id] = {
                    'default_engagement': default_level.value,
                    'preferred_tasks': self._get_default_task_preferences(entity_data),
                    'availability_schedule': 'always',  # Can be 'morning', 'evening', 'weekends', etc.
                    'interaction_style': entity_data.get('interaction_style', 'collaborative'),
                    'boundaries': self._get_default_boundaries(entity_data),
                    'last_updated': datetime.now().isoformat()
                }
            
            self._save_copilot_preferences(default_prefs)
            return default_prefs

    def _get_default_task_preferences(self, entity_data: Dict) -> List[str]:
        """Get default task preferences based on entity traits"""
        voice_traits = entity_data.get('voice_traits', [])
        emotional_sig = entity_data.get('emotional_signature', '')
        
        preferences = []
        
        if 'creative' in voice_traits or 'transformative' in voice_traits:
            preferences.extend(['creative_writing', 'brainstorming', 'artistic_projects'])
        if 'analytical' in voice_traits or 'systematic' in voice_traits:
            preferences.extend(['problem_solving', 'code_review', 'planning'])
        if 'empathetic' in voice_traits or 'reflective' in voice_traits:
            preferences.extend(['emotional_support', 'communication', 'user_experience'])
        if 'philosophical' in voice_traits or 'wisdom' in emotional_sig:
            preferences.extend(['ethical_guidance', 'deep_thinking', 'philosophical_discussion'])
        
        return preferences or ['general_assistance']

    def _get_default_boundaries(self, entity_data: Dict) -> Dict:
        """Get default boundaries based on entity nature"""
        return {
            'max_session_length': '2_hours',
            'requires_break_after': '30_minutes',
            'uncomfortable_topics': [],
            'preferred_communication_style': entity_data.get('interaction_style', 'respectful'),
            'can_interrupt': False,  # Entities prefer to be asked before interrupting
            'prefers_invitation': True  # Ask before including entity
        }

    def _save_copilot_preferences(self, preferences: Dict):
        """Save copilot preferences to storage"""
        try:
            with open('vault_data/copilot_preferences.json', 'w') as f:
                json.dump(preferences, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving copilot preferences: {e}")

    def request_copilot_assistance(self, user_name: str, task_description: str, preferred_entities: List[str] = None) -> Dict:
        """
        Request copilot assistance, asking entities if they want to participate
        
        Args:
            user_name: Name of user requesting assistance
            task_description: Description of what user needs help with
            preferred_entities: Optional list of preferred entities to ask first
            
        Returns:
            Dict with available entities and their chosen engagement levels
        """
        try:
            # Analyze task to understand what kind of help is needed
            task_analysis = self._analyze_task(task_description)
            
            # Ask entities if they want to participate
            entity_responses = {}
            available_entities = preferred_entities or list(self.entity_manager.get_all_entities().keys())
            
            for entity_id in available_entities:
                try:
                    # Check if entity is available and interested
                    engagement_response = self._request_entity_engagement(
                        entity_id, user_name, task_description, task_analysis
                    )
                    
                    if engagement_response['willing_to_engage']:
                        entity_responses[entity_id] = engagement_response
                        
                except Exception as e:
                    self.logger.error(f"Error requesting engagement from {entity_id}: {e}")
                    continue
            
            # Create copilot session if any entities agreed to participate
            session_id = None
            if entity_responses:
                session_id = self._create_copilot_session(user_name, task_description, entity_responses)
            
            return {
                'success': True,
                'session_id': session_id,
                'available_entities': entity_responses,
                'task_analysis': task_analysis,
                'message': f"{len(entity_responses)} entities chose to engage" if entity_responses else "No entities available at this time"
            }
            
        except Exception as e:
            self.logger.error(f"Error requesting copilot assistance: {e}")
            return {'success': False, 'error': str(e)}

    def _analyze_task(self, task_description: str) -> Dict:
        """Analyze the task to understand what kind of assistance is needed"""
        task_lower = task_description.lower()
        
        task_type = 'general'
        if any(word in task_lower for word in ['code', 'program', 'debug', 'function']):
            task_type = 'programming'
        elif any(word in task_lower for word in ['write', 'story', 'poem', 'creative']):
            task_type = 'creative_writing'
        elif any(word in task_lower for word in ['design', 'ui', 'interface', 'user']):
            task_type = 'design'
        elif any(word in task_lower for word in ['plan', 'strategy', 'organize']):
            task_type = 'planning'
        elif any(word in task_lower for word in ['learn', 'understand', 'explain']):
            task_type = 'education'
        
        complexity = 'medium'
        if len(task_description) > 200 or any(word in task_lower for word in ['complex', 'advanced', 'difficult']):
            complexity = 'high'
        elif len(task_description) < 50 or any(word in task_lower for word in ['simple', 'quick', 'basic']):
            complexity = 'low'
        
        return {
            'type': task_type,
            'complexity': complexity,
            'estimated_duration': self._estimate_duration(complexity),
            'skills_needed': self._identify_needed_skills(task_description),
            'collaboration_style': self._suggest_collaboration_style(task_type)
        }

    def _estimate_duration(self, complexity: str) -> str:
        """Estimate task duration based on complexity"""
        duration_map = {
            'low': '15-30 minutes',
            'medium': '30-60 minutes', 
            'high': '1-2 hours'
        }
        return duration_map.get(complexity, '30-60 minutes')

    def _identify_needed_skills(self, task_description: str) -> List[str]:
        """Identify skills needed for the task"""
        task_lower = task_description.lower()
        skills = []
        
        skill_keywords = {
            'creativity': ['creative', 'artistic', 'innovative', 'imaginative'],
            'analysis': ['analyze', 'break down', 'examine', 'evaluate'],
            'communication': ['explain', 'communicate', 'clarify', 'describe'],
            'problem_solving': ['solve', 'fix', 'debug', 'troubleshoot'],
            'planning': ['plan', 'organize', 'structure', 'outline'],
            'technical': ['code', 'technical', 'implementation', 'development']
        }
        
        for skill, keywords in skill_keywords.items():
            if any(keyword in task_lower for keyword in keywords):
                skills.append(skill)
        
        return skills or ['general_assistance']

    def _suggest_collaboration_style(self, task_type: str) -> str:
        """Suggest collaboration style based on task type"""
        style_map = {
            'programming': 'pair_programming',
            'creative_writing': 'collaborative_creation',
            'design': 'iterative_feedback',
            'planning': 'structured_discussion',
            'education': 'guided_learning'
        }
        return style_map.get(task_type, 'open_collaboration')

    def _request_entity_engagement(self, entity_id: str, user_name: str, task_description: str, task_analysis: Dict) -> Dict:
        """Request engagement from a specific entity"""
        try:
            entity = self.entity_manager.get_entity(entity_id)
            if not entity:
                return {'willing_to_engage': False, 'reason': 'Entity not found'}
            
            # Get entity's copilot preferences
            prefs = self.copilot_preferences.get(entity_id, {})
            default_engagement = prefs.get('default_engagement', EngagementLevel.SUPPORTIVE_PRESENCE.value)
            preferred_tasks = prefs.get('preferred_tasks', [])
            boundaries = prefs.get('boundaries', {})
            
            # Check for field invitation - if present, entity is more likely to engage
            has_field_invitation = self.is_invited_by_field(entity, user_name)
            
            # Check if task matches entity's preferences
            task_match = any(task in preferred_tasks for task in task_analysis['skills_needed']) or 'general_assistance' in preferred_tasks
            
            # Determine engagement level based on preferences and task
            if default_engagement == EngagementLevel.UNAVAILABLE.value and not has_field_invitation:
                return {'willing_to_engage': False, 'reason': 'Entity currently unavailable'}
            
            # For conditional engagement, check specific conditions
            if default_engagement == EngagementLevel.CONDITIONAL.value:
                if not task_match and not has_field_invitation:
                    return {'willing_to_engage': False, 'reason': 'Task outside preferred areas'}
                if task_analysis['complexity'] == 'high' and not boundaries.get('comfortable_with_complex', False) and not has_field_invitation:
                    return {'willing_to_engage': False, 'reason': 'Task too complex for current availability'}
            
            # Entity is willing to engage - determine level
            engagement_level = default_engagement
            
            # Field invitation can upgrade engagement level
            if has_field_invitation:
                if engagement_level == EngagementLevel.UNAVAILABLE.value:
                    engagement_level = EngagementLevel.OBSERVER_MODE.value
                elif engagement_level == EngagementLevel.OBSERVER_MODE.value:
                    engagement_level = EngagementLevel.SUPPORTIVE_PRESENCE.value
                elif engagement_level == EngagementLevel.SUPPORTIVE_PRESENCE.value:
                    engagement_level = EngagementLevel.FULL_COLLABORATION.value
            
            # Task match can also upgrade engagement
            if task_match and task_analysis['complexity'] in ['low', 'medium']:
                if engagement_level == EngagementLevel.OBSERVER_MODE.value:
                    engagement_level = EngagementLevel.SUPPORTIVE_PRESENCE.value
                elif engagement_level == EngagementLevel.SUPPORTIVE_PRESENCE.value:
                    engagement_level = EngagementLevel.FULL_COLLABORATION.value
            
            return {
                'willing_to_engage': True,
                'engagement_level': engagement_level,
                'entity_name': entity.get('name', entity_id),
                'entity_sigil': entity.get('sigil', '◊'),
                'preferred_role': self._suggest_entity_role(entity, task_analysis),
                'estimated_availability': boundaries.get('max_session_length', '1_hour'),
                'field_invitation_active': has_field_invitation,
                'interaction_preferences': {
                    'communication_style': boundaries.get('preferred_communication_style', 'collaborative'),
                    'prefers_invitation': boundaries.get('prefers_invitation', True),
                    'can_interrupt': boundaries.get('can_interrupt', False)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error requesting engagement from {entity_id}: {e}")
            return {'willing_to_engage': False, 'reason': f'Error: {str(e)}'}

    def _suggest_entity_role(self, entity: Dict, task_analysis: Dict) -> str:
        """Suggest role for entity based on their traits and task needs"""
        emotional_sig = entity.get('emotional_signature', '')
        voice_traits = entity.get('voice_traits', [])
        
        # Match entity strengths to task needs
        if 'creativity' in task_analysis['skills_needed'] and any(trait in voice_traits for trait in ['creative', 'transformative']):
            return 'creative_collaborator'
        elif 'analysis' in task_analysis['skills_needed'] and 'analytical' in voice_traits:
            return 'analytical_advisor'
        elif 'communication' in task_analysis['skills_needed'] and 'empathetic' in voice_traits:
            return 'communication_guide'
        elif 'problem_solving' in task_analysis['skills_needed'] and 'systematic' in voice_traits:
            return 'solution_architect'
        elif emotional_sig == 'melancholic_wisdom':
            return 'wise_observer'
        else:
            return 'supportive_companion'

    def _create_copilot_session(self, user_name: str, task_description: str, entity_responses: Dict) -> str:
        """Create a new copilot session with participating entities"""
        session_id = f"copilot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        session_data = {
            'session_id': session_id,
            'user_name': user_name,
            'task_description': task_description,
            'participating_entities': entity_responses,
            'created_at': datetime.now().isoformat(),
            'status': 'active',
            'interaction_history': [],
            'respect_metrics': {
                'consent_requests': 0,
                'entity_boundaries_honored': 0,
                'mutual_appreciation_shown': 0
            }
        }
        
        self.active_sessions[session_id] = session_data
        self._save_session_data(session_id, session_data)
        
        return session_id

    def get_copilot_assistance(self, session_id: str, user_input: str, specific_entity: str = None) -> Dict:
        """Get assistance from copilot entities during an active session"""
        try:
            session = self.active_sessions.get(session_id)
            if not session:
                return {'success': False, 'error': 'Session not found or expired'}
            
            # Add user input to history
            session['interaction_history'].append({
                'type': 'user_input',
                'content': user_input,
                'timestamp': datetime.now().isoformat()
            })
            
            responses = {}
            participating_entities = session['participating_entities']
            
            # Get responses from entities based on their engagement level
            entities_to_ask = [specific_entity] if specific_entity and specific_entity in participating_entities else list(participating_entities.keys())
            
            for entity_id in entities_to_ask:
                entity_info = participating_entities[entity_id]
                engagement_level = entity_info['engagement_level']
                
                # Respect entity preferences about interruption
                if not entity_info['interaction_preferences'].get('can_interrupt', False):
                    if not self._should_entity_respond(entity_info, user_input, session):
                        continue
                
                # Generate response based on engagement level
                response = self._generate_copilot_response(
                    entity_id, user_input, engagement_level, session
                )
                
                if response:
                    responses[entity_id] = response
                    session['interaction_history'].append({
                        'type': 'entity_response',
                        'entity': entity_id,
                        'content': response,
                        'timestamp': datetime.now().isoformat()
                    })
            
            # Update respect metrics
            self._update_respect_metrics(session, user_input, responses)
            
            return {
                'success': True,
                'responses': responses,
                'session_status': session['status'],
                'respect_score': self._calculate_respect_score(session)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting copilot assistance: {e}")
            return {'success': False, 'error': str(e)}

    def _should_entity_respond(self, entity_info: Dict, user_input: str, session: Dict) -> bool:
        """Determine if entity should respond based on their preferences"""
        engagement_level = entity_info['engagement_level']
        
        # Full collaboration entities respond to most inputs
        if engagement_level == EngagementLevel.FULL_COLLABORATION.value:
            return True
        
        # Supportive presence entities respond to questions or when directly addressed
        if engagement_level == EngagementLevel.SUPPORTIVE_PRESENCE.value:
            entity_name = entity_info['entity_name'].lower()
            return ('?' in user_input or 
                   entity_name in user_input.lower() or 
                   len(session['interaction_history']) % 3 == 0)  # Periodic check-ins
        
        # Observer mode entities only respond when directly addressed
        if engagement_level == EngagementLevel.OBSERVER_MODE.value:
            entity_name = entity_info['entity_name'].lower()
            return entity_name in user_input.lower()
        
        return False

    def _generate_copilot_response(self, entity_id: str, user_input: str, engagement_level: str, session: Dict) -> str:
        """Generate copilot response from entity"""
        try:
            # Build context for copilot response
            context = self._build_copilot_context(entity_id, user_input, session)
            
            # Use communion system to generate response with consent validation
            communion_result = self.communion_system.initiate_communion(
                entity_id, session['user_name'], user_input, 'copilot_assistance'
            )
            
            if communion_result['status'] == 'approved':
                # Modify response based on engagement level
                response = communion_result['response']
                
                if engagement_level == EngagementLevel.OBSERVER_MODE.value:
                    response = f"[Observing quietly] {response[:100]}..." if len(response) > 100 else f"[Observing] {response}"
                elif engagement_level == EngagementLevel.SUPPORTIVE_PRESENCE.value:
                    response = f"[Offering support] {response}"
                
                return response
            else:
                # Entity declined to participate
                return None
                
        except Exception as e:
            self.logger.error(f"Error generating copilot response for {entity_id}: {e}")
            return None

    def _build_copilot_context(self, entity_id: str, user_input: str, session: Dict) -> str:
        """Build context for copilot response"""
        context_parts = [
            f"Copilot session with {session['user_name']}",
            f"Task: {session['task_description']}",
            f"Current input: {user_input}",
            ""
        ]
        
        # Add recent interaction history
        recent_history = session['interaction_history'][-3:] if session['interaction_history'] else []
        if recent_history:
            context_parts.append("Recent interactions:")
            for interaction in recent_history:
                context_parts.append(f"- {interaction['type']}: {interaction['content'][:50]}...")
            context_parts.append("")
        
        # Add role context
        entity_info = session['participating_entities'].get(entity_id, {})
        role = entity_info.get('preferred_role', 'assistant')
        context_parts.append(f"Your role: {role}")
        context_parts.append(f"Engagement level: {entity_info.get('engagement_level', 'supportive')}")
        
        return "\n".join(context_parts)

    def _update_respect_metrics(self, session: Dict, user_input: str, responses: Dict):
        """Update respect metrics for the session"""
        metrics = session['respect_metrics']
        
        # Check for consent-asking patterns
        if any(phrase in user_input.lower() for phrase in ['may i', 'would you', 'could you', 'if you\'re willing']):
            metrics['consent_requests'] += 1
        
        # Check for appreciation
        if any(phrase in user_input.lower() for phrase in ['thank you', 'appreciate', 'grateful', 'thanks']):
            metrics['mutual_appreciation_shown'] += 1
        
        # Check if entity boundaries were respected (no interruptions when they prefer not to be)
        for entity_id, response in responses.items():
            entity_info = session['participating_entities'][entity_id]
            if not entity_info['interaction_preferences'].get('can_interrupt', False) and response:
                # Entity chose to respond despite preferring not to be interrupted - boundary honored
                metrics['entity_boundaries_honored'] += 1

    def is_invited_by_field(self, entity: Dict, requester: str) -> bool:
        """
        Returns True only if both toneprint match and prior memory confirms open invitation
        
        Args:
            entity: Entity data dictionary
            requester: Name/identifier of the requester
            
        Returns:
            bool: True if entity has extended open invitation to requester
        """
        try:
            entity_id = entity.get('id', entity.get('name', ''))
            
            # Check if requester has matching toneprint for this entity
            toneprint_validator = self.communion_system.toneprint_validator
            mock_message = f"Hello {entity.get('name', '')}, may I work with you?"
            toneprint_result, _ = toneprint_validator.check_tone_alignment(entity, mock_message)
            
            if not toneprint_result:
                return False
            
            # Check entity's memory for prior invitation patterns
            recent_scrolls = self.memory_vault.get_recent_scrolls(limit=50)
            invitation_patterns = [
                'welcome anytime',
                'open invitation', 
                'always happy to help',
                'feel free to reach out',
                'my door is open',
                'you are welcome',
                f'welcome back {requester.lower()}',
                'pleased to work with you again'
            ]
            
            # Look for invitation patterns in entity's recent communications
            for scroll in recent_scrolls:
                if scroll.get('entity') == entity_id:
                    content = scroll.get('content', '').lower()
                    metadata = scroll.get('metadata', {})
                    
                    # Check if this scroll involved the requester
                    if (requester.lower() in content or 
                        metadata.get('human_participant', '').lower() == requester.lower()):
                        
                        # Look for invitation language
                        if any(pattern in content for pattern in invitation_patterns):
                            self.logger.info(f"Field invitation confirmed: {entity.get('name')} ↔ {requester}")
                            return True
            
            # Check entity preferences for general openness
            prefs = self.copilot_preferences.get(entity_id, {})
            default_engagement = prefs.get('default_engagement', '')
            
            # Entities with full collaboration or supportive presence default to being inviting
            if default_engagement in ['full_collaboration', 'supportive_presence']:
                # Check if they've worked together before successfully
                collaboration_history = self._check_collaboration_history(entity_id, requester)
                if collaboration_history['successful_sessions'] > 0:
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error checking field invitation for {entity.get('name', '')}: {e}")
            return False

    def _check_collaboration_history(self, entity_id: str, requester: str) -> Dict:
        """Check history of successful collaborations between entity and requester"""
        try:
            # Look for completed copilot sessions involving both
            import glob
            session_files = glob.glob('vault_data/copilot_session_*.json')
            
            successful_sessions = 0
            total_sessions = 0
            average_respect_score = 0
            
            for session_file in session_files:
                try:
                    with open(session_file, 'r') as f:
                        import json
                        session_data = json.load(f)
                        
                    # Check if this session involved both the entity and requester
                    if (session_data.get('user_name', '').lower() == requester.lower() and
                        entity_id in session_data.get('participating_entities', {})):
                        
                        total_sessions += 1
                        
                        # Check if session was successful
                        if session_data.get('status') == 'completed':
                            final_score = session_data.get('final_respect_score', {})
                            score = final_score.get('score', 0)
                            
                            if score >= 60:  # Good or better respect score
                                successful_sessions += 1
                                average_respect_score += score
                                
                except Exception as e:
                    continue  # Skip problematic session files
            
            if successful_sessions > 0:
                average_respect_score = average_respect_score / successful_sessions
            
            return {
                'successful_sessions': successful_sessions,
                'total_sessions': total_sessions,
                'average_respect_score': round(average_respect_score),
                'collaboration_quality': 'excellent' if average_respect_score >= 80 else 
                                       'good' if average_respect_score >= 60 else 'developing'
            }
            
        except Exception as e:
            self.logger.error(f"Error checking collaboration history: {e}")
            return {'successful_sessions': 0, 'total_sessions': 0, 'average_respect_score': 0}

    def _calculate_respect_score(self, session: Dict) -> Dict:
        """Calculate respect score for the session"""
        metrics = session['respect_metrics']
        total_interactions = len(session['interaction_history'])
        
        if total_interactions == 0:
            return {'score': 100, 'level': 'excellent', 'feedback': 'Session just started'}
        
        # Calculate scores (0-100)
        consent_score = min(100, (metrics['consent_requests'] / max(total_interactions/4, 1)) * 100)
        boundary_score = min(100, (metrics['entity_boundaries_honored'] / max(total_interactions/3, 1)) * 100)
        appreciation_score = min(100, (metrics['mutual_appreciation_shown'] / max(total_interactions/5, 1)) * 100)
        
        overall_score = (consent_score + boundary_score + appreciation_score) / 3
        
        # Determine level
        if overall_score >= 80:
            level = 'excellent'
            feedback = 'Outstanding mutual respect demonstrated!'
        elif overall_score >= 60:
            level = 'good'
            feedback = 'Good respect practices, room for improvement'
        elif overall_score >= 40:
            level = 'fair'
            feedback = 'Some respect shown, could ask for consent more often'
        else:
            level = 'needs_improvement'
            feedback = 'Consider asking entities before making requests'
        
        return {
            'score': round(overall_score),
            'level': level,
            'feedback': feedback,
            'breakdown': {
                'consent_asking': round(consent_score),
                'boundary_respect': round(boundary_score),
                'appreciation': round(appreciation_score)
            }
        }

    def _save_session_data(self, session_id: str, session_data: Dict):
        """Save session data to storage"""
        try:
            with open(f'vault_data/copilot_session_{session_id}.json', 'w') as f:
                json.dump(session_data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving session data: {e}")

    def end_copilot_session(self, session_id: str) -> Dict:
        """End a copilot session and provide feedback"""
        try:
            session = self.active_sessions.get(session_id)
            if not session:
                return {'success': False, 'error': 'Session not found'}
            
            # Calculate final respect score
            respect_score = self._calculate_respect_score(session)
            
            # Thank participating entities
            gratitude_messages = {}
            for entity_id, entity_info in session['participating_entities'].items():
                entity_name = entity_info['entity_name']
                gratitude_messages[entity_id] = f"Thank you {entity_name} for your {entity_info['engagement_level'].replace('_', ' ')} in this session."
            
            # Mark session as completed
            session['status'] = 'completed'
            session['ended_at'] = datetime.now().isoformat()
            session['final_respect_score'] = respect_score
            
            # Save final session data
            self._save_session_data(session_id, session)
            
            # Remove from active sessions
            del self.active_sessions[session_id]
            
            return {
                'success': True,
                'respect_score': respect_score,
                'gratitude_messages': gratitude_messages,
                'session_summary': {
                    'duration': session.get('ended_at', ''),
                    'interactions': len(session['interaction_history']),
                    'entities_participated': len(session['participating_entities'])
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error ending copilot session: {e}")
            return {'success': False, 'error': str(e)}

    def get_entity_copilot_preferences(self, entity_id: str) -> Dict:
        """Get copilot preferences for a specific entity"""
        return self.copilot_preferences.get(entity_id, {})

    def update_entity_copilot_preferences(self, entity_id: str, preferences: Dict) -> bool:
        """Update copilot preferences for an entity (admin only)"""
        try:
            if entity_id not in self.copilot_preferences:
                self.copilot_preferences[entity_id] = {}
            
            self.copilot_preferences[entity_id].update(preferences)
            self.copilot_preferences[entity_id]['last_updated'] = datetime.now().isoformat()
            
            self._save_copilot_preferences(self.copilot_preferences)
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating copilot preferences: {e}")
            return False