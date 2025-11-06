"""
Text Sentiment Analysis Module
Provides sentiment analysis using multiple methods: TextBlob and VADER
"""

from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

# Download NLTK data if not already present (TextBlob will do this automatically on first use)
# This is done lazily to avoid import errors
def _ensure_nltk_data():
    """Ensure NLTK data is downloaded (called on first use)."""
    try:
        import nltk
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords', quiet=True)
    except (ImportError, Exception):
        # NLTK will be installed as a dependency of TextBlob
        pass


class TextAnalyzer:
    """Analyzes text sentiment using multiple methods."""
    
    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()
    
    def clean_text(self, text):
        """Basic text cleaning."""
        if not text:
            return ""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        return text
    
    def analyze_with_textblob(self, text):
        """Analyze sentiment using TextBlob."""
        # Ensure NLTK data is available
        _ensure_nltk_data()
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity  # Range: -1 (negative) to 1 (positive)
        subjectivity = blob.sentiment.subjectivity  # Range: 0 (objective) to 1 (subjective)
        
        # Classify sentiment
        if polarity > 0.1:
            sentiment_label = "positive"
        elif polarity < -0.1:
            sentiment_label = "negative"
        else:
            sentiment_label = "neutral"
        
        return {
            "polarity": round(polarity, 3),
            "subjectivity": round(subjectivity, 3),
            "label": sentiment_label,
            "confidence": round(abs(polarity), 3)
        }
    
    def analyze_with_vader(self, text):
        """Analyze sentiment using VADER (Valence Aware Dictionary and sEntiment Reasoner)."""
        scores = self.vader_analyzer.polarity_scores(text)
        
        # Determine label based on compound score
        compound = scores['compound']
        if compound >= 0.05:
            sentiment_label = "positive"
        elif compound <= -0.05:
            sentiment_label = "negative"
        else:
            sentiment_label = "neutral"
        
        return {
            "compound": round(scores['compound'], 3),
            "positive": round(scores['pos'], 3),
            "neutral": round(scores['neu'], 3),
            "negative": round(scores['neg'], 3),
            "label": sentiment_label,
            "confidence": round(abs(compound), 3)
        }
    
    def analyze(self, text):
        """
        Perform comprehensive sentiment analysis on text.
        
        Args:
            text: Input text string
            
        Returns:
            Dictionary containing analysis results from multiple methods
        """
        if not text or not text.strip():
            return {
                "error": "Empty text provided",
                "text": ""
            }
        
        cleaned_text = self.clean_text(text)
        
        # Analyze with both methods
        textblob_result = self.analyze_with_textblob(cleaned_text)
        vader_result = self.analyze_with_vader(cleaned_text)
        
        # Determine overall sentiment (prefer VADER for social media/text, TextBlob for general)
        # Average the confidence scores
        avg_confidence = (textblob_result["confidence"] + vader_result["confidence"]) / 2
        
        # Use VADER label if both agree, otherwise use the one with higher confidence
        if textblob_result["label"] == vader_result["label"]:
            overall_label = textblob_result["label"]
        else:
            overall_label = textblob_result["label"] if textblob_result["confidence"] > vader_result["confidence"] else vader_result["label"]
        
        return {
            "text": cleaned_text,
            "text_length": len(cleaned_text),
            "word_count": len(cleaned_text.split()),
            "overall_sentiment": {
                "label": overall_label,
                "confidence": round(avg_confidence, 3)
            },
            "textblob": textblob_result,
            "vader": vader_result
        }
    
    def analyze_batch(self, texts):
        """
        Analyze multiple texts at once.
        
        Args:
            texts: List of text strings
            
        Returns:
            List of analysis results
        """
        return [self.analyze(text) for text in texts]

