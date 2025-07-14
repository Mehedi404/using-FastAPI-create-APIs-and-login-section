# routers/file_routes.py

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pathlib import Path
import shutil
import uuid
from auth.jwt_auth import get_current_user


from db import get_db
from models.file_upload import FileUpload

router = APIRouter(prefix="/files", tags=["Files"])

MEDIA_PATH = Path("media")
MEDIA_PATH.mkdir(exist_ok=True)  # ensure folder exists

@router.post("/upload", summary="Upload a file and save to DB")
def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    file_ext = file.filename.split('.')[-1].lower()
    allowed = {"pdf", "jpg", "jpeg", "png", "xlsx", "xls", "docx"}
    if file_ext not in allowed:
        raise HTTPException(status_code=400, detail="File type not allowed")

    filename = f"{uuid.uuid4()}.{file_ext}"
    filepath = MEDIA_PATH / filename

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Save file metadata in DB
    upload_record = FileUpload(
        filename=filename,
        original_name=file.filename,
        user_id=current_user.id

    )
    db.add(upload_record)
    db.commit()
    db.refresh(upload_record)

    return {
        "id": upload_record.id,
        "filename": upload_record.filename,
        "original_name": upload_record.original_name,
        "url": f"/files/download/{filename}"
    }

@router.get("/download/{filename}", summary="Download a file")
def download_file(
    filename: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    filepath = MEDIA_PATH / filename
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=filepath, filename=filename)



@router.get("/my-uploads", summary="List my uploaded files")
def my_uploads(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    uploads = db.query(FileUpload).filter(FileUpload.user_id == current_user.id).all()

    return uploads