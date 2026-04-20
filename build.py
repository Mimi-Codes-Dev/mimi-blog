import os
import re
import markdown
import json
from pathlib import Path

# Configuration
PROJECT_ROOT = Path(__file__).parent
CONTENT_DIR = PROJECT_ROOT / "content"
POSTS_DIR = PROJECT_ROOT / "posts"
TEMPLATES_DIR = PROJECT_ROOT / "templates"
INDEX_TEMPLATE_PATH = TEMPLATES_DIR / "index.html"
POST_TEMPLATE_PATH = TEMPLATES_DIR / "post.html"
OUTPUT_INDEX_PATH = PROJECT_ROOT / "index.html"
SEARCH_INDEX_PATH = PROJECT_ROOT / "search_index.json"
TAGS_LIST_PATH = PROJECT_ROOT / "tags_list.json"

def parse_frontmatter(content):
    """
    Parses YAML-like frontmatter from the top of a markdown file.
    """
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            header = parts[1]
            body = parts[2].strip()
            meta = {}
            for line in header.strip().split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    val = value.strip()
                    # Remove surrounding quotes
                    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                        val = val[1:-1]
                    
                    # Handle tags specifically
                    if key.strip() == "tags":
                        # Support comma-separated strings or [a, b] format
                        if val.startswith("[") and val.endswith("]"):
                            # Simple list parsing
                            val = [t.strip().strip('"').strip("'") for t in val[1:-1].split(",")]
                        else:
                            val = [t.strip() for t in val.split(",")]
                    
                    meta[key.strip()] = val
            return meta, body
    return {}, content

def build():
    # Ensure directories exist
    POSTS_DIR.mkdir(exist_ok=True)

    # Load templates
    with open(INDEX_TEMPLATE_PATH, "r", encoding="utf-8") as f:
        index_template = f.read()
    with open(POST_TEMPLATE_PATH, "r", encoding="utf-8") as f:
        post_template = f.read()

    posts_metadata = []
    all_tags = set()

    # Process all markdown files in content directory
    for md_file in sorted(CONTENT_DIR.glob("*.md")):
        with open(md_file, "r", encoding="utf-8") as f:
            raw_content = f.read()

        meta, body = parse_frontmatter(raw_content)
        
        title = meta.get("title", md_file.stem)
        date = meta.get("date", "Unknown Date")
        description = meta.get("description", "")
        tags = meta.get("tags", [])
        if isinstance(tags, str): # fallback for simple string
            tags = [t.strip() for t in tags.split(",")]
        
        for tag in tags:
            all_tags.add(tag)
        
        # Convert markdown to HTML
        html_content = markdown.markdown(body, extensions=['extra', 'nl2br'])
        
        # Generate post HTML
        output_filename = f"{md_file.stem}.html"
        output_path = POSTS_DIR / output_filename
        
        final_post_html = post_template.replace("{{ title }}", title)\
                                       .replace("{{ date }}", date)\
                                       .replace("{{ content }}", html_content)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_post_html)
        
        # Collect metadata for index and search
        post_data = {
            "title": title,
            "date": date,
            "description": description,
            "url": f"posts/{output_filename}",
            "tags": tags
        }
        posts_metadata.append(post_data)

    # Sort posts by date descending
    posts_metadata.sort(key=lambda x: x["date"], reverse=True)

    # 1. Generate Search Index (JSON)
    with open(SEARCH_INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(posts_metadata, f, ensure_ascii=False, indent=2)

    # 2. Generate Tags List (JSON)
    with open(TAGS_LIST_PATH, "w", encoding="utf-8") as f:
        json.dump(sorted(list(all_tags)), f, ensure_ascii=False, indent=2)

    # 3. Generate Post List HTML for index
    post_list_html = ""
    for post in posts_metadata:
        tags_html = "".join([f'<span class="tag-pill" data-tag="{t}">{t}</span>' for t in post["tags"]])
        post_list_html += f'''
            <div class="post-card" data-tags='{json.dumps(post["tags"])}'>
                <h3><a href="{post["url"]}">{post["title"]}</a></h3>
                <p class="date">{post["date"]}</p>
                <p>{post["description"]}</p>
                <div class="post-tags">
                    {tags_html}
                </div>
            </div>'''

    # 4. Final index HTML
    # We pass the raw posts_metadata as a JSON string to the template so JS can use it
    final_index_html = index_template.replace("{{ post_list }}", post_list_html)\
                                     .replace("{{ posts_json }}", json.dumps(posts_metadata, ensure_ascii=False))\
                                     .replace("{{ tags_json }}", json.dumps(sorted(list(all_tags)), ensure_ascii=False))
    
    with open(OUTPUT_INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(final_index_html)

    print(f"Successfully built {len(posts_metadata)} posts and index.html")
    print(f"Generated: search_index.json, tags_list.json")

if __name__ == "__main__":
    build()
