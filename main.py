import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api import api_router

origins = [
    '*'
]


class BetMakerApp(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


app = BetMakerApp()
app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host='0.0.0.0', port=8000)
