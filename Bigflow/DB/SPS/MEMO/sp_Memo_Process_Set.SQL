CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Memo_Process_Set`(IN `ls_Action` varchar(32),IN `ls_Type` varchar(32),
IN `ls_Sub_Type` varchar(32),IN `lj_Details` json,IN `lj_Status` Json,
IN `lj_Classification` json,IN `ls_Createby` varchar(16),OUT `Message` varchar(6024))
sp_Memo_Process_Set:BEGIN
### Bala Feb 05 2020 - Created
Declare errno int;
Declare msg varchar(1000);
Declare i int;
Declare j int;
Declare countRow int;
Declare Query_Insert varchar(9000);
Declare Query_Update varchar(9000);
Declare Query_Column varchar(9000);
Declare Query_Value varchar(9000);



# Null Selected Output
DECLARE done INT DEFAULT 0;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
#...

  DECLARE EXIT HANDLER FOR SQLEXCEPTION,sqlwarning

     BEGIN
		GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
		set Message = concat(errno , msg);
		ROLLBACK;
     END;

		select  JSON_UNQUOTE(JSON_EXTRACT(lj_Classification,'$.Entity_Gid[0]')) into @Entity_Gids;

        if @Entity_Gids is  null or @Entity_Gids = '' then
				set Message = 'Entity_Gid Is Not Given';
                leave sp_Memo_Process_Set;
        End if;


start transaction;
set autocommit=0;
set autocommit=off;


IF ls_Action = 'INSERT' and ls_Type = 'MEMO' and  ls_Sub_Type = 'REQUEST'  then


						select JSON_LENGTH(lj_Details, '$') into @li_json_count;

						if @li_json_count is null or @li_json_count = 0 then
							set Message = 'No Data In Json.';
							leave sp_Memo_Process_Set;
						end if;



                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.File_Name'))) into @File_Name;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.File_Path'))) into @File_Path;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Request_Name'))) into @Request_Name;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Memo_Subcategory_Gid'))) into @Memo_Subcategory_Gid;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Request_ion'))) into @Request_ion;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Request_Approver_Gid'))) into @Request_Approver_Gid;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Requesttran_Comments'))) into @Requesttran_Comments;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,CONCAT('$.Request_Status'))) into @Request_Status;


                            if @Request_ion='undefined' then
								set @Request_ion = '';
							End if;

                            if @Requesttran_Comments='undefined' then
								set @Requesttran_Comments = '';
							End if;

                            if @Request_Name is null or @Request_Name = '' then
								set Message = 'Request Name Is Needed.';
								leave sp_Memo_Process_Set;
							End if;

                            if @Memo_Subcategory_Gid is null or @Memo_Subcategory_Gid = '' then
								set Message = 'Memo Subcategory Gid  Is Needed.';
								leave sp_Memo_Process_Set;
							End if;

							/*if @Request_Approver_Gid is null or @Request_Approver_Gid = '' then
								set Message = 'Request Approver Gid  Is Needed.';
								leave sp_Memo_Process_Set;
							End if;*/


                            if @Request_Status is null or @Request_Status = '' then
								set Message = 'Request Status Is Needed.';
								leave sp_Memo_Process_Set;
							End if;

                            if ls_Createby is null or ls_Createby = '' then
								set Message = 'Createby  Is Needed.';
								leave sp_Memo_Process_Set;
							End if;


		set @Request_File_Gid=0;
		if @File_Name<>'' and @File_Path <>'' and @File_Name is not null and  @File_Path is not null then

				set @Classification_json = '';
				set @Classification_json = concat('{
													"Entity_Gid":"',@Entity_Gids,'"
													}');

                   #Not null Columns
						/*  mem_trn_trequesttran-->File_Name,File_Path
                        ,requesttran_by,entity_gid,
						create_by*/

			call sp_File_Set('Insert', 'a',0,@File_Name,@File_Path,
				@Classification_json, '{}',ls_Createby, @Msg);


            select substring_index(@Msg,',',-1) INTO @File_Test;
            select substring_index(@Msg,',',1) INTO @Request_File_Gid;


					if @File_Test='SUCCESS' then
						set Message = 'SUCCESS';
					else
						rollback;
						set Message = 'FAIL';
						leave sp_Memo_Process_Set;
					end if;

		end if;#@File_Name<>'' and @File_Path <>'' and @File_Name is not null and  @File_Path

			select exists(select request_code from mem_trn_trequest) into @Test;

			select max(substr(request_code,2)) from mem_trn_trequest  into @Request_Cde;


            if @Test=0 then
				call sp_Generatecode_Get('WITHOUT_DATE', 'B', '000','000', @Message);
				select @Message into @Request_Code;
			else
				call sp_Generatecode_Get('WITHOUT_DATE', 'B', '000',@Request_Cde, @Message);
				select @Message into @Request_Code;
			end if;

             set Query_Column='';
             set Query_Value='';

				if @Request_ion is not null and @Request_ion <> '' then
					set Query_Column= concat(Query_Column,',request_ion ');
					set Query_Value= concat(Query_Value,',''',@Request_ion,''' ');
				End if;

				if @Request_Approver_Gid is not null and @Request_Approver_Gid <> '' then
					set Query_Column= concat(Query_Column,',request_approvergid ');
					set Query_Value= concat(Query_Value,',''',@Request_Approver_Gid,''' ');
				End if;

                if @Request_File_Gid <> 0 then
					set Query_Column= concat(Query_Column,',request_filegid ');
					set Query_Value= concat(Query_Value,',''',@Request_File_Gid,''' ');
				End if;

                #Not null Columns
               /* mem_trn_trequest-->request_code,request_name,
				   request_memosubcategorygid,
                   request_status,entity_gid,
                   create_by*/

			set Query_Insert = '';
			set Query_Insert = concat('INSERT INTO mem_trn_trequest
											 (request_code,request_name,
											 request_memosubcategorygid,
											 request_status,entity_gid,
                                             create_by ',Query_Column,')
									   VALUES(''',@Request_Code,''',''',@Request_Name,''',
											  ',@Memo_Subcategory_Gid,',
											  ''',@Request_Status,''',',@Entity_Gids,',
                                              ',ls_Createby,' ',Query_Value,' )
									   ');

							set @Insert_query = Query_Insert;
							#SELECT @Insert_query;
							PREPARE stmt FROM @Insert_query;
							EXECUTE stmt;
							set countRow = ROW_COUNT();
							DEALLOCATE PREPARE stmt;


							if  countRow>0 then
								set Message = 'SUCCESS';
                                set @Request_Gid=last_insert_id();
							else
								rollback;
								set Message = 'FAIL';
                                leave sp_Memo_Process_Set;
							End if;

                         #Not null Columns
						/*  mem_trn_trequesttran-->requesttran_requestgid,requesttran_status,
					   requesttran_from,requesttran_fromdate,
                       requesttran_to,requesttran_by,entity_gid,
                       create_by*/


					select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.Tran_To')) into @Detail_json_To;

					set @Detail_json_To =concat('{', '"',"Tran_To" '"', ':',@Detail_json_To,'}');

					select JSON_LENGTH(@Detail_json_To ,'$.Tran_To') into @Tran_To_count;

             set @Test_To=0;
            set i =0;

            while i< @Tran_To_count do


			select JSON_UNQUOTE(JSON_EXTRACT(@Detail_json_To,CONCAT('$.Tran_To[',i,']'))) into @Requesttran_To;


					select employee_name into @Emp_To_name from gal_mst_temployee
							where employee_gid=@Requesttran_To
								and  employee_isactive='Y'
								and employee_isremoved='N';


                            SELECT FIND_IN_SET(@Requesttran_To, @Test_To) into @Test_Id;
							set @Test_To=concat(@Test_To,',',@Requesttran_To);

							if @Test_Id <>0 then
								rollback;
								set Message =CONCAT(@Emp_To_name,' - This Requesttran To Is Already Exsist In MEMO To');
                                leave sp_Memo_Process_Set;
							end if;


			set Query_Column='',Query_Value='';

            # select @Request_Gid,@Request_Status, @Request_Approver_Gid,
									#		  @Request_File_Gid, @Entity_Gids,Query_Value;

                if @Requesttran_Comments is not null and @Requesttran_Comments <> '' then
					set Query_Column= concat(Query_Column,',requesttran_comments ');
					set Query_Value= concat(Query_Value,',''',@Requesttran_Comments,''' ');
				End if;


                /*if @Tran_Totype is not null and @Tran_Totype <> '' then
					set Query_Column= concat(Query_Column,',requesttran_totype ');
					set Query_Value= concat(Query_Value,',''',@Tran_Totype,''' ');
				End if; */



			set @Tran_Totype='To';
			set @Requesttran_By=0;

			set Query_Insert = '';
			set Query_Insert = concat('INSERT INTO mem_trn_trequesttran
											 (requesttran_requestgid,requesttran_status,
											  requesttran_from,requesttran_fromdate,
											  requesttran_filegid,requesttran_to,
                                              requesttran_by,requesttran_totype,
                                              entity_gid,create_by
                                              ',Query_Column,')
									   VALUES(',@Request_Gid,',''',@Request_Status,''',
											  ',ls_Createby,',now(),
                                              ',@Request_File_Gid,',',@Requesttran_To,',
                                              ',@Requesttran_By,',''',@Tran_Totype,''',
                                              ',@Entity_Gids,',',ls_Createby,'
													',Query_Value,')
									   ');


							set @Insert_query = Query_Insert;
							#SELECT @Insert_query;
							PREPARE stmt FROM @Insert_query;
							EXECUTE stmt;
							set countRow = ROW_COUNT();
							DEALLOCATE PREPARE stmt;


							if  countRow>0 then
								set Message = 'SUCCESS';
							else
								rollback;
								set Message = 'FAIL';
                                leave sp_Memo_Process_Set;
							End if;

                     set i=i+1;

                     end while;

                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.Tran_CC')) into @Detail_json_CC;

					set @Detail_json_CC =concat('{', '"',"Tran_CC" '"', ':',@Detail_json_CC,'}');

                    select JSON_LENGTH( @Detail_json_CC,'$.Tran_CC') into @Tran_CC_count;



            set i =0;

            while i< @Tran_CC_count do

			select JSON_UNQUOTE(JSON_EXTRACT(@Detail_json_CC,CONCAT('$.Tran_CC[',i,']'))) into @Requesttran_CC;



					select employee_name into @Emp_CC_name from gal_mst_temployee
							where employee_gid=@Requesttran_CC
								and  employee_isactive='Y'
								and employee_isremoved='N';


						SELECT FIND_IN_SET(@Requesttran_CC, @Test_To) into @Test_Id;
							set @Test_To=concat(@Test_To,',',@Requesttran_CC);

							if @Test_Id <>0 then
								rollback;
								set Message =CONCAT(@Emp_CC_name,' - This Requesttran To Is Already Exsist In MEMO To');
                                leave sp_Memo_Process_Set;
							end if;


			set Query_Column='',Query_Value='';


                 if @Requesttran_Comments is not null and @Requesttran_Comments <> '' then
					set Query_Column= concat(Query_Column,',requesttran_comments ');
					set Query_Value= concat(Query_Value,',''',@Requesttran_Comments,''' ');
				End if;


                /*if @Tran_Totype is not null and @Tran_Totype <> '' then
					set Query_Column= concat(Query_Column,',requesttran_totype ');
					set Query_Value= concat(Query_Value,',''',@Tran_Totype,''' ');
				End if;  */


			set @Tran_Totype='Cc';
			set @Requesttran_By=0;

			set Query_Insert = '';
			set Query_Insert = concat('INSERT INTO mem_trn_trequesttran
											 (requesttran_requestgid,requesttran_status,
											  requesttran_from,requesttran_fromdate,
											  requesttran_filegid,requesttran_to,
                                              requesttran_by,requesttran_totype,
                                              entity_gid,create_by
                                              ',Query_Column,')
									   VALUES(',@Request_Gid,',''',@Request_Status,''',
											  ',ls_Createby,',now(),
                                              ',@Request_File_Gid,',',@Requesttran_CC,',
                                              ',@Requesttran_By,',''',@Tran_Totype,''',
                                              ',@Entity_Gids,',',ls_Createby,'
													',Query_Value,')
									   ');


							set @Insert_query = Query_Insert;
							#SELECT @Insert_query;
							PREPARE stmt FROM @Insert_query;
							EXECUTE stmt;
							set countRow = ROW_COUNT();
							DEALLOCATE PREPARE stmt;


							if  countRow>0 then
								set Message = 'SUCCESS';
							else
								rollback;
								set Message = 'FAIL';
                                leave sp_Memo_Process_Set;
							End if;


                     set i=i+1;

                     end while;




							if Message = 'SUCCESS' then
								set Message = 'SUCCESS';
                                commit;
							else
								rollback;
								set Message = 'FAIL';
                                leave sp_Memo_Process_Set;
							End if;


ELSEIF ls_Action = 'UPDATE' and ls_Type = 'MEMO' and  ls_Sub_Type = 'APPROVE'  then

				select JSON_LENGTH(lj_Details,'$') into @li_json_count;

						if @li_json_count is null or @li_json_count = 0 then
							set Message = 'No Data In Json.';
							leave sp_Memo_Process_Set;
						end if;

			select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.File_Name'))) into @File_Name;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.File_Path'))) into @File_Path;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Request_Gid'))) into @Request_Gid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Comments'))) into @Comments;
			#select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Final_Approver'))) into @Final_Approver;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Requesttran_to'))) into @Requesttran_to;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,CONCAT('$.Requesttran_Status'))) into @Requesttran_Status;


					if @Request_Gid is null or @Request_Gid = '' then
							set Message = 'Request Gid Is Needed.';
							leave sp_Memo_Process_Set;
					End if;


                    /*if @Requesttran_to is null or @Requesttran_to = '' then
							set Message = 'Requesttran to Is Needed.';
							leave sp_Memo_Process_Set;
					End if;*/


                    if @Requesttran_Status is null or @Requesttran_Status = '' then
							set Message = 'Requesttran Status Is Needed.';
							leave sp_Memo_Process_Set;
					End if;

					if ls_Createby is null or ls_Createby = '' then
							set Message = 'Createby  Is Needed.';
							leave sp_Memo_Process_Set;
					End if;


               set @File_Gid=0;


                if @File_Name<>'' and  @File_Name is not null and @File_Path <>'' and  @File_Path is not null then

				set @Classification_json = '';
				set @Classification_json = concat('{
													"Entity_Gid":"',@Entity_Gids,'"
													}');

				call sp_File_Set('Insert', 'a',0,@File_Name,@File_Path,
						@Classification_json, '{}',ls_Createby, @Msg);


					select substring_index(@Msg,',',-1) INTO @File_Test;
					select substring_index(@Msg,',',1) INTO @File_Gid;


					if @File_Test='SUCCESS' then
						set Message = 'SUCCESS';
					else
						rollback;
						set Message = 'FAIL';
						leave sp_Memo_Process_Set;
					end if;

				end if;#@File_Name<>'' and @File_Path <>''


          set  @Requesttran_Gid=0;
          select ifnull(requesttran_gid,0) into @Requesttran_Gid from mem_trn_trequesttran
										where requesttran_requestgid=@Request_Gid
                                             AND requesttran_to=ls_Createby
                                             AND requesttran_by='0' AND requesttran_isremoved='N';


            set sql_safe_updates=0;
            #requesttran_status=''',@Requesttran_Status,''',
            set Query_Update = '';
			set Query_Update = concat('UPDATE  mem_trn_trequesttran
											SET	requesttran_by=',ls_Createby,',
												requesttran_date=NOW(),
												update_by=',ls_Createby,',
												Update_date=NOW()
                                            WHERE requesttran_requestgid=',@Request_Gid,'
												  AND requesttran_to=',ls_Createby,'
												  AND requesttran_isremoved=''N''
									');

							set @Query_Update = Query_Update;
							#SELECT @Query_Update;
							PREPARE stmt FROM @Query_Update;
							EXECUTE stmt;
							set countRow = ROW_COUNT();
							DEALLOCATE PREPARE stmt;



							if  countRow>0 then
								set Message = 'SUCCESS';
							else
								rollback;
								set Message = 'FAIL';
                                leave sp_Memo_Process_Set;
							End if;

                        set Query_Column='' ;
                        set Query_Value='' ;

                        #select  @Requesttran_to;
                        if @Requesttran_to <> '' and @Requesttran_to is not null then
							set Query_Column=concat('requesttran_to');
							set Query_Value=concat(',',@Requesttran_to);
						else
							set Query_Column=concat(',','requesttran_to');
							set Query_Value=concat(',',0);
                        end if;


			#set @Requesttran_Status='PENDING-APPROVAL';
			set Query_Insert = '';
			set Query_Insert = concat('INSERT INTO mem_trn_trequesttran
											 (requesttran_requestgid,requesttran_totype,
											  requesttran_from,requesttran_fromdate,
											  requesttran_comments,requesttran_filegid,
                                              entity_gid,create_by,requesttran_by,requesttran_status ',Query_Column,')
									   select requesttran_requestgid,requesttran_totype,
											  ',ls_Createby,' ,now(),
											  ''',@Comments,''', ',@File_Gid,',
                                              entity_gid,',ls_Createby,',0,''',@Requesttran_Status,'''
                                               ',Query_Value,'
										  from mem_trn_trequesttran
										  WHERE   requesttran_gid=',@Requesttran_Gid,'
												  AND requesttran_isremoved=''N''
									');

							set @Query_Insert = Query_Insert;
							#SELECT @Query_Insert;
							PREPARE stmt FROM @Query_Insert;
							EXECUTE stmt;
							set countRow = ROW_COUNT();
							DEALLOCATE PREPARE stmt;

							if  countRow > 0 then
								set Message = 'SUCCESS';
							else
								rollback;
								set Message = 'FAIL';
                                leave sp_Memo_Process_Set;
							End if;

					if  Message = 'SUCCESS' then
						set Message = 'SUCCESS';
						commit;
					else
						rollback;
						set Message = 'FAIL';
						leave sp_Memo_Process_Set;
					End if;


ELSEIF ls_Action = 'UPDATE' and ls_Type = 'MEMO' and  ls_Sub_Type = 'REQUEST_CLOSED'  then


			select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Request_Gid'))) into @Request_Gid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Request_Closed'))) into @Request_Closed;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,CONCAT('$.Request_Status'))) into @Request_Status;


					if @Request_Gid is null or @Request_Gid = '' then
							set Message = 'Request Gid Is Needed.';
							leave sp_Memo_Process_Set;
					End if;

                    if @Request_Closed is null or @Request_Closed = '' then
							set Message = 'Request Closed Is Needed.';
							leave sp_Memo_Process_Set;
					End if;

                    if @Request_Status is null or @Request_Status = '' then
							set Message = 'Request Status Is Needed.';
							leave sp_Memo_Process_Set;
					End if;

					if ls_Createby is null or ls_Createby = '' then
							set Message = 'Createby  Is Needed.';
							leave sp_Memo_Process_Set;
					End if;



			set sql_safe_updates=0;

            set Query_Update = '';
			set Query_Update = concat('UPDATE  mem_trn_trequest
											SET
												request_closed=''',@Request_Closed,''',
                                                request_status=''',@Request_Status,''',
												update_by=',ls_Createby,',
												Update_date=NOW()
                                            WHERE request_gid=',@Request_Gid,'
												  AND request_isactive=''Y''
												  AND request_isremoved=''N''
									');

							set @Query_Update = Query_Update;
							#SELECT @Query_Update;
							PREPARE stmt FROM @Query_Update;
							EXECUTE stmt;
							set countRow = ROW_COUNT();
							DEALLOCATE PREPARE stmt;



							if  countRow>0 then
								set Message = 'SUCCESS';
                                commit;
							else
								rollback;
								set Message = 'FAIL';
                                leave sp_Memo_Process_Set;
							End if;


ELSEIF ls_Action = 'UPDATE' and ls_Type = 'MEMO_REQUEST' and  ls_Sub_Type = 'EDIT'  then


						select JSON_LENGTH(lj_Details, '$') into @li_json_count;

						if @li_json_count is null or @li_json_count = 0 then
							set Message = 'No Data In Json.';
							leave sp_Memo_Process_Set;
						end if;

			select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Request_Gid'))) into @Request_Gid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Requesttran_To'))) into @Requesttran_To;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Request_Name'))) into @Request_Name;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Request_ION'))) into @Request_ION;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Comments'))) into @Comments;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Subcategory_Gid'))) into @Subcategory_Gid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Approver_Gid'))) into @Approver_Gid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.File_Name'))) into @File_Name;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.File_Path'))) into @File_Path;


						    if @Request_Gid is null or @Request_Gid = '' then
								set Message = 'Request Gid  Is Needed.';
								leave sp_Memo_Process_Set;
							End if;


                            if ls_Createby is null or ls_Createby = '' then
								set Message = 'Createby  Is Needed.';
								leave sp_Memo_Process_Set;
							End if;

           #request_ion,Subcategory_Gid,Approver_Gid,

          # Approver_Gid

            set Query_Column='';

				if @Subcategory_Gid is not null and @Subcategory_Gid <> '' then
					set Query_Column= concat(Query_Column,',request_memosubcategorygid =',@Subcategory_Gid,' ');
				End if;

                if @Request_Name is not null and @Request_Name <> '' then
					set Query_Column= concat(Query_Column,',request_name =''',@Request_Name,''' ');
				End if;

                if @Request_ION is not null and @Request_ION <> '' then
					set Query_Column= concat(Query_Column,',request_ion =''',@Request_ION,''' ');
				End if;

                if @Approver_Gid is not null and @Approver_Gid <> '' then
					set Query_Column= concat(Query_Column,',request_approvergid =',@Approver_Gid,' ');
				End if;


			set Query_Update = '';
			set Query_Update = concat('UPDATE  mem_trn_trequest
											SET	update_by=',ls_Createby,',
												Update_date=NOW()
                                                ',Query_Column,'
                                            WHERE request_gid=',@Request_Gid,'
												  AND request_isactive=''Y''
												  AND request_isremoved=''N''
                                                  AND entity_gid=',@Entity_Gids,'
									');

							set @Query_Update = Query_Update;
							#SELECT @Query_Update;
							PREPARE stmt FROM @Query_Update;
							EXECUTE stmt;
							set countRow = ROW_COUNT();
							DEALLOCATE PREPARE stmt;


							if  countRow>0 then
								set Message = 'SUCCESS';
							else
								rollback;
								set Message = 'FAIL';
                                leave sp_Memo_Process_Set;
							End if;


            select B.requesttran_gid into @Requesttran_Gid from mem_trn_trequest A
						inner join mem_trn_trequesttran B on A.request_gid=B.requesttran_requestgid
							    where B.requesttran_by=0 and A.request_gid=@Request_Gid
                                and B.requesttran_to= ls_Createby
                                and A.request_isactive='Y' and A.request_isremoved='N'
                                and B.requesttran_isremoved='N';

            set Query_Column='';

				if @Comments is not null and @Comments <> '' then
					set Query_Column= concat(Query_Column,',requesttran_comments =''',@Comments,''' ');
				End if;


                if @Approver_Gid is not null and @Approver_Gid <> '' then
					set Query_Column= concat(Query_Column,',requesttran_to =',@Approver_Gid,' ');
				End if;

			   # select Query_Column,@Comments;

			set Query_Update = '';
			set Query_Update = concat('UPDATE  mem_trn_trequesttran
											SET	update_by=',ls_Createby,',
												Update_date=NOW()
                                                ',Query_Column,'
                                            WHERE requesttran_gid=',@Requesttran_Gid,'
												  AND requesttran_isremoved=''N''
                                                  AND entity_gid=',@Entity_Gids,'
									');

							set @Query_Update = Query_Update;
							#SELECT @Query_Update;
							PREPARE stmt FROM @Query_Update;
							EXECUTE stmt;
							set countRow = ROW_COUNT();
							DEALLOCATE PREPARE stmt;


							if  countRow>0 then
								set Message = 'SUCCESS';
							else
								rollback;
								set Message = 'FAIL';
                                leave sp_Memo_Process_Set;
							End if;


          #select @File_Name , @File_Path;

          if @File_Name<>'' and @File_Name is not null or @File_Path <>''  and  @File_Path is not null then

				select request_filegid into @File_Gid from mem_trn_trequest
							    where request_gid=@Request_Gid
                                and request_isactive='Y' and request_isremoved='N';


            set Query_Column='';

				if @File_Name is not null and @File_Name <> '' then
					set Query_Column= concat(Query_Column,',file_name =''',@File_Name,''' ');
				End if;


                if @File_Path is not null and @File_Path <> '' then
					set Query_Column= concat(Query_Column,',file_path =''',@File_Path,''' ');
				End if;


			set Query_Update = '';
			set Query_Update = concat('UPDATE  gal_mst_tfile
											SET	update_by=',ls_Createby,',
												Update_date=NOW()
                                                ',Query_Column,'
                                            WHERE file_gid=',@File_Gid,'
												  AND file_isactive=''Y''
												  AND file_isremoved=''N''
                                                  AND entity_gid=',@Entity_Gids,'
									');

							set @Query_Update = Query_Update;
							#SELECT @Query_Update;
							PREPARE stmt FROM @Query_Update;
							EXECUTE stmt;
							set countRow = ROW_COUNT();
							DEALLOCATE PREPARE stmt;


							if  countRow>0 then
								set Message = 'SUCCESS';
							else
								rollback;
								set Message = 'FAIL';
                                leave sp_Memo_Process_Set;
							end if;
				End if;#if @File_Name<>'' and @File_Name is not null



							if  Message = 'SUCCESS' then
								set Message = 'SUCCESS';
                                commit;
							else
								rollback;
								set Message = 'FAIL';
                                leave sp_Memo_Process_Set;
							End if;


ELSEIF ls_Action = 'UPDATE' and ls_Type = 'MEMO_REQUEST_EDIT' and  ls_Sub_Type = 'ACTIVE_INACTIVE'  then


			select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Request_Gid'))) into @Request_Gid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Active_Flag'))) into @Active_Flag;



						    if @Request_Gid is null or @Request_Gid = '' then
								set Message = 'Request Gid  Is Needed.';
								leave sp_Memo_Process_Set;
							End if;

                             if @Active_Flag is null or @Active_Flag = '' then
								set Message = 'Active Flag  Is Needed.';
								leave sp_Memo_Process_Set;
							End if;


									if @Active_Flag='ACTIVE' then
										set  @Flag_Test=1;
									elseif @Active_Flag='IN_ACTIVE' then
										set  @Flag_Test=1;
									else
										set  @Flag_Test=0;
									End if;

                            if @Flag_Test<>1 then
								set Message = 'This is Invalid Flag ';
								leave sp_Memo_Process_Set;
							End if;

                            if ls_Createby is null or ls_Createby = '' then
								set Message = 'Createby  Is Needed.';
								leave sp_Memo_Process_Set;
							End if;

				SET Query_Column='';
                if @Active_Flag='ACTIVE' then
					SET Query_Column=concat('AND request_isactive=''N''
											 AND request_isremoved=''Y'' ');
					set @Flag='Y';
					set @Flag1='N';
                elseif  @Active_Flag='IN_ACTIVE' then
					SET Query_Column=concat('AND request_isactive=''Y''
											 AND request_isremoved=''N'' ');
					set @Flag='N';
					set @Flag1='Y';
                end if;

			#SELECT Query_Column;

			set Query_Update = '';
			set Query_Update = concat('UPDATE  mem_trn_trequest
											SET	request_isactive=''',@Flag,''',
												request_isremoved=''',@Flag1,''',
												update_by=',ls_Createby,',
												Update_date=NOW()
                                            WHERE request_gid=',@Request_Gid,'
												   ',Query_Column,'
                                                  AND entity_gid=',@Entity_Gids,'
									');

							set @Query_Update = Query_Update;
							#SELECT @Query_Update;
							PREPARE stmt FROM @Query_Update;
							EXECUTE stmt;
							set countRow = ROW_COUNT();
							DEALLOCATE PREPARE stmt;


							if  countRow>0 then
								set Message = 'SUCCESS';
                                COMMIT;
							else
								rollback;
								set Message = 'FAIL';
                                leave sp_Memo_Process_Set;
							End if;



END IF;

END