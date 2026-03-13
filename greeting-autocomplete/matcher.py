"""NLP-based greeting matcher using TF-IDF cosine similarity."""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from greetings import GREETINGS, DEFAULT_RESPONSE

# Minimum cosine similarity score required for accepting a fuzzy match.
# Values below this are treated as unrecognised input and trigger the fallback.
THRESHOLD = 0.3

_KNOWN_GREETINGS = list(GREETINGS.keys())

# Pre-fit the vectorizer on the static greeting dictionary so that per-request
# calls only need to transform the user input, not refit the entire corpus.
_vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 3))
_known_vectors = _vectorizer.fit_transform(_KNOWN_GREETINGS)


def match_greeting(user_input: str) -> str:
    """Return an autocompleted response for the given greeting input.

    Steps:
      1. Normalize input (lowercase + strip whitespace).
      2. Return empty string for empty input.
      3. Check for an exact match in the dictionary.
      4. Use TF-IDF with character n-grams and cosine similarity for fuzzy matching.
      5. Return the default fallback response if the best score is below the threshold.

    Args:
        user_input: Raw greeting text from the user.

    Returns:
        The matched or fallback greeting response string.
    """
    normalized = user_input.lower().strip()

    if not normalized:
        return ""

    # Exact match
    if normalized in GREETINGS:
        return GREETINGS[normalized]

    query_vector = _vectorizer.transform([normalized])
    scores = cosine_similarity(query_vector, _known_vectors).flatten()
    best_index = scores.argmax()
    best_score = scores[best_index]

    if best_score < THRESHOLD:
        return DEFAULT_RESPONSE

    return GREETINGS[_KNOWN_GREETINGS[best_index]]
