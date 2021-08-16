CREATE DEFINER=`developer`@`%` PROCEDURE `galley`.`sp_FASale_Set`(IN `ls_Action` varchar(32),IN `ls_Type` varchar(32),IN `ls_Sub_Type` varchar(32),
IN `lj_Details` json,IN `lj_Classification` json,IN `ls_Createby` varchar(32),OUT `li_Last_Id` int,OUT `Message` varchar(1024))
sp_FASale_Set:BEGIN
#### Ramesh Nov 30
Declare errno int;
Declare msg varchar(1000);
Declare countRow int;
Declare Query_Insert varchar(9000);
Declare Query_Update varchar(2048);
Declare i int;
declare lsheaderno varchar(32);
declare Invoice_No varchar(64);

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
                    leave sp_FASale_Set;
             End if;

 if ls_Type = 'FAASSET_SALE' and ls_Sub_Type = 'SO_HEADER' then
		   ### Product Gid - Custome gid , Rate,Qty. - - It Include the Details Too
           select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Customer_Gid'))) into @Customer_Gid;
           select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Sale_Date'))) into @Sale_Date;
           select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_Sale_Header_Gid'))) into @Asset_Sale_Header_Gid;


           select JSON_LENGTH(lj_Details,CONCAT('$.PRODUCT')) into @Product_Length;

                           if @Product_Length is null or @Product_Length = 0  then
								set Message = 'Product Data Is Needed.';
                                rollback;
                                leave sp_FASale_Set;
                           End if;
           ### Validations
           if @Customer_Gid is null or @Customer_Gid = 0 then
					set Message = 'Customer Gid Is Needed.';
                    leave sp_FASale_Set;
           End if;

           if @Sale_Date is null or @Sale_Date = '' THEN
           		set Message = 'Asset Sale Date Is Needed.';
           	   leave sp_FASale_Set;
           End if;

           if @Asset_Sale_Header_Gid is null or @Asset_Sale_Header_Gid = 0 THEN
             set Message = 'Asset Sale Header Gid Is Needed.';
             leave sp_FASale_Set;
           End if;


           	select ifnull(max(soheader_no),0) into @code1 from gal_trn_tsoheader where date_format(soheader_date,'%Y-%m-%d') = curdate();
			#select @code1;
			call sp_Generatecode_Get('WITH_DATESMALL', 'SLG', '00', @code1, @Message);

	              call sp_Generate_number_get('SO','000',@Message);
                  	select @Message into @ls_no from dual;

				if @ls_no is null or @ls_no = '' then
					set Message = 'Problem In SO Header No Generation.';
                    leave sp_FASale_Set;
                End if;

                select ifnull(b.entitydetails_gstno,0) into @Company_GSTno
                            from gal_adm_tentityheader as a
							inner join gal_adm_tentitydetails as b on b.entitydetails_entityheadergid = a.entity_gid
							where a.entity_gid = @Entity_Gid  and b.entitydetails_gid = 1
							and a.entity_isactive = 'Y' and a.entity_isremoved = 'N'
							and b.entitydetails_isactive = 'Y' and b.entitydetails_isremoved = 'N';

                        if @Company_GSTno = 0 or @Company_GSTno = '' or @Company_GSTno is null then
									set Message = 'Error On Company GST No.';
                            End if;

               #select @ls_no;

                #set @Company_GSTno = '33GST';
                set @SO_Header_Amount = 0;
                set @SO_Header_Total = 0;

            set Query_Insert = '';
            set Query_Insert = concat('Insert into gal_trn_tsoheader (soheader_customer_gid,soheader_no,soheader_gstno,soheader_date,soheader_employee_gid,
                                                          Soheader_channel,soheader_status,soheader_amount,soheader_total,entity_gid,
                                                      create_by)
                                              values (''',@Customer_Gid,''',''',@ls_no,''',''',@Company_GSTno,''',''',@Sale_Date,''',1,''F'',''REQUESTED'',''',@SO_Header_Total,''',
                                              ''',@SO_Header_Total,''',''',@Entity_Gid,''',''',ls_Createby,''')
                                                     ');

													set @Insert_query = Query_Insert;
													#SELECT @Insert_query;
													PREPARE stmt FROM @Insert_query;
													EXECUTE stmt;
													set countRow = (select ROW_COUNT());
													DEALLOCATE PREPARE stmt;

                                                    if countRow > 0 then
                                                          set Message = 'SUCCESS';
                                                               select LAST_INSERT_ID() into @SOHeader_Maxgid ;
                                                               set li_Last_Id = @SOHeader_Maxgid;
                                                     else
                                                          set Message = 'FAIL';
                                                          rollback;
                                                          leave sp_FASale_Set;
                                                    End if;

                                               ### Details part.
							set i = 0 ;
                           While i <= @Product_Length -1 Do


										select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.PRODUCT[',i,'].Product_Gid'))) into @Product_Gid;
										#select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.PRODUCT[',i,'].Product_Qty'))) into @Product_Qty;
										select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.PRODUCT[',i,'].Sale_Rate'))) into @Sale_Rate;
   									   	select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.PRODUCT[',i,'].HSN_Code'))) into @HSN_Code;
									  	select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.PRODUCT[',i,'].SGST_Rate'))) into @SGST_Rate;
									 	select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.PRODUCT[',i,'].CGST_Rate'))) into @CGST_Rate;
										select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.PRODUCT[',i,'].IGST_Rate'))) into @IGST_Rate;

                                        if @Product_Gid is null or @Product_Gid = 0 then
												set Message = 'Product Gid Is Needed.';
												leave sp_FASale_Set;
										End if;

                                         if @Sale_Rate is null or @Sale_Rate = 0 then
											set Message = 'Sales Rate Is Needed.';
											leave sp_FASale_Set;
									   End if;

									   if @HSN_Code is null or @HSN_Code = '' THEN
									     set Message = 'HSN Code Is Needed.';
									     leave sp_FASale_Set;
									   End if;

                                    #### Get The Qty
                                     set @Product_Qty = 0;
										Select count(a.assetsale_gid) into @Product_Qty from fa_trn_tassetsale as a
										inner join fa_tmp_tassetdetails as b on b.assetdetails_id = a.assetsale_assetdetailsid
										where a.assetsale_value = @Sale_Rate and b.assetdetails_productgid = @Product_Gid
										and a.assetsale_isactive = 'Y' and a.assetsale_isremoved = 'N'
										and b.assetdetails_isactive = 'Y' and b.assetdetails_isremoved = 'N'
									    and a.assetsale_assetsaleheadergid = @Asset_Sale_Header_Gid
										;

									   if @Product_Qty is null or @Product_Qty = 0 then
											set Message  = 'Product Quantity Is Needed.' ;
											leave sp_FASale_Set;
									   End if;

                                          select P.product_code,P.product_uom_gid,hsn_code
											into  @Product_Code,@UOM_Gid,@HSN_Code
											     from gal_mst_tproduct P
                                                 left join gal_mst_thsn H on H.hsn_gid = P.product_hsn_gid
                                                 where product_gid=@Product_Gid
                                                 and P.product_isactive='Y' and P.product_isremoved='N'
												 and H.hsn_isactive='Y' and H.hsn_isremoved='N' ;

                                         #set @Product_Code = 'RT';
                                         #set @UOM_Gid = 0;
                                         #set @HSN_Code = '65';
                                         set @Sale_Total = @Product_Qty * @Sale_Rate;
                                         set @Sale_Status = 'APPROVED';
                                         set @Sale_Remark = 'RTY';

                                         #select @Inv_Product_Gid, @SOHeader_Maxgid,@Product_Gid,@Product_Code,@UOM_Gid,
                                              #@Sale_Rate,@Product_Qty,@HSN_Code,@Sale_Total,
											  #@Sale_Total,@Sale_Status,@Sale_Remark,@Entity_Gid,ls_Createby;

                                        ### detail Insert
                                        set Query_Insert = '';
                                        set Query_Insert = concat('
											insert into gal_trn_tsodetails (sodetails_soheader_gid,sodetails_product_gid,sodetails_product_code,
											sodetails_uom_gid,sodetails_unitprice,sodetails_qty,sodetails_hsncode,sodetails_amount,
											sodetails_total,sodetails_status,sodetails_remarks,sodetails_cgst,sodetails_sgst,sodetails_igst,
											entity_gid,create_by
											)values(''',@SOHeader_Maxgid,''',''',@Product_Gid,''',''',@Product_Code,''',''',@UOM_Gid,''',
                                              ''',@Sale_Rate,''',''',@Product_Qty,''',''',@HSN_Code,''',''',@Sale_Total,''',
                                             ''',@Sale_Total,''',''',@Sale_Status,''',''',@Sale_Remark,''',''',@SGST_Rate,''',
                                             ''',@CGST_Rate,''',''',@IGST_Rate,''',''',@Entity_Gid,''',''',ls_Createby,'''
                                             )');

                                            		set @Insert_query = '';
                                                    set @Insert_query = Query_Insert;
													#SELECT @Insert_query;
													PREPARE stmt FROM @Insert_query;
													EXECUTE stmt;
													set countRow = (select ROW_COUNT());
													DEALLOCATE PREPARE stmt;

                                                    if countRow > 0 then
                                                          set Message = 'SUCCESS';
														  #select LAST_INSERT_ID() into @SOHeader_Maxgid ;
                                                     else
                                                          set Message = 'FAIL';
                                                          rollback;
                                                          leave sp_FASale_Set;
                                                    End if;


                                 set i = i+1;
                           End while;

  elseif ls_Type = 'SALE_MAKER' and ls_Sub_Type = 'SALE_HEADER' then
               #### To Save The asset Sale only in Asset Tables - Not So header Table.
       select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.Customer_Gid')) into @Customer_Gid;
       select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.Branch_Gid')) into @Branch_Gid;
       select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.Sale_Date')) into @Sale_Date;
       select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.Status')) into @ls_Status;
       select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.Remarks')) into @Remarks;
       ### Validation is Needed

          set Query_Insert = '';
          set Query_Insert = concat('Insert into fa_trn_tassetsaleheader(assetsaleheader_customergid,assetsaleheader_salebranchgid,assetsaleheader_saledate,
			assetsaleheader_saletotalamount,assetsaleheader_invoiceheadergid,assetsaleheader_status,assetsaleheader_remarks,entity_gid,create_by)
            values (''',@Customer_Gid,''',''',@Branch_Gid,''',''',@Sale_Date,''',0,0,''',@ls_Status,''',''',@Remarks,''',''',@Entity_Gid,''',''',ls_Createby,''')'
            );

												set @Insert_query = Query_Insert;
													#SELECT @Insert_query;
													PREPARE stmt FROM @Insert_query;
													EXECUTE stmt;
													set countRow = (select ROW_COUNT());
													DEALLOCATE PREPARE stmt;

                                                    if countRow > 0 then
                                                          set Message = 'SUCCESS';
                                                               select LAST_INSERT_ID() into @AssetSaleH_Maxgid ;
                                                               set li_Last_Id = @AssetSaleH_Maxgid;
                                                     else
                                                          set Message = 'FAIL';
                                                          leave sp_FASale_Set;
                                                    End if;


													call sp_Trans_Set('Insert','FA_SALE',@AssetSaleH_Maxgid,'PENDING','G',
																	  'MAKER',@Remarks,@Entity_Gid,ls_Createby,@message);
													select @message into @tran;
													#select @message; #remove it
													if @tran <>0 or @tran <> '' then
															set Message = 'SUCCESS';
													else
															set Message = 'FAIL in tran';
															leave sp_FASale_Set;
													end if;

 elseif ls_Type = 'SALE_MAKER' and ls_Sub_Type = 'SALE_DETAIL' then
     ### To Save The Asset Detail table
     	 select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.SaleHeader_Gid')) into @SaleHeader_Gid;
	     select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.Sale_Date')) into @Sale_Date;
	   	 select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.Sale_Status')) into @Sale_Status;
   		 select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.Sale_Reason')) into @Sale_Reason;
	 	 select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.Sale_Rate')) into @Sale_Rate;
	 	 select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.Assetdetail_Gids')) into @Assetdetail_Gids;
	 	 select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.HSN_Code')) into @HSN_Code;
	 	 select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.SGST_Rate')) into @SGST_Rate;
	 	 select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.CGST_Rate')) into @CGST_Rate;
	 	 select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.IGST_Rate')) into @IGST_Rate;

	 select @SaleHeader_Gid,@Sale_Date,@Sale_Status,@Sale_Reason,@Sale_Rate,@Entity_Gid,ls_Createby,@Assetdetail_Gids,
	     @HSN_Code,@SGST_Rate,@CGST_Rate,@IGST_Rate ;
	 set Query_Insert = '';
	 set Query_Insert = concat('insert into fa_trn_tassetsale (assetsale_assetsaleheadergid,assetsale_assetdetailsid,assetsale_date,
		assetsale_status,assetsale_reason,assetsale_customer,assetsale_value,assetsale_invoiceheadergid,
        assetsale_hsncode,assetsale_sgst,assetsale_cgst,assetsale_igst,
        entity_gid,create_by)
	 	(select ''',@SaleHeader_Gid,''',assetdetails_id,''',@Sale_Date,''',''',@Sale_Status,''',''',@Sale_Reason,''',
     	''XXX'',''',@Sale_Rate,''',0,''',@HSN_Code,''',''',@SGST_Rate,''',''',@CGST_Rate,''',''',@IGST_Rate,''',
        ''',@Entity_Gid,''',''',ls_Createby,''' from fa_trn_tassetdetails
		where assetdetails_gid in (',@Assetdetail_Gids,')
 		)');

						set @Insert_query = '';
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
                              leave sp_FASale_Set;
                        End if;



elseif ls_Type = 'INVOICE_HEADER_MAKER' and ls_Sub_Type = 'INVOICE_HEADER' then
     ### To Save The Asset Detail table

			select JSON_LENGTH(lj_Details,CONCAT('$')) into @json_count;

				if @json_count=0 or @json_count is null or @json_count='' then
					set  Message='No Data In lj_Details Json';
					leave sp_FASale_Set;
				end if;


                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.Customer_Gid')) into @Customer_Gid;
				#select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.Branch_Gid')) into @Branch_Gid;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.InvoiceHeader_Gid')) into @InvoiceHeader_Gid;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.InvoiceHeader_Date')) into @InvoiceHeader_Date;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.Inv_Total')) into @Amount;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.Remarks')) into @Remarks;
			    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,'$.State_Billing_From_Gid')) into @State_Billing_From_Gid;


                select JSON_LENGTH(lj_Details,CONCAT('$.PRODUCT')) into @Product_Length;
			    #select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Product_Qty'))) into @InvoiceDetails_QTY;
			    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Customer_Gid'))) into @Customer_Gid;

                  #------#@Entity_Gid,@Entity_Detail_Gid --------------

                  Select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,'$.Entity_Details_Gid')) into @Entity_Detail_Gid_fn ;

                  if @Entity_Detail_Gid_fn is null or @Entity_Detail_Gid_fn = 0 THEN
                    set Message = 'Error On Entity Detail Gid.';
                    leave sp_FASale_Set;
                  End if;

                    select ifnull(b.entitydetails_gstno,0) into @InvoiceHeader_GST_No
                            from gal_adm_tentityheader as a
							inner join gal_adm_tentitydetails as b on b.entitydetails_entityheadergid = a.entity_gid
							where a.entity_gid =@Entity_Gid  and b.entitydetails_gid = @Entity_Detail_Gid_fn
							and a.entity_isactive = 'Y' and a.entity_isremoved = 'N'
							and b.entitydetails_isactive = 'Y' and b.entitydetails_isremoved = 'N';

                        if @InvoiceHeader_GST_No = 0 or @InvoiceHeader_GST_No = '' or @InvoiceHeader_GST_No is null then
									set Message = 'Error On InvoiceHeader GST No.';
								   leave sp_FASale_Set;
                            End if;




										     SELECT  S.state_gid,ifnull(b.taxdetails_taxno,'') as gst into @Customer_State_Gid,@Customer_GST_No
            									FROM    fa_trn_tassetsaleheader A
													INNER JOIN	gal_mst_tcustomer C	ON A.assetsaleheader_customergid = C.customer_gid
													INNER JOIN 	gal_mst_taddress AD ON C.customer_add_gid = AD.address_gid
													INNER JOIN	gal_mst_tstate S 	ON AD.address_state_gid = S.state_gid
													INNER JOIN  gal_mst_ttaxdetails as b on b.taxdetails_reftablecode = C.customer_code
                         							inner join gal_mst_tref as z on z.ref_name = 'CUST_GST'
                         							 and b.taxdetails_ref_gid = z.ref_gid
                                                        where A.assetsaleheader_isactive='Y'
                                                        and A.assetsaleheader_isremoved='N'
                                                        and C.customer_isactive='Y'
                                                        and C.customer_isremoved='N'
                                                        and S.state_isremoved='N'
                                                        and C.customer_gid=@Customer_Gid
                                                        and b.taxdetails_isactive = 'Y' and b.taxdetails_isremoved = 'N'
														and z.ref_active = 'Y' and z.ref_isremoved = 'N'
														limit 1
                                                        ;

                                                       if @Customer_State_Gid is null or @Customer_State_Gid = 0 THEN
                                                         set Message = 'Error On Customer State Data.';
                                                          leave sp_FASale_Set;
                                                       End if;

                                                      if @Customer_GST_No is null or @Customer_GST_No = 0 THEN
                                                        set Message = 'Error On Customer GST No.';
                                                        leave sp_FASale_Set;
                                                      End if;



-- 										     SELECT  S.state_name into @Employee_State_Name
-- 											 FROM	fa_trn_tassetsaleheader A
-- 													INNER JOIN	gal_mst_temployee E ON A.create_by = E.employee_gid
-- 													INNER JOIN	gal_mst_taddress AD ON E.employee_add_gid = AD.address_gid
-- 													INNER JOIN	gal_mst_tstate S 	ON AD.address_state_gid = S.state_gid
-- 													  where A.assetsaleheader_isactive='Y'
--                                                       and A.assetsaleheader_isremoved='N'
--                                                       and E.employee_isactive='Y'
--                                                       and E.employee_isremoved='N'
--                                                       and S.state_isremoved='N'
--                                                       and E.employee_gid=ls_Createby
--                                                        group by S.state_name limit 1;
--




                        set @InvoiceHeader_Channel='O';
                        set @Despatch_Gid=0;
                        set @IsPrint=0;
                        set @EntityDetails_Gid=1;
                        set @Branch_Gid=0;


						set @Invoice_Status='NEW';
                        set @Discount=0;
                        set @Employee_Gid=ls_Createby;
                        set @OutStanding=@Amount;


                       set @Invoice_No = (select max(invoiceheader_no) invoiceheader_no from gal_trn_tinvoiceheader);

			        set Invoice_No=@Invoice_No;
							SELECT
			                   CASE WHEN MONTH(now())>=4 THEN
			                       concat(DATE_FORMAT(now(),"%y"), '',DATE_FORMAT(now(),"%y")+1)
			                   ELSE concat(DATE_FORMAT(now(),"%y")-1,'', DATE_FORMAT(now(),"%y")) END into @financial_year;

						select Mid(Invoice_No,length('000'),length('0000')) into @Old_Fin_Year;

			            if Invoice_No <> '' and @Old_Fin_Year = @financial_year then
			               set @lsheaderno=right(Invoice_No,length('00000'));
						   set @Inv_No=concat(@financial_year,@lsheaderno)+1;
			               set lsheaderno=concat('VF',@Inv_No);
						else
						   set @lsheaderno =concat('VF',@financial_year,'0000','1');
			               #select @lsheaderno ;
						   set lsheaderno=@lsheaderno;
						end if;

               #select @Customer_Gid,lsheaderno,@InvoiceHeader_GST_No,
				#								 @InvoiceHeader_Date,ls_Createby,@InvoiceHeader_Channel,
				#								 @Remarks,@Invoice_Status,@Amount,@Discount,@Tax_Amount,
				#								 @Inv_Total,@OutStanding,@Customer_GST_No,@Despatch_Gid,@IsPrint,
				#								 @Entity_Gid,@EntityDetails_Gid,@Branch_Gid,ls_Createby;

					set @Tax_Amount = 0;
				    set @Inv_Total =  0;

				set Query_Insert = '';
				set Query_Insert = concat('INSERT INTO gal_trn_tinvoiceheader
												(invoiceheader_customer_gid, invoiceheader_no,invoiceheader_gstno,
												invoiceheader_date, invoiceheader_employee_gid,invoiceheader_channel,
												invoiceheader_remarks, invoiceheader_status,invoiceheader_amount,
												invoiceheader_discount, invoiceheader_taxamount,invoiceheader_total,
												invoiceheader_outstanding, invoiceheader_customergstno,invoiceheader_despatch_gid,
												invoiceheader_isprint,  entity_gid, entitydetails_gid,branch_gid,create_by)
										  VALUES(',@Customer_Gid,',''',lsheaderno,''',''',@InvoiceHeader_GST_No,''',
												 ''',@InvoiceHeader_Date,''',',ls_Createby,',''',@InvoiceHeader_Channel,''',
												 ''',@Remarks,''',''',@Invoice_Status,''',',@Amount,',',@Discount,',',@Tax_Amount,',
												 ',@Inv_Total,',',@OutStanding,',''',@Customer_GST_No,''',',@Despatch_Gid,',',@IsPrint,',
												 ',@Entity_Gid,',',@EntityDetails_Gid,',',@Branch_Gid,',',ls_Createby,')
								         ');

						set @Insert_query = '';
 						set @Insert_query = Query_Insert;
						#SELECT @Insert_query,2;
						PREPARE stmt FROM @Insert_query;
						EXECUTE stmt;
						set countRow = (select ROW_COUNT());
						DEALLOCATE PREPARE stmt;

                        if countRow > 0 then
                              set Message = 'SUCCESS';
                              select last_insert_Id() into li_Last_Id ;
                         else
                              set Message = 'FAIL';
                              leave sp_FASale_Set;
                        End if;


				set i = 0 ;
				While i < @Product_Length Do

						select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.PRODUCT[',i,'].inv_pdct_gid'))) into @Inv_Product_Gid;
						select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.PRODUCT[',i,'].Product_Qty'))) into @InvoiceDetails_QTY;
						select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.PRODUCT[',i,'].inv_sale_rate'))) into @Inv_Sale_Rate;

					    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.PRODUCT[',i,'].HSN_Code'))) into @HSN_Code;
					    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.PRODUCT[',i,'].SGST_Rate'))) into @SGST_Rate;
					    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.PRODUCT[',i,'].CGST_Rate'))) into @CGST_Rate;
					    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.PRODUCT[',i,'].IGST_Rate'))) into @IGST_Rate;


                            #set @Invoice_Gid=12;
                            #set @Product_Code='PRcd123';
							#set @UOM_Gid=99;
						    #set @Unit_Price=2000;
							#set @InvoiceDetails_HSN_Code='HSNCD123';
							#set @Dealer_Price=3000;
							#set @InvoiceDetails_CGST=60.00;
                            #set @InvoiceDetails_SGST=70.00;
							#set @InvoiceDetails_IGST=45.00;
							#set @Tax_Amount=70;
                            set @NRP_price=@Inv_Sale_Rate;
                            set @Unit_Price = @NRP_price;
                            set @Dealer_Price = @Unit_Price;
                            set @Campaign_Gid=0;
							set	@Discount=0;
							set	@Total=@InvoiceDetails_QTY*@Inv_Sale_Rate;



			                if @Customer_State_Gid = @State_Billing_From_Gid then
									set @InvoiceDetails_CGST =  (@Total * @CGST_Rate)/100;
			                        set @InvoiceDetails_SGST =  (@Total * @SGST_Rate)/100;
			                        set @InvoiceDetails_IGST = 0 ;
			                        set @Tax_Amount = @InvoiceDetails_CGST + @InvoiceDetails_SGST;
			                        set @Total_Pdct_Amount_fn = @Total + @Tax_Amount;

							elseif 	@Customer_State_Gid <> @State_Billing_From_Gid then
									set @InvoiceDetails_CGST =  0;
			                        set @InvoiceDetails_SGST =  0;
			                        set @InvoiceDetails_IGST = (@Total * @IGST_Rate)/100;
			                        set @Tax_Amount = @InvoiceDetails_IGST;
			                        set @Total_Pdct_Amount_fn = @Total + @Tax_Amount;
			                End if;


           /*    select  li_Last_Id,@Campaign_Gid,@Inv_Product_Gid,@Product_Code,
											@UOM_Gid,@Unit_Price,@InvoiceDetails_QTY,@HSN_Code,
											@Dealer_Price,@NRP_price,@InvoiceDetails_CGST,@InvoiceDetails_SGST,
											@InvoiceDetails_IGST,@Tax_Amount,@Discount,@Total,
											@Entity_Gid,ls_Createby;

             */

				set Query_Insert = '';
				set Query_Insert = concat('INSERT INTO gal_trn_tinvoicedetails
												  (invoicedetails_invoice_gid,invoicedetails_campaign_gid,invoicedetails_product_gid,
												   invoicedetails_product_code,invoicedetails_uom_gid,invoicedetails_unitprice, invoicedetails_qty,
												   invoicedetails_hsncode,invoicedetails_dealerprice, invoicedetails_nrpprice,
												   invoicedetails_cgst,invoicedetails_sgst, invoicedetails_igst, invoicedetails_taxamount,
												   invoicedetails_discount, invoicedetails_total,entity_gid, create_by )
										   VALUES(',li_Last_Id,',',@Campaign_Gid,',',@Inv_Product_Gid,',''',@Product_Code,''',
												   ',@UOM_Gid,',',@Unit_Price,',',@InvoiceDetails_QTY,',''',@HSN_Code,''',
												   ',@Dealer_Price,',',@NRP_price,',',@InvoiceDetails_CGST,',',@InvoiceDetails_SGST,',
												   ',@InvoiceDetails_IGST,',',@Tax_Amount,',',@Discount,',',@Total,',
												   ',@Entity_Gid,',',ls_Createby,')
								       ');

						set @Insert_query = '';
 						set @Insert_query = Query_Insert;
						#SELECT @Insert_query,1;
						PREPARE stmt FROM @Insert_query;
						EXECUTE stmt;
						set countRow = (select ROW_COUNT());
						DEALLOCATE PREPARE stmt;

                         if countRow > 0 then
                              set Message = 'SUCCESS';
                         else
                              set Message = 'FAIL';
                              leave sp_FASale_Set;
                        End if;

				set i = i+1;
				End while;



elseif ls_Type = 'SO_INVOICE_MAKER' and ls_Sub_Type = 'SO_INVOICE' then
     ### To Save The Asset Detail table

			select JSON_LENGTH(lj_Details, CONCAT('$')) into @lj_Details_JSON_COUNT;

             if  @lj_Details_JSON_COUNT = 0 or @lj_Details_JSON_COUNT is  null or @lj_Details_JSON_COUNT = '' then
					set Message = 'No Data In lj_Details JSON';
                    leave sp_FASale_Set;
             End if;

             select JSON_LENGTH(lj_Details, CONCAT('$.SO_DATA')) into @SO_DATA_JSON_LENGTH;

             if  @SO_DATA_JSON_LENGTH = 0 or @SO_DATA_JSON_LENGTH is  null or @SO_DATA_JSON_LENGTH = '' then
					set Message = 'No Data In SO_DATA LIST';
                    leave sp_FASale_Set;
             End if;


             set i=0;
             WHILE i < @SO_DATA_JSON_LENGTH DO

		        select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.SO_DATA[',i,'].SO_Header_Gid'))) into @SO_Header_Gid;
		        select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.SO_DATA[',i,'].SO_Details_Gid'))) into @SO_Details_Gid;
		        select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.SO_DATA[',i,'].Invoice_header_Gid'))) into @Invoice_header_Gid;


		        if @SO_Header_Gid='' or @SO_Header_Gid is null then
					set Message='SO_Header Gid Is Not Given';
		        end if;
		        set li_Last_Id=0;

				#select @SO_Header_Gid,@SO_Details_Gid,
					   #li_Last_Id,@Entity_Gid,ls_Createby;

				set Query_Insert = '';
				set Query_Insert = concat('INSERT INTO gal_map_tsoinv
												(soinv_soheader_gid,soinv_sodetails_gid,
												soinv_invoiceheader_gid,entity_gid,create_by)
										   VALUES(',@SO_Header_Gid,',''',@SO_Details_Gid,''',
												  ''',li_Last_Id,''',',@Entity_Gid,',',ls_Createby,')
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
                         else
                              set Message = 'FAIL';
                              leave sp_FASale_Set;
                        End if;


        set i=i+1;
        END WHILE;

 elseif ls_Type = 'ASSET_SALE_UPDATE' and ls_Sub_Type = 'PROCESS' then

  			select JSON_LENGTH(lj_Details, CONCAT('$')) into @lj_Details_JSON_COUNT;

             if  @lj_Details_JSON_COUNT = 0 or @lj_Details_JSON_COUNT is  null or @lj_Details_JSON_COUNT = '' then
					set Message = 'No Data In lj_Details JSON';
                    leave sp_FASale_Set;
             End if;

             select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.AssetSale_Header_Gid'))) into @AssetSale_Header_Gid;
             select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.AssetSale_Status'))) into @AssetSale_Status;
            # select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.AssetSale_Remark'))) into @AssetSale_Remark;

            if @AssetSale_Header_Gid is null or @AssetSale_Header_Gid = 0 THEN
            	set Message = 'Asset Sale Header Gid Is Needed.';
                leave sp_FASale_Set;
            End if;

           if @AssetSale_Status is null or @AssetSale_Status = '' THEN
           		set Message = 'Asset Checker Status Is Needed.';
           	     leave sp_FASale_Set;
           End if;

          # if @AssetSale_Remark is null or @AssetSale_Remark = '' THEN
          #	set Message = 'Asset Checker Remarks Is Needed.';
          # leave sp_FASale_Set;
          #End if;

           ### Reject Reason Will affect in Tran Table
           set Query_Update = '';
           set Query_Update = concat('update fa_trn_tassetsaleheader set assetsaleheader_status = ''',@AssetSale_Status,''' ,
                update_by = ''',ls_Createby,''',update_date = now()
           		where assetsaleheader_gid = ''',@AssetSale_Header_Gid,'''
		           ');

		               set @Update_Query = '';
 						set @Update_Query = Query_Update;
						#SELECT @Update_Query;
						PREPARE stmt FROM @Update_Query;
						EXECUTE stmt;
						set countRow = (select ROW_COUNT());
						DEALLOCATE PREPARE stmt;

                        if countRow > 0 then
                              set Message = 'SUCCESS';
                         else
                              set Message = 'Fail On Asset Header Update.';
                              leave sp_FASale_Set;
                        End if;


                  set sql_safe_updates = 0;
                set Query_Update = '';
        	   set Query_Update = concat('Update fa_trn_tassetsale set assetsale_status = ''',@AssetSale_Status,''',
		          update_by = ''',ls_Createby,''',update_date = now()
		          where assetsale_assetsaleheadergid = ''',@AssetSale_Header_Gid,'''
		           ');


		          	     set @Update_Query = '';
 						set @Update_Query = Query_Update;
						#SELECT @Update_Query;
						PREPARE stmt FROM @Update_Query;
						EXECUTE stmt;
						set countRow = (select ROW_COUNT());
						DEALLOCATE PREPARE stmt;

                        if countRow > 0 then
                              set Message = 'SUCCESS';
                         else
                              set Message = 'Fail On Asset Header Update.';
                              leave sp_FASale_Set;
                        End if;


 End if;




END