import os
from dotenv import load_dotenv
from supabase import create_client, Client

# This command looks for the .env file and loads its content
load_dotenv()

# We tell Python the NAME of the keys to find in the .env file
url: str = os.environ.get("SUPABASE_URL") 
key: str = os.environ.get("SUPABASE_KEY")

# Safety check: if one is missing, the code will tell you why
if not url or not key:
    print("❌ Error: SUPABASE_URL or SUPABASE_KEY not found in .env")

# This creates the actual connection to your cloud database
supabase: Client = create_client(url, key)