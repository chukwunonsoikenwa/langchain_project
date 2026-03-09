from dotenv import load_dotenv
import os

load_dotenv()
print("TAVILY_API_KEY =", os.getenv("TAVILY_API_KEY"))
