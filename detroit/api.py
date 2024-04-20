import geojson

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")

with open("./static/detroit_placekeys.geojson") as f:
    geo = geojson.load(f)

@app.get("/geojson")
def get_geojson():
    features = geo[:1]
    return geojson.dumps(features)