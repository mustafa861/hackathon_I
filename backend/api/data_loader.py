from fastapi import APIRouter, HTTPException
from services.embeddings_service import setup_collection
import subprocess
import sys
from pathlib import Path

router = APIRouter(tags=["data_loader"])

@router.post("/load-textbook-data")
def load_textbook_data():
    """Load textbook content from docs directory into the vector database"""
    try:
        # Setup the collection first
        setup_collection()

        # Import the loading function
        from services.embeddings_service import add_textbook_content

        # Find and load all markdown files from the docs directory
        docs_path = Path("../docs")
        markdown_files = list(docs_path.glob("*.md"))

        if not markdown_files:
            raise HTTPException(status_code=404, detail="No textbook markdown files found in docs directory")

        total_loaded = 0

        for md_file in markdown_files:
            try:
                # Read the content of the markdown file
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract chapter slug from filename
                chapter_slug = md_file.stem

                # Try to extract a section title from the first heading in the file
                section_title = "Untitled"
                lines = content.split('\n')
                for line in lines:
                    if line.startswith('# '):  # H1 heading
                        section_title = line[2:].strip()
                        break
                    elif line.startswith('## '):  # H2 heading
                        section_title = line[3:].strip()
                        break

                # Add the content to the vector database
                success = add_textbook_content(
                    text=content,
                    chapter_slug=chapter_slug,
                    section_title=section_title
                )

                if success:
                    total_loaded += 1

            except Exception as e:
                print(f"Error loading {md_file.name}: {str(e)}")
                continue  # Continue with other files even if one fails

        return {
            "message": f"Successfully loaded {total_loaded} textbook files into the database",
            "files_processed": len(markdown_files),
            "success_rate": f"{(total_loaded/len(markdown_files)*100):.1f}%"
        }

    except Exception as e:
        print(f"Error in load_textbook_data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to load textbook data: {str(e)}")

@router.get("/check-data-status")
def check_data_status():
    """Check the status of the vector database and loaded content"""
    try:
        from qdrant_client.http import models
        from services.embeddings_service import client, COLLECTION_NAME

        # Check if collection exists
        collections = client.get_collections().collections
        collection_exists = any(c.name == COLLECTION_NAME for c in collections)

        if not collection_exists:
            return {
                "collection_exists": False,
                "message": "Collection does not exist. Run /load-textbook-data to initialize."
            }

        # Get collection info
        collection_info = client.get_collection(COLLECTION_NAME)

        return {
            "collection_exists": True,
            "vectors_count": collection_info.points_count,
            "message": f"Collection exists with {collection_info.points_count} vectors"
        }
    except Exception as e:
        return {
            "error": str(e),
            "message": "Could not connect to vector database"
        }