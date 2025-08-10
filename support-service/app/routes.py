
from fastapi import APIRouter

router = APIRouter()

@router.get('/support/ping')
def ping():
    return {'pong': 'support'}
