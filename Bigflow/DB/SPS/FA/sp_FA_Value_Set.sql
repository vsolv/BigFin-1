CREATE DEFINER=`developer`@`%` PROCEDURE `galley`.`sp_FA_Value_Set`(IN `ls_Action` varchar(32),
IN `ls_Type` varchar(32),IN `ls_Sub_Type` varchar(32),IN `lj_Details` json,IN `lj_Classification` json,
IN `ls_Createby` varchar(32),OUT `Message` varchar(1024))
sp_FA_TFR_Asset_Set:BEGIN

#### Bala Oct 17 2019
### Ramesh Nov 7 2019

Declare errno int;
Declare msg varchar(1000);
Declare countRow int;
Declare Query_Insert varchar(9000);
Declare Query_Update varchar(9000);

DECLARE EXIT HANDLER FOR SQLEXCEPTION,sqlwarning

	 BEGIN
		GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
		set Message = concat(errno , msg);
		ROLLBACK;
     END;

	select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid[0]'))) into @Entity_Gid;

             if @Entity_Gid is  null or @Entity_Gid = 0 or @Entity_Gid = '' then
					set Message = 'Entity Gid Is Needed.';
                    leave sp_FA_TFR_Asset_Set;
             End if;

if ls_Type = 'VALUE_MAKER' and  ls_Sub_Type = 'TRAN' then
      if ls_Action = 'INSERT' then

				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_Gid[0]'))) into @Asset_Gid;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_Value[0]'))) into @Asset_Value;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_Value_Date[0]'))) into @Asset_Value_Date;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_Value_Reason'))) into @Asset_Value_Reason;


				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Ref_Name'))) into @Trn_Ref_Name;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_To_Type'))) into @Trn_To_Type;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Role_Name'))) into @Trn_Role_Name;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Remarks'))) into @Trn_Remarks;

							if @Asset_Gid is null or cast(@Asset_Gid as decimal(16,2))  = 0 then
								set Message = 'Asset Gid Is Needed.';
								leave sp_FA_TFR_Asset_Set;
							End if;

                            if @Asset_Value is null or @Asset_Value = '' then
								set Message = 'Asset Value Is Needed.';
								leave sp_FA_TFR_Asset_Set;
							End if;

                            if @Asset_Value_Date is null or @Asset_Value_Date = '' then
								set Message = 'Asset Value Date Is Needed.';
								leave sp_FA_TFR_Asset_Set;
							End if;

                            if @Asset_Value_Reason is null or @Asset_Value_Reason = '' then
								set Message = 'Asset Value Reason Is Needed.';
								leave sp_FA_TFR_Asset_Set;
							End if;


					set @Value_Status='SUBMITTED';
					set Query_Insert = '';
					set Query_Insert = concat('
							INSERT INTO fa_trn_tassetvalue
									(assetvalue_assetdetailsid, assetvalue_date,
									 assetvalue_status, assetvalue_reason,
									 assetvalue_value,assetvalue_oldvalue,
									 entity_gid,create_by)
							(select assetdetails_id,''',@Asset_Value_Date,''',
									''',@Value_Status,''',''',@Asset_Value_Reason,''',
									''',@Asset_Value,''',assetdetails_value,
                                    entity_gid,''',ls_Createby,'''
							from fa_trn_tassetdetails
							where assetdetails_gid in (',@Asset_Gid,')
							)'                 );

							set @Insert_query = Query_Insert;
							#SELECT @Insert_query;
							PREPARE stmt FROM @Insert_query;
							EXECUTE stmt;
							set countRow = (select ROW_COUNT());
							DEALLOCATE PREPARE stmt;

                              if countRow > 0 then
                                  select LAST_INSERT_ID() into @Asset_Value_Maxgid ;

                                  #### Update im Tmp Table
                                  set sql_safe_updates = 0;
                                  Update fa_tmp_tassetdetails set assetdetails_assetvaluegid = @Asset_Value_Maxgid,
                                   assetdetails_value = @Asset_Value
                                  where assetdetails_mainassetdetailsgid = @Asset_Gid;

                                  set countRow = (select ROW_COUNT());

										if  countRow <= 0 then
											set Message = 'FAIL On Asset Temp Data Update.';
                                            leave sp_FA_TFR_Asset_Set;
                                        End if;

									set Message = 'SUCCESS';

                                   # select @Trn_Ref_Name,@Asset_Value_Maxgid,'NEW',
										 #  @Trn_To_Type,@Trn_Role_Name,@Asset_Value_Reason,@Entity_Gid,ls_Createby;


                                    ## TO DO
						call sp_Trans_Set('Insert',@Trn_Ref_Name,@Asset_Value_Maxgid,'NEW',
										  @Trn_To_Type,@Trn_Role_Name,@Asset_Value_Reason,
                                          @Entity_Gid,ls_Createby,@message);
									select @message into @tran;
									#select @message; #remove it
									if @tran <>0 or @tran <> '' then
											set Message = 'SUCCESS';
									else
											set Message = 'FAIL in tran';
											leave sp_FA_TFR_Asset_Set;
									end if;
                              else
                                    set Message = 'FAIL';
                              End if;

      End if;

elseif ls_Type = 'VALUE_CHECKER' and  ls_Sub_Type = 'CHECKER' then
         if ls_Action = 'UPDATE' then

				 select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_Detail_Gids'))) into @Asset_Detail_Gids;### Approve - Trn : reject - tmp
               select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_Value_Gid'))) into @Asset_Value_Gid;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_Value_Status'))) into @Asset_Value_Status;


                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Ref_Name'))) into @Trn_Ref_Name;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_To_Type'))) into @Trn_To_Type;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Role_Name'))) into @Trn_Role_Name;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Remarks'))) into @Trn_Remarks;

                if @Asset_Value_Gid is null or cast(@Asset_Value_Gid as decimal(16,2))  = 0 then
						set Message = 'Asset_Value Gid Is Needed.';
                        leave sp_FA_TFR_Asset_Set;
                End if;

                if @Asset_Value_Status is null or @Asset_Value_Status = '' then
						set Message = 'Asset_Value Status Is Needed.';
                        leave sp_FA_TFR_Asset_Set;
                End if;

               set Query_Update = '';
               set Query_Update = concat('Update fa_trn_tassetvalue
												set assetvalue_status = ''',@Asset_Value_Status,''' ,
                                                update_by = ''',ls_Createby,''' ,
                                                update_date = current_timestamp()
											Where assetvalue_gid = ',@Asset_Value_Gid,'
                                            and entity_gid = ',@Entity_Gid,'
												');

									set @Query_Update = '';
									set @Query_Update = Query_Update;
								   # select @Query_Update; ### Remove IT
									PREPARE stmt FROM @Query_Update;
									EXECUTE stmt;
									set countRow = (select ROW_COUNT());
									DEALLOCATE PREPARE stmt;

									if countRow <= 0 then
										set Message = 'Error On Value Status Update.';
										leave sp_FA_TFR_Asset_Set;
									 elseif    countRow > 0 then
										set Message = 'SUCCESS';
									End if;

			set Query_Update = '';
			set Query_Update = concat('delete from fa_tmp_tassetdetails
											where assetdetails_gid in( ',@Asset_Detail_Gids,') ');

									set @Query_Update = '';
									set @Query_Update = Query_Update;
								    #select @Query_Update; ### Remove IT
									PREPARE stmt FROM @Query_Update;
									EXECUTE stmt;
									set countRow = (select ROW_COUNT());
									DEALLOCATE PREPARE stmt;

									if countRow <= 0 then
										set Message = 'Error On Value Temp Value Delete.';
										leave sp_FA_TFR_Asset_Set;
									 elseif    countRow > 0 then
										set Message = 'SUCCESS';
									End if;
             /*
              If @Asset_Value_Status='REJECTED'  then


                                SET SQL_SAFE_UPDATES = 0;
						set Query_Update = '';
						set Query_Update = concat('update fa_trn_tassetdetails
										set
											update_date=now(),
											update_by=',ls_Createby,',
											assetdetails_requestfor=''''
										where assetdetails_id in (',@AssetDetails_Id,')
									');
								set @Update_query = Query_Update;
								#SELECT @Update_query;
								PREPARE stmt FROM @Update_query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;

                              if countRow > 0 then
									set Message = 'SUCCESS';
                               else
                                    set Message = 'FAIL In Asset Value Reject';
                              End if;

                              /*select @Trn_Ref_Name,@Trn_Process_Gid,
										 @Trn_Process_Staus,@Trn_To_Type, @Trn_Role_Name,
                                         @Trn_Remarks,@Entity_Gid,ls_Createby;

               call sp_Trans_Set('update',@Trn_Ref_Name,@Trn_Process_Gid,
										 @Trn_Process_Staus,@Trn_To_Type, @Trn_Role_Name,
                                         @Trn_Remarks,@Entity_Gid,ls_Createby, @Message);
					select @Message into @out_msg_tran;

                    select @out_msg_tran;

				if @out_msg_tran > 0 then
						set Message = 'SUCCESS';
				elseif @out_msg_tran <= 0  then
						set Message='Fail In Tran';
                        leave sp_FA_TFR_Asset_Set;
				End if;


              End if;*/


         End if;
End if;

END