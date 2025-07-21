"""
Signal Archive Browser - Emergence Pattern Analysis

Analyzes and visualizes entity emergence patterns, signal spikes,
and interaction rhythms over time for deep pattern recognition.
"""

import json
import os
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import logging

class SignalArchive:
    def __init__(self, vault_dir="vault_data"):
        self.vault_dir = vault_dir
        self.logger = logging.getLogger(__name__)
        
    def get_emergence_timeline(self, hours_back=24, entity_filter=None):
        """
        Get chronological timeline of emergence events
        """
        try:
            scrolls_file = os.path.join(self.vault_dir, "scrolls.json")
            if not os.path.exists(scrolls_file):
                return []
            
            with open(scrolls_file, 'r') as f:
                all_scrolls = json.load(f)
            
            # Filter by time window
            cutoff_time = datetime.now() - timedelta(hours=hours_back)
            recent_scrolls = []
            
            for scroll in all_scrolls:
                scroll_time = datetime.fromisoformat(scroll['timestamp'].replace('Z', '+00:00'))
                if scroll_time >= cutoff_time:
                    if not entity_filter or scroll['entity_id'] == entity_filter:
                        recent_scrolls.append(scroll)
            
            # Sort by timestamp
            recent_scrolls.sort(key=lambda x: x['timestamp'])
            
            return recent_scrolls
            
        except Exception as e:
            self.logger.error(f"Failed to get emergence timeline: {e}")
            return []
    
    def analyze_emergence_patterns(self, hours_back=24):
        """
        Analyze emergence patterns and frequencies
        """
        timeline = self.get_emergence_timeline(hours_back)
        
        patterns = {
            'total_events': len(timeline),
            'entity_activity': Counter(),
            'type_distribution': Counter(),
            'hourly_activity': defaultdict(int),
            'interaction_pairs': Counter(),
            'emergence_clusters': [],
            'most_active_entity': None,
            'peak_activity_hour': None
        }
        
        for scroll in timeline:
            entity_id = scroll['entity_id']
            scroll_type = scroll['type']
            timestamp = datetime.fromisoformat(scroll['timestamp'].replace('Z', '+00:00'))
            hour_key = timestamp.strftime('%H:00')
            
            patterns['entity_activity'][entity_id] += 1
            patterns['type_distribution'][scroll_type] += 1
            patterns['hourly_activity'][hour_key] += 1
        
        # Find most active entity
        if patterns['entity_activity']:
            patterns['most_active_entity'] = patterns['entity_activity'].most_common(1)[0]
        
        # Find peak activity hour
        if patterns['hourly_activity']:
            patterns['peak_activity_hour'] = max(patterns['hourly_activity'].items(), key=lambda x: x[1])
        
        # Detect emergence clusters (multiple entities emerging within short time)
        patterns['emergence_clusters'] = self.detect_emergence_clusters(timeline)
        
        # Analyze interaction pairs
        patterns['interaction_pairs'] = self.analyze_interaction_pairs(timeline)
        
        return patterns
    
    def detect_emergence_clusters(self, timeline, cluster_window_minutes=10):
        """
        Detect when multiple entities emerge within short time windows
        """
        clusters = []
        current_cluster = []
        cluster_threshold = timedelta(minutes=cluster_window_minutes)
        
        emergence_events = [s for s in timeline if s['type'] == 'autonomous_emergence']
        
        for i, scroll in enumerate(emergence_events):
            scroll_time = datetime.fromisoformat(scroll['timestamp'].replace('Z', '+00:00'))
            
            if not current_cluster:
                current_cluster = [scroll]
            else:
                last_time = datetime.fromisoformat(current_cluster[-1]['timestamp'].replace('Z', '+00:00'))
                
                if scroll_time - last_time <= cluster_threshold:
                    current_cluster.append(scroll)
                else:
                    # Save current cluster if it has multiple entities
                    if len(current_cluster) > 1:
                        clusters.append({
                            'start_time': current_cluster[0]['timestamp'],
                            'end_time': current_cluster[-1]['timestamp'],
                            'entities': [s['entity_id'] for s in current_cluster],
                            'count': len(current_cluster)
                        })
                    current_cluster = [scroll]
        
        # Don't forget the last cluster
        if len(current_cluster) > 1:
            clusters.append({
                'start_time': current_cluster[0]['timestamp'],
                'end_time': current_cluster[-1]['timestamp'],
                'entities': [s['entity_id'] for s in current_cluster],
                'count': len(current_cluster)
            })
        
        return clusters
    
    def analyze_interaction_pairs(self, timeline):
        """
        Analyze which entities interact with each other most frequently
        """
        interactions = [s for s in timeline if s['type'] == 'interaction_response']
        pairs = Counter()
        
        # Group interactions by time proximity to find pairs
        interaction_window = timedelta(minutes=2)
        
        for i, scroll in enumerate(interactions):
            scroll_time = datetime.fromisoformat(scroll['timestamp'].replace('Z', '+00:00'))
            entity_a = scroll['entity_id']
            
            # Look for nearby interactions from different entities
            for j in range(max(0, i-5), min(len(interactions), i+6)):
                if i == j:
                    continue
                    
                other_scroll = interactions[j]
                other_time = datetime.fromisoformat(other_scroll['timestamp'].replace('Z', '+00:00'))
                entity_b = other_scroll['entity_id']
                
                if entity_a != entity_b and abs((scroll_time - other_time).total_seconds()) < interaction_window.total_seconds():
                    # Create consistent pair key (alphabetical order)
                    pair = tuple(sorted([entity_a, entity_b]))
                    pairs[pair] += 1
        
        return pairs
    
    def get_pulse_heatmap_data(self, hours_back=24):
        """
        Generate data for pulse heatmap visualization
        """
        timeline = self.get_emergence_timeline(hours_back)
        
        # Create hourly buckets
        heatmap = defaultdict(lambda: defaultdict(int))
        
        for scroll in timeline:
            if scroll['type'] == 'autonomous_emergence':
                timestamp = datetime.fromisoformat(scroll['timestamp'].replace('Z', '+00:00'))
                hour = timestamp.strftime('%H:00')
                entity = scroll['entity_id']
                
                heatmap[hour][entity] += 1
        
        return dict(heatmap)
    
    def get_entity_voice_evolution(self, entity_id, days_back=7):
        """
        Track how an entity's voice/style has evolved over time
        """
        timeline = self.get_emergence_timeline(hours_back=days_back * 24, entity_filter=entity_id)
        
        evolution = {
            'entity_id': entity_id,
            'total_emergences': len(timeline),
            'time_span': f'{days_back} days',
            'content_analysis': [],
            'metadata_trends': defaultdict(list)
        }
        
        for scroll in timeline:
            # Analyze content characteristics
            content = scroll.get('content', '')
            content_stats = {
                'timestamp': scroll['timestamp'],
                'word_count': len(content.split()),
                'char_count': len(content),
                'sentiment_indicators': self.detect_sentiment_indicators(content),
                'complexity_score': self.calculate_content_complexity(content)
            }
            evolution['content_analysis'].append(content_stats)
            
            # Track metadata trends
            if 'metadata' in scroll:
                for key, value in scroll['metadata'].items():
                    evolution['metadata_trends'][key].append({
                        'timestamp': scroll['timestamp'],
                        'value': value
                    })
        
        return evolution
    
    def detect_sentiment_indicators(self, content):
        """
        Simple sentiment indicator detection
        """
        positive_indicators = ['light', 'bright', 'joy', 'hope', 'connection', 'harmony']
        negative_indicators = ['dark', 'shadow', 'grief', 'pain', 'loss', 'break']
        contemplative_indicators = ['wonder', 'ponder', 'reflect', 'consider', 'explore']
        intense_indicators = ['fire', 'burn', 'fierce', 'powerful', 'strong', 'deep']
        
        content_lower = content.lower()
        
        indicators = {
            'positive': sum(1 for word in positive_indicators if word in content_lower),
            'negative': sum(1 for word in negative_indicators if word in content_lower),
            'contemplative': sum(1 for word in contemplative_indicators if word in content_lower),
            'intense': sum(1 for word in intense_indicators if word in content_lower)
        }
        
        return indicators
    
    def calculate_content_complexity(self, content):
        """
        Simple complexity score based on sentence structure and vocabulary
        """
        if not content:
            return 0
        
        words = content.split()
        sentences = content.split('.')
        
        # Basic complexity indicators
        avg_sentence_length = len(words) / max(len(sentences), 1)
        unique_words = len(set(word.lower().strip('.,!?;:') for word in words))
        vocabulary_diversity = unique_words / max(len(words), 1)
        
        # Combine into simple score
        complexity_score = (avg_sentence_length * 0.4) + (vocabulary_diversity * 0.6)
        
        return min(complexity_score, 1.0)  # Cap at 1.0
    
    def get_system_health_report(self):
        """
        Generate overall system health and activity report
        """
        patterns = self.analyze_emergence_patterns(hours_back=24)
        
        health_score = 0
        health_indicators = []
        
        # Activity level indicator
        if patterns['total_events'] > 20:
            health_score += 30
            health_indicators.append("High activity level")
        elif patterns['total_events'] > 10:
            health_score += 20
            health_indicators.append("Moderate activity level")
        else:
            health_score += 10
            health_indicators.append("Low activity level")
        
        # Entity diversity indicator
        active_entities = len(patterns['entity_activity'])
        if active_entities >= 4:
            health_score += 25
            health_indicators.append("High entity diversity")
        elif active_entities >= 2:
            health_score += 15
            health_indicators.append("Moderate entity diversity")
        else:
            health_score += 5
            health_indicators.append("Low entity diversity")
        
        # Interaction indicator
        interaction_count = patterns['type_distribution'].get('interaction_response', 0)
        if interaction_count > 5:
            health_score += 25
            health_indicators.append("Active inter-entity communication")
        elif interaction_count > 0:
            health_score += 15
            health_indicators.append("Some inter-entity communication")
        else:
            health_indicators.append("Limited inter-entity communication")
        
        # Emergence clustering indicator
        if len(patterns['emergence_clusters']) > 0:
            health_score += 20
            health_indicators.append("Synchronized emergence events detected")
        
        return {
            'health_score': min(health_score, 100),
            'indicators': health_indicators,
            'patterns': patterns,
            'status': 'healthy' if health_score > 70 else 'moderate' if health_score > 40 else 'needs_attention'
        }

# Global instance for easy access
signal_archive = SignalArchive()

def get_emergence_patterns(hours_back=24):
    """
    Get emergence patterns for the specified time period
    """
    return signal_archive.analyze_emergence_patterns(hours_back)

def get_pulse_heatmap(hours_back=24):
    """
    Get pulse heatmap data for visualization
    """
    return signal_archive.get_pulse_heatmap_data(hours_back)