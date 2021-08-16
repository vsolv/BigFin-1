CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Approval_To_Draft_Document_Set`(in li_Action  varchar(30),
in lj_filter json,in Partner_Gid int,in lj_classification json,out Message varchar(1000))
sp_Atma_Approval_To_Draft_Document_Set:BEGIN
Declare Query_Insert varchar(10000);
Declare countRow varchar(6000);
Declare Query_Update varchar(10000);
Declare Query_delete varchar(1000);
Declare Query_Value varchar(1000);
Declare Query_Column varchar(1000);
Declare d_documents_gid,d_documents_partnergid,d_documents_docgroupgid,d_documents_period,
		d_documents_remarks,d_documents_filegid,d_docments_isactive,d_documents_isremoved,d_entity_gid,
		d_create_by,d_create_date varchar(150);

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
		leave sp_Atma_Approval_To_Draft_Document_Set;
	End if;

			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Gid')))
			into @Partner_Gid;

 #set @NEWPartnergid=4;#NEW_TMP_GID

 SET finished =0;
	BEGIN

	Declare Cursor_atma CURSOR FOR

			select documents_gid,documents_partnergid,documents_docgroupgid,documents_period,
			documents_remarks,documents_filegid,docments_isactive,documents_isremoved,entity_gid,
			create_by,create_date
			from atma_trn_tdocuments where documents_partnergid=@Partner_Gid ;

	DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;

	OPEN Cursor_atma;
	atma_looop:loop

			fetch Cursor_atma into d_documents_gid,d_documents_partnergid,d_documents_docgroupgid,d_documents_period,
			d_documents_remarks,d_documents_filegid,d_docments_isactive,d_documents_isremoved,d_entity_gid,
			d_create_by,d_create_date;
			if finished = 1 then
			leave atma_looop;
		End if;
			set Error_Level='ATMA9.1';
			set Query_Insert = concat('INSERT INTO atma_tmp_trn_tdocuments (documents_partnergid,documents_docgroupgid,documents_period,
            documents_remarks,documents_filegid,docments_isactive,documents_isremoved,entity_gid,create_by,create_date,main_documents_gid)values (',Partner_Gid,',
			',d_documents_docgroupgid,',''',d_documents_period,''',''',d_documents_remarks,''',',d_documents_filegid,',''',d_docments_isactive,''',
            ''',d_documents_isremoved,''',',d_entity_gid,',
            ',d_create_by,',''',d_create_date,''',',d_documents_gid,')');

			#select Query_Insert;
			set @Insert_query = Query_Insert;
			PREPARE stmt FROM @Insert_query;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;
			if countRow >  0 then
			set Message = 'SUCCESS';
			else
			set Message = ' FAILED PARTNER_DOC';
			leave sp_Atma_Approval_To_Draft_Document_Set;
			end if;
End loop atma_looop;
close Cursor_atma;
end;  #Endof Cursor
 END IF;
END