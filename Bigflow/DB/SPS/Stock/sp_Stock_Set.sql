CREATE DEFINER=`root`@`%` PROCEDURE `sp_Stock_Set`(In `ls_Action` Varchar(64),In `ls_Type` Varchar(64),
In `lj_json` json, In `lj_stock_json` json,
in `li_create_by` int,in `li_entity_gid` int,
Out `Message` varchar(1024))
sp_Stock_Set:BEGIN
### Annyutha: Dec 2018
### Ramesh Jan 2019  Edit
declare Query_Insert varchar(1000);
declare Query_Update varchar(1000);
declare countRow int;
declare Updated_Row int;
declare errno int;
declare msg varchar(1000);
declare i int;
declare j int;
declare k int;
declare ls_error varchar(1024);
declare stock_available int;

	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
     ROLLBACK;
    set Message = concat(errno , msg);
    END;
set ls_error = '';

if ls_Action = 'UPDATE' and ls_Type = 'UPDATE_STOCK' then
	select JSON_LENGTH(lj_json, '$') into @li_json_count;

    if (@li_json_count  is null or @li_json_count = 0) then
				set Message = 'No Data In Json For Stock.';
				leave sp_Stock_Set;
	end if;

    select JSON_UNQUOTE(JSON_EXTRACT(lj_json, CONCAT('$.product_gid[0]'))) into @product_gid;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_json, CONCAT('$.count1[0]'))) into @count1;
    #select @product_gid,@count1;

    if  @count1<=0 or  @count1= '' or @count1 is null   then
		set Message='Enter the proper packed and unpacked qty';
        leave sp_Stock_Set;
    end if;

    if  @product_gid=0 then
		set Message='product_gid is not given';
        leave sp_Stock_Set;
    end if;

    set SQL_SAFE_UPDATES=0;
    set  Query_Insert = concat('update gal_trn_tstock stk1 inner join
												(select a.stock_gid as stkgid from gal_trn_tstock as a inner join  ( select stock_gid from gal_trn_tstock
												where stock_mode=1
												and stock_available=0
												and  stock_godown_gid=1
												and stock_product_gid=',@product_gid,' limit ',@count1,') as b on b.stock_gid=a.stock_gid) as stk on stk1.stock_gid=stk.stkgid
												set stk1.stock_available=1,
                                                Update_date=''', now(),''',
												update_by=''',li_create_by,'''
												where stock_mode=1
												and stock_available=0
												and  stock_godown_gid=1
												and stock_product_gid=',@product_gid,' ');


											set @Insert_query = Query_Insert;
										    #SELECT @Insert_query;   ## Remove it
											PREPARE stmt FROM @Insert_query;
											EXECUTE stmt;
											set countRow = (select ROW_COUNT());
											DEALLOCATE PREPARE stmt;

											if countRow >  0 then
												set Message = 'SUCCESS';
											else
												set Message = 'FAIL';
												rollback;
											end if;

end if;


 if ls_Action = 'Insert' and ls_Type = 'SINGLE' then
			select JSON_LENGTH(lj_json, '$.stock') into @li_json_count;

			if (@li_json_count  is null or @li_json_count = 0) then
				set Message = 'No Data In Json For Stock.';
				leave sp_Stock_Set;
			end if;

				set i = 0;
				select JSON_LENGTH(lj_json, '$.stock') into @li_stock_count;

				select JSON_UNQUOTE(JSON_EXTRACT(lj_json, CONCAT('$.ref_Gid[0]'))) into @ref_Gid;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_json, CONCAT('$.reftable_gid[0]'))) into @reftable_gid;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_json, CONCAT('$.type_mode[0]'))) into @type_mode;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_json, CONCAT('$.available[0]'))) into @available;

						if @type_mode = 'Purchase' then
							set @stock_mode = 1;
						elseif @type_mode = 'Sales' then
							set @stock_mode = 0;
						elseif @type_mode = 'Conversion' then
							set @stock_mode = 1;
                        elseif @type_mode = 'Sales Return' then
							set @stock_mode = 0;
						end if;


				if @ref_Gid = '' then
					set Message = 'Ref Gid not Given ';
					leave sp_Stock_Set;
				else
					set @err = concat('select case when isnull(ref_gid) then 0 else ref_gid end into @lref_gid from gal_mst_tref where ref_name like ''%stock_', @ref_Gid ,'%''');
					PREPARE stmt1 FROM @err;
					EXECUTE stmt1;
					DEALLOCATE PREPARE stmt1;

					set @lref_Gid = @lref_gid;
					if @lref_Gid = 0 then
						set ls_error = 'Given ref not in ref table';
                        set Message = ls_error;
                        rollback;
                        leave sp_Stock_Set;
					end if;

				end if;


				if @type_mode <> 'Conversion' then
					If @reftable_gid = 0 then
						set Message = 'Reftable Gid Not Given';
						leave sp_Stock_Set;
					end if;
				end if;

				if @type_mode = '' then
					set Message = 'Ref Gid not Given ';
					leave sp_Stock_Set;
				else
					set @err = concat('select case when isnull(metadata_gid) then 0 else metadata_gid end into @ltype_mode
					from gal_mst_tmetadata
					where metadata_tablename = ''gal_trn_tstock'' and metadata_value = ''', @type_mode ,'''');
					PREPARE stmt1 FROM @err;
					EXECUTE stmt1;
					DEALLOCATE PREPARE stmt1;
					set @ltype_mode = @ltype_mode;

					if @ltype_mode = 0 then
						set ls_error = 'Given Metadata not in Metadata table';
					end if;

				end if;


			WHILE i  <= @li_stock_count - 1 DO
						select JSON_UNQUOTE(JSON_EXTRACT(lj_json, CONCAT('$.stock[',i,'].product_gid[0]'))) into @product_gid;
						select JSON_UNQUOTE(JSON_EXTRACT(lj_json, CONCAT('$.stock[',i,'].quantity[0]'))) into @quantity;
						select JSON_UNQUOTE(JSON_EXTRACT(lj_json, CONCAT('$.stock[',i,'].godown_gid[0]'))) into @godown_gid;

						if @type_mode = 'Conversion' then
						   select JSON_UNQUOTE(JSON_EXTRACT(lj_json, CONCAT('$.stock[',i,'].con_prod_gid[0]'))) into @cprod_gid;
						end if;

						If @product_gid = 0 then
							set Message = 'Product Gid Not Given';
							leave sp_Stock_Set;
						end if;

						If @quantity = 0 or @quantity is null then
							set Message = 'Quantity Not Given';
							leave sp_Stock_Set;
						end if;

						If @godown_gid = 0 then
							set Message = 'Godown Gid Not Given';
							leave sp_Stock_Set;
						end if;

				if ls_error = '' then

						set j = 0;
					WHILE j  <= @quantity - 1 DO

										if @type_mode = 'Conversion' then
											set @stock_mode = 1;
										end if;

											set @q=j+1;

											if @stock_mode = 1 then
													select ifnull(max(stock_code),0) into @stockcode from gal_trn_tstock where stock_mode = 1;
														if @stockcode = 0 then
															set @stock_code = 1;
													else
															set @stock_code = @stockcode+1;
													end if;
											else

													select ifnull(max(stock_code),0) into @code1 from gal_trn_tstock where stock_code not in (
													select stock_code from gal_trn_tstock where stock_mode = 0 and stock_product_gid = @product_gid) limit 1;



												if @code1 = 0 then
													set Message = 'No Stock Available';
													leave sp_Stock_Set;
												else
													set @stock_code = @code1;

												end if;
											end if;

											if @stock_mode = 0 then

												select sum(stock_qty) into @qty1 from gal_trn_tstock where stock_mode = 1 and stock_product_gid = @product_gid;
												select sum(stock_qty) into @qty2 from gal_trn_tstock where stock_mode = 0 and stock_product_gid = @product_gid;
												### TO DO NOY Commented on Actual
												if @qty1 = @qty2 then
													set Message = 'There is no Remaining Quantity in stock';
													leave sp_Stock_Set;
												end if;
											end if;

											set  Query_Insert = concat('INSERT INTO gal_trn_tstock (stock_code, stock_product_gid,
														stock_mode, stock_refgid, stock_reftable_gid, stock_date, stock_typemode, stock_uomgid,
														stock_qty, stock_godown_gid, stock_available, entity_gid, create_by) VALUES (''',@stock_code,''',
														''',@product_gid,''',''',@stock_mode,''',''',@lref_Gid,''',''',@reftable_gid,''',now(),''',@ltype_mode,''',
														3,1,''',@godown_gid,''',''',@available,''',', li_entity_gid , ',' , li_create_by , ')');

											set @Insert_query = Query_Insert;
						#					SELECT @Insert_query;   ## Remove it
											PREPARE stmt FROM @Insert_query;
											EXECUTE stmt;
											set countRow = (select ROW_COUNT());
											DEALLOCATE PREPARE stmt;

											if countRow >  0 then
												set Message = 'SUCCESS';
											else
												set Message = 'FAIL';
												rollback;
											end if;

										SET j = j + 1;
					END WHILE;
				end if;

				if Message = 'SUCCESS' then

								select ifnull(sum(stockbalance_cb),0.00) into @openingbal from gal_trn_tstockbalance where stockbalance_gid in (
								select max(stockbalance_gid) from gal_trn_tstockbalance where stockbalance_productgid = @product_gid);

								if @stock_mode = 1 then
										set @inward = @quantity;
								else
										set @inward = 0;
								end if;

								if @stock_mode = 0 then
										set @outward = @quantity;
								else
										set @outward = 0;
								end if;

								set @closingbal = @openingbal + @inward - @outward;

						set  Query_Insert = concat('INSERT INTO gal_trn_tstockbalance (stockbalance_date, stockbalance_productgid,
								stockbalance_uomgid, stock_typemode, stockbalance_ob, stockbalance_inward, stockbalance_outward,stockbalance_cb,
								entity_gid, create_by) VALUES (now(),''',@product_gid,''',3,''',@ltype_mode,''',
								''',@openingbal,''',''',@inward,''',''',@outward,''',''',@closingbal,''',', li_entity_gid , ','
								, li_create_by , ')');

					set @Insert_query = Query_Insert;
					PREPARE stmt FROM @Insert_query;
					EXECUTE stmt;
					set countRow = (select ROW_COUNT());
					DEALLOCATE PREPARE stmt;

					if countRow >  0 then
							set Message = 'SUCCESS';
					else
							set Message = 'FAIL';
							rollback;
					end if;

				end if;

				if @type_mode = 'Conversion' then
						   select JSON_UNQUOTE(JSON_EXTRACT(lj_json, CONCAT('$.stock[',i,'].con_prod_gid[0]'))) into @cprod_gid;
						   set @stock_mode = 0;
						   set k = 0;
				WHILE k  <= @quantity - 1 DO
										select ifnull(max(stock_code),0) into @code1 from gal_trn_tstock where stock_code not in (
										select stock_code from gal_trn_tstock where stock_mode = 0 and stock_product_gid = @cprod_gid) limit 1;

										if @code1 = 0 then
											set Message = 'No Stock Available';
											leave sp_Stock_Set;
										else
											set @stock_code = @code1;
										end if;

									if @stock_mode = 0 then

										select sum(stock_qty) into @qty1 from gal_trn_tstock where stock_mode = 1 and stock_product_gid = @cprod_gid;
										select sum(stock_qty) into @qty2 from gal_trn_tstock where stock_mode = 0 and stock_product_gid = @cprod_gid;

										if @qty1 = @qty2 then
											set Message = 'There is no Remaining Quantity in stock';
											leave sp_Stock_Set;
										end if;
									end if;

									set  Query_Insert = concat('INSERT INTO gal_trn_tstock (stock_code, stock_product_gid,
												stock_mode, stock_refgid, stock_reftable_gid, stock_date, stock_typemode, stock_uomgid,
												stock_qty, stock_godown_gid, stock_available, entity_gid, create_by) VALUES (''',@stock_code,''',
												''',@cprod_gid,''',''',@stock_mode,''',''',@lref_Gid,''',''',@reftable_gid,''',now(),''',@ltype_mode,''',
												3,1,''',@godown_gid,''',''',@available,''',', li_entity_gid , ',' , li_create_by , ')');

									set @Insert_query = Query_Insert;
									#SELECT @Insert_query;
									PREPARE stmt FROM @Insert_query;
									EXECUTE stmt;
									set countRow = (select ROW_COUNT());
									DEALLOCATE PREPARE stmt;

									if countRow >  0 then
										set Message = 'SUCCESS';
									else
										set Message = 'FAIL';
										rollback;
									end if;

								SET k = k + 1;
				END WHILE;

				if Message = 'SUCCESS' then

								select ifnull(sum(stockbalance_cb),0.00) into @openingbal from gal_trn_tstockbalance where stockbalance_gid in (
								select max(stockbalance_gid) from gal_trn_tstockbalance where stockbalance_productgid = @cprod_gid);

								if @stock_mode = 1 then
									set @inward = @quantity;
								else
									set @inward = 0;
								end if;

								if @stock_mode = 0 then
									set @outward = @quantity;
								else
									set @outward = 0;
								end if;

								set @closingbal = @openingbal + @inward - @outward;
						set  Query_Insert = concat('INSERT INTO gal_trn_tstockbalance (stockbalance_date, stockbalance_productgid,
									stockbalance_uomgid, stock_typemode, stockbalance_ob, stockbalance_inward, stockbalance_outward,stockbalance_cb,
									entity_gid, create_by) VALUES (now(),''',@cprod_gid,''',3,''',@ltype_mode,''',
									''',@openingbal,''',''',@inward,''',''',@outward,''',''',@closingbal,''',', li_entity_gid , ','
									, li_create_by , ')');

								set @Insert_query = Query_Insert;
								PREPARE stmt FROM @Insert_query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;
										select countRow;
									if countRow >  0 then
										set Message = 'SUCCESS';
									else
										set Message = 'FAIL';
										rollback;
									end if;

								end if;
							end if;

							SET i = i + 1;
			END WHILE;


elseif ls_Action = 'Insert' and ls_Type = 'MULTIPLE' then

			select JSON_LENGTH(lj_json, '$.STOCK') into @li_json_count;

			if (@li_json_count  is null or @li_json_count = 0) then
				set Message = 'No Data In Json For Stock.';
				leave sp_Stock_Set;
			end if;

            select JSON_UNQUOTE(JSON_EXTRACT(lj_json, CONCAT('$.Ref_Name'))) into @Ref_Name;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_json, CONCAT('$.Type_Mode'))) into @Type_Mode;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_json, CONCAT('$.Available'))) into @Available;

            if @Ref_Name is null or @Ref_Name = '' then
						set Message = 'Ref Name Is Needed.';
                        leave sp_Stock_Set;
            End if;

					select ifnull(ref_gid,0) into @Ref_Gid_Stock
							from  gal_mst_tref
							where ref_name = @Ref_Name and ref_isremoved = 'N' ;

                if @Ref_Gid_Stock > 0 then
                   set @Ref_Gid_Stock = @Ref_Gid_Stock;
				else
                    set Message = 'Erorr On Stock Ref Gid Generation.Check The Ref Name.';
                    leave sp_Stock_Set;
                End if;

                if @Type_Mode = '' or @Type_Mode is null then
					set Message = 'Type Mode Is Needed.';
                    leave sp_Stock_Set;
                End if;

                set stock_available = @Available;
                if stock_available <> 0 and stock_available <> 1 then
					Set Message = 'Stock Available Must  Be 0 or 1.';
                    leave sp_Stock_Set;
                 end if;
                 ## Temp
                 set @Stock_Code = 1;

                 if @Ref_Name <> '' or @Ref_Name is not null and @Ref_Name = 'STOCK_SALES' then
						set @stock_mode = 1;
                 else
                      set Message = 'Error On Stock Mode.';
                      leave sp_Stock_Set;
                 End if;

                 if @Type_Mode = 'SALE_CANCEL' then
							select metadata_gid into @Type_Mode_Insert
                            from gal_mst_tmetadata
                            where metadata_value = 'SALE_CANCEL' and metadata_isactive = 'Y' and metadata_isremoved = 'N' ;

                        if @Type_Mode_Insert is not null or @Type_Mode_Insert <> '' then
									set @Type_Mode_Insert = @Type_Mode_Insert;
                        else
                                   set Message= 'Error On Stock Type Mode.';
                                   leave sp_Stock_Set;
                        End if;

                  else
                       set Message = 'Error On Stock Type Mode';
                       leave sp_Stock_Set;
                 End if;
				#### Details Level
								set i = 0;
								select JSON_LENGTH(lj_json, '$.STOCK') into @li_stock_count;

                	WHILE i  <= @li_stock_count - 1 DO
								select JSON_UNQUOTE(JSON_EXTRACT(lj_json, CONCAT('$.STOCK[',i,'].Product_Gid[0]'))) into @Product_Gid;
								select JSON_UNQUOTE(JSON_EXTRACT(lj_json, CONCAT('$.STOCK[',i,'].Quantity[0]'))) into @Quantity_Tot_Details;
								select JSON_UNQUOTE(JSON_EXTRACT(lj_json, CONCAT('$.STOCK[',i,'].Godown_Gid[0]'))) into @Godown_Gid;
                                select JSON_UNQUOTE(JSON_EXTRACT(lj_json, CONCAT('$.STOCK[',i,'].Reftable_Gid[0]'))) into @Reftable_Gid;

                                ### Validations if Above Selected ## TO DO
                                if @Product_Gid = 0 or @Product_Gid = '' or @Product_Gid is null  then
									set Message = 'Product Gid Is Needed.';
                                    leave sp_Stock_Set;
                                End if;

                                if @Quantity_Tot_Details = 0 or @Quantity_Tot_Details is null or @Quantity_Tot_Details = '' then
									set Message = 'Product Quantity Is Needed.';
                                    leave sp_Stock_Set;
                                End if;

                                if @Godown_Gid = 0 or @Godown_Gid is null then
									set Message = 'Godown Gid Is Needed.';
                                    leave sp_Stock_Set;
                                End if;

                                if @Reftable_Gid = 0 or @Reftable_Gid is null then
										set Message = 'Reftable Gid Is Needed.';
                                        leave sp_Stock_Set;
                                End if;


									select ifnull(product_uom_gid,0)  into @UOM_Gid_stock from gal_mst_tproduct
									where product_gid = @Product_Gid and product_isactive = 'Y' and product_isremoved = 'N' ;

										if @UOM_Gid_stock is null or @UOM_Gid_stock = 0 then
											set Message = 'Product UOM Gid Not Found.';
                                            leave sp_Stock_Set;
                                        End if;

                                set j = 0;
								WHILE j  <= @Quantity_Tot_Details - 1 DO

										set  Query_Insert = concat('INSERT INTO gal_trn_tstock (stock_code, stock_product_gid,
										stock_mode, stock_refgid, stock_reftable_gid, stock_date, stock_typemode, stock_uomgid,
										stock_qty, stock_godown_gid, stock_available, entity_gid, create_by) VALUES (''',@Stock_Code,''',
										''',@Product_Gid,''',''',@stock_mode,''',''',@Ref_Gid_Stock,''',''',@Reftable_Gid,''',now(),''',@Type_Mode_Insert,''',
										',@UOM_Gid_stock,',1,''',@Godown_Gid,''',''',@Available,''',', li_entity_gid , ',' , li_create_by , ')');

											set @Insert_query = Query_Insert;
										#	SELECT @Insert_query;   ## Remove it
											PREPARE stmt FROM @Insert_query;
											EXECUTE stmt;
											set countRow = (select ROW_COUNT());
											DEALLOCATE PREPARE stmt;

											if countRow >  0 then
												set Message = 'SUCCESS';
											else
												set Message = 'FAIL';
												rollback;
                                                leave sp_Stock_Set;
											end if;

										SET j = j + 1;

								END WHILE;
                                #### Update The Stock Balance Table.

                                	if Message = 'SUCCESS' then

												select ifnull(sum(stockbalance_cb),0.00) into @openingbal
                                                from gal_trn_tstockbalance
                                                where stockbalance_gid in (
												select max(stockbalance_gid)
                                                from gal_trn_tstockbalance where stockbalance_productgid = @Product_Gid);

                                                set @inward = 0 ;
                                                set @outward = 0 ;

												if @stock_mode = 1 then
														set @inward = @Quantity_Tot_Details;
												else
															set @inward = 0;
												end if;

												if @stock_mode = 0 then
														set @outward = @Quantity_Tot_Details;
												else
														set @outward = 0;
												end if;

												set @closingbal = @openingbal + @inward - @outward;


										set  Query_Insert = concat('INSERT INTO gal_trn_tstockbalance (stockbalance_date, stockbalance_productgid,
												stockbalance_uomgid, stock_typemode, stockbalance_ob, stockbalance_inward, stockbalance_outward,stockbalance_cb,
												entity_gid, create_by) VALUES (now(),''',@Product_Gid,''',',@UOM_Gid_stock,',''',@Type_Mode_Insert,''',
												''',@openingbal,''',''',@inward,''',''',@outward,''',''',@closingbal,''',', li_entity_gid , ','
												, li_create_by , ')');

																set @Insert_query = Query_Insert;
																PREPARE stmt FROM @Insert_query;
																EXECUTE stmt;
																set countRow = (select ROW_COUNT());
																DEALLOCATE PREPARE stmt;

																if countRow >  0 then
                                                                	set Message = 'SUCCESS';
																else
																		set Message = 'FAIL';
																		rollback;
																end if;

								end if;

                                set i = i+1;
                    END WHILE;


elseif ls_Action = 'Insert' and ls_Type = 'Inventory' then
			select JSON_LENGTH(lj_json, '$.stock') into @li_json_count;
			#select 'a';
			if (@li_json_count  is null or @li_json_count = 0) then
				set Message = 'No Data In Json For Stock.';
				leave sp_Stock_Set;
			end if;

				set i = 0;
				select JSON_LENGTH(lj_json, '$.stock') into @li_stock_count;

				select JSON_UNQUOTE(JSON_EXTRACT(lj_json, CONCAT('$.ref_Gid[0]'))) into @ref_Gid;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_json, CONCAT('$.reftable_gid[0]'))) into @reftable_gid;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_json, CONCAT('$.type_mode[0]'))) into @type_mode;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_json, CONCAT('$.available[0]'))) into @available;

						if @type_mode = 'Purchase' then
							set @stock_mode = 1;
						elseif @type_mode = 'Sales' then
							set @stock_mode = 0;
						elseif @type_mode = 'Conversion' then
							set @stock_mode = 1;
                        elseif @type_mode = 'Sales Return' then
							set @stock_mode = 1;
                         elseif @type_mode = 'Purchase Return' then
							set @stock_mode = 0;
                         elseif @type_mode = 'Purchase Inward' then
							set @stock_mode = 1;
						elseif @type_mode = 'Purchase Return - Received' then
							set @stock_mode = 1;
                         elseif @type_mode = 'Sales Damage' then
							set @stock_mode = 0;
                            elseif @type_mode = 'New Product' then
							set @stock_mode = 1;
						end if;


				if @ref_Gid = '' then
					set Message = 'Ref Gid not Given ';
					leave sp_Stock_Set;
				else
					set @err = concat('select case when isnull(ref_gid) then 0 else ref_gid end into @lref_gid from gal_mst_tref where ref_name like ''%stock_', @ref_Gid ,'%''');
					PREPARE stmt1 FROM @err;
					EXECUTE stmt1;
					DEALLOCATE PREPARE stmt1;

					set @lref_Gid = @lref_gid;
                    #select @lref_Gid;
					if @lref_Gid = 0 then
						set ls_error = 'Given ref not in ref table';
                        set Message = ls_error;
                        rollback;
                        leave sp_Stock_Set;
					end if;

				end if;


				if @type_mode <> 'Conversion' then
                  if @type_mode <> 'Sales Damage' then
					If @reftable_gid = 0 then
						set Message = 'Reftable Gid Not Given';
						leave sp_Stock_Set;
					end if;
                   end if;
				end if;

				if @type_mode = '' then
					set Message = 'Ref Gid not Given ';
					leave sp_Stock_Set;
				else
                #select @type_mode;
					set @err = concat('select case when isnull(metadata_gid) then 0 else metadata_gid end into @ltype_mode
					from gal_mst_tmetadata
					where metadata_tablename = ''gal_trn_tstock'' and metadata_value = ''', @type_mode ,'''');
					PREPARE stmt1 FROM @err;
					EXECUTE stmt1;
					DEALLOCATE PREPARE stmt1;
					set @ltype_mode = @ltype_mode;

					if @ltype_mode = 0 then
						set ls_error = 'Given Metadata not in Metadata table';
					end if;

				end if;


			WHILE i  <= @li_stock_count - 1 DO
						select JSON_UNQUOTE(JSON_EXTRACT(lj_json, CONCAT('$.stock[',i,'].product_gid[0]'))) into @product_gid;
						select JSON_UNQUOTE(JSON_EXTRACT(lj_json, CONCAT('$.stock[',i,'].quantity[0]'))) into @quantity;
						select JSON_UNQUOTE(JSON_EXTRACT(lj_json, CONCAT('$.stock[',i,'].godown_gid[0]'))) into @godown_gid;

						if @type_mode = 'Conversion' then
						   select JSON_UNQUOTE(JSON_EXTRACT(lj_json, CONCAT('$.stock[',i,'].con_prod_gid[0]'))) into @cprod_gid;
						   select JSON_UNQUOTE(JSON_EXTRACT(lj_json, CONCAT('$.stock[',i,'].conversion_headergid[0]'))) into @conversion_headergid;
						end if;

						If @product_gid = 0 then
							set Message = 'Product Gid Not Given';
							leave sp_Stock_Set;
						end if;

						If @quantity = 0 or @quantity is null then
							set Message = 'Quantity Not Given';
							leave sp_Stock_Set;
						end if;

						If @godown_gid = 0 then
							set Message = 'Godown Gid Not Given';
							leave sp_Stock_Set;
						end if;

				if ls_error = '' then

						set j = 0;
					WHILE j  <= @quantity - 1 DO

										if @type_mode = 'Conversion' then
											set @stock_mode = 1;
										end if;

											set @q=j+1;

											if @stock_mode = 1 then
													select ifnull(max(stock_code),0) into @stockcode from gal_trn_tstock where stock_mode = 1;
													if @stockcode = 0 then
															set @stock_code = 1;
													else
															set @stock_code = @stockcode+1;
															set @stock_code_tocon = @stockcode;
													end if;
											else

													select ifnull(max(stock_code),0) into @code1 from gal_trn_tstock where stock_code not in (
													select stock_code from gal_trn_tstock where stock_mode = 0 and stock_product_gid = @product_gid) limit 1;



												if @code1 = 0 then
													set Message = 'No Stock Available';
													leave sp_Stock_Set;
												else
													set @stock_code = @code1;

												end if;
											end if;

											if @stock_mode = 0 then

												select sum(stock_qty) into @qty1 from gal_trn_tstock where stock_mode = 1 and stock_product_gid = @product_gid;
												select sum(stock_qty) into @qty2 from gal_trn_tstock where stock_mode = 0 and stock_product_gid = @product_gid;
												### TO DO NOY Commented on Actual
												if @qty1 = @qty2 then
													set Message = 'There is no Remaining Quantity in stock';
													leave sp_Stock_Set;
												end if;
											end if;
											#select @product_gid,@stock_code,@stock_mode,@lref_Gid,@reftable_gid,@ltype_mode,@godown_gid,@available;
											set  Query_Insert = concat('INSERT INTO gal_trn_tstock (stock_code, stock_product_gid,
														stock_mode, stock_refgid, stock_reftable_gid, stock_date, stock_typemode, stock_uomgid,
														stock_qty, stock_godown_gid, stock_available, entity_gid, create_by) VALUES (''',@stock_code,''',
														''',@product_gid,''',''',@stock_mode,''',''',@lref_Gid,''',''',@reftable_gid,''',now(),''',@ltype_mode,''',
														3,1,''',@godown_gid,''',''',@available,''',', li_entity_gid , ',' , li_create_by , ')');

											set @Insert_query = Query_Insert;
											#SELECT @Insert_query;   ## Remove it
											PREPARE stmt FROM @Insert_query;
											EXECUTE stmt;
											set countRow = (select ROW_COUNT());
											DEALLOCATE PREPARE stmt;

											if countRow >  0 then
												set Message = 'SUCCESS';
                                                if @type_mode = 'Conversion' then
													select JSON_UNQUOTE(JSON_EXTRACT(lj_json, CONCAT('$.stock[',i,'].con_prod_gid[0]'))) into @cprod_gid;
													set @stock_mode_con = 0;
                                                    select ifnull(max(stock_code),0) into @code1 from gal_trn_tstock where stock_code not in (
															select stock_code from gal_trn_tstock where stock_mode = 0 and stock_product_gid = @cprod_gid) limit 1;

															if @code1 = 0 then
																set Message = 'No Stock Available';
																leave sp_Stock_Set;
															else
																set @stock_code_con = @code1;
															end if;

														if @stock_mode_con = 0 then

															select sum(stock_qty) into @qty1 from gal_trn_tstock where stock_mode = 1 and stock_product_gid = @cprod_gid;
															select sum(stock_qty) into @qty2 from gal_trn_tstock where stock_mode = 0 and stock_product_gid = @cprod_gid;

															if @qty1 = @qty2 then
																set Message = 'There is no Remaining Quantity in stock';
																leave sp_Stock_Set;
															end if;
														end if;

														set  Query_Insert = concat('INSERT INTO gal_trn_tstock (stock_code, stock_product_gid,
																	stock_mode, stock_refgid, stock_reftable_gid, stock_date, stock_typemode, stock_uomgid,
																	stock_qty, stock_godown_gid, stock_available, entity_gid, create_by) VALUES (''',@stock_code_con,''',
																	''',@cprod_gid,''',''',@stock_mode_con,''',''',@lref_Gid,''',''',@reftable_gid,''',now(),''',@ltype_mode,''',
																	3,1,''',@godown_gid,''',''',@available,''',', li_entity_gid , ',' , li_create_by , ')');

														set @Insert_query = Query_Insert;
														#SELECT @Insert_query;
														PREPARE stmt FROM @Insert_query;
														EXECUTE stmt;
														set countRow = (select ROW_COUNT());
														DEALLOCATE PREPARE stmt;

														if countRow >  0 then
															set Message = 'SUCCESS';
                                                            set  Query_Insert = concat('INSERT INTO gal_trn_tprodconversiondtl (prodconversiondtl_prodconversiongid, prodconversiondtl_stockgid,
																	prodconversiondtl_tostockgid, prodconversiondtl_productgid, prodconversiondtl_toproductgid, prodconversiondtl_remarks, entity_gid, create_by
                                                                    ) VALUES (''',@conversion_headergid,''',
																	''',@stock_code,''',''',@stock_code_con,''',''',@product_gid,''',''',@cprod_gid,''',''stock'',', li_entity_gid , ',', li_create_by , ')');
													#select @conversion_headergid,@stock_code,@stock_code_con,@product_gid,@cprod_gid;
															set @Insert_query = Query_Insert;
															SELECT @Insert_query;
															PREPARE stmt FROM @Insert_query;
															EXECUTE stmt;
															set countRow = (select ROW_COUNT());
															DEALLOCATE PREPARE stmt;
														else
															set Message = 'FAIL';
															rollback;
														end if;
                                                end if;
											else
												set Message = 'FAIL';
												rollback;
											end if;

										SET j = j + 1;
					END WHILE;
				end if;

				if Message = 'SUCCESS' then

								select ifnull(sum(stockbalance_cb),0.00) into @openingbal from gal_trn_tstockbalance where stockbalance_gid in (
								select max(stockbalance_gid) from gal_trn_tstockbalance where stockbalance_productgid = @product_gid);

								if @stock_mode = 1 then
										set @inward = @quantity;
								else
										set @inward = 0;
								end if;

								if @stock_mode = 0 then
										set @outward = @quantity;
								else
										set @outward = 0;
								end if;

								set @closingbal = @openingbal + @inward - @outward;

						set  Query_Insert = concat('INSERT INTO gal_trn_tstockbalance (stockbalance_date, stockbalance_productgid,
								stockbalance_uomgid, stock_typemode, stockbalance_ob, stockbalance_inward, stockbalance_outward,stockbalance_cb,
								entity_gid, create_by) VALUES (now(),''',@product_gid,''',3,''',@ltype_mode,''',
								''',@openingbal,''',''',@inward,''',''',@outward,''',''',@closingbal,''',', li_entity_gid , ','
								, li_create_by , ')');

					set @Insert_query = Query_Insert;
					PREPARE stmt FROM @Insert_query;
					EXECUTE stmt;
					set countRow = (select ROW_COUNT());
					DEALLOCATE PREPARE stmt;

					if countRow >  0 then
							set Message = 'SUCCESS';

					else
							set Message = 'FAIL';
							rollback;
					end if;

				end if;

                if @type_mode = 'Conversion' then

					if Message = 'SUCCESS' then

								select ifnull(sum(stockbalance_cb),0.00) into @openingbal from gal_trn_tstockbalance where stockbalance_gid in (
								select max(stockbalance_gid) from gal_trn_tstockbalance where stockbalance_productgid = @cprod_gid);

								if @stock_mode_con = 1 then
									set @inward = @quantity;
								else
									set @inward = 0;
								end if;

								if @stock_mode_con = 0 then
									set @outward = @quantity;
								else
									set @outward = 0;
								end if;

								set @closingbal = @openingbal + @inward - @outward;
						set  Query_Insert = concat('INSERT INTO gal_trn_tstockbalance (stockbalance_date, stockbalance_productgid,
									stockbalance_uomgid, stock_typemode, stockbalance_ob, stockbalance_inward, stockbalance_outward,stockbalance_cb,
									entity_gid, create_by) VALUES (now(),''',@cprod_gid,''',3,''',@ltype_mode,''',
									''',@openingbal,''',''',@inward,''',''',@outward,''',''',@closingbal,''',', li_entity_gid , ','
									, li_create_by , ')');

								set @Insert_query = Query_Insert;
								PREPARE stmt FROM @Insert_query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;
										#select countRow;
									if countRow >  0 then
										set Message = 'SUCCESS';
                                        update gal_trn_tprodconversion set prodconversion_status = 'APPROVED' , update_by =  li_create_by , Update_date = current_timestamp()
												where prodconversion_gid = @conversion_headergid;

												set countRow = (select ROW_COUNT());

											if countRow > 0 then
													set Message = 'SUCCESS';
											else
												set Message = 'FAIL IN STATUS .';
												rollback;

											end if;

									else
										set Message = 'FAIL';
										rollback;
									end if;

						end if;
                     end if;



							SET i = i + 1;
			END WHILE;



End if;



END