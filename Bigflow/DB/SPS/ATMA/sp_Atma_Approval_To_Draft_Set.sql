CREATE  PROCEDURE `sp_Atma_Approval_To_Draft_Set`(in li_Action  varchar(30),
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_Atma_Approval_To_Draft_Set:BEGIN
Declare Query_Insert varchar(10000);
Declare countRow varchar(6000);
Declare Query_Update varchar(10000);
Declare Query_delete varchar(1000);
Declare Query_Value varchar(1000);
Declare Query_Column varchar(1000);
Declare v_director_gid,v_director_partnergid,v_director_name,v_director_isactive,v_director_isremoved,
v_create_by,v_entity_gid	varchar(128) ;
Declare  a_address_gid,a_address_ref_code,a_address_1,a_address_2,a_address_3,a_address_pincode,
		 a_address_district_gid,a_address_city_gid,a_address_state_gid,a_entity_gid,
         a_create_by,a_update_by,a_main_address_gid varchar(150);
Declare  c_contact_gid,c_Contact_ref_gid,c_Contact_reftable_gid,
		 c_contact_reftablecode,c_Contact_contacttype_gid,
		 c_Contact_personname,c_Contact_designation_gid,c_Contact_landline,
		 c_Contact_landline2,c_Contact_mobileno,
		 c_Contact_mobileno2,c_Contact_email,c_Contact_DOB,c_Contact_WD,
		 c_entity_gid,c_create_by,c_update_by,c_main_contact_gid varchar(150);
DECLARE finished INTEGER DEFAULT 0;
Declare errno int;
Declare msg,Error_Level varchar(1000);

DECLARE EXIT HANDLER FOR SQLEXCEPTION
BEGIN
	GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
	set Message = concat(Error_Level,' : No-',errno , msg);
	ROLLBACK;
END;

IF li_Action='Approval_To_Draft_Set' then

	START TRANSACTION;

	select JSON_LENGTH(lj_filter,'$') into @lj_filter_json_count;
	select JSON_LENGTH(lj_classification,'$') into @lj_classification_json_count;

		if @lj_filter_json_count = 0 or @lj_filter_json_count is null then
		set Message = 'No Data In filter Json. ';
	leave sp_Atma_Approval_To_Draft_Set;
	End if;

	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Gid'))) into @Partner_Gid;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Status')))	into @Partner_Status;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Requestfor')))	into @Partner_Requestfor;
  	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Tran_Remarks'))) into @Tran_Remarks;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Entity_Gid')))	into @Entity_Gid;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Create_By')))	into @Create_By;

	####address
	SELECT partner_addressgid,partner_contactgid into @partneraddressgid,@partnercontactgid
           FROM atma_mst_tpartner where Partner_Gid=@Partner_Gid;

    select  address_gid,address_ref_code,address_1,address_2,address_3,address_pincode,
			address_district_gid,address_city_gid,address_state_gid,entity_gid,
			create_by,update_by
	into a_address_gid,a_address_ref_code,a_address_1,a_address_2,a_address_3,
		 a_address_pincode,a_address_district_gid,a_address_city_gid,
		 a_address_state_gid,a_entity_gid,a_create_by ,a_update_by
	from gal_mst_taddress where address_gid=@partneraddressgid ;



    set Query_Column='';
	set Query_Value ='';

	if a_address_1 is not null and a_address_1 <> '' then
		set Query_Column = concat(Query_Column,',address_1 ');
		set Query_Value=concat(Query_Value,', ''',a_address_1,''' ');
	end if;

    if a_address_2 is not null and a_address_2 <> ''  then
		set Query_Column = concat(Query_Column,',address_2 ');
		set Query_Value=concat(Query_Value,', ''',a_address_2,''' ');
	end if;

    if a_address_3 is not null and a_address_3 <> '' then
		set Query_Column = concat(Query_Column,',address_3 ');
		set Query_Value=concat(Query_Value,', ''',a_address_3,''' ');
	end if;

    if a_address_pincode is not null and a_address_pincode <> '' then
		set Query_Column = concat(Query_Column,',address_pincode ');
		set Query_Value=concat(Query_Value,', ',a_address_pincode,' ');
	end if;

	if a_address_city_gid is not null and a_address_city_gid <> '' then
		set Query_Column = concat(Query_Column,',address_city_gid ');
		set Query_Value=concat(Query_Value,', ',a_address_city_gid,' ');
	end if;

	if a_address_state_gid is not null and a_address_state_gid <> '' then
		set Query_Column = concat(Query_Column,',address_state_gid ');
		set Query_Value=concat(Query_Value,', ',a_address_state_gid,' ');
	end if;

    set Error_Level='ATMA16.1';
	set Query_Update = concat('INSERT INTO  atma_tmp_mst_taddress
									  ( address_ref_code,address_district_gid,
                                        entity_gid, create_by, create_date,main_address_gid ',Query_Column,')
							    values (''',a_address_ref_code,''',',a_address_district_gid,',
										',a_entity_gid,',',a_create_by,',
                                        ''',Now(),''',',a_address_gid,'
										',Query_Value,')'
							  );


        #select Query_Update,'ADD';
	set @Insert_query = Query_Update;
	PREPARE stmt FROM @Insert_query;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
	if countRow >  0 then
		set Message = 'SUCCESS';
	else
		set Message = ' FAILED_BR';
		leave sp_Atma_Approval_To_Draft_Set;
	end if;


	set @Address_Gid='';
    select last_insert_id() into @Address_Gid;

	#######contact
				select  contact_gid,Contact_ref_gid,Contact_reftable_gid,
						contact_reftablecode,Contact_contacttype_gid,
						Contact_personname,Contact_designation_gid,Contact_landline,
						Contact_landline2,Contact_mobileno,
						Contact_mobileno2,Contact_email,Contact_DOB,Contact_WD,
						entity_gid,create_by,update_by
                        into c_contact_gid,c_Contact_ref_gid,c_Contact_reftable_gid,
							 c_contact_reftablecode,c_Contact_contacttype_gid,
							 c_Contact_personname,c_Contact_designation_gid,c_Contact_landline,
							 c_Contact_landline2,c_Contact_mobileno,
							 c_Contact_mobileno2,c_Contact_email,c_Contact_DOB,c_Contact_WD,
							 c_entity_gid,c_create_by,c_update_by
						from  gal_mst_tcontact
                        where contact_gid=@partnercontactgid ;


				 set Query_Column='';
				 set Query_Value ='';

            if c_Contact_personname is not null and c_Contact_personname<>'' then
				set Query_Column = concat(Query_Column,',Contact_personname');
				set Query_Value=concat(Query_Value,', ''',c_Contact_personname,''' ');
            end if;

            if c_Contact_landline is not null and c_Contact_landline <>'' then
				set Query_Column = concat(Query_Column,',Contact_landline');
				set Query_Value=concat(Query_Value,', ',c_Contact_landline,' ');
            end if;

            if c_Contact_landline2 is not null and c_Contact_landline2 <>'' then
				set Query_Column = concat(Query_Column,',Contact_landline2');
				set Query_Value=concat(Query_Value,', ',c_Contact_landline2,' ');
            end if;

            if c_Contact_mobileno is not null and c_Contact_mobileno <>'' then
				set Query_Column = concat(Query_Column,',Contact_mobileno');
				set Query_Value=concat(Query_Value,', ',c_Contact_mobileno,' ');
            end if;

			if c_Contact_mobileno2 is not null and c_Contact_mobileno2 <>'' then
				set Query_Column = concat(Query_Column,',Contact_mobileno2');
				set Query_Value=concat(Query_Value,', ',c_Contact_mobileno2,' ');
            end if;

            if c_Contact_email is not null  and c_Contact_email <>'' then
				set Query_Column = concat(Query_Column,',Contact_email');
				set Query_Value=concat(Query_Value,', ''',c_Contact_email,''' ');
            end if;

            if c_Contact_DOB is not null and c_Contact_DOB <>'' then
				set Query_Column = concat(Query_Column,',Contact_DOB');
				set Query_Value=concat(Query_Value,', ''',c_Contact_DOB,''' ');
            end if;

            if c_Contact_WD is not null  and c_Contact_WD <>'' then
				set Query_Column = concat(Query_Column,',Contact_WD');
				set Query_Value=concat(Query_Value,', ''',c_Contact_WD,''' ');
            end if;

            #select Query_Column;
            #select Query_Value;
            set Error_Level='ATMA16.2';
			set Query_Update = concat('INSERT INTO  atma_tmp_mst_tcontact
											  ( Contact_ref_gid,Contact_reftable_gid,contact_reftablecode,
                                              Contact_contacttype_gid,Contact_designation_gid,
                                              entity_gid,create_by,create_date,main_contact_gid
                                              ',Query_Column,')
									    values (',c_Contact_ref_gid,',',c_Contact_reftable_gid,',
												''',c_contact_reftablecode,''',',c_Contact_contacttype_gid,',
												',c_Contact_designation_gid,',',c_entity_gid,',',c_create_by,' ,
												''',Now(),''',',c_contact_gid,'
                                                ',Query_Value,')'
									 );




        #select Query_Update,'CON';
		set @Insert_query = Query_Update;
		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'SUCCESS';
		else
			set Message = ' FAILED_BR';
			leave sp_Atma_Approval_To_Draft_Set;
		end if;


			set @Contact_Gid='';
            select last_insert_id() into @Contact_Gid;


	set Error_Level='ATMA16.3';
	set Query_Insert='';

	set Query_Insert=concat('INSERT INTO atma_tmp_tpartner (partner_code,partner_name,partner_panno,partner_compregno,partner_group,
					partner_custcategorygid,partner_compositevendor,
					partner_Classification,partner_type,partner_web,partner_activecontract,partner_reason_no_contract,partner_contractdatefrom,
					partner_contractdateto,partner_aproxspend,partner_actualspend,partner_noofdir,partner_orgtype,partner_renewaldate,partner_remarks,
					partner_requestfor,partner_status,partner_mainstatus,partner_renewdate,partner_rmname,
                    partner_addressgid,partner_contactgid,partner_isactive,partner_isremoved,entity_gid,
					create_by,create_date,update_by,update_date,main_partner_gid)
				SELECT partner_code,partner_name,partner_panno,partner_compregno,partner_group,
                    partner_custcategorygid,partner_compositevendor,partner_Classification,partner_type,partner_web,partner_activecontract,partner_reason_no_contract,partner_contractdatefrom,
					partner_contractdateto,partner_aproxspend,partner_actualspend,partner_noofdir,partner_orgtype,partner_renewaldate,partner_remarks,
					''',@Partner_Requestfor,''',''',@Partner_Status,''',partner_mainstatus,partner_renewdate,partner_rmname,
                     ',@Address_Gid,',',@Contact_Gid,',partner_isactive,partner_isremoved,entity_gid,
					create_by,create_date,update_by,update_date,',@Partner_Gid,' FROM atma_mst_tpartner
					where Partner_Gid=',@Partner_Gid,' ');





	set @Insert_query = Query_Insert;
	PREPARE stmt FROM @Insert_query;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
    if countRow >  0 then
		set Message = 'SUCCESS';
	else
		set Message = 'INSERT FAILED PARTNER';
		rollback;
        leave sp_Atma_Approval_To_Draft_Set;
	end if;


	set @NEWPartnergid='';
	select LAST_INSERT_ID() into @NEWPartnergid;



BEGIN
	Declare Cursor_atma CURSOR FOR

					select director_gid,director_partnergid,director_name,director_isactive,director_isremoved,create_by,entity_gid
					from atma_mst_tdirectors
					where director_partnergid=@Partner_Gid ;

	DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;
					OPEN Cursor_atma;
					atma_looop:loop
					fetch Cursor_atma into v_director_gid,v_director_partnergid,v_director_name,v_director_isactive,v_director_isremoved,v_create_by,v_entity_gid;
					if finished = 1 then
					leave atma_looop;
					End if;
                             set Error_Level='ATMA16.4';
	set Query_Insert = concat('INSERT INTO atma_tmp_mst_tdirectors (director_partnergid,director_name,director_isactive,
							   director_isremoved,create_by,entity_gid,main_director_gid)
                               values (', @NEWPartnergid,',''',v_director_name,''',''',v_director_isactive,''',''',v_director_isremoved,''',
                               ',v_create_by,',',v_entity_gid,',',v_director_gid,')');


		set @Insert_query = Query_Insert;
		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'SUCCESS';
		else
			set Message = ' FAILED PARTNER_DIR';
			rollback;
            leave sp_Atma_Approval_To_Draft_Set;
		end if;
End loop atma_looop;
close Cursor_atma;
end;

call sp_Atma_Approval_To_Draft_PR_Profile_Set(lj_filter,@NEWPartnergid,lj_classification,@Message);
			select @Message into @Out_Message_profile;

			if  @Out_Message_profile <> 'SUCCESS' then
					set Message = @Out_Message_profile;
					rollback;
					leave sp_Atma_Approval_To_Draft_Set;
			End if;



call sp_Atma_Approval_To_Draft_PR_Client_Set(lj_filter,@NEWPartnergid,lj_classification,@Message);
			select @Message into @Out_Message_Client;

			if  @Out_Message_Client <> 'SUCCESS' then
					set Message = @Out_Message_Client;
					rollback;
					leave sp_Atma_Approval_To_Draft_Set;
			End if;

call sp_Atma_Approval_To_Draft_PR_Product_Set(lj_filter,@NEWPartnergid,lj_classification,@Message);
			select @Message into @Out_Message_Product;

			if  @Out_Message_Product <> 'SUCCESS' then
					set Message = @Out_Message_Product;
					rollback;
					leave sp_Atma_Approval_To_Draft_Set;
			End if;



call sp_Atma_Approval_To_Draft_PR_Contractor_Set(lj_filter,@NEWPartnergid,lj_classification,@Message);
			select @Message into @Out_Message_partnercontractor;

			if  @Out_Message_partnercontractor <> 'SUCCESS' then
					set Message = @Out_Message_partnercontractor;
					rollback;
					leave sp_Atma_Approval_To_Draft_Set;
			End if;



call sp_Atma_Approval_To_Draft_Taxdetails_Set('Insert',lj_filter,lj_classification,@Message);
			select @Message into @Out_Message_Taxdetails;

			if  @Out_Message_Taxdetails <> 'SUCCESS' then
					set Message = @Out_Message_Taxdetails;
					rollback;
					leave sp_Atma_Approval_To_Draft_Set;
			End if;

call sp_Atma_Approval_To_Draft_Document_Set('Insert',lj_filter,@NEWPartnergid,lj_classification,@Message);
			select @Message into @Out_Message_Document;

			if  @Out_Message_Document <> 'SUCCESS' then
					set Message = @Out_Message_Document;
					rollback;
					leave sp_Atma_Approval_To_Draft_Set;
			End if;

 call sp_Atma_Approval_To_Draft_PR_Branch_Set(lj_filter,@NEWPartnergid,lj_classification,@Message);
			select @Message into @Out_Message_Branch;

			if  @Out_Message_Branch <> 'SUCCESS' then
					set Message = @Out_Message_Branch;
					rollback;
					leave sp_Atma_Approval_To_Draft_Set;
			End if;


				update atma_mst_tpartner set
				partner_status='APPROVED'
				where partner_gid=@Partner_Gid and partner_status='APPROVED-VIEW';

			set Message ='SUCCESS';
            commit;


          set @RM_TO_tran='';
        select partner_rmname from atma_mst_tpartner
        where partner_gid=@Partner_Gid into @RM_TO_tran;

        	call sp_Trans_Set('DRAFT_TO_PENDING','PARTNER_NAME_TRAN',@NEWPartnergid,
								 @Partner_Status,'I',@RM_TO_tran,@Tran_Remarks,
								 @Entity_Gid,@Create_By,@message);

				select @message into @out_msg_tran ;

				if @out_msg_tran = 'FAIL' then
					set Message = 'Failed On Tran Insert';
					rollback;
					leave sp_Atma_Approval_To_Draft_Set;
				else
					commit;
				End if;

end if;
END