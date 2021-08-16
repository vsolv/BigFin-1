CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Master_View_And_Cancle`(in li_Action  varchar(40),
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_Atma_Master_View_And_Cancel:BEGIN

#Balamaniraja       28-09-2019

declare Query_Insert varchar(1000);
Declare countRow varchar(6000);
declare Query_Update varchar(1000);
declare Query_Value varchar(1000);
declare Query_Column varchar(1000);
Declare errno int;
Declare msg varchar(1000);

						DECLARE EXIT HANDLER FOR SQLEXCEPTION
						BEGIN
							GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
							set Message = concat(errno , msg);
							ROLLBACK;
						END;


	IF li_Action='APPROVER_TO_REQUEST' then  #Partner Status APPROVER TO REQUEST VIEW In Master

			START TRANSACTION;

			select JSON_LENGTH(lj_filter,'$') into @lj_filter_json_count;
            #select JSON_LENGTH(lj_classification,'$') into @li_classification_jsoncount;

				if @lj_filter_json_count = 0 or @lj_filter_json_count is null then
					set Message = 'No Data In filter Json. ';
					leave sp_Atma_Master_View_And_Cancel;
				End if;


          select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Gid')))
          into @Partner_Gid;
          select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Status')))
          into @Partner_Status;


				if @Partner_Gid = '' or @Partner_Gid is null then
					set Message = 'Partner_Gid is not given. ';
					leave sp_Atma_Master_View_And_Cancel;
				End if;

                if @Partner_Status = '' or @Partner_Status is null then
					set Message = 'Partner_Status is not given. ';
					leave sp_Atma_Master_View_And_Cancel;
				End if;


                 set @Partner_Status1='';
          select partner_status from atma_mst_tpartner
          where partner_gid=@Partner_Gid and partner_status='APPROVED' into @Partner_Status1;
          #select @Partner_Status1;

          select partner_status from atma_mst_tpartner
          where partner_gid=@Partner_Gid into @PR_Status;

              if @Partner_Status1 =''or @Partner_Status1 is null then
					set Message = concat('Already This Partner Is View By Some One ') ;
					leave sp_Atma_Master_View_And_Cancel;
			  End if;


			set Query_Update ='';

            set Query_Update = concat('Update  atma_mst_tpartner
                         set partner_status=''',@Partner_Status,'''
						 Where partner_gid = ',@Partner_Gid,' and
                         partner_isactive=''Y''and
                         partner_isremoved=''N''
                         ');

			#select Query_Update;
			set @Query_Update = Query_Update;
			PREPARE stmt FROM @Query_Update;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;

		if countRow <= 0 then
				set Message = 'Error On Update.';
				rollback;
				leave sp_Atma_Master_View_And_Cancel;
		elseif    countRow > 0 then
				set Message = 'SUCCESS';
                commit;
		end if;

	ELSEIF li_Action='VIEW_TO_CANCEL' then  #Partner Status REQUEST VIEW TO APPROVER In Master

			START TRANSACTION;

			select JSON_LENGTH(lj_filter,'$') into @lj_filter_json_count;
            #select JSON_LENGTH(lj_classification,'$') into @li_classification_jsoncount;

				if @lj_filter_json_count = 0 or @lj_filter_json_count is null then
					set Message = 'No Data In filter Json. ';
					leave sp_Atma_Master_View_And_Cancel;
				End if;


          select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Gid')))
          into @Partner_Gid;
          select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Status')))
          into @Partner_Status;

				if @Partner_Gid = '' or @Partner_Gid is null then
					set Message = 'Partner_Gid is not given. ';
					leave sp_Atma_Master_View_And_Cancel;
				End if;

                if @Partner_Status = '' or @Partner_Status is null then
					set Message = 'Partner_Status is not given. ';
					leave sp_Atma_Master_View_And_Cancel;
				End if;



			set Query_Update ='';

            set Query_Update = concat('Update  atma_mst_tpartner
                         set partner_status=''',@Partner_Status,'''
						 Where partner_gid = ',@Partner_Gid,' and
                         partner_isactive=''Y''and
                         partner_isremoved=''N''
                         ');

			#select Query_Update;
			set @Query_Update = Query_Update;
			PREPARE stmt FROM @Query_Update;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;

		if countRow <= 0 then
				set Message = 'Error On Update.';
				rollback;
				leave sp_Atma_Master_View_And_Cancel;
		elseif    countRow > 0 then
				set Message = 'SUCCESS';
                commit;
		end if;


END IF;


END