#!/usr/bin/env python3

import os
import subprocess
import shutil

def main():
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   Removed {dir_name}/")
    
    # Clean pycache in src and subdirectories
    for root, dirs, files in os.walk("src"):
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            shutil.rmtree(pycache_path)
            print(f"   Removed {pycache_path}")

    subprocess.run("poetry install", shell=True, check=True, text=True)
    subprocess.run("poetry run pyinstaller trackonverter.spec", shell=True, check=True, text=True)
    
if __name__ == "__main__":
    main()