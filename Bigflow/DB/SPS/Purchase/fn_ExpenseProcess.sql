CREATE DEFINER=`developer`@`%` FUNCTION `fn_ExpenseProcess`(ls_Type varchar(64),li_Gid int,li_InvHeader_Gid int,lj_JsonData json,lj_Classification json
 ) RETURNS varchar(9000) CHARSET utf8mb4
fn_ExpenseProcess:BEGIN
### selva oct 16 2019

Declare Out_Message varchar(9000);

if ls_Type = 'ECF_INVOICE_INSERT' then
              				set @igst_value = 0;
							set @cgst_value = 0;
							set @sgst_value = 0;
							set @brtotalamount = 0;

							 select branchexpense_Isgst,c.hsn_code,ifnull(SUBSTRING(d.supplier_gstno,1,2),0),hsn_cgstrate,hsn_sgstrate,hsn_igstrate,branchexpensedetails_amount
															into @isgst,@hsncode,@gstno,@cgst,@sgst,@igst,@bramt  from ap_trn_tbranchexpensedetails as a inner join ap_trn_tbranchexpense
                                                     as b on a.branchexpensedetails_branchexpensegid = b.branchexpense_gid
                                                       left join gal_mst_thsn as c on c.hsn_gid = b.branchexpense_hsngid
                                                       left join gal_mst_tsupplier as d on d.supplier_gid = b.branchexpense_supplierid
                                                        where branchexpensedetails_gid =   li_Gid;

                            if @isgst = 'N' then
                                    set @hsncode = '';
                                    set @brtotalamount = @bramt;
                             else
                                 select SUBSTRING(branch_metadatavalue, 1, 2)  into @branchgst from ap_trn_tbranchexpensedetails as a inner join ap_trn_tbranchexpense
                                                     as b on a.branchexpensedetails_branchexpensegid = b.branchexpense_gid
                                                     inner  join gal_mst_tbranch as br on br.branch_gid = b.branchexpense_branchid
                                                     inner join gal_mst_tbranchinfo as i on i.branchinfo_branchgid = br.branch_gid
                                                                        and branchinfo_metadatagid = (select metadata_gid from gal_mst_tmetadata where metadata_value ='GSTNO' and
                                                                                                         metadata_tablename =  'gal_mst_tbranchinfo')
                                                        where branchexpensedetails_gid =li_Gid;
                                   if @gstno = @branchgst then
                                       set @igst_value = 0;
                                       set @cgst_value =  ROUND((@bramt  * @cgst )/ 100, 2);
                                       set @sgst_value = ROUND((@bramt  * @sgst )/ 100, 2);
                                       set @brtotalamount = @cgst_value + @sgst_value +@bramt;
                                   else
										set @igst_value =ROUND((@bramt  * @igst )/ 100, 2);
                                       set @cgst_value = 0;
                                       set @sgst_value = 0;
										set @brtotalamount = @igst_value +@bramt;
                                   end if;
                            end if;

								##### For Inv details
							select concat(' { "DETAIL": [', group_concat(JSON_OBJECT('Item_Name','RENT','Description','RENT',
							'HSN_Code',@hsncode,'Unit_Price',branchexpensedetails_amount,'Quantity',1,'Amount',branchexpensedetails_amount,'Discount',0,'IGST',@igst_value,'CGST',@cgst_value,'SGST',@sgst_value,
							'Total_Amount',@brtotalamount,'PO_Header_Gid',0,'PO_Detail_Gid',0,'GRN_Header_Gid',0,'GRN_Detail_Gid',0,
                            'Invoice_Header_gid',li_InvHeader_Gid,
								'Invoice_Sno',branchexpensedetails_gid

							  )),'] }')  into @lj_Details
							   from ap_trn_tbranchexpensedetails as a
				  inner join ap_trn_tbranchexpense as b on a.branchexpensedetails_branchexpensegid =  b.branchexpense_gid
				  where a.branchexpensedetails_gid  = li_Gid;

                            if @lj_Details = '' then
									set Out_Message = 'No Details Data.';
                                    return Out_Message;
                            End if;


                            #### For Debit details

                           select  group_concat(JSON_OBJECT('Invoice_Header_Gid',li_InvHeader_Gid,'Invoice_Details_Gid','9999',
                            'Category_Gid',exptype_categorygid,
                            'Sub_Category_Gid',exptype_subcategorygid,'GL_No','1','cc_id',branchexpenseccbs_cc,'bs_id',branchexpenseccbs_bs,'Debit_percentage',branchexpenseccbs_percent,
							'Debit_Amount',branchexpenseccbs_amount,'Debit_Gid','0','Invoice_Sno',branchexpensedetails_gid,
                            'CCBS',concat('[',JSON_OBJECT('cc',branchexpenseccbs_cc,'bs',branchexpenseccbs_bs,'percentage',branchexpenseccbs_percent,'Amount',
                           branchexpenseccbs_amount),']')
							  ))  into @lj_Debit from ap_trn_tbranchexpensedetails as bb inner join ap_trn_tbranchexpense as a
													on bb.branchexpensedetails_branchexpensegid = a.branchexpense_gid
									inner join  ap_trn_tbranchexpenseccbs as b
															  on a.branchexpense_gid = b.branchexpenseccbs_branchexpensegid
                                    inner join ap_mst_texptype as exp on exp.exptype_name = a.branchexpense_type

                            where branchexpensedetails_gid  = li_Gid;

                            set @subcatname = ('');
							set @lj_ccbs = '';
                            if @isgst = 'Y' then
                               if @igst_value=0 then
									set @subcatname = ('CGST','SGST');
                                    set @taxamt =@cgst_value;
                                else
									set @subcatname = ('IGST');
									set @taxamt =@igst_value;

                               end if;
                            end if;

                            if @isgst = 'Y' then
                              select  group_concat(JSON_OBJECT('Invoice_Header_Gid',li_InvHeader_Gid,'Invoice_Details_Gid','9999',
									'Category_Gid',category_gid,
									'Sub_Category_Gid',subcategory_gid,'GL_No',subcategory_glno,'cc_id',tcc_gid,'bs_id',tbs_gid,'Debit_percentage',100,
									'Debit_Amount',@taxamt,'Debit_Gid','0','Invoice_Sno',branchexpensedetails_gid,
									'CCBS',concat('[',JSON_OBJECT('cc',tcc_gid,'bs',tbs_gid,'percentage',100,'Amount',
								   @taxamt),']')
									  )) into  @lj_ccbs from ap_mst_tcategory as cat inner join
															ap_mst_tsubcategory as  sub on sub.subcategory_categorygid = cat.category_gid and
															subcategory_name in (@subcatname)
													inner join  ap_trn_tbranchexpensedetails as bb  on sub.entity_gid = bb.entity_gid
													inner join ap_trn_tbranchexpense as a
															on bb.branchexpensedetails_branchexpensegid = a.branchexpense_gid

											inner join ap_mst_texptype as exp on exp.exptype_name = a.branchexpense_type
										   inner join ap_mst_tbs as bs on bs.entity_gid = bb.entity_gid and tbs_name in('GST')
										   inner join ap_mst_tcc as cc on cc.tcc_bsgid = bs.tbs_gid
									where branchexpensedetails_gid  = li_Gid;

                            end if;

                            set @final_debit = '';

                            select  concat(' { "DEBIT": [',@lj_Debit,',',@lj_ccbs,'] }')  into @final_debit;

                            if @final_debit = '' then
									set Out_Message = 'No Debit Data.';
                                    return Out_Message;
                            End if;

                            #### For Credit details
								select concat(' { "CREDIT": [', group_concat(JSON_OBJECT('Invoice_Header_Gid',li_InvHeader_Gid,'Paymode_Gid','1','Bank_Gid','9',
                                'Ref_No',8,'GL_No','1','Credit_Amount',branchexpensedetails_amount,'Debit_Gid','0','Tax_Type','','Tax_Rate','','TDS_Exempt','N','Credit_Gid',0
								  )),'] }')  into @lj_Credit
								from ap_trn_tbranchexpensedetails as a
				  inner join ap_trn_tbranchexpense as b on a.branchexpensedetails_branchexpensegid =  b.branchexpense_gid
						  where a.branchexpensedetails_gid  = li_Gid;

                                if @lj_Credit = '' then
									set Out_Message = 'No Credit Data.';
                                    return Out_Message;
                                End if;


                            set @lf_full_data = concat('{

										"DETAILS": ',@lj_Details,' ,
										"DEBIT": ',@final_debit,',
										"CREDIT": ',@lj_Credit,'


								}');

                                set Out_Message = @lf_full_data;
                               # set Out_Message = @lj_ccbs;





elseif  ls_Type = 'HEADER_INSERT' then
		### Check the Invoice and GST applicable.
				select concat(' { "HEADER": [', group_concat(JSON_OBJECT('Invoice_Type','BRANCH EXP',
                 'Supplier_gid',c.supplier_gid,
				 'Sup_state_gid',ifnull(d.address_state_gid,0),
				  'Inwarddetails_gid',1,
                  'Is_GST',b.branchexpense_Isgst,
				  'Invoice_Date',current_date(),
				  'Invoice_No',0,
				  'Advance_incr',' ',
				  'Invoice_Other_Amount',0,
				  'Invoice_Tot_Amount',CASE
											WHEN branchexpense_Isgst = 'Y' THEN ROUND((branchexpensedetails_amount  * hsn_igstrate )/ 100, 2)+branchexpensedetails_amount

											ELSE branchexpensedetails_amount
										END,
				  'Supplier_GST_No',ifnull(c.supplier_gstno,''),
				  'Header_Status','NEW',
                  'Employee_gid',employee_gid,
				  'branch_gid',branchexpense_branchid
                  )),'] }')  into  @lj_Header
				  from ap_trn_tbranchexpensedetails as a
				  inner join ap_trn_tbranchexpense as b on a.branchexpensedetails_branchexpensegid =  b.branchexpense_gid
                  inner join gal_mst_tsupplier as c on c.supplier_gid = b.branchexpense_supplierid
                  inner join ap_mst_tproperty as p on p.property_gid = b.branchexpense_propertygid
                  inner join gal_mst_temployee as e  on e.employee_gid  = p.property_inchargegid
                  left join gal_mst_taddress as d on c.supplier_add_gid = d.address_gid
				  left join gal_mst_thsn as h on h.hsn_gid = b.branchexpense_hsngid
				  where a.branchexpensedetails_gid  = li_Gid group by branchexpensedetails_gid

				  ;

                 if @lj_Header = '' then
					set Out_Message = '{"MESSAGE":"ERROR","DATA":"No Header Data."}';
                    return Out_Message;
                  else
                      set Out_Message = concat('{"MESSAGE":"SUCCESS","DATA":',@lj_Header,'}');
                 End if;

End if;


RETURN Out_Message;
END