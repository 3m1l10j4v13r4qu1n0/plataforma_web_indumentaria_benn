from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.infrastructure.core.config import settings
from app.presentation.handlers import register_exception_handlers

# routers
from app.presentation.routers.auth_router import router as auth_router
from app.presentation.routers.cambio_router import router as cambio_router
from app.presentation.routers.dashboard_router import router as dashboard_router
from app.presentation.routers.descuento_router import router as descuento_router
from app.presentation.routers.producto_router import router as producto_router
from app.presentation.routers.venta_router import router as venta_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Eventos de inicio y cierre de la aplicación
    Reemplaza el deprecado @app.on_event("startup")
    """
    # ── Inicio ──────────────────────────────────────
    print(f"🚀 Iniciando {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"🔧 Modo DEBUG: {settings.DEBUG}")
    yield
    # ── Cierre ──────────────────────────────────────
    print("👋 Cerrando aplicación")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    description="""
    API REST Plataforma Web Indumentaria BENN
    """,
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Handlers de errores ──────────────────────────────────────────────
register_exception_handlers(app)

# ── Routers ──────────────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(producto_router)
app.include_router(venta_router)
app.include_router(descuento_router)
app.include_router(cambio_router)
app.include_router(dashboard_router)


# ── Health check ─────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
async def health_check():
    return {
        "estado": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }
