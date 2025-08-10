
from fastapi import APIRouter

router = APIRouter()

@router.get('/property/ping')
def ping():
    return {'pong': 'property'}
