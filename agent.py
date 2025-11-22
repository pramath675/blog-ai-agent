# agent.py
import os
import json
import time
from typing import List, Dict
import openai
from config import OPENAI_API_KEY, MODEL_NAME, OUTPUT_DIR
from prompts import OUTLINE_PROMPT, SECTION_EXPAND_PROMPT, FULL_BLOG_PROMPT
from utils import save_markdown, unique_filename, ensure_dir

openai.api_key = OPENAI_API_KEY

def call_chat_completion(system_prompt: str, user_prompt: str, max_tokens=1000, temperature=0.7):
    """
    Simple wrapper for OpenAI chat completion.
    Adapt this wrapper if your openai package version differs.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    resp = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    text = resp["choices"][0]["message"]["content"].strip()
    return text

def generate_outline(topic: str, audience: str, tone: str, length:int):
    system = "You are a helpful outline generator."
    user = OUTLINE_PROMPT.render(topic=topic, audience=audience, tone=tone, length=length)
    raw = call_chat_completion(system, user, max_tokens=700, temperature=0.2)
    # The model should return JSON; be forgiving and try to parse JSON inside.
    try:
        parsed = json.loads(raw)
    except Exception:
        # try to extract JSON block
        import re
        m = re.search(r"\{.*\}", raw, re.S)
        if m:
            parsed = json.loads(m.group())
        else:
            raise ValueError("Could not parse outline JSON from model response:\n" + raw)
    return parsed

def expand_section(section: Dict, title:str, audience:str, tone:str):
    heading = section.get("heading", "")
    subsections = section.get("subsections", [])
    words = section.get("words", 300)
    system = "You are an expert blog writer."
    user = SECTION_EXPAND_PROMPT.render(
        heading=heading,
        subsections=subsections,
        title=title,
        tone=tone,
        audience=audience,
        words=words
    )
    text = call_chat_completion(system, user, max_tokens=1100, temperature=0.7)
    return text

def assemble_full_blog(title: str, summary: str, sections_markdown: List[str], tone: str, audience: str, length:int):
    system = "You are the final assembler: produce final polished blog markdown."
    sections_joined = "\n\n---\n\n".join(sections_markdown)
    user = FULL_BLOG_PROMPT.render(
        title=title,
        summary=summary,
        sections_json=sections_joined,
        tone=tone,
        audience=audience,
        length=length
    )
    text = call_chat_completion(system, user, max_tokens=1500, temperature=0.6)
    return text

def generate_blog(topic: str, audience: str="general", tone: str="conversational", length:int=800, save:bool=True):
    """
    Full pipeline:
    1) Outline
    2) Expand each top-level section
    3) Assemble final blog
    4) Save to output dir (if requested)
    """
    outline_json = generate_outline(topic, audience, tone, length)
    title = outline_json.get("title", f"Blog about {topic}")
    summary = outline_json.get("summary", "")
    outline = outline_json.get("outline", [])
    sections_markdown = []
    for sec in outline:
        try:
            md = expand_section(sec, title=title, audience=audience, tone=tone)
        except Exception as e:
            # If expansion fails, add a placeholder
            md = f"## {sec.get('heading','Section')}\n\n*Failed to expand this section: {e}*"
        sections_markdown.append(md)
        # polite pause to avoid throttling
        time.sleep(1.2)

    final_md = assemble_full_blog(title, summary, sections_markdown, tone, audience, length)
    if save:
        ensure_dir(OUTPUT_DIR)
        filename = unique_filename("blog", title)
        path = save_markdown(OUTPUT_DIR, filename, final_md)
        return {"title": title, "summary": summary, "path": path, "content": final_md}
    else:
        return {"title": title, "summary": summary, "path": None, "content": final_md}
