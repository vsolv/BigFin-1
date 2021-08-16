CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Partner_Deactivate_Set`(in li_Action  varchar(30),
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_Atma_Partner_Deactivate_Set:BEGIN



declare Query_Insert varchar(2000);
Declare countRow varchar(6000);
declare Query_Update varchar(1000);
Declare errno int;
Declare msg varchar(1000);

						DECLARE EXIT HANDLER FOR SQLEXCEPTION
						BEGIN
							GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
							set Message = concat(errno , msg);
							ROLLBACK;
						END;


IF li_Action='Partner_Deactivate' then


        START TRANSACTION;

        select JSON_LENGTH(lj_filter,'$') into @json_count;
		select JSON_LENGTH(lj_classification,'$') into @lj_classification_json_count;

        if @json_count = 0 or @json_count is null then
			set Message = 'No Data In Filter Json. ';
			leave sp_Atma_Partner_Deactivate_Set;
		End if;



		  select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Gid')))
          into @Partner_Gid;
          select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Tran_Remarks')))
          into @Tran_Remarks;
          select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Status')))
          into @Partner_Status;
          select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_RequestFor')))
          into @Partner_RequestFor;
		  select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Entity_Gid')))
          into @Entity_Gid;
          select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Create_By')))
          into @Create_By;


          if @Partner_Gid = '' or @Partner_Gid is null then
			  set Message = 'Partner_Gid Is Not Given. ';
			  leave sp_Atma_Partner_Deactivate_Set;
		  End if;

          if @Partner_Status = '' or @Partner_Status is null then
			  set Message = 'Partner_Status Is Not Given. ';
			  leave sp_Atma_Partner_Deactivate_Set;
		  End if;

          if @Partner_RequestFor = '' or @Partner_RequestFor is null then
			  set Message = 'Partner_RequestFor Is Not Given. ';
			  leave sp_Atma_Partner_Deactivate_Set;
		  End if;




                set @RequestFor='';
                SELECT partner_requestfor   FROM atma_tmp_tpartner
                WHERE Main_Partner_Gid=@Partner_Gid  into @RequestFor;

				set @Partner_Status1='';
                SELECT partner_status   FROM atma_tmp_tpartner
                WHERE Main_Partner_Gid=@Partner_Gid  into @Partner_Status1;



          if  @Partner_Status1 <> 'APPROVED'  then
			  set Message = concat( 'This Partner Is Already Exists For ',@RequestFor,' Request ')  ;
			  leave sp_Atma_Partner_Deactivate_Set;
		  End if;


          select main_partner_gid from atma_tmp_tpartner   Where main_partner_gid = @Partner_Gid
          into @Main_Partner_Gid;

        set Query_Update='';
        SET SQL_SAFE_UPDATES = 0;
        set Query_Update=concat('Update atma_tmp_tpartner
								 set partner_status = ''',@Partner_Status,''',
								  partner_requestfor = ''',@Partner_RequestFor,'''
								  Where main_partner_gid = ',@Main_Partner_Gid,'
                                 ');

        set @query_update = Query_Update;

		PREPARE stmt FROM @query_update;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'SUCCESSFULLY UPDATED';
            commit;
		else
			set Message = 'FAILED';
			rollback;
		end if;




	  ELSEIF li_Action='Partner_Activate' then


        START TRANSACTION;

        select JSON_LENGTH(lj_filter,'$') into @json_count;
		select JSON_LENGTH(lj_classification,'$') into @lj_classification_json_count;

        if @json_count = 0 or @json_count is null then
			set Message = 'No Data In Filter Json. ';
			leave sp_Atma_Partner_Deactivate_Set;
		End if;



		  select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Gid')))
          into @Partner_Gid;
          select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Tran_Remarks')))
          into @Tran_Remarks;
          select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Status')))
          into @Partner_Status;
          select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_RequestFor')))
          into @Partner_RequestFor;



          if @Partner_Gid = '' or @Partner_Gid is null then
			  set Message = 'Partner_Gid Is Not Given. ';
			  leave sp_Atma_Partner_Deactivate_Set;
		  End if;

          if @Partner_Status = '' or @Partner_Status is null then
			  set Message = 'Partner_Status Is Not Given. ';
			  leave sp_Atma_Partner_Deactivate_Set;
		  End if;

          if @Partner_RequestFor = '' or @Partner_RequestFor is null then
			  set Message = 'Partner_RequestFor Is Not Given. ';
			  leave sp_Atma_Partner_Deactivate_Set;
		  End if;




                set @RequestFor='';
                SELECT partner_requestfor   FROM atma_tmp_tpartner
                WHERE Main_Partner_Gid=@Partner_Gid  into @RequestFor;

				set @Partner_Status1='';
                SELECT partner_status   FROM atma_tmp_tpartner
                WHERE Main_Partner_Gid=@Partner_Gid  into @Partner_Status1;


         if @RequestFor <> 'Deactivation'and @Partner_Status1 <> 'Deactivated'  then
			  set Message = concat( 'This Partner Is Already Exists For ',@RequestFor,' Request ')  ;
			  leave sp_Atma_Partner_Deactivate_Set;
		  End if;

          select main_partner_gid from atma_tmp_tpartner   Where main_partner_gid = @Partner_Gid
          into @Main_Partner_Gid;

        set Query_Update='';
        SET SQL_SAFE_UPDATES = 0;
        set Query_Update=concat('Update atma_tmp_tpartner
								 set partner_status = ''',@Partner_Status,''',
								  partner_requestfor = ''',@Partner_RequestFor,'''
								  Where main_partner_gid = ',@Main_Partner_Gid,'
                                 ');

        set @query_update = Query_Update;

		PREPARE stmt FROM @query_update;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'SUCCESSFULLY UPDATED';
            commit;
		else
			set Message = 'FAILED';
			rollback;
		end if;







END IF;

END