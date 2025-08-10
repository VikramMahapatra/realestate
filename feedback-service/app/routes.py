
from fastapi import APIRouter

router = APIRouter()

@router.get('/feedback/ping')
def ping():
    return {'pong': 'feedback'}
