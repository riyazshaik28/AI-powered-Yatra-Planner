from fastapi import FastAPI

app=FastAPI(
    title="Yatra planner",
    description="Yatra planner is a web application that helps users plan their trips and vacations. It provides features such as itinerary planning, budget tracking, and travel recommendations.",
    version="1.0.0",
    redoc_url="/docs",
    docs_url="/redoc",
)


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