CREATE DEFINER=`developer`@`%` PROCEDURE `sp_SupplierProductMap_Set`(IN `Action` varchar(16),IN `lj_Supplierrate` json,
IN `li_entity_gid` int,IN `ls_create_by` int, OUT `Message` varchar(1000))
sp_SupplierProductMap_Set:BEGIN


declare supplierrate_srch Text;
declare ls_error varchar(100);
declare countRow int;
declare errno int;
declare msg varchar(1000);
declare Query_Update text;

	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
    set Message = concat(errno , msg);
    ROLLBACK;
    END;

set ls_error = '';


if Action = 'Insert' then

    select JSON_UNQUOTE(JSON_EXTRACT(lj_Supplierrate, CONCAT('$.supplierproduct_gid'))) into @supplierproduct_gid;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_Supplierrate, CONCAT('$.supplierproduct_supplier_gid'))) into @supplierproduct_supplier_gid;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_Supplierrate, CONCAT('$.supplierproduct_product_gid'))) into @supplierproduct_product_gid;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_Supplierrate, CONCAT('$.supplierproduct_unitprice'))) into @supplierproduct_unitprice;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_Supplierrate, CONCAT('$.supplierproduct_packingprice'))) into @supplierproduct_packingprice;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_Supplierrate, CONCAT('$.supplierproduct_validfrom'))) into @supplierproduct_validfrom;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_Supplierrate, CONCAT('$.supplierproduct_validto'))) into @supplierproduct_validto;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_Supplierrate, CONCAT('$.supplierproduct_dts'))) into @supplierproduct_dts;



    if @supplierproduct_supplier_gid = 0 then
		set Message = 'Supplier gid Not Given';
        leave sp_SupplierProductMap_Set;
    end if;

    if @supplierproduct_product_gid = 0 then
		set Message = 'Product gid Not Given';
        leave sp_SupplierProductMap_Set;
    end if;

    if @supplierproduct_unitprice = '0.00' then
		set Message = 'Unit Prize Not Given';
        leave sp_SupplierProductMap_Set;
    end if;

    if @supplierproduct_validfrom = '' then
		set Message = 'From Date Not Given';
        leave sp_SupplierProductMap_Set;
    end if;

    if @supplierproduct_validto = '' then
		set Message = 'To Date Not Given';
        leave sp_SupplierProductMap_Set;
    end if;

    if @supplierproduct_packingprice='' or @supplierproduct_packingprice is null then
		set @supplierproduct_packingprice=0.00;
    end if;

if ls_error = '' then

		start transaction;
        #select @supplierproduct_product_gid,@supplierproduct_supplier_gid;

		select  supplierproduct_gid INTO  @supplierproduct_gid
        from gal_map_tsupplierproduct
        where supplierproduct_supplier_gid=@supplierproduct_supplier_gid
        and supplierproduct_product_gid=@supplierproduct_product_gid   and
        supplierproduct_dts = @supplierproduct_dts and supplierproduct_isremoved='N' and supplierproduct_isactive='Y';

        #select @supplierproduct_gid,@supplierproduct_dts;

    if  @supplierproduct_gid  is not null then
		set  Query_Update = Concat('update gal_map_tsupplierproduct set supplierproduct_validto=now(), update_by = ',ls_create_by,',update_date = now(),supplierproduct_isactive=''N''');

		set Query_Update = Concat(Query_Update, ' where supplierproduct_gid = ''', @supplierproduct_gid ,'''');

        set @Query_Update = Query_Update;
        PREPARE stmt FROM @Query_Update;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;

			if countRow > 0 then
				set Message = 'SUCCESS';
				commit;
			else
				set Message = 'FAIL';
				rollback;
			end if;
    end if;


	set supplierrate_srch = concat('INSERT INTO gal_map_tsupplierproduct(supplierproduct_deliverydays,
									supplierproduct_capacitypw,supplierproduct_supplier_gid,
                                    supplierproduct_product_gid,supplierproduct_unitprice,
									supplierproduct_packingprice,supplierproduct_validfrom,supplierproduct_dts,
                                    supplierproduct_validto,entity_gid,create_by) VALUES
                                    (0,0,',@supplierproduct_supplier_gid,',' ,@supplierproduct_product_gid, ',
                                    ''',@supplierproduct_unitprice,''',''',@supplierproduct_packingprice,'''
                                    ,''',@supplierproduct_validfrom,''',''',@supplierproduct_dts,''',''',@supplierproduct_validto,''','
                                    ,li_entity_gid, ',',ls_create_by, ')');


        set @supplierrate_srch = supplierrate_srch;
        #SELECT @supplierrate_srch;
		PREPARE stmt FROM @supplierrate_srch;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;

        if countRow >  0 then
					select LAST_INSERT_ID() into Message ;
					set Message = CONCAT(Message,',SUCCESS');
					commit;
				else
					set Message = 'FAIL';
                    rollback;
		end if;
	else
		set Message = ls_error;
	end if;
end if;
if Action = 'Update' then

	select JSON_UNQUOTE(JSON_EXTRACT(lj_Supplierrate, CONCAT('$.supplierproduct_gid'))) into @supplierproduct_gid;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_Supplierrate, CONCAT('$.supplierproduct_supplier_gid'))) into @supplierproduct_supplier_gid;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_Supplierrate, CONCAT('$.supplierproduct_product_gid'))) into @supplierproduct_product_gid;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_Supplierrate, CONCAT('$.supplierproduct_unitprice'))) into @supplierproduct_unitprice;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_Supplierrate, CONCAT('$.supplierproduct_packingprice'))) into @supplierproduct_packingprice;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_Supplierrate, CONCAT('$.supplierproduct_validfrom'))) into @supplierproduct_validfrom;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_Supplierrate, CONCAT('$.supplierproduct_validto'))) into @supplierproduct_validto;


    if @supplierproduct_gid = 0 then
		set ls_error = 'Supplier Product Gid Not Given';
        leave sp_SupplierProductMap_Set;
	end if;

	if ls_error = '' then

		start transaction;

		set  Query_Update = Concat('update gal_map_tsupplierproduct set  update_by = ',ls_create_by,',update_date = now()');

			if @supplierproduct_supplier_gid <> '' or @supplierproduct_supplier_gid <> 0 then
				set Query_Update = Concat(Query_Update, ',supplierproduct_supplier_gid = ''', @supplierproduct_supplier_gid ,'''');
            end if;

			if @supplierproduct_product_gid <> '' or @supplierproduct_product_gid <> 0 then
				set Query_Update = Concat(Query_Update, ',supplierproduct_product_gid = ', @supplierproduct_product_gid ,'');
            end if;

            if @supplierproduct_unitprice <> '' or @supplierproduct_unitprice <> '0.00' then
				set Query_Update = Concat(Query_Update, ',supplierproduct_unitprice = ', @supplierproduct_unitprice ,'');
            end if;

            if @supplierproduct_packingprice <> '' or @supplierproduct_packingprice <> '0.00'  then
				set Query_Update = Concat(Query_Update, ',supplierproduct_packingprice = ', @supplierproduct_packingprice ,'');
            end if;

             if @supplierproduct_validto <> '' then
				set Query_Update = Concat(Query_Update, ',supplierproduct_validto = ''', @supplierproduct_validto ,'''');
            end if;

		set Query_Update = Concat(Query_Update, ' where supplierproduct_gid = ''', @supplierproduct_gid ,'''');

        set @Query_Update = Query_Update;
        PREPARE stmt FROM @Query_Update;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;

			if countRow > 0 then
				set Message = 'SUCCESS';
				commit;
			else
				set Message = 'FAIL';
				rollback;
			end if;

	else
		set Message = ls_error;
	end if;

end if;
if Action = 'Delete' then

	select JSON_UNQUOTE(JSON_EXTRACT(lj_Supplierrate, CONCAT('$.supplierproduct_gid'))) into @supplierproduct_gid;


    if @supplierproduct_gid = 0 then
		set ls_error = 'Supplier Product Gid Not Given';
        leave sp_SupplierProductMap_Set;
	end if;

	if ls_error = '' then

		start transaction;

		set  Query_Update = Concat('update gal_map_tsupplierproduct set  update_by = ',ls_create_by,',update_date = now(),supplierproduct_isremoved=''Y''');


		set Query_Update = Concat(Query_Update, ' where supplierproduct_gid = ''', @supplierproduct_gid ,'''');

        set @Query_Update = Query_Update;
        PREPARE stmt FROM @Query_Update;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;

			if countRow > 0 then
				set Message = 'SUCCESS';
				commit;
			else
				set Message = 'FAIL';
				rollback;
			end if;

	else
		set Message = ls_error;
	end if;

end if;

END