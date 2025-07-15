import re
from collections import Counter
import nltk
nltk.download('punkt', quiet=True)
from nltk.tokenize import sent_tokenize

def clean_text(text):
    """
    Clean input text by removing URLs and punctuation, and lowering case.
    """
    text = re.sub(r"http\S+", "", text)  # remove URLs
    text = re.sub(r"[^\w\s]", "", text)  # remove punctuation
    return text.lower()

def extract_traits(texts):
    """
    Extract basic traits from a list of text snippets.

    Returns a dict with interests, profession, personality, location, behavior.
    """
    traits = {
        "interests": [],
        "interest_sources": [],
        "personality": [],
        "personality_sources": [],
        "profession": None,
        "profession_sources": [],
        "location": None,
        "location_sources": [],
        "behavior": None,
        "behavior_sources": [],
    }

    interest_keywords = ["gaming", "books", "reading", "tech", "fitness", "music", "sports", "anime", "coding"]
    profession_keywords = ["engineer", "developer", "teacher", "student", "researcher", "designer"]
    location_patterns = [r"from (\w+)", r"based in (\w+)", r"living in (\w+)"]
    personality_adjectives = ["introvert", "extrovert", "funny", "sarcastic", "serious", "emotional"]

    for text in texts:
        clean = clean_text(text)

        for word in interest_keywords:
            if word in clean and word not in traits["interests"]:
                traits["interests"].append(word)
                traits["interest_sources"].append(text)

        for word in profession_keywords:
            if word in clean and traits["profession"] is None:
                traits["profession"] = word
                traits["profession_sources"].append(text)

        for adj in personality_adjectives:
            if adj in clean and adj not in traits["personality"]:
                traits["personality"].append(adj)
                traits["personality_sources"].append(text)

        for pattern in location_patterns:
            match = re.search(pattern, clean)
            if match and traits["location"] is None:
                traits["location"] = match.group(1)
                traits["location_sources"].append(text)

        # Detect emotional/expressive behavior by common phrases
        if traits["behavior"] is None and any(phrase in clean for phrase in ["i hate", "i love helping", "i argue", "i feel"]):
            traits["behavior"] = "emotional or expressive"
            traits["behavior_sources"].append(text)

    return traits
