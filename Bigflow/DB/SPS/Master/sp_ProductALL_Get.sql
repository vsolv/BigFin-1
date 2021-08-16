CREATE DEFINER=`developer`@`%` PROCEDURE `galley`.`sp_ProductALL_Get`(IN `ls_Type` varchar(32),
IN `ls_Subtype` varchar(32),IN `lj_Filters` json,IN `lj_Classification` json,Out `Message` varchar(1024)
)
sp_ProductALL_Get:BEGIN
# Ramesh 2019 Jan 31 , July 12 2019
#Edit Prakash  31-jan-2019
Declare Query_Select varchar(1024);
Declare Query_Search varchar(1024);
Declare li_count int;
declare entity_gid varchar(64);
declare i int;

select JSON_LENGTH(lj_Classification, '$') into @li_jsonclass_count;

			if @li_jsonclass_count <=0 then
				set Message = 'Entity Gid Not Given';
				leave sp_ProductALL_Get;
			end if;

			set i = 0 ;

			select JSON_LENGTH(lj_Classification, CONCAT('$.Entity_Gid')) into @entity_cnt;

				if @entity_cnt <> 0 then
					WHILE i<= @entity_cnt - 1 Do

						select  JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid[',i,']')) into @entity_gid;
						if @entity_cnt  <> '' then
							 if @entity_gid <> 0 then
								if entity_gid <> '' then
									set entity_gid = concat(entity_gid,',',@entity_gid);
								else
									set entity_gid = @entity_gid;
								end if;

							end if;

						end if;
						set i = i + 1;

					END WHILE;
				end if;
 if ls_Type ='PRODUCT_CARTON' and ls_Subtype='SALES' then
        set Query_Select = '';
        set Query_Select = concat('
									select a.product_gid,c.prodcarton_gid,a.product_name,a.product_displayname,c.prodcarton_capacity,c.prodcarton_remarks
									 from gal_mst_tproduct as a
									inner join gal_mst_tproducttype as b on b.producttype_gid = a.product_producttype_gid
									inner join gal_map_tprodcarton as c on c.prodcarton_productcartongid = a.product_gid
									where a.product_isactive = ''Y'' and a.product_isremoved = ''N''
									and b.producttype_isactive = ''Y'' and b.producttype_isremoved = ''N''
									and c.prodcarton_isactive = ''Y'' and c.prodcarton_isremoved = ''N'' and a.entity_gid =  ',entity_gid,'
									group by a.product_name,a.product_displayname,c.prodcarton_capacity,prodcarton_remarks
                                    ');

                            	set @Query_Select = Query_Select;
												#	select @Query_Select; ## Remove It.
													PREPARE stmt1 FROM @Query_Select;
													EXECUTE stmt1;
													Select found_rows() into li_count;
													DEALLOCATE PREPARE stmt1;

													if li_count > 0 then
														set Message = 'FOUND';
													else
														set Message = 'NOT_FOUND';
													end if;
  elseif ls_Type ='PRODUCT_TYPE' and ls_Subtype='ALL' then
											set Query_Select = '';
								set Query_Select = concat('select producttype_gid , producttype_code , producttype_name FROM gal_mst_tproducttype as a
																			where producttype_isremoved = ''N'' and producttype_isactive = ''Y'' and a.entity_gid =  ',entity_gid,' order by producttype_name
														');

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

   elseif ls_Type ='PRODUCT' and ls_Subtype='ALL' then

									select JSON_LENGTH(lj_Filters, CONCAT('$')) into @json_count_filter;

                                      set Query_Search = '';
                                    if @json_count_filter > 0 then
											  select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Product_Type_Gid'))) into @Product_Type_Gid;

                                              if @Product_Type_Gid is not null and @Product_Type_Gid <> 0 and @Product_Type_Gid <> '' then

                                                        Set Query_Search = concat(' and product_producttype_gid = ',@Product_Type_Gid,' ');
                                              End if;

                                    End if;
										  set Query_Select = '';
										set Query_Select = concat('select a.product_gid,a.product_name,a.product_displayname
													 from gal_mst_tproduct as a
													where a.product_isactive = ''Y'' and a.product_isremoved = ''N'' ',Query_Search,'
													 and a.entity_gid in (',entity_gid,')
													order by product_producttype_gid
														');
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
		### ramesh 2019 dec
    elseif ls_Type ='PRODUCT_CAT' and ls_Subtype='PROD_SERVICE' then

        select productcategory_isprodservice as prod_cat_value,
   			case
		      when productcategory_isprodservice = 'P' then 'Product'
		      when productcategory_isprodservice = 'S' then 'Service'
		    end as 'prod_cat_data'
		     from gal_mst_tproductcategory as a
             where productcategory_isactive = 'Y' and productcategory_isremoved = 'N'
             and a.entity_gid = entity_gid
             group by productcategory_isprodservice ;


            Select found_rows() into li_count;

           if li_count > 0 then
				set Message = 'FOUND';
			else
				set Message = 'NOT_FOUND';
			end if;
elseif ls_Type ='PRODUCT_CAT' and ls_Subtype='DDL' then
              ### get The Pdct cat based on search mandatory ;; pdct service
           select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Prod_Service'))) into @Prod_Service;

          if @Prod_Service is null or @Prod_Service = '' THEN
          	set Message = 'Product Or Service Is Needed.';
          	leave sp_ProductALL_Get;
          End if;

        select productcategory_gid,productcategory_name,a.productcategory_isprodservice as prod_cat_value,
         case
		      when productcategory_isprodservice = 'P' then 'Product'
		      when productcategory_isprodservice = 'S' then 'Service'
		    end as 'prod_cat_data'
		     from gal_mst_tproductcategory as a
             where productcategory_isactive = 'Y' and productcategory_isremoved = 'N'
             and productcategory_isprodservice = @Prod_Service
             and a.entity_gid = entity_gid ;


            Select found_rows() into li_count;

           if li_count > 0 then
				set Message = 'FOUND';
			else
				set Message = 'NOT_FOUND';
			end if;


elseif ls_Type ='PRODUCT_TYPE' and ls_Subtype='DDL' then
              ### get The Pdct Type based on search mandatory ;; Pdct Category
           select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Prod_Cat_Gid'))) into @Prod_Cat_Gid;

          if @Prod_Cat_Gid is null or @Prod_Cat_Gid = '' THEN
          	set Message = 'Product Category Is Needed.';
          	leave sp_ProductALL_Get;
          End if;

            select producttype_gid,producttype_code,producttype_name
		     from gal_mst_tproducttype  as a
             where producttype_productcategory_gid = @Prod_Cat_Gid and producttype_isactive = 'Y' and producttype_isremoved = 'N'
             and entity_gid = entity_gid;

            Select found_rows() into li_count;

           if li_count > 0 then
				set Message = 'FOUND';
			else
				set Message = 'NOT_FOUND';
			end if;


end if;
END