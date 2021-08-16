CREATE DEFINER=`root`@`%` PROCEDURE `sp_OutstandingCustomer_Get`(IN `ls_Type` varchar(64),IN `ls_Sub_Type` varchar(64),
IN `lj_Filters` json,IN `lj_Classification` json,OUT `Message` varchar(1024)
)
sp_OutstandingCustomer_Get:BEGIN
## Ramesh Dec 14 2018####
### Ramesh  May 08 2019 #### Subquery in receipt making
### Ramesh : Outstanding Bucket :: Order by Customer as sub : June 19 2019
 #Karthiga : edited for customers gid in BUCKET  subtype
	Declare Query_Select text;
    Declare Query_Search varchar(1024);
	Declare errno int;
	Declare msg varchar(1000);
	Declare li_count int;
    Declare cust  text;
    Declare i int;


		DECLARE EXIT HANDLER FOR SQLEXCEPTION,sqlwarning
		BEGIN

		GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
		set Message = concat(errno , msg);
		ROLLBACK;
		END;


        select fn_Classification('ENTITY_ONLY',lj_Classification) into @OutMsg_Classification ;
        select  JSON_UNQUOTE(JSON_EXTRACT(@OutMsg_Classification, '$.Entity_Gid[0]')) into @Entity_Gids;
        if @Entity_Gids is  null or @Entity_Gids = '' then
				select  JSON_UNQUOTE(JSON_EXTRACT(@OutMsg_Classification, '$.Message')) into @Message;
				set Message = concat('Error On Classification Data - ',@Message);
                leave sp_OutstandingCustomer_Get;
        End if;



  if ls_Type = 'OUTSTANDING_DUE_DAYS' and ls_Sub_Type = 'DUE_DAYS' then
		#select lj_Filters;
        select JSON_LENGTH(lj_Filters,'$.customer_gid') into @li_json_count;
        if @li_json_count is  null or @li_json_count = '' or @li_json_count = 0 then
			set Message = 'No Data In Json -Filters.';
			leave sp_OutstandingCustomer_Get;
        end if;
        set cust='';
        set i=0;
        if @li_json_count is not null or @li_json_count <> '' then
        #select @li_json_count;
			while i<@li_json_count do
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.customer_gid[',i,']'))) into @Customer_Gid;
                if i=0 then
					set cust=concat(@Customer_Gid);
			    else
					set cust=concat(cust,',',@Customer_Gid);
                end if;
					set i=i+1;
			end while;
            #select cust;
        end if;


        select JSON_LENGTH(lj_Classification,'$') into @li_json_count1;
        #select @li_json_count1;
        if @li_json_count1 is  null or @li_json_count1 = '' or @li_json_count1 = 0 then
			set Message = 'No Data In Json -Filters.';
			leave sp_OutstandingCustomer_Get;
        else
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification,'$.Entity_Gid[0]')) into @Entity_Gid;
            #select @Entity_Gid;
        end if;
        set Query_Select = '';
        set Query_Select = concat(' select customer_gid,
																customer_name,
                                                                date_format(min(fetsoutstanding_invoicedate),''%Y-%b-%d'') as from_pending_date,
                                                                datediff(now(),ifnull(min(fetsoutstanding_invoicedate),0)) as due_days ,
                                                                sum(fetsoutstanding_netamount) as due_amount
																from  gal_mst_tcustomer as  a
																inner join fet_trn_tfetsoutstanding as b on b.fetsoutstanding_customer_gid=a.customer_gid
																where  fetsoutstanding_status <> ''PAID''
                                                                and  fetsoutstanding_status <> ''CANCEL''
                                                                and fetsoutstanding_customer_gid in (',cust,')
                                                                and  b.entity_gid=',@Entity_Gid,'
																group by customer_gid');

		set li_count = 0;
        set @Query_Select = Query_Select;
        #select @Query_Select; #######remove
        PREPARE stmt from @Query_Select;
        EXECUTE stmt;
        Select found_rows() into li_count;
        DEALLOCATE PREPARE stmt;

        if li_count > 0 then
			set Message = "SUCCESS";
		else
			set Message = "FAIL";
        end if;



 else if ls_Type = 'OUTSTANDING_AR' and ls_Sub_Type = 'INV_MAPPING_RECEIPT' then
                            ### AS Seen Later :: Based on Cust Group
                            select JSON_LENGTH(lj_Filters,'$') into @li_json_count;
                            if @li_json_count is not null or @li_json_count <> '' then
									select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Customer_Group_Gid[0]'))) into @Customer_Group_Gid;

                                       if @Customer_Group_Gid is not null or @Customer_Group_Gid  <> '' or @Customer_Group_Gid <> 0 then
												set Query_Search = '';
                                                set Query_Search = concat(' and f.customergroup_gid = ',@Customer_Group_Gid,' ');

                                       else
                                           set Message  = 'Customer Group Gid Is Needed.';
                                           leave sp_OutstandingCustomer_Get;
                                       End if;

							else
                                  set Message = 'No Data In Json -Filters.';
                                  leave sp_OutstandingCustomer_Get;
                            End if;

					set Query_Select = '';
					set Query_Select = concat('Select a.fetsoutstanding_gid,c.invoiceheader_gid,ifnull(d.invreceipt_gid,0) as inv_map_gid,
															f.customergroup_gid,f.customergroup_name,
                                                            e.customer_gid,e.customer_name,i.location_name,
                                                            concat(e.customer_name,'' - '',i.location_name) as customer_display_name,
															date_format(a.fetsoutstanding_invoicedate,''%d-%b-%Y'') as invoice_date ,
															a.fetsoutstanding_invoiceno,a.fetsoutstanding_netamount as net_amount
															,ifnull(sum(d.invreceipt_amount),0) as amount_tobe_adjusted
                                                            ,ifnull(sum(b.fetsoutstandingdtl_amount),0) as adjusted_amount,
                                                            a.fetsoutstanding_netamount - ifnull(sum(b.fetsoutstandingdtl_amount),0) as balance_amount
															From fet_trn_tfetsoutstanding as a
                                                            Left join fet_trn_tfetsoutstandingdtl as b on b.fetsoutstandingdtl_fetsoutstanding_gid = a.fetsoutstanding_gid and b.fetsoutstandingdtl_isremoved = ''N''
															Inner join gal_trn_tinvoiceheader as c on c.invoiceheader_no = a.fetsoutstanding_invoiceno and c.invoiceheader_date = a.fetsoutstanding_invoicedate
                                                            Inner join gal_mst_tcustomer as e on e.customer_gid = c.invoiceheader_customer_gid
															inner join gal_mst_tlocation as i on i.location_gid = e.customer_location_gid
															Inner join gal_mst_tcustomergroup as f on f.customergroup_gid = e.customer_custgroup_gid
															Left join gal_map_tinvreceipt as d on d.invreceipt_invoicegid = c.invoiceheader_gid and d.invreceipt_type = 0
															Where a.fetsoutstanding_status <> ''PAID'' and a.fetsoutstanding_status <> ''CANCEL'' and a.fetsoutstanding_isremoved = ''N''
                                                            and e.customer_isactive = ''Y'' and e.customer_isremoved = ''N''
                                                            and i.location_isremoved = ''N''  and e.customer_isremoved = ''N'' and e.customer_isactive = ''Y''
                                                            and f.customergroup_isactive = ''Y'' and f.customergroup_isremoved = ''N'' ',Query_Search,'
                                                            and a.entity_gid in (',@Entity_Gids,')
															Group by a.fetsoutstanding_gid,fetsoutstanding_invoicedate,fetsoutstanding_invoiceno,invoiceheader_gid
															Having a.fetsoutstanding_netamount > ifnull(sum(d.invreceipt_amount),0)
                                                            ');
                                                            ### TO  DO
                                                            set li_count = 0 ;
																set @Query_Select = Query_Select;
															#	 select @Query_Select; ## Remove It.
																PREPARE stmt1 FROM @Query_Select;
																EXECUTE stmt1;
																Select found_rows() into li_count;
																DEALLOCATE PREPARE stmt1;

																if li_count > 0 then
																		set Message = 'FOUND';
																else
																		set Message = 'NOT_FOUND';
																end if;

elseif ls_Type = 'OUTSTANDING_AR_RECEIPTMAKING' and ls_Sub_Type = 'INV_MAPPING_RECEIPTMAKING' then
                            ### Only Receipt Will Come
                            select JSON_LENGTH(lj_Filters,'$') into @li_json_count;
                            if @li_json_count is not null or @li_json_count <> '' then
									select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Customer_Group_Gid[0]'))) into @Customer_Group_Gid;
                                #    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Customer_Gid[0]'))) into @Customer_Gid;
                                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Ref_Table_Gid[0]'))) into @Ref_Table_Gid;
                                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.REF_Gid[0]'))) into @REF_Receipt_Gid;
                                  #  select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Invoice_No[0]'))) into @Invoice_No;
                                  select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Receipt_Gid[0]'))) into @Receipt_Gid;

                                       if @Customer_Group_Gid is not null or @Customer_Group_Gid  <> '' or @Customer_Group_Gid <> 0 then
												set Query_Search = '';
                                                set Query_Search = concat(' and f.customergroup_gid = ',@Customer_Group_Gid,' ');
                                       else
                                           set Message  = 'Customer Group Gid Is Needed.';
                                           leave sp_OutstandingCustomer_Get;
                                       End if;

                                       if @Ref_Table_Gid is  null or @Ref_Table_Gid = '' or @Ref_Table_Gid = 0 then
											set Message  = 'Ref Table Gid Is Needed.';
                                           leave sp_OutstandingCustomer_Get;
                                       End if;

                                        if @REF_Receipt_Gid is  null or @REF_Receipt_Gid = '' or @REF_Receipt_Gid = 0 then
											set Message  = 'REF Gid Is Needed.';
                                           leave sp_OutstandingCustomer_Get;
                                       End if;

                                       ### Changed on May 20 2019 ### show The Mapped Value in receipt Making
                                       set @REF_Outstanding_Gid = 0;
                                       select fn_REFGid('SALES_CREDIT_NOTE') into @REF_Outstanding_Gid;

                                        if @REF_Outstanding_Gid = 0 then
											set Message = 'Problem In REF Gid Generate' ;
                                            leave sp_OutstandingCustomer_Get;
                                        End if;

                                        set @REF_Emp_Receipt = 0;
                                        select fn_REFGid('EMPLOYEE_RECEIPT') into @REF_Emp_Receipt;
											if @REF_Emp_Receipt = 0 then
												set Message = 'Problem In REF Gid Generate For Employee Receipt.' ;
												leave sp_OutstandingCustomer_Get;
											End if;


                                        if @REF_Outstanding_Gid = @REF_Receipt_Gid then
												set @REF_Outstanding_Gid = @REF_Receipt_Gid;

                                                if @Receipt_Gid is null or @Receipt_Gid = 0 then
													set Message = 'Receipt Gid Is Needed.';
                                                    leave sp_OutstandingCustomer_Get;
                                                End if;

                                                set @Ref_Table_Gid = @Ref_Table_Gid; #### used to show the Receipt :: By Credit and Its Mapped Values : AS SAME

										elseif @REF_Emp_Receipt = @REF_Receipt_Gid then
                                               set @REF_Outstanding_Gid = @REF_Receipt_Gid;
                                                if @Receipt_Gid is null or @Receipt_Gid = 0 then
													set Message = 'Receipt Gid Is Needed.';
                                                    leave sp_OutstandingCustomer_Get;
                                                End if;

                                                set @Ref_Table_Gid = @Receipt_Gid; #### used to show the Receipt :: By Employee receipt and Its Mapped Values

                                         else
												 set @REF_Outstanding_Gid = 0;
											select fn_REFGid('COLLECTION_INVMAP') into @REF_Outstanding_Gid;
											if @REF_Outstanding_Gid = 0 then
												set Message = 'Problem In REF Gid Generate' ;
												leave sp_OutstandingCustomer_Get;
											End if;
                                        End if;

							else
                                  set Message = 'No Data In Json -Filters.';
                                  leave sp_OutstandingCustomer_Get;
                            End if;

					set Query_Select = '';
					set Query_Select = concat('Select a.fetsoutstanding_gid,c.invoiceheader_gid,ifnull(d.invreceipt_gid,0) as inv_map_gid,
															date_format(a.fetsoutstanding_invoicedate,''%d-%b-%Y'') as invoice_date ,
															a.fetsoutstanding_invoiceno,a.fetsoutstanding_netamount as net_amount
															,ifnull(sum(d.invreceipt_amount),0) as amount_tobe_adjusted
                                                            ,(select ifnull(sum(z.fetsoutstandingdtl_amount),0) from fet_trn_tfetsoutstandingdtl as z
                                                            where z.fetsoutstandingdtl_fetsoutstanding_gid = a.fetsoutstanding_gid )
                                                            as adjusted_amount,
                                                            a.fetsoutstanding_netamount - ifnull(sum(d.invreceipt_amount),0) as balance_amount,
                                                            a.fetsoutstanding_netamount - (select ifnull(sum(z.fetsoutstandingdtl_amount),0) from fet_trn_tfetsoutstandingdtl as z
                                                            where z.fetsoutstandingdtl_fetsoutstanding_gid = a.fetsoutstanding_gid ) as actual_balance_amount
															From fet_trn_tfetsoutstanding as a
															Inner join gal_trn_tinvoiceheader as c on c.invoiceheader_no = a.fetsoutstanding_invoiceno
                                                            and c.invoiceheader_date = a.fetsoutstanding_invoicedate
                                                            Inner join gal_mst_tcustomer as e on e.customer_gid = c.invoiceheader_customer_gid
															Inner join gal_mst_tcustomergroup as f on f.customergroup_gid = e.customer_custgroup_gid
															Left join gal_map_tinvreceipt as d on d.invreceipt_invoicegid = c.invoiceheader_gid and d.invreceipt_reftablegid = ',@Ref_Table_Gid,'
                                                              and d.invreceipt_refgid = ',@REF_Outstanding_Gid,' and d.invreceipt_type = 1
                                                              and d.invreceipt_mode <> ''RECEIPT''
															Where a.fetsoutstanding_status <> ''PAID'' and a.fetsoutstanding_status <> ''CANCEL'' and  a.fetsoutstanding_isremoved = ''N''  and e.customer_isactive = ''Y'' and e.customer_isremoved = ''N''
                                                            and f.customergroup_isactive = ''Y'' and f.customergroup_isremoved = ''N'' ',Query_Search,'
                                                               and a.entity_gid in (',@Entity_Gids,')
															Group by a.fetsoutstanding_gid,fetsoutstanding_invoicedate,fetsoutstanding_invoiceno,invoiceheader_gid
															#Having a.fetsoutstanding_netamount >= ifnull(sum(d.invreceipt_amount),0)
                                                            ');
                                                            ### TO  DO
																set @Query_Select = Query_Select;
														#select @Query_Select; ## Remove It.
																PREPARE stmt1 FROM @Query_Select;
																EXECUTE stmt1;
																Select found_rows() into li_count;
																DEALLOCATE PREPARE stmt1;

																if li_count > 0 then
																		set Message = 'FOUND';
																else
																		set Message = 'NOT_FOUND';
																end if;

 elseif ls_Type = 'OUTSTANDING_AR_BCL' and ls_Sub_Type = 'INV_MAPPING_BCL' then
					### AS Seen Later :: Based on Cusomer Only
                   select JSON_LENGTH(lj_Filters,'$') into @li_json_count;
                            if @li_json_count is not null or @li_json_count <> '' then
									select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Customer_Gid[0]'))) into @Customer_Gid;
                                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Invoice_No[0]'))) into @Invoice_No;
                                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.From_Inv_Date[0]'))) into @From_Inv_Date;
                                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.To_Inv_Date[0]'))) into @To_Inv_Date;

                                       if @Customer_Gid is not null or @Customer_Gid  <> '' or @Customer_Gid <> 0 then
												set Query_Search = '';
                                                set Query_Search = concat(' and e.customer_gid = ',@Customer_Gid,' ');
                                       else
                                           set Message  = 'Customer Gid Is Needed.';
                                           leave sp_OutstandingCustomer_Get;
                                       End if;

                                       if @Invoice_No is not null and @Invoice_No <> '' and @Invoice_No <> 0 then
												  set Query_Search = concat(Query_Search,' and a.fetsoutstanding_invoiceno like ''%',@Invoice_No,'%'' ');
                                       End if;

                                       if @From_Inv_Date is not null and @From_Inv_Date <> '' then
											set Query_Search = concat(Query_Search,' and a.fetsoutstanding_invoicedate >= ''',@From_Inv_Date,''' ');
                                       End if;

										if @To_Inv_Date is not null and @To_Inv_Date <> '' then
											set Query_Search = concat(Query_Search,' and a.fetsoutstanding_invoicedate <= ''',@To_Inv_Date,''' ');
                                       End if;


							else
                                  set Message = 'No Data In Json -Filters.';
                                  leave sp_OutstandingCustomer_Get;
                            End if;

                                set @REF_Gid = 0;
                                       select fn_REFGid('COLLECTION_INVMAP') into @REF_Gid;

                                        if @REF_Gid = 0 then
											set Message = 'Problem In REF Gid Generate' ;
                                            leave sp_OutstandingCustomer_Get;
                                        End if;

					set Query_Select = '';
					set Query_Select = concat('Select a.fetsoutstanding_gid,c.invoiceheader_gid,ifnull(d.invreceipt_gid,0) as inv_map_gid,
															date_format(a.fetsoutstanding_invoicedate,''%d-%b-%Y'') as invoice_date ,
															a.fetsoutstanding_invoiceno,a.fetsoutstanding_netamount as net_amount
															,ifnull(sum(d.invreceipt_amount),0) as amount_tobe_adjusted
                                                            ,(select ifnull(sum(z.fetsoutstandingdtl_amount),0) from fet_trn_tfetsoutstandingdtl as z
                                                            where z.fetsoutstandingdtl_fetsoutstanding_gid = a.fetsoutstanding_gid )
                                                            as adjusted_amount,
                                                            a.fetsoutstanding_netamount - (select ifnull(sum(z.fetsoutstandingdtl_amount),0) from fet_trn_tfetsoutstandingdtl as z
                                                            where z.fetsoutstandingdtl_fetsoutstanding_gid = a.fetsoutstanding_gid ) as balance_amount
															From fet_trn_tfetsoutstanding as a

															Inner join gal_trn_tinvoiceheader as c on c.invoiceheader_no = a.fetsoutstanding_invoiceno
                                                            and c.invoiceheader_date = a.fetsoutstanding_invoicedate
                                                            Inner join gal_mst_tcustomer as e on e.customer_gid = c.invoiceheader_customer_gid
															Inner join gal_mst_tcustomergroup as f on f.customergroup_gid = e.customer_custgroup_gid
															Left join gal_map_tinvreceipt as d on d.invreceipt_invoicegid = c.invoiceheader_gid #and d.invreceipt_type = 0
                                                            and d.invreceipt_refgid = ',@REF_Gid,'
															Where a.fetsoutstanding_status <> ''PAID'' and a.fetsoutstanding_status <> ''CANCEL'' and  a.fetsoutstanding_isremoved = ''N''  and e.customer_isactive = ''Y'' and e.customer_isremoved = ''N''
                                                            and f.customergroup_isactive = ''Y'' and f.customergroup_isremoved = ''N'' ',Query_Search,'
                                                               and a.entity_gid in (',@Entity_Gids,')
															Group by a.fetsoutstanding_gid,fetsoutstanding_invoicedate,fetsoutstanding_invoiceno,invoiceheader_gid
															Having a.fetsoutstanding_netamount > ifnull(sum(d.invreceipt_amount),0)
                                                            ');
                                                            ### TO  DO
																set @Query_Select = Query_Select;
																#  select @Query_Select; ## Remove It.
																PREPARE stmt1 FROM @Query_Select;
																EXECUTE stmt1;
																Select found_rows() into li_count;
																DEALLOCATE PREPARE stmt1;

																if li_count > 0 then
																		set Message = 'FOUND';
																else
																		set Message = 'NOT_FOUND';
																end if;

 elseif ls_Type = 'OUTSTANDING_REPORT_INVOICE_WISE' and ls_Sub_Type = 'BUCKET' then

									select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Employee_Gid[0]'))) into @Employee_Gid;
                                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Customer_Gid[0]'))) into @Customer_Gid;
                                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Outstanding_Customer_Group_Gid[0]'))) into @Customer_Group_Gid;
                                    set Query_Search = '';
                                       if @Employee_Gid is not null or @Employee_Gid  <> '' or @Employee_Gid <> 0 then
												set Query_Search = '';
                                                set Query_Search = concat(' and f.employee_gid = ',@Employee_Gid,' ');
                                       End if;

                                       if @Customer_Group_Gid is not null and @Customer_Group_Gid  <> '' and @Customer_Group_Gid <> 0 and @Customer_Group_Gid <> '0' then
                                                set Query_Search = concat(Query_Search,' and c.customer_custgroup_gid = ',@Customer_Group_Gid,' ');
                                        elseif @Customer_Gid is not null or @Customer_Gid  <> '' or @Customer_Gid <> 0 then
													set Query_Search = concat(Query_Search,' and c.customer_gid = ',@Customer_Gid,' ');

                                       End if;

                   set Query_Select = '';
                   set @sno = 0;
                   set Query_Select =concat('select * from  (  select c.customer_gid,c.customer_custgroup_gid,a.fetsoutstanding_gid,
									c.customer_name,d.location_name, concat(c.customer_name,'' - '',d.location_name) as customer_display_name, f.employee_name,
                                    a.fetsoutstanding_invoiceno,date_format(a.fetsoutstanding_invoicedate,''%d-%m-%Y'') as fetsoutstanding_invoicedate, a.fetsoutstanding_netamount,
                                    ifnull(sum(b.fetsoutstandingdtl_amount),0) as paid,
									(a.fetsoutstanding_netamount - ifnull(sum(b.fetsoutstandingdtl_amount),0)) as balance_amount,
									( datediff(now(),a.fetsoutstanding_invoicedate)) as Due_Days,
									ifnull(max(b.fetsoutstandingdtl_receiveddate),''-'') as last_paid_date,
									(
									select sum(x.invoicedetails_qty) from gal_trn_tinvoiceheader as y
									inner join gal_trn_tinvoicedetails as x on x.invoicedetails_invoice_gid = y.invoiceheader_gid
									where y.invoiceheader_no = a.fetsoutstanding_invoiceno
									group by y.invoiceheader_gid
									) as total_sale_qty,
									case
										  when  ifnull(max(b.fetsoutstandingdtl_receiveddate),0) <> 0 then
											(   select z.fetsoutstandingdtl_amount from fet_trn_tfetsoutstandingdtl as z where z.fetsoutstandingdtl_fetsoutstanding_gid = a.fetsoutstanding_gid
												and z.fetsoutstandingdtl_receiveddate = max(b.fetsoutstandingdtl_receiveddate)  order by z.fetsoutstandingdtl_gid desc limit 1
											)
										  else 0
										end as ''last_paid_amount''  ,
										case
										  when  ifnull(max(b.fetsoutstandingdtl_receiveddate),0) <> 0 then
											(
											datediff(now(),max(b.fetsoutstandingdtl_receiveddate))
											)
										  else ''-''
										end as ''aging_days'',
									  case
										   when ( datediff(now(),a.fetsoutstanding_invoicedate)) <= 30 Then  ''<=30''
										   when ( datediff(now(),a.fetsoutstanding_invoicedate)) >= 31
											 and( datediff(now(),a.fetsoutstanding_invoicedate)) <= 45 Then ''30_45''
										   when ( datediff(now(),a.fetsoutstanding_invoicedate)) >= 46
											 and( datediff(now(),a.fetsoutstanding_invoicedate)) <= 60 Then  ''46_60''
										   when ( datediff(now(),a.fetsoutstanding_invoicedate)) >= 61
                                             and( datediff(now(),a.fetsoutstanding_invoicedate)) <= 75 Then  ''61_75''
										   when ( datediff(now(),a.fetsoutstanding_invoicedate)) >= 76
                                             and( datediff(now(),a.fetsoutstanding_invoicedate)) <= 90 Then   ''76_90''
										   when ( datediff(now(),a.fetsoutstanding_invoicedate)) >= 91
                                             and( datediff(now(),a.fetsoutstanding_invoicedate)) <= 120 Then  ''91_120''
										   when ( datediff(now(),a.fetsoutstanding_invoicedate)) >= 121
                                             and( datediff(now(),a.fetsoutstanding_invoicedate)) <= 150 Then  ''121_150''
										   when ( datediff(now(),a.fetsoutstanding_invoicedate)) >= 151
                                             and( datediff(now(),a.fetsoutstanding_invoicedate)) <= 180 Then  ''151_180''
										   when ( datediff(now(),a.fetsoutstanding_invoicedate)) >= 181 then  ''>=181''
										   else ( datediff(now(),a.fetsoutstanding_invoicedate))

									 end as Days,fetsoutstanding_status
									 from fet_trn_tfetsoutstanding as a
									left join fet_trn_tfetsoutstandingdtl as b on b.fetsoutstandingdtl_fetsoutstanding_gid = a.fetsoutstanding_gid
                                         and fetsoutstandingdtl_isremoved = ''N''
									inner join gal_mst_tcustomer as c on c.customer_gid = a.fetsoutstanding_customer_gid
                                         and c.customer_isactive =''Y'' and c.customer_isremoved = ''N''
									inner join gal_mst_tlocation as d on d.location_gid = c.customer_location_gid
                                         and d.location_isremoved =''N''
									inner join gal_map_tcustemp as e on e.custemp_customer_gid =  c.customer_gid
                                                 and e.custemp_isactive =''Y'' and e.custemp_isremoved =''N''
									inner join gal_mst_temployee as f on f.employee_gid = e.custemp_employee_gid
                                                 #and f.employee_isactive = ''Y''
                                                 and f.employee_isremoved = ''N''
									where a.fetsoutstanding_status <> ''PAID'' and a.fetsoutstanding_status <> ''CANCEL'' ',Query_Search,'  and a.entity_gid in (',@Entity_Gids,') and
                                    a.fetsoutstanding_isremoved = ''N'' and c.customer_gid not in (199,1174)
									group by customer_name,a.fetsoutstanding_invoiceno,datediff(now(),a.fetsoutstanding_invoicedate)

                                    ) as main_table

                                    inner join (
												select *,@sno := @sno+1 as sno from
											(
											Select fetsoutstanding_customer_gid as Vcustomer_gid,ac.customer_custgroup_gid as Vcustomer_custgroup_gid,
                                            ( datediff(now(),min(a.fetsoutstanding_invoicedate))) as VDue_Days
											 from fet_trn_tfetsoutstanding as a
                                             inner join gal_mst_tcustomer as ac on ac.customer_gid = a.fetsoutstanding_customer_gid
											 where  a.fetsoutstanding_status <> ''PAID'' and a.fetsoutstanding_status <> ''CANCEL''
											 and a.fetsoutstanding_isremoved = ''N''
											 group by ac.customer_custgroup_gid
											 ) as VMainTable
											 order by VDue_Days desc

											) as due_daysTable on due_daysTable.Vcustomer_custgroup_gid = main_table.customer_custgroup_gid
                                    order by sno,Due_Days desc,customer_name
                                    ');

				    set @Query_Select = Query_Select;
				   #select @Query_Select; ## Remove It.
					PREPARE stmt1 FROM @Query_Select;
					EXECUTE stmt1;
					Select found_rows() into li_count;
					DEALLOCATE PREPARE stmt1;

					if li_count > 0 then
							set Message = 'FOUND';
					else
							set Message = 'NOT_FOUND';
					end if;
 elseif ls_Type = 'OUTSTANDING_REPORT_INVOICE_WISE' and ls_Sub_Type = 'APPROVE' then
                               ### Show thw Data in FET Review and in Sales Approve.
                                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Customer_Gid[0]'))) into @Customer_Gid;
                                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Outstanding_Customer_Group_Gid[0]'))) into @Customer_Group_Gid;
                                    set Query_Search = '';

										if @Customer_Group_Gid is not null and @Customer_Group_Gid  <> '' and @Customer_Group_Gid <> 0 and @Customer_Group_Gid <> '0' then
                                                set Query_Search = concat(' and c.customer_custgroup_gid = ',@Customer_Group_Gid,' ');
                                        elseif @Customer_Gid is not null or @Customer_Gid  <> '' or @Customer_Gid <> 0 then
													set Query_Search = concat(' and c.customer_gid = ',@Customer_Gid,' ');
                                       End if;

                   set Query_Select = '';
                   set Query_Select =concat('select c.customer_gid,a.fetsoutstanding_gid,
									c.customer_name,d.location_name, concat(c.customer_name,'' - '',d.location_name) as customer_display_name, a.fetsoutstanding_invoiceno,
									date_format(a.fetsoutstanding_invoicedate,''%d-%m-%Y'') as fetsoutstanding_invoicedate, a.fetsoutstanding_netamount,
                                    ifnull(sum(b.fetsoutstandingdtl_amount),0) as paid,
									(a.fetsoutstanding_netamount - ifnull(sum(b.fetsoutstandingdtl_amount),0)) as balance_amount,fetsoutstanding_status
									 from fet_trn_tfetsoutstanding as a
									left join fet_trn_tfetsoutstandingdtl as b on b.fetsoutstandingdtl_fetsoutstanding_gid = a.fetsoutstanding_gid
                                         and fetsoutstandingdtl_isremoved = ''N''
									inner join gal_mst_tcustomer as c on c.customer_gid = a.fetsoutstanding_customer_gid
                                         and c.customer_isactive =''Y'' and c.customer_isremoved = ''N''
									inner join gal_mst_tlocation as d on d.location_gid = c.customer_location_gid
                                         and d.location_isremoved =''N''
									where a.fetsoutstanding_status <> ''PAID'' and a.fetsoutstanding_status <> ''CANCEL'' ',Query_Search,'   and a.fetsoutstanding_isremoved = ''N''
                                       and a.entity_gid in (',@Entity_Gids,')
									group by customer_name,fetsoutstanding_invoiceno,datediff(now(),a.fetsoutstanding_invoicedate)
                                    ');

				    set @Query_Select = Query_Select;
				   #select @Query_Select; ## Remove It.
					PREPARE stmt1 FROM @Query_Select;
					EXECUTE stmt1;
					Select found_rows() into li_count;
					DEALLOCATE PREPARE stmt1;

					if li_count > 0 then
							set Message = 'FOUND';
					else
							set Message = 'NOT_FOUND';
					end if;

elseif ls_Type = 'OUTSTANDING_REPORT' and ls_Sub_Type = 'BUCKET_CUSTOMER_WISE' then

									select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Customer_Gid'))) into @Customer_Gid;
                                    set Query_Search = '';
                                       if @Customer_Gid is not null or @Customer_Gid  <> '' or @Customer_Gid <> 0 then
												set Query_Search = '';
                                                set Query_Search = concat(' and c.customer_gid = ',@Customer_Gid,' ');
                                       End if;


                   set Query_Select = '';
                   set Query_Select =concat('select c.customer_gid,
											c.customer_name,d.location_name,f.employee_gid,f.employee_name,
											sum(a.fetsoutstanding_netamount) as net_amount,ifnull(sum(b.fetsoutstandingdtl_amount),0) as paid,
											(sum(a.fetsoutstanding_netamount) - ifnull(sum(b.fetsoutstandingdtl_amount),0)) as balance_amount,
											ifnull(max(b.fetsoutstandingdtl_receiveddate),''-'') as last_paid_date,

											case
												 when  ifnull(max(b.fetsoutstandingdtl_receiveddate),0) <> 0 then
												   (   select ifnull(z.fetsoutstandingdtl_amount,0) from fet_trn_tfetsoutstandingdtl as z
															inner join fet_trn_tfetsoutstanding as y on y.fetsoutstanding_gid = z.fetsoutstandingdtl_fetsoutstanding_gid
												   where y.fetsoutstanding_customer_gid = c.customer_gid
													   and z.fetsoutstandingdtl_receiveddate = max(b.fetsoutstandingdtl_receiveddate)
													   order by z.fetsoutstandingdtl_gid desc limit 1
												   )
												 else 0
											   end as ''last_paid_amount''  ,
											   case
												 when  ifnull(max(b.fetsoutstandingdtl_receiveddate),0) <> 0 then
												   (
												   datediff(now(),max(b.fetsoutstandingdtl_receiveddate))
												   )
												 else ''-''
											   end as ''aging_days'',
												case
													when  ifnull(max(b.fetsoutstandingdtl_receiveddate),0) <> 0 then
													   (
													   fn_OustandingBucket(''CUSTOMER_OUTSTANDING_BUCKET'',0,''2019-01-01'',c.customer_gid)
													   )
													 else 0
												end as ''outstanding_bucket''
											from fet_trn_tfetsoutstanding as a
											left join fet_trn_tfetsoutstandingdtl as b on b.fetsoutstandingdtl_fetsoutstanding_gid = a.fetsoutstanding_gid
												 and b.fetsoutstandingdtl_isremoved = ''N''
											inner join gal_mst_tcustomer as c on c.customer_gid = a.fetsoutstanding_customer_gid
                                                 and c.customer_isactive =''Y'' and c.customer_isremoved = ''N''
											inner join gal_mst_tlocation as d on d.location_gid = c.customer_location_gid
                                                 and d.location_isremoved =''N''
                                            inner join gal_map_tcustemp as e on e.custemp_customer_gid =  c.customer_gid
                                                 and e.custemp_isactive =''Y'' and e.custemp_isremoved =''N''
											inner join gal_mst_temployee as f on f.employee_gid = e.custemp_employee_gid
                                                 and f.employee_isactive = ''Y'' and f.employee_isremoved = ''N''
											where a.fetsoutstanding_status <> ''PAID'' and a.fetsoutstanding_status <> ''CANCEL'' ',Query_Search,' and a.fetsoutstanding_isremoved = ''N''
                                               and a.entity_gid in (',@Entity_Gids,')
											group by c.customer_gid,
											c.customer_name,d.location_name limit 10');

				    set @Query_Select = Query_Select;
				   #select @Query_Select; ## Remove It.
					PREPARE stmt1 FROM @Query_Select;
					EXECUTE stmt1;
					Select found_rows() into li_count;
					DEALLOCATE PREPARE stmt1;

					if li_count > 0 then
							set Message = 'FOUND';
					else
							set Message = 'NOT_FOUND';
					end if;

 elseif ls_Type = 'OUTSTANDING_POSITION' and ls_Sub_Type = 'FET_REVIEW' then

                                select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Customer_Gid'))) into @Customer_Gid;
                                    set Query_Search = '';
                                       if @Customer_Gid is not null or @Customer_Gid  <> '' or @Customer_Gid <> 0 then
												set Query_Search = '';
                                                set Query_Search = concat(' and b.customer_gid = ',@Customer_Gid,' ');
                                       End if;

                   set Query_Select = '';
                   set Query_Select =concat('Select b.customer_name,date_format(a.fetsoutstanding_invoicedate,''%Y-%b'') as Outstanding_Month,
									count(a.fetsoutstanding_gid) as no_of_inv ,
									(sum(a.fetsoutstanding_netamount) - ifnull(sum(c.fetsoutstandingdtl_amount),0)) Sum_Outsatnding_Month
									from fet_trn_tfetsoutstanding as a
									inner join gal_mst_tcustomer as b on b.customer_gid = a.fetsoutstanding_customer_gid
									left join fet_trn_tfetsoutstandingdtl as c on c.fetsoutstandingdtl_fetsoutstanding_gid = a.fetsoutstanding_gid and c.fetsoutstandingdtl_isremoved = ''N''
									where a.fetsoutstanding_status <>''PAID''
									and a.fetsoutstanding_isremoved = ''N''
									and b.customer_isactive = ''Y'' and b.customer_isremoved = ''N''
                                    ',Query_Search,' and a.entity_gid  in (',@Entity_Gids,')
									Group by date_format(a.fetsoutstanding_invoicedate,''%Y-%b''),a.fetsoutstanding_customer_gid');

				    set @Query_Select = Query_Select;
				   #select @Query_Select; ## Remove It.
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
        set Message = 'Incorrect Type';
 End if;
end if;

END