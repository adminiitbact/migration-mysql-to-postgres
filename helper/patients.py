from helper.hasura import hasura
from helper.relations import *



def patient_migrate(data):
    query = '''
    mutation MyMutation($objects: [patient_insert_input!]!) {
        insert_patient(objects: $objects, on_conflict: {constraint: patient_pkey, update_columns: id}) {
            affected_rows
        }
    }'''

    response = hasura(query=query, variables={'objects': data})
    print('inserted patient: {}'.format(
        response['data']['insert_patient']['affected_rows']))


def sanitize_patient(data):
    data['id'] = data.pop('patient_id')
    data['created_at'] = data.pop('creation_time').__str__()
    get_key_value(data=data, field='locality',
                  constraint='area_pkey', relation='area')
    get_key_value(data=data, field='gender',
                  constraint='gender_pkey', relation='genderByGender')

    return data




def patient_discharge_migrate(data):
    query = '''
    mutation MyMutation($objects: [patient_discharge_insert_input!]!) {
        insert_patient_discharge(objects: $objects, on_conflict: {constraint: patient_discharge_pkey, update_columns: id}) {
            affected_rows
        }
    }'''

    response = hasura(query=query, variables={'objects': data})
    print('inserted patient_discharge: {}'.format(
        response['data']['insert_patient_discharge']['affected_rows']))


def sanitize_patient_discharge(data):
    data['created_at'] = data.pop('creation_time').__str__()

    get_key_value(data=data, field='severity',
                  constraint='severity_pkey', relation='severityBySeverity')

    get_key_value(data=data, field='test_status',
                  constraint='test_result_status_pkey', relation='test_result_status')

    get_key_value(data=data, field='reason',
                  constraint='patient_discharge_reason_pkey', relation='patient_discharge_reason')

    get_key_value(data=data, field='quarantine_type',
                  constraint='quarantine_type_pkey', relation='quarantineTypeByQuarantineType')


    return data



def patient_live_status_migrate(data):
    query = '''
    mutation MyMutation($objects: [patient_live_status_insert_input!]!) {
        insert_patient_live_status(objects: $objects, on_conflict: {constraint: patient_live_status_pkey, update_columns: id}) {
            affected_rows
        }
    }'''

    response = hasura(query=query, variables={'objects': data})
    print('inserted patient live status: {}'.format(
        response['data']['insert_patient_live_status']['affected_rows']))


def sanitize_patient_live_status(data):
    get_key_value(data=data, field='severity',
                  constraint='severity_pkey', relation='severityBySeverity')

    get_key_value(data=data, field='test_status',
                  constraint='test_result_status_pkey', relation='test_result_status')

    return data



def patient_history_migrate(data):
    query = '''
    mutation MyMutation($objects: [patient_history_insert_input!]!) {
        insert_patient_history(objects: $objects, on_conflict: {constraint: patient_history_pkey, update_columns: id}) {
            affected_rows
        }
    }'''

    response = hasura(query=query, variables={'objects': data})
    print('inserted patient history: {}'.format(
        response['data']['insert_patient_history']['affected_rows']))


def sanitize_patient_history(data):
    data['created_at'] = data.pop('creation_time').__str__()
    get_key_value(data=data, field='severity',
                  constraint='severity_pkey', relation='severityBySeverity')

    get_key_value(data=data, field='test_status',
                  constraint='test_result_status_pkey', relation='test_result_status')

    return data
