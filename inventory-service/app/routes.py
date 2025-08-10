
from fastapi import APIRouter

router = APIRouter()

@router.get('/inventory/ping')
def ping():
    return {'pong': 'inventory'}
