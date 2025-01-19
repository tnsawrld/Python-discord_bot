import mysql.connector
import configparser

config_database = configparser.ConfigParser()
config_database.read("./config.ini")

#mysql
DB_HOST = config_database['mysql']['host']
DB_USER = config_database['mysql']['user']
DB_PASS = config_database['mysql']['password']
DB_NAME = config_database['mysql']['db_name']

def Database_Connect():
    return mysql.connector.Connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )