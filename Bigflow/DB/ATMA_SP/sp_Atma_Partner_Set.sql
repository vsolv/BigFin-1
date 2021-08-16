CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Partner_Set`(in ls_Action varchar(160),
in partner_json json,
in lj_classification json,
out Message varchar(10000))
sp_Atma_Partner_Set:BEGIN
declare Query_Insert varchar(1000);
declare Query_Column varchar(500);
declare Query_Value varchar(500);
declare li_Query varchar(1000);
Declare countRow varchar(6000);
declare Query_Update varchar(1000);
declare Query_Update1 varchar(1000);
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
	select JSON_LENGTH(partner_json,'$') into @li_jsonpartner;
	select JSON_LENGTH(lj_classification,'$') into @li_classification_jsoncount;
	if @li_jsonpartner = 0 or @li_jsonpartner is null  then
		set Message = 'No Data In Json. ';
		leave sp_Atma_Partner_Set;
	End if;
	if @li_classification_jsoncount = 0 or @li_classification_jsoncount is null  then
		set Message = 'No Entity_Gid In Json. ';
		leave sp_Atma_Partner_Set;
	End if;
	if @li_classification_jsoncount is not null or @li_classification_jsoncount	<> ''
		   or @li_classification_jsoncount	<> 0 then
		select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Entity_Gid')))into @Entity_Gid;
	End if;
	if @li_jsonpartner is not null or @li_jsonpartner <> '' then

			#Address
			select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Address_1')))into @Address_1;
			select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Address_2')))into @Address_2;
			select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Address_3')))into @Address_3;
			select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Address_Pincode')))into @Address_Pincode;
			select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Address_District_Gid')))into @Address_District_Gid;
			select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Address_City_Gid')))into @Address_City_Gid;
			select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Address_State_Gid')))into @Address_State_Gid;
            #Contact
			select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Contact_ContactType_Gid')))into @Contact_ContactType_Gid;
			select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Contact_PersonName')))into @Contact_PersonName;
			select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Contact_Designation_Gid')))into @Contact_Designation_Gid;
			select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Contact_LandLine')))into @Contact_LandLine;
			select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Contact_LandLine2')))into @Contact_LandLine2;
			select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Contact_MobileNo')))into @Contact_MobileNo;
			select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Contact_MobileNo2')))into @Contact_MobileNo2;
			select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Contact_Email')))into @Contact_Email;
			select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Contact_DOB')))into @Contact_DOB;
			select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Contact_WD')))into @Contact_WD;

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
					leave sp_Atma_Partner_Set;
				end if;
            end if;
            if  @Address_District_Gid = '' or @Address_District_Gid is null or @Address_District_Gid =0  then
				set Message = 'Address_District_Gid is not given ';
				leave sp_Atma_Partner_Set;
			End if;

            if  @Contact_ContactType_Gid = '' or @Contact_ContactType_Gid is null or @Contact_ContactType_Gid =0  then
				set Message = 'Contact_ContactType_Gid is not given ';
				leave sp_Atma_Partner_Set;
			End if;

            if  @Contact_Designation_Gid = '' or @Contact_Designation_Gid is null or @Contact_Designation_Gid =0  then
				set Message = 'Contact_Designation_Gid is not given ';
				leave sp_Atma_Partner_Set;
			End if;


		 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Name')))into @Partner_Name;
		 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Panno')))into @Partner_Panno;
		 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Compregno')))into @Partner_Compregno;
		 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Group')))into @Partner_Group;
		 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Custcategorygid')))into @Partner_Custcategorygid;
		 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Classification')))into @Partner_Classification;
		 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Type')))into @Partner_Type;
		 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Web')))into @Partner_Web;
		 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Activecontract')))into @Partner_Activecontract;
		 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Reason_No_Contract')))into @Partner_Reason_No_Contract;
		 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Contractdatefrom')))into @Partner_Contractdatefrom;
		 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Contractdateto')))into @Partner_Contractdateto;
		 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Aproxspend')))into @Partner_Aproxspend;
		 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Actualspend')))into @Partner_Actualspend;
		 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Noofdir')))into @Partner_Noofdir;
		 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Orgtype')))into @Partner_Orgtype;

		 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Remarks')))into @Partner_Remarks;
		 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Status')))into @Partner_Status;
		 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Renewdate')))into @Partner_Renewdate;
		 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Rmname')))into @Partner_Rmname;
		 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Addressgid')))into @Partner_Addressgid;
		 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Contactgid')))into @Partner_Contactgid;

		 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Create_By')))into @Create_By;
	end if;
					if  @Partner_Contractdatefrom <> '' and @Partner_Contractdatefrom <> 'null' then
					set @Partner_Contractdatefrom=date_format(@Partner_Contractdatefrom,'%Y-%m-%d');
					end if;
					if  @Partner_Contractdateto <> '' and @Partner_Contractdateto <> 'null' then
					set @Partner_Contractdateto=date_format(@Partner_Contractdateto,'%Y-%m-%d');
					end if;

                    if  @Partner_Contractdatefrom <> '' and @Partner_Contractdateto<>'' and @Partner_Contractdatefrom <> 'null'
                    and @Partner_Contractdateto <> 'null' then
					if @Partner_Contractdatefrom  >= @Partner_Contractdateto then
					set Message ='Contrac to date should be greater than contract from date ';
					rollback;
					leave sp_Atma_Partner_Set;
				end if;
                end if;
    set @Partner_Contractdatefrom_year='';


	set @Partner_Renewdate=date_format(@Partner_Renewdate,'%Y-%m-%d');

	if @Partner_Activecontract='No' then
		set @Activecontract='N';
	elseif @Partner_Activecontract='Yes' then
		set @Activecontract='Y';
	end if;

	if @Partner_Name = ''  or @Partner_Name is null  then
		set Message ='Partner Name Is Not Given';
		rollback;
		leave sp_Atma_Partner_Set;
	end if;

	set@partner_nm='';
	select  count(partner_name) from atma_tmp_tpartner
    where partner_name=@Partner_Name into @partner_nm;

	select count(partner_name)
	from atma_mst_tpartner
	where partner_name=@Partner_Name into @Duplicate_Check_Name;

     if @Duplicate_Check_Name > 0 then
        set Message ='Partner Name Already Exist ';
            leave sp_Atma_Partner_Set;
	 end if;

	if  @partner_nm >0 then
		set Message ='Partner Name Already Exist ';
		rollback;
		leave sp_Atma_Partner_Set;
	end if;

	if @Partner_Custcategorygid = '' or @Partner_Custcategorygid is null or @Partner_Custcategorygid =0 then
		set Message ='Partner Custcategorygid Is Not Given';
		rollback;
		leave sp_Atma_Partner_Set;
	end if;

	if @Partner_Classification = '' or @Partner_Classification is null then
		set Message ='Partner Classification Is Not Given';
		rollback;
		leave sp_Atma_Partner_Set;
	end if;

	if @Partner_Type = '' or @Partner_Type is null then
		set Message ='Partner Type Is Not Given';
		rollback;
		leave sp_Atma_Partner_Set;
	end if;

	if @Partner_Activecontract = '' or @Partner_Activecontract is null then
		set Message ='Partner Activecontract Is Not Given';
		rollback;
		leave sp_Atma_Partner_Set;
	end if;

	if @Partner_Aproxspend = '' or @Partner_Aproxspend is null then
		set Message ='Partner Aproxspend Is Not Given';
		rollback;
		leave sp_Atma_Partner_Set;
	end if;

	if @Partner_Actualspend = '' or @Partner_Actualspend is null then
		set Message ='Partner Actualspend Is Not Given';
		rollback;
		leave sp_Atma_Partner_Set;
	end if;

	if @Partner_Noofdir = '' or @Partner_Noofdir is null then
		set Message ='Partner No of dir Is Not Given';
		rollback;
		leave sp_Atma_Partner_Set;
	end if;

	if @Partner_Orgtype = '' or @Partner_Orgtype is null  then
		set Message ='Partner Orgtype Is Not Given';
		rollback;
		leave sp_Atma_Partner_Set;
	end if;

	if @Partner_Status = '' or @Partner_Status is null  then
		set Message ='Partner Status Is Not Given';
		rollback;
		leave sp_Atma_Partner_Set;
	end if;

	if @Partner_Rmname = '' or @Partner_Rmname is null or @Partner_Rmname =0 then
		set Message ='Partner Rmname Is Not Given';
		rollback;
		leave sp_Atma_Partner_Set;
	end if;

	if @Entity_Gid = 0 or @Entity_Gid = '' or @Entity_Gid is null  then
		set Message ='Entity Gid Is Not Given';
		rollback;
		leave sp_Atma_Partner_Set;
	end if;
	set Query_Column='';
	set Query_Value='';
	if @Partner_Reason_No_Contract is not null or @Partner_Reason_No_Contract=''  then
		set Query_Column = concat(Query_Column,',partner_reason_no_contract');
		set Query_Value=concat(Query_Value,', ''',@Partner_Reason_No_Contract,''' ');
	end if;

#set @AT_partnercode='';
	#select max(partner_code) from atma_tmp_tpartner into @AT_partnercode;
	select codesequence_no from gal_mst_tcodesequence where
	codesequence_type='partner_code' into @AT_partnercode;
    #if  @AT_partnercode is null or @AT_partnercode='' then
		 #set @AT_partnercode='PA00000';
	#end if;
		#call sp_atma_Generatecode_Get('WITHOUT_DATE', 'PA', '0000', @AT_partnercode, @Message);
		#select @Message into @AT_partner_code;
		set @code_partner = concat('PA',SUBSTRING(CONCAT('0000',@AT_partnercode),-5));
    #select @code_partner;

    select count(@Partner_Noofdir) from atma_tmp_tpartner into @noofdircount;
    set @Partner_Addressgid=0;
    set @Partner_Contactgid=0;
	set Query_Insert ='';
	set Query_Insert = concat('INSERT INTO atma_tmp_tpartner
	(partner_code,partner_name,partner_panno,partner_compregno,partner_group,partner_custcategorygid,
	partner_Classification,partner_type,partner_web,partner_activecontract,
	partner_contractdatefrom,partner_contractdateto,partner_aproxspend,partner_actualspend,
	partner_noofdir,partner_orgtype,partner_remarks,partner_status,partner_mainstatus,
	partner_renewdate,partner_rmname,partner_addressgid,partner_contactgid,entity_gid,create_by',Query_Column,') VALUES
	(''',@code_partner,''',''',@Partner_Name,''',''',ifnull(@Partner_Panno,''),''',''',ifnull(@Partner_Compregno,''),''',''',@Partner_Group,''',',@Partner_Custcategorygid,',
	''',@Partner_Classification,''',''',@Partner_Type,''',''',ifnull(@Partner_Web,''),''',''',@Activecontract,''',
    ',if(ifnull(@Partner_Contractdatefrom,null) IS NULL,'NULL',CONCAT('''',@Partner_Contractdatefrom,'''')),',
    ',if(ifnull(@Partner_Contractdateto,null) IS NULL,'NULL',CONCAT('''',@Partner_Contractdateto,'''')),',
    ',@Partner_Aproxspend,',',@Partner_Actualspend,',
	',@Partner_Noofdir,',''',@Partner_Orgtype,''',''',ifnull(@Partner_Remarks,''),
	''',''',@Partner_Status,''',''',@Partner_Status,''',''',@Partner_Renewdate,''',
	',@Partner_Rmname,',',@Partner_Addressgid,',',@Partner_Contactgid,',',@Entity_Gid,',',@Create_By,'',Query_Value,')');

	#select  Query_Insert ,1 ;
	set @Query_Update = Query_Insert;
	PREPARE stmt FROM @Query_Update;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
	if countRow >  0 then
		set Message = 'SUCCESS';
        select LAST_INSERT_ID() into @Partnergid;
	else
		set Message = ' FAILED';
		rollback;
	end if;
	#select LAST_INSERT_ID() into @Partnergid;
    #select @Partnergid;
	select JSON_LENGTH(lj_classification,'$.DirectorName') into @li_jsonpartner_name;
	set @i=0;
	set @count1=0;
	while @i<@li_jsonpartner_name do
		select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.DirectorName[',@i,']')))into @DirectorName;
		set Query_Insert = concat('INSERT INTO atma_tmp_mst_tdirectors
				(director_partnergid,director_name,entity_gid,create_by) values
				(',@Partnergid,',''',@DirectorName,''',',@Entity_Gid,',',@Create_By,')');

		set @Query_Update = Query_Insert;
		PREPARE stmt FROM @Query_Update;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set @count1=@count1+1;
		end if;
		set @i=@i+1;
	end while;
	if @count1 = @li_jsonpartner_name then
		set Message = 'SUCCESS';

        Update gal_mst_tcodesequence
				set  codesequence_no= codesequence_no+1
				Where codesequence_type = 'partner_code';
           else
		set Message = 'FAILED';
		rollback;
	end if;
		#address  #commit;
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


     select fn_REFCode('PARTNERBRANCH_ADDRESS') into @Address_Ref_Code;

     set Query_Insert='';

	 set Query_Insert=concat('insert into atma_tmp_mst_taddress(address_ref_code,
							address_district_gid,entity_gid,create_by',Query_Column,')
								values(''',@Address_Ref_Code,''',
                                ',@Address_District_Gid,',
                                ',@Entity_Gid,',',@Create_By,'',Query_Value,')'
							);

		#select Query_Insert,2;
		set @Insert_query = Query_Insert;
		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'SUCCESS';
            select LAST_INSERT_ID() into @Address_Gid;
		else
			set Message = 'INSERT FAILED';
			rollback;
		end if;

        #select LAST_INSERT_ID() into @Address_Gid;


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

    select partner_code from atma_tmp_tpartner where partner_gid=@Partnergid
    into @Contact_RefTableCode;

	set Query_Insert='';

	set Query_Insert=concat('insert into atma_tmp_mst_tcontact
									(Contact_ref_gid,Contact_reftable_gid,contact_reftablecode,
									 Contact_contacttype_gid,Contact_designation_gid,
                                     entity_gid,create_by',Query_Column,')
						      values(',@Contact_Ref_Gid,',',@Partnergid,',''',@Contact_RefTableCode,''',
									',@Contact_ContactType_Gid,',',@Contact_Designation_Gid,',
									',@Entity_Gid,',',@Create_By,'',Query_Value,')'
                    );
  # SELECT Query_Insert,3;
	set @Insert_query = Query_Insert;

	PREPARE stmt FROM @Insert_query;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
    if countRow >  0 then
		set Message = 'SUCCESS';
		select LAST_INSERT_ID() into @Contact_Gid;
	else
		set Message = 'FAILED';
		rollback;
	end if;

     #select LAST_INSERT_ID() into @Contact_Gid;


				set Query_Update = concat('Update atma_tmp_tpartner
											set partner_addressgid = ',@Address_Gid,' ,
										    partner_contactgid = ',@Contact_Gid,'
										    Where partner_gid = ',@Partnergid,'

                                            ');
			#SELECT Query_Update,4;
			set @Insert_query = Query_Update;
			PREPARE stmt FROM @Insert_query;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;
			if countRow >  0 then
			set Message = concat(@Partnergid,',SUCCESS,',@Partner_Rmname,',',@code_partner);
            commit;
			end if;



end if;





if ls_Action='UPDATE' then
start transaction;

  select JSON_LENGTH(partner_json,'$') into @li_jsonpartner;

		if @li_jsonpartner = 0 or @li_jsonpartner is null  then
			set Message = 'No Data In Json - Update.';
			leave sp_Atma_Partner_Set;
		End if;

	if @li_jsonpartner is not null or @li_jsonpartner <> '' then

		select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Gid')))into @Partner_Gid;
		select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Address_1')))
		into @Address_1;
        select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Address_2')))
		into @Address_2;
        select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Address_3')))
		into @Address_3;
        select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Address_PinCode')))
		into @Address_PinCode;
        select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Address_District_Gid')))into @Address_District_Gid;
		select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Address_City_Gid')))into @Address_City_Gid;
		select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Address_State_Gid')))into @Address_State_Gid;
		#Contact
		select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Contact_ContactType_Gid')))into @Contact_ContactType_Gid;
		select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Contact_PersonName')))into @Contact_PersonName;
		select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Contact_Designation_Gid')))into @Contact_Designation_Gid;
		select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Contact_LandLine')))into @Contact_LandLine;
		select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Contact_LandLine2')))into @Contact_LandLine2;
		select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Contact_MobileNo')))into @Contact_MobileNo;
		select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Contact_MobileNo2')))into @Contact_MobileNo2;
		select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Contact_Email')))into @Contact_Email;
		select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Contact_DOB')))into @Contact_DOB;
		select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Contact_WD')))into @Contact_WD;

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
			leave sp_Atma_Partner_Set;
		end if;
	end if;
				 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Name')))into @Partner_Name;
				 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Panno')))into @Partner_Panno;
				 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Compregno')))into @Partner_Compregno;
				 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Group')))into @Partner_Group;
				 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Custcategorygid')))into @Partner_Custcategorygid;
				 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Classification')))into @Partner_Classification;
				 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Type')))into @Partner_Type;
				 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Web')))into @Partner_Web;
				 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Activecontract')))into @Partner_Activecontract;
				 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Reason_No_Contract')))into @Partner_Reason_No_Contract;
				 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Contractdatefrom')))into @Partner_Contractdatefrom;
				 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Contractdateto')))into @Partner_Contractdateto;
				 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Aproxspend')))into @Partner_Aproxspend;
				 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Actualspend')))into @Partner_Actualspend;
				 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Noofdir')))into @Partner_Noofdir;
				 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Orgtype')))into @Partner_Orgtype;
				 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Remarks')))into @Partner_Remarks;
				 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Status')))into @Partner_Status;
				 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Renewdate')))into @Partner_Renewdate;
				 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Rmname')))into @Partner_Rmname;
                 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Addressgid')))into @Partner_Addressgid;
				 select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Partner_Contactgid')))into @Partner_Contactgid;
				 select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Update_By')))into @Update_By;

			End if;
            #set @Partner_Addressgid=111;
			#set @Partner_Contactgid=222;
					set @RM_Name='';
					select partner_rmname from atma_tmp_tpartner where partner_gid=@Partner_Gid
                    into  @RM_Name;


					set Query_Update = '';

                    if @Partner_Gid is not null or @Partner_Gid <> '' or @Partner_Gid <> 0 then
					set @Partner_Gid=@Partner_Gid;
					end if;

                    if  @Partner_Contractdatefrom <> '' and @Partner_Contractdatefrom <> 'null' then
					set @Partner_Contractdatefrom=date_format(@Partner_Contractdatefrom,'%Y-%m-%d');
					end if;
					if  @Partner_Contractdateto <> '' and @Partner_Contractdateto <> 'null' then
					set @Partner_Contractdateto=date_format(@Partner_Contractdateto,'%Y-%m-%d');
					end if;

					if  @Partner_Contractdatefrom <> '' and @Partner_Contractdateto<>'' and @Partner_Contractdatefrom <> 'null'
                    and @Partner_Contractdateto <> 'null' then
					if @Partner_Contractdatefrom >=@Partner_Contractdateto then
					set Message ='To date should be greater than From date ';
					rollback;
					leave sp_Atma_Partner_Set;
					end if;
					end if;

				set @Partner_Renewdate=date_format(@Partner_Renewdate,'%Y-%m-%d');
               # if @Partner_Renewdate <=@Partner_Contractdatefrom then
				#set Message =' Renewdate should be greater than Contract from date';
				#rollback;
				#leave sp_Atma_Partner_Set;
                #end if;

				if @Partner_Activecontract='No' then
				set @Activecontract='N';
                elseif @Partner_Activecontract='Yes' then
                set @Activecontract='Y';
                end if;


			#set@partner_nm='';
			#select  count(partner_name) from atma_tmp_tpartner
			#where partner_name=@Partner_Name and partner_gid <> @Partner_Gid  into @partner_nm;

			#select main_partner_gid from atma_tmp_tpartner where partner_gid=@Partner_Gid into @chkmainpartnergid;
          /*
			select count(partner_name)
			from atma_mst_tpartner
			where partner_name=@Partner_Name  into @Duplicate_Check_Name;

			if @Duplicate_Check_Name > 0 then
			set Message ='Partner Name Already Exist mst ';
            leave sp_Atma_Partner_Set;
			end if;
	*/
			#if  @partner_nm > 0 then
			#set Message ='Partner Name Already Exist tmp';
			#rollback;
			#leave sp_Atma_Partner_Set;
			#end if;

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
				leave sp_Atma_Partner_Set;
			End if;

            if lower(@Address_City_Gid) <> 'null' and @Address_City_Gid <> '' then
				set Query_Update = concat(Query_Update,',address_city_gid = ',@Address_City_Gid,'  ');
			else
				set Message='Address_City can not be null' ;
				leave sp_Atma_Partner_Set;
			End if;

            if lower(@Address_State_Gid) <> 'null' and @Address_State_Gid <> '' then
				set Query_Update = concat(Query_Update,',address_state_gid = ',@Address_State_Gid,'  ');
			else
				set Message='Address_State can not be null' ;
				leave sp_Atma_Partner_Set;
			End if;

            if @Update_By is not null or @Update_By <> '' then
				set Query_Update = concat(Query_Update,',Update_By = ',@Update_By,'  ');
			End if;
           select partner_addressgid from atma_tmp_tpartner
            where partner_gid=@Partner_Gid into @Address_Gid;


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
				leave sp_Atma_Partner_Set;
			elseif    countRow > 0 then
				set Message = 'SUCCESSFULLY UPDATED';

		    end if;

              set Query_Update ='';


            if lower(@Contact_ContactType_Gid) <> 'null' and @Contact_ContactType_Gid <> '' then
				set Query_Update = concat(Query_Update,',Contact_contacttype_gid = ',@Contact_ContactType_Gid,'  ');
			else
                set Message='Contact_ContactType can not be null' ;
				leave sp_Atma_Partner_Set;
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
				leave sp_Atma_Partner_Set;
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

             select partner_contactgid from atma_tmp_tpartner
			 where partner_gid=@Partner_Gid into @Contact_Gid;
        #select @Contact_Gid;
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
				leave sp_Atma_Partner_Set;
			elseif    countRow > 0 then
				set Message = 'SUCCESSFULLY UPDATED';

		end if;


#####partner_page
				set Query_Update1='';

					if @Partner_Name <>'null' and @Partner_Name <> ''  then

						set Query_Update1 = concat(Query_Update1, ',Partner_Name = ''',@Partner_Name,''' ');
					else
						set Message='Please Enter The Partner Name ' ;
						leave sp_Atma_Partner_Set;
					End if;



					if @Partner_Panno <>'null' and @Partner_Panno <> '' then

						set Query_Update1 = concat(Query_Update1,',Partner_Panno = ''',@Partner_Panno,'''  ');
					else
						set Query_Update1 = concat(Query_Update1,',Partner_Panno = null  ');
					End if;



                    if @partner_compregno <>'null' and @partner_compregno <> '' then

						set Query_Update1 = concat(Query_Update1,',partner_compregno = ''',@partner_compregno,'''  ');
					else
						set Query_Update1 = concat(Query_Update1,',partner_compregno = null  ');

					End if;

                    if @Partner_Group <>'null' and @Partner_Group <> '' then

						set Query_Update1 = concat(Query_Update1,',Partner_Group = ''',@Partner_Group,'''  ');
					else
						set Message='please Enter The Partner Group' ;
						leave sp_Atma_Partner_Set;
					End if;

                    if @Partner_Custcategorygid  <>'null' and @Partner_Custcategorygid <> '' then

						set Query_Update1 = concat(Query_Update1,',Partner_Custcategorygid = ',@Partner_Custcategorygid,'  ');
					else
						set Message='Please Enter The Custcategory' ;
						leave sp_Atma_Partner_Set;
					End if;

                    if @Partner_Classification <>'null' and @Partner_Classification <> '' then

						set Query_Update1 = concat(Query_Update1,',Partner_Classification = ''',@Partner_Classification,'''  ');
					else
						set Message='Please Enter The Partner Classification ' ;
						leave sp_Atma_Partner_Set;
					End if;


					if @Partner_Type <>'null' and @Partner_Type <> '' then

						set Query_Update1 = concat(Query_Update1,',Partner_Type = ''',@Partner_Type,'''  ');
					else
						set Message='Partner Type can not be null' ;
						leave sp_Atma_Partner_Set;
					End if;

                    if @Activecontract <>'null' and @Activecontract <> '' then

						set Query_Update1 = concat(Query_Update1,',Partner_Activecontract = ''',@Activecontract,'''  ');
					else
						set Message='Please Enter The Partner Activecontrac ' ;
						leave sp_Atma_Partner_Set;
					End if;

					if @Partner_Web <>'null' and @Partner_Web <> '' then

						set Query_Update1 = concat(Query_Update1,',Partner_Web = ''',@Partner_Web,'''  ');
					else
						set Query_Update1 = concat(Query_Update1,',Partner_Web = null  ');

					End if;

					if @Partner_Reason_No_Contract <>'null' and @Partner_Reason_No_Contract <> '' then

						set Query_Update1 = concat(Query_Update1,',Partner_Reason_No_Contract = ''',@Partner_Reason_No_Contract,'''  ');
					else
						set Query_Update1 = concat(Query_Update1,',Partner_Reason_No_Contract = null  ');

					End if;

					if @Partner_Contractdatefrom <>'null' and @Partner_Contractdatefrom <> '' then

						set Query_Update1 = concat(Query_Update1,',Partner_Contractdatefrom = ''',@Partner_Contractdatefrom,'''  ');
					else
						set Query_Update1 = concat(Query_Update1,',Partner_Contractdatefrom = null  ');
					End if;

					if @Partner_Contractdateto <>'null' and @Partner_Contractdateto <> '' then

						set Query_Update1 = concat(Query_Update1,',Partner_Contractdateto = ''',@Partner_Contractdateto,'''  ');
					else
						set Query_Update1 = concat(Query_Update1,',Partner_Contractdateto = null  ');
					End if;

					if @Partner_Aproxspend <>'null' and @Partner_Aproxspend <> '' then

						set Query_Update1 = concat(Query_Update1,',Partner_Aproxspend = ',@Partner_Aproxspend,'  ');
					else
						set Message=' Please Enter The Partner Aproxspend ' ;
						leave sp_Atma_Partner_Set;
					End if;

					if @Partner_Actualspend <>'null' and @Partner_Actualspend <> '' then
						set Query_Update1 = concat(Query_Update1,',Partner_Actualspend = ',@Partner_Actualspend,'  ');
					else
						set Message=' Please Enter The Partner Actualspend ' ;
						leave sp_Atma_Partner_Set;
					End if;

					if @Partner_Noofdir <>'null' and @Partner_Noofdir <> '' then
						set Query_Update1 = concat(Query_Update1,',Partner_Noofdir = ',@Partner_Noofdir,'  ');
                    else
						set Message='Please Enter The Partner Noofdir ' ;
						leave sp_Atma_Partner_Set;
					End if;

					if @Partner_Orgtype <>'null' and @Partner_Orgtype <> '' then
						set Query_Update1 = concat(Query_Update1,',Partner_Orgtype = ''',@Partner_Orgtype,'''  ');
                    else
						set Message='Please Enter The Partner Orgtype ' ;
						leave sp_Atma_Partner_Set;
					End if;

					if @Partner_Remarks <>'null' and @Partner_Remarks <> '' then
						set Query_Update1 = concat(Query_Update1,',Partner_Remarks = ''',@Partner_Remarks,'''  ');
					else
						set Query_Update1 = concat(Query_Update1,',Partner_Remarks = null  ');
					End if;

					if @Partner_Status <>'null' and @Partner_Status <> '' then
						set Query_Update1 = concat(Query_Update1,',Partner_Status = ''',@Partner_Status,'''  ');
						set Query_Update1 = concat(Query_Update1,',Partner_mainStatus = ''',@Partner_Status,'''  ');

					End if;

					if @Partner_Renewdate <>'null' and @Partner_Renewdate <> '' then
						set Query_Update1 = concat(Query_Update1,',Partner_Renewdate = ''',@Partner_Renewdate,'''  ');
					 else
						set Message='Please Enter The Partner Renewdate' ;
						leave sp_Atma_Partner_Set;
					End if;

					if @Partner_Rmname <>'null' and @Partner_Rmname <> '' then
						set Query_Update1 = concat(Query_Update1,',Partner_Rmname = ',@Partner_Rmname,' ');
					#else
						#set Message='Please Enter The Partner Rmname ' ;
						#leave sp_Atma_Partner_Set;
					End if;

                    if @Partner_Addressgid <>'null' and @Partner_Addressgid <> '' then
						set Query_Update1 = concat(Query_Update1,',partner_addressgid = ',@Partner_Addressgid,' ');
					End if;

                    if @Partner_Contactgid <>'null' and @Partner_Contactgid <> '' then
						set Query_Update1 = concat(Query_Update1,',partner_contactgid = ',@Partner_Contactgid,' ');
					End if;

					if @Update_By is not null or @Update_By <> '' then

						set Query_Update1 = concat(Query_Update1,',Update_By = ',@Update_By,'  ');

					End if;
                    #select Query_Update1;

		set Query_Insert = concat('Update atma_tmp_tpartner

                         set update_date = CURRENT_TIMESTAMP ',Query_Update1,'

                            Where partner_gid = ',@Partner_Gid,'

							and partner_isactive = ''Y'' and partner_isremoved = ''N'' ');


		#select Query_Insert,1;
		set @Query_Update = '';

		set @Query_Update = Query_Insert;

		PREPARE stmt FROM @Query_Update;

		EXECUTE stmt;

		set countRow = (select ROW_COUNT());

		DEALLOCATE PREPARE stmt;



		if countRow <= 0 then

				set Message = 'Error On .';

				rollback;

				leave sp_Atma_Partner_Set;

		elseif    countRow > 0 then


    select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Entity_Gid')))into @Entity_Gid;
	select JSON_UNQUOTE(JSON_EXTRACT(partner_json,CONCAT('$.Create_By')))into @Create_By;

		SET SQL_SAFE_UPDATES = 0;
		update atma_tmp_mst_tdirectors set  director_isactive='N',director_isremoved='Y' where
		director_isactive='Y' and director_isremoved='N' and director_partnergid=@Partner_Gid;

    select JSON_LENGTH(lj_classification,'$.DirectorName') into @li_jsonpartner_name;
        set @i=0;
        set @count1=0;
        while @i<@li_jsonpartner_name do
			select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.DirectorName[',@i,']')))into @DirectorName;

            set Query_Insert= '';

            set Query_Insert = concat('INSERT INTO atma_tmp_mst_tdirectors
					(director_partnergid,director_name,entity_gid,create_by) values
					(',@Partner_Gid,',''',@DirectorName,''',',@Entity_Gid,',',@Create_By,')');

            set @Query_Update = Query_Insert;
			PREPARE stmt FROM @Query_Update;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;
            if countRow >  0 then
				set @count1=@count1+1;
			end if;
			set @i=@i+1;
        end while;

               select partner_code from atma_tmp_tpartner
               where partner_gid=@Partner_Gid  into @pt_gid;

			if @count1 = @li_jsonpartner_name then

                set Message =  concat(@Partner_Gid,',SUCCESS,',@RM_Name,',',@pt_gid);

			else
				set Message = 'Error On Update.';
				rollback;
			end if;
    #set Message = 'SUCCESS';
			commit;
		end if;	###update elseif    countRow > 0 then


	end if;




END