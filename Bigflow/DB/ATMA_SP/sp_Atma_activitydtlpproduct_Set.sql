CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_activitydtlpproduct_Set`(in Action  varchar(20),
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_Atma_activitydtlpproduct_Set:BEGIN

#Balamaniraja       17-07-2019

declare Query_Insert varchar(1000);
Declare countRow varchar(6000);
declare Query_Update varchar(1000);
declare Query_Value varchar(1000);
declare Query_Column varchar(1000);
Declare errno int;
Declare msg,Error_Level varchar(1000);

DECLARE EXIT HANDLER FOR SQLEXCEPTION
BEGIN
	GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
	set Message = concat(Error_Level,' : No-',errno , msg);
	ROLLBACK;
END;


IF Action = 'activitydtlpp_INSERT'  then

			start transaction;
		select JSON_LENGTH(lj_filter,'$') into @li_jsoncount;
		select JSON_LENGTH(lj_classification,'$') into @li_classification_jsoncount;

			if @li_jsoncount = 0 or @li_jsoncount is null  then
				set Message = 'No Data In Json. ';
				leave sp_Atma_activitydtlpproduct_Set;
			End if;

			if @li_classification_jsoncount = 0 or @li_classification_jsoncount = ''
				or @li_classification_jsoncount is null  then
				set Message = 'No Entity_Gid and Create by In Json. ';
				leave sp_Atma_activitydtlpproduct_Set;
			End if;

		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.activitydtlpproduct_ActivityDetailsGid')))
        into @activitydtlpproduct_ActivityDetailsGid;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.activitydtlpproduct_partnerbranchgid')))
        into @activitydtlpproduct_partnerbranchgid;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.activitydtlpproduct_Category')))
        into @activitydtlpproduct_Category;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.activitydtlpproduct_SubCategory')))
        into @activitydtlpproduct_SubCategory;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.activitydtlpproduct_Name')))
        into @Catlog_Name;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.activitydtlpproduct_Spec')))
        into @activitydtlpproduct_Spec;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.activitydtlpproduct_Size')))
        into @activitydtlpproduct_Size;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.activitydtlpproduct_Remarks')))
        into @activitydtlpproduct_Remarks;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.activitydtlpproduct_UomGid')))
        into @activitydtlpproduct_UomGid;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.activitydtlpproduct_Rate')))
        into @activitydtlpproduct_Rate;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.activitydtlpproduct_ValidFrom')))
        into @activitydtlpproduct_ValidFrom;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.activitydtlpproduct_ValidTo')))
        into @activitydtlpproduct_ValidTo;

        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mPartnerProduct_Status')))
        into @mPartnerProduct_Status;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mPartnerProduct_Partner_Gid')))
        into @mPartnerProduct_Partner_Gid;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mPartnerProduct_Product_Gid')))
        into @mPartnerProduct_Product_Gid;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mPartnerProduct_UnitPrice')))
        into @mPartnerProduct_UnitPrice;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mPartnerProduct_PackingPrice')))
        into @mPartnerProduct_PackingPrice;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mPartnerProduct_DeliveryDays')))
        into @mPartnerProduct_DeliveryDays;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mPartnerProduct_CapacityPW')))
        into @mPartnerProduct_CapacityPW;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mPartnerProduct_DTS')))
        into @mPartnerProduct_DTS;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Entity_Gid')))into @Entity_Gid;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Create_By')))into @Create_By;

			set @activitydtlpproduct_ValidFrom=date_format(@activitydtlpproduct_ValidFrom,'%Y-%m-%d');
			set @activitydtlpproduct_ValidTo=date_format(@activitydtlpproduct_ValidTo,'%Y-%m-%d');

		if @activitydtlpproduct_ValidFrom >= @activitydtlpproduct_ValidTo then
				set Message ='To date should be greater than From date ';
				rollback;
				leave sp_Atma_activitydtlpproduct_Set;
		end if;

		if @activitydtlpproduct_ActivityDetailsGid = '' or @activitydtlpproduct_ActivityDetailsGid is null
			or @activitydtlpproduct_ActivityDetailsGid =0 then
				set Message ='activitydtlpproduct_ActivityDetailsGid Is Not Given';
				rollback;
				leave sp_Atma_activitydtlpproduct_Set;
		end if;

        if @activitydtlpproduct_Category = '' or @activitydtlpproduct_Category is null then
				set Message ='activitydtlpproduct_Category Is Not Given';
				rollback;
				leave sp_Atma_activitydtlpproduct_Set;
		end if;

        if @activitydtlpproduct_SubCategory = '' or @activitydtlpproduct_SubCategory is null then
				set Message ='activitydtlpproduct_SubCategory Is Not Given';
				rollback;
				leave sp_Atma_activitydtlpproduct_Set;
		end if;

        if @Catlog_Name = '' or @Catlog_Name is null then
				set Message ='activitydtlpproduct_Name Is Not Given';
				rollback;
				leave sp_Atma_activitydtlpproduct_Set;
		end if;

		if @activitydtlpproduct_UomGid = '' or @activitydtlpproduct_UomGid is null then
				set Message ='activitydtlpproduct_UomGid Is Not Given';
				rollback;
				leave sp_Atma_activitydtlpproduct_Set;
		end if;

        if @activitydtlpproduct_Rate = '' or @activitydtlpproduct_Rate is null then
				set Message ='activitydtlpproduct_Rate Is Not Given';
				rollback;
				leave sp_Atma_activitydtlpproduct_Set;
		end if;

        if @activitydtlpproduct_ValidFrom = '' or @activitydtlpproduct_ValidFrom is null then
				set Message ='activitydtlpproduct_ValidFrom Is Not Given';
				rollback;
				leave sp_Atma_activitydtlpproduct_Set;
		end if;

        if @activitydtlpproduct_ValidTo = '' or @activitydtlpproduct_ValidTo is null then
				set Message ='activitydtlpproduct_ValidTo Is Not Given';
				rollback;
				leave sp_Atma_activitydtlpproduct_Set;
		end if;

        if @mPartnerProduct_Partner_Gid = '' or @mPartnerProduct_Partner_Gid is null then
				set Message ='mPartnerProduct_Partner_Gid Is Not Given';
				rollback;
				leave sp_Atma_activitydtlpproduct_Set;
		end if;

		if @mPartnerProduct_Product_Gid = '' or @mPartnerProduct_Product_Gid is null then
				set Message ='mPartnerProduct_Product_Gid Is Not Given';
				rollback;
				leave sp_Atma_activitydtlpproduct_Set;
		end if;

		if @mPartnerProduct_UnitPrice = '' or @mPartnerProduct_UnitPrice is null then
				set Message ='mPartnerProduct_UnitPrice Is Not Given';
				rollback;
				leave sp_Atma_activitydtlpproduct_Set;
		end if;

		if @mPartnerProduct_PackingPrice = '' or @mPartnerProduct_PackingPrice is null then
				set Message ='mPartnerProduct_PackingPrice Is Not Given';
				rollback;
				leave sp_Atma_activitydtlpproduct_Set;
		end if;

		if @mPartnerProduct_DeliveryDays = '' or @mPartnerProduct_DeliveryDays is null then
				set Message ='mPartnerProduct_DeliveryDays Is Not Given';
				rollback;
				leave sp_Atma_activitydtlpproduct_Set;
		end if;

		if @mPartnerProduct_CapacityPW = '' or @mPartnerProduct_CapacityPW is null then
				set Message ='mPartnerProduct_CapacityPW Is Not Given';
				rollback;
				leave sp_Atma_activitydtlpproduct_Set;
		end if;

        if @mPartnerProduct_DTS = '' or @mPartnerProduct_DTS is null then
				set Message ='mPartnerProduct_DTS Is Not Given';
				rollback;
				leave sp_Atma_activitydtlpproduct_Set;
		end if;



	#set @mPartnerProduct_Status='Pending';
    set Error_Level='ATMA4.1';
	set Query_Insert='';
    set Query_Insert=concat('insert into atma_tmp_map_tpartnerproduct
								    (mpartnerproduct_partner_gid,mpartnerproduct_partnerbranch_gid,
                                    mpartnerproduct_product_gid,
                                    mpartnerproduct_unitprice,mpartnerproduct_packingprice,
                                    mpartnerproduct_validfrom,mpartnerproduct_validto,
                                    mpartnerproduct_deliverydays,mpartnerproduct_capacitypw,
                                    mpartnerproduct_dts,mpartnerproduct_status,
                                    entity_gid, create_by)
                            values(',@mPartnerProduct_Partner_Gid,',',@activitydtlpproduct_partnerbranchgid,',',@mPartnerProduct_Product_Gid,',
									',@mPartnerProduct_UnitPrice,',',@mPartnerProduct_PackingPrice,',
                                    ''',@activitydtlpproduct_ValidFrom,''',''',@activitydtlpproduct_ValidTo,''',
                                    ',@mPartnerProduct_DeliveryDays,',',@mPartnerProduct_CapacityPW,',
                                    ''',@mPartnerProduct_DTS,''',''',@mPartnerProduct_Status,''',
                                    ',@Entity_Gid,',',@Create_By,')
										');

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

    #set activitydtlpproduct_mpartnerproductgid

    select LAST_INSERT_ID() into @activitydtlpproduct_mpartnerproductgid;

		set Query_Column='';
		set Query_Value='';

		if @activitydtlpproduct_Spec is not null then
            set Query_Column = concat(Query_Column,",activitydtlpproduct_spec ");
            set Query_Value=   concat(Query_Value,",'",@activitydtlpproduct_Spec,"'");
		end if;

        if @activitydtlpproduct_Size is not null then
            set Query_Column = concat(Query_Column,",activitydtlpproduct_size ");
            set Query_Value=   concat(Query_Value,",'",@activitydtlpproduct_Size,"'");
		end if;

        if @activitydtlpproduct_Remarks is not null then
            set Query_Column = concat(Query_Column,",activitydtlpproduct_remarks ");
            set Query_Value=   concat(Query_Value,",'",@activitydtlpproduct_Remarks,"'");
		end if;
    set Error_Level='ATMA4.2';
    set Query_Insert='';
    set Query_Insert=concat("insert into atma_tmp_map_tactivitydtlpproduct(activitydtlpproduct_activitydetailsgid,
							 activitydtlpproduct_category,
							 activitydtlpproduct_subcategory,activitydtlpproduct_name,
                             activitydtlpproduct_mpartnerproductgid,
                             activitydtlpproduct_uomgid,
							 activitydtlpproduct_rate,activitydtlpproduct_validfrom,activitydtlpproduct_validto,
							 entity_gid,create_by",Query_Column,")values(",@activitydtlpproduct_ActivityDetailsGid,","
                             ,@activitydtlpproduct_Category,",",@activitydtlpproduct_SubCategory,",'",@Catlog_Name,"'",
                             ",",@activitydtlpproduct_mpartnerproductgid,
                             ",",@activitydtlpproduct_UomGid,",",@activitydtlpproduct_Rate,",'",@activitydtlpproduct_ValidFrom,"'",
                             ",'",@activitydtlpproduct_ValidTo,"',",@Entity_Gid,",",@Create_By,"",Query_Value,")");

	set @Insert_query = Query_Insert;

    #select Query_Insert;

	PREPARE stmt FROM @Insert_query;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
    if countRow >  0 then
		set Message = 'SUCCESSFULLY INSERTED';
        commit;
	else
		set Message = 'INSERT FAILED';
		rollback;
	end if;

				set Error_Level='ATMA4.3';
				call sp_Trans_Set('Insert','PARTNER_NAME',@activitydtlpproduct_mpartnerproductgid,
								 @mPartnerProduct_Status,'I','MAKER','',
								 @Entity_Gid,@Create_By,@message);

				select @message into @out_msg_tran ;

				if @out_msg_tran = 'FAIL' then
					set Message = 'Failed On Tran Insert';
					rollback;
					leave sp_Atma_activitydtlpproduct_Set;
				else
					commit;
				End if;


ELSEIF Action='activitydtlpp_UPDATE' then

				START TRANSACTION;

		select JSON_LENGTH(lj_filter,'$') into @li_jsoncount;
		select JSON_LENGTH(lj_classification,'$') into @li_classification_json_count;

					if @li_jsoncount = 0 or @li_jsoncount is null
						or @li_jsoncount = ''  then
							set Message = 'No Data In filter Json - Update.';
							leave sp_Atma_activitydtlpproduct_Set;
					End if;

					if @li_classification_json_count = 0  or @li_classification_json_count = ''
						or @li_classification_json_count is null  then
							set Message = 'No Data In classification Json - Update.';
							leave sp_Atma_activitydtlpproduct_Set;
					End if;

				select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.activitydtlpproduct_Gid')))
                into @activitydtlpproduct_Gid;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.activitydtlpproduct_partnerbranchgid')))
        into @activitydtlpproduct_partnerbranchgid;
                #select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.activitydtlpproduct_mpartnerproductgid')))
                #into @activitydtlpproduct_mpartnerproductgid;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.activitydtlpproduct_Category')))
				into @activitydtlpproduct_Category;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.activitydtlpproduct_SubCategory')))
				into @activitydtlpproduct_SubCategory;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.activitydtlpproduct_Spec')))
				into @activitydtlpproduct_Spec;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.activitydtlpproduct_Size')))
				into @activitydtlpproduct_Size;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.activitydtlpproduct_Remarks')))
				into @activitydtlpproduct_Remarks;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.activitydtlpproduct_UomGid')))
				into @activitydtlpproduct_UomGid;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.activitydtlpproduct_Rate')))
				into @activitydtlpproduct_Rate;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.activitydtlpproduct_ValidFrom')))
				into @activitydtlpproduct_ValidFrom;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.activitydtlpproduct_ValidTo')))
				into @activitydtlpproduct_ValidTo;


				select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mPartnerProduct_Product_Gid')))
				into @mPartnerProduct_Product_Gid;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mPartnerProduct_UnitPrice')))
				into @mPartnerProduct_UnitPrice;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mPartnerProduct_PackingPrice')))
				into @mPartnerProduct_PackingPrice;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mPartnerProduct_DeliveryDays')))
				into @mPartnerProduct_DeliveryDays;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mPartnerProduct_CapacityPW')))
				into @mPartnerProduct_CapacityPW;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mPartnerProduct_DTS')))
				into @mPartnerProduct_DTS;

                select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Update_By')))
				into @Update_By;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Entity_Gid')))
				into @Entity_Gid;

					set @activitydtlpproduct_ValidFrom=date_format(@activitydtlpproduct_ValidFrom,'%Y-%m-%d');
					set @activitydtlpproduct_ValidTo=date_format(@activitydtlpproduct_ValidTo,'%Y-%m-%d');

						if @activitydtlpproduct_ValidFrom >= @activitydtlpproduct_ValidTo then
							set Message ='To date should be greater than From date ';
							rollback;
							leave sp_Atma_activitydtlpproduct_Set;
						end if;

			set Query_Update = '';

            if @activitydtlpproduct_ActivityDetailsGid is not null or @activitydtlpproduct_ActivityDetailsGid <> '' then
				    set Query_Update = concat(Query_Update, ',activitydtlpproduct_activitydetailsgid = ',@activitydtlpproduct_ActivityDetailsGid,' ');
			end if;

            if @activitydtlpproduct_Category is not null or @activitydtlpproduct_Category <> '' then
				    set Query_Update = concat(Query_Update, ',activitydtlpproduct_Category = ',@activitydtlpproduct_Category,' ');
			end if;

            if @activitydtlpproduct_SubCategory is not null or @activitydtlpproduct_SubCategory <> '' then
				    set Query_Update = concat(Query_Update, ',activitydtlpproduct_subcategory = ',@activitydtlpproduct_SubCategory,' ');
			end if;


            #if @Catlog_Name is not null or @Catlog_Name <> '' then
				 #   set Query_Update = concat(Query_Update, ',activitydtlpproduct_name = ''',@Catlog_Name,''' ');
			#end if;

			if @activitydtlpproduct_Spec is not null or @activitydtlpproduct_Spec <> '' then
				    set Query_Update = concat(Query_Update, ',activitydtlpproduct_spec = ''',@activitydtlpproduct_Spec,''' ');
			end if;

            if @activitydtlpproduct_Size is not null or @activitydtlpproduct_Size <> '' then
				    set Query_Update = concat(Query_Update, ',activitydtlpproduct_size = ',@activitydtlpproduct_Size,' ');
			end if;

            if @activitydtlpproduct_Remarks is not null or @activitydtlpproduct_Remarks <> '' then
				    set Query_Update = concat(Query_Update, ',activitydtlpproduct_remarks = ''',@activitydtlpproduct_Remarks,''' ');
			end if;

            if @activitydtlpproduct_UomGid is not null or @activitydtlpproduct_UomGid <> '' then
				    set Query_Update = concat(Query_Update, ',activitydtlpproduct_uomgid = ',@activitydtlpproduct_UomGid,' ');
			end if;

            if @activitydtlpproduct_Rate is not null or @activitydtlpproduct_Rate <> '' then
				    set Query_Update = concat(Query_Update, ',activitydtlpproduct_rate = ',@activitydtlpproduct_Rate,' ');
			end if;

            if @activitydtlpproduct_ValidFrom is not null or @activitydtlpproduct_ValidFrom <> '' then
				    set Query_Update = concat(Query_Update, ',activitydtlpproduct_validfrom = ''',@activitydtlpproduct_ValidFrom,''' ');
			end if;

            if @activitydtlpproduct_ValidTo is not null or @activitydtlpproduct_ValidTo <> '' then
				    set Query_Update = concat(Query_Update, ',activitydtlpproduct_validto = ''',@activitydtlpproduct_ValidTo,''' ');
			end if;
            set Error_Level='ATMA4.4';
            set Query_Update = concat('Update atma_tmp_map_tactivitydtlpproduct
                         set update_date = CURRENT_TIMESTAMP,update_by=',@Update_By,'
                         ',Query_Update,'
						 Where activitydtlpproduct_gid = ',@activitydtlpproduct_Gid,' and
                         activitydtlpproduct_isactive=''Y''and
                         activitydtlpproduct_isremoved=''N'' and entity_gid=',@Entity_Gid,'
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
				leave sp_Atma_activitydtlpproduct_Set;
		elseif    countRow > 0 then
				set Message = 'SUCCESSFULLY UPDATED';
                commit;
		end if;




			set Query_Update = '';

                if @mPartnerProduct_Product_Gid is not null or @mPartnerProduct_Product_Gid <> '' then
				    set Query_Update = concat(Query_Update, ',mpartnerproduct_product_gid = ',@mPartnerProduct_Product_Gid,' ');
				end if;

                select @mPartnerProduct_Product_Gid;

               if @mPartnerProduct_UnitPrice is not null or @mPartnerProduct_UnitPrice <> '' then
				    set Query_Update = concat(Query_Update, ',mpartnerproduct_unitprice = ''',@mPartnerProduct_UnitPrice,''' ');
				end if;

                if @mPartnerProduct_PackingPrice is not null or @mPartnerProduct_PackingPrice <> '' then
				    set Query_Update = concat(Query_Update, ',mpartnerproduct_packingprice = ''',@mPartnerProduct_PackingPrice,''' ');
				end if;

               if @activitydtlpproduct_ValidFrom is not null or @activitydtlpproduct_ValidFrom <> '' then
				    set Query_Update = concat(Query_Update, ',mpartnerproduct_validfrom = ''',@activitydtlpproduct_ValidFrom,''' ');
				end if;

                if @activitydtlpproduct_ValidTo is not null or @activitydtlpproduct_ValidTo <> '' then
				    set Query_Update = concat(Query_Update, ',mpartnerproduct_validto = ''',@activitydtlpproduct_ValidTo,''' ');
				end if;

                if @mPartnerProduct_DeliveryDays is not null or @mPartnerProduct_DeliveryDays <> '' then
				    set Query_Update = concat(Query_Update, ',mpartnerproduct_deliverydays = ',@mPartnerProduct_DeliveryDays,' ');
				end if;

                if @mPartnerProduct_CapacityPW is not null or @mPartnerProduct_CapacityPW <> '' then
				    set Query_Update = concat(Query_Update, ',mpartnerproduct_capacitypw = ',@mPartnerProduct_CapacityPW,' ');
				end if;

                if @mPartnerProduct_DTS is not null or @mPartnerProduct_DTS <> '' then
				    set Query_Update = concat(Query_Update, ',mpartnerproduct_dts = ''',@mPartnerProduct_DTS,''' ');
				end if;


			select activitydtlpproduct_mpartnerproductgid from atma_tmp_map_tactivitydtlpproduct
            where activitydtlpproduct_gid=@activitydtlpproduct_Gid into @mPartnerProduct_Gid;


            set Error_Level='ATMA4.5';
            set Query_Update = concat('Update atma_tmp_map_tpartnerproduct
                         set update_date = CURRENT_TIMESTAMP,update_by=',@Update_By,'
                         ,mpartnerproduct_partnerbranch_gid=',@activitydtlpproduct_partnerbranchgid,'
                         ',Query_Update,'
						 Where mpartnerproduct_gid = ',@mPartnerProduct_Gid,' and
                         mpartnerproduct_isactive=''Y'' and
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
				leave sp_Atma_activitydtlpproduct_Set;
		elseif    countRow > 0 then
				set Message = 'SUCCESSFULLY UPDATED';
                commit;
		end if;


END IF;



END