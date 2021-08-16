CREATE DEFINER=`developer`@`%` PROCEDURE `galley`.`sp_FAAssetProcess_Get`(IN `ls_Type` varchar(64),IN `ls_Sub_Type` varchar(64),
IN `lj_Filters` json,IN `lj_Classification` json, OUT `Message` varchar(1024))
sp_FAAssertProcess_Get:BEGIN
### Ramesh Sep 18 2019 - Created
Declare Query_Select varchar(6144);
Declare Query_Search varchar(1024);
Declare Query_Search1 varchar(1024);
Declare Query_Where varchar(2048);
Declare Query_Limit varchar(500);
declare errno int;
declare msg varchar(1000);
declare li_count int;

# Null Selected Output
DECLARE done INT DEFAULT 0;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
#....

	DECLARE EXIT HANDLER FOR SQLEXCEPTION,sqlwarning

    BEGIN
		GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
		set Message = concat(errno , msg);
		ROLLBACK;
    END;

   SET SESSION group_concat_max_len=4294967295;

select fn_Classification('ENTITY_ONLY',lj_Classification) into @OutMsg_Classification ;
        select  JSON_UNQUOTE(JSON_EXTRACT(@OutMsg_Classification, '$.Entity_Gid[0]')) into @Entity_Gids;
        if @Entity_Gids is  null or @Entity_Gids = '' then
				select  JSON_UNQUOTE(JSON_EXTRACT(@OutMsg_Classification, '$.Message')) into @Message;
				set Message = concat('Error On Classification Data - ',@Message);
                leave sp_FAAssertProcess_Get;
        End if;

if ls_Type = 'ASSERT_MAKER' and ls_Sub_Type = 'SUMMARY' then

            select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Id'))) into @Asset_Id;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.Asset_Value'))) into @Asset_Value;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.Cap_Date'))) into @Asset_CP_Date;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.Asset_Code'))) into @Category_Name;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.Branch'))) into @Branch_Name;


  # select @Asset_Id,@Asset_Value,@Asset_CP_Date,@Category_Name,@Branch_Name;

                    set Query_Search = '';

                    if @Asset_Id <> '' and @Asset_Id is not null  then
                         set Query_Search = concat(Query_Search,' and a.assetdetails_id like ''','%',@Asset_Id,'%','''  ');
                    End if;

                    if @Asset_Value <> '' and @Asset_Value is not null then
                         set Query_Search = concat(Query_Search,' and a.assetdetails_value like ''','%',@Asset_Value,'%','''  ');
                    End if;

					if @Asset_CP_Date <> '' and @Asset_CP_Date is not null  then
                        set Query_Search = concat(Query_Search,'and date_format(a.assetdetails_capdate,''%Y-%m-%d'') = ''',@Asset_CP_Date,'''  ');
                    End if;

                    if @Category_Name <> '' and @Category_Name is not null  then
                         set Query_Search = concat(Query_Search,' and g.assetcat_subcatname like ''','%',@Category_Name,'%','''  ');
                    End if;

                     if @Branch_Name <> '' and @Branch_Name is not null  then
                         set Query_Search = concat(Query_Search,' and b.branch_name like ''','%',@Branch_Name,'%','''  ');
                    End if;
			#select Query_Search;

				set Query_Select = '';
                set Query_Select = concat('
							Select a.assetdetails_gid,a.assetdetails_id,a.assetdetails_value,
                            date_format(a.assetdetails_capdate,''%Y-%b-%d'') as assetdetails_capdate,
                            a.assetdetails_branchgid,a.assetdetails_status,b.branch_name,a.assetdetails_vendorname,
                            fn_Asset_Data(''ASSET_TMP'',a.assetdetails_gid,a.entity_gid,''{}'') as lj_default_details,
                            g.assetcat_subcatname
							from fa_tmp_tassetdetails as a
                            inner join gal_mst_tbranch as b on b.branch_gid = a.assetdetails_branchgid
                            inner join fa_mst_tassetcat as g on g.assetcat_gid = a.assetdetails_assetcatgid
                            where a.assetdetails_isactive = ''Y'' and a.assetdetails_isremoved = ''N''
                             and b.branch_isactive = ''Y'' and b.branch_isremoved = ''N''
                             and g.assetcat_isactive= ''Y'' and g.assetcat_isremoved = ''N''
                            ',Query_Search,' and a.entity_gid in (',@Entity_Gids,') and b.entity_gid in (',@Entity_Gids,')
											 and g.entity_gid in (',@Entity_Gids,')
							');
                     	set @Query_Select = Query_Select;
			      		#select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;

elseif ls_Type = 'ASSERT_CHECKER' and ls_Sub_Type = 'SUMMARY' then


			select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Id'))) into @Asset_Id;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.Asset_Value'))) into @Asset_Value;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.Cap_Date'))) into @Asset_CP_Date;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.Asset_Code'))) into @Category_Name;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.Branch'))) into @Branch_Name;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.Asset_Group'))) into @lc_Asset_Group;


                 set Query_Search = '';

                    if @Asset_Id <> '' and @Asset_Id is not null  then
                         set Query_Search = concat(Query_Search,' and a.assetdetails_id like ''','%',@Asset_Id,'%','''  ');
                    End if;

                    if @Asset_Value <> '' and @Asset_Value is not null then
                         set Query_Search = concat(Query_Search,' and a.assetdetails_value like ''','%',@Asset_Value,'%','''  ');
                    End if;

					if @Asset_CP_Date <> '' and @Asset_CP_Date is not null  then
                        set Query_Search = concat(Query_Search,'and date_format(a.assetdetails_capdate,''%Y-%m-%d'') = ''',@Asset_CP_Date,'''  ');
                    End if;

                    if @Category_Name <> '' and @Category_Name is not null  then
                         set Query_Search = concat(Query_Search,' and g.assetcat_subcatname like ''','%',@Category_Name,'%','''  ');
                    End if;

                     if @Branch_Name <> '' and @Branch_Name is not null  then
                         set Query_Search = concat(Query_Search,' and b.branch_name like ''','%',@Branch_Name,'%','''  ');
                    End if;

           # select Query_Search;


            if @lc_Asset_Group = 'Y' then
			   set Query_Select = '';
			   set Query_Select = concat('
							Select assetdetails_assetgroupid,group_concat(a.assetdetails_gid) as assetdetails_gids,sum(a.assetdetails_value) as asset_value ,
                            date_format(a.assetdetails_capdate,''%Y-%b-%d'') as assetdetails_capdate,
                            a.assetdetails_branchgid,a.assetdetails_status,b.branch_name,a.assetdetails_vendorname,
                            count(a.assetdetails_gid) as asset_count,
                            fn_Asset_Data(''ASSET_TMP'',a.assetdetails_gid,a.entity_gid,''{}'') as lj_default_details,
                            g.assetcat_subcatname
							from fa_tmp_tassetdetails as a
                             inner join gal_mst_tbranch as b on b.branch_gid = a.assetdetails_branchgid
                             inner join fa_mst_tassetcat as g on g.assetcat_gid = a.assetdetails_assetcatgid
                            and b.branch_isactive = ''Y'' and b.branch_isremoved = ''N''
                            where assetdetails_isactive = ''Y'' and assetdetails_isremoved = ''N''
                            and a.assetdetails_requestfor = ''NEW''
                            and g.assetcat_isactive= ''Y'' and g.assetcat_isremoved = ''N''
                            ',Query_Search,' and a.entity_gid in (',@Entity_Gids,') and g.entity_gid in (',@Entity_Gids,')
                            Group by a.assetdetails_assetgroupid
							');
            elseif @lc_Asset_Group = 'N' then
							set Query_Select = concat('
							Select a.assetdetails_gid,a.assetdetails_id,a.assetdetails_value,
                            date_format(a.assetdetails_capdate,''%Y-%b-%d'') as assetdetails_capdate,
                            a.assetdetails_branchgid,a.assetdetails_status,b.branch_name,a.assetdetails_vendorname,
                            fn_Asset_Data(''ASSET_TMP'',a.assetdetails_gid,a.entity_gid,''{}'') as lj_default_details,
							g.assetcat_subcatname
							from fa_tmp_tassetdetails as a
                            inner join gal_mst_tbranch as b on b.branch_gid = a.assetdetails_branchgid
                            inner join fa_mst_tassetcat as g on g.assetcat_gid = a.assetdetails_assetcatgid
                            and b.branch_isactive = ''Y'' and b.branch_isremoved = ''N''
                            and a.assetdetails_requestfor = ''NEW''

                            where assetdetails_isactive = ''Y'' and assetdetails_isremoved = ''N''
                             and g.assetcat_isactive= ''Y'' and g.assetcat_isremoved = ''N''
                            ',Query_Search,' and a.entity_gid in (',@Entity_Gids,') and g.entity_gid in (',@Entity_Gids,')
							');
            End if;


                     	set @Query_Select = Query_Select;
			      			#select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;

  elseif ls_Type = 'ASSERT_CHECKER' and ls_Sub_Type = 'DETAILS' then
         ### To DO search
            select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, '$.Asset_Id')) into @Asset_Id;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.Asset_Value'))) into @Asset_Value;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.Cap_Date'))) into @Cap_Date;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.Asset_Code'))) into @Asset_Code;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.Branch'))) into @Branch;

            select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.Asset_Group_ID'))) into @Asset_Group_ID;
                  select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Page_Index'))) into @Page_Index;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Page_Size'))) into @Page_Size;

           #select @Asset_Group_ID,@Asset_Id,@Asset_Value,@Asset_CP_Date,@Category_Name,@Branch_Name;

            set Query_Search = '';
           set Query_Limit = '';
            ### Changed - if used this a Common One

            if @Asset_Group_ID is not null or @Asset_Group_ID <> 0 then
               set Query_Search = concat(Query_Search, ' and a.assetdetails_assetgroupid = ',@Asset_Group_ID,' ' );
            End if;

					if @Asset_Id <> '' and @Asset_Id is not null  then
                         set Query_Search = concat(Query_Search,' and a.assetdetails_id like ''','%',@Asset_Id,'%','''  ');
                    End if;

                    if @Asset_Value <> '' and @Asset_Value is not null then
                         set Query_Search = concat(Query_Search,' and a.assetdetails_value like ''','%',@Asset_Value,'%','''  ');
                    End if;

					if @Asset_CP_Date <> '' and @Asset_CP_Date is not null  then
                        set Query_Search = concat(Query_Search,'and date_format(a.assetdetails_capdate,''%Y-%m-%d'') = ''',@Asset_CP_Date,'''  ');
                    End if;

                    if @Category_Name <> '' and @Category_Name is not null  then
                         set Query_Search = concat(Query_Search,' and g.assetcat_subcatname like ''','%',@Category_Name,'%','''  ');
                    End if;

                     if @Branch_Name <> '' and @Branch_Name is not null  then
                         set Query_Search = concat(Query_Search,' and b.branch_name like ''','%',@Branch_Name,'%','''  ');
                    End if;
            set Query_Search = concat(Query_Search,'and assetdetails_requestfor = ''NEW''  and assetdetails_requeststatus = ''REQUESTED'' ');

             if @Page_Index <> '' and @Page_Index is not null and @Page_Size <> '' and @Page_Size is not null  then
                         set @total_size= @Page_Index*@Page_Size;
                         set Query_Limit = concat(Query_Limit,' LIMIT ',@Page_Size,' OFFSET ',@total_size,'  ');
                    End if;

                set Query_Select ='';
                set Query_Where = '';
                set Query_Select = concat('
							Select a.assetdetails_gid,a.assetdetails_id,a.assetdetails_value,
                            date_format(a.assetdetails_capdate,''%Y-%b-%d'') as assetdetails_capdate,
                            a.assetdetails_branchgid,a.assetdetails_status,a.assetdetails_imagepath,b.branch_name,
                            h.product_name,@Total_Row ');

					set Query_Where = concat('from fa_tmp_tassetdetails as a
                            inner join gal_mst_tbranch as b on b.branch_gid = a.assetdetails_branchgid
							inner join fa_mst_tassetcat as g on g.assetcat_gid = a.assetdetails_assetcatgid
                            inner join gal_mst_tproduct as h on h.product_gid = a.assetdetails_productgid
                            where assetdetails_isactive = ''Y'' and assetdetails_isremoved = ''N''
                             and b.branch_isactive = ''Y'' and b.branch_isremoved = ''N''
                             and g.assetcat_isactive= ''Y'' and g.assetcat_isremoved = ''N''
                             and h.product_isactive = ''Y'' and h.product_isremoved = ''N''
                            ',Query_Search,' and a.entity_gid in (',@Entity_Gids,') and g.entity_gid in (',@Entity_Gids,') ');

                        set @Query_Count = '';
                        set @Query_Count = concat('Select count(assetdetails_gid) into @Total_Row ',Query_Where);
                          	PREPARE stmt FROM @Query_Count;
								EXECUTE stmt;
							DEALLOCATE PREPARE stmt;

                     	set @Query_Select = concat(Query_Select,Query_Where,Query_Limit);
			      			#select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;
 elseif ls_Type = 'CWIP_CHECKER' and ls_Sub_Type = 'CHECKER_SUMMARY' then

			select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Invoice_No'))) into @Invoice_No;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.Product_Gid'))) into @Product_Gid;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.CWIP_Group'))) into @lc_CWIP_Group;
               set Query_Search = '';
               set Query_Select = '';

               if @lc_CWIP_Group = 'Y' THEN
               		set Query_Select = '';
                 set Query_Select = concat('select a.cwipasset_gid,b.cwipgroup_name,count(a.cwipasset_gid) as cwip_count,
						date_format(cwipasset_date,''%d-%m-%Y'') as cwip_date,group_concat(a.cwipasset_gid) as cwip_gids,
                        cwipgroup_gid
						from fa_trn_tcwipasset as a
						inner join fa_mst_tcwipgroup as b on b.cwipgroup_gid = a.cwipasset_cwipgroupgid
						where a.cwipasset_requeststatus = ''PENDING''
						and a.cwipasset_isactive = ''Y'' and a.cwipasset_isremoved = ''N''
						and b.cwipgroup_isactive = ''Y'' and b.cwipgroup_isremoved = ''N''
                        ',Query_Search,' and a.entity_gid in (',@Entity_Gids,')
						Group by a.cwipasset_cwipgroupgid ');
               ELSEIF @lc_CWIP_Group = 'N' THEN
                 set Query_Select = '';
                 set Query_Select = concat('select a.cwipasset_gid,b.cwipgroup_name,c.product_name,d.assetcat_subcatname,
						a.cwipasset_id,a.cwipasset_cost,a.cwipasset_imagepath
						from fa_trn_tcwipasset as a
						inner join fa_mst_tcwipgroup as b on b.cwipgroup_gid = a.cwipasset_cwipgroupgid
						inner join gal_mst_tproduct as c on c.product_gid = a.cwipasset_productgid
						inner join fa_mst_tassetcat as d on d.assetcat_gid = a.cwipasset_assetcatgid
						where a.cwipasset_requeststatus = ''PENDING''
						and a.cwipasset_isactive = ''Y'' and a.cwipasset_isremoved = ''N''
						and b.cwipgroup_isactive = ''Y'' and b.cwipgroup_isremoved = ''N''
						and c.product_isactive = ''Y'' and c.product_isremoved = ''N''
						and d.assetcat_isactive = ''Y'' and d.assetcat_isremoved = ''N''
                        ',Query_Search,' and a.entity_gid in (',@Entity_Gids,')'
                        );
                ELSE
                     set Message = 'NOT_FOUND';
					 leave sp_FAAssertProcess_Get;
               End if;

        	     	set @Query_Select = Query_Select;
             		 #   select @Query_Select; ### Remove It
						PREPARE stmt FROM @Query_Select;
						EXECUTE stmt;
						Select found_rows() into li_count;

					  if li_count > 0 then
							set Message = 'FOUND';
					  else
							set Message = 'NOT_FOUND';
					  end if;


  elseif ls_Type = 'INVOICE_DETAILS' and ls_Sub_Type = 'SUMMARY' then
         ### Shown the Invoice from AP Summary - Paid Status Only


				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Invoice_No'))) into @Invoice_No;
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Invoice_Date'))) into @Invoice_Date;
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Supplier_Name'))) into @Supplier_Name;

                set Query_Search = '';

						if @Invoice_No <> '' and @Invoice_No is not null  then
							set Query_Search = concat(Query_Search,' and a.invoiceheader_invoiceno like ''','%',@Invoice_No,'%','''  ');
                        End if;

                        if @Invoice_Date <> '' and @Invoice_Date is not null  then
							set Query_Search = concat(Query_Search,' and date_format(a.invoiceheader_invoicedate,''%Y-%m-%d'') like ''','%',@Invoice_Date,'%','''  ');
                        End if;

                        if @Supplier_Name <> '' and @Supplier_Name is not null  then
							set Query_Search = concat(Query_Search,' and b.supplier_name like ''','%',@Supplier_Name,'%','''  ');
                        End if;

                set Query_Select = '';
                set Query_Select = concat('
							Select a.invoiceheader_gid, a.invoiceheader_invoiceno, date_format(a.invoiceheader_invoicedate,''%Y-%b-%d'') as invoiceheader_invoicedate,
							b.supplier_name,a.invoiceheader_amount,
                            a.invoiceheader_invoicetype, group_concat(distinct h.poheader_no) as po_nos ,i.employee_name,j.credit_amount,
                            ifnull(sum(k.paymentdetails_amount),0) as amount_paid

							from ap_trn_tinvoiceheader as a
							inner join gal_mst_tsupplier as b on b.supplier_gid = a.invoiceheader_suppliergid
							inner join ap_map_tinvoicepo as c on c.invoicepo_invoiceheadergid = a.invoiceheader_gid
							inner join gal_trn_tgrninwarddetails as d on d.grninwarddetails_gid = c.invoicepo_grninwarddetailsgid
							inner join gal_trn_tpodetails as e on e.podetails_gid = d.grninwarddetails_podetails_gid
							inner join gal_mst_tproduct as f on f.product_gid = e.podetails_product_gid
							inner join ap_mst_tcategory as g on g.category_gid = f.product_category_gid

                            inner join gal_trn_tpoheader as h on h.poheader_gid = c.invoicepo_poheadergid
                            inner join gal_mst_temployee as i on i.employee_gid = a.invoiceheader_employeegid
                            inner join ap_trn_tcredit as j on j.credit_invoiceheadergid = a.invoiceheader_gid
                            left join ap_trn_tpaymentdetails as k on k.paymentdetails_invoiceheadergid = a.invoiceheader_gid
                              and k.paymentdetails_creditgid = j.credit_gid and k.paymentdetails_isactive = ''Y''
                              and k.paymentdetails_isremoved = ''N''

							where a.invoiceheader_status in (''PAID'',''PAYMENT'',''PARTIALLY PAID'')
							and c.invoicepo_capitalised = ''N''
							and g.category_isasset = ''Y''
							and a.invoiceheader_isactive = ''Y'' and a.invoiceheader_isremoved = ''N''
							and b.supplier_isactive = ''Y'' and b.supplier_isremoved = ''N''
							and c.invoicepo_isactive = ''Y'' and c.invoicepo_isremoved = ''N''
							and d.grninwarddetails_isremoved = ''N''
							and e.podetails_isremoved = ''N''
							and f.product_isactive = ''Y''
							and f.product_isremoved = ''N''
							and g.category_isactive = ''Y''
							and g.category_isremoved = ''N''

                            and h.poheader_isactive = ''Y'' and h.poheader_isremoved = ''N''
                            and i.employee_isactive = ''Y'' and i.employee_isremoved = ''N''
                            and j.credit_isactive = ''Y'' and j.credit_isremoved = ''N''

                            ',Query_Search,' and a.entity_gid in (',@Entity_Gids,')
                            group by a.invoiceheader_gid, a.invoiceheader_invoiceno, date_format(a.invoiceheader_invoicedate,''%Y-%b-%d''),
							b.supplier_name,a.invoiceheader_amount
							');
                	       	set @Query_Select = Query_Select;
			      			    #select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;

  elseif ls_Type = 'INVOICE_DETAILS' and ls_Sub_Type = 'DETAILS' then
                        # Show Product Wise Inv Details Based on Inv gid
					set Query_Select = '';
					set Query_Search = '';
				    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Invoice_Gid'))) into @Invoice_Gid;

                    if @Invoice_Gid is null or @Invoice_Gid = 0 or @Invoice_Gid = '' then
						set Message = 'Invoice Gid Is Needed.';
                        leave sp_FAAssertProcess_Get;
                    End if;

                set Query_Select = concat('
							Select a.invoiceheader_gid, aa.invoicedetails_gid,e.podetails_gid,f.product_gid,b.supplier_gid,
                            date_format(a.invoiceheader_invoicedate,''%Y-%b-%d'') as invoiceheader_invoicedate,
                            b.supplier_name,f.product_name,d.grninwarddetails_qty as invoicedetail_qty,aa.invoicedetails_unitprice,
                            aa.invoicedetails_taxamt,aa.invoicedetails_totalamt,d.grninwarddetails_qty,
                            fn_FA_Data(''PRODUCT_ASSETCAT'',f.product_gid,0,a.entity_gid,''{}'')  as asset_cat_gid,g.category_name,

                            Case
							when fn_REFGid(''PO_GODOWN'')  then
							   (select ifnull(z.godown_name,'''') from gal_mst_tgodown as z where godown_gid = h.podelivery_reftablegid)
							 when fn_REFGid(''PO_BRANCH'')  then
								(select ifnull(y.branch_name,'''') from gal_mst_tbranch as y where branch_gid = h.podelivery_reftablegid)
							End as ''branch_name'',j.branch_name as ap_branch,

                            concat(''{"DEBIT_DATA":['',group_concat(JSON_OBJECT(''Debit_Amount'',i.debit_amount,''Invoice_Item'',aa.invoicedetails_item,
                            ''Category_Name'',g.category_name)),'']}'')
                            as debit_data

							from ap_trn_tinvoiceheader as a
                            inner join ap_trn_tinvoicedetails as aa on aa.invoicedetails_headergid = a.invoiceheader_gid
							inner join gal_mst_tsupplier as b on b.supplier_gid = a.invoiceheader_suppliergid
							left join ap_map_tinvoicepo as c on c.invoicepo_invoicedetailsgid = aa.invoicedetails_gid
                             and c.invoicepo_capitalised = ''N'' and c.invoicepo_isactive = ''Y'' and c.invoicepo_isremoved = ''N''
							left join gal_trn_tgrninwarddetails as d on d.grninwarddetails_gid = c.invoicepo_grninwarddetailsgid
                             and d.grninwarddetails_isremoved = ''N''
							left join gal_trn_tpodetails as e on e.podetails_gid = d.grninwarddetails_podetails_gid
                             and e.podetails_isremoved = ''N''
							left join gal_mst_tproduct as f on f.product_gid = e.podetails_product_gid
                             and f.product_isactive = ''Y'' and f.product_isremoved = ''N''
							left join ap_mst_tcategory as g on g.category_gid = f.product_category_gid
								and g.category_isactive = ''Y'' and g.category_isremoved = ''N''
                            left join gal_trn_tpodelivery as h on h.podelivery_product_gid = f.product_gid and h.podelivery_podetails_gid = e.podetails_gid
                            inner join ap_trn_tdebit as i on i.debit_invoiceheadergid = a.invoiceheader_gid
                              inner join gal_mst_tbranch as j on j.branch_gid = a.invoiceheader_branchgid
                             and j.branch_isactive = ''Y'' and j.branch_isremoved = ''N''
                            where a.invoiceheader_status in (''PAID'',''PAYMENT'',''PARTIALLY PAID'')
                            and f.product_name is not null
                            and a.invoiceheader_gid = ',@Invoice_Gid,'
                            and a.invoiceheader_isactive = ''Y'' and a.invoiceheader_isremoved = ''N''
							and b.supplier_isactive = ''Y'' and b.supplier_isremoved = ''N''
                            ',Query_Search,' and a.entity_gid in (',@Entity_Gids,')
                             Group by a.invoiceheader_gid, aa.invoicedetails_gid,e.podetails_gid,f.product_gid,
                             b.supplier_gid,date_format(a.invoiceheader_invoicedate,''%Y-%b-%d'') ,
                          b.supplier_name,f.product_name,d.grninwarddetails_qty
							');

                     	set @Query_Select = Query_Select;
			      			#select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;
  elseif ls_Type = 'CWIP_DETAILS' and ls_Sub_Type = 'SUMMARY' then
        ### Newly Added -
		        select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Invoice_No'))) into @Invoice_No;
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Invoice_Date'))) into @Invoice_Date;
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Supplier_Name'))) into @Supplier_Name;

			  set Query_Search = '';
                /*
						if @Invoice_No <> '' and @Invoice_No is not null  then
							set Query_Search = concat(Query_Search,' and a.invoiceheader_invoiceno like ''','%',@Invoice_No,'%','''  ');
                        End if;

                        if @Invoice_Date <> '' and @Invoice_Date is not null  then
							set Query_Search = concat(Query_Search,' and date_format(a.invoiceheader_invoicedate,''%Y-%m-%d'') like ''','%',@Invoice_Date,'%','''  ');
                        End if;

                        if @Supplier_Name <> '' and @Supplier_Name is not null  then
							set Query_Search = concat(Query_Search,' and b.supplier_name like ''','%',@Supplier_Name,'%','''  ');
                        End if;
			         */
                set Query_Select = '';
                set Query_Select = concat('
							   Select b.cwipgroup_gid,count(a.cwipasset_gid) as cwip_count,b.cwipgroup_name,sum(a.cwipasset_cost) as tot_value,
                                   date_format(cwipasset_date,''%d-%b-%Y'') as cwip_date
								from fa_trn_tcwipasset as a
								inner join fa_mst_tcwipgroup as b on b.cwipgroup_gid = a.cwipasset_cwipgroupgid
								where a.cwipasset_capdate is  null
								and a.cwipasset_isactive = ''Y'' and a.cwipasset_isremoved = ''N''
								and b.cwipgroup_isactive = ''Y'' and b.cwipgroup_isremoved = ''N''
                               ',Query_Search,' and a.entity_gid in (',@Entity_Gids,')
	   							');
                	       	set @Query_Select = Query_Select;
		      			   # select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;
  elseif ls_Type = 'CWIP_DETAILS' and ls_Sub_Type = 'DETAILS' then
        ### Newly Added -
		        select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.CWIP_Group_Gids'))) into @CWIP_Group_Gids;
		           select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Page_Index'))) into @Page_Index;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Page_Size'))) into @Page_Size;

		        if @CWIP_Group_Gids is null or @CWIP_Group_Gids = '' THEN
		        	set Message = 'CWIP Group Gids Is Needed.';
		            leave sp_FAAssertProcess_Get;
		        End if;

			  set Query_Search = '';
			  set Query_Limit = '';
                /*
						if @Invoice_No <> '' and @Invoice_No is not null  then
							set Query_Search = concat(Query_Search,' and a.invoiceheader_invoiceno like ''','%',@Invoice_No,'%','''  ');
                        End if;

                        if @Invoice_Date <> '' and @Invoice_Date is not null  then
							set Query_Search = concat(Query_Search,' and date_format(a.invoiceheader_invoicedate,''%Y-%m-%d'') like ''','%',@Invoice_Date,'%','''  ');
                        End if;

                        if @Supplier_Name <> '' and @Supplier_Name is not null  then
							set Query_Search = concat(Query_Search,' and b.supplier_name like ''','%',@Supplier_Name,'%','''  ');
                        End if;
			         */



                    if @Page_Index <> '' and @Page_Index is not null and @Page_Size <> '' and @Page_Size is not null  then
                         set @total_size= @Page_Index*@Page_Size;
                         set Query_Limit = concat(Query_Limit,' LIMIT ',@Page_Size,' OFFSET ',@total_size,'  ');
                    End if;
                set Query_Select = '';
                set Query_Select = concat('
							   select a.cwipasset_cwipgroupgid as cwip_group_gid,a.cwipasset_gid,0 as supplier_gid,
                                cwipasset_invoicegid as invoiceheader_gid ,e.invoicepo_invoicedetailsgid as invoicedetails_gid,a.cwipasset_assetcatgid as asset_cat_gid,
								b.cwipgroup_name,c.product_name,
                                a.cwipasset_qty as invoicedetail_qty,a.cwipasset_cost as invoicedetails_unitprice,product_gid,
                                d.assetcat_subcatname,
								a.cwipasset_cost,a.cwipasset_imagepath
								from fa_trn_tcwipasset as a
								inner join fa_mst_tcwipgroup as b on b.cwipgroup_gid = a.cwipasset_cwipgroupgid
								inner join gal_mst_tproduct as c on c.product_gid = a.cwipasset_productgid
								inner join fa_mst_tassetcat as d on d.assetcat_gid = a.cwipasset_assetcatgid
                                inner join ap_map_tinvoicepo as e on e.invoicepo_invoiceheadergid = a.cwipasset_invoicegid
								inner join gal_trn_tpodetails as f on f.podetails_gid = e.invoicepo_podetailsgid
                                  and f.podetails_product_gid = c.product_gid
								where a.cwipasset_requeststatus = ''PENDING''
                                and a.cwipasset_capdate is null
								and a.cwipasset_isactive = ''Y'' and a.cwipasset_isremoved = ''N''
								and b.cwipgroup_isactive = ''Y'' and b.cwipgroup_isremoved = ''N''
								and c.product_isactive = ''Y'' and c.product_isremoved = ''N''
								and d.assetcat_isactive = ''Y'' and d.assetcat_isremoved = ''N''
								and a.cwipasset_cwipgroupgid in (',@CWIP_Group_Gids,')
                               ',Query_Search,' and a.entity_gid in (',@Entity_Gids,')
                               ',Query_Limit,'
	   							');
                	       	set @Query_Select = Query_Select;
			      			    #select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;


  elseif  ls_Type = 'VALUEREDUCTION'  and ls_Sub_Type = 'SUMMARY' then

					select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Invoice_Gid'))) into @Invoice_Gid;
					select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Id'))) into @Asset_Id;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Value'))) into @Asset_Value;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Cap_Date'))) into @Asset_CP_Date;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Code'))) into @Category_Name;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Branch'))) into @Branch_Name;

   # select @Asset_Id,@Asset_Value,@Asset_CP_Date,@Category_Name,@Branch_Name;

                    set Query_Search = '';

                    if @Asset_Id <> '' and @Asset_Id is not null  then
                         set Query_Search = concat(Query_Search,' and b.assetdetails_id like ''','%',@Asset_Id,'%','''  ');
                    End if;

                    if @Asset_Value <> '' and @Asset_Value is not null then
                         set Query_Search = concat(Query_Search,' and b.assetdetails_value like ''','%',@Asset_Value,'%','''  ');
                    End if;

					if @Asset_CP_Date <> '' and @Asset_CP_Date is not null  then
                        set Query_Search = concat(Query_Search,'and date_format(b.assetdetails_capdate,''%Y-%m-%d'') = ''',@Asset_CP_Date,'''  ');
                    End if;

                    if @Category_Name <> '' and @Category_Name is not null  then
                         set Query_Search = concat(Query_Search,' and g.assetcat_subcatname like ''','%',@Category_Name,'%','''  ');
                    End if;

                     if @Branch_Name <> '' and @Branch_Name is not null  then
                         set Query_Search = concat(Query_Search,' and c.branch_name like ''','%',@Branch_Name,'%','''  ');
                    End if;


                    ##WIP
					set @Request_For = '';
					set Query_Select = '';
                    set Query_Select = concat('Select a.assetvalue_gid,b.assetdetails_gid,b.assetdetails_id,
								a.assetvalue_oldvalue,a.assetvalue_value,b.assetdetails_value,
								a.assetvalue_status,a.assetvalue_reason,g.assetcat_subcatname,c.branch_name,
								date_format(a.assetvalue_date,''%d-%b-%Y'') as value_date,
                                date_format(b.assetdetails_capdate,''%d-%b-%Y'') as assetdetails_capdate ,
                                b.assetdetails_branchgid,b.assetdetails_imagepath,b.assetdetails_status,
                                fn_Asset_Data(''ASSET_TRAN'',b.assetdetails_gid,b.entity_gid,''{}'') as lj_default_details
                                from fa_trn_tassetvalue as a
								inner join fa_trn_tassetdetails as b on b.assetdetails_id = a.assetvalue_assetdetailsid
								inner join gal_mst_tbranch as c on c.branch_gid = b.assetdetails_branchgid
								inner join fa_mst_tassetcat as g on g.assetcat_gid = b.assetdetails_assetcatgid
								where a.assetvalue_isactive = ''Y'' and a.assetvalue_isremoved = ''N''
								and b.assetdetails_isactive = ''Y'' and b.assetdetails_isremoved = ''N''
								and g.assetcat_isactive= ''Y'' and g.assetcat_isremoved = ''N''
								and c.branch_isactive = ''Y'' and c.branch_isremoved = ''N''
								',Query_Search,' and a.entity_gid in (',@Entity_Gids,') and c.entity_gid in (',@Entity_Gids,')
                                and g.entity_gid in (',@Entity_Gids,')
								');

								set @Query_Select = Query_Select;
							   #select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;

  elseif ls_Type = 'WRITEOFF_DETAILS' and ls_Sub_Type = 'SUMMARY' then
                                 #### Writr Off Main Summary
                                 #### Search TO DO
                                 #wip

                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Id'))) into @Asset_Id;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Value'))) into @Asset_Value;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Cap_Date'))) into @Asset_CP_Date;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Code'))) into @Category_Name;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Branch'))) into @Branch_Name;

   # select @Asset_Id,@Asset_Value,@Asset_CP_Date,@Category_Name,@Branch_Name;

                    set Query_Search = '';


                    if @Asset_Id <> '' and @Asset_Id is not null  then
                         set Query_Search = concat(Query_Search,' and b.assetdetails_id like ''','%',@Asset_Id,'%','''  ');
                    End if;

                    if @Asset_Value <> '' and @Asset_Value is not null then
                         set Query_Search = concat(Query_Search,' and b.assetdetails_value like ''','%',@Asset_Value,'%','''  ');
                    End if;

					if @Asset_CP_Date <> '' and @Asset_CP_Date is not null  then
                        set Query_Search = concat(Query_Search,'and date_format(b.assetdetails_capdate,''%Y-%m-%d'') = ''',@Asset_CP_Date,'''  ');
                    End if;

                    if @Category_Name <> '' and @Category_Name is not null  then
                         set Query_Search = concat(Query_Search,' and g.assetcat_subcatname like ''','%',@Category_Name,'%','''  ');
                    End if;

                     if @Branch_Name <> '' and @Branch_Name is not null  then
                         set Query_Search = concat(Query_Search,' and c.branch_name like ''','%',@Branch_Name,'%','''  ');
                    End if;


    set Query_Select = '';
	set Query_Select = concat('Select a.writeoff_gid,b.assetdetails_gid,b.assetdetails_id,a.writeoff_value,
									b.assetdetails_value,a.writeoff_status,a.writeoff_reason,
									date_format(a.writeoff_date,''%d-%b-%Y'') as writeoff_date,
									date_format(b.assetdetails_capdate,''%d-%b-%Y'') as assetdetails_capdate ,
									b.assetdetails_branchgid,	b.assetdetails_imagepath,b.assetdetails_status,
									fn_Asset_Data(''ASSET_TRAN'',b.assetdetails_gid,
                                    b.entity_gid,''{}'') as lj_default_details,g.assetcat_subcatname,c.branch_name
								from fa_trn_twriteoff as a
									inner join fa_trn_tassetdetails as b on b.assetdetails_id = a.writeoff_assetdetailsid
									inner join gal_mst_tbranch as c on c.branch_gid = b.assetdetails_branchgid
                                    inner join fa_mst_tassetcat as g on g.assetcat_gid = b.assetdetails_assetcatgid
								where a.writeoff_isactive = ''Y'' and a.writeoff_isremoved = ''N''
									and b.assetdetails_isactive = ''Y'' and b.assetdetails_isremoved = ''N''
                                    and g.assetcat_isactive= ''Y'' and g.assetcat_isremoved = ''N''
									and c.branch_isactive = ''Y'' and c.branch_isremoved = ''N''
									',Query_Search,' and a.entity_gid in (',@Entity_Gids,')
                                    and g.entity_gid in (',@Entity_Gids,') and c.entity_gid in (',@Entity_Gids,')
									order by writeoff_date desc
										');
								set @Query_Select = Query_Select;
			      			    #select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;

   elseif ls_Type = 'WRITEOFF_DETAILS' and ls_Sub_Type = 'CHECKER_SUMMARY' then
                                 #### Writr Off Checker Summary
                                 #### Search TO DO
                                 #wip

					select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Id'))) into @Asset_Id;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Value'))) into @Asset_Value;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Cap_Date'))) into @Asset_CP_Date;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Code'))) into @Category_Name;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Branch'))) into @Branch_Name;

   # select @Asset_Id,@Asset_Value,@Asset_CP_Date,@Category_Name,@Branch_Name;

                    set Query_Search = '';


                    if @Asset_Id <> '' and @Asset_Id is not null  then
                         set Query_Search = concat(Query_Search,' and a.assetdetails_id like ''','%',@Asset_Id,'%','''  ');
                    End if;

                    if @Asset_Value <> '' and @Asset_Value is not null then
                         set Query_Search = concat(Query_Search,' and a.assetdetails_value like ''','%',@Asset_Value,'%','''  ');
                    End if;

					if @Asset_CP_Date <> '' and @Asset_CP_Date is not null  then
                        set Query_Search = concat(Query_Search,'and date_format(a.assetdetails_capdate,''%Y-%m-%d'') = ''',@Asset_CP_Date,'''  ');
                    End if;

                    if @Category_Name <> '' and @Category_Name is not null  then
                         set Query_Search = concat(Query_Search,' and g.assetcat_subcatname like ''','%',@Category_Name,'%','''  ');
                    End if;

                    if @Branch_Name <> '' and @Branch_Name is not null  then
                         set Query_Search = concat(Query_Search,' and c.branch_name like ''','%',@Branch_Name,'%','''  ');
                    End if;


                   # select Query_Search;
            set Query_Select = '';
			set Query_Select = concat('Select a.assetdetails_gid,a.assetdetails_branchgid,
								b.writeoff_gid,a.assetdetails_id,a.assetdetails_requeststatus,
                                date_format(b.writeoff_date,''%d-%b-%Y'') as writeoff_date,
                                date_format(a.assetdetails_capdate,''%d-%b-%Y'') as assetdetails_capdate,
                                b.writeoff_reason,b.writeoff_value,
								a.assetdetails_imagepath,fn_Asset_Data(''ASSET_TMP'',a.assetdetails_gid,
                                a.entity_gid,''{}'') as lj_default_details
							from fa_tmp_tassetdetails as a
								inner join fa_trn_twriteoff as b on b.writeoff_assetdetailsid = a.assetdetails_id
								inner join gal_mst_tbranch as c on c.branch_gid = a.assetdetails_branchgid
								inner join fa_mst_tassetcat as g on g.assetcat_gid = a.assetdetails_assetcatgid
							where a.assetdetails_requestfor = ''WRITEOFF'' and a.assetdetails_requeststatus = ''SUBMITTED''
								and a.assetdetails_isactive = ''Y''	and a.assetdetails_isremoved = ''N''
                                and c.branch_isactive=''Y'' and c.branch_isremoved=''N''
                                and g.assetcat_isactive= ''Y'' and g.assetcat_isremoved = ''N''
								',Query_Search,' and a.entity_gid in (',@Entity_Gids,')
                                and c.entity_gid in (',@Entity_Gids,') and g.entity_gid in (',@Entity_Gids,')
                                order by writeoff_date desc
										');

								set @Query_Select = Query_Select;
			      	      	#	select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;

    elseif ls_Type = 'IMPAIRMENT_DETAILS' and ls_Sub_Type = 'SUMMARY' then
                                 #### Impairment Main Summary
                                 #### Search TO DO
                                 #wip

                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Id'))) into @Asset_Id;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Value'))) into @Asset_Value;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Cap_Date'))) into @Asset_CP_Date;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Code'))) into @Category_Name;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Branch'))) into @Branch_Name;

					# select @Asset_Id,@Asset_Value,@Asset_CP_Date,@Category_Name,@Branch_Name;

                    set Query_Search = '';


                    if @Asset_Id <> '' and @Asset_Id is not null and @Asset_Id <> 0 then
                         set Query_Search = concat(Query_Search,' and b.assetdetails_id like ''','%',@Asset_Id,'%','''  ');
                    End if;

                    if @Asset_Value <> '' and @Asset_Value is not null then
                         set Query_Search = concat(Query_Search,' and b.assetdetails_value like ''','%',@Asset_Value,'%','''  ');
                    End if;

					if @Asset_CP_Date <> '' and @Asset_CP_Date is not null  then
                        set Query_Search = concat(Query_Search,'and date_format(b.assetdetails_capdate,''%Y-%m-%d'') = ''',@Asset_CP_Date,'''  ');
                    End if;

                    if @Category_Name <> '' and @Category_Name is not null  then
                         set Query_Search = concat(Query_Search,' and g.assetcat_subcatname like ''','%',@Category_Name,'%','''  ');
                    End if;

                    if @Branch_Name <> '' and @Branch_Name is not null  then
                         set Query_Search = concat(Query_Search,' and c.branch_name like ''','%',@Branch_Name,'%','''  ');
                    End if;

                      #select Query_Search;

					set Query_Select = '';
					set Query_Select = concat('Select a.impairasset_gid,b.assetdetails_id,b.assetdetails_assetlocationgid,
											date_format(a.impairasset_date,''%d-%b-%Y'') as impairasset_date ,g.assetcat_subcatname,
                                            c.branch_name,a.impairasset_reason,a.impairasset_status,a.impairasset_value,
											b.assetdetails_status,b.assetdetails_requestfor,b.assetdetails_requeststatus,
											b.assetdetails_imagepath,fn_Asset_Data(''ASSET_TRAN'',b.assetdetails_gid,
                                            b.entity_gid,''{}'') as lj_default_details
											from fa_trn_timpairasset as a
											inner join fa_trn_tassetdetails as b on b.assetdetails_id = a.impairasset_assetdetailsid
											inner join gal_mst_tbranch as c on c.branch_gid = b.assetdetails_branchgid
											inner join fa_mst_tassetcat as g on g.assetcat_gid = b.assetdetails_assetcatgid
											where a.impairasset_isactive = ''Y'' and a.impairasset_isremoved = ''N''
											and b.assetdetails_isactive  = ''Y'' and b.assetdetails_isremoved = ''N''
											and c.branch_isactive = ''Y'' and c.branch_isremoved = ''N''
                                             and g.assetcat_isactive= ''Y'' and g.assetcat_isremoved = ''N''
											',Query_Search,' and a.entity_gid in (',@Entity_Gids,') and g.entity_gid in (',@Entity_Gids,')
                                            and c.entity_gid in (',@Entity_Gids,')
											order by impairasset_date desc
										');

								set @Query_Select = Query_Select;
			      		       #select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;
   elseif ls_Type = 'IMPAIRMENT_DETAILS' and ls_Sub_Type = 'CHECKER_SUMMARY' then
                                 #### Imppairment Checker Summary
                                 #### Search TO DO
                                 #wip


					select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Id'))) into @Asset_Id;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Value'))) into @Asset_Value;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Cap_Date'))) into @Asset_CP_Date;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Code'))) into @Category_Name;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Branch'))) into @Branch_Name;

					# select @Asset_Id,@Asset_Value,@Asset_CP_Date,@Category_Name,@Branch_Name;


                    set Query_Search = '';

                    if @Asset_Id <> '' and @Asset_Id is not null and @Asset_Id <> 0 then
                         set Query_Search = concat(Query_Search,' and a.assetdetails_id like ''','%',@Asset_Id,'%','''  ');
                    End if;

                    if @Asset_Value <> '' and @Asset_Value is not null then
                         set Query_Search = concat(Query_Search,' and a.assetdetails_value like ''','%',@Asset_Value,'%','''  ');
                    End if;

					if @Asset_CP_Date <> '' and @Asset_CP_Date is not null  then
                        set Query_Search = concat(Query_Search,'and date_format(a.assetdetails_capdate,''%Y-%m-%d'') = ''',@Asset_CP_Date,'''  ');
                    End if;

                    if @Category_Name <> '' and @Category_Name is not null  then
                         set Query_Search = concat(Query_Search,' and g.assetcat_subcatname like ''','%',@Category_Name,'%','''  ');
                    End if;

                    if @Branch_Name <> '' and @Branch_Name is not null  then
                         set Query_Search = concat(Query_Search,' and c.branch_name like ''','%',@Branch_Name,'%','''  ');
                    End if;



						set Query_Select = '';
						set Query_Select = concat('Select a.assetdetails_gid,a.assetdetails_branchgid,
								b.impairasset_gid,assetdetails_id,c.branch_name,a.assetdetails_requeststatus,
                                date_format(b.impairasset_date,''%d-%b-%Y'') as impairasset_date,g.assetcat_subcatname,
                                date_format(a.assetdetails_capdate,''%d-%b-%Y'') as assetdetails_capdate,
                                b.impairasset_reason,b.impairasset_value,
								a.assetdetails_imagepath,fn_Asset_Data(''ASSET_TMP'',a.assetdetails_gid,a.entity_gid,''{}'') as lj_default_details
								 from fa_tmp_tassetdetails as a
								inner join fa_trn_timpairasset as b on b.impairasset_assetdetailsid = a.assetdetails_id
								inner join gal_mst_tbranch as c on c.branch_gid = a.assetdetails_branchgid
                                inner join fa_mst_tassetcat as g on g.assetcat_gid = a.assetdetails_assetcatgid
								where a.assetdetails_requestfor = ''IMPAIRMENT'' and a.assetdetails_requeststatus = ''SUBMITTED''
								and a.assetdetails_isactive = ''Y''	and a.assetdetails_isremoved = ''N''
                                 and g.assetcat_isactive= ''Y'' and g.assetcat_isremoved = ''N''
								',Query_Search,' and a.entity_gid in (',@Entity_Gids,') and g.entity_gid in (',@Entity_Gids,')
                                order by impairasset_date desc
										');

								set @Query_Select = Query_Select;
			      			    #select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;

   elseif ls_Type = 'CPCHANGE_DETAILS' and ls_Sub_Type = 'SUMMARY' then


				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Branch_Gid'))) into @Asset_Branch_Gid;
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Id'))) into @Asset_Id;
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Code'))) into @Asset_Code;
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Cap_Date'))) into @Asset_CP_Date;
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Branch'))) into @Branch_Name;
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Group'))) into @Asset_Group;
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Category'))) into @Category_Name;
				#### Cp Date  Main Summary
				#### Search TO DO
			    #wip
					set Query_Search = '';

                    if @Asset_Value <> '' and @Asset_Value is not null then
                         set Query_Search = concat(Query_Search,' and b.assetdetails_value like ''','%',@Asset_Value,'%','''  ');
                    End if;

                    if @Asset_Id <> '' and @Asset_Id is not null and @Asset_Id <> 0 then
                         set Query_Search = concat(Query_Search,' and b.assetdetails_id like ''','%',@Asset_Id,'%','''  ');
                    End if;

					if @Asset_CP_Date <> '' and @Asset_CP_Date is not null  then
                        set Query_Search = concat(Query_Search,'and date_format(b.assetdetails_capdate,''%Y-%m-%d'') = ''',@Asset_CP_Date,'''  ');
                    End if;

                    if @Branch_Name <> '' and @Branch_Name is not null  then
                         set Query_Search = concat(Query_Search,' and c.branch_name like ''','%',@Branch_Name,'%','''  ');
                    End if;

                    if @Category_Name <> '' and @Category_Name is not null  then
                         set Query_Search = concat(Query_Search,' and g.assetcat_subcatname like ''','%',@Category_Name,'%','''  ');
                    End if;



                    set Query_Select='';
					set Query_Select = concat('Select b.assetdetails_gid,
									a.assetcapdate_gid,b.assetdetails_id,b.assetdetails_cost,b.assetdetails_value,
									date_format(a.assetcapdate_capdate,''%d-%b-%Y'') as new_cap_date,
									date_format(a.assetcapdate_oldcapdate,''%d-%b-%Y'') as old_cap_date,
									a.assetcapdate_reason,a.assetcapdate_status,
									b.assetdetails_imagepath,b.assetdetails_status,
									fn_Asset_Data(''ASSET_TRAN'',b.assetdetails_gid,b.entity_gid,''{}'') as lj_default_details
									from fa_trn_tassetcapdate as a
									inner join fa_trn_tassetdetails as b on  b.assetdetails_id = a.assetcapdate_assetdetailsid
									inner join gal_mst_tbranch as c on c.branch_gid = b.assetdetails_branchgid
									inner join fa_mst_tassetloaction as d on d.assetlocation_gid = b.assetdetails_assetlocationgid
									where
									b.assetdetails_isactive = ''Y'' and b.assetdetails_isremoved = ''N''
                                    and b.entity_gid in (',@Entity_Gids,')
									and a.assetcapdate_isactive = ''Y'' and a.assetcapdate_isremoved = ''N''
									and c.branch_isactive = ''Y'' and c.branch_isremoved = ''N''
									and c.entity_gid in (',@Entity_Gids,')
									and d.assetlocation_isactive = ''Y'' and d.assetlocation_isremoved = ''N''
                                    and d.entity_gid in (',@Entity_Gids,')
									',Query_Search,' and a.entity_gid in (',@Entity_Gids,')
									order by a.assetcapdate_gid desc ');

								set @Query_Select = Query_Select;
			      			    #select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;

   elseif ls_Type = 'CPCHANGE_DETAILS' and ls_Sub_Type = 'CHECKER_SUMMARY' then
                                 #### Writr Off Checker Summary
                                 #### Search TO DO
                                 #wip
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Branch_Gid'))) into @Asset_Branch_Gid;
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Id'))) into @Asset_Id;
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Value'))) into @Asset_Value;
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Code'))) into @Category_Name;
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Branch'))) into @Branch_Name;
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Group'))) into @Asset_Group;
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Cap_Date'))) into @Asset_CP_Date;
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Category'))) into @Category_Name;



					set Query_Search = '';

                    if @Asset_Value <> '' and @Asset_Value is not null then
                         set Query_Search = concat(Query_Search,' and a.assetdetails_value like ''','%',@Asset_Value,'%','''  ');
                    End if;

                    if @Asset_Id <> '' and @Asset_Id is not null  then
                         set Query_Search = concat(Query_Search,' and a.assetdetails_id like ''','%',@Asset_Id,'%','''  ');
                    End if;

					if @Asset_CP_Date <> '' and @Asset_CP_Date is not null  then
                        set Query_Search = concat(Query_Search,'and date_format(a.assetdetails_capdate,''%Y-%m-%d'') = ''',@Asset_CP_Date,'''  ');
                    End if;

                    if @Branch_Name <> '' and @Branch_Name is not null  then
                         set Query_Search = concat(Query_Search,' and c.branch_name like ''','%',@Branch_Name,'%','''  ');
                    End if;

                    if @Category_Name <> '' and @Category_Name is not null  then
                         set Query_Search = concat(Query_Search,' and g.assetcat_subcatname like ''','%',@Category_Name,'%','''  ');
                    End if;


                    #select Query_Search;
					set Query_Select ='';
					set Query_Select = concat('Select a.assetdetails_gid,a.assetdetails_branchgid,
                            b.assetcapdate_gid,a.assetdetails_id,
									a.assetdetails_value,
                                    d.assetdetails_cost as old_cost,a.assetdetails_cost as new_cost,
									date_format(b.assetcapdate_oldcapdate,''%d-%b-%Y'') as oldcapdate,
									date_format(b.assetcapdate_capdate,''%d-%b-%Y'') as new_capdate,
									c.branch_name,a.assetdetails_status,a.assetdetails_requestfor,a.assetdetails_requeststatus,b.assetcapdate_reason,
									a.assetdetails_imagepath,fn_Asset_Data(''ASSET_TMP'',a.assetdetails_gid,a.entity_gid,''{}'') as lj_default_details
									 from fa_tmp_tassetdetails as a
									inner join fa_trn_tassetcapdate as b on b.assetcapdate_assetdetailsid = a.assetdetails_id
									inner join gal_mst_tbranch as c on c.branch_gid = a.assetdetails_branchgid
                                    inner join fa_trn_tassetdetails as d on d.assetdetails_gid = a.assetdetails_mainassetdetailsgid
									where a.assetdetails_requestfor = ''CAPDATE''  and a.assetdetails_requeststatus = ''SUBMITTED''
									and a.assetdetails_isactive = ''Y''
									and a.assetdetails_isremoved = ''N''
                                    and d.assetdetails_isactive = ''Y''
									and d.assetdetails_isremoved = ''N''
									',Query_Search,' and a.entity_gid in (',@Entity_Gids,')
                                     and b.assetcapdate_status = ''SUBMITTED''
									order by b.assetcapdate_gid desc ');

								set @Query_Select = Query_Select;
			      		        #select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;

 elseif ls_Type = 'TRANSFER_DETAILS' and ls_Sub_Type = 'SUMMARY' then
                                 #### Transfer Main Summary
                                 #### Search TO DO
                                 #wip


                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Id'))) into @Asset_Id;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Value'))) into @Asset_Value;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Cap_Date'))) into @Asset_CP_Date;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Code'))) into @Category_Name;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Branch'))) into @Branch_Name;

					 #select @Asset_Id,@Asset_Value,@Asset_CP_Date,@Category_Name,@Branch_Name;


                    set Query_Search = '';

                    if @Asset_Id <> '' and @Asset_Id is not null  then
                         set Query_Search = concat(Query_Search,' and b.assetdetails_id like ''','%',@Asset_Id,'%','''  ');
                    End if;

                    if @Asset_Value <> '' and @Asset_Value is not null then
                         set Query_Search = concat(Query_Search,' and b.assetdetails_value like ''','%',@Asset_Value,'%','''  ');
                    End if;

					if @Asset_CP_Date <> '' and @Asset_CP_Date is not null  then
                        set Query_Search = concat(Query_Search,'and date_format(b.assetdetails_capdate,''%Y-%m-%d'') = ''',@Asset_CP_Date,'''  ');
                    End if;

                    if @Category_Name <> '' and @Category_Name is not null  then
                         set Query_Search = concat(Query_Search,' and g.assetcat_subcatname like ''','%',@Category_Name,'%','''  ');
                    End if;

                    if @Branch_Name <> '' and @Branch_Name is not null  then
                         set Query_Search = concat(Query_Search,' and br.branch_name like ''','%',@Branch_Name,'%','''  ');
                    End if;

			set Query_Select = '';
			set Query_Select = concat('Select a.assettfr_gid,a.assettfr_from,b.assetdetails_id,a.assettfr_newassetdetailsid,
											a.assettfr_reason,a.assettfr_status,a.assettfr_to,
                                            a.assettfr_value,b.assetdetails_imagepath,
											date_format(b.assetdetails_capdate,''%d-%b-%Y'') as cap_date,
											c.product_displayname,d.branch_name branch_name_from,br.branch_name branch_name_to,
                                            e.assetlocation_name,e.assetlocation_floor,
											ifnull(e.assetlocation_remarks,'''') as remarks,
											fn_Asset_Data(''ASSET_TRAN'',b.assetdetails_gid,b.entity_gid,''{}'') as lj_default_details,
                                            b.assetdetails_capdate,b.assetdetails_status
									   from fa_trn_tassettfr as a
											inner join fa_trn_tassetdetails as b on b.assetdetails_id = a.assettfr_assetdetailsid
											inner join gal_mst_tproduct as c on c.product_gid = b.assetdetails_productgid
											inner join gal_mst_tbranch as d on d.branch_gid = a.assettfr_from
											inner join gal_mst_tbranch as br on br.branch_gid = a.assettfr_to
											inner join fa_mst_tassetloaction as e on e.assetlocation_gid = b.assetdetails_assetlocationgid
                                            inner join fa_mst_tassetcat as g on g.assetcat_gid = b.assetdetails_assetcatgid
									   where a.assettfr_isactive = ''Y'' and a.assettfr_isremoved = ''N''
											and a.entity_gid in (',@Entity_Gids,')
											and b.assetdetails_isactive = ''Y'' and b.assetdetails_isremoved = ''N''
                                            and b.entity_gid in (',@Entity_Gids,')
											and c.product_isactive = ''Y'' and c.product_isremoved = ''N''
											and c.entity_gid in (',@Entity_Gids,')
											and d.branch_isactive = ''Y'' and d.branch_isremoved = ''N''
                                            and d.entity_gid in (',@Entity_Gids,')
											and e.assetlocation_isactive = ''Y'' and e.assetlocation_isremoved = ''N''
											and g.assetcat_isactive= ''Y'' and g.assetcat_isremoved = ''N''
											and g.entity_gid in (',@Entity_Gids,')
											and e.entity_gid in (',@Entity_Gids,') ',Query_Search,'
											order by assettfr_date desc
										');

								set @Query_Select = Query_Select;
			      		       #select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;



 elseif ls_Type = 'TRANSFER_DETAILS' and ls_Sub_Type = 'CHECKER_SUMMARY' then
                                 #### Transfer CHecker Summary
                                 #wip

                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Id'))) into @Asset_Id;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Value'))) into @Asset_Value;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Cap_Date'))) into @Asset_CP_Date;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Code'))) into @Category_Name;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Branch'))) into @Branch_Name;

					 #select @Asset_Id,@Asset_Value,@Asset_CP_Date,@Category_Name,@Branch_Name;


                    set Query_Search = '';

                    if @Asset_Id <> '' and @Asset_Id is not null then
                         set Query_Search = concat(Query_Search,' and a.assetdetails_id like ''','%',@Asset_Id,'%','''  ');
                    End if;

                    if @Asset_Value <> '' and @Asset_Value is not null then
                         set Query_Search = concat(Query_Search,' and a.assetdetails_value like ''','%',@Asset_Value,'%','''  ');
                    End if;

					if @Asset_CP_Date <> '' and @Asset_CP_Date is not null  then
                        set Query_Search = concat(Query_Search,'and date_format(a.assetdetails_capdate,''%Y-%m-%d'') = ''',@Asset_CP_Date,'''  ');
                    End if;

                    if @Category_Name <> '' and @Category_Name is not null  then
                         set Query_Search = concat(Query_Search,' and g.assetcat_subcatname like ''','%',@Category_Name,'%','''  ');
                    End if;

                    if @Branch_Name <> '' and @Branch_Name is not null  then
                         set Query_Search = concat(Query_Search,' and c.branch_name like ''','%',@Branch_Name,'%','''  ');
                    End if;

                         #select Query_Search;

			set Query_Select = '';
			set Query_Select = concat('Select a.assetdetails_gid,b.assettfr_gid,a.assetdetails_id,
											a.assetdetails_value,date_format(a.assetdetails_capdate,''%d-%b-%Y'') as cap_date,
											b.assettfr_reason,b.assettfr_status,c.branch_name as transfer_from,
											d.branch_name as transfer_to,fn_Asset_Data(''ASSET_TMP'',a.assetdetails_gid,
											a.entity_gid,''{}'') as lj_default_details,g.assetcat_subcatname,a.assetdetails_imagepath
										from fa_tmp_tassetdetails as a
											inner join fa_trn_tassettfr as b on b.assettfr_assetdetailsid = a.assetdetails_id
											inner join gal_mst_tbranch as c on c.branch_gid = b.assettfr_from
											inner join gal_mst_tbranch as d on d.branch_gid = b.assettfr_to
                                            inner join fa_mst_tassetcat as g on g.assetcat_gid = a.assetdetails_assetcatgid
										where a.assetdetails_requestfor = ''TRANSFER'' and a.assetdetails_requeststatus = ''SUBMITTED''
											and a.assetdetails_isactive = ''Y'' and a.assetdetails_isremoved = ''N''
											and b.assettfr_isactive = ''Y'' and b.assettfr_isremoved = ''N''
											and c.branch_isactive = ''Y'' and c.branch_isremoved = ''N''
											and d.branch_isactive = ''Y'' and d.branch_isremoved = ''N''
                                            and g.assetcat_isactive= ''Y'' and g.assetcat_isremoved = ''N''
											and a.entity_gid in (',@Entity_Gids,') and g.entity_gid in (',@Entity_Gids,') ',Query_Search,'
										order by assettfr_date desc,assettfr_gid
										');

								set @Query_Select = Query_Select;
			      			   #select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;

 elseif ls_Type = 'CAT_DETAILS' and ls_Sub_Type = 'SUMMARY' then
                                 #### CAT Main Summary
                                 #### Search TO DO
                                 #wip

                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Id'))) into @Asset_Id;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Value'))) into @Asset_Value;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Cap_Date'))) into @Asset_CP_Date;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Code'))) into @Category_Name;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Branch'))) into @Branch_Name;

					# select @Asset_Id,@Asset_Value,@Asset_CP_Date,@Category_Name,@Branch_Name;


                    set Query_Search = '';

                    if @Asset_Id <> '' and @Asset_Id is not null and @Asset_Id <> 0 then
                         set Query_Search = concat(Query_Search,' and b.assetdetails_id like ''','%',@Asset_Id,'%','''  ');
                    End if;

                    if @Asset_Value <> '' and @Asset_Value is not null then
                         set Query_Search = concat(Query_Search,' and b.assetdetails_value like ''','%',@Asset_Value,'%','''  ');
                    End if;

					if @Asset_CP_Date <> '' and @Asset_CP_Date is not null  then
                        set Query_Search = concat(Query_Search,'and date_format(b.assetdetails_capdate,''%Y-%m-%d'') = ''',@Asset_CP_Date,'''  ');
                    End if;

                    if @Category_Name <> '' and @Category_Name is not null  then
                         set Query_Search = concat(Query_Search,' and g.assetcat_subcatname like ''','%',@Category_Name,'%','''  ');
                    End if;

                    if @Branch_Name <> '' and @Branch_Name is not null  then
                         set Query_Search = concat(Query_Search,' and d.branch_name like ''','%',@Branch_Name,'%','''  ');
                    End if;


		set Query_Select = '';
		set Query_Select = concat('Select a.assetcatchange_gid,a.assetcatchange_assetdetailsid,
										  a.assetcatchange_oldcat,g.assetcat_subcatname new_catname,
										  a.assetcatchange_cat,a.assetcatchange_reason,a.assetcatchange_status,
										  date_format(b.assetdetails_capdate,''%d-%b-%Y'') as cap_date,
                                          b.assetdetails_cost as old_cost,b.assetdetails_cost as new_cost,
										  c.product_displayname,d.branch_name,e.assetlocation_name,e.assetlocation_floor,
                                          ifnull(e.assetlocation_remarks,'''') as remark,b.assetdetails_value,
                                          fn_Asset_Data(''ASSET_TRAN'',b.assetdetails_gid,b.entity_gid,''{}'') as lj_default_details,
                                          b.assetdetails_imagepath,b.assetdetails_status
								  from fa_trn_tassetcatchange as a
								      inner join fa_trn_tassetdetails as b on b.assetdetails_id = a.assetcatchange_assetdetailsid
								      inner join gal_mst_tproduct as c on c.product_gid = b.assetdetails_productgid
								      inner join gal_mst_tbranch as d on d.branch_gid = b.assetdetails_branchgid
								      inner join fa_mst_tassetloaction as e on e.assetlocation_gid = b.assetdetails_assetlocationgid
                                      inner join fa_mst_tassetcat as g on g.assetcat_gid = a.assetcatchange_cat
								  where a.assetcatchange_isactive = ''Y'' and a.assetcatchange_isremoved = ''N''
										and a.entity_gid in (',@Entity_Gids,')
										and b.assetdetails_isactive = ''Y'' and b.assetdetails_isremoved = ''N''
                                        and b.entity_gid in (',@Entity_Gids,')
										and c.product_isactive = ''Y'' and c.product_isremoved = ''N''
                                        and c.entity_gid in (',@Entity_Gids,')
										and d.branch_isactive = ''Y'' and d.branch_isremoved = ''N''
                                        and d.entity_gid in (',@Entity_Gids,')
										and e.assetlocation_isactive = ''Y'' and e.assetlocation_isremoved = ''N''
										and e.entity_gid in (',@Entity_Gids,')
                                        and g.assetcat_isactive = ''Y'' and g.assetcat_isremoved = ''N''
										and g.entity_gid in (',@Entity_Gids,') ',Query_Search,'
                                  order by assetcatchange_gid desc
								');

								set @Query_Select = Query_Select;
								#select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;

 elseif ls_Type = 'CAT_DETAILS' and ls_Sub_Type = 'CHECKER_SUMMARY' then
                                 #### CAT Checker Summary
                                 #### Search TO DO
                                 #wip
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Id'))) into @Asset_Id;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Value'))) into @Asset_Value;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Cap_Date'))) into @Asset_CP_Date;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Code'))) into @Category_Name;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Branch'))) into @Branch_Name;

					#select @Asset_Id,@Asset_Value,@Asset_CP_Date,@Category_Name,@Branch_Name;


                    set Query_Search = '';

                    if @Asset_Id <> '' and @Asset_Id is not null  then
                         set Query_Search = concat(Query_Search,' and a.assetdetails_id like ''','%',@Asset_Id,'%','''  ');
                    End if;

                    if @Asset_Value <> '' and @Asset_Value is not null then
                         set Query_Search = concat(Query_Search,' and a.assetdetails_value like ''','%',@Asset_Value,'%','''  ');
                    End if;

					if @Asset_CP_Date <> '' and @Asset_CP_Date is not null  then
                        set Query_Search = concat(Query_Search,'and date_format(a.assetdetails_capdate,''%Y-%m-%d'') = ''',@Asset_CP_Date,'''  ');
                    End if;

                    if @Category_Name <> '' and @Category_Name is not null  then
                         set Query_Search = concat(Query_Search,' and g.assetcat_subcatname like ''','%',@Category_Name,'%','''  ');
                    End if;

                    if @Branch_Name <> '' and @Branch_Name is not null  then
                         set Query_Search = concat(Query_Search,' and d.branch_name like ''','%',@Branch_Name,'%','''  ');
                    End if;


	 set Query_Select = '';
	 set Query_Select = concat('Select a.assetdetails_gid,b.assetcatchange_gid,a.assetdetails_id,a.assetdetails_value,
									   date_format(a.assetdetails_capdate,''%d-%b-%Y'') as cap_date,
									   b.assetcatchange_reason,b.assetcatchange_status,b.assetcatchange_oldcat,
                                       g.assetcat_subcatname as new_catname,b.assetcatchange_cat,c.product_displayname,
                                       d.branch_name,e.assetlocation_name,e.assetlocation_floor,a.assetdetails_imagepath,
									   fn_Asset_Data(''ASSET_TMP'',a.assetdetails_gid,a.entity_gid,''{}'') as lj_default_details,
                                       t.assetdetails_cost as old_cost,a.assetdetails_cost as new_cost
								from fa_tmp_tassetdetails as a
									inner join fa_trn_tassetcatchange as b on b.assetcatchange_assetdetailsid = a.assetdetails_id
									inner join gal_mst_tproduct as c on c.product_gid = a.assetdetails_productgid
									inner join gal_mst_tbranch as d on d.branch_gid = a.assetdetails_branchgid
									inner join fa_mst_tassetloaction as e on e.assetlocation_gid = a.assetdetails_assetlocationgid
                                    inner join fa_mst_tassetcat as g on g.assetcat_subcatname = b.assetcatchange_cat
                                    inner join fa_trn_tassetdetails as t on t.assetdetails_gid = a.assetdetails_mainassetdetailsgid
								where a.assetdetails_requestfor = ''ASSETCAT'' and b.assetcatchange_status = ''SUBMITTED''
									  and a.assetdetails_isactive = ''Y'' and a.assetdetails_isremoved = ''N''
									  and a.entity_gid in (',@Entity_Gids,')
									  and b.assetcatchange_isactive = ''Y'' and b.assetcatchange_isremoved = ''N''
                                      and b.entity_gid in (',@Entity_Gids,')
									  and c.product_isactive = ''Y'' and c.product_isremoved = ''N''
									  and c.entity_gid in (',@Entity_Gids,')
									  and d.branch_isactive = ''Y'' and d.branch_isremoved = ''N''
									  and d.entity_gid in (',@Entity_Gids,')
                                      and e.assetlocation_isactive = ''Y'' and e.assetlocation_isremoved = ''N''
									  and e.entity_gid in (',@Entity_Gids,')
									  and g.assetcat_isactive = ''Y'' and g.assetcat_isremoved = ''N''
									  and g.entity_gid in (',@Entity_Gids,')
									  and t.assetdetails_isactive = ''Y'' and t.assetdetails_isremoved = ''N''
									  and t.entity_gid in (',@Entity_Gids,') ',Query_Search,'
                                order by assetcatchange_gid desc
										');

								set @Query_Select = Query_Select;
							    #select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;

 elseif ls_Type = 'CLUB_DETAILS' and ls_Sub_Type = 'CHECKER_SUMMARY' then
                                 #### CAT Checker Summary
                                 #### Search TO DO
                                 #wip

                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Id'))) into @Asset_Id;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Value'))) into @Asset_Value;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Cap_Date'))) into @Asset_CP_Date;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Code'))) into @Category_Name;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Branch'))) into @Branch_Name;

					# select @Asset_Id,@Asset_Value,@Asset_CP_Date,@Category_Name,@Branch_Name;

                    set Query_Search = '';

                    if @Asset_Id <> '' and @Asset_Id is not null  then
                         set Query_Search = concat(Query_Search,' and a.assetdetails_id like ''','%',@Asset_Id,'%','''  ');
                    End if;

                    if @Asset_Value <> '' and @Asset_Value is not null then
                         set Query_Search = concat(Query_Search,' and a.assetdetails_value like ''','%',@Asset_Value,'%','''  ');
                    End if;

					if @Asset_CP_Date <> '' and @Asset_CP_Date is not null  then
                        set Query_Search = concat(Query_Search,'and date_format(a.assetdetails_capdate,''%Y-%m-%d'') = ''',@Asset_CP_Date,'''  ');
                    End if;

                    if @Category_Name <> '' and @Category_Name is not null  then
                         set Query_Search = concat(Query_Search,' and g.assetcat_subcatname like ''','%',@Category_Name,'%','''  ');
                    End if;

                    if @Branch_Name <> '' and @Branch_Name is not null  then
                         set Query_Search = concat(Query_Search,' and c.branch_name like ''','%',@Branch_Name,'%','''  ');
                    End if;



					set Query_Select = '';
					set Query_Select = concat('Select a.assetdetails_gid,a.assetdetails_id,a.assetdetails_value,
                            a.assetdetails_imagepath,g.assetcat_subcatname,
                            date_format(a.assetdetails_capdate,''%d-%b-%Y'') as cp_date,a.assetdetails_requeststatus,
							c.branch_name,d.product_displayname,e.assetlocation_name,e.assetlocation_floor,

							(Select concat(''['', group_concat(JSON_OBJECT(''child_gid'',b.assetdetails_gid,''aaset_id'',
                             b.assetdetails_id,''asset_cost'',b.assetdetails_cost,
                             ''Image_Path'',b.assetdetails_imagepath,''product_name'',y.product_displayname,
                             ''location_name'',z.assetlocation_name,''cp_date'',date_format(b.assetdetails_capdate,''%d-%b-%Y'')
                            )) ,'']'')
							from fa_tmp_tassetdetails as b
                               inner join fa_mst_tassetloaction as z on z.assetlocation_gid = b.assetdetails_assetlocationgid
                            inner join gal_mst_tproduct as y on y.product_gid = b.assetdetails_productgid
							 where b.assetdetails_parentgid = a.assetdetails_gid
                             and b.assetdetails_gid <> b.assetdetails_parentgid
                             )
							 as lj_child_data
							from fa_tmp_tassetdetails as a
                            inner join gal_mst_tbranch as c on c.branch_gid = a.assetdetails_branchgid
							inner join fa_mst_tassetcat as g on g.assetcat_gid = a.assetdetails_assetcatgid
                            inner join gal_mst_tproduct as d on d.product_gid = a.assetdetails_productgid
                            inner join fa_mst_tassetloaction as e on e.assetlocation_gid = a.assetdetails_assetlocationgid
							where a.assetdetails_requeststatus = ''SUBMITTED'' and
                            a.assetdetails_gid = a.assetdetails_parentgid and
                             g.assetcat_isactive=''Y'' and g.assetcat_isremoved=''N''
                                     and g.entity_gid in (',@Entity_Gids,')
								',Query_Search,' and a.entity_gid in (',@Entity_Gids,')
										');
### TO DO Remove ::: Remove
								set @Query_Select = Query_Select;
			      			    #select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;

elseif ls_Type = 'MERGE_DETAILS' and ls_Sub_Type = 'SUMMARY' then


                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Id'))) into @Asset_Id;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Value'))) into @Asset_Value;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Cap_Date'))) into @Asset_CP_Date;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Code'))) into @Category_Name;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Branch'))) into @Branch_Name;

					# select @Asset_Id,@Asset_Value,@Asset_CP_Date,@Category_Name,@Branch_Name;

                    set Query_Search = '';

                    if @Asset_Id <> '' and @Asset_Id is not null  then
                         set Query_Search = concat(Query_Search,' and b.assetdetails_id like ''','%',@Asset_Id,'%','''  ');
                    End if;

                    if @Asset_Value <> '' and @Asset_Value is not null then
                         set Query_Search = concat(Query_Search,' and b.assetdetails_value like ''','%',@Asset_Value,'%','''  ');
                    End if;

					if @Asset_CP_Date <> '' and @Asset_CP_Date is not null  then
                        set Query_Search = concat(Query_Search,'and date_format(b.assetdetails_capdate,''%Y-%m-%d'') = ''',@Asset_CP_Date,'''  ');
                    End if;

                    #if @Category_Name <> '' and @Category_Name is not null  then
                         #set Query_Search = concat(Query_Search,' and g.assetcat_subcatname like ''','%',@Category_Name,'%','''  ');
                    #End if;

                    if @Branch_Name <> '' and @Branch_Name is not null  then
                         set Query_Search = concat(Query_Search,' and c.branch_name like ''','%',@Branch_Name,'%','''  ');
                    End if;


			set Query_Select = '';
			set Query_Select = concat('Select a.assetmergeheader_gid,b.assetdetails_id,b.assetdetails_assetlocationgid,
											  date_format(a.assetmergeheader_date,''%d-%b-%Y'') as assetmergeheader_date ,
											  date_format(b.assetdetails_capdate,''%d-%b-%Y'') as assetdetails_capdate ,
											  c.branch_name,d.assetlocation_name,a.assetmergeheader_reason,a.assetmergeheader_status,
											  a.assetmergeheader_value,b.assetdetails_status,b.assetdetails_requestfor,
											  b.assetdetails_requeststatus,b.assetdetails_imagepath,
											  fn_Asset_Data(''ASSET_TRAN'',b.assetdetails_gid,
											  b.entity_gid,''{}'') as lj_default_details,
											  m.assetmerge_assetdetailsid,a.assetmergeheader_newassetid
										from fa_trn_tassetmergeheader as a
											inner join fa_trn_tassetmerge as m on a.assetmergeheader_gid = m.assetmerge_assetmergeheader_gid
											inner join fa_trn_tassetdetails as b on b.assetdetails_id = m.assetmerge_assetdetailsid
											inner join gal_mst_tbranch as c on c.branch_gid = b.assetdetails_branchgid
                                            inner join fa_mst_tassetloaction as d on d.assetlocation_gid = b.assetdetails_assetlocationgid
										where a.assetmergeheader_isactive = ''Y'' and a.assetmergeheader_isremoved = ''N'' and
												a.entity_gid in (',@Entity_Gids,')
												and b.assetdetails_isactive  = ''Y'' and b.assetdetails_isremoved = ''N'' and
												b.entity_gid in (',@Entity_Gids,')
												and c.branch_isactive = ''Y'' and c.branch_isremoved = ''N''
                                                and d.assetlocation_isactive = ''Y'' and d.assetlocation_isremoved = ''N''
												',Query_Search,' and c.entity_gid in (',@Entity_Gids,')
												order by assetdetails_capdate desc
										');

								set @Query_Select = Query_Select;
								#select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;

 elseif ls_Type = 'MERGE_DETAILS' and ls_Sub_Type = 'CHECKER_SUMMARY' then
                                 #### CAT Checker Summary
                                 #### Search TO DO
                                 #wip


                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Id'))) into @Asset_Id;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Value'))) into @Asset_Value;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Cap_Date'))) into @Asset_CP_Date;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Code'))) into @Category_Name;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Branch'))) into @Branch_Name;

					 #select @Asset_Id,@Asset_Value,@Asset_CP_Date,@Category_Name,@Branch_Name;

                    set Query_Search = '';

                    #if @Asset_Id <> '' and @Asset_Id is not null  then
                        # set Query_Search = concat(Query_Search,' and z.assetmerge_assetdetailsid like ''','%',@Asset_Id,'%','''  ');
                    #End if;

                    if @Asset_Value <> '' and @Asset_Value is not null then
                         set Query_Search = concat(Query_Search,' and b.assetdetails_value like ''','%',@Asset_Value,'%','''  ');
                    End if;

					if @Asset_CP_Date <> '' and @Asset_CP_Date is not null  then
                        set Query_Search = concat(Query_Search,'and date_format(b.assetdetails_capdate,''%d-%b-%Y'') = ''',@Asset_CP_Date,'''  ');
                    End if;

                    if @Category_Name <> '' and @Category_Name is not null  then
                         set Query_Search = concat(Query_Search,' and g.assetcat_subcatname like ''','%',@Category_Name,'%','''  ');
                    End if;

                    if @Branch_Name <> '' and @Branch_Name is not null  then
                         set Query_Search = concat(Query_Search,' and c.branch_name like ''','%',@Branch_Name,'%','''  ');
                    End if;


                    set Query_Search1 = '';

                    if @Asset_Id <> '' and @Asset_Id is not null  then
                         set Query_Search1 = concat(Query_Search1,' and z.assetmerge_assetdetailsid like ''','%',@Asset_Id,'%','''  ');
                    End if;

                   # if @Asset_Value <> '' and @Asset_Value is not null then
                       # set Query_Search1 = concat(Query_Search1,' and b.assetdetails_value like ''','%',@Asset_Value,'%','''  ');
                    #End if;

					 if @Asset_CP_Date <> '' and @Asset_CP_Date is not null  then
						set Query_Search1 = concat(Query_Search1,'and date_format(b.assetdetails_capdate,''%d-%b-%Y'') = ''',@Asset_CP_Date,'''  ');
                     End if;

                     if @Category_Name <> '' and @Category_Name is not null  then
                          set Query_Search1 = concat(Query_Search1,' and g.assetcat_subcatname like ''','%',@Category_Name,'%','''  ');
                     End if;

                     if @Branch_Name <> '' and @Branch_Name is not null  then
                          set Query_Search1 = concat(Query_Search1,' and c.branch_name like ''','%',@Branch_Name,'%','''  ');
                    End if;

				set Query_Select = '';
				set Query_Select = concat('Select a.assetmergeheader_gid,b.assetdetails_id as new_id,
									c.branch_name,d.assetlocation_name,
									(select concat( ''['',group_concat(json_object(''ids'',z.assetmerge_assetdetailsid
                                    ,''asset_value'',b.assetdetails_value ,''asset_value'',b.assetdetails_value,
                                  ''assetcat_subcatname'' ,g.assetcat_subcatname ,''status'' ,b.assetdetails_requeststatus ,
                                  ''product_name'' ,p.product_name ,''branch_name'' ,c.branch_name,
                                  ''cp_date'',  date_format(b.assetdetails_capdate,''%d-%b-%Y'')
                                  )),'']'')
									   from fa_trn_tassetmerge as z
									   inner join fa_tmp_tassetdetails as y on y.assetdetails_id = z.assetmerge_assetdetailsid
									   where z.assetmerge_isactive = ''Y''
                                       and z.assetmerge_assetmergeheader_gid = a.assetmergeheader_gid
                                       ',Query_Search1,'
									 ) as lj_default_details,b.assetdetails_value,
                                     date_format(b.assetdetails_capdate,''%d-%b-%Y'') as assetdetails_capdate,
                                     g.assetcat_subcatname,b.assetdetails_requeststatus,b.assetdetails_status,p.product_name
									 from fa_trn_tassetmergeheader as a
									inner join fa_tmp_tassetdetails as b on b.assetdetails_id = a.assetmergeheader_newassetid
                                    inner join gal_mst_tbranch as c on c.branch_gid = b.assetdetails_branchgid
                                    inner join fa_mst_tassetcat as g on g.assetcat_gid = b.assetdetails_assetcatgid
                                    inner join gal_mst_tproduct as p on p.product_gid = b.assetdetails_productgid
									inner join fa_mst_tassetloaction as d on d.assetlocation_gid = b.assetdetails_assetlocationgid
									where   g.assetcat_isactive=''Y'' and g.assetcat_isremoved=''N''
                                     and g.entity_gid in (',@Entity_Gids,')
                                    and a.assetmergeheader_status = ''SUBMITTED''
                                     and a.assetmergeheader_isactive = ''Y'' and a.assetmergeheader_isremoved = ''N''
                                     and d.assetlocation_isactive = ''Y'' and d.assetlocation_isremoved = ''N''
									 and a.entity_gid in (',@Entity_Gids,') ',Query_Search,'
										');
### TO DO Remove ::: Remove
								set @Query_Select = Query_Select;
			      			    #select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;


 elseif ls_Type = 'VALUE_DETAILS' and ls_Sub_Type = 'CHECKER_SUMMARY' then
                                 #### Imppairment Checker Summary
                                 #### Search TO DO
                                 #wip

                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Id'))) into @Asset_Id;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Value'))) into @Asset_Value;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Cap_Date'))) into @Asset_CP_Date;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Code'))) into @Category_Name;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Branch'))) into @Branch_Name;

					# select @Asset_Id,@Asset_Value,@Asset_CP_Date,@Category_Name,@Branch_Name;

                    set Query_Search = '';

                    if @Asset_Id <> '' and @Asset_Id is not null  then
                         set Query_Search = concat(Query_Search,' and a.assetdetails_id like ''','%',@Asset_Id,'%','''  ');
                    End if;

                    if @Asset_Value <> '' and @Asset_Value is not null then
                         set Query_Search = concat(Query_Search,' and a.assetdetails_value like ''','%',@Asset_Value,'%','''  ');
                    End if;

					if @Asset_CP_Date <> '' and @Asset_CP_Date is not null  then
                        set Query_Search = concat(Query_Search,'and date_format(a.assetdetails_capdate,''%Y-%m-%d'') = ''',@Asset_CP_Date,'''  ');
                    End if;

                    if @Category_Name <> '' and @Category_Name is not null  then
                         set Query_Search = concat(Query_Search,' and g.assetcat_subcatname like ''','%',@Category_Name,'%','''  ');
                    End if;

                    if @Branch_Name <> '' and @Branch_Name is not null  then
                         set Query_Search = concat(Query_Search,' and c.branch_name like ''','%',@Branch_Name,'%','''  ');
                    End if;

                   #select Query_Search;

				set Query_Select = '';
				set Query_Select = concat('Select a.assetdetails_gid,a.assetdetails_branchgid,date_format(a.assetdetails_capdate,''%d-%b-%Y'') as assetdetails_capdate,
								b.assetvalue_gid,a.assetdetails_id,c.branch_name,a.assetdetails_requeststatus,
                                date_format(b.assetvalue_date,''%d-%b-%Y'') as assetvalue_date,g.assetcat_subcatname,
                                b.assetvalue_reason,b.assetvalue_value,b.assetvalue_oldvalue,
								a.assetdetails_imagepath,fn_Asset_Data(''ASSET_TMP'',a.assetdetails_gid,a.entity_gid,''{}'')
                                as lj_default_details
							from fa_tmp_tassetdetails as a
								inner join fa_trn_tassetvalue as b on b.assetvalue_assetdetailsid = a.assetdetails_id
                                   and b.assetvalue_status = ''SUBMITTED''
								inner join gal_mst_tbranch as c on c.branch_gid = a.assetdetails_branchgid
                                inner join fa_mst_tassetcat as g on g.assetcat_gid = a.assetdetails_assetcatgid
							where a.assetdetails_requestfor = ''VALUE REDUCTION'' and a.assetdetails_requeststatus = ''SUBMITTED''
								and a.assetdetails_isactive = ''Y'' and a.assetdetails_isremoved = ''N'' and a.entity_gid in (',@Entity_Gids,')
								and b.assetvalue_isactive = ''Y'' and b.assetvalue_isremoved = ''N'' and b.entity_gid in (',@Entity_Gids,')
                                and c.branch_isactive=''Y''and c.branch_isremoved=''N''  and c.entity_gid in (',@Entity_Gids,')
                                and g.assetcat_isactive=''Y'' and g.assetcat_isremoved=''N'' and g.entity_gid in (',@Entity_Gids,')
                                ',Query_Search,'
                                order by assetvalue_date desc
										');

								set @Query_Select = Query_Select;
			      			    #select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;

 elseif ls_Type = 'SPLIT_DETAILS' and ls_Sub_Type = 'MAKER_SUMMARY' then
                                 #### Split Checker Summary
                                 #### Search TO DO
                                 #wip

                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Id'))) into @Asset_Id;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Value'))) into @Asset_Value;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Cap_Date'))) into @Asset_CP_Date;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Code'))) into @Category_Name;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Branch'))) into @Branch_Name;

					# select @Asset_Id,@Asset_Value,@Asset_CP_Date,@Category_Name,@Branch_Name;

                    set Query_Search = '';

                    if @Asset_Id <> '' and @Asset_Id is not null  then
                         set Query_Search = concat(Query_Search,' and c.assetdetails_id like ''','%',@Asset_Id,'%','''  ');
                    End if;

                    if @Asset_Value <> '' and @Asset_Value is not null then
                         set Query_Search = concat(Query_Search,' and c.assetdetails_value like ''','%',@Asset_Value,'%','''  ');
                    End if;

					if @Asset_CP_Date <> '' and @Asset_CP_Date is not null  then
                        set Query_Search = concat(Query_Search,'and date_format(c.assetdetails_capdate,''%Y-%m-%d'') = ''',@Asset_CP_Date,'''  ');
                    End if;

                    if @Category_Name <> '' and @Category_Name is not null  then
                         set Query_Search = concat(Query_Search,' and ct.assetcat_subcatname like ''','%',@Category_Name,'%','''  ');
                    End if;

                    if @Branch_Name <> '' and @Branch_Name is not null  then
                         set Query_Search = concat(Query_Search,' and br.branch_name like ''','%',@Branch_Name,'%','''  ');
                    End if;


				set Query_Select = '';
				set Query_Select = concat('Select a.assetsplitheader_gid,a.assetsplitheader_assetdetailsid,
													a.assetsplitheader_reason,a.assetsplitheader_date,
													a.assetsplitheader_value,a.assetsplitheader_status,
													b.assetsplit_newassetdetailsid,b.assetsplit_value,br.branch_name,
													p.product_name,l.assetlocation_name,ct.assetcat_subcatname,
                                                    date_format(c.assetdetails_capdate,''%d-%b-%Y'') as assetdetails_capdate,
                                                    c.assetdetails_status
											from fa_trn_tassetsplitheader as a
												inner join fa_trn_tassetsplit as b on b.assetsplit_assetsplitheader_gid = a.assetsplitheader_gid
												inner join fa_trn_tassetdetails as c on c.assetdetails_id = a.assetsplitheader_assetdetailsid
												inner join gal_mst_tbranch as br on br.branch_gid = c.assetdetails_branchgid
												inner join gal_mst_tproduct as p on p.product_gid = c.assetdetails_productgid
												inner join fa_mst_tassetloaction as l on l.assetlocation_gid = c.assetdetails_assetlocationgid
												inner join fa_mst_tassetcat as ct on ct.assetcat_gid = c.assetdetails_assetcatgid
											where a.assetsplitheader_isactive = ''Y'' and a.assetsplitheader_isremoved = ''N''
												  and a.entity_gid in (',@Entity_Gids,')
												  and c.assetdetails_isactive = ''Y'' and c.assetdetails_isremoved = ''N''
												  and c.entity_gid in (',@Entity_Gids,')
												  and b.assetsplit_isactive = ''Y'' and b.assetsplit_isremoved = ''N''
												  and b.entity_gid in (',@Entity_Gids,')
                                                  and br.branch_isactive = ''Y'' and br.branch_isremoved = ''N''
												  and br.entity_gid in (',@Entity_Gids,')
                                                  and p.product_isactive = ''Y'' and p.product_isremoved = ''N''
												  and p.entity_gid in (',@Entity_Gids,')
                                                  and l.assetlocation_isactive = ''Y'' and l.assetlocation_isremoved = ''N''
												  and l.entity_gid in (',@Entity_Gids,')
                                                  and ct.assetcat_isactive = ''Y'' and ct.assetcat_isremoved = ''N''
												  and ct.entity_gid in (',@Entity_Gids,')  ',Query_Search,'

										');
							### TO DO Remove ::: Remove
								set @Query_Select = Query_Select;
			      			    #select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;


 elseif ls_Type = 'SPLIT_DETAILS' and ls_Sub_Type = 'CHECKER_SUMMARY' then
                                 #### Split Checker Summary
                                 #wip
					select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Id'))) into @Asset_Id;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Value'))) into @Asset_Value;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Cap_Date'))) into @Asset_CP_Date;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Code'))) into @Category_Name;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Branch'))) into @Branch_Name;

					# select @Asset_Id,@Asset_Value,@Asset_CP_Date,@Category_Name,@Branch_Name;

                    set Query_Search = '';

                    if @Asset_Id <> '' and @Asset_Id is not null  then
                         set Query_Search = concat(Query_Search,' and b.assetdetails_id like ''','%',@Asset_Id,'%','''  ');
                    End if;

                    if @Asset_Value <> '' and @Asset_Value is not null then
                         set Query_Search = concat(Query_Search,' and b.assetdetails_value like ''','%',@Asset_Value,'%','''  ');
                    End if;

					if @Asset_CP_Date <> '' and @Asset_CP_Date is not null  then
                        set Query_Search = concat(Query_Search,'and date_format(b.assetdetails_capdate,''%Y-%m-%d'') = ''',@Asset_CP_Date,'''  ');
                    End if;

                    if @Category_Name <> '' and @Category_Name is not null  then
                         set Query_Search = concat(Query_Search,' and g.assetcat_subcatname like ''','%',@Category_Name,'%','''  ');
                    End if;

                    if @Branch_Name <> '' and @Branch_Name is not null  then
                         set Query_Search = concat(Query_Search,' and c.branch_name like ''','%',@Branch_Name,'%','''  ');
                    End if;


				set Query_Select = '';
				set Query_Select = concat('Select a.assetsplitheader_gid,a.assetsplitheader_assetdetailsid,
										b.assetdetails_id,date_format(a.assetsplitheader_date,''%d-%b-%Y'') as assetsplitheader_date ,
										a.assetsplitheader_value,a.assetsplitheader_reason,a.assetsplitheader_status, b.assetdetails_requeststatus,
                                        date_format(b.assetdetails_capdate,''%d-%b-%Y'') as assetdetails_capdate,
										(
										select ifnull(concat(''['',group_concat(json_object(''asset_id'',y.assetdetails_id,
                                        ''asset_value'',y.assetdetails_value,''assetsplitheader_status'',a.assetsplitheader_status,
                                       ''branch_name'',c.branch_name,''product_name'',p.product_name,''assetcat_subcatname'',g.assetcat_subcatname
                                       ,''cp_date'',  date_format(b.assetdetails_capdate,''%d-%b-%Y'')
                                       )),'']''),''[]'')
										from fa_trn_tassetsplit as z
										inner join fa_tmp_tassetdetails  as y on y.assetdetails_id = z.assetsplit_newassetdetailsid
										where z.assetsplit_assetsplitheader_gid = a.assetsplitheader_gid
										) as lj_split_values,c.branch_name,p.product_name,g.assetcat_subcatname ,
                                        fn_Asset_Data(''ASSET_TMP'',b.assetdetails_gid,a.entity_gid,''{}'') as lj_default_details
										from fa_trn_tassetsplitheader as a
										inner join fa_tmp_tassetdetails as b on b.assetdetails_id = a.assetsplitheader_assetdetailsid
                                        inner join gal_mst_tbranch as c on c.branch_gid = b.assetdetails_branchgid
										inner join fa_mst_tassetcat as g on g.assetcat_gid = b.assetdetails_assetcatgid
										inner join gal_mst_tproduct as p on p.product_gid = b.assetdetails_productgid
										where a.assetsplitheader_isactive = ''Y'' and a.assetsplitheader_isremoved = ''N''
										and a.assetsplitheader_status = ''SUBMITTED'' and
                                          g.assetcat_isactive=''Y'' and g.assetcat_isremoved=''N''
                                     and g.entity_gid in (',@Entity_Gids,')
										',Query_Search,' and a.entity_gid in (',@Entity_Gids,')
										');
							### TO DO Remove ::: Remove
								set @Query_Select = Query_Select;
			      			    #select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;

elseif ls_Type = 'SALE_DETAILS' and ls_Sub_Type = 'HEADER_SUMMARY' then

         ### search Comes Here - Checker Summary
         set Query_Search = '';

					select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Id'))) into @Asset_Id;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Value'))) into @Asset_Value;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Cap_Date'))) into @Asset_CP_Date;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Code'))) into @Category_Name;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Branch'))) into @Branch_Name;

                 set Query_Search = '';

                    if @Asset_Id <> '' and @Asset_Id is not null  then
                         set Query_Search = concat(Query_Search,' and t.assetdetails_id like ''','%',@Asset_Id,'%','''  ');
                    End if;

                    if @Asset_Value <> '' and @Asset_Value is not null then
                         set Query_Search = concat(Query_Search,' and t.assetdetails_value like ''','%',@Asset_Value,'%','''  ');
                    End if;

					if @Asset_CP_Date <> '' and @Asset_CP_Date is not null  then
                        set Query_Search = concat(Query_Search,'and date_format(t.assetdetails_capdate,''%Y-%m-%d'') = ''',@Asset_CP_Date,'''  ');
                    End if;

                    if @Category_Name <> '' and @Category_Name is not null  then
                         set Query_Search = concat(Query_Search,' and ct.assetcat_subcatname like ''','%',@Category_Name,'%','''  ');
                    End if;

                    if @Branch_Name <> '' and @Branch_Name is not null  then
                         set Query_Search = concat(Query_Search,' and c.branch_name like ''','%',@Branch_Name,'%','''  ');
                    End if;
                        #and b.customer_isremoved=''N''  we need include

     set Query_Select = '';
	 set Query_Select = concat('Select a.assetsaleheader_gid,a.assetsaleheader_saletotalamount,a.assetsaleheader_status,
								a.assetsaleheader_remarks,b.customer_name,
								DATE_FORMAT(a.assetsaleheader_saledate,''%d-%m-%Y'') as sale_date,
								count(d.assetsale_gid) as total_count,
								c.branch_name,ct.assetcat_subcatname,d.assetsale_date
							from fa_trn_tassetsaleheader as a
								inner join gal_mst_tcustomer as b on b.customer_gid = a.assetsaleheader_customergid
								inner join gal_mst_tbranch as c on c.branch_gid = a.assetsaleheader_salebranchgid
								inner join fa_trn_tassetsale as d on d.assetsale_assetsaleheadergid = a.assetsaleheader_gid
							    inner join fa_tmp_tassetdetails as t on t.assetdetails_id = d.assetsale_assetdetailsid
                                inner join fa_mst_tassetcat as ct on ct.assetcat_gid = t.assetdetails_assetcatgid
							where a.assetsaleheader_status = ''PENDING''
								and a.assetsaleheader_isactive = ''Y'' and a.assetsaleheader_isremoved = ''N''
                                and b.customer_isactive=''Y''
								and c.branch_isactive = ''Y'' and c.branch_isremoved = ''N''
								and d.assetsale_isactive = ''Y'' and d.assetsale_isremoved = ''N''
                                and t.assetdetails_isactive=''Y'' and t.assetdetails_isremoved=''N''
                                and ct.assetcat_isactive=''Y'' and ct.assetcat_isremoved=''N''
								',Query_Search,' and a.entity_gid in (',@Entity_Gids,') and b.entity_gid in (',@Entity_Gids,')
                                and c.entity_gid in (',@Entity_Gids,') and d.entity_gid in (',@Entity_Gids,')
                                and t.entity_gid in (',@Entity_Gids,')  and ct.entity_gid in (',@Entity_Gids,')
								group by a.assetsaleheader_gid,a.assetsaleheader_saletotalamount,a.assetsaleheader_status,
								a.assetsaleheader_remarks,b.customer_name,c.branch_name,assetsaleheader_saledate');

         						set @Query_Select = Query_Select;
			      			   # select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;

 elseif ls_Type = 'SALE_DETAILS' and ls_Sub_Type = 'HEADER_DETAIL' then

 			### search Comes Here
         set Query_Search = '';
        select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_SaleHeader_Gid'))) into @Asset_SaleHeader_Gid;

         if @Asset_SaleHeader_Gid is null or @Asset_SaleHeader_Gid = 0 THEN
         	set Message = 'Asset Sale Header Gid Is Needed.';
            leave sp_FAAssertProcess_Get;
         ELSE
              set Query_Search = concat(Query_Search,' and a.assetsaleheader_gid  = ',@Asset_SaleHeader_Gid,'');
         End if;

         set Query_Select = '';
         set Query_Select = concat('Select a.assetsaleheader_gid,d.assetsale_value ,a.assetsaleheader_saletotalamount,a.assetsaleheader_status,
								a.assetsaleheader_remarks,b.customer_name,c.branch_name,
								DATE_FORMAT(a.assetsaleheader_saledate,''%d-%m-%Y'') as sale_date,
								fn_Asset_Data(''ASSET_TMP'',e.assetdetails_gid,a.entity_gid,''{}'')
                                as lj_default_details
								 from fa_trn_tassetsaleheader as a
								inner join gal_mst_tcustomer as b on b.customer_gid = a.assetsaleheader_customergid
								inner join gal_mst_tbranch as c on c.branch_gid = a.assetsaleheader_salebranchgid
								inner join fa_trn_tassetsale as d on d.assetsale_assetsaleheadergid = a.assetsaleheader_gid
                                inner join fa_tmp_tassetdetails as e on e.assetdetails_id = d.assetsale_assetdetailsid
								where a.assetsaleheader_status = ''PENDING''
								and a.assetsaleheader_isactive = ''Y'' and a.assetsaleheader_isremoved = ''N''
								and c.branch_isactive = ''Y'' and c.branch_isremoved = ''N''
								and d.assetsale_isactive = ''Y'' and d.assetsale_isremoved = ''N''
								',Query_Search,' and a.entity_gid in (',@Entity_Gids,')
								');

         						set @Query_Select = Query_Select;
			      			    #select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;

elseif ls_Type = 'SALE_DETAILS' and ls_Sub_Type = 'MAKER_SUMMARY' then

 			### search Comes Here      --- SALE MAKER_SUMMARY

					select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Id'))) into @Asset_Id;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Value'))) into @Asset_Value;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Cap_Date'))) into @Asset_CP_Date;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Code'))) into @Category_Name;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Branch'))) into @Branch_Name;

         set Query_Search = '';

					 if @Asset_Id <> '' and @Asset_Id is not null  then
                         set Query_Search = concat(Query_Search,' and c.assetdetails_id like ''','%',@Asset_Id,'%','''  ');
                    End if;

                    if @Asset_Value <> '' and @Asset_Value is not null then
                         set Query_Search = concat(Query_Search,' and c.assetdetails_value like ''','%',@Asset_Value,'%','''  ');
                    End if;

					if @Asset_CP_Date <> '' and @Asset_CP_Date is not null  then
                        set Query_Search = concat(Query_Search,'and date_format(c.assetdetails_capdate,''%Y-%m-%d'') = ''',@Asset_CP_Date,'''  ');
                    End if;

                    if @Category_Name <> '' and @Category_Name is not null  then
                         set Query_Search = concat(Query_Search,' and g.assetcat_subcatname like ''','%',@Category_Name,'%','''  ');
                    End if;

                    if @Branch_Name <> '' and @Branch_Name is not null  then
                         set Query_Search = concat(Query_Search,' and br.branch_name like ''','%',@Branch_Name,'%','''  ');
                    End if;

         set Query_Select = '';
         set Query_Select = concat('select  a.assetsale_gid, a.assetsale_assetsaleheadergid, a.assetsale_assetdetailsid,
									      date_format(a.assetsale_date,''%Y-%m-%d'') as assetsale_date, a.assetsale_status, a.assetsale_reason,
										 a.assetsale_value, a.assetsale_invoiceheadergid, a.create_by assetsale_create_by,
										 b.assetsaleheader_gid, b.assetsaleheader_customergid,
										 b.assetsaleheader_salebranchgid, date_format(b.assetsaleheader_saledate,''%Y-%m-%d'') as assetsaleheader_saledate ,
										 b.assetsaleheader_saletotalamount, b.assetsaleheader_invoiceheadergid,
										 b.assetsaleheader_status, b.assetsaleheader_remarks, b.create_by assetsale_header_create_by,
                                         fn_Asset_Data(''ASSET_TRAN'',c.assetdetails_gid,c.entity_gid,''{}'')
										 as lj_default_details,c.assetdetails_id,c.assetdetails_value,
                                         date_format(c.assetdetails_capdate,''%Y-%m-%d'') assetdetails_capdate,g.assetcat_subcatname,
                                         br.branch_name,h.customer_name,c.assetdetails_imagepath,c.assetdetails_status
									from fa_trn_tassetsale a
										 inner join fa_trn_tassetsaleheader b on a.assetsale_assetsaleheadergid=b.assetsaleheader_gid
										 inner join fa_trn_tassetdetails c on c.assetdetails_id=a.assetsale_assetdetailsid
										 inner join gal_mst_tbranch as br on br.branch_gid = c.assetdetails_branchgid
										 inner join fa_mst_tassetcat as g on g.assetcat_gid = c.assetdetails_assetcatgid
										 inner join gal_mst_tcustomer as h on h.customer_gid =  b.assetsaleheader_customergid
									where a.assetsale_isactive=''Y'' and a.assetsale_isremoved=''N''
										 and a.entity_gid in (',@Entity_Gids,')
										 and b.assetsaleheader_isactive=''Y'' and b.assetsaleheader_isremoved=''N''
                                         and b.entity_gid in (',@Entity_Gids,')
                                         and c.assetdetails_isactive=''Y'' and c.assetdetails_isremoved=''N''
                                         and c.entity_gid in (',@Entity_Gids,')
                                         and br.branch_isactive=''Y'' and br.branch_isremoved=''N''
                                         and br.entity_gid in (',@Entity_Gids,')
                                         and g.assetcat_isactive=''Y'' and g.assetcat_isremoved=''N''
                                         and g.entity_gid in (',@Entity_Gids,')
                                         and h.customer_isactive=''Y'' and h.customer_isremoved=''N''
                                         and h.entity_gid in (',@Entity_Gids,')
                                         ',Query_Search,'
								 ');

         						set @Query_Select = Query_Select;
			      			    #select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;



  elseif ls_Type = 'ASSET_DETAILS' and ls_Sub_Type = 'DETAILS' then
					#### Values Shown On The POP Up screen

					set Query_Search = '';
				    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Product_Gid'))) into @Asset_Product_Gid;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Cat_Gid'))) into @Asset_Cat_Gid;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Branch_Gid'))) into @Asset_Branch_Gid;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Invoice_Gid'))) into @Invoice_Gid;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Invoice_Gid'))) into @Invoice_Gid;

                    ##WIP
					set Query_Select = '';
                    set Query_Select = concat('
                      Select a.assetdetails_gid,a.assetdetails_value,date_format(assetdetails_capdate,''%d-%m-%Y''),a.assetdetails_id,a.assetdetails_branchgid,
						a.assetdetails_requestfor,a.assetdetails_requeststatus,a.assetdetails_imagepath,b.branch_name
						 from fa_trn_tassetdetails as a
                           inner join gal_mst_tbranch as b on b.branch_gid = a.assetdetails_branchgid
                            and b.branch_isactive = ''Y'' and b.branch_isremoved = ''N''
                         where a.assetdetails_isactive = ''Y'' and a.assetdetails_isremoved = ''N''
                         ',Query_Search,'
                         and a.entity_gid in (',@Entity_Gids,')

                    ');

						set @Query_Select = Query_Select;
			      			#select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;

  elseif ls_Type = 'ASSET_DETAILS' and ls_Sub_Type = 'SEARCH' then
					#### Values Shown On The POP Up screen
                    ###Its for ALL.

				    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Product_Gid'))) into @Asset_Product_Gid;
				    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Value'))) into @Asset_Value;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Cap_Date'))) into @Asset_CP_Date;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Branch_Gid'))) into @Asset_Branch_Gid;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Id'))) into @Asset_Id;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Code'))) into @Category_Name;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Branch'))) into @Branch_Name;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Group'))) into @Asset_Group;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Invoice_Gid'))) into @Invoice_Gid;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Page_Index'))) into @Page_Index;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Page_Size'))) into @Page_Size;



                    set Query_Search = '';


                    if @Asset_Value <> '' and @Asset_Value is not null then
                         set Query_Search = concat(Query_Search,' and a.assetdetails_value like ''','%',@Asset_Value,'%','''  ');
                    End if;

                    if @Asset_Id <> '' and @Asset_Id is not null  then
                         set Query_Search = concat(Query_Search,' and a.assetdetails_id like ''','%',@Asset_Id,'%','''  ');
                    End if;

					if @Asset_CP_Date <> '' and @Asset_CP_Date is not null  then
                        set Query_Search = concat(Query_Search,'and date_format(a.assetdetails_capdate,''%Y-%m-%d'') = ''',@Asset_CP_Date,'''  ');
                    End if;

                    if @Branch_Name <> '' and @Branch_Name is not null  then
                         set Query_Search = concat(Query_Search,' and b.branch_name like ''','%',@Branch_Name,'%','''  ');
                    End if;

                    if @Category_Name <> '' and @Category_Name is not null  then
                         set Query_Search = concat(Query_Search,' and g.assetcat_subcatname like ''','%',@Category_Name,'%','''  ');
                    End if;

                    set @total_size= @Page_Index*@Page_Size;

                    if @Page_Index <> '' and @Page_Index is not null and @Page_Size <> '' and @Page_Size is not null  then
                         set Query_Search = concat(Query_Search,' LIMIT ',@Page_Size,' OFFSET ',@total_size,'  ');
                    End if;


                    #select  @Asset_Id;
                    #select @Asset_CP_Date;
                    #select Query_Search;
                    ##WIP
                    set Query_Select = '';
                    set Query_Select = concat('Select a.assetdetails_gid,a.assetdetails_value,a.assetdetails_value as asset_value,
									date_format(assetdetails_capdate,''%d-%b-%Y'') as assetdetails_capdate,a.assetdetails_capdate capdate,
									a.assetdetails_id,a.assetdetails_branchgid,
									a.assetdetails_requestfor,a.assetdetails_requeststatus,a.assetdetails_imagepath,b.branch_name,
									fn_Asset_Data(''ASSET_TRAN'',a.assetdetails_gid,a.entity_gid,''{}'') as lj_default_details,
									g.assetcat_subcatname,g.assetcat_gid,a.assetdetails_productgid
							from fa_trn_tassetdetails as a
									inner join gal_mst_tbranch as b on b.branch_gid = a.assetdetails_branchgid
									inner join fa_mst_tassetcat as g on g.assetcat_gid = a.assetdetails_assetcatgid
							where a.assetdetails_isactive = ''Y'' and a.assetdetails_isremoved = ''N''
									and b.branch_isactive=''Y'' and b.branch_isremoved=''N''
									and g.assetcat_isactive= ''Y'' and g.assetcat_isremoved = ''N''
									and a.assetdetails_status = ''ACTIVE'' and a.assetdetails_requeststatus = ''APPROVED''
									and a.assetdetails_requestfor = ''''

									and a.entity_gid in (',@Entity_Gids,')  and b.entity_gid in (',@Entity_Gids,')
									and g.entity_gid in (',@Entity_Gids,') ',Query_Search,'

							               ');

						set @Query_Select = Query_Select;
			      			   # select @Query_Select; ### Remove It

								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;
elseif ls_Type = 'ASSET_SALE_DETAILS' and ls_Sub_Type = 'SEARCH' then
					#### Values Shown On The POP Up screen
                    ###Its for ALL.

				    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Product_Gid'))) into @Asset_Product_Gid;
				    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Value'))) into @Asset_Value;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Cap_Date'))) into @Asset_CP_Date;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Branch_Gid'))) into @Asset_Branch_Gid;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Id'))) into @Asset_Id;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Code'))) into @Category_Name;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Branch'))) into @Branch_Name;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Asset_Group'))) into @Asset_Group;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Invoice_Gid'))) into @Invoice_Gid;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Page_Index'))) into @Page_Index;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Page_Size'))) into @Page_Size;



                    set Query_Search = '';


                    if @Asset_Value <> '' and @Asset_Value is not null then
                         set Query_Search = concat(Query_Search,' and a.assetdetails_value like ''','%',@Asset_Value,'%','''  ');
                    End if;

                    if @Asset_Id <> '' and @Asset_Id is not null  then
                         set Query_Search = concat(Query_Search,' and a.assetdetails_id like ''','%',@Asset_Id,'%','''  ');
                    End if;

					if @Asset_CP_Date <> '' and @Asset_CP_Date is not null  then
                        set Query_Search = concat(Query_Search,'and date_format(a.assetdetails_capdate,''%Y-%m-%d'') = ''',@Asset_CP_Date,'''  ');
                    End if;

                    if @Branch_Name <> '' and @Branch_Name is not null  then
                         set Query_Search = concat(Query_Search,' and b.branch_name like ''','%',@Branch_Name,'%','''  ');
                    End if;

                    if @Category_Name <> '' and @Category_Name is not null  then
                         set Query_Search = concat(Query_Search,' and g.assetcat_subcatname like ''','%',@Category_Name,'%','''  ');
                    End if;

                    set @total_size= @Page_Index*@Page_Size;

                    if @Page_Index <> '' and @Page_Index is not null and @Page_Size <> '' and @Page_Size is not null  then
                         set Query_Search = concat(Query_Search,' LIMIT ',@Page_Size,' OFFSET ',@total_size,'  ');
                    End if;


                    #select  @Asset_Id;
                    #select @Asset_CP_Date;
                    #select Query_Search;
                    ##WIP
                    set Query_Select = '';
                    set Query_Select = concat('Select a.assetdetails_gid,a.assetdetails_value,a.assetdetails_value as asset_value,
									date_format(assetdetails_capdate,''%d-%b-%Y'') as assetdetails_capdate,a.assetdetails_capdate capdate,
									a.assetdetails_id,a.assetdetails_branchgid,
									a.assetdetails_requestfor,a.assetdetails_requeststatus,a.assetdetails_imagepath,b.branch_name,
									fn_Asset_Data(''ASSET_TRAN'',a.assetdetails_gid,a.entity_gid,''{}'') as lj_default_details,
									g.assetcat_subcatname,g.assetcat_gid,a.assetdetails_productgid,i.hsn_code,i.hsn_sgstrate,i.hsn_cgstrate,
									i.hsn_igstrate
							from fa_trn_tassetdetails as a
									inner join gal_mst_tbranch as b on b.branch_gid = a.assetdetails_branchgid
									inner join fa_mst_tassetcat as g on g.assetcat_gid = a.assetdetails_assetcatgid
                                    inner join gal_mst_tproduct as h on h.product_gid = a.assetdetails_productgid
                                    left  join gal_mst_thsn as i on i.hsn_gid = h.product_hsn_gid
                                      and i.hsn_isactive = ''Y'' and i.hsn_isremoved = ''N''
							where a.assetdetails_isactive = ''Y'' and a.assetdetails_isremoved = ''N''
									and b.branch_isactive=''Y'' and b.branch_isremoved=''N''
									and g.assetcat_isactive= ''Y'' and g.assetcat_isremoved = ''N''
									and a.assetdetails_status = ''ACTIVE'' and a.assetdetails_requeststatus = ''APPROVED''
									and a.assetdetails_requestfor = ''''

									and a.entity_gid in (',@Entity_Gids,')  and b.entity_gid in (',@Entity_Gids,')
									and g.entity_gid in (',@Entity_Gids,') ',Query_Search,'

							               ');

						set @Query_Select = Query_Select;
			      			    #select @Query_Select; ### Remove It

								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;


  else
                         set Message = 'Incorrect Type Data.';
                         leave sp_FAAssertProcess_Get;
 End if;

END