import asyncio
import sys
import uvicorn
from pyngrok import ngrok
from dotenv import load_dotenv
import os

def run_ngrok():
    # Load environment variables from .env
    load_dotenv()
    auth_token = os.getenv("NGROK_AUTH_TOKEN")
    
    if not auth_token:
        print("--- NGROK SETUP ---")
        print("To get a long-lasting link, visit https://dashboard.ngrok.com/get-started/your-authtoken")
        auth_token = input("Enter your ngrok AuthToken (or leave blank for temporary session): ").strip()
        # Clean up if user pasted the whole line from .env
        if auth_token.startswith("NGROK_AUTH_TOKEN="):
            auth_token = auth_token.replace("NGROK_AUTH_TOKEN=", "")
    
    if auth_token:
        ngrok.set_auth_token(auth_token)
    
    # Open a HTTP tunnel on port 8000
    public_url = ngrok.connect(8000).public_url
    print(f"\n🚀 PUBLIC URL: {public_url}")
    print(f"📄 DOCUMENTATION: {public_url}/docs\n")
    
    # Run the uvicorn server
    uvicorn.run("api:app", host="127.0.0.1", port=8000, log_level="info")

if __name__ == "__main__":
    try:
        run_ngrok()
    except KeyboardInterrupt:
        print("\nStopping server...")
        ngrok.kill()
