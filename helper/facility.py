import json
from helper.wards import Ward
from helper.hasura import hasura


class Facility:
    def __init__(self, data, db_connector):
        self.db_connector = db_connector
        self.data = data
        self.get_related()

    def __str__(self):
        print('--------------------')
        for key, value in self.data.items():
            print(key, value)
        # print('wards: ')
        # for item in self.wards:
        #     print(item)
        print('--------------------')
        return ''

    def get_related(self):
        self.data['assets'] = self.db_connector.get_data(
            'select data from facility_assets where facility_id={}'.format(self.data['facility_id']))
        self.data['checklist'] = self.db_connector.get_data(
            'select data from facility_checklist where facility_id={}'.format(self.data['facility_id']))
        self.data['contacts'] = self.db_connector.get_data(
            'select data from facility_contacts where facility_id={}'.format(self.data['facility_id']))
        self.data['inventory'] = self.db_connector.get_data(
            'select data from facility_inventory where facility_id={}'.format(self.data['facility_id']))
        self.data['mapped_facilities'] = self.db_connector.get_data(
            'select * from facilities join facility_mapping on facilities.facility_id=facility_mapping.mapped_facility where facility_mapping.source_facility={}'.format(self.data['facility_id']))
        self.data['staff'] = self.db_connector.get_data(
            'select data from facility_medstaff where facility_id={}'.format(self.data['facility_id']))
        self.data['hospital_users'] = self.db_connector.get_data(
            'select * from hospital_users where facility_id={}'.format(self.data['facility_id']))
        self.wards = [Ward(data=item, db_connector=self.db_connector) for item in self.db_connector.get_data(
            'select * from wards where facility_id={}'.format(self.data['facility_id']))]

    def migrate(self):
        query = '''
        mutation insert_facility($objects: [facility_insert_input!]!) {
            insert_facility(objects: $objects) {
                affected_rows
            }
        }
        '''

        obj = {
            'address':   self.data['address'],
            'email':  self.data['email'],
            'facility_status':  self.data['facility_status'],
            'government_hospital': self.data['government_hospital'],
            'has_links': self.data['has_links'],
            'is_fever_clinic_available': True if self.data['is_fever_clinic_available'] == 1 else False,
            'is_separate_entry_exit_available': True if self.data['is_seperate_entry_exit_available'] == 1 else False,
            'name':  self.data['name'],
            'telephone':  self.data['telephone'],
            'ulb_ward_name':  self.data['ulb_ward_name'],
            'ulb_zone_name':  self.data['ulb_zone_name'],
            'assets':  self.data['assets'],
            'checklist':  self.data['checklist'],
            'contacts':  self.data['contacts'],
            'staff':  self.data['staff'],
            'inventory':  self.data['inventory'],
            'area':  self.data['area'],
            'covid_facility_type': self.data['covid_facility_type'],
            'agreement_status': self.data['agreement_status'],
            'status':  self.data['facility_status'],
            'hospital_category':  self.data['hospital_category'],
            'institution_type':  self.data['institution_type'],
            'jurisdiction':  self.data['jurisdiction'],
            'region':  str(self.data['region']),
        }

        print('inserting facility: {}'.format(self.data['name']))
        response = hasura(query=query, variables={'objects': [obj]})
        print(response)
        if 'errors' in response:
            if 'facility_covid_facility_type_fkey' in response['errors'][0]['message']:
                pass
                # TODO here
        if 'data' in response and response['data']['insert_facility']['affected_rows' == 1]: return True
        return False
