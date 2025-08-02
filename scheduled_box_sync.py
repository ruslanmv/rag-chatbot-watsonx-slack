import schedule
import time
import subprocess
from sync_and_import import sync_box_and_create_kb

def update_knowledge_base():
    """Update knowledge base with latest Box documents"""
    try:
        print("Starting scheduled Box sync...")
        config_path = sync_box_and_create_kb()
        
        if config_path:
            # Re-import knowledge base with updated documents
            result = subprocess.run([
                "orchestrate", "knowledge-bases", "import", 
                "-f", config_path
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("Knowledge base updated successfully!")
            else:
                print(f"Error updating knowledge base: {result.stderr}")
                
    except Exception as e:
        print(f"Error during scheduled sync: {e}")

# Schedule sync every 6 hours
schedule.every(6).hours.do(update_knowledge_base)

print("Box sync scheduler started. Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
