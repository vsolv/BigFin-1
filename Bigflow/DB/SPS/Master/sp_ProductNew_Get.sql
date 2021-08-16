CREATE DEFINER=`developer`@`%` PROCEDURE `sp_ProductNew_Get`(IN `Type` varchar(64),IN `Sub_Type` varchar(64),
IN `Product_json` json,IN `lj_Classification` json,OUT `Message` varchar(1024))
sp_ProductNew_GET:BEGIN
Declare Query_Select varchar(60000);
Declare li_count int;
Declare Query_srch text;

##karthiga edited for productcarton name (subquery) and isactive & isremove 07-dec-19

select fn_Classification('ENTITY_ONLY',lj_Classification) into @OutMsg_Classification ;
        select  JSON_UNQUOTE(JSON_EXTRACT(@OutMsg_Classification, '$.Entity_Gid[0]')) into @Entity_Gids;
        if @Entity_Gids is  null or @Entity_Gids = '' then
				select  JSON_UNQUOTE(JSON_EXTRACT(@OutMsg_Classification, '$.Message')) into @Message;
				set Message = concat('Error On Classification Data - ',@Message);
                leave sp_ProductNew_GET;
        End if;


if type = 'get' and Sub_Type='get_data' then

/*select JSON_LENGTH(Product_json,'$') into @li_product_count;

     if  @li_product_count <=0  then
				#set Message = 'No Data in Json Object';
				#leave sp_ProductNew_GET;
	 end if;*/
			   select  JSON_UNQUOTE(JSON_EXTRACT(Product_json, CONCAT('$.producttype_gid'))) into @producttype_gid;
               select  JSON_UNQUOTE(JSON_EXTRACT(Product_json, CONCAT('$.product_gid'))) into @product_gid;
              # select  JSON_UNQUOTE(JSON_EXTRACT(Product_json, CONCAT('$.productcategory_gid[0]'))) into @productcategory_gid;
               #select  JSON_UNQUOTE(JSON_EXTRACT(Product_json, CONCAT('$.prodcarton_gid[0]'))) into @prodcarton_gid;
                    set Query_srch='';

	if @producttype_gid <> 0 then

			set Query_srch = concat(Query_srch,' and product_producttype_gid = ',@producttype_gid);
	 else
			set Query_srch = concat(Query_srch,'');
    end if;

     if @product_gid <> 0 then
			set Query_srch = concat(Query_srch,' and product_gid = ',@product_gid)	;
	 else
			set Query_srch = concat(Query_srch,'');
	 end if;

     /* if @productcategory_gid <> 0 then
			set Query_srch = concat(Query_srch,' and productcategory_gid = ',@productcategory_gid)	;
	 else
			set Query_srch = concat(Query_srch,'');
	 end if;

      if @prodcarton_gid <> 0 then
			set Query_srch = concat(Query_srch,' and prodcarton_gid = ',@prodcarton_gid)	;
	 else
			set Query_srch = concat(Query_srch,'');
	 end if;
               */
					set Query_Select = '';
					set Query_Select = concat('select a.product_gid, a.product_code,
                    apc.category_name,aps.subcategory_name,
                    a.product_name,a.product_displayname,a.product_tradingitem,
                    a.product_hsn_gid,a.product_uom_gid,
                    a.product_category_gid,
                    a.product_subcategory_gid,
                    a.product_productcategory_gid,
                    a.product_producttype_gid,
                    a.product_unitprice,
                    #a.tally_product_name,prodcarton_productcartongid
                    a.product_weight,a.product_isactive,
                    a.product_isremoved,a.entity_gid,a.create_by,
                    a.create_date,a.insert_flag,a.update_flag,a.product_tallyname,
                    a.update_by,a.Update_date,b.producttype_name,b.producttype_gid,
                    b.producttype_productcategory_gid,
                    c. productcategory_gid,c.productcategory_clientgid,
                    #c.productcategory_code,
                    c.productcategory_name,
                    c.productcategory_stockimpact,
                    sub.carton_name ,
                    sub.prodcarton_productcartongid,
                    sub.prodcarton_gid,
                    sub.prodcarton_productgid,
                    sub.prodcarton_capacity,
                    sub.prodcarton_remarks,
					e.hsn_code,f.uom_name,f.uom_code,e.hsn_gid,f.uom_gid,
                    c.productcategory_isprodservice as prod_cat_value,
				case
					when c.productcategory_isprodservice = ''P'' then ''Product''
					when c.productcategory_isprodservice = ''S'' then ''Service''
                    when c.productcategory_isprodservice = ''B'' then ''Goods''
                    else ''Un-Known''
				end as ''prod_cat_data''


                    from gal_mst_tproduct as a
                    inner join gal_mst_tproducttype as b on b.producttype_gid = a.product_producttype_gid and b.producttype_isactive=''Y'' and b.producttype_isremoved=''N''
                    inner join gal_mst_tproductcategory as c on c.productcategory_gid=a.product_productcategory_gid and c.productcategory_isactive=''Y'' and c.productcategory_isremoved=''N''
                    left join (	select pc.prodcarton_productcartongid,(p.product_name) as carton_name,pc.prodcarton_gid,pc.prodcarton_productgid,
								pc.prodcarton_capacity,pc.prodcarton_remarks
								from gal_map_tprodcarton as pc
								inner join gal_mst_tproduct as p on p.product_gid =pc.prodcarton_productcartongid
                                and p.product_isactive=''Y'' and  p.product_isremoved=''N'') as sub

					on sub.prodcarton_productgid=a.product_gid
                    #and pc.prodcarton_isactive=''Y'' and pc.prodcarton_isremoved=''N''
					# gal_map_tprodcarton as d on d.prodcarton_productgid=a.product_gid
					inner join gal_mst_thsn as e on e.hsn_gid=a.product_hsn_gid and e.hsn_isactive=''Y'' and e.hsn_isremoved=''N''
                    left join ap_mst_tcategory as apc on apc.category_gid=a.product_category_gid and apc.category_isactive=''Y''
                    left join ap_mst_tsubcategory as aps on aps.subcategory_gid=a.product_subcategory_gid and aps.subcategory_isactive=''Y''
					inner join gal_mst_tuom as f on f.uom_gid  =a.product_uom_gid and f.uom_isactive=''Y'' and f.uom_isremoved=''N''
                    where a.entity_gid in (',@Entity_Gids,') ',Query_srch,' and a.product_isactive=''Y'' and  a.product_isremoved=''N'' '
                    );


                                               set li_count = 0 ;
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

			end if;

END