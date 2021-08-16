CREATE  PROCEDURE `sp_FASplit_Set`(IN `ls_Action` varchar(32),
IN `ls_Type` varchar(32),IN `ls_Sub_Type` varchar(32),
IN `lj_Details` json,IN `lj_Classification` json,IN `ls_Createby` varchar(32),
OUT `Last_Id` int(11) ,OUT `Message` varchar(1024))
sp_FASplit_Set:BEGIN
#### Bala Nov 01 2019

Declare errno int;
Declare msg varchar(1000);
Declare countRow int;
Declare Query_Insert varchar(9000);
Declare Query_Update varchar(2048);
Declare Query_Delete varchar(2048);

DECLARE EXIT HANDLER FOR SQLEXCEPTION,sqlwarning

    BEGIN

     GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
     set Message = concat(errno , msg);
     ROLLBACK;
     END;

	select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid[0]'))) into @Entity_Gid;

             if @Entity_Gid is  null or @Entity_Gid = 0 or @Entity_Gid = '' then
					set Message = 'Entity Gid Is Needed.';
                    leave sp_FASplit_Set;
             End if;

if ls_Type = 'ASSET_SPLIT' and ls_Sub_Type = 'HEADER' then
		select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_Id'))) into @Asset_Id;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Split_Date'))) into @Split_Date;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Split_Reason'))) into @Split_Reason;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Split_Value'))) into @Split_Value;


        select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_To_Type'))) into @Trn_To_Type;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Role_Name'))) into @Trn_Role_Name;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Ref_Name'))) into @Trn_Ref_Name;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Remarks'))) into @Trn_Remarks;




        set @Split_Status = 'SUBMITTED';

        if @Asset_Id = '' or @Asset_Id is null then
				set Message = 'Asset ID Is Needed.';
                leave sp_FASplit_Set;
        End if;

        if @Split_Date is null or @Split_Date = '' then
			set Message = 'Split Date Is  Needed.';
            leave sp_FASplit_Set;
        End if;

        if @Split_Value is null or @Split_Value = '' then
			set Message = 'Split Value Is Needed.';
            leave sp_FASplit_Set;
        End if;

        #select @Asset_Id,@Split_Date,@Split_Status,@Split_Reason,@Split_Value,@Entity_Gid;

        set Query_Insert = '';
        set Query_Insert  = concat('insert into fa_trn_tassetsplitheader (assetsplitheader_assetdetailsid,assetsplitheader_date,assetsplitheader_status,assetsplitheader_reason,
													assetsplitheader_value,entity_gid,create_by)
													values (''',@Asset_Id,''',''',@Split_Date,''',''',@Split_Status,''',''',@Split_Reason,''',''',@Split_Value,''',''',@Entity_Gid,''',''',ls_Createby,'''
                                                    )  ');

												set @Insert_query = Query_Insert;
												#SELECT @Insert_query;
												PREPARE stmt FROM @Insert_query;
												EXECUTE stmt;
												set countRow = (select ROW_COUNT());
												DEALLOCATE PREPARE stmt;

											  if countRow > 0 then
													select LAST_INSERT_ID() into Last_Id;
                                                    set Message = 'SUCCESS';
											   else
													set Message = 'FAIL';
                                                    leave sp_FASplit_Set;
											  End if;

								#select @Trn_Ref_Name,Last_Id,
										 #@Split_Status,@Trn_To_Type, @Trn_Role_Name,
                                         #@Trn_Remarks,@Entity_Gid, ls_Createby;

			  call sp_Trans_Set('Insert',@Trn_Ref_Name,Last_Id,
										 @Split_Status,@Trn_To_Type, @Trn_Role_Name,
                                         @Trn_Remarks,@Entity_Gid, ls_Createby, @Message);
					select @Message into @out_msg_tran ;

									#select @out_msg_tran;

				if @out_msg_tran>0 then
					set Message = 'SUCCESS';
                else
					set Message = 'Failed On Tran Insert';
					leave sp_FASplit_Set;
				End if;


 elseif ls_Type = 'ASSET_SPLIT' and ls_Sub_Type = 'DETAIL' then
                       #### Asset Detail Table Insert :: It will 2 or 3 times
					select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_Header_Gid'))) into @Asset_Header_Gid;
					select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_New_Id'))) into @Asset_New_Id;
					select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Split_Value'))) into @Split_Value;

					if @Asset_Header_Gid = '' or @Asset_Header_Gid is null then
							set Message = 'Split Header  Id Is Needed.';
							leave sp_FASplit_Set;
					End if;

					if @Asset_New_Id is null or @Asset_New_Id = '' then
						set Message = 'New Asset Id Is  Needed.';
						leave sp_FASplit_Set;
					End if;

					if @Split_Value is null or @Split_Value = '' then
						set Message = 'Split Value Is Needed.';
						leave sp_FASplit_Set;
					End if;

					set Query_Insert = '';
                    #select @Asset_Header_Gid,@Asset_New_Id,@Split_Value,@Entity_Gid,ls_Createby;
					set Query_Insert  = concat('insert into fa_trn_tassetsplit
													(assetsplit_assetsplitheader_gid,assetsplit_newassetdetailsid,
                                                    assetsplit_value,entity_gid,create_by)
													values (''',@Asset_Header_Gid,''',''',@Asset_New_Id,''',
                                                    ''',@Split_Value,''',''',@Entity_Gid,''',''',ls_Createby,'''
                                                    )  ');

												set @Insert_query = '';
												set @Insert_query = Query_Insert;
												#SELECT @Insert_query;
												PREPARE stmt FROM @Insert_query;
												EXECUTE stmt;
												set countRow = (select ROW_COUNT());
												DEALLOCATE PREPARE stmt;

											  if countRow > 0 then
													#select LAST_INSERT_ID() into Last_Id;
                                                    set Message = 'SUCCESS';
											   else
													set Message = 'FAIL';
                                                    leave sp_FASplit_Set;
											  End if;

 elseif ls_Type = 'ASSET_SPLIT' and (ls_Sub_Type = 'TEMP_OLD' or ls_Sub_Type = 'TEMP_NEW' ) then

               select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_Id'))) into @New_Asset_Id;
               select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Split_Value'))) into @Split_Value;
               select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_Split_Gid'))) into @Asset_Split_Gid;

               if @Asset_Split_Gid is null or @Asset_Split_Gid = 0 then
					set Message = 'Asset Split Gid Is Needed.';
                    leave sp_FASplit_Set;
               End if;


                    if ls_Sub_Type = 'TEMP_OLD' then
					     	select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_Gid'))) into @Asset_Gid;
                    End if;

					set @ls_Status = 'IN_ACTIVE';
                    set @ls_Request_For = 'SPLIT';
                    set @ls_Request_Status = 'SUBMITTED';
                    ### Bala 19
                    #set @New_Asset_Id = '';
                    #select ifnull(max(cast(assetdetails_id as decimal)),1) + 100 into @New_Asset_Id from fa_tmp_tassetdetails;
                    ## Bala 19
                    #select @New_Asset_Id;
                    ##### Creation Of New Asset
                    #select @New_Asset_Id,@Split_Value,@ls_Status,@ls_Request_For,@ls_Request_Status,@Asset_Gid;
                   if ls_Sub_Type = 'TEMP_NEW' then
                    select ifnull(max(cast(assetdetails_id as decimal)),0)+1 into @New_Asset_TmpId from fa_tmp_tassetdetails where assetdetails_id not like '%-%';
                    select ifnull(max(cast(assetdetails_id as decimal)),0)+1 into @New_Asset_TrnId from fa_trn_tassetdetails where assetdetails_id not like '%-%';

                     if @New_Asset_TmpId > @New_Asset_TrnId THEN
                       set @New_Asset_Id = @New_Asset_TmpId;
                     ELSEIF @New_Asset_TmpId <= @New_Asset_TrnId THEN
                       set @New_Asset_Id = @New_Asset_TrnId;
                     ELSE
                       set Message = 'Error On Asset New Id.';
                       leave sp_FASplit_Set;
                     End if;
                    ### TO DO Not Needed
                   elseif ls_Sub_Type = 'TEMP_OLD' then
                      set @New_Asset_Id = @New_Asset_Id;
                   End if;


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
							assetdetails_imagepath,assetdetails_vendorname,assetdetails_mainassetdetailsgid,
                            assetdetails_isactive,assetdetails_isremoved,entity_gid,create_by,assetdetails_assetlocationgid)
								(select ''',@New_Asset_Id,''',assetdetails_qty,assetdetails_barcode,assetdetails_date,assetdetails_assetgroupid,assetdetails_assetcatgid,
								assetdetails_cat,assetdetails_subcat,assetdetails_productgid,''',@Split_Value,''',assetdetails_cost,assetdetails_description,assetdetails_capdate,
								assetdetails_source,''',@ls_Status,''',''',@ls_Request_For,''',''',@ls_Request_Status,''',assetdetails_assettfrgid,
								assetdetails_assetsalegid,assetdetails_not5k,assetdetails_assetowner,assetdetails_lease_startdate,
								assetdetails_lease_enddate,assetdetails_impairassetgid,assetdetails_impairasset,
								assetdetails_writeoffgid,assetdetails_assetcatchangegid,assetdetails_assetvaluegid,assetdetails_assetcapdategid,	''',@Asset_Split_Gid,''',
								assetdetails_assetmergegid,assetdetails_assetcatchangedate,assetdetails_reducedvalue,
								assetdetails_branchgid,assetdetails_bs,assetdetails_cc,assetdetails_deponhold,assetdetails_deprate,assetdetails_parentgid,assetdetails_assetserialno,
								assetdetails_invoicegid,assetdetails_inwheadergid,assetdetails_inwdetailgid,assetdetails_inwarddate,assetdetails_mepno,
								assetdetails_ponum,assetdetails_crnum,assetdetails_imagepath,assetdetails_vendorname,assetdetails_gid,assetdetails_isactive,
								assetdetails_isremoved,entity_gid,create_by,assetdetails_assetlocationgid
								from fa_trn_tassetdetails  where assetdetails_gid in (',@Asset_Gid,')
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
                                    #select LAST_INSERT_ID() into @New_Asset_Id;
                               else
                                    set Message = 'FAIL';
                              End if;


Elseif ls_Type = 'ASSET_SPLIT' and ls_Sub_Type = 'CHECKER' then

				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Split_Gid'))) into @Split_Gid;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Split_Status'))) into @Split_Status;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_To_Type'))) into @Trn_To_Type;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Role_Name'))) into @Trn_Role_Name;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Ref_Name'))) into @Trn_Ref_Name;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Remarks'))) into @Trn_Remarks;

					if @Split_Gid is null or cast(@Split_Gid as decimal(16,2))  = 0 then
						set Message = 'Split_Gid Is Needed.';
                        leave sp_FASplit_Set;
					End if;

					if @Split_Status is null or @Split_Status = '' then
						set Message = 'Split_Status Is Needed.';
                        leave sp_FASplit_Set;
					End if;


                    set @Asset_Detail_Gids='';

					select group_concat(assetsplit_newassetdetailsid)
						 from fa_trn_tassetsplit
                         where  assetsplit_isactive='Y'
                         and assetsplit_isremoved='N' and entity_gid=@Entity_Gid
                         and assetsplit_assetsplitheader_gid=@Split_Gid into @Asset_Detail_Gids;


               if  @Split_Status='APPROVED' then

					set Query_Update = '';
					set Query_Update = concat('Update fa_trn_tassetsplitheader
											    set assetsplitheader_status = ''',@Split_Status,''' ,
													update_by = ''',ls_Createby,''' ,
                                                    update_date = current_timestamp()
											Where assetsplitheader_gid = ',@Split_Gid,'
												  and entity_gid = ',@Entity_Gid,' and
                                                  assetsplitheader_isactive=''Y'' and
                                                  assetsplitheader_isremoved=''N''
											 ');

									set @Query_Update = '';
									set @Query_Update = Query_Update;
								    #select @Query_Update; ### Remove IT
									PREPARE stmt FROM @Query_Update;
									EXECUTE stmt;
									set countRow = (select ROW_COUNT());
									DEALLOCATE PREPARE stmt;

									if countRow <= 0 then
										set Message = 'Error On split Update.';
										leave sp_FASplit_Set;
									 elseif    countRow > 0 then
										set Message = 'SUCCESS';
									End if;


					set @ls_Status = 'ACTIVE';


						 set Query_Insert = '';
						 set Query_Insert = concat('
							INSERT INTO fa_trn_tassetdetails
									(assetdetails_id,assetdetails_qty,assetdetails_barcode,assetdetails_date,assetdetails_assetgroupid,
										assetdetails_assetcatgid,
										assetdetails_cat,assetdetails_subcat,assetdetails_productgid,assetdetails_value,
                                        assetdetails_cost,assetdetails_description,assetdetails_capdate,
										assetdetails_source,assetdetails_status,assetdetails_requestfor,assetdetails_requeststatus,
                                        assetdetails_assettfrgid,assetdetails_assetsalegid,assetdetails_not5k,
                                        assetdetails_assetowner,assetdetails_lease_startdate,
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
							(select assetdetails_id,assetdetails_qty,assetdetails_barcode,assetdetails_date,assetdetails_assetgroupid,
										assetdetails_assetcatgid,assetdetails_cat,assetdetails_subcat,assetdetails_productgid,assetdetails_value,
                                        assetdetails_cost,assetdetails_description,assetdetails_capdate,
										assetdetails_source,''',@ls_Status,''','''',''',@Split_Status,''',assetdetails_assettfrgid,
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
									from fa_tmp_tassetdetails  where assetdetails_id in (',@Asset_Detail_Gids,'))');

								set @Insert_query = Query_Insert;
								#SELECT @Insert_query;
								PREPARE stmt FROM @Insert_query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;

                              if countRow > 0 then
										set sql_safe_updates=0;
										set Query_Delete = '';
										set Query_Delete = concat('Delete from fa_tmp_tassetdetails
																where assetdetails_assetsplitgid in
																(',@Split_Gid,')');
										set @Query_Delete = '';
										set @Query_Delete = Query_Delete;
										#select @Query_Delete; ### Remove IT
										PREPARE stmt FROM @Query_Delete;
										EXECUTE stmt;
										set countRow = (select ROW_COUNT());
										DEALLOCATE PREPARE stmt;

										if countRow <= 0 then
											set Message = 'Error On Delete .';
											leave sp_FASplit_Set;
										elseif    countRow > 0 then
											set Message = 'SUCCESS';
										End if;

							   set Message = 'SUCCESS';
                               else
                                    set Message = 'FAIL In Split';
                               End if;

							select @Trn_Ref_Name,@Split_Gid,
										 'APPROVE',@Trn_To_Type, @Trn_Role_Name,
                                         @Trn_Remarks,@Entity_Gid,ls_Createby;


					call sp_Trans_Set('update',@Trn_Ref_Name,@Split_Gid,
										 'APPROVE',@Trn_To_Type, @Trn_Role_Name,
                                         @Trn_Remarks,@Entity_Gid,ls_Createby, @Message);
					select @Message into @out_msg_tran;

                    #select @out_msg_tran;

				if @out_msg_tran > 0  then
					 set Message = 'SUCCESS';
                  elseif @out_msg_tran <= 0 then
                    set Message = concat('Fail On Tran Update. ',@out_msg_tran);
                    rollback;
					leave sp_FASplit_Set;
				End if;

			  Elseif @Split_Status='REJECTED' then

				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Detail_Gids'))) into @Asset_Detail_Gids;

                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Remark'))) into @Remark;

					if @Remark is null or @Remark = '' then
						set Message = 'Remark Is Needed.';
                        leave sp_FASplit_Set;
					End if;


					set Query_Update = '';
					set Query_Update = concat('Update fa_trn_tassetsplitheader
											      set assetsplitheader_status = ''',@Split_Status,''' ,
													  update_by = ''',ls_Createby,''' ,
                                                      update_date = current_timestamp()
											   Where assetsplitheader_gid = ',@Split_Gid,'
												  and entity_gid = ',@Entity_Gid,' and
                                                  assetsplitheader_isactive=''Y'' and
                                                  assetsplitheader_isremoved=''N''
												');

									set @Query_Update = '';
									set @Query_Update = Query_Update;
								    #select @Query_Update; ### Remove IT
									PREPARE stmt FROM @Query_Update;
									EXECUTE stmt;
									set countRow = (select ROW_COUNT());
									DEALLOCATE PREPARE stmt;



									if countRow <= 0 then
											set Message = 'Error On split Update.';
											leave sp_FASplit_Set;

										elseif  countRow > 0 then
													set sql_safe_updates=0;
													set Query_Delete = '';
													set Query_Delete = concat('Delete from fa_tmp_tassetdetails
																				where assetdetails_assetsplitgid in
																   (',@Split_Gid,')');
													set @Query_Delete = '';
													set @Query_Delete = Query_Delete;
													#select @Query_Delete; ### Remove IT
													PREPARE stmt FROM @Query_Delete;
													EXECUTE stmt;
													set countRow = (select ROW_COUNT());
													DEALLOCATE PREPARE stmt;

													if countRow <= 0 then
														set Message = 'Error On Delete .';
														leave sp_FASplit_Set;
													elseif    countRow > 0 then
														set Message = 'SUCCESS';
													End if;
									set Message = 'SUCCESS';
									End if;

							    set Query_Update = '';
					            set Query_Update = concat('update fa_trn_tassetdetails set assetdetails_requestfor = '''' ,
                                                    update_by = ''',ls_Createby,''' ,
                                                      update_date = current_timestamp()
                                                    where assetdetails_gid in (',@Asset_Detail_Gids,')
												');

									set @Query_Update = '';
									set @Query_Update = Query_Update;
								    select @Query_Update; ### Remove IT
									PREPARE stmt FROM @Query_Update;
									EXECUTE stmt;
									set countRow = (select ROW_COUNT());
									DEALLOCATE PREPARE stmt;

								    	if countRow <= 0 then
														set Message = 'Error On Main Table Update .';
														leave sp_FASplit_Set;
													elseif    countRow > 0 then
														set Message = 'SUCCESS';
										End if;
                                    
                                   #select @Trn_Ref_Name,@Split_Gid, 
										#@Split_Status,@Trn_To_Type, @Trn_Role_Name,
                                        #@Trn_Remarks,@Entity_Gid,ls_Createby;
                                    
                     call sp_Trans_Set('update',@Trn_Ref_Name,@Split_Gid, 
										 @Split_Status,@Trn_To_Type, @Trn_Role_Name,
                                         @Trn_Remarks,@Entity_Gid,ls_Createby, @Message);
					select @Message into @out_msg_tran;                        
                    
                    #select @out_msg_tran,1;
																				
				if @out_msg_tran > 0  then
					 set Message = 'SUCCESS';
                  elseif @out_msg_tran <= 0 then
                    set Message = concat('Fail On Tran Update. ',@out_msg_tran);
                    rollback;
					leave sp_FASplit_Set;
				End if;                                        
                    
			  End if;       
End if;
    
    
END