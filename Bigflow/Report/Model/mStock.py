from django.db import connection
import pandas as pd
from Bigflow.Master.Model import mVariable


class StockModel(mVariable.variable):

    # def __init__(self):
    #     self.filter_json = {}
    #     self.Classification = {}

    def get_stock(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.jsonData, self.from_date, self.to_date, self.product_gid,           self.supplier_gid,
                      self.entity_gid, '')
        cursor.callproc('sp_Stock_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_dp = pd.DataFrame(rows, columns=columns)
        cursor.execute('select @_sp_Stock_Get_8')
        sp_out_message = cursor.fetchone()
        return {"DATA": df_dp, "MESSAGE": sp_out_message[0]}

    def set_stock(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.json, self.stock_json, self.create_by, self.entity_gid,'')
        cursor.callproc('sp_Stock_Set', parameters)
        cursor.execute('select @_sp_Stock_Set_6')
        sp_out_message = cursor.fetchone()
        return {"MESSAGE": sp_out_message[0]}