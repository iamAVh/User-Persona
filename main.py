from reddit_scraper import fetch_reddit_data
from persona_builder import build_persona
import os

def main():
    reddit_url = input("Enter Reddit profile URL (e.g., https://www.reddit.com/user/spez/): ").strip()
    
    try:
        if "user/" not in reddit_url:
            raise ValueError("Invalid Reddit URL. Make sure it contains 'user/'.")
        
        username = reddit_url.split("user/")[1].strip("/")

        print(f"\n[+] Fetching data for user: u/{username}")
        user_data = fetch_reddit_data(username)

        print("[+] Building user persona...")
        persona_text = build_persona(username, user_data)

        # Create output folder if not exists
        os.makedirs("output", exist_ok=True)

        output_path = f"output/{username}.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(persona_text)

        print(f"[✓] Persona saved to {output_path}")

    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    main()
