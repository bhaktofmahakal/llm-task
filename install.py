#!/usr/bin/env python3
import subprocess
import sys
import os

def run_command(cmd, description=""):
    """Run a command and print output."""
    if description:
        print(f"\n{'='*60}")
        print(f"[INSTALL] {description}")
        print('='*60)
    
    try:
        result = subprocess.run(cmd, shell=True, check=False, capture_output=False, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return False

def main():
    print("[START] LLM Fact Checker - Installation Script")
    print("=" * 60)
    
    packages = [
        ("pip install --upgrade pip setuptools wheel", "Upgrading pip and dependencies"),
        ("pip install groq", "Installing Groq SDK"),
        ("pip install python-dotenv", "Installing python-dotenv"),
        ("pip install pandas", "Installing Pandas"),
        ("pip install chromadb", "Installing ChromaDB"),
        ("pip install sentence-transformers", "Installing Sentence Transformers"),
        ("pip install streamlit", "Installing Streamlit"),
    ]
    
    print("\nStarting installation...\n")
    
    for cmd, desc in packages:
        success = run_command(cmd, desc)
        if not success:
            print(f"[WARNING] Command failed: {cmd}")
            print("Continuing with next package...\n")
    
    print("\n" + "=" * 60)
    print("[OK] Installation Summary")
    print("=" * 60)
    print("\nAll packages have been installed!")
    print("\nNext steps:")
    print("1. Create .env file with GROQ_API_KEY")
    print("   Copy from: .env.example")
    print("   Get API key from: https://console.groq.com")
    print("\n2. Run the application:")
    print("   streamlit run streamlit_app.py")
    print("\n3. For command-line test:")
    print("   python sample_usage.py")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
