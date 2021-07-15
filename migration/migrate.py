import psycopg2
import datetime
import configparser

# config
config = configparser.ConfigParser()
config.read('../config.ini')
database = config['DATABASE']
# database["dbname"]

# connect db 1
con = psycopg2.connect(
	host = database["host"],
	database = database["dbname"],
	user = database["user"],
	password = database["password"],
	)

# cursor
cur = con.cursor()

# users
cur.execute("""

	CREATE TABLE users (
	id serial PRIMARY KEY,
	username VARCHAR ( 255 ) NOT NULL,
	password VARCHAR ( 255 ) NOT NULL);

	""")

# device
cur.execute("""

	CREATE TABLE device (
	id serial PRIMARY KEY,
	dev_type VARCHAR ( 255 ) NULL,
	dev_name VARCHAR ( 255 ) NULL,
	dev_cor_lat VARCHAR ( 255 ) NULL,
	dev_cor_long VARCHAR ( 255 ) NULL
	);

	""")

# data
cur.execute("""

	CREATE TABLE data (
	id serial PRIMARY KEY,
	device_id INT NULL,
	data_smoke VARCHAR ( 255 ) NULL,
	data_vibration VARCHAR ( 255 ) NULL,
	data_mic VARCHAR ( 255 ) NULL,
	data_motion VARCHAR ( 255 ) NULL,
	data_active INT NULL,
	data_created_at timestamp NOT NULL DEFAULT NOW()
	);

	""")

# save data to db
con.commit()

# close cursor
cur.close()
con.close()
print('DONE MIGRATE')