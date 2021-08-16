CREATE  PROCEDURE `sp_FAMerge_Set`(IN `ls_Action` varchar(32),IN `ls_Type` varchar(32),
IN `ls_Sub_Type` varchar(32),
IN `lj_Details` json,IN `lj_Classification` json,IN `ls_Createby` varchar(32),OUT `Message` varchar(1024))
sp_FAMerge_Set:BEGIN
#### Ramesh Oct 24 2019

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
                    leave sp_FAMerge_Set;
             End if;

   if ls_Type = 'ASSET_MERGE' and  ls_Sub_Type = 'TRAN' then

                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_Detail_Gids'))) into @Asset_Detail_Gids;    ### More Than One Gid
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_Gid'))) into @Asset_Gid;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Merge_Value'))) into @Merge_Value;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Merge_Date'))) into @Merge_Date;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Merge_Reason'))) into @Merge_Reason;


				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Ref_Name'))) into @Trn_Ref_Name;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_To_Type'))) into @Trn_To_Type;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Role_Name'))) into @Trn_Role_Name;
                #select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Remarks'))) into @Trn_Remarks;
                #select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Process_Gid'))) into @Trn_Process_Gid;
                #select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Process_Staus'))) into @Trn_Process_Staus;

                #select lj_Details;

                if @Merge_Value is null or @Merge_Value = 0 then
					set Message = 'Merge Value Is Needed.';
                    leave sp_FAMerge_Set;
                End if;

                if @Merge_Date is null or @Merge_Date = '' then
					set Message = 'Merge Date Is Needed.';
                    leave sp_FAMerge_Set;
                End if;

                ### TO DO Validations
        #        select @Asset_Detail_Gids,@Asset_Gid,@Merge_Value,@Merge_Date,@Merge_Reason;

				set @ls_Status = 'IN_ACTIVE';
                    set @ls_Request_For = 'MERGE';
                    set @ls_Request_Status = 'SUBMITTED';
                    set @New_Asset_Id = '';
                    #select max(cast(assetdetails_id as decimal)) + 99110 into @New_Asset_Id from fa_tmp_tassetdetails;
                    select ifnull(max(cast(assetdetails_id as decimal)),0)+1 into @New_Asset_TmpId from fa_tmp_tassetdetails where assetdetails_id not like '%-%';
                    select ifnull(max(cast(assetdetails_id as decimal)),0)+1 into @New_Asset_TrnId from fa_trn_tassetdetails where assetdetails_id not like '%-%';

                     if @New_Asset_TmpId > @New_Asset_TrnId THEN
                       set @New_Asset_Id = @New_Asset_TmpId;
                     ELSEIF @New_Asset_TmpId <= @New_Asset_TrnId THEN
                       set @New_Asset_Id = @New_Asset_TrnId;
                     ELSE
                       set Message = 'Error On Asset New Id.';
                       leave sp_FAMerge_Set;
                     End if;

                    #select @New_Asset_Id; # TO DO
                    ##### Creation Of New Asset
                  #  select @New_Asset_Id,@Merge_Value,@ls_Status,@ls_Request_For,@ls_Request_Status,@Asset_Gid;
                    set Query_Insert = '';
						 set Query_Insert = concat('
						  INSERT INTO fa_tmp_tassetdetails
							(assetdetails_id,assetdetails_qty,assetdetails_barcode,assetdetails_date,assetdetails_assetgroupid,assetdetails_assetcatgid,assetdetails_cat,
							assetdetails_subcat,assetdetails_productgid,assetdetails_value,assetdetails_cost,assetdetails_description,assetdetails_capdate,assetdetails_source,
                            assetdetails_status,assetdetails_requestfor,
							assetdetails_requeststatus,assetdetails_assettfrgid,assetdetails_assetsalegid,assetdetails_not5k,assetdetails_assetowner,assetdetails_lease_startdate,
							assetdetails_lease_enddate,assetdetails_impairassetgid,assetdetails_impairasset,assetdetails_writeoffgid,assetdetails_assetcatchangegid,assetdetails_assetvaluegid,
							assetdetails_assetcapdategid,assetdetails_assetsplitgid,assetdetails_assetmergegid,assetdetails_assetcatchangedate,assetdetails_reducedvalue,
							assetdetails_branchgid,assetdetails_bs,assetdetails_cc,assetdetails_deponhold,assetdetails_deprate,assetdetails_parentgid,assetdetails_assetserialno,assetdetails_invoicegid,
							assetdetails_inwheadergid,assetdetails_inwdetailgid,assetdetails_inwarddate,assetdetails_mepno,assetdetails_ponum,assetdetails_crnum,
							assetdetails_imagepath,assetdetails_vendorname,assetdetails_mainassetdetailsgid,assetdetails_isactive,assetdetails_isremoved,entity_gid,create_by,assetdetails_assetlocationgid)
								(select ''',@New_Asset_Id,''',assetdetails_qty,assetdetails_barcode,assetdetails_date,assetdetails_assetgroupid,assetdetails_assetcatgid,
								assetdetails_cat,assetdetails_subcat,assetdetails_productgid,''',@Merge_Value,''',assetdetails_cost,assetdetails_description,assetdetails_capdate,
								assetdetails_source,''',@ls_Status,''',''',@ls_Request_For,''',''',@ls_Request_Status,''',assetdetails_assettfrgid,
								assetdetails_assetsalegid,assetdetails_not5k,assetdetails_assetowner,assetdetails_lease_startdate,
								assetdetails_lease_enddate,assetdetails_impairassetgid,assetdetails_impairasset,
								assetdetails_writeoffgid,assetdetails_assetcatchangegid,assetdetails_assetvaluegid,assetdetails_assetcapdategid,	assetdetails_assetsplitgid,
								assetdetails_assetmergegid,assetdetails_assetcatchangedate,assetdetails_reducedvalue,
								assetdetails_branchgid,assetdetails_bs,assetdetails_cc,assetdetails_deponhold,assetdetails_deprate,assetdetails_parentgid,assetdetails_assetserialno,
								assetdetails_invoicegid,assetdetails_inwheadergid,assetdetails_inwdetailgid,assetdetails_inwarddate,assetdetails_mepno,
								assetdetails_ponum,assetdetails_crnum,assetdetails_imagepath,assetdetails_vendorname,assetdetails_gid,assetdetails_isactive,
								assetdetails_isremoved,entity_gid,create_by,assetdetails_assetlocationgid
								from fa_trn_tassetdetails  where assetdetails_gid in (',@Asset_Gid,')
								)
						 ');
								set @Insert_query = '';
                                set @Insert_query = Query_Insert;
						#		SELECT @Insert_query;
								PREPARE stmt FROM @Insert_query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;

                              if countRow > 0 then
									set Message = 'SUCCESS';
                                    select LAST_INSERT_ID() into @New_Asset_IdDB;
                               else
                                    set Message = 'FAIL';
                                    leave sp_FAMerge_Set;
                              End if;

                              ######## Merge table
                          #    select @New_Asset_Id,@Merge_Date,@ls_Request_Status,@Merge_Reason,@Merge_Value,@Entity_Gid,ls_Createby;
							set Query_Insert = '';
                            set Query_Insert = concat('Insert into fa_trn_tassetmergeheader
																		(assetmergeheader_newassetid,assetmergeheader_date,
																		assetmergeheader_status,assetmergeheader_reason,
                                                                        assetmergeheader_value,entity_gid,create_by)
																values (''',@New_Asset_Id,''',''',@Merge_Date,''',
                                                                        ''',@ls_Request_Status,''',''',@Merge_Reason,''',
                                                                        ''',@Merge_Value,''',''',@Entity_Gid,''',''',ls_Createby,''')');

                                         set @Insert_query = '';
                                         set @Insert_query = Query_Insert;
										#SELECT @Insert_query;
										PREPARE stmt FROM @Insert_query;
										EXECUTE stmt;
										set countRow = (select ROW_COUNT());
										DEALLOCATE PREPARE stmt;

									  if countRow > 0 then
											set Message = 'SUCCESS';
											select LAST_INSERT_ID() into @New_Merge_Id;
									   else
											set Message = 'FAIL';
                                            leave sp_FAMerge_Set;
									  End if;

                                      #### Update in Tmp Table
                                      #select @Asset_Detail_Gids,@New_Asset_IdDB;

									set @Asset_CombineGids = concat(@Asset_Detail_Gids,',',@New_Asset_IdDB);

                                    #select @Asset_CombineGids;
                                    #select @New_Merge_Id;

                                  set sql_safe_updates = 0;

							set Query_Update = '';
							set Query_Update = concat('Update fa_tmp_tassetdetails
															set assetdetails_assetmergegid = ''',@New_Merge_Id,'''
															where assetdetails_mainassetdetailsgid in (',@Asset_CombineGids,') ');

									set @Update_query = '';
										set @Update_query = Query_Update;
										#SELECT @Update_query;
										PREPARE stmt FROM @Update_query;
										EXECUTE stmt;
										set countRow = (select ROW_COUNT());
										DEALLOCATE PREPARE stmt;

									  if countRow > 0 then
											set Message = 'SUCCESS';
									   else
													set Message = 'FAIL On Asset Temp Data Update.';
                                                    leave sp_FAMerge_Set;
									  End if;

                                    #####   Merger Details
                                   set Query_Insert = '';
                            set Query_Insert = concat('
                                         INSERT INTO fa_trn_tassetmerge
													(assetmerge_assetmergeheader_gid,assetmerge_assetdetailsid,
													 assetmerge_value,entity_gid,create_by)
											(select ''',@New_Merge_Id,''',assetdetails_gid,
													 assetdetails_value,
													''',@Entity_Gid,''',''',ls_Createby,'''
													from fa_trn_tassetdetails
													where assetdetails_gid in (',@Asset_Detail_Gids,'));
                                    ');

                                        set @Insert_query = '';
										set @Insert_query = Query_Insert;
										#SELECT @Insert_query;
										PREPARE stmt FROM @Insert_query;
										EXECUTE stmt;
										set countRow = (select ROW_COUNT());
										DEALLOCATE PREPARE stmt;

									  if countRow > 0 then
											set Message = 'SUCCESS';
                                            #select LAST_INSERT_ID() into @Trn_Reftable_Gid;
									   else
											set Message = 'FAIL';
									  End if;

				#select @Trn_Ref_Name,@Trn_Reftable_Gid,@ls_Status,@Trn_To_Type, @Trn_Role_Name,
                                        # @Merge_Reason,@Entity_Gid,ls_Createby ;



						call sp_Trans_Set('Insert',@Trn_Ref_Name,@New_Merge_Id,
										    @ls_Status,@Trn_To_Type, @Trn_Role_Name,
                                            @Merge_Reason,@Entity_Gid,ls_Createby, @Message);
										select @Message into @out_msg_tran;

                                        #select  @out_msg_tran;

                                        select max(tran_gid) from gal_trn_ttran into @Tran_Gid;

									if @out_msg_tran =@Tran_Gid  then
										set Message = 'SUCCESS';
                                    else
										set Message = 'Failed On Tran Insert';
										leave sp_FAMerge_Set;
									End if;

  else
       set Message = 'Incorrect Type.';

   End if;


if ls_Type = 'MERGE_CHECKER' and  ls_Sub_Type = 'UPDATE' and  ls_Action = 'UPDATE' then

				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Merge_Gid'))) into @Merge_Gid;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Merge_Status'))) into @Merge_Status;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Ref_Name'))) into @Trn_Ref_Name;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_To_Type'))) into @Trn_To_Type;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Role_Name'))) into @Trn_Role_Name;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Remarks'))) into @Trn_Remarks;

					if @Merge_Gid is null or cast(@Merge_Gid as decimal(16,2))  = 0 then
						set Message = 'Merge_Gid Is Needed.';
                        leave sp_FAMerge_Set;
					End if;

					if @Merge_Status is null or @Merge_Status = '' then
						set Message = 'Merge_Status Is Needed.';
                        leave sp_FAMerge_Set;
					End if;


				set @Asset_Detail_Gids='';

						select b.assetdetails_gid
                                from fa_trn_tassetmergeheader a
                                inner join fa_tmp_tassetdetails b on b.assetdetails_id=a.assetmergeheader_newassetid
                                and a.assetmergeheader_gid=@Merge_Gid into @Asset_Detail_New_Gid ;

                               Select group_concat(assetdetails_gid) into @Asset_Detail_Gids
                               from fa_tmp_tassetdetails where assetdetails_assetmergegid = @Merge_Gid
                               and assetdetails_isactive = 'Y' and assetdetails_isremoved = 'N';

                    #select @Asset_Detail_Gids;

               if  @Merge_Status='APPROVED' then

					set Query_Update = '';
					set Query_Update = concat('Update fa_trn_tassetmergeheader
											    set assetmergeheader_status = ''',@Merge_Status,''' ,
													update_by = ''',ls_Createby,''' ,
                                                    update_date = current_timestamp()
											Where assetmergeheader_gid = ',@Merge_Gid,'
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
										set Message = 'Error On Merge Update.';
										leave sp_FAMerge_Set;
									 elseif    countRow > 0 then
										set Message = 'SUCCESS';
									End if;

                        set @ls_Status = 'ACTIVE';
                        #select @ls_Status,@ls_Request_For,@ls_Request_Status,@Asset_Detail_Gids;



						 set Query_Insert = '';
						 set Query_Insert = concat('
							INSERT INTO fa_trn_tassetdetails
									(assetdetails_id,assetdetails_qty,assetdetails_barcode,assetdetails_date,assetdetails_assetgroupid,
										assetdetails_assetcatgid,
										assetdetails_cat,assetdetails_subcat,assetdetails_productgid,assetdetails_value,assetdetails_cost,assetdetails_description,assetdetails_capdate,
										assetdetails_source,assetdetails_status,assetdetails_requestfor,assetdetails_requeststatus,assetdetails_assettfrgid,
										assetdetails_assetsalegid,assetdetails_not5k,assetdetails_assetowner,assetdetails_lease_startdate,
										assetdetails_lease_enddate,assetdetails_impairassetgid,assetdetails_impairasset,
										assetdetails_writeoffgid,assetdetails_assetcatchangegid,assetdetails_assetvaluegid,
                                        assetdetails_assetcapdategid,	assetdetails_assetsplitgid,
										assetdetails_assetmergegid,assetdetails_assetcatchangedate,assetdetails_reducedvalue,
										assetdetails_branchgid,assetdetails_bs,assetdetails_cc,assetdetails_deponhold,assetdetails_deprate,assetdetails_parentgid,
                                        assetdetails_assetserialno,
										assetdetails_invoicegid,assetdetails_inwheadergid,assetdetails_inwdetailgid,
                                        assetdetails_inwarddate,assetdetails_mepno,
										assetdetails_ponum,assetdetails_crnum,assetdetails_imagepath,assetdetails_vendorname,
                                        assetdetails_gid,assetdetails_isactive,
										assetdetails_isremoved,entity_gid,create_by,assetdetails_assetlocationgid)
							    (select assetdetails_id,assetdetails_qty,assetdetails_barcode,assetdetails_date,
										assetdetails_assetgroupid,assetdetails_assetcatgid,
										assetdetails_cat,assetdetails_subcat,assetdetails_productgid,assetdetails_value,assetdetails_cost,assetdetails_description,assetdetails_capdate,
										assetdetails_source,''',@ls_Status,''','''',''',@Merge_Status,''',assetdetails_assettfrgid,
										assetdetails_assetsalegid,assetdetails_not5k,assetdetails_assetowner,assetdetails_lease_startdate,
										assetdetails_lease_enddate,assetdetails_impairassetgid,assetdetails_impairasset,
										assetdetails_writeoffgid,assetdetails_assetcatchangegid,assetdetails_assetvaluegid,
                                        assetdetails_assetcapdategid,	assetdetails_assetsplitgid,
										assetdetails_assetmergegid,assetdetails_assetcatchangedate,assetdetails_reducedvalue,
										assetdetails_branchgid,assetdetails_bs,assetdetails_cc,assetdetails_deponhold,assetdetails_deprate,assetdetails_parentgid,
                                        assetdetails_assetserialno,
										assetdetails_invoicegid,assetdetails_inwheadergid,assetdetails_inwdetailgid,
                                        assetdetails_inwarddate,assetdetails_mepno,
										assetdetails_ponum,assetdetails_crnum,assetdetails_imagepath,assetdetails_vendorname,
                                        assetdetails_gid,assetdetails_isactive,
										assetdetails_isremoved,entity_gid,create_by,assetdetails_assetlocationgid
									from fa_tmp_tassetdetails  where assetdetails_gid in (',@Asset_Detail_New_Gid,'))');

								#select @Asset_Detail_Gids;

								set @Insert_query = Query_Insert;
								#SELECT @Insert_query;
								PREPARE stmt FROM @Insert_query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;

                              if countRow > 0 then
									set sql_safe_updates=0;  ### Check All the Data is Not deleted.

								set Query_Update = '';
							   set Query_Update = concat('Delete from fa_tmp_tassetdetails
									where assetdetails_gid in (',@Asset_Detail_Gids,')');

							    set @Update_Query = '';
							    set @Update_Query = Query_Update;
							 	PREPARE stmt FROM @Update_Query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;

							      if countRow > 0 THEN
							        set Message = 'SUCCESS';
							      ELSE
							         set Message = 'Error On Temp Data Delete.';
							         leave sp_FAMerge_Set;
							      end if;
                               else
                                    set Message = 'FAIL';
                                   leave sp_FAMerge_Set;
                              End if;


                      #select @Merge_Gid,@Trn_Ref_Name,@Merge_Gid,
							  #'APPROVE',@Trn_To_Type, @Trn_Role_Name,
                                      #   @Trn_Remarks,@Entity_Gid,ls_Createby;

			call sp_Trans_Set('update',@Trn_Ref_Name,@Merge_Gid,
							  'APPROVE',@Trn_To_Type, @Trn_Role_Name,
                                         @Trn_Remarks,@Entity_Gid,ls_Createby, @Message);
					select @Message into @out_msg_tran;

                    #select @out_msg_tran;

				if @out_msg_tran > 0  then
					 set Message = 'SUCCESS';
                  elseif @out_msg_tran <= 0 then
                    set Message = concat('Fail On Tran Update. ',@out_msg_tran);
                    rollback;
					leave sp_FAMerge_Set;
				End if;


			Elseif @Merge_Status='REJECTED' then

                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Remark'))) into @Remark;

					if @Remark is null or @Remark   = '' then
						set Message = 'Remark Is Needed.';
                        leave sp_FAMerge_Set;
					End if;


					set Query_Update = '';
					set Query_Update = concat('Update fa_trn_tassetmergeheader
											    set assetmergeheader_status = ''',@Merge_Status,''' ,
													update_by = ''',ls_Createby,''' ,
                                                    update_date = current_timestamp()
											Where assetmergeheader_gid = ',@Merge_Gid,'
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
											set Message = 'Error On Merge Update.';
											leave sp_FAMerge_Set;
										elseif    countRow > 0 then
											set sql_safe_updates=0;
											Delete from fa_tmp_tassetdetails
											where assetdetails_gid in (@Asset_Detail_Gids);
												set Message = 'SUCCESS';
									End if;


                      #select @Trn_Ref_Name,@Merge_Gid,
							 # @Merge_Status,@Trn_To_Type, @Trn_Role_Name,
                                      #   @Trn_Remarks,@Entity_Gid,ls_Createby;



			call sp_Trans_Set('update',@Trn_Ref_Name,@Merge_Gid,
							  @Merge_Status,@Trn_To_Type, @Trn_Role_Name,
                                         @Trn_Remarks,@Entity_Gid,ls_Createby, @Message);
					select @Message into @out_msg_tran;

                    #select @out_msg_tran;

				if @out_msg_tran > 0  then
					 set Message = 'SUCCESS';
                  elseif @out_msg_tran <= 0 then
                    set Message = concat('Fail On Tran Update. ',@out_msg_tran);
                    rollback;
					leave sp_FAMerge_Set;
				End if;

				End if;#APPOVED,REJECTED - End IF

			End if;
END