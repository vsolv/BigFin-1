CREATE DEFINER=`root`@`%` PROCEDURE `sp_Prodtype_Get_Backup_OLd One `(IN `prodtype_gid` int,IN `li_Supp_gid` int)
BEGIN
#Vigneshwari       14-11-2017
declare Query_search varchar(1000);
declare query1 varchar(1000);
set Query_search = '';
if prodtype_gid <> 0 then
set Query_search = concat(Query_search , ' and product_producttype_gid = ' , prodtype_gid);
else
set Query_search = '';
end if;
if li_Supp_gid <> 0 then
set Query_search = concat(Query_search , ' and supplierproduct_supplier_gid = ' , li_Supp_gid);
else
set Query_search = concat(Query_search,'');
end if;
set query1 = 'select product_gid , supplierproduct_dts,product_code,product_name , uom_name , supplierproduct_supplier_gid , supplierproduct_unitprice,
			case when avg(supplierproduct_unitprice) is null then 0
            else  round(avg(supplierproduct_unitprice),2) end as prod_price,product_displayname
					FROM gal_mst_tproduct
					left join gal_map_tsupplierproduct on product_gid = supplierproduct_product_gid
                    and supplierproduct_isremoved = ''N'' and supplierproduct_isactive = ''Y''
                    left join gal_mst_tuom on product_uom_gid = uom_gid and uom_isremoved = ''N'' and uom_isactive = ''Y''
			where product_isremoved = ''N'' and product_isactive = ''Y''';
set @p = concat(query1 , Query_search ,' group by product_gid ');
#select @p;
PREPARE stmt FROM @p;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
END

