from supabase import create_client
from dotenv import load_dotenv
load_dotenv()
import os
from datetime import datetime, timedelta

url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_KEY')

supabase = create_client(url, key)
