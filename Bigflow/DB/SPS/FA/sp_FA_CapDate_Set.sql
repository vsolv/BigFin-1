CREATE DEFINER=`developer`@`%` PROCEDURE `galley`.`sp_FA_CapDate_Set`(IN `ls_Action` varchar(32),IN `ls_Type` varchar(32),
IN `ls_Sub_Type` varchar(32),IN `lj_Details` json,IN `lj_Classification` json,IN `ls_Createby` varchar(32),
OUT `Message` varchar(1024))
sp_FA_CapDate_Set:BEGIN
#### Bala Oct 14 2019
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
                    leave sp_FA_CapDate_Set;
             End if;

if ls_Type = 'CAPDATE_MAKER' and  ls_Sub_Type = 'TRAN' then
      if ls_Action = 'INSERT' then

                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.CapDate_Date'))) into @CapDate_Date;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.CapDate_Reason'))) into @CapDate_Reason;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_Detail_Gids'))) into @Asset_Detail_Gids;

                if @CapDate_Date is  null or @CapDate_Date = '' then
					set Message = 'CapDate_Date Is Needed.';
                    leave sp_FA_CapDate_Set;
				End if;

                if @CapDate_Reason is  null or @CapDate_Reason = '' then
					set Message = 'CapDate_Reason Is Needed.';
                    leave sp_FA_CapDate_Set;
				End if;

                if @Asset_Detail_Gids is  null or @Asset_Detail_Gids = '' then
					set Message = 'Asset_Detail_Gids Is Needed.';
                    leave sp_FA_CapDate_Set;
				End if;

                set @ls_Status = 'SUBMITTED';

					set Query_Insert = '';
					set Query_Insert = concat('
							INSERT INTO fa_trn_tassetcapdate
									(assetcapdate_assetdetailsid, assetcapdate_date,
									 assetcapdate_status, assetcapdate_reason,
									 assetcapdate_capdate, assetcapdate_oldcapdate,
									 entity_gid, create_by)
							(select assetdetails_id,curdate(),
									''',@ls_Status,''',''',@CapDate_Reason,''',
									''',@CapDate_Date,''',assetdetails_capdate,
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
                                  select LAST_INSERT_ID() into @CapDate_Maxgid ;

                                  #### Update The Tmp Table Cap Gid
                                  set sql_safe_updates = 0 ;
                                  Update fa_tmp_tassetdetails set assetdetails_assetcapdategid = @CapDate_Maxgid
                                  where assetdetails_mainassetdetailsgid = @Asset_Detail_Gids;

                                set countRow = (select ROW_COUNT());

                                  if countRow <= 0 then
									set Message = 'FAIL On Temp Asset Data Update.';
                                    leave sp_FA_CapDate_Set;
                                  End if;




									set Message = 'SUCCESS';

										#        select  assetdetails_gid  from fa_tmp_tassetdetails
										#	  where   assetdetails_mainassetdetailsgid=@CapDate_Maxgid into @CapDate_Reftable_Gid;

									call sp_Trans_Set('Insert','FA_CPDATE',@CapDate_Maxgid,'NEW',
											  'G','MAKER',@CapDate_Reason,@Entity_Gid,ls_Createby,@message);
										select @message into @tran;
										#select @message; #remove it
										if @tran <>0 or @tran <> '' then
												set Message = 'SUCCESS';
										else
												set Message = 'FAIL in tran';
												leave sp_FA_CapDate_Set;
										end if;
                               else
                                    set Message = 'FAIL';
                              End if;

      End if;


elseif ls_Type = 'CAPDATE_CHECKER' and  ls_Sub_Type = 'UPDATE' then
         if ls_Action = 'UPDATE' then

				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.CapDate_Gid'))) into @CapDate_Gid;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.CapDate_Status'))) into @CapDate_Status;

                if @CapDate_Gid is null or cast(@CapDate_Gid as decimal(16,2)) = 0 then
						set Message = 'CapDate Gid Is Needed.';
                        leave sp_FA_CapDate_Set;
                End if;

                if @CapDate_Status is null or @CapDate_Status = '' then
						set Message = 'CapDate Status Is Needed.';
                        leave sp_FA_CapDate_Set;
                End if;

               set Query_Update = '';
               set Query_Update = concat('Update fa_trn_tassetcapdate
											  set assetcapdate_status = ''',@CapDate_Status,''',
												  update_by = ''',ls_Createby,''',
                                                  update_date = current_timestamp()
											  Where assetcapdate_gid = ',@CapDate_Gid,'
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
										set Message = 'Error On CapDate Asset Update.';
										leave sp_FA_CapDate_Set;
									 elseif    countRow > 0 then
										set Message = 'SUCCESS';
									End if;


         End if;

End if;


END