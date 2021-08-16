CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Activity_Set`(in Action  varchar(30),
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_Atma_Activity_Set:BEGIN

#Balamaniraja      08-07-19
#Some Modification By Abishok  12-07-19

Declare Query_Insert varchar(1000);
Declare Query_Column varchar(1000);
Declare Query_Value varchar(1000);
Declare countRow varchar(6000);
Declare Query_Update varchar(1000);
Declare errno int;
Declare msg,Error_Level varchar(1000);

DECLARE EXIT HANDLER FOR SQLEXCEPTION
BEGIN
	GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
	set Message = concat(Error_Level,' : No-',errno , msg);
	ROLLBACK;
END;

if Action='Activity_Insert' then
	START TRANSACTION;

	select JSON_LENGTH(lj_filter,'$') into @li_filter_jsoncount;
	select JSON_LENGTH(lj_classification,'$') into @li_classification_jsoncount;

	if @li_filter_jsoncount = 0 or @li_filter_jsoncount is null then
		set Message = 'No Data In filter Json. ';
		leave sp_Atma_Activity_Set;
	End if;

	 if @li_classification_jsoncount = 0 or @li_classification_jsoncount is null  then
		set Message = 'No Data In classification Json. ';
		leave sp_Atma_Activity_Set;
	End if;

	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_Partnergid')))into @Activity_Partnergid;
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
			leave sp_Atma_Activity_Set;
		end if;
	end if;


	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_PartnerCode')))into @Activity_PartnerCode;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_partnerbranchgid')))into @Activity_partnerbranchgid;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_Code')))into @Activity_Code;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_Type')))into @Activity_Type;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_Name')))into @Activity_Name;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_Desc')))into @Activity_Desc;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_StartDate')))into @Activity_StartDate;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_EndDate')))into @Activity_EndDate;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_ProjectedSpend')))into @Activity_ProjectedSpend;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_rm')))into @Activity_rm;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_FidiInsur')))into @Activity_FidiInsur;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_Bidding')))into @Activity_Bidding;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_Reason')))into @Activity_Reason;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_Status')))into @Activity_Status;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Create_By')))into @Create_By;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Entity_Gid'))) into @Entity_Gid;

    if  @Activity_StartDate <> '' and @Activity_StartDate <> 'null' then
		set @Activity_StartDate=date_format(@Activity_StartDate,'%Y-%m-%d');
	end if;
	if  @Activity_EndDate <> '' and @Activity_EndDate <> 'null' then
		set @Activity_EndDate=date_format(@Activity_EndDate,'%Y-%m-%d');
	end if;
	if  @Activity_StartDate <> '' and @Activity_EndDate<>'' and @Activity_StartDate <> 'null' and @Activity_EndDate <> 'null' then
		if @Activity_StartDate  >= @Activity_EndDate then
			set Message ='Activity Start date should be less than End date ';
			rollback;
			leave sp_Atma_Activity_Set;
		end if;
	end if;
	if  @Activity_PartnerCode = '' or @Activity_PartnerCode is null then
			set Message ='Activity_PartnerCode Is Not Given';
			rollback;
			leave sp_Atma_Activity_Set;
	end if;
	#Contact
	if  @Contact_ContactType_Gid = 0 or @Contact_ContactType_Gid = ''
		or @Contact_ContactType_Gid is null then
			set Message ='Contact_ContactType_Gid Is Not Given';
			rollback;
			leave sp_Atma_Activity_Set;
	end if;

	if  @Contact_Designation_Gid = '' or @Contact_Designation_Gid = 0
		or @Contact_Designation_Gid is null then
			set Message ='Contact_Designation_Gid Is Not Given';
			rollback;
			leave sp_Atma_Activity_Set;
	end if;

	select count(activity_name) from atma_mst_tactivity
	where activity_name=@Activity_Name into @Duplicate_Check_Name_Mst;

     if @Duplicate_Check_Name_Mst > 0 then
        set Message ='Activity Name Already Exits Mst';
		leave sp_Atma_Activity_Set;
	 end if;

    select count(activity_name) from atma_tmp_mst_tactivity
	where activity_name=@Activity_Name into @Duplicate_Check_Name_Tmp;

	if @Duplicate_Check_Name_Tmp > 0 then
		set Message ='Activity Name Already Exits Tmp';
		leave sp_Atma_Activity_Set;
	end if;


	if  @Activity_Type = '' or @Activity_Type is null then
			set Message ='Activity_Type Is Not Given';
			rollback;
			leave sp_Atma_Activity_Set;
	end if;

	if  @Activity_Name = '' or @Activity_Name is null then
			set Message ='Activity_Name Is Not Given';
			rollback;
			leave sp_Atma_Activity_Set;
	end if;

	if  @Activity_Desc = '' or @Activity_Desc is null then
			set Message ='Activity_Desc Is Not Given';
			rollback;
			leave sp_Atma_Activity_Set;
	end if;

	if  @Activity_StartDate = '' or @Activity_StartDate is null then
			set Message ='Activity_StartDate Is Not Given';
			rollback;
			leave sp_Atma_Activity_Set;
	end if;

	if  @Activity_EndDate = '' or @Activity_EndDate is null then
			set Message ='Activity_EndDate Is Not Given';
			rollback;
			leave sp_Atma_Activity_Set;
	end if;

	if  @Activity_ProjectedSpend = '' or @Activity_ProjectedSpend is null then
			set Message ='Activity_ProjectedSpend Is Not Given';
			rollback;
			leave sp_Atma_Activity_Set;
	end if;

	if  @Activity_rm = '' or @Activity_rm is null or @Activity_rm = 0 then
			set Message ='Activity_rm Is Not Given';
			rollback;
			leave sp_Atma_Activity_Set;
	end if;

	if  @Activity_FidiInsur = '' or @Activity_FidiInsur is null then
			set Message ='Activity_FidiInsur Is Not Given';
			rollback;
			leave sp_Atma_Activity_Set;
	end if;

	if  @Activity_Bidding = '' or @Activity_Bidding is null then
			set Message ='Activity_Bidding Is Not Given';
			rollback;
			leave sp_Atma_Activity_Set;
	end if;

	if  @Activity_Status = '' or @Activity_Status is null then
			set Message ='Activity_Status Is Not Given';
			rollback;
			leave sp_Atma_Activity_Set;
	end if;

	if  @Create_By = '' or @Create_By is null
		or @Create_By = 0 then
			set Message ='Create_By Is Not Given';
			rollback;
			leave sp_Atma_Activity_Set;
	end if;

	if  @Entity_Gid = '' or @Entity_Gid is null
		or @Entity_Gid = 0 then
			set Message ='Entity_Gid Is Not Given';
			rollback;
			leave sp_Atma_Activity_Set;
	end if;

	set Query_Column='';
	set Query_Value='';
	if @Activity_Reason is not null then
		set Query_Column = concat(Query_Column,',activity_reason');
		set Query_Value=concat(Query_Value,', ''',@Activity_Reason,''' ');
	end if;

	select codesequence_no from gal_mst_tcodesequence where
	codesequence_type='activity_code' into @AT_activitycode;

	set @AT_activitycode = concat('AC',SUBSTRING(CONCAT('0000',@AT_activitycode),-5));
	set Query_Insert='';

      #select LAST_INSERT_ID() into @Activity_ContactGid
     #set @activity_partnercode='PRCOD2006';
	set @Activity_ContactGid =0;
     set Error_Level='ATMA6.1';
	set Query_Insert=concat('insert into atma_tmp_mst_tactivity
							(activity_partnergid,activity_code,activity_partnercode,activity_partnerbranchgid,
							activity_type,activity_name,
							activity_desc,activity_startdate,
							activity_enddate,activity_projectedspend,
							activity_rm,activity_contactgid,
							activity_fidiinsur, activity_bidding,
							activity_status,entity_gid, create_by',Query_Column,')
			      values(',@Activity_Partnergid,',''',@AT_activitycode,''',
                         ''',@Activity_PartnerCode,''',
                         ''',@Activity_partnerbranchgid,''',
                         ''',@Activity_Type,''',
                         ''',@Activity_Name,''',''',@Activity_Desc,''',
                         ''',@Activity_StartDate,''',''',@Activity_EndDate,''',
                         ''',@Activity_ProjectedSpend,''',',@Activity_rm,',
                         ',@Activity_ContactGid,',''',@Activity_FidiInsur,''',
                         ''',@Activity_Bidding,''',''',@Activity_Status,''',
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
		set Message = 'INSERT FAILED';
		rollback;
	end if;

	set Error_Level='ATMA6.2';
	set Query_Insert='';
    select LAST_INSERT_ID() into @Contact_RefTable_Gid;
	select activity_code from atma_tmp_mst_tactivity where activity_gid=@Contact_RefTable_Gid into @Contact_RefTableCode;
	select fn_REFGid('ACTIVITY_CONTACT') into @Contact_Ref_Gid ;

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

	set Error_Level='ATMA6.3';
	set Query_Insert=concat('insert into atma_tmp_mst_tcontact
									(Contact_ref_gid,Contact_reftable_gid,
									Contact_contacttype_gid,Contact_designation_gid,
                                    contact_reftablecode,
                                    entity_gid,create_by',Query_Column,')
			      values(',@Contact_Ref_Gid,',',@Contact_RefTable_Gid,',
						  ',@Contact_ContactType_Gid,',',@Contact_Designation_Gid,',
						 ''',@Contact_RefTableCode,''',
                         ',@Entity_Gid,',',@Create_By,'
                         ',Query_Value,')'
                    );

   #select LAST_INSERT_ID() into @act_contactgid;
	#SELECT Query_Insert;
    set @Insert_query = Query_Insert;
	PREPARE stmt FROM @Insert_query;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
    if countRow >  0 then
		set Message = 'SUCCESSFULLY INSERTED';
         Update gal_mst_tcodesequence
				set  codesequence_no= codesequence_no+1
				Where codesequence_type = 'activity_code';
        commit;
	else
		set Message = 'INSERT FAILED';
		rollback;
	end if;

       select max(contact_gid) from atma_tmp_mst_tcontact into @act_contactgid;

	   update  atma_tmp_mst_tactivity set
       activity_contactgid=@act_contactgid
       where activity_gid=@Contact_RefTable_Gid;

END IF;

if Action='ACTIVITY_UPDATE' then
	START TRANSACTION;
	select JSON_LENGTH(lj_filter,'$') into @li_jsoncount;
	select JSON_LENGTH(lj_classification,'$') into @li_classification_json_count;

	if @li_jsoncount = 0 or @li_jsoncount is null
	   or @li_jsoncount = ''  then
		set Message = 'No Data In filter Json - Update.';
		leave sp_Atma_Activity_Set;
	End if;

	if @li_classification_json_count = 0  or @li_classification_json_count = ''
	   or @li_classification_json_count is null  then
			set Message = 'No Data In classification Json - Update.';
			leave sp_Atma_Activity_Set;
	End if;

	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_ContactType_Gid')))
	into @Contact_ContactType_Gid;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_PersonName')))
	into @Contact_PersonName;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_Designation_Gid')))
	into @Contact_Designation_Gid;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_LandLine')))
	into @Contact_LandLine;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_LandLine2')))
	into @Contact_LandLine2;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_MobileNo')))
	into @Contact_MobileNo;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_MobileNo2')))
	into @Contact_MobileNo2;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_Email')))
	into @Contact_Email;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_DOB')))
	into @Contact_DOB;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_WD')))
	into @Contact_WD;

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
			leave sp_Atma_Activity_Set;
		end if;
	end if;



	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_Gid')))
	into @Activity_Gid;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_Code')))
	into @Activity_Code;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_partnerbranchgid')))
	into @Activity_partnerbranchgid;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_Type')))
	into @Activity_Type;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_Name')))
	into @Activity_Name;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_Desc')))
	into @Activity_Desc;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_StartDate')))
	into @Activity_StartDate;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_EndDate')))
	into @Activity_EndDate;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_ProjectedSpend')))
	into @Activity_ProjectedSpend;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_rm')))
	into @Activity_rm;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_FidiInsur')))
	into @Activity_FidiInsur;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_Bidding')))
	into @Activity_Bidding;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_Reason')))
	into @Activity_Reason;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_Status')))
	into @Activity_Status;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Update_By')))
	into @Update_By;

	if @Activity_Gid is null or @Activity_Gid= ''
	   or @Activity_Gid = 0 then
			set Message = 'Activity_Gid IS Not Given';
			leave sp_Atma_Activity_Set;
	End if;

	set Query_Update = '';
	if @Activity_Code is not null or @Activity_Code <> '' then
		set Query_Update = concat(Query_Update, ',activity_code = ''',@Activity_Code,''' ');
	end if;
    if @Activity_partnerbranchgid is not null or @Activity_partnerbranchgid <> '' or @Activity_partnerbranchgid=0 then
		set Query_Update = concat(Query_Update, ',activity_partnerbranchgid = ',@Activity_partnerbranchgid,' ');
	end if;
	if @Activity_Type is not null or @Activity_Type <> '' then
		set Query_Update = concat(Query_Update, ',activity_type = ''',@Activity_Type,''' ');
	end if;
	if @Activity_Name is not null or @Activity_Name <> '' then
		set Query_Update = concat(Query_Update, ',activity_name = ''',@Activity_Name,''' ');
	end if;
	if @Activity_Desc is not null or @Activity_Desc <> '' then
		set Query_Update = concat(Query_Update, ',activity_desc = ''',@Activity_Desc,''' ');
	end if;
	if @Activity_StartDate is not null or @Activity_StartDate <> '' then
		set Query_Update = concat(Query_Update, ',activity_startdate = ''',@Activity_StartDate,''' ');
		set @Activity_StartDate=date_format(@Activity_StartDate,'%Y-%m-%d');
	end if;
	if @Activity_EndDate is not null or @Activity_EndDate <> '' then
		set Query_Update = concat(Query_Update, ',activity_enddate = ''',@Activity_EndDate,''' ');
		set @Activity_EndDate=date_format(@Activity_EndDate,'%Y-%m-%d');
	end if;
	if @Activity_ProjectedSpend is not null or @Activity_ProjectedSpend <> '' then
		set Query_Update = concat(Query_Update, ',activity_projectedspend = ''',@Activity_ProjectedSpend,''' ');
	end if;
	if @Activity_rm is not null or @Activity_rm <> '' then
		set Query_Update = concat(Query_Update, ',activity_rm = ''',@Activity_rm,''' ');
	end if;
	if @Activity_FidiInsur is not null or @Activity_FidiInsur <> '' then
		set Query_Update = concat(Query_Update, ',activity_fidiinsur = ''',@Activity_FidiInsur,''' ');
	end if;
	if @Activity_Bidding is not null or @Activity_Bidding <> '' then
		set Query_Update = concat(Query_Update, ',activity_bidding = ''',@Activity_Bidding,''' ');
	end if;
	if @Activity_Reason is not null or @Activity_Reason <> '' then
		set Query_Update = concat(Query_Update, ',activity_reason = ''',@Activity_Reason,''' ');
	end if;
	if @Activity_Status is not null or @Activity_Status <> '' then
		set Query_Update = concat(Query_Update, ',activity_status = ''',@Activity_Status,''' ');
	end if;

	set Error_Level='ATMA6.4';
	set Query_Update = concat('Update  atma_tmp_mst_tactivity
			 set update_date = CURRENT_TIMESTAMP,update_by=',@Update_By,'
			 ',Query_Update,'
			 Where activity_gid = ',@Activity_Gid,'
			 and activity_isactive = ''Y'' and activity_isremoved = ''N''
			 ');

	#select Query_Update;
	set @Query_Update = '';
	set @Query_Update = Query_Update;
	PREPARE stmt FROM @Query_Update;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;

	if countRow <= 0 then
			set Message = 'Error On Update.';
			rollback;
			leave sp_Atma_Activity_Set;
	elseif countRow > 0 then
			set Message = 'SUCCESSFULLY UPDATED';
			#commit;
	end if;
	set Query_Update = '';

	if lower(@Contact_ContactType_Gid) <> 'null' and @Contact_ContactType_Gid <> '' then
				set Query_Update = concat(Query_Update,',Contact_contacttype_gid = ',@Contact_ContactType_Gid,'  ');
			else
                set Message='Contact_ContactType can not be null' ;
				leave sp_Atma_Activity_Set;
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
				leave sp_Atma_Activity_Set;
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

	select activity_contactgid from atma_tmp_mst_tactivity where activity_gid=@Activity_Gid
	into @Contact_Gid;
    set Error_Level='ATMA6.5';
    set Query_Update = concat('Update atma_tmp_mst_tcontact
                         set update_date = CURRENT_TIMESTAMP,update_by=',@Update_By,'
                         ',Query_Update,'
						 Where contact_gid = ',@Contact_Gid,'
                         ');
	#select Query_Update;
	set @Query_Update = '';
	set @Query_Update = Query_Update;
	PREPARE stmt FROM @Query_Update;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
	if countRow <= 0 then
			set Message = 'Error On Update.';
			rollback;
			leave sp_Atma_Activity_Set;
	elseif    countRow > 0 then
			set Message = 'SUCCESSFULLY UPDATED';
			commit;
	end if;


END IF;

/*
if Action='Activity_Mst' then

	SELECT EXISTS(SELECT main_activity_gid FROM atma_tmp_mst_tactivity
		WHERE main_activity_gid=1) into @Main_Activity_Gid;


if @Main_Activity_Gid <>'' then

	START TRANSACTION;

	select JSON_LENGTH(lj_filter,'$') into @li_filter_jsoncount;
	select JSON_LENGTH(lj_classification,'$') into @li_classification_jsoncount;


        if @li_filter_jsoncount = 0 or @li_filter_jsoncount is null then
			set Message = 'No Data In filter Json. ';
			leave sp_Atma_Activity_Set;
		End if;

         if @li_classification_jsoncount = 0 or @li_classification_jsoncount is null  then
			set Message = 'No Data In classification Json. ';
			leave sp_Atma_Activity_Set;
		End if;

        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_Partnergid')))into @Activity_Partnergid;
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

        set @Contact_DOB=date_format(@Contact_DOB,'%Y-%m-%d');
		set @Contact_WD=date_format(@Contact_WD,'%Y-%m-%d');

                if @Contact_DOB  >= @Contact_WD then
					set Message ='Contact_WD date should be greater than Contact_DOB date ';
					rollback;
					leave sp_Atma_Activity_Set;
				end if;

        #select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_PartnerCode')))into @Activity_PartnerCode;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_Code')))into @Activity_Code;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_Type')))into @Activity_Type;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_Name')))into @Activity_Name;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_Desc')))into @Activity_Desc;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_StartDate')))into @Activity_StartDate;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_EndDate')))into @Activity_EndDate;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_ProjectedSpend')))into @Activity_ProjectedSpend;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_rm')))into @Activity_rm;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_FidiInsur')))into @Activity_FidiInsur;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_Bidding')))into @Activity_Bidding;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_Reason')))into @Activity_Reason;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_Status')))into @Activity_Status;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Create_By')))into @Create_By;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Entity_Gid'))) into @Entity_Gid;

			set @Activity_StartDate=date_format(@Activity_StartDate,'%Y-%m-%d');
			set @Activity_EndDate=date_format(@Activity_EndDate,'%Y-%m-%d');

				if @Activity_StartDate >= @Activity_EndDate then
					set Message ='End date should be greater than Start date ';
					rollback;
					leave sp_Atma_Activity_Set;
				end if;


        #if  @Activity_PartnerCode = '' or @Activity_PartnerCode is null then

				#set Message ='Activity_PartnerCode Is Not Given';
				#rollback;
				#leave sp_Atma_Activity_Set;
		#end if;


        #Contact
        if  @Contact_ContactType_Gid = 0 or @Contact_ContactType_Gid = ''
            or @Contact_ContactType_Gid is null then

				set Message ='Contact_ContactType_Gid Is Not Given';
				rollback;
				leave sp_Atma_Activity_Set;
		end if;

        if  @Contact_PersonName = '' or @Contact_PersonName is null then

				set Message ='Contact_PersonName Is Not Given';
				rollback;
				leave sp_Atma_Activity_Set;
		end if;

        if  @Contact_Designation_Gid = '' or @Contact_Designation_Gid = 0
            or @Contact_Designation_Gid is null then

				set Message ='Contact_Designation_Gid Is Not Given';
				rollback;
				leave sp_Atma_Activity_Set;
		end if;

        if  @Contact_LandLine = '' or @Contact_LandLine = 0
            or @Contact_LandLine is null then

				set Message ='Contact_LandLine Is Not Given';
				rollback;
				leave sp_Atma_Activity_Set;
		end if;

        if  @Contact_LandLine2 = '' or @Contact_LandLine2 = 0
            or @Contact_LandLine2 is null then

				set Message ='Contact_LandLine2 Is Not Given';
				rollback;
				leave sp_Atma_Activity_Set;
		end if;

        if  @Contact_MobileNo = '' or @Contact_MobileNo = 0
            or @Contact_MobileNo is null then

				set Message ='Contact_MobileNo Is Not Given';
				rollback;
				leave sp_Atma_Activity_Set;
		end if;

        if  @Contact_MobileNo2 = '' or @Contact_MobileNo2 = 0
            or @Contact_MobileNo2 is null then

				set Message ='Contact_MobileNo2 Is Not Given';
				rollback;
				leave sp_Atma_Activity_Set;
		end if;

        if  @Contact_Email = ''  or @Contact_Email is null then

				set Message ='Contact_Email Is Not Given';
				rollback;
				leave sp_Atma_Activity_Set;
		end if;

        if  @Contact_DOB = ''  or @Contact_DOB is null then

				set Message ='Contact_DOB Is Not Given';
				rollback;
				leave sp_Atma_Activity_Set;
		end if;

        if  @Contact_WD = ''  or @Contact_WD is null then

				set Message ='Contact_WD Is Not Given';
				rollback;
				leave sp_Atma_Activity_Set;
		end if;

        #Activity
        if  @Activity_Code = '' or @Activity_Code is null then

				set Message ='Activity_Code Is Not Given';
				rollback;
				leave sp_Atma_Activity_Set;
		end if;

        if  @Activity_Type = '' or @Activity_Type is null then

				set Message ='Activity_Type Is Not Given';
				rollback;
				leave sp_Atma_Activity_Set;
		end if;

        if  @Activity_Name = '' or @Activity_Name is null then

				set Message ='Activity_Name Is Not Given';
				rollback;
				leave sp_Atma_Activity_Set;
		end if;

        if  @Activity_Desc = '' or @Activity_Desc is null then

				set Message ='Activity_Desc Is Not Given';
				rollback;
				leave sp_Atma_Activity_Set;
		end if;

        if  @Activity_StartDate = '' or @Activity_StartDate is null then

				set Message ='Activity_StartDate Is Not Given';
				rollback;
				leave sp_Atma_Activity_Set;
		end if;

        if  @Activity_EndDate = '' or @Activity_EndDate is null then

				set Message ='Activity_EndDate Is Not Given';
				rollback;
				leave sp_Atma_Activity_Set;
		end if;

        if  @Activity_ProjectedSpend = '' or @Activity_ProjectedSpend is null then

				set Message ='Activity_ProjectedSpend Is Not Given';
				rollback;
				leave sp_Atma_Activity_Set;
		end if;

        if  @Activity_rm = '' or @Activity_rm is null or @Activity_rm = 0 then

				set Message ='Activity_rm Is Not Given';
				rollback;
				leave sp_Atma_Activity_Set;
		end if;

        if  @Activity_FidiInsur = '' or @Activity_FidiInsur is null then

				set Message ='Activity_FidiInsur Is Not Given';
				rollback;
				leave sp_Atma_Activity_Set;
		end if;

        if  @Activity_Bidding = '' or @Activity_Bidding is null then

				set Message ='Activity_Bidding Is Not Given';
				rollback;
				leave sp_Atma_Activity_Set;
		end if;

        if  @Activity_Reason = '' or @Activity_Reason is null then

				set Message ='Activity_Reason Is Not Given';
				rollback;
				leave sp_Atma_Activity_Set;
		end if;

        if  @Activity_Status = '' or @Activity_Status is null then

				set Message ='Activity_Status Is Not Given';
				rollback;
				leave sp_Atma_Activity_Set;
		end if;

        if  @Create_By = '' or @Create_By is null
            or @Create_By = 0 then

				set Message ='Create_By Is Not Given';
				rollback;
				leave sp_Atma_Activity_Set;
		end if;

        if  @Entity_Gid = '' or @Entity_Gid is null
            or @Entity_Gid = 0 then

				set Message ='Entity_Gid Is Not Given';
				rollback;
				leave sp_Atma_Activity_Set;
		end if;


set Query_Insert='';

      #select LAST_INSERT_ID() into @Activity_ContactGid ;

     set @Activity_ContactGid =0;
     set @activity_partnercode='PRCOD2006';
     set Error_Level='ATMA6.6';
	set Query_Insert=concat('insert into atma_mst_tactivity
							(activity_partnergid,activity_code,activity_partnercode,
							activity_type, activity_name,
							activity_desc, activity_startdate,
							activity_enddate, activity_projectedspend,
							activity_rm, activity_contactgid,
							activity_fidiinsur, activity_bidding,
							activity_reason,activity_status,
							entity_gid, create_by)
			      values(',@Activity_Partnergid,',''',@Activity_Code,''',
                         ''',@Activity_PartnerCode,''',''',@Activity_Type,''',
                         ''',@Activity_Name,''',''',@Activity_Desc,''',
                         ''',@Activity_StartDate,''',''',@Activity_EndDate,''',
                         ''',@Activity_ProjectedSpend,''',',@Activity_rm,',
                         ',@Activity_ContactGid,',''',@Activity_FidiInsur,''',
                         ''',@Activity_Bidding,''',''',@Activity_Reason,''',
                         ''',@Activity_Status,''',
                         ',@Entity_Gid,',',@Create_By,')'
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
		set Message = 'INSERT FAILED';
		rollback;
	end if;



	set Query_Insert='';

	select LAST_INSERT_ID() into @Contact_RefTable_Gid;
	select activity_code from atma_tmp_mst_tactivity where activity_gid=@Contact_RefTable_Gid into @Contact_RefTableCode;
	select fn_REFGid('ACTIVITY_CONTACT') into @Contact_Ref_Gid ;
    #select Contact_Ref_Gid;
    #set @Contact_RefTable_Gid=2;
    #set @Contact_RefTableCode='RF002';
    set Error_Level='ATMA6.7';
	set Query_Insert=concat('insert into atma_mst_tcontact
									(Contact_ref_gid, Contact_reftable_gid,
									contact_reftablecode,Contact_contacttype_gid,
                                    Contact_personname, Contact_designation_gid,
                                    Contact_landline, Contact_landline2, Contact_mobileno,
                                    Contact_mobileno2, Contact_email,Contact_DOB, Contact_WD,
                                    entity_gid, create_by)
			      values(',@Contact_Ref_Gid,',',@Contact_RefTable_Gid,',
						 ''',@Contact_RefTableCode,''',
                         ',@Contact_ContactType_Gid,',''',@Contact_PersonName,''',
                         ',@Contact_Designation_Gid,',',@Contact_LandLine,',
                         ',@Contact_LandLine2,',',@Contact_MobileNo,',
                         ',@Contact_MobileNo2,',''',@Contact_Email,''',
                         ''',@Contact_DOB,''',''',@Contact_WD,''',
                         ',@Entity_Gid,',',@Create_By,')'
                    );

   #select LAST_INSERT_ID() into @act_contactgid;
	#SELECT Query_Insert;
    set @Insert_query = Query_Insert;
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

       select max(contact_gid) from atma_tmp_mst_tcontact into @act_contactgid;

	   update  atma_tmp_mst_tactivity set
       activity_contactgid=@act_contactgid
       where activity_gid=@Contact_RefTable_Gid;

  END IF;


      #select Action;

			START TRANSACTION;

		select JSON_LENGTH(lj_filter,'$') into @li_jsoncount;
		select JSON_LENGTH(lj_classification,'$') into @li_classification_json_count;

			if @li_jsoncount = 0 or @li_jsoncount is null
               or @li_jsoncount = ''  then
				set Message = 'No Data In filter Json - Update.';
				leave sp_Atma_Activity_Set;
			End if;

            if @li_classification_json_count = 0  or @li_classification_json_count = ''
               or @li_classification_json_count is null  then
					set Message = 'No Data In classification Json - Update.';
					leave sp_Atma_Activity_Set;
			End if;

        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_ContactType_Gid')))
		into @Contact_ContactType_Gid;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_PersonName')))
        into @Contact_PersonName;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_Designation_Gid')))
        into @Contact_Designation_Gid;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_LandLine')))
        into @Contact_LandLine;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_LandLine2')))
        into @Contact_LandLine2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_MobileNo')))
        into @Contact_MobileNo;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_MobileNo2')))
        into @Contact_MobileNo2;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_Email')))
        into @Contact_Email;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_DOB')))
        into @Contact_DOB;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Contact_WD')))
        into @Contact_WD;

            select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_Gid')))
            into @Activity_Gid;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_Code')))
            into @Activity_Code;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_Type')))
            into @Activity_Type;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_Name')))
            into @Activity_Name;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_Desc')))
            into @Activity_Desc;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_StartDate')))
            into @Activity_StartDate;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_EndDate')))
            into @Activity_EndDate;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_ProjectedSpend')))
            into @Activity_ProjectedSpend;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_rm')))
            into @Activity_rm;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_FidiInsur')))
            into @Activity_FidiInsur;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_Bidding')))
            into @Activity_Bidding;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_Reason')))
            into @Activity_Reason;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Activity_Status')))
            into @Activity_Status;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Update_By')))
            into @Update_By;


                if @Activity_Gid is null or @Activity_Gid= ''
				   or @Activity_Gid = 0 then
						set Message = 'Activity_Gid IS Not Given';
						leave sp_Atma_Activity_Set;
				End if;

			set Query_Update = '';

			if @Activity_Code is not null or @Activity_Code <> '' then
				set Query_Update = concat(Query_Update, ',activity_code = ''',@Activity_Code,''' ');
			end if;


            if @Activity_Type is not null or @Activity_Type <> '' then
				set Query_Update = concat(Query_Update, ',activity_type = ''',@Activity_Type,''' ');
			end if;

            if @Activity_Name is not null or @Activity_Name <> '' then
				set Query_Update = concat(Query_Update, ',activity_name = ''',@Activity_Name,''' ');
			end if;

            if @Activity_Desc is not null or @Activity_Desc <> '' then
				set Query_Update = concat(Query_Update, ',activity_desc = ''',@Activity_Desc,''' ');
			end if;

            if @Activity_StartDate is not null or @Activity_StartDate <> '' then
				set Query_Update = concat(Query_Update, ',activity_startdate = ''',@Activity_StartDate,''' ');
                set @Activity_StartDate=date_format(@Activity_StartDate,'%Y-%m-%d');
			end if;

            if @Activity_EndDate is not null or @Activity_EndDate <> '' then
				set Query_Update = concat(Query_Update, ',activity_enddate = ''',@Activity_EndDate,''' ');
                set @Activity_EndDate=date_format(@Activity_EndDate,'%Y-%m-%d');
			end if;

            if @Activity_ProjectedSpend is not null or @Activity_ProjectedSpend <> '' then
				set Query_Update = concat(Query_Update, ',activity_projectedspend = ''',@Activity_ProjectedSpend,''' ');
			end if;

            if @Activity_rm is not null or @Activity_rm <> '' then
				set Query_Update = concat(Query_Update, ',activity_rm = ''',@Activity_rm,''' ');
			end if;

            if @Activity_FidiInsur is not null or @Activity_FidiInsur <> '' then
				set Query_Update = concat(Query_Update, ',activity_fidiinsur = ''',@Activity_FidiInsur,''' ');
			end if;

            if @Activity_Bidding is not null or @Activity_Bidding <> '' then
				set Query_Update = concat(Query_Update, ',activity_bidding = ''',@Activity_Bidding,''' ');
			end if;

            if @Activity_Reason is not null or @Activity_Reason <> '' then
				set Query_Update = concat(Query_Update, ',activity_reason = ''',@Activity_Reason,''' ');
			end if;

            if @Activity_Status is not null or @Activity_Status <> '' then
				set Query_Update = concat(Query_Update, ',activity_status = ''',@Activity_Status,''' ');
			end if;

            set Error_Level='ATMA6.8';
			set Query_Update = concat('Update  atma_tmp_mst_tactivity
                         set update_date = CURRENT_TIMESTAMP,update_by=',@Update_By,'
                         ',Query_Update,'
						 Where activity_gid = ',@Activity_Gid,'
						 and activity_isactive = ''Y'' and activity_isremoved = ''N''
                         ');

			#select Query_Update;
			set @Query_Update = '';
			set @Query_Update = Query_Update;
			PREPARE stmt FROM @Query_Update;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;

		if countRow <= 0 then
				set Message = 'Error On Update.';
				rollback;
				leave sp_Atma_Activity_Set;
		elseif    countRow > 0 then
				set Message = 'SUCCESSFULLY UPDATED';
                commit;
		end if;


        set Query_Update = '';


            if @Contact_PersonName is not null or @Contact_PersonName <> '' then
				set Query_Update = concat(Query_Update, ',Contact_personname = ''',@Contact_PersonName,''' ');
			end if;

            if @Contact_Designation_Gid is not null or @Contact_Designation_Gid <> '' then
				set Query_Update = concat(Query_Update, ',Contact_designation_gid = ''',@Contact_Designation_Gid,''' ');
			end if;

            if @Contact_LandLine is not null or @Contact_LandLine <> '' then
				set Query_Update = concat(Query_Update, ',Contact_landline = ''',@Contact_LandLine,''' ');
			end if;

            if @Contact_LandLine2 is not null or @Contact_LandLine2 <> '' then
				set Query_Update = concat(Query_Update, ',Contact_LandLine2 = ''',@Contact_LandLine2,''' ');
			end if;

            if @Contact_MobileNo is not null or @Contact_MobileNo <> '' then
				set Query_Update = concat(Query_Update, ',Contact_mobileno = ''',@Contact_MobileNo,''' ');
			end if;

            if @Contact_MobileNo2 is not null or @Contact_MobileNo2 <> '' then
				set Query_Update = concat(Query_Update, ',Contact_mobileno2 = ''',@Contact_MobileNo2,''' ');
			end if;

            if @Contact_Email is not null or @Contact_Email <> '' then
				set Query_Update = concat(Query_Update, ',Contact_email = ''',@Contact_Email,''' ');
			end if;

            if @Contact_DOB is not null or @Contact_DOB <> '' then
				set @Contact_DOB=date_format(@Contact_DOB,'%Y-%m-%d');
				set Query_Update = concat(Query_Update, ',Contact_DOB = ''',@Contact_DOB,''' ');
			end if;

            if @Contact_WD is not null or @Contact_WD <> '' then
				set @Contact_WD=date_format(@Contact_WD,'%Y-%m-%d');
				set Query_Update = concat(Query_Update, ',Contact_WD = ''',@Contact_WD,''' ');

			end if;


		    select activity_contactgid from atma_tmp_mst_tactivity where activity_gid=@Activity_Gid
            into @Contact_Gid;
            set Error_Level='ATMA6.9';
            if Query_Update<> '' or Query_Update <> 0 or Query_Update=null then

        set Query_Update = concat('Update atma_tmp_mst_tcontact
                         set update_date = CURRENT_TIMESTAMP,update_by=',@Update_By,'
                         ',Query_Update,'
						 Where contact_gid = ',@Contact_Gid,'
                         ');


       #select Query_Update;
			set @Query_Update = '';
			set @Query_Update = Query_Update;
			PREPARE stmt FROM @Query_Update;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;

		if countRow <= 0 then
				set Message = 'Error On Update.';
				rollback;
				leave sp_Atma_Activity_Set;
		elseif    countRow > 0 then
				set Message = 'SUCCESSFULLY UPDATED';
                commit;
		end if;
	end if;


END IF;
*/
END