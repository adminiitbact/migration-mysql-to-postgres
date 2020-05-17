class Patient:
    def __init__(self, data, db_connector):
        self.db_connector = db_connector
        self.data = data
        self.get_related()

    def __str__(self):
        print('--------------------')
        for key,value in self.data.items():
            print(key, value)
        print('--------------------')
        return ''

    def get_related(self):
        self.data['patient_clinical_hist'] = self.db_connector.get_data('select * from patient_clinical_hist where patient_id={}'.format(self.data['patient_id']))
        self.data['patient_covid_test_details'] = self.db_connector.get_data('select * from patient_covid_test_details where patientid={}'.format(self.data['patient_id']))
        self.data['patient_discharged'] = self.db_connector.get_data('select * from patient_discharged where patient_id={}'.format(self.data['patient_id']))
        self.data['patient_history'] = self.db_connector.get_data('select * from patient_history where patient_id={}'.format(self.data['patient_id']))
        self.data['patient_live_status'] = self.db_connector.get_data('select * from patient_live_status where patient_id={}'.format(self.data['patient_id']))