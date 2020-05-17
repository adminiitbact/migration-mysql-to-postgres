class AdminUser:
    def __init__(self, data, db_connector):
        self.db_connector = db_connector
        self.data = data
        self.get_facility()
    
    def get_facility(self):
        for item in self.db_connector.get_data('select * from facilities f inner join admin_user_facility_mapping a on f.facility_id=a.facility_id where a.admin_user_id="{}"'.format(self.data['id'])):
            print(item)


    def __str__(self):
        print('--------------------')
        for key,value in self.data.items():
            print(key, value)
        print('--------------------')
        return ''
