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

END