from flask import Blueprint
from controllers.PatientController import PatientController

patient = Blueprint('patient', __name__);

# [GET]
@patient.route('/patient', methods=['get'])
def index_none_pagination():
    return PatientController.index(1);

# [GET]
@patient.route('/patient/<pages>', methods=['get'])
def index(pages):
    return PatientController().index(pages)