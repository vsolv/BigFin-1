# from __future__ import absolute_import, unicode_literals
# from celery import task
# from django.db import connection
# import pandas as pd
#
# @task()
# def task_number_one():
#     cursor = connection.cursor()
#     parameters = ('SUPPLIER_DETAILS',2,1, '')
#     parameters = ('COLUMN', 'ECF_INSERT', '{}', 'Y',
#  '{"Entity_Gid": [1]}', 1,  '')
#     cursor.callproc('sp_APExpense_Set', parameters)
#     cursor.execute('select @_sp_APExpense_Set_6')
#     sp_out_message = cursor.fetchone()
#     return {"MESSAGE": sp_out_message[0]}
