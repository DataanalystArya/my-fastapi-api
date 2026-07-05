import time
import uuid
from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 1. CORS Policy Settings
ALLOWED_ORIGIN = "https://dash-j0c4z9.example.com"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://dash-j0c4z9.example.com"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Required Headers Middleware (X-Request-ID and X-Process-Time)
@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    start_time = time.perf_counter()
    
    response = await call_next(request)
    
    process_time = time.perf_counter() - start_time
    
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{process_time:.6f}"
    
    return response

# 3. GET /stats Endpoint
@app.get("/stats")
async def get_stats(values: str = Query(..., description="Comma-separated integers")):
    try:
        num_list = [int(x.strip()) for x in values.split(",") if x.strip()]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid integer format.")
    
    if not num_list:
        raise HTTPException(status_code=400, detail="Values cannot be empty.")
    
    count = len(num_list)
    total_sum = sum(num_list)
    minimum = min(num_list)
    maximum = max(num_list)
    mean = total_sum / count

    return {
        "email": "24f2000456@ds.study.iitm.ac.in", 
        "count": count,
        "sum": total_sum,
        "min": minimum,
        "max": maximum,
        "mean": round(mean, 4)
    }
