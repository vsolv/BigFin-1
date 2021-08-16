from rest_framework.response import Response
from rest_framework.utils import json
from Bigflow.eClaim.model import meClaim
import Bigflow.Core.jwt_file as jwt
import Bigflow.Core.models as common

ip = common.localip()

# from datetime import datetime
# import pytz
# IST = pytz.timezone('Asia/Kolkata')
# datetime_ist = datetime.now(IST)
# today = datetime_ist.strftime('%Y-%m-%d')

import requests


class travel_exp():
    def grade_eligible(self, g):
        travel_class = [{"mode": "AIR", "Class": [{"type": "Econamy"}, {"type": "Business"}, {"type": "FirstClass"}]},
                        {"mode": "Train",
                         "Class": [{"type": "AC II Tier"}, {"type": "AC III Tier"}, {"type": "II AC Sleeper"}]},
                        {"mode": "Road", "Class": [{"type": "Econamy"}, {"type": "Business"}, {"type": "FirstClass"}]}]
        grade = ["BDA", "C1", "L1", "L2", "L3", "L4", "L5", "L6", "L7", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "ME",
                 "RE"]
        if g in grade[9:12]:
            mode_class = travel_class[1].get('Class')[2]
            data = {
                "type": mode_class
            }
            print("OFFICER")
            return data

        elif g in grade[11:]:
            mode_class = travel_class[0].get('Class')[1]
            data = {
                "type": mode_class
            }
            print("EXCUTIVES")
            return data
        else:
            mode_class = travel_class[1].get('Class')[1]
            data = {
                "type": mode_class
            }
            print("WORK MEN")
            return data

    def check_eligbility(self, priorpermission, claimedamount, fare_amount):
        if claimedamount > fare_amount:
            if priorpermission == "1":
                amount = claimedamount
                logic = "True"
                return amount
            else:
                amount = fare_amount
                logic = "True"
                return amount
        elif claimedamount <= fare_amount:
            amount = claimedamount
            logic = "True"
            return amount

    def check_ticket(self, tktbybank, amount):
        if tktbybank == 1:
            fare_amount = 0
            return fare_amount
        else:
            fare_amount = amount
            return fare_amount

    def ticket_fare(self, jsondata, classs):
        depatureplace = jsondata.get('Params').get('FILTER').get('depatureplace')
        placeofvisit = jsondata.get('Params').get('FILTER').get('placeofvisit')
        fare_amount = trainfare(self, depatureplace, placeofvisit, classs)
        return fare_amount

    def calck_totalamt(self, valid_data, outer_data):
        tot = 0
        for i in valid_data:
            i['eligibleamount'] = i.get('claimedamount')
            i['approvedamount'] = i.get('claimedamount')
            tot = tot + float(i.get('claimedamount'))
            i['eligibletravel'] = i.get('actualtravel')
        outer_data['approvedamount'] = tot
        return "True"


import datetime
from datetime import date, timedelta


class dailydiem():
    def submit_data(self, data, outer_data):
        for i in data:
            if float(i.get('eligibleamount')) > float(i.get('claimedamount')):
                i['approvedamount'] = i.get('claimedamount')
            elif float(i.get('eligibleamount')) < float(i.get('claimedamount')):
                i['approvedamount'] = i.get('eligibleamount')
            elif float(i.get('eligibleamount')) == float(i.get('claimedamount')):
                i['approvedamount'] = i.get('eligibleamount')
        totalamt = 0
        for j in data:
            totalamt = totalamt + float(j.get('approvedamount'))
        outer_data['approvedamount'] = totalamt

        return "True"

    def eligible_amount(self, jsondata, grade, empid):
        expensegid = jsondata.get('Params').get('FILTER').get('expensegid')
        city = jsondata.get('Params').get('FILTER').get('visitcity')
        boardingbybank = int(jsondata.get('Params').get('FILTER').get('boardingbybank'))
        accbybank = int(jsondata.get('Params').get('FILTER').get('accbybank'))
        declaration = int(jsondata.get('Params').get('FILTER').get('declaration'))
        isleave = int(jsondata.get('Params').get('FILTER').get('isleave'))
        if city != "":
            out_data = elig_citytoamount(self, grade, city, expensegid)
            amount = out_data[0].get('amount')
        else:
            amount = 0
        if boardingbybank != "" and accbybank != "" and declaration != "":
            if int(accbybank) == 1 and int(boardingbybank) == 0 and int(declaration) == 0:
                amount = (amount / 100) * 75

            elif int(accbybank) == 0 and int(boardingbybank) == 1 and int(declaration) == 0:
                amount = (amount / 100) * 50

            elif int(accbybank) == 1 and int(boardingbybank) == 1 and int(declaration) == 0:
                amount = (amount / 100) * 25

            elif int(accbybank) == 1 and int(boardingbybank) == 0 and int(declaration) == 1:
                amount = (amount / 100) * 100

        from_date = jsondata.get('Params').get('FILTER').get('from_date')
        to_date = jsondata.get('Params').get('FILTER').get('to_date')
        datetimeFormat = '%Y-%m-%d %H:%M'
        diff = datetime.datetime.strptime(to_date, datetimeFormat) - datetime.datetime.strptime(from_date,
                                                                                                datetimeFormat)
        eligible_amount = 0
        day = str(diff).split()
        days = diff.days
        sec = diff.total_seconds()
        min = sec / 60
        hours = min // 60
        if days == 0:
            hour = day[0].split(':')
            hour = int(hour[0])
        else:
            hour = day[2].split(':')
            hour = int(hour[0])

        if hour > 0:
            days = int(days) + 1

        if isleave == "" and isleave == None:
            isleave = 0

        Entity_Gid = int(jsondata.get('Params').get('FILTER').get('Entity_Gid'))
        holiday = 0
        if city != "":
            obj_claim = meClaim.eClaim_Model()
            state_get = {
                "City": city.upper(),
                "Entity_Gid": Entity_Gid
            }
            obj_claim.filter_json = json.dumps(state_get)
            ld_out_message = obj_claim.eClaim_citytostate_get()
            out_data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
            state_gid = out_data[0].get('state_gid')
            holiday = holiday_check(self, state_gid, from_date, to_date)
            if holiday != 0:
                state_get = {
                    "Emp_Grade": grade.upper(),
                    "Entity_Gid": Entity_Gid
                }
                obj_claim.filter_json = json.dumps(state_get)
                ld_out_message = obj_claim.eClaim_holydaydeim_get()
                out_data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                if out_data != []:
                    for i in out_data:
                        if i.get('city') == city.upper():
                            days = days - (int(holiday) + int(isleave))
                            eligible_amount = (days * amount) + int(i.get('amount')) + (int(isleave) * 0)
                else:
                    eligible_amount = (days * amount) + (int(isleave) * 0)
            else:
                days = days - (int(holiday) + int(isleave))
                eligible_amount = (days * amount) + (holiday * amount * 1.25) + (int(isleave) * 0)

        inspection_amount = 0
        if 'tourgid' in jsondata.get('Params').get('FILTER'):
            tourgid = int(jsondata.get('Params').get('FILTER').get('tourgid'))
            obj_claim = meClaim.eClaim_Model()
            obj_claim.filter_json = json.dumps(
                {"Employee_gid": empid, "Entity_Gid": Entity_Gid, "Tour_Gid": tourgid})
            out_data = obj_claim.eClaim_tourdetails_get()
            if out_data.get("MESSAGE") == 'FOUND':
                data = json.loads(out_data.get("DATA").to_json(orient='records'))
                for d in data:
                    tourreason = d.get('name')
                    # tourreason = 'INSPECTION'
            if tourreason.upper() == 'INSPECTION':
                inspection_amount = days * 100

        eligible_amount = eligible_amount + inspection_amount
        eligible_value = {
            "Eligible_amount": eligible_amount,
            "sys_hours": hours

        }
        ld_dict = {"DATA": eligible_value,
                   "MESSAGE": 'FOUND'}
        print(eligible_amount)
        return ld_dict


class lodging():
    def date_valid(self, jsondata, grade):
        city = jsondata.get('Params').get('FILTER').get('city')
        expensegid = jsondata.get('Params').get('FILTER').get('expensegid')
        out_data = elig_citytoamount(self, grade, city, expensegid)
        if out_data != []:
            amount = out_data[0].get('amount')
            frdt = jsondata.get('Params').get('FILTER').get('checkindate')
            todt = jsondata.get('Params').get('FILTER').get('checkoutdate')
            datetimeFormat = '%Y-%m-%d %H:%M'
            diff = datetime.datetime.strptime(todt, datetimeFormat) - datetime.datetime.strptime(frdt, datetimeFormat)
            day = str(diff).split()
            days = diff.days
            if days == 0:
                hour = day[0].split(':')
                hour = int(hour[0])
            else:
                hour = day[2].split(':')
                hour = int(hour[0])
            noofdays = days
            if hour > 1:
                days = int(days) + 1
                amount = days * amount
            else:
                amount = days * amount

        eligible_value = {
            "Eligible_amount": amount,
            "noofdays": noofdays

        }
        return eligible_value

    def calc_accbybank(self, jsondata, eligamount):
        accbybank = int(jsondata.get('Params').get('FILTER').get('accbybank'))
        if accbybank == 0:
            eligamount = eligamount
            eligible_value = {
                "Eligible_amount": eligamount,
            }
            return eligible_value
        else:
            eligamount = 0
            eligible_value = {
                "Eligible_amount": eligamount,
            }
            return eligible_value

    def calc_gst(self, data):
        if data.get('bankgstno') != 0 and data.get('vendorgstno') != 0:
            bnk_gst = data.get('bankgstno')[0:2]
            lodge_gst = data.get('vendorgstno')[0:2]
            if bnk_gst == lodge_gst:
                print("CGST SCGST")
                cgst = int(data.get('cgst'))
                sgst = int(data.get('sgst'))
                tax_amt = int(data.get('eligibleamount')) + (int(data.get('eligibleamount')) * int(sgst)) / 100
                return int(tax_amt)
            else:
                print("IGST")
                igst = int(data.get('igst'))
                tax_amt = int(data.get('eligibleamount')) + (int(data.get('eligibleamount')) * int(igst)) / 100
                return int(tax_amt)
        else:
            return int(0)

    def calck_totalamt(self, valid_data, outer_data):
        # tot = 0
        # for i in valid_data:
        #     app_amount = lodging.calc_gst(self,i)
        #     i['approvedamount'] = app_amount
        #     tot = tot + float(app_amount)
        # outer_data['approvedamount'] = tot
        tot = 0
        for i in valid_data:
            if float(i.get('eligibleamount')) > float(i.get('claimedamount')):
                i['approvedamount'] = i.get('claimedamount')
                tot = tot + float(i.get('claimedamount'))
            elif float(i.get('eligibleamount')) < float(i.get('claimedamount')):
                i['approvedamount'] = i.get('eligibleamount')
                tot = tot + float(i.get('eligibleamount'))
            elif float(i.get('eligibleamount')) == float(i.get('claimedamount')):
                i['approvedamount'] = i.get('eligibleamount')
                tot = tot + float(i.get('eligibleamount'))
        outer_data['approvedamount'] = tot

        return "True"


import math


class incidental():
    def validation(self, jsondata):
        code = jsondata.get('Params').get('FILTER').get('code').upper()
        samedayreturn = int(jsondata.get('Params').get('FILTER').get('samedayreturn'))
        travelhours = jsondata.get('Params').get('FILTER').get('travelhours')
        singlefare = jsondata.get('Params').get('FILTER').get('singlefare')
        if code == "OWN":
            amount = 0
            return amount
        elif code == "TRAIN":
            if samedayreturn == 1:
                amount = 10
                return amount

            elif samedayreturn == 0:
                tothour = int(travelhours)
                day = math.ceil(tothour / 24)
                if day == 1:
                    totamount = 15
                else:
                    amount = 20
                    totamount = amount * day
                return totamount

        elif code == "ROAD":
            singlefare = float(singlefare)
            amount = math.ceil(singlefare * (1 / 3))
            if amount <= 10:
                amount = 10
            return amount

    def calck_totalamt(self, valid_data, outer_data):
        tot = 0
        for i in valid_data:
            i['eligibleamount'] = i.get('expenses')
            i['approvedamount'] = i.get('expenses')
            i['claimedamount'] = i.get('expenses')
            tot = tot + float(i.get('expenses'))
        outer_data['approvedamount'] = tot
        outer_data['claimedamount'] = tot
        return "True"


class pkg_moving():
    def validate_data(self, jsondata, grade):
        obj_claim = meClaim.eClaim_Model()
        totaldisttrans = jsondata.get('Params').get('FILTER').get('totaldisttrans')
        tonnagehhgood = jsondata.get('Params').get('FILTER').get('tonnagehhgood')
        distinhilly = jsondata.get('Params').get('FILTER').get('distinhilly')
        twowheelertrans = jsondata.get('Params').get('FILTER').get('twowheelertrans')

        datas = {
            "Grade": grade.upper()
        }
        obj_claim.filter_json = json.dumps(datas)
        ld_eligible = obj_claim.eClaim_gradetoelig_get()
        ld_elig = json.loads(ld_eligible.get("DATA").to_json(orient='records'))
        if int(totaldisttrans) in range(0, 1000):
            rupeeforton = ld_elig[0].get('freight1000')
        else:
            rupeeforton = ld_elig[0].get('freight1001')
        if int(tonnagehhgood) <= ld_elig[0].get('maxtonnage'):
            tonnage = int(tonnagehhgood)
        else:
            tonnage = int(ld_elig[0].get('maxtonnage'))

        if ld_elig[0].get('twowheeler') == 1:
            twowheeler = [0, 1]
        else:
            twowheeler = [0]

        tot_amt = 0
        if int(twowheelertrans) in twowheeler:
            if int(distinhilly) != 0:
                tot_amt = tot_amt + int(distinhilly) * tonnage * rupeeforton * ld_elig[0].get('hillyregion')

            if int(totaldisttrans) - int(distinhilly) != 0:
                tot_amt = tot_amt + (int(totaldisttrans) - int(distinhilly)) * tonnage * rupeeforton

            formatted_float = "{:.2f}".format(tot_amt)
            return formatted_float
        else:
            logic = "false"
            ld_dict = {"MESSAGE": "Not Eligible In Two wheeler"}
            return logic, ld_dict

    def calck_driverbata(self, jsondata, grades):
        traveltimeinhours = jsondata.get('Params').get('FILTER').get('traveltimeinhours')
        expensegid = jsondata.get('Params').get('FILTER').get('expensegid')
        common.logger.error([{"Grade": str(grades.upper())}])
        g = grades.upper()
        tothour = int(traveltimeinhours)
        day = math.ceil(tothour / 24)
        obj_claim = meClaim.eClaim_Model()
        obj_claim.filter_json = json.dumps({"Grade": grades})
        designation = obj_claim.eClaim_empwise_grade_get()
        designation = json.loads(designation.get("DATA").to_json(orient='records'))
        designation = designation[0].get('designation')
        common.logger.error([{"designation": str(designation)}])
        out_data = elig_citytoamount(self, designation, "driverbata", expensegid)
        common.logger.error([{"out_data": str(out_data)}])
        if out_data != []:
            if day == 1:
                data = {
                    "driverbatta": out_data[0].get('amount'),
                    "daysdrivereng": day
                }
                common.logger.error([{"data": str(data)}])
                return data
            else:
                data = {
                    "driverbatta": out_data[0].get('amount') + out_data[0].get('amount'),
                    "daysdrivereng": day
                }
                common.logger.error([{"data": str(data)}])
                return data
        else:
            return 0

    def calc_breakage(self, jsondata, grades):
        g = grades.upper()
        receipt = int(jsondata.get('Params').get('FILTER').get('receiptlosses'))
        expensegid = int(jsondata.get('Params').get('FILTER').get('expensegid'))
        obj_claim = meClaim.eClaim_Model()
        obj_claim.filter_json = json.dumps({"Grade": grades})
        designation = obj_claim.eClaim_empwise_grade_get()
        designation = json.loads(designation.get("DATA").to_json(orient='records'))
        designation = designation[0].get('designation')
        common.logger.error([{"designation2": str(designation)}])
        out_data = elig_citytoamount(self, designation, "Lumpsum", expensegid)
        common.logger.error([{"out_data2": str(out_data)}])
        if out_data != []:
            for data in out_data:
                if receipt == int(data.get('applicableto')):
                    common.logger.error([{"amount": str(data.get('amount'))}])
                    return data.get('amount')

        else:
            return 0

    def calck_totalamt(self, valid_data, outer_data):
        tot = 0
        for i in valid_data:
            if float(i.get('eligibleamount')) > float(i.get('claimedamount')):
                i['approvedamount'] = i.get('claimedamount')
                tot = tot + float(i.get('claimedamount'))
            elif float(i.get('eligibleamount')) < float(i.get('claimedamount')):
                i['approvedamount'] = i.get('eligibleamount')
                tot = tot + float(i.get('eligibleamount'))
            elif float(i.get('eligibleamount')) == float(i.get('claimedamount')):
                i['approvedamount'] = i.get('eligibleamount')
                tot = tot + float(i.get('eligibleamount'))
        outer_data['approvedamount'] = tot
        return "True"


class localcon():
    def validate_data(self, jsondata, grad):
        obj_claim = meClaim.eClaim_Model()
        obj_claim.filter_json = json.dumps({"Grade": grad})
        designation = obj_claim.eClaim_empwise_grade_get()
        designation = json.loads(designation.get("DATA").to_json(orient='records'))
        designation = designation[0].get('designation')
        city = jsondata.get('Params').get('FILTER').get('center')
        expensegid = jsondata.get('Params').get('FILTER').get('expensegid')
        out_data = elig_citytoamount(self, designation, city, expensegid)
        amount = out_data[0].get('amount')
        eligible_value = {
            "Eligible_amount": amount,
        }
        return eligible_value

    def calck_totalamt(self, valid_data, outer_data):
        tot = 0
        for i in valid_data:
            if float(i.get('eligibleamount')) > float(i.get('claimedamount')):
                i['approvedamount'] = i.get('claimedamount')
                tot = tot + float(i.get('claimedamount'))
            elif float(i.get('eligibleamount')) < float(i.get('claimedamount')):
                i['approvedamount'] = i.get('eligibleamount')
                tot = tot + float(i.get('eligibleamount'))
            elif float(i.get('eligibleamount')) == float(i.get('claimedamount')):
                i['approvedamount'] = i.get('eligibleamount')
                tot = tot + float(i.get('eligibleamount'))
        outer_data['approvedamount'] = tot
        return "True"


class miscellaneous():
    def elegibility_data(self, data, grade):
        obj_claim = meClaim.eClaim_Model()
        obj_claim.filter_json = json.dumps({"Grade": grade})
        designation = obj_claim.eClaim_empwise_grade_get()
        designation = json.loads(designation.get("DATA").to_json(orient='records'))
        designation = designation[0].get('designation')
        if 'center' in data.get('Params').get('FILTER') and data.get('Params').get('FILTER').get('center') != None:
            city = data.get('Params').get('FILTER').get('center')
            expensegid = data.get('Params').get('FILTER').get('expensegid')
            out_data = elig_citytoamount(self, designation, city, expensegid)
            amount = out_data[0].get('amount')
            return amount
        else:
            return data.get('Params').get('FILTER').get('claimedamount')

    def validate_data(self, data, outer_data):
        tot = 0
        for i in data:
            if float(i.get('eligibleamount')) > float(i.get('claimedamount')):
                i['approvedamount'] = i.get('claimedamount')
                tot = tot + float(i.get('claimedamount'))
            elif float(i.get('eligibleamount')) < float(i.get('claimedamount')):
                i['approvedamount'] = i.get('eligibleamount')
                tot = tot + float(i.get('eligibleamount'))
            elif float(i.get('eligibleamount')) == float(i.get('claimedamount')):
                i['approvedamount'] = i.get('eligibleamount')
                tot = tot + float(i.get('eligibleamount'))
        outer_data['approvedamount'] = tot
        return "True"


def elig_citytoamount(self, grade, city, expensegid):
    obj_claim = meClaim.eClaim_Model()
    amount_get = {
        "salarygrade": grade.upper(),
        "city": city,
        "expensegid": expensegid
    }
    obj_claim.filter_json = json.dumps(amount_get)
    ld_out_message = obj_claim.eClaim_citytoallowance_get()
    out_data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
    return out_data


def tourtoemployee(self, tourgid):
    obj_claim = meClaim.eClaim_Model()
    obj_claim.employee_gid = tourgid
    ld_out_emp = obj_claim.eClaim_tourtoemp_get()
    ld_dict = json.loads(ld_out_emp.get("DATA").to_json(orient='records'))
    return ld_dict


def holiday_check(self, state_gid, frdt, todt):
    obj_claim = meClaim.eClaim_Model()
    sdate = frdt.split()
    edate = todt.split()

    sdate = sdate[0].split('-')
    edate = edate[0].split('-')

    sdate = date(int(sdate[0]), int(sdate[1]), int(sdate[2]))  # start date
    edate = date(int(edate[0]), int(edate[1]), int(edate[2]))  # end date

    delta = edate - sdate  # as timedelta
    totholiday = 0
    for i in range(delta.days + 1):
        day = sdate + timedelta(days=i)
        get_holiday = {
            "Stategid": state_gid,
            "Entity_Gid": 1,
            "Date": str(day)
        }
        obj_claim.filter_json = json.dumps(get_holiday)
        ld_out_holiday = obj_claim.eClaim_statetoholiday_get()
        holiday = json.loads(ld_out_holiday.get("DATA").to_json(orient='records'))
        totholiday = totholiday + int(holiday[0].get('Data'))

    return totholiday


def trainfare(self, source, destination, classs):
    train_data = [{"source": "CHENNAI", "destination": "TRICHY", "class": "AC II Tier", "fare": "1000"},
                  {"source": "CHENNAI", "destination": "TRICHY", "class": "AC III Tier", "fare": "800"},
                  {"source": "CHENNAI", "destination": "TRICHY", "class": "II AC Sleeper", "fare": "1200"},
                  {"source": "CHENNAI", "destination": "MADURAI", "class": "AC II Tier", "fare": "1200"},
                  {"source": "CHENNAI", "destination": "MADURAI", "class": "AC III Tier", "fare": "1000"},
                  {"source": "CHENNAI", "destination": "MADURAI", "class": "II AC Sleeper", "fare": "1500"},
                  {"source": "CHENNAI", "destination": "COIMBATORE", "class": "AC II Tier", "fare": "1200"},
                  {"source": "CHENNAI", "destination": "COIMBATORE", "class": "AC III Tier", "fare": "1500"},
                  {"source": "CHENNAI", "destination": "COIMBATORE", "class": "II AC Sleeper", "fare": "1800"},
                  {"source": "TRICHY", "destination": "MADURAI", "class": "AC II Tier", "fare": "800"},
                  {"source": "TRICHY", "destination": "MADURAI", "class": "AC III Tier", "fare": "1000"},
                  {"source": "TRICHY", "destination": "MADURAI", "class": "II AC Sleeper", "fare": "1200"},
                  {"source": "MADURAI", "destination": "COIMBATORE", "class": "AC II Tier", "fare": "1000"},
                  {"source": "MADURAI", "destination": "COIMBATORE", "class": "AC III Tier", "fare": "1200"},
                  {"source": "MADURAI", "destination": "COIMBATORE", "class": "II AC Sleeper", "fare": "1500"},
                  {"source": "CHENNAI", "destination": "KARUR", "class": "AC II Tier", "fare": "1200"},
                  {"source": "CHENNAI", "destination": "KARUR", "class": "AC III Tier", "fare": "1500"},
                  {"source": "CHENNAI", "destination": "KARUR", "class": "II AC Sleeper", "fare": "1800"},
                  {"source": "KARUR", "destination": "CHENNAI", "class": "AC II Tier", "fare": "1200"},
                  {"source": "KARUR", "destination": "CHENNAI", "class": "AC III Tier", "fare": "1500"},
                  {"source": "KARUR", "destination": "CHENNAI", "class": "II AC Sleeper", "fare": "1800"}]

    data = {
        "source": source.upper(),
        "destination": destination.upper(),
        "classs": classs
    }
    for i in train_data:
        if data.get('source') == i.get('source'):
            if data.get('destination') == i.get('destination'):
                if data.get('classs') == i.get('class'):
                    print(i.get('fare'))
                    return i.get('fare')
    else:
        return 2000


def ccbs(self, data, entity, token):
    for i in data:
        bs_data = {
            "Table_name": "ap_mst_tbs",
            "Column_1": "tbs_gid as bs_gid,tbs_code as bs_code,tbs_no as bs_no,tbs_name as bs_name",
            "Column_2": "",
            "Where_Common": "tbs",
            "Where_Primary": "gid",
            "Primary_Value": i.get('bsgid'),
            "Order_by": "no"
        }
        bs = json.loads(alltable(self, bs_data, entity, token))
        if bs.get('MESSAGE') == 'FOUND':
            cc_data = {
                "Table_name": "ap_mst_tcc",
                "Column_1": "tcc_gid as cc_gid,tcc_code as cc_code,tcc_no as cc_no,tcc_name as cc_name",
                "Column_2": "",
                "Where_Common": "tcc",
                "Where_Primary": "gid",
                "Primary_Value": i.get('ccgid'),
                "Order_by": "no"
            }
            cc = json.loads(alltable(self, cc_data, entity, token))
            if cc.get('MESSAGE') == 'FOUND':
                i['ccname'] = cc.get('DATA')[0].get('cc_name')
            i['bsname'] = bs.get('DATA')[0].get('bs_name')
    return data


def alltable(self, table_data, entity, token):
    drop_tables = {"data": table_data}
    action = 'Debit'
    params = {'Action': action, 'Entity_Gid': encrypt1(entity)}
    token = token
    headers = {"content-type": "application/json", "Authorization": "" + token + ""}
    datas = json.dumps(drop_tables.get('data'))
    resp = requests.post("" + ip + "/All_Tables_Values_Get", params=params, data=datas, headers=headers,
                         verify=False)
    response_data = resp.content.decode("utf-8")
    return response_data


import sys


class ecf_entry():
    def invoice_header(self, request, jsondata):
        obj_claim = meClaim.eClaim_Model()
        # jsondata = json.loads(request.body.decode('utf-8'))
        tourgid = jsondata.get('Params').get('DETAILS').get('tourgid')
        entity_gid = jsondata.get('Params').get('DETAILS').get('Entity_Gid')
        out_data = 0
        if jsondata.get('Params').get('DETAILS').get('apptype') == "TOURADV":
            obj_claim.filter_json = json.dumps({"Tour_gid": tourgid})
            out_data = obj_claim.eClaim_touradvance_get()
            out_data = json.loads(out_data.get("DATA").to_json(orient='records'))
            out_data = json.loads(out_data[0].get('advance'))

        elif jsondata.get('Params').get('DETAILS').get('apptype') == "CLAIM":
            obj_claim.filter_json = json.dumps({"Claimrequest_Tourgid": tourgid, "Entity_Gid": entity_gid})
            out_data = obj_claim.eClaim_claimedexpense_get()
            out_data = json.loads(out_data.get("DATA").to_json(orient='records'))

        obj_claim.employee_gid = tourgid
        ld_out_emp = obj_claim.eClaim_tourtoemp_get()
        ld_dict = json.loads(ld_out_emp.get("DATA").to_json(orient='records'))
        emp_gid = ld_dict[0].get('empgid')
        tour_no = ld_dict[0].get('requestno')

        # requestdate = ld_dict[0].get('requestdate')
        # req_date = date.fromordinal(requestdate)
        # print(req_date.isoformat())
        # requestdate = str(str(req_date.year) +'-'+str(req_date.month)+'-'+str(req_date.day))
        tot = 0
        advancegid = 0
        sno = ''
        if jsondata.get('Params').get('DETAILS').get('apptype') == "TOURADV":
            for ot in out_data:
                if ot.get('status') == 0:
                    tot = ot.get('appamount')
                    advancegid = ot.get('gid')
            sno = "_" + str(len(out_data))
            reason = out_data[0].get('appcomment')
        elif jsondata.get('Params').get('DETAILS').get('apptype') == "CLAIM":
            total_amount = 0
            for ot in out_data:
                details_exp = get_expensedetails(self, ot, entity_gid)
                for d in details_exp:
                    amount = d.get('appamt')
                    total_amount = int(d.get('appamt'))
                    branchgstno = ''
                    suppliergstno = ''
                    IGST = 0
                    CGST = 0
                    SGST = 0
                    HSN_Code = '1'
                    # if ot.get('description') == 'Travelling Expenses' or ot.get('description') == 'Lodging' or ot.get(
                    #         'description') == 'Packaging/Freight':
                    #     branchgstno = d.get('bankgstno')
                    #     suppliergstno = d.get('vendorgstno')
                    #     IGST = d.get('igst')
                    #     CGST = d.get('cgst')
                    #     SGST = d.get('sgst')
                    #     if branchgstno != '' and suppliergstno != '' and branchgstno != 'NA' and suppliergstno != 'NA':
                    #         if branchgstno[0:2] == suppliergstno[0:2]:
                    #             percent = int(CGST) + int(SGST)
                    #             amt = int(d.get('appamt')) * percent/100
                    #             IGST = 0
                    #             CGST = "{:.2f}".format(amt / 2)
                    #             SGST = "{:.2f}".format(amt / 2)
                    #             # total_amount = "{:.2f}".format(int(amount) + amt)
                    #         else:
                    #             amt = int(d.get('appamt')) * int(IGST)/100
                    #             IGST = "{:.2f}".format(amt)
                    #             CGST = 0
                    #             SGST = 0
                    #             # total_amount = "{:.2f}".format(int(amount) + amt)
                    tot = float(tot) + float(total_amount)
            reason = out_data[0].get('requestorcomment')

        emp_data = {
            "empids": emp_gid
        }
        obj_claim.filter_json = json.dumps(emp_data)
        obj_claim.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
        emp_out_message = obj_claim.eClaim_employee_get()
        employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
        branch_gid = employee_data[0].get('branch_gid')
        employee_gender = employee_data[0].get('employee_gender')
        params = {"action": "INSERT",
                  "type": "INVOICE_HEADER",
                  "entity_gid": jsondata.get('Params').get('DETAILS').get('Entity_Gid'),
                  "employee_gid": emp_gid}
        tk = str(request.auth.token)
        token = "Bearer  " + tk[2:len(tk) - 1]
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        obj_claim.date = 'DATE'
        date = obj_claim.get_server_date()
        requestdate = date
        comodity_table = {
            "Table_name": "ap_mst_tcommodity",
            "Column_1": "commodity_gid,commodity_code,commodity_name",
            "Column_2": "",
            "Where_Common": "commodity",
            "Where_Primary": "name",
            "Primary_Value": "Tour ClaimStaff",
            "Order_by": "gid"
        }
        comodity = json.loads(alltable(self, comodity_table, entity_gid, token))
        if comodity.get("MESSAGE") == 'FOUND':
            comoditygid = comodity.get("DATA")[0].get('commodity_gid')
        else:
            comoditygid = 1
        if jsondata.get('Params').get('DETAILS').get('apptype') == "TOURADV":
            tmp_data = {
                "IsTa": "Y",
                "Invoice_Type": "ADVANCE",
                "Supplier_gid": 0,
                "Sup_state_gid": 1,
                "Inwarddetails_gid": 1,
                "Is_GST": "N",
                "Invoice_Date": requestdate,
                "Invoice_No": "TOUR" + str(tour_no) + str(sno),
                "Invoice_Tot_Amount": tot,
                "invoicetaxamount": tot,
                "Supplier_GST_No": "",
                "Header_Status": "NEW",
                "Reprocessed": "",
                "Remark": reason,
                "Employee_gid": emp_gid,
                "GROUP": "INWARD",
                "branch_gid": branch_gid,
                "Advance_incr": "E",
                "Commodity_gid": comoditygid
            }
        elif jsondata.get('Params').get('DETAILS').get('apptype') == "CLAIM":
            tmp_data = {
                "IsTa": "Y",
                "Invoice_Type": "TCF",
                "Supplier_gid": 0,
                "Sup_state_gid": 1,
                "Inwarddetails_gid": 1,
                "Is_GST": "N",
                "Invoice_Date": requestdate,
                "Invoice_No": "TOUR" + str(tour_no) + "Exp",
                "Invoice_Tot_Amount": tot,
                "invoicetaxamount": tot,
                "Supplier_GST_No": "",
                "Header_Status": "NEW",
                "Reprocessed": "",
                "Remark": reason,
                "Employee_gid": emp_gid,
                "GROUP": "INWARD",
                "branch_gid": branch_gid,
                "Advance_incr": "E",
                "Commodity_gid": comoditygid
            }
        header = []
        header.append(tmp_data)
        tmp = {
            "params": {
                "header_json": {"HEADER": header},
                "detail_json": {},
                "invoice_json": {},
                "debit_json": {},
                "credit_json": {},
                "status_json": {}
            }
        }
        datas = json.dumps(tmp)
        common.logger.error([{"invoice_header_json": str(datas)}])
        resp = requests.post("" + ip + "/ECFInvoice", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        response = json.loads(response)
        common.logger.error([{"invoiceheader_set": str(response)}])
        response['advancegid'] = advancegid
        return response

    def invoice_detail(self, request, response, jsondata):
        try:
            obj_claim = meClaim.eClaim_Model()
            # jsondata = json.loads(request.body.decode('utf-8'))
            tourgid = jsondata.get('Params').get('DETAILS').get('tourgid')
            entity_gid = jsondata.get('Params').get('DETAILS').get('Entity_Gid')

            out_data = 0
            if jsondata.get('Params').get('DETAILS').get('apptype') == "TOURADV":
                obj_claim.filter_json = json.dumps({"Tour_gid": tourgid})
                out_data = obj_claim.eClaim_touradvance_get()
                out_data = json.loads(out_data.get("DATA").to_json(orient='records'))
                out_data = json.loads(out_data[0].get('advance'))

            elif jsondata.get('Params').get('DETAILS').get('apptype') == "CLAIM":
                obj_claim.filter_json = json.dumps({"Claimrequest_Tourgid": tourgid, "Entity_Gid": entity_gid})
                out_data = obj_claim.eClaim_claimedexpense_get()
                out_data = json.loads(out_data.get("DATA").to_json(orient='records'))

            obj_claim.employee_gid = tourgid
            ld_out_emp = obj_claim.eClaim_tourtoemp_get()
            ld_dict = json.loads(ld_out_emp.get("DATA").to_json(orient='records'))
            emp_gid = ld_dict[0].get('empgid')
            tour_no = ld_dict[0].get('requestno')
            empgrade = ld_dict[0].get('empgrade')
            # requestdate = ld_dict[0].get('requestdate')
            # req_date = datetime.fromtimestamp(requestdate // 1000)
            # requestdate = str(str(req_date.year) + '-' + str(req_date.month) + '-' + str(req_date.day))
            branchgid = ld_dict[0].get('empbranchgid')
            obj_claim.date = 'DATE'
            date = obj_claim.get_server_date()
            requestdate = date
            tot = 0
            reason = 0
            advancecat_gid = 0
            advance_subcat_gid = 0
            advance_subcat_gl = 0
            if jsondata.get('Params').get('DETAILS').get('apptype') == "CLAIM":
                emp_data = {
                    "empids": emp_gid
                }
                obj_claim.filter_json = json.dumps(emp_data)
                obj_claim.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                emp_out_message = obj_claim.eClaim_employee_get()
                employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                employee_gender = employee_data[0].get('employee_gender')
                obj_claim.filter_json = json.dumps({"Tour_Gid": tourgid, "Entity_Gid": entity_gid})
                tourreason = obj_claim.eClaim_tourreasondata_get()
                tourreason = json.loads(tourreason.get("DATA").to_json(orient='records'))
                tour_reason = tourreason[0].get('reason')
                if "General" in str(tour_reason):
                    reason = tour_reason.split('-')
                    tour_reason = reason[1]
                obj_claim.filter_json = json.dumps({"Grade": empgrade})
                designation = obj_claim.eClaim_empwise_grade_get()
                designation = json.loads(designation.get("DATA").to_json(orient='records'))
                designation = designation[0].get('designation')
                if designation == "EXECUTIVE" or designation == "OFFICER":
                    designation = designation + 'S'
                gl_description = "TRAVEL EXPENSES-- " + designation
                if employee_gender == 'M':
                    gender_data = 'Male'
                elif employee_gender == 'F':
                    gender_data = 'Female'
                obj_claim.filter_json = json.dumps(
                    {"Gl_Desc": gl_description, "Tour_Reason": tour_reason, "Gender": gender_data,
                     "Entity_Gid": entity_gid})
                gl_mapping = obj_claim.eClaim_glmapping_get()
                gl_mapping = json.loads(gl_mapping.get("DATA").to_json(orient='records'))
                common.logger.error([{"glmapping": str(gl_mapping)}])
                cat_code = gl_mapping[0].get('categorycode')
                cat_gid = cat_apicall(self, request, cat_code, entity_gid)
                subcat_data = subcat_apicall(self, request, cat_gid, entity_gid)
                common.logger.error([{"cat_data": str(cat_gid)}])
                common.logger.error([{"subcat_data": str(subcat_data)}])
            elif jsondata.get('Params').get('DETAILS').get('apptype') == "TOURADV":
                obj_claim.filter_json = json.dumps(
                    {"Gl_Desc": "ADVANCE", "Tour_Reason": "ADVANCE", "Gender": "Other",
                     "Entity_Gid": entity_gid})
                gl_mapping = obj_claim.eClaim_glmapping_get()
                gl_mapping = json.loads(gl_mapping.get("DATA").to_json(orient='records'))
                common.logger.error([{"glmapping": str(gl_mapping)}])
                cat_code = gl_mapping[0].get('categorycode')
                advancecat_gid = cat_apicall(self, request, cat_code, entity_gid)
                subcat_data = subcat_apicall(self, request, advancecat_gid, entity_gid)
                common.logger.error([{"cat_data": str(advancecat_gid)}])
                common.logger.error([{"subcat_data": str(subcat_data)}])
                for d in subcat_data:
                    if d.get('subcategory_name') == "Employee":
                        advance_subcat_gid = d.get('subcategory_gid')
                        advance_subcat_gl = d.get('subcategory_glno')

            adv_gid = 0
            if jsondata.get('Params').get('DETAILS').get('apptype') == "TOURADV":
                for ot in out_data:
                    if ot.get('status') == 0:
                        adv_gid = ot.get('gid')
                        tot = ot.get('appamount')
                sno = "_" + str(len(out_data))
                # reason = out_data[0].get('appcomment')
            elif jsondata.get('Params').get('DETAILS').get('apptype') == "CLAIM":
                for d in out_data:
                    tot = tot + d.get('approvedamount')
                reason = out_data[0].get('requestorcomment')

            obj_claim.action = "GET"
            obj_claim.type = "EMPLOYEE_DETAILS"
            filter = {"employee_gid": emp_gid}
            obj_claim.filter = json.dumps(filter)
            obj_claim.classification = json.dumps({"Entity_Gid": int(entity_gid)})
            emp_bnk = obj_claim.get_APbankdetails()
            bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
            common.logger.error([{"bankdata": str(bank_data)}])
            header_gid = response.get('Header_Gid')
            detail = 0
            debit = 0
            claim_details = []
            claim_debit = []
            adv_debit = []
            if len(bank_data) != 0:
                obj_claim.filter_json = json.dumps({"Tour_Gid": tourgid, "CCBS_Type": 1})
                ccbs_data = obj_claim.eClaim_ccbs_get()
                if ccbs_data.get("MESSAGE") == 'FOUND':
                    ccbs_detail = json.loads(ccbs_data.get("DATA").to_json(orient='records'))
                    for ccbsdtl in ccbs_detail:
                        if adv_gid == ccbsdtl.get('claimreqgid'):
                            data = {
                                "Invoice_Header_Gid": header_gid,
                                "Invoice_Details_Gid": "0",
                                "Category_Gid": advancecat_gid,
                                "Sub_Category_Gid": advance_subcat_gid,
                                # "Category_Gid": 122,
                                # "Sub_Category_Gid": 776,
                                "GL_No": advance_subcat_gl,
                                "Debit_Amount": ccbsdtl.get('amount'),
                                # "Debit_Amount": tot,
                                "Debit_Gid": "0",
                                "Invoice_Sno": 1,
                                "cc_id": ccbsdtl.get('ccgid'),
                                "bs_id": ccbsdtl.get('bsgid'),
                                "Debit_percentage": ccbsdtl.get('percentage')}
                            adv_debit.append(data)
                # empcc = bank_data[0].get('ccgid')
                # empcc = 141
                # empbs = bank_data[0].get('bsgid')
                # empbs = 49
                else:
                    data = {
                        "Invoice_Header_Gid": header_gid,
                        "Invoice_Details_Gid": "0",
                        "Category_Gid": advancecat_gid,
                        "Sub_Category_Gid": advance_subcat_gid,
                        # "Category_Gid": 122,
                        # "Sub_Category_Gid": 776,
                        "GL_No": advance_subcat_gl,
                        "Debit_Amount": tot,
                        "Debit_Gid": "0",
                        "Invoice_Sno": 1,
                        "cc_id": 141,
                        "bs_id": 49,
                        "Debit_percentage": 100}
                    adv_debit.append(data)

                empBank = bank_data[0].get('bankdetails_gid')
                accno = bank_data[0].get('bankdetails_acno')
            else:
                return Response({"MESSAGE": "Employee Bank Data Missing"})

            if jsondata.get('Params').get('DETAILS').get('apptype') == "TOURADV":
                detail = {
                    "DETAIL": [{
                        "Item_Name": "ADVANCE",
                        "Description": "ADVANCE",
                        "HSN_Code": "1",
                        "Unit_Price": tot,
                        "Quantity": "1",
                        "Amount": tot,
                        "Discount": 0,
                        "IGST": 0,
                        "CGST": 0,
                        "SGST": 0,
                        "Total_Amount": tot,
                        "PO_Header_Gid": "0",
                        "PO_Detail_Gid": 0,
                        "GRN_Header_Gid": 0,
                        "GRN_Detail_Gid": 0,
                        "Invoice_Header_gid": header_gid,
                        "Invoice_Sno": 1,
                        "Invoice_Other_Amount": 0
                    }
                    ]}
                debit = {"DEBIT": adv_debit}
                common.logger.error([{"ad_detail": str(detail)}])
                common.logger.error([{"ad_debit": str(debit)}])
            elif jsondata.get('Params').get('DETAILS').get('apptype') == "CLAIM":
                sno = 1
                tmp = 0
                for ot in out_data:
                    details_exp = get_expensedetails(self, ot, entity_gid)
                    for d in details_exp:
                        if tmp == sno:
                            sno = sno + 1
                        amount = d.get('appamt')
                        total_amount = int(d.get('appamt'))
                        vendor_name = ''
                        vendor_code = ''
                        branchgstno = ''
                        suppliergstno = ''
                        IGST = 0
                        CGST = 0
                        SGST = 0
                        HSN_Code = '1'
                        gst = False
                        gst_igst = False
                        if ot.get('description') == 'Travelling Expenses' or ot.get(
                                'description') == 'Lodging' or ot.get('description') == 'Packaging/Freight':
                            vendor_code = d.get('vendorcode')
                            vendor_name = d.get('vendorname')
                            branchgstno = d.get('bankgstno')
                            suppliergstno = d.get('vendorgstno')
                            IGST = d.get('igst')
                            CGST = d.get('cgst')
                            SGST = d.get('sgst')
                            HSN_Code = d.get('hsncode')
                            if branchgstno != '' and suppliergstno != '' and branchgstno != 'NA' and suppliergstno != 'NA':
                                gst = True
                                if branchgstno[0:2] == suppliergstno[0:2]:
                                    percent = int(CGST) + int(SGST)
                                    amt = int(d.get('appamt')) * percent / 100
                                    IGST = 0
                                    CGST = "{:.2f}".format(amt / 2)
                                    SGST = "{:.2f}".format(amt / 2)
                                    # total_amount = "{:.2f}".format(int(amount) + amt)
                                else:
                                    gst_igst = True
                                    amt = int(d.get('appamt')) * int(IGST) / 100
                                    IGST = "{:.2f}".format(amt)
                                    CGST = 0
                                    SGST = 0
                                    # total_amount = "{:.2f}".format(int(amount) + amt)
                        dt = {
                            "Item_Name": ot.get('description'),
                            "Description": ot.get('description'),
                            "HSN_Code": HSN_Code,
                            "Unit_Price": d.get('appamt'),
                            "Quantity": "1",
                            # "Amount": amount,
                            "Amount": total_amount,
                            "Discount": 0,
                            "IGST": 0,
                            "CGST": 0,
                            "SGST": 0,
                            "Total_Amount": total_amount,
                            "PO_Header_Gid": "0",
                            "PO_Detail_Gid": 0,
                            "GRN_Header_Gid": 0,
                            "GRN_Detail_Gid": 0,
                            "Invoice_Header_gid": header_gid,
                            "Invoice_Sno": sno,
                            "Invoice_Other_Amount": 0,
                            "_branchgstno": branchgstno,
                            "_invoiceno": "TOUR" + str(tour_no),
                            "_suppliercode": vendor_code,
                            "_suppliername": vendor_name,
                            "_suppliergstno": suppliergstno,
                            "_branchgid": branchgid,
                            "_invoicedate": requestdate
                        }
                        common.logger.error([{"claim_detail": str(dt)}])
                        claim_details.append(dt)
                        common.logger.error([{"get_subcat": str(subcat_data) + str(ot.get('description'))}])
                        subcatogry = get_subcat(self, subcat_data, ot.get('description'))
                        common.logger.error([{"subcatogry": str(subcatogry)}])
                        # if gst:
                        #     # gst_catcode = "4"+str(suppliergstno[0:2])
                        #     gst_catcode = "483"
                        #     gst_cat_gid = cat_apicall(self, request, gst_catcode, entity_gid)
                        #     get_subcat_data = subcat_apicall(self, request, gst_cat_gid, entity_gid)
                        #     for tax in get_subcat_data:
                        #         if tax.get('subcategory_code')=="I-ITC":
                        #             igst_gl = tax.get('subcategory_glno')
                        #             igst_gid = tax.get('subcategory_gid')
                        #         elif tax.get('subcategory_code')=="C-ITC":
                        #             cgst_gl = tax.get('subcategory_glno')
                        #             cgst_gid = tax.get('subcategory_gid')
                        #         elif tax.get('subcategory_code')=="S-ITC":
                        #             sgst_gl = tax.get('subcategory_glno')
                        #             sgst_gid = tax.get('subcategory_gid')
                        #     if gst_igst:
                        #         debit = {
                        #             "Invoice_Header_Gid": header_gid,
                        #             "Invoice_Details_Gid": "0",
                        #             "Category_Gid": gst_cat_gid,
                        #             "Sub_Category_Gid": igst_gid,
                        #             "GL_No": igst_gl,
                        #             "Debit_Amount": IGST,
                        #             "Debit_Gid": "0",
                        #             "Invoice_Sno": sno,
                        #             "cc_id": empcc,
                        #             "bs_id": empbs,
                        #             "Debit_percentage": 100}
                        #         claim_debit.append(debit)
                        #     else:
                        #         i=0
                        #         while i<2:
                        #             if i==0:
                        #                 csgst_gl = cgst_gl
                        #                 csgst_gid = cgst_gid
                        #             elif i==1:
                        #                 csgst_gl = sgst_gl
                        #                 csgst_gid = sgst_gid
                        #             debit = {
                        #                 "Invoice_Header_Gid": header_gid,
                        #                 "Invoice_Details_Gid": "0",
                        #                 "Category_Gid": cat_gid,
                        #                 "Sub_Category_Gid": csgst_gid,
                        #                 "GL_No": csgst_gl,
                        #                 "Debit_Amount": CGST,
                        #                 "Debit_Gid": "0",
                        #                 "Invoice_Sno": sno,
                        #                 "cc_id": empcc,
                        #                 "bs_id": empbs,
                        #                 "Debit_percentage": 100}
                        #             claim_debit.append(debit)
                        #             i= i+1
                        #     debit = {
                        #         "Invoice_Header_Gid": header_gid,
                        #         "Invoice_Details_Gid": "0",
                        #         "Category_Gid": cat_gid,
                        #         "Sub_Category_Gid": subcatogry.get('subcat_gid'),
                        #         "GL_No": subcatogry.get('gl_no'),
                        #         "Debit_Amount": d.get('appamt'),
                        #         "Debit_Gid": "0",
                        #         "Invoice_Sno": sno,
                        #         "cc_id": empcc,
                        #         "bs_id": empbs,
                        #         "Debit_percentage": 100}
                        #     claim_debit.append(debit)
                        #
                        # else:
                        obj_claim.filter_json = json.dumps({"Tour_Gid": tourgid, "CCBS_Type": 2})
                        ccbs_data = obj_claim.eClaim_ccbs_get()
                        if ccbs_data.get("MESSAGE") == 'FOUND':
                            ccbs_detail = json.loads(ccbs_data.get("DATA").to_json(orient='records'))
                            for ccbsdtl in ccbs_detail:
                                debit = {
                                    "Invoice_Header_Gid": header_gid,
                                    "Invoice_Details_Gid": "0",
                                    "Category_Gid": cat_gid,
                                    "Sub_Category_Gid": subcatogry.get('subcat_gid'),
                                    "GL_No": subcatogry.get('gl_no'),
                                    "Debit_Amount": d.get('appamt'),
                                    # "Debit_Amount": ccbsdtl.get('amount'),
                                    "Debit_Gid": "0",
                                    "Invoice_Sno": sno,
                                    "cc_id": ccbsdtl.get('ccgid'),
                                    "bs_id": ccbsdtl.get('bsgid'),
                                    "Debit_percentage": ccbsdtl.get('percentage')
                                }
                                claim_debit.append(debit)
                        # elif ccbs_data.get("MESSAGE") == 'NOT_FOUND':
                        #     debit = {
                        #         "Invoice_Header_Gid": header_gid,
                        #         "Invoice_Details_Gid": "0",
                        #         "Category_Gid": cat_gid,
                        #         "Sub_Category_Gid": subcatogry.get('subcat_gid'),
                        #         "GL_No": subcatogry.get('gl_no'),
                        #         # "Debit_Amount": d.get('appamt'),
                        #         "Debit_Amount": total_amount,
                        #         "Debit_Gid": "0",
                        #         "Invoice_Sno": sno,
                        #         "cc_id": empcc,
                        #         "bs_id": empbs,
                        #         "Debit_percentage": 100}
                        #     claim_debit.append(debit)

                        tmp = int(sno)
                    sno = int(sno) + 1

                detail = {
                    "DETAIL": claim_details
                }
                debit = {
                    "DEBIT": claim_debit
                }
            sum_amount = 0
            for dtl in detail.get('DETAIL'):
                sum_amount = float(dtl.get('Total_Amount')) + sum_amount
            claim_credit = []
            paymodedata = paymode_apicall(self, request, entity_gid)
            for pay in paymodedata:
                if pay.get('Paymode_name') == "ERA":
                    era_gid = pay.get('paymode_gid')
                elif pay.get('Paymode_name') == "PPX":
                    ppx_gid = pay.get('paymode_gid')
            if jsondata.get('Params').get('DETAILS').get('apptype') == "TOURADV":
                credit = {"CREDIT":
                    [{
                        "Invoice_Header_Gid": header_gid,
                        "Paymode_Gid": era_gid,
                        "Paymode_name": "ERA",
                        "GL_No": accno,
                        "Bank_Gid": empBank,
                        "Ref_No": accno,
                        "Tax_Gid": "",
                        "Tax_Type": "",
                        "Tax_Rate": "",
                        "TDS_Exempt": "N",
                        "Credit_Amount": sum_amount,
                        "Credit_Gid": "0",
                        "taxable_amt": 0,
                        "ppx_headergid": 0,
                        "Is_due": "false",
                        "supplier_gid": ""
                    }]
                }
                common.logger.error([{"ad_credit": str(credit)}])
            elif jsondata.get('Params').get('DETAILS').get('apptype') == "CLAIM":
                # Advance Liqudation so that this code Commented
                obj_claim.filter_json = json.dumps({"Tour_gid": tourgid})
                out_advdata = obj_claim.eClaim_touradvance_get()
                out_adv = json.loads(out_advdata.get("DATA").to_json(orient='records'))
                totadv_amt = 0
                if out_adv[0].get('advance') != None:
                    advance = json.loads(out_adv[0].get('advance'))
                    for adv in advance:
                        if adv.get('adjustamount') != None:
                            totadv_amt = float(totadv_amt) + float(adv.get('adjustamount'))

                credit_amt = float(sum_amount) - float(totadv_amt)
                if credit_amt == 0:
                    credit_amt = 0
                elif credit_amt < 0:
                    credit_amt = 0
                elif credit_amt > 0:
                    credit_amt = credit_amt
                else:
                    credit_amt = credit_amt

                credit = {
                    "Invoice_Header_Gid": header_gid,
                    "Paymode_Gid": era_gid,
                    "Paymode_name": "ERA",
                    "GL_No": accno,
                    "Bank_Gid": empBank,
                    "Ref_No": accno,
                    "Tax_Gid": "",
                    "Tax_Type": "",
                    "Tax_Rate": "",
                    "TDS_Exempt": "N",
                    "Credit_Amount": credit_amt,
                    "Credit_Gid": "0",
                    "taxable_amt": 0,
                    "ppx_headergid": 0,
                    "Is_due": "false",
                    "supplier_gid": ""
                }
                claim_credit.append(credit)
                if out_adv[0].get('advance') != None:
                    advance = json.loads(out_adv[0].get('advance'))
                    obj_claim.filter_json = json.dumps(
                        {"Gl_Desc": "ADVANCE", "Tour_Reason": "ADVANCE", "Gender": "Other",
                         "Entity_Gid": entity_gid})
                    gl_mapping = obj_claim.eClaim_glmapping_get()
                    gl_mapping = json.loads(gl_mapping.get("DATA").to_json(orient='records'))
                    common.logger.error([{"glmapping": str(gl_mapping)}])
                    cat_code = gl_mapping[0].get('categorycode')
                    advancecat_gid = cat_apicall(self, request, cat_code, entity_gid)
                    subcat_data = subcat_apicall(self, request, advancecat_gid, entity_gid)
                    common.logger.error([{"cat_data": str(advancecat_gid)}])
                    common.logger.error([{"subcat_data": str(subcat_data)}])
                    for d in subcat_data:
                        if d.get('subcategory_name') == "Employee":
                            advance_subcat_gid = d.get('subcategory_gid')
                            advance_subcat_gl = d.get('subcategory_glno')
                    for adv in advance:
                        if adv.get('adjustamount') != None:
                            credit = {
                                "Invoice_Header_Gid": header_gid,
                                "Paymode_Gid": ppx_gid,
                                "Paymode_name": "PPX",
                                "GL_No": advance_subcat_gl,
                                "Bank_Gid": 0,
                                "Ref_No": adv.get('adjustamount'),
                                "Tax_Gid": "",
                                "Tax_Type": "",
                                "Tax_Rate": "",
                                "TDS_Exempt": "N",
                                "trnbranch": "",
                                "paybranch": "",
                                "Credit_Amount": adv.get('adjustamount'),
                                "Credit_Gid": "0",
                                "taxable_amt": 0,
                                "ppx_headergid": adv.get('ppx_headergid'),
                                "Is_due": "false",
                                "supplier_gid": 0,
                                "Credit_catgid": 0,
                                "Credit_subcatgid": 0
                            }
                            claim_credit.append(credit)

                credit = {
                    "CREDIT": claim_credit
                }
            common.logger.error([{"claim_credit": str(credit)}])

            obj_claim.filter_json = json.dumps({"Tour_gid": tourgid})
            ld_out_file = obj_claim.eClaim_file_get()

            file = json.loads(ld_out_file.get("DATA").to_json(orient='records'))
            filedata = []
            if file != []:
                for i in file:
                    data = {
                        "file_key": i.get('file_path'),
                        "file_path": i.get('file_name'),
                    }
                    filedata.append(data)

            status = {
                "Invoice_Header_Gid": header_gid,
                "Status": "APPROVED",
                "Emp_id": jsondata.get('Params').get('DETAILS').get('processedby'),
                "Individual_approval": "Y",
                "file_data": filedata
            }
            params = {"action": "INSERT",
                      "type": "INVOICE_DETAILS",
                      "entity_gid": jsondata.get('Params').get('DETAILS').get('Entity_Gid'),
                      "employee_gid": jsondata.get('Params').get('DETAILS').get('processedby')}
            tmp_dtl = {
                "params": {
                    "header_json": {},
                    "detail_json": detail,
                    "invoice_json": {},
                    "debit_json": debit,
                    "credit_json": credit,
                    "status_json": status
                }
            }
            common.logger.error([{"tot_claim": str(tmp_dtl)}])
            tk = str(request.auth.token)
            token = "Bearer  " + tk[2:len(tk) - 1]
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}

            data_dtl = json.dumps(tmp_dtl)
            common.logger.error([{"invoice_dtl_json": str(data_dtl)}])
            resp = requests.post("" + ip + "/ECFInvoice", params=params, data=data_dtl, headers=headers,
                                 verify=False)
            response_data = resp.content.decode("utf-8")
            common.logger.error([{"invoice_dtl_set1": str(response_data)}])
            response_data = json.loads(response_data)
            common.logger.error([{"invoice_dtl_set": str(response_data)}])
            return response_data
        except Exception as e:
            er = "Erro Line no :" + str(format(sys.exc_info()[-1].tb_lineno)) + " " + "Error :" + str(e)
            return er


class ecf_reverse_entry():
    def jv_entry(self, request, jsondata):
        obj_claim = meClaim.eClaim_Model()
        employee_gid = request.auth.payload.get('user_id')
        obj_claim.employee_gid = employee_gid
        emp_bnk = obj_claim.eClaim_entity_get()
        data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
        entity = 0
        if len(data) != 0:
            entity = data[0].get('entity_gid')

        emp_data = {
            "empids": employee_gid
        }
        obj_claim.filter_json = json.dumps(emp_data)
        obj_claim.json_classification = json.dumps({})
        emp_out_message = obj_claim.eClaim_employee_get()
        employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
        branch_gid = employee_data[0].get('branch_gid')
        obj_claim.date = 'DATE'
        date = obj_claim.get_server_date()
        requestdate = date
        crnno = jsondata.get('Params').get('DETAILS').get('invoiceheader_crno')
        obj_claim.filter_json = json.dumps({"crnno":crnno,"entity_gid":entity,"entry_type":"213"})
        jv_validation = obj_claim.eClaim_jv_crn_get()
        if jv_validation.get('MESSAGE') == "FOUND":
            jv = json.loads(jv_validation.get("DATA").to_json(orient='records'))
            data = jv[0]
            if jv[0].get('jventry_status') == 'MAKER':
                return {"MESSAGE": "Already JV Submitted", "STATUS": 1}
        balance = jsondata.get('Params').get('DETAILS').get('ppxheader_balance')
        # ppxheader_crno = jsondata.get('Params').get('DETAILS').get('ppxheader_crno')
        amount = jsondata.get('Params').get('DETAILS').get('ppxheader_balance')
        obj_claim.filter_json = json.dumps({"Invoice_crnno": crnno,"Balanceamt":balance})
        jvdata = obj_claim.eClaim_jvdata_get()
        detail = []
        if jvdata.get('debit') != []:
            for i in jvdata.get('debit'):
                detail.append(json.loads(i.get('debit')))
        else:
            return {"MESSAGE": "No Debit Data", "STATUS": 1}

        if jvdata.get('credit') != []:
            for i in jvdata.get('credit'):
                detail.append(json.loads(i.get('credit')))
        else:
            return {"MESSAGE": "No Credit Data", "STATUS": 1}

        params = {"action": "INSERT", "type": "JV_CREATION", "create_by": 1}
        tmp = {
            "action": "INSERT",
            "type": "JV_CREATION",
            "filter": {
                "entry_type": 213,
                "transaction_date": requestdate,
                "ref_no": crnno,
                "description": "yes",
                "jv_status": "MAKER",
                "branch_gid": branch_gid,
                "amount": amount,
                "detail": detail
            },
            "classification": {
                "entity_gid": entity,
                "entity_detailsgid": 1
            }
        }
        datas = json.dumps(tmp)
        tk = str(request.auth.token)
        token = "Bearer  " + tk[2:len(tk) - 1]
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/JV_Process_Set_API", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        response = json.loads(response)
        return response

    def ecf_status_update(self, request, jsondata, entity, emp_gid):
        obj_claim = meClaim.eClaim_Model()
        obj_claim.filter_json = json.dumps({"Tour_gid": jsondata.get('Params').get('DETAILS').get('tourgid')})
        out_data = obj_claim.eClaim_touradvance_get()
        out_data = json.loads(out_data.get("DATA").to_json(orient='records'))
        out_data = json.loads(out_data[0].get('advance'))
        l = len(out_data) - 1
        if out_data[l].get('status') == 1:
            ecf_no = out_data[l].get('crnno')
            invoice_headergid = out_data[l].get('invoiceheadergid')
        else:
            return True
        tk = str(request.auth.token)
        token = "Bearer  " + tk[2:len(tk) - 1]
        data = {
            "params": {
                "filter": {
                    "Page_Index": 0,
                    "Page_Size": 10,
                    "ecf_number": ecf_no
                }
            }
        }
        params = {'action': "GET", "type": "ECF_HEADER_BY_BRANCH", "entity_gid": entity}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(data)
        resp = requests.post("" + ip + "/ECF_STATUS_GET", params=params, data=datas, headers=headers,
                             verify=False)
        statusdata = json.loads(resp.content.decode("utf-8"))

        if statusdata[0].get('ecf_status') == "APPROVED":
            if statusdata[0].get('ap_status') == None:
                data = {
                    "params": {
                        "header_json": {},
                        "detail_json": {},
                        "invoice_json": {},
                        "debit_json": {},
                        "credit_json": {},
                        "status_json": {
                            "Invoice_Header_Gid": invoice_headergid,
                            "Status": "REJECTED",
                            "Remark": "Done"
                        }
                    }
                }
                params = {'action': "UPDATE", "type": "STATUS", "entity_gid": entity, "employee_gid": emp_gid}
                headers = {"content-type": "application/json", "Authorization": "" + token + ""}
                datas = json.dumps(data)
                resp = requests.post("" + ip + "/ECF_STATUS_SET", params=params, data=datas, headers=headers,
                                     verify=False)
                response = json.loads(resp.content.decode("utf-8"))
                if response.get('MESSAGE') == "SUCCESS":
                    return True
                else:
                    return response
        elif statusdata[0].get('ecf_status') == "APProcess":
            if statusdata[0].get('ap_status') == "NEW" or statusdata[0].get('ap_status') == 'CHECKER' \
                    or statusdata[0].get('ap_status') == 'MAKER':
                data = {
                    "params": {
                        "header_json": {},
                        "detail_json": {},
                        "invoice_json": {},
                        "debit_json": {},
                        "credit_json": {},
                        "status_json": {
                            "Invoice_Header_Gid": statusdata[0].get('apinvoiceheader_gid'),
                            "Status": "REJECT",
                            "Remark": "Done",
                            "file_data": [],
                            "Ref_no": ecf_no
                        }
                    }
                }
                params = {'action': "UPDATE", "type": "STATUS", "entity_gid": entity, "employee_gid": emp_gid}
                headers = {"content-type": "application/json", "Authorization": "" + token + ""}
                datas = json.dumps(data)
                resp = requests.post("" + ip + "/AP_STATUS_SET", params=params, data=datas, headers=headers,
                                     verify=False)
                response = json.loads(resp.content.decode("utf-8"))

                if response.get('MESSAGE') == "SUCCESS":
                    return True
                else:
                    return response
            else:
                return {"MESSAGE":"AP Status Update Issue"}


def get_subcat(self, subcatdata, cat):
    if cat == 'Packaging/Freight':
        cat = "Packaging and Moving"
    else:
        cat = cat
    for sub in subcatdata:
        if sub.get('subcategory_name').upper() in cat.upper():
            return {"subcat_gid": sub.get('subcategory_gid'), "gl_no": sub.get('subcategory_glno')}


def cat_apicall(self, request, cat_code, entity_gid):
    tk = str(request.auth.token)
    token = "Bearer  " + tk[2:len(tk) - 1]
    drop_cat = {
        "Table_name": "ap_mst_tcategory",
        "Column_1": "category_gid,category_code,category_no,category_name",
        "Column_2": "",
        "Where_Common": "category",
        "Where_Primary": "no",
        "Primary_Value": cat_code,
        "Order_by": "gid"
    }
    drop_tables = {"data": drop_cat}
    action = 'Debit'
    params = {'Action': action, 'Entity_Gid': encrypt1(entity_gid)}
    headers = {"content-type": "application/json", "Authorization": "" + token + ""}
    datas = json.dumps(drop_tables.get('data'))
    resp = requests.post("" + ip + "/All_Tables_Values_Get", params=params, data=datas, headers=headers,
                         verify=False)
    cat_data = json.loads(resp.content.decode("utf-8"))
    cat_gid = cat_data.get('DATA')[0].get('category_gid')
    return cat_gid


def paymode_apicall(self, request, entity_gid):
    tk = str(request.auth.token)
    token = "Bearer  " + tk[2:len(tk) - 1]
    drop_cat = {
        "Table_name": "gal_mst_tpaymode",
        "Column_1": "paymode_gid,paymode_code,Paymode_name",
        "Column_2": "",
        "Where_Common": "paymode",
        "Where_Primary": "paymode_gid",
        "Primary_Value": "",
        "Order_by": "code"
    }
    drop_tables = {"data": drop_cat}
    action = 'Debit'
    params = {'Action': action, 'Entity_Gid': encrypt1(entity_gid)}
    headers = {"content-type": "application/json", "Authorization": "" + token + ""}
    datas = json.dumps(drop_tables.get('data'))
    resp = requests.post("" + ip + "/All_Tables_Values_Get", params=params, data=datas, headers=headers,
                         verify=False)
    paymode_data = json.loads(resp.content.decode("utf-8"))
    paymode_data = paymode_data.get('DATA')
    return paymode_data


def subcat_apicall(self, request, cat_gid, entity_gid):
    tk = str(request.auth.token)
    token = "Bearer  " + tk[2:len(tk) - 1]
    drop_subcat = {
        "Table_name": "ap_mst_tsubcategory",
        "Column_1": "subcategory_gid,subcategory_glno,subcategory_code,subcategory_no,subcategory_name",
        "Column_2": "",
        "Where_Common": "subcategory",
        "Where_Primary": "categorygid",
        "Primary_Value": cat_gid,
        "Order_by": "gid"
    }
    drop_tables = {"data": drop_subcat}
    action = 'Debit'
    params = {'Action': action, 'Entity_Gid': encrypt1(entity_gid)}
    headers = {"content-type": "application/json", "Authorization": "" + token + ""}
    datas = json.dumps(drop_tables.get('data'))
    resp = requests.post("" + ip + "/All_Tables_Values_Get", params=params, data=datas, headers=headers,
                         verify=False)
    subcat_data = json.loads(resp.content.decode("utf-8"))
    subcat_data = subcat_data.get('DATA')
    return subcat_data


class hsnget():
    def hsndata(self, data):
        obj_claim = meClaim.eClaim_Model()
        for i in data:
            if int(i.get('hsngid')) != 0:
                obj_claim.employee_gid = int(i.get('hsngid'))
                out_data = obj_claim.eClaim_hsncode()
                out_data = json.loads(out_data.get("DATA").to_json(orient='records'))
                i['searchhsn'] = out_data[0].get('hsn_code')
        return data


def get_expensedetails(self, dt, entity_gid):
    subcat = dt.get('description')
    filter = {
        "Claimreqgid": dt.get('claimreq_gid'),
        "Entity_Gid": entity_gid
    }
    obj_eclaim = meClaim.eClaim_Model()
    if subcat == 'Travelling Expenses':
        obj_eclaim.filter_json = json.dumps(filter)
        ld_out_message = obj_eclaim.eClaim_travelexp_get()
        if ld_out_message.get("MESSAGE") == 'FOUND':
            dict = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
            return dict
    elif subcat == 'Daily Diem':
        obj_eclaim.filter_json = json.dumps(filter)
        ld_out_message = obj_eclaim.eClaim_dailydiem_get()
        if ld_out_message.get("MESSAGE") == 'FOUND':
            dict = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
            return dict
    elif subcat == 'Incidental Expenses':
        obj_eclaim.filter_json = json.dumps(filter)
        ld_out_message = obj_eclaim.eClaim_incidental_get()
        if ld_out_message.get("MESSAGE") == 'FOUND':
            dict = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
            return dict
    elif subcat == 'Local Conveyance':
        obj_eclaim.filter_json = json.dumps(filter)
        ld_out_message = obj_eclaim.eClaim_loccon_get()
        if ld_out_message.get("MESSAGE") == 'FOUND':
            dict = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
            return dict
    elif subcat == 'Lodging':
        obj_eclaim.filter_json = json.dumps(filter)
        ld_out_message = obj_eclaim.eClaim_lodging_get()
        if ld_out_message.get("MESSAGE") == 'FOUND':
            dict = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
            return dict
    elif subcat == 'Miscellaneous Charges':
        obj_eclaim.filter_json = json.dumps(filter)
        ld_out_message = obj_eclaim.eClaim_miscellaneous_get()
        if ld_out_message.get("MESSAGE") == 'FOUND':
            dict = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
            return dict
    elif subcat == 'Packaging/Freight':
        obj_eclaim.filter_json = json.dumps(filter)
        ld_out_message = obj_eclaim.eClaim_packingmoving_get()
        if ld_out_message.get("MESSAGE") == 'FOUND':
            dict = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
            return dict

def branch_apicall(self, request, entity_gid,branchgid):
    tk = str(request.auth.token)
    token = "Bearer  " + tk[2:len(tk) - 1]
    drop_cat = {
        "Table_name": "gal_mst_tbranch",
        "Column_1": "branch_code,branch_name,branch_gid",
        "Column_2": "",
        "Where_Common": "branch",
        "Where_Primary": "gid",
        "Primary_Value":branchgid ,
        "Order_by": "gid"
    }
    drop_tables = {"data": drop_cat}
    action = 'Debit'
    params = {'Action': action, 'Entity_Gid': encrypt1(entity_gid)}
    headers = {"content-type": "application/json", "Authorization": "" + token + ""}
    datas = json.dumps(drop_tables.get('data'))
    resp = requests.post("" + ip + "/All_Tables_Values_Get", params=params, data=datas, headers=headers,
                         verify=False)
    branch_data = json.loads(resp.content.decode("utf-8"))
    branch_data = branch_data.get('DATA')
    return branch_data

def advance_adjust(self, request,tourgid):
    empgid = request.auth.payload.get('user_id')
    obj_claim = meClaim.eClaim_Model()
    emp_data = {
        "empids": empgid
    }
    obj_claim.filter_json = json.dumps(emp_data)
    emp_bnk = obj_claim.eClaim_employeebnk_get()
    bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
    entity_gid = bank_data[0].get('entity_gid')
    tk = str(request.auth.token)
    token = "Bearer  " + tk[2:len(tk) - 1]
    params = {'Entity_Gid':entity_gid,"TourGid":tourgid,"Api_Type" : "WEB"}
    headers = {"content-type": "application/json", "Authorization": "" + token + ""}
    datas = {}
    resp = requests.get("" + ip + "/AP_ADVANCE_GET", params=params, data=datas, headers=headers,
                         verify=False)
    return_data = json.loads(resp.content.decode("utf-8"))

    if return_data.get('MESSAGE') =='FOUND':
        return_data = return_data.get('DATA')
        ld_dict ={
            "MESSAGE":'SUCCESS'
        }
        if ld_dict.get("MESSAGE") == 'SUCCESS':
            for i in return_data:
                data ={
                    "Params":{
                        "DETAILS":{
                            "advance_gid": i.get('advancegid'),
                            "ppx_headergid": i.get('ppxheader_gid'),
                            "adjustamount": i.get('adjustamount'),
                            "processedby": empgid,
                            "createby": empgid,
                            "Entity_Gid": entity_gid
                        }
                    }
                }
                params = {'Api_Type': "WEB"}
                headers = {"content-type": "application/json", "Authorization": "" + token + ""}
                datas = json.dumps(data)
                resp = requests.post("" + ip + "/ADVANCE_ADJUST", params=params, data=datas, headers=headers,
                                    verify=False)
                advance_data = json.loads(resp.content.decode("utf-8"))
                if advance_data.get("MESSAGE") == 'SUCCESS':
                    return {"MESSAGE": "SUCCESS"}
                else:
                    return {"MESSAGE": "FAIL in Advance Adjust", "STATUS": 0}
    else :
        return {"MESSAGE": "SUCCESS"}


from Bigflow.settings import Password_Key
from hashids import Hashids


def encrypt1(text):
    hashids = Hashids(salt=Password_Key)
    ints = hashids.encode(text)
    return ints
