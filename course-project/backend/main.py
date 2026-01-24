# added a bloilerpalte fastapi server as a starting point created with gemini ai

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = FastAPI(title="FastAPI Backend")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Backend!"}

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Server is running smoothly"}

@app.get("/api")
async def api_root():
    return {"message": "Welcome to the API!"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 5001))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
