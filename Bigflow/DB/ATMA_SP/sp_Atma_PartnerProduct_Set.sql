CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_PartnerProduct_Set`(in li_Action  varchar(20),
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_ATMA_PartnerProduct_Set:BEGIN

#Balamaniraja       05-07-2019

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

IF li_Action='Atma_Product_Insert' then


			START TRANSACTION;

		select JSON_LENGTH(lj_filter,'$') into @lj_filter_json_count;
		select JSON_LENGTH(lj_classification,'$') into @lj_classification_json_count;


		if @lj_filter_json_count = 0 or @lj_filter_json_count is null then
			set Message = 'No Data In Filter Json. ';
			leave sp_ATMA_PartnerProduct_Set;
		End if;

		if @lj_classification_json_count = 0 or @lj_classification_json_count is null then
			set Message = 'No Data In classification Json. ';
			leave sp_ATMA_PartnerProduct_Set;
		End if;

          select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Entity_Gid')))
          into @Entity_Gid;
          select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Create_By')))
          into @Create_By;

        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_ContactType_Gid')))into @Client_Contact_ContactType_Gid;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_PersonName')))into @Client_Contact_PersonName;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_Designation_Gid')))into @Client_Contact_Designation_Gid;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_LandLine')))into @Client_Contact_LandLine;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_LandLine2')))into @Client_Contact_LandLine2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_MobileNo')))into @Client_Contact_MobileNo;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_MobileNo2')))into @Client_Contact_MobileNo2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_Email')))into @Client_Contact_Email;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_DOB')))into @Client_Contact_DOB;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_WD')))into @Client_Contact_WD;

       if  @Client_Contact_DOB <> '' and @Client_Contact_DOB <> 'null' then
			set @Client_Contact_DOB=date_format(@Client_Contact_DOB,'%Y-%m-%d');
		end if;
		if  @Client_Contact_WD <> '' and @Client_Contact_WD <> 'null' then
			set @Client_Contact_WD=date_format(@Client_Contact_WD,'%Y-%m-%d');
		end if;
		if  @Client_Contact_DOB <> '' and @Client_Contact_WD<>'' and @Client_Contact_DOB <> 'null' and @Client_Contact_WD <> 'null' then
			if @Client_Contact_DOB  >= @Client_Contact_WD then
				set Message ='Wedding date should be greater than Birth date ';
				rollback;
				leave sp_Atma_PartnerProduct_Set;
			end if;
		end if;

		set @Client_Contact_Ref_Gid=0;
		set @Client_Contact_RefTable_Gid=0;
		set @Client_Contact_RefTableCode=0;

		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_ContactType_Gid_2')))into @Client_Contact_ContactType_Gid_2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_PersonName_2')))into @Client_Contact_PersonName_2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_Designation_Gid_2')))into @Client_Contact_Designation_Gid_2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_LandLine_2')))into @Client_Contact_LandLine_2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_LandLine2_2')))into @Client_Contact_LandLine2_2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_MobileNo_2')))into @Client_Contact_MobileNo_2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_MobileNo2_2')))into @Client_Contact_MobileNo2_2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_Email_2')))into @Client_Contact_Email_2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_DOB_2')))into @Client_Contact_DOB_2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_WD_2')))into @Client_Contact_WD_2;

		if  @Client_Contact_DOB_2 <> '' and @Client_Contact_DOB_2 <> 'null' then
			set @Client_Contact_DOB_2=date_format(@Client_Contact_DOB_2,'%Y-%m-%d');
		end if;
		if  @Client_Contact_WD_2 <> '' and @Client_Contact_WD_2 <> 'null' then
			set @Client_Contact_WD_2=date_format(@Client_Contact_WD_2,'%Y-%m-%d');
		end if;
		if  @Client_Contact_DOB_2 <> '' and @Client_Contact_WD_2<>'' and @Client_Contact_DOB_2 <> 'null' and @Client_Contact_WD_2 <> 'null' then
			if @Client_Contact_DOB_2  >= @Client_Contact_WD_2 then
				set Message ='Wedding date should be greater than Birth date ';
				rollback;
				leave sp_Atma_PartnerProduct_Set;
			end if;
		end if;

        set @Client_Contact_Ref_Gid_2=0;
		set @Client_Contact_RefTable_Gid_2=0;
		set @Client_Contact_RefTableCode_2=0;

		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_ContactType_Gid')))into @Customer_Contact_ContactType_Gid;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_PersonName')))into @Customer_Contact_PersonName;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_Designation_Gid')))into @Customer_Contact_Designation_Gid;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_LandLine')))into @Customer_Contact_LandLine;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_LandLine2')))into @Customer_Contact_LandLine2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_MobileNo')))into @Customer_Contact_MobileNo;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_MobileNo2')))into @Customer_Contact_MobileNo2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_Email')))into @Customer_Contact_Email;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_DOB')))into @Customer_Contact_DOB;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_WD')))into @Customer_Contact_WD;

		if  @Customer_Contact_DOB <> '' and @Customer_Contact_DOB <> 'null' then
			set @Customer_Contact_DOB=date_format(@Customer_Contact_DOB,'%Y-%m-%d');
		end if;
		if  @Customer_Contact_WD <> '' and @Customer_Contact_WD <> 'null' then
			set @Customer_Contact_WD=date_format(@Customer_Contact_WD,'%Y-%m-%d');
		end if;
		if  @Customer_Contact_DOB <> '' and @Customer_Contact_WD<>'' and @Customer_Contact_DOB <> 'null' and @Customer_Contact_WD <> 'null' then
			if @Customer_Contact_DOB  >= @Customer_Contact_WD then
				set Message ='Wedding date should be greater than Birth date ';
				rollback;
				leave sp_Atma_PartnerProduct_Set;
			end if;
		end if;

		set @Customer_Contact_Ref_Gid=0;
		set @Customer_Contact_RefTable_Gid=0;
		set @Customer_Contact_RefTableCode=0;

		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_ContactType_Gid_2')))into @Customer_Contact_ContactType_Gid_2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_PersonName_2')))into @Customer_Contact_PersonName_2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_Designation_Gid_2')))into @Customer_Contact_Designation_Gid_2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_LandLine_2')))into @Customer_Contact_LandLine_2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_LandLine2_2')))into @Customer_Contact_LandLine2_2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_MobileNo_2')))into @Customer_Contact_MobileNo_2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_MobileNo2_2')))into @Customer_Contact_MobileNo2_2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_Email_2')))into @Customer_Contact_Email_2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_DOB_2')))into @Customer_Contact_DOB_2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_WD_2')))into @Customer_Contact_WD_2;

		#"PartnerProduct":
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.PartnerProduct_Type')))
        into @PartnerProduct_Type;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.PartnerProduct_Name')))
        into @PartnerProduct_Name;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.PartnerProduct_Age')))
        into @PartnerProduct_Age;

        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.PartnerProduct_Partner_Gid')))
        into @PartnerProduct_Partner_Gid;

		if  @Customer_Contact_DOB_2 <> '' and @Customer_Contact_DOB_2 <> 'null' then
			set @Customer_Contact_DOB_2=date_format(@Customer_Contact_DOB_2,'%Y-%m-%d');
		end if;
		if  @Customer_Contact_WD_2 <> '' and @Customer_Contact_WD_2 <> 'null' then
			set @Customer_Contact_WD_2=date_format(@Customer_Contact_WD_2,'%Y-%m-%d');
		end if;
		if  @Customer_Contact_DOB_2 <> '' and @Customer_Contact_WD_2<>'' and @Customer_Contact_DOB_2 <> 'null' and @Customer_Contact_WD_2 <> 'null' then
			if @Customer_Contact_DOB_2  >= @Customer_Contact_WD_2 then
				set Message ='Wedding date should be greater than Birth date ';
				rollback;
				leave sp_Atma_PartnerProduct_Set;
			end if;
		end if;

		set @Customer_Contact_Ref_Gid_2=0;
		set @Customer_Contact_RefTable_Gid_2=0;
		set @Customer_Contact_RefTableCode_2=0;



         if  @Client_Contact_ContactType_Gid = '' or @Client_Contact_ContactType_Gid is null or @Client_Contact_ContactType_Gid =0  then
				set Message = 'Client_Contact_ContactType Gid  is not given ';
				leave sp_Atma_PartnerProduct_Set;
			End if;

		if  @Client_Contact_Designation_Gid = '' or @Client_Contact_Designation_Gid is null or @Client_Contact_Designation_Gid =0  then
				set Message = 'Contact_designation_gid is not given ';
				leave sp_Atma_PartnerProduct_Set;
		End if;

        if  @Client_Contact_ContactType_Gid_2 = '' or @Client_Contact_ContactType_Gid_2 is null or @Client_Contact_ContactType_Gid_2 =0  then
				set Message = 'Client_Contact_ContactType_Gid is not given ';
				leave sp_Atma_PartnerProduct_Set;
			End if;

		if  @Client_Contact_Designation_Gid_2 = '' or @Client_Contact_Designation_Gid_2 is null or @Client_Contact_Designation_Gid_2 =0  then
				set Message = 'Client_Contact_Designation_Gid_2 is not given ';
				leave sp_Atma_PartnerProduct_Set;
		End if;

        if  @Customer_Contact_ContactType_Gid = '' or @Customer_Contact_ContactType_Gid is null or @Customer_Contact_ContactType_Gid =0  then
				set Message = 'Client_Contact_ContactType_Gid 2 is not given ';
				leave sp_Atma_PartnerProduct_Set;
			End if;

		if  @Customer_Contact_Designation_Gid = '' or @Customer_Contact_Designation_Gid is null or @Customer_Contact_Designation_Gid =0  then
				set Message = 'Customer_Contact_Designation_Gid is not given ';
				leave sp_Atma_PartnerProduct_Set;
		End if;

        if  @Customer_Contact_ContactType_Gid_2 = '' or @Customer_Contact_ContactType_Gid_2 is null or @Customer_Contact_ContactType_Gid_2 =0  then
				set Message = 'Customer_Contact_ContactType_Gid_2 is not given ';
				leave sp_Atma_PartnerProduct_Set;
			End if;

		if  @Customer_Contact_Designation_Gid_2 = '' or @Customer_Contact_Designation_Gid_2 is null or @Customer_Contact_Designation_Gid_2 =0  then
				set Message = 'Customer_Contact_Designation_Gid_2 is not given ';
				leave sp_Atma_PartnerProduct_Set;
		End if;

        set Query_Column='';
		set Query_Value ='';

            if @Client_Contact_RefTableCode is not null then
            set Query_Column = concat(Query_Column,',contact_reftablecode');
            set Query_Value=concat(Query_Value,', ''',@Client_Contact_RefTableCode,''' ');
            end if;

            if @Client_Contact_PersonName is not null then
            set Query_Column = concat(Query_Column,',Contact_personname');
            set Query_Value=concat(Query_Value,', ''',@Client_Contact_PersonName,''' ');
            end if;

            if @Client_Contact_LandLine is not null then
            set Query_Column = concat(Query_Column,',Contact_landline');
            set Query_Value=concat(Query_Value,', ',@Client_Contact_LandLine,' ');
            end if;

            if @Client_Contact_LandLine2 is not null then
            set Query_Column = concat(Query_Column,',Contact_landline2');
            set Query_Value=concat(Query_Value,', ',@Client_Contact_LandLine2,' ');
            else
            set Query_Column = concat(Query_Column,'');
            set Query_Value=concat(Query_Value);
            end if;

            if @Client_Contact_MobileNo is not null then
            set Query_Column = concat(Query_Column,',Contact_mobileno');
            set Query_Value=concat(Query_Value,', ',@Client_Contact_MobileNo,' ');
            end if;

			if @Client_Contact_MobileNo2 is not null then
            set Query_Column = concat(Query_Column,',Contact_mobileno2');
            set Query_Value=concat(Query_Value,', ''',@Client_Contact_MobileNo2,''' ');
            end if;

            if @Client_Contact_Email is not null then
            set Query_Column = concat(Query_Column,',Contact_email');
            set Query_Value=concat(Query_Value,', ''',@Client_Contact_Email,''' ');
            end if;
            if @Client_Contact_DOB <> '' and @Client_Contact_DOB <> 'null' then
				set Query_Column = concat(Query_Column,',Contact_DOB');
				set Query_Value=concat(Query_Value,', ''',@Client_Contact_DOB,''' ');
            end if;

            if @Client_Contact_WD <> '' and @Client_Contact_WD <> 'null' then
            set Query_Column = concat(Query_Column,',Contact_WD');
            set Query_Value=concat(Query_Value,', ''',@Client_Contact_WD,''' ');
            end if;


	set Query_Insert='';

	set Query_Insert=concat('insert into atma_tmp_mst_tcontact
									(Contact_ref_gid,Contact_reftable_gid,
									Contact_contacttype_gid,Contact_designation_gid,
                                    entity_gid,create_by',Query_Column,')
						 values(',@Client_Contact_Ref_Gid,',',@Client_Contact_RefTable_Gid,',
								',@Client_Contact_ContactType_Gid,',',@Client_Contact_Designation_Gid,',
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
        leave sp_Atma_PartnerProduct_Set;
	end if;

    select last_insert_id() into @Client_Contact_Gid;
    #select @Client_Contact_Gid,1;
    set @Client_Contact_Gid_2='';
    set @Customer_Contact_Gid_2='';

      if @Client_Contact_ContactType_Gid_2 is not null or  @Client_Contact_ContactType_Gid_2<>'' then

		set Query_Column='';
		set Query_Value ='';

            if @Client_Contact_RefTableCode_2 is not null then
				set Query_Column = concat(Query_Column,',contact_reftablecode');
				set Query_Value=concat(Query_Value,', ''',@Client_Contact_RefTableCode_2,''' ');
            end if;

            if @Client_Contact_PersonName_2 is not null then
				set Query_Column = concat(Query_Column,',Contact_personname');
				set Query_Value=concat(Query_Value,', ''',@Client_Contact_PersonName_2,''' ');
            end if;

            if @Client_Contact_LandLine_2 is not null then
            set Query_Column = concat(Query_Column,',Contact_landline');
            set Query_Value=concat(Query_Value,', ',@Client_Contact_LandLine_2,' ');
            end if;

            if @Client_Contact_LandLine2_2 is not null then
            set Query_Column = concat(Query_Column,',Contact_landline2');
            set Query_Value=concat(Query_Value,', ',@Client_Contact_LandLine2_2,' ');
            end if;

            if @Client_Contact_MobileNo_2 is not null then
            set Query_Column = concat(Query_Column,',Contact_mobileno');
            set Query_Value=concat(Query_Value,', ',@Client_Contact_MobileNo_2,' ');
            end if;

			if @Client_Contact_MobileNo2_2 is not null then
            set Query_Column = concat(Query_Column,',Contact_mobileno2');
            set Query_Value=concat(Query_Value,', ''',@Client_Contact_MobileNo2_2,''' ');
            end if;

            if @Client_Contact_Email_2 is not null then
            set Query_Column = concat(Query_Column,',Contact_email');
            set Query_Value=concat(Query_Value,', ''',@Client_Contact_Email_2,''' ');
            end if;

            if @Client_Contact_DOB_2 <> '' and @Client_Contact_DOB_2 <> 'null' then
            set Query_Column = concat(Query_Column,',Contact_DOB');
            set Query_Value=concat(Query_Value,', ''',@Client_Contact_DOB_2,''' ');
            end if;

            if @Client_Contact_WD_2 <> '' and @Client_Contact_WD_2 <> 'null' then
				set Query_Column = concat(Query_Column,',Contact_WD');
				set Query_Value=concat(Query_Value,', ''',@Client_Contact_WD_2,''' ');
            end if;



        set Query_Insert='';

		set Query_Insert=concat('insert into atma_tmp_mst_tcontact
								 (Contact_ref_gid,Contact_reftable_gid,
								 Contact_contacttype_gid,Contact_designation_gid,
								 entity_gid,create_by',Query_Column,')
						     values(',@Client_Contact_Ref_Gid_2,',',@Client_Contact_RefTable_Gid_2,',
								',@Client_Contact_ContactType_Gid_2,',',@Client_Contact_Designation_Gid_2,',
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
        leave sp_Atma_PartnerProduct_Set;
	end if;

    select last_insert_id() into @Client_Contact_Gid_2;
    #select @Client_Contact_Gid_2,2;
    END IF;



		set Query_Column='';
		set Query_Value ='';

            if @Customer_Contact_RefTableCode is not null then
            set Query_Column = concat(Query_Column,',contact_reftablecode');
            set Query_Value=concat(Query_Value,', ''',@Customer_Contact_RefTableCode,''' ');
            end if;

            if @Customer_Contact_PersonName is not null then
            set Query_Column = concat(Query_Column,',Contact_personname');
            set Query_Value=concat(Query_Value,', ''',@Customer_Contact_PersonName,''' ');
            end if;

            if @Customer_Contact_LandLine is not null then
            set Query_Column = concat(Query_Column,',Contact_landline');
            set Query_Value=concat(Query_Value,', ',@Customer_Contact_LandLine,' ');
            end if;

            if @Customer_Contact_LandLine2 is not null then
            set Query_Column = concat(Query_Column,',Contact_landline2');
            set Query_Value=concat(Query_Value,', ',@Customer_Contact_LandLine2,' ');
            end if;

            if @Customer_Contact_MobileNo is not null then
            set Query_Column = concat(Query_Column,',Contact_mobileno');
            set Query_Value=concat(Query_Value,', ',@Customer_Contact_MobileNo,' ');
            end if;

			if @Customer_Contact_MobileNo2 is not null then
            set Query_Column = concat(Query_Column,',Contact_mobileno2');
            set Query_Value=concat(Query_Value,', ''',@Customer_Contact_MobileNo2,''' ');
            end if;

            if @Customer_Contact_Email is not null then
            set Query_Column = concat(Query_Column,',Contact_email');
            set Query_Value=concat(Query_Value,', ''',@Customer_Contact_Email,''' ');
            end if;

            if @Customer_Contact_DOB <> '' and @Customer_Contact_DOB <> 'null' then
            set Query_Column = concat(Query_Column,',Contact_DOB');
            set Query_Value=concat(Query_Value,', ''',@Customer_Contact_DOB,''' ');
            end if;

            if @Customer_Contact_WD <> '' and @Customer_Contact_WD <> 'null' then
            set Query_Column = concat(Query_Column,',Contact_WD');
            set Query_Value=concat(Query_Value,', ''',@Customer_Contact_WD,''' ');
            end if;

		set Query_Insert='';

		set Query_Insert=concat('insert into atma_tmp_mst_tcontact
									(Contact_ref_gid,Contact_reftable_gid,
									Contact_contacttype_gid,Contact_designation_gid,
                                    entity_gid,create_by',Query_Column,')
						 values(',@Customer_Contact_Ref_Gid,',',@Customer_Contact_RefTable_Gid,',
								',@Customer_Contact_ContactType_Gid,',',@Customer_Contact_Designation_Gid,',
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
        leave sp_Atma_PartnerProduct_Set;
	end if;

    select last_insert_id() into @Customer_Contact_Gid;
    #select @Customer_Contact_Gid,3;

      if @Customer_Contact_ContactType_Gid_2 is not null or @Customer_Contact_ContactType_Gid_2<>'' then

		set Query_Column='';
		set Query_Value ='';

            if @Customer_Contact_RefTableCode_2 is not null then
            set Query_Column = concat(Query_Column,',contact_reftablecode');
            set Query_Value=concat(Query_Value,', ''',@Customer_Contact_RefTableCode_2,''' ');
            end if;

            if @Customer_Contact_PersonName_2 is not null then
            set Query_Column = concat(Query_Column,',Contact_personname');
            set Query_Value=concat(Query_Value,', ''',@Customer_Contact_PersonName_2,''' ');
            end if;

            if @Customer_Contact_LandLine_2 is not null then
            set Query_Column = concat(Query_Column,',Contact_landline');
            set Query_Value=concat(Query_Value,', ',@Customer_Contact_LandLine_2,' ');
            end if;

            if @Customer_Contact_LandLine2_2 is not null then
            set Query_Column = concat(Query_Column,',Contact_landline2');
            set Query_Value=concat(Query_Value,', ',@Customer_Contact_LandLine2_2,' ');
            end if;

            if @Customer_Contact_MobileNo_2 is not null then
            set Query_Column = concat(Query_Column,',Contact_mobileno');
            set Query_Value=concat(Query_Value,', ',@Customer_Contact_MobileNo_2,' ');
            end if;

			if @Customer_Contact_MobileNo2_2 is not null then
            set Query_Column = concat(Query_Column,',Contact_mobileno2');
            set Query_Value=concat(Query_Value,', ''',@Customer_Contact_MobileNo2_2,''' ');
            end if;

            if @Customer_Contact_Email_2 is not null then
            set Query_Column = concat(Query_Column,',Contact_email');
            set Query_Value=concat(Query_Value,', ''',@Customer_Contact_Email_2,''' ');
            end if;

            if @Customer_Contact_DOB_2 <> '' and @Customer_Contact_DOB_2 <> 'null' then
            set Query_Column = concat(Query_Column,',Contact_DOB');
            set Query_Value=concat(Query_Value,', ''',@Customer_Contact_DOB_2,''' ');
            end if;

            if @Customer_Contact_WD_2 <> '' and @Customer_Contact_WD_2 <> 'null' then
            set Query_Column = concat(Query_Column,',Contact_WD');
            set Query_Value=concat(Query_Value,', ''',@Customer_Contact_WD_2,''' ');
            end if;

		set Query_Insert='';

		set Query_Insert=concat('insert into atma_tmp_mst_tcontact
									(Contact_ref_gid,Contact_reftable_gid,
									 Contact_contacttype_gid,Contact_designation_gid,
                                     entity_gid,create_by',Query_Column,')
								values(',@Customer_Contact_Ref_Gid_2,',',@Customer_Contact_RefTable_Gid_2,',
								',@Customer_Contact_ContactType_Gid_2,',',@Customer_Contact_Designation_Gid_2,',
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
        leave sp_Atma_PartnerProduct_Set;
	end if;
    select last_insert_id() into @Customer_Contact_Gid_2;
    #select @Customer_Contact_Gid_2,4;
	END IF;







			    set Query_Column='';
				set Query_Value='';

			if @PartnerProduct_Age is not null then
				set Query_Column = concat(Query_Column,',partnerproduct_age');
				set Query_Value=concat(Query_Value,', ',@PartnerProduct_Age,' ');
            else
				set Query_Column = concat(Query_Column,'');
				set Query_Value=concat(Query_Value);
            end if;

			if @Client_Contact_Gid_2 <> '' then
				set Query_Column = concat(Query_Column,',partnerproduct_clientcontactgid2');
				set Query_Value=concat(Query_Value,', ',@Client_Contact_Gid_2,' ');
            elseif @Client_Contact_Gid_2 is null or @Client_Contact_Gid_2 ='' then
				set Query_Column = concat(Query_Column);
				set Query_Value=concat(Query_Value);
            end if;

			if   @Customer_Contact_Gid_2 <> '' then
				set Query_Column = concat(Query_Column,',partnerproduct_customercontactgid2');
				set Query_Value=concat(Query_Value,', ',@Customer_Contact_Gid_2,' ');
			elseif @Client_Contact_Gid_2 is null or @Client_Contact_Gid_2='' then
				set Query_Column = concat(Query_Column);
				set Query_Value=concat(Query_Value);
            end if;

    #select Query_Column;
    #select Query_Value;
    	set Query_Insert='';
		set Query_Insert=concat('insert into atma_tmp_mst_tpartnerproduct
										(partnerproduct_partnergid,partnerproduct_type,
										partnerproduct_name,partnerproduct_clientcontactgid1,
										partnerproduct_customercontactgid1,
										entity_gid,create_by
										',Query_Column,')
								values(',@PartnerProduct_Partner_Gid,',''',@PartnerProduct_Type,''',
										''',@PartnerProduct_Name,''',',@Client_Contact_Gid,',
										',@Customer_Contact_Gid,',',@Entity_Gid,',
										',@Create_By,'',Query_Value,')'
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
        leave sp_Atma_PartnerProduct_Set;
	end if;
    select last_insert_id() into @Lst_insrt_partnerproduct_Gid;

            set Query_Value='';

			if @Client_Contact_Gid is not null or @Client_Contact_Gid <>'' then
				set Query_Value=concat(Query_Value,' ',@Client_Contact_Gid,' ');
            end if;

            if  @Client_Contact_Gid_2 <>'' then
				set Query_Value=concat(Query_Value,', ',@Client_Contact_Gid_2,' ');
            else
				set Query_Value=concat(Query_Value);
            end if;

            if @Customer_Contact_Gid is not null or @Customer_Contact_Gid <>'' then
				set Query_Value=concat(Query_Value,', ',@Customer_Contact_Gid,' ');
            end if;

            if  @Customer_Contact_Gid_2 <>'' then
				set Query_Value=concat(Query_Value,', ',@Customer_Contact_Gid_2,' ');
            else
				set Query_Value=concat(Query_Value);
            end if;

            select partner_code from  atma_tmp_tpartner
            where partner_gid=@PartnerProduct_Partner_Gid into @Contact_ReftableCode;


		set Query_Update='';

		set Query_Update = concat('Update atma_tmp_mst_tcontact
									set Contact_reftable_gid = ',@Lst_insrt_partnerproduct_Gid,',
                                    contact_reftablecode = ''',@Contact_ReftableCode,'''
									Where contact_gid in (',Query_Value,')');
                                    #contact_reftablecode=',,'

				#select Query_Update;
				set @Query_Update = Query_Update;
				PREPARE stmt FROM @Query_Update;
				EXECUTE stmt;
				set countRow = (select ROW_COUNT());
				DEALLOCATE PREPARE stmt;

			if countRow <= 0 then
				set Message = 'Error On Update.';
				rollback;
				leave sp_Atma_PartnerProduct_Set;
			elseif    countRow > 0 then
				set Message = 'SUCCESSFULLY UPDATED';
		    end if;

            set Query_Value='';

			if @Client_Contact_Gid is not null or @Client_Contact_Gid <>'' then
				set Query_Value=concat(Query_Value,' ',@Client_Contact_Gid,' ');
            end if;


            if @Client_Contact_ContactType_Gid_2 is not null or @Client_Contact_ContactType_Gid_2 <>'' then
				set Query_Value=concat(Query_Value,', ',@Client_Contact_Gid_2,' ');
            else
				set Query_Value=concat(Query_Value);
            end if;

            select fn_REFGid('CLIENT_CONTACT_PARTNERPRODUCT') into @Contact_Ref_Gid;

		set Query_Update='';

		set Query_Update = concat('Update atma_tmp_mst_tcontact
									set Contact_ref_gid = ',@Contact_Ref_Gid,'
									Where contact_gid in (',Query_Value,')');
                                    #contact_reftablecode=',,'

				#select Query_Update;
				set @Query_Update = Query_Update;
				PREPARE stmt FROM @Query_Update;
				EXECUTE stmt;
				set countRow = (select ROW_COUNT());
				DEALLOCATE PREPARE stmt;

			if countRow <= 0 then
				set Message = 'Error On Update.';
				rollback;
				leave sp_Atma_PartnerProduct_Set;
			elseif    countRow > 0 then
				set Message = 'SUCCESSFULLY UPDATED';
		    end if;

            set Query_Value='';

			if @Customer_Contact_Gid is not null or @Customer_Contact_Gid <>'' then
				set Query_Value=concat(Query_Value,' ',@Customer_Contact_Gid,' ');
            end if;

            if @Customer_Contact_ContactType_Gid_2 is not null or @Customer_Contact_ContactType_Gid_2 <>'' then
				set Query_Value=concat(Query_Value,', ',@Customer_Contact_Gid_2,' ');
            else
				set Query_Value=concat(Query_Value);
            end if;

            select fn_REFGid('CUST_CONTACT_PARTNERPRODUCT') into @Contact_Ref_Gid;

		set Query_Update='';

		set Query_Update = concat('Update atma_tmp_mst_tcontact
									set Contact_ref_gid = ',@Contact_Ref_Gid,'
									Where contact_gid in (',Query_Value,')');
                                    #contact_reftablecode=',,'

				#select Query_Update;
				set @Query_Update = Query_Update;
				PREPARE stmt FROM @Query_Update;
				EXECUTE stmt;
				set countRow = (select ROW_COUNT());
				DEALLOCATE PREPARE stmt;

			if countRow <= 0 then
				set Message = 'Error On Update.';
				rollback;
				leave sp_Atma_PartnerProduct_Set;
			elseif    countRow > 0 then
				set Message = 'SUCCESS';
                commit;
		    end if;




END IF;

IF li_Action='PRODUCT_UPDATE' then

	select JSON_LENGTH(lj_filter,'$') into @lj_jsoncount;
	select JSON_LENGTH(lj_classification,'$') into @lj_classification_json_count;
	if @lj_jsoncount = 0 or @lj_jsoncount is null
		or @lj_jsoncount = ''  then
			set Message = 'No Data In filter Json - Update.';
			leave sp_Atma_PartnerProduct_Set;
	End if;
	if @lj_classification_json_count = 0  or @lj_classification_json_count = ''
		   or @lj_classification_json_count is null  then
			set Message = 'No Data In classification Json - Update.';
			leave sp_Atma_PartnerProduct_Set;
	End if;
	if @lj_jsoncount is not null or @lj_jsoncount <> '' or @lj_jsoncount <> 0 then
		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.PartnerProduct_Gid')))	into @PartnerProduct_Gid;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_ContactType_Gid')))into @Client_Contact_ContactType_Gid;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_PersonName')))into @Client_Contact_PersonName;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_Designation_Gid')))into @Client_Contact_Designation_Gid;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_LandLine')))into @Client_Contact_LandLine;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_LandLine2')))into @Client_Contact_LandLine2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_MobileNo')))into @Client_Contact_MobileNo;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_MobileNo2')))into @Client_Contact_MobileNo2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_Email')))into @Client_Contact_Email;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_DOB')))into @Client_Contact_DOB;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_WD')))into @Client_Contact_WD;

        if  @Client_Contact_DOB <> '' and @Client_Contact_DOB <> 'null' then
			set @Client_Contact_DOB=date_format(@Client_Contact_DOB,'%Y-%m-%d');
		end if;
		if  @Client_Contact_WD <> '' and @Client_Contact_WD <> 'null' then
			set @Client_Contact_WD=date_format(@Client_Contact_WD,'%Y-%m-%d');
		end if;
		if  @Client_Contact_DOB <> '' and @Client_Contact_WD<>'' and @Client_Contact_DOB <> 'null' and @Client_Contact_WD <> 'null' then
			if @Client_Contact_DOB  >= @Client_Contact_WD then
				set Message ='Wedding date should be greater than Birth date ';
				rollback;
				leave sp_Atma_PartnerProduct_Set;
			end if;
		end if;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_ContactType_Gid_2')))into @Client_Contact_ContactType_Gid_2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_PersonName_2')))into @Client_Contact_PersonName_2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_Designation_Gid_2')))into @Client_Contact_Designation_Gid_2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_LandLine_2')))into @Client_Contact_LandLine_2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_LandLine2_2')))into @Client_Contact_LandLine2_2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_MobileNo_2')))into @Client_Contact_MobileNo_2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_MobileNo2_2')))into @Client_Contact_MobileNo2_2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_Email_2')))into @Client_Contact_Email_2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_DOB_2')))into @Client_Contact_DOB_2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Client_Contact_WD_2')))into @Client_Contact_WD_2;
		if  @Client_Contact_DOB_2 <> '' and @Client_Contact_DOB_2 <> 'null' then
			set @Client_Contact_DOB_2=date_format(@Client_Contact_DOB_2,'%Y-%m-%d');
		end if;
		if  @Client_Contact_WD_2 <> '' and @Client_Contact_WD_2 <> 'null' then
			set @Client_Contact_WD_2=date_format(@Client_Contact_WD_2,'%Y-%m-%d');
		end if;
		if  @Client_Contact_DOB_2 <> '' and @Client_Contact_WD_2<>'' and @Client_Contact_DOB_2 <> 'null' and @Client_Contact_WD_2 <> 'null' then
			if @Client_Contact_DOB_2  >= @Client_Contact_WD_2 then
				set Message ='Wedding date should be greater than Birth date ';
				rollback;
				leave sp_Atma_PartnerProduct_Set;
			end if;
		end if;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_ContactType_Gid')))into @Customer_Contact_ContactType_Gid;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_PersonName')))into @Customer_Contact_PersonName;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_Designation_Gid')))into @Customer_Contact_Designation_Gid;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_LandLine')))into @Customer_Contact_LandLine;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_LandLine2')))into @Customer_Contact_LandLine2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_MobileNo')))into @Customer_Contact_MobileNo;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_MobileNo2')))into @Customer_Contact_MobileNo2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_Email')))into @Customer_Contact_Email;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_DOB')))into @Customer_Contact_DOB;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_WD')))into @Customer_Contact_WD;

        if  @Customer_Contact_DOB <> '' and @Customer_Contact_DOB <> 'null' then
			set @Customer_Contact_DOB=date_format(@Customer_Contact_DOB,'%Y-%m-%d');
		end if;
		if  @Customer_Contact_WD <> '' and @Customer_Contact_WD <> 'null' then
			set @Customer_Contact_WD=date_format(@Customer_Contact_WD,'%Y-%m-%d');
		end if;
		if  @Customer_Contact_DOB <> '' and @Customer_Contact_WD<>'' and @Customer_Contact_DOB <> 'null' and @Customer_Contact_WD <> 'null' then
			if @Customer_Contact_DOB  >= @Customer_Contact_WD then
				set Message ='Wedding date should be greater than Birth date ';
				rollback;
				leave sp_Atma_PartnerProduct_Set;
			end if;
		end if;
	end if;

	if @lj_classification_json_count <> 0 OR @lj_classification_json_count <> '' or @lj_classification_json_count is NOT null  then
		select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Update_By')))
		into @Update_By;
	end if;
	if @Update_By = 0 or @Update_By = '' or @Update_By is null  then
		set Message ='Update_By Gid Is Not Given';
		rollback;
		leave sp_Atma_PartnerProduct_Set;
	end if;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_ContactType_Gid_2')))into @Customer_Contact_ContactType_Gid_2;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_PersonName_2')))into @Customer_Contact_PersonName_2;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_Designation_Gid_2')))into @Customer_Contact_Designation_Gid_2;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_LandLine_2')))into @Customer_Contact_LandLine_2;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_LandLine2_2')))into @Customer_Contact_LandLine2_2;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_MobileNo_2')))into @Customer_Contact_MobileNo_2;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_MobileNo2_2')))into @Customer_Contact_MobileNo2_2;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_Email_2')))into @Customer_Contact_Email_2;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_DOB_2')))into @Customer_Contact_DOB_2;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Customer_Contact_WD_2')))into @Customer_Contact_WD_2;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.PartnerProduct_Type'))) into @PartnerProduct_Type;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.PartnerProduct_Name'))) into @PartnerProduct_Name;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.PartnerProduct_Age'))) into @PartnerProduct_Age;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.PartnerProduct_Partner_Gid'))) into @PartnerProduct_Partner_Gid;

	if  @Customer_Contact_DOB_2 <> '' and @Customer_Contact_DOB_2 <> 'null' then
		set @Customer_Contact_DOB_2=date_format(@Customer_Contact_DOB_2,'%Y-%m-%d');
	end if;
	if  @Customer_Contact_WD_2 <> '' and @Customer_Contact_WD_2 <> 'null' then
		set @Customer_Contact_WD_2=date_format(@Customer_Contact_WD_2,'%Y-%m-%d');
	end if;
	if  @Customer_Contact_DOB_2 <> '' and @Customer_Contact_WD_2<>'' and @Customer_Contact_DOB_2 <> 'null' and @Customer_Contact_WD_2 <> 'null' then
		if @Customer_Contact_DOB_2  >= @Customer_Contact_WD_2 then
			set Message ='Wedding date should be greater than Birth date ';
			rollback;
			leave sp_Atma_PartnerProduct_Set;
		end if;
	end if;

	set Query_Update ='';

	if @Client_Contact_ContactType_Gid is null or @Client_Contact_ContactType_Gid = '' or @Client_Contact_ContactType_Gid = 'null' then
		set Message='Client_Contact_ContactType_Gid can not be null' ;
		leave sp_Atma_PartnerProduct_Set;
	else
		set Query_Update = concat(Query_Update,',Contact_contacttype_gid = ''',@Client_Contact_ContactType_Gid,'''  ');
	End if;

	if @Client_Contact_PersonName is null or @Client_Contact_PersonName = '' or @Client_Contact_PersonName = 'null' then
		set Query_Update = concat(Query_Update,',Contact_personname = null ');
	else
		set Query_Update = concat(Query_Update,',Contact_personname = ''',@Client_Contact_PersonName,'''  ');
	End if;

	if @Client_Contact_Designation_Gid is null or @Client_Contact_Designation_Gid = '' or @Client_Contact_Designation_Gid = 'null' then
		set Message='Contact_Designation_Gid can not be null' ;
		leave sp_Atma_PartnerProduct_Set;
	else
		set Query_Update = concat(Query_Update,',Contact_designation_gid = ''',@Client_Contact_Designation_Gid,'''  ');
    End if;

	if @Client_Contact_LandLine is null or @Client_Contact_LandLine = '' or @Client_Contact_LandLine = 'null' then
		set Query_Update = concat(Query_Update,',Contact_landline = null ');
	else
		set Query_Update = concat(Query_Update,',Contact_landline = ''',@Client_Contact_LandLine,'''  ');
	End if;

	if @Client_Contact_LandLine2 is null or @Client_Contact_LandLine2 = '' or @Client_Contact_LandLine2 = 'null' then
		set Query_Update = concat(Query_Update,',Contact_landline2 = null ');
	else
		set Query_Update = concat(Query_Update,',Contact_landline2 = ''',@Client_Contact_LandLine2,'''  ');
	End if;

	if @Client_Contact_MobileNo is null or @Client_Contact_MobileNo = '' or @Client_Contact_MobileNo = 'null' then
		set Query_Update = concat(Query_Update,',Contact_mobileno = null ');
	else
		set Query_Update = concat(Query_Update,',Contact_mobileno = ''',@Client_Contact_MobileNo,'''  ');
	End if;

	if @Client_Contact_MobileNo2 is null or @Client_Contact_MobileNo2 = '' or @Client_Contact_MobileNo2 = 'null' then
		set Query_Update = concat(Query_Update,',Contact_mobileno2 =null ');
	else
		set Query_Update = concat(Query_Update,',Contact_mobileno2 = ''',@Client_Contact_MobileNo2,'''  ');
	End if;

	if @Client_Contact_Email is null or @Client_Contact_Email = '' or @Client_Contact_Email = 'null' then
		set Query_Update = concat(Query_Update,',Contact_email =null ');
	else
		set Query_Update = concat(Query_Update,',Contact_email = ''',@Client_Contact_Email,'''  ');
	End if;

	if @Client_Contact_DOB is null or @Client_Contact_DOB = '' or  @Client_Contact_DOB = 'null' then
		set Query_Update = concat(Query_Update,',Contact_DOB = null ');
	else
		set Query_Update = concat(Query_Update,',Contact_DOB = ''',@Client_Contact_DOB,'''  ');
	End if;
	if @Client_Contact_WD is null or @Client_Contact_WD = '' or  @Client_Contact_WD = 'null' then
		set Query_Update = concat(Query_Update,',Contact_WD = null ');
	else
		set Query_Update = concat(Query_Update,',Contact_WD = ''',@Client_Contact_WD,'''  ');
	End if;

	select partnerproduct_clientcontactgid1 from atma_tmp_mst_tpartnerproduct
	where partnerproduct_gid=@PartnerProduct_Gid into @Contact_Gid1;

	set Query_Update = concat('Update atma_tmp_mst_tcontact
							set update_date = CURRENT_TIMESTAMP ,update_by=',@Update_By,'
							',Query_Update,'
							Where contact_gid = ',@Contact_Gid1,'');
	#select Query_Update;
	set @Query_Update = Query_Update;
	PREPARE stmt FROM @Query_Update;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;

	if countRow <= 0 then
		set Message = 'Error On Update.';
		rollback;
		leave sp_Atma_PartnerProduct_Set;
	elseif    countRow > 0 then
		set Message = 'SUCCESSFULLY UPDATED';
		commit;
	end if;

	set Query_Update ='';

	if @Client_Contact_ContactType_Gid_2 is null or @Client_Contact_ContactType_Gid_2 = '' or @Client_Contact_ContactType_Gid_2 = 'null' then
		set Message='Client_Contact_ContactType_Gid_2 can not be null' ;
		leave sp_Atma_PartnerProduct_Set;
    else
		set Query_Update = concat(Query_Update,',Contact_contacttype_gid = ''',@Client_Contact_ContactType_Gid_2,'''  ');
	End if;

	if @Client_Contact_PersonName_2 is null or @Client_Contact_PersonName_2 = '' or @Client_Contact_PersonName_2 = 'null' then
		set Query_Update = concat(Query_Update,',Contact_personname =null ');
    else
		set Query_Update = concat(Query_Update,',Contact_personname = ''',@Client_Contact_PersonName_2,'''  ');
	End if;

	if @Client_Contact_Designation_Gid_2 is null or @Client_Contact_Designation_Gid_2 = ''  or @Client_Contact_Designation_Gid_2 = 'null' then
		set Message='Client_Contact_Designation_Gid_2 can not be null' ;
		leave sp_Atma_PartnerProduct_Set;
	else
		set Query_Update = concat(Query_Update,',Contact_designation_gid = ''',@Client_Contact_Designation_Gid_2,'''  ');
	End if;
	if @Client_Contact_LandLine_2 is null or @Client_Contact_LandLine_2 = '' or @Client_Contact_LandLine_2 = 'null' then
		set Query_Update = concat(Query_Update,',Contact_landline =null ');
	else
		set Query_Update = concat(Query_Update,',Contact_landline = ''',@Client_Contact_LandLine_2,'''  ');
	End if;

	if @Client_Contact_LandLine2_2 is null or @Client_Contact_LandLine2_2 = '' or @Client_Contact_LandLine2_2 = 'null' then
		set Query_Update = concat(Query_Update,',Contact_landline2 = null ');
	else
		set Query_Update = concat(Query_Update,',Contact_landline2 = ''',@Client_Contact_LandLine2_2,'''  ');
	End if;

	if @Client_Contact_MobileNo_2 is null or @Client_Contact_MobileNo_2 = '' or @Client_Contact_MobileNo_2 = 'null' then
		set Query_Update = concat(Query_Update,',Contact_mobileno = null ');
	else
		set Query_Update = concat(Query_Update,',Contact_mobileno = ''',@Client_Contact_MobileNo_2,'''  ');
	End if;

	if @Client_Contact_MobileNo2_2 is null or @Client_Contact_MobileNo2_2 = '' or @Client_Contact_MobileNo2_2 = 'null' then
		set Query_Update = concat(Query_Update,',Contact_mobileno2 =null ');
	else
		set Query_Update = concat(Query_Update,',Contact_mobileno2 = ''',@Client_Contact_MobileNo2_2,'''  ');
	End if;

	if @Client_Contact_Email_2 is null or @Client_Contact_Email_2 = '' or @Client_Contact_Email_2 = 'null' then
		set Query_Update = concat(Query_Update,',Contact_email =null ');
	else
		set Query_Update = concat(Query_Update,',Contact_email = ''',@Client_Contact_Email_2,'''  ');
	End if;

	if @Client_Contact_DOB_2 is null or @Client_Contact_DOB_2 = '' or  @Client_Contact_DOB_2 = 'null' then
		set Query_Update = concat(Query_Update,',Contact_DOB = null ');
	else
		set Query_Update = concat(Query_Update,',Contact_DOB = ''',@Client_Contact_DOB_2,'''  ');
	End if;
	if @Client_Contact_WD_2 is null or @Client_Contact_WD_2 = '' or  @Client_Contact_WD_2 = 'null' then
		set Query_Update = concat(Query_Update,',Contact_WD = null ');
	else
		set Query_Update = concat(Query_Update,',Contact_WD = ''',@Client_Contact_WD_2,'''  ');
	End if;

	select partnerproduct_clientcontactgid2 from atma_tmp_mst_tpartnerproduct
	where partnerproduct_gid=@PartnerProduct_Gid into @Contact_Gid2;

	set Query_Update = concat('Update atma_tmp_mst_tcontact
								set update_date = CURRENT_TIMESTAMP,update_by=',@Update_By,'
								',Query_Update,'
								Where contact_gid = ',@Contact_Gid2,'');
	#select Query_Update;
	set @Query_Update = Query_Update;
	PREPARE stmt FROM @Query_Update;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;

	if countRow <= 0 then
		set Message = 'Error On Update.';
		rollback;
		leave sp_Atma_PartnerProduct_Set;
	elseif    countRow > 0 then
		set Message = 'SUCCESSFULLY UPDATED';
		commit;
	end if;

	set Query_Update ='';

	if @Customer_Contact_ContactType_Gid is null or @Customer_Contact_ContactType_Gid = '' or @Customer_Contact_ContactType_Gid = 'null' then
		set Message='Customer_Contact_ContactType_Gid can not be null' ;
		leave sp_Atma_PartnerProduct_Set;
	else
		set Query_Update = concat(Query_Update,',Contact_contacttype_gid = ''',@Customer_Contact_ContactType_Gid,'''  ');
    End if;

	if @Customer_Contact_PersonName is null or @Customer_Contact_PersonName = '' or @Customer_Contact_PersonName = 'null' then
		set Query_Update = concat(Query_Update,',Contact_personname =null ');
	else
		set Query_Update = concat(Query_Update,',Contact_personname = ''',@Customer_Contact_PersonName,'''  ');
	End if;

	if @Customer_Contact_Designation_Gid is null or @Customer_Contact_Designation_Gid = '' or @Customer_Contact_Designation_Gid = 'null' then
		set Message='Customer_Contact_Designation_Gid can not be null' ;
		leave sp_Atma_PartnerProduct_Set;
    else
		set Query_Update = concat(Query_Update,',Contact_designation_gid = ''',@Customer_Contact_Designation_Gid,'''  ');
	End if;

	if @Customer_Contact_LandLine is null or @Customer_Contact_LandLine = '' or @Customer_Contact_LandLine = 'null' then
		set Query_Update = concat(Query_Update,',Contact_LandLine = null ');
	else
		set Query_Update = concat(Query_Update,',Contact_landline = ''',@Customer_Contact_LandLine,'''  ');
	End if;

	if @Customer_Contact_LandLine2 is null or @Customer_Contact_LandLine2 = '' or @Customer_Contact_LandLine2 = 'null' then
		set Query_Update = concat(Query_Update,',Contact_landline2 =null ');
	else
		set Query_Update = concat(Query_Update,',Contact_landline2 = ''',@Customer_Contact_LandLine2,'''  ');
	End if;

	if @Customer_Contact_MobileNo is null or @Customer_Contact_MobileNo = '' or @Customer_Contact_MobileNo = 'null' then
		set Query_Update = concat(Query_Update,',Contact_mobileno =null ');
	else
		set Query_Update = concat(Query_Update,',Contact_mobileno = ''',@Customer_Contact_MobileNo,'''  ');
	End if;

	if @Customer_Contact_MobileNo2 is null or @Customer_Contact_MobileNo2 = '' or @Customer_Contact_MobileNo2 = 'null' then
		set Query_Update = concat(Query_Update,',Contact_mobileno2 =null ');
	else
		set Query_Update = concat(Query_Update,',Contact_mobileno2 = ''',@Customer_Contact_MobileNo2,'''  ');
	End if;

	if @Customer_Contact_Email is null or @Customer_Contact_Email = ''  or @Customer_Contact_Email = 'null' then
		set Query_Update = concat(Query_Update,',Contact_email = null ');
	else
		set Query_Update = concat(Query_Update,',Contact_email = ''',@Customer_Contact_Email,'''  ');
	End if;

	if @Customer_Contact_DOB is null or @Customer_Contact_DOB = '' or  @Customer_Contact_DOB = 'null' then
		set Query_Update = concat(Query_Update,',Contact_DOB = null ');
	else
		set Query_Update = concat(Query_Update,',Contact_DOB = ''',@Customer_Contact_DOB,'''  ');
	End if;
	if @Customer_Contact_WD is null or @Customer_Contact_WD = '' or  @Customer_Contact_WD = 'null' then
		set Query_Update = concat(Query_Update,',Contact_WD = null ');
	else
		set Query_Update = concat(Query_Update,',Contact_WD = ''',@Customer_Contact_WD,'''  ');
	End if;

	select partnerproduct_customercontactgid1 from atma_tmp_mst_tpartnerproduct
	where partnerproduct_gid=@PartnerProduct_Gid into @Contact_Gid3;

	set Query_Update = concat('Update atma_tmp_mst_tcontact
								set update_date = CURRENT_TIMESTAMP ,update_by=',@Update_By,'
								',Query_Update,'
								Where contact_gid = ',@Contact_Gid3,'');
	#select Query_Update;
	set @Query_Update = Query_Update;
	PREPARE stmt FROM @Query_Update;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;

	if countRow <= 0 then
		set Message = 'Error On Update.';
		rollback;
		leave sp_Atma_PartnerProduct_Set;
	elseif    countRow > 0 then
		set Message = 'SUCCESSFULLY UPDATED';
		commit;
	end if;

	set Query_Update ='';

	if @Customer_Contact_ContactType_Gid_2 is null or @Customer_Contact_ContactType_Gid_2 = ''  or @Customer_Contact_ContactType_Gid_2 = 'null' then
		set Message='Contact_ContactType_Gid can not be null' ;
		leave sp_Atma_PartnerProduct_Set;
	else
		set Query_Update = concat(Query_Update,',Contact_contacttype_gid = ''',@Customer_Contact_ContactType_Gid_2,'''  ');
	End if;
	if @Customer_Contact_PersonName_2 is null or @Customer_Contact_PersonName_2 = '' or @Customer_Contact_PersonName_2 = 'null' then
		set Query_Update = concat(Query_Update,',Contact_PersonName = null ');
	else
		set Query_Update = concat(Query_Update,',Contact_personname = ''',@Customer_Contact_PersonName_2,'''  ');
	End if;
	if @Customer_Contact_Designation_Gid_2 is null or @Customer_Contact_Designation_Gid_2 = '' or @Customer_Contact_Designation_Gid_2 = 'null' then
		set Message='Contact_Designation_Gid can not be null' ;
		leave sp_Atma_PartnerProduct_Set;
	else
		set Query_Update = concat(Query_Update,',Contact_designation_gid = ''',@Customer_Contact_Designation_Gid_2,'''  ');
	End if;
	if @Customer_Contact_LandLine_2 is null or @Customer_Contact_LandLine_2 = '' or @Customer_Contact_LandLine_2 = 'null' then
		set Query_Update = concat(Query_Update,',Contact_LandLine = null ');
	else
		set Query_Update = concat(Query_Update,',Contact_landline = ''',@Customer_Contact_LandLine_2,'''  ');
	End if;
	if @Customer_Contact_LandLine2_2 is null or @Customer_Contact_LandLine2_2 = ''  or @Customer_Contact_LandLine2_2 = 'null' then
		set Query_Update = concat(Query_Update,',Contact_LandLine2 = null ');
	else
		set Query_Update = concat(Query_Update,',Contact_landline2 = ''',@Customer_Contact_LandLine2_2,'''  ');
	End if;
	if @Customer_Contact_MobileNo_2 is null or @Customer_Contact_MobileNo_2 = ''  or @Customer_Contact_MobileNo_2 = 'null' then
		set Query_Update = concat(Query_Update,',Contact_mobileno = null ');
	else
		set Query_Update = concat(Query_Update,',Contact_mobileno = ''',@Customer_Contact_MobileNo_2,'''  ');
	End if;
	if @Customer_Contact_MobileNo2_2 is null or @Customer_Contact_MobileNo2_2 = ''  or @Customer_Contact_MobileNo2_2 = 'null' then
		set Query_Update = concat(Query_Update,',Contact_mobileno2 = null ');
	else
		set Query_Update = concat(Query_Update,',Contact_mobileno2 = ''',@Customer_Contact_MobileNo2_2,'''  ');
	End if;
	if @Customer_Contact_Email_2 is null or @Customer_Contact_Email_2 = '' or @Customer_Contact_Email_2 = 'null' then
		set Query_Update = concat(Query_Update,',Contact_email = null ');
	else
		set Query_Update = concat(Query_Update,',Contact_email = ''',@Customer_Contact_Email_2,'''  ');
	End if;
	if @Customer_Contact_DOB_2 is null or @Customer_Contact_DOB_2 = '' or  @Customer_Contact_DOB_2 = 'null' then
		set Query_Update = concat(Query_Update,',Contact_DOB = null ');
	else
		set Query_Update = concat(Query_Update,',Contact_DOB = ''',@Customer_Contact_DOB_2,'''  ');
	End if;
	if @Customer_Contact_WD_2 is null or @Customer_Contact_WD_2 = '' or  @Customer_Contact_WD_2 = 'null' then
		set Query_Update = concat(Query_Update,',Contact_WD = null ');
	else
		set Query_Update = concat(Query_Update,',Contact_WD = ''',@Customer_Contact_WD_2,'''  ');
	End if;

	select partnerproduct_customercontactgid2 from atma_tmp_mst_tpartnerproduct
	where partnerproduct_gid=@PartnerProduct_Gid into @Contact_Gid4;

	set Query_Update = concat('Update atma_tmp_mst_tcontact
								set update_date = CURRENT_TIMESTAMP ,update_by=',@Update_By,'
								',Query_Update,'
								Where contact_gid = ',@Contact_Gid4,'');
	#select Query_Update;
	set @Query_Update = Query_Update;
	PREPARE stmt FROM @Query_Update;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;

	if countRow <= 0 then
		set Message = 'Error On Update.';
		rollback;
		leave sp_Atma_PartnerProduct_Set;
	elseif    countRow > 0 then
		set Message = 'SUCCESSFULLY UPDATED';
		commit;
	end if;
	set Query_Update ='';
	if @PartnerProduct_Type is not null or @PartnerProduct_Type <> '' then
		set Query_Update = concat(Query_Update,',partnerproduct_type = ''',@PartnerProduct_Type,'''  ');
	End if;

	if @PartnerProduct_Age is not null or @PartnerProduct_Age <> '' then
		set Query_Update = concat(Query_Update,',partnerproduct_age = ''',@PartnerProduct_Age,'''  ');
	End if;

	if @PartnerProduct_Name is not null or @PartnerProduct_Name <> '' then
		set Query_Update = concat(Query_Update,',partnerproduct_name = ''',@PartnerProduct_Name,'''  ');
	End if;

	set Query_Update = concat('Update atma_tmp_mst_tpartnerproduct
							set update_date = CURRENT_TIMESTAMP,update_by=',@Update_By,'
							',Query_Update,'
							Where partnerproduct_gid = ',@PartnerProduct_Gid,'');
	#select Query_Update;
	set @Query_Update = Query_Update;
	PREPARE stmt FROM @Query_Update;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;

	if countRow <= 0 then
		set Message = 'Error On Update.';
		rollback;
		leave sp_Atma_PartnerProduct_Set;
	elseif    countRow > 0 then
		set Message = 'SUCCESSFULLY UPDATED';
		commit;
	end if;

END IF; #IF li_Action='PRODUCT_UPDATE' then


END