CREATE DEFINER=`developer`@`%` FUNCTION `galley`.`fn_SalesSODetailsProcess`(ls_Type varchar(64),li_State_BillingFrom_Gid int,li_SOHeader_Gid int,li_SODetail_Gid int,
li_Product_Gid int, ld_Order_Quantity decimal(16,2),li_Godown_Gid int,li_Campaign_Gid int,li_Customer_Gid int,li_Employee_Gid int,lj_Classification json
 ) RETURNS varchar(9000) CHARSET utf8mb4
BEGIN
### Ramesh Dec 2018
#### Ramesh Price Edit Feb 2020

Declare Out_Message varchar(9000);
if ls_Type = 'INSERT' then
##  pdct code, uom_gid, unity_price,hsncode,dealerPprice,nrp_price,cgst,sgst,isgt,taxamount,discount,total,

			Select customer_custgroup_gid,d.district_state_gid into @Customer_group_Gid_fn,@State_Gid_fn
			from gal_mst_tcustomer as a
			inner join gal_mst_tlocation as b on b.location_gid = a.customer_location_gid
			inner join gal_mst_tpincode as c on c.pincode_gid = b.location_pincode_gid
			inner join gal_mst_tdistrict as d on d.district_gid = c.pincode_district_gid
			where a.customer_gid = li_Customer_Gid
			and a.customer_isactive = 'Y' and a.customer_isremoved = 'N'
			and b.location_isremoved = 'N' and c.pincode_isremoved = 'N'
			and d.district_isremoved = 'N' ;

				set @check_rate_count = 0 ;		### Check Even if the Empty Values Comes
				select a.product_code,b.uom_gid,a.product_unitprice,d.hsn_code,d.hsn_cgstrate,d.hsn_sgstrate,d.hsn_igstrate,c.dealerprice_amount,
                e.ratecard_finalrate,count(ratecard_gid)
                into @product_code_fn,@uom_gid_fn,@product_unitprice_fn,@hsn_code_fn,@hsn_cgstrate_fn,@hsn_sgstrate_fn,@hsn_igstrate_fn,
                @dealerprice_amount_fn,@ratecard_finalrate_fn,@check_rate_count
				from gal_mst_tproduct as a
				inner join gal_mst_tuom as b on b.uom_gid = a.product_uom_gid
				inner join gal_mst_tdealerprice as c on c.dealerprice_productgid = a.product_gid
					and dealerprice_statepricegid = fn_Customer_Data('CUSTOMER_STATEPRICE',li_Customer_Gid,c.entity_gid)
				inner join gal_mst_thsn as d on d.hsn_gid = a.product_hsn_gid
				inner join gal_map_tratecard as e on e.ratecard_productgid = a.product_gid
				where a.product_isremoved = 'N' and a.product_gid = li_Product_Gid
                and c.dealerprice_gid = e.ratecard_dealerpricegid
				and c.dealerprice_isactive = 'Y' and c.dealerprice_isremoved = 'N'
				and now() between c.dealerprice_validfrom and c.dealerprice_validto
				and e.ratecard_isactive = 'Y' and e.ratecard_isremoved = 'N'
				and  now() between e.ratecard_validfrom and e.ratecard_validto
				and ld_Order_Quantity between e.ratecard_minqty and e.ratecard_maxqty
				and e.ratecard_status = 'APPROVED'  and e.ratecard_campaigngid = li_Campaign_Gid and
				case
						 when (select ifnull(count( z.ratecard_customergroupgid),0) from gal_map_tratecard as z where z.ratecard_campaigngid = e.ratecard_campaigngid
								and z.ratecard_productgid = e.ratecard_productgid and z.ratecard_customergroupgid = @Customer_group_Gid_fn
								and ld_Order_Quantity between z.ratecard_minqty and z.ratecard_maxqty
                                and z.ratecard_status = 'APPROVED' and z.ratecard_campaigngid = li_Campaign_Gid
								  ) = 0 then ( e.ratecard_customergroupgid = 0 or e.ratecard_customergroupgid is null ) #or e.ratecard_customergroupgid is null
						 when (select ifnull(count( z.ratecard_customergroupgid),0) from gal_map_tratecard as z where z.ratecard_campaigngid = e.ratecard_campaigngid
								and z.ratecard_productgid = e.ratecard_productgid and z.ratecard_customergroupgid = @Customer_group_Gid_fn
								and ld_Order_Quantity between z.ratecard_minqty and z.ratecard_maxqty
                                and z.ratecard_status = 'APPROVED' and z.ratecard_campaigngid = li_Campaign_Gid
								  ) <> 0 then e.ratecard_customergroupgid  = @Customer_group_Gid_fn
				   end

				and b.uom_isactive = 'Y' and b.uom_isremoved = 'N'
				and d.hsn_isactive = 'Y' and d.hsn_isremoved = 'N'
                group by ratecard_gid limit 1
                ;

				### Validations.

                if @check_rate_count = 0 then
							set Out_Message = 'Error On Rate';
                            return Out_Message;
                End if;

                #### GST Calculations Starts
                set @Product_Amount_fn = @ratecard_finalrate_fn * ld_Order_Quantity ;

                if li_State_BillingFrom_Gid = @State_Gid_fn then
						set @CGST_Amount_fn =  (@Product_Amount_fn * @hsn_cgstrate_fn)/100;
                        set @SGST_Amount_fn =  (@Product_Amount_fn * @hsn_sgstrate_fn)/100;
                        set @IGST_Amount_fn = 0 ;
                        set @Tax_Amount_fn = @CGST_Amount_fn + @SGST_Amount_fn;
                        set @Total_Pdct_Amount_fn = @Product_Amount_fn + @Tax_Amount_fn;

				elseif 	li_State_BillingFrom_Gid <> @State_Gid_fn then
						set @CGST_Amount_fn =  0;
                        set @SGST_Amount_fn =  0;
                        set @IGST_Amount_fn = (@Product_Amount_fn * @hsn_igstrate_fn)/100;
                        set @Tax_Amount_fn = @IGST_Amount_fn;
                        set @Total_Pdct_Amount_fn = @Product_Amount_fn + @Tax_Amount_fn;
                End if;

		insert into tTmp_SOdetail values(li_SOHeader_Gid,li_SODetail_Gid,li_Product_Gid,ld_Order_Quantity,li_Godown_Gid,li_Campaign_Gid,li_Customer_Gid,@product_code_fn,
        @uom_gid_fn,@product_unitprice_fn,@hsn_code_fn,@dealerprice_amount_fn,@ratecard_finalrate_fn,@CGST_Amount_fn,@SGST_Amount_fn,@IGST_Amount_fn,
        @Tax_Amount_fn,0,@Total_Pdct_Amount_fn
        );

        set Out_Message = 'SUCCESS';
        return Out_Message;

elseif ls_Type = 'FETCH' then
				select concat(' { "DETAILS": [', group_concat(distinct JSON_OBJECT('SO_Details_Gid',tmp_SODetail_Gid,'SO_Header_gid',tmp_SOHeader_Gid,'Product_Gid',tmp_pdct_gid,
												 'Product_Code',tmp_pdct_code,'UOM_Gid',tmp_uom_gid,'Unit_Price',tmp_pdct_unit_price,'Quantity',tmp_pdct_qty,'Godown_Gid',tmp_godown_gid,'Campaign_Gid',tmp_campaign_gid,
                                                 'HSN_Code',tmp_hsn_code,'Dealer_Price',tmp_dealer_price_amount,'NRP_Price',tmp_rate_card_final_rate,
												'CGST',tmp_cgst,'SGST',tmp_sgst,'IGST',tmp_igst,
												'Tax_Amount',tmp_tax_amount,
												'Discount',tmp_discount,
												'Total',tmp_total)),'] }')
                                    into Out_Message
                                from tTmp_SOdetail  ;

                           if   Out_Message is null then
									set Out_Message = 'FAIL';
                                    return Out_Message;
                           End if;

 elseif ls_Type = 'HEADER_DETAILS' then

			set @Invoice_date_fn = date_format(current_date(),'%Y-%m-%d');
							### To Get The Customer GST
                            set @Customer_GST_No_fn = '';
							select ifnull(b.taxdetails_taxno,'') as gst , count(a.customer_gid) as ss into @Customer_GST_No_fn,@checkcount_custgst_fn
                            from gal_mst_tcustomer as a
							inner join gal_mst_ttaxdetails as b on b.taxdetails_reftablecode = a.customer_code
							inner join gal_mst_tref as c on c.ref_name = 'CUST_GST' and b.taxdetails_ref_gid = c.ref_gid
							where a.customer_isactive = 'Y' and a.customer_isremoved = 'N'
							and b.taxdetails_isactive = 'Y' and b.taxdetails_isremoved = 'N'
							and c.ref_active = 'Y' and c.ref_isremoved = 'N'
							and a.customer_gid = li_Customer_Gid;

						if @Customer_GST_No_fn = ''  then
									#set Out_Message = 'Error On Customer GST No.';
                                    #set Out_Message = li_Customer_Gid;
                                    #return Out_Message;
                                   set @Customer_GST_No_fn = '-';
                        End if;
                  ### To Get The Company GST No

								#### Classification
                                Select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,'$.Entity_Details_Gid[0]')) into @Entity_Detail_Gid_fn ;
                                Select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,'$.Entity_Gid[0]')) into @Entity_Gid ;

							select ifnull(b.entitydetails_gstno,0),count(a.entity_gid) into @Company_GSTno_fn,@check_count_company_gst_fn
                            from gal_adm_tentityheader as a
							inner join gal_adm_tentitydetails as b on b.entitydetails_entityheadergid = a.entity_gid
							where a.entity_gid = @Entity_Gid and b.entitydetails_gid = @Entity_Detail_Gid_fn
							and a.entity_isactive = 'Y' and a.entity_isremoved = 'N'
							and b.entitydetails_isactive = 'Y' and b.entitydetails_isremoved = 'N';

                            if @Company_GSTno_fn = 0 or @Company_GSTno_fn = '' or @Company_GSTno_fn is null then
									set Out_Message = 'Error On Company GST No.';
                                    return Out_Message;
                            End if;

						set @custemp_emp_gid = 0 ;
						select ifnull(custemp_employee_gid,0) into @custemp_emp_gid from gal_map_tcustemp as a  where
							 custemp_customer_gid = li_Customer_Gid and
							now() between custemp_validfrom and custemp_validto and custemp_isactive = 'Y' and custemp_isremoved = 'N' limit 1 ;

                    if @custemp_emp_gid =0  then
							set Out_Message = 'Employee Not Mapped With Customer.';
                            return Out_Message;
                    End if;


			set @HeaderData_fn = concat( '{
								"Customer_gid":',li_Customer_Gid,',
								"Invoice_Date": ' '"',@Invoice_date_fn, '"' ',
								"Invoice_No":"",
								"Employee_Gid":',@custemp_emp_gid,',
								"Channel":"X",
								"Remarks":"Invoice Generate",
								"Status":"PENDING_DISPATCH",
								"Company_GST_No":' '"' ,@Company_GSTno_fn, '"' ',
								"Customer_GST_No":'  '"',@Customer_GST_No_fn, '"' '
								}');

                  set Out_Message = @HeaderData_fn;

elseif ls_Type = 'CHECK_SPLIT_QUANTITY' then
         if li_SODetail_Gid = 0 or li_SODetail_Gid = '' or li_SODetail_Gid is null then
				set Out_Message = 'SO Details Gid Is Needed.';
                return Out_Message;
         End if;

							select
					case
						when ifnull(sum(sodetails_qty),0) > ifnull(sum(invoicedetails_qty),0)  then 1
						when ifnull(sum(sodetails_qty),0) <= ifnull(sum(invoicedetails_qty),0)  then 0
					 End as 'ls_Count' into @Split_Count_fn
					from gal_trn_tsoheader as a
					inner join gal_trn_tsodetails as b on b.sodetails_soheader_gid = a.soheader_gid
					inner join gal_map_tsoinv as c on c.soinv_sodetails_gid = b.sodetails_gid
					inner join gal_trn_tinvoiceheader as d on d.invoiceheader_gid = c.soinv_invoiceheader_gid
					inner join gal_trn_tinvoicedetails as e on e.invoicedetails_invoice_gid = d.invoiceheader_gid
					and e.invoicedetails_product_gid=b.sodetails_product_gid
					where b.sodetails_gid = li_SODetail_Gid
					and b.sodetails_isremoved = 'N' and c.soinv_isremoved = 'N' and a.soheader_isremoved = 'N' and d.invoiceheader_isremoved = 'N'
					and e.invoicedetails_isremoved = 'N'
					group by sodetails_gid;
										 #set Out_Message = @Split_Count_fn;
                     #return Out_Message;

                     if  @Split_Count_fn  > 0 then
							set Out_Message = 'NOT_COMPLETED';
                     elseif @Split_Count_fn = 0 then
							set Out_Message = 'COMPLETED';
                      else
                            set Out_Message = 'Error Occured.';
                     End if;

                     return Out_Message;
elseif ls_Type = 'RATECARD_DETAIL' then   ###To Shown in a Sales Register Before Geneerate Invoice :: Only Final rate
					#### Included DP Table too May 28 2019
                    			Select customer_custgroup_gid into @Customer_group_Gid_fn
								from gal_mst_tcustomer as a
								where a.customer_gid = li_Customer_Gid
								and a.customer_isactive = 'Y' and a.customer_isremoved = 'N';

            set @check_rate_count = 0 ;		### Check Even if the Empty Values Comes
				select  e.ratecard_finalrate,count(ratecard_gid)   into @ratecard_finalrate_fn,@check_rate_count
				from gal_mst_tproduct as a
				inner join gal_map_tratecard as e on e.ratecard_productgid = a.product_gid
                inner join gal_mst_tdealerprice as c on c.dealerprice_statepricegid  = fn_Customer_Data('CUSTOMER_STATEPRICE',li_Customer_Gid,a.entity_gid)
				 and now() between c.dealerprice_validfrom and c.dealerprice_validto and c.dealerprice_isactive = 'Y' and c.dealerprice_isremoved = 'N'
				 and c.dealerprice_productgid = li_Product_Gid and c.dealerprice_status = 'APPROVED'
				where a.product_isremoved = 'N' and a.product_gid = li_Product_Gid
				and c.dealerprice_gid = e.ratecard_dealerpricegid
                and e.ratecard_isactive = 'Y' and e.ratecard_isremoved = 'N'
				and  now() between e.ratecard_validfrom and e.ratecard_validto
				and ld_Order_Quantity between e.ratecard_minqty and e.ratecard_maxqty
				and e.ratecard_status = 'APPROVED'  and e.ratecard_campaigngid = li_Campaign_Gid and
				case
						 when (select ifnull(count( z.ratecard_customergroupgid),0) from gal_map_tratecard as z where z.ratecard_campaigngid = e.ratecard_campaigngid
								and z.ratecard_productgid = e.ratecard_productgid and z.ratecard_customergroupgid = @Customer_group_Gid_fn
								and ld_Order_Quantity between z.ratecard_minqty and z.ratecard_maxqty
                                and z.ratecard_status = 'APPROVED' and z.ratecard_campaigngid = li_Campaign_Gid
                                and  now() between z.ratecard_validfrom and z.ratecard_validto
								  ) = 0 then ( e.ratecard_customergroupgid = 0 or e.ratecard_customergroupgid is null ) #or e.ratecard_customergroupgid is null
						 when (select ifnull(count( z.ratecard_customergroupgid),0) from gal_map_tratecard as z where z.ratecard_campaigngid = e.ratecard_campaigngid
								and z.ratecard_productgid = e.ratecard_productgid and z.ratecard_customergroupgid = @Customer_group_Gid_fn
								and ld_Order_Quantity between z.ratecard_minqty and z.ratecard_maxqty
                                and z.ratecard_status = 'APPROVED' and z.ratecard_campaigngid = li_Campaign_Gid
                                and  now() between z.ratecard_validfrom and z.ratecard_validto
								  ) <> 0 then e.ratecard_customergroupgid  = @Customer_group_Gid_fn
				   end
				group by ratecard_gid limit 1
                ;

              if @check_rate_count <> 0 then
					  if @ratecard_finalrate_fn <> 0 then
							set Out_Message = @ratecard_finalrate_fn;
                       else
                           set Out_Message = 0;
                      end if;
               else
                    set Out_Message = 0 ;
              End if;

elseif ls_Type = 'CAMPAIGN_CUST_PDCT' then

								Select customer_custgroup_gid into @Customer_group_Gid_fn
								from gal_mst_tcustomer as a
								where a.customer_gid = li_Customer_Gid
								and a.customer_isactive = 'Y' and a.customer_isremoved = 'N';

                                select entity_gid into @Entity_Gid_fn from gal_mst_tcustomer where customer_gid = li_Customer_Gid limit 1 ;

							select concat(' { "DETAILS": [', group_concat(distinct JSON_OBJECT('Campaign_Gid',a.campaign_gid,'Campaign_Name', a.campaign_name,
					'Final_Rate',b.ratecard_finalrate
					)),'] }')  into Out_Message
					from gal_mst_tcampaign as a
					inner join gal_map_tratecard as b on b.ratecard_campaigngid = a.campaign_gid
					inner join gal_mst_tdealerprice as c on c.dealerprice_gid = b.ratecard_dealerpricegid
					and c.dealerprice_statepricegid = fn_Customer_Data('CUSTOMER_STATEPRICE',li_Customer_Gid,@Entity_Gid_fn)
					where
                    #(ratecard_customergroupgid = @Customer_group_Gid_fn or ratecard_customergroupgid = 0 or ratecard_customergroupgid is null)
					#and
                    ratecard_productgid = li_Product_Gid
                    and c.dealerprice_gid = b.ratecard_dealerpricegid
					and now() between b.ratecard_validfrom and b.ratecard_validto
					and ld_Order_Quantity between b.ratecard_minqty and b.ratecard_maxqty
					and b.ratecard_isactive = 'Y' and b.ratecard_isremoved = 'N'
					and b.ratecard_status = 'APPROVED'
					and c.dealerprice_productgid = li_Product_Gid
					and now() between c.dealerprice_validfrom and c.dealerprice_validto
					and c.dealerprice_isactive = 'Y' and c.dealerprice_isremoved = 'N'
					and c.dealerprice_status = 'APPROVED'
                    and now() between a.campaign_validfrom and a.campaign_validto
					and a.campaign_isactive = 'Y' and a.campaign_isremoved = 'N'


                     and
                    case
						 when (select ifnull(count( z.ratecard_customergroupgid),0) from gal_map_tratecard as z where z.ratecard_campaigngid = b.ratecard_campaigngid
								and z.ratecard_productgid = b.ratecard_productgid and z.ratecard_customergroupgid = @Customer_group_Gid_fn
								and ld_Order_Quantity between z.ratecard_minqty and z.ratecard_maxqty
                                and z.ratecard_status = 'APPROVED' and z.ratecard_campaigngid = a.campaign_gid
                                and  now() between z.ratecard_validfrom and z.ratecard_validto
								  ) = 0 then ( b.ratecard_customergroupgid = 0 or b.ratecard_customergroupgid is null ) #or e.ratecard_customergroupgid is null
						 when (select ifnull(count( z.ratecard_customergroupgid),0) from gal_map_tratecard as z where z.ratecard_campaigngid = b.ratecard_campaigngid
								and z.ratecard_productgid = b.ratecard_productgid and z.ratecard_customergroupgid = @Customer_group_Gid_fn
								and ld_Order_Quantity between z.ratecard_minqty and z.ratecard_maxqty
                                and z.ratecard_status = 'APPROVED' and z.ratecard_campaigngid = a.campaign_gid
                                and  now() between z.ratecard_validfrom and z.ratecard_validto
								  ) <> 0 then b.ratecard_customergroupgid  = @Customer_group_Gid_fn
				   end



                    ;

                    if   Out_Message is null then
									set Out_Message = '{"FAIL":"FAIL"}';
                                    return Out_Message;
					End if;


End if;

	if length(Out_Message) > 9000 then
			set Out_Message = 'Size Error.Contact Admin.';
    End if;

RETURN Out_Message;
END