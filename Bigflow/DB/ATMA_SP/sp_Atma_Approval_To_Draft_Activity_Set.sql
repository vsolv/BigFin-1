CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Approval_To_Draft_Activity_Set`(in li_Action  varchar(30),
in lj_filter json,in Partner_Gid int,in Newpartnerbranchgid int,in Oldpartnerbranch_gid int,
in lj_classification json,out Message varchar(1000))
sp_Atma_Approval_To_Draft_Activity_Set:BEGIN
Declare Query_Insert varchar(10000);
Declare countRow varchar(6000);
Declare Query_Update varchar(10000);
Declare Query_delete varchar(1000);
Declare Query_Value varchar(1000);
Declare Query_Column varchar(1000);
Declare a_activity_gid,a_activity_partnergid,a_activity_code,a_activity_partnercode,a_activity_partnerbranchgid,a_activity_type,a_activity_name,
		a_activity_desc,a_activity_startdate,a_activity_enddate,a_activity_projectedspend,a_activity_rm,a_activity_contactgid,
		a_activity_fidiinsur,a_activity_bidding,a_activity_reason,a_activity_status,a_activity_isactive,a_activity_isremoved,
		a_entity_gid,a_create_by,a_create_date varchar(150);
Declare c_contact_gid,c_Contact_ref_gid,c_Contact_reftable_gid,c_contact_reftablecode,c_Contact_contacttype_gid,
		c_Contact_personname,c_Contact_designation_gid,c_Contact_landline,c_Contact_landline2,c_Contact_mobileno,
		c_Contact_mobileno2,c_Contact_email,c_Contact_DOB,c_Contact_WD,c_entity_gid,c_create_by,c_create_date varchar(150);
Declare ad_activitydetails_gid,ad_activitydetails_activitygid,ad_activitydetails_code,ad_activitydetails_name,
		ad_activitydetails_remarks,ad_activitydetails_raisor,ad_activitydetails_approver,ad_activitydetails_isactive,
		ad_activitydetails_isremoved,ad_entity_gid,ad_create_by,ad_create_date varchar(150);

DECLARE finished INTEGER DEFAULT 0;
DECLARE finished1 INTEGER DEFAULT 0;
Declare errno int;
Declare msg,Error_Level varchar(1000);

DECLARE EXIT HANDLER FOR SQLEXCEPTION
BEGIN
	GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
	set Message = concat(Error_Level,' : No-',errno , msg);
	ROLLBACK;
END;

 IF li_Action='insert' then

						select JSON_LENGTH(lj_filter,'$') into @lj_filter_json_count;
						select JSON_LENGTH(lj_classification,'$') into @lj_classification_json_count;

						if @lj_filter_json_count = 0 or @lj_filter_json_count is null then
						set Message = 'No Data In filter Json. ';
						leave sp_Atma_Approval_To_Draft_Activity_Set;
						End if;

						select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Gid')))
						into @Partner_Gid;


 SET finished =0;


BEGIN

		Declare Cursor_atma CURSOR FOR

						select activity_gid,activity_partnergid,activity_code,activity_partnercode,activity_partnerbranchgid,activity_type,activity_name,
						activity_desc,activity_startdate,activity_enddate,activity_projectedspend,activity_rm,activity_contactgid,
						activity_fidiinsur,activity_bidding,activity_reason,activity_status,activity_isactive,activity_isremoved,
						entity_gid,create_by,create_date
						from atma_mst_tactivity where activity_partnergid=@Partner_Gid
                        and activity_partnerbranchgid=Oldpartnerbranch_gid;

		DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;

		OPEN Cursor_atma;
		atma_looop:loop
						fetch Cursor_atma into a_activity_gid,a_activity_partnergid,a_activity_code,a_activity_partnercode,a_activity_partnerbranchgid,a_activity_type,a_activity_name,
						a_activity_desc,a_activity_startdate,a_activity_enddate,a_activity_projectedspend,a_activity_rm,a_activity_contactgid,
						a_activity_fidiinsur,a_activity_bidding,a_activity_reason,a_activity_status,a_activity_isactive,a_activity_isremoved,
						a_entity_gid,a_create_by,a_create_date;

		if finished = 1 then
		leave atma_looop;
		End if;
						select contact_gid,Contact_ref_gid,Contact_reftable_gid,contact_reftablecode,Contact_contacttype_gid,Contact_personname,
						Contact_designation_gid,Contact_landline,Contact_landline2,Contact_mobileno,Contact_mobileno2,Contact_email,Contact_DOB,Contact_WD,
						entity_gid,create_by into @contact_gid,@Contact_ref_gid,@Contact_reftable_gid,@contact_reftablecode,@Contact_contacttype_gid,@Contact_personname,
						@Contact_designation_gid,@Contact_landline,@Contact_landline2,@Contact_mobileno,@Contact_mobileno2,@Contact_email,@Contact_DOB,@Contact_WD,
						@entity_gid,@create_by  from gal_mst_tcontact
						where contact_gid=a_activity_contactgid ;

    	set Error_Level='ATMA8.1';
		set Query_Insert = CONCAT('INSERT INTO atma_tmp_mst_tcontact (Contact_ref_gid,Contact_reftable_gid,contact_reftablecode,Contact_contacttype_gid,Contact_personname,Contact_designation_gid,
							Contact_landline,Contact_landline2,Contact_mobileno,Contact_mobileno2,Contact_email,Contact_DOB,Contact_WD,entity_gid,create_by,main_contact_gid)values
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
							',@create_by,',
							',@contact_gid,'
							)');



			set @Insert_query = Query_Insert;
			PREPARE stmt FROM @Insert_query;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;
			if countRow >  0 then
			set Message = 'SUCCESS';
			else
			set Message = ' FAILED ACT_CONTACT';
			leave sp_Atma_Approval_To_Draft_Activity_Set;
			end if;
            set @activity_contactgid='';
            select last_insert_id() into @activity_contactgid;


			set Error_Level='ATMA8.2';
			set Query_Insert = concat('INSERT INTO atma_tmp_mst_tactivity (activity_partnergid,activity_code,
            activity_partnercode,activity_partnerbranchgid,activity_type,activity_name,activity_desc,activity_startdate,
			activity_enddate,activity_projectedspend,activity_rm,activity_contactgid,activity_fidiinsur,
            activity_bidding,activity_reason, activity_status,activity_isactive,activity_isremoved,entity_gid,create_by,
            create_date,main_activity_gid)values (',Partner_Gid,',''',a_activity_code,''',''',a_activity_partnercode,''',
            ',Newpartnerbranchgid,',
            ''',a_activity_type,''',''',a_activity_name,''',''',a_activity_desc,''',
            ''',a_activity_startdate,''',''',a_activity_enddate,''',',a_activity_projectedspend,',',a_activity_rm,',
            ',@activity_contactgid,',''',a_activity_fidiinsur,''',''',a_activity_bidding,''',''',ifnull(a_activity_reason,''),''',''',a_activity_status,''',''',a_activity_isactive,''',''',a_activity_isremoved,''',',a_entity_gid,',
            ',a_create_by,',''',a_create_date,''',',a_activity_gid,')');


			set @Insert_query = Query_Insert;
			PREPARE stmt FROM @Insert_query;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;
			if countRow >  0 then
			set Message = 'SUCCESS';
			else
			set Message = ' FAILED ACTIVITY';
			leave sp_Atma_Approval_To_Draft_Activity_Set;
			end if;
            set @activitydetails_activitygid='';
            select last_insert_id() into @activitydetails_activitygid;
 SET finished1 =0;
	BEGIN

		Declare Cursor_atma1 CURSOR FOR

					select activitydetails_gid,activitydetails_activitygid,activitydetails_code,activitydetails_name,activitydetails_remarks,
					activitydetails_raisor,activitydetails_approver,activitydetails_isactive,activitydetails_isremoved,entity_gid,create_by,create_date
					from  atma_mst_tactivitydetails
					where activitydetails_activitygid=a_activity_gid ;

		DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished1 = 1;

		OPEN Cursor_atma1;
		atma_looop1:loop
					fetch Cursor_atma1 into ad_activitydetails_gid,ad_activitydetails_activitygid,ad_activitydetails_code,ad_activitydetails_name,
					ad_activitydetails_remarks,ad_activitydetails_raisor,ad_activitydetails_approver,ad_activitydetails_isactive,
					ad_activitydetails_isremoved,ad_entity_gid,ad_create_by,ad_create_date ;

		if finished1 = 1 then
			leave atma_looop1;
		End if;
		set Error_Level='ATMA8.3';
		set Query_Insert = concat('INSERT INTO atma_tmp_mst_tactivitydetails (activitydetails_activitygid,activitydetails_code,activitydetails_name,activitydetails_remarks,activitydetails_raisor,
							activitydetails_approver,activitydetails_isactive,activitydetails_isremoved,entity_gid,create_by,create_date,main_activitydetails_gid)
							values (',@activitydetails_activitygid,',''',ad_activitydetails_code,''',''',ad_activitydetails_name,''',
							''',ifnull(ad_activitydetails_remarks,''),''',''',ad_activitydetails_raisor,''',''',ad_activitydetails_approver,''',
							''',ad_activitydetails_isactive,''',''',ad_activitydetails_isremoved,''',',ad_entity_gid,',
							',ad_create_by,',''',ad_create_date,''',',ad_activitydetails_gid,')');


			set @Insert_query = Query_Insert;
			PREPARE stmt FROM @Insert_query;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;
			if countRow >  0 then
			set Message = 'SUCCESS';
			else
			set Message = ' FAILED ACT_DET';
			leave sp_Atma_Approval_To_Draft_Activity_Set;
			end if;
End loop atma_looop1;
close Cursor_atma1;
end;

      set  @Mst_activitydetails='';
        select last_insert_id() into @Mst_activitydetails;

End loop atma_looop;
close Cursor_atma;
end;

call sp_Atma_Approval_To_Draft_Activitydtlpproduct_Set('Insert',lj_filter,Partner_Gid,@Mst_activitydetails,
Newpartnerbranchgid,Oldpartnerbranch_gid,lj_classification,@Message);
			select @Message into @Out_Message_Activitydtlpproduct;

			if  @Out_Message_Activitydtlpproduct <> 'SUCCESS' then
					set Message = @Out_Message_Activitydtlpproduct;

					leave sp_Atma_Approval_To_Draft_Activity_Set;
			End if;
			set Message ='SUCCESS';


 END IF;

END