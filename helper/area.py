from helper.hasura import hasura


class Area:
    def __init__(self, data, db_connector):
        self.db_connector = db_connector
        self.data = data

    def __str__(self):
        print('--------------------')
        for key, value in self.data.items():
            print(key, value)
        print('--------------------')
        return ''

    def create_region(self):
        query = '''
        mutation insert_region($key: String!, $value: String!) {
            insert_region(objects: {value: $value, key: $key}) {
                affected_rows
            }
        }
        '''
        response = hasura(query=query, variables={
                          'key': self.data['region'], 'value': self.data['region']})
        if 'errors' in response:
            self.handle_error(response['errors'][0]['message'])
        elif 'data' in response and response['data']['insert_region']['affected_rows'] == 1:
            return True

    def handle_error(self, error):
        if 'area_region_fkey' in error:
            if self.create_region():
                self.migrate()
        elif 'area_pkey' in error:
            print('area exists: {}'.format(self.data['area']))

    def migrate(self):
        print('inserting area: {}'.format(self.data['area']))

        query = '''
        mutation insert_area($objects: [area_insert_input!]!) {
            insert_area(objects: $objects) {
                affected_rows
            }
        }
        '''
        response = hasura(query=query, variables={'objects': [
                          {'key': self.data['area'], 'value': self.data['area'], 'region': self.data['region']}]})
        if 'errors' in response:
            self.handle_error(response['errors'][0]['message'])
        elif 'data' in response and response['data']['insert_area']['affected_rows'] == 1: return True
        return False
