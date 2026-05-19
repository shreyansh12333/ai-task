from fastapi import FastAPI
from pydantic import BaseModel
import os 
import sys
from fastapi.middleware.cors import CORSMiddleware

from google_services import (
    upload_to_drive,
    create_sheet
)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ai.report import generate_report

from pdf_generator import generate_pdf



from ai.scrapping.pipeline import research


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ReportRequest(BaseModel):
    company: str
    accessToken: str



@app.post("/generate-report")
def generate_report_api(data: ReportRequest):

    try:

       
        company_data = research(data.company)

        if not company_data:
            return {
                "success": False,
                "message": "Company research failed"
            }

       
        report = generate_report(company_data)

        if not report:
            return {
                "success": False,
                "message": "AI report generation failed"
            }

      
        pdf_path = generate_pdf(
            report,
            data.company
        )

      
        pdf_link = upload_to_drive(
            data.accessToken,
            pdf_path
        )

      
        sheet_link = create_sheet(
            data.accessToken,
            data.company,
            pdf_link
        )

        return {
            "success": True,
            "pdfLink": pdf_link,
            "sheetLink": sheet_link
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }