from fastapi import FastAPI

import uvicorn
from src.shelters import router as shelter_router
from src.cats import router as cat_router
from src.dogs import router as dog_router
from src.auth import router as auth_router

app = FastAPI()
app.include_router(shelter_router)
app.include_router(cat_router)
app.include_router(dog_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
