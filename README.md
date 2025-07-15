# 🧠 Reddit User Persona Generator

A lightweight Python-based project that analyzes a Reddit user's public activity to generate a **concise third-person persona profile**. The goal is to distill personality traits, interests, profession, and behavior patterns from a user’s posts and comments using a combination of **Natural Language Processing (NLP)** and **Large Language Model (LLM)** summarization.

---

## 🔍 What It Does

Given a Reddit username or profile URL (e.g., `https://www.reddit.com/user/spez/`), the tool:

1. Fetches the user's most recent Reddit comments and posts.
2. Chunks and summarizes the combined text using a HuggingFace summarization model.
3. Extracts structured traits (interests, profession, location, etc.) using pattern-based NLP.
4. Outputs a structured persona in a clean, professional format (ideal for UX, marketing, or behavioral studies).

---

## 🧱 Project Architecture

reddit_user_persona/
├── main.py # CLI Entry Point
├── reddit_scraper.py # Fetches Reddit user data via PRAW
├── persona_builder.py # Builds and formats persona using summarization + rule-based NLP
├── utils.py # Text cleaning & trait extraction utilities
├── output/ # Folder to store generated personas
└── requirements.txt # Dependencies


---

## 📦 Libraries & Tools Used

| Tool / Library           | Purpose                                        |
|-------------------------|------------------------------------------------|
| `PRAW`                  | Python Reddit API Wrapper for scraping data   |
| `Transformers` (HuggingFace) | Summarization using `bart-large-cnn-samsum` |
| `nltk`                  | Text preprocessing and tokenization           |
| `re` (regex)            | Rule-based trait extraction from raw text     |
| `os`                    | File handling and output directory management |

---

## 🧠 Approach

### 1. **Data Collection**
- Reddit username is extracted from input URL.
- `PRAW` fetches up to **100 comments** and **50 submissions** using the Reddit API.

### 2. **Summarization**
- The texts are combined and tokenized using `AutoTokenizer`.
- Text is chunked into **≤900 token blocks** to stay within model limits (max 1024).
- Each chunk is summarized using HuggingFace’s `philschmid/bart-large-cnn-samsum` pipeline.
- Chunk summaries are then optionally re-summarized to create a final distilled version.

### 3. **Trait Extraction**
Using regex + keyword matching:
- **Interests**: Detected via words like "music", "coding", etc.
- **Profession**: Parsed from keywords like "developer", "teacher", etc.
- **Location**: Regex patterns like "based in X", "from Y"
- **Personality**: Matches adjectives like "introvert", "sarcastic", etc.
- **Behavior**: Captures expressive language like "I feel", "I hate", etc.

### 4. **Persona Formatting**
- Final output is styled in a structured and **third-person** tone similar to marketing persona templates.



---

## 🖥️ How to Run

```bash
git clone https://github.com/yourusername/reddit-user-persona
cd reddit-user-persona
pip install -r requirements.txt
python main.py

