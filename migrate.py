from helper.db_connector import MySQL
from helper.admin_user import AdminUser
from helper.facility import Facility
from helper.area import Area


def migrate(model):
    skipped = inserted = 0
    for item in model:
        response = item.migrate()
        if response == True: inserted += 1
        elif response == False: skipped += 1

    print('Total: {}, Inserted: {}, skipped: {}'.format(len(model), inserted, skipped))



if __name__ == '__main__':
    mig = MySQL()
    areas = [Area(data=item, db_connector=mig) for item in mig.get_data('select * from areas')]
    migrate(areas)

    facilities = [Facility(data=item, db_connector=mig) for item in mig.get_data('select * from facilities')]
    migrate(facilities)

    admin_users = [AdminUser(data=item, db_connector=mig) for item in mig.get_data('select * from admin_users')]
    migrate(admin_users)