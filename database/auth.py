from supabase import create_client
from dotenv import load_dotenv
load_dotenv()
import os
from datetime import datetime, timedelta

# from gotrue.exceptions import APIError

url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_KEY')

supabase = create_client(url, key)

data = (
    supabase
    .table("todos")
    .select("*")
    .execute()
)

print(f"Data before sign in : {data}")

# Create a random user login email and password.
random_email: str = "arunthiru77@gmail.com"
random_password: str = "test_password_123"
# user = supabase.auth.sign_up({ "email": random_email, "password": random_password })

session = None

try:
    session = supabase.auth.sign_in_with_password({ "email": random_email, "password": random_password })
    print('Login Success')
    print(session.session.access_token)
except Exception as e:
    print(e)
    print('Login Failed')

supabase.postgrest.auth(session.session.access_token)  

data = (
    supabase
    .table("todos")
    .select("*")
    .execute()
)

print(f"Data after sign in : {data}")

supabase.auth.sign_out()