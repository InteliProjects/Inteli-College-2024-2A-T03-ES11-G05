from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middlewares import exception_handler_middleware
from controllers import EndPointsRouter
from configs.logging import Logger

app = FastAPI()

logger = Logger(
    log_group="cosmeticoders-api",
    log_stream="health-route",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.add_middleware(exception_handler_middleware.ExceptionHandlerMiddleware)
app.include_router(EndPointsRouter)

@app.get("/health")
def health():
    logger.log("error", "Health check done!")
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}