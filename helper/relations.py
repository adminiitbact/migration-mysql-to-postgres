def get_key_value(field, constraint, relation, data):
    temp = data.pop(field)
    data[relation] = {'data': {'key': str(temp), 'value': str(temp)}, 'on_conflict': {'constraint': constraint, 'update_columns': 'value'}}

    return data


def get_area(data):
    temp = data.pop('area')
    data['areaByArea'] = {'data': {'regionByRegion': {'data': {'key': str(data['region']), 'value': str(data['region'])}, 'on_conflict': {'constraint': 'region_pkey', 'update_columns': 'value'}}, 'key': str(temp), 'value': str(temp)}, 'on_conflict': {'constraint': 'area_pkey', 'update_columns': 'value'}}
    return data


def get_jurisdiction(data):
    get_key_value(data=data, field='jurisdiction',
                  constraint='jurisdiction_pkey', relation='jurisdictionByJurisdiction')
    return data