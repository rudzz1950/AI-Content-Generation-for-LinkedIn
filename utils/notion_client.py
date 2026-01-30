from notion_client import Client
import os
from datetime import datetime
from config import NOTION_DATABASE_ID

class NotionPostSaver:
    def __init__(self):
        token = os.getenv("NOTION_API_TOKEN")
        if not token:
            print("Warning: NOTION_API_TOKEN not set. Notion saving disabled.")
            self.client = None
        else:
            self.client = Client(auth=token)
            self.database_id = NOTION_DATABASE_ID

    def save_post(self, title: str, content: str, topic: str, url: str):
        """Save to Notion (auto-detects Database vs Page)."""
        if not self.client or not self.database_id:
            return None
            
        try:
            # 1. Try to fetch as Database
            is_db = False
            try:
                self.client.databases.retrieve(self.database_id)
                is_db = True
            except:
                pass # Not a DB or no access, assume Page handling or fail later
                
            if is_db:
                # Original Database Logic
                print(f"--- DEBUG: Saving to Database {self.database_id} ---")
                response = self.client.pages.create(
                    parent={"database_id": self.database_id},
                    properties={
                        "Name": {"title": [{"text": {"content": title}}]},
                        "Topic": {"select": {"name": topic}},
                        "Source URL": {"url": url},
                        "Date": {"date": {"start": datetime.now().isoformat()}},
                        "Status": {"status": {"name": "Draft"}}
                    },
                    children=[
                        {
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": [{"type": "text", "text": {"content": content[:2000]}}] # Truncate block limit
                            }
                        }
                    ]
                )
                print(f"Saved to Notion Database: {response['url']}")
                return response['url']
            
            else:
                # Page Append Logic
                print(f"--- DEBUG: target ID seems to be a PAGE. Appending content... ---")
                # Create a toggle header for the new post
                response = self.client.blocks.children.append(
                    block_id=self.database_id,
                    children=[
                        {
                            "object": "block",
                            "type": "heading_2",
                            "heading_2": {
                                "rich_text": [{"type": "text", "text": {"content": f"Draft: {title}"}}]
                            }
                        },
                        {
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": [
                                    {"type": "text", "text": {"content": f"Topic: {topic}\nURL: {url}\nDate: {datetime.now().isoformat()}\n\n"}}
                                ]
                            }
                        },
                        {
                            "object": "block",
                            "type": "code",
                            "code": {
                                "language": "markdown",
                                "rich_text": [{"type": "text", "text": {"content": content[:2000]}}]
                            }
                        },
                        {
                            "object": "block",
                            "type": "divider",
                            "divider": {}
                        }
                    ]
                )
                # Notion Append returns a list of blocks, not the page URL directly
                # We construct the URL manually or from context
                page_url = f"https://notion.so/{self.database_id.replace('-', '')}"
                print(f"Appended to Notion Page: {page_url}")
                return page_url

        except Exception as e:
            print(f"Failed to save to Notion: {e}")
            return None
