CREATE DEFINER=`developer`@`%` PROCEDURE `galley`.`sp_PRPO_Query_Get`(IN `ls_Type` varchar(64),IN `ls_Sub_Type` varchar(64),
IN `lj_Filters` json,IN `lj_Classification` json, OUT `Message` varchar(1024))
sp_PRPO_Query_Get:BEGIN
	### Ramesh - Jan 18 2019
Declare Query_Column varchar(2048);
Declare Query_Select varchar(6144);
Declare Query_Search varchar(1024);
Declare Query_Join varchar(4000);
Declare Query_Where varchar(2048);
Declare Query_Limit varchar(500);
Declare Query_Group varchar(1024);


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

	select fn_Classification('ENTITY_ONLY',lj_Classification) into @OutMsg_Classification ;
        select  JSON_UNQUOTE(JSON_EXTRACT(@OutMsg_Classification, '$.Entity_Gid[0]')) into @Entity_Gids;
        if @Entity_Gids is  null or @Entity_Gids = '' then
				select  JSON_UNQUOTE(JSON_EXTRACT(@OutMsg_Classification, '$.Message')) into @Message;
				set Message = concat('Error On Classification Data - ',@Message);
                leave sp_PRPO_Query_Get;
        End if;

if ls_Type = 'PR' and ls_Sub_Type = 'QUERY_SUMMARY' THEN


       set Query_Column = '';
       set Query_Search = '';

       select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, '$.Supplier_Group_Gid')) into @Supplier_Group_Gid;
       select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, '$.Supplier_Gid')) into @Supplier_Gid;
       select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, '$.Raiser_Gid')) into @Raiser_Gid;
       select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, '$.Status')) into @Pr_Status;
       select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, '$.Amount')) into @Pr_Amount;
       select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, '$.Commodity_Gid')) into @Commodity_Gid;
       select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, '$.Product_Gid')) into @Product_Gid;
       select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, '$.MEP_No')) into @MEP_No;
       select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, '$.From_Date')) into @Pr_From_Date;
       select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, '$.To_Date')) into @Pr_To_Date;
       select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, '$.Branch_Gid')) into @Branch_Gid;

       if @Supplier_Group_Gid is not null and @Supplier_Group_Gid <> 0 THEN
         set Query_Search = concat('  and d.supplier_groupgid = ',@Supplier_Group_Gid,' ');
       End if;

       if @Supplier_Gid is not null and @Supplier_Gid <> 0 THEN
         set Query_Search = concat(' and d.supplier_gid = ',@Supplier_Gid,' ');
       End if;

       if @Raiser_Gid is not null and @Raiser_Gid <> 0 THEN
         set Query_Search = concat(' and a.prheader_employee_gid = ',@Raiser_Gid,' ');
       End if;

       if @Pr_Status is not null and @Pr_Status <> '' THEN
         set Query_Search = concat(' and a.prheader_status = ''',@Pr_Status,''' ');
       End if;

       if @Pr_Amount is not null and @Pr_Amount <> 0 THEN
         set Query_Search = concat('  and a.prheader_totalamount = ''',@Pr_Amount,''' ');
       End if;

      if @Commodity_Gid is not null and @Commodity_Gid <> 0 THEN
        set Query_Search = concat(' h.commodity_gid = ''',@Commodity_Gid,''' ');
      End if;

     if @Product_Gid is not null and @Product_Gid <> 0 THEN
       set Query_Search = concat('  and c.product_gid = ''',@Product_Gid,''' ');
     End if;

     if @MEP_No is not null and @MEP_No <> '' THEN
        set Query_Search = concat('  and a.prheader_mepno like ''%',@MEP_No,'%'' ');
     End if;

     if @Pr_From_Date is not null and  @Pr_From_Date <> '' THEN
       set Query_Search = concat(' and a.prheader_date >= ''',@Pr_From_Date,''' ');
     End if;

     if @Pr_To_Date is not null and @Pr_To_Date <> '' THEN
       set Query_Search = concat(' and a.prheader_date <= ''',@Pr_To_Date,''' ');
     End if;

     if @Branch_Gid is not null and @Branch_Gid <> 0 THEN
       set Query_Search = concat(' and i.branch_gid = ',@Branch_Gid,' ');
     End if;


      set Query_Column = concat('Select a.prheader_gid,d.supplier_name,d.supplier_branchname,i.branch_name,c.product_displayname,
                                 b.prdetails_qty,a.prheader_no,a.prheader_status,
							   	e.prpoqty_qty,f.employee_name,h.commodity_name,a.prheader_totalamount,date_format(a.prheader_date,''%Y-%b-%d'') as poheader_date
                                 ');

      set Query_Join = '';
      set Query_Join = concat('from gal_trn_tprheader as a
                  inner join gal_trn_tprdetails as b on b.prdetails_prheader_gid = a.prheader_gid
                  inner join gal_mst_tproduct as c on c.product_gid = b.prdetails_product_gid
   				  inner join gal_mst_tsupplier as d on d.supplier_gid = b.prdetails_supplierproductgid
				  left join gal_trn_tprpoqty as e on e.prpoqty_prdetails_gid = b.prdetails_gid
				  inner join gal_mst_temployee as f on f.employee_gid = a.prheader_employee_gid
				  inner join gal_map_tcommodityprod as g on g.commodityprod_productgid = b.prdetails_product_gid
				  inner join ap_mst_tcommodity as h on h.commodity_gid = g.commodityprod_commoditygid
				  inner join gal_mst_tbranch as i on i.branch_gid = a.prheader_branchgid');

	 set Query_Where = '';
	 set Query_Where = concat(' where a.prheader_isactive = ''Y'' and a.prheader_isremoved = ''N''
		and c.product_isactive = ''Y'' and c.product_isremoved = ''N'' and d.supplier_isactive = ''Y'' and d.supplier_isremoved = ''N''
		and e.prpoqty_isactive = ''Y'' and e.prpoqty_isremoved = ''N'' and f.employee_isactive = ''Y'' and f.employee_isremoved = ''N''
		and h.commodity_isactive = ''Y'' and h.commodity_isremoved = ''N'' and g.commodityprod_isactive = ''Y'' and g.commodityprod_isremoved = ''N''
		and i.branch_isactive = ''Y'' and i.branch_isremoved = ''N'' and a.entity_gid in  (',@Entity_Gids,') ' );

		   set  Query_Select = concat(Query_Column,Query_Join,Query_Where,Query_Search);

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

ELSEIF ls_Type = 'PO' and ls_Sub_Type = 'QUERY_SUMMARY' THEN

       set Query_Column = '';
       set Query_Search = '';
       set Query_Join = '';
       set Query_Where = '';
       set Query_Group = '';

       select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, '$.Supplier_Group_Gid')) into @Supplier_Group_Gid;
       select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, '$.Supplier_Gid')) into @Supplier_Gid;
       select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, '$.Raiser_Gid')) into @Raiser_Gid;
       select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, '$.Status')) into @PO_Status;
       select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, '$.Amount')) into @PO_Amount;
       select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, '$.Commodity_Gid')) into @Commodity_Gid;
       select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, '$.Product_Gid')) into @Product_Gid;
       select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, '$.MEP_No')) into @MEP_No;
       select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, '$.From_Date')) into @PO_From_Date;
       select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, '$.To_Date')) into @PO_To_Date;
       select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, '$.Branch_Gid')) into @Branch_Gid;

       if @Supplier_Group_Gid is not null and @Supplier_Group_Gid <> 0 THEN
          set Query_Search = concat('  and c.supplier_groupgid = ',@Supplier_Group_Gid,' ');
       End if;

       if @Supplier_Gid is not null and @Supplier_Gid <> 0 THEN
         set Query_Search = concat('  and c.supplier_gid = ',@Supplier_Gid,' ');
       End if;

       if @Raiser_Gid is not null or @Raiser_Gid <> 0 THEN
         set Query_Search = concat(' and a.create_by = ',@Raiser_Gid, ' ');
       End if;

       if @PO_Status is not null and @PO_Status <> '' THEN
         set Query_Search = concat('  and a.poheader_status = ''',@PO_Status,''' ');
       End if;

       if @Commodity_Gid is not null and @Commodity_Gid <> 0 THEN
         set Query_Search = concat('  and e.commodity_gid = ',@Commodity_Gid,' ');
       End if;

       if @Product_Gid is not null and @Product_Gid <> 0 THEN
         set Query_Search = concat('  and g.product_gid = ',@Product_Gid,' ');
       End if;

       if @MEP_No is not null and @MEP_No <> '' THEN
         set Query_Search = concat('  and a.poheader_mepno = ''',@MEP_No,''' ');
       End if;

       if @PO_From_Date is not null and @PO_From_Date <> '' THEN
         set Query_Search = concat(' and a.poheader_date >= ''',@PO_From_Date,''' ');
       End if;

       if @PO_To_Date is not null and @PO_To_Date <> '' THEN
         set Query_Search = concat(' and a.poheader_date <= ''',@PO_To_Date,''' ');
       End if;

       if @Branch_Gid is not null and @Branch_Gid <> 0 THEN
         set Query_Search = concat(' and f.branch_gid = ',@Branch_Gid,' ');
       End if;

      set Query_Column = concat('  Select a.poheader_gid,a.poheader_no,
				date_format(a.poheader_date,''%Y-%b-%d'') as poheader_date,
				c.supplier_name,c.supplier_branchname,
				g.product_displayname,b.podetails_qty,e.commodity_name,f.branch_name,d.employee_name as raiser_name,
				ifnull(sum(h.podelivery_qty),0) as delivered_qty,a.poheader_status,a.poheader_close,a.poheader_closeremarks ');

	  set Query_Join = concat(' from gal_trn_tpoheader as a
				inner join gal_trn_tpodetails as b on b.podetails_poheader_gid = a.poheader_gid
				inner join gal_mst_tsupplier as c on c.supplier_gid = a.poheader_supplier_gid
				inner join gal_mst_temployee as d on d.employee_gid = a.create_by
				inner join ap_mst_tcommodity as e on e.commodity_gid = a.poheader_commodity_gid
				inner join gal_mst_tbranch as f on f.branch_gid = a.poheader_branchgid
				inner join gal_mst_tproduct as g on g.product_gid = b.podetails_product_gid
				left join gal_trn_tpodelivery as h on h.podelivery_poheader_gid = a.poheader_gid
				 and h.podelivery_podetails_gid = b.podetails_gid ');

    	set Query_Where = concat('  where a.poheader_isactive = ''Y'' and a.poheader_isremoved = ''N''
				and b.podetails_isremoved = ''N''
				and c.supplier_isactive = ''Y'' and c.supplier_isremoved = ''N''
				and d.employee_isactive = ''Y'' and d.employee_isremoved = ''N''
				and e.commodity_isactive = ''Y'' and e.commodity_isremoved = ''N''
				and f.branch_isactive = ''Y'' and f.branch_isremoved = ''N''
				and g.product_isactive = ''Y'' and g.product_isremoved = ''N''
 				');

     set Query_Group = '';
     set Query_Group = ' Group by a.poheader_gid,a.poheader_no,a.poheader_date,c.supplier_name,c.supplier_branchname,
				g.product_displayname,b.podetails_qty,e.commodity_name,f.branch_name,d.employee_name  ';

				     set  Query_Select = concat(Query_Column,Query_Join,Query_Where,Query_Search,Query_Group);

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


End if;

END