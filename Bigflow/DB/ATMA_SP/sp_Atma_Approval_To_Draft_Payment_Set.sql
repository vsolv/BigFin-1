CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Approval_To_Draft_Payment_Set`(in li_Action  varchar(30),
in lj_filter json,in Partner_Gid int,in Newpartnerbranchgid int,in Oldpartnerbranch_gid int,
in lj_classification json,out Message varchar(1000))
sp_Atma_Approval_To_Draft_Payment_Set:BEGIN
Declare Query_Insert varchar(10000);
Declare countRow varchar(6000);
Declare Query_Update varchar(10000);
Declare Query_delete varchar(1000);
Declare Query_Value varchar(1000);
Declare Query_Column varchar(1000);
Declare p_payment_gid,p_payment_partnergid,p_payment_partnerbranchgid,p_payment_paymodegid,p_payment_bankgid,p_payment_bankbranchgid,p_payment_acctype,p_payment_accnumber,
		p_payment_benificiaryname,p_payment_remarks,p_payment_isactive,p_payment_isremoved,p_entity_gid,p_create_by,p_create_date varchar(150);

DECLARE finished INTEGER DEFAULT 0;
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
		leave sp_Atma_Approval_To_Draft_Payment_Set;
	End if;

			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Gid')))
			into @Partner_Gid;



 SET finished =0;

BEGIN

	Declare Cursor_atma CURSOR FOR
	select payment_gid,payment_partnergid,payment_partnerbranchgid,payment_paymodegid,payment_bankgid,payment_bankbranchgid,
    payment_acctype,payment_accnumber,payment_benificiaryname,payment_remarks,payment_isactive,payment_isremoved,
    entity_gid,create_by,create_date
	 from atma_mst_tpayment where payment_partnergid=@Partner_Gid
     and payment_partnerbranchgid=Oldpartnerbranch_gid ;

	DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;

	OPEN Cursor_atma;
	atma_looop:loop
		fetch Cursor_atma into p_payment_gid,p_payment_partnergid,p_payment_partnerbranchgid,p_payment_paymodegid,p_payment_bankgid,
        p_payment_bankbranchgid,p_payment_acctype,p_payment_accnumber,p_payment_benificiaryname,p_payment_remarks,
        p_payment_isactive,p_payment_isremoved,p_entity_gid,p_create_by,p_create_date;
		if finished = 1 then
			leave atma_looop;
		End if;
            set Error_Level='ATMA10.1';
			set Query_Insert = concat('INSERT INTO atma_tmp_mst_tpayment (payment_partnergid,payment_partnerbranchgid,payment_paymodegid,payment_bankgid,
            payment_bankbranchgid,payment_acctype,payment_accnumber,payment_benificiaryname,payment_remarks,payment_isactive,payment_isremoved,
            entity_gid,create_by,create_date,main_payment_gid)values (', Partner_Gid,',',Newpartnerbranchgid,',
			',p_payment_paymodegid,',',p_payment_bankgid,',',p_payment_bankbranchgid,',''',p_payment_acctype,''',''',p_payment_accnumber,''',
            ''',p_payment_benificiaryname,''',''',p_payment_remarks,''',''',p_payment_isactive,''',''',p_payment_isremoved,''',',p_entity_gid,',
            ',p_create_by,',''',p_create_date,''',',p_payment_gid,')');


		set @Insert_query = Query_Insert;
		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'SUCCESS';
		else
			set Message = ' FAILED PARTNER_PAY';
			leave sp_Atma_Approval_To_Draft_Payment_Set;
		end if;
End loop atma_looop;
close Cursor_atma;
end;

 END IF;
END