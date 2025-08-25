from fastapi import APIRouter


router = APIRouter()


@router.get("/healthz", tags=["health"])  # k8s-style
async def healthz():
    return {"status": "ok"}


@router.get("/livez", tags=["health"])  # liveness probe
async def livez():
    return {"status": "ok"}


@router.get("/readyz", tags=["health"])  # readiness probe
async def readyz():
    return {"status": "ok"}

