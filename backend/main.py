import asyncio
from aio_pika import connect_robust
from aio_pika.patterns import RPC

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from router import user, dataset, task, base_router
from settings import allow_cors_origins, RABBITMQ_URI
from rpc.router import rpc_router_start_training, rpc_router_finish_training
from cache.redis import init_redis_pool
# create database table, skip this if there already has one
# entity.Base.metadata.create_all(bind=engine)

# app = FastAPI(docs_url='/api/v1/docs')
app = FastAPI(docs_url='/api/v1/docs')
app.include_router(base_router.router, prefix="/api/v1")
app.include_router(user.router, prefix="/api/v1")
app.include_router(dataset.router, prefix="/api/v1")
app.include_router(task.router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_cors_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.middleware("http")
async def rpc_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        # You can also pass a loop as an argument. Keep it here now for simplicity
        loop = asyncio.get_event_loop()
        connection = await connect_robust(host=RABBITMQ_URI, port=5672, loop=loop)
        channel = await connection.channel()
        request.state.rpc = await RPC.create(channel)
        response = await call_next(request)
    finally:

        # UPD: just thought that we probably want to keep queue and don't
        # recreate it for each request so we can remove this line and move
        # connection, channel and rpc initialisation out from middleware 
        # and do it once on app start

        # Also based of this: https://github.com/encode/starlette/issues/1029
        # it's better to create ASGI middleware instead of HTTP
        await request.state.rpc.close()
    return response

@app.on_event('startup')
def startup():
    loop = asyncio.get_event_loop()
    # use the same loop to consume
    asyncio.ensure_future(rpc_router_start_training(loop=loop))
    asyncio.ensure_future(rpc_router_finish_training(loop=loop))

@app.on_event('startup')
async def startup_redis():
    print("Redis Startup Conenct")
    redis = await init_redis_pool()
    
    app.state.redis = redis

@app.on_event("shutdown")
async def shutdown_event():
    await app.state.redis.close()