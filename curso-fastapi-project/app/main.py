import zoneinfo

from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI , HTTPException 
from datetime import datetime



from db import create_all_tables
from routers import customers , transactions , invoices , plans



# 2. Define the lifespan wrapper
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This happens ON STARTUP
    create_all_tables() 
    print("Database tables initialized!")
    yield
    # This happens ON SHUTDOWN (if you need to close connections)

# 3. Pass the wrapper to FastAPI
app = FastAPI(lifespan=create_all_tables)

app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(invoices.router)
app.include_router(plans.router)



@app.get("/")
async def root():
    return {"message": "Hello, Andres!"}

# Dictionary mapping ISO country codes to timezone strings
country_timezones = {
    "US": "America/New_York",
    "GB": "Europe/London",
    "IN": "Asia/Kolkata",
    "JP": "Asia/Tokyo",
    "AU": "Australia/Sydney",
    "CO": "America/Bogota",
}


@app.get("/time/{iso_code}")
async def time(iso_code: str):

   # Convert to uppercase to match keys in the dictionary
    iso = iso_code.upper()
 #  Get the timezone string from the dictionary
    timezone_str = country_timezones.get(iso)

    tz = zoneinfo.ZoneInfo(timezone_str)

    return {"time": datetime.now(tz)}






@app.get("/convert-time")
def convert_time_format(time_str: str):
    """
    Endpoint to convert a 12-hour time string to 24-hour format.
    Example input: '03:30 PM' -> Output: '15:30'
    """
    try:
        # 1. Parse the string into a datetime object
        # %I is 12h clock, %M is minutes, %p is AM/PM
        time_obj = datetime.strptime(time_str, "%I:%M %p")
        
        # 2. Format the object into a 24-hour string
        # %H is 24h clock
        time_24h = time_obj.strftime("%H:%M")
        
        return {
            "original": time_str,
            "converted_24h": time_24h
        }
    except ValueError:
        # 3. If the format doesn't match '00:00 AM/PM', raise an error
        raise HTTPException(
            status_code=400, 
            detail="Invalid time format. Please use 'HH:MM AM/PM' (e.g., 03:30 PM)"
        )

# Endpoint that returns both current time and converted time.
@app.get("/current-time")
def convert_time_format(time_str: str):

    time_obj = datetime.strptime(time_str, "%I:%M %p")
    converted_time = time_obj.strftime("%I:%M %p")

    now_obj =  datetime.now()

    current_time_24h = now_obj.strftime("%Y-%m-%d %H:%M:%S")
    return {
        "converted_time": converted_time,
        "current_time": current_time_24h
        }


# To run this:
# fastapi dev main.py