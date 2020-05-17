from helper.hasura import hasura
from helper.hasura import hasura


class AdminUser:
    def __init__(self, data, db_connector):
        self.db_connector = db_connector
        self.data = data
        self.sanitize()

    def __str__(self):
        print('--------------------')
        for key, value in self.data.items():
            print(key, value)
        print('--------------------')
        return ''

    def sanitize(self):
        self.data.pop('id')
        self.created_at = self.data.pop('creation_time').__str__()

        temp = self.data.pop('region')
        self.data['regionByRegion'] = {'data': {'key': str(temp), 'value': str(temp)}, 'on_conflict': {'constraint': 'region_pkey', 'update_columns': 'value'}}

        temp = self.data.pop('jurisdiction')
        self.data['jurisdictionByJurisdiction'] = {'data': {'key': temp, 'value': temp}, 'on_conflict': {'constraint': 'jurisdiction_pkey', 'update_columns': 'value'}}

    def handle_error(self, error):
        print(error)

    def migrate(self):
        print('inserting admin_user: {}'.format(self.data['name']))

        query = '''
        mutation insert_admin_users_one($object: admin_users_insert_input!) {
            insert_admin_users_one(object: $object) {
                id
            }
        }'''

        response = hasura(query=query, variables={'object': self.data})
        if 'errors' in response:
            self.handle_error(response)
        if 'data' in response and response['data']['insert_admin_users_one']['id']:
            return True
        return False
