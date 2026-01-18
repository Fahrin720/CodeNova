import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from .env
load_dotenv()

url: str = os.environ.get(https://nmsfqfbjrebhllwsxpee.supabase.co)
key: str = os.environ.get(sb_publishable_3w7pPF3j12aZ9og_PoPP4Q_z74l1ERT)

# Create the Supabase client
supabase: Client = create_client(url, key)