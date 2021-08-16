from django.db import connection
import pandas as pd
import json
from Bigflow.Transaction.Model import mFET

from django import forms
from django.db import models

class Service_model():
    def __init__(self):
        self.producttype_gid = 0
        self.supplier_gid = 0
        self.customer_gid =0
        self.action = 0
        self.date = ''
        self.status =''
        self.entity_gid = 0
        self.employee_gid = 0
        self.SERVICE_JSON =''
        self.product_gid =''
        self.type =''
        self.courier_gid = 0
        self.Dispatch_date =''
        self.send_by = ''
        self.awbno = 0
        self.dispatch_mode = ''
        self.dispatch_type = ''
        self.packets = 0
        self.weight = 0
        self.dispatch_to = ''
        self.city = ''
        self.state =''
        self.pincode = 0
        self.remark = ''
        self.returned = ''
        self.returned_on = ''
        self.returned_remark = ''
        self.pod = 0
        self.pod_image = ''
        self.isactive = ''
        self.isremoved = ''
        self.dispatch_gid = 0
        self.SERVICE = ' '
        self.ref_gid = 0
        self.ref_no = 0


    def get_producttype(self):
        cursor = connection.cursor()
        parameters = (self.producttype_gid, '')
        cursor.callproc('sp_producttype_get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        producttype = pd.DataFrame(rows, columns=columns)
        return producttype

    def get_productname(self):
        cursor = connection.cursor()
        parameters = (self.producttype_gid,self.supplier_gid)
        cursor.callproc('sp_Prodtype_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        productname = pd.DataFrame(rows, columns=columns)
        return productname

    def get_customer(self):
        cursor = connection.cursor()
        parameters = (self.customer_gid,'','',"{}",self.entity_gid,'')
        cursor.callproc('sp_Customer_Get',parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_customerddl = pd.DataFrame(rows, columns=columns)
        return df_customerddl

    def set_servicedtl(self):
        cursor = connection.cursor()
        jsondata = self.SERVICE_JSON
        SERVICE_JSON = json.dumps(jsondata)
        parameters = (self.action,self.date,self.customer_gid,self.status,SERVICE_JSON,self.dispatch_gid,self.entity_gid,self.employee_gid,'')
        cursor.callproc('sp_SRService_Set',parameters)
        cursor.execute('select @_sp_SRService_Set_8')
        output_msg = cursor.fetchone()
        return output_msg

    def get_Servicedtl(self):
        cursor = connection.cursor()
        parameters = (self.from_date,self.to_date,self.customer_gid,self.employee_gid,self.product_gid,self.service_gid,self.entity_gid,self.status,'')
        cursor.callproc('sp_SRService_Get',parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        service_out = pd.DataFrame(rows,columns=columns)
        return service_out

    def set_Dispatch(self):
        cursor = connection.cursor()
        jsondata = self.SERVICE_JSON
        SERVICE_JSON = json.dumps(jsondata)
        parameters = (self.action,self.type,self.in_out,self.courier_gid,self.Dispatch_date,self.send_by,
                      self.awbno,self.dispatch_mode,self.dispatch_type,self.packets,self.weight,
                      self.dispatch_to,self.address,self.city,self.state,self.pincode,self.remark,
                      self.returned,self.returned_on,self.returned_remark,self.pod,
                      self.pod_image,self.isactive,self.isremoved,self.dispatch_gid,
                      SERVICE_JSON,self.status,self.entity_gid,self.employee_gid,'')
        cursor.callproc('sp_DispatchSPs_Set',parameters)
        cursor.execute('select @_sp_DispatchSPs_Set_29')
        output_msg = cursor.fetchone()
        return output_msg

    def get_courier(self):
        cursor = connection.cursor()
        parameters = (self.courier_gid,self.courier_name,self.entity_gid)
        cursor.callproc('sp_Courier_Get',parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_customerddl = pd.DataFrame(rows, columns=columns)
        return df_customerddl

    def set_Repair(self):
        cursor = connection.cursor()
        jsondata = self.SERVICE_JSON
        SERVICE_JSON = json.dumps(jsondata)
        parameters = (self.action,SERVICE_JSON,self.entity_gid,self.employee_gid,'')
        cursor.callproc('sp_Components_Set', parameters)
        cursor.execute('select @_sp_Components_Set_4')
        output_msg = cursor.fetchone()
        return output_msg


    def get_component(self):
        cursor = connection.cursor()
        parameters = (self.component_gid,self.service_gid,self.entity_gid,'')
        cursor.callproc('sp_Components_Get',parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_customerddl = pd.DataFrame(rows, columns=columns)
        return df_customerddl

    def set_PODDispatch(self):
        cursor = connection.cursor()
        parameters = (self.action,self.type,self.courier_gid,self.Dispatch_date,self.send_by,
                      self.awbno,self.dispatch_mode,self.dispatch_type,self.packets,self.weight,
                      self.dispatch_to,self.address,self.city,self.state,self.pincode,self.remark,
                      self.returned,self.returned_on,self.returned_remark,self.pod,
                      self.pod_image,self.isactive,self.isremoved,self.dispatch_gid,self.status,
                      self.entity_gid,self.employee_gid,'')
        cursor.callproc('sp_Dispatch_Set',parameters)
        cursor.execute('select @_sp_Dispatch_Set_27')
        output_msg = cursor.fetchone()
        return output_msg

    def get_employee(self):
        cursor = connection.cursor()
        Parameters = ('0','','0','ALL', '',self.jsonData,'')
        cursor.callproc('sp_Employee_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_Employee_Get_6')
        out_put = cursor.fetchone()
        rows = list(rows)
        df_employee = pd.DataFrame(rows, columns=columns)
        return df_employee

    def Location_Get(self):
        cursor = connection.cursor()
        parameters = (self.location_gid,self.entity_gid,'')
        cursor.callproc('sp_Address_Get',parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        service_out = pd.DataFrame(rows,columns=columns)
        return service_out

    def Dispatch_Get(self):
        cursor = connection.cursor()
        parameters = (self.action,self.entity_gid,'')
        cursor.callproc('sp_Dispatch_Get',parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        dispatch_out = pd.DataFrame(rows,columns=columns)
        return dispatch_out



class Document(models.Model):
    docfile = models.FileField(upload_to='pod/%Y/%m/%d')

class UploadFileForm(forms.Form):
    #title = forms.CharField(max_length=50)
    file = forms.FileField()

