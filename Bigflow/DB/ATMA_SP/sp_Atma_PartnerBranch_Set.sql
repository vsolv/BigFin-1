CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_PartnerBranch_Set`(in li_Action  varchar(30),
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_Atma_PartnerBranch_Set:BEGIN

#Balamaniraja       08-08-2019

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

IF li_Action='Atma_Branch_Insert' then

			START TRANSACTION;
		select JSON_LENGTH(lj_filter,'$') into @lj_filter_json_count;
		select JSON_LENGTH(lj_classification,'$') into @lj_classification_json_count;

        if @lj_classification_json_count = 0 or @lj_classification_json_count is null then
			set Message = 'No Data In classification Json. ';
			leave sp_Atma_PartnerBranch_Set;
		End if;

          select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Entity_Gid')))
          into @Entity_Gid;

          select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Create_By')))
          into @Create_By;

            #Address
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Address_1')))into @Address_1;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Address_2')))into @Address_2;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Address_3')))into @Address_3;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Address_Pincode')))into @Address_Pincode;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Address_District_Gid')))into @Address_District_Gid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Address_City_Gid')))into @Address_City_Gid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Address_State_Gid')))into @Address_State_Gid;
            #Contact
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_ContactType_Gid')))into @Contact_ContactType_Gid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_PersonName')))into @Contact_PersonName;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_Designation_Gid')))into @Contact_Designation_Gid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_LandLine')))into @Contact_LandLine;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_LandLine2')))into @Contact_LandLine2;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_MobileNo')))into @Contact_MobileNo;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_MobileNo2')))into @Contact_MobileNo2;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_Email')))into @Contact_Email;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_DOB')))into @Contact_DOB;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_WD')))into @Contact_WD;

            if  @Contact_DOB <> '' and @Contact_DOB <> 'null' then
				set @Contact_DOB=date_format(@Contact_DOB,'%Y-%m-%d');
			end if;
            if  @Contact_WD <> '' and @Contact_WD <> 'null' then
				set @Contact_WD=date_format(@Contact_WD,'%Y-%m-%d');
            end if;
            if  @Contact_DOB <> '' and @Contact_WD<>'' and @Contact_DOB <> 'null' and @Contact_WD <> 'null' then
				if @Contact_DOB  >= @Contact_WD then
					set Message ='Wedding date should be greater than Birth date ';
					rollback;
					leave sp_Atma_PartnerBranch_Set;
				end if;
            end if;
            #Partner_Branch
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.PartnerBranch_Code')))into @PartnerBranch_Code;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.PartnerBranch_Partner_Gid')))into @PartnerBranch_Partner_Gid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.PartnerBranch_Name')))into @PartnerBranch_Name;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.partnerbranch_gstno')))into @partnerbranch_gstno;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.partnerbranch_panno')))into @partnerbranch_panno;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.CreditLimit_Days')))into @CreditLimit_Days;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.CreditLimit_Terms')))into @CreditLimit_Terms;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.PartnerBranch_Remarks')))into @PartnerBranch_Remarks;
            ###auto code
            set @AT_partnerBranchcode='';

			select codesequence_no from gal_mst_tcodesequence where
			codesequence_type='partnerbranch_code' into @AT_partnerBranchcode;

			set @Branchcode = concat('SUPA',SUBSTRING(CONCAT('000',@AT_partnerBranchcode),-4));

			if  @Address_District_Gid = '' or @Address_District_Gid is null or @Address_District_Gid =0  then
				set Message = 'Address_District_Gid is not given ';
				leave sp_Atma_PartnerBranch_Set;
			End if;

            if  @Entity_Gid = '' or @Entity_Gid is null or @Entity_Gid =0  then
				set Message = 'Entity_Gid is not given ';
				leave sp_Atma_PartnerBranch_Set;
			End if;

            if  @Create_By = '' or @Create_By is null or @Create_By =0  then
				set Message = 'Create_By is not given ';
				leave sp_Atma_PartnerBranch_Set;
			End if;

            if  @Contact_ContactType_Gid = '' or @Contact_ContactType_Gid is null or @Contact_ContactType_Gid =0  then
				set Message = 'Contact_ContactType_Gid is not given ';
				leave sp_Atma_PartnerBranch_Set;
			End if;

            if  @Contact_Designation_Gid = '' or @Contact_Designation_Gid is null or @Contact_Designation_Gid =0  then
				set Message = 'Contact_Designation_Gid is not given ';
				leave sp_Atma_PartnerBranch_Set;
			End if;



	 set Query_Column='';
	 set Query_Value ='';

	if lower(@PartnerBranch_Remarks) <>'null' and  @PartnerBranch_Remarks <>'' then
		set Query_Column = concat(Query_Column,',partnerbranch_remarks');
		set Query_Value=concat(Query_Value,', ''',@PartnerBranch_Remarks,''' ');
	end if;
    if lower(@partnerbranch_gstno) <>'null' and  @partnerbranch_gstno <>'' then
		set Query_Column = concat(Query_Column,',partnerbranch_gstno');
		set Query_Value=concat(Query_Value,', ''',@partnerbranch_gstno,''' ');
	end if;
	if lower(@partnerbranch_panno) <>'null' and  @partnerbranch_panno <>'' then
		set Query_Column = concat(Query_Column,',partnerbranch_panno');
		set Query_Value=concat(Query_Value,', ''',@partnerbranch_panno,''' ');
	end if;


	set Query_Insert='';

	set Query_Insert=concat('insert into atma_tmp_mst_tpartnerbranch
									(partnerbranch_code,partnerbranch_partnergid,
                                    partnerbranch_name,partnerbranch_creditperiod,partnerbranch_paymentterms,
                                    entity_gid,create_by
                                    ',Query_Column,')
						      values(''',@Branchcode,''',',@PartnerBranch_Partner_Gid,
                              ',''',@PartnerBranch_Name,''',',@CreditLimit_Days,
                              ',''',@CreditLimit_Terms,''',',@Entity_Gid,',',@Create_By,'',Query_Value,')'
                    );


	set @Insert_query = Query_Insert;
	SELECT Query_Insert;
	PREPARE stmt FROM @Insert_query;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
    if countRow >  0 then
		set Message = 'SUCCESSFULLY INSERTED';
	else
		set Message = 'FAILED';
		rollback;
	end if;

    select LAST_INSERT_ID() into @PartnerBranch_Gid;

	set Query_Column='';
	set Query_Value ='';

	if lower(@Address_1) <> 'null' and @Address_1 <> '' then
	set Query_Column = concat(Query_Column,',address_1 ');
	set Query_Value=concat(Query_Value,', ''',@Address_1,''' ');
	end if;

	if lower(@Address_2) <>'null' and @Address_2 <> '' then
	set Query_Column = concat(Query_Column,',address_2 ');
	set Query_Value=concat(Query_Value,', ''',@Address_2,''' ');
	end if;

	if lower(@Address_3) <>'null' and @Address_3 <> '' then
	set Query_Column = concat(Query_Column,',address_3 ');
	set Query_Value=concat(Query_Value,', ''',@Address_3,''' ');
	end if;

	if lower(@Address_Pincode) <>'null' and @Address_Pincode <> '' then
		set Query_Column = concat(Query_Column,',address_pincode ');
		set Query_Value=concat(Query_Value,', ',@Address_Pincode,' ');
	end if;

	if @Address_City_Gid is not null and @Address_City_Gid <> '' then
		set Query_Column = concat(Query_Column,',address_city_gid ');
		set Query_Value=concat(Query_Value,', ',@Address_City_Gid,' ');
	end if;

	if @Address_State_Gid is not null and @Address_State_Gid <> '' then
		set Query_Column = concat(Query_Column,',address_state_gid ');
		set Query_Value=concat(Query_Value,', ',@Address_State_Gid,' ');
	end if;

     #set @Address_Ref_Code ='ADDCD123';
     select fn_REFCode('PARTNERBRANCH_ADDRESS') into @Address_Ref_Code;

     set Query_Insert='';

	 set Query_Insert=concat('insert into atma_tmp_mst_taddress(address_ref_code,
							address_district_gid,entity_gid,create_by',Query_Column,')
								values(''',@Address_Ref_Code,''',
                                ',@Address_District_Gid,',
                                ',@Entity_Gid,',',@Create_By,'',Query_Value,')'
							);

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

        select LAST_INSERT_ID() into @Address_Gid;


        set Query_Column='';
		set Query_Value ='';



	if lower(@Contact_PersonName) <> 'null' and  @Contact_PersonName <> '' then
		set Query_Column = concat(Query_Column,',Contact_personname');
		set Query_Value=concat(Query_Value,', ''',@Contact_PersonName,''' ');
	end if;

	if lower(@Contact_LandLine) <> 'null' and  @Contact_LandLine <> '' then
	set Query_Column = concat(Query_Column,',Contact_landline');
	set Query_Value=concat(Query_Value,', ',@Contact_LandLine,' ');
	end if;

	if lower(@Contact_LandLine2) <> 'null' and  @Contact_LandLine2 <> '' then
	set Query_Column = concat(Query_Column,',Contact_landline2');
	set Query_Value=concat(Query_Value,', ',@Contact_LandLine2,' ');
	end if;

	if lower(@Contact_MobileNo) <> 'null' and  @Contact_MobileNo <> '' then
	set Query_Column = concat(Query_Column,',Contact_mobileno');
	set Query_Value=concat(Query_Value,', ',@Contact_MobileNo,' ');
	end if;

	if lower(@Contact_MobileNo2) <> 'null' and  @Contact_MobileNo2 <> '' then
	set Query_Column = concat(Query_Column,',Contact_mobileno2');
	set Query_Value=concat(Query_Value,', ',@Contact_MobileNo2,' ');
	end if;

	if lower(@Contact_Email) <> 'null' and @Contact_Email <> '' then
		set Query_Column = concat(Query_Column,',Contact_Email');
		set Query_Value=concat(Query_Value,', ''',@Contact_Email,''' ');
	End if;

	if @Contact_DOB <> '' and @Contact_DOB <> 'null' then
		set Query_Column = concat(Query_Column,',Contact_DOB');
		set Query_Value=concat(Query_Value,', ''',@Contact_DOB,''' ');
	End if;
	if @Contact_WD <> '' and @Contact_WD <> 'null'  then
		set Query_Column = concat(Query_Column,',Contact_WD');
		set Query_Value=concat(Query_Value,', ''',@Contact_WD,''' ');
	End if;

    select fn_REFGid('PARTNERBRANCH_CONTACT') into @Contact_Ref_Gid ;

    select partnerbranch_code from atma_tmp_mst_tpartnerbranch where partnerbranch_gid=@PartnerBranch_Gid
    into @Contact_RefTableCode;

	set Query_Insert='';

	set Query_Insert=concat('insert into atma_tmp_mst_tcontact
									(Contact_ref_gid,Contact_reftable_gid,contact_reftablecode,
									 Contact_contacttype_gid,Contact_designation_gid,
                                     entity_gid,create_by',Query_Column,')
						      values(',@Contact_Ref_Gid,',',@PartnerBranch_Gid,',''',@Contact_RefTableCode,''',
									',@Contact_ContactType_Gid,',',@Contact_Designation_Gid,',
									',@Entity_Gid,',',@Create_By,'',Query_Value,')'
                    );

	set @Insert_query = Query_Insert;
	#SELECT Query_Insert;
	PREPARE stmt FROM @Insert_query;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
    if countRow >  0 then
		set Message = 'SUCCESSFULLY INSERTED';
	else
		set Message = 'FAILED';
		rollback;
	end if;

     select LAST_INSERT_ID() into @Contact_Gid;


				set Query_Update = concat('Update atma_tmp_mst_tpartnerbranch
										set partnerbranch_addressgid = ',@Address_Gid,' ,
										    partnerbranch_contactgid = ',@Contact_Gid,'
										    Where partnerbranch_gid = ',@PartnerBranch_Gid,'

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
				leave sp_Atma_PartnerBranch_Set;
			elseif    countRow > 0 then
				set Message = 'SUCCESS';

                Update gal_mst_tcodesequence
				set  codesequence_no= codesequence_no+1
				Where codesequence_type = 'partnerbranch_code';
				commit;
		    end if;




END IF;


IF li_Action='BRANCH_UPDATE' then

	START TRANSACTION;
	select JSON_LENGTH(lj_filter,'$') into @lj_jsoncount;
	select JSON_LENGTH(lj_classification,'$') into @lj_classification_json_count;


	if @lj_jsoncount = 0 or @lj_jsoncount is null
	or @lj_jsoncount = ''  then
		set Message = 'No Data In filter Json - Update.';
		leave sp_Atma_PartnerBranch_Set;
	End if;

	if @lj_classification_json_count = 0  or @lj_classification_json_count = ''
		   or @lj_classification_json_count is null  then
			set Message = 'No Data In classification Json - Update.';
			leave sp_Atma_PartnerBranch_Set;
	End if;

	if @lj_jsoncount is not null or @lj_jsoncount <> ''
           or @lj_jsoncount <> 0 then

        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.PartnerBranch_Gid')))
		into @PartnerBranch_Gid;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Address_1')))
		into @Address_1;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Address_2')))
		into @Address_2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Address_3')))
		into @Address_3;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Address_PinCode')))
		into @Address_PinCode;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Address_District_Gid')))into @Address_District_Gid;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Address_City_Gid')))into @Address_City_Gid;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Address_State_Gid')))into @Address_State_Gid;
		#Contact
		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_ContactType_Gid')))into @Contact_ContactType_Gid;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_PersonName')))into @Contact_PersonName;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_Designation_Gid')))into @Contact_Designation_Gid;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_LandLine')))into @Contact_LandLine;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_LandLine2')))into @Contact_LandLine2;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_MobileNo')))into @Contact_MobileNo;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_MobileNo2')))into @Contact_MobileNo2;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_Email')))into @Contact_Email;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_DOB')))into @Contact_DOB;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_WD')))into @Contact_WD;

	if  @Contact_DOB <> '' and lower(@Contact_DOB) <> 'null' then
			set @Contact_DOB=date_format(@Contact_DOB,'%Y-%m-%d');
	end if;
	if  @Contact_WD <> '' and lower(@Contact_WD) <> 'null' then
			set @Contact_WD=date_format(@Contact_WD,'%Y-%m-%d');
	end if;
	if  @Contact_DOB <> '' and @Contact_WD<>''  and lower(@Contact_DOB) <> 'null' and lower(@Contact_WD) <> 'null' then
		if @Contact_DOB  >= @Contact_WD then
			set Message ='Contact_WD date should be greater than Contact_DOB date ';
			rollback;
			leave sp_Atma_PartnerBranch_Set;
		end if;
	end if;
       # select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.PartnerBranch_Code')))into @PartnerBranch_Code;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.PartnerBranch_Name')))into @PartnerBranch_Name;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.partnerbranch_gstno')))into @partnerbranch_gstno;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.partnerbranch_panno')))into @partnerbranch_panno;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.CreditLimit_Days')))into @CreditLimit_Days;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.CreditLimit_Terms')))into @CreditLimit_Terms;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.PartnerBranch_Remarks')))into @PartnerBranch_Remarks;

		end if;

        if @lj_classification_json_count <> 0 OR @lj_classification_json_count <> ''
               or @lj_classification_json_count is NOT null  then

            select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Update_By')))
            into @Update_By;

		end if;

         if @Update_By = 0 or @Update_By = '' or @Update_By is null  then
				set Message ='Update_By  Is Not Given';
				rollback;
				leave sp_Atma_PartnerBranch_Set;
		 end if;


	set Query_Update ='';

	if lower(@Address_1) <>'null' and @Address_1 <> '' then
		set Query_Update = concat(Query_Update,',address_1 = ''',@Address_1,'''  ');
	else
		set Query_Update = concat(Query_Update,',address_1 = null  ');
	End if;

	if lower(@Address_2) <> 'null' and @Address_2 <> '' then
		set Query_Update = concat(Query_Update,',address_2 = ''',@Address_2,'''  ');
	else
		set Query_Update = concat(Query_Update,',address_2 = null  ');
	End if;

			if lower(@Address_3) <>'null' and @Address_3 <> '' then
				set Query_Update = concat(Query_Update,',address_3 = ''',@Address_3,'''  ');
			else
				set Query_Update = concat(Query_Update,',address_3 = null  ');
			End if;


            if lower(@Address_PinCode) <>'null' and @Address_PinCode <> '' then
				set Query_Update = concat(Query_Update,',address_pincode = ',@Address_PinCode,'  ');
			else
				set Query_Update = concat(Query_Update,',address_pincode = null  ');
			End if;


            if lower(@Address_District_Gid) <> 'null' and @Address_District_Gid <> '' then
				set Query_Update = concat(Query_Update,',address_district_gid = ',@Address_District_Gid,'  ');
            else
				set Message='Address_District can not be null' ;
				leave sp_Atma_PartnerBranch_Set;
			End if;

            if lower(@Address_City_Gid) <> 'null' and @Address_City_Gid <> '' then
				set Query_Update = concat(Query_Update,',address_city_gid = ',@Address_City_Gid,'  ');
			else
				set Message='Address_City can not be null' ;
				leave sp_Atma_PartnerBranch_Set;
			End if;

            if lower(@Address_State_Gid) <> 'null' and @Address_State_Gid <> '' then
				set Query_Update = concat(Query_Update,',address_state_gid = ',@Address_State_Gid,'  ');
			else
				set Message='Address_State can not be null' ;
				leave sp_Atma_PartnerBranch_Set;
			End if;

            if @Update_By is not null or @Update_By <> '' then
				set Query_Update = concat(Query_Update,',Update_By = ',@Update_By,'  ');
			End if;

            select partnerbranch_addressgid from atma_tmp_mst_tpartnerbranch
            where partnerbranch_gid=@PartnerBranch_Gid into @Address_Gid;


			set Query_Update = concat('Update atma_tmp_mst_taddress
										set update_date = CURRENT_TIMESTAMP ',Query_Update,'
										Where address_gid = ',@Address_Gid,'');
				#select Query_Update;
				set @Query_Update = Query_Update;
				PREPARE stmt FROM @Query_Update;
				EXECUTE stmt;
				set countRow = (select ROW_COUNT());
				DEALLOCATE PREPARE stmt;

			if countRow <= 0 then
				set Message = 'Error On Update.';
				rollback;
				leave sp_Atma_PartnerBranch_Set;
			elseif    countRow > 0 then
				set Message = 'SUCCESSFULLY UPDATED';
				commit;
		    end if;


            set Query_Update ='';


            if lower(@Contact_ContactType_Gid) <> 'null' and @Contact_ContactType_Gid <> '' then
				set Query_Update = concat(Query_Update,',Contact_contacttype_gid = ',@Contact_ContactType_Gid,'  ');
			else
                set Message='Contact_ContactType can not be null' ;
				leave sp_Atma_PartnerBranch_Set;
			End if;

            if lower(@Contact_PersonName) <> 'null' and @Contact_PersonName <> '' then
				set Query_Update = concat(Query_Update,',Contact_personname = ''',@Contact_PersonName,'''  ');
			else
				set Query_Update = concat(Query_Update,',Contact_personname = null  ');
			End if;

            if lower(@Contact_Designation_Gid) <> 'null' and @Contact_Designation_Gid <> '' then
				set Query_Update = concat(Query_Update,',Contact_designation_gid = ',@Contact_Designation_Gid,'  ');
			else
				set Message='Contact_Designation can not be null' ;
				leave sp_Atma_PartnerBranch_Set;
			End if;

            if lower(@Contact_LandLine) <> 'null' and @Contact_LandLine <> '' then
				set Query_Update = concat(Query_Update,',Contact_landline = ',@Contact_LandLine,'  ');
			else
				set Query_Update = concat(Query_Update,',Contact_landline = null  ');
			End if;

            if lower(@Contact_LandLine2) <> 'null' and @Contact_LandLine2 <> '' then
				set Query_Update = concat(Query_Update,',Contact_landline2 = ',@Contact_LandLine2,'  ');
			else
				set Query_Update = concat(Query_Update,',Contact_landline2 = null');
			End if;

            if lower(@Contact_MobileNo) <> 'null' and @Contact_MobileNo <> '' then
				set Query_Update = concat(Query_Update,',Contact_mobileno = ',@Contact_MobileNo,'  ');
			else
				set Query_Update = concat(Query_Update,',Contact_mobileno = null ');
			End if;


            if lower(@Contact_MobileNo2) <> 'null' and @Contact_MobileNo2 <> '' then
				set Query_Update = concat(Query_Update,',Contact_mobileno2 = ',@Contact_MobileNo2,'  ');
			else
				set Query_Update = concat(Query_Update,',Contact_mobileno2 = null  ');
			End if;

			if lower(@Contact_Email) <> 'null' and @Contact_Email <> '' then
				set Query_Update = concat(Query_Update,',contact_email = ''',@Contact_Email,'''  ');
			else
				set Query_Update = concat(Query_Update,',contact_email = null');
			End if;

            if @Contact_DOB <> '' and lower(@Contact_DOB) <> 'null' then
                set Query_Update = concat(Query_Update,',Contact_DOB =''',@Contact_DOB,'''');
			else
				set Query_Update = concat(Query_Update,',Contact_DOB =null');
			End if;
            if @Contact_WD <> '' and lower(@Contact_WD) <> 'null'  then
                set Query_Update = concat(Query_Update,',Contact_WD =''',@Contact_WD,'''');
			else
				set Query_Update = concat(Query_Update,',Contact_WD =null');
			End if;

            select partnerbranch_contactgid from atma_tmp_mst_tpartnerbranch
            where partnerbranch_gid=@PartnerBranch_Gid into @Contact_Gid;

			set Query_Update = concat('Update atma_tmp_mst_tcontact
										set update_date = CURRENT_TIMESTAMP ',Query_Update,'
										Where contact_gid = ',@Contact_Gid,'');
				#select Query_Update;
				set @Query_Update = Query_Update;
				PREPARE stmt FROM @Query_Update;
				EXECUTE stmt;
				set countRow = (select ROW_COUNT());
				DEALLOCATE PREPARE stmt;

			if countRow <= 0 then
				set Message = 'Error On Update.';
				rollback;
				leave sp_Atma_PartnerBranch_Set;
			elseif    countRow > 0 then
				set Message = 'SUCCESSFULLY UPDATED';
				commit;
		end if;


			set Query_Update ='';
			 if lower(@CreditLimit_Days) <>'null' and @CreditLimit_Days <> '' then
				set Query_Update = concat(Query_Update,',partnerbranch_creditperiod = ',@CreditLimit_Days,'  ');
			else
				set Query_Update = concat(Query_Update,',partnerbranch_creditperiod = 0  ');
			End if;

            if lower(@CreditLimit_Terms) <>'null' and @CreditLimit_Terms <> '' then
				set Query_Update = concat(Query_Update,',partnerbranch_paymentterms = ''',@CreditLimit_Terms,'''  ');
			else
				set Query_Update = concat(Query_Update,',partnerbranch_paymentterms = null  ');
			End if;
           # if lower(@PartnerBranch_Code) <> 'null' and @PartnerBranch_Code <> '' then
				#set Query_Update = concat(Query_Update,',partnerbranch_code = ''',@PartnerBranch_Code,'''  ');
			#else
				#set Message='PartnerBranch_Code can not be empty' ;
				#leave sp_Atma_PartnerBranch_Set;
			#End if;

            if lower(@PartnerBranch_Name) <> 'null' and @PartnerBranch_Name <> '' then
				set Query_Update = concat(Query_Update,',partnerbranch_name = ''',@PartnerBranch_Name,'''  ');
			else
				set Message='PartnerBranch_Name can not be empty' ;
				leave sp_Atma_PartnerBranch_Set;
			End if;

            if lower(@partnerbranch_gstno) <> 'null' and @partnerbranch_gstno <> '' then
				set Query_Update = concat(Query_Update,',partnerbranch_gstno = ''',@partnerbranch_gstno,'''  ');
			else
				set Query_Update = concat(Query_Update,',partnerbranch_gstno = ''''  ');
			End if;


            if lower(@partnerbranch_panno) <> 'null' and @partnerbranch_panno <> '' then
				set Query_Update = concat(Query_Update,',partnerbranch_panno = ''',@partnerbranch_panno,'''  ');
			else
				set Query_Update = concat(Query_Update,',partnerbranch_panno = ''''  ');
			End if;

            if lower(@PartnerBranch_Remarks) <> 'null' and @PartnerBranch_Remarks <> '' then
				set Query_Update = concat(Query_Update,',partnerbranch_remarks = ''',@PartnerBranch_Remarks,'''  ');
			else
				set Query_Update = concat(Query_Update,',partnerbranch_remarks = ''''  ');
			End if;


        set Query_Update = concat('Update atma_tmp_mst_tpartnerbranch
										set update_date = CURRENT_TIMESTAMP ',Query_Update,'
										Where partnerbranch_gid = ',@PartnerBranch_Gid,'');
				#select Query_Update;
				set @Query_Update = Query_Update;
				PREPARE stmt FROM @Query_Update;
				EXECUTE stmt;
				set countRow = (select ROW_COUNT());
				DEALLOCATE PREPARE stmt;

			if countRow <= 0 then
				set Message = 'Error On Update.';
				rollback;
				leave sp_Atma_PartnerBranch_Set;
			elseif    countRow > 0 then
				set Message = 'SUCCESSFULLY UPDATED';
				commit;
		end if;


END IF;


END