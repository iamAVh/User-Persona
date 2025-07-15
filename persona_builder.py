from transformers import pipeline, AutoTokenizer
from utils import clean_text, extract_traits

MAX_TOKENS = 400  # Keep safely below 512 to avoid token errors

def chunk_text_by_tokens(text, tokenizer, max_tokens=MAX_TOKENS):
    tokens = tokenizer.encode(text, add_special_tokens=False)
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i+max_tokens]
        yield tokenizer.decode(chunk_tokens, clean_up_tokenization_spaces=True)

def generate_structured_persona_text(username, combined_summary, traits):
    # Build a structured third-person user persona text

    persona_lines = []
    persona_lines.append(f"{username.capitalize()}’s User Persona")
    persona_lines.append("-" * 40)
    
    # Age: Not available — placeholder
    persona_lines.append("Age: Unknown")
    
    # Occupation
    occupation = traits.get("profession", "Unknown")
    persona_lines.append(f"Occupation: {occupation.capitalize() if occupation else 'Unknown'}")
    
    # Location
    location = traits.get("location", "Unknown")
    persona_lines.append(f"Location: {location.capitalize() if location else 'Unknown'}")
    
    # Interests
    interests = traits.get("interests", [])
    if interests:
        persona_lines.append(f"Interests: {', '.join([i.capitalize() for i in interests])}")
    
    # Personality Traits
    personality = traits.get("personality", [])
    if personality:
        persona_lines.append(f"Personality Traits: {', '.join([p.capitalize() for p in personality])}")
    
    # Behavior
    behavior = traits.get("behavior", None)
    if behavior:
        persona_lines.append(f"Behavior: {behavior.capitalize()}")

    # Add a concise summary section as motivation or description
    summary_sentence = combined_summary.split('. ')[0].strip() if combined_summary else "No summary available."
    if not summary_sentence.endswith('.'):
        summary_sentence += '.'
    persona_lines.append("\nSummary:")
    persona_lines.append(summary_sentence)

    # Add placeholders for Frustrations, Goals, Quote to mimic your example
    persona_lines.append("\nFrustrations:")
    persona_lines.append("Detailed frustrations data is not available.")

    persona_lines.append("\nGoals:")
    persona_lines.append("Engages meaningfully within their community and interests.")

    persona_lines.append('\nQuote:')
    persona_lines.append(f'"{username.capitalize()} values insightful and constructive discussions online."')

    return "\n".join(persona_lines)

def build_persona(username, data):
    print("[+] Loading summarizer model...")
    summarizer = pipeline("summarization", model="philschmid/bart-large-cnn-samsum")
    tokenizer = AutoTokenizer.from_pretrained("philschmid/bart-large-cnn-samsum")

    # Combine comments and posts text
    all_text = [c['body'] for c in data['comments']] + \
               [p['title'] + " " + p['selftext'] for p in data['posts']]
    combined_text = " ".join(all_text)

    # Chunk text safely under token limits
    chunks = list(chunk_text_by_tokens(combined_text, tokenizer))

    chunk_summaries = []
    for i, chunk in enumerate(chunks):
        try:
            summary = summarizer(chunk, max_length=120, min_length=30, do_sample=False)[0]['summary_text']
            chunk_summaries.append(summary)
        except Exception as e:
            print(f"[!] Skipping chunk {i} due to error: {e}")

    # Summarize chunk summaries to produce a final concise summary
    combined_summary_text = " ".join(chunk_summaries)
    try:
        combined_summary = summarizer(combined_summary_text, max_length=100, min_length=30, do_sample=False)[0]['summary_text']
    except Exception as e:
        print(f"[!] Could not create final summary: {e}")
        combined_summary = combined_summary_text  # fallback

    # Extract traits from all raw text
    traits = extract_traits(all_text)

    # Generate the final persona text in third-person format
    persona_text = generate_structured_persona_text(username, combined_summary, traits)

    return persona_text
