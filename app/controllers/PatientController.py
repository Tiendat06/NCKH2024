from flask import request, render_template
from models.Patient import PatientModel

class PatientController:
    def __init__(self):
        self.patient_model = PatientModel();

    def index(self, pages):
        patient_db = self.patient_model;
        pages = int(pages);
        per_page = 8;
        start = (pages - 1) * per_page;
        end = start + per_page

        patient_list = []
        patient_list = patient_db.getAllPatient();

        total_pages = (len(patient_list) + per_page - 1) // per_page
        items_on_page = patient_list[start: end]
        return render_template("index.html", content='index', page='patient', patient_list=items_on_page, total_pages=total_pages, pages=pages)
