from dotenv import load_dotenv
import os
from supabase import create_client

# Load your .env file
load_dotenv()

# Read the keys
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

# Connect to Supabase
supabase = create_client(url, key)

print("Connection successful!")
print(f"Connected to: {url}")