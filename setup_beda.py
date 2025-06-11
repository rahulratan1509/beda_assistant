# setup_beda.py - module for beda assistant

import subprocess
import sys
import os

def install_packages():
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def download_textblob_corpora():
    import nltk
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        print("Downloading TextBlob corpora...")
        import textblob.download_corpora
        textblob.download_corpora.download_all()

if __name__ == "__main__":
    # Check if virtual environment is activated (optional)
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("Virtual environment detected.")
    else:
        print("Warning: It is recommended to use a virtual environment.")

    install_packages()
    download_textblob_corpora()
    print("Setup complete. You can now run 'python run.py' to start Beda assistant.")
