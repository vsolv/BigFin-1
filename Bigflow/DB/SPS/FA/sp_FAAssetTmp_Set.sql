CREATE  PROCEDURE `sp_FAAssetTmp_Set`(IN `ls_Action` varchar(32),IN `ls_Type` varchar(32),IN `ls_Sub_Type` varchar(32),
IN `lj_Details` json,IN `lj_File` json,IN `lj_Classification` json,IN `ls_Createby` varchar(32),OUT `Message` varchar(1024)
)
sp_AssetTmp_Set:BEGIN
### Ramesh - Sep 24 2019.
### Save the Asset data in a temp Table
declare Query_Insert varchar(9000);
declare Query_Update varchar(9000);
Declare Query_Column varchar(1024);
Declare Query_Value varchar(1024);
Declare errno int;
Declare msg varchar(1000);
declare countRow int;
Declare i int;
Declare Asset_Qty int;
Declare Asset_Product_Gid int;
Declare Asset_Barcode varchar(16);
Declare Asset_Date varchar(32);
Declare Asset_Group_Id int;


	DECLARE EXIT HANDLER FOR SQLEXCEPTION,sqlwarning
    BEGIN

     GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
     set Message = concat(errno , msg);
     ROLLBACK;
     END;

     select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid[0]'))) into @Entity_Gid;

             if @Entity_Gid is  null or @Entity_Gid = 0 or @Entity_Gid = '' then
					set Message = 'Entity Gid Is Needed.';
                    leave sp_AssetTmp_Set;
             End if;


 if ls_Type = 'FA_INITIAL' and ls_Sub_Type = 'TMP' then



	 select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Product_Gid'))) into Asset_Product_Gid;
     select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Qty'))) into Asset_Qty;
     select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Barcode'))) into Asset_Barcode;
     select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Date'))) into Asset_Date;
     select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Group_Id'))) into Asset_Group_Id;
     select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Asset_SubCat_Id'))) into @Asset_Asset_SubCat_Id;
     select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Cat_Id'))) into @Asset_Cat_Id;
     select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_SubCat_Id'))) into @Asset_SubCat_Id;
     select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Value'))) into @Asset_Value;   ### Single Asset Value Is Needed
     select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Cost'))) into @Asset_Cost;
     select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Description'))) into @Asset_Description;
     select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_CapDate'))) into @Asset_CapDate;
     select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Source'))) into @Asset_Source;
     select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Status'))) into @Asset_Status;
     select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_RequestFor'))) into @Asset_RequestFor;
     select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_RequestStatus'))) into @Asset_RequestStatus;
     select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_AssetOwner'))) into @Asset_AssetOwner;
	 select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_PONo'))) into @Asset_PONo;
     select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_CRNo'))) into @Asset_CRNo;
     select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_VendorName'))) into @Asset_VendorName;
     select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_ImagePath'))) into @Asset_ImagePath;
     select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Invoice_Gid'))) into @Asset_Invoice_Gid;
     select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Branch_Gid'))) into @Asset_Branch_Gid;
     select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Location_Gid'))) into @Asset_Location_Gid;
     select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_BS'))) into @Asset_BS;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_CC'))) into @Asset_CC;
     select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Ref_Name'))) into @Trn_Ref_Name; ##********
     select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_To_Type'))) into @Trn_To_Type;     ##********
     select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Role_Name'))) into @Trn_Role_Name;               ##********
     select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Trn_Remarks'))) into @Trn_Remarks; ##********
     select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Detail_Gids'))) into @Asset_Detail_Gids;

 ### Validation Pending


      if Asset_Qty = 0 and Asset_Qty is null then
			set Message ='Asset QuantityNeeded.';
            leave sp_AssetTmp_Set;
      End if;

						set Query_Column = '';
						set Query_Value = '';
				if @Asset_ImagePath <> '' and @Asset_ImagePath is not null then
							##### Query Starts.
						set Query_Column = concat(Query_Column, ' assetdetails_imagepath,');
						set Query_Value = concat(Query_Value, '''',@Asset_ImagePath,''',');
				End if;

                if @Asset_Invoice_Gid <> '' and @Asset_Invoice_Gid is not null then
						set Query_Column = concat(Query_Column, ' assetdetails_invoicegid,');
						set Query_Value = concat(Query_Value, '''',@Asset_Invoice_Gid,''',');
                End if;


                if @Asset_Location_Gid <> '' and @Asset_Location_Gid is not null then
						set Query_Column = concat(Query_Column, '   assetdetails_assetlocationgid,');
						set Query_Value = concat(Query_Value, '''',@Asset_Location_Gid,''',');
                End if;

		#select @Asset_Qty;
    set @Asset_QtyTmp = 1;
	set i = 0;
  #  set Asset_Qty = @Asset_Qty;
    While i <= Asset_Qty - 1 Do


					#select 	@Asset_Id, @Asset_Qty, @Asset_Barcode, @Asset_Date, @Asset_Group_Id, @Asset_Asset_SubCat_Id, @Asset_Cat_Id,
					                   #    @Asset_SubCat_Id,@Asset_Value, @Asset_Cost, @Asset_Description, @Asset_CapDate, @Asset_Source, @Asset_Status, @Asset_RequestFor,
									#	@Asset_RequestStatus,@Asset_AssetOwner,@Asset_PONo,@Asset_CRNo,@Asset_VendorName,@Entity_Gid,ls_Createby;



				#select DATE_ADD(b.assetdetails_capdate, INTERVAL a.assetcat_lifetime YEAR)
						#from fa_mst_tassetcat a inner join fa_trn_tassetdetails b
						#on a.assetcat_gid=@Asset_Asset_SubCat_Id
							#where b.assetdetails_isactive='Y' and b.assetdetails_isremoved='N'
							#and b.entity_gid in ('',@Entity_Gid,'') and a.assetcat_isactive='Y'
                           # and a.assetcat_isremoved='N'
                            #and a.entity_gid in ('',@Entity_Gid,'') into @AssetDetails_End_Date  ;

										select assetcat_lifetime into  @Months from fa_mst_tassetcat
										where assetcat_gid = @Asset_Asset_SubCat_Id ;

										SELECT ADDDATE(@Asset_CapDate, INTERVAL @Months MONTH) into @End_date;




				     select ifnull(max(cast(assetdetails_id as decimal)),0)+1 into @New_Asset_TmpId from fa_tmp_tassetdetails where assetdetails_id not like '%-%';

                    select ifnull(max(cast(assetdetails_id as decimal)),0)+1 into @New_Asset_TrnId from fa_trn_tassetdetails where assetdetails_id not like '%-%';




                     if @New_Asset_TmpId > @New_Asset_TrnId THEN
                       set @Asset_Id = @New_Asset_TmpId;
                     ELSEIF @New_Asset_TmpId <= @New_Asset_TrnId THEN
                       set @Asset_Id = @New_Asset_TrnId;
                     ELSE
                       set Message = 'Error On Asset New Id.';
                       leave sp_AssetTmp_Set;
                     End if;

					set Query_Insert = '';
					set Query_Insert = concat('INSERT INTO fa_tmp_tassetdetails (assetdetails_id, assetdetails_productgid,
													 assetdetails_qty, assetdetails_barcode, assetdetails_date, assetdetails_assetgroupid,
													 assetdetails_assetcatgid, assetdetails_cat, assetdetails_subcat, assetdetails_value,
                                                     assetdetails_cost, assetdetails_description, assetdetails_capdate,
													 assetdetails_source, assetdetails_status, assetdetails_requestfor,
                                                     assetdetails_requeststatus,assetdetails_assetowner,assetdetails_branchgid,assetdetails_bs,
                                                     assetdetails_cc,assetdetails_ponum,assetdetails_crnum,assetdetails_vendorname,assetdetails_enddate,
                                                     ',Query_Column,'entity_gid,create_by)
											VALUES (''',@Asset_Id,''', ''',Asset_Product_Gid,''',''',@Asset_QtyTmp,''',
													''',Asset_Barcode,''', ''',Asset_Date,''', ''',Asset_Group_Id,''',
													''',@Asset_Asset_SubCat_Id,''', ''',@Asset_Cat_Id,''',
													''',@Asset_SubCat_Id,''',''',@Asset_Value,''', ''',@Asset_Cost,''',
                                                    ''',@Asset_Description,''',''',@Asset_CapDate,''', ''',@Asset_Source,''',
                                                    ''',@Asset_Status,''', ''',@Asset_RequestFor,''',''',@Asset_RequestStatus,''',
                                                    ''',@Asset_AssetOwner,''',''',@Asset_Branch_Gid,''',''',@Asset_BS,''',''',@Asset_CC,''',
                                                    ''',@Asset_PONo,''',''',@Asset_CRNo,''',''',@Asset_VendorName,''',''',@End_date,''',',Query_Value,'''',@Entity_Gid,''',
                                                    ''',ls_Createby,''')');

                                set @Insert_query = Query_Insert;
								#SELECT @Insert_query;
								PREPARE stmt FROM @Insert_query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;

                                if countRow > 0 then
									set Message = 'SUCCESS';
                                 Else
                                     set Message = 'FAIL In Temp Insert.';
                                End if;

					set @Trn_Reftable_Gid='';
				    set @Asset_tmp_GidMax = @Trn_Reftable_Gid;
					select LAST_INSERT_ID() into @Trn_Reftable_Gid ;

				call sp_Trans_Set('Insert',@Trn_Ref_Name,@Trn_Reftable_Gid,
										 @Asset_RequestStatus,@Trn_To_Type, @Trn_Role_Name,
                                         @Trn_Remarks,@Entity_Gid, ls_Createby, @Message);
					select @Message into @out_msg_tran ;

				if @out_msg_tran = 'FAIL' then
					set Message = 'Failed On Tran Insert';
					leave sp_AssetTmp_Set;
				End if;




        set @lj_Details_Data = '';	#Asset_Detail_Gids#Trn_Reftable_Gid
                                set @lj_Details_Data = concat(
                                '{"Asset_Detail_Gids":"',@Trn_Reftable_Gid,'",
                                   "Status":"IN-PROCESS"
                                }');

                                ### TO DO No -
                               #select @lj_Details_Data;
						call sp_FAAsset_Set('INSERT','ASSET_INITIAL','TRAN',
                                @lj_Details_Data,'{}',lj_Classification,ls_Createby,@Message);
                                select @Message into @Out_Msg_Asset;
                               #select @Out_Msg_Asset;

                                if @Out_Msg_Asset = 'SUCCESS' then
									set Message = 'SUCCESS';
                                elseif @Out_Msg_Asset is null or @Out_Msg_Asset <> 'SUCCESS' then
                                    set Message = concat('FAIL In Asset Tran.',@Out_Msg_Asset);
                                End if;

				set @Assetdetails_Trn_Gid='';
				select LAST_INSERT_ID() into @Assetdetails_Trn_Gid ;
               #select @Assetdetails_Trn_Gid;

				update fa_tmp_tassetdetails
				set assetdetails_mainassetdetailsgid = @Assetdetails_Trn_Gid
				where assetdetails_gid=@Asset_Detail_Gids;

                 set i = i+1;
		End While;
       ### Validations

 elseif ls_Type = 'GROUP' and ls_Sub_Type = 'INITIAL' then
               select JSON_LENGTH(lj_Details,'$') into @li_Group_count;
					if @li_Group_count is null or @li_Group_count = 0 then
							set Message = 'No Data In Json - Group Details.';
                            leave sp_AssetTmp_Set;
					end if;

                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Cat_Gid'))) into @Asset_Cat_GidG;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_SubCat_Gid'))) into @Asset_SubCat_GidG;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_CPDate'))) into @Asset_CPDateG;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Value'))) into @Asset_ValueG;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Branch_Gid'))) into @Asset_Branch_GidG;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Group_MaxNo'))) into @Asset_Group_MaxNoG;

                #select @Asset_Cat_Gid,@Asset_SubCat_Gid,@Asset_CPDate,@Asset_Value,@Asset_Branch_Gid,@Asset_Group_MaxNo,@Entity_Gid,ls_Createby;

           set Query_Insert = '';
           set Query_Insert = concat('INSERT INTO fa_trn_tassetgroup (assetgroup_no,assetdetails_cat,assetdetails_subcat,assetgroup_capdate,
                                                     assetgroup_assetvalue,assetgroup_branchgid,entity_gid,create_by)
                                                     values (''',@Asset_Group_MaxNoG,''',''',@Asset_Cat_GidG,''',''',@Asset_SubCat_GidG,''',''',@Asset_CPDateG,''',
                                                     ''',@Asset_ValueG,''',''',@Asset_Branch_GidG,''',''',@Entity_Gid,''',''',ls_Createby,'''
                                                     )
													 ');

																   set @Insert_query = Query_Insert;
																#	SELECT @Insert_query;
																	PREPARE stmt FROM @Insert_query;
																	EXECUTE stmt;
																	set countRow = (select ROW_COUNT());
																	DEALLOCATE PREPARE stmt;

																	if countRow > 0 then
																		set Message = 'SUCCESS';
																	 Else
																		 set Message = 'FAIL';
																	End if;

 elseif ls_Type = 'ASSET_INITIAL' and ls_Sub_Type = 'CHECKER' then

         if ls_Action = 'UPDATE' then

						select JSON_LENGTH(lj_Details,'$') into @li_DetailjsonTmp_count;
					if @li_DetailjsonTmp_count is null or @li_DetailjsonTmp_count = 0 then
							set Message = 'No Data In Json - FA Details.';
                            leave sp_AssetTmp_Set;
					end if;

                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Detail_Gids'))) into @Asset_DetailTmp_Gids;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Status'))) into @ls_TmpStatus;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Remark'))) into @ls_TmpRemark;

                    set Query_Update = '';
                    set Query_Update = concat('Update fa_tmp_tassetdetails set assetdetails_requeststatus = ''',@ls_TmpStatus,'''
                                                   where assetdetails_gid in (',@Asset_DetailTmp_Gids,')
                    ');

											set @Query_Update = Query_Update;
                                    #        select Query_Update;
											PREPARE stmt FROM @Query_Update;
											EXECUTE stmt;
											set countRow = (select ROW_COUNT());
											DEALLOCATE PREPARE stmt;


											if countRow >  0 then
												set Message = 'SUCCESS';
                                             Else
                                                set Message = 'Error On FA Detail Status Change.';
                                                leave sp_AssetTmp_Set;
											End if;


         End if;



 elseif ls_Type = 'ASSET_PARENT' and ls_Sub_Type = 'MAKER' then
                            #### Club
						select JSON_LENGTH(lj_Details,'$') into @li_Detailjson_count;
						select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.AssetDetails_Gid'))) into @AssetDetails_Gid;
						select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.AssetDetails_Parent_Gid'))) into @AssetDetails_Parent_Gid_Tmp;
						select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Status'))) into @ls_Status;
						select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Request_For'))) into @ls_Request_For;
						select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Request_Status'))) into @ls_Request_Status;

							if @li_Detailjson_count is null or @li_Detailjson_count = 0 then
									set Message = 'No Data In Json - FA PARENT UPDATE';
									leave sp_AssetTmp_Set;
							end if;

                            if @AssetDetails_Parent_Gid_Tmp = 0  or @AssetDetails_Parent_Gid_Tmp = ''
								or @AssetDetails_Parent_Gid is null  then
									set Message = 'AssetDetails_Parent_Gid Is Not Given';
									leave sp_AssetTmp_Set;
							End if;

                            if  @ls_Status = '' or @ls_Status is null  then
									set Message = 'Status Is Not Given';
									leave sp_AssetTmp_Set;
							End if;

                            if  @ls_Request_For = '' or @ls_Request_For is null  then
                                 select @ls_Request_For;
									set Message = 'Request_For Is Not Given';
									leave sp_AssetTmp_Set;
							End if;

                            if  @ls_Request_Status = '' or @ls_Request_Status is null  then
									set Message = 'Request_Status Is Not Given';
									leave sp_AssetTmp_Set;
							End if;

                         set Query_Insert = '';
						 set Query_Insert = concat('
						  INSERT INTO fa_tmp_tassetdetails
							(assetdetails_id,assetdetails_qty,assetdetails_barcode,assetdetails_date,assetdetails_assetgroupid,
                            assetdetails_assetcatgid,assetdetails_cat,assetdetails_subcat,assetdetails_productgid,assetdetails_value,
                            assetdetails_cost,assetdetails_description,assetdetails_capdate,assetdetails_source,assetdetails_status,
                            assetdetails_requestfor,assetdetails_requeststatus,assetdetails_assettfrgid,
                            assetdetails_assetsalegid,assetdetails_not5k,assetdetails_assetowner,assetdetails_lease_startdate,
                            assetdetails_lease_enddate,assetdetails_impairassetgid,
                            assetdetails_impairasset,assetdetails_writeoffgid,assetdetails_assetcatchangegid,assetdetails_assetvaluegid,
                            assetdetails_assetcapdategid,assetdetails_assetsplitgid,assetdetails_assetmergegid,assetdetails_assetcatchangedate,
                            assetdetails_reducedvalue,assetdetails_branchgid,assetdetails_bs,assetdetails_cc,assetdetails_deponhold,assetdetails_deprate,assetdetails_parentgid,
                            assetdetails_assetserialno,
                            assetdetails_invoicegid,assetdetails_inwheadergid,assetdetails_inwdetailgid,assetdetails_inwarddate,assetdetails_mepno,
                            assetdetails_ponum,
                            assetdetails_crnum,assetdetails_imagepath,assetdetails_vendorname,assetdetails_mainassetdetailsgid,assetdetails_isactive,
                            assetdetails_isremoved,
                            entity_gid,create_by,assetdetails_assetlocationgid)
								(select assetdetails_id,assetdetails_qty,assetdetails_barcode,assetdetails_date,assetdetails_assetgroupid,
									assetdetails_assetcatgid,assetdetails_cat,assetdetails_subcat,assetdetails_productgid,assetdetails_value,
									assetdetails_cost,assetdetails_description,assetdetails_capdate,assetdetails_source,''',@ls_Status,''',
									''',@ls_Request_For,''',''',@ls_Request_Status,''',assetdetails_assettfrgid,assetdetails_assetsalegid,
									assetdetails_not5k,assetdetails_assetowner,assetdetails_lease_startdate,assetdetails_lease_enddate,
									assetdetails_impairassetgid,assetdetails_impairasset,assetdetails_writeoffgid,assetdetails_assetcatchangegid,
									assetdetails_assetvaluegid,assetdetails_assetcapdategid,assetdetails_assetsplitgid,
									assetdetails_assetmergegid,assetdetails_assetcatchangedate,assetdetails_reducedvalue,
									assetdetails_branchgid,assetdetails_bs,assetdetails_cc,assetdetails_deponhold,assetdetails_deprate,''',@AssetDetails_Parent_Gid_Tmp,''',
									assetdetails_assetserialno,assetdetails_invoicegid,assetdetails_inwheadergid,assetdetails_inwdetailgid,
									assetdetails_inwarddate,assetdetails_mepno,assetdetails_ponum,assetdetails_crnum,assetdetails_imagepath,
									assetdetails_vendorname,assetdetails_gid,assetdetails_isactive,assetdetails_isremoved,entity_gid,
									create_by,assetdetails_assetlocationgid
								from fa_trn_tassetdetails  where assetdetails_gid in (',@AssetDetails_Gid,')
								)
						 ');

								set @Insert_query = Query_Insert;
							#	SELECT @Insert_query,1;
								PREPARE stmt FROM @Insert_query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;

                              if countRow > 0 then
									set Message = 'SUCCESS';
									select LAST_INSERT_ID() into @AssetDetails_Maxgid ;
                               else
                                    set Message = 'FAIL insert';
                              End if;

                        set @Parent_Gid='';
							Select  assetdetails_gid	from fa_tmp_tassetdetails
							where assetdetails_mainassetdetailsgid in (@AssetDetails_Parent_Gid_Tmp) into @Parent_Gid;


                       if @Parent_Gid='' or @Parent_Gid is null then
						  set Message = 'Error On FA Detail Parent Update';
									leave sp_AssetTmp_Set;
                        End if;

                        set Query_Update = '';
						set Query_Update = concat('Update fa_tmp_tassetdetails
													  set update_by=''',ls_Createby,''',
														  update_date=now(),
														  assetdetails_parentgid = ',@Parent_Gid,'
													  where assetdetails_mainassetdetailsgid in (',@AssetDetails_Gid,')
												  ');

											set @Query_Update = Query_Update;
                                            #select Query_Update;
											PREPARE stmt FROM @Query_Update;
											EXECUTE stmt;
											set countRow = (select ROW_COUNT());
											DEALLOCATE PREPARE stmt;

                                           if countRow >  0 then
												set Message = 'SUCCESS';
                                             Else
                                                set Message = 'Error On FA Detail Parent Change.';
                                                leave sp_AssetTmp_Set;
											End if;

                                            call sp_Trans_Set('Insert','ASSET_CLUB',@AssetDetails_Parent_Gid_Tmp,'NEW',
											  'G','MAKER','CLUB',@Entity_Gid,ls_Createby,@message);
												select @message into @tran;

											if @tran <>0 or @tran <> '' then
													set Message = 'SUCCESS';
											else
													set Message = 'FAIL in tran';
													leave sp_AssetTmp_Set;
											end if;


  elseif ls_Type = 'ASSET_TMP' and ls_Sub_Type = 'MAKER' then
              ### used to Insert in TMP Table -- For All Transaction Pages.

              ### The Action is Insert

              		  select JSON_LENGTH(lj_Details,'$') into @li_Detailjson_count;
						if @li_Detailjson_count is null or @li_Detailjson_count = 0 then
                                set Message = 'No Data In Json - FA Details.';
								leave sp_AssetTmp_Set;
						end if;


						select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Detail_Gids'))) into @Asset_Detail_Gids;
						select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Status'))) into @ls_Request_For;

                        set @ls_Status = 'IN_ACTIVE';
                        set @ls_Request_Status = 'SUBMITTED';
                        #select @ls_Status,@ls_Request_For,@ls_Request_Status,@Asset_Detail_Gids;

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
							assetdetails_imagepath,assetdetails_vendorname,assetdetails_mainassetdetailsgid,assetdetails_isactive,assetdetails_isremoved,
                            entity_gid,create_by,assetdetails_assetlocationgid)
								(select assetdetails_id,assetdetails_qty,assetdetails_barcode,assetdetails_date,assetdetails_assetgroupid,assetdetails_assetcatgid,
								assetdetails_cat,assetdetails_subcat,assetdetails_productgid,assetdetails_value,assetdetails_cost,assetdetails_description,assetdetails_capdate,
								assetdetails_source,''',@ls_Status,''',''',@ls_Request_For,''',''',@ls_Request_Status,''',assetdetails_assettfrgid,
								assetdetails_assetsalegid,assetdetails_not5k,assetdetails_assetowner,assetdetails_lease_startdate,
								assetdetails_lease_enddate,assetdetails_impairassetgid,assetdetails_impairasset,
								assetdetails_writeoffgid,assetdetails_assetcatchangegid,assetdetails_assetvaluegid,assetdetails_assetcapdategid,	assetdetails_assetsplitgid,
								assetdetails_assetmergegid,current_date(),assetdetails_reducedvalue,
								assetdetails_branchgid,assetdetails_bs,assetdetails_cc,assetdetails_deponhold,assetdetails_deprate,assetdetails_parentgid,assetdetails_assetserialno,
								assetdetails_invoicegid,assetdetails_inwheadergid,assetdetails_inwdetailgid,assetdetails_inwarddate,assetdetails_mepno,
								assetdetails_ponum,assetdetails_crnum,assetdetails_imagepath,assetdetails_vendorname,assetdetails_gid,assetdetails_isactive,
								assetdetails_isremoved,entity_gid,create_by,assetdetails_assetlocationgid
								from fa_trn_tassetdetails  where assetdetails_gid in (',@Asset_Detail_Gids,')
								)
						 ');
                         #assetdetails_assetcatchangedate


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

                              ##### For Asset Book Value Change Process.

                              if @ls_Request_For = 'CAPDATE'  or @ls_Request_For = 'ASSETCAT' then

									Select ifnull(sum(b.depreciation_value),0) into@Dep_ValueD
									 from fa_trn_tassetdetails as a
									left join fa_trn_tdepreciation as b on b.depreciation_assetdetailsgid = a.assetdetails_gid
									inner join gal_mst_tproduct as c on c.product_gid = a.assetdetails_productgid
									where a.assetdetails_gid = @Asset_Detail_Gids;


                                    #select @Dep_ValueD;
                                   # select @New_cat_gid,@Asset_CPDate_NewD,@Dep_ValueD;



                                    if @Dep_ValueD <> 0 then


                                            if @ls_Request_For = 'CAPDATE' then
												select assetdetails_assetcatgid from fa_trn_tassetdetails
												where  assetdetails_gid = @Asset_Detail_Gids  into @New_cat_gid;
												select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_CPDate_New'))) into @Asset_CPDate_NewD;

											elseif @ls_Request_For = 'ASSETCAT' then

												select date_format(assetdetails_capdate,'%Y-%m-%d') from fa_trn_tassetdetails
												where  assetdetails_gid = @Asset_Detail_Gids into @Asset_CPDate_NewD;

											    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.New_Cat_Gid'))) into @New_cat_gid;
                                            End if;


                                        set @DepCalTo_DateD = date_format(now(),'%Y-%m-%d');

                                        select datediff(@DepCalTo_DateD,@Asset_CPDate_NewD) into @DepDaysD ;

                                       #select @DepCalTo_DateD,@Asset_CPDate_NewD;

                                       #select @New_cat_gid;
                                       #select @Asset_Detail_Gids;

										Select a.assetdetails_cost,a.assetdetails_value,b.assetcat_deptype,
									case
                                      when b.assetcat_deprate_itc <> 0 then b.assetcat_deprate_itc
                                      when b.assetcat_deprate_ca <> 0 then b.assetcat_deprate_ca
                                      when b.assetcat_deprate_mgmt <> 0 then b.assetcat_deprate_mgmt
                                	end,b.assetcat_lifetime
										into @asset_costD,@asset_valueD,@asset_deptypeD,@asset_deprateD,@asset_lifetimeD
									 from fa_trn_tassetdetails as a
									 inner join fa_mst_tassetcat as b on  b.assetcat_gid = @New_cat_gid
									where a.assetdetails_deponhold = 'N' and a.assetdetails_status = 'ACTIVE'
									and  a.assetdetails_isactive = 'Y' and a.assetdetails_isremoved = 'N'
									and b.assetcat_isactive = 'Y' and b.assetcat_isremoved = 'N'
                                    and a.assetdetails_gid = @Asset_Detail_Gids	;



                                    #select  @asset_costD,@asset_valueD,@asset_deptypeD,@asset_deprateD,@asset_lifetimeD;
											if @asset_deptypeD = 'SLM' then
												 ### Get Rate Per Day
												 set @DepValuePerDay = ((@asset_costD * @asset_deprateD) / 100)/365;
												 set @DepValueTotalD = @DepDaysD * @DepValuePerDay;
												 set @DepValueTotalD = cast(@DepValueTotalD as decimal(16,2));

											elseif @asset_deptypeD = 'WDV' then
													set @DepValuePerDay = ((@asset_valueD * @asset_deprateD) / 100)/365;
													set @DepValueTotalD = @DepDaysD * @DepValuePerDay;      ### TO DO Update
													set @DepValueTotalD = cast(@DepValueTotalD as decimal(16,2));
											 else
												 set Message = 'Error On Depreciation Type.';
												 leave sp_AssetTmp_Set;
											End if;

                                   #select @DepValuePerDay,@asset_valueD,@asset_deprateD,@DepDaysD,@DepValueTotalD,@Dep_ValueD;


										   set sql_safe_updates = 0 ;
										update fa_tmp_tassetdetails set assetdetails_cost = (assetdetails_cost  - @DepValueTotalD) where assetdetails_mainassetdetailsgid = @Asset_Detail_Gids ;

                                      #  select @DepValueTotalD;

                                    End if;

                              End if;

 elseif ls_Action='UPDATE' and ls_Type = 'ASSET_TMP' and ls_Sub_Type = 'TMP' then


			 select JSON_LENGTH(lj_Details,'$') into @li_Detailjson_count;
						if @li_Detailjson_count is null or @li_Detailjson_count = 0 then
                                set Message = 'No Data In Json - FA Details.';
								leave sp_AssetTmp_Set;
						end if;


					select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Asset_Tran_Gids'))) into @Asset_Tran_Gids;
					select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.AssetDetails_CapDate'))) into @AssetDetails_CapDate;
					select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.AssetDetails_Cat_Gid'))) into @AssetDetails_Cat_Gid;
					select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.AssetDetails_Branch_Gid'))) into @AssetDetails_Branch_Gid;

                    set @AssetDetails_CapDate=date_format(@AssetDetails_CapDate,'%Y-%m-%d');

							if @Asset_Tran_Gids is null or @Asset_Tran_Gids = '' then
                                set Message = 'Tran_Gids Is Not Given';
								leave sp_AssetTmp_Set;
							end if;


				set Query_Column = '';
				if @AssetDetails_CapDate <> '' and @AssetDetails_CapDate is not null then
						set Query_Column = concat(Query_Column, ',assetdetails_capdate=''',@AssetDetails_CapDate,''' ');
				End if;
                if @AssetDetails_Cat_Gid <> '' and @AssetDetails_Cat_Gid is not null then
						set Query_Column = concat(Query_Column, ',assetdetails_assetcatgid=''',@AssetDetails_Cat_Gid,''' ');
				End if;
                if @AssetDetails_Branch_Gid <> '' and @AssetDetails_Branch_Gid is not null then
						set Query_Column = concat(Query_Column, ',assetdetails_branchgid=''',@AssetDetails_Branch_Gid,''' ');
				End if;

						 set sql_safe_updates=0;
                         set Query_Update = '';
						 set Query_Update = concat('update fa_tmp_tassetdetails
														   set update_by=''',ls_Createby,''',
																update_date=''',Now(),'''
																',Query_Column,'
															where assetdetails_mainassetdetailsgid in (',@Asset_Tran_Gids,')
                                                            and assetdetails_isactive=''Y''
                                                            and assetdetails_isremoved=''N''
                                                            and entity_gid=',@Entity_Gid,'
												  ');

								set @Query_Update = Query_Update;
								#SELECT @Query_Update;
								PREPARE stmt FROM @Query_Update;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;

                              if countRow > 0 then
									set Message = 'SUCCESS';
                               else
                                    set Message = 'FAIL';
                              End if;

 End if;


END