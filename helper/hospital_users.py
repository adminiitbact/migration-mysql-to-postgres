from helper.hasura import hasura
from helper.relations import *




def hospital_users_migrate(data):
    query = '''
    mutation MyMutation($objects: [hospital_users_insert_input!]!) {
    insert_hospital_users(objects: $objects, on_conflict: {constraint: hospital_users_pkey, update_columns: name}) {
            affected_rows
        }
    }'''

    response = hasura(query=query, variables={'objects': data})
    print('inserted facility medstaff: {}'.format(
        response['data']['insert_hospital_users']['affected_rows']))


def sanitize_hospital_users(data):
    data['created_at'] = data.pop('creation_time').__str__()
    get_key_value(data=data, field='region',
                  constraint='region_pkey', relation='regionByRegion')


    return data

