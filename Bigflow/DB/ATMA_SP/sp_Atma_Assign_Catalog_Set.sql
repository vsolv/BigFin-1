CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Assign_Catalog_Set`(in li_Action  varchar(30),
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_Atma_Assign_Catalog_Set:BEGIN

#Balamaniraja       05-09-2019

Declare Query_Insert varchar(2000);
Declare Query_Update varchar(2000);
Declare countRow varchar(6000);
Declare errno int;
Declare msg varchar(1000);

						DECLARE EXIT HANDLER FOR SQLEXCEPTION
						BEGIN
							GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
							set Message = concat(errno , msg);
							ROLLBACK;
						END;

IF li_Action = 'Assign_Catalog_Insert'  then

START TRANSACTION;
		select JSON_LENGTH(lj_filter,'$') into @lj_filter_json_count;
		select JSON_LENGTH(lj_classification,'$') into @lj_classification_json_count;

        if @lj_classification_json_count = 0 or @lj_classification_json_count is null then
			set Message = 'No Data In classification Json. ';
			leave sp_Atma_Assign_Catalog_Set;
		End if;

        if @lj_filter_json_count = 0 or @lj_filter_json_count is null then
			set Message = 'No Data In filter Json. ';
			leave sp_Atma_Assign_Catalog_Set;
		End if;

    select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ActivitydtlpProduct_ActivityDetailsGid')))
	into @ActivitydtlpProduct_ActivityDetailsGid;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mPartnerProduct_Status')))
	into @mPartnerProduct_Status;
	#select @ActivitydtlpProduct_ActivityDetailsGid;

    select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mPartnerProduct_Gid')))
	into @mPartnerProduct_Gid;
	#select @mPartnerProduct_Gid;

	select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Entity_Gid')))
	into @Entity_Gid;
	#select @Entity_Gid;

	select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Create_By')))
	into @Create_By;
	#select @Create_By;

		if  @Entity_Gid = '' or @Entity_Gid is null   then
			set Message = 'Entity_Gid is not given ';
			leave sp_Atma_Assign_Catalog_Set;
		End if;

        if  @Create_By = '' or @Create_By is null   then
			set Message = 'Create_By is not given ';
			leave sp_Atma_Assign_Catalog_Set;
		End if;

        if  @ActivitydtlpProduct_ActivityDetailsGid = '' or @ActivitydtlpProduct_ActivityDetailsGid is null   then
			set Message = 'ActivitydtlpProduct_ActivityDetailsGid is not given ';
			leave sp_Atma_Assign_Catalog_Set;
		End if;

            set  @Product_Gid='';
			select mpartnerproduct_product_gid
			from atma_tmp_map_tpartnerproduct where
			mpartnerproduct_gid=@mPartnerProduct_Gid
            into @PartnerProduct_Gid ;
          #  select @PartnerProduct_Gid ;
           # select @ActivitydtlpProduct_ActivityDetailsGid;

            set  @Product_Category_Gid='';
            select product_category_gid
			from  gal_mst_tproduct 	where product_gid=@PartnerProduct_Gid
            into @Product_Category_Gid;
          #  select @Product_Category_Gid;

            set  @Product_Subcategory_Gid='';
            select product_subcategory_gid
			from  gal_mst_tproduct 	where product_gid=@PartnerProduct_Gid
            into @Product_Subcategory_Gid;
           # select @Product_Subcategory_Gid;

            set  @Product_Uom_Gid='';
            select product_uom_gid
			from  gal_mst_tproduct 	where product_gid=@PartnerProduct_Gid
            into @Product_Uom_Gid;
           # select @Product_Uom_Gid;

            set  @Product_UnitPrice='';
            select product_unitprice
			from  gal_mst_tproduct 	where product_gid=@PartnerProduct_Gid
            into @Product_UnitPrice;
           # select @Product_UnitPrice;

            set  @Product_Name='';
            select product_name
			from  gal_mst_tproduct 	where product_gid=@PartnerProduct_Gid
            into @Product_Name;
           # select @Product_Name;

            set  @mPartnerProduct_ValidFrom='';
            select mpartnerproduct_validfrom
			from  atma_tmp_map_tpartnerproduct 	where mpartnerproduct_gid=@mPartnerProduct_Gid
            into @mPartnerProduct_ValidFrom;
           # select @mPartnerProduct_ValidFrom;

            set  @mPartnerProduct_ValidTo='';
            select mpartnerproduct_validto
			from  atma_tmp_map_tpartnerproduct 	where mpartnerproduct_gid=@mPartnerProduct_Gid
            into @mPartnerProduct_ValidTo;
            #select @mPartnerProduct_ValidTo;


	set Query_Insert='';
	set Query_Insert=concat('insert into atma_tmp_map_tactivitydtlpproduct
                                 (activitydtlpproduct_activitydetailsgid,
								 activitydtlpproduct_category,activitydtlpproduct_subcategory,
								 activitydtlpproduct_name,activitydtlpproduct_mpartnerproductgid,
								 activitydtlpproduct_uomgid,activitydtlpproduct_rate,activitydtlpproduct_validfrom,
								 activitydtlpproduct_validto,entity_gid,create_by)
							 values(',@ActivitydtlpProduct_ActivityDetailsGid,','
								 ,@Product_Category_Gid,',',@Product_Subcategory_Gid,',
								 ''',@Product_Name,'''',',',@mPartnerProduct_Gid,',
								 ',@Product_Uom_Gid,',',@Product_UnitPrice,',
								 ''',@mPartnerProduct_ValidFrom,'''',',''',@mPartnerProduct_ValidTo,''',
								 ',@Entity_Gid,',',@Create_By,')');

	set @Insert_query = Query_Insert;

    #select Query_Insert;
	PREPARE stmt FROM @Insert_query;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
    if countRow >  0 then
		set Message = 'SUCCESSFULLY INSERTED';
	else
		set Message = 'INSERT FAILED';
		rollback;
	end if;


    set Query_Update ='';
    set Query_Update = concat('Update atma_tmp_map_tpartnerproduct
                         set mpartnerproduct_status=''',@mPartnerProduct_Status,'''
						 Where mpartnerproduct_gid = ',@mPartnerProduct_Gid,' and
                         mpartnerproduct_isactive=''Y''and
                         mpartnerproduct_isremoved=''N'' and entity_gid=',@Entity_Gid,'
                         ');

			#select Query_Update;
			set @Query_Update = Query_Update;
			PREPARE stmt FROM @Query_Update;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;

		if countRow <= 0 then
				set Message = 'Error On Update.';
				rollback;
				leave sp_Atma_Assign_Catalog_Set;
		elseif    countRow > 0 then
				set Message = 'SUCCESS';
                commit;
		end if;

    END IF;



END