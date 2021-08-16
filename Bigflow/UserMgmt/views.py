from django.shortcuts import render
from Bigflow.UserMgmt.Model import muser
from django.http import JsonResponse
from Bigflow.Core import class1
#from Bigflow.menuClass import utility as utl
import json
import datetime
import pandas as pd
from Bigflow.Core.models import decrpt as decry_data
from Bigflow.menuClass import utility as utl


def rolesummaryIndex(request):
    utl.check_authorization(request)
    return render(request, "user_roleSummary.html")


def get_rollgroup(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_rollgroup = muser.user_model()
        empgid = request.session['Emp_gid']
        obj_rollgroup.employee_gid = decry_data(empgid)
        df_rolegroup = obj_rollgroup.get_roleGroup()
        jdata = df_rolegroup.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def get_roleList(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_roleList = muser.user_model()
        obj_roleList.role_code = request.GET['role_code']
        obj_roleList.role_name = request.GET['role_name']
        obj_roleList.rolegroup_gid = request.GET['rGroup_gid']
        gid = decry_data(request.session['Entity_gid'])
        obj_roleList.entity_gid = json.dumps({"Entity_Gid":gid})
        df_rolegroup = obj_roleList.get_roleList()
        jdata = df_rolegroup.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def get_userList(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_userList = muser.user_model()
        obj_userList.role_gid = request.GET['role_gid']
        obj_userList.employee_gid = request.GET['user_gid']
        obj_userList.entity_gid = decry_data(request.session['Entity_gid'])
        obj_userList.type = request.GET['gettype']
        obj_userList.json_data = json.dumps({"Entity_Gid": obj_userList.entity_gid})
        df_rolegroup = obj_userList.get_userList()
        df_rolegroup['STATUS'] = df_rolegroup['STATUS'].astype('bool')
        jdata = df_rolegroup.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def get_menuList(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_menuList = muser.user_model()
        obj_menuList.role_gid = request.GET['role_gid']
        obj_menuList.ismobile=request.GET['ismobile']
        df_menuList = obj_menuList.get_menuList()
        df_menuList['rolemenu_role_gid'] = df_menuList['rolemenu_role_gid'].fillna(0)

        df = pd.DataFrame({'menu_gid':['N','Y'],
                    'menu_name':['Web','Android']}, index = [0,1])
        mainlist = []
    for xy, main in df.iterrows():
        maindis={}
        maindis['menu_gid'] =  main['menu_gid']
        maindis['menu_name'] = main['menu_name']
        maindis['rVSMenu_isAssign'] = bool(1)
        df_parant = df_menuList[(df_menuList['menu_parent_gid'] == 0) & (df_menuList['menu_mobile'] == main['menu_gid'])]
        menulist= []
        for x, menu in df_parant.iterrows():
            menudis = {}
            menudis['menu_gid'] = menu['menu_gid']
            menudis['menu_name'] = menu['menu_name']
            menudis['role_gid'] = menu['rolemenu_role_gid']
            menudis['menu_displayorder'] = menu['menu_displayorder']
            menudis['rVSMenu_isAssign'] = bool(menu['Rights'])
            menudis['ismobile'] = menu['menu_mobile']
            df_child = df_menuList[df_menuList['menu_parent_gid'] == menu['menu_gid']]
            childlist = []
            for y, child in df_child.iterrows():
                childdid = {}
                childdid['menu_gid'] = child['menu_gid']
                childdid['menu_name'] = child['menu_name']
                childdid['role_gid'] = child['rolemenu_role_gid']
                childdid['menu_displayorder'] = child['menu_displayorder']
                childdid['rVSMenu_isAssign'] = bool(child['Rights'])
                childdid['ismobile'] = child['menu_mobile']
                subchildlist = []
                df_subchild = df_menuList[df_menuList['menu_parent_gid'] == child['menu_gid']]
                for z, subchild in df_subchild.iterrows():
                    subdis = {}
                    subdis['menu_gid'] = subchild['menu_gid']
                    subdis['menu_name'] = subchild['menu_name']
                    subdis['role_gid'] = subchild['rolemenu_role_gid']
                    subdis['menu_displayorder'] = subchild['menu_displayorder']
                    subdis['rVSMenu_isAssign'] = bool(subchild['Rights'])
                    subdis['ismobile'] = subchild['menu_mobile']
                    subchildlist.append(subdis)
                childdid['subchild'] = subchildlist
                childlist.append(childdid)
            menudis['menu_children'] = childlist
            menulist.append(menudis)
        # jdata = menulist.to_json(orient='records')
        maindis['main_children'] = menulist
        mainlist.append(maindis)
    return JsonResponse(json.dumps(mainlist), safe=False)


def setRoleDetails(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        result='false'
        obj_roledtl = muser.user_model()
        jsondata = json.loads(request.body.decode('utf-8')).get('parms')
        obj_roledtl.role_gid = jsondata.get('role_gid')
        obj_roledtl.role_code = jsondata.get('role_code')
        obj_roledtl.role_name = jsondata.get('role_name')
        obj_roledtl.rolegroup_gid = jsondata.get('group_gid')
        obj_roledtl.created_by=decry_data(request.session['Emp_gid'])
        obj_roledtl.entity_gid=decry_data(request.session['Entity_gid'])

        user = []
        user = jsondata.get('user_roles')
        menu = []
        menu = jsondata.get('role_menu')

        if(jsondata.get('role_gid')==0):
            temp=obj_roledtl.setroles()[0].split(',')
            if(len(temp)>1):
                obj_roledtl.role_gid=int(temp[0])
            else:
                return JsonResponse(json.dumps(temp[0]),safe=False)

        if(type(obj_roledtl.role_gid) == int):
            menudtl=getmenudtlList(menu)
            # add
            jsondate={'role_gid':obj_roledtl.role_gid}
            jsondate['menu']=list(filter(lambda p:p['rVSMenu_isAssign']==True and p['role_gid'] == 0,menudtl))
            if(len(jsondate['menu'])>0):
                obj_roledtl.menu_gid=0
                obj_roledtl.json_data=json.dumps(jsondate)
                result = outputReturn(obj_roledtl.setrolevsMenu(), 1)
            # remove  unchecked menu details
            for m in filter(lambda p:p['rVSMenu_isAssign']==False and p['role_gid'] != 0  ,menudtl):
                obj_roledtl.menu_gid=m['menu_gid']
                obj_roledtl.json_data='0'
                result =outputReturn( obj_roledtl.setrolevsMenu(),1)

            # user
            # add user
            for u in filter(lambda p:p['STATUS']== True and p['role_gid'] == None,user):
                obj_roledtl.employee_gid=u['employee_gid']
                obj_roledtl.is_removed=''
                result=outputReturn(obj_roledtl.setusersvsMenu(),1)

            # Remove user
            for u in filter(lambda p:p['STATUS']== False and p['role_gid'] != None,user):
                obj_roledtl.employee_gid = u['employee_gid']
                obj_roledtl.role_gid = u['role_gid']
                obj_roledtl.is_removed = 'Y'
                result=outputReturn(obj_roledtl.setusersvsMenu(),1)

            if (result== 'UPDATE_SUCCESS' or result =='SUCCESS'):
                return JsonResponse('true', safe=False)
            else:
                return JsonResponse('false', safe=False)
        else:
            return JsonResponse('false', safe=False)
def getmenudtlList(menu):
    menulist=[]
    for x in menu:
        # obj_menu={}
        # obj_menu['menu_gid'] = x['menu_gid']
        # obj_menu['role_gid'] = x['role_gid']
        # obj_menu['rVSMenu_isAssign'] = x['rVSMenu_isAssign']
        for xy in x['main_children']:
            menulist.append(
                {'menu_gid': xy['menu_gid'], 'role_gid': xy['role_gid'], 'rVSMenu_isAssign': xy['rVSMenu_isAssign']})
            for y in xy['menu_children']:
                menulist.append(
                    {'menu_gid': y['menu_gid'], 'role_gid': y['role_gid'], 'rVSMenu_isAssign': y['rVSMenu_isAssign']})
                for z in y['subchild']:
                    menulist.append(
                        {'menu_gid': z['menu_gid'], 'role_gid': z['role_gid'], 'rVSMenu_isAssign': z['rVSMenu_isAssign']})
    return  menulist
def outputReturn(tubledtl,index):
    temp=tubledtl[0].split(',')
    if(len(temp)>1):
        if (index==0):
            return int(temp[0])
        else:
            return temp[1]
    else:
        return  temp[0]
def userroleIndex(request):
    utl.check_authorization(request)
    return render(request, "user_userRoles.html")


def getEmployeeDtl(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_empList = muser.user_model()
        obj_empList.employee_gid = 0
        obj_empList.employee_name = ''
        obj_empList.cluster_gid = request.GET['clust_gid']
        gid = decry_data(request.session['Entity_gid'])
        obj_empList.jsonData = json.dumps({"entity_gid": [gid], "client_gid": []})
        df_empList = obj_empList.get_employee()
        jdata = df_empList.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)

def getClustGroup(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_empList = muser.user_model()
        obj_empList.entity_gid = decry_data(request.session['Entity_gid'])
        df_empList = obj_empList.get_clustgroupList()
        jdata = df_empList.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)

def setEmployeeRole(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        result='false'
        obj_emproledtl = muser.user_model()
        jsondata = json.loads(request.body.decode('utf-8')).get('parms')
        obj_emproledtl.employee_gid=jsondata.get('user_gid')
        obj_emproledtl.created_by = decry_data(request.session['Emp_gid'])
        obj_emproledtl.entity_gid = decry_data(request.session['Entity_gid'])

        role =jsondata.get('user_role')

        # add user
        for u in filter(lambda p: p['STATUS'] == True and p['employee_gid'] == None, role):
            obj_emproledtl.role_gid = u['role_gid']
            obj_emproledtl.is_removed = ''
            result = outputReturn(obj_emproledtl.setusersvsMenu(), 1)

        # Remove user
        for u in filter(lambda p: p['STATUS'] == False and p['employee_gid'] != None, role):
            obj_emproledtl.role_gid = u['role_gid']
            obj_emproledtl.is_removed = 'Y'
            result = outputReturn(obj_emproledtl.setusersvsMenu(), 1)

        if (result == 'UPDATE_SUCCESS' or result == 'SUCCESS'):
            return JsonResponse('true', safe=False)
        else:
            return JsonResponse('false', safe=False)

# password

def changepwdIndex(request):
    utl.check_authorization(request)
    return render(request, "user_changePassword.html")

def Employee_detail(request):
    utl.check_pointaccess(request)
    obj_change_pwd = muser.user_model()
    obj_change_pwd.employee_gid = request.session['Emp_gid']
    obj_change_pwd.employee_name = ''
    obj_change_pwd.cluster_gid = '0'
    obj_change_pwd.jsonData = json.dumps({"entity_gid": [request.session['Entity_gid']], "client_gid": []})
    df_changepwd_view = obj_change_pwd.get_employee()
    jdata = df_changepwd_view.to_json(orient='records')
    return JsonResponse(json.loads(jdata), safe=False)

def Password_verifiy(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        cust_code = jsondata.get('params').get('emp_code')
        old_pwd = jsondata.get('params').get('old_pswd')
        oldpswd_verify = class1.get_login(cust_code,old_pwd)
        if (oldpswd_verify[1][0] == 'SUCCESS'):
            obj_pwd_set = muser.user_model()
            obj_pwd_set.employee_gid = request.session['Emp_gid']
            new_password = jsondata.get('params').get('new_pswd')
            obj_pwd_set.new_password=class1.converttoascii(new_password)
            dtpassword = obj_pwd_set.get_password()
            dt_pawword = pd.DataFrame(dtpassword)
            for index, row in dt_pawword.iterrows():
              password1 = str(row['employee_pwd1'])
              password2 = str(row['employee_pwd2'])
              password3 = str(row['employee_pwd3'])
            if password1 == obj_pwd_set.new_password:
                jdata = 'password dont not match previews 3 password'
                return JsonResponse(json.dumps(jdata), safe=False)
            elif password2 == obj_pwd_set.new_password:
                jdata = 'password dont not match previews 3 password'
                return JsonResponse(json.dumps(jdata), safe=False)
            elif password3 == obj_pwd_set.new_password:
                jdata = 'password dont not match previews 3 password'
                return JsonResponse(json.dumps(jdata), safe=False)
            else:
                df_changepwd_view = obj_pwd_set.set_password()
            return JsonResponse(json.dumps(df_changepwd_view), safe=False)
        elif(oldpswd_verify[1][0] == 'FAIL'):
            jdata='Wrong old password'
            return JsonResponse(json.dumps(jdata), safe=False)

def resetpwdIndex(request):
    utl.check_authorization(request)
    return render(request, "user_resetPassword.html")

def All_Employeedetail(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_change_pwd = muser.user_model()
        obj_change_pwd.employee_gid = 0
        obj_change_pwd.employee_name = ''
        obj_change_pwd.cluster_gid = '0'
        obj_change_pwd.jsonData = json.dumps({"entity_gid": [decry_data(request.session['Entity_gid'])], "client_gid": []})
        df_changepwd_view = obj_change_pwd.get_employee()
        jdata = df_changepwd_view.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)

def Set_Password(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_pwd_set = muser.user_model()
        obj_pwd_set.employee_gid = jsondata.get('params').get('emp_gid')
        new_password = jsondata.get('params').get('pswd')
        obj_pwd_set.new_password = class1.converttoascii(new_password)
        df_changepwd_view = obj_pwd_set.set_password()
        return JsonResponse(json.dumps(df_changepwd_view), safe=False)

def get_password(request):
        utl.check_pointaccess(request)
        if request.method == 'GET':
            obj_change_pwd = muser.user_model()
            obj_change_pwd.employee_gid = request.session['Emp_gid']
            obj_change_pwd.employee_name=''
            df_changepwd_view = obj_change_pwd.get_password()
            jdata = df_changepwd_view.to_json(orient='records')
            return JsonResponse(json.loads(jdata), safe=False)


def menu_set(request):
    if request.method == 'POST':
        utl.check_pointaccess(request)
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_pwd_set = muser.user_model()
        obj_pwd_set.employee_gid = jsondata.get('params').get('emp_gid')
        new_password = jsondata.get('params').get('pswd')
        obj_pwd_set.new_password = class1.converttoascii(new_password)
        df_changepwd_view = obj_pwd_set.set_password()
        return JsonResponse(json.dumps(df_changepwd_view), safe=False)
