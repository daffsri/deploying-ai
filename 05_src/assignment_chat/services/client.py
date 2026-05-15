import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv("../../05_src/.secrets")

if OpenAI is None:
    raise RuntimeError("The openai package is not installed.")
if not os.getenv("API_GATEWAY_KEY"):
    raise RuntimeError("API_GATEWAY_KEY is not set.")

client = OpenAI(
    base_url="https://k7uffyg03f.execute-api.us-east-1.amazonaws.com/prod/openai/v1",
    api_key="any value",
    default_headers={"x-api-key": os.getenv("API_GATEWAY_KEY")}
)