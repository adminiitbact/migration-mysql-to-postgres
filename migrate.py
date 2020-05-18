from helper.db_connector import MySQL
from helper.admin_user import *
from helper.area import *
from helper.facility import *
from helper.hospital_users import *
from helper.patients import *
from helper.wards import *


def migrate(model):
    skipped = inserted = 0
    for item in model:
        response = item.migrate()
        if response == True: inserted += 1
        elif response == False: skipped += 1

    print('Total: {}, Inserted: {}, skipped: {}'.format(len(model), inserted, skipped))



if __name__ == '__main__':
    mig = MySQL()

    admin_migrate(list(map(sanitize_admin_users, mig.get_data('select * from admin_users'))))
    area_migrate(list(map(sanitize_area, mig.get_data('select * from areas'))))
    facility_migrate(list(map(sanitize_facility, mig.get_data('select * from facilities'))))
    facility_assets_migrate(list(map(sanitize_facility_assets, mig.get_data('select * from facility_assets'))))
    facility_checklist_migrate(list(map(sanitize_facility_checklist, mig.get_data('select * from facility_checklist'))))
    facility_contacts_migrate(list(map(sanitize_facility_contacts, mig.get_data('select * from facility_contacts'))))
    facility_inventory_migrate(list(map(sanitize_facility_inventory, mig.get_data('select * from facility_inventory'))))
    facility_mapping_through_table_migrate(mig.get_data('select * from facility_mapping'))
    facility_medstaff_migrate(list(map(sanitize_facility_medstaff, mig.get_data('select * from facility_medstaff'))))
    hospital_users_migrate(list(map(sanitize_hospital_users, mig.get_data('select * from hospital_users'))))
    ward_migrate(list(map(sanitize_ward, mig.get_data('select * from wards'))))
    ward_history_migrate(list(map(sanitize_ward_history, mig.get_data('select * from wards_history'))))
    patient_migrate(list(map(sanitize_patient, mig.get_data('select * from patients'))))
    patient_discharge_migrate(list(map(sanitize_patient_discharge, mig.get_data('select * from patient_discharged'))))
    patient_live_status_migrate(list(map(sanitize_patient_live_status, mig.get_data('select * from patient_live_status'))))
    patient_history_migrate(list(map(sanitize_patient_history, mig.get_data('select * from patient_history'))))