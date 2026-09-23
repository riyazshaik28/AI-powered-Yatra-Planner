from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.planner import router as planner_router
from app.routes.stream import router as stream_router
app = FastAPI(
    title="Yatra Planner",
    description="""
    Yatra Planner is a travel data aggregation platform that integrates multiple external services,
    including Weather, Places, and Currency APIs. The system provides both RESTful endpoints and
    real-time updates through Server-Sent Events (SSE), enabling travelers to access live,
    accurate, and centralized travel information efficiently.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(planner_router)
app.include_router(stream_router)
@app.get("/")
async def root():
    return{
"message": "Welcome to Yatra planner!",
"version": "1.0.0",
 "endpoints":{
     "post /plan": "Create a new travel plan(aggreate the data from the user and provide a travel plan)",
     "GET /plan/{plan_id}": "stream a travel plan by its ID",
     "GET/plan/cache-stats": "Get cache statistics for travel plans",
     "DELETE/plan/cache":
    "Clear the cache for travel plans"

 }
    }