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
    
    def handle_error(self, error):
        pass

    def migrate(self):
        print('inserting area: {}'.format(self.data['area']))

        query = '''
        mutation insert_area($objects: [area_insert_input!]!) {
            insert_area(objects: $objects) {
                affected_rows
            }
        }
        '''

        insert_region = '''
        mutation insert_region($key: String!, $value: String!) {
            insert_region(objects: {value: $value, key: $key}) {
                affected_rows
            }
        }
        '''

        response = hasura(query=query, variables={'objects': [{'key': self.data['area'], 'value': self.data['area'], 'region': self.data['region']}]})
        print(response)
        # if 'errors' in response:
        #     if 'area_region_fkey' in response['errors'][0]['message']:
        #         response = hasura(query=insert_region, variables={'key': self.data['region'], 'value': self.data['region']})
        #         if response['data']['insert_region']['affected_rows'] == 1:
                    
        #             if response['data']['insert_area']['affected_rows'] == 1:
        #                 return True
        #     elif 'area_pkey' in response['errors'][0]['message']:
        #         return False
        # elif 'data' in response and response['data']['insert_area']['affected_rows'] == 1:
        #     return True