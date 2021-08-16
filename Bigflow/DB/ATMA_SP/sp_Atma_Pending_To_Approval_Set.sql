CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Pending_To_Approval_Set`(in li_Action  varchar(30),
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_Atma_Pending_To_Approval_Set:BEGIN
declare Query_Insert varchar(10000);
Declare countRow varchar(6000);
declare Query_Update varchar(10000);
declare Query_Update1 varchar(10000);
declare Query_delete varchar(1000);
declare Query_Value varchar(1000);
declare Query_Column varchar(1000);
declare new_insert_gid varchar(1000);
Declare v_director_gid,v_director_partnergid,v_director_name,v_director_isactive,v_director_isremoved,v_create_by,v_entity_gid,v_main_director_gid varchar(128) ;
DECLARE finished INTEGER DEFAULT 0;
Declare p_partnerbranch_gid,p_partnerbranch_gstno,p_partnerbranch_panno,p_partnerbranch_addressgid,p_partnerbranch_contactgid,p_partnerbranch_name
,p_partnerbranch_creditperiod,p_partnerbranch_creditlimit,p_partnerbranch_paymentterms,p_partnerbranch_code
 varchar(150);
DECLARE finished1 INTEGER DEFAULT 0;
Declare  a_address_gid,a_address_ref_code,a_address_1, a_address_2, a_address_3, a_address_pincode,
a_address_district_gid,a_address_city_gid, a_address_state_gid, a_entity_gid,
         a_create_by,a_update_by,a_main_address_gid varchar(150);

Declare  c_contact_gid,c_Contact_ref_gid,c_Contact_reftable_gid,
c_contact_reftablecode,c_Contact_contacttype_gid,
c_Contact_personname,c_Contact_designation_gid,c_Contact_landline,
c_Contact_landline2,c_Contact_mobileno,
c_Contact_mobileno2,c_Contact_email,c_Contact_DOB,c_Contact_WD,
c_entity_gid,c_create_by,c_update_by,c_main_contact_gid varchar(150);
DECLARE finished_partnerproduct INTEGER DEFAULT 0;
declare m_mpartnerproduct_product_gid,m_mpartnerproduct_unitprice,
m_mpartnerproduct_packingprice,m_mpartnerproduct_validfrom,m_mpartnerproduct_validto,
m_mpartnerproduct_deliverydays,m_mpartnerproduct_capacitypw,m_mpartnerproduct_dts varchar(150);
DECLARE finished_supplierpayment INTEGER DEFAULT 0;
Declare p_payment_gid,p_payment_partnergid,p_payment_partnerbranchgid,p_payment_paymodegid,p_payment_bankgid,p_payment_bankbranchgid,p_payment_acctype,p_payment_accnumber,
		p_payment_benificiaryname,p_entity_gid,p_create_by varchar(150);
Declare errno int;
Declare msg varchar(1000);

DECLARE EXIT HANDLER FOR SQLEXCEPTION
BEGIN
GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
set Message = concat(errno , msg);
ROLLBACK;
END;

IF li_Action='Pending_To_Approval_Insert' then

START TRANSACTION;

select JSON_LENGTH(lj_filter,'$') into @lj_filter_json_count;
select JSON_LENGTH(lj_classification,'$') into @lj_classification_json_count;

if @lj_filter_json_count = 0 or @lj_filter_json_count is null then
set Message = '1.No Data In filter Json. ';
leave sp_Atma_Pending_To_Approval_Set;
End if;

select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Gid'))) into @Partner_Gid;
select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Status'))) into @Partner_Status;
select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Entity_Gid'))) into @Entity_Gid;
select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Update_By'))) into @Update_By;

   if @Partner_Gid = '' or @Partner_Gid is null  or @Partner_Gid=0 then
		set Message = '1.Partner is not provided';
		leave sp_Atma_Pending_To_Approval_Set;
	End if;
	if @partner_status = '' or @partner_status is null then
		set Message = '1.Partner Status Is Not Provided';
		leave sp_Atma_Pending_To_Approval_Set;
	End if;

    set @Pr_Gid='';
    select partner_gid from atma_tmp_tpartner where partner_gid=@Partner_Gid into @Pr_Gid;
    if @Pr_Gid = '' or @Pr_Gid is null  or @Pr_Gid=0 then
		set Message = '1.2 - Partner is not available(Temp)';
		leave sp_Atma_Pending_To_Approval_Set;
	End if;

	select main_partner_gid from atma_tmp_tpartner where partner_gid=@Partner_Gid into @Main_partner_gid;

	SELECT partner_addressgid,partner_contactgid into @partneraddressgid,@partnercontactgid
		FROM atma_tmp_tpartner where Partner_Gid=@Partner_Gid;

  #####start address and contact

    select  address_gid,address_ref_code,address_1,address_2,address_3,address_pincode,
	address_district_gid,address_city_gid,address_state_gid,entity_gid,
	create_by,update_by,main_address_gid
                        into a_address_gid,a_address_ref_code,a_address_1,a_address_2,a_address_3,
	a_address_pincode,a_address_district_gid,a_address_city_gid,
	a_address_state_gid,a_entity_gid,a_create_by ,a_update_by,a_main_address_gid
	from atma_tmp_mst_taddress where address_gid=@partneraddressgid ;

	#select a_main_address_gid;
if a_main_address_gid = '' or a_main_address_gid is null  or a_main_address_gid=0 then
	set Query_Column='';
	set Query_Value ='';

	if a_address_1 is not null and a_address_1 <> '' then
	set Query_Column = concat(Query_Column,',address_1 ');
	set Query_Value=concat(Query_Value,', ''',a_address_1,''' ');
	end if;

	if a_address_2 is not null and a_address_2 <> ''  then
	set Query_Column = concat(Query_Column,',address_2 ');
	set Query_Value=concat(Query_Value,', ''',a_address_2,''' ');
	end if;

	if a_address_3 is not null and a_address_3 <> '' then
	set Query_Column = concat(Query_Column,',address_3 ');
	set Query_Value=concat(Query_Value,', ''',a_address_3,''' ');
	end if;

	if a_address_pincode is not null and a_address_pincode <> '' then
	set Query_Column = concat(Query_Column,',address_pincode ');
	set Query_Value=concat(Query_Value,', ',a_address_pincode,' ');
	end if;

	if a_address_city_gid is not null and a_address_city_gid <> '' then
	set Query_Column = concat(Query_Column,',address_city_gid ');
	set Query_Value=concat(Query_Value,', ',a_address_city_gid,' ');
	end if;

	if a_address_state_gid is not null and a_address_state_gid <> '' then
	set Query_Column = concat(Query_Column,',address_state_gid ');
	set Query_Value=concat(Query_Value,', ',a_address_state_gid,' ');
	end if;
	#select Query_Column,Query_Value;

	set Query_Update = concat('INSERT INTO gal_mst_taddress
	( address_ref_code,address_district_gid,entity_gid, create_by, create_date ',Query_Column,')
   values (''',a_address_ref_code,''',',a_address_district_gid,',
	',a_entity_gid,',',a_create_by,',''',Now(),'''
	',Query_Value,')'
	);
else
	set Query_Update = concat('Update gal_mst_taddress
	set address_1 = ''',ifnull(a_address_1,''),''',
	address_2 = ''',ifnull(a_address_2,''),''',
	address_3 = ''',ifnull(a_address_3,''),''',
	address_pincode =''',ifnull(a_address_pincode,''),''',
	address_city_gid = ',ifnull(a_address_city_gid,0),',
	address_state_gid = ',ifnull(a_address_state_gid,0),',
	address_district_gid =  ',a_address_district_gid,',
	update_date = CURRENT_TIMESTAMP,
	Update_By = ',@Update_By,'
	where address_gid=',a_main_address_gid,' ');
    select Query_Update;
end if;
	#select Query_Update,'ADD';

	set @Insert_query = Query_Update;
	PREPARE stmt FROM @Insert_query;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
	if countRow >  0 then
		set Message = 'SUCCESS';
	else
		set Message = 'FAILED-1.4';
		rollback;
		leave sp_Atma_Pending_To_Approval_Set;
	end if;

    if a_main_address_gid = '' or a_main_address_gid is null  or a_main_address_gid=0 then
		set @Address_Gid='';
		select last_insert_id() into @Address_Gid;
    else
		set @Address_Gid=a_main_address_gid;
    end if;

	SET SQL_SAFE_UPDATES = 0;
	set Query_delete=concat('DELETE FROM atma_tmp_mst_taddress WHERE address_gid=',a_address_gid,'');
    set @Insert_query = Query_delete;
	PREPARE stmt FROM @Insert_query;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
    if countRow >  0 then
		set Message = 'SUCCESS';
        #select 'partner add -address -success';
	else
		set Message = ' FAILED-1.5';
        rollback;
		leave sp_Atma_Pending_To_Approval_Set;
	end if;




select  contact_gid,Contact_ref_gid,Contact_reftable_gid,
contact_reftablecode,Contact_contacttype_gid,
Contact_personname,Contact_designation_gid,Contact_landline,
Contact_landline2,Contact_mobileno,
Contact_mobileno2,Contact_email,Contact_DOB,Contact_WD,
entity_gid,create_by,update_by,main_contact_gid
                        into c_contact_gid,c_Contact_ref_gid,c_Contact_reftable_gid,
c_contact_reftablecode,c_Contact_contacttype_gid,
c_Contact_personname,c_Contact_designation_gid,c_Contact_landline,
c_Contact_landline2,c_Contact_mobileno,
c_Contact_mobileno2,c_Contact_email,c_Contact_DOB,c_Contact_WD,
c_entity_gid,c_create_by,c_update_by,c_main_contact_gid
from   atma_tmp_mst_tcontact
                        where contact_gid=@partnercontactgid ;



if c_main_contact_gid = '' or c_main_contact_gid is null  or c_main_contact_gid=0 then

set Query_Column='';
set Query_Value ='';

            if c_Contact_personname is not null and c_Contact_personname<>'' then
set Query_Column = concat(Query_Column,',Contact_personname');
set Query_Value=concat(Query_Value,', ''',c_Contact_personname,''' ');
            end if;

            if c_Contact_landline is not null and c_Contact_landline <>'' then
set Query_Column = concat(Query_Column,',Contact_landline');
set Query_Value=concat(Query_Value,', ',c_Contact_landline,' ');
            end if;

            if c_Contact_landline2 is not null and c_Contact_landline2 <>'' then
set Query_Column = concat(Query_Column,',Contact_landline2');
set Query_Value=concat(Query_Value,', ',c_Contact_landline2,' ');
            end if;

            if c_Contact_mobileno is not null and c_Contact_mobileno <>'' then
set Query_Column = concat(Query_Column,',Contact_mobileno');
set Query_Value=concat(Query_Value,', ',c_Contact_mobileno,' ');
            end if;

if c_Contact_mobileno2 is not null and c_Contact_mobileno2 <>'' then
set Query_Column = concat(Query_Column,',Contact_mobileno2');
set Query_Value=concat(Query_Value,', ',c_Contact_mobileno2,' ');
            end if;

            if c_Contact_email is not null  and c_Contact_email <>'' then
set Query_Column = concat(Query_Column,',Contact_email');
set Query_Value=concat(Query_Value,', ''',c_Contact_email,''' ');
            end if;

            if c_Contact_DOB is not null and c_Contact_DOB <>'' then
set Query_Column = concat(Query_Column,',Contact_DOB');
set Query_Value=concat(Query_Value,', ''',c_Contact_DOB,''' ');
            end if;

            if c_Contact_WD is not null  and c_Contact_WD <>'' then
set Query_Column = concat(Query_Column,',Contact_WD');
set Query_Value=concat(Query_Value,', ''',c_Contact_WD,''' ');
            end if;

set Query_Update = concat('INSERT INTO gal_mst_tcontact
 ( Contact_ref_gid, Contact_reftable_gid, contact_reftablecode,
                                              Contact_contacttype_gid, Contact_designation_gid,
                                              entity_gid, create_by, create_date ',Query_Column,')
   values (',c_Contact_ref_gid,',',c_Contact_reftable_gid,',
''',c_contact_reftablecode,''',',c_Contact_contacttype_gid,',
',c_Contact_designation_gid,',',c_entity_gid,',',c_create_by,' ,
''',Now(),''' ',Query_Value,')'
);


else
set Query_Update1='';
if c_Contact_DOB is null  then
set Query_Update1 = concat('Contact_DOB = null,');
                else
set Query_Update1 = concat('Contact_DOB = ''',c_Contact_DOB,''',');
end if;

                if c_Contact_WD is null  then
set Query_Update1 = concat(Query_Update1,'Contact_WD = null,');
                else
set Query_Update1 = concat(Query_Update1,'Contact_WD = ''',c_Contact_WD,''',');
end if;
                    #Contact_DOB = ''',ifnull(c_Contact_DOB,'0000-00-00 00:00:00'),''',
# Contact_WD = ''',ifnull(C_Contact_WD,'0000-00-00 00:00:00'),''',

set Query_Update = concat(' Update gal_mst_tcontact
set Contact_contacttype_gid = ',c_Contact_contacttype_gid,',
                                        Contact_designation_gid = ',c_Contact_designation_gid,',
                                        Contact_personname = ''',ifnull(c_Contact_personname,''),''',
                                        Contact_landline = ''',ifnull(c_Contact_landline,''),''',
                                        Contact_landline2 = ''',ifnull(c_Contact_landline2,''),''',
                                        Contact_mobileno = ''',ifnull(c_Contact_mobileno,''),''',
                                        Contact_mobileno2 = ''',ifnull(c_Contact_mobileno2,''),''',
                                        Contact_email = ''',ifnull(c_Contact_email,''),''',
',Query_Update1,'
                                        Update_By=',@Update_By,',
                                        update_date = ''',now(),'''
Where contact_gid = ',c_main_contact_gid,'
                                              ');


         select Query_Update;
end if;



        #select Query_Update,'CON';
set @Insert_query = Query_Update;
PREPARE stmt FROM @Insert_query;
EXECUTE stmt;
set countRow = (select ROW_COUNT());
DEALLOCATE PREPARE stmt;
if countRow >  0 then
set Message = 'SUCCESS';
            #select 'partner add -contact -success';
else
set Message = ' FAILED_BR';
            rollback;
leave sp_Atma_Pending_To_Approval_Set;
end if;

         SET SQL_SAFE_UPDATES = 0;
set Query_delete=concat('DELETE FROM atma_tmp_mst_tcontact
WHERE contact_gid=',c_contact_gid,'');
    #select Query_delete,c_contact_gid;
    set @Insert_query = Query_delete;
PREPARE stmt FROM @Insert_query;
EXECUTE stmt;
set countRow = (select ROW_COUNT());
DEALLOCATE PREPARE stmt;
    if countRow >  0 then
set Message = 'SUCCESS';
else
set Message = ' FAILED_PARTNER_C deletion';
        rollback;
leave sp_Atma_Pending_To_Approval_Set;
end if;

       set @Contact_Gid='';
            select last_insert_id() into @Contact_Gid;

if @Main_partner_gid = '' or @Main_partner_gid is null  or @Main_partner_gid=0 then
set Query_Insert='';
set Query_Insert=concat('INSERT INTO atma_mst_tpartner (partner_code,partner_name,partner_panno,partner_compregno,
partner_group,partner_custcategorygid,
partner_Classification,partner_type,partner_web,partner_activecontract,
partner_reason_no_contract,partner_contractdatefrom,
partner_contractdateto,partner_aproxspend,partner_actualspend,
partner_noofdir,partner_orgtype,partner_renewaldate,partner_remarks,
partner_requestfor,partner_status,partner_mainstatus,partner_renewdate,
partner_rmname,partner_addressgid,partner_contactgid,
partner_isactive,partner_isremoved,entity_gid,
create_by,create_date,update_by,update_date)
SELECT partner_code,partner_name,partner_panno,partner_compregno,partner_group,
partner_custcategorygid,
partner_Classification,partner_type,partner_web,partner_activecontract,
partner_reason_no_contract,partner_contractdatefrom,
partner_contractdateto,partner_aproxspend,partner_actualspend,partner_noofdir,
partner_orgtype,partner_renewaldate,partner_remarks,
partner_requestfor,''',@Partner_Status,''',''',@Partner_Status,''',partner_renewdate,
partner_rmname,',@Address_Gid,',',@Contact_Gid,',
partner_isactive,partner_isremoved,entity_gid,
create_by,create_date,update_by,update_date  FROM atma_tmp_tpartner
where Partner_Gid=',@Partner_Gid,' ');
#select Query_Insert;
set @Insert_query = Query_Insert;
PREPARE stmt FROM @Insert_query;
EXECUTE stmt;
set countRow = (select ROW_COUNT());
DEALLOCATE PREPARE stmt;
    if countRow >  0 then
set Message = 'SUCCESS';
        #select 'partner add  -success';
        SELECT partner_code,partner_name,partner_addressgid,partner_contactgid,partner_contractdatefrom,partner_contractdateto
        into @partner_code,@partner_name,@partner_addressgid,@partner_contactgid,@partner_contractdatefrom,@partner_contractdateto
                                    FROM atma_tmp_tpartner
where Partner_Gid=@Partner_Gid;
else
set Message = 'FAILED PAR';
rollback;
        leave sp_Atma_Pending_To_Approval_Set;
end if;
set @NEWPartnergid='';
select LAST_INSERT_ID() into @NEWPartnergid;
#select @NEWPartnergid;
    set Query_Insert=concat('INSERT INTO atma_mst_tdirectors (director_partnergid,director_name,director_isactive,
director_isremoved,entity_gid,create_by,create_date,update_by,update_date) SELECT
                            ',@NEWPartnergid,',director_name,director_isactive,director_isremoved,entity_gid,create_by,
                            create_date,update_by,update_date FROM atma_tmp_mst_tdirectors
where director_partnergid=',@Partner_Gid,' ');
    set @Insert_query = Query_Insert;
PREPARE stmt FROM @Insert_query;
EXECUTE stmt;
set countRow = (select ROW_COUNT());
DEALLOCATE PREPARE stmt;
    if countRow >  0 then
set Message = 'SUCCESS';
        #select 'partner add -director -success';
else
set Message = 'FAILED DIR';
rollback;
        leave sp_Atma_Pending_To_Approval_Set;
end if;

    SET SQL_SAFE_UPDATES = 0;
set Query_delete=concat('DELETE FROM atma_tmp_mst_tdirectors WHERE director_partnergid=',@Partner_Gid,'');
    set @Insert_query = Query_delete;
PREPARE stmt FROM @Insert_query;
EXECUTE stmt;
set countRow = (select ROW_COUNT());
DEALLOCATE PREPARE stmt;
    if countRow >  0 then
set Message = 'DELETED';
else
set Message = ' FAILED_DIR deletion';
rollback;
        leave sp_Atma_Pending_To_Approval_Set;
end if;

else

set Query_Update = concat('Update atma_mst_tpartner as A, atma_tmp_tpartner as B set
A.partner_code=B.partner_code,A.partner_name=B.partner_name,
    A.partner_panno=B.partner_panno,A.partner_compregno=B.partner_compregno,
A.partner_group=B.partner_group,A.partner_custcategorygid=B.partner_custcategorygid,
    A.partner_Classification=B.partner_Classification,
A.partner_type=B.partner_type,A.partner_web=B.partner_web,
    A.partner_activecontract=B.partner_activecontract,
    A.partner_reason_no_contract=B.partner_reason_no_contract,
A.partner_contractdatefrom=B.partner_contractdatefrom,
    A.partner_contractdateto=B.partner_contractdateto,
    A.partner_aproxspend=B.partner_aproxspend,
A.partner_actualspend=B.partner_actualspend,
    A.partner_noofdir=B.partner_noofdir,
    A.partner_orgtype=B.partner_orgtype,
A.partner_remarks=B.partner_remarks,
    A.partner_requestfor=B.partner_requestfor,
    A.partner_status=''',@Partner_Status,''',
    A.partner_mainstatus=''',@Partner_Status,''',
    A.partner_renewdate=B.partner_renewdate,
A.partner_rmname=B.partner_rmname,A.partner_isactive=B.partner_isactive,
A.partner_isremoved=B.partner_isremoved,A.entity_gid=B.entity_gid,
A.create_by=B.create_by,A.create_date=B.create_date,A.update_by=',@Update_By,',A.update_date=B.update_date where
A.partner_gid= B.main_partner_gid and B.main_partner_gid=',@Main_partner_gid,'');
select Query_Update;
set @Insert_query = Query_Update;
PREPARE stmt FROM @Insert_query;
EXECUTE stmt;
set countRow = (select ROW_COUNT());
DEALLOCATE PREPARE stmt;
    if countRow >  0 then
set Message = 'SUCCESS';
else
set Message = 'FAILED UPDATE_PAR';
rollback;
        leave sp_Atma_Pending_To_Approval_Set;
end if;


    BEGIN
Declare Cursor_atma CURSOR FOR

select director_gid,director_partnergid,director_name,director_isactive,director_isremoved,create_by,entity_gid,
main_director_gid from atma_tmp_mst_tdirectors where director_partnergid=@Partner_Gid ;

DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;
OPEN Cursor_atma;
atma_looop:loop
fetch Cursor_atma into v_director_gid,v_director_partnergid,v_director_name,v_director_isactive,v_director_isremoved,v_create_by,v_entity_gid,v_main_director_gid;
if finished = 1 then
leave atma_looop;
End if;

if v_main_director_gid = '' or v_main_director_gid is null  or v_main_director_gid=0 then
set Query_Update = concat('INSERT INTO atma_mst_tdirectors (director_partnergid,director_name,director_isactive,
director_isremoved,create_by,entity_gid)values (',@Main_partner_gid,',
''',v_director_name,''',''',v_director_isactive,''',''',v_director_isremoved,''',',v_create_by,',',v_entity_gid,')');

            #select  Query_Update;
            SET SQL_SAFE_UPDATES = 0;
            set Query_delete=concat('DELETE FROM atma_tmp_mst_tdirectors WHERE director_gid=',v_director_gid,'');
set @Insert_query = Query_delete;
PREPARE stmt FROM @Insert_query;
EXECUTE stmt;
set countRow = (select ROW_COUNT());
DEALLOCATE PREPARE stmt;
if countRow >  0 then
set Message = 'DELETED';
else
set Message = ' FAILED_DIR DELETION';
rollback;
            leave sp_Atma_Pending_To_Approval_Set;
end if;

else
SET SQL_SAFE_UPDATES = 0;
set Query_Update = concat('Update atma_mst_tdirectors  set
director_name=''',v_director_name,''',
            director_isactive=''',v_director_isactive,''',
            director_isremoved=''',v_director_isremoved,''',
            update_by=',@Update_By,',
            update_date=''',Now(),''',
entity_gid=',v_entity_gid,' where
director_gid=',v_main_director_gid,'');
         #select Query_Update,'direct';
            SET SQL_SAFE_UPDATES = 0;
            set Query_delete=concat('DELETE FROM atma_tmp_mst_tdirectors WHERE director_gid=',v_director_gid,'');
set @Insert_query = Query_delete;
PREPARE stmt FROM @Insert_query;
EXECUTE stmt;
set countRow = (select ROW_COUNT());
DEALLOCATE PREPARE stmt;
if countRow >  0 then
set Message = 'DELETED';
else
set Message = ' FAILED_DIR DELETION';
rollback;
            leave sp_Atma_Pending_To_Approval_Set;
end if;


end if;
set @Insert_query = Query_Update;
PREPARE stmt FROM @Insert_query;
EXECUTE stmt;
set countRow = (select ROW_COUNT());
DEALLOCATE PREPARE stmt;
if countRow >  0 then
set Message = 'SUCCESS';
else
set Message = 'UPDATE FAILED PARTNER_DIR';
rollback;
            leave sp_Atma_Pending_To_Approval_Set;
end if;
End loop atma_looop;
close Cursor_atma;
end;


end if;

         select main_partner_gid from atma_tmp_tpartner where partner_gid=@Partner_Gid into @maingid;


if @maingid > 0 then
set new_insert_gid=@maingid;
else
set new_insert_gid=@NEWPartnergid;
end if;
select new_insert_gid;

call sp_Atma_Pending_To_Approval_profile_Set('insert',lj_filter,new_insert_gid,lj_classification,@Message);
select @Message into @Out_Message_profile;
if  @Out_Message_profile <> 'SUCCESS' then
select @Out_Message_profile;
set Message = @Out_Message_profile;
        rollback;
leave sp_Atma_Pending_To_Approval_Set;
else
select 'profile_Set -success';
End if;

call sp_Atma_Pending_To_Approval_PR_Client_Set(lj_filter,new_insert_gid,lj_classification,@Message);
select @Message into @Out_Message_Client;
#select @Out_Message_Client;
if  @Out_Message_Client <> 'SUCCESS' then
set Message = @Out_Message_Client;
rollback;
leave sp_Atma_Pending_To_Approval_Set;
else
select 'Client_Set -success';
End if;


call sp_Atma_Pending_To_Approval_PR_Product_Set(lj_filter,new_insert_gid,lj_classification,@Message);
select @Message into @Out_Message_Product;
#select @Out_Message_Product;
if  @Out_Message_Product <> 'SUCCESS' then
set Message = @Out_Message_Product;
rollback;
leave sp_Atma_Pending_To_Approval_Set;
else
select 'PR_Product_Set -success';
End if;

call sp_Atma_Pending_To_Approval_partnercontractor_Set('insert',lj_filter,new_insert_gid,lj_classification,@Message);
select @Message into @Out_Message_partnercontractor;

if  @Out_Message_partnercontractor <> 'SUCCESS' then
#select @Out_Message_partnercontractor;
set Message = @Out_Message_partnercontractor;
rollback;
leave sp_Atma_Pending_To_Approval_Set;
else
select 'contractor -success';
End if;

call sp_Atma_Pending_To_Approval_Taxdetails_Set('Insert',lj_filter,lj_classification,@Message);
select @Message into @Out_Message_Taxdetails;
##select @Out_Message_Taxdetails;
if  @Out_Message_Taxdetails <> 'SUCCESS' then
set Message = @Out_Message_Taxdetails;
rollback;
leave sp_Atma_Pending_To_Approval_Set;
else
select 'tax -success';
End if;


call sp_Atma_Pending_To_Approval_Document_Set('Insert',lj_filter,new_insert_gid,lj_classification,@Message);
select @Message into @Out_Message_Document;
#select @Out_Message_Document;
if  @Out_Message_Document <> 'SUCCESS' then
set Message = @Out_Message_Document;
rollback;
leave sp_Atma_Pending_To_Approval_Set;
else
select 'document -success';
End if;


call sp_Atma_Pending_To_Approval_PR_Branch_Set(lj_filter,new_insert_gid,lj_classification,@Message);
select @Message into @Out_Message_Branch;
select @Out_Message_Branch;
if  @Out_Message_Branch <> 'SUCCESS' then
set Message = @Out_Message_Branch;
rollback;
leave sp_Atma_Pending_To_Approval_Set;
else
select 'branch -success';
#rollback;#remove
End if;


SET SQL_SAFE_UPDATES = 0;
set Query_delete=concat('DELETE FROM atma_tmp_tpartner WHERE partner_gid=',@Partner_Gid,'');
set @Insert_query = Query_delete;
PREPARE stmt FROM @Insert_query;
EXECUTE stmt;
set countRow = (select ROW_COUNT());
DEALLOCATE PREPARE stmt;
if countRow >  0 then
set Message = 'SUCCESS';
else
set Message = ' FAILED_PARTNER deletion';
rollback;
leave sp_Atma_Pending_To_Approval_Set;
end if;


select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.TRAN_Remarks')))
into @TRAN_Remarks;
select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Create_By')))
into @Create_By;



set @trn_partner_gid ='';
if @Main_partner_gid is null then
set @trn_partner_gid=@NEWPartnergid;
else
set @trn_partner_gid=@Main_partner_gid;
end if;

select fn_REFGid('PARTNER_NAME_TRAN_MST') into @partner_ref_gid_mst;
select fn_REFGid('PARTNER_NAME_TRAN') into @partner_ref_gid_tmp;

update  gal_trn_ttran set  tran_ref_gid=@partner_ref_gid_mst,tran_reftable_gid= @trn_partner_gid
where  tran_ref_gid=@partner_ref_gid_tmp and tran_reftable_gid=@Partner_Gid ;

call sp_Trans_Set('Update','PARTNER_NAME_TRAN_MST',@trn_partner_gid,
@Partner_Status,'C',@Create_By,ifnull(@TRAN_Remarks,''),@Entity_Gid,@Create_By,@message);
select @message into @out_msg_tran ;
#select @out_msg_tran;

if @out_msg_tran = 'FAIL' then
	set Message = 'Failed On Tran Insert';
	rollback;
	leave sp_Atma_Pending_To_Approval_Set;
end if;

#if @out_msg_tran = 'SUCCESS' then
if @out_msg_tran > 0 then
	select @out_msg_tran,'in tran success' ;
if @Main_partner_gid = '' or @Main_partner_gid is null  or @Main_partner_gid=0 then
	SET @Supplier_capacity=0;
	set @lj_supplier= concat('{"Supplier_Group_Name":"',@partner_name,'","Supplier_Capacity":0,
								"AtmaSupplierGrp_Code":"',@partner_code,'"}');
	set @lj_address=concat('{"supplier_add_gid":',@Address_Gid,'}');
	set @lj_contact=concat('{"supplier_contact_gid":',@Contact_Gid,'}');
	#select @lj_supplier,@lj_address,@lj_contact;
	call sp_SupplierSPS_Set('SUPPLIER_GROUP_INSERT',@lj_supplier,@lj_address,@lj_contact,lj_Classification,@Message);
	select @Message into @Out_Msg_SupplierGROUP ;
    #select @Out_Msg_SupplierGROUP;
	if @Out_Msg_SupplierGROUP >0 then
		set @out_msg_suppgroup='SUCCESS';
	else
		set @out_msg_suppgroup='FAIL';
	end if;
else
	set @out_msg_suppgroup='FAIL';
    #rollback;
    commit;
end if;
end if;#if @out_msg_tran = 'SUCCESS' then
if @out_msg_suppgroup='SUCCESS' then
	set @Supplier_msg ='';
	SET finished1 =0;
	BEGIN
	Declare Cursor_atma1 CURSOR FOR

		select partnerbranch_gid,partnerbranch_gstno,partnerbranch_panno,partnerbranch_addressgid,partnerbranch_contactgid,partnerbranch_name,
		partnerbranch_creditperiod,partnerbranch_creditlimit,partnerbranch_paymentterms,partnerbranch_code
		from atma_mst_tpartnerbranch
        where partnerbranch_partnergid=new_insert_gid and partnerbranch_isactive='Y'
		and  partnerbranch_isremoved='N';

	DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished1 = 1;

	OPEN Cursor_atma1;
	atma_looop1:loop

	fetch Cursor_atma1 into p_partnerbranch_gid,p_partnerbranch_gstno,p_partnerbranch_panno,p_partnerbranch_addressgid,
    p_partnerbranch_contactgid,p_partnerbranch_name,p_partnerbranch_creditperiod,p_partnerbranch_creditlimit,
    p_partnerbranch_paymentterms,p_partnerbranch_code;
	if finished1 = 1 then
		leave atma_looop1;
	End if;

	set @lj_supplier= concat('{"Supplier_Name":"',@partner_name,'","Supplier_Capacity":0,
		"atmaSupplier_Code":"',p_partnerbranch_code,'","Supplier_Group_Gid":',@Out_Msg_SupplierGROUP,',
		"Supplier_Branch_Name":"',p_partnerbranch_name,'","Supplier_GST_No":"',ifnull(p_partnerbranch_gstno,''),'",
		"Supplier_Panno":"',ifnull(p_partnerbranch_panno,''),'"}');
		set @lj_address=concat('{"supplier_add_gid":',p_partnerbranch_addressgid,'}');
		set @lj_contact=concat('{"supplier_contact_gid":',p_partnerbranch_contactgid,'}');

	#select @lj_supplier,@lj_address,@lj_contact,lj_Classification;
	call sp_SupplierSPS_Set('SUPP_INSERT',@lj_supplier,@lj_address,@lj_contact,lj_Classification,@Message);
	select @Message into @Supplier_partner ;
	#select @Supplier_partner;

	SET @suppliergid = (SELECT SPLIT_STR((@Supplier_partner), ',', 2));
	SET @Supplier_msg = (SELECT SPLIT_STR((@Supplier_partner), ',', 1));
	#SELECT @suppliergid;
	#SELECT @Supplier_msg;
	#SET @suppliergid=(select SUBSTRING_INDEX(@Supplier_partner,',',-1));
	#SET @Supplier_msg=(select SUBSTRING_INDEX(@Supplier_partner,',',1));
	if @Supplier_msg = 'SUCCESS' then
		SET finished_partnerproduct =0;
		BEGIN
		Declare Cursor_atma_partnerproduct CURSOR FOR

		select mpartnerproduct_product_gid,mpartnerproduct_unitprice,
		mpartnerproduct_packingprice,mpartnerproduct_validfrom,mpartnerproduct_validto,
		mpartnerproduct_deliverydays,mpartnerproduct_capacitypw,mpartnerproduct_dts
		from atma_map_tpartnerproduct where mpartnerproduct_partner_gid=new_insert_gid
		and mpartnerproduct_partnerbranch_gid=p_partnerbranch_gid;

		DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished_partnerproduct = 1;

		OPEN Cursor_atma_partnerproduct;
		atma_looopsupplier:loop
		fetch Cursor_atma_partnerproduct into m_mpartnerproduct_product_gid,m_mpartnerproduct_unitprice,
		m_mpartnerproduct_packingprice,m_mpartnerproduct_validfrom,m_mpartnerproduct_validto,
		m_mpartnerproduct_deliverydays,m_mpartnerproduct_capacitypw,m_mpartnerproduct_dts;
		if finished_partnerproduct = 1 then
		leave atma_looopsupplier;
		End if;

		set @lj_supplier_map= concat('{"supplierproduct_supplier_gid":"',@suppliergid,'",
								"supplierproduct_product_gid":"',m_mpartnerproduct_product_gid,'",
                                "supplierproduct_unitprice":"',m_mpartnerproduct_unitprice,'",
								"supplierproduct_packingprice":"',m_mpartnerproduct_packingprice,'",
                                "supplierproduct_validfrom":"',m_mpartnerproduct_validfrom,'",
								"supplierproduct_validto":"',m_mpartnerproduct_validto,'",
                                "supplierproduct_dts":"',m_mpartnerproduct_dts,'"
                                }');
        call sp_SupplierProductMap_Set('Insert',@lj_supplier_map,@Entity_Gid,@Create_By, @Message);
        select @Message into @Out_Message_supplier_map;
        SET @Out_msg = (SELECT SPLIT_STR((@Out_Message_supplier_map), ',', 2));

		if @Out_msg <> 'SUCCESS' then
		set Message = concat('Error On supplier_map',@Out_msg);
		rollback;
		leave sp_Atma_Pending_To_Approval_Set;
		End if;

		End loop atma_looopsupplier;
		close Cursor_atma_partnerproduct;
		end;
		#####paymentDetails open
		SET finished_supplierpayment =0;
		BEGIN
		Declare Cursor_atma_supplierpayment CURSOR FOR

		select payment_gid,payment_partnergid,payment_partnerbranchgid,payment_paymodegid,
		payment_bankgid,payment_bankbranchgid,
		payment_acctype,payment_accnumber,payment_benificiaryname,entity_gid,create_by
		from atma_mst_tpayment where payment_partnergid=new_insert_gid
		and payment_partnerbranchgid=p_partnerbranch_gid;

		DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished_supplierpayment = 1;

		OPEN Cursor_atma_supplierpayment;
		atma_looopsupplierpayment:loop
		fetch Cursor_atma_supplierpayment into p_payment_gid,p_payment_partnergid,p_payment_partnerbranchgid,
		p_payment_paymodegid,p_payment_bankgid,p_payment_bankbranchgid,p_payment_acctype,p_payment_accnumber,
		p_payment_benificiaryname,p_entity_gid,p_create_by;
		if finished_supplierpayment = 1 then
			leave atma_looopsupplierpayment;
		End if;
		set @partner_ref_gid_supp_payment='';
			select fn_REFGid('SUPPLIER_PAYMENT')into @partner_ref_gid_supp_payment;
		set Query_Update='';
		set Query_Update = concat('INSERT INTO gal_trn_tbankdetails (bankdetails_ref_gid,bankdetails_reftable_gid,
								bankdetails_reftable_code,bankdetails_paymode_gid,
								bankdetails_bank_gid,bankdetails_bankbranch_gid,bankdetails_acno,
                                bankdetails_beneficiaryname,entity_gid,create_by,create_date)
			values (',@partner_ref_gid_supp_payment,',',@suppliergid,',''',p_partnerbranch_code,''',',p_payment_paymodegid,',
					',p_payment_bankgid,',''',p_payment_bankbranchgid,''',
					''',ifnull(p_payment_accnumber,''),''',''',ifnull(p_payment_benificiaryname,''),''',
					',p_entity_gid,',',p_create_by,',
				  ''',Now(),''')');
        set @Insert_query = Query_Update;
		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'SUCCESS';
		else
			set Message = ' FAILED supplier payment';
			rollback;
			leave sp_Atma_Pending_To_Approval_Set;
		end if;
		End loop atma_looopsupplierpayment;
		close Cursor_atma_supplierpayment;
		end;
		#####paymentDetails close
		### gal_trn_tcreditlimit###open##
		set Query_Update='';
		set Query_Update = concat('INSERT INTO gal_trn_tcreditlimit (creditlimit_ref_gid,creditlimit_reftable_gid,
									creditlimit_reftable_code,
                                    creditlimit_limit,
									creditlimit_days,
									creditlimit_creditterms,
                                    creditlimit_validfrom,creditlimit_validto,
                                    entity_gid,create_by,create_date)
			values (',@partner_ref_gid_supp_payment,',',@suppliergid,',
					''',p_partnerbranch_code,''',
                    ''',p_partnerbranch_creditlimit,''',
					''',p_partnerbranch_creditperiod,''',
                    ''',ifnull(p_partnerbranch_paymentterms,''),''',
					',if(ifnull(@partner_contractdatefrom,null) IS NULL,'NULL',CONCAT('''',@partner_contractdatefrom,'''')),',
					',if(ifnull(@partner_contractdateto,null) IS NULL,'NULL',CONCAT('''',@partner_contractdateto,'''')),',
					',p_entity_gid,',',p_create_by,',
					''',Now(),''')');

        set @Insert_query = Query_Update;
		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'SUCCESS';
		else
			set Message = ' FAILED supplier creditlimit ';
			rollback;
			leave sp_Atma_Pending_To_Approval_Set;
		end if;

	else
		set Message = 'Failed On Supplier Insert1';
		rollback;
		leave sp_Atma_Pending_To_Approval_Set;
	end if;#if @Supplier_msg = 'SUCCESS' then

	End loop atma_looop1;
	close Cursor_atma1;
	end;
else
	rollback;
	leave sp_Atma_Pending_To_Approval_Set;
end if;#if @out_msg_suppgroup='SUCCESS' then

if @out_msg_suppgroup='SUCCESS' and @Supplier_msg = 'SUCCESS' then
	#rollback;
	commit;
else
	rollback;
	leave sp_Atma_Pending_To_Approval_Set;
end if;
END IF;#IF li_Action='Pending_To_Approval_Insert' then


END