import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_required_env(name):
    value = os.getenv(name)
    if value == None : 
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def get_connection():
    return psycopg2.connect(
        host=get_required_env("POSTGRES_HOST"),
        port=get_required_env("POSTGRES_PORT"),
        database=get_required_env("POSTGRES_DB"),
        user=get_required_env("POSTGRES_USER"),
        password=get_required_env("POSTGRES_PASSWORD")
    )