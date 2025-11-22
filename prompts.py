# prompts.py
from jinja2 import Template

OUTLINE_PROMPT = Template("""You are a professional content writer.
Create a detailed blog outline for the following request.

Topic: {{ topic }}
Target audience: {{ audience }}
Tone: {{ tone }}
Desired blog length (words): {{ length }}

Requirements:
- Provide a short one-line title.
- Provide a 3-sentence summary (meta description).
- Provide a structured outline with sections and subsections.
- Provide estimated word counts for each top-level section.
Respond in JSON with keys: title, summary, outline (list of sections).
Format example:
{
  "title": "...",
  "summary": "...",
  "outline": [
    {"heading":"Introduction", "subsections":["..."], "words": 150},
    ...
  ]
}
""")

SECTION_EXPAND_PROMPT = Template("""You are an expert blog writer.
Write the content for the section below in fluent, engaging markdown.
Section heading: {{ heading }}
Subsections: {{ subsections }}
Context / blog title: {{ title }}
Tone: {{ tone }}
Target audience: {{ audience }}
Desired section word count: {{ words }}

Instructions:
- Write in Markdown.
- Include examples, a short code block if relevant, and 1-2 bullet-point takeaways at the end of the section.
- Use clear headings for subsections.
- Do not invent false facts.
- Keep content original and human-readable.
""")

FULL_BLOG_PROMPT = Template("""You are a professional content writer. Use the following pieces (title, summary, sections) to assemble a blog post in Markdown.

Title: {{ title }}
Meta summary (1 sentence): {{ summary }}
Sections: {{ sections_json }}   # the sections content already generated (markdown)
Tone: {{ tone }}
Audience: {{ audience }}

Instructions:
- Produce a clean Markdown blog article with a short intro, the sections in order, a conclusion, and a 3-bullet "Key takeaways" section at the end.
- Add simple front-matter at top: title, meta description.
- Make sure the article length is roughly {{ length }} words.
""")
