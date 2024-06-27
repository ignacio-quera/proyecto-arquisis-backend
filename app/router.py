from fastapi import APIRouter
from app.routes.flights import router as flights_router
from app.routes.tickets import router as tickets_router
from app.routes.geolocation import router as geolocation_router
from app.routes.predictions import router as predictions_router
from app.routes.purchases import router as purchases_router
from app.routes.workers import router as workers_router
from app.routes.admintickets import router as admin_tickets_router
from app.routes.adminpurchases import router as admin_purchases_router
from app.routes.auctions import router as auctions_router
router = APIRouter()

router.include_router(flights_router, tags=["flights"], prefix="/flights")
router.include_router(tickets_router, tags=["tickets"], prefix="/tickets")
router.include_router(purchases_router, tags=["purchases"], prefix="/purchases")
router.include_router(geolocation_router, tags=["geolocation"], prefix="/geolocation")
router.include_router(predictions_router, tags=["predictions"], prefix="/predictions")
router.include_router(workers_router, tags=["workers"], prefix="/workers")
router.include_router(admin_tickets_router, tags=["admintickets"], prefix="/admintickets")
router.include_router(admin_purchases_router, tags=["adminpurchases"], prefix="/adminpurchases")
router.include_router(auctions_router, tags=["auctions"], prefix = "/auctions")