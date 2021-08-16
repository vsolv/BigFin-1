CREATE DEFINER=`developer`@`%` PROCEDURE `sp_PODetail_Get`(IN `li_podetail_gid` int,IN `ls_prod_name` varchar(128),IN `li_emp_gid` int,
OUT `Message` varchar(128))
BEGIN

#Vigneshwari       18-11-2017

declare Query_search varchar(1000);
declare PO_Detailssrch text;
declare ls_error varchar(64);

set ls_error = '';

if li_podetail_gid <> 0 then
	set Query_search = concat(' and podetails_poheader_gid = ' , li_podetail_gid);
else
	set ls_error = 'PO Detail Not Given.';
end if;

if ls_prod_name <> '' then
	set Query_search = concat(Query_search , ' and product_name like ''%' , ls_prod_name , '%''');
else
	set Query_search = concat(Query_search , '');
end if;

if li_emp_gid <> 0 then
	set Query_search = concat(Query_search , ' and a.create_by = ' , li_emp_gid);
else
	set Query_search = concat(Query_search , '');
end if;

if ls_error = '' then

	set PO_Detailssrch = 'select poheader_gid,a.create_by as raised_by,poheader_commodity_gid,commodity_name,podetails_gid,podetails_imagepath ,product_gid , producttype_gid , productcategory_gid , 
		poterms_gid,poheader_supplier_gid ,poheader_no ,productcategory_name ,producttype_name ,product_name ,uom_name ,
        podetails_qty , podetails_uom , podetails_unitprice ,podetails_amount ,podetails_taxamount ,podetails_totalamount ,	
        poterms_name,poheader_remarks ,poheader_status,concat(supplier_name,''-'',supplier_branchname) as supplier_name,poheader_date ,poheader_validfrom,poheader_validto,poheader_approvallater,branch_name,branch_gid,branch_code,a.create_by
		from gal_trn_tpoheader as a
		inner join gal_trn_tpodetails on a.poheader_gid = podetails_poheader_gid
        inner join ap_mst_tcommodity on commodity_gid= a.poheader_commodity_gid
        inner join gal_mst_tbranch  on branch_gid=a.poheader_branchgid
		and  branch_isactive=''Y'' and  branch_isremoved =''N''
		left join gal_mst_tproduct on podetails_product_gid = product_gid and product_isremoved = ''N''
		left join gal_mst_tproducttype on product_producttype_gid = producttype_gid and producttype_isremoved = ''N''
		left join gal_mst_tproductcategory on producttype_productcategory_gid = productcategory_gid and product_isremoved = ''N''
		left join gal_mst_tuom on product_uom_gid = uom_gid and uom_isremoved = ''N''
        left join gal_mst_tpoterms on poheader_poterms_gid = poterms_gid and poterms_isremoved = ''N''
        left join gal_mst_tsupplier on supplier_gid = poheader_supplier_gid and supplier_isremoved = ''N''
		where a.poheader_isremoved = ''N'' and a.poheader_isactive = ''Y'' and podetails_isremoved = ''N'' ';

	set @stmt = concat(PO_Detailssrch , Query_search);
    #select @stmt;
	PREPARE stmt FROM @stmt;
	EXECUTE stmt;
	DEALLOCATE PREPARE stmt;
	set Message = 'done';
else
	set Message = ls_error ;
end if;
END