from fastapi import APIRouter, Depends
from security import api_key_scheme, custom_header

router = APIRouter(prefix="/headers", tags=["Headers Test"])

@router.get("/test/")
def read_headers(
    my_header: str = Depends(api_key_scheme),
    another_header: str = Depends(custom_header)
):
    return {
        "My-Header": my_header,
        "Another-Header": another_header
    }
