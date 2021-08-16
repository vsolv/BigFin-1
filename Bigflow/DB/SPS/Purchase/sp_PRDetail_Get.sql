CREATE DEFINER=`developer`@`%` PROCEDURE `sp_PRDetail_Get`(
IN `li_action` varchar(128),
IN `li_prheader_gid` int,
IN `ls_prod_name` varchar(128),
IN `li_emp_gid` int,
IN `li_entity_gid` int,
OUT `Message` varchar(128))
BEGIN

#Vigneshwari       18-11-2017

declare Query_search varchar(1000);
declare PR_Headersrch Text;
declare ls_error varchar(128);
declare li_count int;

set ls_error = '';

if li_prheader_gid <> 0 then
	set Query_search = concat(' and prheader_gid = ' , li_prheader_gid);
else
	set ls_error = '';
end if;

if ls_prod_name <> '' then
	set Query_search = concat(Query_search , ' and product_name like ''%' , ls_prod_name , '%''');
else
	set Query_search = concat(Query_search , '');
end if;


/*set @REF_Gid11=0;
select fn_REFGid('PR') into @REF_Gid11;*/

/*if li_emp_gid <> '' then
	set Query_search = concat(Query_search , ' and prheader_employee_gid =' , li_emp_gid);
else
	set Query_search = concat(Query_search , '');
end if;*/
#select 1;
if li_action='Details' then
set @count1=2;
#select  count(delmat_gid) from gal_trn_tprheader as a
#				inner join ap_mst_tcommodity as b on b.commodity_gid=a.prheader_commodity_gid
 #               inner join gal_mst_tdelmat as c on c.delmat_commoditygid=b.commodity_gid
  #              where prheader_gid=li_prheader_gid and delmat_employeegid=li_emp_gid 
   #             and delmat_tran=133
    #            into @count1;
#select @count1;            
if @count1 > 0 then
         
					if ls_error = '' then

						set PR_Headersrch = ' 	select distinct employee_code,
									supplierproduct_dts,employee_gid,concat(supplier_name,''-'',supplier_branchname) as supplier_name,
                                  supplierproduct_unitprice as supplierproduct_unitprice,prheader_totalamount,prheader_commodity_gid,commodity_name,prheader_gid ,
                                    prdetails_gid, prdetails_qty , product_name ,producttype_name , employee_name,prheader_remarks,
											prheader_date,productcategory_name ,prdetails_supplierproductgid,uom_name,
                                            prheader_no ,product_gid ,producttype_gid ,productcategory_gid,prheader_status,prdetails_imagepath
											from gal_trn_tprheader
											inner join gal_trn_tprdetails on prheader_gid = prdetails_prheader_gid
											inner join ap_mst_tcommodity on commodity_gid=prheader_commodity_gid
											left join gal_mst_tproduct on prdetails_product_gid = product_gid and product_isremoved = ''N''
											left join gal_mst_tproducttype on product_producttype_gid = producttype_gid and producttype_isremoved = ''N''
											left join gal_mst_tproductcategory on producttype_productcategory_gid = productcategory_gid and productcategory_isremoved = ''N''
											left join gal_mst_tuom on product_uom_gid = uom_gid and uom_isremoved = ''N''
											inner join gal_map_tsupplierproduct on 
													supplierproduct_gid = prdetails_supplierproductgid and 
													 prdetails_product_gid= supplierproduct_product_gid and supplierproduct_isremoved = ''N'' 
													 and  supplierproduct_isactive=''Y'' and  prdetails_isremoved=''N''
													inner join gal_mst_tsupplier as f on supplier_gid = supplierproduct_supplier_gid
	                                                 and
                                                      f.supplier_isactive=''Y'' and  f.supplier_isremoved=''N''
											left join gal_mst_temployee on employee_gid = prheader_employee_gid and employee_isremoved = ''N''
											where prheader_isremoved = ''N'' and prheader_isactive = ''Y'' and prdetails_isremoved = ''N''';
						#select PR_Headersrch;
						set @stmt = concat(PR_Headersrch , Query_search);
						#select @stmt;
						PREPARE stmt FROM @stmt;
						EXECUTE stmt;
						DEALLOCATE PREPARE stmt;
						set Message = 'done';
					else
						set Message = ls_error ;
					end if;
end if;



elseif li_action='Draft' then

		#select 1;
		set PR_Headersrch ='';
		set PR_Headersrch = concat('
						select branch_gid,branch_name,supplier_gid,concat(supplier_name,''-'',supplier_branchname) as supplier_name,prheader_gid,
                        prheader_no,
                        prheader_date,
                        prdetails_gid,
                        prdetails_product_gid,
                        prdetails_supplierproductgid,
                        supplierproduct_gid,
                        product_gid,
                        product_name,
                        product_code,
                        product_displayname,
                        prdetails_qty,
                        commodity_name,
                        commodity_gid,
                        uom_name,
                        supplierproduct_unitprice 
                        from gal_trn_tprheader as a
						inner join gal_trn_tprdetails as b on b.prdetails_prheader_gid=a.prheader_gid
						and b.prdetails_isremoved=''N''
						inner join gal_mst_tproduct as d on d.product_gid=b.prdetails_product_gid
						and d.product_isactive=''Y'' and d.product_isremoved=''N''
                        inner join ap_mst_tcommodity as c1 on commodity_gid=a.prheader_commodity_gid
						
                       #left join gal_mst_tproduct on prdetails_product_gid = product_gid and product_isremoved = ''N''
						left join gal_mst_tproducttype as d1 on d.product_producttype_gid = d1.producttype_gid 
                        and d1.producttype_isremoved = ''N''
						left join gal_mst_tproductcategory as d2 on d1.producttype_productcategory_gid = d2.productcategory_gid 
                        and d2.productcategory_isremoved = ''N''
                       
						left join gal_mst_tuom as d3 on d.product_uom_gid = d3.uom_gid 
                        and d3.uom_isremoved = ''N''
						inner join gal_map_tsupplierproduct as c on c.supplierproduct_supplier_gid=b.prdetails_supplierproductgid
						and c.supplierproduct_product_gid=b.prdetails_product_gid
						and c.supplierproduct_isactive=''Y''
                        
                        inner join gal_mst_tsupplier as h on b.prdetails_supplierproductgid=h.supplier_gid 
                        and supplier_isactive=''Y'' and supplier_isremoved=''N''
                        inner join gal_mst_tbranch as br on br.branch_gid=a.prheader_branchgid  and 
						branch_isremoved=''N'' and branch_isactive=''Y''
                         
                        
						where a.prheader_gid=',li_prheader_gid,'
                        and a.prheader_status=''Draft''
						and a.prheader_isactive=''Y''
						and a.prheader_isremoved=''N''
						and a.entity_gid=',li_entity_gid,';
										');
									#select PR_Headersrch;
									set @p = PR_Headersrch;
									#select @p;
									PREPARE stmt FROM @p;
									EXECUTE stmt; 
									DEALLOCATE PREPARE stmt;
									select found_rows() into li_count;
                                    
									if li_count>0 then
										set Message='FOUND';
									 else
										set Message='NOT FOUND';
									 end if;  
         
					
					
end if;

END