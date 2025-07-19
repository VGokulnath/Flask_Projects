#!/usr/bin/env python3
"""
DocChatWeb Startup Script
Run this script to start the DocChatWeb application with proper setup.
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required packages are installed."""
    try:
        import flask
        import openai
        import markdown
        print("✅ All dependencies are installed.")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_api_key():
    """Check if OpenAI API key is configured."""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("⚠️  OpenAI API key not found.")
        print("Please set your OpenAI API key:")
        print("  Linux/Mac: export OPENAI_API_KEY='your-key-here'")
        print("  Windows: set OPENAI_API_KEY=your-key-here")
        print("\nYou can still run the app, but AI features won't work without the API key.")
        return False
    else:
        print("✅ OpenAI API key is configured.")
        return True

def check_document():
    """Check if data.md exists."""
    if os.path.exists('data.md'):
        print("✅ Document file (data.md) found.")
        return True
    else:
        print("⚠️  Document file (data.md) not found. A sample will be created.")
        return False

def main():
    """Main startup function."""
    print("🚀 Starting DocChatWeb...")
    print("=" * 50)
    
    # Check all requirements
    deps_ok = check_dependencies()
    api_ok = check_api_key()
    doc_ok = check_document()
    
    print("=" * 50)
    
    if not deps_ok:
        print("❌ Cannot start due to missing dependencies.")
        sys.exit(1)
    
    if not api_ok:
        response = input("Continue without OpenAI API key? (y/n): ").lower().strip()
        if response != 'y':
            print("Please configure your OpenAI API key and try again.")
            sys.exit(1)
    
    print("🌟 Starting DocChatWeb server...")
    print("📱 Open your browser to: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Start the Flask app
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 DocChatWeb stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting the application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()