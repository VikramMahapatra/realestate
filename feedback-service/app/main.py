
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router as api_router\n\napp = FastAPI(title="feedback-service")

app.include_router(api_router, prefix='')\n\napp.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/healthz')
def healthz():
    return {'status':'ok','service':'feedback'})

@app.get('/ready')
def ready():
    return {'ready': True}
