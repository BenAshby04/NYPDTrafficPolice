import MySQLdb

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'db': 'NYPD'
}

conn = MySQLdb.connect(**db_config)