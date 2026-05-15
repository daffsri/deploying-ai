"""One-time helper script to build CitySidekick's persistent ChromaDB."""

from services.semantic_service import build_chroma_db


if __name__ == "__main__":
    print(build_chroma_db(force_rebuild=True))
