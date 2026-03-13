# Greeting Autocomplete

A Python Streamlit application that autocompletes greetings using NLP-based matching with scikit-learn TF-IDF and cosine similarity.

## Features

- **Streamlit UI** — simple, interactive web interface for entering greetings
- **Predefined greeting dictionary** — covers common greetings in multiple styles
- **NLP fuzzy matching** — TF-IDF with character n-grams and cosine similarity for typo-tolerant matching
- **Safe fallbacks** — handles empty input and unrecognised input gracefully

## Project Structure

```
greeting-autocomplete/
├── app.py            # Streamlit UI
├── greetings.py      # Predefined greeting → response dictionary
├── matcher.py        # TF-IDF cosine similarity matcher
├── test_matcher.py   # Unit tests
├── requirements.txt  # Python dependencies
├── README.md         # This file
└── DOCUMENTATION.md  # Architecture docs with Mermaid diagrams
```

## Setup

### Prerequisites

- Python 3.9 or higher

### Install dependencies

```bash
cd greeting-autocomplete
pip install -r requirements.txt
```

## Run

Start the Streamlit application:

```bash
cd greeting-autocomplete
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## Test

Run the unit tests from inside the `greeting-autocomplete` directory:

```bash
cd greeting-autocomplete
pytest test_matcher.py -v
```

## How It Works

1. The user types a greeting into the text input field.
2. The input is normalised (lowercased and stripped of whitespace).
3. An exact lookup is attempted against the greeting dictionary.
4. If no exact match is found, TF-IDF vectorisation with character n-grams (2–3) is used to compute cosine similarity between the input and all known greetings.
5. If the best similarity score meets the threshold (0.3), the corresponding response is returned; otherwise a default fallback message is shown.
