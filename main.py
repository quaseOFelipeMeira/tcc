from fastapi import FastAPI
from core.database import engine
from core.models import Base

from routers import v1


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

Base.metadata.create_all(engine)

# uvicorn main:app --reload --port 8000

if __name__ == '__main__':
    import uvicorn
    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)