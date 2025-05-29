from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(prefix="/report", tags=["Reports"])

@router.get("/pdf/{applicant_id}")
async def download_pdf(applicant_id: str):
    # TODO: Logic to locate PDF file path
    file_path = f"./reports/{applicant_id}.pdf"
    return FileResponse(file_path, media_type="application/pdf", filename=f"{applicant_id}_report.pdf")

@router.get("/excel")
async def download_excel():
    # TODO: Logic to locate Excel summary file
    file_path = "./reports/interview_summary.xlsx"
    return FileResponse(file_path, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename="interview_summary.xlsx")
