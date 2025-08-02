import os
import requests
from pathlib import Path
from boxsdk import JWTAuth, Client
from dotenv import load_dotenv

load_dotenv()

class BoxDocumentSync:
    def __init__(self, developer_token=None, folder_id=None):
        self.developer_token = developer_token or os.getenv('BOX_DEVELOPER_TOKEN')
        self.folder_id = folder_id or os.getenv('BOX_FOLDER_ID')
        self.client = Client(oauth=None)
        self.client.auth._access_token = self.developer_token
        
    def download_folder_contents(self, local_path="./documents"):
        """Download all files from Box folder to local directory"""
        Path(local_path).mkdir(exist_ok=True)
        
        folder = self.client.folder(self.folder_id)
        items = folder.get_items()
        
        downloaded_files = []
        
        for item in items:
            if item.type == 'file':
                # Check file size (max 25MB for most formats)
                if item.size > 25 * 1024 * 1024:
                    print(f"Skipping {item.name} - file too large ({item.size} bytes)")
                    continue
                    
                file_path = os.path.join(local_path, item.name)
                
                with open(file_path, 'wb') as file_handle:
                    item.download_to(file_handle)
                    
                downloaded_files.append(file_path)
                print(f"Downloaded: {item.name}")
                
        return downloaded_files

# Usage
if __name__ == "__main__":
    sync = BoxDocumentSync()
    files = sync.download_folder_contents()
    print(f"Downloaded {len(files)} files from Box")
