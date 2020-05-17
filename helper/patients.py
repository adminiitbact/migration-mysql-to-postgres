from helper.hasura import hasura
from helper.hasura import hasura
import json


class Patient:
    def __init__(self, data, db_connector):
        self.db_connector = db_connector
        self.data = data
        self.get_related()

    def __str__(self):
        print('--------------------')
        for key, value in self.data.items():
            print(key, value)
        print('--------------------')
        return ''

    def get_related(self):
        self.data['patient_discharges'] = {'data': self.db_connector.get_data(
            'select * from patient_discharged where patient_id={}'.format(self.data['patient_id']))}
        self.data['patient_histories'] = {'data': self.db_connector.get_data(
            'select * from patient_history where patient_id={}'.format(self.data['patient_id']))}
        self.data['patient_live_statuses'] = {'data': self.db_connector.get_data(
            'select * from patient_live_status where patient_id={}'.format(self.data['patient_id']))}

    def sanitize(self, facility_id, ward_id):
        self.data.pop('patient_id')
        self.data['created_at'] = self.data.pop('creation_time').__str__()
        self.data['pre_existing_medical_condition'] = json.loads(self.data['pre_existing_medical_condition'])

        temp = self.data.pop('locality')
        self.data['area'] = {'data': {'key': temp, 'value': temp, 'regionByRegion': {'data': {'key': temp, 'value': temp}, 'on_conflict': {'constraint': 'region_pkey', 'update_columns': 'value'}}}, 'on_conflict': {'constraint': 'area_pkey', 'update_columns': 'value'}}

        temp = self.data.pop('gender')
        self.data['genderByGender'] = {'data': {'key': temp, 'value': temp}, 'on_conflict': {'constraint': 'gender_pkey', 'update_columns': 'value'}}

        for row in self.data['patient_discharges']['data']:
            row.pop('id')
            row.pop('patient_id')
            row.pop('facility_id')
            row.pop('ward_id')
            row['facility'] = facility_id
            row['ward'] = ward_id
            row['created_at'] = row.pop('creation_time').__str__()

            temp = row.pop('test_status')
            row['test_result_status'] = {'data': {'key': temp, 'value': temp}, 'on_conflict': {
                'constraint': 'test_result_status_pkey', 'update_columns': 'value'}}

            temp = row.pop('severity')
            row['severityBySeverity'] = {'data': {'key': temp, 'value': temp}, 'on_conflict': {
                'constraint': 'severity_pkey', 'update_columns': 'value'}}

            temp = row.pop('reason')
            row['patient_discharge_reason'] = {'data': {'key': temp, 'value': temp}, 'on_conflict': {
                'constraint': 'patient_discharge_reason_pkey', 'update_columns': 'value'}}

            temp = row.pop('quarantine_type')
            row['quarantineTypeByQuarantineType'] = {'data': {'key': temp, 'value': temp}, 'on_conflict': {
                'constraint': 'quarantine_type_pkey', 'update_columns': 'value'}}

        for row in self.data['patient_histories']['data']:
            row.pop('id')
            row.pop('patient_id')
            row.pop('facility_id')
            row.pop('ward_id')
            row['facility'] = facility_id
            row['ward'] = ward_id
            row['created_at'] = row.pop('creation_time').__str__()
            
            temp = row.pop('test_status')
            row['test_result_status'] = {'data': {'key': temp, 'value': temp}, 'on_conflict': {
                'constraint': 'test_result_status_pkey', 'update_columns': 'value'}}

            temp = row.pop('severity')
            row['severityBySeverity'] = {'data': {'key': temp, 'value': temp}, 'on_conflict': {
                'constraint': 'severity_pkey', 'update_columns': 'value'}}

        for row in self.data['patient_live_statuses']['data']:
            row.pop('id')
            row.pop('patient_id')
            row.pop('facility_id')
            row.pop('ward_id')
            row['facility'] = facility_id
            row['ward'] = ward_id
            
            temp = row.pop('test_status')
            row['test_result_status'] = {'data': {'key': temp, 'value': temp}, 'on_conflict': {
                'constraint': 'test_result_status_pkey', 'update_columns': 'value'}}

            temp = row.pop('severity')
            row['severityBySeverity'] = {'data': {'key': temp, 'value': temp}, 'on_conflict': {
                'constraint': 'severity_pkey', 'update_columns': 'value'}}

    def handle_error(self, error):
        print(error)

    def migrate(self, facility_id, ward_id):
        print('inserting patient: {}'.format(self.data['name']))

        self.sanitize(facility_id=facility_id, ward_id=ward_id)

        query = '''
        mutation insert_patient_one($object: patient_insert_input!) {
            insert_patient_one(object: $object) {
                id
            }
        }'''


        response = hasura(query=query, variables={'object': self.data})
        if 'errors' in response:
            self.handle_error(response)
        if 'data' in response and response['data']['insert_patient_one']['id']:
            return True
        return False
