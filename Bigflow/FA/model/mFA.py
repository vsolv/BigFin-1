from django.db import connection
import pandas as pd
import json
import boto3
from Bigflow.Master.Model import mVariable
import Bigflow.Core.models as common

class FaModel(mVariable.variable):
    def get_fa_summary(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.filter_json, self.json_classification, '')
        cursor.callproc('sp_FAAssetProcess_Get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_FAAssetProcess_Get_4')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_fa_data = pd.DataFrame(rows, columns=columns)
            full_data = json.loads(df_fa_data.to_json(orient='records'))
            if 'assetdetails_imagepath' in df_fa_data.columns:
                for i in full_data:
                    img_data = []
                    if i.get('assetdetails_imagepath') != '0':
                        for j in json.loads(i.get('assetdetails_imagepath')):
                        # print(i.get('assetdetails_imagepath'))
                            path = image_path(self, j.get('file_path'))
                            img_data.append(path)
                    i['assetdetails_imagepath'] = img_data
                full_data = json.dumps(full_data)
                df_fa = pd.read_json(full_data)
                # print(df_fa)
            else:
                df_fa = df_fa_data

            if self.type == 'INVOICE_DETAILS' and self.sub_type == 'DETAILS':
                df_fa['debit_data'] = df_fa['debit_data'].apply(json.loads)
                return {"DATA": df_fa, "MESSAGE": outmsg_sp[0]}
            elif self.type == 'CLUB_DETAILS' and self.sub_type == 'CHECKER_SUMMARY':
                df_fa['lj_child_data'] = df_fa['lj_child_data'].apply(json.loads)
                return {"DATA": df_fa, "MESSAGE": outmsg_sp[0]}
            # elif self.type == 'MERGE_DETAILS' and self.sub_type == 'CHECKER_SUMMARY' and 'lj_default_details' in df_fa.columns:
            #     df_fa['lj_default_details'] = df_fa['lj_default_details'].apply(json.loads)
            #     print(df_fa)
            #     return {"DATA": df_fa, "MESSAGE": outmsg_sp[0]}
            elif 'lj_default_details' in df_fa.columns:

                df_fa['lj_default_details'] = df_fa['lj_default_details'].apply(json.loads)
                if 'lj_checker_data' in df_fa.columns:
                    df_fa['lj_checker_data'] = df_fa['lj_checker_data'].apply(json.loads)
                    return {"DATA": df_fa, "MESSAGE": outmsg_sp[0]}
                elif self.type == 'SPLIT_DETAILS' and self.sub_type == 'CHECKER_SUMMARY' and 'lj_split_values' in df_fa.columns:
                    df_fa['lj_split_values'] = df_fa['lj_split_values'].apply(json.loads)
                    return {"DATA": df_fa, "MESSAGE": outmsg_sp[0]}
                return {"DATA": df_fa, "MESSAGE": outmsg_sp[0]}
            elif self.type == 'SPLIT_DETAILS' and self.sub_type == 'CHECKER_SUMMARY' and 'lj_split_values' in df_fa.columns:
                df_fa['lj_split_values'] = df_fa['lj_split_values'].apply(json.loads)
                df_fa['lj_default_details'] = df_fa['lj_default_details'].apply(json.loads)
                return {"DATA": df_fa, "MESSAGE": outmsg_sp[0]}
            elif 'lj_child_data' in df_fa.columns:
                df_fa['lj_child_data'] = df_fa['lj_child_data'].apply(json.loads)
                if 'lj_checker_data' in df_fa.columns:
                    df_fa['lj_checker_data'] = df_fa['lj_checker_data'].apply(json.loads)
                    return {"DATA": df_fa, "MESSAGE": outmsg_sp[0]}
                return {"DATA": df_fa, "MESSAGE": outmsg_sp[0]}
            return {"DATA": df_fa, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_FAAssetProcess_Get_4')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def set_fa_make(self):
        cursor = connection.cursor()
        parameters = (self.action,self.type,self.sub_type,self.jsondata,self.jsonData,self.json_file,self.jsonData_sec,self.json_classification,self.employee_gid,'')
        cursor.callproc('sp_FAAssetProcess_Set', parameters)
        cursor.execute('select @_sp_FAAssetProcess_Set_9')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def get_entitybranch(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.filter_json, self.json_classification, '')
        cursor.callproc('sp_EntityDetails_Get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_EntityDetails_Get_4')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_EntityDetails_Get_4')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def get_fa_location(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.filter_json, self.json_classification, '')
        cursor.callproc('sp_FALocation_Get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_FALocation_Get_4')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_FALocation_Get_4')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def set_fa_location(self):
        cursor = connection.cursor()
        parameters = (self.action,self.type,self.sub_type,self.jsondata,self.json_classification,self.employee_gid,'')
        cursor.callproc('sp_FALocation_Set', parameters)
        cursor.execute('select @_sp_FALocation_Set_6')

        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def set_fa_category(self):
        cursor = connection.cursor()
        parameters = ( self.action, self.type, self.sub_type, self.jsondata, self.json_classification, self.employee_gid, '')
        cursor.callproc('sp_FAAssetCategory_Set', parameters)
        cursor.execute('select @_sp_FAAssetCategory_Set_6')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def get_fa_category(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.filter_json, self.json_classification, '')
        cursor.callproc('sp_FA_Category_Get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_FA_Category_Get_4')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_asset_cat = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_asset_cat, "MESSAGE": outmsg_sp[0]}

        else:
            cursor.execute('select @_sp_FA_Category_Get_4')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def set_sales(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.sub_type, self.jsondata, self.json_classification, self.employee_gid, '')
        cursor.callproc('sp_OtherCustomer_Set', parameters)
        cursor.execute('select @_sp_OtherCustomer_Set_6')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def set_fa_depreciation(self):
        cursor = connection.cursor()
        parameters = (self.action,self.type,self.sub_type,self.jsondata,self.jsonData,self.json_classification,self.employee_gid,'')
        cursor.callproc('sp_FADepreciation_Set', parameters)
        cursor.execute('select @_sp_FADepreciation_Set_7')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def get_fa_depreciation(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.filter_json, self.json_classification, '')
        cursor.callproc('sp_FADepreciation_Get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_FADepreciation_Get_4')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}

        else:
            cursor.execute('select @_sp_FADepreciation_Get_4')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}


    def get_fin_year(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.filter_json, self.json_classification, '')
        cursor.callproc('sp_Finace_Get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_Finace_Get_4')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}

        else:
            cursor.execute('select @_sp_Finace_Get_4')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}


    def set_fin_year(self):
        cursor = connection.cursor()
        parameters = (self.action,self.type,self.sub_type,self.jsondata,self.json_classification,self.employee_gid,'')
        cursor.callproc('sp_Finace_Set', parameters)
        cursor.execute('select @_sp_Finace_Set_6')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def get_theme_css(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.filter_json, '')
        cursor.callproc('sp_Gal_trn_ttheme_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_Gal_trn_ttheme_Get_3')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_theme = pd.DataFrame(rows, columns=columns)
        if self.type == 'THEME' and self.sub_type == 'CSS':
            df_theme['theme_content'] = df_theme['theme_content'].apply(json.loads)
            return {"DATA": df_theme, "MESSAGE": outmsg_sp[0]}
        return {"DATA": df_theme, "MESSAGE": outmsg_sp[0]}

    def set_theme_css(self):
        cursor = connection.cursor()
        parameters = (self.action,self.type,self.sub_type,self.jsondata,self.employee_gid,'')
        cursor.callproc('sp_Gal_trn_ttheme_Set', parameters)
        cursor.execute('select @_sp_Gal_trn_ttheme_Set_5')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def get_fa_query(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.filter_json, self.json_classification, '')
        cursor.callproc('sp_FAAssetQuery_Get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_FAAssetQuery_Get_4')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_fa = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_fa, "MESSAGE": outmsg_sp[0]}

        else:
            cursor.execute('select @_sp_FAAssetQuery_Get_4')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def get_fadepreciation(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.filter_json, self.json_classification, '')
        common.logger.error([{"FA_Before_getDep_Sp_called": 'get_fadepreciation_called'}])
        cursor.callproc('sp_FADepreciation_Get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_FADepreciation_Get_4')
            outmsg_sp = cursor.fetchone()
            common.logger.error([{"FA_After_getDep_Sp_called": 'get_fadepreciation_called'}])
            if outmsg_sp[0] == 'FOUND':
                rows = list(rows)
                df_fa = pd.DataFrame(rows, columns=columns)
                return {"MESSAGE":'FOUND',"DATA":df_fa}
            else:
                rows = list(rows)
                df_fa = pd.DataFrame(rows, columns=columns)
                return {"MESSAGE": 'FOUND', "DATA": df_fa}

        else:
            cursor.execute('select @_sp_FADepreciation_Get_4')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def get_sale_generate(self):
        cursor = connection.cursor()
        parameters = (self.type, self.filter_json, self.json_classification, '')
        cursor.callproc('sp_SaleTemplate_Get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_SaleTemplate_Get_3')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_SaleTemplate_Get_3')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

from Bigflow.settings import S3_BUCKET_NAME
def image_path(self,file_name):
    s3_client = boto3.client('s3','ap-south-1')
    response = s3_client.generate_presigned_url('get_object',
                                                Params={'Bucket': S3_BUCKET_NAME, 'Key': file_name},
                                                ExpiresIn=None)
    # print(response)
    content = {
        "File_path": response,
    }
    return content



