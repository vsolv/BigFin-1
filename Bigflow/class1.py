from django import forms
import pymysql
import pandas as pd
from django.http import JsonResponse
import json
from django.http import HttpResponse
from django.db import connection
from django.conf import settings
from django import template


global db




class login:
#    global db
    cursor = connection.cursor()


def get_login(str1,str2):

    global db
    db = pymysql.connect(host="PONRAJ", user="mysqlponraj", passwd="vsolv", db="galley")
    cur = db.cursor()

    cur.callproc("sp_UMLogin_Get",(0,str1,converttoascii(str2),''))

    columns = [d[0] for d in cur.description]
    ldict = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.execute('select @_sp_UMLogin_Get_3')
    id= cur.fetchone()
    ldist=[ldict,id]
    return ldist




def converttoascii(password):
    l=len(password)
    newuser=''
    for i in range(0,l):
        tmp=ord(password[i])
        temp = tmp - l
        g=len(str(temp))
        newuser = newuser + ("0" if g < 3 else "") + str(temp)
    return newuser

    @property
    def get_employee(self):

        return "hello"

def menulist(str1,str2):
    cur = db.cursor()
    cur.callproc("sp_UMEmployeevsMenu_Get",(str1,str2,''))
    columns = [d[0] for d in cur.description]
    ldict = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.execute('select @_sp_UMEmployeevsMenu_Get_2')
    id= cur.fetchone()
    ldist=[ldict,id]
    return ldist

class employee():

    def __init__(self,emp_gid,emp_name,emp_phone=None):
        self.emp_gid = emp_gid
        self.emp_name = emp_name
        self.emp_phone = emp_phone
