from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials



def upload_to_drive(
    access_token: str,
    file_path: str
):

    creds = Credentials(token=access_token)

    drive_service = build(
        "drive",
        "v3",
        credentials=creds
    )

    file_metadata = {
        "name": file_path.split("/")[-1]
    }

    media = MediaFileUpload(
        file_path,
        mimetype="application/pdf"
    )

    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()

    file_id = file.get("id")

    # PUBLIC ACCESS
    drive_service.permissions().create(
        fileId=file_id,
        body={
            "role": "reader",
            "type": "anyone"
        }
    ).execute()

    file_link = (
        f"https://drive.google.com/file/d/{file_id}/view"
    )

    return file_link


def create_sheet(
    access_token: str,
    company_name: str,
    pdf_link: str
):

    creds = Credentials(token=access_token)

    sheets_service = build(
        "sheets",
        "v4",
        credentials=creds
    )

    spreadsheet = {
        "properties": {
            "title": f"{company_name} Report"
        }
    }

    sheet = sheets_service.spreadsheets().create(
        body=spreadsheet,
        fields="spreadsheetId"
    ).execute()

    spreadsheet_id = sheet.get("spreadsheetId")

    values = [
        ["Company", "PDF Link"],
        [company_name, pdf_link]
    ]

    sheets_service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range="Sheet1!A1",
        valueInputOption="RAW",
        body={
            "values": values
        }
    ).execute()

    sheet_link = (
        f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"
    )

    return sheet_link