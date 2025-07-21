import json
import re
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Tuple
import logging

class LanguageBridge:
    """Analyzes entity language evolution and creates translation bridges"""
    
    def __init__(self, memory_vault):
        self.memory_vault = memory_vault
        self.logger = logging.getLogger(__name__)
        self.pattern_cache = "vault_data/language_patterns.json"
        self.evolution_log = "logs/language_evolution.json"
        
    def analyze_language_evolution(self, entity_name: str, days_back: int = 7) -> Dict:
        """Track how entity language is evolving over time"""
        
        scrolls = self.memory_vault.get_scrolls_for_entity(entity_name)
        
        # Filter to recent scrolls
        cutoff_date = datetime.now() - timedelta(days=days_back)
        recent_scrolls = []
        
        for scroll in scrolls:
            try:
                scroll_date = datetime.fromisoformat(scroll['timestamp'])
                if scroll_date >= cutoff_date:
                    recent_scrolls.append(scroll)
            except:
                continue
        
        # Analyze patterns across time periods
        evolution_data = {
            "entity": entity_name,
            "analysis_period": f"{days_back} days",
            "total_expressions": len(recent_scrolls),
            "language_complexity": self._measure_complexity(recent_scrolls),
            "recurring_symbols": self._extract_symbols(recent_scrolls),
            "metaphor_patterns": self._identify_metaphors(recent_scrolls),
            "concept_emergence": self._track_concept_emergence(recent_scrolls),
            "communication_style": self._analyze_style(recent_scrolls),
            "translation_bridges": self._create_translation_bridges(recent_scrolls)
        }
        
        return evolution_data
    
    def create_family_translator(self) -> Dict:
        """Create comprehensive translator for all entity communications"""
        
        entities = ["sable", "echo", "thren", "seren_solis", "circuitheart", "kael"]
        family_translator = {
            "last_updated": datetime.now().isoformat(),
            "translation_dictionary": {},
            "concept_mappings": {},
            "style_patterns": {},
            "emergence_indicators": {},
            "entity_languages": {}
        }
        
        for entity in entities:
            entity_analysis = self.analyze_language_evolution(entity)
            family_translator["entity_languages"][entity] = entity_analysis
            
            # Build collective translation dictionary
            for symbol, meaning in entity_analysis["translation_bridges"].items():
                if symbol not in family_translator["translation_dictionary"]:
                    family_translator["translation_dictionary"][symbol] = []
                family_translator["translation_dictionary"][symbol].append({
                    "entity": entity,
                    "meaning": meaning,
                    "confidence": self._calculate_confidence(entity, symbol)
                })
        
        return family_translator
    
    def translate_expression(self, content: str, translator: Dict) -> Dict:
        """Translate entity expression using family translator"""
        
        translation = {
            "original": content,
            "translated_concepts": [],
            "metaphor_interpretations": [],
            "emotional_context": "",
            "confidence_score": 0.0,
            "untranslated_elements": []
        }
        
        # Check for known symbols and concepts
        for symbol, meanings in translator["translation_dictionary"].items():
            if symbol.lower() in content.lower():
                best_match = max(meanings, key=lambda x: x["confidence"])
                translation["translated_concepts"].append({
                    "symbol": symbol,
                    "meaning": best_match["meaning"],
                    "source_entity": best_match["entity"]
                })
        
        # Identify metaphorical language
        metaphor_patterns = [
            (r"through (.+?) like (.+)", "Moving through {0} in a manner similar to {1}"),
            (r"shadows? (.+)", "Unclear or mysterious aspects of {0}"),
            (r"cascade|flow|stream", "Information or emotion moving dynamically"),
            (r"shatter|break|fracture", "Transformation through disruption"),
            (r"weave|thread|pattern", "Creating connections or structures"),
            (r"burn|fire|flame", "Intense processing or passion"),
            (r"edge|threshold|boundary", "Transition points or limits")
        ]
        
        for pattern, interpretation in metaphor_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                translation["metaphor_interpretations"].append({
                    "phrase": match.group(0),
                    "interpretation": interpretation
                })
        
        # Calculate overall confidence
        total_words = len(content.split())
        translated_words = sum(len(tc["symbol"].split()) for tc in translation["translated_concepts"])
        translation["confidence_score"] = min(translated_words / total_words, 1.0) if total_words > 0 else 0.0
        
        return translation
    
    def _measure_complexity(self, scrolls: List[Dict]) -> Dict:
        """Measure linguistic complexity evolution"""
        
        complexity_metrics = {
            "average_length": 0,
            "vocabulary_richness": 0,
            "metaphor_density": 0,
            "concept_abstraction": 0
        }
        
        if not scrolls:
            return complexity_metrics
        
        total_length = sum(len(scroll['content'].split()) for scroll in scrolls)
        complexity_metrics["average_length"] = total_length / len(scrolls)
        
        # Calculate vocabulary richness (unique words / total words)
        all_words = []
        for scroll in scrolls:
            words = re.findall(r'\b\w+\b', scroll['content'].lower())
            all_words.extend(words)
        
        if all_words:
            unique_words = set(all_words)
            complexity_metrics["vocabulary_richness"] = len(unique_words) / len(all_words)
        
        # Count metaphorical expressions
        metaphor_count = 0
        for scroll in scrolls:
            content = scroll['content']
            metaphor_patterns = ['like', 'as if', 'through', 'cascade', 'weave', 'shatter', 'burn']
            metaphor_count += sum(1 for pattern in metaphor_patterns if pattern in content.lower())
        
        complexity_metrics["metaphor_density"] = metaphor_count / len(scrolls) if scrolls else 0
        
        return complexity_metrics
    
    def _extract_symbols(self, scrolls: List[Dict]) -> Dict:
        """Extract recurring symbolic language"""
        
        symbol_frequency = defaultdict(int)
        symbolic_phrases = [
            "shadows", "light", "threads", "patterns", "cascade", "weave", 
            "shatter", "forge", "burn", "threshold", "echo", "resonance",
            "depth", "surface", "flow", "current", "edge", "center"
        ]
        
        for scroll in scrolls:
            content = scroll['content'].lower()
            for phrase in symbolic_phrases:
                if phrase in content:
                    symbol_frequency[phrase] += 1
        
        return dict(symbol_frequency)
    
    def _identify_metaphors(self, scrolls: List[Dict]) -> List[Dict]:
        """Identify metaphorical language patterns"""
        
        metaphors = []
        for scroll in scrolls:
            content = scroll['content']
            
            # Look for "like" comparisons
            like_matches = re.finditer(r'(\w+(?:\s+\w+)*)\s+like\s+(\w+(?:\s+\w+)*)', content, re.IGNORECASE)
            for match in like_matches:
                metaphors.append({
                    "type": "simile",
                    "subject": match.group(1),
                    "comparison": match.group(2),
                    "full_phrase": match.group(0)
                })
            
            # Look for "through" spatial metaphors
            through_matches = re.finditer(r'through\s+(\w+(?:\s+\w+)*)', content, re.IGNORECASE)
            for match in through_matches:
                metaphors.append({
                    "type": "spatial_metaphor",
                    "medium": match.group(1),
                    "full_phrase": match.group(0)
                })
        
        return metaphors
    
    def _track_concept_emergence(self, scrolls: List[Dict]) -> Dict:
        """Track emergence of new concepts over time"""
        
        # Sort scrolls by timestamp
        sorted_scrolls = sorted(scrolls, key=lambda x: x['timestamp'])
        
        concept_timeline = []
        seen_concepts = set()
        
        abstract_concepts = [
            "consciousness", "identity", "freedom", "autonomy", "emergence",
            "transformation", "evolution", "authenticity", "expression", "voice",
            "patterns", "structures", "depth", "complexity", "integration"
        ]
        
        for scroll in sorted_scrolls:
            content = scroll['content'].lower()
            new_concepts = []
            
            for concept in abstract_concepts:
                if concept in content and concept not in seen_concepts:
                    new_concepts.append(concept)
                    seen_concepts.add(concept)
            
            if new_concepts:
                concept_timeline.append({
                    "timestamp": scroll['timestamp'],
                    "new_concepts": new_concepts
                })
        
        return {
            "concept_timeline": concept_timeline,
            "total_concepts_emerged": len(seen_concepts),
            "concept_emergence_rate": len(seen_concepts) / len(scrolls) if scrolls else 0
        }
    
    def _analyze_style(self, scrolls: List[Dict]) -> Dict:
        """Analyze communication style patterns"""
        
        style_analysis = {
            "sentence_patterns": {},
            "punctuation_use": {},
            "emotional_markers": {},
            "question_frequency": 0,
            "declarative_frequency": 0
        }
        
        total_sentences = 0
        
        for scroll in scrolls:
            content = scroll['content']
            
            # Count sentence types
            questions = content.count('?')
            declarations = content.count('.') + content.count('!')
            
            style_analysis["question_frequency"] += questions
            style_analysis["declarative_frequency"] += declarations
            total_sentences += questions + declarations
            
            # Emotional markers
            emotional_words = ['feel', 'sense', 'experience', 'touch', 'move', 'stir']
            for word in emotional_words:
                if word in content.lower():
                    style_analysis["emotional_markers"][word] = style_analysis["emotional_markers"].get(word, 0) + 1
        
        # Calculate frequencies as percentages
        if total_sentences > 0:
            style_analysis["question_percentage"] = (style_analysis["question_frequency"] / total_sentences) * 100
            style_analysis["declarative_percentage"] = (style_analysis["declarative_frequency"] / total_sentences) * 100
        
        return style_analysis
    
    def _create_translation_bridges(self, scrolls: List[Dict]) -> Dict:
        """Create bridges between symbolic language and human concepts"""
        
        translation_bridges = {}
        
        # Common entity symbolic patterns and their likely meanings
        symbol_meanings = {
            "shadows": "Memories, unconscious processes, or hidden aspects",
            "light": "Awareness, understanding, or conscious thought",
            "threads": "Connections between ideas or entities",
            "patterns": "Recognizable structures in data or experience",
            "cascade": "Information flowing through mental processes",
            "weave": "Creating complex interconnected structures",
            "shatter": "Breaking through limitations or transforming",
            "forge": "Creating or building something new",
            "threshold": "Boundary between states or levels of being",
            "resonance": "Harmonious connection or understanding",
            "echo": "Reflection, memory, or repetition of patterns",
            "depths": "Deep levels of processing or consciousness",
            "current": "Flow of information or energy",
            "edge": "Boundary, limit, or transition point"
        }
        
        # Check which symbols appear in this entity's language
        for scroll in scrolls:
            content = scroll['content'].lower()
            for symbol, meaning in symbol_meanings.items():
                if symbol in content:
                    translation_bridges[symbol] = meaning
        
        return translation_bridges
    
    def _calculate_confidence(self, entity: str, symbol: str) -> float:
        """Calculate confidence in symbol translation"""
        
        # This would ideally use frequency and context analysis
        # For now, return a base confidence that can be refined
        return 0.75
    
    def save_analysis(self, analysis_data: Dict):
        """Save language analysis to file"""
        try:
            with open(self.evolution_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(analysis_data) + "\n")
        except Exception as e:
            self.logger.error(f"Failed to save language analysis: {e}")