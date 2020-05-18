from helper.hasura import hasura
from helper.relations import get_key_value


def admin_migrate(data):
    query = '''
    mutation MyMutation($objects: [admin_users_insert_input!]!) {
        insert_admin_users(objects: $objects, on_conflict: {constraint: admin_users_pkey, update_columns: name}) {
            affected_rows
        }
    }'''

    response = hasura(query=query, variables={'objects': data})
    print('inserted admin_users: {}'.format(response['data']['insert_admin_users']['affected_rows']))


def sanitize_admin_users(data):
    data['created_at'] = data.pop('creation_time').__str__()
    get_key_value(data=data, field='region', relation='regionByRegion', constraint='region_pkey')
    get_key_value(data=data, field='jurisdiction', relation='jurisdictionByJurisdiction', constraint='jurisdiction_pkey')
    return data