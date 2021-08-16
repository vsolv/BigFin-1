CREATE DEFINER=`developer`@`%` PROCEDURE `galley`.`sp_FA_CatChange_Set`(IN `ls_Action` varchar(32),
IN `ls_Type` varchar(32),IN `ls_Sub_Type` varchar(32),IN `lj_Details` json,IN `lj_Classification` json,
IN `ls_Createby` varchar(32),OUT `Message` varchar(1024))
sp_FA_CatChange_Set:BEGIN

#### Bala Oct 16 2019

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
                    leave sp_FA_CatChange_Set;
             End if;

if ls_Type = 'CAT_CHANGE_MAKER' and  ls_Sub_Type = 'TRAN' then
      if ls_Action = 'INSERT' then


                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.CatChange_Reason'))) into @CatChange_Reason;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.CatChange_Cat'))) into @CatChange_Cat;
                #"CatChange_Cat Is Varchar in Table(fa_trn_tassetcatchange) so we get it from front end"
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.CatChange_OldCat'))) into @CatChange_OldCat;
				#"CatChange_OldCat Is Varchar in Table(fa_trn_tassetcatchange) so we get it from front end"
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_Detail_Gids'))) into @Asset_Detail_Gids;


					if @CatChange_Reason is  null or @CatChange_Reason = '' then
						set Message = 'CatChange_Reason Is Needed.';
						leave sp_FA_CatChange_Set;
					End if;

					if @CatChange_Cat is  null or @CatChange_Cat = '' then
						set Message = 'CatChange_Cat Is Needed.';
						leave sp_FA_CatChange_Set;
					End if;

					if @CatChange_OldCat is  null or @CatChange_OldCat = '' then
						set Message = 'CatChange_OldCat Is Needed.';
						leave sp_FA_CatChange_Set;
					End if;

					if @Asset_Detail_Gids is  null or @Asset_Detail_Gids = '' then
						set Message = 'Asset_Detail_Gids Is Needed.';
						leave sp_FA_CatChange_Set;
					End if;

						set @ls_Status = 'SUBMITTED';

					set Query_Insert = '';
					set Query_Insert = concat('
							INSERT INTO fa_trn_tassetcatchange
									(assetcatchange_assetdetailsid, assetcatchange_date,
									 assetcatchange_status, assetcatchange_reason,
									 assetcatchange_cat, assetcatchange_oldcat,
									 entity_gid, create_by)
							(select assetdetails_id,curdate(),
									''',@ls_Status,''',''',@CatChange_Reason,''',
									''',@CatChange_Cat,''',''',@CatChange_OldCat,''',
                                    entity_gid,''',ls_Createby,'''
							from fa_trn_tassetdetails
							where assetdetails_gid in (',@Asset_Detail_Gids,')
								 )');

								set @Insert_query = Query_Insert;
								#SELECT @Insert_query;
								PREPARE stmt FROM @Insert_query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;

                              if countRow > 0 then
                                  select LAST_INSERT_ID() into @CatChange_Maxgid ;

                                    #### Update im Tmp Table
                                  set sql_safe_updates = 0;
                                  Update fa_tmp_tassetdetails set assetdetails_assetcatchangegid = @CatChange_Maxgid
                                  where assetdetails_mainassetdetailsgid = @Asset_Detail_Gids;

                                  set countRow = (select ROW_COUNT());

										if  countRow <= 0 then
											set Message = 'FAIL On Asset Temp Data Update.';
                                            leave sp_FA_CatChange_Set;
                                        End if;


                                set Message = 'SUCCESS';
                                   ### TO DO
								call sp_Trans_Set('Insert','FA_CATCHANGE',@CatChange_Maxgid,'NEW',
										  'G','MAKER',@CatChange_Reason,@Entity_Gid,ls_Createby,@message);
									select @message into @tran;
									#select @message; #remove it
									if @tran <>0 or @tran <> '' then
											set Message = 'SUCCESS';
									else
											set Message = 'FAIL in tran';
											leave sp_FA_CatChange_Set;
									end if;
                               else
                                    set Message = 'FAIL';
                              End if;


         End if;


elseif ls_Type = 'CAT_CHANGE_CHECKER' and  ls_Sub_Type = 'UPDATE' then
         if ls_Action = 'UPDATE' then

				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.CatChange_Gid'))) into @CatChange_Gid;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.CatChange_Status'))) into @CatChange_Status;
						#select @CatChange_Status;
						#select @CatChange_Gid;
                if @CatChange_Gid is null or cast(@CatChange_Gid as decimal(16,2))  = 0 then
						set Message = 'CatChange Gid Is Needed.';
                        leave sp_FA_CatChange_Set;
                End if;

                if @CatChange_Status is null or @CatChange_Status = '' then
						set Message = 'CatChange Status Is Needed.';
                        leave sp_FA_CatChange_Set;
                End if;

               set Query_Update = '';
               set Query_Update = concat('Update fa_trn_tassetcatchange
											    set assetcatchange_status = ''',@CatChange_Status,''' ,
													update_by = ''',ls_Createby,''' ,
                                                    update_date = current_timestamp()
											Where assetcatchange_gid = ',@CatChange_Gid,'
												  and entity_gid = ',@Entity_Gid,'
												');

									set @Query_Update = '';
									set @Query_Update = Query_Update;
								    #select @Query_Update; ### Remove IT
									PREPARE stmt FROM @Query_Update;
									EXECUTE stmt;
									set countRow = (select ROW_COUNT());
									DEALLOCATE PREPARE stmt;

									if countRow <= 0 then
										set Message = 'Error On catchange Update.';
										rollback;
										leave sp_FA_CatChange_Set;
									 elseif    countRow > 0 then
										set Message = 'SUCCESS';
									End if;

			End if;
End if;


END