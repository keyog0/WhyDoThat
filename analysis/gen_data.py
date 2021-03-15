import pymysql
import pandas as pd
import json
from model.db_loader import MySQL

sql_db = MySQL(key_file='../keys/localhost_sql_key.json',
               database='crawl_job')
with open('model/dtype_map.json') as file :
    dtype_map = json.load(file)

class GenerateData :
    def get_dataframe(self) :
        sql = "select job_detail.title,job_detail.skill_tag from job_detail ;"
        sql_db.execute(sql)
        return pd.DataFrame(sql_db.fetchall())