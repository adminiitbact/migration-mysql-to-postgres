from helper.hasura import hasura
from helper.relations import *
import json



def ward_migrate(data):
    query = '''
    mutation MyMutation($objects: [ward_insert_input!]!) {
        insert_ward(objects: $objects, on_conflict: {constraint: ward_pkey, update_columns: id}) {
            affected_rows
        }
    }'''

    response = hasura(query=query, variables={'objects': data})
    print('inserted ward: {}'.format(
        response['data']['insert_ward']['affected_rows']))


def sanitize_ward(data):
    data['created_at'] = data.pop('creation_time').__str__()
    if data['modification_time'] is not None:
        data['updated_at'] = data.pop('modification_time').__str__()
    else:
        data.pop('modification_time')
    data['extra_fields'] = json.loads(data.pop('extra_fields'))

    data['active'] = [True if data['active'] == 1 else False][0]
    data['covid_ward'] = [True if data['covid_ward'] == 1 else False][0]

    get_key_value(data=data, field='severity',
                  constraint='severity_pkey', relation='severityBySeverity')
    get_key_value(data=data, field='gender',
                  constraint='gender_pkey', relation='genderByGender')

    return data





def ward_history_migrate(data):
    query = '''
    mutation MyMutation($objects: [wards_history_insert_input!]!) {
        insert_wards_history(objects: $objects, on_conflict: {constraint: wards_history_pkey, update_columns: id}) {
            affected_rows
        }
    }'''

    response = hasura(query=query, variables={'objects': data})
    print('inserted ward_history: {}'.format(
        response['data']['insert_wards_history']['affected_rows']))


def sanitize_ward_history(data):
    data['id'] = data.pop('ward_history_id')
    data['created_at'] = data.pop('creation_time').__str__()
    data['extra_fields'] = json.loads(data.pop('extra_fields'))

    data['active'] = [True if data['active'] == 1 else False][0]
    data['covid_ward'] = [True if data['covid_ward'] == 1 else False][0]

    get_key_value(data=data, field='severity',
                  constraint='severity_pkey', relation='severityBySeverity')
    get_key_value(data=data, field='gender',
                  constraint='gender_pkey', relation='genderByGender')

    return data