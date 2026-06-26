#Program to arrange my files in the download folder based on their extensions

import os
import shutil
from pathlib import Path

def organize_downloads():
    download_dir = Path.home() / "Downloads"
    
    file_categories = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".ico"],
        "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx", ".ppt", ".csv"],
        "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
        "Videos": [".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "Installers": [".exe", ".msi", ".dmg", ".pkg", ".deb"],
        "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".json"]
    }

    print(f"Scanning target directory: {download_dir}\n")

    if not download_dir.exists():
        print("Error: Downloads directory could not be found.")
        return

    moved_count = 0

    # Iterate through every item in the Downloads directory
    for item in download_dir.iterdir():
        if item.is_dir() or item.name.startswith('.'):
            continue
            
        file_extension = item.suffix.lower()
        
        target_folder_name = "Others"
        
        for category, extensions in file_categories.items():
            if file_extension in extensions:
                target_folder_name = category
                break
                
        target_dir = download_dir / target_folder_name
        
        destination_path = target_dir / item.name
        
        try:
            target_dir.mkdir(exist_ok=True)
            
            shutil.move(str(item), str(destination_path))
            print(f"Moved: '{item.name}' ➔ [{target_folder_name}]")
            moved_count += 1
            
        except Exception as error:
            print(f"Failed to move '{item.name}': {error}")

    print(f"\nTask complete. Successfully organized {moved_count} files!")

if __name__ == "__main__":
    organize_downloads()
