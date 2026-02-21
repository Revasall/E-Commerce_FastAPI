from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from .database.database import lifespan
from .endpoints import (auth_router, 
                        user_router, 
                        category_router, 
                        product_router,
                        cart_router)



app = FastAPI(
    title='E-Commerce_FastAPI',
    description='An online store API with implemented authorization, a shopping cart, and service, and Stripe',
    version='1.0.0',
    lifespan=lifespan
)

#Connecting routers
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(category_router.router)
app.include_router(product_router.router)
app.include_router(cart_router.router)


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