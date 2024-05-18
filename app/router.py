from fastapi import APIRouter
from app.routes.flights import router as flights_router
from app.routes.tickets import router as tickets_router
from app.routes.geolocation import router as geolocation_router
from app.routes.predictions import router as predictions_router
from app.routes.purchases import router as purchases_router
router = APIRouter()

router.include_router(flights_router, tags=["flights"], prefix="/flights")
router.include_router(tickets_router, tags=["tickets"], prefix="/tickets")
router.include_router(purchases_router, tags=["purchases"], prefix="/purchases")
router.include_router(geolocation_router, tags=["geolocation"], prefix="/geolocation")
router.include_router(predictions_router, tags=["predictions"], prefix="/predictions")