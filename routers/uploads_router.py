from fastapi import APIRouter, UploadFile, File, HTTPException
from datetime import datetime
import shutil
import os

router = APIRouter(prefix="/upload", tags=["Uploads"])

@router.post("/excel")
async def upload_excel(file: UploadFile = File(...)):
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="지원되지 않는 파일 형식입니다.")

    upload_dir = "./uploads/interviewees"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, f"{datetime.now().strftime('%Y-%m-%d')}_{file.filename}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "파일이 성공적으로 업로드되었습니다.",
        "file_path": file_path,
        "file_name": file.filename,
        "upload_time": datetime.utcnow().isoformat() + "Z"
    }
