import time
import uuid
from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# ---------------------------------------------------------
# 1. CORS Middleware Configuration
# ---------------------------------------------------------
# Strictly allow only your assigned origin (No wildcards '*')
ALLOWED_ORIGIN = "https://dash-j0c4z9.example.com"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# 2. Custom Middleware for Required Headers
# ---------------------------------------------------------
@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    start_time = time.perf_counter()
    
    # Process the request
    response = await call_next(request)
    
    # Calculate duration
    process_time = time.perf_counter() - start_time
    
    # Inject required headers into every response
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{process_time:.6f}"
    
    return response

# ---------------------------------------------------------
# 3. GET /stats Endpoint
# ---------------------------------------------------------
@app.get("/stats")
async def get_stats(values: str = Query(..., description="Comma-separated integers")):
    try:
        # Parse the comma-separated string into a list of integers
        num_list = [int(x.strip()) for x in values.split(",") if x.strip()]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid integer format in values parameter.")
    
    if not num_list:
        raise HTTPException(status_code=400, detail="Values list cannot be empty.")
    
    # Compute Descriptive Statistics
    count = len(num_list)
    total_sum = sum(num_list)
    minimum = min(num_list)
    maximum = max(num_list)
    mean = total_sum / count

    # Return required JSON structure with your exact email
    return {
        "email": "24f2000456@ds.study.iitm.ac.in", 
        "count": count,
        "sum": total_sum,
        "min": minimum,
        "max": maximum,
        "mean": round(mean, 4)  # Easily satisfies the ±0.01 precision limit
    }
