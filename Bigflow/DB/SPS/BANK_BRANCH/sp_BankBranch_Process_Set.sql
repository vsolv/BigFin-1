CREATE DEFINER=`developer`@`%` PROCEDURE `sp_BankBranch_Process_Set`(IN `ls_Action` varchar(32),IN `ls_Type` varchar(32),
IN `ls_Sub_Type` varchar(32),IN `lj_Details` json,
IN `lj_Classification` json,IN `ls_Createby` varchar(16),OUT `Message` varchar(1024))
sp_BankBranch_Process_Set:BEGIN
### Bala Mar 12 2020 - Created
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
                leave sp_BankBranch_Process_Set;
        End if;


start transaction;
set autocommit=0;
set autocommit=off;


IF ls_Action = 'INSERT' and ls_Type = 'BANK_BRANCH' and  ls_Sub_Type = 'MAKING'  then


				select JSON_LENGTH(lj_Details, '$') into @li_json_count;

						if @li_json_count is null or @li_json_count = 0 then
							set Message = 'No Data In Json.';
							leave sp_BankBranch_Process_Set;
						end if;


                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Address1'))) into @Address1;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Address2'))) into @Address2;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Address3'))) into @Address3;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Address_Ref_Code'))) into @Address_Ref_Code;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Address_Pincode')))into @Address_Pincode;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Address_District_Gid')))into @Address_District_Gid;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Address_City_Gid')))into @Address_City_Gid;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Address_State_Gid')))into @Address_State_Gid;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Bank_Name')))into @Bank_Name;
				#select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.BankBranch_Code')))into @BankBranch_Code;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.BankBranch_Name')))into @BankBranch_Name;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.BankBr_ifscCode')))into @BankBr_ifscCode;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.BankBr_MicroCode')))into @BankBr_MicroCode;

                select ifnull(bank_gid,0)  into @Bank_Gid from gal_mst_tbank
							where bank_name=@Bank_Name
								  and bank_isactive='Y'
								  and bank_isremoved='N';


                            if @Bank_Gid = 0 then
								set Message = 'Invalid Bank Name';
								leave sp_BankBranch_Process_Set;
							End if;

                            if @Bank_Name is null or @Bank_Name = '' then
								set Message = 'Bank Name Needed.';
								leave sp_BankBranch_Process_Set;
							End if;

                            if @BankBranch_Name is null or @BankBranch_Name = '' then
								set Message = 'BankBranch Name Needed.';
								leave sp_BankBranch_Process_Set;
							End if;

                            if @BankBr_ifscCode is null or @BankBr_ifscCode = '' then
								set Message = 'BankBranch ifscCode Needed.';
								leave sp_BankBranch_Process_Set;
							End if;

                            if @BankBr_MicroCode is null or @BankBr_MicroCode = '' then
								set Message = 'BankBranch MicroCode Needed.';
								leave sp_BankBranch_Process_Set;
							End if;

                            if ls_Createby is null or ls_Createby = '' then
								set Message = 'Createby Is Needed.';
								leave sp_BankBranch_Process_Set;
							End if;

						set Query_Column = '';
                        set Query_Value = '';

                        if @Address1 is not null and @Address1 <> '' then
							set Query_Column = concat(Query_Column,',address_1');
							set Query_Value = concat(Query_Value,',','''',@Address1,'''');
						End if;

                        if @Address2 is not null and @Address2 <> '' then
							set Query_Column = concat(Query_Column,',address_2');
							set Query_Value = concat(Query_Value,',','''',@Address2,'''');
						End if;

                        if @Address3 is not null and @Address3 <> '' then
							set Query_Column = concat(Query_Column,',address_3');
							set Query_Value = concat(Query_Value,',','''',@Address3,'''');
						End if;


                        if @Address_Pincode is not null and @Address_Pincode <> '' then
							set Query_Column = concat(Query_Column,',address_pincode');
							set Query_Value = concat(Query_Value,',',@Address_Pincode);
						End if;

                        if @Address_City_Gid is not null and @Address_City_Gid <> '' then
							set Query_Column = concat(Query_Column,',address_city_gid');
							set Query_Value = concat(Query_Value,',',@Address_City_Gid);
						End if;

                        if @Address_State_Gid is not null and @Address_State_Gid <> '' then
							set Query_Column = concat(Query_Column,',address_state_gid');
							set Query_Value = concat(Query_Value,',',@Address_State_Gid);
						End if;

			set @BankBranch_Addrs_Gid=0;

            if @Address_District_Gid<>'' and @Address_District_Gid is not null then

			set Query_Insert = '';
			set Query_Insert = concat('INSERT INTO gal_mst_taddress
											(address_ref_code,address_district_gid,
                                            entity_gid,create_by ',Query_Column,' )
									   VALUES(''',@Address_Ref_Code,''',',@Address_District_Gid,',
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
                                set @BankBranch_Addrs_Gid= LAST_INSERT_ID();
							else
								rollback;
								set Message = 'FAIL';
                                leave sp_BankBranch_Process_Set;
							End if;
				End if; #if @Address_District_Gid<>'' and @Address_District_Gid is not null then



			select exists(select bankbranch_code from gal_mst_tbankbranch) into @Test;

			#select max(substr(bankbranch_code,3)) from gal_mst_tbankbranch  into @BankBr_Code;
			select bankbranch_code from gal_mst_tbankbranch
							ORDER BY bankbranch_gid DESC LIMIT 1  into @BankBr_Code;

            if @Test=0 then
				call sp_Generatecode_Get('WITHOUT_DATE', '', '000','000', @Message);
				select @Message into @BankBranch_Code;
			else
				call sp_Generatecode_Get('WITHOUT_DATE', '', '000',@BankBr_Code, @Message);
				select @Message into @BankBranch_Code;
			end if;


                        /*select @Bank_Gid,@BankBranch_Code,
											 @BankBranch_Name,@BankBr_ifscCode,
											 @BankBr_MicroCode,@BankBranch_Addrs_Gid,
                                              @Entity_Gids,ls_Createby;*/

            set Query_Insert = '';
			set Query_Insert = concat('INSERT INTO gal_mst_tbankbranch
											(bankbranch_bank_gid, bankbranch_code,
											 bankbranch_name, bankbranch_ifsccode,
                                             bankbranch_microcode,bankbranch_address_gid,
											 entity_gid, create_by)
									   VALUES(',@Bank_Gid,',''',@BankBranch_Code,''',
											 ''',@BankBranch_Name,''',''',@BankBr_ifscCode,''',
											 ''',@BankBr_MicroCode,''',',@BankBranch_Addrs_Gid,',
                                              ',@Entity_Gids,',',ls_Createby,')
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
                                leave sp_BankBranch_Process_Set;
							End if;


					if  Message = 'SUCCESS' then
						set Message = 'SUCCESS';
						COMMIT;
					else
						rollback;
						set Message = 'FAIL';
						leave sp_BankBranch_Process_Set;
					End if;


ELSEIF ls_Action = 'UPDATE' and ls_Type = 'BANK_BRANCH' and  ls_Sub_Type = 'EDIT'  then

				select JSON_LENGTH(lj_Details, '$') into @li_json_count;

						if @li_json_count is null or @li_json_count = 0 then
							set Message = 'No Data In Json.';
							leave sp_BankBranch_Process_Set;
						end if;


				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.BankBranch_Gid')))into @BankBranch_Gid;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Bank_Name')))into @Bank_Name;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.BankBranch_Name')))into @BankBranch_Name;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.BankBr_ifscCode')))into @BankBr_ifscCode;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.BankBr_MicroCode')))into @BankBr_MicroCode;

                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Address1'))) into @Address1;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Address2'))) into @Address2;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Address3'))) into @Address3;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Address_Pincode')))into @Address_Pincode;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Address_District_Gid')))into @Address_District_Gid;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Address_City_Gid')))into @Address_City_Gid;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Address_State_Gid')))into @Address_State_Gid;


						select ifnull(bank_gid,0)  into @Bank_Gid from gal_mst_tbank
							where bank_name=@Bank_Name
								  and bank_isactive='Y'
								  and bank_isremoved='N';



							if ls_Createby is null or ls_Createby = '' then
								set Message = 'Createby Is Needed.';
								leave sp_BankBranch_Process_Set;
							End if;


							if  @Bank_Gid = 0 then
								set Message = 'Invalid Bank Name';
								leave sp_BankBranch_Process_Set;
							End if;

                            if @BankBranch_Gid is null or @BankBranch_Gid = '' then
								set Message = 'BankBranch Gid Is Needed.';
								leave sp_BankBranch_Process_Set;
							End if;


						set Query_Column = '';
                        set Query_Value = '';

                       # select @Bank_Gid,@BankBranch_Name,@BankBr_ifscCode,@bankbranch_microcode;

                        if @Bank_Gid is not null and @Bank_Gid <> '' then
							set Query_Column = concat(Query_Column,',bankbranch_bank_gid= ',@Bank_Gid,' ');
						End if;

                        if @BankBranch_Name is not null and @BankBranch_Name <> '' then
							set Query_Column = concat(Query_Column,',bankbranch_name= ''',@BankBranch_Name,''' ');
						End if;

                        if @BankBr_ifscCode is not null and @BankBr_ifscCode <> '' then
							set Query_Column = concat(Query_Column,',bankbranch_ifsccode= ''',@BankBr_ifscCode,''' ');
						End if;

                        if @BankBr_MicroCode is not null and @BankBr_MicroCode <> '' then
							set Query_Column = concat(Query_Column,',bankbranch_microcode= ''',@BankBr_MicroCode,''' ');
						End if;


                        /*select bank_gid  into @Bank_Gid from gal_mst_tbank
							where bank_name=@Bank_Name
								  and bank_isactive='Y'
								  and bank_isremoved='N';*/


            set sql_safe_updates=0;
            set Query_Update = '';
			set Query_Update = concat('UPDATE  gal_mst_tbankbranch
											SET	Update_by=',ls_Createby,',
												Update_date=NOW()
                                                ',Query_Column,'
                                            WHERE bankbranch_gid=',@BankBranch_Gid,'
												  AND bankbranch_isactive=''Y''
												  AND bankbranch_isremoved=''N''
									');

							set @Query_Update = Query_Update;
							#SELECT @Query_Update;
							PREPARE stmt FROM @Query_Update;
							EXECUTE stmt;
							set countRow = ROW_COUNT();
							DEALLOCATE PREPARE stmt;



						set Query_Column = '';

                        if @Address1 is not null and @Address1 <> '' then
							set Query_Column = concat(Query_Column,',address_1=''',@Address1,'''');
						End if;

                        if @Address2 is not null and @Address2 <> '' then
							set Query_Column = concat(Query_Column,',address_2=''',@Address2,'''');
						End if;

                        if @Address3 is not null and @Address3 <> '' then
							set Query_Column = concat(Query_Column,',address_3=''',@Address3,'''');
						End if;

                        if @Address_Pincode is not null and @Address_Pincode <> '' then
							set Query_Column = concat(Query_Column,',address_pincode=',@Address_Pincode);
						End if;

                        if @Address_City_Gid is not null and @Address_City_Gid <> '' then
							set Query_Column = concat(Query_Column,',address_city_gid=',@Address_City_Gid);
						End if;

                        if @Address_State_Gid is not null and @Address_State_Gid <> '' then
							set Query_Column = concat(Query_Column,',address_state_gid=',@Address_State_Gid);
						End if;


                        select bankbranch_address_gid  into @BankBr_Addrs_Gid from gal_mst_tbankbranch
							where bankbranch_gid=@BankBranch_Gid
								  and bankbranch_isactive='Y'
								  and bankbranch_isremoved='N';



			set sql_safe_updates=0;
            set Query_Update = '';
			set Query_Update = concat('UPDATE  gal_mst_taddress
											SET	Update_by=',ls_Createby,',
												Update_date=NOW()
                                                ',Query_Column,'
                                            WHERE address_gid=',@BankBr_Addrs_Gid,'	');

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
                                leave sp_BankBranch_Process_Set;
							End if;


					if  Message = 'SUCCESS' then
						set Message = 'SUCCESS';
                        COMMIT;
					else
						rollback;
						set Message = 'FAIL';
                        leave sp_BankBranch_Process_Set;
					End if;




ELSEIF ls_Action = 'UPDATE' and ls_Type = 'BANK_BRANCH' and  ls_Sub_Type = 'ACTIVE_INACTIVE'  then



				select JSON_LENGTH(lj_Details, '$') into @li_json_count;

						if @li_json_count is null or @li_json_count = 0 then
							set Message = 'No Data In Json.';
							leave sp_BankBranch_Process_Set;
						end if;

				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.BankBranch_Gid')))into @BankBranch_Gid;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Active_Flag')))into @Active_Flag;


							if @BankBranch_Gid is null or @BankBranch_Gid = '' then
								set Message = 'BankBranch Gid Is Needed.';
								leave sp_BankBranch_Process_Set;
							End if;

							if ls_Createby is null or ls_Createby = '' then
								set Message = 'Createby Is Needed.';
								leave sp_BankBranch_Process_Set;
							End if;

                            if @Active_Flag is null or @Active_Flag = '' then
								set Message = 'Active Flag  Is Needed.';
								leave sp_BankBranch_Process_Set;
							End if;

									if @Active_Flag='ACTIVE' then
										set  @Flag_Test=1;
									elseif @Active_Flag='IN_ACTIVE' then
										set  @Flag_Test=1;
									else
										set  @Flag_Test=0;
									End if;


                            if @Flag_Test=0 then
								set Message = 'This is Invalid Flag ';
								leave sp_BankBranch_Process_Set;
							End if;

                            if ls_Createby is null or ls_Createby = '' then
								set Message = 'Createby  Is Needed.';
								leave sp_BankBranch_Process_Set;
							End if;

				SET Query_Column='';
                if @Active_Flag='IN_ACTIVE' then
					SET Query_Column=concat('AND bankbranch_isactive=''Y''
											 AND bankbranch_isremoved=''N'' ');
					set @Flag='N';
					set @Flag1='Y';
                elseif  @Active_Flag='ACTIVE' then
					SET Query_Column=concat('AND bankbranch_isactive=''N''
											 AND bankbranch_isremoved=''Y'' ');
					set @Flag='Y';
					set @Flag1='N';
                end if;



			set sql_safe_updates=0;
            set Query_Update = '';
			set Query_Update = concat('UPDATE  gal_mst_tbankbranch
											SET	bankbranch_isactive=''',@Flag,''',
												bankbranch_isremoved=''',@Flag1,''',
                                                Update_by=',ls_Createby,',
												Update_date=NOW()
                                            WHERE bankbranch_gid=',@BankBranch_Gid,'
                                            ',Query_Column,'

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
                                leave sp_BankBranch_Process_Set;
							End if;



					/*if  Message = 'SUCCESS' then
						set Message = 'SUCCESS';
						COMMIT;
					else
						rollback;
						set Message = 'FAIL';
						leave sp_BankBranch_Process_Set;
					End if;*/



END IF;


END