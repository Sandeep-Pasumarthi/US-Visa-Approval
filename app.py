from src.constants import APP_HOST, APP_PORT
from src.pipeline.prediction import Data, Classifier

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uvicorn import run

from typing import Optional


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.add_middleware(CORSMiddleware, allow_origins=["*"], 
                   allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])


class DataForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.continent: Optional[str] = None
        self.education_of_employee: Optional[str] = None
        self.has_job_experience: Optional[str] = None
        self.requires_job_training: Optional[str] = None
        self.no_of_employees: Optional[str] = None
        self.company_age: Optional[str] = None
        self.region_of_employment: Optional[str] = None
        self.prevailing_wage: Optional[str] = None
        self.unit_of_wage: Optional[str] = None
        self.full_time_position: Optional[str] = None
    
    async def get_data(self):
        form = await self.request.form()
        self.continent = form.get("continent")
        self.education_of_employee = form.get("education_of_employee")
        self.has_job_experience = form.get("has_job_experience")
        self.requires_job_training = form.get("requires_job_training")
        self.no_of_employees = form.get("no_of_employees")
        self.company_age = form.get("company_age")
        self.region_of_employment = form.get("region_of_employment")
        self.prevailing_wage = form.get("prevailing_wage")
        self.unit_of_wage = form.get("unit_of_wage")
        self.full_time_position = form.get("full_time_position")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("usvisa.html", {"request": request, "context": "Rendering"})

@app.post("/")
async def predict(request: Request):
    form = DataForm(request)
    await form.get_data()
    data = Data(continent=form.continent,
                education_of_employee=form.education_of_employee,
                has_job_experience=form.has_job_experience,
                requires_job_training=form.requires_job_training,
                no_of_employees=form.no_of_employees,
                company_age=form.company_age,
                region_of_employment=form.region_of_employment,
                prevailing_wage=form.prevailing_wage,
                unit_of_wage=form.unit_of_wage,
                full_time_position=form.full_time_position)
    classifier = Classifier()
    result = classifier.predict(data.as_dataframe())[0]

    if result == 1:
        result = "Visa Approved"
    else:
        result = "Visa Denied"
    return templates.TemplateResponse("usvisa.html", {"request": request, "context": result})

if __name__ == "__main__":
    run(app=app, host=APP_HOST, port=APP_PORT)
