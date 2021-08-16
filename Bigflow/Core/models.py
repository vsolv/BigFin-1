import datetime
import logging
import logging.handlers
import os
import socket

import time
import traceback

import Bigflow
from Bigflow.settings import BASE_DIR,Password_Key
from base64 import b64encode, b64decode
from simplecrypt import encrypt, decrypt
import xmltodict
import pprint
import json
from environs import Env
env = Env()
env.read_env()
import requests as rq

from Bigflow.xmlread import fun
from importlib import import_module
from django.conf import settings
SessionStore = import_module(settings.SESSION_ENGINE).SessionStore

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# # Handler
# LOG_FILE = '/opt/python/log/app.out.apperror.log'
# handler = logging.handlers.RotatingFileHandler(LOG_FILE)
# handler.setLevel(logging.INFO)
#
# # Formatter
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#
# # Add Formatter to Handler
# handler.setFormatter(formatter)
#
# # add Handler to Logger
# logger.addHandler(handler)




# log_path = '/home/ramesh/Desktop/BIN/'
log_path = '/opt/python/log/'
# if not os.path.exists(log_path):
#     os.makedirs(log_path)

# logging.basicConfig(filename=log_path + 'app.out.apperror.log', level=logging.ERROR,
#                     format='%(asctime)s %(levelname)s %(name)s %(message)s')

logger=logging.getLogger(__name__)

def convertDate(stringDate):
    return datetime.datetime.strptime(stringDate, "%d/%m/%Y").strftime("%Y-%m-%d")
def convertdbDate(stringDate):
    return datetime.datetime.strptime(stringDate, "%d-%b-%Y").strftime("%Y-%m-%d")
def convertDateTime(stringDate):
    return datetime.datetime.strptime(stringDate, "%d/%m/%Y")
def outputReturn(tubledtl, index):
   temp = tubledtl[0].split(',')
   if (len(temp) > 1):
       if (index == 0):
           return int(temp[0])
       else:
           return temp[1]
   else:
       return temp[0]
def outputReturns(tubledtl, index):
    temp = tubledtl[0].split(',')
    if (len(temp) > 1):
        if (index == 0):
            return int(temp[0])
        elif(index == 2):
            return int(temp[2])
        elif(index == 3):
            return (temp[3])
        else:
            return temp[1]
    else:
        return temp[0]

def localip():
    return env.str("APP_URL")

def ip_address_validate():
    return env.str("Two_Factor_Auth_KVB_Whitelisted_IPs")

def two_factor_authenticate():
    return env.str("Two_Factor_Auth_Status")

def server_environ_var():
    return env.str("SERVER_ENVIRONMENT")


def token():   # NEED TO REMOVE BUT NOW FOR TEMPORARY
    return "Token 7111797114100105971106449505132"

def clientapi():
    return env.str("API_CLIENT_URL")

def memoapi_url():
    return env.str("MEMO_API_URL")

def master_accesstoken():
    return env.str("API_CLIENT_URL") + "/next//v1/oauth/cc/accesstoken"

def master_sync():
    return env.str("API_CLIENT_URL") + "/next/v1/mw/master/sync"

def senderemail():
    return env.str("TO_EMAIL")

def s3_bucket_name():
    return env.str("S3_BUCKET_NAME")

def ADToken():
    return env.str("API_CLIENT_ID")

def ClientSecret():
    return env.str("API_CLIENT_SECRET")

import json
import re
common_str = "^[A-Za-z0-9.]+$";
inject_xss = "^[!|~|@|#|$|%|&|*|-|\w]+$"
def load_regex():
    regex = {"email":"^[A-Za-z]+$"}
    return regex
# i = fun()

def main_fun(e):
    return True

def main_fun1(jsondata,f):
    return True
#    test_list = fun()
#    res = test_list[1:-1]
#    Dict = eval(res)
#    url = f
#    e = jsondata.decode("utf-8")
#    v = json.loads(e)
#    body = v
#    for i in Dict:
#        if i['@path'] == url:
#            v = i['params']
#            e = v['param']
#            r = e[1:-1]
#            # t = r['@name']
#            do_server_validation(body,e)
#            break
#    else:
#        raise Exception("Parameter Has Not provided In Validation")



class RegexValidator:
    __validator = None
    __regex_map = load_regex()
    def __init__(self):
            self.__validator = self
    def __init__(self, regex_map):
            self.__validator = self
            self.__regex_map = regex_map
    def get_regex(self,pattern_name):
        if pattern_name in self.__regex_map:
            return self.__regex_map[pattern_name]
        else:
            return common_str
    def validate(self,pattern_name, value):
        if pattern_name == '':
            pattern_name = "default"
        pattern = self.get_regex(pattern_name)
        pattern = inject_xss
        # print(re.search(pattern, value))
        # print(pattern)
        # print(value)
        if re.search(pattern, value) == None:
            return True
        else:
            return False
def do_server_validation(validationObj,xmldata):
    if is_primitive(validationObj):
        do_validate('', validationObj, type(validationObj),xmldata)
    elif type(validationObj) is dict:
        iterate_json('', validationObj,xmldata)
    elif type(validationObj) is list:
        iterate_list('', validationObj,xmldata)
def validate_inject_xss_str(ty,value):
    if ty == 'stringonly':
        xss_str_arr =  ["<",">","!","@","#","$","%","^","&","*","(",")","[","]","{","}","?"]
        for xss_str in xss_str_arr:
            if xss_str in value:
                return False
        return True
    if ty == 'specialchar':
        return True
    if ty == 'numberonly':
        return True


def do_validate(key, value, val_type,xmldata):
    regx = RegexValidator(load_regex())
    if key == '':
        key = common_str;
    if val_type is str:
        for name in xmldata:
            if key in name['@name']:
                ty = name['@type']
                #validation_result = regx.validate(key,ty)
                validation_result = validate_inject_xss_str(ty,value)
            else:
                validation_result = True
                # print(validation_result)
            if validation_result == False:
                raise Exception("Invalid Input Has Given")
    if val_type is int:
        for name in xmldata:
            if key in name['@name']:
                ty = name['@type']
                # validation_result = regx.validate(key,ty)
                validation_result = validate_inject_xss_str(ty, value)
            else:
                validation_result = True
                # print(validation_result)
            if validation_result == False:
                raise Exception("Invalid Input Has Given")


def iterate_json(key, jsonObject,xmldata):
    for key in jsonObject:
        value = jsonObject[key]
        if is_primitive(value):
            do_validate(key, value, type(value),xmldata)
        if type(value) is list:
            iterate_list(key, value,xmldata)
        if type(value) is dict:
            iterate_json(key, value,xmldata)
def is_primitive(value):
    if type(value) is str or type(value) is int or type(value) is float or type(value) is bool:
        return True
    return False
def iterate_list(key, jsonArr,xmldata):
    length = len(jsonArr)
    for i in range(length):
        if is_primitive(jsonArr[i]):
            do_validate(key, jsonArr[i], type(jsonArr[i]),xmldata)
        if type(jsonArr[i]) is list:
            iterate_list(key, jsonArr[i],xmldata)
        if type(jsonArr[i]) is dict:
            iterate_json(key, jsonArr[i],xmldata)
from hashids import Hashids
def decrpt(encrypt_text):
    hashids = Hashids(salt=Password_Key)
    hashid = hashids.decode(encrypt_text)
    data = hashid[0]
    return data
def encrypt1(text):
    hashids = Hashids(salt=Password_Key)
    ints = hashids.encode(text)
    return ints
def Excelfilename(filename):
    File_name=time.strftime(filename+"_%Y_%m_%d_%H_%M.xlsx")
    return File_name

from django.db import connection
def get_server_date(type):
    cursor = connection.cursor()
    parameters = (type, '')
    cursor.callproc('sp_Server_Get', parameters)
    if cursor.description != None:
        rows = cursor.fetchone()
        cursor.execute('select @_sp_Server_Get_1')
        outmsg_sp = cursor.fetchone()
        return rows
    else:
        return ''
host_url=env.str('MEMO_API_URL')+'/'
mtom_token_generated=True
class MasterRequestObject():
    fields = {"STATE": ("code","name", "country_id"), "DISTRICT": ("name", "state_id"), "CITY": ("name", "state_id"),
              "PINCODE": (), "PRODUCT CATEGORY": ("name", "isprodservice", "stockimpact", "client_id"), "PRODUCT": (
        "name", "weight", "unitprice", "uom_id", "hsn_id", "category_id", "subcategory_id", "producttype_id",
        "productcategory_id"), "PRODUCT TYPE": ('productcategory_code', 'name', 'code'), "UOM": ('name', 'code'), "BANK": ("name"),
              "PAYMODE": ('name', 'code'), "DESIGNATION": ('name', 'remarks', 'code'), "TAX": ("name", "receivable", "payable", "glno"),
              "SUBTAX": ("tax_id", "name", "remarks", "glno"), "TAXRATE": ("subtax_id", "code", "name", "rate"),
              "COMMODITY": ('code',"name"), "DELMAT": ("commodity_id", "employee_id", "type", "limit"),
              "BS": ("no", "name", "remarks", "description"), "CC": ("no", "name", "remarks", "description"),
              "CATEGORY": ("code","no", "name", "glno", "isasset", "isodit"),
              "SUBCATEGORY": ("no", "name", "category_id", "gstrcm", "glno", "expense_id", "gstblocked", "assetcode")};

    execute=True
    all_master_urls = {
        'MAINTENANCE': {
            'CITY MASTER': {
                'STATE': 'mstserv/statemtom',
                'DISTRICT': 'mstserv/districtmtom',
                'CITY': 'mstserv/citymtom',
                'PINCODE': 'mstserv/pincodemtom'
            },
            'PRODUCT_MASTER': {
                'PRODUCT CATEGORY': 'mstserv/pdtcatmtom',
                'PRODUCT': 'mstserv/productmtom',
                'PRODUCT TYPE': 'mstserv/pdttypemtom',

            },
            'COMMON MASTER': {
                'UOM': 'mstserv/uommtom',
                'BANK': 'mstserv/bankmtom',
                'BANK BRANCH': 'mstserv/bankbranchmtom',
                'PAYMODE': 'mstserv/paymodemtom',
                'DESIGNATION': 'mstserv/designationmtom',
                'CONTACTTYPE(STOP)': 'mstserv/contacttype',
            }
        },
        'PROCUREMENT': {
            'COMMODITY': 'mstserv/commoditymtom',
            'DELMAT': 'prserv/delmatmtom',
            'BS': 'usrserv/businesssegmentmtom',
            'CC': 'usrserv/costcentremtom',
            'CATEGORY':'mstserv/Apcategorymtom',
            'SUBCATEGORY':'mstserv/Apsubcategorymtom',
        },
        'TAX MASTER':{
            'TAX':'mstserv/taxmtom',
            'SUB TAX':'mstserv/subtaxmtom',
            'TAX RATE':'mstserv/taxratemtom',
            'TAXACT':'mstserv/taxrate_inactive',
            'HSN':'mstserv/hsnmtom'
        }
    }
    def __init__(self,type,parameter,method,sync_data=None):
        self.param_data=self.get_response(type,parameter,method)

    env = Env()
    env.read_env()
    host_url=env.str('MEMO_API_URL')+'/'
    def set_parameter(self,parameter):
        self.parameter=parameter
    def get_url(self,mastertype):
        url_obj=''
        for main,value in self.all_master_urls.items():
            for master_cat,master_det in value.items():
                if(master_cat.replace(' ','')==mastertype.replace(' ','')):
                    url_obj=master_det
                    break
                if (isinstance(master_det, dict)):
                    for master,url in master_det.items():
                        if(master.replace(' ','')==mastertype.replace(' ','')):
                            url_obj=url
                            break
                else:
                    if(master_cat==master):
                        url_obj=master_det
                        break
        if url_obj is not None:
            return self.host_url+url_obj
    # def get_params(self):
    # return self.params_data
    def set_method(self,method_type):
        self.method_type=method_type
    def get_response(self,type,parameter,method):
        self.master_url = self.get_url(type)
        ent_gid=parameter.pop('Entity_Gid')
        create_by=parameter.pop('create_by')
        self.set_method(method)
        parameter_json = json.dumps(parameter)
        userparameters_json=json.dumps({
            "username": "apuser",
            "password": "dnNvbHYxMjM="
        })
        # for i in range(5):
        #     auth_token = rq.post(host_url + 'usrserv/auth_token', data=userparameters_json).json()['token']
        #     header = {'Authorization': 'Token ' + auth_token}
        #     respo = rq.get(self.master_url.replace('mtom',''), headers=header)
        #     logger.error(respo.text)
        # try:
        #     auth_token = None
        #     auth_token = rq.post(host_url+'usrserv/auth_token', data=userparameters_json).json()['token']
        #     logger.error(str(auth_token))
        #     while(auth_token==None):
        #         pass
        #     if(auth_token==None):
        #         logger.error([{"MASTER_WseFin_ApiCall": 'Token not generated'}])
        #     header = {'Authorization': 'Token ' + auth_token}
        #     # header = {'Authorization': 'Token ' + 'auth_token'}
        # except:
        #     logger.error(str(traceback.print_exc()))
        #     logger.error([{"MASTER_WseFin_ApiCall": 'Token not generated'}])
        #     status = 'FAIL
        try:
            header={'Authorization': 'Token ' + mtom_token_generate(userparameters_json)}
        except:
            logger.error([{"FA_WseFin_ApiCall_Before": 'API CONNECTION ERROR'}])
        if self.method_type=='POST' or 'post':
            logger.error(self.master_url)
            if(self.execute):
                try:
                    if('sync' in parameter.keys()):
                        sync_data=parameter.pop('sync')
                    else:
                        sync_data=0
                    logger.info('Inserting data in the Micro service..')
                    # print(parameter_json)
                    logger.info('MASTER_DATA:'+str(parameter_json))
                    respo=rq.post(self.master_url, data=parameter_json,headers=header)
                    while(respo==None):
                        pass
                    logger.info(respo.text)
                    status=None
                    try:
                        resp_obj=json.loads(respo.text)
                    except:

                        status='FAIL'
                    parameter_json=json.loads(parameter_json)
                    try:
                        if (status == 'FAIL'):
                            parameter_json['status'] = status
                    except:
                        pass
                    if (respo.status_code != 200):
                        logger.error('CHECK API CONNECTION OR CHECK API CALL')
                        status = 'FAIL'
                        parameter_json['status'] = status
                    else:
                        status = 'SUCCESS'
                        parameter_json['status'] = status
                    try:
                        if(resp_obj['code'] == "UNEXPECTED_ERROR"):
                            logger.error([{"MASTER_WseFin_ApiCall": 'Error in Data passed.'}])
                            if(resp_obj['description']=='Duplicate Name'):
                                status='PASS'
                            if(type=='BANK BRANCH'):
                                logger.error([{"MASTER_WseFin_ApiCall": 'BankBranch Pincode data mismatch in microservice'}])
                            status = 'FAIL'
                            parameter_json['status'] = status
                        if (resp_obj['code'] == "INVALID_DATA"):
                            logger.error([{"FA_WseFin_ApiCall_After": 'API Called'}])
                            status = 'FAIL'
                            parameter_json['status'] = status
                    except:
                        logger.error(str(traceback.print_exc()))
                except:
                    logger.error(str(traceback.print_exc()))
            else:
                logger.info(type+" API call didn't execute because you have set the API_EXECUTE=False in env")

            try:
                if(sync_data!=1):
                    parameter_json['Entity_Gid']=decrpt(ent_gid)
                    parameter_json['create_by'] = decrpt(create_by)
                    parameter_json['Action_Type']='create'

                    #print(parameter_json)
                    parameter=("SYNC",'{"Action_Type":"get_date","Entity_Gid":'+str(int(parameter_json["Entity_Gid"]))+',"create_by":'+str(int(parameter_json["create_by"]))+',"Master_Name":"'+type.replace(' ','')+'"}','@message')
                    if(type=='TAXACT'):
                        parameter = ("SYNC", '{"Action_Type":"get_date","Entity_Gid":' + str(
                            int(parameter_json["Entity_Gid"])) + ',"create_by":' + str(
                            int(parameter_json["create_by"])) + ',"Master_Name":"' + type.replace(' ', '') + '","tax_code":"'+str(parameter_json['tax_code'])+'"}',
                                     '@message')

                    #print(parameter)
                    cursor=connection.cursor()
                    cursor.callproc('sp_APIBigflowOrmSync_Get',parameter)
                    date=cursor.fetchone()
                    # print(qry)
                    parameter_json['create_date']=str(date[0])
                    # print(parameter_json)
                    parameter_json['master']=type

                    add_sync_data('create',parameter_json)
                else:

                    parameter_json['status']=status
                    parameter_json['Entity_Gid'] = 1
                    parameter_json['create_by'] = 1
                    parameter_json['Action_Type'] = 'update'
                    # print(parameter_json)
                    # print(parameter_json)
                    parameter_json['master'] = type
                    #print(parameter_json)
                    add_sync_data('update', parameter_json)

            except:
                traceback.print_exc()
            return respo
nowtime=datetime.datetime.now()
def delmat_tran_to_type(dtran):
    if (dtran == 197):
        out = 4
    elif (dtran == 191):
        out = 3
    elif (dtran == 132):
        out = 2
    elif (dtran == 133):
        out = 1
    return out
fields = {"STATE": ("code","name", "country_id"), "DISTRICT": ("code","name", "state_id"), "CITY": ("code","name", "state_id"),
          "PINCODE": ('city_code','district_code','no'), "PRODUCTCATEGORY": ("code","name", "isprodservice", "stockimpact", "client_id"), "PRODUCT": ('code','name', 'weight', 'unitprice','uom_code', 'hsn_code', 'category_code', 'subcategory_code', 'productcategory_code', 'producttype_code'),
          "PRODUCTTYPE": ("code","name","productcategory_code" ), "UOM": ("code","name"), "BANK": ("code","name"),
          "PAYMODE": ("code","name"), "DESIGNATION": ("code","name"), "TAX": ("code","name", "receivable", "payable", "glno"),
          "SUBTAX": ("code","tax_id", "name", "remarks", "glno"), "TAXRATE": ("subtax_id", "code", "name", "rate"),
          "COMMODITY": ("code","name"), "DELMAT": ("commodity_id", "employee_id", "type", "limit"),
          "BS": ("code", "name","no", "remarks", "description"), "CC": ('code',"no", "name", "remarks", "description"),
          "CATEGORY": ("code","no", "name", "glno", "isasset", "isodit"),
          "SUBCATEGORY": ("code","no", "name", "category_id", "gstrcm", "glno", "expense_id", "gstblocked", "assetcode"),
          "BANKBRANCH":("code","bank_gid","address_gid","ifsccode",'microcode',"name"),
          "HSN":("code","description","cgstrate_id","sgstrate_id","igstrate_id"),
          "TAXRATEEDIT":("tax_code",'isactive')};

def schedule_apiRun():
    parameter = {}
    logger.info("Started scheduled API Sync at "+str(nowtime))
    cursor = connection.cursor()
    #cursor.execute('call sp_APIBigflowOrmSync_GET ("SYNC", \'{"Entity_Gid": 1, "Action_Type": "sync"}\',@messsage)');
    parameter = ("SYNC", '{"Entity_Gid": 1, "Action_Type": "sync"}', '@message')
    cursor.callproc('sp_APIBigflowOrmSync_GET',parameter)
    rows = cursor.fetchall()
    for row in rows:
        parameter={}
        logger.error("SYNC DATA: "+str(row))
        #print(json.loads(row[0]))
        row=json.loads(row[0])

        for data in row:
            mst_name = data.pop(0)
            records=data.pop(0)
            if(records==None or records=='NO DATA'):
                continue
            records='['+records+']'
            records=json.loads(records)
            for record in records:
                print(record)
                create_date=record.pop(-1)
                #print(mst_name,record)
                data_fields = fields[mst_name]
                #print(record,fields)
                parameter={}
                for data, fld in zip(record, data_fields):
                        parameter[fld] = data
                parameter['Entity_Gid'] = 1
                parameter['create_by'] = 1
                parameter['sync'] = 1
                parameter['create_date']=create_date
                print(parameter)
                print(mst_name)
                if(mst_name not in ('PRODUCTCATEGORY','UOM','PAYMODE','DESIGNATION','BANK','BS','TAX','CATEGORY','STATE','CC','COMMODITY','TAXRATEEDIT')):
                    codes=get_sync_data_from_id(mst_name,parameter)
                    print(parameter,mst_name,"codes: ",codes)
                    parameter.update(codes)
                    if (mst_name == 'DELMAT'):
                        print(parameter['type'])
                        parameter['type'] = delmat_tran_to_type(parameter['type'])
                    if(mst_name=='BANKBRANCH'):
                        parameter['address_id']={'line1':parameter.pop("line1"),'line2':parameter.pop("line2"),'line3':parameter.pop("line3"),
                                                'pincode_code':parameter.pop('pincode_code'),'city_code':parameter.pop('city_code'),
                                                 'district_code':parameter.pop('district_code'),'state_code':parameter.pop('state_code')
                                                 }
                else:
                    if(mst_name=='PRODUCTCATEGORY'):
                        parameter['isprodservice']=True
                        if(parameter['stockimpact']=="Y"):
                            parameter['stockimpact']=True
                        else:
                            parameter['stockimpact'] = False
                    if(mst_name=="BS"):
                        parameter["remarks"]=parameter["description"]
                    if (mst_name == "CC"):
                        parameter["description"] = parameter["remarks"]
                    if (mst_name == "TAX"):
                        parameter["receivable"] = str(parameter["receivable"])
                        parameter["payable"] = str(parameter["payable"])
                    if (mst_name == "SUBTAX"):
                        parameter.pop("tax_id")
                    if (mst_name == "TAXRATE"):
                        parameter.pop("subtax_id")
                    if (mst_name == "TAXRATE"):
                        parameter.pop("state_id")
                    if (mst_name == "SUBCATEGORY"):
                        parameter.pop("category_id")
                        parameter.pop("expense_id")
                        if(parameter['gstrcm']=="N"):
                            parameter['gstrcm']=0
                        else:
                            parameter['gstrcm']=1
                        if(parameter['gstblocked']=="N"):
                            parameter['gstblocked']=0
                        else:
                            parameter['gstblocked']=1
                    if (mst_name == "CATEGORY"):
                        if(parameter["isasset"]=="N"):
                            parameter["isasset"] =0
                        else:
                            parameter["isasset"] = 1
                        parameter["no"]=int(parameter["no"])
                        parameter["glno"] = int(parameter["glno"])
                    if(mst_name=='TAXRATEEDIT'):
                        mst_name='TAXACT'

                mrobject = MasterRequestObject(mst_name, parameter, 'POST')

            # parameter['master']=mst_name
            # parameter['Action_Type']='update'
            # parameter['Entity_Gid']=1
            # parameter['create_by']=1
            # parameter['create_date']=str(create_date)
            # add_sync_data('update', parameter)


def add_sync_data(type, data):
    #print(data)
    if (type == 'create'):
        try:
            print(data)
            insert_cols=['create_date','status','create_by','Entity_Gid','master','Action_Type']
            finalval=data.copy()
            data1={}
            for val in insert_cols:
                data1[val]=finalval[val]
            logger.info("Data created in the Mono  successfully")
            #print('updating sync_data table')
            cursor = connection.cursor()
            mst=data.pop('master')
            #print(data1)
            parameter=(mst.replace(' ',''),str(data1).replace("'",'"'),'@message')
            logger.error(str(parameter))
            cursor.callproc('sp_APIBigflowOrmSync_GET',parameter)

        except:
            traceback.print_exc()
    elif (type == 'update'):
        update_cols = ['create_date', 'status', 'create_by', 'Entity_Gid', 'master', 'Action_Type']
        finalval = data.copy()
        finaldata = {}
        #print(data)
        for val in update_cols:
            data[val] = finalval[val]
        mst_type=data['master']
        logger.info("Updating sync data table")
        cursor = connection.cursor()
        #print(data)
        parameter=(mst_type.replace(' ',''),str(data).replace("'",'"').replace('True','"true"').replace('False','"false"'),'@message')
        print(parameter)
        cursor.callproc('sp_APIBigflowOrmSync_GET', parameter);
def get_data_from_id(master_name,data):
    cursor=connection.cursor()
    params={}
    params['Entity_Gid']=1
    params['Master_Name']=master_name
    params['Action_Type']='get_data_from_id'
    params['Data']=data
    parameter=('SYNC',str(params).replace("'",'"'),'@message')
    #print(parameter)
    cursor.callproc('sp_APIBigflowOrmSync_GET',parameter)
    codes=json.loads(cursor.fetchone()[0])
    #print(codes)
    data_fields={'Product':['uom_code','hsn_code','category_code','subcategory_code','productcategory_code','producttype_code','code'],
                 'Product_Type':['Producttype_Category_code','code'],
                 'TAX':['code'],
                 'BANKBRANCH':['bank_code','city_code','district_code','state_code','code'],
                 'SUBTAX':['tax_code','code'],
                 'DISTRICT':['state_code','code'],
                 'CITY':['state_code','code'],
                 'PINCODE':['district_code'],
                 'TAXRATE':['subtax_code','code'],
                 'TAXACT':['tax_code'],
                 'PRODUCTCAT':['code'],
                 'STATE':['code'],
                 'APSUBCAT':['category_code','expense_code','code'],
                 'HSN':['cgstrate_code','cgstrate','sgstrate_code','sgstrate','igstrate_code','igstrate'],
                 'DELMAT':['commodity_code','employee_code'],
                 }
    out_data={}
    for master,master_fields in data_fields.items():
        if(master==master_name):
            for fields,code in zip(master_fields,codes):
                out_data[fields]=code
    return out_data
mtom_token=None
def set_mtom(value):
    Bigflow.Core.models.mtom_token=value
def mtom_token_generate(userparameters_json):
    try:
        mtom_token=Bigflow.Core.models.mtom_token
        if(mtom_token!=None):
            header = {'Authorization': 'Token ' + mtom_token}
            respo = rq.get(host_url+'mstserv/uom', headers=header)
            if(respo.status_code==403):
                auth_token = rq.post(host_url+'usrserv/auth_token', data=userparameters_json).json()['token']
                logger.error('Token generated')
                set_mtom(auth_token)
                return auth_token
            else:
                logger.error('token not generated')
                return mtom_token
        else:
            auth_token = rq.post(host_url + 'usrserv/auth_token', data=userparameters_json).json()['token']
            set_mtom(auth_token)
            logger.error('token generated')
            return auth_token
    except:
        logger.error(traceback.print_exc())
        logger.error('Token generation error in Master_Sync')



def get_sync_data_from_id(master_name,data):
    cursor=connection.cursor()
    params={}
    params['Entity_Gid']=1
    if master_name in ('PRODUCT','PRODUCTCATEGORY'):
        if(master_name=='PRODUCT'):
            master_name='Product'
    params['Master_Name']=master_name
    params['Action_Type']='sync_get_data_from_id'
    params['Data']=data
    #print("params: ",params)
    parameter=('SYNC',str(params).replace("'",'"'),'@message')
    print(str(parameter))
    cursor.callproc('sp_APIBigflowOrmSync_GET',parameter)
    codes=json.loads(cursor.fetchone()[0])
    #print("codes: ",codes)
    data_fields={'Product':['uom_code','hsn_code','category_code','subcategory_code','productcategory_code','producttype_code'],
                 'PRODUCTTYPE':['productcategory_code'],
                 'TAX':['code'],
                 'BANKBRANCH':['bank_code','line1','line2','line3','pincode_code','city_code','district_code','state_code'],
                 'SUBTAX':['tax_code'],
                 'DISTRICT':['state_code'],
                 'CITY':['state_code'],
                 'PINCODE':['city_code','district_code','state_code'],
                 'TAXRATE':['subtax_code','code'],
                 'TAXACT':['tax_code'],
                 'PRODUCTCAT':['code'],
                 'SUBCATEGORY':['category_code','expense_code'],
                 'HSN':['cgstrate_code','cgstrate','sgstrate_code','sgstrate','igstrate_code','igstrate'],
                 'DELMAT': ['commodity_code', 'employee_code'],
                 }
    out_data={}
    for master,master_fields in data_fields.items():
        if(master==master_name):
            for fields,code in zip(master_fields,codes):
                out_data[fields]=code
    return out_data
def multisystem_sync_create():
    cursor = connection.cursor()
    ip=socket.gethostbyname(socket.gethostname())
    params={'create_time':str(datetime.datetime.now())[0:18],'name':'MASTER_SYNC','sysip':ip,'Action_Type':'create_scheduler'}
    params['Entity_Gid'] = 1
    parameters=('SYNC',str(params).replace("'",'"'),'@message')
    cursor.callproc('sp_APIBigflowOrmSync_GET',parameters)
    time.sleep(2)
def get_sync_ip():
    params={}
    cursor = connection.cursor()
    params['Entity_Gid'] = 1
    params['Action_Type'] = 'get_scheduler'
    parameters=('SYNC',str(params).replace("'",'"'),'@message')
    cursor.callproc('sp_APIBigflowOrmSync_GET',parameters)
    ip=cursor.fetchone()
    return ip


