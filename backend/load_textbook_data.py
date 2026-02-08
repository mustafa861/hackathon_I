#!/usr/bin/env python3
"""
Script to load textbook content into the Qdrant vector database.
This makes the content available for the chatbot to search and use.
"""

import os
import glob
from pathlib import Path
from services.embeddings_service import add_textbook_content

def load_textbook_content():
    """Load all textbook markdown files into the vector database"""

    # Find all markdown files in the docs directory
    docs_path = Path("../docs")  # Relative to backend directory
    markdown_files = list(docs_path.glob("*.md"))

    print(f"Found {len(markdown_files)} markdown files to load...")

    total_loaded = 0

    for md_file in markdown_files:
        print(f"Loading {md_file.name}...")

        try:
            # Read the content of the markdown file
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract chapter slug from filename
            chapter_slug = md_file.stem  # Remove .md extension

            # Try to extract a section title from the first heading in the file
            section_title = "Untitled"
            lines = content.split('\n')
            for line in lines:
                if line.startswith('# '):  # H1 heading
                    section_title = line[2:].strip()  # Remove '# ' prefix
                    break
                elif line.startswith('## '):  # H2 heading (if no H1)
                    section_title = line[3:].strip()  # Remove '## ' prefix
                    break

            # Add the content to the vector database
            success = add_textbook_content(
                text=content,
                chapter_slug=chapter_slug,
                section_title=section_title
            )

            if success:
                print(f"  ✓ Successfully loaded {chapter_slug}")
                total_loaded += 1
            else:
                print(f"  ✗ Failed to load {chapter_slug}")

        except Exception as e:
            print(f"  ✗ Error loading {md_file.name}: {str(e)}")

    print(f"\nLoaded {total_loaded} out of {len(markdown_files)} files successfully.")

if __name__ == "__main__":
    load_textbook_content()