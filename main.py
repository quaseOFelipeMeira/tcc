from fastapi import FastAPI
from core.database import engine
from core.models import Base

from routers import v1

from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Tooling Management API",
    # terms_of_service="http://google.com",
    # contact={
    #     "Developer name": "Felipe Meira",
    #     "email": "felipecmeira2004@gmail.com",
    # },
    # license_info={
    #     "name": "XZY",
    #     "url": "http://google.com",
    # },
    # docs_url="/docs",
    redoc_url=None,
)


app.include_router(v1.router)
add_pagination(app)

Base.metadata.create_all(engine)

# uvicorn main:app --reload --port 8000

# Allow requests from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
