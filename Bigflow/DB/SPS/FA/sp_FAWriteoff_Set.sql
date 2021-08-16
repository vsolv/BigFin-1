CREATE DEFINER=`developer`@`%` PROCEDURE `galley`.`sp_FAWriteoff_Set`(IN `ls_Action` varchar(32),IN `ls_Type` varchar(32),IN `ls_Sub_Type` varchar(32),
IN `lj_Details` json,IN `lj_Classification` json,IN `ls_Createby` varchar(32),OUT `Message` varchar(1024))
sp_FAWriteoff_Set:BEGIN
#### Ramesh Oct 11 2019
Declare errno int;
Declare msg varchar(1000);
Declare countRow int;
Declare Query_Insert varchar(9000);
Declare Query_Update varchar(2048);

DECLARE EXIT HANDLER FOR SQLEXCEPTION,sqlwarning

    BEGIN

     GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
     set Message = concat(errno , msg);
     ROLLBACK;
     END;

	select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid[0]'))) into @Entity_Gid;

             if @Entity_Gid is  null or @Entity_Gid = 0 or @Entity_Gid = '' then
					set Message = 'Entity Gid Is Needed.';
                    leave sp_FAWriteoff_Set;
             End if;

if ls_Type = 'WRITEOFF_MAKER' and  ls_Sub_Type = 'TRAN' then
      if ls_Action = 'INSERT' then

                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.WriteOff_Date'))) into @WriteOff_Date;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.WriteOff_Reason'))) into @WriteOff_Reason;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_Detail_Gids'))) into @Asset_Detail_Gids;

                set @ls_Status = 'REQUESTED';

								set Query_Insert = '';
								 set Query_Insert = concat('
								  INSERT INTO fa_trn_twriteoff
									(writeoff_assetdetailsid,writeoff_date,writeoff_status,writeoff_reason,writeoff_value,entity_gid,create_by)
										(select assetdetails_id,''',@WriteOff_Date,''',''',@ls_Status,''',''',@WriteOff_Reason,''',assetdetails_value,entity_gid,
										''',ls_Createby,''' from fa_trn_tassetdetails  where assetdetails_gid in (',@Asset_Detail_Gids,')
										)');

								set @Insert_query = Query_Insert;
								#SELECT @Insert_query;
								PREPARE stmt FROM @Insert_query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;

                              if countRow > 0 then
                                  select LAST_INSERT_ID() into @writeoff_Maxgid ;


                                  #### Update im Tmp Table
                                  set sql_safe_updates = 0;
                                  Update fa_tmp_tassetdetails set assetdetails_writeoffgid = @writeoff_Maxgid
                                  where assetdetails_mainassetdetailsgid = @Asset_Detail_Gids;

                                  set countRow = (select ROW_COUNT());

										if  countRow <= 0 then
											set Message = 'FAIL On Asset Temp Data Update.';
                                            leave sp_FAWriteoff_Set;
                                        End if;


									set Message = 'SUCCESS';

                                    call sp_Trans_Set('Insert','FA_WRITEOFF',@writeoff_Maxgid,'NEW','G',
													  'MAKER',@WriteOff_Reason,@Entity_Gid,ls_Createby,@message);
									select @message into @tran;
									#select @message; #remove it
									if @tran <>0 or @tran <> '' then
											set Message = 'SUCCESS';
									else
											set Message = 'FAIL in tran';
											leave sp_FAWriteoff_Set;
									end if;

                               else
                                    set Message = 'FAIL';
                              End if;
      End if;

 elseif ls_Type = 'WRITEOFF_CHECKER' and  ls_Sub_Type = 'UPDATE' then
         if ls_Action = 'UPDATE' then

				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.WriteOff_Gid'))) into @WriteOff_Gid;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.WriteOff_Status'))) into @WriteOff_Status;

                if @WriteOff_Gid is null or cast(@WriteOff_Gid as decimal(16,2))  = 0 then
						set Message = 'Writeoff Gid Is Needed.';
                        leave sp_FAWriteoff_Set;
                End if;

                if @WriteOff_Status is null or @WriteOff_Status = '' then
						set Message = 'Writeoff Status Is Needed.';
                        leave sp_FAWriteoff_Set;
                End if;

               set Query_Update = '';
               set Query_Update = concat('Update fa_trn_twriteoff set writeoff_status = ''',@WriteOff_Status,''' , update_by = ''',ls_Createby,''' ,update_date = current_timestamp()
											Where writeoff_gid = ',@WriteOff_Gid,'  and entity_gid = ',@Entity_Gid,'
												');

                                      set @Query_Update = '';
									set @Query_Update = Query_Update;
								   #select @Query_Update; ### Remove IT
									PREPARE stmt FROM @Query_Update;
									EXECUTE stmt;
									set countRow = (select ROW_COUNT());
									DEALLOCATE PREPARE stmt;

									if countRow <= 0 then
										set Message = 'Error On Write Off Update.';
										rollback;
										leave sp_FAWriteoff_Set;
									 elseif    countRow > 0 then
										set Message = 'SUCCESS';
									End if;


         End if;
End if;


END