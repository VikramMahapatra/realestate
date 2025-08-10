
from fastapi import APIRouter

router = APIRouter()

@router.get('/auth/ping')
def ping():
    return {'pong': 'auth'}
