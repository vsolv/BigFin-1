CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Receipt_Set`(IN `ls_Action` varchar(32),IN `ls_Type` varchar(32),
IN `lj_Data` json,IN `Is_Commit` char,IN `lj_Classification` json,IN `ls_Create_By` varchar(16),OUT `Message` varchar(1024),OUT `Msg_Last_ID` varchar(16)
)
sp_Receipt_Set:BEGIN
# Ramesh Dec 2018
# Type = INITIAL_SET
#Edit --11-01-2019 Entity_Gid 02-02-2019--Validation Prakash S
Declare Query_Insert varchar(2048);
Declare Query_Update varchar(1024);
Declare Query_Column varchar(1024);
Declare Query_Value varchar(1024);
Declare errno int;
Declare msg varchar(1000);
Declare ls_ReceiptNo varchar(16);
Declare countRow int;
Declare i int;
Declare j int;
Declare ld_Adjusted_Amount double;
Declare ld_Adjusted_Amount_Tot double;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION,sqlwarning

    BEGIN

     GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
     set Message = concat(errno , msg);
     ROLLBACK;
     END;
				set autocommit = 0 ;
				#start transaction;  ### This Is Not Need and Dont give without needed.

				select JSON_LENGTH(lj_Classification,'$')into @li_json_class_count;
					  if @li_json_class_count is null or @li_json_class_count =0 then
						   set message ='No classification Data In Json - Classification';
						   rollback;
						   leave sp_Receipt_Set;
					  end if;

                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification,CONCAT('$.Entity_Gid[0]'))) into @Entity_Gid;

                    if @Entity_Gid is null or @Entity_Gid = '' or @Entity_Gid = 0 then
						set Message = 'Error On Entity Gid';
                        leave sp_Receipt_Set;
                    End if;

  if ls_Type = 'INITIAL_SET' and ls_Action = 'INSERT' then
           #select lj_Data;
			select JSON_LENGTH(lj_Data,'$.RECEIPT') into @li_json_count;
					if @li_json_count is null or @li_json_count = 0 then
							set Message = 'No Data In Json - Receipt.';
                            leave sp_Receipt_Set;
					end if;

			        select JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.RECEIPT[0].Receipt_From[0]'))) into @Receipt_From;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.RECEIPT[0].Receipt_Date[0]'))) into @Receipt_Date;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.RECEIPT[0].Receipt_VoucherType[0]'))) into @Receipt_VoucherType;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.RECEIPT[0].Receipt_Type[0]'))) into @Receipt_Type;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.RECEIPT[0].Receipt_REFName[0]'))) into @Receipt_REFName;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.RECEIPT[0].Receipt_RefTable_Gid[0]'))) into @Receipt_RefTable_Gid;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.RECEIPT[0].Receipt_Amount[0]'))) into @Receipt_Amount;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.RECEIPT[0].Receipt_BalanceAmount[0]'))) into @Receipt_BalanceAmount;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.RECEIPT[0].Receipt_Remarks[0]'))) into @Receipt_Remarks;

                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification,CONCAT('$.Entity_Gid[0]'))) into @Entity_Gid;#Entity_Gid

                      #Validation
                        if @Receipt_From ='' then
                          set Message = 'Receipt From Is Needed';
                            leave sp_Receipt_Set;
                        end if;

                        if @Receipt_Date ='' then
                          set Message = 'Receipt Date Is Needed';
                            leave sp_Receipt_Set;
                        end if;

                        if @Receipt_VoucherType ='' then
                          set Message = 'Receipt VoucherType Is Needed';
                            leave sp_Receipt_Set;
                        end if;

                        if @Receipt_Type ='' then
                          set Message = 'Receipt Type Is Needed';
                            leave sp_Receipt_Set;
                        end if;

                        if @Receipt_RefTable_Gid = 0  or  @Receipt_RefTable_Gid ='' then
                          set Message = 'Receipt RefTable Gid Is Needed';
                            leave sp_Receipt_Set;
                        end if;

                        if @Receipt_Amount ='' and @Receipt_Amount < 0 then
                          set Message = 'Receipt Amount Is Needed';
                            leave sp_Receipt_Set;
                        end if;

						if @Receipt_BalanceAmount ='' and @Receipt_Amount < 0 then
                          set Message = 'Receipt BalanceAmount Is Needed';
                            leave sp_Receipt_Set;
                        end if;

                      # Validation End

                    ##### Get The REF Gid
							If @Receipt_REFName <> '' then
										select fn_REFGid(@Receipt_REFName) into @REF_Gid;

                                        if @REF_Gid = 0 then
											set Message = 'Problem In REF Gid Generate' ;
                                            leave sp_Receipt_Set;
                                        End if;
                             Else
									set Message = 'REF Name Is Needed';
                                    leave sp_Receipt_Set;
							End if;

                    ####

						select ifnull(max(receipt_no),0) into @code1 from gal_trn_treceipt where date_format(create_date,'%Y-%m-%d') = curdate();
						#select @code1;
						Call sp_Generatecode_Get('WITH_DATESMALL', 'RP', '00', @code1, @Message);
						select @Message into ls_ReceiptNo ;
								# TO DO number Length Validations
						If ls_ReceiptNo = '' then
								set Message = 'Error On Receipt No Generate.';
								leave sp_Receipt_Set;
						End if;
									### Frame the Query Column and Value
                                    set Query_Column = '';
                                    set Query_Value = '';

								if @Receipt_BalanceAmount <> '0.00' then
									set Query_Column = concat(Query_Column, ' receipt_balanceamount,');
									set Query_Value = concat(Query_Value, '''',@Receipt_BalanceAmount,''',');

								End if;

								if @Receipt_Remarks <> '' then
										set Query_Column = concat(Query_Column, ' receipt_remarks,');
										set Query_Value = concat(Query_Value, '''',@Receipt_Remarks,''',');
								end if;

								#select ls_ReceiptNo,@Receipt_From,@Receipt_Date,@Receipt_VoucherType,@Receipt_Type,@REF_Gid,@Receipt_RefTable_Gid,@Receipt_Amount,
                                    #Query_Column,Query_Value,@Entity_Gid,ls_Create_By;

								set Query_Insert = '';
								Set Query_Insert = Concat('Insert into gal_trn_treceipt (receipt_no,receipt_from,receipt_date,
														receipt_vouchertype,receipt_type,receipt_refgid,receipt_reftablegid,receipt_amount,'
														,Query_Column,'entity_gid, create_by)
														Values(''',ls_ReceiptNo,''',''',@Receipt_From,''',''',@Receipt_Date,''',''',@Receipt_VoucherType,'''
														,''',@Receipt_Type,''',''',@REF_Gid,''',''',@Receipt_RefTable_Gid,''',''',@Receipt_Amount,''','
														,Query_Value,'',@Entity_Gid, ',' ,ls_Create_By, ')'
														);

		set @Insert_query = Query_Insert;
	#select @Insert_query;
        PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;

		if countRow >  0 then
            set Message = 'SUCCESS';
            select LAST_INSERT_ID() into Msg_Last_ID ;
            if Msg_Last_ID > 0 then
				set Msg_Last_ID = Msg_Last_ID;
             else
               set  Msg_Last_ID = 0;
            End if;


			if 	Is_Commit = 'Y' then
				commit;
            End if;
		else
			set Message = 'FAIL';
			#rollback;
		end if;

elseif ls_Action = 'UPDATE' and ls_Type = 'INV_MAPPING_RECEIPT' then

            select JSON_LENGTH(lj_Data,'$.RECEIPT') into @li_json_Receipt_count;
					if @li_json_Receipt_count is null or @li_json_Receipt_count = 0 then
							set Message = 'No Data In Json - Receipt Update.';
                            rollback;
                            leave sp_Receipt_Set;
					end if;

					select JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.RECEIPT[0].Receipt_Gid[0]'))) into @Receipt_Gid;
			        select JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.RECEIPT[0].Receipt_REFTable_Gid[0]'))) into @Receipt_REFTable_Gid;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.RECEIPT[0].REF_Gid[0]'))) into @REF_Receipt_Gid;
					select JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.RECEIPT[0].Receipt_Amount[0]'))) into @Receipt_Amount;

					 select JSON_LENGTH(lj_Data,'$.INV_DETAILS') into @li_json_INV_Mapping_count;
					if @li_json_INV_Mapping_count is null or @li_json_INV_Mapping_count = 0 then
							set Message = 'No Data In Json - INV Mapping Count.';
                            rollback;
                            leave sp_Receipt_Set;
					end if;

                    set i = 0 ;
                    set ld_Adjusted_Amount_Tot = 0 ;
                    set ld_Adjusted_Amount = 0 ;
                    WHILE i <= @li_json_INV_Mapping_count -1 DO

								select JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.INV_DETAILS[',i,'].Adjusted_Amount[0]'))) into ld_Adjusted_Amount ;

                                set ld_Adjusted_Amount_Tot = ld_Adjusted_Amount_Tot + ld_Adjusted_Amount;

                    set i = i + 1;
                    END WHILE;

                    # Validations

                    if cast(ld_Adjusted_Amount_Tot as decimal) is null or cast(ld_Adjusted_Amount_Tot as decimal) = 0 then
							set Message = 'Error On Adjusted Amount Calculate.';
                            rollback;
                            leave sp_Receipt_Set;
                    End if;

                    if cast(ld_Adjusted_Amount_Tot as decimal) > cast(@Receipt_Amount as decimal) then
							set Message = 'Adjusted Amount Is Greater Than Receipt Amount.';
                            rollback;
                            leave sp_Receipt_Set;
                    End if;
                                        ### Calculate the Balance Amount .
                    set @Balance_Receipt_Amount = cast(@Receipt_Amount as decimal) - cast(ld_Adjusted_Amount_Tot as decimal);
                    ####
                    select fn_REFGid('COLLECTION_RECEIPT') into @Ref_Collection_Gid;
                    if @REF_Receipt_Gid = @Ref_Collection_Gid then
											 # To DO No Hard Code#DO 18-01-2019
													#### Frame The Status
												if cast(@Receipt_Amount as decimal) = cast(ld_Adjusted_Amount_Tot as decimal) then
														set @Collection_Status = 'FULLY_ADJUSTED';
												 Elseif cast(@Receipt_Amount as decimal) >cast(ld_Adjusted_Amount_Tot as decimal) then
														set @Collection_Status = 'PARTIALLY_ADJUSTED';
												  Else
														set Message = 'Error On Collection Status Generate.';
														rollback;
														leave sp_Receipt_Set;
												End if;
										#### Status Ends

									#### update Starts Collection header
                                                                    set @b=cast( @Balance_Receipt_Amount as decimal);
																	set Query_Update = '';
																	set Query_Update = concat('Update fet_trn_tfetcollectionheader set fetcollectionheader_status = ''',@Collection_Status,'''
																												, fetcollectionheader_balanceamt = ''', @b,'''
                                                                                                                , update_by = ''',ls_Create_By,''',Update_date = current_timestamp()
                                                                                                                Where fetcollectionheader_gid = ',@Receipt_REFTable_Gid,'
                                                                                                                and fetcollectionheader_isactive = ''Y'' and fetcollectionheader_isremoved = ''N''
																												');

																				set @Query_Update = '';
																				set @Query_Update = Query_Update;
																				PREPARE stmt FROM @Query_Update;
																				EXECUTE stmt;
																				set countRow = (select ROW_COUNT());
																				DEALLOCATE PREPARE stmt;

																		if countRow <= 0 then
																				set Message = 'Error On Collection Balance And Status Update.';
																				rollback;
																				leave sp_Receipt_Set;
																		elseif    countRow > 0 then
																				set Message = 'SUCCESS';

                                                                                 #### Tran Update.
																				 if @Collection_Status <> '' and @Collection_Status is not null then
																				    call sp_Trans_Set('update','COLLECTION_RECEIPT',@Receipt_REFTable_Gid,@Collection_Status,'I','CHECKER',
																							'BANK STMT',@Entity_Gid,ls_Create_By,@message);
																						select @message into @out_msg_tran ;

																								if @out_msg_tran = 'FAIL' then
																									set Message = 'Failed On Tran Update';
																										rollback;
																										leave sp_Receipt_Set;
																								End if;
																				 End if;


																		End if;
                        #### Get The Colllection Mode  - And Insert in the Receipt Map Table - Entry Two.
									select fetcollectionheader_mode into @ReceiptInv_Map_Mode  from fet_trn_tfetcollectionheader
                                    where fetcollectionheader_gid = @Receipt_REFTable_Gid ;

                    End if; #### Condition Based Insert :: Not Always Insert.

                    ##### Update Starts.
                    set @bal=cast(@Balance_Receipt_Amount as decimal);
                    set Query_Update = '';
                    set Query_Update = concat('Update gal_trn_treceipt set receipt_balanceamount = ',@bal,' ,
																		update_by = ''',ls_Create_By,''', Update_date = current_timestamp()
																	Where receipt_gid = ''',@Receipt_Gid,''' and receipt_isactive = ''Y'' and receipt_isremoved = ''N''
																	');

																				set @Query_Update = '';
																				set @Query_Update = Query_Update;
                                                               #                select @Query_Update;  ## Remove it
																				PREPARE stmt FROM @Query_Update;
																				EXECUTE stmt;
																				set countRow = (select ROW_COUNT());
																				DEALLOCATE PREPARE stmt;

																		if countRow <= 0 then
																				set Message = 'Error On Receipt Balance Update.';
																				rollback;
																				leave sp_Receipt_Set;
																		elseif    countRow > 0 then
																				set Message = 'SUCCESS';
																		End if;
                       ##### Update of Receipt Ends
                   ##### Outstanding Starts.
                   set j = 0 ;
                   set @ls_Current_Date = date_format(current_date(),'%Y-%m-%d');
         ###      set @ls_Current_Date = date_format(current_date(),'%d-%m-%Y');  ### For Testing Purpose
						select JSON_LENGTH(lj_Data,'$.INV_DETAILS') into @li_json_Invdetails_count;
								if @li_json_Invdetails_count is null or @li_json_Invdetails_count = 0 then
										set Message = 'No Data In Json - Inv Details Update.';
                                        rollback;
										leave sp_Receipt_Set;
								end if;

                           WHILE j <= @li_json_Invdetails_count -1 DO

											select JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.INV_DETAILS[',j,'].Outstanding_Gid[0]'))) into @Outstanding_Gid ;
                                            select JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.INV_DETAILS[',j,'].Adjusted_Amount[0]'))) into @Adjusted_Amount ;
                                            select JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.INV_DETAILS[',j,'].INV_Map_Gid[0]'))) into @INV_Map_Gid ;
                                            select JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.INV_DETAILS[',j,'].Invoice_Gid[0]'))) into @Invoice_Gid ;
                                            select JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.INV_DETAILS[',j,'].Is_Update[0]'))) into @Is_Update ;

												## Frame The JSON data....

                                                set @lj_INV_Details = '';
                                                set @lj_INV_Details = concat('{
																					"HEADER": {
																									"Customer_Gid": ""
																								},
																					"DETAILS": [{

																									"Outstanding_Header_Gid": "',@Outstanding_Gid,'",
																									"Payment_Type": "R",
																									"Received_Date": "',@ls_Current_Date,'",
																									"Amount": "',@Adjusted_Amount,'",
																									"Status": "PAID",
																									"Description": "R",
                                                                                                    "Invoice_Gid":"',@Invoice_Gid ,'"
																													}
																									]}');
												#	select @lj_INV_Details; ### Remove it.
												call sp_OutstandingCustomer_Set('UPDATE','DETAILS_UPDATE',
																				@lj_INV_Details,
																										'N',
																										ls_Create_By,
																										lj_Classification,
																										@Message);
                                                                                                        Select @Message;

                                                                    if @Message <> 'SUCCESS' then
																			set Message = 'Error On Outstanding Detail Insert.';
                                                                            rollback;
                                                                            leave sp_Receipt_Set;
																	End if;
															##### Outstanding Ends.
                                ###### INV MAP Starts    ################

                                select fn_REFGid('STOCK_RECEIPT') into @Ref_Stock_Gid;
									if @Ref_Stock_Gid = 0 then
										set 	Message = 'Error On Stock Receipt Ref Gid Generate.';
										rollback;
										leave sp_Receipt_Set;
									End if;

								select fn_REFGid('SALES_CREDIT_NOTE') into @Ref_SCr_Gid;
									if @Ref_Cr_Gid = 0 then
										set 	Message = 'Error On Sales Credit Receipt Ref Gid Generate.';
										rollback;
										leave sp_Receipt_Set;
									End if;

                                 select fn_REFGid('CREDITNOTE_RECEIPT') into @Ref_Cr_Gid;
									if @Ref_Cr_Gid = 0 then
										set 	Message = 'Error On Credit Receipt Ref Gid Generate.';
										rollback;
										leave sp_Receipt_Set;
									End if;

                                select fn_REFGid('BADDEBTS_RECEIPT') into @Ref_Baddebts_Gid;
									if @Ref_Baddebts_Gid = 0 then
										set 	Message = 'Error On Baddebts Ref Gid Generate.';
										rollback;
										leave sp_Receipt_Set;
									End if;

                                    select fn_REFGid('DUE_PAYMENT') into @Ref_DuePayment_Gid;
									if @Ref_DuePayment_Gid = 0 then
										set 	Message = 'Error On Due Payment Ref Gid Generate.';
										rollback;
										leave sp_Receipt_Set;
									End if;

                                select fn_REFGid('EMPLOYEE_RECEIPT') into @Ref_EmpReceipt_Gid;
									if @Ref_EmpReceipt_Gid = 0 then
										set 	Message = 'Error On Employee Receipt Ref Gid Generate.';
										rollback;
										leave sp_Receipt_Set;
									End if;


                                if @REF_Receipt_Gid = @Ref_Collection_Gid then##### FET Cltn
                                   set @Ref_Gid_ps = @Ref_Collection_Gid;
                                elseif @REF_Receipt_Gid = @Ref_Stock_Gid then ### Sales Return
									   set @Ref_Gid_ps = @Ref_Stock_Gid;

									   set @stock_inward_type = '';
										Select ifnull(b.metadata_value,'') into @stock_inward_type
										from gal_trn_treturnheader as a
										inner join gal_mst_tmetadata as b on b.metadata_gid = a.returnheader_returntype
										where a.returnheader_gid = @Receipt_REFTable_Gid
										and a.entity_gid = @Entity_Gid ;

										### Validations
										if @stock_inward_type = '' then
											set Message = 'Error On Stock Return Receipt Mode Generate. ';
											rollback;
											leave sp_Receipt_Set;
										End if;

									   if @stock_inward_type = 'Sales Return' then
											   set @ReceiptInv_Map_Mode = 'SALES RETURN';
                                        elseif @stock_inward_type = 'Purchase Inward' then
                                              set @ReceiptInv_Map_Mode = 'PURCHASE INWARD';
									   End if;

								elseif @REF_Receipt_Gid = @Ref_SCr_Gid then
                                     set @Ref_Gid_ps = @Ref_SCr_Gid;
                                     set @ReceiptInv_Map_Mode = 'DISCOUNT';
                                 elseif @REF_Receipt_Gid = @Ref_Cr_Gid then
                                      set @Ref_Gid_ps = @Ref_Cr_Gid;
                                     set @ReceiptInv_Map_Mode = 'DISCOUNT';
                                  elseif @REF_Receipt_Gid = @Ref_Baddebts_Gid then
										set @Ref_Gid_ps = @Ref_Baddebts_Gid;
										set @ReceiptInv_Map_Mode = 'DISCOUNT';
                                 elseif @REF_Receipt_Gid = @Ref_EmpReceipt_Gid then
										 set @Ref_Gid_ps = @Ref_EmpReceipt_Gid;
											set @ReceiptInv_Map_Mode = 'RECEIPT';
                                  elseif @REF_Receipt_Gid = @Ref_DuePayment_Gid then
                                           set @Ref_Gid_ps = @Ref_DuePayment_Gid;
											set @ReceiptInv_Map_Mode = 'RECEIPT';
                                End if;
                                   #### To Set A New Insert in receipt Map while Receipt Making. May 8 2019 : Ramesh
                                   select date_format(receipt_date,'%Y-%m-%d') into @Receipt_Date_ps from gal_trn_treceipt
                                   where receipt_gid = @Receipt_Gid;

										set @lj_INVmap_Detail_ps = '';
                                                                  set @lj_INVmap_Detail_ps = concat('
																			{
                                                                            "Receipt_Mode":"',@ReceiptInv_Map_Mode,'",
                                                                            "Receipt_Type":"1",
                                                                            "REF_Gid":',@Ref_Gid_ps,',
                                                                            "REF_Table_Gid":',@Receipt_Gid,',
                                                                            "Receipt_Date":"',@Receipt_Date_ps,'",
                                                                            "Invoice_Gid":',@Invoice_Gid,',
                                                                            "Adjusted_Amount":"',@Adjusted_Amount,'",
                                                                            "entity_gid":',@Entity_Gid,',
                                                                            "create_by":',ls_Create_By,',
                                                                            "Remarks":"RECEIPT_MAKING"
                                                                            }
																		');

                                                                  # select @lj_INVmap_Detail_ps;
                                                                       # select @ReceiptInv_Map_Mode,@Ref_Gid_ps,@Receipt_Gid,@Receipt_Date_ps,@Invoice_Gid,@Adjusted_Amount,@Entity_Gid;

																		call sp_InvoiceReceiptMap_Set('INSERT', 'RECEIPT_MAKING',
																				@lj_INVmap_Detail_ps,
																				'N', ls_Create_By, lj_Classification,@Message);

																				select @Message into @Out_Msg_INV_Receipt_Map_ps;

																		if @Out_Msg_INV_Receipt_Map_ps <> 'SUCCESS' then
																				set Message = concat('Error on Invoice Receipt Map - ',@Out_Msg_INV_Receipt_Map_ps);
																				leave sp_Receipt_Set;
                                                                         elseif @Out_Msg_INV_Receipt_Map_ps = 'SUCCESS' then
                                                                             set Message = 'SUCCESS';
																		End if;


                                /*
										set @IS_UPADTE_FLAG = '';
                                                if @INV_Map_Gid = 0 then  #### Note Here
													  set @IS_UPADTE_FLAG = 'N';
                                                 else
                                                      set @IS_UPADTE_FLAG = 'Y';
                                                End if;


											if @Is_Update = 'Y' then
																set @lj_InvMapFinal = '';
														set @lj_InvMapFinal = concat('{
															"CHEQUE": [{
                                                            "Invreceipt_Id": "',@INV_Map_Gid,'",
                                                            "Receipt_Mode": "Cheque",
															"Receipt_Type": "1",
                                                            "Remarks": "RF",
															"Adjusted_Amount": "',@Adjusted_Amount,'",
                                                            "Receipt_Date":"',@ls_Current_Date,'",
															"Invoice_Gid": "',@Invoice_Gid,'",
                                                            "REF_Table_Gid": "',@Receipt_REFTable_Gid,'",
															"REF_Gid": "',@REF_Gid,'",
                                                            "Is_Update": "',@IS_UPADTE_FLAG,'"
																}]}');
															call sp_InvoiceReceiptMap_Set('Update', '',
																@lj_InvMapFinal,'N',ls_Create_By,lj_Classification, @Message);
															select @Message;


															if @Message <> 'SUCCESS' then
																	set Message  = 'Error On Inv Receipt Map Update.';
																	rollback;
																	leave sp_Receipt_Set;
															End if;

                                            END if; #### TO DO for Later Inv Map

                                            */
                                            set @adj_amt = cast(@Adjusted_Amount as decimal);
                                            set @lj_Invoice_Outstanding_Amount = '';
                                            set @lj_Invoice_Outstanding_Amount = concat('{"INV_Header_Gid":"',@Invoice_Gid,'",
																				 "Adjusted_Amount":"', @adj_amt,'"
																				 }');

							   call sp_SOInvoice_Set('Update', 'Outstanding_Amount', '{}', '{}',
																			   @lj_Invoice_Outstanding_Amount, '{}', lj_Classification, ls_Create_By,@Message);

                                             select @Message into @Out_Msg_SOInv;
                                             ##select @Out_Msg_SOInv; ### Remove it
                                              if @Message <> 'SUCCESS' then
																set Message  = 'Error On Invoice Outstanding Amount Update.';
                                                                rollback;
                                                                leave sp_Receipt_Set;
												End if;


                                ###### INV Map Ends
                                set j = j+1;
                           END WHILE;

                       if @Message = 'SUCCESS' and Is_Commit = 'Y' then
								commit;
                       End if;
   elseif ls_Action = 'UPDATE' and ls_Type = 'RECEIPT_CANCEL' then
					### To Cancel The Receipt
                    select JSON_LENGTH(lj_Data,'$.RECEIPT') into @li_json_ReceiptCancel_count;
					if @li_json_ReceiptCancel_count is null or @li_json_ReceiptCancel_count = 0 then
							set Message = 'No Data In Json - Receipt.';
                            leave sp_Receipt_Set;
					end if;

                       select JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.RECEIPT[0].Receipt_Gid[0]'))) into @Receipt_Gid_Cancel;

                       if @Receipt_Gid_Cancel <> 0 then
								Select receipt_type,receipt_vouchertype,receipt_reftablegid,receipt_amount into @receipt_type,@receipt_vouchertype,@receipt_reftable_gid,
                                @receipt_amount_cancel
                                from gal_trn_treceipt where receipt_gid = @Receipt_Gid_Cancel and receipt_isactive = 'Y' and receipt_isremoved  = 'N' ;
                        end if;
                      if @receipt_type = 'COLLECTION' and @receipt_vouchertype = 'R' then
								set Query_Update = '';
							set Query_Update = concat(
								'update gal_trn_treceipt set receipt_balanceamount =  ',@receipt_amount_cancel,'
                                where receipt_gid = ',@Receipt_Gid_Cancel,' and receipt_isactive = ''Y'' and receipt_isremoved  = ''N'' '
                            );

													set @Query_Update = '';
														set @Query_Update = Query_Update;
									   #                 select @Query_Update;  ## Remove it
														PREPARE stmt FROM @Query_Update;
														EXECUTE stmt;
														set countRow = (select ROW_COUNT());
														DEALLOCATE PREPARE stmt;

												if countRow <= 0 then
														set Message = 'Error On Receipt Balance Update For Receipt Cancel.';
														rollback;
														leave sp_Receipt_Set;
												elseif    countRow > 0 then
														set Message = 'SUCCESS';
												End if;

                      End if;

  End if; ### IF Type Ends

END