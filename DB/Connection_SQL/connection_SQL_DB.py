from peewee import *

database = SqliteDatabase('./SQLiteDB.db')

if __name__ == "__main__":
    pass





# import datetime
# from peewee import *
#
# db = SqliteDatabase('DB/Data.db')
#
#
# class SensorLog(Model):
#     id = PrimaryKeyField(unique=True)
#     dateTimeField = DateTimeField(default=datetime.datetime.now)
#     value = FloatField()
#
#     class Meta:
#         database = db
#         order = '-id'
#         db_table = 'Sensor_logs'
#
#
# db.create_tables([SensorLog])
# # with db:
# #     db.create_tables([SensorLog])
