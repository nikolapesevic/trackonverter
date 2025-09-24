#!/usr/bin/env python3

import os
import subprocess
import shutil
import platform
import zipfile

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

    print("Installing dependencies...")
    subprocess.run("poetry install", shell=True, check=True, text=True)
    
    print("Building executable...")
    subprocess.run("poetry run pyinstaller trackonverter.spec", shell=True, check=True, text=True)
    
    # Post-processing based on platform
    if platform.system() == "Darwin":  # macOS
        print("Creating macOS App Bundle zip...")
        app_path = "dist/Trackonverter.app"
        zip_path = "trackonverter-macos.zip"
        
        if os.path.exists(app_path):
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(app_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, "dist")
                        zipf.write(file_path, arcname)
            print(f"Created {zip_path}")
        else:
            print("Warning: App bundle not found at expected path")
    
    elif platform.system() == "Windows":
        print("Renaming Windows executable...")
        old_path = "dist/trackonverter.exe"
        new_path = "dist/trackonverter-windows.exe"
        if os.path.exists(old_path):
            shutil.move(old_path, new_path)
            print(f"Renamed to {new_path}")
            print("Single-file Windows executable created successfully!")
        else:
            print("Warning: Windows executable not found at expected path")
    
    print("Build completed!")
    
if __name__ == "__main__":
    main()