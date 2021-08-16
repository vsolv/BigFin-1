CREATE  PROCEDURE `sp_FAAsset_Set`(IN `ls_Action` varchar(32),IN `ls_Type` varchar(32),
IN `ls_Sub_Type` varchar(32),IN `lj_Details` json,IN `lj_File` json,IN `lj_Classification` json,
IN `ls_Createby` varchar(32),OUT `Message` varchar(1024)
)
sp_FAAsset_Set:BEGIN
### Ramesh Sep 27 2019
### To Save The FA Data while Approve from Tmp Table
declare Query_Insert varchar(9000);
declare Query_Update varchar(9000);
declare Query_Delete varchar(9000);
declare Query_Update1 varchar(9000);
Declare errno int;
Declare msg varchar(1000);
declare countRow int;
Declare i int;

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

if ls_Type = 'ASSET_INITIAL' and ls_Sub_Type = 'TRAN' then

         		select JSON_LENGTH(lj_Details,'$') into @li_Detailjson_count;
					if @li_Detailjson_count is null or @li_Detailjson_count = 0 then
							set Message = 'No Data In Json - FA Details.';
                            leave sp_FAAsset_Set;
					end if;

                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Detail_Gids'))) into @Asset_Detail_Gids;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Status'))) into @ls_Status;

         set Query_Insert = '';
         set Query_Insert = concat('
          INSERT INTO fa_trn_tassetdetails
			(assetdetails_id,assetdetails_qty,assetdetails_barcode,assetdetails_date,assetdetails_assetgroupid,assetdetails_assetcatgid,assetdetails_cat,
            assetdetails_subcat,assetdetails_productgid,assetdetails_value,assetdetails_cost,assetdetails_description,assetdetails_capdate,assetdetails_source,assetdetails_status,assetdetails_requestfor,
            assetdetails_requeststatus,assetdetails_assettfrgid,assetdetails_assetsalegid,assetdetails_not5k,assetdetails_assetowner,assetdetails_lease_startdate,
            assetdetails_lease_enddate,assetdetails_impairassetgid,assetdetails_impairasset,assetdetails_writeoffgid,assetdetails_assetcatchangegid,assetdetails_assetvaluegid,
            assetdetails_assetcapdategid,assetdetails_assetsplitgid,assetdetails_assetmergegid,assetdetails_assetcatchangedate,assetdetails_reducedvalue,
            assetdetails_branchgid,assetdetails_assetlocationgid,assetdetails_bs,assetdetails_cc,assetdetails_deponhold,assetdetails_deprate,assetdetails_parentgid,assetdetails_assetserialno,assetdetails_invoicegid,
            assetdetails_inwheadergid,assetdetails_inwdetailgid,assetdetails_inwarddate,assetdetails_mepno,assetdetails_ponum,assetdetails_crnum,
			assetdetails_imagepath,assetdetails_vendorname,assetdetails_isactive,
            assetdetails_isremoved,entity_gid,create_by,assetdetails_enddate)
				(select assetdetails_id,assetdetails_qty,assetdetails_barcode,assetdetails_date,assetdetails_assetgroupid,assetdetails_assetcatgid,
				assetdetails_cat,assetdetails_subcat,assetdetails_productgid,assetdetails_value,assetdetails_cost,assetdetails_description,assetdetails_capdate,
				assetdetails_source,''',@ls_Status,''',assetdetails_requestfor,assetdetails_requeststatus,assetdetails_assettfrgid,
				assetdetails_assetsalegid,assetdetails_not5k,assetdetails_assetowner,assetdetails_lease_startdate,
				assetdetails_lease_enddate,assetdetails_impairassetgid,assetdetails_impairasset,
				assetdetails_writeoffgid,assetdetails_assetcatchangegid,assetdetails_assetvaluegid,assetdetails_assetcapdategid,	assetdetails_assetsplitgid,
				assetdetails_assetmergegid,assetdetails_assetcatchangedate,assetdetails_reducedvalue,
				assetdetails_branchgid,assetdetails_assetlocationgid,assetdetails_bs,assetdetails_cc,assetdetails_deponhold,assetdetails_deprate,assetdetails_parentgid,assetdetails_assetserialno,
				assetdetails_invoicegid,assetdetails_inwheadergid,assetdetails_inwdetailgid,assetdetails_inwarddate,assetdetails_mepno,
				assetdetails_ponum,assetdetails_crnum,assetdetails_imagepath,assetdetails_vendorname,assetdetails_isactive,
				assetdetails_isremoved,entity_gid,create_by,assetdetails_enddate
				from fa_tmp_tassetdetails  where assetdetails_gid in (',@Asset_Detail_Gids,')
				)
         ');

								set @Insert_query = Query_Insert;
								#SELECT @Insert_query;
								PREPARE stmt FROM @Insert_query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;

                              if countRow > 0 then
									set Message = 'SUCCESS';
                               else
                                    set Message = 'FAIL';
                              End if;


elseif ls_Type = 'ASSET_CHECKER' and ls_Sub_Type = 'APPROVE' then
                          ### Asset Maker Checker  -    Initial --- Approve The Data

				select JSON_LENGTH(lj_Details,'$') into @li_Detailjson_count;
					if @li_Detailjson_count is null or @li_Detailjson_count = 0 then
							set Message = 'No Data In Json - FA Details.';
                            leave sp_FAAsset_Set;
					end if;

                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Detail_Gids'))) into @Asset_Details_Gids;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Status'))) into @AssetDetails_RequestStatus;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Request_For'))) into @Request_For;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Ref_Name'))) into @Trn_Ref_Name;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_To_Type'))) into @Trn_To_Type;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Role_Name'))) into @Trn_Role_Name;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Remarks'))) into @Trn_Remarks;

                    if @Asset_Details_Gids is null or @Asset_Details_Gids = 0 then
							set Message = 'Asset_Details_Gid Is Not Given';
                            leave sp_FAAsset_Set;
					end if;

                    if @AssetDetails_RequestStatus is null or @AssetDetails_RequestStatus = '' then
							set Message = 'AssetDetails_RequestStatus Is Not Given';
                            leave sp_FAAsset_Set;
					end if;

					set Query_Update1 = '';

                if @Request_For ='SUCCESS' then
					set Query_Update1 = Concat(Query_Update1, ',assetdetails_requestfor = ''''');
				elseif @Request_For is not null AND @Request_For <>'' then
					set Query_Update1 = Concat(Query_Update1, ',assetdetails_requestfor = ''',@Request_For,'''');
                end if;

                   select ifnull(assetdetails_mainassetdetailsgid,0) from fa_tmp_tassetdetails
				   where  assetdetails_gid=@Asset_Details_Gids into @AssetDetails_Tran_Gid ;

				  if @AssetDetails_Tran_Gid = 0 or @AssetDetails_Tran_Gid is null THEN
				    set Message = 'Error On Asset Detail Main Data.';
				    leave sp_FAAsset_Set;
				  End if;


         SET SQL_SAFE_UPDATES = 0;
         SET @AssetDetails_Status = 'ACTIVE';
		 #select @AssetDetails_Tran_Gid,@AssetDetails_Status,@Asset_Details_Gids,@Request_For,Query_Update1;
		 set Query_Update = '';
         set Query_Update = concat('update fa_trn_tassetdetails
										set
											update_date=now(),
											update_by=',ls_Createby,',
											assetdetails_requeststatus=''',@AssetDetails_RequestStatus,''',
                                            assetdetails_status=''',@AssetDetails_Status,'''
                                            ',Query_Update1,'
										where assetdetails_gid in (',@AssetDetails_Tran_Gid,')
									');
								set @Update_query = Query_Update;
								#SELECT @Update_query;
								PREPARE stmt FROM @Update_query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;

                              if countRow > 0 then
								SET SQL_SAFE_UPDATES = 0;
								Delete from fa_tmp_tassetdetails where assetdetails_gid in (@Asset_Details_Gids) ;
									set Message = 'SUCCESS';

                               else
                                    set Message = 'FAIL In Asset_Details';
                                   leave sp_FAAsset_Set;
                              End if;


             set @Trn_REF_Gid='';
             set @Trn_REF_Gid=fn_REFGid(@Trn_Ref_Name);

          #select @Asset_Details_Gid;


		  set Query_Update = '';
          set Query_Update = concat('update gal_trn_ttran
										set
											update_by=',ls_Createby,',
                                            Update_date=now(),
											tran_reftable_gid=',@AssetDetails_Tran_Gid,'
										where tran_ref_gid=',@Trn_REF_Gid,'
											and tran_reftable_gid=',@Asset_Details_Gids,'
									');
								set @Update_query = Query_Update;
							    #SELECT @Update_query,'Asset';
								PREPARE stmt FROM @Update_query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;

                              if countRow > 0  then
									set Message = 'SUCCESS';
                               else
                                    set Message = 'FAIL in Tran Reftable_Gid';
                                   leave sp_FAAsset_Set;
                              End if;

                  call sp_Trans_Set('update',@Trn_Ref_Name,@AssetDetails_Tran_Gid,
										 'APPROVE',@Trn_To_Type, @Trn_Role_Name,
                                         @Trn_Remarks,@Entity_Gid,ls_Createby, @Message);
					select @Message into @out_msg_tran;

                    #select @out_msg_tran;
                    #select @Trn_Ref_Name,@AssetDetails_Tran_Gid,@Trn_To_Type,@Trn_Role_Name,@Trn_Remarks,@Entity_Gid,ls_Createby;

				if @out_msg_tran > 0  then
                     set Message = 'SUCCESS';
                  elseif @out_msg_tran <= 0 then
                    set Message = concat('Fail On Tran Update. ',@out_msg_tran);
					leave sp_FAAsset_Set;
				End if;



#UPDATE STATUS REJECTED IN TMP AND COMMON TRN

elseif ls_Type = 'ASSET_CHECKER' and ls_Sub_Type = 'REJECT' then
                      #### In Asset Maker and Checker  - Reject The Data
				select JSON_LENGTH(lj_Details,'$') into @li_Detailjson_count;
					if @li_Detailjson_count is null or @li_Detailjson_count = 0 then
							set Message = 'No Data In Json - FA Details.';
                            leave sp_FAAsset_Set;
					end if;

                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Detail_Gids'))) into @Asset_Details_Gid;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Status'))) into @Asset_Details_Status;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Ref_Name'))) into @Trn_Ref_Name;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Remark'))) into @Remarks;

                    if @Asset_Details_Gid is null or @Asset_Details_Gid = 0 then
							set Message = 'Asset_Details_Gid Is Not Given';
                            leave sp_FAAsset_Set;
					end if;

                    if @Asset_Details_Status is null or @Asset_Details_Status = '' then
							set Message = 'Status Is Not Given';
                            leave sp_FAAsset_Set;
					end if;

                    if @Remarks is null or @Remarks = '' then
							set Message = 'Remarks Is Not Given';
                            leave sp_FAAsset_Set;
					end if;

			SET SQL_SAFE_UPDATES = 0;
			set Query_Update = '';
			set Query_Update = concat('update fa_tmp_tassetdetails
										set
											update_date=now(),
											update_by=',ls_Createby,',
											assetdetails_requeststatus=''',@Asset_Details_Status,'''
										where assetdetails_gid in (',@Asset_Details_Gid,')
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
                                    set Message = 'FAIL In Asset_Details';
                              End if; set Query_Update = '';


            /*set @Trn_REF_Gid='';
             set @Trn_REF_Gid=fn_REFGid(@Trn_Ref_Name);


		  SET SQL_SAFE_UPDATES = 0; #TRN_UPDATE STATUS
		  set Query_Update = '';
          set Query_Update = concat('update gal_trn_ttran
										set
											update_by=',ls_Createby,',
                                            Update_date=now(),
											tran_status=''',@Asset_Details_Status,''',
                                            tran_remarks=''',@Remarks,'''
										where tran_ref_gid=',@Trn_REF_Gid,'
										and tran_reftable_gid=',@Asset_Details_Gid,'
									');
								set @Update_query = Query_Update;
								#SELECT @Update_query;
								PREPARE stmt FROM @Update_query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;

                              if countRow > 0  then
									set Message = 'SUCCESS';
                               else
                                    set Message = 'FAIL in Tran_Reftable_Gid';
                              End if; */

elseif ls_Type = 'ASSET_PROCESS_CHECKER' and ls_Sub_Type = 'APPROVE' then
                          ### Asset Maker Checker  -    Initial --- Approve The Data

				select JSON_LENGTH(lj_Details,'$') into @li_Detailjson_count;
					if @li_Detailjson_count is null or @li_Detailjson_count = 0 then
							set Message = 'No Data In Json - FA Details.';
                            leave sp_FAAsset_Set;
					end if;

                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Detail_Gids'))) into @Asset_Details_Gids;#### trn gid
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Status'))) into @AssetDetails_RequestStatus;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Request_For'))) into @Request_For;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Ref_Name'))) into @Trn_Ref_Name;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_To_Type'))) into @Trn_To_Type;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Role_Name'))) into @Trn_Role_Name;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Remarks'))) into @Trn_Remarks;

                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Process_Gid'))) into @Trn_Process_Gid;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Process_Staus'))) into @Trn_Process_Staus;

                    if @Asset_Details_Gids is null or @Asset_Details_Gids = 0 then
							set Message = 'Asset_Details_Gid Is Not Given';
                            leave sp_FAAsset_Set;
					end if;

                    if @AssetDetails_RequestStatus is null or @AssetDetails_RequestStatus = '' then
							set Message = 'AssetDetails RequestStatus Is Not Given';
                            leave sp_FAAsset_Set;
					end if;

                    if @Trn_Process_Gid = 0 or @Trn_Process_Gid is null then
						set Message = 'Asset Tran Process Gid Is Needed.';
                        leave sp_FAAsset_Set;
                    End if;

                    if @Trn_Process_Staus = '' or @Trn_Process_Staus is null then
						set Message = 'Asset Tran Process Staus Is Needed.';
                        leave sp_FAAsset_Set;
                    End if;

					set Query_Update1 = '';

                if @Request_For ='SUCCESS' then
					set Query_Update1 = Concat(Query_Update1, ',assetdetails_requestfor = ''''');
				elseif @Request_For is not null AND @Request_For <>'' then
					set Query_Update1 = Concat(Query_Update1, ',assetdetails_requestfor = ''',@Request_For,'''');
                end if;

                  #select assetdetails_trangid from fa_tmp_tassetdetails
				  #where  assetdetails_gid=@Asset_Details_Gids into @AssetDetails_Tran_Gid ;

         SET SQL_SAFE_UPDATES = 0;
         SET @AssetDetails_Status = 'ACTIVE';
		 set Query_Update = '';
         set Query_Update = concat('update fa_trn_tassetdetails
										set
											update_date=now(),
											update_by=',ls_Createby,',
											assetdetails_requeststatus=''',@AssetDetails_RequestStatus,''',
                                            assetdetails_status=''',@AssetDetails_Status,'''
                                            ',Query_Update1,'
										where assetdetails_gid in (',@Asset_Details_Gids,')
									');
								set @Update_query = Query_Update;
								#SELECT @Update_query,1;
								PREPARE stmt FROM @Update_query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;
                                #select countRow;
                              if countRow > 0 then
									set Message = 'SUCCESS';
                               else
                                    set Message = 'FAIL In Asset_Details';
                              End if;


             set @Trn_REF_Gid='';
             set @Trn_REF_Gid=fn_REFGid(@Trn_Ref_Name);

          	/*select exists(select assetdetails_trangid from fa_tmp_tassetdetails
				where assetdetails_trangid in (@Asset_Details_Gid))
                and assetdetails_isactive='Y' and assetdetails_isactive='Y' into @Test;

		  select @Test;
		  if @Test=1 then
			    SET SQL_SAFE_UPDATES = 0;
		        Delete from fa_tmp_tassetdetails where assetdetails_trangid in (@Asset_Details_Gid);
			elseif @Test=0 then
			    SET SQL_SAFE_UPDATES = 0;
                select 1;
		        Delete from fa_tmp_tassetdetails where assetdetails_gid in (@Asset_Details_Gid);
		  End if;  */

				#select @Asset_Details_Gids,'D1';
	   SET SQL_SAFE_UPDATES = 0;
       Delete from fa_tmp_tassetdetails where assetdetails_mainassetdetailsgid in (@Asset_Details_Gids);

                #select @Trn_Ref_Name,@Trn_Process_Gid, 1,
				#					   @Trn_Process_Staus,@Trn_To_Type, @Trn_Role_Name,
				 #                     @Trn_Remarks,@Entity_Gid,ls_Createby;

                  call sp_Trans_Set('update',@Trn_Ref_Name,@Trn_Process_Gid,
										 @Trn_Process_Staus,@Trn_To_Type, @Trn_Role_Name,
                                         @Trn_Remarks,@Entity_Gid,ls_Createby, @Message);
					select @Message into @out_msg_tran;

                   # select @out_msg_tran;

				if @out_msg_tran > 0 then
						set Message = 'SUCCESS';
				elseif @out_msg_tran <= 0  then
						set Message='Fail In Tran';
                        leave sp_FAAsset_Set;
				End if;


#UPDATE STATUS REJECTED IN TMP AND COMMON TRN

elseif ls_Type = 'ASSET_PROCESS_CHECKER' and ls_Sub_Type = 'REJECT' then
                      #### In Asset Maker and Checker  - Reject The Data
				select JSON_LENGTH(lj_Details,'$') into @li_Detailjson_count;
					if @li_Detailjson_count is null or @li_Detailjson_count = 0 then
							set Message = 'No Data In Json - FA Details.';
                            leave sp_FAAsset_Set;
					end if;

                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Detail_Gids'))) into @Asset_Details_Gid;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Status'))) into @Asset_Details_Status;
               	select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Trn_Gids'))) into @Asset_Trn_Gids;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Ref_Name'))) into @Trn_Ref_Name;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Remark'))) into @Remarks;

                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_To_Type'))) into @Trn_To_Type;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Role_Name'))) into @Trn_Role_Name;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Remarks'))) into @Trn_Remarks;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Process_Gid'))) into @Trn_Process_Gid;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Process_Staus'))) into @Trn_Process_Staus;

                    if @Asset_Details_Gid is null or @Asset_Details_Gid = 0 then
							set Message = 'Asset_Details_Gid Is Not Given';
                            leave sp_FAAsset_Set;
					end if;

                    if @Asset_Details_Status is null or @Asset_Details_Status = '' then
							set Message = 'Status Is Not Given';
                            leave sp_FAAsset_Set;
					end if;

                    if @Remarks is null or @Remarks = '' then
							set Message = 'Remarks Is Not Given';
                            leave sp_FAAsset_Set;
					end if;



              ### Ramesh Changed - Dec 13 - tmp to trn table
              ## assetdetails_requeststatus=''',@Asset_Details_Status,'''
			SET SQL_SAFE_UPDATES = 0;
			set Query_Update = '';
			set Query_Update = concat('update fa_trn_tassetdetails
										set
											update_date=now(),
											update_by=',ls_Createby,',
											assetdetails_requestfor = ''''
										where assetdetails_gid in (',@Asset_Trn_Gids,')
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
                                    set Message = 'FAIL In Asset_Details';
                              End if; set Query_Update = '';

          SET SQL_SAFE_UPDATES = 0;

          set Query_Delete = '';
          set Query_Delete = concat('Delete from fa_tmp_tassetdetails where assetdetails_gid in (',@Asset_Details_Gid,')');

                              set @Delete_query = '';
                              set @Delete_query = Query_Delete;
								#SELECT @Delete_query;
								PREPARE stmt FROM @Delete_query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;
                                #select countRow;

                              if countRow > 0 then
									set Message = 'SUCCESS';
                               else
                                    set Message = 'FAIL In Deletion';
                              End if;
                              set @Delete_query = '';

                              #select @Trn_Ref_Name,@Trn_Process_Gid,
										 #@Trn_Process_Staus,@Trn_To_Type, @Trn_Role_Name,
                                        #@Trn_Remarks,@Entity_Gid,ls_Createby;

                  call sp_Trans_Set('update',@Trn_Ref_Name,@Trn_Process_Gid,
										 @Trn_Process_Staus,@Trn_To_Type, @Trn_Role_Name,
                                         @Trn_Remarks,@Entity_Gid,ls_Createby, @Message);
					select @Message into @out_msg_tran;


				if length(@out_msg_tran ) < 12 then
						set Message = 'SUCCESS';
				elseif length(@out_msg_tran) >= 12  then
						set Message='Fail In Tran';
                        leave sp_FAAsset_Set;
				else
                      set Message = 'Error On Tran Update';
                      leave sp_FAAsset_Set;
				End if;




 elseif ls_Type = 'ASSET_CHECKER' and ls_Sub_Type = 'REQUEST_FOR' and ls_Action='UPDATE' then

     #REQUEST_FOR  UPDATE
				select JSON_LENGTH(lj_Details,'$') into @li_Detailjson_count;
					if @li_Detailjson_count is null or @li_Detailjson_count = 0 then
							set Message = 'No Data In Json - FA Details.';
                            leave sp_FAAsset_Set;
					end if;

                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Detail_Gids'))) into @Asset_Details_Gid;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.RequestFor'))) into @AssetDetails_RequestFor;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Status'))) into @Asset_Details_Status;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_CapDate'))) into @Asset_CapDate;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Cat_Gid'))) into @Asset_Cat_Gid;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Detail_id'))) into @Asset_Details_id;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Cap_Gid'))) into @Asset_Cap_Gid; ### Only for CP Date
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_WriteOff_Gid'))) into @Asset_WriteOff_Gid; ### Only for WriteOff Gid
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Impair_Gid'))) into @Asset_Impair_Gid; ### Only for Asset_Impair_Gid
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_CatChange_gid'))) into @Asset_CatChange_gid; ### Only for Asset_Impair_Gid
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Transfer_Gid'))) into @Asset_Transfer_Gid; ### Only for Asset_Transfer_Gid
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Value_Gid'))) into @Asset_Value_Gid; ### Only for Asset_value ch_Gid
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Value_New'))) into @Asset_Value_New; ### Only for Asset_valuench_Gid
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Merge_Gid'))) into @Asset_Merge_Gid; ### Only for Asset Merge
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Split_Gid'))) into @Asset_Split_Gid; ### Only for Asset Split
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Sale_Gid'))) into @Asset_Sale_Gid; ### Only for Asset Sale
                #select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Sale_Gid'))) into @Asset_Sale_Gid; ### Only for Asset Sale


                    if @Asset_Details_Gid is null or @Asset_Details_Gid = 0 then
							set Message = 'Asset_Details_Gid Is Not Given';
                            leave sp_FAAsset_Set;
					end if;

                    if @AssetDetails_RequestFor is null or @AssetDetails_RequestFor = '' then
							set Message = 'RequestFor Is Not Given';
                            leave sp_FAAsset_Set;
					end if;

                    if  @AssetDetails_RequestFor = 'SUCCESS' then
							set @AssetDetails_RequestFor = '';
					end if;

                set Query_Update1 = '';
				if @Asset_Details_Status is not null AND @Asset_Details_Status <>'' then
					set Query_Update1 = Concat(Query_Update1, ',assetdetails_status = ''',@Asset_Details_Status,'''');
                end if;

                if @Asset_CapDate is not null AND @Asset_CapDate <>'' then
					set Query_Update1 = Concat(Query_Update1, ',assetdetails_capdate = ''',@Asset_CapDate,'''');
                end if;

                if @Asset_Cat_Gid is not null AND @Asset_Cat_Gid <>'' then
					set Query_Update1 = Concat(Query_Update1, ',assetdetails_assetcatgid = ''',@Asset_Cat_Gid,'''');
                end if;

                if @Asset_Details_id is not null AND @Asset_Details_id <>'' then
					set Query_Update1 = Concat(Query_Update1, ',assetdetails_id = ''',@Asset_Details_id,'''');
                end if;

                if @Asset_Cap_Gid is not null and @Asset_Cap_Gid <> 0 then
					set Query_Update1 = Concat(Query_Update1,' ,assetdetails_assetcapdategid = ''',@Asset_Cap_Gid,'''  ');
                End if;

                if @Asset_WriteOff_Gid is not null and @Asset_WriteOff_Gid <> 0 then
					set Query_Update1 = Concat(Query_Update1,' ,assetdetails_writeoffgid = ''',@Asset_WriteOff_Gid,'''  ');
                End if;

                if @Asset_Impair_Gid is not null and @Asset_Impair_Gid <> 0 then
					set Query_Update1 = Concat(Query_Update1,' ,assetdetails_impairassetgid = ''',@Asset_Impair_Gid,'''  ');
                End if;

                if @Asset_CatChange_gid is not null and @Asset_CatChange_gid <> 0 then
					set Query_Update1 = Concat(Query_Update1,' ,assetdetails_assetcatchangegid = ''',@Asset_CatChange_gid,'''  ');
                End if;

                if @Asset_Transfer_Gid is not null and @Asset_Transfer_Gid <> 0 then
					set Query_Update1 = Concat(Query_Update1,' ,assetdetails_assettfrgid = ''',@Asset_Transfer_Gid,'''
															   ,assetdetails_status = ''IN_ACTIVE''  ');
                End if;

                if @Asset_Value_Gid is not null and @Asset_Value_Gid <> 0 then
					set Query_Update1 = Concat(Query_Update1,' ,assetdetails_assetvaluegid = ''',@Asset_Value_Gid,''', assetdetails_value = ''',@Asset_Value_New,'''  ');
                End if;

                if @Asset_Merge_Gid is not null and @Asset_Merge_Gid <> 0 then
					set Query_Update1 = Concat(Query_Update1,' ,assetdetails_assetmergegid = ''',@Asset_Merge_Gid,''' ,assetdetails_status = ''IN_ACTIVE''  ');
                End if;

                if @Asset_Split_Gid is not null and @Asset_Split_Gid <> 0 then
                   set Query_Update1 = Concat(Query_Update1,' ,assetdetails_assetsplitgid = ''',@Asset_Split_Gid,'''  ');
                    set Query_Update1 = Concat(Query_Update1,' ,assetdetails_requeststatus = ''APPROVED'',assetdetails_status = ''IN_ACTIVE''  ');
                End if;

                if @Asset_Sale_Gid is not null and @Asset_Sale_Gid <> 0 then
					 set Query_Update1 = Concat(Query_Update1,' ,assetdetails_assetsalegid = ''',@Asset_Sale_Gid,'''  ');
					set @AssetDetails_RequestFor = 'SALE';
				    set Query_Update1 = Concat(Query_Update1,' ,assetdetails_requeststatus = ''APPROVED'',assetdetails_status = ''IN_ACTIVE''  ');
                End if;




			SET SQL_SAFE_UPDATES = 0;
			set Query_Update = '';
			set Query_Update = concat('update fa_trn_tassetdetails
										set
											update_date=now(),
											update_by=',ls_Createby,',
											assetdetails_requestfor=''',@AssetDetails_RequestFor,'''
                                            ',Query_Update1,'
										where assetdetails_gid in (',@Asset_Details_Gid,')
									');

								set @Update_query = '';
								set @Update_query = Query_Update;
							   #SELECT @Update_query;
								PREPARE stmt FROM @Update_query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;

                              if countRow > 0 then
									set Message = 'SUCCESS';
							  elseif countRow<=0 then
                                    set Message = 'FAIL In Asset_Details';
                              End if;

   elseif ls_Type = 'ASSET_CHECKER' and ls_Sub_Type = 'PARENT' and ls_Action='UPDATE' then

		select JSON_LENGTH(lj_Details,'$') into @li_Detailjson_count;
					if @li_Detailjson_count is null or @li_Detailjson_count = 0 then
							set Message = 'No Data In Json - FA Details.';
                            leave sp_FAAsset_Set;
					end if;

                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Parent_Gids'))) into @Asset_Parent_Gids;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Status'))) into @Approve_Status;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Remark'))) into @ls_Remark;



                    if @Asset_Parent_Gids is null or @Asset_Parent_Gids = 0 then
							set Message = 'Asset_Parent_Gid Is Not Given';
                            leave sp_FAAsset_Set;
					end if;

                    #select @Asset_Parent_Gids;
				SET @Asset_Tran_Gids='';
                    select group_concat(assetdetails_mainassetdetailsgid) from fa_tmp_tassetdetails
						   where assetdetails_parentgid = @Asset_Parent_Gids INTO @Asset_Detail_Tran_Gids ;

				   select assetdetails_mainassetdetailsgid into @Asset_Parent_Trn
				      from fa_tmp_tassetdetails where assetdetails_gid = @Asset_Parent_Gids;


			SET SQL_SAFE_UPDATES = 0;
			set Query_Update = '';
			set Query_Update = concat('update fa_trn_tassetdetails
										set
											update_date=now(),
											update_by=',ls_Createby,',
											assetdetails_parentgid=',@Asset_Parent_Trn,',
                                            assetdetails_requestfor = ''''
										where assetdetails_gid in (',@Asset_Detail_Tran_Gids,')
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
                                    set Message = 'FAIL In Asset_Parent';
                                   leave sp_FAAsset_Set;
                              End if;


                       ##### Tran Update.

								if @ls_Remark is null or @ls_Remark = '' THEN
								  set @ls_Remark = 'APPROVE';
								End if;

							call sp_Trans_Set('update','ASSET_CLUB',@Asset_Parent_Trn,
														 @Approve_Status,'C','CHECKER',
				                                         @ls_Remark,@Entity_Gid,ls_Createby, @Message);
								select @Message into @out_msg_tran;

				                   # select @out_msg_tran;

								if @out_msg_tran > 0 then
										set Message = 'SUCCESS';
								elseif @out_msg_tran <= 0  then
										set Message='Fail In Tran';
				                        leave sp_FAAsset_Set;
								End if;



End if;
END