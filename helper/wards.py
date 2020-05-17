class Ward:
    def __init__(self, data, db_connector):
        self.db_connector = db_connector
        self.data = data
        self.get_related()

    def __str__(self):
        print('--------------------')
        for key,value in self.data.items():
            print(key, value)
        print('--------------------')
        return ''

    def get_related(self):
        self.data['wards_history'] = self.db_connector.get_data('select * from wards_history where ward_id={}'.format(self.data['id']))