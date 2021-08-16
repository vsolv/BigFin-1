CREATE PROCEDURE `sp_FAAssetProcess_Set`(IN `ls_Action` varchar(32),IN `ls_Type` varchar(32),
IN `ls_Sub_Type` varchar(32),IN `lj_Details` json,IN `lj_Change` json,IN `lj_File` json,IN `lj_Status` Json, IN `lj_Classification` json,
IN `ls_Createby` varchar(16),OUT `Message` varchar(1024)
)
sp_FAAssertProcess_Set:BEGIN
# Ramesh Sep 19 2019
# Bala
Declare errno int;
Declare msg varchar(1000);
Declare i int;
Declare j int;
Declare Query_Select varchar(2048);
Declare countRow int;
Declare AssetDetails_Gid varchar(2048);
Declare Asset_Value varchar(2048);
Declare Asset_Value_Date varchar(2048);
Declare Query_Update varchar(2048);

Declare lj_AssetDetails json;

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

     select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid[0]'))) into @Entity_Gid;

             if @Entity_Gid is  null or @Entity_Gid = 0 or @Entity_Gid = '' then
					set Message = 'Entity Gid Is Needed.';
                    leave sp_FAAssertProcess_Set;
             End if;

start transaction;
set autocommit = 0 ;
if ls_Type = 'ASSET_MAKER' and  ls_Sub_Type = 'TEMP' then
        ## Set The Asset Data in Temp Table.
		if ls_Action = 'INSERT' then

                select JSON_LENGTH(lj_Details,'$.ASSET') into @li_json_count_Details ;

                   if @li_json_count_Details is null or @li_json_count_Details = 0 then
						set Message = 'No Data In Json - data.';
						leave sp_FAAssertProcess_Set;
					end if;

				   set @Invoice_Detail_Gid_Check = 0;
                   set i = 0;
                   While i <=  @li_json_count_Details -1 do

                                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.ASSET[',i,'].Invoice_Gid'))) into @Invoice_Gid;
                                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.ASSET[',i,'].Invoice_Detail_Gid'))) into @Invoice_Detail_Gid;
								select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.ASSET[',i,'].Product_Gid'))) into @Product_Gid;
                                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.ASSET[',i,'].Asset_Qty'))) into @Asset_Qty;
                                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.ASSET[',i,'].Asset_Asset_SubCat_Gid'))) into @Asset_Asset_SubCat_Id;#### Not Used :: Select From The Table
                                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.ASSET[',i,'].Asset_Value'))) into @Asset_Value;
                                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.ASSET[',i,'].CP_Date'))) into @CP_Date; ### date Validations TO DO
                                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.ASSET[',i,'].Location_Gid'))) into @Asset_Location_Gid;
                                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.ASSET[',i,'].Captilisation_Type'))) into @Captilisation_Type;
                                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.ASSET[',i,'].CWIP_Gid'))) into @CWIP_Gid;
                               select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.ASSET[',i,'].BS_NO'))) into @BS_NO;
                              select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.ASSET[',i,'].CC_NO'))) into @CC_NO;

                             if  @Invoice_Gid is null or @Invoice_Gid = 0 THEN
                                set Message = 'Invoice Gid Is Needed.';
                                rollback;
                                leave sp_FAAssertProcess_Set;
                             End if;

                             if @Invoice_Detail_Gid is null or @Invoice_Detail_Gid = 0 THEN
                               set Message = 'Invoice Detail Gid Is Needed.';
                               rollback;
                              leave  sp_FAAssertProcess_Set;
                             End if;

                             if @Product_Gid is null or @Product_Gid = 0 THEN
                               set Message = 'Product Gid Is Needed.';
                              rollback;
                              leave sp_FAAssertProcess_Set;
                             End if;

                             if @Asset_Qty is null or @Asset_Qty = 0 THEN
                               set Message  = 'Asset Quantity Is Needed.';
                              rollback;
                               leave  sp_FAAssertProcess_Set;
                             End if;

                            if @Asset_Value is null or @Asset_Value = 0 THEN
                              set Message = 'Asset Value Is Needed.';
                             rollback;
                              leave sp_FAAssertProcess_Set;
                            End if;

                           if @CP_Date is null or @CP_Date = '' THEN
                             set Message = 'Captilize Date Is Needed.';
                            rollback;
                             leave sp_FAAssertProcess_Set;
                           End if;

                           if @Asset_Location_Gid is null or @Asset_Location_Gid = 0 THEN
                             set Message = 'Asset Location Is Needed.';
                            rollback;
                              leave sp_FAAssertProcess_Set;
                           End if;

                           if @Captilisation_Type is null or @Captilisation_Type = '' THEN
                             set Message = 'Captilisation Type Is Needed.';
                            rollback;
                             leave sp_FAAssertProcess_Set;
                           End if;

                                ### Getting Category and Sub cat from Product Table
                                Select a.product_category_gid,a.product_subcategory_gid into @Category_Gid,@Subcat_Gid
								from gal_mst_tproduct as a where product_gid = @Product_Gid and a.product_isactive = 'Y' and a.product_isremoved = 'N' and a.entity_gid = @Entity_Gid ;
                                ### TO DO Validation Pending

                                set @Asset_PONo = '';
                                Select ifnull(b.poheader_no,''),ifnull(c.invoiceheader_crno,''),ifnull(d.supplier_name,'')  into @Asset_PONo,@Asset_CRNo,@Vendor_Name
                                from ap_map_tinvoicepo as a
								inner join gal_trn_tpoheader as b on b.poheader_gid = a.invoicepo_poheadergid
                                inner join ap_trn_tinvoiceheader as c on c.invoiceheader_gid = a.invoicepo_invoiceheadergid
                                inner join gal_mst_tsupplier as d on d.supplier_gid = b.poheader_supplier_gid
								where a.invoicepo_invoiceheadergid = @Invoice_Gid  and a.invoicepo_isactive = 'Y' and a.invoicepo_isremoved = 'N'
								and b.poheader_isactive = 'Y' and b.poheader_isremoved = 'N'
								and a.entity_gid = @Entity_Gid
                                and c.invoiceheader_isactive = 'Y' and c.invoiceheader_isremoved = 'N'
                                and d.supplier_isactive = 'Y' and d.supplier_isremoved = 'N'
                                limit 1 ;

                                if @Asset_PONo = '' then
										set Message = 'Error While Getting PO Number.';
									    rollback;
                                        leave sp_FAAssertProcess_Set;
                                End if;

                                if @Asset_CRNo = '' then
										set Message = 'Error While Getting CR Number.';
									    rollback;
                                        leave sp_FAAssertProcess_Set;
                                End if;

                                if @Vendor_Name = '' then
                                       set Message = 'Error While Getting Vendor Name.';
                                        rollback;
                                        leave sp_FAAssertProcess_Set;
                                End if;

								set @Asset_Date  = date_format(now(),'%Y-%m-%d');
								#set @Asset_Group_Id = '1'; ### Based on Group Table
                                       set @Asset_Barcode = 1;
                                       set @Asset_Max_Gid = 0;
                                       ### File Part

								select JSON_LENGTH(lj_File,'$') into @li_json_class_filepath;

                               # select @li_json_class_filepath;

								if  @li_json_class_filepath is not null and @li_json_class_filepath <> 0 then
										set j = 0;
                                        While j <= @li_json_class_filepath  -1 Do

                                                select JSON_UNQUOTE(JSON_EXTRACT(lj_File,CONCAT('$[',j,'].RefTable_Gid'))) into @RefTable_Gid;
                                                if @Invoice_Detail_Gid = @RefTable_Gid then
														select JSON_UNQUOTE(JSON_EXTRACT(lj_File,CONCAT('$[',j,'].SavedFilePath'))) into @file_Path;
														select JSON_UNQUOTE(JSON_EXTRACT(lj_File,CONCAT('$[',j,'].File_Name'))) into @file_Name;


                                                        set  @file_Id=0;

														call sp_File_Set('Insert','a',@file_Id,@file_Name,@file_Path,
																lj_Classification, '{}',ls_Createby ,@Message);
														 select @Message into @Out_Msg_Image;

														SELECT SUBSTRING_INDEX(@Out_Msg_Image, ',', 1) into @ctrl_file_gid;

                                                        #### Image Path Extra
                                                        if @file_Path <> '' and @file_Path is not null then
                                                            set @Image_Path = '';
															set @Image_Path = @file_Path;
                                                         else
                                                            set @Image_Path = '';
                                                        End if;
												End if;

                                            set j = j+1;
                                        End While;

                               else
                                     set @Image_Path = '';
								end if;

                                ### Grouping - If Captalize - CP date used - If CWIP - ?
                                if @Asset_Qty > 1 and @Captilisation_Type = 'A' then

                                      set @Asset_Branch_Gid = 1;### TO DO
                                      Select ifnull(max(assetgroup_no),0)+1 into @Asset_Group_MaxNo from fa_trn_tassetgroup;

                                    #select @Category_Gid,@Subcat_Gid,@CP_Date,@Asset_Tot_Value,@Asset_Branch_Gid,@Asset_Group_MaxNo;

                                    set @Asset_Tot_Value = cast(@Asset_Qty as decimal ) * cast(@Asset_Value as decimal );

									  set @lj_GroupDetail = '';
                                      set @lj_GroupDetail = concat('{
                                      "Asset_Cat_Gid":"',@Category_Gid,'",
                                      "Asset_SubCat_Gid":"',@Subcat_Gid,'",
                                      "Asset_CPDate":"',@CP_Date,'",
                                      "Asset_Value":"',@Asset_Tot_Value,'",
                                      "Asset_Branch_Gid":"',@Asset_Branch_Gid,'",
                                      "Asset_Group_MaxNo":"',@Asset_Group_MaxNo,'"
                                      }')
                                      ;

											#select @lj_GroupDetail;
											call sp_FAAssetTmp_Set('INSERT','GROUP','INITIAL',@lj_GroupDetail,'{}',lj_Classification,ls_Createby,@Message);
											select @Message into @Out_Msg_Group;

                                          #  select @Out_Msg_Group;

                                        if @Out_Msg_Group = 'SUCCESS' then
											set @Message = 'SUCCESS';
                                          select max(assetgroup_gid) into @Asset_Max_Gid from fa_trn_tassetgroup;
                                        elseif @Out_Msg_Group is null or @Out_Msg_Group <> '' or @Out_Msg_Group = 'FAIL' then
                                             set Message = 'FAIL';
                                             rollback;
                                             leave sp_FAAssertProcess_Set;
                                        End if;

								End if;
                                       set @Asset_Group_Id = @Asset_Max_Gid;
                                       set @Asset_Branch_Gid = 0;
                           Select ifnull(invoiceheader_branchgid,0) into @Asset_Branch_Gid from ap_trn_tinvoiceheader
                          where invoiceheader_gid = @Invoice_Gid and invoiceheader_isactive = 'Y' and invoiceheader_isremoved = 'N' ;

                          if @Asset_Branch_Gid = 0 THEN
                             set Message = 'Error On Invoice Branch Gid.';
                             rollback;
                             leave sp_FAAssertProcess_Set;
                          End if;

                               if @Captilisation_Type = 'A' then

				                 #select @Product_Gid,@Asset_Qty,@Asset_Barcode,@Asset_Date,@Asset_Group_Id,@Asset_Asset_SubCat_Id,
								   #	  @Category_Gid,@Subcat_Gid,@Asset_Value,@Asset_Value,@CP_Date,@Asset_PONo,@Asset_CRNo,
				                   #    @Vendor_Name,@Image_Path,@Invoice_Gid,@Asset_Branch_Gid,@Asset_Location_Gid;
				                                  ###  @Asset_Id not Needed
							     set lj_AssetDetails = '{}';
							     set lj_AssetDetails = concat(
							     '{ "Asset_Product_Gid":"',@Product_Gid,'",
									"Asset_Qty":"',@Asset_Qty,'",
								   "Asset_Barcode": "',@Asset_Barcode,'",
								   "Asset_Date":"',@Asset_Date,'",
								   "Asset_Group_Id":"',@Asset_Group_Id,'",
								   "Asset_Asset_SubCat_Id":"',@Asset_Asset_SubCat_Id,'",
								   "Asset_Cat_Id":"',@Category_Gid,'",
                                   "Asset_SubCat_Id":"',@Subcat_Gid,'",
                                   "Asset_Value":"',@Asset_Value,'",
                                   "Asset_Cost":"',@Asset_Value,'",
                                   "Asset_Description":"RT",
                                   "Asset_CapDate":"',@CP_Date,'",
                                   "Asset_Source":"NEW",
                                   "Asset_Status":"ACTIVE",
                                   "Asset_RequestFor":"NEW",
                                   "Asset_RequestStatus":"REQUESTED",
                                   "Asset_AssetOwner":"OWN",
                                   "Asset_PONo":"',@Asset_PONo,'",
                                   "Asset_CRNo":"',@Asset_CRNo,'",
                                   "Asset_VendorName":"',@Vendor_Name,'",
                                   "Asset_ImagePath":"',@Image_Path,'",
                                   "Asset_Invoice_Gid":"',@Invoice_Gid,'",
                                   "Asset_Branch_Gid":"',@Asset_Branch_Gid,'",
                                   "Location_Gid":"',@Asset_Location_Gid,'",
                                   "Asset_BS":"',@BS_NO,'",
                                   "Asset_CC":"',@CC_NO,'",
                                   "Trn_Ref_Name":"FA_MAKE",
                                   "Trn_To_Type":"G",
                                   "Trn_Role_Name":"MAKER",
                                   "Trn_Remarks":"MAKER"
							   }'
							   );


								 call sp_FAAssetTmp_Set('INSERT','FA_INITIAL','TMP',lj_AssetDetails,lj_File,
														lj_Classification,ls_Createby,@Message);
								 select @Message into @Out_Msg_AssetTmp;
							#select @Out_Msg_AssetTmp;
                                #select lj_AssetDetails;
                               #select lj_File;
								 if @Out_Msg_AssetTmp <> 'SUCCESS' or @Out_Msg_AssetTmp is null  then
                                           if @Out_Msg_AssetTmp is null then
												set @Out_Msg_AssetTmp = '';
                                           End if;

										set Message = concat('Error Occured On FA Initial Insert.',@Out_Msg_AssetTmp);
										rollback;
										leave sp_FAAssertProcess_Set;
								  elseif @Out_Msg_AssetTmp = 'SUCCESS' then
									  set Message = 'SUCCESS';

								 End if;


								if @CWIP_Gid is not null and @CWIP_Gid <> 0 THEN
								     set @lj_CWIP_Detail = '';
								     set @lj_CWIP_Detail = concat('{
                                          "CWIP_Gids":"',@CWIP_Gid,'",
                                          "CWIP_RequestNo":"',@Invoice_Gid,'",
                                          "CWIP_CPDATE":"',@CP_Date,'"
                                            }');


								    call sp_FACWIP_Set('INSERT', 'CWIP_TOASSET', 'ASSET_MAKE',
						               @lj_CWIP_Detail,'{}',lj_Classification,ls_Createby,@Message);
						              select @Message into @Out_Msg_Cwip;

						             if @Out_Msg_Cwip <> 'SUCCESS' THEN
						             	set Message = concat('Error In CWIP Save. -',@Out_Msg_Cwip);
						                ROLLBACK;
						                leave sp_FAAssertProcess_Set;
						             ELSEIF @Out_Msg_Cwip is null THEN
						               set Message = 'Error On CWIP Update.- Unknown Error.';
						               ROLLBACK;
						               leave sp_FAAssertProcess_Set;
						             End if;
								End if;

						ELSEIF @Captilisation_Type = 'C' THEN
						        set @lj_CWIP_Detail ='';
						       set @lj_CWIP_Detail = concat('{
						                 "CWIP_Qty":"',@Asset_Qty,'",
						                 "CWIP_Date":"',@CP_Date,'",
						                 "CWIP_Asset_Group_Gid":"',@Asset_Group_Id,'",
						                 "Asset_CatGid":"',@Asset_Asset_SubCat_Id,'",
						                 "CWIPProduct_Gid":"',@Product_Gid,'",
						                 "GL_Cat":"',@Category_Gid,'",
						                 "GL_SubCat":"',@Subcat_Gid,'",
						                 "Asset_Value":"',@Asset_Value,'",
						                 "Asset_Cost":"',@Asset_Value,'",
						                 "CWIP_Description":"RT",
						                 "CWIP_Status":"ACTIVE",
                                         "CWIP_RequestStatus":"PENDING",
                                         "CWIP_Owner":"OWN",
                                         "CWIP_Inv_Gid":"',@Invoice_Gid,'",
                                         "CWIP_Inw_Gid":"0",
                                         "CWIP_InwDetails_Gid":"0",
                                         "CWIP_Inw_Date":"1985-01-01",
                                         "CWIP_Mep_No":"888",
                                         "CWIP_PONo":"',@Asset_PONo,'",
                                         "CWIP_CRNo":"',@Asset_CRNo,'",
                                         "CWIP_ImagePath":"',@Image_Path,'",
                                         "CWIP_VendorName":"',@Vendor_Name,'",
                                         "CWIP_Group_Gid":"',@Asset_Location_Gid,'"

						                   }');

						                  ### TO DO - MEP No - Inw Date
						                  #select @lj_CWIP_Detail;

						       call sp_FACWIP_Set('INSERT', 'CWIP_INITIAL', 'MAKER',
						               @lj_CWIP_Detail,'{}',lj_Classification,ls_Createby,@Message);
						              select @Message into @Out_Msg_Cwip;

						             if @Out_Msg_Cwip <> 'SUCCESS' THEN
						             	set Message = concat('Error In CWIP Save. -',@Out_Msg_Cwip);
						                ROLLBACK;
						                leave sp_FAAssertProcess_Set;
						             ELSEIF @Out_Msg_Cwip is null THEN
						               set Message = 'Error On CWIP Save.- Unknown Error.';
						               ROLLBACK;
						               leave sp_FAAssertProcess_Set;
						             End if;

						ELSE
						   set Message = 'Error On Asset Captilisation Type.';
						   ROLLBACK;
						   leave sp_FAAssertProcess_Set;
						End if;
                        #### Update in Tran
                        #### The Same Inv Detail May come for Diffrfent Process.
					   if @Invoice_Detail_Gid_Check <> @Invoice_Detail_Gid then
					       set @lj_Details_Data = '';
							set @lj_Details_Data = concat('{"Invoice_Detail_Gid":"',@Invoice_Detail_Gid,'"}');

								#select @lj_Details_Data;
								call sp_APInvoice_Set('UPDATE','CAPTILIZE_UPDATE',
									'{}',@lj_Details_Data,'{}','{}',ls_Createby,@Entity_Gid,@Message);
								select @Message into @Out_Msg_Captilize_Update;

							if @Out_Msg_Captilize_Update <> 'SUCCESS' or @Out_Msg_Captilize_Update is null  then
									set Message = concat('Error Occured On Captilize Update',@Out_Msg_Captilize_Update);
									rollback;
									leave sp_FAAssertProcess_Set;
							elseif @Out_Msg_Captilize_Update = 'SUCCESS' then
									set Message = 'SUCCESS';
								 set @Invoice_Detail_Gid_Check = @Invoice_Detail_Gid;
							End if;

					   End if;

						set i = i+1;
                   End while;


           else
               set Message = 'Incorrect Action.';
          End if;
 elseif ls_Type = 'ASSET_CHECKER' and ls_Sub_Type = 'INITIAL' then
               ### Approve or Reject The Asset - Move from Tmp Table to Tran Table

           if ls_Action = 'UPDATE' then

					select JSON_LENGTH(lj_Details,'$') into @li_Detailjson_count;
					if @li_Detailjson_count is null or @li_Detailjson_count = 0 then
							set Message = 'No Data In Json - Asset Details.';
                            leave sp_FAAssertProcess_Set;
					end if;

					select JSON_LENGTH(lj_Status,'$') into @li_Statusjson_count;
					if @li_Statusjson_count is null or @li_Statusjson_count = 0 then
							set Message = 'No Data In Json - Asset Status.';
                            leave sp_FAAssertProcess_Set;
					end if;

                        select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,CONCAT('$.Status'))) into @ls_Status;

                        if @ls_Status is null or @ls_Status = '' then
								set Message = 'Status Is Needed.';
                                leave sp_FAAssertProcess_Set;
                        End if;

                        #### Get The Value by loop in a Variable
                                  select JSON_LENGTH(lj_Details, CONCAT('$.ASSET[0].Asset_Gid')) into @Asset_Gid_Count;

									if @Asset_Gid_Count is null or @Asset_Gid_Count = 0 or @Asset_Gid_Count = '' then
											set Message = 'Asset Detail Gid Is Needed.';
											leave sp_FAAssertProcess_Set;
									End if;
                        set i = 0 ;
								While i <= @Asset_Gid_Count - 1 DO

												select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].Asset_Gid[',i,']'))) into @AssetDetails_Gid;

											if @AssetDetails_Gid <> 0 then

																if @ls_Status = 'APPROVED' then
																			#### Call the Sp to Insert Teh Asset data from TMP table
																			set @lj_Details_Data = '';
																			set @lj_Details_Data = concat(
																			'{"Asset_Detail_Gids":"',@AssetDetails_Gid,'",
																			   "Status":"APPROVED",
                                                                               "Request_For":"SUCCESS",
																			   "Trn_Ref_Name":"FA_MAKE",
																			   "Trn_To_Type":"C",
																			   "Trn_Role_Name":"CHECKER",
																			   "Trn_Remarks":"APPROVE"
																			}'
																			);
																			#select @lj_Details_Data;
																			call sp_FAAsset_Set('INSERT','ASSET_CHECKER','APPROVE',@lj_Details_Data,'{}',lj_Classification,ls_Createby,@Message);
																			select @Message into @Out_Msg_Asset;
																			#select @Out_Msg_Asset;
																			if @Out_Msg_Asset = 'SUCCESS' then
																				set Message = 'SUCCESS';
																			elseif @Out_Msg_Asset is null or @Out_Msg_Asset <> 'SUCCESS' then
																				 set Message = concat('FAIL ',@Out_Msg_Asset);
																				 rollback;
                                                                                 leave sp_FAAssertProcess_Set;
																			End if;

															elseif @ls_Status = 'REJECTED' then
																	select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,CONCAT('$.Remark'))) into @ls_Remark;

																	if @ls_Remark is null  or @ls_Remark = '' then
																		set Message = 'Remark Is Needed For Reject.';
																	    rollback;
																		leave sp_FAAssertProcess_Set;
																	End if;

																	set @lj_Details_Data = '';
																			set @lj_Details_Data = concat(
																			'{"Asset_Detail_Gids":"',@AssetDetails_Gid,'",
																			   "Status":"REJECTED",
                                                                                "Trn_Ref_Name":"FA_MAKE",
																			   "Remark": "',@ls_Remark,'"
																			  }'
																			);

																			#select @AssetDetails_Gid,@ls_Remark;

																			#select @lj_Details_Data;

																			call sp_FAAsset_Set('UPDATE','ASSET_CHECKER','REJECT',@lj_Details_Data,
                                                                            '{}',lj_Classification,ls_Createby,@Message);
																			select @Message into @Out_Msg_Asset;

																			#select @Out_Msg_Asset;

																			if @Out_Msg_Asset = 'SUCCESS' then
																				set Message = 'SUCCESS';
																			elseif @Out_Msg_Asset is null or @Out_Msg_Asset <> 'SUCCESS' then
																				set Message = 'FAIL CHECKER';
																			End if;

															End if;

										end if;

									set i = i+1;
								End while;


           End if;


  elseif ls_Type = 'ASSET_WRITEOFF' and ls_Sub_Type = 'MAKER' then

              if ls_Action = 'UPDATE' then
				   #### To Write Off - Check The child Gid too.
                                 #### Get The Value by loop in a Variable
							select JSON_LENGTH(lj_Details, CONCAT('$.ASSET[0].Asset_Gid')) into @Asset_Gid_Count;
                          /*  select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].Asset_Gid'))) into @Asset_Writeoff_Fn_Gids;


										set @Fn_Json_Data = '';
										set @Fn_Json_Data = concat('{"ASSET":
																			 {"Asset_Gid":',@Asset_Writeoff_Fn_Gids,'}}');

				    set @Fn_Test= fn_FA_Data('ASSET_CLUB_CHECK',0,0,@Entity_Gid,@Fn_Json_Data);

									if @Fn_Test<>'SUCCESS' then
											set Message = 'Parent Is Miss Matched';
											leave sp_FAAssertProcess_Set;
									End if;*/

									if @Asset_Gid_Count is null or @Asset_Gid_Count = 0 or @Asset_Gid_Count = '' then
											set Message = 'Asset Detail Gid Is Needed.';
											leave sp_FAAssertProcess_Set;
									End if;

							select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.ASSET[0].Writeoff_Date'))) into @Writeoff_Date;
                              select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,'$.Remark')) into @WriteOff_Remark;

                              if @WriteOff_Remark is  null and @WriteOff_Remark = '' then
								set @WriteOff_Remark = '';
                              End if;

								set i = 0 ;
								While i <= @Asset_Gid_Count - 1 DO

										select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].Asset_Gid[',i,']'))) into @AssetDetails_Gid;

										if @AssetDetails_Gid <> 0 then

															set @msg = '';
															set @msg = (select fn_FA_Data('ASSET_REQUEST_CHECK',@AssetDetails_Gid,'',@Entity_Gid,'{}'));

															if @msg = 'SUCCESS' then
																set Message = 'SUCCESS';
															elseif @msg is null or @msg <> 'SUCCESS' then
																set Message = 'Already In Process';
                                                                rollback;
																leave sp_FAAssertProcess_Set;
															End if;

															set @lj_Details_Data = '';
															set @lj_Details_Data = concat(
															'{"Asset_Detail_Gids":"',@AssetDetails_Gid,'",
															   "Status":"WRITEOFF",
															   "Remark": "',@WriteOff_Remark,'"
															}'
															);
															#select AssetDetails_Gid,@ls_Remark;
															#select @lj_Details_Data;
															call sp_FAAssetTmp_Set('INSERT','ASSET_TMP','MAKER',@lj_Details_Data,'{}',lj_Classification,ls_Createby,@Message);
															select @Message into @Out_Msg_Asset;
															 ### TO DO
															 ### + Update The Write Off Table.
													      #select @Out_Msg_Asset;
															if @Out_Msg_Asset = 'SUCCESS' then
																set Message = 'SUCCESS';
															elseif @Out_Msg_Asset is null or @Out_Msg_Asset <> 'SUCCESS' then
																set Message = concat('FAIL-',@Out_Msg_Asset);
															End if;

                                                            #### Insert in Write Off Process Table.

																	set @lj_Writeoff_Data = '';
																	set @lj_Writeoff_Data = concat(
																	'{
																		"WriteOff_Date":"',@Writeoff_Date,'",
																		"WriteOff_Reason":"',@WriteOff_Remark,'",
																		"Asset_Detail_Gids":"',@AssetDetails_Gid,'"
																		}'
																	);

																	call sp_FAWriteoff_Set('INSERT','WRITEOFF_MAKER','TRAN',
																	@lj_Writeoff_Data,lj_Classification,ls_Createby,@Message);
																	select @Message   into @Out_Msg_writeOff;
                                                             #select @Out_Msg_writeOff;
                                                                    if @Out_Msg_writeOff <> 'SUCCESS' then
																			set Message = Concat('FAIL',@Out_Msg_writeOff);
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                    End if;


                                                                        # TO DO
                                                            ### Use if it Needed
													if AssetDetails_Gid <> '' then
															set AssetDetails_Gid = concat(AssetDetails_Gid,',',@AssetDetails_Gid);
													else
															set AssetDetails_Gid = @AssetDetails_Gid;
													end if;
										end if;

									set i = i+1;
								End while;

												##### Update The Main Table.
																	set @lj_Writeoff_Data = '';
                                                                    set @lj_Writeoff_Data =
                                                                    concat('{
                                                                    "Asset_Detail_Gids":"',AssetDetails_Gid,'",
                                                                    "RequestFor":"WRITEOFF"
                                                                    }');

																	call sp_FAAsset_Set('UPDATE', 'ASSET_CHECKER',
																	'REQUEST_FOR',
                                                                    @lj_Writeoff_Data,'{}',lj_Classification,ls_Createby,@Message);
                                                                    set @Out_Msg_WriteOff = '';
																	select @Message   into @Out_Msg_WriteOff;
															#select  @Out_Msg_WriteOff;

                                                                    if @Out_Msg_WriteOff <> 'SUCCESS' then
																			set Message = Concat('FAIL',@Out_Msg_WriteOff);
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                    End if;



              End if;

   elseif ls_Type = 'ASSET_CPDATE' and ls_Sub_Type = 'MAKER' then

              if ls_Action = 'UPDATE' then

				   #### To Write Off - Check The child Gid too.
                                 #### Get The Value by loop in a Variable
                                 select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].AssetDetails_CP_Date_New'))) into @Asset_CPDate_New;

                                 if @Asset_CPDate_New is null or @Asset_CPDate_New = '' then
									set Message = 'Asset New Captilize Date Is Needed.';
                                    leave sp_FAAssertProcess_Set;
                                 End if;

                        select JSON_LENGTH(lj_Details, CONCAT('$.ASSET[0].AssetDetails_Gid')) into @Asset_Gid_Count;

									if @Asset_Gid_Count is null or @Asset_Gid_Count = 0 or @Asset_Gid_Count = '' then
											set Message = 'Asset Detail Gid Is Needed.';
											leave sp_FAAssertProcess_Set;
									End if;
                                 select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,'$.Remark')) into @CPDate_Remark;

                              if @CPDate_Remark is  null and @CPDate_Remark = '' then
								set @CPDate_Remark = '';
                              End if;

                        set i = 0 ;
								While i <= @Asset_Gid_Count - 1 DO

										select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].AssetDetails_Gid[',i,']'))) into @AssetDetails_Gid;

												set @msg = '';
												set @msg = (select fn_FA_Data('ASSET_REQUEST_CHECK',@AssetDetails_Gid,'',@Entity_Gid,'{}'));

												if @msg = 'SUCCESS' then
													set Message = 'SUCCESS';
												elseif @msg is null or @msg <> 'SUCCESS' then
													set Message = 'Already In Process';
													rollback;
													leave sp_FAAssertProcess_Set;
												End if;

															  set @lj_Details_Data = '';
														set @lj_Details_Data = concat(
														'{"Asset_Detail_Gids":"',@AssetDetails_Gid,'",
														   "Asset_CPDate_New":"',@Asset_CPDate_New,'",
														   "Status":"CAPDATE",
														   "Remark": "',@CPDate_Remark,'"
														}'
														);
														#select @AssetDetails_Gid,@Asset_CPDate_New,@CPDate_Remark;
														#select @lj_Details_Data;
														call sp_FAAssetTmp_Set('INSERT','ASSET_TMP','MAKER',@lj_Details_Data,'{}',lj_Classification,ls_Createby,@Message);
														select @Message into @Out_Msg_Asset;

														 ### TO DO
														#select @Out_Msg_Asset;
														if @Out_Msg_Asset = 'SUCCESS' then
															set Message = 'SUCCESS';
														elseif @Out_Msg_Asset is null or @Out_Msg_Asset <> 'SUCCESS' then
															set Message = concat('FAIL -',@Out_Msg_Asset);
                                                            leave sp_FAAssertProcess_Set;
														End if;

                                                        #### Insert in Process Table

                                                        	set @lj_CPDate_Data = '';
																	set @lj_CPDate_Data = concat(
																	'{
																		"Asset_Detail_Gids":"',@AssetDetails_Gid,'",
																		"CapDate_Date":"',@Asset_CPDate_New,'",
                                                                        "CapDate_Reason":"',@CPDate_Remark,'",
                                                                        "TRN_Remarks":"',@CPDate_Remark,'"
																		}'
																	);

                                                        #select @lj_CPDate_Data;

                                                        call sp_FA_CapDate_Set('INSERT', 'CAPDATE_MAKER','TRAN',
																@lj_CPDate_Data,lj_Classification,ls_Createby,@Message);
																	select @Message into @Out_Msg_CPDate;
                                                    #select @Out_Msg_CPDate;
                                                                    if @Out_Msg_CPDate <> 'SUCCESS' then
																			set Message = concat('FAIL - ',@Out_Msg_CPDate);
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                    End if;


                                ### Use It If needed
										if @AssetDetails_Gid <> 0 then
												if AssetDetails_Gid <> '' then
														set AssetDetails_Gid = concat(AssetDetails_Gid,',',@AssetDetails_Gid);
												else
														set AssetDetails_Gid = @AssetDetails_Gid;
												end if;
										end if;

									set i = i+1;
								End while;


                                ##### Update The Main Table.
																	set @lj_CP_Data = '';
                                                                    set @lj_CP_Data =
                                                                    concat('{
                                                                    "Asset_Detail_Gids":"',AssetDetails_Gid,'",
                                                                    "RequestFor":"CAPDATE"
                                                                    }');

                                                                 #   select @lj_CP_Data;

																	call sp_FAAsset_Set('UPDATE', 'ASSET_CHECKER',
																	'REQUEST_FOR',
                                                                    @lj_CP_Data,'{}',lj_Classification,ls_Createby,@Message);
                                                                    set @Out_Msg_CPDate = '';
																	select @Message   into @Out_Msg_CPDate;
                                                       #select @Out_Msg_CPDate;
                                                                    if @Out_Msg_CPDate <> 'SUCCESS' then
																			set Message = Concat('FAIL',@Out_Msg_CPDate);
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                    End if;

															#### Update in Tmp Table CP Date
                                                            set @lj_Tmp_UpdateData = '';
                                                            set @lj_Tmp_UpdateData = concat(
                                                            '{
                                                            "Asset_Tran_Gids":"',AssetDetails_Gid,'",
                                                            "AssetDetails_CapDate":"',@Asset_CPDate_New,'"
                                                            }'
                                                            );

                                                         call sp_FAAssetTmp_Set('UPDATE', 'ASSET_TMP', 'TMP',
																  @lj_Tmp_UpdateData,'{}',
																 lj_Classification,ls_Createby,@Message);
																select @Message into @Out_Msg_CPTmp ;
                                                      #select @Out_Msg_CPTmp;
																	if @Out_Msg_CPTmp <> 'SUCCESS' then
																			set Message = concat('FAIL - ',@Out_Msg_CPTmp);
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                    End if;


              End if;

  elseif ls_Type = 'ASSET_IMPAIRMENT' and ls_Sub_Type = 'MAKER' then

              if ls_Action = 'UPDATE' then
				   #### To Write Off - Check The child Gid too.
                                 #### Get The Value by loop in a Variable
					select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].Impair_Date'))) into @Impair_Date;
                   /* select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].Asset_Gid'))) into @Asset_Fn_Gids;

                                 if @Impair_Date is null or @Impair_Date = '' then
									set Message = 'Asset Impaired Date Is Needed.';
                                    leave sp_FAAssertProcess_Set;
                                 End if;

										set @Fn_Json_Data = '';
										set @Fn_Json_Data = concat('{"ASSET":
																			 {"Asset_Gid":',@Asset_Fn_Gids,'}}');

				    set @Fn_Test= fn_FA_Data('ASSET_CLUB_CHECK',0,0,@Entity_Gid,@Fn_Json_Data);

									#select @Fn_Test;
									if @Fn_Test<>'SUCCESS' then
											set Message = 'Parent Is Miss Matched';
											leave sp_FAAssertProcess_Set;
									End if;*/


					select JSON_LENGTH(lj_Details, CONCAT('$.ASSET[0].Asset_Gid')) into @Asset_Gid_Count;

								    if @Asset_Gid_Count is null or @Asset_Gid_Count = 0 or @Asset_Gid_Count = '' then
											set Message = 'Asset Detail Gid Is Needed.';
											leave sp_FAAssertProcess_Set;
									End if;

                             select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,'$.Remark')) into @Impair_Remark;

                              if @Impair_Remark is  null and @Impair_Remark = '' then
								set @Impair_Remark = '';
                              End if;

                        set i = 0 ;
								While i <= @Asset_Gid_Count - 1 DO

										select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].Asset_Gid[',i,']'))) into @AssetDetails_Gid;
														##### Date Not Needed Here
														  set @lj_Details_Data = '';
														set @lj_Details_Data = concat(
														'{"Asset_Detail_Gids":"',@AssetDetails_Gid,'",
														   "Asset_ImpairDate":"',@Impair_Date,'",
														   "Status":"IMPAIRMENT",
														   "Remark": "',@Impair_Remark,'"
														}'
														);
														#select @AssetDetails_Gid,@Asset_CPDate_New,@CPDate_Remark;
														#select @lj_Details_Data;
														call sp_FAAssetTmp_Set('INSERT','ASSET_TMP','MAKER',@lj_Details_Data,'{}',lj_Classification,ls_Createby,@Message);
														select @Message into @Out_Msg_Asset;
														 ### TO DO
														#select @Out_Msg_Asset;
														if @Out_Msg_Asset = 'SUCCESS' then
															set Message = 'SUCCESS';
														elseif @Out_Msg_Asset is null or @Out_Msg_Asset <> 'SUCCESS' then
															set Message = concat('FAIL -',@Out_Msg_Asset);
														    rollback;
                                                            leave sp_FAAssertProcess_Set;
														End if;

                                                        #### Insert in Process Table

                                                        	set @lj_Impair_Data = '';
															set @lj_Impair_Data = concat(
																	'{
																		"Asset_Detail_Gids":"',@AssetDetails_Gid,'",
																		"Impair_Date":"',@Impair_Date,'",
                                                                        "ImpairAsset_Reason":"',@Impair_Remark,'"
																		}'
																	);

                                                        #select @lj_CPDate_Data;

                                                        call sp_FA_Impair_Asset_Set('INSERT', 'IMPAIR_ASSET_MAKER','TRAN',
																@lj_Impair_Data,lj_Classification,ls_Createby,@Message);
																select @Message into @Out_Msg_Impair;

                                                                    if @Out_Msg_Impair <> 'SUCCESS' then
																			set Message = concat('FAIL - ',@Out_Msg_Impair);
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                    End if;


                                ### Use It If needed
										if @AssetDetails_Gid <> 0 then
												if AssetDetails_Gid <> '' then
														set AssetDetails_Gid = concat(AssetDetails_Gid,',',@AssetDetails_Gid);
												else
														set AssetDetails_Gid = @AssetDetails_Gid;
												end if;
										end if;

									set i = i+1;
								End while;

                            ##### Update The Main Table.
																	set @lj_Impair_Data = '';
                                                                    set @lj_Impair_Data =
                                                                    concat('{
                                                                    "Asset_Detail_Gids":"',AssetDetails_Gid,'",
                                                                    "RequestFor":"IMPAIRMENT"
                                                                    }');

																	call sp_FAAsset_Set('UPDATE', 'ASSET_CHECKER',
																	'REQUEST_FOR',
                                                                    @lj_Impair_Data,'{}',lj_Classification,ls_Createby,@Message);
                                                                    set @Out_Msg_WriteOff = '';
																	select @Message   into @Out_Msg_Impair;

                                                                    if @Out_Msg_Impair <> 'SUCCESS' then
																			set Message = Concat('FAIL',@Out_Msg_Impair);
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                    End if;



              End if;

   elseif ls_Type = 'ASSET_TRANSFER' and ls_Sub_Type = 'MAKER' then

              if ls_Action = 'UPDATE' then
				   #### To Write Off - Check The child Gid too.
                                 #### Get The Value by loop in a Variable
                                 select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].AssetDetails_TransferTo_Gid'))) into @AssetDetails_TransferTo_Gid;
                                 select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].AssetDetails_Transfer_Date'))) into @AssetDetails_Transfer_Date;
                                 select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].AssetDetails_Location_Gid'))) into @AssetDetails_Location_Gid;
                                 select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].BS_NO'))) into @TFR_BS_NO;
                                 select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].CC_NO'))) into @TFR_CC_NO;
                                /* select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].Asset_Gid'))) into @Asset_TFR_Fn_Gids;


										set @Fn_Json_Data = '';
										set @Fn_Json_Data = concat('{"ASSET":
																			 {"Asset_Gid":',@Asset_TFR_Fn_Gids,'}}');

									set @Fn_Test= fn_FA_Data('ASSET_CLUB_CHECK',0,0,@Entity_Gid,@Fn_Json_Data);

									if @Fn_Test<>'SUCCESS' then
											set Message = 'Parent Is Miss Matched';
											leave sp_FAAssertProcess_Set;
									End if;*/


                                 if @AssetDetails_TransferTo_Gid is null or @AssetDetails_TransferTo_Gid = 0 then
									set Message = 'Asset Transfer To Is Needed.';
                                    leave sp_FAAssertProcess_Set;
                                 End if;

                                 if @AssetDetails_Transfer_Date is null or @AssetDetails_Transfer_Date = '' then
									set Message = 'Asset Transfer Date Is Needed.';
                                    leave sp_FAAssertProcess_Set;
                                 End if;

                                if @TFR_BS_NO is null or @TFR_BS_NO = '' THEN
                                  set Message = 'Asset Transfer BS No Is Needed.';
                                  leave sp_FAAssertProcess_Set;
                                End if;

                                if @TFR_CC_NO is null or @TFR_CC_NO = '' THEN
                                  set Message  = 'Asset CC No Is Needed.';
                                  leave sp_FAAssertProcess_Set;
                                End if;

                        select JSON_LENGTH(lj_Details, CONCAT('$.ASSET[0].Asset_Gid')) into @Asset_Gid_Count;

									if @Asset_Gid_Count is null or @Asset_Gid_Count = 0 or @Asset_Gid_Count = '' then
											set Message = 'Asset Detail Gid Is Needed.';
											leave sp_FAAssertProcess_Set;
									End if;
                                 select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,'$.Remark')) into @Transfer_Remark;

                              if @Transfer_Remark is  null and @Transfer_Remark = '' then
								set @Transfer_Remark = '';
                              End if;

                        set i = 0 ;
								While i <= @Asset_Gid_Count - 1 DO

										select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].Asset_Gid[',i,']'))) into @AssetDetails_Gid;

														/*set @lj_Details_Data = '';
														set @lj_Details_Data = concat(
														'{"Asset_Detail_Gids":"',@AssetDetails_Gid,'",
														   "Status":"TRANSFER",
														   "Remark": "',@Transfer_Remark,'"
														}'
														);
														#select @AssetDetails_Gid,@Asset_CPDate_New,@CPDate_Remark;
														#select @lj_Details_Data;
														call sp_FAAssetTmp_Set('INSERT','ASSET_TMP','MAKER',
																				@lj_Details_Data,'{}',lj_Classification,ls_Createby,@Message);
														select @Message into @Out_Msg_Asset;

														 ### TO DO
														#select @Out_Msg_Asset;
														if @Out_Msg_Asset = 'SUCCESS' then
															set Message = 'SUCCESS';
														elseif @Out_Msg_Asset is null or @Out_Msg_Asset <> 'SUCCESS' then
															set Message = concat('FAIL -',@Out_Msg_Asset);
                                                            leave sp_FAAssertProcess_Set;
														End if;*/

                                                        #### Creation Of New Asset is Done in Process SP

                                                        #### Insert in Process Table



                                                        	set @lj_Transfer_Data = '';
															set @lj_Transfer_Data = concat(
																	'{	"AssetDetails_Location_Gid":"',@AssetDetails_Location_Gid,'",
                                                                        "Asset_TFR_BS":"',@TFR_BS_NO,'",
 																		"Asset_TFR_CC":"',@TFR_CC_NO,'",
																		"Asset_Detail_Gids":"',@AssetDetails_Gid,'",
                                                                        "AssetDetails_Transfer_Date":"',@AssetDetails_Transfer_Date,'",
																		"Asset_TFR_To":"',@AssetDetails_TransferTo_Gid,'",
                                                                        "Asset_TFR_Reason":"',@Transfer_Remark,'" ,
                                                                        "Asset_TFR_DATE":"',@AssetDetails_Transfer_Date,'"
																		}'
																	);

                                                        #select @lj_Transfer_Data;

                                                        call sp_FA_TFR_Asset_Set('INSERT', 'TFR_MAKER','TRAN',
																@lj_Transfer_Data,lj_Classification,ls_Createby,@Message);
																	select @Message into @Out_Msg_Transfer;

                                                                    #select @Out_Msg_Transfer;

                                                                    if @Out_Msg_Transfer <> 'SUCCESS' then
																			set Message = concat('FAIL - ',@Out_Msg_Transfer);
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
																	elseif @Out_Msg_Transfer = 'SUCCESS' then
																			set Message = 'SUCCESS';
																	End if;


                                ### Use It If needed
										if @AssetDetails_Gid <> 0 then
												if AssetDetails_Gid <> '' then
														set AssetDetails_Gid = concat(AssetDetails_Gid,',',@AssetDetails_Gid);
												else
														set AssetDetails_Gid = @AssetDetails_Gid;
												end if;
										end if;

									set i = i+1;
								End while;


                                ##### Update The Main Table.
																	set @lj_Transfer_Data = '';
                                                                    set @lj_Transfer_Data =
                                                                    concat('{
                                                                    "Asset_Detail_Gids":"',AssetDetails_Gid,'",
                                                                    "RequestFor":"TRANSFER"
                                                                    }');

                                                                   #select @lj_Transfer_Data;

																	call sp_FAAsset_Set('UPDATE', 'ASSET_CHECKER','REQUEST_FOR',
																						@lj_Transfer_Data,'{}',lj_Classification,ls_Createby,@Message);
                                                                    set @Out_Msg_Transfer = '';
																	select @Message   into @Out_Msg_Transfer;

                                                                    if @Out_Msg_Transfer <> 'SUCCESS' then
																			set Message = Concat('FAIL',@Out_Msg_Transfer);
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
																	elseif @Out_Msg_Transfer = 'SUCCESS' then
																			set Message = 'SUCCESS';
                                                                    End if;


              End if;

    elseif ls_Type = 'ASSET_CAT' and ls_Sub_Type = 'MAKER' then

              if ls_Action = 'UPDATE' then

                                 #### Get The Value by loop in a Variable
                                 select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].AssetDetails_NewCat'))) into @AssetDetails_NewCat;
                                 select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].AssetDetails_NewCat_Gid'))) into @AssetDetails_NewCat_Gid;

                                 if @AssetDetails_NewCat is null or @AssetDetails_NewCat = '' then
									set Message = 'Asset New Category  Is Needed.';
                                    leave sp_FAAssertProcess_Set;
                                 End if;

                                 if @AssetDetails_NewCat_Gid is null or @AssetDetails_NewCat_Gid = 0 then
									  set Message = 'Asset New Category Gid  Is Needed.';
                                    leave sp_FAAssertProcess_Set;
                                 End if;

                        select JSON_LENGTH(lj_Details, CONCAT('$.ASSET[0].Asset_Gid')) into @Asset_Gid_Count;

									if @Asset_Gid_Count is null or @Asset_Gid_Count = 0 or @Asset_Gid_Count = '' then
											set Message = 'Asset Detail Gid Is Needed.';
											leave sp_FAAssertProcess_Set;
									End if;


                                 select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,'$.Remark')) into @Cat_Remark;

                              if @Cat_Remark is  null and @Cat_Remark = '' then
								set @Cat_Remark = '';
                              End if;

                        set i = 0 ;
								While i <= @Asset_Gid_Count - 1 DO

										select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].Asset_Gid[',i,']'))) into @AssetDetails_Gid;

															  set @lj_Details_Data = '';
														set @lj_Details_Data = concat(
														'{"Asset_Detail_Gids":"',@AssetDetails_Gid,'",
														   "Status":"ASSETCAT",
                                                           "New_Cat_Gid":"',@AssetDetails_NewCat_Gid,'",
														   "Remark": "',@Cat_Remark,'"
														}'
														);
														#select @AssetDetails_Gid,@Asset_CPDate_New,@CPDate_Remark;
														#select @lj_Details_Data;
														call sp_FAAssetTmp_Set('INSERT','ASSET_TMP','MAKER',@lj_Details_Data,'{}',lj_Classification,ls_Createby,@Message);
														select @Message into @Out_Msg_Asset;


													### TO DO
														#select @Out_Msg_Asset;
														if @Out_Msg_Asset = 'SUCCESS' then
															set Message = 'SUCCESS';
														elseif @Out_Msg_Asset is null or @Out_Msg_Asset <> 'SUCCESS' then
															set Message = concat('FAIL -',@Out_Msg_Asset);
														    rollback;
                                                            leave sp_FAAssertProcess_Set;
														End if;

                                                        #### Insert in Process Table
                                                        #### Get The Old Category
                                                        set @Asset_Cat = '';
                                                        Select b.assetcat_subcatname into @Asset_Cat from fa_trn_tassetdetails as a
														inner join fa_mst_tassetcat as b on b.assetcat_gid = a.assetdetails_assetcatgid
														where a.assetdetails_gid = @AssetDetails_Gid  and a.assetdetails_isactive = 'Y' and a.assetdetails_isremoved = 'N'
														and b.assetcat_isactive = 'Y' and b.assetcat_isremoved = 'N'  ;

                                                        set @AssetDetails_OldCat = @Asset_Cat;

                                                        	set @lj_Cat_Data = '';
																	set @lj_Cat_Data = concat(
																	'{
																		"Asset_Detail_Gids":"',@AssetDetails_Gid,'",
																		"CatChange_Cat":"',@AssetDetails_NewCat,'",
                                                                        "CatChange_OldCat":"',@AssetDetails_OldCat,'",
                                                                        "CatChange_Reason":"',@Cat_Remark,'"
																		}'
																	);

                                                        #select @lj_CPDate_Data;

                                                        call sp_FA_CatChange_Set('INSERT', 'CAT_CHANGE_MAKER','TRAN',
																@lj_Cat_Data,lj_Classification,ls_Createby,@Message);
																	select @Message into @Out_Msg_Cat;

                                                                    if @Out_Msg_Cat <> 'SUCCESS' then
																			set Message = concat('FAIL - ',@Out_Msg_Cat);
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                    ELSEIF @Out_Msg_Cat = 'SUCCESS' THEN
                                                                       set Message = 'SUCCESS';

                                                                    End if;


                                ### Use It If needed
										if @AssetDetails_Gid <> 0 then
												if AssetDetails_Gid <> '' then
														set AssetDetails_Gid = concat(AssetDetails_Gid,',',@AssetDetails_Gid);
												else
														set AssetDetails_Gid = @AssetDetails_Gid;
												end if;
										end if;

									set i = i+1;
								End while;


                                ##### Update The Main Table.
																	set @lj_Cat_Data = '';
                                                                    set @lj_Cat_Data =
                                                                    concat('{
                                                                    "Asset_Detail_Gids":"',AssetDetails_Gid,'",
                                                                    "RequestFor":"ASSETCAT"
                                                                    }');

                                                                 #   select @lj_CP_Data;

																	call sp_FAAsset_Set('UPDATE', 'ASSET_CHECKER',
																	'REQUEST_FOR',
                                                                    @lj_Cat_Data,'{}',lj_Classification,ls_Createby,@Message);
                                                                    set @Out_Msg_Cat = '';
																	select @Message   into @Out_Msg_Cat;

                                                                    if @Out_Msg_CPDate <> 'SUCCESS' then
																			set Message = Concat('FAIL In Asset Main Update',@Out_Msg_Cat);
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                    ELSEIF @Out_Msg_CPDate = 'SUCCESS' THEN
                                                                       set Message = 'SUCCESS';
                                                                    End if;
                                #### Update in Tmp Table Cat
                                                            set @lj_Tmp_UpdateData = '';
                                                            set @lj_Tmp_UpdateData = concat(
                                                            '{
                                                            "Asset_Tran_Gids":"',AssetDetails_Gid,'",
                                                            "AssetDetails_Cat_Gid":"',@AssetDetails_NewCat_Gid,'"
                                                            }'
                                                            );

                                                          # select @lj_Tmp_UpdateData;

                                                         call sp_FAAssetTmp_Set('UPDATE', 'ASSET_TMP', 'TMP',
																  @lj_Tmp_UpdateData,'{}',
																 lj_Classification,ls_Createby,@Message);
																select @Message into @Out_Msg_CatTmp ;

																	if @Out_Msg_CatTmp <> 'SUCCESS' then
																			set Message = concat('FAIL In Asset Temp Update - ',@Out_Msg_CatTmp);
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                    ELSEIF @Out_Msg_CatTmp = 'SUCCESS' THEN
                                                                       set Message = 'SUCCESS';
                                                                    End if;




              End if;

    elseif ls_Type = 'ASSET_MERGE' and ls_Sub_Type = 'MAKER' then

              if ls_Action = 'UPDATE' then
				   #### To Write Off - Check The child Gid too.
                                 #### Get The Value by loop in a Variable
                                 select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].AssetDetails_Value'))) into @Merge_Value;
                                 select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].AssetDetails_Merge_Date'))) into @AssetDetails_Merge_Date;
                                 /*select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].Asset_Gid'))) into @Asset_Merge_Fn_Gids;


										set @Fn_Json_Data = '';
										set @Fn_Json_Data = concat('{"ASSET":
																			 {"Asset_Gid":',@Asset_Merge_Fn_Gids,'}}');

									set @Fn_Test= fn_FA_Data('ASSET_CLUB_CHECK',0,0,@Entity_Gid,@Fn_Json_Data);

									if @Fn_Test<>'SUCCESS' then
											set Message = 'Parent Is Miss Matched';
											leave sp_FAAssertProcess_Set;
									End if;*/

                                 if @Merge_Value is null or @Merge_Value = 0 then
									set Message = 'Asset Merge Value Is Needed.';
                                    leave sp_FAAssertProcess_Set;
                                 End if;

                                 if @AssetDetails_Merge_Date is null or @AssetDetails_Merge_Date = '' then
									set Message = 'Asset Merge Date Is Needed.';
                                    leave sp_FAAssertProcess_Set;
                                 End if;

                        select JSON_LENGTH(lj_Details, CONCAT('$.ASSET[0].Asset_Gid')) into @Asset_Gid_Count;

									if @Asset_Gid_Count is null or @Asset_Gid_Count = 0 or @Asset_Gid_Count = '' then
											set Message = 'Asset Detail Gid Is Needed.';
											leave sp_FAAssertProcess_Set;
									End if;
                                 select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,'$.Remark')) into @Merge_Remark;

                              if @Merge_Remark is  null and @Merge_Remark = '' then
								set @Merge_Remark = '';
                              End if;

                        set i = 0 ;
								While i <= @Asset_Gid_Count - 1 DO

										select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].Asset_Gid[',i,']'))) into @AssetDetails_Gid;
                                ### Use It If needed
										if @AssetDetails_Gid <> 0 then
												if AssetDetails_Gid <> '' then
														set AssetDetails_Gid = concat(AssetDetails_Gid,',',@AssetDetails_Gid);
												else
														set AssetDetails_Gid = @AssetDetails_Gid;
												end if;
										end if;

									set i = i+1;
								End while;


												set @lj_Details_Data = '';
														set @lj_Details_Data = concat(
														'{"Asset_Detail_Gids":"',AssetDetails_Gid,'",
														   "Status":"MERGE",
														   "Remark": "',@Merge_Remark,'"
														}'
														);
														#select @AssetDetails_Gid,@Asset_CPDate_New,@CPDate_Remark;
														#select @lj_Details_Data;
														call sp_FAAssetTmp_Set('INSERT','ASSET_TMP','MAKER',@lj_Details_Data,
																			   '{}',lj_Classification,ls_Createby,@Message);
														select @Message into @Out_Msg_Asset;

														### TO DO
														#select @Out_Msg_Asset;
														if @Out_Msg_Asset = 'SUCCESS' then
															set Message = 'SUCCESS';
														elseif @Out_Msg_Asset is null or @Out_Msg_Asset <> 'SUCCESS' then
															set Message = concat('FAIL -',@Out_Msg_Asset);
														    rollback;
                                                            leave sp_FAAssertProcess_Set;
														End if;

                                                        #### Creation Of New Asset is Done in Process SP
                                                        #### Insert in Process Table

                                                        set @Asset_MaxGid_ps = 0 ;


                                                        	set @lj_Merge_Data = '';
																	set @lj_Merge_Data = concat(
																	'{
                                                                       "Asset_Gid":"',@AssetDetails_Gid,'",
																		"Asset_Detail_Gids":"',AssetDetails_Gid,'",
                                                                        "Merge_Value":"',@Merge_Value,'",
																		"Merge_Date":"',@AssetDetails_Merge_Date,'",
                                                                        "Merge_Reason":"',@Merge_Remark,'" ,
                                                                        "Trn_Ref_Name":"FA_MERGE",
                                                                        "Trn_To_Type":"I",
                                                                        "Trn_Role_Name":"MAKER"
																		}'
																	);

													#select @lj_Merge_Data,@Asset_MaxGid_ps,@Asset_MaxGid_pss,AssetDetails_Gid,@Merge_Value,@AssetDetails_Merge_Date,@Merge_Remark;
                                                      #select   @lj_Merge_Data,lj_Classification,ls_Createby;
                                                        call sp_FAMerge_Set('INSERT', 'ASSET_MERGE','TRAN',
																@lj_Merge_Data,lj_Classification,ls_Createby,@Message);
																	select @Message into @Out_Msg_Merge;
                                                                 # select @Out_Msg_Merge;
                                                                    if @Out_Msg_Merge <> 'SUCCESS'  then
																			set Message = concat('FAIL - ',@Out_Msg_Merge);
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                     elseif @Out_Msg_Merge is null then
                                                                            set Message = 'Error On Merge Save.';
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                      else
                                                                         set Message = 'SUCCESS';
                                                                    End if;


                                ##### Update The Main Table.
																	set @lj_Transfer_Data = '';
                                                                    set @lj_Transfer_Data =
                                                                    concat('{
                                                                    "Asset_Detail_Gids":"',AssetDetails_Gid,'",
                                                                    "RequestFor":"MERGE"
                                                                             }');

                                                                 #   select @lj_CP_Data;

																	call sp_FAAsset_Set('UPDATE', 'ASSET_CHECKER',
																	'REQUEST_FOR',
                                                                    @lj_Transfer_Data,'{}',lj_Classification,ls_Createby,@Message);
                                                                    set @Out_Msg_Transfer = '';
																	select @Message   into @Out_Msg_Transfer;

                                                                    if @Out_Msg_Transfer <> 'SUCCESS' and @Out_Msg_Transfer is not null then
																			set Message = Concat('FAIL',@Out_Msg_Transfer);
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                     elseif @Out_Msg_Transfer = 'SUCCESS' then
                                                                          set Message = 'SUCCESS';
																	elseif @Out_Msg_Transfer is null then
                                                                        set Message = 'Error On Asset Table Update.';
                                                                        rollback;
                                                                        leave sp_FAAssertProcess_Set;
                                                                    End if;




              End if;

  elseif ls_Type = 'ASSET_SPLIT' and ls_Sub_Type = 'MAKER' then

              if ls_Action = 'UPDATE' then
				   #### To SPLIT - Check The child Gid too.
                                 #### Get The Value by loop in a Variable
                                 select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].Asset_Id'))) into @Asset_Id; ### A is Split to B and C :: A id here
                                 select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].AssetSplit_Date'))) into @Asset_Split_Date;
                                 select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].All_Value'))) into @All_Value;
                                 select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].Asset_Gid'))) into @Asset_Gid;
								 /*select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].Asset_Gid'))) into @Asset_Split_Fn_Gids;


										set @Fn_Json_Data = '';
										set @Fn_Json_Data = concat('{"ASSET":
																			 {"Asset_Gid":',@Asset_Split_Fn_Gids,'}}');

									set @Fn_Test= fn_FA_Data('ASSET_CLUB_CHECK',0,0,@Entity_Gid,@Fn_Json_Data);

									if @Fn_Test<>'SUCCESS' then
											set Message = 'Parent Is Miss Matched';
											leave sp_FAAssertProcess_Set;
									End if;*/

                                 set @Asset_Gid_Update = @Asset_Gid;

                                 if @Asset_Split_Date is null or @Asset_Split_Date = '' then
									set Message = 'Asset Split Date Is Needed.';
                                    leave sp_FAAssertProcess_Set;
                                 End if;

                                 if @All_Value is null or @All_Value = 0 then
									set Message = 'Asset Value Is Needed.';
                                    leave sp_FAAssertProcess_Set;
                                 End if;

							select JSON_LENGTH(lj_Details, CONCAT('$.SPLIT')) into @Asset_Split_Count;

									if @Asset_Split_Count is null or @Asset_Split_Count = 0 or @Asset_Split_Count = '' then
											set Message = 'Asset Split Details Is Needed.';
											leave sp_FAAssertProcess_Set;
									End if;
                                 select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,'$.Remark')) into @Split_Remark;

                              if @Split_Remark is  null and @Split_Remark = '' then
								set @Split_Remark = '';
                              End if;
                               #### Insert The Header in Split  Table First and Get Gid
                                    set @lj_SplitDetails = '';
                                    set @lj_SplitDetails = concat('{
                                    "Asset_Id":"',@Asset_Id,'",
                                    "Split_Date":"',@Asset_Split_Date,'",
                                    "Split_Reason":"',@Split_Remark,'",
                                    "Split_Value":"',@All_Value,'",
                                    "Trn_To_Type":"G",
                                    "Trn_Role_Name":"MAKER",
                                    "Trn_Remarks":"',@Split_Remark,'",
                                    "Trn_Ref_Name":"FA_SPLIT"


                                    }');

					call sp_FASplit_Set('INSERT','ASSET_SPLIT','HEADER',
                                        @lj_SplitDetails,lj_Classification,ls_Createby,
                                        @Last_Insert_id,@Message);

                                    select @Message into @Out_Msg_Split ;

                                    if @Out_Msg_Split = 'SUCCESS' then
										select @Last_Insert_id into @Last_Insert_SplitId;
                                     elseif @Out_Msg_Split is null then
                                         set Message = 'Error Occured On Splitting The Data.';
                                         rollback;
                                         leave sp_FAAssertProcess_Set;
                                       else
                                         set Message = concat('FAIL','-',@Out_Msg_Split);
                                         rollback;
                                         leave sp_FAAssertProcess_Set;
                                    End if;

                              ##### Temp Create a Asset a Original
                              set @lj_AssetOldData = '';
                              set @lj_AssetOldData = concat('{
                               "Asset_Id":"',@Asset_Id,'",
                               "Split_Value":"',@All_Value,'",
                               "Asset_Gid":"',@Asset_Gid,'",
                               "Asset_Split_Gid":"',@Last_Insert_SplitId,'"
                              }
                              ');

                               call sp_FASplit_Set('INSERT','ASSET_SPLIT','TEMP_OLD',@lj_AssetOldData,lj_Classification,ls_Createby,@faid,@Message);
                               select @Message into @Out_Msg_AssetOld;

                               if @Out_Msg_AssetOld <> 'SUCCESS' then
									set Message = concat('FAIL','-',@Out_Msg_AssetOld);
                                    rollback;
                                    leave sp_FAAssertProcess_Set;
                                elseif @Out_Msg_AssetOld is null then
                                    set Message = 'FAIL';
                                    rollback;
                                    leave sp_FAAssertProcess_Set;
                               End if;


                        set i = 0 ;
								While i <= @Asset_Split_Count - 1 DO

										select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.SPLIT[',i,'].Asset_New_Id'))) into @Asset_New_Id;
										select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.SPLIT[',i,'].Asset_Value'))) into @Asset_Value;


									      select ifnull(max(cast(assetdetails_id as decimal)),0)+1 into @New_Asset_TmpId from fa_tmp_tassetdetails where assetdetails_id not like '%-%';
							              select ifnull(max(cast(assetdetails_id as decimal)),0)+1 into @New_Asset_TrnId from fa_trn_tassetdetails where assetdetails_id not like '%-%';

							                     if @New_Asset_TmpId > @New_Asset_TrnId THEN
							                       set @New_Asset_Id = @New_Asset_TmpId;
							                     ELSEIF @New_Asset_TmpId <= @New_Asset_TrnId THEN
							                       set @New_Asset_Id = @New_Asset_TrnId;
							                     ELSE
							                       set Message = 'Error On Asset New Id.';
							                       rollback;
							                       leave sp_FAAssertProcess_Set;
							                     End if;

									##### Temp Create a Asset New
											  set @lj_AssetNewData = '';
											  set @lj_AssetNewData = concat('{
											   "Asset_Id":"',@New_Asset_Id,'",
											   "Split_Value":"',@Asset_Value,'",
											   "Asset_Gid":"',@Asset_Gid,'",
                                               "Asset_Split_Gid":"',@Last_Insert_SplitId,'"
											  }
											  ');


											   call sp_FASplit_Set('INSERT','ASSET_SPLIT','TEMP_NEW',@lj_AssetNewData,lj_Classification,ls_Createby,@faid,@Message);
											   select @Message into @Out_Msg_AssetNew;

											   if @Out_Msg_AssetNew <> 'SUCCESS' then
													set Message = concat('FAIL','-',@Out_Msg_AssetNew);
													rollback;
													leave sp_FAAssertProcess_Set;
												elseif @Out_Msg_AssetNew is null then
													set Message = 'FAIL';
													rollback;
													leave sp_FAAssertProcess_Set;
											   End if;

                                              #### Insert in Split Detail Table
                                              set @lj_AssetSplitDetail = '';
											  set @lj_AssetSplitDetail = concat('{
                                              "Asset_Header_Gid":"',@Last_Insert_SplitId,'",
											   "Asset_New_Id":"',@New_Asset_Id,'",
											   "Split_Value":"',@Asset_Value,'"
											  }
											  ');

											   call sp_FASplit_Set('INSERT','ASSET_SPLIT','DETAIL',@lj_AssetSplitDetail,lj_Classification,ls_Createby,@faid,@Message);
											   select @Message into @Out_Msg_AssetDetail;
											   #select @Out_Msg_AssetDetail;
											   if @Out_Msg_AssetDetail <> 'SUCCESS' then
													set Message = concat('FAIL','-',@Out_Msg_AssetDetail);
													rollback;
													leave sp_FAAssertProcess_Set;
												elseif @Out_Msg_AssetDetail is null then
													set Message = 'FAIL';
													rollback;
													leave sp_FAAssertProcess_Set;
											   End if;

									set i = i+1;

								End while;
                                ##### Update The Main Table.
																	set @lj_Split_Data = '';
                                                                    set @lj_Split_Data =
                                                                    concat('{
                                                                    "Asset_Detail_Gids":"',@Asset_Gid_Update,'",
                                                                    "RequestFor":"SPLIT"
                                                                    }');

                                                                    #select @lj_Split_Data;
                                                                 #   select @lj_CP_Data;
																	call sp_FAAsset_Set('UPDATE', 'ASSET_CHECKER',
																	'REQUEST_FOR',
                                                                    @lj_Split_Data,'{}',lj_Classification,ls_Createby,@Message);
                                                                    set @Out_Msg_Split = '';
																	select @Message   into @Out_Msg_Split;
                                                              #      select @Out_Msg_Split;
                                                                    if @Out_Msg_Split <> 'SUCCESS' and @Out_Msg_Split is not null then
																			set Message = Concat('FAIL',@Out_Msg_Split);
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                     elseif @Out_Msg_Split = 'SUCCESS' then
                                                                          set Message = 'SUCCESS';
																	elseif @Out_Msg_Split is null then
                                                                        set Message = 'Error On Asset Table Update.';
                                                                        rollback;
                                                                        leave sp_FAAssertProcess_Set;
                                                                    End if;

              End if;

elseif ls_Type = 'ASSET_VALUE' and ls_Sub_Type = 'MAKER' then

              if ls_Action = 'UPDATE' then
				   #### To ASSET_VALUE - Check The child Gid too.
                                 #### Get The Value by loop in a Variable
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].Asset_Value_Date'))) into @Asset_Value_Date;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].Asset_Value[0]'))) into @Asset_Value_Count;
				#select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].Asset_Value_Reason'))) into @Asset_Value_Reason;


								 if @Asset_Value_Date is null or @Asset_Value_Date = '' then
									set Message = 'Asset Value Date  Is Needed.';
                                    leave sp_FAAssertProcess_Set;
                                 End if;

                                 if @Asset_Value_Count is null or @Asset_Value_Count = '' then
									set Message = 'Asset Value Reason Is Needed.';
                                    leave sp_FAAssertProcess_Set;
                                 End if;



                        select JSON_LENGTH(lj_Details, CONCAT('$.ASSET[0].Asset_Gid')) into @Asset_Gid_Count;

									if @Asset_Gid_Count is null or @Asset_Gid_Count = 0 or @Asset_Gid_Count = '' then
											set Message = 'Asset Detail Gid Is Needed.';
											leave sp_FAAssertProcess_Set;
									End if;

                                 select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,'$.Remark')) into @Value_Remark;

                              if @Merge_Remark is  null and @Merge_Remark = '' then
								set @Merge_Remark = '';
                              End if;

                        set i = 0 ;
								While i <= @Asset_Gid_Count - 1 DO

                                        set @AssetDetails_Gid='';
                                        set @Asset_Value='';
										select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].Asset_Gid[',i,']'))) into @AssetDetails_Gid;
										select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].Asset_Value[',i,']'))) into @Asset_Value;

                                					set @lj_Details_Data = '';
														set @lj_Details_Data = concat(
														'{"Asset_Detail_Gids":"',@AssetDetails_Gid,'",
														  "Status":"VALUE REDUCTION",
														  "Remark": "',@Value_Remark,'"
														  }'
																					 );



														set @query_val = '';
   										                set @asset_cp_date_value = '';
													    set @query_val = concat('select assetdetails_capdate into @asset_cp_date_value
														from fa_trn_tassetdetails
														where assetdetails_gid = ',@AssetDetails_Gid,' ');


																	PREPARE stmt FROM @query_val;
																	EXECUTE stmt;

													    if date_format(@asset_cp_date_value,'%Y-%m-%d') > DATE_FORMAT(@Asset_Value_Date,'%Y-%m-%d') THEN
													          set Message = 'Asset Value Change Date Is Greater Than CP Date.';
													          rollback;
													          leave sp_FAAssertProcess_Set;
													    elseif @asset_cp_date_value is  null and @asset_cp_date_value = ''  then
													       set Message = 'Error In Asset CP Date.';
													       rollback;
													       leave sp_FAAssertProcess_Set;
													    End if;

														#### remove flag ++ .. Not Needed

														#select @AssetDetails_Gid,@Asset_CPDate_New,@CPDate_Remark;
														#select @lj_Details_Data;
														call sp_FAAssetTmp_Set('INSERT','ASSET_TMP','MAKER',
																				@lj_Details_Data,'{}',lj_Classification,
															 ls_Createby,@Message);
														select @Message into @Out_Msg_Asset;

														 ### TO DO
														#select @Out_Msg_Asset;
														if @Out_Msg_Asset = 'SUCCESS' then
															set Message = 'SUCCESS';
														elseif @Out_Msg_Asset is null or @Out_Msg_Asset <> 'SUCCESS' then
															set Message = concat('FAIL -',@Out_Msg_Asset);
                                                            leave sp_FAAssertProcess_Set;
														End if;

                                                        #### Creation Of New Asset is Done in Process SP
                                                        #### Insert in Process Table

                                                        set @Asset_MaxGid_ps = 0 ;


                                                        	set @lj_Value_Data = '';
																	set @lj_Value_Data = concat(
																	'{
                                                                        "Asset_Gid":"',@AssetDetails_Gid,'",
																		"Asset_Detail_Gids":"',@AssetDetails_Gid,'",
                                                                        "Asset_Value":"',@Asset_Value,'",
                                                                        "Asset_Value_Reason":"',@Value_Remark,'",
                                                                        "Asset_Value_Date":"',@Asset_Value_Date,'",
                                                                        "Trn_Ref_Name":"FA_VALUE",
                                                                        "Trn_To_Type":"G",
                                                                        "Trn_Role_Name":"MAKER",
                                                                        "Trn_Remarks":"',@Value_Remark,'"
																		}'
																	);
                                                        #select @lj_Value_Data;
											#select @lj_Merge_Data,@Asset_MaxGid_ps,@Asset_MaxGid_pss,AssetDetails_Gid,@Merge_Value,@AssetDetails_Merge_Date,@Merge_Remark;

                                                        call sp_FA_Value_Set('INSERT', 'VALUE_MAKER','TRAN',
																@lj_Value_Data,lj_Classification,ls_Createby,@Message);
																	set @Out_Msg_Value='';
																	select @Message into @Out_Msg_Value;
                                                      #              select @Out_Msg_Value;
                                                                    if @Out_Msg_Value <> 'SUCCESS'  then
																			set Message = concat('FAIL - ',@Out_Msg_Value);
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                     elseif @Out_Msg_Value is null then
                                                                            set Message = 'Error On Value Save.';
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                      else
                                                                         set Message = 'SUCCESS';
                                                                    End if;


                                ##### Update The Main Table.
																	set @lj_Transfer_Data = '';
                                                                    set @lj_Transfer_Data =
                                                                    concat('{
                                                                    "Asset_Detail_Gids":"',@AssetDetails_Gid,'",
                                                                    "RequestFor":"VALUE REDUCTION",
                                                                    "Asset_Status":"ACTIVE"
                                                                    }');

                                                                 #   select @lj_CP_Data;

																	call sp_FAAsset_Set('UPDATE', 'ASSET_CHECKER',
																	'REQUEST_FOR',
                                                                    @lj_Transfer_Data,'{}',lj_Classification,ls_Createby,@Message);
                                                                    set @Out_Msg_Transfer = '';
																	select @Message   into @Out_Msg_Transfer;
                                                                #select @Out_Msg_Transfer;
                                                                    if @Out_Msg_Transfer <> 'SUCCESS' and @Out_Msg_Transfer is not null then
																			set Message = Concat('FAIL',@Out_Msg_Transfer);
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                     elseif @Out_Msg_Transfer = 'SUCCESS' then
                                                                          set Message = 'SUCCESS';
																	elseif @Out_Msg_Transfer is null then
                                                                        set Message = 'Error On Asset Table Update.';
                                                                        rollback;
                                                                        leave sp_FAAssertProcess_Set;
                                                                    End if;



                               set i = i+1;
                                		End while;

              End if;

  elseif ls_Type = 'ASSET_CLUB' and ls_Sub_Type = 'TMP' then
           if ls_Action = 'UPDATE' then
				   #### To Club the Asset - Parent and Child.
                                 #### Get The Value by loop in a Variable
						select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].AssetDetails_Parent_Gid'))) into @AssetDetails_Parent_Gid;

									if @AssetDetails_Parent_Gid is null or @AssetDetails_Parent_Gid = 0 or @AssetDetails_Parent_Gid = '' then
											set Message = 'Asset Parent Gid Is Needed.';
											leave sp_FAAssertProcess_Set;
									End if;

								select JSON_LENGTH(lj_Details, CONCAT('$.ASSET[0].AssetDetails_List_Gid')) into @AssetDetails_List_Gid_Count;

                        set @AssetDetails_Gid = 0;
                        set i = 0 ;
								While i <= @AssetDetails_List_Gid_Count - 1 DO

										select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].AssetDetails_List_Gid[',i,']'))) into @AssetDetails_Gid;

										if @AssetDetails_Gid <> 0 then
												if AssetDetails_Gid <> '' then
														set AssetDetails_Gid = concat(AssetDetails_Gid,',',@AssetDetails_Gid);
												else
														set AssetDetails_Gid = @AssetDetails_Gid;
												end if;
										end if;

									set i = i+1;
								End while;

                                set @lj_Details_Data = '';
                                set @lj_Details_Data = concat(
                                '{"AssetDetails_Parent_Gid":"',@AssetDetails_Parent_Gid,'",
                                   "AssetDetails_Gid":"',AssetDetails_Gid,'",
                                   "Request_For":"CLUB",
                                   "Request_Status":"SUBMITTED",
                                   "Status":"CLUB"
								 }'
                                );
                                #select AssetDetails_Gid,@ls_Remark;
                                #select @lj_Details_Data;
                                call sp_FAAssetTmp_Set('UPDATE','ASSET_PARENT','MAKER',@lj_Details_Data,'{}',lj_Classification,ls_Createby,@Message);
                                select @Message into @Out_Msg_Asset;
                                #select @Out_Msg_Asset;
                                 ### TO DO
                                #select @Out_Msg_Asset;
                                if @Out_Msg_Asset = 'SUCCESS' then
									set Message = 'SUCCESS';
                                elseif @Out_Msg_Asset is null or @Out_Msg_Asset <> 'SUCCESS' then
                                    set Message = 'FAIL';
                                End if;


						set @lj_Club_Data = '';
						set @lj_Club_Data = concat('{
														"Asset_Detail_Gids":"',AssetDetails_Gid,'",
														"RequestFor":"CLUB"
													 }');

							   #select @lj_Club_Data;

							call sp_FAAsset_Set('UPDATE', 'ASSET_CHECKER','REQUEST_FOR',
												@lj_Club_Data,'{}',lj_Classification,
                                                ls_Createby,@Message);
											set @Out_Msg_Club = '';
											select @Message   into @Out_Msg_Club;

									if @Out_Msg_Club <> 'SUCCESS' then
										set Message = Concat('FAIL',@Out_Msg_Club);
										rollback;
									    leave sp_FAAssertProcess_Set;
									End if;


              End if;

 elseif ls_Type = 'ASSET_SALE' and ls_Sub_Type = 'MAKER' then
			### sale The asset - Group By Rate too
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].Customer_Gid'))) into @Sale_Customer_Gid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].Branch_Gid'))) into @Sale_Branch_Gid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].Sale_Date'))) into @Sale_Date;

			select JSON_UNQUOTE(JSON_EXTRACT(lj_Status, '$.Status')) into @ls_Status;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Status, '$.Remark')) into @ls_Remarks;

            if @Sale_Customer_Gid is null or @Sale_Customer_Gid = 0 then
					set Message = 'Sale Customer Gid Is Needed.';
                    leave sp_FAAssertProcess_Set;
            End if;

            if @Sale_Branch_Gid is null or @Sale_Branch_Gid = 0 then
				set Message = 'Asset Branch Is Needed.';
                leave sp_FAAssertProcess_Set;
            End if;

            if @Sale_Date is null or @Sale_Date = '' then
				set Message = 'Sale Date Is Needed.';
                leave sp_FAAssertProcess_Set;
            End if;

            if @ls_Status is null or @ls_Status = '' THEN
            	set Message = 'Asset Sale Status Is Needed.';
                leave sp_FAAssertProcess_Set;
            End if;

            if @ls_Remarks is null or @ls_Remarks = '' THEN
               set Message = 'Asset Sale Remarks Is Needed.';
               leave sp_FAAssertProcess_Set;
            End if;

            set @lj_SaleData = '';
            set @lj_SaleData = concat('{
            "Customer_Gid":"',@Sale_Customer_Gid,'",
            "Branch_Gid":"',@Sale_Branch_Gid,'",
            "Sale_Date":"',@Sale_Date,'",
            "Status":"',@ls_Status,'",
            "Remarks":"',@ls_Remarks,'"
            }');
           ### No Duplicate Need to Catch
           call sp_FASale_Set('INSERT', 'SALE_MAKER', 'SALE_HEADER', @lj_SaleData, lj_Classification, ls_Createby,@Last_id,@Message);
            select @Last_id into @Out_Msg_LastID;
            select @Message into @Out_Msg_Sale;
#           select @Out_Msg_Sale;

           if @Out_Msg_Sale <> 'SUCCESS' THEN
           		set Message = 'Error On Asset Sale Save.';
           	    ROLLBACK;
           	    leave  sp_FAAssertProcess_Set;
           End if;

           if @Out_Msg_LastID is null or @Out_Msg_LastID = 0 THEN
              set Message = 'Error On Asset Detail Save.';
             rollback;
              leave sp_FAAssertProcess_Set;
           End IF;

          select JSON_LENGTH(lj_Change,'$')into @li_Change_Count;
           if @li_Change_Count is null or @li_Change_Count = 0 THEN
           		set Message = 'Sales Product Is Needed.';
           	      rollback;
           End if;



          set i = 0;
         While i <= @li_Change_Count -1 Do

     		 select JSON_UNQUOTE(JSON_EXTRACT(lj_Change, CONCAT('$[',i,'].Product_Gid'))) into @Product_Gid; ### Not needed.
        	 select JSON_UNQUOTE(JSON_EXTRACT(lj_Change, CONCAT('$[',i,'].Product_Qty'))) into @Product_Qty;
       		 select JSON_UNQUOTE(JSON_EXTRACT(lj_Change, CONCAT('$[',i,'].Sale_Rate'))) into @Sale_Rate;
       		 select JSON_UNQUOTE(JSON_EXTRACT(lj_Change, CONCAT('$[',i,'].HSN_Code'))) into @HSN_Code;### Added By Jan 23
       		 select JSON_UNQUOTE(JSON_EXTRACT(lj_Change, CONCAT('$[',i,'].SGST_Rate'))) into @SGST_Rate;
       		 select JSON_UNQUOTE(JSON_EXTRACT(lj_Change, CONCAT('$[',i,'].CGST_Rate'))) into @CGST_Rate;
       		 select JSON_UNQUOTE(JSON_EXTRACT(lj_Change, CONCAT('$[',i,'].IGST_Rate'))) into @IGST_Rate;


       	 		select JSON_LENGTH(lj_Change, CONCAT('$[',i,'].Asset_Gid')) into @Asset_Gid_Count;


              #  select @Asset_Gid_Count,@Sale_Rate,@li_Change_Count;
					if @Asset_Gid_Count is null or @Asset_Gid_Count = 0 or @Asset_Gid_Count = '' then
							set Message = 'Asset Detail Gid Is Needed.';
						       ROLLBACK;
							leave sp_FAAssertProcess_Set;
					End if;

				if @Product_Qty is null or @Product_Qty = 0 then
					    set Message = 'Product Quantity Is Needed.';
						 ROLLBACK;
						leave sp_FAAssertProcess_Set;
				End if;

			    if @HSN_Code is null or @HSN_Code = '' THEN
			      set Message  = 'HSN Code Is Needed.';
			      ROLLBACK;
			      leave sp_FAAssertProcess_Set;
			    End if;

			    if @SGST_Rate is null or @SGST_Rate = '' THEN
			      set Message  = 'SGST Rate Is Needed.';
			      ROLLBACK;
			      leave sp_FAAssertProcess_Set;
			    End if;

			    if @CGST_Rate is null or @CGST_Rate = '' THEN
			      set Message  = 'CGST Rate Is Needed.';
			      ROLLBACK;
			      leave sp_FAAssertProcess_Set;
			    End if;

			    if @IGST_Rate is null or @IGST_Rate = '' THEN
			      set Message  = 'IGST Rate Is Needed.';
			      ROLLBACK;
			      leave sp_FAAssertProcess_Set;
			    End if;

				### Loop The Data - Final Validations May be Used.
				set AssetDetails_Gid = '' ;
				set j = 0;
			   While j <= @Asset_Gid_Count -1 DO
			   	  	select JSON_UNQUOTE(JSON_EXTRACT(lj_Change, CONCAT('$[',i,'].Asset_Gid[',j,']'))) into @AssetDetails_Gid;

			   	  	if AssetDetails_Gid <> '' then
							set AssetDetails_Gid = concat(AssetDetails_Gid,',',@AssetDetails_Gid);
					else
   							set AssetDetails_Gid = @AssetDetails_Gid;
					end if;


			     set j = j+1;
			   End While;

               ### Duplicate Check

			  set @Asset_Gid_Duplicate = 0 ;
               set Query_Select = '';
               set Query_Select = concat('Select count(assetdetails_gid) into @Asset_Gid_Duplicate from fa_trn_tassetdetails as a
               where assetdetails_gid in (',@AssetDetails_Gid,')
               and assetdetails_requestfor = ''SALE'' and a.entity_gid = ''',@Entity_Gid,'''
               and a.assetdetails_isactive = ''Y'' and a.assetdetails_isremoved = ''N''
               ');

   	           set @selectquery = Query_Select;
             #select Query_Select;
				PREPARE stmt1 FROM @selectquery;
				EXECUTE stmt1;
				Select found_rows() into countRow;
				DEALLOCATE PREPARE stmt1;

              #select @Asset_Gid_Duplicate,@AssetDetails_Gid;


			    if @Asset_Gid_Duplicate > 0 THEN
			    	set Message = 'Already Some Of The Selected Asset Are In Sale Process';
			        rollback;
			        leave sp_FAAssertProcess_Set;
			    End if;

			  		### In temp Table Insert

							set @lj_Details_Data = '';
							set @lj_Details_Data = concat(
							'{"Asset_Detail_Gids":"',AssetDetails_Gid,'",
							  "Status":"SALE",
							  "Remark": "',@ls_Remarks,'"
							  }'
														 );
							#select @AssetDetails_Gid,@Asset_CPDate_New,@CPDate_Remark;
							#select @lj_Details_Data;
							call sp_FAAssetTmp_Set('INSERT','ASSET_TMP','MAKER',
													@lj_Details_Data,'{}',lj_Classification,
								 ls_Createby,@Message);
							select @Message into @Out_Msg_Asset;

							if @Out_Msg_Asset = 'SUCCESS' then
										set Message = 'SUCCESS';
							elseif @Out_Msg_Asset is null or @Out_Msg_Asset <> 'SUCCESS' then
								set Message = concat('FAIL -',@Out_Msg_Asset);
							    rollback;
                                leave sp_FAAssertProcess_Set;
							End if;


				#### Temp Insert Ends

						##### Update The Main Table.
								set @lj_Sale_Data = '';
                                set @lj_Sale_Data =
                                concat('{
                                "Asset_Detail_Gids":"',AssetDetails_Gid,'",
                                "RequestFor":"SALE",
                                "Asset_Status":"ACTIVE"
                                }');

                             #   select @lj_CP_Data;

								call sp_FAAsset_Set('UPDATE', 'ASSET_CHECKER',
								'REQUEST_FOR',
                                @lj_Sale_Data,'{}',lj_Classification,ls_Createby,@Message);
                                set @Out_Msg_Sale = '';
								select @Message   into @Out_Msg_Sale;
                            #select @Out_Msg_Transfer;
                                if @Out_Msg_Sale <> 'SUCCESS' and @Out_Msg_Sale is not null then
										set Message = Concat('FAIL',@Out_Msg_Sale);
                                        rollback;
                                        leave sp_FAAssertProcess_Set;
                                elseif @Out_Msg_Sale = 'SUCCESS' then
                                      set Message = 'SUCCESS';
								elseif @Out_Msg_Sale is null then
                                    set Message = 'Error On Asset Table Update.';
                                    rollback;
                                    leave sp_FAAssertProcess_Set;
                                End if;
                       #### Main Table Insert Ends


			  set @lj_SaleProductData = '';
			 set @lj_SaleProductData = concat('{
					"SaleHeader_Gid":"',@Out_Msg_LastID,'",
                    "Sale_Date":"',@Sale_Date,'",
                    "Sale_Status":"',@ls_Status,'",
                    "Sale_Reason":"',@ls_Remarks,'",
                     "Sale_Rate":"',@Sale_Rate,'",
                     "Assetdetail_Gids":"',@AssetDetails_Gid,'",
                     "HSN_Code":"',@HSN_Code,'",
                     "SGST_Rate":"',@SGST_Rate,'",
                     "CGST_Rate":"',@CGST_Rate,'",
                     "IGST_Rate":"',@IGST_Rate,'"

                    }');


			 	 call sp_FASale_Set('INSERT','SALE_MAKER', 'SALE_DETAIL', @lj_SaleProductData,lj_Classification,ls_Createby,@Last_Id,@Message);
			  	 select @Message into @Out_Msg_SaleDetail ;
			  #select @Out_Msg_SaleDetail;
			    if @Out_Msg_SaleDetail <> 'SUCCESS' THEN
			    	set Message = 'Error On Asset Sale Detail Insert.';
			        ROLLBACK;
			        leave sp_FAAssertProcess_Set;
			    ELSE
			        set Message = 'SUCCESS';
			    End if;



         set i = i+1;
         End While;

        ##### Update The Asset Sale Total Amount.
            set @Asset_TotalSale = 0;
        	select sum(assetsale_value) into @Asset_TotalSale from fa_trn_tassetsale
        	where assetsale_assetsaleheadergid = @Out_Msg_LastID  and assetsale_isactive = 'Y' and assetsale_isremoved = 'N' ;

        if @Asset_TotalSale <> 0 THEN

        	update fa_trn_tassetsaleheader set assetsaleheader_saletotalamount = @Asset_TotalSale,
             update_by = ls_Createby and update_date = now()
            where assetsaleheader_gid = @Out_Msg_LastID ;

						set countRow = (select ROW_COUNT());


                      if countRow > 0 then
							set Message = 'SUCCESS';
                       else
                            set Message = 'FAIL';
                           rollback;
                            leave sp_FAAssertProcess_Set;
                      End if;




         ELSEIF @Asset_TotalSale = 0 THEN
            set Message = 'Error On Asset Sale Total.';
            ROLLBACK;
            leave sp_FAAssertProcess_Set;
        End if;




              ############## iChecker Starts Here
elseif ls_Type = 'ASSET_WRITEOFF' and ls_Sub_Type = 'CHECKER' then
              ##### Write Off Checker :: Approve or Reject
              if ls_Action = 'UPDATE' then


					select JSON_LENGTH(lj_Details,'$') into @li_Detailjson_count;
					if @li_Detailjson_count is null or @li_Detailjson_count = 0 then
							set Message = 'No Data In Json - Asset Details.';
                            leave sp_FAAssertProcess_Set;
					end if;

					select JSON_LENGTH(lj_Status,'$') into @li_Statusjson_count;
					if @li_Statusjson_count is null or @li_Statusjson_count = 0 then
							set Message = 'No Data In Json - Asset Status.';
                            leave sp_FAAssertProcess_Set;
					end if;

                        select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,CONCAT('$.Status'))) into @ls_Status;

                        if @ls_Status is null or @ls_Status = '' then
								set Message = 'Status Is Needed.';
                                leave sp_FAAssertProcess_Set;
                        End if;

                        #### Get The Value by loop in a Variable
                        select JSON_LENGTH(lj_Details, CONCAT('$.ASSET[0].Asset_Gid')) into @Asset_Gid_Count;

									if @Asset_Gid_Count is null or @Asset_Gid_Count = 0 or @Asset_Gid_Count = '' then
											set Message = 'Asset Detail Gid Is Needed.';
											leave sp_FAAssertProcess_Set;
									End if;
                        set i = 0 ;
								While i <= @Asset_Gid_Count - 1 DO

											select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].Asset_Gid[',i,']'))) into @AssetDetails_Gid;

											if @AssetDetails_Gid <> 0 then
																	set @assetdetails_Trngid = 0;
																	Select b.assetdetails_gid into @assetdetails_Trngid
                                                                    from fa_tmp_tassetdetails as a
																	inner join fa_trn_tassetdetails as b on b.assetdetails_id = a.assetdetails_id
																	where a.assetdetails_isactive = 'Y' and a.assetdetails_isremoved = 'N'
																	and b.assetdetails_isactive = 'Y' and b.assetdetails_isremoved = 'N'
																	and a.entity_gid = @Entity_Gid
																	and a.assetdetails_gid = @AssetDetails_Gid;

                                                                    if @assetdetails_Trngid = 0 then
																			set Message = 'Error On Asset Transaction Data.';
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                    End if;

                                                            set @WriteOff_Gid = 0;
															Select ifnull(b.writeoff_gid,0) into @WriteOff_Gid from fa_tmp_tassetdetails as a
															inner join fa_trn_twriteoff as b on b.writeoff_assetdetailsid = a.assetdetails_id
															where a.assetdetails_isactive = 'Y' and a.assetdetails_isremoved = 'N'
															and b.writeoff_isactive = 'Y' and b.writeoff_isremoved = 'N'
                                                            and a.assetdetails_gid = @AssetDetails_Gid
                                                            ;


                                                            if @WriteOff_Gid = 0 then
																set Message = 'Error On WriteOff Data';
                                                                rollback;
                                                                leave sp_FAAssertProcess_Set;
                                                            End if;


																if @ls_Status = 'APPROVED' then
																			#### Call the Sp to Insert Teh Asset data from TMP table
																			set @lj_Details_Data = '';
																			set @lj_Details_Data = concat(
																			'{"Asset_Detail_Gids":"',@assetdetails_Trngid,'",
																			   "Status":"APPROVED",
																			   "Trn_Ref_Name":"FA_WRITEOFF",
																			   "Trn_To_Type":"C",
																			   "Trn_Role_Name":"CHECKER",
																			   "Trn_Remarks":"APPROVE",
                                                                               "Trn_Process_Gid":"',@WriteOff_Gid,'",
                                                                               "Trn_Process_Staus":"APPROVE"
																			}'
																			);
																			#select @lj_Details_Data;
																			call sp_FAAsset_Set('INSERT','ASSET_PROCESS_CHECKER','APPROVE',@lj_Details_Data,'{}',lj_Classification,ls_Createby,@Message);
																			select @Message into @Out_Msg_Asset;
																			#select @Out_Msg_Asset;
																			if @Out_Msg_Asset = 'SUCCESS' then
																				set Message = 'SUCCESS';
																			elseif @Out_Msg_Asset is null or @Out_Msg_Asset <> 'SUCCESS' then
																				 set Message = concat('FAIL ',@Out_Msg_Asset);
                                                                                 rollback;
                                                                                 leave sp_FAAssertProcess_Set;
																			End if;

                                                                            ### Affect In Main Table.
                                                                            ##### Update The Main Table.
																	set @lj_Writeoff_Data = '';
                                                                    set @lj_Writeoff_Data =
                                                                    concat('{
                                                                    "Asset_Detail_Gids":"',@assetdetails_Trngid,'",
                                                                    "RequestFor":"SUCCESS",
                                                                    "Asset_Status":"IN_ACTIVE",
                                                                    "Asset_WriteOff_Gid":"',@WriteOff_Gid,'"
                                                                    }');

																	call sp_FAAsset_Set('UPDATE', 'ASSET_CHECKER',
																	'REQUEST_FOR',
                                                                    @lj_Writeoff_Data,'{}',lj_Classification,ls_Createby,@Message);
                                                                    set @Out_Msg_WriteOff = '';
																	select @Message   into @Out_Msg_WriteOff;

                                                                    if @Out_Msg_WriteOff <> 'SUCCESS' then
																			set Message = Concat('FAIL',@Out_Msg_WriteOff);
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                     elseif @Out_Msg_WriteOff is null then
                                                                          set Message = Concat('FAIL In WriteOff Transaction Update. ');
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                    End if;


															elseif @ls_Status = 'REJECTED' then
																	select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,CONCAT('$.Remark'))) into @ls_Remark;

																	if @ls_Remark is null  or @ls_Remark = '' then
																		set Message = 'Remark Is Needed For Reject.';
                                                                        rollback;
																		leave sp_FAAssertProcess_Set;
																	End if;


																	set @lj_Details_Data = '';
																			set @lj_Details_Data = concat(
																			 '{"Asset_Detail_Gids":"',@AssetDetails_Gid,'",
																			   "Status":"REJECTED",
                                                                               "Asset_Trn_Gids" : "',@assetdetails_Trngid,'",
                                                                               "Trn_Ref_Name":"FA_WRITEOFF",
																			   "Remark": "',@ls_Remark,'",
                                                                               "Trn_To_Type":"C",
                                                                               "Trn_Role_Name":"CHECKER",
                                                                               "Trn_Process_Gid":"',@WriteOff_Gid,'",
                                                                               "Trn_Process_Staus":"REJECTED",
                                                                               "Trn_Remarks":"',@ls_Remark,'"

																			  }'
																			);

																			#select @AssetDetails_Gid,@ls_Remark;

																			#select @lj_Details_Data;

																			call sp_FAAsset_Set('UPDATE','ASSET_PROCESS_CHECKER','REJECT',@lj_Details_Data,
                                                                            '{}',lj_Classification,ls_Createby,@Message);
																			select @Message into @Out_Msg_Asset;

																			#select @Out_Msg_Asset;

																			if @Out_Msg_Asset = 'SUCCESS' then
																				set Message = 'SUCCESS';
																			elseif @Out_Msg_Asset is null or @Out_Msg_Asset <> 'SUCCESS' then
																				set Message = 'FAIL CHECKER';
                                                                                rollback;
                                                                                leave sp_FAAssertProcess_Set;
																			End if;



															End if;

                                                            #### Affect in the Process Table
                                                            ### set @WriteOff_Gid = 0;                                                            Check for Roll Back

                                                            set @WriteOff_Status = @ls_Status;

                                                            set @lj_Writeoff_Data = '';
                                                            set @lj_Writeoff_Data = concat('
                                                            {
                                                            "WriteOff_Gid":"',@WriteOff_Gid,'",
                                                            "WriteOff_Status":"',@WriteOff_Status,'"
                                                            }
                                                            ');

																call sp_FAWriteoff_Set('UPDATE','WRITEOFF_CHECKER','UPDATE',@lj_Writeoff_Data,lj_Classification,ls_Createby,@Message);
																			select @Message into @Out_Msg_WriteOff;
																			#select @Out_Msg_Asset;
																			if @Out_Msg_WriteOff = 'SUCCESS' then
																				set Message = 'SUCCESS';
																			elseif @Out_Msg_WriteOff is null or @Out_Msg_WriteOff <> 'SUCCESS' then
																				set Message = concat('FAIL In WriteOff Checker.',@Out_Msg_WriteOff);
                                                                                rollback;
                                                                                leave sp_FAAssertProcess_Set;
																			End if;

										end if;

									set i = i+1;
								End while;


           End if;

 elseif ls_Type = 'ASSET_IMPAIRMENT' and ls_Sub_Type = 'CHECKER' then
              ##### Write Off Checker :: Approve or Reject
              if ls_Action = 'UPDATE' then

					select JSON_LENGTH(lj_Details,'$') into @li_Detailjson_count;
					if @li_Detailjson_count is null or @li_Detailjson_count = 0 then
							set Message = 'No Data In Json - Asset Details.';
                            leave sp_FAAssertProcess_Set;
					end if;

					select JSON_LENGTH(lj_Status,'$') into @li_Statusjson_count;
					if @li_Statusjson_count is null or @li_Statusjson_count = 0 then
							set Message = 'No Data In Json - Asset Status.';
                            leave sp_FAAssertProcess_Set;
					end if;

                        select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,CONCAT('$.Status'))) into @ls_Status;

                        if @ls_Status is null or @ls_Status = '' then
								set Message = 'Status Is Needed.';
                                leave sp_FAAssertProcess_Set;
                        End if;

                        #### Get The Value by loop in a Variable
                        select JSON_LENGTH(lj_Details, CONCAT('$.ASSET[0].Asset_Gid')) into @Asset_Gid_Count;

									if @Asset_Gid_Count is null or @Asset_Gid_Count = 0 or @Asset_Gid_Count = '' then
											set Message = 'Asset Detail Gid Is Needed.';
											leave sp_FAAssertProcess_Set;
									End if;
                        set i = 0 ;
								While i <= @Asset_Gid_Count - 1 DO

											select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].Asset_Gid[',i,']'))) into @AssetDetails_Gid;

											if @AssetDetails_Gid <> 0 then
																	set @assetdetails_Trngid = 0;
																	Select b.assetdetails_gid into @assetdetails_Trngid
                                                                    from fa_tmp_tassetdetails as a
																	inner join fa_trn_tassetdetails as b on b.assetdetails_id = a.assetdetails_id
																	where a.assetdetails_isactive = 'Y' and a.assetdetails_isremoved = 'N'
																	and b.assetdetails_isactive = 'Y' and b.assetdetails_isremoved = 'N'
																	and a.entity_gid = @Entity_Gid
																	and a.assetdetails_gid = @AssetDetails_Gid;

                                                                    if @assetdetails_Trngid = 0 then
																			set Message = 'Error On Asset Transaction Data.';
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                    End if;

                                                            set @Impairmet_Gid = 0;
															Select ifnull(b.impairasset_gid,0) into @Impairmet_Gid
                                                            from fa_tmp_tassetdetails as a
															inner join fa_trn_timpairasset as b on b.impairasset_assetdetailsid = a.assetdetails_id
															where a.assetdetails_isactive = 'Y' and a.assetdetails_isremoved = 'N'
															and b.impairasset_isactive = 'Y' and b.impairasset_isremoved = 'N'
                                                            and a.assetdetails_gid = @AssetDetails_Gid
                                                            ;


                                                            if @Impairmet_Gid = 0 then
																set Message = 'Error On Impairment Data';
                                                                rollback;
                                                                leave sp_FAAssertProcess_Set;
                                                            End if;


																if @ls_Status = 'APPROVED' then
																			#### Call the Sp to Insert Teh Asset data from TMP table
																			set @lj_Details_Data = '';
																			set @lj_Details_Data = concat(
																			'{"Asset_Detail_Gids":"',@assetdetails_Trngid,'",
																			   "Status":"APPROVED",
                                                                               "Trn_Process_Gid":"',@Impairmet_Gid,'",
                                                                               "Trn_Process_Staus":"APPROVED",
																			   "Trn_Ref_Name":"FA_IMPAIRMENT",
																			   "Trn_To_Type":"C",
																			   "Trn_Role_Name":"CHECKER",
																			   "Trn_Remarks":"APPROVE"
																			}'
																			);
																			#select @lj_Details_Data;
																			call sp_FAAsset_Set('INSERT','ASSET_PROCESS_CHECKER','APPROVE',@lj_Details_Data,'{}',lj_Classification,ls_Createby,@Message);
																			select @Message into @Out_Msg_Asset;
																			#select @Out_Msg_Asset;
																			if @Out_Msg_Asset = 'SUCCESS' then
																				set Message = 'SUCCESS';
																			elseif @Out_Msg_Asset is null or @Out_Msg_Asset <> 'SUCCESS' then
																				 set Message = concat('FAIL ',@Out_Msg_Asset);
																			End if;

                                                                            ### Affect In Main Table.
                                                                            ##### Update The Main Table.
																	set @lj_Impair_Data = '';
                                                                    set @lj_Impair_Data =
                                                                    concat('{
                                                                    "Asset_Detail_Gids":"',@assetdetails_Trngid,'",
                                                                    "RequestFor":"SUCCESS",
                                                                    "Asset_Impair_Gid":"',@Impairmet_Gid,'"
                                                                    }');

																	call sp_FAAsset_Set('UPDATE', 'ASSET_CHECKER',
																	'REQUEST_FOR',
                                                                    @lj_Impair_Data,'{}',lj_Classification,ls_Createby,@Message);
                                                                    set @Out_Msg_Impair = '';
																	select @Message   into @Out_Msg_Impair;

                                                                    if @Out_Msg_Impair <> 'SUCCESS' then
																			set Message = Concat('FAIL',@Out_Msg_Impair);
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                     elseif @Out_Msg_Impair is null then
                                                                          set Message = Concat('FAIL In Impairment Transaction Update. ');
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                    End if;


															elseif @ls_Status = 'REJECTED' then
																	select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,CONCAT('$.Remark'))) into @ls_Remark;

																	if @ls_Remark is null  or @ls_Remark = '' then
																		set Message = 'Remark Is Needed For Reject.';
																	    rollback;
																		leave sp_FAAssertProcess_Set;
																	End if;


																	set @lj_Details_Data = '';
																			set @lj_Details_Data = concat(
																			'{"Asset_Detail_Gids":"',@AssetDetails_Gid,'",
 																				"Asset_Trn_Gids" : "',@assetdetails_Trngid,'",
																			   "Status":"REJECTED",
																			   "Remark": "',@ls_Remark,'",
                                                                               "Trn_Process_Gid":"',@Impairmet_Gid,'",
                                                                               "Trn_Process_Staus":"REJECTED",
																			   "Trn_Ref_Name":"FA_IMPAIRMENT",
																			   "Trn_To_Type":"C",
																			   "Trn_Role_Name":"CHECKER",
																			   "Trn_Remarks":"',@ls_Remark,'"
																			  }'
																			);

																			#select @AssetDetails_Gid,@ls_Remark;

																			#select @lj_Details_Data;

																			call sp_FAAsset_Set('UPDATE','ASSET_PROCESS_CHECKER','REJECT',@lj_Details_Data,
                                                                            '{}',lj_Classification,ls_Createby,@Message);
																			select @Message into @Out_Msg_Asset;

																			#select @Out_Msg_Asset;

																			if @Out_Msg_Asset = 'SUCCESS' then
																				set Message = 'SUCCESS';
																			elseif @Out_Msg_Asset is null or @Out_Msg_Asset <> 'SUCCESS' then
																				set Message = 'FAIL CHECKER';
                                                                                rollback;
                                                                                leave sp_FAAssertProcess_Set;
																			End if;

															End if;

                                                            #### Affect in the Process Table
                                                            ### set @WriteOff_Gid = 0;                                                            Check for Roll Back

                                                            set @Impair_Status = @ls_Status;

                                                            set @lj_Impairment_Data = '';
                                                            set @lj_Impairment_Data = concat('
                                                            {
                                                            "Impairment_Gid":"',@Impairmet_Gid,'",
                                                            "Impairment_Status":"',@Impair_Status,'"
                                                            }
                                                            ');

																call sp_FA_Impair_Asset_Set('UPDATE','IMPAIRMENT_CHECKER','UPDATE',@lj_Impairment_Data,lj_Classification,ls_Createby,@Message);
																			select @Message into @Out_Msg_Impairment;

																			if @Out_Msg_Impairment = 'SUCCESS' then
																				set Message = 'SUCCESS';
																			elseif @Out_Msg_Impairment <> 'SUCCESS'  then
																				set Message = concat('FAIL In Impairment Checker.',@Out_Msg_Impairment);
																					rollback;
																					leave sp_FAAssertProcess_Set;
                                                                              elseif @Out_Msg_Impairment is null  then
																					set Message = 'FAIL In Impairment Checker.';
																					rollback;
                                                                                leave sp_FAAssertProcess_Set;
																			End if;

										end if;

									set i = i+1;
								End while;


           End if;


elseif ls_Type = 'ASSET_CPDATE' and ls_Sub_Type = 'CHECKER' then
              ##### CAPDATE Checker :: Approve or Reject
              if ls_Action = 'UPDATE' then

					select JSON_LENGTH(lj_Details,'$') into @li_Detailjson_count;
					if @li_Detailjson_count is null or @li_Detailjson_count = 0 then
							set Message = 'No Data In Json - Asset Details.';
                            leave sp_FAAssertProcess_Set;
					end if;

					select JSON_LENGTH(lj_Status,'$') into @li_Statusjson_count;
					if @li_Statusjson_count is null or @li_Statusjson_count = 0 then
							set Message = 'No Data In Json - Asset Status.';
                            leave sp_FAAssertProcess_Set;
					end if;

                        select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,CONCAT('$.Status'))) into @ls_Status;

                        if @ls_Status is null or @ls_Status = '' then
								set Message = 'Status Is Needed.';
                                leave sp_FAAssertProcess_Set;
                        End if;

                        #### Get The Value by loop in a Variable
                        select JSON_LENGTH(lj_Details, CONCAT('$.ASSET[0].Asset_Gid')) into @Asset_Gid_Count;

									if @Asset_Gid_Count is null or @Asset_Gid_Count = 0 or @Asset_Gid_Count = '' then
											set Message = 'Asset Detail Gid Is Needed.';
											leave sp_FAAssertProcess_Set;
									End if;
                        set i = 0 ;
								While i <= @Asset_Gid_Count - 1 DO

											select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].Asset_Gid[',i,']'))) into @AssetDetails_Gid;

											if @AssetDetails_Gid <> 0 then
																	set @assetdetails_Trngid = 0;
                                                                    set @cap_date = '';
																	Select b.assetdetails_gid,date_format(a.assetdetails_capdate,'%Y-%m-%d') into @assetdetails_Trngid,@cap_date_New
                                                                    from fa_tmp_tassetdetails as a
																	inner join fa_trn_tassetdetails as b on b.assetdetails_id = a.assetdetails_id
																	where a.assetdetails_isactive = 'Y' and a.assetdetails_isremoved = 'N'
																	and b.assetdetails_isactive = 'Y' and b.assetdetails_isremoved = 'N'
																	and a.entity_gid = @Entity_Gid
																	and a.assetdetails_gid = @AssetDetails_Gid;

                                                                    if @assetdetails_Trngid = 0 then
																			set Message = 'Error On Asset Transaction Data.';
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                    End if;


														set @CapDate_Gid = 0;
                                                            Select ifnull(b.assetcapdate_gid,0) into @CapDate_Gid
															from fa_tmp_tassetdetails as a
                                                            inner join fa_trn_tassetcapdate as b on b.assetcapdate_assetdetailsid = a.assetdetails_id
                                                            where a.assetdetails_isactive = 'Y' and a.assetdetails_isremoved = 'N'
                                                            and b.assetcapdate_isactive = 'Y' and b.assetcapdate_isremoved = 'N'
                                                            and a.assetdetails_gid=@AssetDetails_Gid
                                                            and b.assetcapdate_status = 'SUBMITTED'
                                                            ;


                                                            if @CapDate_Gid = 0 then
																set Message = 'Error On CapDate Data';
                                                                rollback;
                                                                leave sp_FAAssertProcess_Set;
                                                            End if;


																if @ls_Status = 'APPROVED' then
																			#### Call the Sp to Insert Teh Asset data from TMP table
																			set @lj_Details_Data = '';
																			set @lj_Details_Data = concat(
																			'{"Asset_Detail_Gids":"',@assetdetails_Trngid,'",
																			   "Status":"APPROVED",
																			   "Trn_Ref_Name":"FA_CPDATE",
																			   "Trn_To_Type":"C",
																			   "Trn_Role_Name":"CHECKER",
																			   "Trn_Remarks":"APPROVE",
                                                                               "Trn_Process_Gid":"',@CapDate_Gid,'",
                                                                               "Trn_Process_Staus":"APPROVE"
																			}'
																			);
																		#	select @lj_Details_Data;
																			call sp_FAAsset_Set('UPDATE','ASSET_PROCESS_CHECKER','APPROVE',
																				@lj_Details_Data,'{}',lj_Classification,ls_Createby,@Message);
																			select @Message into @Out_Msg_Asset;
																			#select @Out_Msg_Asset; ### remove it
																			if @Out_Msg_Asset = 'SUCCESS' then
																				set Message = 'SUCCESS';
																			elseif @Out_Msg_Asset is null or @Out_Msg_Asset <> 'SUCCESS' then
																				 set Message = concat('FAIL ',@Out_Msg_Asset);
																			End if;

                                                                            ### Affect In Main Table.
                                                                            ##### Update The Main Table..
																	set @lj_CapDate_Data = '';
                                                                    set @lj_CapDate_Data =
                                                                    concat('{
                                                                    "Asset_Detail_Gids":"',@assetdetails_Trngid,'",
                                                                    "RequestFor":"SUCCESS",
                                                                    "Asset_CapDate":"',@cap_date_New,'",
                                                                    "Asset_Cap_Gid":"',@CapDate_Gid,'"
                                                                    }');

                                                                    #select @lj_CapDate_Data;
																	call sp_FAAsset_Set('UPDATE', 'ASSET_CHECKER',
																	'REQUEST_FOR',
                                                                    @lj_CapDate_Data,'{}',lj_Classification,ls_Createby,@Message);
                                                                    set @Out_Msg_CapDate = '';
																	select @Message   into @Out_Msg_CapDate;
                                                                    #select @Out_Msg_CapDate;
                                                                    if @Out_Msg_CapDate <> 'SUCCESS' then
																			set Message = Concat('FAIL',@Out_Msg_CapDate);
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                     elseif @Out_Msg_CapDate is null then
                                                                          set Message = Concat('FAIL In CapDate Transaction Update. ');
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                    End if;

                                                                   #### Calculate The Depreciation.
                                                                    ### delete The Depreciation if Exists.

                                                                   set @Depreciation_OldGids = 0;
                                                                   select ifnull(group_concat(depreciation_gid),0) into @Depreciation_OldGids
                                                                   from fa_trn_tdepreciation where depreciation_assetdetailsgid = @assetdetails_Trngid
                                                                   and depreciation_isactive = 'Y' and depreciation_isremoved = 'N' and depreciation_type = 1
                                                                   and entity_gid = @Entity_Gid;

                                                                   if @Depreciation_OldGids <> 0 THEN
                                                                       select @Depreciation_OldGids;
                                                                       set @lj_depreciation_data = '';
                                                                       set @lj_depreciation_data = concat('{
																				"Depreciation_Gid":"',@Depreciation_OldGids,'"
                                                                             }');

                                                                       call sp_FADepreciation_Set('UPDATE', 'DEPRECIATION', 'FLAG', @lj_depreciation_data, '{}', lj_Classification, ls_Createby,@Message);
                                                                        select @Message into @Out_Msg_Depreciation;

                                                                       if @Out_Msg_Depreciation <> 'SUCCESS' THEN
                                                                          set Message = CONCAT('Error On Old Depreciation Delete. - ',@Out_Msg_Depreciation);
                                                                          ROLLBACK;
                                                                          leave sp_FAAssertProcess_Set;
                                                                        ELSEIF @Out_Msg_Depreciation is null THEN
                                                                          set Message = 'Error On Old Depreciation Delete.';
                                                                          ROLLBACK;
                                                                          leave sp_FAAssertProcess_Set;
                                                                         ELSEIF @Out_Msg_Depreciation = 'SUCCESS' THEN
                                                                           set Message = 'SUCCESS';
                                                                       End if;


                                                                      ### Calculate Depreciation
                                                                      select date_format(now(),'%Y-%m-%d') into @Cur_Date ;
                                                                       set @lj_depreciation_data = '';
                                                                       set @lj_depreciation_data = concat('{
																				"Asset_Gids":"',@assetdetails_Trngid,'",
                                                                                "From_Date":"',@cap_date_New,'",
 																				"To_Date":"',@Cur_Date,'"
                                                                             }');

                                                                       call sp_FADepreciation_Set('INSERT', 'DEPRECATION', 'SINGLEPROCESS', @lj_depreciation_data, '{}', lj_Classification, ls_Createby,@Message);
                                                                        select @Message into @Out_Msg_Depreciation;

                                                                       if @Out_Msg_Depreciation <> 'SUCCESS' THEN
                                                                          set Message = CONCAT('Error On Old Depreciation Calculate. - ',@Out_Msg_Depreciation);
                                                                          ROLLBACK;
                                                                          leave sp_FAAssertProcess_Set;
                                                                        ELSEIF @Out_Msg_Depreciation is null THEN
                                                                          set Message = 'Error On Old Depreciation Delete.';
                                                                          ROLLBACK;
                                                                          leave sp_FAAssertProcess_Set;
                                                                        ELSEIF @Out_Msg_Depreciation = 'SUCCESS' THEN
                                                                           set Message = 'SUCCESS';
                                                                       End if;


                                                                   End if;

															elseif @ls_Status = 'REJECTED' then
																	select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,CONCAT('$.Remark'))) into @ls_Remark;
																	#select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,CONCAT('$.Trn_Ref_Name'))) into @Trn_Ref_Name;

																	if @ls_Remark is null  or @ls_Remark = '' then
																		set Message = 'Remark Is Needed For Reject.';
																	    rollback;
																		leave sp_FAAssertProcess_Set;
																	End if;

																	set @lj_Details_Data = '';
																			set @lj_Details_Data = concat(
																			'{"Asset_Detail_Gids":"',@AssetDetails_Gid ,'",
                                                                               "Asset_Trn_Gids" : "',@assetdetails_Trngid,'",
																			   "Status":"REJECTED",
																			   "Remark": "',@ls_Remark,'",
                                                                               "Trn_Ref_Name":"FA_CPDATE",
                                                                               "Trn_Process_Gid":"',@CapDate_Gid,'",
                                                                               "Trn_Process_Staus":"REJECTED",
																			   "Trn_To_Type":"C",
																			   "Trn_Role_Name":"CHECKER",
																			   "Trn_Remarks":"',@ls_Remark,'"
																			  }'

																			);

																			#select @AssetDetails_Gid,@ls_Remark;

																			#select @lj_Details_Data;

																			call sp_FAAsset_Set('UPDATE','ASSET_PROCESS_CHECKER','REJECT',@lj_Details_Data,
                                                                            '{}',lj_Classification,ls_Createby,@Message);
																			select @Message into @Out_Msg_Asset;

																#			select @Out_Msg_Asset;

																			if @Out_Msg_Asset = 'SUCCESS' then
																				set Message = 'SUCCESS';
																			elseif @Out_Msg_Asset is null or @Out_Msg_Asset <> 'SUCCESS' then
																				set Message = 'FAIL CHECKER';
                                                                                rollback;
                                                                                leave sp_FAAssertProcess_Set;
																			End if;

															End if;

                                                            #### Affect in the Process Table
                                                            ### set @WriteOff_Gid = 0;                                                            Check for Roll Back

                                                            set @CapDate_Status = @ls_Status;

                                                            set @lj_CapDate_Data = '';
                                                            set @lj_CapDate_Data = concat('
                                                            {
                                                            "CapDate_Gid":"',@CapDate_Gid,'",
                                                            "CapDate_Status":"',@CapDate_Status,'"
                                                            }
                                                            ');

																call sp_FA_CapDate_Set('UPDATE','CAPDATE_CHECKER',
																	'UPDATE',@lj_CapDate_Data,lj_Classification,ls_Createby,@Message);
																			select @Message into @Out_Msg_CapDate;

																			if @Out_Msg_CapDate = 'SUCCESS' then
																				set Message = 'SUCCESS';
																			elseif @Out_Msg_CapDate <> 'SUCCESS'  then
																				set Message = concat('FAIL In CapDate Checker.',@Out_Msg_CapDate);
																					rollback;
																					leave sp_FAAssertProcess_Set;
                                                                              elseif @Out_Msg_CapDate is null  then
																					set Message = 'FAIL In CapDate Checker.';
																					rollback;
                                                                                leave sp_FAAssertProcess_Set;
																			End if;
                                                                           # select @Out_Msg_CapDate;

										end if;

									set i = i+1;
								End while;

           End if;

 elseif ls_Type = 'ASSET_CAT' and ls_Sub_Type = 'CHECKER' then
              #####CATEGORY Checker :: Approve or Reject
              if ls_Action = 'UPDATE' then

					select JSON_LENGTH(lj_Details,'$') into @li_Detailjson_count;
					if @li_Detailjson_count is null or @li_Detailjson_count = 0 then
							set Message = 'No Data In Json - Asset Details.';
                            leave sp_FAAssertProcess_Set;
					end if;

					select JSON_LENGTH(lj_Status,'$') into @li_Statusjson_count;
					if @li_Statusjson_count is null or @li_Statusjson_count = 0 then
							set Message = 'No Data In Json - Asset Status.';
                            leave sp_FAAssertProcess_Set;
					end if;

                        select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,CONCAT('$.Status'))) into @ls_Status;

                        if @ls_Status is null or @ls_Status = '' then
								set Message = 'Status Is Needed.';
                                leave sp_FAAssertProcess_Set;
                        End if;

                        #### Get The Value by loop in a Variable
                        select JSON_LENGTH(lj_Details, CONCAT('$.ASSET[0].Asset_Gid')) into @Asset_Gid_Count;

									if @Asset_Gid_Count is null or @Asset_Gid_Count = 0 or @Asset_Gid_Count = '' then
											set Message = 'Asset Detail Gid Is Needed.';
											leave sp_FAAssertProcess_Set;
									End if;
                        set i = 0 ;
								While i <= @Asset_Gid_Count - 1 DO

											select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].Asset_Gid[',i,']'))) into @AssetDetails_Gid;

											if @AssetDetails_Gid <> 0 then
																	set @assetdetails_Trngid = 0;
                                                                    set @assetdetails_Catgid = 0;

																	Select b.assetdetails_gid,a.assetdetails_assetcatgid,date_format(b.assetdetails_capdate,'%Y-%m-%d') into @assetdetails_Trngid,
																	@assetdetails_Catgid,@cap_date_New
                                                                    from fa_tmp_tassetdetails as a
																	inner join fa_trn_tassetdetails as b on b.assetdetails_id = a.assetdetails_id
																	where a.assetdetails_isactive = 'Y' and a.assetdetails_isremoved = 'N'
																	and b.assetdetails_isactive = 'Y' and b.assetdetails_isremoved = 'N'
																	and a.entity_gid = @Entity_Gid
																	and a.assetdetails_gid = @AssetDetails_Gid;

                                                                    if @assetdetails_Trngid = 0 then
																			set Message = 'Error On Asset Transaction Data.';
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                    End if;


															set @Cat_Gid = 0;
                                                            Select ifnull(b.assetcatchange_gid,0) into @Cat_Gid
															from fa_tmp_tassetdetails as a
                                                            inner join fa_trn_tassetcatchange as b
                                                            on b.assetcatchange_assetdetailsid = a.assetdetails_id
                                                            where a.assetdetails_isactive = 'Y' and a.assetdetails_isremoved = 'N'
                                                            and b.assetcatchange_isactive = 'Y' and b.assetcatchange_isremoved = 'N'
                                                            and a.assetdetails_gid=@AssetDetails_Gid
                                                            and b.assetcatchange_status = 'SUBMITTED'
                                                            ;

														#	select @assetdetails_Trngid,@assetdetails_Catgid ,	@Cat_Gid ;

                                                            if @Cat_Gid = 0 then
																set Message = 'Error On Cat Data';
                                                                rollback;
                                                                leave sp_FAAssertProcess_Set;
                                                            End if;


																if @ls_Status = 'APPROVED' then
																			#### Call the Sp to Insert Teh Asset data from TMP table
																			set @lj_Details_Data = '';
																			set @lj_Details_Data = concat(
																			 '{"Asset_Detail_Gids":"',@assetdetails_Trngid,'",
																			   "Status":"APPROVED",
                                                                               "Trn_Process_Gid":"',@Cat_Gid,'",
                                                                               "Trn_Process_Staus":"APPROVED",
																			   "Trn_Ref_Name":"FA_CATCHANGE",
																			   "Trn_To_Type":"C",
																			   "Trn_Role_Name":"CHECKER",
																			   "Trn_Remarks":"APPROVE"
																			  }'
																			);
																			#select @lj_Details_Data;
																			call sp_FAAsset_Set('UPDATE','ASSET_PROCESS_CHECKER','APPROVE',
																				@lj_Details_Data,'{}',lj_Classification,ls_Createby,@Message);
																			select @Message into @Out_Msg_Asset;
														#		select @Out_Msg_Asset;
																			if @Out_Msg_Asset = 'SUCCESS' then
																				set Message = 'SUCCESS';
																			elseif @Out_Msg_Asset is null or @Out_Msg_Asset <> 'SUCCESS' then
																				 set Message = concat('FAIL ',@Out_Msg_Asset);
																				 ROLLBACK;
																				leave sp_FAAssertProcess_Set;
																			End if;

                                                                            ### Affect In Main Table.
                                                                            ##### Update The Main Table.

																	set @lj_Cat_Data = '';
                                                                    set @lj_Cat_Data =
                                                                    concat('{
                                                                    "Asset_Detail_Gids":"',@assetdetails_Trngid,'",
                                                                    "RequestFor":"SUCCESS",
                                                                    "Asset_Cat_Gid":"',@assetdetails_Catgid,'",
                                                                    "Asset_CatChange_gid":"',@Cat_Gid,'"
                                                                    }');

                                                         #           select @lj_Cat_Data;
																	call sp_FAAsset_Set('UPDATE', 'ASSET_CHECKER',
																	'REQUEST_FOR',
                                                                    @lj_Cat_Data,'{}',lj_Classification,ls_Createby,@Message);
                                                                    set @Out_Msg_Cat = '';
																	select @Message   into @Out_Msg_Cat;

                                                                    if @Out_Msg_Cat <> 'SUCCESS' then
																			set Message = Concat('FAIL',@Out_Msg_Cat);
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                     elseif @Out_Msg_Cat is null then
                                                                          set Message = Concat('FAIL In Cat Transaction Update. ');
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                     else
																			set Message = 'SUCCESS';
                                                                    End if;


                                                                  #### Calculate The Depreciation.
                                                                    ### delete The Depreciation if Exists.

                                                                   set @Depreciation_OldGids = 0;
                                                                   select ifnull(group_concat(depreciation_gid),0) into @Depreciation_OldGids
                                                                   from fa_trn_tdepreciation where depreciation_assetdetailsgid = @assetdetails_Trngid
                                                                   and depreciation_isactive = 'Y' and depreciation_isremoved = 'N' and depreciation_type = 1
                                                                   and entity_gid = @Entity_Gid;

                                                                  #select @Depreciation_OldGids;

                                                                   if @Depreciation_OldGids <> 0 THEN
                                                                   #    select @Depreciation_OldGids;
                                                                       set @lj_depreciation_data = '';
                                                                       set @lj_depreciation_data = concat('{
																				"Depreciation_Gid":"',@Depreciation_OldGids,'"
                                                                             }');

                                                                       call sp_FADepreciation_Set('UPDATE', 'DEPRECIATION', 'FLAG', @lj_depreciation_data, '{}', lj_Classification, ls_Createby,@Message);
                                                                        select @Message into @Out_Msg_Depreciation;

                                                                       if @Out_Msg_Depreciation <> 'SUCCESS' THEN
                                                                          set Message = CONCAT('Error On Old Depreciation Delete. - ',@Out_Msg_Depreciation);
                                                                          ROLLBACK;
                                                                          leave sp_FAAssertProcess_Set;
                                                                        ELSEIF @Out_Msg_Depreciation is null THEN
                                                                          set Message = 'Error On Old Depreciation Delete.';
                                                                          ROLLBACK;
                                                                          leave sp_FAAssertProcess_Set;
                                                                         ELSEIF @Out_Msg_Depreciation = 'SUCCESS' THEN
                                                                           set Message = 'SUCCESS';
                                                                       End if;


                                                                      ### Calculate Depreciation

                                                                      #      select  date_format(assetdetails_capdate,'%Y-%m-%d') into @cap_date_New
                                                                      #from fa_trn_tassetdetails where assetdetails_gid = 10 and entity_gid = 1 ;

                                                                      select date_format(now(),'%Y-%m-%d') into @Cur_Date ;
                                                                       set @lj_depreciation_data = '';
                                                                       set @lj_depreciation_data = concat('{
																				"Asset_Gids":"',@assetdetails_Trngid,'",
                                                                                "From_Date":"',@cap_date_New,'",
 																				"To_Date":"',@Cur_Date,'"
                                                                             }');

                                                                         #   select @lj_depreciation_data,@assetdetails_Trngid,@cap_date_New,@Cur_Date,@Entity_Gid;

                                                                       call sp_FADepreciation_Set('INSERT', 'DEPRECATION', 'SINGLEPROCESS', @lj_depreciation_data, '{}', lj_Classification, ls_Createby,@Message);
                                                                        select @Message into @Out_Msg_Depreciation;

                                                                       if @Out_Msg_Depreciation <> 'SUCCESS' THEN
                                                                          set Message = CONCAT('Error On Old Depreciation Calculate. - ',@Out_Msg_Depreciation);
                                                                          rollback;
                                                                          leave sp_FAAssertProcess_Set;
                                                                        ELSEIF @Out_Msg_Depreciation is null THEN
                                                                          set Message = 'Error On Old Depreciation Delete.';
                                                                         ROLLBACK;
                                                                          leave sp_FAAssertProcess_Set;
                                                                        ELSEIF @Out_Msg_Depreciation = 'SUCCESS' THEN
                                                                           set Message = 'SUCCESS';
                                                                       End if;


                                                                   End if;


															elseif @ls_Status = 'REJECTED' then
																	select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,CONCAT('$.Remark'))) into @ls_Remark;


																	if @ls_Remark is null  or @ls_Remark = '' then
																		set Message = 'Remark Is Needed For Reject.';
																		leave sp_FAAssertProcess_Set;
																	End if;


																	set @lj_Details_Data = '';
																			set @lj_Details_Data = concat(
																			'{"Asset_Detail_Gids":"',@AssetDetails_Gid ,'",
                                                                               "Asset_Trn_Gids" : "',@assetdetails_Trngid,'",
																			   "Status":"REJECTED",
																			   "Remark": "',@ls_Remark,'",
                                                                               "Trn_Ref_Name":"FA_CATCHANGE",
                                                                               "Trn_Process_Gid":"',@Cat_Gid,'",
                                                                               "Trn_Process_Staus":"REJECTED",
																			   "Trn_To_Type":"C",
																			   "Trn_Role_Name":"CHECKER",
																			   "Trn_Remarks":"',@ls_Remark,'"

																			  }'
																			);

																			#select @AssetDetails_Gid,@ls_Remark;

																			#select @lj_Details_Data;

																			call sp_FAAsset_Set('UPDATE','ASSET_PROCESS_CHECKER','REJECT',@lj_Details_Data,
                                                                            '{}',lj_Classification,ls_Createby,@Message);
																			select @Message into @Out_Msg_Asset;

																			#select @Out_Msg_Asset;

																			if @Out_Msg_Asset = 'SUCCESS' then
																				set Message = 'SUCCESS';
																			elseif @Out_Msg_Asset is null or @Out_Msg_Asset <> 'SUCCESS' then
																				set Message = 'FAIL CHECKER';
                                                                                rollback;
                                                                                leave sp_FAAssertProcess_Set;
																			End if;

															End if;

                                                            #### Affect in the Process Table
                                                            ### set @WriteOff_Gid = 0;                                                            Check for Roll Back


													set @Cat_Status = @ls_Status;

                                                            set @Cat_Data = '';
                                                            set @Cat_Data = concat('
                                                            {
                                                            "CatChange_Gid":"',@Cat_Gid,'",
                                                            "CatChange_Status":"',@Cat_Status,'"
                                                            }
                                                            ');

                                                           # select @Cat_Data;
																call sp_FA_CatChange_Set('UPDATE','CAT_CHANGE_CHECKER',
																	'UPDATE',@Cat_Data,lj_Classification,ls_Createby,@Message);
																			select @Message into @Out_Msg_CatChange;

																			if @Out_Msg_CatChange = 'SUCCESS' then
																				set Message = 'SUCCESS';
																			elseif @Out_Msg_CatChange <> 'SUCCESS'  then
																				set Message = concat('FAIL In Cat Checker.',@Out_Msg_CatChange);
																					rollback;
																					leave sp_FAAssertProcess_Set;
                                                                              elseif @Out_Msg_CatChange is null  then
																					set Message = 'FAIL In Cat Checker.';
																					rollback;
                                                                                leave sp_FAAssertProcess_Set;
																			End if;

										end if;

									set i = i+1;
								End while;

           End if;

 elseif ls_Type = 'ASSET_TRANSFER' and ls_Sub_Type = 'CHECKER' then
              #####Transfer Checker :: Approve or Reject
              if ls_Action = 'UPDATE' then

					select JSON_LENGTH(lj_Details,'$') into @li_Detailjson_count;
					if @li_Detailjson_count is null or @li_Detailjson_count = 0 then
							set Message = 'No Data In Json - Asset Details.';
                            leave sp_FAAssertProcess_Set;
					end if;

					select JSON_LENGTH(lj_Status,'$') into @li_Statusjson_count;
					if @li_Statusjson_count is null or @li_Statusjson_count = 0 then
							set Message = 'No Data In Json - Asset Status.';
                            leave sp_FAAssertProcess_Set;
					end if;

                        select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,CONCAT('$.Status'))) into @ls_Status;

                        if @ls_Status is null or @ls_Status = '' then
								set Message = 'Status Is Needed.';
                                leave sp_FAAssertProcess_Set;
                        End if;

                        #### Get The Value by loop in a Variable
                        select JSON_LENGTH(lj_Details, CONCAT('$.ASSET[0].Asset_Gid')) into @Asset_Gid_Count;

									if @Asset_Gid_Count is null or @Asset_Gid_Count = 0 or @Asset_Gid_Count = '' then
											set Message = 'Asset Detail Gid Is Needed.';
											leave sp_FAAssertProcess_Set;
									End if;
                        set i = 0 ;
								While i <= @Asset_Gid_Count - 1 DO

											select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].Asset_Gid[',i,']'))) into @AssetDetails_Gid;

											if @AssetDetails_Gid <> 0 then
																	set @assetdetails_Trngid = 0;
                                                                    set @assetdetails_Id_New = 0;
                                                                    set @assetdetails_BranchGid_New = 0;
																	Select b.assetdetails_gid,a.assetdetails_assetcatgid,a.assetdetails_branchgid
																		into @assetdetails_Trngid,@assetdetails_Id_New,@assetdetails_BranchGid_New
                                                                    from fa_tmp_tassetdetails as a
																	inner join fa_trn_tassetdetails as b on b.assetdetails_id = a.assetdetails_id
																	where a.assetdetails_isactive = 'Y' and a.assetdetails_isremoved = 'N'
																	and b.assetdetails_isactive = 'Y' and b.assetdetails_isremoved = 'N'
																	and a.entity_gid = @Entity_Gid
																	and a.assetdetails_gid = @AssetDetails_Gid;

                                                                    if @assetdetails_Trngid = 0 then
																			set Message = 'Error On Asset Transaction Data.';
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                    End if;


															set @Transfer_Gid = 0;
                                                            Select b.assettfr_gid into @Transfer_Gid
															from fa_tmp_tassetdetails as a
                                                            inner join fa_trn_tassettfr as b on b.assettfr_assetdetailsid = a.assetdetails_id
                                                            where a.assetdetails_isactive = 'Y' and a.assetdetails_isremoved = 'N'
                                                            and b.assettfr_isactive = 'Y' and b.assettfr_isremoved = 'N'
                                                            and a.assetdetails_gid=@AssetDetails_Gid;




                                                            if @Transfer_Gid = 0 then
																set Message = 'Error On Transfer Data';
                                                                rollback;
                                                                leave sp_FAAssertProcess_Set;
                                                            End if;

                                	if @ls_Status = 'APPROVED' then

										set @lj_Transfer_Data = '';
										set @lj_Transfer_Data = concat(
																	'{  "Asset_Detail_Gids":"',@AssetDetails_Gid,'",
																		"Asset_TFR_Gid":"',@Transfer_Gid,'",
                                                                        "Asset_TFR_Status":"APPROVED"

																		}'
																	);

                                                       # select @lj_Transfer_Data;

                                                        call sp_FA_TFR_Asset_Set('UPDATE', 'TFR_CHECKER','TRANSFER',
																@lj_Transfer_Data,lj_Classification,ls_Createby,@Message);
																	set @Out_Msg_Transfer='';
																	select @Message into @Out_Msg_Transfer;
                                                                   #select @Out_Msg_Transfer;
                                                                    if @Out_Msg_Transfer <> 'SUCCESS' then
																			set Message = concat('FAIL - ',@Out_Msg_Transfer);
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                    End if;



																			#### Call the Sp to Insert Teh Asset data from TMP table
																			set @lj_Details_Data = '';
																			set @lj_Details_Data = concat(
																			 '{"Asset_Detail_Gids":"',@assetdetails_Trngid,'",
																			   "Status":"APPROVED",
                                                                               "Trn_Process_Gid":"',@Transfer_Gid,'",
                                                                               "Trn_Process_Staus":"APPROVED",
																			   "Trn_Ref_Name":"FA_TRANSFER",
																			   "Trn_To_Type":"C",
																			   "Trn_Role_Name":"CHECKER",
																			   "Trn_Remarks":"APPROVE"
																			  }'
																			);
																			#select @lj_Details_Data;
																			call sp_FAAsset_Set('UPDATE','ASSET_PROCESS_CHECKER','APPROVE',
																				@lj_Details_Data,'{}',lj_Classification,ls_Createby,@Message);
																			select @Message into @Out_Msg_Asset;
																			#select @Out_Msg_Asset;
																			if @Out_Msg_Asset = 'SUCCESS' then
																				set Message = 'SUCCESS';
																			elseif @Out_Msg_Asset is null or @Out_Msg_Asset <> 'SUCCESS' then
																				 set Message = concat('FAIL ',@Out_Msg_Asset);
																			End if;



                                                                            ### Affect In Main Table.
                                                                            ##### Update The Main Table.
																	set @lj_Transfer_Data = '';
                                                                    set @lj_Transfer_Data =
                                                                    concat('{
                                                                    "Asset_Detail_Gids":"',@assetdetails_Trngid,'",
                                                                    "RequestFor":"SUCCESS",
                                                                    "Asset_Transfer_Gid":"',@Transfer_Gid,'"
																			 }');

                                                                    #select @lj_Transfer_Data;
																	call sp_FAAsset_Set('UPDATE', 'ASSET_CHECKER',
																	'REQUEST_FOR',
                                                                    @lj_Transfer_Data,'{}',lj_Classification,ls_Createby,@Message);
                                                                    set @Out_Msg_Tfr = '';
																	select @Message   into @Out_Msg_Tfr;

                                                                    #select @Out_Msg_Tfr;

                                                                    if @Out_Msg_Tfr <> 'SUCCESS' then
																			set Message = Concat('FAIL',@Out_Msg_Tfr);
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                     elseif @Out_Msg_Tfr is null then
                                                                          set Message = Concat('FAIL In TRANSFER REQUEST_FOR Update. ');
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                    End if;



															elseif @ls_Status = 'REJECTED' then

																	select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,CONCAT('$.Remark'))) into @ls_Remark;


																	if @ls_Remark is null  or @ls_Remark = '' then
																		set Message = 'Remark Is Needed For Reject.';
																	   rollback;
																		leave sp_FAAssertProcess_Set;
																	End if;

																	set @lj_Details_Data = '';
																	set @lj_Details_Data = concat(
																			'{"Asset_Detail_Gids":"',@AssetDetails_Gid ,'",
                                                                               "Asset_Trn_Gids" : "',@assetdetails_Trngid,'",
																			   "Status":"REJECTED",
																			   "Remark": "',@ls_Remark,'",
																			   "Trn_Process_Gid":"',@Transfer_Gid,'",
                                                                               "Trn_Process_Staus":"REJECTED",
																			   "Trn_Ref_Name":"FA_TRANSFER",
																			   "Trn_To_Type":"C",
																			   "Trn_Role_Name":"CHECKER",
																			   "Trn_Remarks":"',@ls_Remark,'"
																			  }'
																			);

																			#select @AssetDetails_Gid,@ls_Remark;

																			#select @lj_Details_Data;

																			call sp_FAAsset_Set('UPDATE','ASSET_PROCESS_CHECKER','REJECT',@lj_Details_Data,
                                                                            '{}',lj_Classification,ls_Createby,@Message);
																			select @Message into @Out_Msg_Asset;

																			#select @Out_Msg_Asset;

																			if @Out_Msg_Asset = 'SUCCESS' then
																				set Message = 'SUCCESS';
																			elseif @Out_Msg_Asset is null or @Out_Msg_Asset <> 'SUCCESS' then
																				set Message = 'FAIL CHECKER';
                                                                                rollback;
                                                                                leave sp_FAAssertProcess_Set;
																			End if;


																	set @lj_Transfer_Data = '';
																	set @lj_Transfer_Data = concat(
																	'{
																		"Asset_TFR_Gid":"',@Transfer_Gid,'",
                                                                        "Asset_TFR_Status":"',@ls_Status,'"
																		}'
																	);

                                                        #select @lj_Transfer_Data;

                                                        call sp_FA_TFR_Asset_Set('UPDATE', 'TFR_CHECKER','TRANSFER',
																@lj_Transfer_Data,lj_Classification,ls_Createby,@Message);
																	set @Out_Msg_Transfer='';
																	select @Message into @Out_Msg_Transfer;

																			#select @Out_Msg_Transfer;
                                                                    if @Out_Msg_Transfer <> 'SUCCESS' then
																			set Message = concat('FAIL - ',@Out_Msg_Transfer);
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                    End if;






															End if;

                                                            #### Affect in the Process Table
                                                            ### set @WriteOff_Gid = 0;                                                            Check for Roll Back


										end if;

									set i = i+1;
								End while;

           End if;

 elseif ls_Type = 'ASSET_MERGE' and ls_Sub_Type = 'CHECKER' then
              #####Transfer Checker :: Approve or Reject
              if ls_Action = 'UPDATE' then

							select JSON_LENGTH(lj_Details,'$') into @li_Detailjson_count;
							if @li_Detailjson_count is null or @li_Detailjson_count = 0 then
									set Message = 'No Data In Json - Asset Details.';
									leave sp_FAAssertProcess_Set;
							end if;

							select JSON_LENGTH(lj_Status,'$') into @li_Statusjson_count;
							if @li_Statusjson_count is null or @li_Statusjson_count = 0 then
									set Message = 'No Data In Json - Asset Status.';
									leave sp_FAAssertProcess_Set;
							end if;

								select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,CONCAT('$.Status'))) into @ls_Status;
								#select @ls_Status;

								if @ls_Status is null or @ls_Status = '' then
										set Message = 'Status Is Needed.';
										leave sp_FAAssertProcess_Set;
								End if;

								#### Get The Value by loop in a Variable
								select JSON_LENGTH(lj_Details, CONCAT('$.ASSET[0].MergeHeader_Gid')) into @MergeHeader_Gid_Count;

											if @MergeHeader_Gid_Count is null or @MergeHeader_Gid_Count = 0 or @MergeHeader_Gid_Count = '' then
													set Message = 'Asset Merge Header Gid Is Needed.';
													leave sp_FAAssertProcess_Set;
											End if;
								set i = 0 ;
									While i <= @MergeHeader_Gid_Count - 1 DO

											select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].MergeHeader_Gid[',i,']'))) into @MergeHeader_Gid;
											#SELECT @MergeHeader_Gid;
											if @MergeHeader_Gid <> 0 then

												if @ls_Status = 'APPROVED' then

												    ### Get The Merge Source Gids.
                                                        set @asset_merge_src_gids = 0;
														Select ifnull(group_concat(c.assetdetails_mainassetdetailsgid),0) into @asset_merge_src_gids
														from fa_trn_tassetmergeheader as a
														inner join fa_trn_tassetmerge as b on b.assetmerge_assetmergeheader_gid = a.assetmergeheader_gid
														inner join fa_tmp_tassetdetails as c on c.assetdetails_id = b.assetmerge_assetdetailsid
														where a.assetmergeheader_gid = @MergeHeader_Gid
														and a.assetmergeheader_isactive = 'Y' and a.assetmergeheader_isremoved = 'N'
														and a.entity_gid = @Entity_Gid
														and b.assetmerge_isactive = 'Y' and b.assetmerge_isremoved = 'N'
														and c.assetdetails_isactive = 'Y' and c.assetdetails_isremoved = 'N';

                                                        if @asset_merge_src_gids = 0 then
                                                          set Message = 'No Asset Merge Source Data.';
                                                          ROLLBACK;
                                                          leave sp_FAAssertProcess_Set;
                                                        End if;


													#### Call the Sp to Insert Teh Asset data from TMP table
													set @lj_Details_Data = '';
													set @lj_Details_Data = concat(
															'{"Merge_Gid":"',@MergeHeader_Gid,'",
															  "Merge_Status":"APPROVED",
                                                              "Trn_Ref_Name":"FA_MERGE",
															  "Trn_To_Type":"C",
															  "Trn_Role_Name":"CHECKER",
															  "Trn_Remarks":"APPROVE"
															 }'                  );
																			#select @lj_Details_Data;
													call sp_FAMerge_Set('UPDATE','MERGE_CHECKER','UPDATE',
														@lj_Details_Data,lj_Classification,ls_Createby,@Message);
														select @Message into @Out_Msg_Merge;
														#select @Out_Msg_Merge;
														if @Out_Msg_Merge = 'SUCCESS' then
																set Message = 'SUCCESS';
														elseif @Out_Msg_Merge is null or @Out_Msg_Merge <> 'SUCCESS' then
																set Message = concat('FAIL ',@Out_Msg_Merge);
															 ROLLBACK;
                                                             leave sp_FAAssertProcess_Set;
														End if;


                                                        ### Affect In Main Table.
                                                                            ##### Update The Main Table.

                                                                select @asset_merge_src_gids;
                                                                select @MergeHeader_Gid;

																	set @lj_Merge_Data = '';
                                                                    set @lj_Merge_Data = concat('{"Asset_Detail_Gids":"',@asset_merge_src_gids,'",
																			 "RequestFor":"SUCCESS",
																			 "Merge_Gid":"',@MergeHeader_Gid,'"
																			}');

                                                                   # select @lj_Merge_Data;
																	call sp_FAAsset_Set('UPDATE', 'ASSET_CHECKER','REQUEST_FOR',
                                                                    @lj_Merge_Data,'{}',lj_Classification,ls_Createby,@Message);
                                                                    set @Out_Msg_Merge = '';
																	select @Message   into @Out_Msg_Merge;

                                                                    if @Out_Msg_Merge <> 'SUCCESS' then
																			set Message = Concat('FAILs',@Out_Msg_Merge);
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                     elseif @Out_Msg_Merge is null then
                                                                          set Message = Concat('FAIL In Merge Transaction Update. ');
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                    End if;



												Elseif @ls_Status = 'REJECTED' then

													select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,CONCAT('$.Remark'))) into @ls_Remark;

													set @lj_Details_Data = '';
													set @lj_Details_Data = concat(
														'{"Merge_Gid":"',@MergeHeader_Gid,'",
														  "Merge_Status":"REJECTED",
														  "Remark":"',@ls_Remark,'",
                                                          "Trn_Ref_Name":"FA_MERGE",
														  "Trn_To_Type":"C",
														  "Trn_Role_Name":"CHECKER",
														  "Trn_Remarks":"REJECT"
														  }'                  );
													#select  @lj_Details_Data;

													call sp_FAMerge_Set('UPDATE','MERGE_CHECKER','UPDATE',
															@lj_Details_Data,lj_Classification,ls_Createby,@Message);
															set @Out_Msg_Merge='';
															select @Message into @Out_Msg_Merge;

															#select   @Out_Msg_Merge;

														if @Out_Msg_Merge = 'SUCCESS' then
																	set Message = 'SUCCESS';
														elseif @Out_Msg_Merge is null or @Out_Msg_Merge <> 'SUCCESS' then
																	set Message = concat('FAIL ',@Out_Msg_Merge);
														End if;

											End if;


										end if;

									set i = i+1;
								End while;

           End if;

elseif ls_Type = 'ASSET_SPLIT' and ls_Sub_Type = 'CHECKER' then
              #####Transfer Checker :: Approve or Reject
              if ls_Action = 'UPDATE' then

					select JSON_LENGTH(lj_Details,'$') into @li_Detailjson_count;
					if @li_Detailjson_count is null or @li_Detailjson_count = 0 then
							set Message = 'No Data In Json - Asset Details.';
                            leave sp_FAAssertProcess_Set;
					end if;

					select JSON_LENGTH(lj_Status,'$') into @li_Statusjson_count;
					if @li_Statusjson_count is null or @li_Statusjson_count = 0 then
							set Message = 'No Data In Json - Asset Status.';
                            leave sp_FAAssertProcess_Set;
					end if;

                        select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,CONCAT('$.Status'))) into @ls_Status;

                        if @ls_Status is null or @ls_Status = '' then
								set Message = 'Status Is Needed.';
                                leave sp_FAAssertProcess_Set;
                        End if;

                        #### Get The Value by loop in a Variable
                        select JSON_LENGTH(lj_Details, CONCAT('$.ASSET[0].SplitHeader_Gid')) into @SplitHeader_Gid_Count;

									if @SplitHeader_Gid_Count is null or @SplitHeader_Gid_Count = 0 or @SplitHeader_Gid_Count = '' then
											set Message = 'Asset Split Header Gid Is Needed.';
											leave sp_FAAssertProcess_Set;
									End if;
                        set i = 0 ;
								While i <= @SplitHeader_Gid_Count - 1 DO

										select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].SplitHeader_Gid[',i,']'))) into @SplitHeader_Gid;

										if @SplitHeader_Gid <> 0 then

                                               ##### Get The Asset Id to Update teh Split header Id.
																	set @asset_split_new_gids = 0 ;
																	Select group_concat(distinct c.assetdetails_mainassetdetailsgid) into @asset_split_new_gids
																	 from fa_trn_tassetsplitheader as a
																	inner join fa_trn_tassetsplit as b on b.assetsplit_assetsplitheader_gid = a.assetsplitheader_gid
																	inner join fa_tmp_tassetdetails as c on c.assetdetails_id	 = b.assetsplit_newassetdetailsid
																	where a.assetsplitheader_gid = @SplitHeader_Gid
																	and a.assetsplitheader_isactive = 'Y' and a.assetsplitheader_isremoved = 'N'
																	and a.entity_gid = @Entity_Gid
																	and b.assetsplit_isactive = 'Y' and b.assetsplit_isremoved = 'N'
																	and c.assetdetails_isactive = 'Y' and c.assetdetails_isremoved = 'N'
                                                                    ;


																   #select @asset_split_new_gids;
																   if @asset_split_new_gids =0 or @asset_split_new_gids is null then
																		set Message = 'Asset Split Data Is Needed.';
																		rollback;
																		leave sp_FAAssertProcess_Set;
																   End if;

												if @ls_Status = 'APPROVED' then
																#### Call the Sp to Insert Teh Asset data from TMP table
																		set @lj_Details_Data = '';
																		set @lj_Details_Data = concat(
																				'{"Split_Gid":"',@SplitHeader_Gid,'",
																				  "Split_Status":"APPROVED",
																				  "Trn_To_Type":"C",
																				  "Trn_Role_Name":"CHECKER",
																				  "Trn_Remarks":"APPROVE",
																				  "Trn_Ref_Name":"FA_SPLIT"
																				  }'                  );
																									#select @lj_Details_Data;
																call sp_FASplit_Set('UPDATE','ASSET_SPLIT','CHECKER',
																		 @lj_Details_Data,lj_Classification,ls_Createby,@Last_Id,@Message);
																		set  @Out_Msg_Split='';
																		select @Message into @Out_Msg_Split;
																#select @Out_Msg_Merge;
																	if @Out_Msg_Split = 'SUCCESS' then
																				set Message = 'SUCCESS';
																			elseif @Out_Msg_Split is null or @Out_Msg_Split <> 'SUCCESS' then
																				set Message = concat('FAIL ',@Out_Msg_Split);
																	End if;


                                                               ### Affect In Main Table.
                                                                            ##### Update The Main Table.
																	set @lj_Split_Data = '';
                                                                    set @lj_Split_Data =
                                                                    concat('{
                                                                    "Asset_Detail_Gids":"',@asset_split_new_gids,'",
                                                                    "RequestFor":"SUCCESS",
                                                                    "Split_Gid":"',@SplitHeader_Gid,'",
																	"Trn_To_Type":"C",
																	"Trn_Role_Name":"CHECKER",
																	"Trn_Remarks":"REJECT",
																	"Trn_Ref_Name":"FA_SPLIT"
                                                                    }');
                                                                    #select @lj_Split_Data;
                                                                    #select @asset_split_new_gids,@SplitHeader_Gid,@Entity_Gid;
                                                                    #select @lj_CapDate_Data;
																	call sp_FAAsset_Set('UPDATE', 'ASSET_CHECKER',
																	'REQUEST_FOR',
                                                                    @lj_Split_Data,'{}',lj_Classification,ls_Createby,@Message);
                                                                    set @Out_Msg_Split = '';
																	select @Message   into @Out_Msg_Split;

                                                                    if @Out_Msg_Split <> 'SUCCESS' then

																			set Message = Concat('FAIL - ',@Out_Msg_Split);
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                     elseif @Out_Msg_Split is null then
                                                                          set Message = Concat('FAIL In Merge Transaction Update. ');
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                    End if;




												Elseif @ls_Status = 'REJECTED' then

																	select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,CONCAT('$.Remark'))) into @ls_Remark;


																	set @lj_Details_Data = '';
																		set @lj_Details_Data = concat(
																				'{"Split_Gid":"',@SplitHeader_Gid,'",
																				  "Split_Status":"REJECTED",
																				  "Remark":"',@ls_Remark,'",
                                                                                  "Asset_Detail_Gids":"',@asset_split_new_gids,'",
                                                                                  "Trn_To_Type":"C",
																				  "Trn_Role_Name":"CHECKER",
																				  "Trn_Remarks":"REJECT",
																				  "Trn_Ref_Name":"FA_SPLIT"
																				  }'                  );

																#select @lj_Details_Data;

																	call sp_FASplit_Set('UPDATE','ASSET_SPLIT','CHECKER',
																		 @lj_Details_Data,lj_Classification,ls_Createby,@Last_Id,@Message);
																	set @Out_Msg_Split='';
																	select @Message into @Out_Msg_Split;

																	if @Out_Msg_Split = 'SUCCESS' then
																				set Message = 'SUCCESS';
																			elseif @Out_Msg_Split is null or @Out_Msg_Split <> 'SUCCESS' then
																				set Message = concat('FAIL ',@Out_Msg_Split);
																	End if;

												  End if;#APPROVED,REJECTED End if

							end if;

								set i = i+1;
								End while;

           End if;

elseif ls_Type = 'ASSET_SALE' and ls_Sub_Type = 'CHECKER' then
              #####Sale Checker :: Approve or Reject
              if ls_Action = 'UPDATE' then

					select JSON_LENGTH(lj_Details,'$') into @li_Detailjson_count;
					if @li_Detailjson_count is null or @li_Detailjson_count = 0 then
							set Message = 'No Data In Json - Asset Details.';
                            leave sp_FAAssertProcess_Set;
					end if;

					select JSON_LENGTH(lj_Status,'$') into @li_Statusjson_count;
					if @li_Statusjson_count is null or @li_Statusjson_count = 0 then
							set Message = 'No Data In Json - Asset Status.';
                            leave sp_FAAssertProcess_Set;
					end if;

                        select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,CONCAT('$.Status'))) into @ls_Status;

                        if @ls_Status is null or @ls_Status = '' then
								set Message = 'Status Is Needed.';
                                leave sp_FAAssertProcess_Set;
                        End if;

                        #### Get The Value by loop in a Variable
                        select JSON_LENGTH(lj_Details, CONCAT('$.ASSET[0].SaleHeader_Gid')) into @SaleHeader_Gid_Count;

									if @SaleHeader_Gid_Count is null or @SaleHeader_Gid_Count = 0 or @SaleHeader_Gid_Count = '' then
											set Message = 'Asset Sale Header Gid Is Needed.';
											leave sp_FAAssertProcess_Set;
									End if;

					  #### Billing State.
					  select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].State_Billing_From_Gid'))) into @State_Billing_From_Gid;

					   if @State_Billing_From_Gid is null or @State_Billing_From_Gid = 0 THEN
					     set Message  = 'State Billing From Gid Is Needed.';
					     leave sp_FAAssertProcess_Set;
					   End if;


                        set i = 0 ;
								While i <= @SaleHeader_Gid_Count - 1 DO

										select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].SaleHeader_Gid[',i,']'))) into @SaleHeader_Gid;

										if @SaleHeader_Gid is null or @SaleHeader_Gid = 0 then
											set Message = 'SO Header Gid Is Needed. ';
										    leave sp_FAAssertProcess_Set;
										End if;


												if @ls_Status = 'APPROVED' then

									              ##### Insert For SO header
                                             	  	select  a.assetsaleheader_customergid,a.assetsaleheader_saledate,
													a.assetsaleheader_saletotalamount,a.assetsaleheader_remarks
													into @Sale_Customer_Gid,@Sale_Date,@Sale_Tot_Amount,@Sale_Remarks
													from fa_trn_tassetsaleheader as a
													where a.assetsaleheader_gid = @SaleHeader_Gid  and a.assetsaleheader_isactive = 'Y' and a.assetsaleheader_isremoved = 'N';

													### Validations  TO DO
                                                 #   select @Sale_Customer_Gid;
                                                    ### On Approve - SO Detail
													Select concat('[',group_concat(distinct JSON_OBJECT('Product_Gid',c.assetdetails_productgid,
													'Sale_Rate',b.assetsale_value,'HSN_Code',b.assetsale_hsncode,'SGST_Rate',b.assetsale_sgst,'CGST_Rate',b.assetsale_cgst,
													'IGST_Rate',b.assetsale_igst
													)),']')  into @lj_pdct from fa_trn_tassetsaleheader as a
													inner join fa_trn_tassetsale as b on b.assetsale_assetsaleheadergid = a.assetsaleheader_gid
													inner join fa_tmp_tassetdetails as c on c.assetdetails_id = b.assetsale_assetdetailsid
													where a.assetsaleheader_gid = @SaleHeader_Gid
													#group by b.assetsale_value
													;


																	### Frame The Data - SO Header and Detail
															set @lj_Sale_Details = '';
															set @lj_Sale_Details = concat('
															{
															"Customer_Gid":"',@Sale_Customer_Gid,'",
                                                            "Sale_Date":"',@Sale_Date,'",
															"PRODUCT":',@lj_pdct,',
                                                            "Asset_Sale_Header_Gid":"',@SaleHeader_Gid,'"
															}
															');


                                                            call sp_FASale_Set('','FAASSET_SALE','SO_HEADER',@lj_Sale_Details,lj_Classification,ls_Createby,@last_id,@Message);
                                                            select @Message into @Out_Msg_SaleSO;
                                                           select @last_id into @Out_Msg_SOHeader_Gid;


                                                           		Select concat('[',group_concat(JSON_OBJECT('asset_soheader_gid',a.soheader_gid,'inv_pdct_gid',b.sodetails_product_gid,
																'inv_sale_rate',b.sodetails_unitprice,'Product_Qty',b.sodetails_qty,'HSN_Code',b.sodetails_hsncode,
																'SGST_Rate',b.sodetails_sgst,'CGST_Rate',b.sodetails_cgst,'IGST_Rate',b.sodetails_igst
																)),']')  into  @lj_sodetails from gal_trn_tsoheader as a
																inner join gal_trn_tsodetails as b on b.sodetails_soheader_gid = a.soheader_gid
																where a.soheader_gid = @Out_Msg_SOHeader_Gid;



                                                              set @lj_Invoice_Details = '';
                                                              set @lj_Invoice_Details = concat('
                                                              {"Customer_Gid":"',@Sale_Customer_Gid,'",
                                                                 "InvoiceHeader_Date":"',@Sale_Date,'",
                                                                 "PRODUCT":',@lj_sodetails,',
                                                                 "Inv_Total":"',@Sale_Tot_Amount,'",
                                                                 "Remarks":"',@Sale_Remarks,'",
                                                                 "State_Billing_From_Gid":"',@State_Billing_From_Gid,'"
                                                              }
                                                              ');

                                                               call sp_FASale_Set('INSERT','INVOICE_HEADER_MAKER','INVOICE_HEADER',
                                                               @lj_Invoice_Details,lj_Classification,ls_Createby,@last_id,@Message);
                                                            select @Message into @Out_Msg_SaleInv;

                                                            #select @Out_Msg_SaleInv;
                                                            #select @lj_Invoice_Details;
                                                            set @LastId_Inv_header = 0;

                                                           if @Out_Msg_SaleInv = 'SUCCESS' THEN
                                                           		set Message = 'SUCCESS';
                                                           	select @last_id into @LastId_Inv_header;
                                                           elseif @Out_Msg_SaleInv is null then
                                                              set Message = 'FAIL In Invoice Save';
                                                              ROLLBACK;
                                                              leave sp_FAAssertProcess_Set;
                                                            else
                                                                set Message = concat('Fail In invoice Header -',@Out_Msg_SaleInv);
                                                                rollback;
                                                                leave sp_FAAssertProcess_Set;
                                                           End if;


                                                          if @LastId_Inv_header is null or @LastId_Inv_header = 0 THEN
                                                              set Message = 'Error In Last Invoice Data.';
                                                              ROLLBACK;
                                                             leave sp_FAAssertProcess_Set;
                                                          End if;

                                                         Update fa_trn_tassetsaleheader set assetsaleheader_invoiceheadergid = @LastId_Inv_header
                                                         where assetsaleheader_gid = @SaleHeader_Gid;

                                                        	set countRow = (select ROW_COUNT());

                                                        if countRow = 0 THEN
                                                           set Message ='Error On FA Sale Update.';
                                                           ROLLBACK;
                                                          leave sp_FAAssertProcess_Set;
                                                        End if;

                                                          ### SO Inv Map Save

                                                          ### Bala


										select CONCAT('[',group_concat(JSON_OBJECT('SO_Header_Gid',@Out_Msg_SOHeader_Gid,
													'SO_Details_Gid',b.sodetails_gid,'Invoice_header_Gid',@last_id)),']')
                                                    into @SO_DATA_LIST from gal_trn_tsoheader a
													inner join gal_trn_tsodetails b on b.sodetails_soheader_gid=a.soheader_gid
													where soheader_gid=@Out_Msg_SOHeader_Gid;

                                                          set @lj_Details='';
                                                          set @lj_Details=concat('{
                                                                 "SO_DATA":',@SO_DATA_LIST,'
																				  }');

														#select @lj_Details;

												call sp_FASale_Set('INSERT', 'SO_INVOICE_MAKER', 'SO_INVOICE',@lj_Details ,
																	lj_Classification,ls_Createby, @li_Last_Id, @Message);
												select  @Message into  @Out_Msg_So_Inv;

                                                		 if @Out_Msg_So_Inv = 'SUCCESS' THEN
                                                           		set Message = 'SUCCESS';
                                                           elseif @Out_Msg_So_Inv is null then
                                                              set Message = 'FAIL In So_Inv Save';
                                                              ROLLBACK;
                                                              leave sp_FAAssertProcess_Set;
                                                           End if;




                                                          #select @SaleHeader_Gid,@Entity_Gid;
                                                          #leave sp_FAAssertProcess_Set;


												Elseif @ls_Status = 'REJECTEDXXXX' then
                            											### To DO
																	select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,CONCAT('$.Remark'))) into @ls_Remark;


																	set @lj_Details_Data = '';
																		set @lj_Details_Data = concat(
																				'{"Split_Gid":"',@SplitHeader_Gid,'",
																				  "Split_Status":"REJECTED",
																				  "Remark":"',@ls_Remark,'",
                                                                                  "Trn_To_Type":"C",
																				  "Trn_Role_Name":"CHECKER",
																				  "Trn_Remarks":"REJECT",
																				  "Trn_Ref_Name":"FA_SPLIT"
																				  }'                  );

																#select @lj_Details_Data;

																	call sp_FASplit_Set('UPDATE','ASSET_SPLIT','CHECKER',
																		 @lj_Details_Data,lj_Classification,ls_Createby,@Last_Id,@Message);
																	set @Out_Msg_Split='';
																	select @Message into @Out_Msg_Split;

																	if @Out_Msg_Split = 'SUCCESS' then
																				set Message = 'SUCCESS';
																	elseif @Out_Msg_Split is null or @Out_Msg_Split <> 'SUCCESS' then
																				set Message = concat('FAIL ',@Out_Msg_Split);
																	End if;

												  End if;#APPROVED,REJECTED End if

												  if @ls_Status = 'APPROVED' or @ls_Status = 'REJECTED' THEN

												          Select group_concat(c.assetdetails_mainassetdetailsgid) into @assetSale_Gids from fa_trn_tassetsaleheader as a
															inner join fa_trn_tassetsale as b on b.assetsale_assetsaleheadergid = a.assetsaleheader_gid
															inner join fa_tmp_tassetdetails as c on c.assetdetails_id = b.assetsale_assetdetailsid
															where a.assetsaleheader_gid = @SaleHeader_Gid and a.assetsaleheader_isactive = 'Y' and a.assetsaleheader_isremoved = 'N'
															and b.assetsale_isactive = 'Y' and b.assetsale_isremoved = 'N' and c.assetdetails_isactive = 'Y' and c.assetdetails_isremoved = 'N'
															and a.entity_gid = @Entity_Gid
															;
                                                               ### Affect In Main Table.
                                                                            ##### Update The Main Table.


                                                                   if @ls_Status = 'APPROVED' THEN
                                                                       	set @lj_Sale_Data = '';
                                                                    set @lj_Sale_Data =
                                                                    concat('{
                                                                    "Asset_Detail_Gids":"',@assetSale_Gids,'",
                                                                    "RequestFor":"SUCCESS",
                                                                    "Sale_Gid":"',@SaleHeader_Gid,'"

                                                                    }');

                                                                   set @Tran_Remarks = 'APPROVE';

                                                                   ELSEIF @ls_Status = 'REJECTED' THEN
                                                                      	set @lj_Sale_Data = '';
                                                                    set @lj_Sale_Data =
                                                                    concat('{
                                                                    "Asset_Detail_Gids":"',@assetSale_Gids,'",
                                                                    "RequestFor":"SUCCESS"
                                                                    }');

                                                                    set @Tran_Remarks = @ls_Remark; ### Ita a Tran remark

                                                                   End if;

                                                                   call sp_FAAsset_Set('UPDATE', 'ASSET_CHECKER',
																	'REQUEST_FOR',
                                                                    @lj_Sale_Data,'{}',lj_Classification,ls_Createby,@Message);
                                                                    set @Out_Msg_Sale = '';
																	select @Message   into @Out_Msg_Sale;

                                                                    #select @Out_Msg_Sale;
                                                                    #select @assetSale_Gids;

                                                                    if @Out_Msg_Sale <> 'SUCCESS' then
																			set Message = Concat('FAIL - ',@Out_Msg_Sale);
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                     elseif @Out_Msg_Sale is null then
                                                                          set Message = Concat('FAIL In Sale Transaction Update. ');
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                    End if;

                                                                   set Query_Update = '';
                                                                   set Query_Update = concat('delete from fa_tmp_tassetdetails where assetdetails_mainassetdetailsgid in (',@assetSale_Gids,')');

                                                                  set @Update_query = '';
                                                                  set @Update_query = Query_Update;
																	#SELECT @Update_query;
																	PREPARE stmt FROM @Update_query;
																	EXECUTE stmt;
																	set countRow = (select ROW_COUNT());
																	DEALLOCATE PREPARE stmt;

																if countRow > 0 THEN
																	set Message = 'SUCCESS';
																ELSE
																    set Message = 'FAIL';
																    ROLLBACK;
																    leave sp_FAAssertProcess_Set;
																End if;

															#### Update The Sale Header Table
															 set @lj_UpdateDetails = '';
															 set @lj_UpdateDetails = concat('{
 																	"AssetSale_Header_Gid":"',@SaleHeader_Gid,'",
																	"AssetSale_Status":"',@ls_Status,'"
                                                                       }');

															 	call sp_FASale_Set('UPDATE', 'ASSET_SALE_UPDATE', 'PROCESS',@lj_UpdateDetails ,
																	lj_Classification,ls_Createby, @li_Last_Id, @Message);
																select  @Message into  @Out_Msg_FASale_Update;



                                                		 if @Out_Msg_FASale_Update = 'SUCCESS' THEN
                                                           		set Message = 'SUCCESS';
                                                         elseif @Out_Msg_FASale_Update is null then
                                                              set Message = 'FAIL In FA Sale Update.';
                                                              ROLLBACK;
                                                              leave sp_FAAssertProcess_Set;
                                                         ELSEIF @Out_Msg_FASale_Update <> 'SUCCESS' THEN
                                                            set Message = concat('Error Occured. - ',@Out_Msg_FASale_Update);
                                                            ROLLBACK;
                                                            leave sp_FAAssertProcess_Set;
                                                           End if;


															#### Tran Update

															  call sp_Trans_Set('update','FA_SALE',@SaleHeader_Gid,
																		 @ls_Status,'G', 'CHECKER',
								                                         @Tran_Remarks,@Entity_Gid,ls_Createby, @Message);
																	select @Message into @out_msg_tran;

												                    #select @out_msg_tran;

																if @out_msg_tran > 0  then
												                     set Message = 'SUCCESS';
												                  elseif @out_msg_tran <= 0 then
												                    set Message = concat('Fail On Tran Update. ',@out_msg_tran);
												                    rollback;
																	leave sp_FAAssertProcess_Set;
																End if;


												  End if;



								set i = i+1;
								End while;

           End if;

elseif ls_Type = 'ASSET_VALUE' and ls_Sub_Type = 'CHECKER' then
              #####Transfer Checker :: Approve or Reject
              if ls_Action = 'UPDATE' then

					select JSON_LENGTH(lj_Details,'$') into @li_Detailjson_count;
					if @li_Detailjson_count is null or @li_Detailjson_count = 0 then
							set Message = 'No Data In Json - Asset Details.';
                            leave sp_FAAssertProcess_Set;
					end if;

					select JSON_LENGTH(lj_Status,'$') into @li_Statusjson_count;
					if @li_Statusjson_count is null or @li_Statusjson_count = 0 then
							set Message = 'No Data In Json - Asset Status.';
                            leave sp_FAAssertProcess_Set;
					end if;

                        select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,CONCAT('$.Status'))) into @ls_Status;
#                       select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,CONCAT('$.Remark'))) into @ls_Remark

                        if @ls_Status is null or @ls_Status = '' then
								set Message = 'Status Is Needed.';
                                leave sp_FAAssertProcess_Set;
                        End if;



                        #### Get The Value by loop in a Variable
                        select JSON_LENGTH(lj_Details, CONCAT('$.ASSET[0].Asset_Gid')) into @Asset_Gid_Count;

									if @Asset_Gid_Count is null or @Asset_Gid_Count = 0 or @Asset_Gid_Count = '' then
											set Message = 'Asset  Gid Is Needed.';
											leave sp_FAAssertProcess_Set;
									End if;
								set i = 0 ;
								While i <= @Asset_Gid_Count - 1 DO

											select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].Asset_Gid[',i,']'))) into @AssetDetails_Gid;

											if @AssetDetails_Gid <> 0 then

											                       set @assetdetails_Trngid = 0;
											                       set @Asset_Value_New = 0;
																	Select b.assetdetails_gid,a.assetdetails_value,date_format(b.assetdetails_capdate,'%Y-%m-%d')
																	into @assetdetails_Trngid,@Asset_Value_new,@asset_cp_date
                                                                    from fa_tmp_tassetdetails as a
																	inner join fa_trn_tassetdetails as b on b.assetdetails_id = a.assetdetails_id
																	where a.assetdetails_isactive = 'Y' and a.assetdetails_isremoved = 'N'
																	and b.assetdetails_isactive = 'Y' and b.assetdetails_isremoved = 'N'
																	and a.entity_gid = @Entity_Gid
																	and a.assetdetails_gid = @AssetDetails_Gid;

                                                                    if @assetdetails_Trngid = 0 then
																			set Message = 'Error On Asset Transaction Data.';
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                    End if;

                                                            set @Asset_Value_Gid = 0;
															Select ifnull(b.assetvalue_gid,0) into @Asset_Value_Gid from fa_tmp_tassetdetails as a
															inner join fa_trn_tassetvalue as b on b.assetvalue_assetdetailsid = a.assetdetails_id
															where a.assetdetails_isactive = 'Y' and a.assetdetails_isremoved = 'N'
															and b.assetvalue_isactive = 'Y' and b.assetvalue_isremoved = 'N'
                                                            and a.assetdetails_gid = @AssetDetails_Gid;


                                                            if @WriteOff_Gid = 0 then
																set Message = 'Error On Value Data';
                                                                rollback;
                                                                leave sp_FAAssertProcess_Set;
                                                            End if;


									if @ls_Status = 'APPROVED' then

											#### Call the Sp to Insert Teh Asset data from TMP table
												set @lj_Details_Data = '';
												set @lj_Details_Data = concat(
														'{"Asset_Value_Gid":"',@Asset_Value_Gid,'",
														  "Asset_Value_Status":"',@ls_Status,'",
                                                           "Asset_Detail_Gids":"',@AssetDetails_Gid,'"
														 }'                  );
																			#select @lj_Details_Data;
											call sp_FA_Value_Set('UPDATE','VALUE_CHECKER','CHECKER',
												 @lj_Details_Data,lj_Classification,ls_Createby,@Message);
                                                set  @Out_Msg_Value='';
												select @Message into @Out_Msg_Value;
										   #select @Out_Msg_Merge;
											if @Out_Msg_Value = 'SUCCESS' then
														set Message = 'SUCCESS';
											elseif @Out_Msg_Value is null or @Out_Msg_Value <> 'SUCCESS' then
														set Message = concat('FAIL ',@Out_Msg_Value);
											End if;

                              			#### Call the Sp to Insert Teh Asset data from TMP table
											set @lj_Details_Data = '';
											set @lj_Details_Data = concat(
																  '{"Asset_Detail_Gids":"',@assetdetails_Trngid,'",
																    "Status":"APPROVED",
																    "Request_For":"SUCCESS",
                                                                    "Trn_Process_Gid":"',@Asset_Value_Gid,'",
                                                                    "Trn_Process_Staus":"APPROVED",
																	"Trn_Ref_Name":"FA_VALUE",
																	"Trn_To_Type":"C",
																	"Trn_Role_Name":"CHECKER",
																	"Trn_Remarks":"APPROVE "
																	}'    );
										#select @lj_Details_Data;
									call sp_FAAsset_Set('UPDATE','ASSET_PROCESS_CHECKER','APPROVE',@lj_Details_Data,
														'{}',lj_Classification,ls_Createby,@Message);
                                        set @Out_Msg_Asset='';
										select @Message into @Out_Msg_Asset;
										#select @Out_Msg_Asset;
													if @Out_Msg_Asset = 'SUCCESS' then
														set Message = 'SUCCESS';
													elseif @Out_Msg_Asset is null or @Out_Msg_Asset <> 'SUCCESS' then
														set Message = concat('FAIL ',@Out_Msg_Asset);
													    rollback;
														leave sp_FAAssertProcess_Set;
													End if;

															### Affect In Main Table.
                                                                            ##### Update The Main Table.
																	set @lj_Value_Data = '';
                                                                    set @lj_Value_Data =
                                                                    concat('{
                                                                    "Asset_Detail_Gids":"',@assetdetails_Trngid,'",
                                                                    "RequestFor":"SUCCESS",
                                                                    "Asset_Value_Gid":"',@Asset_Value_Gid,'",
																	"Asset_Value_New":"',@Asset_Value_New,'"
                                                                    }');

																	call sp_FAAsset_Set('UPDATE', 'ASSET_CHECKER',
																	'REQUEST_FOR',
                                                                    @lj_Value_Data,'{}',lj_Classification,ls_Createby,@Message);
                                                                    set @Out_Msg_Value = '';
																	select @Message   into @Out_Msg_Value;

																#select @Out_Msg_Value;

                                                                    if @Out_Msg_Value <> 'SUCCESS' then
																			set Message = Concat('FAIL',@Out_Msg_Value);
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                     elseif @Out_Msg_Value is null then
                                                                          set Message = Concat('FAIL In Value  Transaction Update. ');
                                                                            rollback;
                                                                            leave sp_FAAssertProcess_Set;
                                                                    End if;

                                                 #### Calculate The Depreciation.
                                                                    ### delete The Depreciation if Exists.

                                                                   set @Depreciation_OldGids = 0;
                                                                   select ifnull(group_concat(depreciation_gid),0) into @Depreciation_OldGids
                                                                   from fa_trn_tdepreciation where depreciation_assetdetailsgid = @assetdetails_Trngid
                                                                   and depreciation_isactive = 'Y' and depreciation_isremoved = 'N' and depreciation_type = 1
                                                                   and entity_gid = @Entity_Gid;

                                                                   if @Depreciation_OldGids <> 0 THEN
                                                                       select @Depreciation_OldGids;
                                                                       set @lj_depreciation_data = '';
                                                                       set @lj_depreciation_data = concat('{
																				"Depreciation_Gid":"',@Depreciation_OldGids,'"
                                                                             }');

                                                                       call sp_FADepreciation_Set('UPDATE', 'DEPRECIATION', 'FLAG', @lj_depreciation_data, '{}', lj_Classification, ls_Createby,@Message);
                                                                        select @Message into @Out_Msg_Depreciation;

                                                                       if @Out_Msg_Depreciation <> 'SUCCESS' THEN
                                                                          set Message = CONCAT('Error On Old Depreciation Delete. - ',@Out_Msg_Depreciation);
                                                                          ROLLBACK;
                                                                          leave sp_FAAssertProcess_Set;
                                                                        ELSEIF @Out_Msg_Depreciation is null THEN
                                                                          set Message = 'Error On Old Depreciation Delete.';
                                                                          ROLLBACK;
                                                                          leave sp_FAAssertProcess_Set;
                                                                         ELSEIF @Out_Msg_Depreciation = 'SUCCESS' THEN
                                                                           set Message = 'SUCCESS';
                                                                       End if;


                                                                      ### Calculate Depreciation
                                                                      select date_format(now(),'%Y-%m-%d') into @Cur_Date ;

                                                                       set @lj_depreciation_data = '';
                                                                       set @lj_depreciation_data = concat('{
																				"Asset_Gids":"',@assetdetails_Trngid,'",
                                                                                "From_Date":"',@asset_cp_date,'",
 																				"To_Date":"',@Cur_Date,'"
                                                                             }');

                                                                       call sp_FADepreciation_Set('INSERT', 'DEPRECATION', 'SINGLEPROCESS', @lj_depreciation_data, '{}', lj_Classification, ls_Createby,@Message);
                                                                        select @Message into @Out_Msg_Depreciation;

                                                                       if @Out_Msg_Depreciation <> 'SUCCESS' THEN
                                                                          set Message = CONCAT('Error On Old Depreciation Calculate. - ',@Out_Msg_Depreciation);
                                                                          ROLLBACK;
                                                                          leave sp_FAAssertProcess_Set;
                                                                        ELSEIF @Out_Msg_Depreciation is null THEN
                                                                          set Message = 'Error On Old Depreciation Delete.';
                                                                          ROLLBACK;
                                                                          leave sp_FAAssertProcess_Set;
                                                                        ELSEIF @Out_Msg_Depreciation = 'SUCCESS' THEN
                                                                           set Message = 'SUCCESS';
                                                                       End if;


                                                                   End if;



						Elseif @ls_Status = 'REJECTED' then

								select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,CONCAT('$.Remark'))) into @ls_Remark;

							    if @ls_Remark is null or @ls_Remark = '' THEN
							       set Message = 'Reject Remark Is Needed.';
							      rollback;
							       leave sp_FAAssertProcess_Set;
							    End if;


									set @lj_Details_Data = '';
												set @lj_Details_Data = concat(
														'{"Asset_Value_Gid":"',@Asset_Value_Gid,'",
														  "Asset_Value_Status":"',@ls_Status,'",
                                                          "Asset_Detail_Gids":"',@AssetDetails_Gid,'"

														 }'                  );
																			#select @lj_Details_Data;
									call sp_FA_Value_Set('UPDATE','VALUE_CHECKER','CHECKER',
												 @lj_Details_Data,lj_Classification,ls_Createby,@Message);
                                                set  @Out_Msg_Value='';
												select @Message into @Out_Msg_Value;

											if @Out_Msg_Value = 'SUCCESS' then
														set Message = 'SUCCESS';
													elseif @Out_Msg_Value is null or @Out_Msg_Value <> 'SUCCESS' then
														set Message = concat('FAIL In Asset Value ',@Out_Msg_Value);
													   ROLLBACK;
														leave sp_FAAssertProcess_Set;
											End if;




                                            set @lj_Details_Data = '';
											set @lj_Details_Data = concat(
																  '{"Asset_Detail_Gids":"',@AssetDetails_Gid,'",
                                                                    "Asset_Trn_Gids" : "',@assetdetails_Trngid,'",
																    "Status":"REJECTED",
																    "Request_For":"SUCCESS",
                                                                    "Remark":"',@ls_Remark,'",
                                                                    "Trn_Process_Gid":"',@Asset_Value_Gid,'",
                                                                    "Trn_Process_Staus":"REJECTED",
																	"Trn_Ref_Name":"FA_VALUE",
																	"Trn_To_Type":"C",
																	"Trn_Role_Name":"CHECKER",
																	"Trn_Remarks":"',@ls_Remark,'"
																	}'    );
										#select @lj_Details_Data;
									call sp_FAAsset_Set('UPDATE','ASSET_PROCESS_CHECKER','REJECT',@lj_Details_Data,
														'{}',lj_Classification,ls_Createby,@Message);
                                        set @Out_Msg_Asset='';
										select @Message into @Out_Msg_Asset;
										#select @Out_Msg_Asset;
													if @Out_Msg_Asset = 'SUCCESS' then
														set Message = 'SUCCESS';
													elseif @Out_Msg_Asset is null or @Out_Msg_Asset <> 'SUCCESS' then
														set Message = concat('FAIL ',@Out_Msg_Asset);
													    ROLLBACK;
														leave sp_FAAssertProcess_Set;
													End if;

						  End if;#APPROVED,REJECTED End if

							end if;

								set i = i+1;
								End while;

           End if;

elseif ls_Type = 'ASSET_CLUB' and ls_Sub_Type = 'TRN' then
               ### Approve or Reject The Asset - Move from Tmp Table to Tran Table
           if ls_Action = 'UPDATE' then

					select JSON_LENGTH(lj_Details,'$') into @li_Detailjson_count;
					if @li_Detailjson_count is null or @li_Detailjson_count = 0 then
							set Message = 'No Data In Json - Asset Details.';
                            leave sp_FAAssertProcess_Set;
					end if;


					select JSON_LENGTH(lj_Status,'$') into @li_Statusjson_count;
					if @li_Statusjson_count is null or @li_Statusjson_count = 0 then
							set Message = 'No Data In Json - Asset Status.';
                            leave sp_FAAssertProcess_Set;
					end if;

                        select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,CONCAT('$.Status'))) into @ls_Status;

                        if @ls_Status is null or @ls_Status = '' then
								set Message = 'Status Is Needed.';
                                leave sp_FAAssertProcess_Set;
                        End if;

                             #### Get The Value by loop in a Variable
                             select JSON_LENGTH(lj_Details, CONCAT('$.ASSET[0].Asset_Gid')) into @Asset_Gid_Count;

									if @Asset_Gid_Count is null or @Asset_Gid_Count = 0 or @Asset_Gid_Count = '' then
											set Message = 'Asset Detail Gid Is Needed.';
											leave sp_FAAssertProcess_Set;
									End if;
								set i = 0 ;
								While i <= @Asset_Gid_Count - 1 DO

										select  JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.ASSET[0].Asset_Gid[',i,']'))) into @AssetDetails_Gid;

											if @AssetDetails_Gid <> 0 then


											                #### Delete from Tmp Table
											                 set @Asset_TmpGids = 0;
											            set @qry_tmp = concat('select ifnull(group_concat(assetdetails_gid),0) into @Asset_TmpGids
														 from fa_tmp_tassetdetails
														 where assetdetails_parentgid = ',@AssetDetails_Gid,' ');

														PREPARE stmt FROM @qry_tmp;
														EXECUTE stmt;
														Select found_rows() into @li_count;

														if @Asset_TmpGids is null or @Asset_TmpGids = 0 THEN
														  set Message = 'Error On Asset Delete.';
														  ROLLBACK;
                                                          leave sp_FAAssertProcess_Set;
														End if;

											   if @ls_Status = 'REJECTED' then
													select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,CONCAT('$.Remark'))) into @ls_Remark;

													if @ls_Remark is null  or @ls_Remark = '' then
														set Message = 'Remark Is Needed For Reject.';
													   rollback;
														leave sp_FAAssertProcess_Set;
													End if;
												ELSE
												    set @ls_Remark = '';
                                                End if;


												set @lj_Details_Parent_Data = '';
												set @lj_Details_Parent_Data = concat(
																					'{"Parent_Gids":"',@AssetDetails_Gid,'",
																					  "Status":"',@ls_Status,'",
                                                                                      "Remark":"',@ls_Remark,'"
                                                                                      }'

																					 );
												#select @lj_Details_Parent_Data;

												call sp_FAAsset_Set('UPDATE', 'ASSET_CHECKER', 'PARENT',
																	@lj_Details_Parent_Data,
																	'{}', '{}',ls_Createby, @Message);
                                                             select @Message into @Out_Msg_Parent;
															   #select @Out_Msg_Parent;
																		if @Out_Msg_Parent = 'SUCCESS' then
																			set Message = 'SUCCESS';
																		elseif @Out_Msg_Parent is null or @Out_Msg_Parent <> 'SUCCESS' then
																			set Message = concat('FAIL ',@Out_Msg_Parent);
																		    rollback;
																			leave sp_FAAssertProcess_Set;
																		End if;

                                                                /*
                                                              if @ls_Status = 'APPROVED' then

																			#### Call the Sp to Insert Teh Asset data from TMP table
                                                                            #### The @AssetDetails_Gid is a Tran gid Only :: Select it  -- Nov 26 2019

                                                                               set @Asset_Detail_Tran_Gid = 0 ;
                                                                               set @query_test = concat('Select ifnull(assetdetails_mainassetdetailsgid,0) into @Asset_Detail_Tran_Gid
                                                                                from fa_tmp_tassetdetails
                                                                                where assetdetails_gid = ''',@AssetDetails_Gid,''' ');

                                                                                set @p = @query_test;
																				PREPARE stmt FROM @p;
																				EXECUTE stmt;
																				DEALLOCATE PREPARE stmt;

                                                                                if @Asset_Detail_Tran_Gid = 0 or @Asset_Detail_Tran_Gid is null then
																					set Message  = 'Problem In Getting The Asset Tran Data. ';
                                                                                    leave sp_FAAssertProcess_Set;
                                                                                End if;
                                                                                ### validation TO DO


																			set @lj_Details_Data = '';
																			set @lj_Details_Data = concat(
																			'{"Asset_Detail_Gids":"',@Asset_Detail_Tran_Gid,'",
																			   "Status":"APPROVED",
                                                                               "Request_For":"SUCCESS",
																			   "Trn_Ref_Name":"ASSET_CLUB",
																			   "Trn_To_Type":"C",
																			   "Trn_Role_Name":"CHECKER",
																			   "Trn_Remarks":"APPROVE",
                                                                                "Trn_Process_Gid":"',@Asset_Detail_Tran_Gid,'",
                                                                               "Trn_Process_Staus":"APPROVE"
																			}'
																			);
																			#select @lj_Details_Data;
																			call sp_FAAsset_Set('INSERT','ASSET_PROCESS_CHECKER','APPROVE',@lj_Details_Data,'{}',
																								lj_Classification,ls_Createby,@Message);
																			select @Message into @Out_Msg_Asset;
																		#	select @Out_Msg_Asset;
																			if @Out_Msg_Asset = 'SUCCESS' then
																				SET SQL_SAFE_UPDATES = 0;
																				set Message = 'SUCCESS';
																			elseif @Out_Msg_Asset is null or @Out_Msg_Asset <> 'SUCCESS' then
																				 set Message = concat('FAIL ',@Out_Msg_Asset);
                                                                                 rollback;
                                                                                 leave sp_FAAssertProcess_Set;
																			End if;



															elseif @ls_Status = 'REJECTED' then
																	select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,CONCAT('$.Remark'))) into @ls_Remark;

																	if @ls_Remark is null  or @ls_Remark = '' then
																		set Message = 'Remark Is Needed For Reject.';
																		leave sp_FAAssertProcess_Set;
																	End if;

																	set @lj_Details_Data = '';
																			set @lj_Details_Data = concat(
																			'{"Asset_Detail_Gids":"',@AssetDetails_Gid,'",
																			   "Status":"REJECTED",
																			   "Trn_Ref_Name":"ASSET_CLUB",
																			   "Remark": "',@ls_Remark,'"
																			  }'
																			);

																			#select @AssetDetails_Gid,@ls_Remark;

																			#select @lj_Details_Data;

																			call sp_FAAsset_Set('UPDATE','ASSET_CHECKER','REJECT',@lj_Details_Data,
                                                                            '{}',lj_Classification,ls_Createby,@Message);
																			select @Message into @Out_Msg_Asset;

																			#select @Out_Msg_Asset;

																			if @Out_Msg_Asset = 'SUCCESS' then
																				set Message = 'SUCCESS';
																			elseif @Out_Msg_Asset is null or @Out_Msg_Asset <> 'SUCCESS' then
																				set Message = 'FAIL CHECKER';
																			End if;

															End if;
														*/



														set sql_safe_updates = 0;
													    delete from fa_tmp_tassetdetails where assetdetails_parentgid = @AssetDetails_Gid;

													    set countRow = (select ROW_COUNT());
							                                  if countRow > 0 then
																	set Message = 'SUCCESS';
								                               else
								                                    set Message = 'FAIL In Asset Temp Delete.';
								                                    ROLLBACK;
								                                   leave sp_FAAssertProcess_Set;
								                              End if;




										end if;

									set i = i+1;
								End while;


           End if;


elseif ls_Type = 'CWIP' and ls_Sub_Type = 'CHECKER' then
	      ### CWIP Checker
             select JSON_LENGTH(lj_Details,'$') into @li_Detailjson_count;
					if @li_Detailjson_count is null or @li_Detailjson_count = 0 then
							set Message = 'No Data In Json - Asset Details.';
                            leave sp_FAAssertProcess_Set;
					end if;

					select JSON_LENGTH(lj_Status,'$') into @li_Statusjson_count;
					if @li_Statusjson_count is null or @li_Statusjson_count = 0 then
							set Message = 'No Data In Json - Asset Status.';
                            leave sp_FAAssertProcess_Set;
					end if;

                        select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,CONCAT('$.Status'))) into @ls_Status;

                        if @ls_Status is null or @ls_Status = '' then
								set Message = 'Status Is Needed.';
							    rollback;
                                leave sp_FAAssertProcess_Set;
                        ELSEIF @ls_Status = 'APPROVED' or @ls_Status = 'REJECTED' THEN
                                set @ls_Status = @ls_Status;
                        ELSE
                              set Message ='Incorrect Checker Status Provided.';
                               rollback;
                              leave sp_FAAssertProcess_Set;
                        End if;


                       select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,CONCAT('$.Remark'))) into @ls_Remark;

                      if @ls_Remark is null THEN
                        set @ls_Remark = '';
                      End if;

                      #  select JSON_LENGTH(lj_Details, CONCAT('$.CWIP[0].CWIP_Gid')) into @CWIP_Gid_Count;

						#			if @CWIP_Gid_Count is null or @CWIP_Gid_Count = 0 or @CWIP_Gid_Count = '' then
						#					set Message = 'CWIP  Gid Is Needed.';
						#					leave sp_FAAssertProcess_Set;
						#			End if;

                        set @Is_GroupBy = '';
                        select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Is_GroupBy'))) into @Is_GroupBy;

                        set @lj_Data = '';
						if @Is_GroupBy  = "Y" then

								select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.CWIP[0].CWIP_Group_Gid'))) into @CWIP_Group_Gid;

								set @lj_Data = (select concat('{"CWIP":{"CWIP_Gid":[',group_concat(cwipasset_gid),']}}') from fa_trn_tcwipasset where cwipasset_cwipgroupgid = @CWIP_Group_Gid);
                                #select @lj_Data;
                                select JSON_LENGTH(@lj_Data, CONCAT('$.CWIP[0].CWIP_Gid')) into @CWIP_Gid_Count;
                                #select @CWIP_Gid_Count;
                                if @CWIP_Gid_Count is null or @CWIP_Gid_Count = 0 or @CWIP_Gid_Count = '' then
											set Message = 'CWIP  Gid Is Needed.';
										    rollback;
											leave sp_FAAssertProcess_Set;
									End if;
                        ELSEIF @Is_GroupBy  = "N"  THEN
                                select JSON_LENGTH(lj_Details, CONCAT('$.CWIP[0].CWIP_Gid')) into @CWIP_Gid_Count;
                                set @lj_Data = lj_Details;

									if @CWIP_Gid_Count is null or @CWIP_Gid_Count = 0 or @CWIP_Gid_Count = '' then
											set Message = 'CWIP  Gid Is Needed.';
										    rollback;
											leave sp_FAAssertProcess_Set;
									End if;
                        End if;

					set @CWIP_Gids = 0;
					Set i = 0 ;
				 WHILE i <= @CWIP_Gid_Count -1 DO
						#select @lj_Data;
				       select JSON_UNQUOTE(JSON_EXTRACT(@lj_Data, CONCAT('$.CWIP[0].CWIP_Gid[',i,']'))) into @CWIP_Gid;

				       if @CWIP_Gid is not null and @CWIP_Gid <> 0 THEN

				             #### Tran
				                call sp_Trans_Set('Insert','CWIP_ASSET',@CWIP_Gid,
										 @ls_Status,'G', 'CHECKER',
                                         @ls_Remark,@Entity_Gid, ls_Createby, @Message);
				   					select @Message into @out_msg_tran ;

                                    #select @out_msg_tran ;
									if @out_msg_tran = 'FAIL' then
										set Message = 'Failed On Tran Insert';
									    rollback;
										leave sp_FAAssertProcess_Set;
									ELSEIF @out_msg_tran is not null and LENGTH(@out_msg_tran) < 12 then
									   set Message ='SUCCESS';
									End if;
				             ## Tran Edns

				           if @CWIP_Gids = 0 THEN
				              set @CWIP_Gids = @CWIP_Gid;
				             ### Tran TO DO
				           ELSE
				              set @CWIP_Gids = concat(@CWIP_Gids,',',@CWIP_Gid);
				           End if;
				       End if;

				      set i = i+1;



				 END WHILE;

				##### Frame and Approve The Chekcer CWIP.
				#### To DO Tran
				if @ls_Status = 'APPROVED' THEN
				   set @lj_Cwip_Details = '';
				   set @lj_Cwip_Details =  concat('{
                       "CWIP_Status":"APPROVED",
                       "CWIP_Gids":"',@CWIP_Gids,'"
                      }');
                 ELSEIF @ls_Status = 'REJECTED' THEN
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Status,CONCAT('$.Remark'))) into @ls_Remark;
                   set @lj_Cwip_Details = '';
				   set @lj_Cwip_Details =  concat('{
                       "CWIP_Status":"REJECTED",
                       "CWIP_Gids":"',@CWIP_Gids,'",
                       "Remark":"',@ls_Remark,'"
                      }');
				End if;


				call sp_FACWIP_Set('UPDATE','CWIP_CHECKER','CHECKER',@lj_Cwip_Details,'{}', lj_Classification, ls_Createby,@Message);
			      select @Message into @Out_Msg_Cwip;

			     if @Out_Msg_Cwip <> 'SUCCESS' THEN
			        set Message = concat('Error On CWIP Checker. - ',@Out_Msg_Cwip);
			     ELSEIF @Out_Msg_Cwip is null THEN
			        set Message = 'Error On CWIP Checker.';
			     ELSE
			        set Message ='SUCCESS';
			     End if;


End if;

if Message = 'SUCCESS' then

	commit;
else
    rollback;
    set Message = concat('FAIL-',Message);
End if;

END