CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Suppliercapacity_Get`(IN `Action` varchar(32),IN `Type` varchar(32),IN `ljsuppcap` json,IN `Message` varchar(1000))
BEGIN
#Vigneshwari       15-05-2018

declare suppcap_srch text;
declare Query_srch1 varchar(1000);
declare ls_error varchar(100);
    
set ls_error = '';
set Query_srch1 = '';


if Action = 'suppliercapacity' then
	
	select JSON_EXTRACT(ljsuppcap, CONCAT('$.product_gid')) into @prod_gid;
        
	if @prod_gid <> 0 then
		set Query_srch1 = concat(Query_srch1,' and supplierproduct_product_gid in( ',@prod_gid,')');
	end if;
        
	set suppcap_srch = concat('SELECT distinct supplierproduct_gid,supplier_gid,Supplier_code,supplierproduct_dts,concat(supplier_name,'' - '',supplier_branchname) as supplier_name,ifnull(supplier_capacity,0) as sup_capacity,ifnull(supplierproduct_capacitypw,0) as prod_capacity,ifnull((supplierproduct_unitprice + supplierproduct_packingprice),0) as unitprice,
							ifnull(sum(qty-grnqty),0) as total,ifnull(creditlimit_days,0) as creditlimit_days,ifnull(supplierproduct_deliverydays,0) as delivery_days,supplierproduct_product_gid as product_gid,address_state_gid
							FROM gal_mst_tsupplier 
							left join gal_map_tsupplierproduct on supplier_gid = supplierproduct_supplier_gid and supplierproduct_isremoved = ''N'' and supplierproduct_isactive = ''Y''
							left join gal_mst_taddress  on address_gid = supplier_add_gid
                            left join (select distinct podetails_gid,poheader_supplier_gid,podetails_product_gid,sum(ifnull(podetails_qty,0)) as qty
							from gal_trn_tpoheader inner join gal_trn_tpodetails on poheader_gid = podetails_poheader_gid
							where poheader_isremoved = ''N'' and podetails_isremoved = ''N''
							group by poheader_supplier_gid) as po on podetails_product_gid = supplierproduct_product_gid 
							and poheader_supplier_gid = supplierproduct_supplier_gid
							left join (select grninwarddetails_podetails_gid,sum(ifnull(grninwarddetails_qty,0)) as grnqty 
                            from gal_trn_tgrninwarddetails where grninwarddetails_isremoved = ''N''
                            group by grninwarddetails_podetails_gid) as grn on grninwarddetails_podetails_gid = podetails_gid
                            left join (select creditlimit_reftable_gid,creditlimit_days from gal_trn_tcreditlimit 
							inner join gal_mst_tref on creditlimit_ref_gid = ref_gid and ref_name = ''sup_CREDITLIMIT'') as credit 
                            on creditlimit_reftable_gid = supplier_gid
							where supplier_isremoved = ''N'' and supplier_isactive = ''Y'' ',Query_srch1,'
							group by supplierproduct_supplier_gid,supplierproduct_product_gid
							');
                                

	set @p = suppcap_srch;
    #select @p;
	PREPARE stmt FROM @p;
	EXECUTE stmt; 
	DEALLOCATE PREPARE stmt;

end if;
END