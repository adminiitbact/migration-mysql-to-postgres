from helper.hasura import hasura
from helper.relations import get_key_value



def area_migrate(data):
    query = '''
    mutation MyMutation($objects: [area_insert_input!]!) {
        insert_area(objects: $objects, on_conflict: {constraint: area_pkey, update_columns: value}) {
            affected_rows
        }
    }'''

    response = hasura(query=query, variables={'objects': data})
    print('inserted area: {}'.format(response['data']['insert_area']['affected_rows']))


def sanitize_area(data):
    data['key'] = data['value'] = data.pop('area')
    get_key_value(data=data, field='region', relation='regionByRegion', constraint='region_pkey')
    return data