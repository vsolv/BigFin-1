CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Pending_To_Approval_payment_Set`(in li_Action  varchar(30),
in lj_filter json,in Partner_Gid int,in lj_classification json,out Message varchar(1000))
sp_Atma_Pending_To_Approval_payment_Set:BEGIN
declare Query_Insert varchar(10000);
Declare countRow varchar(6000);
declare Query_Update varchar(10000);
declare Query_delete varchar(1000);
declare Query_Value varchar(1000);
declare Query_Column varchar(1000);
Declare p_payment_gid,p_payment_partnergid,p_payment_partnerbranchgid,p_payment_paymodegid,p_payment_bankgid,p_payment_bankbranchgid,p_payment_acctype,p_payment_accnumber,
		p_payment_benificiaryname,p_payment_remarks,p_payment_isactive,p_payment_isremoved,p_entity_gid,p_create_by,p_create_date,p_update_by,p_main_payment_gid varchar(150);
DECLARE finished INTEGER DEFAULT 0;
Declare errno int;
Declare msg,Error_Level varchar(1000);

						DECLARE EXIT HANDLER FOR SQLEXCEPTION
						BEGIN
							GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
							set Message = concat(Error_Level,':No-',errno,msg);
							ROLLBACK;
						END;

IF li_Action='Insert' then


	select JSON_LENGTH(lj_filter,'$') into @lj_filter_json_count;
	select JSON_LENGTH(lj_classification,'$') into @lj_classification_json_count;

	if @lj_filter_json_count = 0 or @lj_filter_json_count is null then
		set Message = 'No Data In filter Json. ';
		leave sp_Atma_Pending_To_Approval_payment_Set;
	End if;

	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Gid')))
	into @Partner_Gid_tmp;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.newpartnerbranchgid')))
    into @newpartnerbranchgid;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.oldpartnerbranchgid')))
    into @oldpartnerbranchgid;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Update_By')))
    into @Update_By;
    #select @newpartnerbranchgid,@oldpartnerbranchgid,@Partner_Gid_tmp;

	if @Partner_Gid_tmp = '' or @Partner_Gid_tmp is null  or @Partner_Gid_tmp=0 then
			set Message = 'Partner Is Not Provided';
			leave sp_Atma_Pending_To_Approval_payment_Set;
	End if;



BEGIN
	Declare Cursor_atma CURSOR FOR

	select payment_gid,payment_partnergid,payment_partnerbranchgid,payment_paymodegid,payment_bankgid,
    payment_bankbranchgid,payment_acctype,payment_accnumber,payment_benificiaryname,payment_remarks,
    payment_isactive,payment_isremoved,entity_gid,create_by,create_date,update_by,	main_payment_gid
	from atma_tmp_mst_tpayment where payment_partnergid=@Partner_Gid_tmp
    and payment_partnerbranchgid=@oldpartnerbranchgid ;

	DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;
	OPEN Cursor_atma;
	atma_looop:loop
		fetch Cursor_atma into p_payment_gid,p_payment_partnergid,p_payment_partnerbranchgid,p_payment_paymodegid,
        p_payment_bankgid,p_payment_bankbranchgid,p_payment_acctype,p_payment_accnumber,
		p_payment_benificiaryname,p_payment_remarks,p_payment_isactive,p_payment_isremoved,p_entity_gid,
        p_create_by,p_create_date,p_update_by,p_main_payment_gid;
	 if finished = 1 then
			leave atma_looop;
		End if;
	if p_main_payment_gid = '' or p_main_payment_gid is null  or p_main_payment_gid=0 then
set Error_Level='ATMA53.1';
		set Query_Update = concat('INSERT INTO atma_mst_tpayment (payment_partnergid,payment_partnerbranchgid,
				payment_paymodegid,payment_bankgid,payment_bankbranchgid,payment_acctype ,
				payment_accnumber,payment_benificiaryname,payment_remarks,
				payment_isactive,payment_isremoved,
				entity_gid,create_by,create_date)
			values (',Partner_Gid,',',@newpartnerbranchgid,',',p_payment_paymodegid,',',p_payment_bankgid,',
					',p_payment_bankbranchgid,',''',p_payment_acctype,''',
					''',p_payment_accnumber,''',''',p_payment_benificiaryname,''',
					''',p_payment_remarks,''',''',p_payment_isactive,''',
					''',p_payment_isremoved,''',',p_entity_gid,',',p_create_by,',
				  ''',Now(),''')');
		#select Query_Update;
		SET SQL_SAFE_UPDATES = 0;
        set Query_delete=concat('DELETE FROM atma_tmp_mst_tpayment WHERE payment_gid=',p_payment_gid,'');
		set @Insert_query = Query_delete;
		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
		set Message = 'DELETED';
		else
		set Message = ' FAILED deletion';
		leave sp_Atma_Pending_To_Approval_payment_Set;
		end if;
	else
   # select 1;
		set Query_Update = '';
		#if p_payment_partnerbranchgid is not null or p_payment_partnerbranchgid <> '' or p_payment_partnerbranchgid <> 0  then
		#	set Query_Update = concat(Query_Update, ',payment_partnerbranchgid = ',p_payment_partnerbranchgid,' ');
		#end if;
		if p_payment_paymodegid is not null or p_payment_paymodegid <> '' or p_payment_paymodegid <> 0  then
				set Query_Update = concat(Query_Update, ',payment_paymodegid = ',p_payment_paymodegid,' ');
		end if;
        if p_payment_bankgid is not null or p_payment_bankgid <> '' or p_payment_bankgid <> 0 then
				set Query_Update = concat(Query_Update,',payment_bankgid = ',p_payment_bankgid,'  ');
		End if;
		if p_payment_bankbranchgid is not null or p_payment_bankbranchgid <> '' or p_payment_bankbranchgid <> 0 then
				set Query_Update = concat(Query_Update,',payment_bankbranchgid = ',p_payment_bankbranchgid,'  ');
		End if;
		if p_payment_acctype is not null or p_payment_acctype <> '' then
			set Query_Update = concat(Query_Update,',payment_acctype = ''',p_payment_acctype,'''  ');
		End if;
		if p_payment_accnumber is not null or p_payment_accnumber <> '' then
			set Query_Update = concat(Query_Update,',payment_accnumber = ''',p_payment_accnumber,'''  ');
		End if;
		if p_payment_benificiaryname is not null or p_payment_benificiaryname <> '' then
			set Query_Update = concat(Query_Update,',payment_benificiaryname = ''',p_payment_benificiaryname,'''  ');
		End if;
		if p_payment_remarks is not null or p_payment_remarks <> '' then
			set Query_Update = concat(Query_Update,',payment_remarks = ''',p_payment_remarks,'''  ');
		End if;
		if @Update_By is not null or @Update_By <> '' then
			set Query_Update = concat(Query_Update,',update_by = ',@Update_By,'  ');
		End if;
        #select p_payment_partnerbranchgid,p_payment_acctype;
set Error_Level='ATMA53.2';
		set Query_Update = concat('Update atma_mst_tpayment  set
				update_date = CURRENT_TIMESTAMP ',Query_Update,'
				where payment_gid=',p_main_payment_gid,'');
#select Query_Update;
		SET SQL_SAFE_UPDATES = 0;
		set Query_delete=concat('DELETE FROM atma_tmp_mst_tpayment WHERE payment_gid=',p_payment_gid,'');
		set @Insert_query = Query_delete;
		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'DELETED';
		else
			set Message = 'FAILED';
			leave sp_Atma_Pending_To_Approval_payment_Set;
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
	else
		set Message = ' FAILED_pay';
		leave sp_Atma_Pending_To_Approval_payment_Set;
	end if;
	End loop atma_looop;
	close Cursor_atma;
	end;


End if;

END