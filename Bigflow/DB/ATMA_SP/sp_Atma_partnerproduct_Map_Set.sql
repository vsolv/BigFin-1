CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_partnerproduct_Map_Set`(in ls_Action varchar(16),
in lj_filter json,in lj_classification json,
out Message varchar(1000))
sp_Atma_partnerproduct_Map_Set:BEGIN
declare Query_Insert varchar(1000);
Declare countRow varchar(6000);
Declare Query_Update varchar(1000);
Declare Query_Value varchar(1000);
Declare Query_Column varchar(1000);
Declare errno int;
Declare msg varchar(1000);

						DECLARE EXIT HANDLER FOR SQLEXCEPTION
						BEGIN
							GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
							set Message = concat(errno , msg);
							ROLLBACK;
						END;

if ls_Action = 'INSERT'  then

         start transaction;

		select JSON_LENGTH(lj_filter,'$') into @li_filter_jsoncount;
		select JSON_LENGTH(lj_classification,'$') into @li_classification_jsoncount;

		if @li_filter_jsoncount = 0 or @li_filter_jsoncount is null  then
			set Message = 'No Data In Json. ';
			leave sp_Atma_partnerproduct_Map_Set;
		End if;

         if @li_classification_jsoncount = 0 or @li_classification_jsoncount = ''
            or @li_classification_jsoncount is null  then
			set Message = 'No Entity_Gid and Create by In Json. ';
			leave sp_Atma_partnerproduct_Map_Set;
		End if;



			select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Entity_Gid')))into @Entity_Gid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Create_By')))into @Create_By;



			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Mpartnerproduct_Partner_gid')))into @Mpartnerproduct_Partner_gid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Mpartnerproduct_Product_gid')))into @Mpartnerproduct_Product_gid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Mpartnerproduct_Unitprice')))into @Mpartnerproduct_Unitprice;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Mpartnerproduct_Packingprice')))into @Mpartnerproduct_Packingprice;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Mpartnerproduct_Validfrom')))into @Mpartnerproduct_Validfrom;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Mpartnerproduct_Validto')))into @Mpartnerproduct_Validto;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Mpartnerproduct_Deliverydays')))into @Mpartnerproduct_Deliverydays;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Mpartnerproduct_Capacitypw')))into @Mpartnerproduct_Capacitypw;
			#select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Mpartnerproduct_Dts')))into @Mpartnerproduct_Dts;
			set @Mpartnerproduct_Status='PENDING';

				if  @Mpartnerproduct_Validfrom = '' or
                @Mpartnerproduct_Validfrom is null  then
				set Message ='Mpartnerproduct_Validfrom Is Not Given';
				rollback;
				leave sp_Atma_partnerproduct_Map_Set;
				end if;

				if  @Mpartnerproduct_Validto = '' or
                @Mpartnerproduct_Validto is null  then
				set Message ='Mpartnerproduct ValidtoIs Not Given';
				rollback;
				leave sp_Atma_partnerproduct_Map_Set;
				end if;

				set @Mpartnerproduct_Validfrom=date_format(@Mpartnerproduct_Validfrom,'%Y-%m-%d');
				set @Mpartnerproduct_Validto=date_format(@Mpartnerproduct_Validto,'%Y-%m-%d');

                if @Mpartnerproduct_Validfrom >= @Mpartnerproduct_Validto then
				set Message ='Valid To Date  should be greater than Valid From Date ';
				rollback;
				leave sp_Atma_partnerproduct_Map_Set;
				end if;

                if @Entity_Gid = 0 or @Entity_Gid = '' or @Entity_Gid is null  then
				set Message ='Entity Gid Is Not Given';
				rollback;
				leave sp_Atma_partnerproduct_Map_Set;
				end if;

                if @Create_By = 0 or @Create_By = '' or @Create_By is null  then
				set Message ='Create By Is Not Given';
				rollback;
				leave sp_Atma_partnerproduct_Map_Set;
				end if;

                if @Mpartnerproduct_Partner_gid = 0 or @Mpartnerproduct_Partner_gid = '' or
                @Mpartnerproduct_Partner_gid is null  then
				set Message ='Mpartnerproduct Partner gid Is Not Given';
				rollback;
				leave sp_Atma_partnerproduct_Map_Set;
				end if;

                if @Mpartnerproduct_Product_gid = 0 or @Mpartnerproduct_Product_gid = '' or
                @Mpartnerproduct_Product_gid is null  then
				set Message ='Mpartnerproduct Product gid Is Not Given';
				rollback;
				leave sp_Atma_partnerproduct_Map_Set;
				end if;

                if  @Mpartnerproduct_Unitprice = '' or
                @Mpartnerproduct_Unitprice is null  then
				set Message ='Mpartnerproduct Product gid Is Not Given';
				rollback;
				leave sp_Atma_partnerproduct_Map_Set;
				end if;

				if  @Mpartnerproduct_Packingprice = '' or
                @Mpartnerproduct_Packingprice is null  then
				set Message ='Mpartnerproduct Packing price Is Not Given';
				rollback;
				leave sp_Atma_partnerproduct_Map_Set;
				end if;

				if  @Mpartnerproduct_Deliverydays = '' or
                @Mpartnerproduct_Deliverydays is null  then
				set Message ='Mpartnerproduct Delivery days Is Not Given';
				rollback;
				leave sp_Atma_partnerproduct_Map_Set;
				end if;

                if  @Mpartnerproduct_Capacitypw = '' or
                @Mpartnerproduct_Capacitypw is null  then
				set Message ='Mpartnerproduct Capacitypw Is Not Given';
				rollback;
				leave sp_Atma_partnerproduct_Map_Set;
				end if;

		set Query_Insert='';

		set Query_Insert=concat('insert into atma_tmp_map_tpartnerproduct(mpartnerproduct_partner_gid,mpartnerproduct_product_gid,mpartnerproduct_unitprice,
								mpartnerproduct_packingprice,mpartnerproduct_validfrom,mpartnerproduct_validto,
                                mpartnerproduct_deliverydays,mpartnerproduct_capacitypw,mpartnerproduct_status
								,entity_gid,create_by)
								values(',@Mpartnerproduct_Partner_gid,',',@Mpartnerproduct_Product_gid,',',@Mpartnerproduct_Unitprice,',
                                ',@Mpartnerproduct_Packingprice,',''',@Mpartnerproduct_Validfrom,''',''',@Mpartnerproduct_Validto,''',
                                ',@Mpartnerproduct_Deliverydays,',',@Mpartnerproduct_Capacitypw,',''',@Mpartnerproduct_Status,''',
                                ',@Entity_Gid,',',@Create_By,')'

							);
		#select Query_Insert;
		set @Insert_query = Query_Insert;

		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'SUCCESSFULLY INSERTED';
			#commit;
		else
			set Message = 'INSERT FAILED';
			rollback;
		end if;

select LAST_INSERT_ID() into @li_Mpartnerproduct_gid_Max ;

#select max(partnerproduct_gid) from atma_mst_tpartnerproduct into @li_Mpartnerproduct_gid_Max;
#Select fn_REFGid('PARTNER_NAME') into @refparnerproductid;
call sp_Trans_Set('Insert','PARTNER_NAME',@li_Mpartnerproduct_gid_Max,@Mpartnerproduct_Status,'I','MAKER','',
                     @Entity_Gid,@Create_By,@message);
					select @message into @out_msg_tran ;

				if @out_msg_tran = 'FAIL' then
					set Message = 'Failed On Tran Insert';
					rollback;
					leave sp_Atma_partnerproduct_Map_Set;
				else
					commit;
				End if;

end if;
if ls_Action = 'DELETE'  then

		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Mpartnerproduct_Gid')))into @Mpartnerproduct_Gid;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Update_By')))into @Update_By;


		set Query_Update = concat('update atma_tmp_map_tpartnerproduct set update_date = CURRENT_TIMESTAMP,update_by=',@Update_By,',mpartnerproduct_isactive=''N'',mpartnerproduct_isremoved=''Y''
								where  mpartnerproduct_isactive=''Y'' and mpartnerproduct_isremoved=''N''
                           and mpartnerproduct_gid=',@Mpartnerproduct_Gid,'');

          # select  Query_Update;
		set @Query_Update = Query_Update;
		PREPARE stmt FROM @Query_Update;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'DELETED';
			commit;
		else
			set Message = ' FAILED';
			rollback;
		end if;

end if;
END