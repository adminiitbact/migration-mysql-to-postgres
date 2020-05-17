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

        relations = [
            'region',
            'jurisdiction'
        ]

        for item in relations:
            if self.data[item]:
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
            field, field, field), variables={'object': {'key': str(self.data[field]), 'value': str(self.data[field])}})
        if 'errors' in response:
            if '{}_pkey'.format(field) in response['errors'][0]['message']:
                self.data[field] = str(self.data[field])
            else:
                print(response)
        elif 'data' in response:
            print('creating {}: {} for admin_user: {}'.format(
                field, self.data[field], self.data['name']))
            self.data[field] = response['data']['insert_{}_one'.format(
                field)]['key']

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
