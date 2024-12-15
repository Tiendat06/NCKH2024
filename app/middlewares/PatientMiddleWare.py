from app.controllers.PatientController import PatientController

class PatientMiddleWare:
    def __init__(self):
        self.patientController = PatientController()

    def view_patient(self):
        return self.patientController.login_patient()