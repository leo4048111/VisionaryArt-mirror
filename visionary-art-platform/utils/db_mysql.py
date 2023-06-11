#!/bin/env python
# -*- coding: utf-8 -*-
from configs import db_config
# import records
import sqlalchemy
from sqlalchemy import text
from sqlalchemy_utils import database_exists, create_database

from utils import common
import os

class DBMySql(object):
    db_mysql = {}

    @staticmethod
    def reloadMySql(dbname):
        mysql_dict = db_config.config.get(dbname)
        if mysql_dict:
            database_url = "mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}".format(
                **mysql_dict)
            # 设置连接池的失效时间，解决"MySQL server has gone away"
            # DBMySql.db_mysql[dbname] = records.Database(database_url, pool_recycle=60*50)

            engine = sqlalchemy.create_engine(database_url, pool_recycle=60*50, pool_size=100, max_overflow=1000, pool_timeout=60*5, echo=False)
            DBMySql.db_mysql[dbname] = engine
            if not database_exists(engine.url):
                create_database(engine.url, encoding='utf8mb4', template='innodb')
                with engine.connect() as connection:
                    sql_path = os.path.join(os.path.join(common.root_dir(), 'sql'), 'create_table.sql')
                    with open(sql_path, 'r', encoding='utf-8') as f:
                        sql_scripts = f.read().split(';')
                        for sql_script in sql_scripts:
                            if sql_script.strip():  # 确保 SQL 语句不是空的
                                connection.execute(text(sql_script))

    @staticmethod
    def GetMySql(dbname):
        if not DBMySql.db_mysql.get(dbname):
            DBMySql.reloadMySql(dbname)
        return DBMySql.db_mysql.get(dbname)
