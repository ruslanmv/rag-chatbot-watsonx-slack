import os
import yaml
from pathlib import Path
from box_sync_tool import BoxDocumentSync

def sync_box_and_create_kb():
    # Download documents from Box
    print("Syncing documents from Box...")
    sync = BoxDocumentSync()
    downloaded_files = sync.download_folder_contents("./documents")
    
    if not downloaded_files:
        print("No files downloaded from Box. Check your credentials and folder ID.")
        return
    
    # Update knowledge base YAML with downloaded files
    kb_config_path = "knowledge_base_box.yaml"
    
    with open(kb_config_path, 'r') as file:
        kb_config = yaml.safe_load(file)
    
    # Update documents list with relative paths
    kb_config['documents'] = [f"./{file}" for file in downloaded_files]
    
    # Write updated config
    with open(kb_config_path, 'w') as file:
        yaml.dump(kb_config, file, default_flow_style=False)
    
    print(f"Updated knowledge base config with {len(downloaded_files)} documents")
    print("Files included:")
    for file in downloaded_files:
        print(f"  - {file}")
    
    return kb_config_path

if __name__ == "__main__":
    config_path = sync_box_and_create_kb()
    if config_path:
        print(f"\nRun the following command to import the knowledge base:")
        print(f"orchestrate knowledge-bases import -f {config_path}")
