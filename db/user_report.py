# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 20:02:43 2017

@author: ngund_000
"""

import sqlite3
#import datetime
import time
import pandas as pd

now = time.strftime("%Y-%m-%d")
#time.strftime("yyyy-mm-dd",now)

conn = sqlite3.connect('users.db')
c = conn.cursor()
#c.execute('''CREATE TABLE users (username varchar(35), password varchar(25), createdate date)''')
#c.execute("INSERT INTO users values ('ngundrum2','Loyola08','{}')".format(now))
df = pd.read_sql("Select * from users",conn)


#users = df['username'].tolist()
#df.set_index("username",drop=True,inplace=True)
#passwords = df.to_dict(orient="index")

#conn.commit()
conn.close()



df.to_csv('report.csv')