from server.lib.utils.logger import status_logger

from pymongo import MongoClient
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

PRODUCTION = os.environ.get("PRODUCTION")
DB_HOST = os.environ.get('DB_HOST')

if PRODUCTION != 'TRUE':
    DB_HOST = 'localhost'


client = MongoClient(DB_HOST, 27017)


def db_session_operation(transaction):
    with client.start_session() as session:
        with session.start_transaction():
            return transaction()


def get_transaction(DatabaseCollection):
    def pull_from_db():
        db_values = {}
        for db_entry in DatabaseCollection.find():
            try:
                db_values[db_entry['column']] = db_entry['row']
            except KeyError:
                pass
        return db_values
    return db_session_operation(pull_from_db)


def save_transaction(DatabaseCollection, data):
    def save_to_db():
        for key, value in data.items():
            DatabaseCollection.update_one(
                {'column': key},
                {'$set': {'row': value}},
                upsert=True
            )
    return db_session_operation(save_to_db)


def get_db(db_name):
    status_logger(non_status_text=f"getting mongodb -> ",
                  status_text=db_name, cyan=True)
    return client[db_name]


def get_table(db, table_name):
    return db[table_name]


def get_from_db(db, table,  column, get_timestamp=False):
    status_logger(
        non_status_text='searching record -> {} in table -> {}'.format(column, table))
    db_entry = db[table].find_one({'column':  column})
    if db_entry:
        status_logger(non_status_text='record -> {} found'.format(column))
        if get_timestamp:
            return db_entry['row'], db_entry.get('_id').generation_time
        return db_entry['row']
    else:
        status_logger(non_status_text='record -> {} NOT found'.format(column))
        return None


def save_to_db(db, table, column_name):
    status_logger(
        non_status_text='new update saved in db {} -> {} table updated with entry -> {}'.format(table, db, column_name))

    return db[table].insert_one(column_name).inserted_id


def delete_from_db(db, table, column):
    if column:
        status_logger(non_status_text='deleting entry -> {} in db {}'.format(column, db))
        return db[table].delete_one({'column': column})

    table = db[table]
    status_logger(
        non_status_text='table -> dropped from db ->'.format(table, db))

    return table.drop()


def delete_record(db, table, column):
    row_id = does_exist(db, table, column)

    if row_id:
        status_logger(
            non_status_text='deleting entry -> {} in db {}'.format(column, db))
        return db[table].remove(row_id)


def update_record(db, table,  column, data, forceNew=False):

    if forceNew:
        row_id = None
    else:
        row_id = does_exist(db, table, column)

    if type(data) is set:
        data = list(data)

    if row_id:

        new_row = {
            'row': data,
            'column': column
        }

        return db[table].replace_one({'column':  column}, new_row)

    return save_to_db(db, table, {'column':  column, 'row': data})


def does_exist(db, table, column_name):
    status_logger(
        non_status_text='check if record -> {} in table -> {}'.format(column_name, table))
    db_entry = db[table].find_one({'column': column_name})
    if db_entry:
        status_logger(non_status_text='record -> {} found'.format(column_name))
        return db_entry['_id']
    else:
        status_logger(
            non_status_text='record -> {} NOT found'.format(column_name))
        return None
