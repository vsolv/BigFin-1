CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Report_Customer_Performance`(
in `Type` varchar(64),
in `Sub_Type` varchar(64),
in  `lj_filter` json,
in `lj_classification` json,
out `Message` varchar(64)
)
sp_Report_Customer:BEGIN
#Akshay--------june 15 2019
#karthiga --- edited -- sales -- isremove-- feb 14 20
declare Query_select text;
declare Query_search text;
declare Query_search1 text;
declare Query_search2 text;
declare i int;
declare li_count int;

if Type='Customer_Performance' and  Sub_Type='Total_Sales' then

	select JSON_LENGTH(lj_filter,'$') into @lj_filter_count;

	if @lj_filter_count  is  null or @lj_filter_count =0 or @lj_filter_count ='' then
	set Message='NO Json lj_filter is present';
	leave sp_Report_Customer;
	end if;

	select JSON_LENGTH(lj_classification,'$') into @lj_classification_count;

    if @lj_classification_count  is  null or @lj_classification_count =0 or @lj_classification_count ='' then
	set Message='NO Json lj_classification is present';
	leave sp_Report_Customer;
	end if;


    select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,'$.Executive_gid')) into @Executive_gid;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,'$.Customer_gid')) into @Customer_gid;
    select JSON_LENGTH(lj_filter,'$.Month') into @lj_filter_Month;
	set @REF_Gid=0;
	select fn_REFGid('CREDITNOTE_RECEIPT') into @REF_Gid;
    drop temporary Table if exists MonthDate_Wise;
	create temporary table MonthDate_Wise (
								monthid   int,
                               monthdate date
                       );


     set i=0;
     while(i<@lj_filter_Month) do
		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Month[0]'))) into @Month2;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Month[',i,']'))) into @Month1;
		insert into MonthDate_Wise(monthid,monthdate) values(i+1,@Month1);
		set i=i+1;
   end while;

	select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,'$.Entity_Gid[0]')) into @Entity_Gid;


     set Query_search2='';

    if @Executive_gid is not null and @Executive_gid <> '' then
		set Query_search2=concat(Query_search2,'  and t.employee_gid=',@Executive_gid,'');
    end if;

       if @Customer_gid is not null and @Customer_gid <> '' then
		set Query_search2=concat(Query_search2,'  and t.custgid=',@Customer_gid,'');
    end if;




					set Query_select='';

					set Query_select=concat('select  t.custgid,t.execname as employee_name,t.custname as customer_name,t.customer_status,t.custcategory_name,
															concat(t.custname,''-'',t.location_name) as branch_name,t.create_date,t.dept_name,t.location_name,t.mntdate,t.invdate,
															t.monthid,t.invtot,t.reptamt,t.cramt,t.outstanding,
															@custname:=if(t.monthid=1,@ost:=ifnull(t.outstanding,0)+(case when t.invtot is null then 0 else t.invtot end  -
															(case when t.reptamt is null then 0 else t.reptamt end + case when t.cramt is null then 0 else t.cramt end)),
															@ost:=@ost+(case when t.invtot is null then 0 else t.invtot end  - (case when t.reptamt is null then 0 else t.reptamt end
															+case when t.cramt is null then 0 else t.cramt end))) as oss
															from (select @rt:=0,@ost:=0,@custname='''') i join
															(
															select m.execname,
															m.employee_gid,
															m.custname,
															m.custgid,
															m.customer_status,
															m.custcategory_name,
															m.create_date,
															m.dept_name,
															m.location_name,
															m.mntdate,
															m.monthid,
															inv.invdate,
															m.entity_gid,
															ifnull(inv.invtot,0) as invtot,
															ifnull(rept.amt,0) as reptamt,
															ifnull(crnt.amt,0) as cramt ,
															ifnull(os.outamt,0) as outamt ,
															t2.outstanding
															from
															(select b.customer_gid as custgid,b.customer_name as custname,b.entity_gid as entity_gid,b.customer_isactive as customer_status,
															e.employee_name as execname,e.employee_gid as employee_gid,c.custcategory_name as custcategory_name,
															date_format(b.create_date,''%Y-%b-%d'') as create_date,f.dept_name as dept_name,g.location_name as location_name,
															md.monthid,date_format(md.monthdate,''%m-%Y'') as mntdate from MonthDate_Wise md
															join gal_mst_tcustomer as b
															inner join gal_mst_tcustcategory as c on c.custcategory_gid=b.customer_category_gid
															inner join gal_map_tcustemp as d on d.custemp_customer_gid =b.customer_gid
															inner join gal_mst_temployee as e on e.employee_gid=d.custemp_employee_gid
															inner join gal_mst_tdept as f on f.dept_gid=e.employee_dept_gid
															inner join gal_mst_tlocation as g on g.location_gid=b.customer_location_gid and d.custemp_isactive=''Y''
															and e.employee_isactive=''Y'' and customer_isactive=''Y'' and custcategory_isactive=''Y''
															) m
															left join
															(
															select b.invoiceheader_customer_gid as cust_gid,date_format(b.invoiceheader_date,''%m-%Y'') as invdate,
																sum(invoiceheader_total) as invtot from gal_trn_tinvoiceheader b
															where b.invoiceheader_status not in (''CANCEL'') and invoiceheader_isremoved=''N''
																group by date_format(b.invoiceheader_date,''%m-%Y''),b.invoiceheader_customer_gid
															) as inv
															on inv.invdate=m.mntdate and m.custgid=inv.cust_gid
															left join
															(
															select ir.invreceipt_invoicegid as invrecgid,ih.invoiceheader_customer_gid as cust_gid,
															date_format(ir.invreceipt_date,''%m-%Y'') as irdate,sum(ir.invreceipt_amount) as amt
															from gal_map_tinvreceipt ir inner join gal_trn_tinvoiceheader ih
															on ih.invoiceheader_gid=ir.invreceipt_invoicegid inner join gal_mst_tcustomer ic
															on ih.invoiceheader_customer_gid=ic.customer_gid
															where
															ir.invreceipt_refgid not in (41,46,47,49,71,35)
                                                            and ir.invreceipt_type=1 and invoiceheader_isremoved=''N'' and customer_isactive=''Y''
															group by date_format(ir.invreceipt_date,''%m-%Y''),ih.invoiceheader_customer_gid
															order by ih.invoiceheader_date
															) as rept
															on irdate=m.mntdate and m.custgid=rept.cust_gid
															left join
															(
															select cr.invreceipt_invoicegid as invrecgid,ch.invoiceheader_customer_gid as cust_gid,
															date_format(cr.invreceipt_date,''%m-%Y'') as crdate,sum(cr.invreceipt_amount) as amt
															from gal_map_tinvreceipt cr inner join gal_trn_tinvoiceheader ch
															on ch.invoiceheader_gid=cr.invreceipt_invoicegid inner join gal_mst_tcustomer cc
															on ch.invoiceheader_customer_gid=cc.customer_gid
															where
                                                            cr.invreceipt_refgid in (41,46,47,49,71,35)
                                                            and cr.invreceipt_type=1 and invoiceheader_isremoved=''N'' and customer_isactive=''Y''
															group by date_format(cr.invreceipt_date,''%m-%Y''),ch.invoiceheader_customer_gid
															order by ch.invoiceheader_date
															) as crnt
															on crdate=m.mntdate and m.custgid=crnt.cust_gid
															left join
															(
															select date_format(fetsoutstandingdtl_receiveddate,''%m-%Y'') as ordate,
															fetsoutstanding_customer_gid as cust_gid,
															(sum(fetsoutstanding_netamount)-sum(fetsoutstandingdtl_amount) ) as outamt
															from fet_trn_tfetsoutstanding
                                                            left join fet_trn_tfetsoutstandingdtl on
															fetsoutstanding_gid=fetsoutstandingdtl_fetsoutstanding_gid and fetsoutstandingdtl_isremoved=''N'' and fetsoutstanding_isremoved=''N''
															group by date_format(fetsoutstandingdtl_receiveddate,''%m-%Y''),fetsoutstanding_customer_gid
															) as os
															on ordate=m.mntdate and m.custgid=os.cust_gid
															left join
															(
															select oscustgid,(ifnull(oss.osamt,0)-ifnull(dtl.dtlamt,0)) as outstanding from
																#select oscustgid,oss.osamt-dtl.dtlamt as outstanding from
															(select fetsoutstanding_customer_gid as oscustgid,
															sum(ifnull(fetsoutstanding_netamount,0)) as osamt from fet_trn_tfetsoutstanding where
															fetsoutstanding_status not in (''CANCEL'') and fetsoutstanding_invoicedate< ''',@Month2,''' and fetsoutstanding_isremoved=''N''
															group by fetsoutstanding_customer_gid
															) as oss left join
																	(
															select a.fetsoutstanding_netamount,a.fetsoutstanding_customer_gid custgid,sum(b.fetsoutstandingdtl_amount) dtlamt
															from fet_trn_tfetsoutstanding a
															left join  fet_trn_tfetsoutstandingdtl b on a.fetsoutstanding_gid=b.fetsoutstandingdtl_fetsoutstanding_gid and fetsoutstandingdtl_isremoved=''N''
															where
															b.fetsoutstandingdtl_receiveddate< ''',@Month2,''' and
															a.fetsoutstanding_status not in (''CANCEL'') and fetsoutstanding_isremoved=''N''
															group by a.fetsoutstanding_customer_gid
															) as dtl on dtl.custgid =oss.oscustgid) t2 on m.custgid=t2.oscustgid
															) as t  where t.entity_gid=1 ',Query_search2,'
															order by t.custgid,t.monthid,t.mntdate');

                                            set @p= Query_select;
                                            #select @p;#---------remove
                                           PREPARE stmt FROM @p;
										  EXECUTE stmt;
										  DEALLOCATE PREPARE stmt;
										  select found_rows() into  li_count;

										  if  li_count >0 then

											set  Message='FOUND';
										  else
											set Message='NOT_FOUND';
										  end if;



end if;


 if Type='Customer_Performance' and  Sub_Type='Total_Receipt' then

		select JSON_LENGTH(lj_filter,'$') into @lj_filter_count;

		if @lj_filter_count  is  null or @lj_filter_count =0 or @lj_filter_count ='' then
		set Message='NO Json lj_filter is present';
		leave sp_Report_Customer;
		end if;

        select JSON_LENGTH(lj_classification,'$') into @lj_classification_count;

		if @lj_classification_count  is  null or @lj_classification_count =0 or @lj_classification_count ='' then
		set Message='NO Json lj_classification is present';
		leave sp_Report_Customer;
		end if;


	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,'$.From_date')) into @from_date;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,'$.To_date')) into @to_date;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,'$.Entity_Gid[0]')) into @Entity_Gid;

    set @REF_Gid1=0;
	select fn_REFGid('COLLECTION_RECEIPT') into @REF_Gid1;

    set Query_search='';
	if @from_date is not null and @from_date <> '' then
		set @from1_date=date_format(@from_date,'%Y-%m-%d');
		set Query_search=concat(Query_search,'  and i.invreceipt_date >=' '''',@from1_date,'''');
    else
		set Query_search=concat(Query_search,'  and i.invreceipt_date >=' '''',now()-interval 6 month,'''');
    end if;

	if @to_date is not null and @to_date <> '' then
		set @to1_date=date_format(@to_date,'%Y-%m-%d');
		set Query_search=concat(Query_search,'  and i.invreceipt_date <=' '''',@to1_date,'''');
    else
		set Query_search=concat(Query_search,'  and i.invreceipt_date <=' '''',now(),'''');
    end if;

    set Query_select='';

    set Query_select=concat('select
												customer_gid,
												customergroup_name,
												concat(customer_name,''-'',location_name) as customer_name,
												employee_name,
												dept_name,
												custcategory_name,
												location_name,
												invoiceheader_gid,
												invreceipt_invoicegid,
												sum(invreceipt_amount) as receipt_note,
												date_format(invreceipt_date,''%Y-%b'') as  invreceipt_date
												 from gal_mst_tcustomergroup as a
												inner join gal_mst_tcustomer as b on b.customer_custgroup_gid=a.customergroup_gid
												and a.customergroup_isactive=''Y'' and a.customergroup_isremoved=''N'' and a.entity_gid=',@Entity_Gid,'
												and b.customer_isactive=''Y'' and b.customer_isremoved=''N'' and b.entity_gid=',@Entity_Gid,'
												inner join gal_mst_tcustcategory as c on c.custcategory_gid=b.customer_category_gid
												and  c.custcategory_isactive=''Y''  and  c.custcategory_isremoved=''N'' and c.entity_gid=',@Entity_Gid,'
												inner join gal_map_tcustemp as d on d.custemp_customer_gid=b.customer_gid
												and d.custemp_isactive=''Y'' and d.custemp_isremoved=''N'' and d.entity_gid=',@Entity_Gid,'
												inner join gal_mst_temployee as e on e.employee_gid=d.custemp_employee_gid
												and e.employee_isactive=''Y'' and e.employee_isremoved=''N'' and e.entity_gid=',@Entity_Gid,'
												inner join gal_mst_tdept as f on f.dept_gid=d.custemp_dept_gid
												and f.dept_isactive=''Y'' and f.dept_isremoved=''N'' and f.entity_gid=',@Entity_Gid,'
												inner join gal_mst_tlocation as g on g.location_gid=b.customer_location_gid
												and g.location_isremoved=''N'' and g.entity_gid=',@Entity_Gid,'
												left join gal_trn_tinvoiceheader as h on h.invoiceheader_customer_gid=b.customer_gid
												and h.invoiceheader_isremoved=''N'' and  h.entity_gid=',@Entity_Gid,'
												inner join gal_map_tinvreceipt as i on i.invreceipt_invoicegid=h.invoiceheader_gid
												',Query_search,'
												and  invreceipt_refgid=',@REF_Gid1,'

												group by customer_gid,date_format(invreceipt_date,''%Y-%m'')
												order by customer_gid
												');

                                                 set @p= Query_select;
										   #select @p;#---------remove
                                           PREPARE stmt FROM @p;
										  EXECUTE stmt;
										  DEALLOCATE PREPARE stmt;
										  select found_rows() into  li_count;

										  if  li_count >0 then
                                          #select 1;
											set  Message='FOUND';
										  else
											set Message='NOT_FOUND';
										  end if;





end if;

 if Type='Customer_Performance' and  Sub_Type='Total_Credit' then

		select JSON_LENGTH(lj_filter,'$') into @lj_filter_count;

		if @lj_filter_count  is  null or @lj_filter_count =0 or @lj_filter_count ='' then
		set Message='NO Json lj_filter is present';
		leave sp_Report_Customer;
		end if;

        select JSON_LENGTH(lj_classification,'$') into @lj_classification_count;

		if @lj_classification_count  is  null or @lj_classification_count =0 or @lj_classification_count ='' then
		set Message='NO Json lj_classification is present';
		leave sp_Report_Customer;
		end if;


	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,'$.From_date')) into @from_date;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,'$.To_date')) into @to_date;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,'$.Entity_Gid[0]')) into @Entity_Gid;

    set @REF_Gid1=0;
	select fn_REFGid('CREDITNOTE_RECEIPT') into @REF_Gid1;

    set Query_search='';
	if @from_date is not null and @from_date <> '' then
		set @from1_date=date_format(@from_date,'%Y-%m-%d');
		set Query_search=concat(Query_search,'  and i.invreceipt_date >=' '''',@from1_date,'''');
    else
		set Query_search=concat(Query_search,'  and i.invreceipt_date >=' '''',now()-interval 6 month,'''');
    end if;

	if @to_date is not null and @to_date <> '' then
		set @to1_date=date_format(@to_date,'%Y-%m-%d');
		set Query_search=concat(Query_search,'  and i.invreceipt_date <=' '''',@to1_date,'''');
    else
		set Query_search=concat(Query_search,'  and i.invreceipt_date <=' '''',now(),'''');
    end if;

    set Query_select='';

    set Query_select=concat('select
												customer_gid,
												customergroup_name,
												concat(customer_name,''-'',location_name) as customer_name,
												employee_name,
												dept_name,
												custcategory_name,
												location_name,
												invoiceheader_gid,
                                                invreceipt_invoicegid,
                                                date_format(invreceipt_date,''%Y-%b'') as invreceipt_date,
												sum(invreceipt_amount) as Credit_note
												 from gal_mst_tcustomergroup as a
												inner join gal_mst_tcustomer as b on b.customer_custgroup_gid=a.customergroup_gid
												and a.customergroup_isactive=''Y'' and a.customergroup_isremoved=''N'' and a.entity_gid=',@Entity_Gid,'
												and b.customer_isactive=''Y'' and b.customer_isremoved=''N'' and b.entity_gid=',@Entity_Gid,'
												inner join gal_mst_tcustcategory as c on c.custcategory_gid=b.customer_category_gid
												and  c.custcategory_isactive=''Y''  and  c.custcategory_isremoved=''N'' and c.entity_gid=',@Entity_Gid,'
												inner join gal_map_tcustemp as d on d.custemp_customer_gid=b.customer_gid
												and d.custemp_isactive=''Y'' and d.custemp_isremoved=''N'' and d.entity_gid=',@Entity_Gid,'
												inner join gal_mst_temployee as e on e.employee_gid=d.custemp_employee_gid
												and e.employee_isactive=''Y'' and e.employee_isremoved=''N'' and e.entity_gid=',@Entity_Gid,'
												inner join gal_mst_tdept as f on f.dept_gid=d.custemp_dept_gid
												and f.dept_isactive=''Y'' and f.dept_isremoved=''N'' and f.entity_gid=',@Entity_Gid,'
												inner join gal_mst_tlocation as g on g.location_gid=b.customer_location_gid
												and g.location_isremoved=''N'' and g.entity_gid=',@Entity_Gid,'
												left join gal_trn_tinvoiceheader as h on h.invoiceheader_customer_gid=b.customer_gid
												and h.invoiceheader_isremoved=''N'' and  h.entity_gid=',@Entity_Gid,'
												inner join gal_map_tinvreceipt as i on i.invreceipt_invoicegid=h.invoiceheader_gid
												',Query_search,'
												and  invreceipt_refgid=',@REF_Gid1,'

												group by customer_gid,date_format(invreceipt_date,''%Y-%m'')
												order by customer_gid
												');

                                                 set @p= Query_select;
										   #select @p;#---------remove
                                           PREPARE stmt FROM @p;
										  EXECUTE stmt;
										  DEALLOCATE PREPARE stmt;
										  select found_rows() into  li_count;

										  if  li_count >0 then
                                          #select 1;
											set  Message='FOUND';
										  else
											set Message='NOT_FOUND';
										  end if;





end if;


END