from mongoengine import register_connection, connect

from documents.test_mongo import TestMongo

connection_params = {
    "name": 'crypto-test-bed',
    "host": 'localhost',
    "port": "27017",
    "username": 'binance_synch',
    "password": 'prout',
    "authentication_source": 'crypto-test-bed',
    "authentication_mechanism": 'SCRAM-SHA-1'

}

register_connection('default', **connection_params)

connect(alias='default')

test = TestMongo()
test.title='Mes boules'

test.save()
