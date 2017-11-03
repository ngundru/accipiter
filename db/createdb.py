# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 20:12:41 2017

@author: ngund_000
"""

import sqlite3
#import datetime
import time
import pandas as pd

conn = sqlite3.connect('/home/ubuntu/flaskapp/db/users.db')
c = conn.cursor()
c.execute('''
          CREATE TABLE users (
           username varchar(35)
          ,password varchar(25)
          ,createdate date
          ,practicename varchar(50)
          ,contactname varchar(50)		  
          ,contactphone varchar(50)
          ,contactemail varchar(50)  
          ,nodoctors varchar(50)
          ,nolocations varchar(50)
          ,MailingAddress1 varchar(50)
          ,MailingAddress2 varchar(50)	  
          ,MailingAddress3 varchar(50)		  
          ,MailingAddressCity varchar(50)
          ,MailingAddressState varchar(50)	
          ,MailingAddressZip varchar(50)	  
          ,BillingAddress1 varchar(50)	  
          ,BillingAddress2 varchar(50)	  
          ,BillingAddress3 varchar(50)	  
          ,BillingAddressCity varchar(50)
          ,BillingAddressState varchar(50)	
          ,BillingAddressZip varchar(50)
          ,PracticeType varchar(50)		  	  
          ,PracticeAge varchar(50)	  
          ,nopatients varchar(50)	  
          ,EstSupplySpend varchar(50)
          ,FiscalYearEnd varchar(50) 
          );  
          ''')     
c.close()
          

       