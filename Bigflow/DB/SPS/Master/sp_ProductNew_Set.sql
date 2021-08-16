CREATE DEFINER=`developer`@`%` PROCEDURE `galley`.`sp_ProductNew_Set`(in Action varchar(16),
                                in Type varchar(32),
                                in in_json json,
                                out Message varchar(1000))
sp_ProductNew_Set:BEGIN
declare num varchar(30);
declare num1 int;
declare varchr varchar(30);
declare countRow int;
declare productcat_code varchar(16);
declare producttype_code varchar(12);
declare Query_Update varchar(5000);
### Santhosh` Create - aug-oct- 2019.
## Ramesh Edit - Dec 2019

if Action = 'Insert' and Type='insert_data' then
               ### Product Insert
			select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.product_name'))into @product_name;
			select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.product_displayname'))into @product_displayname;
			select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.product_tradingitem'))into @product_tradingitem;
			select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.product_hsn_gid'))into @product_hsn_gid;
			select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.product_uom_gid'))into @product_uom_gid;
			select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.product_category_gid'))into @product_category_gid;
			select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.product_subcategory_gid'))into @product_subcategory_gid;

			select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.product_productcategory_gid'))into @product_productcategory_gid;
			select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.product_producttype_gid'))into @product_producttype_gid;
            select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.product_tallyname'))into @product_tallyname;
			select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.product_unitprice'))into @product_unitprice;
			select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.product_weight'))into @product_weight;
			select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.product_isactive'))into @product_isactive;
			select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.product_isremoved'))into @product_isremoved;
			select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.entity_gid'))into @entity_gid;
			select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.create_by'))into @create_by;
			select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.create_date'))into @create_date;
			select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.insert_flag'))into @insert_flag;
			select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.update_flag'))into @update_flag;
			select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.update_by'))into @update_by;
			select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.Update_date'))into @Update_date;

				#select max(product_code) into @product_code from gal_mst_tproduct;
				select substring(product_code,5)  from gal_mst_tproduct where product_gid =(select max(product_gid)
					from gal_mst_tproduct where product_isremoved='N') into @codes;

                    if @codes is null or @codes = '' then
						set @codes = '0';
                    End if;

				call sp_Generatecode_Get('WITHOUT_DATE','PROD','00000',@codes,@Message) ;
				select @Message into  @product_code;

				  select count(product_gid) into @duplicate_check from gal_mst_tproduct where product_name=@product_name;
					if @duplicate_check > 0 then
						set Message="Duplicate Product Name";
						leave sp_ProductNew_Set;
					end if;

					start transaction;

						  insert into gal_mst_tproduct(product_code,
						  product_name,product_tallyname, product_displayname, product_tradingitem,
						  product_hsn_gid, product_uom_gid, product_category_gid,
						  product_subcategory_gid, product_productcategory_gid,
						  product_producttype_gid, product_unitprice, product_weight,
						  entity_gid,
						  create_by)
						  values(@product_code,@product_name,@product_tallyname, @product_displayname, @product_tradingitem,
						  @product_hsn_gid, @product_uom_gid, @product_category_gid,
						  @product_subcategory_gid, @product_productcategory_gid,
						  @product_producttype_gid, @product_unitprice, @product_weight,
							@entity_gid, @create_by);


					   set countRow = (select ROW_COUNT());



					if countRow > 0 then
						select LAST_INSERT_ID() into Message ;
						set Message ='SUCCESS';
							commit;
						else
							set Message = 'FAIL';
							rollback;
					end if;
		 #Productcategory_insert Santhosh 08-06-2019
elseif Action = 'Insert' and Type='Product_Category' then

			select JSON_LENGTH(in_json,'$') into @json_count;

			if @json_count is null and @json_count =0 then
			  set Message='Productcategory Json Empty';
			  leave sp_ProductNew_Set;
			end if;

		   select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.Productcat_Name'))into @productcat_name;
		   select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.Entity_Gid'))into @entity_gid;
		   select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.Create_By'))into @create_by;
		   select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.Client_Gid'))into @client_gid;
		   select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.Stock_impact'))into @stock_impact;
           select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.Prod_Service'))into @Prod_Service;

           if @Prod_Service is null or @Prod_Service = '' then
				set Message = 'Product Or Service Is Required.';
                leave sp_ProductNew_Set;
           End if;

         select substring(productcategory_code,5)  from gal_mst_tproductcategory where productcategory_gid =(select max(productcategory_gid)
         from gal_mst_tproductcategory where productcategory_isremoved='N') into @codes;

         if @codes is null or @codes = '' then
				set @codes = '0';
         End if;

         call sp_Generatecode_Get('WITHOUT_DATE','PDCT','00',@codes,@Message) ;

         select @Message into productcat_code;

         select count(productcategory_gid) into @Cate_duplicate_check from gal_mst_tproductcategory where
         productcategory_name=@productcat_name;

         if @Cate_duplicate_check > 0 then
          set Message='Duplicate Productcategory Name';
          leave sp_ProductNew_Set;
         end if;

         start transaction;

				  insert into gal_mst_tproductcategory(productcategory_code,
                  productcategory_name,productcategory_clientgid,productcategory_stockimpact,productcategory_isprodservice,entity_gid,
                  create_by)
				  values(productcat_code,@productcat_name,@client_gid,@stock_impact,@Prod_Service,@entity_gid, @create_by);

               set countRow = (select ROW_COUNT());

			if countRow > 0 then
				set Message ='SUCCESS';
					commit;
				else
					set Message = 'FAIL';
					rollback;
			end if;

#Producttype Insert Santhosh 10-06-2019

elseif Action = 'Insert' and Type='Product_Type' then

        set producttype_code='PTYPE';

        select JSON_LENGTH(in_json,'$') into @json_count;

        if @json_count is null and @json_count =0 then
          set Message='Producttype Json Empty';
          leave sp_ProductNew_Set;
	    end if;

		   select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.Producttype_Name'))into @producttype_name;
		   select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.Producttype_Category_gid'))into @producttype_cate_gid;
		   select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.Entity_Gid'))into @entity_gid;
		   select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.Create_By'))into @create_by;


             select count(producttype_gid) into @Type_duplicate_check from gal_mst_tproducttype where
         producttype_name = @producttype_name;

         if @Type_duplicate_check > 0 then
          set Message='Duplicate Producttype Name';
          leave sp_ProductNew_Set;
         end if;

         start transaction;

				  insert into gal_mst_tproducttype(producttype_productcategory_gid,producttype_code,
                  producttype_name,entity_gid, create_by)
                 values(@producttype_cate_gid,producttype_code,@producttype_name,@entity_gid, @create_by);
               set countRow = (select ROW_COUNT());

			if countRow > 0 then
				set Message ='SUCCESS';
					commit;
				else
					set Message = 'FAIL';
					rollback;
			end if;
 #Productcarton Mapping Santhosh 11-06-2019
elseif Action='Insert' and Type='Product_Carton_Map' then

        select JSON_LENGTH(in_json,'$') into @json_count;

        if @json_count is null and @json_count =0 then
          set Message='Productcarton Json Empty';
          leave sp_ProductNew_Set;
	    end if;

		   select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.Productcarton_gid'))into @productcarton_gid;
		   select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.Product_gid'))into @product_gid;
		   select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.Productcarton_Capacity'))into @productcarton_capacity;
		   select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.Productcarton_Remark'))into @productcarton_remark;
		   select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.Entity_Gid'))into @entity_gid;
		   select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.Create_By'))into @create_by;

           if @productcarton_capacity is null or @productcarton_capacity = 0 or cast(@productcarton_capacity as decimal) <= 0 then
				set Message = 'Product Carton Capacity Must Be Greater Than Zero.';
                leave sp_ProductNew_Set;
           End if;


         start transaction;

				  insert into gal_map_tprodcarton(prodcarton_productgid,prodcarton_productcartongid,
                  prodcarton_capacity,prodcarton_remarks,entity_gid, create_by)
                 values(@product_gid,@productcarton_gid,@productcarton_capacity,@productcarton_remark,@entity_gid, @create_by);
               set countRow = (select ROW_COUNT());

			if countRow > 0 then
				set Message ='SUCCESS';
					commit;
				else
					set Message = 'FAIL';
					rollback;
			end if;
 #karthiga - update -    23-10-2019
elseif Action='Update' and Type='insert_data' then

            select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.product_gid'))into @product_gid;
			select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.product_code'))into @product_code;
            select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.product_name'))into @product_name;
			select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.product_displayname'))into @product_displayname;
			select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.product_tradingitem'))into @product_tradingitem;
			select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.product_hsn_gid'))into @product_hsn_gid;
            select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.product_uom_gid'))into @product_uom_gid;
            select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.product_category_gid'))into @product_category_gid;
            select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.product_subcategory_gid'))into @product_subcategory_gid;
		    #set @product_category_gid=0;
			 #set @product_subcategory_gid=0;

			select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.product_productcategory_gid'))into @product_productcategory_gid;
			select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.product_producttype_gid'))into @product_producttype_gid;
			select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.product_unitprice'))into @product_unitprice;
			select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.product_weight'))into @product_weight;
			select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.create_by'))into @create_by;
			select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.entity_gid'))into @entity_gid;
			select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.product_tallyname'))into @product_tallyname;
			#select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.tally_product_name'))into @tally_product_name;

			select count(product_gid) into @duplicate_check from gal_mst_tproduct where product_name=@product_name
            and product_gid<> @product_gid;
            if @duplicate_check > 0 then
            set Message="Duplicate Product Name";
            leave sp_ProductNew_Set;
            end if;

         if @product_gid is not null or @product_gid <> ''
				   or @product_gid <> 0 then
			set @product_gid=@product_gid;
			end if;

			set Query_Update = '';


            if @product_code is not null or @product_code <> '' then
				set Query_Update = concat(Query_Update, ',product_code = ''',@product_code,''' ');
			end if;

            if @product_name is not null or @product_name <> '' then
				set Query_Update = concat(Query_Update, ',product_name = ''',@product_name,''' ');
			end if;

            if @product_tallyname is not null or @product_tallyname <> '' then
				set Query_Update = concat(Query_Update, ',product_tallyname = ''',@product_tallyname,''' ');
			end if;

            #if @tally_product_name is not null or @tally_product_name <> '' then
			#	set Query_Update = concat(Query_Update, ',tally_product_name = ''',@tally_product_name,''' ');
			#end if;

            if @product_displayname is not null or @product_displayname <> '' then
				set Query_Update = concat(Query_Update, ',product_displayname = ''',@product_displayname,''' ');
			end if;

             if @product_tradingitem is not null or @product_tradingitem <> '' then
				set Query_Update = concat(Query_Update, ',product_tradingitem = ''',@product_tradingitem,''' ');
			end if;

            if @product_unitprice is not null or @product_unitprice <> '' then
				set Query_Update = concat(Query_Update, ',product_unitprice = ''',@product_unitprice,''' ');
			end if;

            if @product_weight is not null or @product_weight <> '' then
				set Query_Update = concat(Query_Update, ',product_weight = ''',@product_weight,''' ');
			end if;

            if @product_hsn_gid is not null or @product_hsn_gid <> '' then
				set Query_Update = concat(Query_Update, ',product_hsn_gid = ''',@product_hsn_gid,''' ');
			end if;

            if @product_uom_gid is not null or @product_uom_gid <> '' then
				set Query_Update = concat(Query_Update, ',product_uom_gid = ''',@product_uom_gid,''' ');
			end if;

            if @product_category_gid is not null or @product_category_gid <> '' then
				set Query_Update = concat(Query_Update, ',product_category_gid = ''',@product_category_gid,''' ');
			end if;

            if @product_subcategory_gid is not null or @product_subcategory_gid <> '' then
				set Query_Update = concat(Query_Update, ',product_subcategory_gid = ''',@product_subcategory_gid,''' ');
			end if;

            if @product_productcategory_gid is not null or @product_productcategory_gid <> '' then
				set Query_Update = concat(Query_Update, ',product_productcategory_gid = ''',@product_productcategory_gid,''' ');
			end if;

            if @product_producttype_gid is not null or @product_producttype_gid <> '' then
				set Query_Update = concat(Query_Update, ',product_producttype_gid = ''',@product_producttype_gid,''' ');
			end if;


		 SET SQL_SAFE_UPDATES = 0;
		 set Query_Update = concat('Update gal_mst_tproduct
									set Update_date = CURRENT_TIMESTAMP,update_by=',@create_by,'',Query_Update,'
									Where  product_gid=',@product_gid,'
									and
                                    product_isactive = ''Y'' and product_isremoved = ''N'' ');

            #set @Query_Update = '';
			set @Query_Update = Query_Update;
			PREPARE stmt FROM @Query_Update;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;

		if countRow <= 0 then
				set Message = 'Error On Update.';
				rollback;
				leave sp_ProductNew_Set;
		elseif    countRow > 0 then
				set Message = 'SUCCESSFULLY UPDATED';
                commit;
		end if;

elseif Action = 'Update' and Type='Product_Category' then

        select JSON_LENGTH(in_json,'$') into @json_count;

        if @json_count is null and @json_count =0 then
          set Message='Productcategory Json Empty';
          leave sp_ProductNew_Set;
	    end if;

		   select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.productcategory_name'))into @productcategory_name;
		   select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.Entity_Gid'))into @entity_gid;
		   select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.productcategory_gid'))into @productcategory_gid;
		   #select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.productcategory_code'))into @productcategory_code;
		   select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.productcategory_stockimpact'))into @productcategory_stockimpact;
           select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.create_by'))into @create_by;
		   select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.productcategory_clientgid'))into @productcategory_clientgid;
           select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.Prod_Service'))into @Prod_Service;


        select count(productcategory_gid) into @Cate_duplicate_check from gal_mst_tproductcategory where
         productcategory_name=@productcategory_name and productcategory_gid <> @productcategory_gid ;

         if @Cate_duplicate_check > 0 then
          set Message='Duplicate Productcategory Name';
          leave sp_ProductNew_Set;
         end if;

           if @productcategory_gid is not null or @productcategory_gid <> ''
				   or @productcategory_gid <> 0 then
			set @productcategory_gid=@productcategory_gid;
			end if;

			set Query_Update = '';


           # if @productcategory_code is not null or @productcategory_code <> '' then
				#set Query_Update = concat(Query_Update, ',productcategory_code = ''',@productcategory_code,''' ');
		#	end if;

            if @productcategory_name is not null or @productcategory_name <> '' then
				set Query_Update = concat(Query_Update, ',productcategory_name = ''',@productcategory_name,''' ');
			end if;

            if @productcategory_stockimpact is not null or @productcategory_stockimpact <> '' then
				set Query_Update = concat(Query_Update, ',productcategory_stockimpact = ''',@productcategory_stockimpact,''' ');
			end if;

            if @productcategory_clientgid is not null or @productcategory_clientgid <> '' then
				set Query_Update = concat(Query_Update, ',productcategory_clientgid = ''',@productcategory_clientgid,''' ');
			end if;

            if @Prod_Service is not null or @Prod_Service <> '' then
				set Query_Update = concat(Query_Update, ',productcategory_isprodservice = ''',@Prod_Service,''' ');
            End if;


             SET SQL_SAFE_UPDATES = 0;
		 set Query_Update = concat('Update gal_mst_tproductcategory
									set Update_date = CURRENT_TIMESTAMP,update_by=',@create_by,'',Query_Update,'
									Where  productcategory_gid=',@productcategory_gid,'
									and
                                    productcategory_isactive = ''Y'' and productcategory_isremoved = ''N'' ');
		 select Query_Update;

            #set @Query_Update = '';
			set @Query_Update = Query_Update;
			PREPARE stmt FROM @Query_Update;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;

		if countRow <= 0 then
				set Message = 'Error On Update.';
				rollback;
				leave sp_ProductNew_Set;
		elseif    countRow > 0 then
				set Message = 'SUCCESSFULLY UPDATED';
                commit;
		end if;


elseif Action = 'Update' and Type='Product_Type' then
	    #select 1;
        set producttype_code='PTYPE';

        select JSON_LENGTH(in_json,'$') into @json_count;

        if @json_count is null and @json_count =0 then
          set Message='Producttype Json Empty';
          leave sp_ProductNew_Set;
	    end if;

		   select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.producttype_name'))into @producttype_name;
		   select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.producttype_gid'))into @producttype_gid;
		   select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.producttype_productcategory_gid'))into @producttype_productcategory_gid;
		   select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.producttype_code'))into @producttype_code;
           select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.create_by'))into @create_by;


		   select count(producttype_gid) into @Type_duplicate_check from gal_mst_tproducttype where
           producttype_name = @producttype_name and producttype_gid <> @producttype_gid ;

           if @Type_duplicate_check > 0 then
             set Message='Duplicate Producttype Name';
             leave sp_ProductNew_Set;
           end if;

           if @producttype_gid is not null or @producttype_gid <> '' or @producttype_gid <> 0 then
				set @producttype_gid=@producttype_gid;
		   end if;

			set Query_Update = '';


            if @producttype_name is not null or @producttype_name <> '' then
				set Query_Update = concat(Query_Update, ',producttype_name = ''',@producttype_name,''' ');
			end if;

            if @producttype_productcategory_gid is not null or @producttype_productcategory_gid <> '' then
				set Query_Update = concat(Query_Update, ',producttype_productcategory_gid = ''',@producttype_productcategory_gid,''' ');
			end if;


             SET SQL_SAFE_UPDATES = 0;
		 set Query_Update = concat('Update gal_mst_tproducttype
									set Update_date = CURRENT_TIMESTAMP,update_by=',@create_by,'',Query_Update,'
									Where  producttype_gid=',@producttype_gid,'
									and
                                    producttype_isactive = ''Y'' and producttype_isremoved = ''N'' ');
			#select Query_Update;

            #set @Query_Update = '';
			set @Query_Update = Query_Update;
			PREPARE stmt FROM @Query_Update;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;

		if countRow <= 0 then
				set Message = 'Error On Update.';
				rollback;
				leave sp_ProductNew_Set;
		elseif    countRow > 0 then
				set Message = 'SUCCESSFULLY UPDATED';
                commit;
		end if;

elseif Action='Update' and Type='Product_Carton_Map' then
                #  select 1;
        select JSON_LENGTH(in_json,'$') into @json_count;

        if @json_count is null and @json_count =0 then
          set Message='Productcarton Json Empty';
          leave sp_ProductNew_Set;
	    end if;
      # select @json_count;

		   select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.prodcarton_gid'))into @prodcarton_gid;
		   select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.prodcarton_capacity'))into @prodcarton_capacity;
		   #select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.Productcarton_Capacity'))into @productcarton_capacity;
		   select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.prodcarton_remarks'))into @prodcarton_remarks;
           select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.prodcarton_productgid'))into @prodcarton_productgid;
           select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.prodcarton_productcartongid'))into @prodcarton_productcartongid;
		   select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.Entity_Gid'))into @entity_gid;
		   select JSON_UNQUOTE(JSON_EXTRACT(in_json,'$.create_by'))into @create_by;
		  	#prodcarton_gid,prodcarton_capacity,prodcarton_remarks,prodcarton_isactive,prodcarton_isremoved,entity_gid,

          if @prodcarton_gid is not null or @prodcarton_gid <> ''
				   or @prodcarton_gid <> 0 then
			set @prodcarton_gid=@prodcarton_gid;
			end if;

			set Query_Update = '';


            if @prodcarton_capacity is not null or @prodcarton_capacity <> '' then
                  if cast(@prodcarton_capacity as decimal) <= 0 then
						set Message = 'Product Carton Capacity Must Be Greater Than Zero.';
                        leave sp_ProductNew_Set;
                  end if;
				set Query_Update = concat(Query_Update, ',prodcarton_capacity = ''',@prodcarton_capacity,''' ');
			end if;

            if @prodcarton_remarks is not null or @prodcarton_remarks <> '' then
				set Query_Update = concat(Query_Update, ',prodcarton_remarks = ''',@prodcarton_remarks,''' ');
			end if;

			 if @prodcarton_productgid is not null or @prodcarton_productgid <> '' then
				set Query_Update = concat(Query_Update, ',prodcarton_productgid = ''',@prodcarton_productgid,''' ');
			end if;

             if @prodcarton_productcartongid is not null or @prodcarton_productcartongid <> '' then
				set Query_Update = concat(Query_Update, ',prodcarton_productcartongid = ''',@prodcarton_productcartongid,''' ');
			end if;
                    #select 3;
             SET SQL_SAFE_UPDATES = 0;
		 set Query_Update = concat('Update gal_map_tprodcarton
									set Update_date = CURRENT_TIMESTAMP,update_by=',@create_by,'',Query_Update,'
									Where  prodcarton_gid=',@prodcarton_gid,'
									and
                                    prodcarton_isactive = ''Y'' and prodcarton_isremoved = ''N'' ');


            set @Query_Update = '';
			set @Query_Update = Query_Update;
			PREPARE stmt FROM @Query_Update;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;

		if countRow <= 0 then
				set Message = 'Error On Update.';
				rollback;
				leave sp_ProductNew_Set;
		elseif    countRow > 0 then
				set Message = 'SUCCESSFULLY UPDATED';
                commit;
		end if;


	end if;

END