import json
from helper.wards import Ward
from helper.hasura import hasura
from helper.hospital_users import HospitalUser

class Facility:
    def __init__(self, data, db_connector):
        self.db_connector = db_connector
        self.data = data
        self.get_related()
        self.sanitize()

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
        self.data['assets'] = list(map(self.get_json, self.db_connector.get_data(
            'select data from facility_assets where facility_id={}'.format(self.data['facility_id']))))
        self.data['checklist'] = list(map(self.get_json, self.db_connector.get_data(
            'select data from facility_checklist where facility_id={}'.format(self.data['facility_id']))))
        self.data['contacts'] = list(map(self.get_json, self.db_connector.get_data(
            'select data from facility_contacts where facility_id={}'.format(self.data['facility_id']))))
        self.data['inventory'] = list(map(self.get_json, self.db_connector.get_data(
            'select data from facility_inventory where facility_id={}'.format(self.data['facility_id']))))
        self.data['staff'] = list(map(self.get_json, self.db_connector.get_data(
            'select data from facility_medstaff where facility_id={}'.format(self.data['facility_id']))))

        # self.data['mapped_facilities'] = self.db_connector.get_data(
        #     'select * from facilities join facility_mapping on facilities.facility_id=facility_mapping.mapped_facility where facility_mapping.source_facility={}'.format(self.data['facility_id']))
        self.hospital_users = [HospitalUser(data=item, db_connector=self.db_connector) for item in self.db_connector.get_data(
            'select * from hospital_users where facility_id={}'.format(self.data['facility_id']))]
        self.wards = [Ward(data=item, db_connector=self.db_connector, get_hist=True) for item in self.db_connector.get_data(
            'select * from wards where facility_id={}'.format(self.data['facility_id']))]

    def get_json(self, item):
        return json.loads(item['data'])

    def sanitize(self):
        self.data.pop('facility_id')

        self.data['created_at'] = self.data.pop('creation_time').__str__()
        self.data['region'] = str(self.data['region'])
        self.data['is_fever_clinic_available'] = [
            True if self.data['is_fever_clinic_available'] == 1 else False][0]
        self.data['is_separate_entry_exit_available'] = [
            True if self.data.pop('is_seperate_entry_exit_available') == 1 else False][0]

        relations = [
            {
                'query_field': 'region',
                'data_field': 'region',
                'query_var': {'key': self.data['region'], 'value': self.data['region']}
            },
            {
                'query_field': 'facility_status',
                'data_field': 'facility_status',
                'query_var': {'key': self.data['facility_status'], 'value': self.data['facility_status']}
            },
            {
                'query_field': 'jurisdiction',
                'data_field': 'jurisdiction',
                'query_var': {'key': self.data['jurisdiction'], 'value': self.data['jurisdiction']}
            },
            {
                'query_field': 'institution_type',
                'data_field': 'institution_type',
                'query_var': {'key': self.data['institution_type'], 'value': self.data['institution_type']}
            },
            {
                'query_field': 'hospital_category',
                'data_field': 'hospital_category',
                'query_var': {'key': self.data['hospital_category'], 'value': self.data['hospital_category']}
            },
            {
                'query_field': 'covid_facility_type',
                'data_field': 'covid_facility_type',
                'query_var': {'key': self.data['covid_facility_type'], 'value': self.data['covid_facility_type']}
            },

            {
                'query_field': 'area',
                'data_field': 'area',
                'query_var': {'key': self.data['area'], 'value': self.data['area'], 'region': self.data['region']}
            },
            {
                'query_field': 'facility_agreement_status',
                'data_field': 'agreement_status',
                'query_var': {'key': self.data['agreement_status'], 'value': self.data['agreement_status']}
            },
        ]

        for item in relations:
            if self.data[item['data_field']] != None:
                self.create_relation(
                    query_field=item['query_field'], data_field=item['data_field'], query_var=item['query_var'])

    def create_relation(self, query_field, data_field, query_var):
        query = '''
        mutation insert_%s_one($object: %s_insert_input!) {
            insert_%s_one(object: $object) {
                key
                value
            }
        }'''

        response = hasura(query=query % (
            query_field, query_field, query_field), variables={'object': query_var})
        if 'errors' in response:
            if '{}_pkey'.format(query_field) in response['errors'][0]['message']:
                self.data[data_field] = query_var['key']
            else:
                print(response)
        elif 'data' in response:
            print('creating {}: {} for facility: {}'.format(
                data_field, self.data[data_field], self.data['name']))
            self.data[data_field] = response['data']['insert_{}_one'.format(
                query_field)]['key']

    def handle_error(self, error):
        print(error)


    def migrate(self):
        print('inserting facility: {}'.format(self.data['name']))

        query = '''
        mutation insert_facility_one($object: facility_insert_input!) {
            insert_facility_one(object: $object) {
                id
            }
        }
        '''

        response = hasura(query=query, variables={'object': self.data})
        if 'errors' in response:
            self.handle_error(response)
        if 'data' in response and response['data']['insert_facility_one']['id']:
            [item.migrate(facility_id=response['data']['insert_facility_one']['id']) for item in self.wards]
            [item.migrate(facility_id=response['data']['insert_facility_one']['id']) for item in self.hospital_users]
            return True
        return False
