from helper.hasura import hasura
import json


class Ward:
    def __init__(self, data, db_connector, get_hist):
        self.db_connector = db_connector
        self.data = data
        self.get_hist = get_hist

        if self.get_hist:
            self.get_history()
        self.sanitize()

    def __str__(self):
        print('--------------------')
        for key, value in self.data.items():
            print(key, value)
        print('--------------------')
        return ''

    def get_history(self):
        self.wards_histories = [Ward(data=item, db_connector=self.db_connector, get_hist=False) for item in self.db_connector.get_data(
            'select * from wards_history where ward_id={}'.format(self.data['id']))]

    def sanitize(self):
        self.data.pop('facility_id')
        if 'id' in self.data:
            self.data.pop('id')
        if 'modification_time' in self.data:
            self.data.pop('modification_time')
        if 'ward_history_id' in self.data:
            self.data.pop('ward_history_id')
        if 'ward_id' in self.data:
            self.data.pop('ward_id')
        self.data['created_at'] = self.data.pop('creation_time').__str__()
        self.data['active'] = [True if self.data['active'] == 1 else False][0]
        self.data['covid_ward'] = [
            True if self.data['covid_ward'] == 1 else False][0]

        self.data['extra_fields'] = json.loads(self.data['extra_fields'])

        relations = [
            'severity',
            'gender'
        ]

        for item in relations:
            self.create_relation(field=item)

    def create_relation(self, field):
        query = '''
        mutation insert_%s_one($object: %s_insert_input!) {
            insert_%s_one(object: $object) {
                key
                value
            }
        }'''

        response = hasura(query=query % (
            field, field, field), variables={'object': {'key': self.data[field], 'value': self.data[field]}})
        if 'errors' in response:
            if '{}_pkey'.format(field) in response['errors'][0]['message']:
                pass
            else:
                print(response)
        elif 'data' in response:
            print('creating {}: {} for facility: {}'.format(
                field, self.data[field], self.data['name']))
            self.data[field] = response['data']['insert_{}_one'.format(
                field)]['key']

    def handle_error(self, error):
        print(error)

    def migrate_hist(self, facility_id, ward_id):
        print('inserting ward history: {}'.format(self.data['name']))

        query = '''
        mutation insert_wards_history_one($object: wards_history_insert_input!) {
            insert_wards_history_one(object: $object) {
                id
            }
        }
        '''

        self.data['facility'] = facility_id
        self.data['ward'] = ward_id

        response = hasura(query=query, variables={'object': self.data})
        if 'errors' in response:
            self.handle_error(response)
        if 'data' in response and response['data']['insert_wards_history_one']['id']:
            return True
        return False


    def migrate(self, facility_id):
        print('inserting ward: {}'.format(self.data['name']))

        query = '''
        mutation insert_ward_one($object: ward_insert_input!) {
            insert_ward_one(object: $object) {
                id
            }
        }
        '''
        self.data['facility'] = facility_id

        response = hasura(query=query, variables={'object': self.data})
        if 'errors' in response:
            self.handle_error(response)
        if 'data' in response and response['data']['insert_ward_one']['id']:
            if self.get_hist:
                [item.migrate_hist(facility_id=facility_id, ward_id=response['data']
                                   ['insert_ward_one']['id']) for item in self.wards_histories]
            return True
        return False
