CREATE DEFINER=`developer`@`%` PROCEDURE `sp_GRNdetails_Get`(IN `ls_Type` varchar(64),IN `ls_Sub_Type` varchar(64),
IN `lj_Filters` json,IN `lj_Classification` json, OUT `Message` varchar(1024)
)
sp_GRNdetail_Get:BEGIN
### Selva sep 19 2019
## Type EXPENSE   
### SUb Type  =  COLUMN
##
Declare Query_Select varchar(6144);
Declare Query_Search varchar(1024);
Declare i int;
declare errno int;
declare msg varchar(1000);
declare li_count int;
declare Entity_Gid int;
# Null Selected Output
DECLARE done INT DEFAULT 0;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
#...

	DECLARE EXIT HANDLER FOR SQLEXCEPTION,sqlwarning
    BEGIN
    
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
    set Message = concat(errno , msg);
    ROLLBACK;
    END;
#SET session group_concat_max_len=50000000;
SET SESSION group_concat_max_len=4294967295;
if ls_Type = 'GRN' and ls_Sub_Type = 'SEARCH' then
		select JSON_LENGTH(lj_Filters,'$') into @li_json_INVProcess_count;
        
           if @li_json_INVProcess_count is null or @li_json_INVProcess_count = 0 then
			set Message = 'No Data In Json - Filter.';
            rollback;
			leave sp_GRNdetail_Get;
        end if;
        
        Select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.prno'))) into @prno ;  
        Select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.pono'))) into @pono ;  
        Select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.suppliergid'))) into @suppliergid ;  
        Select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.pogid'))) into @pogid ;  

       # if @ExpenseType = 0 then
		##		set Message = ' Header Gid Is Needed.';
       #         leave sp_SOInvoiceProcess_Get;
       # End if;
        
        
        
        set Query_Search = '';
        if @suppliergid is not null then
				set Query_Search = concat(Query_Search,' and supplier_gid = ',@suppliergid,' ');
        End if;
        if @prno is not null then
				set Query_Search = concat(Query_Search,' and prheader_no = ''',@prno,''' ');
        End if;
        
        if @pono is not null then
				set Query_Search = concat(Query_Search,' and poheader_no = ''',@pono,''' ');
        End if;
        
        set Query_Select = '';
        
        set Query_Select = concat( 'select podelivery_gid,main.poheader_gid ,podelivery_refgid,prheader_no,podelivery_reftablegid,ref_name,location,delivery_location, main.podetails_gid , 
                             main.podetails_product_gid ,main.podelivery_godown_gid ,main.uom_name,
						main.supplier_gid ,main.grninwarddetails_gid, main.podetails_uom,concat(main.supplier_name,'' - '',main.supplier_branchname) as supplier_name,main.poheader_no,main.poheader_date,
                        main.product_name,main.product_code ,main.total_qty ,main.allreceive_qty,main. rem_qty
                        from ( select podelivery_gid,prheader_no,podelivery_refgid,podelivery_reftablegid,poheader_gid ,ref_name, podetails_gid, podetails_product_gid ,
                                  podelivery_godown_gid ,supplier_gid ,uom_name, 
							grninwarddetails_gid,podetails_uom,supplier_name,supplier_branchname,poheader_no,poheader_amount,product_name,product_code ,poheader_date, 
							case when isnull(podetails_qty) then 0 else podelivery_qty end as total_qty,
                            case when isnull(grninwarddetails_qty) then 0 else sum(grninwarddetails_qty) end as allreceive_qty,
							''0'' as current_qty,
                            case when isnull(podelivery_qty) then 0 else (podelivery_qty) end - case when isnull(grninwarddetails_qty) then 0 
							else sum(grninwarddetails_qty) end as rem_qty,
                            case when ref_name = ''PO_BRANCH'' then ''BRANCH'' else ''GODOWN'' end as location,
                            case when ref_name = ''PO_BRANCH'' then 
                                    (select branch_name from gal_mst_tbranch where branch_gid = del.podelivery_reftablegid)
                            else 
                                    (select godown_name from gal_mst_tgodown where godown_gid = del.podelivery_reftablegid)
							end as delivery_location
                            
							FROM gal_trn_tpoheader 
							inner join gal_trn_tpodetails on poheader_gid = podetails_poheader_gid
							left join gal_trn_tpodelivery as del on podetails_gid = podelivery_podetails_gid and podelivery_isremoved = ''N''
							left join gal_mst_tref as ref on ref.ref_gid = podelivery_refgid 
                            left join gal_trn_tprccbs as ccbs on ccbs.prccbs_gid = del.podelivery_ccbs and ccbs.prccbs_isremoved = ''N''
                            left join gal_trn_tprdetails as prde on prde.prdetails_gid = ccbs.prccbs_prdetailsgid and prde.prdetails_isremoved = ''N''
                            left join gal_trn_tprheader as prhe on prhe.prheader_gid = prde.prdetails_prheader_gid and prhe.prheader_isremoved = ''N''
                              left join (
								select grninwarddetails_podelivary_gid,grninwarddetails_refgid,grninwarddetails_reftablegid,grninwarddetails_gid,grninwarddetails_podetails_gid,grninwarddetails_poheader_gid,grninwarddetails_qty,grninwardheader_status 
								from gal_trn_tgrninwarddetails 
								inner join gal_trn_tgrninwardheader on grninwarddetails_grninwardheader_gid = grninwardheader_gid 
								where  grninwarddetails_isremoved = ''N'' and grninwardheader_status in (''Approved'',''Pending for Approval'')
							) as grn on podelivery_podetails_gid = grninwarddetails_podetails_gid and grninwarddetails_refgid = podelivery_refgid and 
                                                            podelivery_reftablegid = grninwarddetails_reftablegid
															and grninwarddetails_podelivary_gid = del.podelivery_gid
                        
                        left join gal_mst_tproduct on podetails_product_gid = product_gid and product_isremoved = ''N''
                        left join gal_mst_tsupplier on poheader_supplier_gid = supplier_gid and supplier_isremoved = ''N''
                        left join gal_mst_tuom on uom_gid = product_uom_gid and uom_isremoved = ''N'' and uom_isactive = ''Y''
                        where poheader_isremoved = ''N'' and poheader_isactive = ''Y'' and podetails_isremoved = ''N''
                        and poheader_status in (''Approved'',''REOPENED'')
                        and poheader_gid not in (select poclose_poheader_gid from gal_trn_tpoclose where poclose_isremoved = ''N''
                        and poclose_isactive = ''Y'')
                        and poheader_gid not in (select pocancel_poheader_gid from gal_trn_tpocancel where pocancel_isremoved = ''N''
                        and pocancel_isactive = ''Y'')
                         ', Query_search ,'
                          
                        group by podetails_product_gid,poheader_gid,podelivery_gid
						 having rem_qty > 0) as main  '	);
                            
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
if ls_Type = 'GRN' and ls_Sub_Type = 'DETAIL_VIEW' then
 		select JSON_LENGTH(lj_Filters,'$') into @li_json_INVProcess_count;
        
           if @li_json_INVProcess_count is null or @li_json_INVProcess_count = 0 then
			set Message = 'No Data In Json - Filter.';
            rollback;
			leave sp_GRNdetail_Get;
        end if;
        
        Select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.grnheader_id'))) into @grnheader_id ;  
  

       # if @ExpenseType = 0 then
		##		set Message = ' Header Gid Is Needed.';
       #         leave sp_SOInvoiceProcess_Get;
       # End if;
        
        
        
        set Query_Search = '';
        if @grnheader_id is not null then
				set Query_Search = concat(Query_Search,' and grninwardheader_gid = ',@grnheader_id,' ');
        End if;
        
        
        set Query_Select = '';
        
        set Query_Select = concat( ' select b.grninwardheader_code,b.grninwardheader_remarks,b.grninwardheader_dcnote,b.grninwardheader_date,b.grninwardheader_invoiceno,concat(f.supplier_name,''-'',f.supplier_branchname) as supplier_name,d.poheader_no,e.product_name,
                             grninwarddetails_refgid,grninwarddetails_reftablegid,grninwarddetails_gid,grninwarddetails_podetails_gid,
                              grninwarddetails_poheader_gid,grninwarddetails_qty,grninwardheader_gid,grninwardheader_status 
								,case when ref_name = ''PO_BRANCH'' then ''BRANCH'' else ''GODOWN'' end as location,
                            case when ref_name = ''PO_BRANCH'' then 
                                    (select branch_name from gal_mst_tbranch where branch_gid = a.grninwarddetails_reftablegid)
                            else 
                                    (select godown_name from gal_mst_tgodown where godown_gid = a.grninwarddetails_reftablegid)
							end as delivery_location
                            from gal_trn_tgrninwarddetails as a
								inner join gal_trn_tgrninwardheader as b on grninwarddetails_grninwardheader_gid = grninwardheader_gid 
								left join gal_mst_tref as ref on ref.ref_gid = grninwarddetails_refgid 
                                left join gal_trn_tpodetails as c on c.podetails_gid = a.grninwarddetails_podetails_gid 
                                left join gal_trn_tpoheader as d on d.poheader_gid = c.podetails_poheader_gid 
                                left join gal_mst_tproduct as e on e.product_gid = c.podetails_product_gid
                                left join gal_mst_tsupplier as f on f.supplier_gid = poheader_supplier_gid
								where  grninwarddetails_isremoved = ''N'' and poheader_isactive = ''Y'' and poheader_isremoved = ''N''   and 
                                grninwardheader_isactive = ''Y'' and grninwardheader_isremoved = ''N''  ', Query_search ,' '	);
                            
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
end if;	

END
