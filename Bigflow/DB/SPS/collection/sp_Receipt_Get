CREATE DEFINER=`root`@`%` PROCEDURE `sp_Receipt_Get`(IN `ls_Type` varchar(64),IN `ls_Sub_Type`varchar(64),
IN `lj_Filters` json,IN `lj_Classification` json,Out `Message`  varchar(1024))
sp_Receipt_Get:BEGIN
### Ramesh Dec 13 2018, Feb 2019
### Selva Dec 2018 search
#### Ramesh May 15 2019, Union All, Sep 5 2019

Declare Query_Select varchar(10000);
Declare Query_srch varchar(2048);

Declare Query_Select_Cltn varchar(2048);
Declare Query_Select_Stock varchar(2048);
Declare Query_Search_Cltn varchar(1024);
Declare Query_Search_Stock varchar(1024);
Declare Query_Select_Cr varchar(2048);
Declare Query_Select_Emp varchar(2048);
Declare Query_Select_SCr varchar(2048);
Declare Query_Select_DuePayment varchar(2048);


Declare errno int;
Declare j int;
Declare msg varchar(1000);
Declare entity_gid,client_gid varchar(1000);

Declare li_count int;

		DECLARE EXIT HANDLER FOR SQLEXCEPTION,sqlwarning
		BEGIN

		GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
		set Message = concat(errno , msg);
		ROLLBACK;
		END;
        set Query_srch = '';
        set entity_gid = '';


            SELECT JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,'$.Cheque_From_Date'))INTO @ls_fromdate;
			SELECT JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,'$.Cheque_To_Date'))INTO @ls_todate;
			SELECT JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,'$.Cheque_No'))INTO @ls_chqno;
			SELECT JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,'$.Collection_Status'))INTO @ls_status;
			SELECT JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,'$.CustomerGroup_Gid'))INTO @ls_groupgid;
			SELECT JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,'$.Collection_Amount'))INTO @ls_collectionamt;


           if @ls_fromdate <> 0 then

				set Query_srch = concat(Query_srch,' and c.fetcollectionheader_date >=''',@ls_fromdate,'''' );
			end if;

			if @ls_todate <> 0 then
				set Query_srch = concat(Query_srch,' and c.fetcollectionheader_date <=''',@ls_todate,'''' );
			end if;

			if @ls_chqno <> '' then
				set Query_srch = concat(Query_srch,' and c.fetcollectionheader_chequeno = ''',@ls_chqno,'''' );
			end if;

			if @ls_status <> '' then
				set Query_srch = concat(Query_srch,' and c.fetcollectionheader_status = ''',@ls_status ,'''');
			end if;

			if @ls_collectionamt <> 0 then
				set Query_srch = concat(Query_srch,' and c.fetcollectionheader_amount = ''',@ls_collectionamt,'''' );
			end if;

			if @ls_groupgid <> 0 then
				set Query_srch = concat(Query_srch,' and d.customergroup_gid = ''',@ls_groupgid,'''' );
			end if;


            select JSON_LENGTH(lj_classification, '$') into @li_jsonclass_count;

			if @li_jsonclass_count <=0 then
				set Message = 'Entity Gid or Client Gid Not Given';
				leave sp_Receipt_Get;
			end if;


		set j = 0 ;
			select  JSON_LENGTH(lj_classification, CONCAT('$.entity_gid')) into @entity_cnt;
			if @entity_cnt <> 0 then
				WHILE j<= @entity_cnt - 1 Do

					select JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.entity_gid[',j,']'))) into @entity_gid;
					if @entity_cnt  <> '' then
						 if @entity_gid <> 0 then
							if entity_gid <> '' then
								set entity_gid = concat(entity_gid,',',@entity_gid);
							else
								set entity_gid = @entity_gid;
							end if;

						end if;

					end if;
					set j = j + 1;

				END WHILE;
			end if;

            set j = 0 ;
			select  JSON_LENGTH(lj_classification, CONCAT('$.client_gid')) into @client_cnt;
			if @client_cnt <> 0 then
				WHILE j<= @client_cnt - 1 Do

					select  JSON_EXTRACT(lj_classification, CONCAT('$.client_gid[',j,']')) into @client_gid;
					if @client_cnt  <> '' then
						 if @client_gid <> 0 then
							if client_gid <> '' then
								set client_gid = concat(client_gid,',',@client_gid);
							else
								set client_gid = @client_gid;
							end if;

						end if;

					end if;
					set j = j + 1;

				END WHILE;
			else
				set client_gid = '';
			end if;

 if ls_Type = 'INV_RECEIPT_MAPPING' and ls_Sub_Type = 'COLLECTION' then

              SELECT JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,'$.Cheque_From_Date'))INTO @Cheque_From_Date;
              SELECT JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,'$.Cheque_To_Date'))INTO @Cheque_To_Date;
              SELECT JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,'$.Cheque_No'))INTO @Cheque_No;
              SELECT JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,'$.CustomerGroup_Gid'))INTO @CustomerGroup_Gid;
              SELECT JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,'$.Collection_Amount'))INTO @Collection_Amount;
              SELECT JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,'$.Receipt_Date'))INTO @Receipt_Date;
              SELECT JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,'$.Collection_Status'))INTO @Collection_Status;

             set Query_srch = '';
              if @Cheque_From_Date is not null and @Cheque_From_Date <> '' then
					set Query_srch = concat(Query_srch,' and cheque_date >=''',@Cheque_From_Date,'''' );
              End if;
              if @Cheque_To_Date is not null and @Cheque_To_Date <> '' then
					set Query_srch = concat(Query_srch,' and cheque_date <=''',@Cheque_To_Date,'''' );
              End if;
              if @Cheque_No is not null and @Cheque_No <> '' then
					set Query_srch = concat(Query_srch,' and cheque_no =''',@Cheque_No,'''' );
              End if;
              if @CustomerGroup_Gid is not null and @CustomerGroup_Gid <> '' and @CustomerGroup_Gid <> 0 then
					set Query_srch = concat(Query_srch,' and customer_group_gid = ''',@CustomerGroup_Gid,'''' );
              End if;
              if @Collection_Amount is not null and @Collection_Amount <> '' and @Collection_Amount <> 0 then
					set Query_srch = concat(Query_srch,' and receipt_amount = ''',@Collection_Amount,'''' );
              End if;
			 if @Receipt_Date is not null and @Receipt_Date <> '' and @Receipt_Date <> 0 then
					set Query_srch = concat(Query_srch,' and receipt_date = ''',@Receipt_Date,'''' );
              End if;

              if @Collection_Status is not null and @Collection_Status <> ''  then
				set Query_srch = concat(Query_srch, ' and  fetcollectionheader_mode = ''',@Collection_Status,''' ');
              End if;

							select fn_REFGid('COLLECTION_RECEIPT') into @REF_Collection_Gid;

                                        if @REF_Gid = 0 then
											set Message = 'Problem In REF Gid Generate For Collection.' ;
                                            leave sp_Receipt_Get;
                                        End if;

								select fn_REFGid('STOCK_RECEIPT') into @REF_Stock_Gid;

                                        if @REF_Stock_Gid = 0 then
											set Message = 'Problem In REF Gid Generate For Stock.' ;
                                            leave sp_Receipt_Get;
                                        End if;

                                 select fn_REFGid('CREDITNOTE_RECEIPT') into @REF_Cr_Gid;

                                        if @REF_Cr_Gid = 0 then
											set Message = 'Problem In REF Gid Generate For All Discounts.' ;
                                            leave sp_Receipt_Get;
                                        End if;

                                     select fn_REFGid('BADDEBTS_RECEIPT') into @REF_BD_Gid;

                                        if @REF_Cr_Gid = 0 then
											set Message = 'Problem In REF Gid Generate For Bad Debts.' ;
                                            leave sp_Receipt_Get;
                                        End if;

                                        set @REF_Cr_Gid = concat(@REF_Cr_Gid,',',@REF_BD_Gid);

								select fn_REFGid('SALES_CREDIT_NOTE') into @REF_SCr_Gid;

                                        if @REF_SCr_Gid = 0 then
											set Message = 'Problem In REF Gid Generate For Sale Discounts.' ;
                                            leave sp_Receipt_Get;
                                        End if;
                                        #

                                   select fn_REFGid('EMPLOYEE_RECEIPT') into @REF_Emp_Gid;
                                           if @REF_Emp_Gid = 0 then
												set Message = 'Problem In REF Gid Generate For Employee Receipt.' ;
												leave sp_Receipt_Get;
											End if;

                                 select fn_REFGid('DUE_PAYMENT') into @REF_Due_Payment_Gid;
                                           if @REF_Due_Payment_Gid = 0 then
												set Message = 'Problem In REF Gid Generate For Due Payment Receipt.' ;
												leave sp_Receipt_Get;
											End if;

				set Query_Select_Cltn = '';
                set Query_Select_Cltn = concat('Select a.receipt_gid,a.receipt_refgid as ref_gid,a.receipt_reftablegid as receipt_reftable_gid,
													c.customergroup_name,a.receipt_remarks,
													date_format(a.receipt_date,''%d-%b-%Y'') as receipt_date,b.fetcollectionheader_mode,
													date_format(b.fetcollectionheader_date,''%d-%b-%Y'') as collection_date,
													date_format(b.fetcollectionheader_chequedate,''%d-%b-%Y'') as cheque_date,
                                                    b.fetcollectionheader_chequeno as cheque_no,
													a.receipt_amount,a.receipt_balanceamount,a.receipt_from,a.receipt_type,a.receipt_vouchertype,c.customergroup_gid as customer_group_gid
													from gal_trn_treceipt as a
													Left join fet_trn_tfetcollectionheader as b on b.fetcollectionheader_gid = a.receipt_reftablegid
													Left join gal_mst_tcustomergroup as c on c.customergroup_gid = b.fetcollectionheader_customergroup_gid
													Where a.receipt_isactive = ''Y'' and a.receipt_isremoved = ''N''  and a.receipt_balanceamount <> 0
													and a.receipt_refgid = ',@REF_Collection_Gid,' and a.entity_gid in (',entity_gid,')
                                                    ');

                   set Query_Select_Stock = '';
                   set Query_Select_Stock = concat('Select d.receipt_gid,d.receipt_refgid as ref_gid,d.receipt_reftablegid as receipt_reftable_gid,
													g.customergroup_name,d.receipt_remarks,
													date_format(d.receipt_date,''%d-%b-%Y'') as receipt_date, ''Sales Return'' as fetcollectionheader_mode,
													date_format(e.returnheader_date,''%d-%b-%Y'') as collection_date,
													'''' as cheque_date,'''' as cheque_no,
													d.receipt_amount,d.receipt_balanceamount,d.receipt_from,d.receipt_type,d.receipt_vouchertype,g.customergroup_gid as customer_group_gid
													from gal_trn_treceipt as d
													inner join gal_trn_treturnheader  as e on e.returnheader_gid = d.receipt_reftablegid
													inner join gal_mst_tcustomer as f on f.customer_gid = e.returnheader_customergid
													inner join gal_mst_tcustomergroup as g on g.customergroup_gid = f.customer_custgroup_gid
													Where d.receipt_isactive = ''Y'' and d.receipt_isremoved = ''N''  and d.receipt_balanceamount <> 0
													and d.receipt_refgid = ',@REF_Stock_Gid,' and d.entity_gid in (',entity_gid,')
                                                    ');

                       set Query_Select_Cr = '';
                       set Query_Select_Cr = concat('Select h.receipt_gid,h.receipt_refgid as ref_gid,h.receipt_reftablegid as receipt_reftable_gid,
													i.customergroup_name,h.receipt_remarks,
													date_format(h.receipt_date,''%d-%b-%Y'') as receipt_date, receipt_type as fetcollectionheader_mode,
													date_format(h.receipt_date,''%d-%b-%Y'') as collection_date,
													'''' as cheque_date,'''' as cheque_no,
													h.receipt_amount,h.receipt_balanceamount,h.receipt_from,h.receipt_type,h.receipt_vouchertype,i.customergroup_gid as customer_group_gid
													from gal_trn_treceipt as h
													inner join gal_mst_tcustomergroup as i on i.customergroup_gid = h.receipt_reftablegid
													Where h.receipt_isactive = ''Y'' and h.receipt_isremoved = ''N''  and h.receipt_balanceamount <> 0
													and h.receipt_refgid in (',@REF_Cr_Gid,') and h.entity_gid in (',entity_gid,')');


                                          set Query_Select_Emp = '';
                                          set Query_Select_Emp = concat(' Select j.receipt_gid,j.receipt_refgid as ref_gid,j.receipt_reftablegid as receipt_reftable_gid,
													n.customergroup_name,j.receipt_remarks,
													date_format(j.receipt_date,''%d-%b-%Y'') as receipt_date, j.receipt_type as fetcollectionheader_mode,
													date_format(j.receipt_date,''%d-%b-%Y'') as collection_date,
													'''' as cheque_date,'''' as cheque_no,
													j.receipt_amount,j.receipt_balanceamount,j.receipt_from,j.receipt_type,j.receipt_vouchertype,n.customergroup_gid as customer_group_gid
													from gal_trn_treceipt as j
                                                    inner join gal_map_tinvreceipt as k on k.invreceipt_reftablegid = j.receipt_gid and k.invreceipt_refgid  = ',@REF_Emp_Gid,'
                                                    inner join gal_trn_tinvoiceheader as l on l.invoiceheader_gid = k.invreceipt_invoicegid and l.invoiceheader_isremoved = ''N''
                                                    inner join gal_mst_tcustomer as m on m.customer_gid = l.invoiceheader_customer_gid and m.customer_isactive = ''Y''
                                                       and m.customer_isremoved = ''N''
													inner join gal_mst_tcustomergroup as n on n.customergroup_gid = m.customer_custgroup_gid and n.customergroup_isactive = ''Y''
														and n.customergroup_isremoved = ''N''
													Where j.receipt_isactive = ''Y'' and j.receipt_isremoved = ''N''  and j.receipt_balanceamount <> 0
													and j.receipt_refgid in (',@REF_Emp_Gid,') and j.entity_gid in (',entity_gid,')
                                                    group by j.receipt_gid,j.receipt_refgid,j.receipt_reftablegid,n.customergroup_name,j.receipt_date,
                                                    j.receipt_amount,j.receipt_balanceamount,j.receipt_from,
                                                       j.receipt_type,j.receipt_vouchertype,n.customergroup_gid '
                                                    );

                                          set Query_Select_SCr = '';
                                          set Query_Select_SCr = concat(' Select j.receipt_gid,j.receipt_refgid as ref_gid,j.receipt_reftablegid as receipt_reftable_gid,
													n.customergroup_name,j.receipt_remarks,
													date_format(j.receipt_date,''%d-%b-%Y'') as receipt_date, j.receipt_type as fetcollectionheader_mode,
													date_format(j.receipt_date,''%d-%b-%Y'') as collection_date,
													'''' as cheque_date,'''' as cheque_no,
													j.receipt_amount,j.receipt_balanceamount,j.receipt_from,j.receipt_type,j.receipt_vouchertype,n.customergroup_gid as customer_group_gid
													from gal_trn_treceipt as j
                                                    inner join gal_map_tinvreceipt as k on k.invreceipt_reftablegid = j.receipt_gid and k.invreceipt_refgid  = ',@REF_SCr_Gid,'
                                                    inner join gal_trn_tinvoiceheader as l on l.invoiceheader_gid = k.invreceipt_invoicegid and l.invoiceheader_isremoved = ''N''
                                                    inner join gal_mst_tcustomer as m on m.customer_gid = l.invoiceheader_customer_gid and m.customer_isactive = ''Y''
                                                       and m.customer_isremoved = ''N''
													inner join gal_mst_tcustomergroup as n on n.customergroup_gid = m.customer_custgroup_gid and n.customergroup_isactive = ''Y''
														and n.customergroup_isremoved = ''N''
													Where j.receipt_isactive = ''Y'' and j.receipt_isremoved = ''N''  and j.receipt_balanceamount <> 0
													and j.receipt_refgid in (',@REF_SCr_Gid,') and j.entity_gid in (',entity_gid,')
                                                    group by j.receipt_gid,j.receipt_refgid,j.receipt_reftablegid,n.customergroup_name,j.receipt_date,
                                                    j.receipt_amount,j.receipt_balanceamount,j.receipt_from,
                                                       j.receipt_type,j.receipt_vouchertype,n.customergroup_gid '
                                                    );

                                              set Query_Select_DuePayment = '';
                                              set Query_Select_DuePayment = concat('Select o.receipt_gid,o.receipt_refgid as ref_gid,o.receipt_reftablegid as receipt_reftable_gid,
													customergroup_name,o.receipt_remarks,
													date_format(o.receipt_date,''%d-%b-%Y'') as receipt_date, receipt_type as fetcollectionheader_mode,
													date_format(o.receipt_date,''%d-%b-%Y'') as collection_date,
													'''' as cheque_date,'''' as cheque_no,
													o.receipt_amount,o.receipt_balanceamount,o.receipt_from,o.receipt_type,o.receipt_vouchertype,customergroup_gid as customer_group_gid
													from gal_trn_treceipt as o
                                                    inner join gal_mst_tsupplier as p on p.supplier_gid = o.receipt_reftablegid
													inner join gal_mst_tcustomergroup as q on q.customergroup_gid = p.supplier_customergroupgid
													Where o.receipt_isactive = ''Y'' and o.receipt_isremoved = ''N''  and o.receipt_balanceamount <> 0
													and o.receipt_refgid in (',@REF_Due_Payment_Gid,') and o.entity_gid in (',entity_gid,')
                                                    and p.supplier_isactive = ''Y'' and p.supplier_isremoved = ''N''
                                                    and q.customergroup_isactive = ''Y'' and q.customergroup_isremoved = ''N'' ');


                                                                set @Query_Select =  concat('select   receipt_gid,ref_gid,receipt_reftable_gid,customergroup_name,receipt_remarks,receipt_date,
																								fetcollectionheader_mode,collection_date,cheque_date,cheque_no,receipt_amount,receipt_balanceamount,
																									receipt_from,receipt_type,receipt_vouchertype,customer_group_gid
																										from (',Query_Select_Cltn,' Union All ',Query_Select_Stock,' Union All ',Query_Select_Cr,
                                                                                                        ' Union All ',Query_Select_Emp,'   Union All ', Query_Select_SCr,
                                                                                                        ' Union All ',Query_Select_DuePayment,'
                                                                                                        ) as main where 1=1 ',Query_srch);
																set @smt = @Query_Select;
																#select @Query_Select; ## Remove It.
																PREPARE stmt1 FROM @smt;
																EXECUTE stmt1;
																Select found_rows() into li_count;
																DEALLOCATE PREPARE stmt1;

																if li_count > 0 then
																		set Message = 'FOUND';
																else
																		set Message = 'NOT_FOUND';
																end if;

elseif ls_Type = 'INV_RECEIPT' and ls_Sub_Type = 'SUMMARY' then
         ### Used To Show Summary for Receipt cancel
			          SELECT JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,'$.Receipt_From_Date'))INTO @ls_Receipt_fromdate;
						SELECT JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,'$.Receipt_To_Date'))INTO @ls_Receipt_todate;
                        SELECT JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,'$.Customer_Group_Gid'))INTO @Customer_Group_Gid;
                        #SELECT JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,'$.Invoice_No'))INTO @ls_Invoice_No;

                 set Query_srch = '';
				if @ls_Receipt_fromdate is not null and @ls_Receipt_fromdate <> '' then
						set Query_srch = concat(Query_srch,' and a.receipt_date >=''',@ls_Receipt_fromdate,'''' );
                End if;

                if @ls_Receipt_todate is not null and @ls_Receipt_todate <> '' then
						set Query_srch = concat(Query_srch,' and a.receipt_date <=''',@ls_Receipt_todate,'''' );
                End if;

				if @Customer_Group_Gid is not null and @Customer_Group_Gid <> '' and @Customer_Group_Gid <> 0  then
						set Query_srch = concat(Query_srch,' and customergroup_gid =''',@Customer_Group_Gid,'''' );
                End if;


                set Query_Select = '';
                set Query_Select = concat('select a.receipt_gid,a.receipt_refgid as ref_gid,a.receipt_reftablegid as receipt_reftable_gid,d.customergroup_name,
									date_format(a.receipt_date,''%d-%b-%Y'') as receipt_date,c.fetcollectionheader_mode,
									date_format(c.fetcollectionheader_date,''%d-%b-%Y'') as collection_date,
									date_format(c.fetcollectionheader_chequedate,''%d-%b-%Y'') as cheque_date,
									a.receipt_amount,a.receipt_balanceamount,a.receipt_from,a.receipt_type,a.receipt_vouchertype,

                                    case
                                          When a.receipt_amount = a.receipt_balanceamount then ''N''
                                          When a.receipt_amount <> a.receipt_balanceamount then ''Y''
                                      end as ''Is_Cancel_Show''

									from gal_trn_treceipt as a
									inner join gal_mst_tref as b on b.ref_gid=a.receipt_refgid and b.ref_active=''Y'' and b.ref_isremoved=''N''
									inner join fet_trn_tfetcollectionheader as c on c.fetcollectionheader_gid=a.receipt_reftablegid
																				and c.fetcollectionheader_isactive=''Y'' and c.fetcollectionheader_isremoved=''N''
									inner join gal_mst_tcustomergroup as d on d.customergroup_gid =c.fetcollectionheader_customergroup_gid
																				and d.customergroup_isactive=''Y'' and d.customergroup_isremoved=''N''
									where a.receipt_isactive=''Y'' and a.receipt_isremoved=''N'' and a.entity_gid in (',entity_gid,')' ,Query_srch );

									set @Query_Select = Query_Select;
                                    #select @Query_Select; ### Remove it
                                    PREPARE stmt1 FROM @Query_Select;
									EXECUTE stmt1;
									Select found_rows() into li_count;
									DEALLOCATE PREPARE stmt1;

									if li_count > 0 then
											set Message = 'FOUND';
									else
											set Message = 'NOT_FOUND';
									end if;
else
       set Message = 'Incorrect Type And Sub Type.';
       leave sp_Receipt_Get;

 End if;


END