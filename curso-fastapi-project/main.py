import zoneinfo

from datetime import datetime

from fastapi import FastAPI


app = FastAPI()

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
}


@app.get("/time/{iso_code}")
async def time(iso_code: str):

   # Convert to uppercase to match keys in the dictionary
    iso = iso_code.upper()
 #  Get the timezone string from the dictionary
    timezone_str = country_timezones.get(iso)

    tz = zoneinfo.ZoneInfo(timezone_str)

    return {"time": datetime.now(tz)}