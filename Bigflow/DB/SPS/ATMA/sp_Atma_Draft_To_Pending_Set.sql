CREATE PROCEDURE `sp_Atma_Draft_To_Pending_Set`(in li_Action  varchar(40),
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_Atma_Draft_To_Pending_Set:BEGIN
### Abi
declare Query_Insert varchar(1000);
Declare countRow varchar(6000);
declare Query_Update varchar(1000);
declare Query_Value varchar(1000);
declare Query_Column varchar(1000);
Declare errno int;
Declare msg varchar(1000);

						DECLARE EXIT HANDLER FOR SQLEXCEPTION
						BEGIN
							GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
							set Message = concat(errno , msg);
							ROLLBACK;
						END;

IF li_Action='Draft_To_Pending_Insert' then



			START TRANSACTION;

		  select JSON_LENGTH(lj_filter,'$') into @lj_filter_json_count;
          select JSON_LENGTH(lj_classification,'$') into @li_classification_jsoncount;


				if @lj_filter_json_count = 0 or @lj_filter_json_count is null then
					set Message = 'No Data In filter Json. ';
					leave sp_Atma_Draft_To_Pending_Set;
				End if;

                if @li_classification_jsoncount = 0 or @li_classification_jsoncount = ''
					or @li_classification_jsoncount is null  then
						set Message = 'No Data In classification Json. ';
						leave sp_Atma_Draft_To_Pending_Set;
				End if;

          select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Gid')))
          into @Partner_Gid;
          select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Status')))
          into @Partner_Status;
          select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Remarks'))) into @Remarks;
          select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Create_By')))
          into @Create_By;
          select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Entity_Gid')))
          into @Entity_Gid;
          #####concat_remarks---requestfor
          select main_partner_gid from atma_tmp_tpartner where partner_gid=@Partner_Gid
          and partner_isactive='Y' and partner_isremoved='N' into @chk_main_gid;
          select partner_requestfor from atma_tmp_tpartner where partner_gid=@Partner_Gid and
          partner_isactive='Y' and partner_isremoved='N' into @requestfor;

          if @chk_main_gid is null then
          set @remark=CONCAT(ifnull(@Remarks,''),'-','ONBOARD');
          else
          set @remark=CONCAT(ifnull(@Remarks,''),'-',@requestfor);
          end if;

          set  @Partner_Gid1='';
          select partner_gid from atma_tmp_tpartner
          where partner_gid=@Partner_Gid  into @Partner_Gid1;

          set @Partner_Status1='';
          select partner_status from atma_tmp_tpartner
          where partner_gid=@Partner_Gid and (partner_status='DRAFT' or partner_status='REJECTED') into @Partner_Status1;



          select max(partner_code) from atma_tmp_tpartner
          where  partner_gid=@Partner_Gid into @ReftableCode;

        /*
          select max(taxdetails_gid) from atma_tmp_mst_ttaxdetails
          inner join atma_tmp_mst_tpartnerbranch on taxdetails_reftablecode=partnerbranch_code
            and partnerbranch_partnergid=@Partner_Gid into @Tax_Partner_Code;*/


          set  @Payment_PartnerGid='';
          select max(payment_partnergid) from atma_tmp_mst_tpayment
          where payment_partnergid=@Partner_Gid into @Payment_PartnerGid;


		  set  @Documents_PartnerGid='';
		  select max(documents_partnergid) from atma_tmp_trn_tdocuments
		  where documents_partnergid=@Partner_Gid into @Documents_PartnerGid;

          set  @Activity_PartnerGid='';
		  select max(activity_partnergid) from atma_tmp_mst_tactivity
		  where activity_partnergid=@Partner_Gid into @Activity_PartnerGid;


          select max(activity_gid) from atma_tmp_mst_tactivity
          where activity_partnergid=@Partner_Gid into @Activity_Gid;



          SELECT EXISTS(SELECT * FROM atma_tmp_mst_tactivity  a
          inner join atma_tmp_mst_tactivitydetails  b
		  on a.activity_gid=b.activitydetails_activitygid
          WHERE b.activitydetails_activitygid = @Activity_Gid) as activity_dtl  into @ActivityDetail;


		  set  @PartnerClient_PartnerGid='';
		  select max(partnerclient_partnergid) from atma_tmp_mst_tpartnerclient
		  where partnerclient_partnergid=@Partner_Gid into @PartnerClient_PartnerGid;

		  set  @PartnerContractor_PartnerGid='';
		  select max(partnercontractor_partnergid) from atma_tmp_mst_tpartnercontractor
		  where partnercontractor_partnergid=@Partner_Gid into @PartnerContractor_PartnerGid;

		  set @Partnerprofile_PartnerGid ='';
		  select max(partnerprofile_partnergid) from atma_tmp_mst_tpartnerprofile
		  where partnerprofile_partnergid=@Partner_Gid into @Partnerprofile_PartnerGid;

		  set @Partnerproduct_PartnerGid ='';
		  select max(partnerproduct_partnergid) from atma_tmp_mst_tpartnerproduct
		  where partnerproduct_partnergid=@Partner_Gid into @Partnerproduct_PartnerGid;

          set @Partnerbranch ='';
		  select  max(partnerbranch_partnergid) from atma_tmp_mst_tpartnerbranch
		  where partnerbranch_partnergid=@Partner_Gid into @Partnerbranch;

		  set @Partnercatalog ='';
		  select  max(mpartnerproduct_partner_gid) from atma_tmp_map_tpartnerproduct
          where mpartnerproduct_partner_gid=@Partner_Gid into @Partnercatalog;


			   if @Partner_Gid1 = '' or @Partner_Gid1 is null then
					set Message = 'Add Partner Details';
					leave sp_Atma_Draft_To_Pending_Set;
			   elseif @Partner_Status1 ='' or @Partner_Status1 is null then
					set Message = 'Partner Is Already Altered';
					leave sp_Atma_Draft_To_Pending_Set;
			   End if;

             /* select partner_compositevendor from atma_tmp_tpartner
              where partner_gid=@Partner_Gid into @partnercompositevendor ;

               if @partnercompositevendor='N' then

               select max(taxdetails_reftablecode) from atma_tmp_mst_ttaxdetails
			   inner join atma_tmp_mst_tpartnerbranch on taxdetails_reftablecode=partnerbranch_code
			   and partnerbranch_partnergid=@Partner_Gid into @Tax_Partner_Code;

				if @Tax_Partner_Code is null then
               set Message = 'Add Tax Details ';
               leave sp_Atma_Draft_To_Pending_Set;
               end if;

			   End if;*/



			   #if @Tax_Partner_Code = '' or @Tax_Partner_Code is null then
					#set Message = 'Add Tax Details ';
					#leave sp_Atma_Draft_To_Pending_Set;
			   #End if;

               if @Payment_PartnerGid = '' or @Payment_PartnerGid is null then
					set Message = 'Add Payment Details ';
					leave sp_Atma_Draft_To_Pending_Set;
			   End if;

               if @Documents_PartnerGid = '' or @Documents_PartnerGid is null then
					set Message = 'Add Document Details';
					leave sp_Atma_Draft_To_Pending_Set;
			   End if;

               if @Activity_PartnerGid = '' or @Activity_PartnerGid is null then
					set Message = 'Add Activity Details';
					leave sp_Atma_Draft_To_Pending_Set;
			   End if;


               if @ActivityDetail <> 1 or @ActivityDetail is null or @ActivityDetail='' then
					set Message = 'Add ActivityDetails';
					leave sp_Atma_Draft_To_Pending_Set;
			   End if;

                if   @PartnerClient_PartnerGid is null or @PartnerClient_PartnerGid='' then
					set Message = 'Add Client Details';
					leave sp_Atma_Draft_To_Pending_Set;
			   End if;

               if @PartnerContractor_PartnerGid = '' or @PartnerContractor_PartnerGid is null then
					set Message = 'Add PartnerContractor Details';
					leave sp_Atma_Draft_To_Pending_Set;
			   End if;

				if @Partnerprofile_PartnerGid = '' or @Partnerprofile_PartnerGid is null then
					set Message = 'Add profile Details ';
					leave sp_Atma_Draft_To_Pending_Set;
			    End if;

				if @Partnerproduct_PartnerGid = '' or @Partnerproduct_PartnerGid is null then
					set Message = 'Add Partnerproduct Details';
					leave sp_Atma_Draft_To_Pending_Set;
			    End if;

				if @Partnerbranch = '' or @Partnerbranch is null then
					set Message = 'Add Branch Details';
					leave sp_Atma_Draft_To_Pending_Set;
			    End if;

                if @Partnercatalog = '' or @Partnercatalog is null then
					set Message = 'Add Catalog Details';
					leave sp_Atma_Draft_To_Pending_Set;
			    End if;

			set Query_Update ='';

            set Query_Update = concat('Update  atma_tmp_tpartner
                         set partner_status=''',@Partner_Status,'''
						 Where partner_gid = ',@Partner_Gid,' and
                         partner_isactive=''Y''and
                         partner_isremoved=''N''
                         ');


			set @Query_Update = Query_Update;
			PREPARE stmt FROM @Query_Update;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;
		if countRow <= 0 then
				set Message = 'Error On Update.';
                rollback;
				leave sp_Atma_Draft_To_Pending_Set;

		elseif    countRow > 0 then

        select partner_rmname from atma_tmp_tpartner
        where partner_gid=@Partner_Gid into @RM_TO_tran;

  ####maker
  call sp_Trans_Set('DRAFT_TO_PENDING','PARTNER_NAME_TRAN',@Partner_Gid,
								 @Partner_Status,'I',@RM_TO_tran,@remark,
								 @Entity_Gid,@Create_By,@message);

				select @message into @out_msg_tran ;

				if @out_msg_tran = 'FAIL' then
					set Message = 'Failed On Tran Insert';
					rollback;
					leave sp_Atma_Draft_To_Pending_Set;


				End if;
                set Message = 'SUCCESS';
                commit;
              end if;



	ELSEIF li_Action='RM_To_VMU_Update' then

                START TRANSACTION;

			select JSON_LENGTH(lj_filter,'$') into @lj_filter_json_count;


				if @lj_filter_json_count = 0 or @lj_filter_json_count is null then
					set Message = 'No Data In filter Json. ';
					leave sp_Atma_Draft_To_Pending_Set;
				End if;



          select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Gid')))
          into @Partner_Gid;
          select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Status')))
          into @Partner_Status;
          select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.TRAN_Remarks')))
          into @TRAN_Remarks;
          select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Rolegroup_Name')))
          into @Rolegroup_Name;
          select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Create_By')))
          into @Create_By;
          select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Entity_Gid')))
          into @Entity_Gid;
         #####concat_remarks---requestfor
          select main_partner_gid from atma_tmp_tpartner where partner_gid=@Partner_Gid
          and partner_isactive='Y' and partner_isremoved='N' into @chk_main_gid;
          select partner_requestfor from atma_tmp_tpartner where partner_gid=@Partner_Gid and
          partner_isactive='Y' and partner_isremoved='N' into @requestfor;

          if @chk_main_gid is null then
          set @remark=CONCAT(ifnull(@TRAN_Remarks,''),'-','ONBOARD');
          else
          set @remark=CONCAT(ifnull(@TRAN_Remarks,''),'-',@requestfor);
          end if;



          set @Partner_Status1='';
          select partner_status from atma_tmp_tpartner
          where partner_gid=@Partner_Gid and (partner_status='PENDING-RM' or partner_status='REJECTED') into @Partner_Status1;


              if @Partner_Status1 =''or @Partner_Status1 is null then
					set Message = 'Partner Is Already Altered';
					leave sp_Atma_Draft_To_Pending_Set;
			  End if;


			set Query_Update ='';

            set Query_Update = concat('Update  atma_tmp_tpartner
                         set partner_status=''',@Partner_Status,'''
						 Where partner_gid = ',@Partner_Gid,' and
                         partner_isactive=''Y''and
                         partner_isremoved=''N''
                         ');


			set @Query_Update = Query_Update;
			PREPARE stmt FROM @Query_Update;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;

		if countRow <= 0 then
				set Message = 'Error On Update.';
                rollback;
				leave sp_Atma_Draft_To_Pending_Set;
		elseif    countRow > 0 then

 ######RM
      SET  @rolegroupgid='';
      SET   @rolegid='';
	#####REJECTED
      if @Partner_Status='REJECTED' then
      set @TO_TYPE ='C';
      else
      set @TO_TYPE ='G';
      END IF;
      ##### checking same name RM
	/*#select fn_REFGid('PARTNER_NAME_TRAN_MST') into @partner_ref_gid_mst;
		select fn_REFGid('PARTNER_NAME_TRAN') into @partner_ref_gid_tmp;
		select tran_from from gal_trn_ttran where
		tran_ref_gid=@partner_ref_gid_tmp and  tran_reftable_gid=@Partner_Gid into @checkingRM ;
		if @checkingRM=@Create_By then
		set Message = 'Change Rm Name';
        leave sp_Atma_Draft_To_Pending_Set;
		end if;*/

			select rolegroup_gid from gal_mst_trolegroup
			where rolegroup_name=@Rolegroup_Name into @rolegroupgid;
			select role_name from gal_mst_trole
			where role_rolegroup_gid=@rolegroupgid into @rolegid;

				call sp_Trans_Set('Update','PARTNER_NAME_TRAN',@Partner_Gid,
						@Partner_Status,@TO_TYPE,
						@rolegid,@remark,@Entity_Gid,@Create_By,@message);
				##ifnull(@remark,'')
				select @message into @out_msg_tran ;

				if @out_msg_tran = 'Not Updated' then
					set Message = 'Failed On Tran Update';
					rollback;
					leave sp_Atma_Draft_To_Pending_Set;

				End if;
		set Message = 'SUCCESS';
                commit;
		end if;


ELSEIF li_Action='VMU_To_VMUH_Update' then

			START TRANSACTION;

			select JSON_LENGTH(lj_filter,'$') into @lj_filter_json_count;


				if @lj_filter_json_count = 0 or @lj_filter_json_count is null then
					set Message = 'No Data In filter Json. ';
					leave sp_Atma_Draft_To_Pending_Set;
				End if;



          select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Gid')))
          into @Partner_Gid;
          select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Status')))
          into @Partner_Status;
          select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.TRAN_Remarks')))
          into @TRAN_Remarks;
		  select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Rolegroup_Name')))
          into @Rolegroup_Name;
		  select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Create_By')))
          into @Create_By;
          select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Entity_Gid')))
          into @Entity_Gid;

          set @Partner_Status1='';
          select partner_status from atma_tmp_tpartner
          where partner_gid=@Partner_Gid and (partner_status='PENDING-CHECKER' or partner_status='REJECTED') into @Partner_Status1;
         #####concat_remarks---requestfor
         select main_partner_gid from atma_tmp_tpartner where partner_gid=@Partner_Gid
          and partner_isactive='Y' and partner_isremoved='N' into @chk_main_gid;
          select partner_requestfor from atma_tmp_tpartner where partner_gid=@Partner_Gid and
          partner_isactive='Y' and partner_isremoved='N' into @requestfor;

          if @chk_main_gid is null then
          set @remark=CONCAT(ifnull(@TRAN_Remarks,''),'-','ONBOARD');
          else
          set @remark=CONCAT(ifnull(@TRAN_Remarks,''),'-',@requestfor);
          end if;


           #select 1;
              if @Partner_Status1 =''or @Partner_Status1 is null then
					set Message = 'Partner Is Already Altered';
					leave sp_Atma_Draft_To_Pending_Set;
			  End if;
         #######checking rights
     /*    select fn_REFGid('PARTNER_NAME_TRAN') into @partner_ref_gid_tmp;

        set @checker='';
		select max(tran_gid) from gal_trn_ttran where
		tran_ref_gid=@partner_ref_gid_tmp and tran_reftable_gid=@Partner_Gid
		and tran_status='PENDING-RM' into @trangid;
		#select @trangid,'trainid';
		select tran_by from gal_trn_ttran where tran_gid>=@trangid and
        tran_ref_gid=@partner_ref_gid_tmp and tran_reftable_gid=@Partner_Gid and tran_by=@Create_By
		into @checker;
        #select @checker,'more then rows';
		 #select JSON_LENGTH(lj_classification,'$.DirectorName') into @li_jsonpartner_name;
        #select ifnull(tran_by,0) from gal_trn_ttran where tran_gid in(@checker) INTO @TEST;
        #select  tran_by from gal_trn_ttran where tran_gid in(@checker);
    #select  @TEST;
        #if @checker=@Create_By then
       if @checker=@Create_By then
		set Message = 'NO RIGHTS';
        leave sp_Atma_Draft_To_Pending_Set;
		end if;


        ####checking rights end*/

			set Query_Update ='';

            set Query_Update = concat('Update  atma_tmp_tpartner
                         set partner_status=''',@Partner_Status,'''
						 Where partner_gid = ',@Partner_Gid,' and
                         partner_isactive=''Y''and
                         partner_isremoved=''N''
                         ');


			set @Query_Update = Query_Update;
			PREPARE stmt FROM @Query_Update;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;

		if countRow <= 0 then
				set Message = 'Error On Update.';
                rollback;
				leave sp_Atma_Draft_To_Pending_Set;
		elseif    countRow > 0 then


   ####HEAD
        select @rolegroupgid='';
        select @rolegid='';
    ##### REJECTED
	if @Partner_Status='REJECTED' then
      set @TO_TYPE ='C';
      else
      set @TO_TYPE ='G';
	END IF;

			select rolegroup_gid from gal_mst_trolegroup
			where rolegroup_name=@Rolegroup_Name into @rolegroupgid;
			select role_name from gal_mst_trole
			where role_rolegroup_gid=@rolegroupgid into @rolegid;


				call sp_Trans_Set('Update','PARTNER_NAME_TRAN',@Partner_Gid,
						@Partner_Status,@TO_TYPE,
						@rolegid,@remark,@Entity_Gid,@Create_By,@message);

				select @message into @out_msg_tran ;

				if @out_msg_tran = 'Not Updated' then
					set Message = 'Failed On Tran Update';
					rollback;
					leave sp_Atma_Draft_To_Pending_Set;

				End if;

                set Message = 'SUCCESS';
                commit;
		end if;

 ELSEIF li_Action='PENDING_HEAD' then

 START TRANSACTION;

			select JSON_LENGTH(lj_filter,'$') into @lj_filter_json_count;


				if @lj_filter_json_count = 0 or @lj_filter_json_count is null then
					set Message = 'No Data In filter Json. ';
					leave sp_Atma_Draft_To_Pending_Set;
				End if;



          select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Gid')))
          into @Partner_Gid;
          select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Status')))
          into @Partner_Status;
          select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.TRAN_Remarks')))
          into @TRAN_Remarks;
		  select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Rolegroup_Name')))
          into @Rolegroup_Name;
		  select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Create_By')))
          into @Create_By;
          select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Entity_Gid')))
          into @Entity_Gid;

          set @Partner_Status1='';
          select partner_status from atma_tmp_tpartner
          where partner_gid=@Partner_Gid and (partner_status='PENDING-HEAD' or partner_status='REJECTED') into @Partner_Status1;
         #####concat_remarks---requestfor
		  select main_partner_gid from atma_tmp_tpartner where partner_gid=@Partner_Gid
          and partner_isactive='Y' and partner_isremoved='N' into @chk_main_gid;
          select partner_requestfor from atma_tmp_tpartner where partner_gid=@Partner_Gid and
          partner_isactive='Y' and partner_isremoved='N' into @requestfor;

          if @chk_main_gid is null then
          set @remark=CONCAT(ifnull(@TRAN_Remarks,''),'-','ONBOARD');
          else
          set @remark=CONCAT(ifnull(@TRAN_Remarks,''),'-',@requestfor);
          end if;

              if @Partner_Status1 =''or @Partner_Status1 is null then
					set Message = 'Partner Is Already Altered';
					leave sp_Atma_Draft_To_Pending_Set;
			  End if;
                #select @Partner_Status1;
           #######checking head rights
		/*select fn_REFGid('PARTNER_NAME_TRAN') into @partner_ref_gid_tmp;

        set @checker='';
		select tran_by from gal_trn_ttran where
		tran_ref_gid=@partner_ref_gid_tmp and  tran_reftable_gid=@Partner_Gid and tran_by=@Create_By into @checker ;
         */
         select max(tran_gid) from gal_trn_ttran where
		tran_ref_gid=@partner_ref_gid_tmp and tran_reftable_gid=@Partner_Gid
		and tran_status='PENDING-HEAD' into @trangid;
       ###
        set @checker='';
		select tran_by from gal_trn_ttran where
		 tran_gid=@trangid into @checker ;
        if @checker=@Create_By then
		set Message = 'NO RIGHTS';
        #rollback;
        leave sp_Atma_Draft_To_Pending_Set;
		end if;
        ####checking rights end


			set Query_Update ='';

            set Query_Update = concat('Update  atma_tmp_tpartner
                         set partner_status=''',@Partner_Status,'''
						 Where partner_gid = ',@Partner_Gid,' and
                         partner_isactive=''Y''and
                         partner_isremoved=''N''
                         ');


			set @Query_Update = Query_Update;
			PREPARE stmt FROM @Query_Update;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;

		if countRow <= 0 then
				set Message = 'Error On Update.';
				rollback;
				leave sp_Atma_Draft_To_Pending_Set;
		elseif    countRow > 0 then


 #select @rolegroupgid='';
        #select @rolegid='';
    ##### REJECTED
	if @Partner_Status='REJECTED' then
      set @TO_TYPE ='C';
      else
      set @TO_TYPE ='G';
	END IF;

			select rolegroup_gid from gal_mst_trolegroup
			where rolegroup_name=@Rolegroup_Name into @rolegroupgid;
			select role_name from gal_mst_trole
			where role_rolegroup_gid=@rolegroupgid into @rolegid;


				call sp_Trans_Set('Update','PARTNER_NAME_TRAN',@Partner_Gid,
						@Partner_Status,@TO_TYPE,
						@rolegid,@remark,@Entity_Gid,@Create_By,@message);

				select @message into @out_msg_tran ;

				if @out_msg_tran = 'Not Updated' then
					set Message = 'Failed On Tran Update';
					rollback;
					leave sp_Atma_Draft_To_Pending_Set;
				End if;

 				set Message = 'SUCCESS';
                commit;
		end if;



	ELSEIF li_Action='APPROVER_TO_REQUEST' then

			START TRANSACTION;

			select JSON_LENGTH(lj_filter,'$') into @lj_filter_json_count;


				if @lj_filter_json_count = 0 or @lj_filter_json_count is null then
					set Message = 'No Data In filter Json. ';
					leave sp_Atma_Draft_To_Pending_Set;
				End if;


          select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Gid')))
          into @Partner_Gid;
          select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Status')))
          into @Partner_Status;


				if @Partner_Gid = '' or @Partner_Gid is null then
					set Message = 'Partner_Gid is not given. ';
					leave sp_Atma_Draft_To_Pending_Set;
				End if;

                if @Partner_Status = '' or @Partner_Status is null then
					set Message = 'Partner_Status is not given. ';
					leave sp_Atma_Draft_To_Pending_Set;
				End if;


                 set @Partner_Status1='';
          select partner_status from atma_mst_tpartner
          where partner_gid=@Partner_Gid and partner_status='APPROVED' into @Partner_Status1;
          select @Partner_Status1;

          select partner_status from atma_mst_tpartner
          where partner_gid=@Partner_Gid into @PR_Status;

              if @Partner_Status1 =''or @Partner_Status1 is null then
					set Message = concat('Already This Partner Is View By Some One ') ;
					leave sp_Atma_Draft_To_Pending_Set;
			  End if;


			set Query_Update ='';

            set Query_Update = concat('Update  atma_mst_tpartner
                         set partner_status=''',@Partner_Status,'''
						 Where partner_gid = ',@Partner_Gid,' and
                         partner_isactive=''Y''and
                         partner_isremoved=''N''
                         ');


			set @Query_Update = Query_Update;
			PREPARE stmt FROM @Query_Update;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;

		if countRow <= 0 then
				set Message = 'Error On Update.';
				rollback;
				leave sp_Atma_Draft_To_Pending_Set;
		elseif    countRow > 0 then
				set Message = 'SUCCESS';
                commit;
		end if;


	ELSEIF li_Action='VIEW_TO_APPROVED' then

			START TRANSACTION;

			select JSON_LENGTH(lj_filter,'$') into @lj_filter_json_count;


				if @lj_filter_json_count = 0 or @lj_filter_json_count is null then
					set Message = 'No Data In filter Json. ';
					leave sp_Atma_Draft_To_Pending_Set;
				End if;


          select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Gid')))
          into @Partner_Gid;
          select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Status')))
          into @Partner_Status;

				if @Partner_Gid = '' or @Partner_Gid is null then
					set Message = 'Partner_Gid is not given. ';
					leave sp_Atma_Draft_To_Pending_Set;
				End if;

                if @Partner_Status = '' or @Partner_Status is null then
					set Message = 'Partner_Status is not given. ';
					leave sp_Atma_Draft_To_Pending_Set;
				End if;



			set Query_Update ='';

            set Query_Update = concat('Update  atma_mst_tpartner
                         set partner_status=''',@Partner_Status,'''
						 Where partner_gid = ',@Partner_Gid,' and
                         partner_isactive=''Y''and
                         partner_isremoved=''N''
                         ');


			set @Query_Update = Query_Update;
			PREPARE stmt FROM @Query_Update;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;

		if countRow <= 0 then
				set Message = 'Error On Update.';
				rollback;
				leave sp_Atma_Draft_To_Pending_Set;
		elseif    countRow > 0 then
				set Message = 'SUCCESS';
                commit;
		end if;


END IF;


END