from flask import Blueprint
from controllers.PatientController import PatientController

patient = Blueprint('patient', __name__);

# [GET]
@patient.route('/patient', methods=['get'])
def index_none_pagination():
    return PatientController().index(1);

# [GET]
@patient.route('/patient/<pages>', methods=['get'])
def index(pages):
    return PatientController().index(pages)

@patient.route('/patient/edit', methods=['post'])
def edit_patient():
    return PatientController().edit_patient();

@patient.route('/patient/delete', methods=['post'])
def delete_patient():
    return PatientController().delete_patient();

@patient.route('/patient/medical_record', methods=['post'])
def view_medical_record():
    return PatientController().view_medical_record();