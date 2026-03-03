from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from .core.apenapi import tags_metadata
from .database.database import lifespan
from .endpoints import (auth_router, 
                        user_router, 
                        category_router, 
                        product_router,
                        cart_router,
                        order_router,
                        webhooks)



app = FastAPI(
    title='E-Commerce_FastAPI',
    description="""
    E‑Commerce_FastAPI
    This FastAPI application used by the
    online‑store backend.  The project is intended as a full‑featured

    Features
    --------

    * User registration/login with JWT‑based auth.
    * Role‑aware user management (admin/customer).
    * CRUD for categories and products.
    * Shopping cart: add/remove items, view totals.
    * Order creation/processing and order history.
    * Yookassa payment integration with webhook handling.
    * Database lifespan management (startup/shutdown).
    * Global HTTPException handler returning JSON errors.

    Usage
    -----
    Run with Uvicorn:

    ```bash
    uvicorn app.main:app --reload
    """,
    version='0.1.0',
    openapi_tags=tags_metadata,
    
    lifespan=lifespan
)

#Connecting routers
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(category_router.router)
app.include_router(product_router.router)
app.include_router(cart_router.router)
app.include_router(order_router.router)
app.include_router(webhooks.router)


@app.get('/')
async def root():
    return {'message':'Welcome to E-Commerce_FastAPI'}

@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail': exc.detail}
    )