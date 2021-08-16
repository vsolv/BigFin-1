CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Finalapproval_Get`(in li_action varchar(200),
out message varchar(200))
sp_Finalapproval_Get:BEGIN

declare query_select text;
declare query_sel text;
declare li_count int;

SET SESSION group_concat_max_len=4294967295;
if li_action='select' then

#set query_select='';
set query_select=concat('select distinct product_gid,product_name,hsn_gid,hsn_cgstrate,hsn_sgstrate,hsn_igstrate,
						 prheader_gid,prheader_no,prheader_employee_gid,
						 prheader_status,prheader_commodity_gid,commodity_gid,
						 commodity_name,prdetails_gid,prdetails_qty,
                         supplier_gid,supplierproduct_unitprice,
                         prheader_totalamount,
						 prheader_mepno,prheader_branchgid,
                         concat(supplier_name,''-'',supplier_branchname) as supplier_name,
                         branch_gid,
                         branch_name,prdetails_product_gid,
                         supplierproduct_dts,
                         branch_code,
                         branch_inchargegid,
                         branch_addressgid,
                         branch_contactgid,
                         address_1,
                         address_2,
                         address_3,
                         address_pincode,
                         state_code,
                         state_name,
                         district_code,
                         district_name,
                         City_code,
                         City_Name,
                         ifnull((select
                         concat(''['',group_concat( JSON_OBJECT(
																						''prccbs_gid'',prccbs_gid,
                                                                                        ''prccbs_remaining_qty_Value'',ifnull(prccbs_qty,0)-ifnull((select ifnull(sum(prpoqty_qty),0) from gal_trn_tprpoqty where prpoqty_prccbs_gid = prccbs_gid and prpoqty_prdetails_gid=prccbs_prdetailsgid),0) ,
																						''prccbs_prdetailsgid'',prccbs_prdetailsgid,
																						 ''prccbs_bs'',prccbs_bs,
                                                                                         ''prccbs_cc'',prccbs_cc,
                                                                                         ''prccbs_refgid'',prccbs_refgid,
                                                                                         ''product_name'',product_name,
                                                                                         ''product_gid'',product_gid,
                                                                                         ''temp_ref'',(select ref_name from gal_mst_tref where ref_gid =prccbs_refgid)   ,

                                                ''temp_reftable'', case
                                                when (select ref_name from gal_mst_tref where ref_gid =prccbs_refgid)  =''PO_BRANCH'' then
                                                (select
                                                concat(''['',group_concat( JSON_OBJECT(
																															''branch_gid'',a1.branch_gid,
                                                                                                                            ''branch_name'',a1.branch_name,
																															''branch_code'',a1.branch_code,
																														    ''employee_name'',f1.employee_name,
 																															''address_1'',b1.address_1,
                                                                                                                            ''address_2'',b1.address_2,
                                                                                                                            ''address_3'',b1.address_3,
                                                                                                                            ''district_name'',c1.district_name,
                                                                                                                            ''state_name'',d1.state_name,
                                                                                                                            ''address_pincode'',b1.address_pincode,
                                                                                                                            ''country_name'',e1.country_name
																														)),'']'')
												from gal_mst_tbranch as a1
											    inner join gal_mst_taddress as b1 on b1.address_gid = a1.branch_addressgid
                                                inner join gal_mst_tdistrict as c1 on c1.district_gid =b1.address_district_gid
												inner join gal_mst_tstate as d1 on d1.state_gid = c1.district_state_gid
												inner join gal_mst_tcountry as e1 on e1.country_gid =d1.state_country_gid
												inner join gal_mst_temployee as f1 on f1.employee_gid = a1.branch_inchargegid
                                                and a1.branch_isactive=''Y'' and a1.branch_isremoved=''N'' and a1.entity_gid=1
                                                and b1.entity_gid=1
                                                and c1.district_isremoved=''N'' and c1.entity_gid=1
                                                and d1.state_isremoved=''N'' and d1.entity_gid=1
                                                and e1.country_isremoved=''N'' and e1.entity_gid=1
												and f1.employee_isactive=''Y'' and f1.employee_isremoved=''N'' and f1.entity_gid=1
												where a1.branch_gid = prccbs_reftablegid )

                                                when (select ref_name from gal_mst_tref where ref_gid =prccbs_refgid) =''PO_GODOWN'' then

                                                (select concat(''['',group_concat( JSON_OBJECT(
																															''godown_gid'',a2.godown_gid,
                                                                                                                            ''godown_name'',a2.godown_name,
																														    ''godown_code'',a2.godown_code,
																														    ''employee_name'',f2.employee_name,
                                                                                                                            ''address_1'',b2.address_1,
                                                                                                                            ''address_2'',b2.address_2,
                                                                                                                            ''address_3'',b2.address_3,
                                                                                                                            ''district_name'',c2.district_name,
																														    ''state_name'',d2.state_name,
                                                                                                                            ''address_pincode'',b2.address_pincode,
																															''country_name'',e2.country_name
 																															)),'']'')
												from gal_mst_tgodown as a2
											    inner join gal_mst_taddress as b2 on b2.address_gid = a2.godown_address_gid
												inner join gal_mst_tdistrict as c2 on c2.district_gid =b2.address_district_gid
                                                inner join gal_mst_tstate as d2 on d2.state_gid = c2.district_state_gid
												inner join gal_mst_tcountry as e2 on e2.country_gid =d2.state_country_gid
											    inner join gal_mst_temployee as f2 on f2.employee_gid = a2.godown_inchage_gid
											    and a2.godown_isactive=''Y'' and a2.godown_isremoved=''N'' and a2.entity_gid=1
                                                and b2.entity_gid=1
                                                and c2.district_isremoved=''N'' and c2.entity_gid=1
                                                and d2.state_isremoved=''N''  and d2.entity_gid=1
                                                and e2.country_isremoved=''N'' and e2.entity_gid=1
                                                and f2.employee_isactive=''Y'' and f2.employee_isremoved=''N'' and f2.entity_gid=1
											    where a2.godown_gid =  prccbs_reftablegid )
                                                end ,
                                                ''prccbs_reftablegid'',prccbs_reftablegid,
                                                ''prccbs_code'',prccbs_code,
                                                ''prccbs_qty'',prccbs_qty)),'']'')

                                                from gal_trn_tprheader as a
                                                inner join gal_trn_tprdetails as  b on b.prdetails_prheader_gid=a.prheader_gid
                                                inner join gal_trn_tprccbs as c on c.prccbs_prdetailsgid = b.prdetails_gid
                                                inner join gal_mst_tproduct as d on d.product_gid=b.prdetails_product_gid
                                                and d.product_isactive=''Y'' and d.product_isremoved=''N''
                                                and a.prheader_isactive=''Y'' and  a.prheader_isremoved=''N'' and a.entity_gid=1
                                                and b.prdetails_isremoved=''N''  and b.entity_gid=1
                                                and c.prccbs_isactive=''Y'' and c.prccbs_isremoved=''N'' and c.entity_gid=1
                                                where prheader_gid=b.prheader_gid and prdetails_product_gid=a.prdetails_product_gid ),''[{}]'') as ccbs_details,



                        ifnull(prdetails_qty - ifnull((select sum(pr.prpoqty_qty)
                          from gal_trn_tprpoqty pr where pr.prpoqty_prdetails_gid = a.prdetails_gid ) ,0),0) as remaining_qty,
                       prdetails_qty as initial_qty,uom_name
						 from gal_trn_tprdetails as a

            inner join gal_trn_tprheader as b on a.prdetails_prheader_gid=b.prheader_gid and b.entity_gid=1  and prheader_status=''Approved'' and prheader_isremoved=''N'' and prheader_isactive=''Y''
            inner join gal_mst_tproduct as c on a.prdetails_product_gid=c.product_gid and c.entity_gid=1 and product_isremoved=''N''
            inner join gal_mst_tuom as i on c.product_uom_gid = i.uom_gid and uom_isactive=''Y'' and uom_isremoved=''N'' and i.entity_gid=1
			inner join ap_mst_tcommodity as d on b.prheader_commodity_gid=d.commodity_gid
            and d.entity_gid=1 and commodity_isremoved=''N'' and commodity_isactive=''Y''
           inner join gal_map_tsupplierproduct on
			supplierproduct_gid = prdetails_supplierproductgid and
			 prdetails_product_gid= supplierproduct_product_gid and supplierproduct_isremoved = ''N''
			 and  supplierproduct_isactive=''Y'' and  prdetails_isremoved=''N''
             inner join gal_mst_tbranch as f on f.branch_gid=b.prheader_branchgid and f.entity_gid=1 and
            branch_isremoved=''N'' and branch_isactive=''Y''
            inner join gal_mst_taddress as ff on ff.address_gid=f.branch_addressgid
            and ff.entity_gid=1
            inner join gal_mst_tstate as gg on gg.state_gid=ff.address_state_gid
            and gg.state_isremoved=''N''
            inner join gal_mst_tdistrict as ii on ii.district_gid=ff.address_district_gid
            and ii.district_isremoved=''N''
            inner join  gal_mst_tcity as hh on hh.city_gid=ff.address_city_gid
            and hh.city_isremoved=''N''
            left join gal_trn_tprpoqty as g on g.prpoqty_prdetails_gid=a.prdetails_gid and g.entity_gid=1 and prpoqty_isactive=''Y'' and prpoqty_isremoved=''N''
inner join gal_mst_tsupplier as sup on supplier_gid = supplierproduct_supplier_gid
	                                                 and
                                                      sup.supplier_isactive=''Y'' and  sup.supplier_isremoved=''N''
                                                      inner join gal_mst_thsn as k on k.hsn_gid = c.product_hsn_gid and k.entity_gid=1 and hsn_isactive=''Y'' and hsn_isremoved=''N''
            left join gal_trn_tpodetails as l on l.podetails_gid=g.prpoqty_podetails_gid and l.entity_gid=1 and podetails_isremoved=''N''
			left join gal_trn_tpoheader as m on m.poheader_gid=l.podetails_poheader_gid and m.entity_gid=1  and  poheader_isactive=''Y'' and poheader_isremoved=''N''
            and prdetails_isremoved=''N''
                          having remaining_qty >0

            ');

	#select query_select;
	set @stmt= query_select;
	PREPARE stmt FROM @stmt;
	EXECUTE stmt;
	DEALLOCATE PREPARE stmt;
	Select found_rows() into li_count;

		if li_count > 0 then
			set Message = 'FOUND';
		else
			set Message = 'NOT_FOUND';
            leave sp_Finalapproval_Get;
		end if;

end if;


END