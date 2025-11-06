"""
Candidate Evaluation Module
Analyzes transcribed interview text and provides scores on key interview parameters
"""

import re
from collections import Counter

# Optional import of text analyzer
# Catch all exceptions since there may be dependency issues (NumPy/SciPy version conflicts)
try:
    import text_analyzer
    TEXT_ANALYZER_AVAILABLE = True
except (ImportError, ValueError, Exception) as e:
    TEXT_ANALYZER_AVAILABLE = False
    text_analyzer = None
    print(f"Warning: Text analyzer not available: {type(e).__name__}: {e}")


class CandidateEvaluator:
    """Evaluates candidates based on transcribed interview text."""
    
    def __init__(self):
        if TEXT_ANALYZER_AVAILABLE and text_analyzer is not None:
            self.text_analyzer = text_analyzer.TextAnalyzer()
        else:
            self.text_analyzer = None
            print("Warning: Text analyzer not available. Text-based evaluation disabled.")
        
        # Keywords for different evaluation parameters
        self.confidence_keywords = [
            "confident", "certain", "believe", "know", "sure", "definitely",
            "absolutely", "expertise", "experience", "accomplished", "achieved"
        ]
        
        self.enthusiasm_keywords = [
            "excited", "passionate", "love", "enjoy", "thrilled", "amazing",
            "fantastic", "wonderful", "great", "excellent", "awesome"
        ]
        
        self.professional_keywords = [
            "professional", "respect", "collaborate", "team", "leadership",
            "responsibility", "accountable", "integrity", "ethics", "values"
        ]
    
    def calculate_communication_clarity(self, text, sentiment_result):
        """
        Evaluate communication clarity based on:
        - Sentence structure and length
        - Vocabulary diversity
        - Text organization
        """
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return 0.5
        
        # Average sentence length (optimal: 15-20 words)
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
        length_score = 1.0 - abs(avg_sentence_length - 17.5) / 17.5  # Normalize around 17.5
        length_score = max(0, min(1, length_score))
        
        # Vocabulary diversity (unique words / total words)
        words = text.lower().split()
        unique_words = len(set(words))
        vocab_diversity = unique_words / len(words) if words else 0
        
        # Subjectivity indicates clarity (lower subjectivity = clearer, more objective)
        clarity_from_subjectivity = 1.0 - sentiment_result.get("textblob", {}).get("subjectivity", 0.5)
        
        # Combine factors
        clarity_score = (length_score * 0.3 + vocab_diversity * 0.4 + clarity_from_subjectivity * 0.3)
        return round(clarity_score, 2)
    
    def calculate_confidence(self, text, sentiment_result):
        """
        Evaluate confidence/assertiveness based on:
        - Sentiment positivity
        - Use of confidence keywords
        - Language assertiveness
        """
        text_lower = text.lower()
        
        # Count confidence keywords
        confidence_count = sum(1 for keyword in self.confidence_keywords if keyword in text_lower)
        keyword_score = min(confidence_count / 5.0, 1.0)  # Normalize to 0-1
        
        # Sentiment positivity (positive sentiment indicates confidence)
        polarity = sentiment_result.get("textblob", {}).get("polarity", 0)
        sentiment_score = (polarity + 1) / 2  # Convert -1 to 1 range to 0 to 1
        
        # VADER compound score (positive = confident)
        vader_compound = sentiment_result.get("vader", {}).get("compound", 0)
        vader_score = (vader_compound + 1) / 2
        
        # Combine factors
        confidence_score = (keyword_score * 0.3 + sentiment_score * 0.35 + vader_score * 0.35)
        return round(confidence_score, 2)
    
    def calculate_enthusiasm(self, text, sentiment_result):
        """
        Evaluate enthusiasm/positivity based on:
        - Positive sentiment
        - Enthusiasm keywords
        - Overall energy in language
        """
        text_lower = text.lower()
        
        # Count enthusiasm keywords
        enthusiasm_count = sum(1 for keyword in self.enthusiasm_keywords if keyword in text_lower)
        keyword_score = min(enthusiasm_count / 5.0, 1.0)
        
        # Positive sentiment
        polarity = sentiment_result.get("textblob", {}).get("polarity", 0)
        sentiment_score = max(0, polarity)  # Only positive sentiment counts
        
        # VADER positive score
        vader_positive = sentiment_result.get("vader", {}).get("positive", 0)
        
        # Combine factors
        enthusiasm_score = (keyword_score * 0.3 + sentiment_score * 0.4 + vader_positive * 0.3)
        return round(enthusiasm_score, 2)
    
    def calculate_professionalism(self, text, sentiment_result):
        """
        Evaluate professionalism based on:
        - Professional keywords
        - Language formality
        - Balanced sentiment (not overly emotional)
        """
        text_lower = text.lower()
        
        # Count professional keywords
        professional_count = sum(1 for keyword in self.professional_keywords if keyword in text_lower)
        keyword_score = min(professional_count / 5.0, 1.0)
        
        # Subjectivity (lower = more professional/objective)
        subjectivity = sentiment_result.get("textblob", {}).get("subjectivity", 0.5)
        objectivity_score = 1.0 - subjectivity
        
        # Balanced sentiment (not too extreme in either direction)
        polarity = abs(sentiment_result.get("textblob", {}).get("polarity", 0))
        balance_score = 1.0 - min(polarity, 0.5) * 2  # Prefer moderate sentiment
        
        # Combine factors
        professionalism_score = (keyword_score * 0.4 + objectivity_score * 0.4 + balance_score * 0.2)
        return round(professionalism_score, 2)
    
    def calculate_engagement(self, text, sentiment_result):
        """
        Evaluate engagement/energy based on:
        - Text length and detail
        - Sentiment strength
        - Language variety
        """
        # Text length indicates engagement (longer = more engaged, but not too long)
        word_count = len(text.split())
        length_score = min(word_count / 200.0, 1.0)  # Optimal around 200+ words
        
        # Sentiment confidence (stronger sentiment = more engaged)
        confidence = sentiment_result.get("overall_sentiment", {}).get("confidence", 0)
        
        # Vocabulary diversity
        words = text.lower().split()
        unique_words = len(set(words))
        vocab_diversity = unique_words / len(words) if words else 0
        
        # Combine factors
        engagement_score = (length_score * 0.3 + confidence * 0.4 + vocab_diversity * 0.3)
        return round(engagement_score, 2)
    
    def evaluate(self, transcribed_text):
        """
        Comprehensive candidate evaluation.
        
        Args:
            transcribed_text: The transcribed text from the interview
            
        Returns:
            Dictionary with evaluation scores and analysis
        """
        if not transcribed_text or not transcribed_text.strip():
            return {
                "error": "No text provided for evaluation",
                "scores": {}
            }
        
        if self.text_analyzer is None:
            return {
                "error": "Text analyzer not available. Install dependencies: pip install textblob vaderSentiment nltk",
                "scores": {}
            }
        
        # Perform sentiment analysis
        sentiment_result = self.text_analyzer.analyze(transcribed_text)
        
        if "error" in sentiment_result:
            return sentiment_result
        
        # Calculate scores for each parameter
        scores = {
            "communication_clarity": self.calculate_communication_clarity(transcribed_text, sentiment_result),
            "confidence": self.calculate_confidence(transcribed_text, sentiment_result),
            "enthusiasm": self.calculate_enthusiasm(transcribed_text, sentiment_result),
            "professionalism": self.calculate_professionalism(transcribed_text, sentiment_result),
            "engagement": self.calculate_engagement(transcribed_text, sentiment_result)
        }
        
        # Calculate overall score
        overall_score = sum(scores.values()) / len(scores)
        
        # Get sentiment summary
        overall_sentiment = sentiment_result.get("overall_sentiment", {})
        
        return {
            "transcribed_text": transcribed_text,
            "text_length": len(transcribed_text),
            "word_count": len(transcribed_text.split()),
            "scores": scores,
            "overall_score": round(overall_score, 2),
            "overall_sentiment": overall_sentiment,
            "sentiment_details": {
                "textblob": sentiment_result.get("textblob", {}),
                "vader": sentiment_result.get("vader", {})
            }
        }

