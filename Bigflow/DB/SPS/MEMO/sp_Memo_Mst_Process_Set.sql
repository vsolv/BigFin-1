CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Memo_Mst_Process_Set`(IN `ls_Action` varchar(32),IN `ls_Type` varchar(32),
IN `ls_Sub_Type` varchar(32),IN `lj_Details` json,IN `lj_Status` Json,
IN `lj_Classification` json,IN `ls_Createby` varchar(16),OUT `Message` varchar(1024))
sp_Memo_Mst_Process_Set:BEGIN
### Bala Mar 01 2020 - Created
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
                leave sp_Memo_Mst_Process_Set;
        End if;


start transaction;
set autocommit=0;
set autocommit=off;


IF ls_Action = 'INSERT' and ls_Type = 'MEMO' and  ls_Sub_Type = 'CATEGORY'  then


						select JSON_LENGTH(lj_Details, '$') into @li_json_count;

						if @li_json_count is null or @li_json_count = 0 then
							set Message = 'No Data In Json.';
							leave sp_Memo_Mst_Process_Set;
						end if;



                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Memo_Cat_Name'))) into @Memo_Cat_Name;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Memo_Cat_Remark'))) into @Memo_Cat_Remark;


                            if @Memo_Cat_Name is null or @Memo_Cat_Name = '' then
								set Message = 'Memo Category Name Is Needed.';
								leave sp_Memo_Mst_Process_Set;
							End if;


                            if ls_Createby is null or ls_Createby = '' then
								set Message = 'Createby  Is Needed.';
								leave sp_Memo_Mst_Process_Set;
							End if;


			select exists(select memocategory_code from mem_mst_tmemocategory) into @Test;
			#select  @Test;

			select max(substr(memocategory_code,2)) from mem_mst_tmemocategory  into @Category_Code;
			#select  @Category_Code;


            if @Test=0 then
				call sp_Generatecode_Get('WITHOUT_DATE', 'C', '000','000', @Message);
				select @Message into @Category_Code;
			else
				call sp_Generatecode_Get('WITHOUT_DATE', 'C', '000',@Category_Code, @Message);
				select @Message into @Category_Code;
			end if;

            #select  @Category_Code,@Memo_Cat_Remark;


            set Query_Column='';
            set Query_Value='';

            if @Memo_Cat_Remark is not null and @Memo_Cat_Remark<>'' then
					set Query_Column=concat(',memocategory_remarks');
					set Query_Value=concat(' ,''',@Memo_Cat_Remark,''' ');
            end if;


        #select @Category_Code,  Query_Column,Query_Value;

			set Query_Insert = '';
			set Query_Insert = concat('INSERT INTO mem_mst_tmemocategory
											 (memocategory_code,memocategory_name,
											  entity_gid,create_by ',Query_Column,' )
									   VALUES(''',@Category_Code,''',''',@Memo_Cat_Name,''',
                                              ',@Entity_Gids,',',ls_Createby,' ',Query_Value,')
									   ');

							set @Insert_query = Query_Insert;
							#SELECT @Insert_query;
							PREPARE stmt FROM @Insert_query;
							EXECUTE stmt;
							set countRow = ROW_COUNT();
							DEALLOCATE PREPARE stmt;


							if  countRow>0 then
								set Message = 'SUCCESS';
								commit;
							else
								rollback;
								set Message = 'FAIL';
                                leave sp_Memo_Mst_Process_Set;
							End if;



ELSEIF ls_Action = 'INSERT' and ls_Type = 'MEMO' and  ls_Sub_Type = 'SUB_CATEGORY'  then


						select JSON_LENGTH(lj_Details, '$') into @li_json_count;

						if @li_json_count is null or @li_json_count = 0 then
							set Message = 'No Data In Json.';
							leave sp_Memo_Mst_Process_Set;
						end if;



                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Memo_Cat_Gid'))) into @Memo_Cat_Gid;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Memo_SubCat_Name'))) into @Memo_SubCat_Name;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Memo_SubCat_Remark'))) into @Memo_SubCat_Remark;



                            if @Memo_Cat_Gid is null or @Memo_Cat_Gid = '' then
								set Message = 'Memo Category Gid Is Needed.';
								leave sp_Memo_Mst_Process_Set;
							End if;

                            if @Memo_SubCat_Name is null or @Memo_SubCat_Name = '' then
								set Message = 'Memo SubCategory Name Is Needed.';
								leave sp_Memo_Mst_Process_Set;
							End if;

							# Memo_SubCat_Remark Optional

                            if ls_Createby is null or ls_Createby = '' then
								set Message = 'Createby  Is Needed.';
								leave sp_Memo_Mst_Process_Set;
							End if;


			select exists(select memosubcategory_code from mem_mst_tmemosubcategory) into @Test;

			select max(substr(memosubcategory_code,2)) from mem_mst_tmemosubcategory  into @Sub_Cat_Code;


            if @Test=0 then
				call sp_Generatecode_Get('WITHOUT_DATE', 'B', '000','000', @Message);
				select @Message into @Sub_Cat_Code;
			else
				call sp_Generatecode_Get('WITHOUT_DATE', 'B', '000',@Sub_Cat_Code, @Message);
				select @Message into @Sub_Cat_Code;
			end if;

					set Query_Column='';
					set Query_Value='';

					if @Memo_SubCat_Remark is not null and @Memo_SubCat_Remark<>'' then
							set Query_Column=concat(',memosubcategory_remarks');
							set Query_Value=concat(' ,''',@Memo_SubCat_Remark,''' ');
					end if;



			set Query_Insert = '';
			set Query_Insert = concat('INSERT INTO mem_mst_tmemosubcategory
											 (memosubcategory_memocategorygid,
                                              memosubcategory_code, memosubcategory_name,
                                              entity_gid,create_by ',Query_Column,')
									   VALUES(',@Memo_Cat_Gid,',''',@Sub_Cat_Code,''',
											  ''',@Memo_SubCat_Name,''',
											  ',@Entity_Gids,',',ls_Createby,' ',Query_Value,')
									   ');

							set @Query_Insert = Query_Insert;
							#SELECT @Query_Insert;
							PREPARE stmt FROM @Query_Insert;
							EXECUTE stmt;
							set countRow = ROW_COUNT();
							DEALLOCATE PREPARE stmt;


							if  countRow>0 then
								set Message = 'SUCCESS';
                                commit;
							else
								rollback;
								set Message = 'FAIL';
                                leave sp_Memo_Mst_Process_Set;
							End if;




ELSEIF ls_Action = 'UPDATE' and ls_Type = 'MEMO_CATEGORY' and  ls_Sub_Type = 'EDIT'  then


			    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Memo_Cat_Gid'))) into @Memo_Cat_Gid;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Memo_Cat_Name'))) into @Memo_Cat_Name;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Memo_Cat_Remark'))) into @Memo_Cat_Remark;


                            if @Memo_Cat_Gid is null or @Memo_Cat_Gid = '' then
								set Message = 'Memo Category Gid  Is Needed.';
								leave sp_Memo_Mst_Process_Set;
							End if;

                            if ls_Createby is null or ls_Createby = '' then
								set Message = 'Createby  Is Needed.';
								leave sp_Memo_Mst_Process_Set;
							End if;

				SET Query_Column='';
                if @Memo_Cat_Name<>''  and @Memo_Cat_Name is not null then
					SET Query_Column=concat(Query_Column,' ,memocategory_name=''',@Memo_Cat_Name,'''  ');

                end if;

                if @Memo_Cat_Remark<>''  and @Memo_Cat_Remark is not null then
					SET Query_Column=concat(Query_Column,' ,memocategory_remarks=''',@Memo_Cat_Remark,''' ');

                end if;

			#SELECT Query_Column;

			set Query_Update = '';
			set Query_Update = concat('UPDATE  mem_mst_tmemocategory
											SET	update_by=',ls_Createby,',
												Update_date=NOW()
                                                ',Query_Column,'
                                            WHERE memocategory_gid=',@Memo_Cat_Gid,'
												  AND memocategory_isactive=''Y''
												  AND memocategory_isremoved=''N''
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
                                leave sp_Memo_Mst_Process_Set;
							End if;




ELSEIF ls_Action = 'UPDATE' and ls_Type = 'MEMO_SUB_CATEGORY' and  ls_Sub_Type = 'EDIT'  then


                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Memo_Cat_Gid'))) into @Memo_Cat_Gid;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Memo_SubCat_Gid'))) into @Memo_SubCat_Gid;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Memo_SubCat_Name'))) into @Memo_SubCat_Name;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Memo_SubCat_Remark'))) into @Memo_SubCat_Remark;


                            if @Memo_SubCat_Gid is null or @Memo_SubCat_Gid = '' then
								set Message = 'Memo SubCategory Gid  Is Needed.';
								leave sp_Memo_Mst_Process_Set;
							End if;

                            if ls_Createby is null or ls_Createby = '' then
								set Message = 'Createby  Is Needed.';
								leave sp_Memo_Mst_Process_Set;
							End if;

				SET Query_Column='';
                if @Memo_SubCat_Name<>''  and @Memo_SubCat_Name is not null then
					SET Query_Column=concat(Query_Column,' ,memosubcategory_name=''',@Memo_SubCat_Name,'''  ');

                end if;

                if @Memo_SubCat_Remark<>''  and @Memo_SubCat_Remark is not null then
					SET Query_Column=concat(Query_Column,' ,memosubcategory_remarks=''',@Memo_SubCat_Remark,''' ');

                end if;

                if @Memo_Cat_Gid<>''  and @Memo_Cat_Gid is not null then
					SET Query_Column=concat(Query_Column,' ,memosubcategory_memocategorygid=''',@Memo_Cat_Gid,''' ');

                end if;

			#SELECT Query_Column;

			set Query_Update = '';
			set Query_Update = concat('UPDATE  mem_mst_tmemosubcategory
											SET	update_by=',ls_Createby,',
												Update_date=NOW()
                                                ',Query_Column,'
                                            WHERE memosubcategory_gid=',@Memo_SubCat_Gid,'
												  AND memosubcategory_isactive=''Y''
												  AND memosubcategory_isremoved=''N''
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
                                leave sp_Memo_Mst_Process_Set;
							End if;






ELSEIF ls_Action = 'UPDATE' and ls_Type = 'MEMO_CATEGORY' and  ls_Sub_Type = 'ACTIVE_INACTIVE'  then

			select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Memo_Cat_Gid'))) into @Memo_Cat_Gid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Active_Flag'))) into @Active_Flag;



						    if @Memo_Cat_Gid is null or @Memo_Cat_Gid = '' then
								set Message = 'Memo Category Gid  Is Needed.';
								leave sp_Memo_Mst_Process_Set;
							End if;

                            if @Active_Flag is null or @Active_Flag = '' then
								set Message = 'Active Flag  Is Needed.';
								leave sp_Memo_Mst_Process_Set;
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
								leave sp_Memo_Mst_Process_Set;
							End if;

                            if ls_Createby is null or ls_Createby = '' then
								set Message = 'Createby  Is Needed.';
								leave sp_Memo_Mst_Process_Set;
							End if;

				SET Query_Column='';
                if @Active_Flag='ACTIVE' then
					SET Query_Column=concat('AND memocategory_isactive=''N''
											 AND memocategory_isremoved=''Y'' ');
					set @Flag='Y';
					set @Flag1='N';
                elseif  @Active_Flag='IN_ACTIVE' then
					SET Query_Column=concat('AND memocategory_isactive=''Y''
											 AND memocategory_isremoved=''N'' ');
					set @Flag='N';
					set @Flag1='Y';
                end if;

			#SELECT Query_Column;

			set Query_Update = '';
			set Query_Update = concat('UPDATE  mem_mst_tmemocategory
											SET	memocategory_isactive=''',@Flag,''',
												memocategory_isremoved=''',@Flag1,''',
												update_by=',ls_Createby,',
												Update_date=NOW()
                                            WHERE memocategory_gid=',@Memo_Cat_Gid,'
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
                                leave sp_Memo_Mst_Process_Set;
							End if;






ELSEIF ls_Action = 'UPDATE' and ls_Type = 'MEMO_SUB_CATEGORY' and  ls_Sub_Type = 'ACTIVE_INACTIVE'  then


			select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Memo_SubCat_Gid'))) into @Memo_SubCat_Gid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Active_Flag'))) into @Active_Flag;



						    if @Memo_SubCat_Gid is null or @Memo_SubCat_Gid = '' then
								set Message = 'Memo SubCategory Gid Is Needed.';
								leave sp_Memo_Mst_Process_Set;
							End if;

                            if @Active_Flag is null or @Active_Flag = '' then
								set Message = 'Active Flag  Is Needed.';
								leave sp_Memo_Mst_Process_Set;
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
								leave sp_Memo_Mst_Process_Set;
							End if;

                            if ls_Createby is null or ls_Createby = '' then
								set Message = 'Createby  Is Needed.';
								leave sp_Memo_Mst_Process_Set;
							End if;

				SET Query_Column='';
                if @Active_Flag='ACTIVE' then
					SET Query_Column=concat('AND memosubcategory_isactive=''N''
											 AND memosubcategory_isremoved=''Y'' ');
					set @Flag='Y';
					set @Flag1='N';
                elseif  @Active_Flag='IN_ACTIVE' then
					SET Query_Column=concat('AND memosubcategory_isactive=''Y''
											 AND memosubcategory_isremoved=''N'' ');
					set @Flag='N';
					set @Flag1='Y';
                end if;

			#SELECT Query_Column;

			set Query_Update = '';
			set Query_Update = concat('UPDATE  mem_mst_tmemosubcategory
											SET	memosubcategory_isactive=''',@Flag,''',
												memosubcategory_isremoved=''',@Flag1,''',
												update_by=',ls_Createby,',
												Update_date=NOW()
                                            WHERE memosubcategory_gid=',@Memo_SubCat_Gid,'
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
                                leave sp_Memo_Mst_Process_Set;
							End if;



END IF;

END