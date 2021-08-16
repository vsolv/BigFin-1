CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Pending_To_Approval_Activity_Set`(in li_Action  varchar(30),
in lj_filter json,in Partner_Gid int,in lj_classification json,out Message varchar(1000))
sp_Atma_Pending_To_Approval_Activity_Set:BEGIN
declare Query_Insert varchar(10000);
Declare countRow varchar(6000);
declare Query_Update varchar(10000);
declare Query_delete varchar(1000);
declare Query_Value varchar(1000);
declare Query_Column varchar(1000);

Declare a_activity_gid,a_activity_partnergid,a_activity_code,a_activity_partnercode,a_activity_partnerbranchgid,a_activity_type,a_activity_name,
		a_activity_desc,a_activity_startdate,a_activity_enddate,a_activity_projectedspend,a_activity_rm,a_activity_contactgid,
		a_activity_fidiinsur,a_activity_bidding,a_activity_reason,a_activity_status,a_activity_isactive,a_activity_isremoved,
		a_entity_gid,a_create_by,a_update_by,a_main_activity_gid varchar(150);
Declare ad_activitydetails_gid,ad_activitydetails_activitygid,ad_activitydetails_code,ad_activitydetails_name,
		ad_activitydetails_remarks,ad_activitydetails_raisor,ad_activitydetails_approver,ad_activitydetails_isactive,
		ad_activitydetails_isremoved,ad_entity_gid,ad_create_by,ad_update_by,ad_update_date,
		ad_main_activitydetails_gid varchar(150);
DECLARE finished INTEGER DEFAULT 0;
DECLARE finished1 INTEGER DEFAULT 0;

Declare errno int;
Declare msg,Error_Level varchar(1000);

DECLARE EXIT HANDLER FOR SQLEXCEPTION
BEGIN
	GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
	set Message = concat(Error_Level,' :No-',errno,msg);
	ROLLBACK;
END;
#start transaction;
IF li_Action='Insert' then
	select JSON_LENGTH(lj_filter,'$') into @lj_filter_json_count;
	select JSON_LENGTH(lj_classification,'$') into @lj_classification_json_count;

	if @lj_filter_json_count = 0 or @lj_filter_json_count is null then
		set Message = 'No Data In filter Json. ';
		leave sp_Atma_Pending_To_Approval_Activity_Set;
	End if;

	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Gid'))) into @Partner_Gid;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Update_By'))) into @Update_By2;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.newpartnerbranchgid')))
    into @newpartnerbranchgid;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.oldpartnerbranchgid')))
    into @oldpartnerbranchgid;

SET finished =0;
BEGIN
	Declare Cursor_atma CURSOR FOR

	select activity_gid,activity_partnergid,activity_code,activity_partnercode,activity_partnerbranchgid,activity_type,
    activity_name,activity_desc,activity_startdate,activity_enddate,activity_projectedspend,activity_rm,
    activity_contactgid,activity_fidiinsur,activity_bidding,activity_reason,activity_status,activity_isactive,
    activity_isremoved,entity_gid,create_by,update_by,main_activity_gid
	from atma_tmp_mst_tactivity where activity_partnergid=@Partner_Gid
	and activity_partnerbranchgid=@oldpartnerbranchgid;

	DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;
	OPEN Cursor_atma;
	atma_looop:loop

	fetch Cursor_atma into a_activity_gid,a_activity_partnergid,a_activity_code,a_activity_partnercode,
    a_activity_partnerbranchgid,a_activity_type,a_activity_name,a_activity_desc,a_activity_startdate,
    a_activity_enddate,a_activity_projectedspend,a_activity_rm,a_activity_contactgid,
	a_activity_fidiinsur,a_activity_bidding,a_activity_reason,a_activity_status,a_activity_isactive,
    a_activity_isremoved,a_entity_gid,a_create_by,a_update_by,a_main_activity_gid;

	if finished = 1 then
		leave atma_looop;
	End if;

	select contact_gid,Contact_ref_gid,Contact_reftable_gid,contact_reftablecode,Contact_contacttype_gid,Contact_personname,
	Contact_designation_gid,Contact_landline,Contact_landline2,Contact_mobileno,Contact_mobileno2,Contact_email,Contact_DOB,Contact_WD,
	entity_gid,create_by,update_by,main_contact_gid into @contact_gid,@Contact_ref_gid,@Contact_reftable_gid,@contact_reftablecode,@Contact_contacttype_gid,@Contact_personname,
	@Contact_designation_gid,@Contact_landline,@Contact_landline2,@Contact_mobileno,@Contact_mobileno2,@Contact_email,@Contact_DOB,@Contact_WD,
	@entity_gid,@create_by,@update_by,@main_contact_gid  from atma_tmp_mst_tcontact
	where contact_gid=a_activity_contactgid ;

	set  @activity_contactgid='';
	#select @main_contact_gid;
	if @main_contact_gid = '' or @main_contact_gid is null  or @main_contact_gid=0 then
		set Error_Level='ATMA49.1';
   		set Query_Update = CONCAT('INSERT INTO gal_mst_tcontact (Contact_ref_gid,Contact_reftable_gid,
        contact_reftablecode,Contact_contacttype_gid,Contact_personname,Contact_designation_gid,
		Contact_landline,Contact_landline2,Contact_mobileno,Contact_mobileno2,Contact_email,Contact_DOB,Contact_WD,
        entity_gid,create_by)values
            (',@Contact_ref_gid,',
            ''',@Contact_reftable_gid,''',
            ''',@contact_reftablecode,''',
            ',@Contact_contacttype_gid,',
            ''',ifnull(@Contact_personname,''),''',
            ',@Contact_designation_gid,',
            ''',ifnull(@Contact_landline,''),''',
            ''',ifnull(@Contact_landline2,''),''',
            ''',ifnull(@Contact_mobileno,''),''',
			''',ifnull(@Contact_mobileno2,''),''',
            ''',ifnull(@Contact_email,''),''',
             ',if(ifnull(@Contact_DOB,null) IS NULL,'NULL',CONCAT('''',@Contact_DOB,'''')),',
             ',if(ifnull(@Contact_WD,null) IS NULL,'NULL',CONCAT('''',@Contact_WD,'''')),',
            ',@entity_gid,',
            ',@create_by,'
            )');

		SET SQL_SAFE_UPDATES = 0;
		set Query_delete=concat('DELETE FROM atma_tmp_mst_tcontact WHERE contact_gid=',@contact_gid,'');
		set @Insert_query = Query_delete;
		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
				set Message = 'DELETED';
		else
				set Message = ' FAILED DELETION';
				leave sp_Atma_Pending_To_Approval_Activity_Set;
		end if;
	else
		set Error_Level='ATMA49.2';
		set Query_Update = concat('Update gal_mst_tcontact  set
            Contact_contacttype_gid=',@Contact_contacttype_gid,',
            Contact_personname=''',ifnull(@Contact_personname,''),''',
            Contact_designation_gid=',@Contact_designation_gid,',
            Contact_landline=''',ifnull(@Contact_landline,''),''',
            Contact_landline2=''',ifnull(@Contact_landline2,''),''',
            Contact_mobileno=''',ifnull(@Contact_mobileno,''),''',
            Contact_mobileno2= ''',ifnull(@Contact_mobileno2,''),''',
            Contact_email=''',ifnull(@Contact_email,''),''',
			Contact_DOB=',if(ifnull(@Contact_DOB,null) IS NULL,'NULL',CONCAT('''',@Contact_DOB,'''')),',
			Contact_WD=',if(ifnull(@Contact_WD,null) IS NULL,'NULL',CONCAT('''',@Contact_WD,'''')),',
			update_by=',@Update_By2,',
            update_date=''',now(),'''
			where
			contact_gid=',@main_contact_gid,'');

		SET SQL_SAFE_UPDATES = 0;
		set Query_delete=concat('DELETE FROM atma_tmp_mst_tcontact WHERE contact_gid=',@contact_gid,'');
		set @Insert_query = Query_delete;
		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'DELETED';
		else
			set Message = ' FAILED DELETION';
			leave sp_Atma_Pending_To_Approval_Activity_Set;
		end if;
end if;
		#SELECT Query_Update,1;
		set @Insert_query = Query_Update;
		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
		set Message = 'SUCCESS';
		#rollback;#remove
		else
		set Message = ' FAILED_CONT';
		leave sp_Atma_Pending_To_Approval_Activity_Set;
		end if;
		#set @activity_contactgid='';
		select last_insert_id() into @activity_contactgid;

if a_main_activity_gid = '' or a_main_activity_gid is null  or a_main_activity_gid=0 then

	set Query_Column='';
	set Query_Value ='';
	if a_activity_reason is not null then
		set Query_Column = concat(Query_Column,',activity_reason ');
		set Query_Value=concat(Query_Value,', ''',a_activity_reason,''' ');
	else
		set Query_Column = concat('');
		set Query_Value=concat('');
	end if;

	set Error_Level='ATMA49.2';
	set Query_Update = concat('INSERT INTO atma_mst_tactivity ( activity_partnergid,activity_code,
    activity_partnercode,activity_partnerbranchgid,activity_type,activity_name,activity_desc,activity_startdate,
    activity_enddate,activity_projectedspend,activity_rm,activity_contactgid,activity_fidiinsur,activity_bidding,
    activity_status,activity_isactive,activity_isremoved,entity_gid,create_by ',Query_Column,')values
    (',Partner_Gid,',''',a_activity_code,''',''',a_activity_partnercode,''',
            ',@newpartnerbranchgid,',
            ''',a_activity_type,''',''',a_activity_name,''',''',a_activity_desc,''',''',
            a_activity_startdate,''',''',a_activity_enddate,''',''',a_activity_projectedspend,''',
			',a_activity_rm,',',@activity_contactgid,',''',a_activity_fidiinsur,''',''',a_activity_bidding,'''
            ,''',a_activity_status,''',''',a_activity_isactive,''',''',a_activity_isremoved,''',
            ',a_entity_gid,',',a_create_by,' ',Query_Value,')');


	SET SQL_SAFE_UPDATES = 0;
	set Query_delete=concat('DELETE FROM atma_tmp_mst_tactivity WHERE activity_gid=',a_activity_gid,'');
	set @Insert_query = Query_delete;
	PREPARE stmt FROM @Insert_query;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
	if countRow >  0 then
		set Message = 'DELETED';
	else
		set Message = ' FAILED DELETION';
		leave sp_Atma_Pending_To_Approval_Activity_Set;
	end if;

else
	set Error_Level='ATMA49.3';
	set Query_Update = concat('Update atma_mst_tactivity  set
            activity_type=''',a_activity_type,''',
            activity_name=''',a_activity_name,''',
            activity_desc=''',a_activity_desc,''',
            activity_startdate=''',a_activity_startdate,''',
            activity_enddate=''',a_activity_enddate,''',
            activity_projectedspend=''',a_activity_projectedspend,''',
            activity_rm= ',a_activity_rm,',
			activity_fidiinsur=''',a_activity_fidiinsur,''',
			activity_bidding=''',a_activity_bidding,''',
			activity_reason=''',ifnull(a_activity_reason,''),''',
			activity_status=''',a_activity_status,''',
            update_by=',@Update_By2,',
            update_date=''',now(),'''
			where
			activity_gid=',a_main_activity_gid,'');

           #SELECT Query_Update,2;

			SET SQL_SAFE_UPDATES = 0;
			set Query_delete=concat('DELETE FROM atma_tmp_mst_tactivity WHERE activity_gid=',a_activity_gid,'');
			set @Insert_query = Query_delete;
			PREPARE stmt FROM @Insert_query;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;
			if countRow >  0 then
			set Message = 'DELETED';
			else
			set Message = ' FAILED DELETION';
			leave sp_Atma_Pending_To_Approval_Activity_Set;
			end if;

end if;
	#select Query_Update;
	set @Insert_query = Query_Update;
	PREPARE stmt FROM @Insert_query;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
	if countRow >  0 then
		set Message = 'SUCCESS';
		#rollback;
		#commit;
		#leave sp_Atma_Pending_To_Approval_Activity_Set;
	else
		set Message = ' FAILED_ACT';
		leave sp_Atma_Pending_To_Approval_Activity_Set;
	end if;

	set  @Mst_activitygid='';
	select last_insert_id() into @Mst_activitygid;
	#select 'new Activitygid',  @Mst_activitygid, ' old ',a_activity_gid;

SET finished1 =0;
BEGIN
Declare ActivityCursor_atma CURSOR FOR

	select activitydetails_gid,activitydetails_activitygid,activitydetails_code,activitydetails_name,activitydetails_remarks,
	activitydetails_raisor,activitydetails_approver,activitydetails_isactive,activitydetails_isremoved,entity_gid,create_by,update_by,update_date,
	main_activitydetails_gid
	from  atma_tmp_mst_tactivitydetails
	where activitydetails_activitygid=a_activity_gid ;

	DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished1 = 1;
	OPEN ActivityCursor_atma;
	atma_Activityloop:loop
		fetch ActivityCursor_atma into ad_activitydetails_gid,ad_activitydetails_activitygid,ad_activitydetails_code,ad_activitydetails_name,
			ad_activitydetails_remarks,ad_activitydetails_raisor,ad_activitydetails_approver,ad_activitydetails_isactive,
			ad_activitydetails_isremoved,ad_entity_gid,ad_create_by,ad_update_by,ad_update_date,
            ad_main_activitydetails_gid;


	if finished1 = 1 then
			leave atma_Activityloop;
	End if;

	if ad_main_activitydetails_gid = '' or ad_main_activitydetails_gid is null  or ad_main_activitydetails_gid=0 then
		set Query_Column='';
		set Query_Value ='';

		if ad_activitydetails_remarks is not null then
			set Query_Column = concat(Query_Column,',activitydetails_remarks ');
			set Query_Value=concat(Query_Value,', ''',ad_activitydetails_remarks,''' ');
		else
			set Query_Column = concat('');
			set Query_Value=concat('');
		end if;
    	set Error_Level='ATMA49.4';
		set Query_Update = concat('INSERT INTO atma_mst_tactivitydetails (activitydetails_activitygid,
        activitydetails_code,activitydetails_name,activitydetails_raisor,activitydetails_approver,
        activitydetails_isactive,activitydetails_isremoved,entity_gid,create_by',Query_Column,')
            values (',@Mst_activitygid,',''',ad_activitydetails_code,''',''',ad_activitydetails_name,''',
            ''',ad_activitydetails_raisor,''',''',ad_activitydetails_approver,''',
            ''',ad_activitydetails_isactive,''',''',ad_activitydetails_isremoved,''',',ad_entity_gid,',
            ',ad_create_by,'',Query_Value,')');

			#select main_activitydetails_gid from atma_tmp_mst_tactivitydetails where
           # activitydetails_code=ad_activitydetails_code
			#into @main;
		#select Query_Update,'details';
		SET SQL_SAFE_UPDATES = 0;
		set Query_delete=concat('DELETE FROM atma_tmp_mst_tactivitydetails WHERE activitydetails_gid=',ad_activitydetails_gid,'');
		set @Insert_query = Query_delete;
		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'DELETED';
		else
			set Message = ' FAILED DELETION';
			leave sp_Atma_Pending_To_Approval_Activity_Set;
		end if;
else

		set Error_Level='ATMA49.5';
        set Query_Update = concat('Update atma_mst_tactivitydetails  set
            activitydetails_name=''',ad_activitydetails_name,'''
            ,activitydetails_remarks=''',ifnull(ad_activitydetails_remarks,''),''',
            activitydetails_raisor=',ad_activitydetails_raisor,',
            activitydetails_approver=',ad_activitydetails_approver,',
			update_by=',@Update_By2,',
            update_date=''',Now(),'''
			where activitydetails_gid=',ad_main_activitydetails_gid,'');


        #SELECT Query_Update,2;
		SET SQL_SAFE_UPDATES = 0;
		set Query_delete=concat('DELETE FROM atma_tmp_mst_tactivitydetails WHERE activitydetails_gid=',ad_activitydetails_gid,'');
		set @Insert_query = Query_delete;
		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'DELETED';
		else
			set Message = ' FAILED DELETION ACTD';
			leave sp_Atma_Pending_To_Approval_Activity_Set;
		end if;

end if;
       #select Query_Update;
		set @Insert_query = Query_Update;
		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'SUCCESS ';
           # select Message,1;
		else
			set Message = ' FAILED_ad';
			#rollback;
			leave sp_Atma_Pending_To_Approval_Activity_Set;
		end if;


    set @Mst_activitydetails='';
    select last_insert_id() into @Mst_activitydetails;

   # SELECT 'new activity detail gid',@Mst_activitydetails, ' old ',ad_activitydetails_gid;
	select activitydetails_gid from atma_mst_tactivitydetails where activitydetails_code=ad_activitydetails_code
			into @mainactivitydetails;

  # select @mainactivitydetails,'164';
     if @Mst_activitydetails = 0 or @Mst_activitydetails is null  then
     set @Mst_activitydetails=@mainactivitydetails;
     end if;
    #select @Mst_activitydetails,'in';
    set Error_Level='ATMA49.6';
	call sp_Atma_Pending_To_Approval_Activitydtlpproduct_Set('Insert',lj_filter,Partner_Gid,@Mst_activitydetails,
        @newpartnerbranchgid,@oldpartnerbranchgid,ad_activitydetails_gid,lj_classification,@Message);
	select @Message into @Out_Message_Activitydtlpproduct;
	#if  @Out_Message_Activitydtlpproduct is null then
		#rollback;
		#leave sp_Atma_Pending_To_Approval_Activity_Set;
	#end if;
	if  @Out_Message_Activitydtlpproduct <> 'SUCCESS' then
		set Message = @Out_Message_Activitydtlpproduct;
		#rollback;
		leave sp_Atma_Pending_To_Approval_Activity_Set;
	else
		select 'Out_Msg_Activitydtlpproduct',@Out_Message_Activitydtlpproduct;
	End if;

	End loop atma_Activityloop;
	close ActivityCursor_atma;
	end;

End loop atma_looop;
	close Cursor_atma;
	end;
 #   rollback;
  #  leave sp_Atma_Pending_To_Approval_Activity_Set;

End if;

END