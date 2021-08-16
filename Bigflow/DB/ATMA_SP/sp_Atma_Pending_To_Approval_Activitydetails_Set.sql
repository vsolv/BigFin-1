CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Pending_To_Approval_Activitydetails_Set`(in li_Action  varchar(30),
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_Atma_Pending_To_Approval_Activitydetails_Set:BEGIN
declare Query_Insert varchar(10000);
Declare countRow varchar(6000);
declare Query_Update varchar(10000);
declare Query_delete varchar(1000);
declare Query_Value varchar(1000);
declare Query_Column varchar(1000);
Declare ad_activitydetails_gid,ad_activitydetails_activitygid,ad_activitydetails_code,ad_activitydetails_name,
			ad_activitydetails_remarks,ad_activitydetails_raisor,ad_activitydetails_approver,ad_activitydetails_isactive,
			ad_activitydetails_isremoved,ad_entity_gid,ad_create_by,ad_update_by,ad_update_date,
            ad_main_activitydetails_gid varchar(150);

DECLARE finished INTEGER DEFAULT 0;
Declare errno int;
Declare msg varchar(1000);

						DECLARE EXIT HANDLER FOR SQLEXCEPTION
						BEGIN
							GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
							set Message = concat(errno , msg);
							ROLLBACK;
						END;

IF li_Action='Insert' then



	select JSON_LENGTH(lj_filter,'$') into @lj_filter_json_count;
	select JSON_LENGTH(lj_classification,'$') into @lj_classification_json_count;

	if @lj_filter_json_count = 0 or @lj_filter_json_count is null then
		set Message = 'No Data In filter Json. ';
		leave sp_Atma_Pending_To_Approval_Activitydetails_Set;
	End if;

	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Gid')))
	into @Partner_Gid;



	if @Partner_Gid = '' or @Partner_Gid is null  or @Partner_Gid=0 then
			set Message = 'Partner Is Not Provided';
			leave sp_Atma_Pending_To_Approval_Activitydetails_Set;
	End if;

	set @Main_partner_gid=4;
      #SET finished =0;
BEGIN
	Declare Cursor_atma CURSOR FOR

			select ad.activitydetails_gid,ad.activitydetails_activitygid,ad.activitydetails_code,ad.activitydetails_name,ad.activitydetails_remarks,
			ad.activitydetails_raisor,ad.activitydetails_approver,ad.activitydetails_isactive,ad.activitydetails_isremoved,ad.entity_gid,ad.create_by,ad.update_by,ad.update_date,
            ad.main_activitydetails_gid
			 from atma_tmp_mst_tactivity a inner join atma_tmp_mst_tactivitydetails ad on a.activity_gid=ad.activitydetails_activitygid
            where activity_partnergid=@Partner_Gid ;

	DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;
	OPEN Cursor_atma;
	atma_looop:loop
		fetch Cursor_atma into ad_activitydetails_gid,ad_activitydetails_activitygid,ad_activitydetails_code,ad_activitydetails_name,
			ad_activitydetails_remarks,ad_activitydetails_raisor,ad_activitydetails_approver,ad_activitydetails_isactive,
			ad_activitydetails_isremoved,ad_entity_gid,ad_create_by,ad_update_by,ad_update_date,
            ad_main_activitydetails_gid;
	 if finished = 1 then
			leave atma_looop;
		End if;
	if ad_main_activitydetails_gid = '' or ad_main_activitydetails_gid is null  or ad_main_activitydetails_gid=0 then
			set Query_Update = concat('INSERT INTO atma_mst_tactivitydetails (activitydetails_activitygid,activitydetails_code,activitydetails_name,activitydetails_remarks,activitydetails_raisor,
			activitydetails_approver,activitydetails_isactive,activitydetails_isremoved,entity_gid,create_by)
            values (',ad_activitydetails_activitygid,',''',ad_activitydetails_code,''',''',ad_activitydetails_name,''',
            ''',ad_activitydetails_remarks,''',''',ad_activitydetails_raisor,''',''',ad_activitydetails_approver,''',
            ''',ad_activitydetails_isactive,''',''',ad_activitydetails_isremoved,''',',ad_entity_gid,',
            ',ad_create_by,')');

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
			leave sp_Atma_Pending_To_Approval_Activitydetails_Set;
			end if;

	else

		 	set Query_Update = concat('Update atma_mst_tactivitydetails  set
            activitydetails_activitygid=',ad_activitydetails_activitygid,',activitydetails_name=''',ad_activitydetails_name,'''
            ,activitydetails_remarks=''',ad_activitydetails_remarks,''',
            activitydetails_raisor=',ad_activitydetails_raisor,',activitydetails_approver=''',ad_activitydetails_approver,''',
			update_by=',ad_update_by,',update_date=''',Now(),'''
			where activitydetails_gid=',ad_main_activitydetails_gid,'');

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
			leave sp_Atma_Pending_To_Approval_Activitydetails_Set;
			end if;

	end if;
       # select Query_Update;
		set @Insert_query = Query_Update;
		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'SUCCESS';
		else
			set Message = ' FAILED';
			leave sp_Atma_Pending_To_Approval_Activitydetails_Set;
		end if;
	End loop atma_looop;
	close Cursor_atma;
	end;  #Endof Cursor


End if;

END
3