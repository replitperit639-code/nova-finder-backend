from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json
import os
from typing import List, Optional

app = FastAPI()

# Enable CORS for the Tauri app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Google Drive folder ID
DRIVE_FOLDER_ID = "1h2eU1fYr7IG4-V9-lFnTG0wVndHFH_ei"

class SearchRequest(BaseModel):
    username: str
    database: Optional[str] = ""

class SearchResult(BaseModel):
    database_name: str
    server_ip: str
    server: str
    ip: str
    password: str
    salts: str
    found: bool

# Mock database for testing - in production this would connect to real databases
MOCK_DATABASES = {
    "daniela55": [
        {
            "database_name": "nigthbox",
            "server_ip": "play.nigthbox.com",
            "server": "nigthbox",
            "ip": "192.168.1.100",
            "password": "hash123456",
            "salts": "0",
            "found": True
        },
        {
            "database_name": "nauticmc",
            "server_ip": "play.nauticmc.com",
            "server": "nauticmc",
            "ip": "192.168.1.101",
            "password": "hash789012",
            "salts": "0",
            "found": True
        }
    ]
}

@app.post("/api/search")
async def search_username(request: SearchRequest):
    """Search for username in all databases"""
    username = request.username.lower()
    
    # Check mock database first
    if username in MOCK_DATABASES:
        return {
            "success": True,
            "username": username,
            "results": MOCK_DATABASES[username],
            "total_found": len(MOCK_DATABASES[username])
        }
    
    # If not in mock, return empty results with available databases
    available_dbs = [
        {"database_name": "nigthbox", "server_ip": "play.nigthbox.com", "server": "nigthbox", "ip": "Nova no encontró", "password": "••••••••", "salts": "0", "found": False},
        {"database_name": "nauticmc", "server_ip": "play.nauticmc.com", "server": "nauticmc", "ip": "Nova no encontró", "password": "••••••••", "salts": "0", "found": False}
    ]
    
    return {
        "success": True,
        "username": username,
        "results": available_dbs,
        "total_found": 0,
        "message": "Usuario no encontrado en las databases"
    }

@app.get("/api/databases")
async def list_databases():
    """List all available databases"""
    try:
        # Try to get list from Google Drive
        list_url = f"https://www.googleapis.com/drive/v3/files?q='{DRIVE_FOLDER_ID}'+in+parents&fields=files(id,name,mimeType)"
        response = requests.get(list_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            files = data.get("files", [])
            databases = []
            
            for file in files:
                name = file.get("name", "")
                if name.endswith(".db") or name.endswith(".json"):
                    clean_name = name.replace(".db", "").replace(".json", "")
                    databases.append({
                        "id": file.get("id"),
                        "name": clean_name,
                        "filename": name,
                        "size": "Unknown"
                    })
            
            return {"success": True, "databases": databases}
        
        # Return default if API fails
        return {
            "success": True,
            "databases": [
                {"name": "nigthbox", "filename": "nigthbox.db"},
                {"name": "nauticmc", "filename": "nauticmc.db"}
            ]
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "databases": [
                {"name": "nigthbox", "filename": "nigthbox.db"},
                {"name": "nauticmc", "filename": "nauticmc.db"}
            ]
        }

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "Nova Finder Backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
