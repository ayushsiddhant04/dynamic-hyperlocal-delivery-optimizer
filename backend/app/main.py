from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes.health import router as health_router
from app.api.routes.optimization import router as optimization_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Backend API engine for RouteFlow — Dynamic Hyperlocal Delivery Optimizer",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Configuration for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routers
app.include_router(health_router, prefix=settings.API_V1_PREFIX)
app.include_router(optimization_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    """Root entrypoint returning basic service information."""
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online",
        "documentation": "/docs",
        "health_check": f"{settings.API_V1_PREFIX}/health",
        "system_status": f"{settings.API_V1_PREFIX}/status",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
    )
