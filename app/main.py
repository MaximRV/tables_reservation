from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI
from starlette.responses import RedirectResponse
from uvicorn import lifespan

from app.routers.tables import router as router_tables
from app.routers.reservations import router as router_reservation

app = FastAPI(title="Резервирование Столиков",
              version="0.1.0",
              root_path="/api",
              )

origins = [
    "http://localhost:3000",
]

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

# Подключение роутеров
app.include_router(router_reservation, prefix="/api", tags=["reservations"])
app.include_router(router_tables, prefix="/api", tags=["tables"])

# Подключение версионирования
app = VersionedFastAPI(
    app,
    version_format="{major}",
    prefix_format="/api/v{major}",
    )


@app.get("/")
def read_root():
    return RedirectResponse(url="/api/v1/docs")
