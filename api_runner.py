#!/usr/bin/env python3
"""
API Runner for RAG-based IT Orientation System
Run this file from the project root directory to start the FastAPI server
"""

import os
import sys
from pathlib import Path

# Add the src directory to the path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

try:
    from api import app
    import uvicorn

    if __name__ == "__main__":
        print("🚀 Starting RAG-based IT Orientation API...")
        print("📍 API will be available at: http://localhost:8000")
        print("📖 API documentation at: http://localhost:8000/docs")
        print("🔄 Press Ctrl+C to stop the server")
        print()

        uvicorn.run(
            "api:app",
            host="0.0.0.0",
            port=8000,
            reload=False,  # Disable reload to avoid import issues
            log_level="info"
        )
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the project root directory")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error starting server: {e}")
    sys.exit(1)