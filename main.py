# main.py
import argparse
from agent import generate_blog

def main():
    parser = argparse.ArgumentParser("Blog Writer AI Agent")
    parser.add_argument("--topic", "-t", required=True, help="Blog topic or prompt")
    parser.add_argument("--audience", "-a", default="general", help="Target audience")
    parser.add_argument("--tone", default="conversational", help="Tone (e.g., professional, casual)")
    parser.add_argument("--length", "-l", type=int, default=900, help="Desired blog length in words")
    parser.add_argument("--no-save", action="store_true", help="Do not save output to file")
    args = parser.parse_args()

    result = generate_blog(
        topic=args.topic,
        audience=args.audience,
        tone=args.tone,
        length=args.length,
        save=(not args.no_save)
    )

    print("=== Blog Generated ===")
    print("Title:", result["title"])
    print("Saved to:", result["path"])
    print("\n--- Preview (first 500 chars) ---\n")
    print(result["content"][:500])

if __name__ == "__main__":
    main()
