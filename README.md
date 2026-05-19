# AI Report Generator

An AI-powered business audit platform that researches companies, generates detailed audit reports using Gemini AI, converts them into professional PDFs, uploads them to Google Drive, stores metadata in Google Sheets, and provides downloadable report links.

---

# Features

- Google Authentication using NextAuth
- AI-powered business analysis
- Company research pipeline
- Gemini AI report generation
- Professional PDF generation
- Google Drive PDF uploads
- Google Sheets integration
- Modern Next.js frontend
- FastAPI backend
- Jinja2 HTML templating
- Playwright PDF rendering

---

# Architecture

```txt
Next.js Frontend
        ↓
Google OAuth (NextAuth)
        ↓
Access Token
        ↓
FastAPI Backend
        ↓
Company Research Pipeline
        ↓
Gemini AI Report Generation
        ↓
Jinja2 HTML Template
        ↓
Playwright PDF Generation
        ↓
Google Drive Upload
        ↓
Google Sheets Storage
        ↓
Return Report Links
```

---

# Tech Stack

## Frontend

- Next.js
- TypeScript
- Tailwind CSS
- NextAuth.js

## Backend

- Python
- FastAPI
- Gemini AI
- Jinja2
- Playwright

## Google Services

- Google OAuth
- Google Drive API
- Google Sheets API

---

# Project Structure

```txt
AI-INTERN/
│
├── backend/
│
├── frontend/
│
├── templates/
│     └── report_template.html
│
├── outputs/
│
├── ai/
│     └── scrapping/
│
├── report.py
├── pdf.py
├── google_services.py
├── main.py
│
├── requirements.txt
└── README.md
```

---

# Setup Instructions

# 1. Clone Repository

```bash
git clone <your-repo-url>
```

---

# 2. Frontend Setup

```bash
cd frontend
npm install
```

Create:

```txt
.env.local
```

Add:

```env
GOOGLE_CLIENT_ID=YOUR_CLIENT_ID
GOOGLE_CLIENT_SECRET=YOUR_CLIENT_SECRET
NEXTAUTH_SECRET=YOUR_SECRET
NEXTAUTH_URL=http://localhost:3000
```

Run frontend:

```bash
npm run dev
```

---

# 3. Backend Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Playwright:

```bash
playwright install
```

Create:

```txt
.env
```

Add:

```env
GEMINI_API_KEY=YOUR_GEMINI_KEY
```

Run backend:

```bash
uvicorn main:app --reload
```

---

# Google Cloud Setup

Enable these APIs:

- Google Drive API
- Google Sheets API

Add OAuth Redirect URI:

```txt
http://localhost:3000/api/auth/callback/google
```

---

# PDF Generation Flow

```txt
Gemini JSON Report
        ↓
Jinja2 HTML Rendering
        ↓
Playwright PDF Generation
        ↓
Professional PDF Output
```

---

# Google Integration Flow

```txt
User Login
      ↓
Google Access Token
      ↓
Upload PDF to Drive
      ↓
Create Google Sheet
      ↓
Return Shareable Links
```

---

# API Endpoint

## Generate Report

```http
POST /generate-report
```

### Request Body

```json
{
  "company": "Notion",
  "accessToken": "google_access_token"
}
```

### Response

```json
{
  "success": true,
  "pdfLink": "https://drive.google.com/...",
  "sheetLink": "https://docs.google.com/..."
}
```

---


# Current Status

- Google Authentication 
- Gemini AI Reports 
- PDF Generation 
- Google Drive Upload 
- Google Sheets Integration 
- Frontend Dashboard 

---

# Author

Built as a full-stack AI automation platform using:
- Next.js
- FastAPI
- Gemini AI
- Playwright
- Google APIs

Architecture workflow 
First of all the user comes to the login page and then we get the access token using the google auth then we move to the backend where this is the scrapping layer which generates the repost then using api we save it to the google drive and google sheets 
the backend is the simple fastapi backend which is has the routes which are hit by the frontend.
