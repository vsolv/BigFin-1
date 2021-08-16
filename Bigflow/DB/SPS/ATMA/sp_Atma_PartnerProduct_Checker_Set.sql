CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_PartnerProduct_Checker_Set`(in ls_Action  varchar(16),
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_Atma_PartnerProduct_Checker_Set:BEGIN

#Balamaniraja      13-08-19

declare Query_Insert varchar(1000);
Declare countRow varchar(6000);
declare Query_Update varchar(1000);
Declare errno int;
Declare msg varchar(1000);

						DECLARE EXIT HANDLER FOR SQLEXCEPTION
						BEGIN
							GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
							set Message = concat(errno , msg);
							ROLLBACK;
						END;

 select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Mpartnerproduct_Status')))into @Mpartnerproduct_Status;
 select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Mpartnerproduct_Gid')))into @Mpartnerproduct_Gid;
 select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Tran_Remarks')))into @Tran_Remarks;
 select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Entity_Gid')))into @Entity_Gid;
 select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Update_By')))into @Update_By;
 if @Mpartnerproduct_Status='APPROVED' then
  set ls_Action = 'APPROVED CATALOG';
elseif @Mpartnerproduct_Status='REJECTED' then
  set ls_Action = 'REJECTED CATALOG';
end if;
select ls_Action;

IF ls_Action = 'CHECKER_UPDATE'  then

		start transaction;

		select JSON_LENGTH(lj_filter,'$') into @li_jsoncount;
		select JSON_LENGTH(lj_classification,'$') into @li_classification_jsoncount;

			if @li_jsoncount = 0 or @li_jsoncount is null  then
				set Message = 'No Data In Json. ';
				leave sp_Atma_PartnerProduct_Checker_Set;
			End if;

			if @li_classification_jsoncount = 0 or @li_classification_jsoncount = ''
			or @li_classification_jsoncount is null  then
				set Message = 'No Entity_Gid In Json. ';
				leave sp_Atma_PartnerProduct_Checker_Set;
			End if;

		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.PartnerProduct_Gid')))into @PartnerProduct_Gid;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.PartnerProduct_Status')))into @PartnerProduct_Status;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Entity_Gid')))into @Entity_Gid;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Update_By')))into @Update_By;

				if @PartnerProduct_Status is null or @PartnerProduct_Status='' then
					set Message ='Partner_Product Status Is Not Given ';
					rollback;
					leave sp_Atma_PartnerProduct_Checker_Set;
				end if;

                if @Entity_Gid is null or @Entity_Gid='' then
					set Message ='Entity_Gid Is Not Given ';
					rollback;
					leave sp_Atma_PartnerProduct_Checker_Set;
				end if;

                if @Update_By is null or @Update_By='' then
					set Message ='Update_By Is Not Given ';
					rollback;
					leave sp_Atma_PartnerProduct_Checker_Set;
				end if;

		set Query_Update = '';

            if @PartnerProduct_Status is not null or @PartnerProduct_Status <> '' then
				    set Query_Update = concat(Query_Update, ',mpartnerproduct_status = ''',@PartnerProduct_Status,''' ');
			end if;

		select mpartnerproduct_status from atma_tmp_map_tpartnerproduct
		where mpartnerproduct_gid = @PartnerProduct_Gid into @Pr_Status;
        #select @Pr_Status;

           if @Pr_Status<>'Pending' then
			    set Message ='This Recod Is Already Altered ';
				rollback;
				leave sp_Atma_PartnerProduct_Checker_Set;
		   end if;


		set Query_Update = concat('Update  atma_tmp_map_tpartnerproduct
                         set update_date = CURRENT_TIMESTAMP,update_by=',@Update_By,'
                         ',Query_Update,'
						 Where mpartnerproduct_gid = ',@PartnerProduct_Gid,' and
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
				leave sp_Atma_PartnerProduct_Checker_Set;
		elseif    countRow > 0 then
				set Message = 'SUCCESSFULLY UPDATED';
		end if;


			 call sp_Trans_Set('update','PARTNER_NAME',@PartnerProduct_Gid,
             @PartnerProduct_Status,'I',
             'CHECKER','',@Entity_Gid,@Update_By,@message);

				select @message into @out_msg_tran ;

				if @out_msg_tran = 'Not Updated' then
					set Message = 'Failed On Tran Update';
					rollback;
					leave sp_Atma_PartnerProduct_Checker_Set;
				else
					commit;
				End if;




END IF;

if ls_Action = 'APPROVED CATALOG'  then

start transaction;

		select JSON_LENGTH(lj_filter,'$') into @li_filter_jsoncount;
		select JSON_LENGTH(lj_classification,'$') into @li_classification_jsoncount;

		if @li_filter_jsoncount = 0 or @li_filter_jsoncount is null  then
			set Message = 'No Data In Json. ';
			leave sp_Atma_PartnerProduct_Checker_Set;
		End if;

         if @li_classification_jsoncount = 0 or @li_classification_jsoncount = ''
            or @li_classification_jsoncount is null  then
			set Message = 'No Entity_Gid and Create by In Json. ';
			leave sp_Atma_PartnerProduct_Checker_Set;
		End if;




			#select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Tran_Remarks')))into @Tran_Remarks;
            #select 1;
			 select mpartnerproduct_partnerbranch_gid,mpartnerproduct_product_gid
            into @oldpartnerbranch_gid,@mpartnerproduct_product_gid  from atma_map_tpartnerproduct where
            mpartnerproduct_gid=@Mpartnerproduct_Gid;

            select mpartnerproduct_gid from atma_map_tpartnerproduct where
            mpartnerproduct_isactive='Y'AND mpartnerproduct_isremoved='N' AND
			mpartnerproduct_partnerbranch_gid=@oldpartnerbranch_gid and
			mpartnerproduct_product_gid=@mpartnerproduct_product_gid into @mpartnerproductgid;

            select @mpartnerproductgid;
            SET SQL_SAFE_UPDATES = 0;
			update atma_map_tpartnerproduct set
			mpartnerproduct_isactive='N',mpartnerproduct_isremoved='Y'
			where  mpartnerproduct_isactive='Y'AND mpartnerproduct_isremoved='N' AND
			mpartnerproduct_partnerbranch_gid=@oldpartnerbranch_gid and
			mpartnerproduct_product_gid=@mpartnerproduct_product_gid ;



set Query_Update = concat('update atma_map_tpartnerproduct set mpartnerproduct_status=''APPROVED'',
							update_date = CURRENT_TIMESTAMP,update_by=',@Update_By,',
							mpartnerproduct_isactive=''Y'',mpartnerproduct_isremoved=''N''
							where  mpartnerproduct_isactive=''N'' and mpartnerproduct_isremoved=''Y''
							and mpartnerproduct_gid=',@Mpartnerproduct_Gid,' and mpartnerproduct_status=''PENDING'' ');

           #select  Query_Update;
		set @Query_Update = Query_Update;
		PREPARE stmt FROM @Query_Update;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'SUCCESS';

            #select mpartnerproduct_gid from atma_map_tpartnerproduct where
            #mpartnerproduct_partnerbranch_gid= @oldpartnerbranch_gid and mpartnerproduct_isactive='N'
            #into @oldmpartnerproduct_gid;
            #select @oldpartnerbranch_gid;
            #select @oldmpartnerproduct_gid;
            #select @Mpartnerproduct_Gid;
SET SQL_SAFE_UPDATES = 0;
set Query_Update = concat(' update atma_map_tactivitydtlpproduct set
						  activitydtlpproduct_mpartnerproductgid=',@Mpartnerproduct_Gid,'
							where
							activitydtlpproduct_mpartnerproductgid=',@mpartnerproductgid,'');
							select Query_Update;
							set @Query_Update = Query_Update;
							PREPARE stmt FROM @Query_Update;
							EXECUTE stmt;
							set countRow = (select ROW_COUNT());
                            select countRow;
							DEALLOCATE PREPARE stmt;
							if countRow >  0 then
							set Message = 'SUCCESS';

               select partnerbranch_code from atma_mst_tpartnerbranch
               where partnerbranch_gid=@oldpartnerbranch_gid into @partnerbranchcode;
               select @partnerbranchcode;
				select supplier_gid from gal_mst_tsupplier where Supplier_code=@partnerbranchcode
                into  @suppliergid ;
               # select @suppliergid;

                select  mpartnerproduct_product_gid,mpartnerproduct_partnerbranch_gid,mpartnerproduct_unitprice,
                mpartnerproduct_packingprice, mpartnerproduct_validfrom, mpartnerproduct_validto,
                mpartnerproduct_deliverydays, mpartnerproduct_capacitypw, mpartnerproduct_dts
				into @mpartnerproduct_product_gid,@mpartnerproduct_partnerbranch_gid,@mpartnerproduct_unitprice,
				@mpartnerproduct_packingprice,@mpartnerproduct_validfrom,@mpartnerproduct_validto,@mpartnerproduct_deliverydays,
				@mpartnerproduct_capacitypw,@mpartnerproduct_dts
				from atma_map_tpartnerproduct where
				mpartnerproduct_gid=@Mpartnerproduct_Gid and mpartnerproduct_isactive='Y' and mpartnerproduct_isremoved='N';

		set Query_Update = concat(' update gal_map_tsupplierproduct set
							supplierproduct_isactive=''N'',supplierproduct_isremoved=''Y''
							where
							supplierproduct_supplier_gid=',@suppliergid,' and
                            supplierproduct_product_gid=',@mpartnerproduct_product_gid,' and
                            supplierproduct_isactive=''Y'' and supplierproduct_isremoved=''N'' ');
							#select Query_Update;
							set @Query_Update = Query_Update;
							PREPARE stmt FROM @Query_Update;
							EXECUTE stmt;
							set countRow = (select ROW_COUNT());
                            #select countRow;
							DEALLOCATE PREPARE stmt;
							if countRow >  0 then
							set Message = 'SUCCESS';
		set Query_Update = concat('INSERT INTO gal_map_tsupplierproduct (supplierproduct_supplier_gid,supplierproduct_product_gid,
									supplierproduct_unitprice,supplierproduct_packingprice,
									supplierproduct_validfrom, supplierproduct_validto, supplierproduct_deliverydays,
                                    supplierproduct_capacitypw,supplierproduct_dts,entity_gid,create_by,create_date)
							values (',@suppliergid,',',@mpartnerproduct_product_gid,',''',@mpartnerproduct_unitprice,''',
                            ''',@mpartnerproduct_packingprice,''',''',@mpartnerproduct_validfrom,''',''',@mpartnerproduct_validto,''',
							''',@mpartnerproduct_deliverydays,''',''',@mpartnerproduct_capacitypw,''',''',@mpartnerproduct_dts,''',
							',@Entity_Gid,',',@Update_By,',
							''',Now(),''')');
                            #select Query_Update;
                            set @Query_Update = Query_Update;
							PREPARE stmt FROM @Query_Update;
							EXECUTE stmt;
							set countRow = (select ROW_COUNT());
                            #select countRow;
							DEALLOCATE PREPARE stmt;
							if countRow >  0 then
							set Message = 'SUCCESS';
                            call sp_Trans_Set('update','PARTNER_NAME',@Mpartnerproduct_Gid,
							@Mpartnerproduct_Status,'C',
							'CHECKER',ifnull(@Tran_Remarks,''),@Entity_Gid,@Update_By,@message);

				select @message into @out_msg_tran ;
                select @out_msg_tran;
                if @out_msg_tran >  0 then
					set Message = 'SUCCESS';
					commit;
				else
					set Message = 'Failed On Tran Update';
					rollback;
					leave sp_Atma_PartnerProduct_Checker_Set;
				End if;

                            else
                            set Message = 'FAILED';
                            rollback;
                            end if;
						else
                            set Message = 'FAILED';
                            rollback;
                            end if;#### update gal_map_tsupplierproduct

					else
					set Message = ' FAILED';
					rollback;
					end if;

			else
			set Message = ' FAILED';
			rollback;
			end if;##update atma_map_tactivitydtlpproduct


end if;

if ls_Action = 'REJECTED CATALOG' then
set Query_Update='';
set Query_Update = concat('update atma_map_tpartnerproduct set mpartnerproduct_status=''',@Mpartnerproduct_Status,''',
							update_date = CURRENT_TIMESTAMP,update_by=',@Update_By,'
							where
                            mpartnerproduct_isactive=''N'' and mpartnerproduct_isremoved=''Y''and
							 mpartnerproduct_gid=',@Mpartnerproduct_Gid,'  ');


           select  Query_Update;
		set @Query_Update = Query_Update;
		PREPARE stmt FROM @Query_Update;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'SUCCESS';
            call sp_Trans_Set('update','PARTNER_NAME',@Mpartnerproduct_Gid,
							@Mpartnerproduct_Status,'C',
							'CHECKER',ifnull(@Tran_Remarks,''),@Entity_Gid,@Update_By,@message);

				select @message into @out_msg_tran ;
                select @out_msg_tran;
                if @out_msg_tran >  0 then
					set Message = 'SUCCESS';
					commit;
				else
					set Message = 'Failed On Tran Update';
					rollback;
					leave sp_Atma_PartnerProduct_Checker_Set;
				End if;

		else
			set Message = ' FAILED';
			rollback;
			end if;


end if;

END