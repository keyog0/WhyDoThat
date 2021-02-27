import json

def load_key(key_file) :
    with open(key_file) as key_file :
        key = json.load(key_file)
        print(key)
    return key

FLASK_ADMIN_SWATCH = 'cerulean'

SECRET_KEY = '123456790'

db = load_key(key_file='../keys/localhost_sql_key.json')
database = "crawl_job"
SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{database}?charset=utf8mb4"
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = False