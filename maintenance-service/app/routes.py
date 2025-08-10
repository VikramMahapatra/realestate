
from fastapi import APIRouter

router = APIRouter()

@router.get('/maintenance/ping')
def ping():
    return {'pong': 'maintenance'}
