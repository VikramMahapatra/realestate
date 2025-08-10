
from fastapi import APIRouter

router = APIRouter()

@router.get('/brokerage/ping')
def ping():
    return {'pong': 'brokerage'}
