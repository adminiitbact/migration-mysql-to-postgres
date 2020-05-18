import json
from helper.hasura import hasura
from helper.relations import *


def facility_migrate(data):
    query = '''
    mutation MyMutation($objects: [facility_insert_input!]!) {
        insert_facility(objects: $objects, on_conflict: {constraint: facility_pkey, update_columns: name}) {
            affected_rows
        }
    }'''

    response = hasura(query=query, variables={'objects': data})
    print('inserted facility: {}'.format(
        response['data']['insert_facility']['affected_rows']))


def sanitize_facility(data):
    data['id'] = data.pop('facility_id')

    get_area(data=data)

    get_key_value(data=data, field='region',
                  constraint='region_pkey', relation='regionByRegion')

    get_jurisdiction(data=data)

    get_key_value(data=data, field='institution_type',
                  constraint='institution_type_pkey', relation='institutionTypeByInstitutionType')

    get_key_value(data=data, field='hospital_category',
                  constraint='hospital_category_pkey', relation='hospitalCategoryByHospitalCategory')

    get_key_value(data=data, field='facility_status',
                  constraint='facility_status_pkey', relation='facilityStatusByFacilityStatus')

    get_key_value(data=data, field='covid_facility_type',
                  constraint='covid_facility_type_pkey', relation='covidFacilityTypeByCovidFacilityType')

    get_key_value(data=data, field='agreement_status',
                  constraint='facility_agreement_status_pkey', relation='facility_agreement_status')

    data['is_fever_clinic_available'] = [
        True if data['is_fever_clinic_available'] == 1 else False][0]
    data['is_separate_entry_exit_available'] = [True if data.pop(
        'is_seperate_entry_exit_available') == 1 else False][0]
    data['created_at'] = data.pop('creation_time').__str__()

    return data


def facility_assets_migrate(data):
    query = '''
    mutation MyMutation($objects: [facility_assets_insert_input!]!) {
        insert_facility_assets(objects: $objects, on_conflict: {constraint: facility_assets_pkey, update_columns: data}) {
            affected_rows
        }
    }'''

    response = hasura(query=query, variables={'objects': data})
    print('inserted facility assets: {}'.format(
        response['data']['insert_facility_assets']['affected_rows']))


def sanitize_facility_assets(data):
    data['created_at'] = data.pop('creation_time').__str__()
    data['data'] = json.loads(data['data'])

    return data


def facility_checklist_migrate(data):
    query = '''
    mutation MyMutation($objects: [facility_checklist_insert_input!]!) {
        insert_facility_checklist(objects: $objects, on_conflict: {constraint: facility_checklist_pkey, update_columns: data}) {
            affected_rows
        }
    }'''

    response = hasura(query=query, variables={'objects': data})
    print('inserted facility checklist: {}'.format(
        response['data']['insert_facility_checklist']['affected_rows']))


def sanitize_facility_checklist(data):
    data['created_at'] = data.pop('creation_time').__str__()
    data['data'] = json.loads(data['data'])

    return data


def facility_contacts_migrate(data):
    query = '''
    mutation MyMutation($objects: [facility_contacts_insert_input!]!) {
        insert_facility_contacts(objects: $objects, on_conflict: {constraint: facility_contacts_pkey, update_columns: data}) {
            affected_rows
        }
    }'''

    response = hasura(query=query, variables={'objects': data})
    print('inserted facility contacts: {}'.format(
        response['data']['insert_facility_contacts']['affected_rows']))


def sanitize_facility_contacts(data):
    data['created_at'] = data.pop('creation_time').__str__()
    data['data'] = json.loads(data['data'])

    return data


def facility_inventory_migrate(data):
    query = '''
    mutation MyMutation($objects: [facility_inventory_insert_input!]!) {
        insert_facility_inventory(objects: $objects, on_conflict: {constraint: facility_inventory_pkey, update_columns: data}) {
            affected_rows
        }
    }'''

    response = hasura(query=query, variables={'objects': data})
    print('inserted facility inventory: {}'.format(
        response['data']['insert_facility_inventory']['affected_rows']))


def sanitize_facility_inventory(data):
    data['created_at'] = data.pop('creation_time').__str__()
    data['data'] = json.loads(data['data'])

    return data


def facility_mapping_through_table_migrate(data):
    query = '''
    mutation MyMutation($objects: [facility_mapping_though_table_insert_input!]!) {
        insert_facility_mapping_though_table(objects: $objects, on_conflict: {constraint: facility_mapping_though_table_pkey, update_columns: [mapped_facility, source_facility]}) {
            affected_rows
        }
    }'''

    response = hasura(query=query, variables={'objects': data})
    print('inserted facility mapping_through_table: {}'.format(
        response['data']['insert_facility_mapping_though_table']['affected_rows']))






def facility_medstaff_migrate(data):
    query = '''
    mutation MyMutation($objects: [facility_medstaff_insert_input!]!) {
        insert_facility_medstaff(objects: $objects, on_conflict: {constraint: facility_medstaff_pkey, update_columns: data}) {
            affected_rows
        }
    }'''

    response = hasura(query=query, variables={'objects': data})
    print('inserted facility medstaff: {}'.format(
        response['data']['insert_facility_medstaff']['affected_rows']))


def sanitize_facility_medstaff(data):
    data['created_at'] = data.pop('creation_time').__str__()
    data['data'] = json.loads(data['data'])

    return data
