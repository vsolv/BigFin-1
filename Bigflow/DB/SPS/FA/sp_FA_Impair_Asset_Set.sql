CREATE DEFINER=`developer`@`%` PROCEDURE `galley`.`sp_FA_Impair_Asset_Set`(IN `ls_Action` varchar(32),IN `ls_Type` varchar(32),
IN `ls_Sub_Type` varchar(32),IN `lj_Details` json,IN `lj_Classification` json,IN `ls_Createby` varchar(32),
OUT `Message` varchar(1024))
sp_FA_Impair_Asset_Set:BEGIN
#### Bala Oct 15 2019
Declare errno int;
Declare msg varchar(1000);
Declare Query_Update varchar(1000);
Declare countRow int;
Declare Query_Insert varchar(9000);

DECLARE EXIT HANDLER FOR SQLEXCEPTION,sqlwarning

    BEGIN

     GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
     set Message = concat(errno , msg);
     ROLLBACK;
     END;

	select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid[0]'))) into @Entity_Gid;

             if @Entity_Gid is  null or @Entity_Gid = 0 or @Entity_Gid = '' then
					set Message = 'Entity Gid Is Needed.';
                    leave sp_FA_Impair_Asset_Set;
             End if;

if ls_Type = 'IMPAIR_ASSET_MAKER' and  ls_Sub_Type = 'TRAN' then
      if ls_Action = 'INSERT' then


                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.ImpairAsset_Reason'))) into @ImpairAsset_Reason;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_Detail_Gids'))) into @Asset_Detail_Gids;

                if @ImpairAsset_Reason is  null or @ImpairAsset_Reason = '' then
					set Message = 'ImpairAsset_Reason Is Needed.';
                    leave sp_FA_Impair_Asset_Set;
				End if;

                if @Asset_Detail_Gids is  null or @Asset_Detail_Gids = '' then
					set Message = 'Asset_Detail_Gids Is Needed.';
                    leave sp_FA_Impair_Asset_Set;
				End if;

                set @ls_Status = 'SUBMITTED';

					set Query_Insert = '';
					set Query_Insert = concat('
							INSERT INTO fa_trn_timpairasset
									(impairasset_assetdetailsid, impairasset_date,
									 impairasset_status, ImpairAsset_Reason,
									 impairasset_value,entity_gid, create_by)
							(select assetdetails_id,curdate(),
									''',@ls_Status,''',''',@ImpairAsset_Reason,''',
									assetdetails_value,entity_gid,	',ls_Createby,'
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
                                  select LAST_INSERT_ID() into @ImpairAsset_Maxgid ;

                                  #### Update im Tmp Table
                                  set sql_safe_updates = 0;
                                  Update fa_tmp_tassetdetails set assetdetails_impairassetgid = @ImpairAsset_Maxgid
                                  where assetdetails_mainassetdetailsgid = @Asset_Detail_Gids;

									set countRow = (select ROW_COUNT());

										if  countRow <= 0 then
											set Message = 'FAIL On Asset Temp Data Update.';
                                            leave sp_FA_Impair_Asset_Set;
                                        End if;

									set Message = 'SUCCESS';

						call sp_Trans_Set('Insert','FA_IMPAIRMENT',@ImpairAsset_Maxgid,'NEW',
										  'G','MAKER',@ImpairAsset_Reason,@Entity_Gid,ls_Createby,@message);
									select @message into @tran;
									#select @message; #remove it
									if @tran <>0 or @tran <> '' then
											set Message = 'SUCCESS';
									else
											set Message = 'FAIL in tran';
											leave sp_FA_Impair_Asset_Set;
									end if;

                               else
                                    set Message = 'FAIL';
                              End if;

      End if;


 elseif ls_Type = 'IMPAIRMENT_CHECKER' and  ls_Sub_Type = 'UPDATE' then
         if ls_Action = 'UPDATE' then

				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Impairment_Gid'))) into @Impairment_Gid;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Impairment_Status'))) into @Impairment_Status;

                if @Impairment_Gid is null or cast(@Impairment_Gid as decimal(16,2))  = 0 then
						set Message = 'Impairment Gid Is Needed.';
                        leave sp_FA_Impair_Asset_Set;
                End if;

                if @Impairment_Status is null or @Impairment_Status = '' then
						set Message = 'Impairment Status Is Needed.';
                        leave sp_FA_Impair_Asset_Set;
                End if;

               set Query_Update = '';
               set Query_Update = concat('Update fa_trn_timpairasset
											  set impairasset_status = ''',@Impairment_Status,''' ,
												  update_by = ''',ls_Createby,''' ,
                                                  update_date = current_timestamp()
											  Where impairasset_gid = ',@Impairment_Gid,'
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
										set Message = 'Error On Impair Asset Update.';
										leave sp_FA_Impair_Asset_Set;
									 elseif    countRow > 0 then
										set Message = 'SUCCESS';
									End if;


         End if;
End if;


END