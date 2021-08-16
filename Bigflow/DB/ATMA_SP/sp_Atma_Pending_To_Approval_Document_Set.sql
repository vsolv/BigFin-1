CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Pending_To_Approval_Document_Set`(in li_Action  varchar(30),
in lj_filter json,in Partner_Gid int,in lj_classification json,out Message varchar(1000))
sp_Atma_Pending_To_Approval_Document_Set:BEGIN
declare Query_Insert varchar(10000);
Declare countRow varchar(6000);
declare Query_Update varchar(10000);
declare Query_delete varchar(1000);
declare Query_Value varchar(1000);
declare Query_Column varchar(1000);
Declare d_documents_gid,d_documents_partnergid,d_documents_docgroupgid,d_documents_period,d_documents_remarks,
d_documents_filegid,d_docments_isactive,d_documents_isremoved,d_entity_gid,d_create_by,d_update_by,
d_main_documents_gid varchar(150);
DECLARE finished INTEGER DEFAULT 0;

Declare errno int;
Declare msg,Error_Level varchar(1000);

						DECLARE EXIT HANDLER FOR SQLEXCEPTION
						BEGIN
							GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
							set Message = concat(Error_Level,' :No-',errno,msg);
							ROLLBACK;
						END;

IF li_Action='Insert' then



	select JSON_LENGTH(lj_filter,'$') into @lj_filter_json_count;
	select JSON_LENGTH(lj_classification,'$') into @lj_classification_json_count;

	if @lj_filter_json_count = 0 or @lj_filter_json_count is null then
		set Message = 'No Data In filter Json. ';
		leave sp_Atma_Pending_To_Approval_Document_Set;
	End if;

	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Gid')))
	into @Partner_Gid;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Update_By')))
    into @Update_By;



	if @Partner_Gid = '' or @Partner_Gid is null  or @Partner_Gid=0 then
			set Message = 'Partner Is Not Provided';
			leave sp_Atma_Pending_To_Approval_Document_Set;
	End if;


      #SET finished =0;
      #set @Main_partner_gid=4;
BEGIN
	Declare Cursor_atma CURSOR FOR

	select documents_gid,documents_partnergid,documents_docgroupgid,documents_period,documents_remarks,
	documents_filegid,docments_isactive,documents_isremoved,entity_gid,create_by,update_by,main_documents_gid
	from atma_tmp_trn_tdocuments where documents_partnergid=@Partner_Gid ;

	DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;
	OPEN Cursor_atma;
	atma_looop:loop
		fetch Cursor_atma into d_documents_gid,d_documents_partnergid,d_documents_docgroupgid,d_documents_period,d_documents_remarks,
		d_documents_filegid,d_docments_isactive,d_documents_isremoved,d_entity_gid,d_create_by,d_update_by,
		d_main_documents_gid;
	      if finished = 1 then
			leave atma_looop;
		End if;
	if d_main_documents_gid = '' or d_main_documents_gid is null  or d_main_documents_gid=0 then

set Error_Level='ATMA50.1';
			set Query_Update = concat('INSERT INTO atma_trn_tdocuments (documents_partnergid,documents_docgroupgid,documents_period,documents_remarks,
			documents_filegid,docments_isactive,documents_isremoved,entity_gid,create_by,create_date)values (',Partner_Gid,',',d_documents_docgroupgid,',
            ''',d_documents_period,''',''',d_documents_remarks,''',',d_documents_filegid,',
			''',d_docments_isactive,''',''',d_documents_isremoved,''',',d_entity_gid,',',d_create_by,',''',Now(),''')');

            #select Query_Update;
			SET SQL_SAFE_UPDATES = 0;
            set Query_delete=concat('DELETE FROM atma_tmp_trn_tdocuments WHERE documents_gid=',d_documents_gid,'');
			set @Insert_query = Query_delete;
			PREPARE stmt FROM @Insert_query;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;
			if countRow >  0 then
			set Message = 'DELETED';
			else
			set Message = ' FAILED DELETION';
			leave sp_Atma_Pending_To_Approval_Document_Set;
			end if;

	else


				set Query_Update = '';

					if d_documents_docgroupgid is not null or d_documents_docgroupgid <> '' or d_documents_docgroupgid <> 0 then

						set Query_Update = concat(Query_Update,',documents_docgroupgid = ',d_documents_docgroupgid,'  ');

					End if;

                    if d_documents_period is not null or d_documents_period <> ''  then

						set Query_Update = concat(Query_Update,',documents_period = ''',d_documents_period,'''  ');

					End if;

					if d_documents_remarks is not null or d_documents_remarks <> '' then

						set Query_Update = concat(Query_Update,',documents_remarks = ''',d_documents_remarks,'''  ');

					End if;

                    if d_documents_filegid is not null or d_documents_filegid <> '' then

						set Query_Update = concat(Query_Update,',documents_filegid = ',d_documents_filegid,'  ');

					End if;

                    if @Update_By is not null or @Update_By <> '' then

						set Query_Update = concat(Query_Update,',update_by = ',@Update_By,'  ');

					End if;

 set Error_Level='ATMA50.2';
				set Query_Update = concat(' Update atma_trn_tdocuments  set
									  update_date = CURRENT_TIMESTAMP ',Query_Update,'
									  where documents_gid=',d_main_documents_gid,'');


           SET SQL_SAFE_UPDATES = 0;
			set Query_delete=concat('DELETE FROM atma_tmp_trn_tdocuments WHERE documents_gid=',d_documents_gid,'');
			set @Insert_query = Query_delete;
			PREPARE stmt FROM @Insert_query;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;
			if countRow >  0 then
			set Message = 'DELETED';
			else
			set Message = ' FAILED DELETION';
			leave sp_Atma_Pending_To_Approval_Document_Set;
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
			set Message = ' FAILED_D';
			leave sp_Atma_Pending_To_Approval_Document_Set;
		end if;
		End loop atma_looop;
		close Cursor_atma;
		end;  #Endof Cursor




End if;

END