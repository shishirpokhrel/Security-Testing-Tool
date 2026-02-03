from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import sys
import os
import subprocess
import json
import asyncio

# Add current directory to path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.nmap_scanner import NmapScanner
from modules.subfinder_module import SubfinderScanner
from modules.bruteforce import BruteForce
from modules.xss_scanner import XSSScanner
import config

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Security Testing Tool API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class NmapRequest(BaseModel):
    target: str
    ports: str = "common"
    nmap_args: Optional[str] = None
    vuln_scan: bool = False

class SubfinderRequest(BaseModel):
    domain: str
    sources: Optional[str] = None

class BruteForceRequest(BaseModel):
    target: str
    protocol: str = Field(..., pattern="^(http-basic|http-form|ssh|ftp)$")
    username_field: Optional[str] = None
    password_field: Optional[str] = None
    usernames: List[str] = []
    passwords: List[str] = []
    success_string: Optional[str] = None
    failure_string: Optional[str] = None

class XSSRequest(BaseModel):
    url: str
    max_payloads: int = 50
    no_forms: bool = False

# Endpoints

@app.get("/")
async def root():
    return {
        "message": "Security Testing Tool API is running",
        "docs": "Visit /docs for API documentation",
        "warning": "This is the API Server. The Web UI runs on a different port (usually 5173).",
        "frontend_url": "http://localhost:5173"
    }

@app.post("/api/scan/nmap")
async def scan_nmap(request: NmapRequest):
    try:
        scanner = NmapScanner()
        # Since these scanners might be blocking, ideally we run them in a thread pool
        # For simplicity, calling directly, but in production use background tasks
        if request.vuln_scan:
            results = await asyncio.to_thread(scanner.vulnerability_scan, request.target, ports=request.ports)
        else:
            nmap_args = request.nmap_args if request.nmap_args else '-sV -sC'
            results = await asyncio.to_thread(scanner.scan_ports, request.target, ports=request.ports, arguments=nmap_args)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/scan/subfinder")
async def scan_subfinder(request: SubfinderRequest):
    try:
        scanner = SubfinderScanner()
        results = await asyncio.to_thread(
            scanner.enumerate_subdomains,
            request.domain,
            sources=request.sources
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/scan/bruteforce")
async def scan_bruteforce(request: BruteForceRequest):
    try:
        bf = BruteForce()
        
        usernames = request.usernames if request.usernames else config.DEFAULT_USERNAMES
        passwords = request.passwords if request.passwords else config.DEFAULT_PASSWORDS
        
        if request.protocol == 'http-basic':
            results = await asyncio.to_thread(bf.http_basic_auth, request.target, usernames, passwords)
        elif request.protocol == 'http-form':
            if not request.username_field or not request.password_field:
                 raise HTTPException(status_code=400, detail="Username and password fields are required for http-form")
            results = await asyncio.to_thread(
                bf.http_form_auth,
                request.target,
                request.username_field,
                request.password_field,
                usernames,
                passwords,
                success_string=request.success_string,
                failure_string=request.failure_string
            )
        elif request.protocol == 'ssh':
             host, port = request.target.split(':') if ':' in request.target else (request.target, 22)
             results = await asyncio.to_thread(bf.ssh_bruteforce, host, int(port), usernames, passwords)
        elif request.protocol == 'ftp':
             host, port = request.target.split(':') if ':' in request.target else (request.target, 21)
             results = await asyncio.to_thread(bf.ftp_bruteforce, host, int(port), usernames, passwords)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown protocol: {request.protocol}")
            
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/scan/xss")
async def scan_xss(request: XSSRequest):
    try:
        scanner = XSSScanner(max_payloads=request.max_payloads)
        results = await asyncio.to_thread(
            scanner.scan_url,
            request.url,
            config.XSS_PAYLOADS_FILE,
            test_forms=not request.no_forms
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
