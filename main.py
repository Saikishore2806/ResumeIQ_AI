from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from reportlab.pdfgen import canvas
from parser import parse_resume
from scorer import score_resume
from feedback import generate_feedback
import shutil
import os

app = FastAPI()
latest_report_data = {}

UPLOAD_FOLDER = "uploads"
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request
        }
    )


@app.post("/upload-resume/")
async def upload_resume(
    request: Request,
    file: UploadFile = File(...),
    target_role: str = Form(...)
):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Step 1: Parse Resume
    parsed_data = parse_resume(file_path)

    if "error" in parsed_data:
        return {
            "error": "Unsupported file format"
        }

    # Step 2: Score Resume
    score_data = score_resume(parsed_data, target_role)

    # Step 3: Generate Feedback
    feedback_data = generate_feedback(parsed_data, score_data)

    global latest_report_data
    latest_report_data = {
    "score_data": score_data,
    "feedback_data": feedback_data,
    "parsed_data": parsed_data
    }
    return templates.TemplateResponse(
    request,
    "result.html",
    {
        "request": request,
        "parsed_data": parsed_data,
        "score_data": score_data,
        "feedback_data": feedback_data
    }
)

@app.get("/download-report/")
def download_report():
    global latest_report_data

    file_path = "resume_report.pdf"

    if not latest_report_data:
        file_path = "empty_report.pdf"
        c = canvas.Canvas(file_path)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(180, 800, "Resume Analysis Report")
        c.setFont("Helvetica", 12)
        c.drawString(50, 760, "No resume analysis found yet.")
        c.save()

        return FileResponse(
            path=file_path,
            filename="Resume_Analysis_Report.pdf",
            media_type="application/pdf"
        )

    score_data = latest_report_data["score_data"]
    feedback_data = latest_report_data["feedback_data"]

    final_score = score_data.get("Final Resume Score", 0)
    ats_score = score_data.get("ATS Score", 0)
    target_role = score_data.get("Target Role", "Not Specified")
    matched_skills = score_data.get("Matched Skills", [])
    missing_skills = score_data.get("Missing Skills", [])

    if final_score >= 85:
        status = "Excellent Resume"
    elif final_score >= 70:
        status = "Good Resume"
    elif final_score >= 55:
        status = "Average Resume"
    else:
        status = "Needs Improvement"

    c = canvas.Canvas(file_path)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(170, 800, "Resume Analysis Report")

    c.setFont("Helvetica", 12)
    y = 760

    c.drawString(50, y, f"Target Role: {target_role}")
    y -= 25

    c.drawString(50, y, f"Final Resume Score: {final_score}/100")
    y -= 25

    c.drawString(50, y, f"ATS Score: {ats_score}/10")
    y -= 25

    c.drawString(50, y, f"Resume Status: {status}")
    y -= 40

    c.drawString(50, y, "Matched Skills:")
    y -= 20

    for skill in matched_skills:
        c.drawString(70, y, f"- {skill}")
        y -= 18

    y -= 10

    c.drawString(50, y, "Missing Skills:")
    y -= 20

    for skill in missing_skills:
        c.drawString(70, y, f"- {skill}")
        y -= 18

    y -= 10

    c.drawString(50, y, "Suggestions:")
    y -= 20

    for item in feedback_data:
        c.drawString(70, y, f"- {str(item)[:80]}")
        y -= 18

    c.save()

    return FileResponse(
        path=file_path,
        filename="Resume_Analysis_Report.pdf",
        media_type="application/pdf"
    )
