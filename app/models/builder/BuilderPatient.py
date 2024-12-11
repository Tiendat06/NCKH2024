from app.models.builder.IBuilderPatient import IBuilderPatient

class BuilderPatient(IBuilderPatient):

    def setPatientIdBuilder(self, id) -> 'IBuilderPatient':
        self.__patient_id = id;
        return self
    
    def setPatientNameBuilder(self, name)-> 'IBuilderPatient':
        self.__patient_name = name
        return self
    
    def setPatientAgeBuilder(self, age)-> 'IBuilderPatient':
        self.__patient_age = age;
        return self
    
    def setPatientImgBuilder(self, img)-> 'IBuilderPatient':
        self.__img = img;
        return self
    
    def setPatientPhoneBuilder(self, phone)-> 'IBuilderPatient':
        self.__phone = phone;
        return self
    
    def setPatientPIDBuilder(self, PID)-> 'IBuilderPatient':
        self.__PID = PID;
        return self
    
    def setPatientGenderBuilder(self, gender)-> 'IBuilderPatient':
        self.__gender = gender;
        return self
    
    def setPatientAddressBuilder(self, address)-> 'IBuilderPatient':
        self.__address = address;
        return self
    
    def setPatientDateCreatedBuilder(self, date_created)-> 'IBuilderPatient':
        self.__date_created = date_created;
        return self
    
    def setPatientDOBBuilder(self, dob)-> 'IBuilderPatient':
        self.__dob = dob;
        return self
    
    def setPatientMailBuilder(self, email)-> 'IBuilderPatient':
        self.__email = email;
        return self
    
    def build(self):
        from app.models.Patient import Patient
        return Patient(self.__patient_id, self.__patient_name, self.__patient_age, self.__img, 
        self.__phone, self.__PID, self.__gender, self.__address, self.__date_created, self.__dob, self.__email);