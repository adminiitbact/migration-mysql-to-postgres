from helper.db_connector import MySQL
from helper.admin_user import AdminUser
from helper.facility import Facility
from helper.area import Area


def migrate(model):
    skipped = inserted = 0
    for item in model:
        # print(item)
        response = item.migrate()
        if response == False: skipped += 1
        elif response == True: inserted += 1

    print('Total: {}, Inserted: {}, skipped: {}'.format(len(model), inserted, skipped))



if __name__ == '__main__':
    mig = MySQL()
    facilities = [Facility(data=item, db_connector=mig) for item in mig.get_data('select * from facilities')]
    areas = [Area(data=item, db_connector=mig) for item in mig.get_data('select * from areas')]
    

    migrate(areas)
    # migrate(facilities)