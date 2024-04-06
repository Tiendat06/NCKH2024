from abc import ABC, abstractmethod
# from models.Patient import Patient

class IBuilderPatient(ABC):
    @abstractmethod
    def setPatientIdBuilder(self, id) -> 'IBuilderPatient':
        pass

    @abstractmethod
    def setPatientNameBuilder(self, name) -> 'IBuilderPatient':
        pass

    @abstractmethod
    def setPatientAgeBuilder(self, age) -> 'IBuilderPatient':
        pass

    @abstractmethod
    def setPatientImgBuilder(self, img) -> 'IBuilderPatient':
        pass

    @abstractmethod
    def setPatientPhoneBuilder(self, phone) -> 'IBuilderPatient':
        pass

    @abstractmethod
    def setPatientPIDBuilder(self, PID) -> 'IBuilderPatient':
        pass

    @abstractmethod
    def setPatientGenderBuilder(self, gender) -> 'IBuilderPatient':
        pass

    @abstractmethod
    def setPatientAddressBuilder(self, address) -> 'IBuilderPatient':
        pass

    @abstractmethod
    def setPatientDateCreatedBuilder(self, date_created) -> 'IBuilderPatient':
        pass

    @abstractmethod
    def setPatientDOBBuilder(self, dob) -> 'IBuilderPatient':
        pass

    @abstractmethod
    def setPatientMailBuilder(self, email) -> 'IBuilderPatient':
        pass

    @abstractmethod
    def build(self):
        pass

