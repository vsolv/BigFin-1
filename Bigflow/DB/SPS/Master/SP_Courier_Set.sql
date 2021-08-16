CREATE PROCEDURE `galley`.`sp_Courier_Set`( IN `ls_Action` varchar(32),
IN `ls_Type` varchar(32),IN `ls_Sub_Type` varchar(32),
IN `lj_Details` json,IN `lj_Classification` json,IN `ls_Createby` varchar(32), OUT `Message` varchar(1000))
SP_Courier_Set:BEGIN
declare Query_Insert varchar(1000);
declare errno int;
declare countRow int;
declare msg varchar(1000);


	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
		GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
		set Message = concat(errno , msg);
		ROLLBACK;
	END;

       select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid[0]'))) into @Entity_Gid;

             if @Entity_Gid is  null or @Entity_Gid = 0 or @Entity_Gid = '' then
					set Message = 'Entity Gid Is Needed.';
                    leave SP_Courier_Set;
             End if;
start transaction;
set autocommit = 0 ;
    if ls_Type = 'COURIER_SET'  then

      select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.COURIER[0].Courier_Name'))) into @Courier_Name;
	  select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.COURIER[0].Courier_Type'))) into @Courier_Type;
	  select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.COURIER[0].Courier_ContactPerson'))) into @Courier_ContactPerson;

	  select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.ADDRESS[0].Add1'))) into @Add1;
	  select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.ADDRESS[0].Add2'))) into @Add2;
	  select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.ADDRESS[0].Add3'))) into @Add3;
	  select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.ADDRESS[0].Pincode'))) into @Pincode;
	  select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.ADDRESS[0].State_Gid'))) into @State_Gid;
	  select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.ADDRESS[0].District_Gid'))) into @District_Gid;
	  select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.ADDRESS[0].City_Gid'))) into @City_Gid;


	   select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.CONTACT[0].ContactType_Gid'))) into @ContactType_Gid;
	   select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.CONTACT[0].Person_Name'))) into @Person_Name;
	   select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.CONTACT[0].Designation_Gid'))) into @Designation_Gid;
	   select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.CONTACT[0].LandLine_1'))) into @LandLine_1;
	   select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.CONTACT[0].LandLine_2'))) into @LandLine_2;
	   select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.CONTACT[0].Mobile_1'))) into @Mobile_1;
	   select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.CONTACT[0].Mobile_2'))) into @Mobile_2;
	   select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.CONTACT[0].Email'))) into @Email;
	   select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.CONTACT[0].Dob'))) into @Dob;
	   select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.CONTACT[0].WD'))) into @WD;

	   ### Validations To DO

	   if @Courier_Name is null or @Courier_Name = '' THEN
	     set Message = 'Courier Name Is Needed.';
	     leave SP_Courier_Set;
	   End if;

	  if @Courier_Type is null or @Courier_Type = '' then
	     set Message = 'Courier Type Is Needed.';
	     leave SP_Courier_Set;
     end if;

     if @Courier_ContactPerson is null or @Courier_ContactPerson = '' THEN
       set Message = 'Courier Contcat Person Is Needed.';
       leave SP_Courier_Set;
     End if;

    #### Courier Name Duplicate

    set @Courier_gidDB = 0 ;

    select ifnull(courier_gid,0)  into @Courier_gidDB from dis_mst_tcourier where courier_name = @Courier_Name;
   select ifnull(courier_gid,0)  into @Courier_CPDB from dis_mst_tcourier where courier_contactperson = @Courier_ContactPerson;

     if @Courier_gidDB <> 0 then
       set Message = 'Courier Name Is Duplicate.';
       leave  SP_Courier_Set;
     End if;

    if @Courier_CPDB <> 0 then
        set Message = 'Courier Contact Person Is Duplicate.';
       leave  SP_Courier_Set;
    End if;


      select ifnull(max(courier_code),0) into @courier_code_db from dis_mst_tcourier ;

      call sp_Generatecode_Get('WITHOUT_DATE','COU','00',@courier_code_db,@Message);
      select @Message into @Courier_Code ;

     if @Courier_Code is null or @Courier_Code = '' THEN
       set Message = 'Courier Code Is Needed.';
       leave SP_Courier_Set;
     End if;

     set  Query_Insert = '';
     set Query_Insert = concat('insert into dis_mst_tcourier (courier_type,courier_code,courier_name,courier_contactperson,
               entity_gid,create_by)
               values(''',@Courier_Type,''',''',@Courier_Code,''',''',@Courier_Name,''',''',@Courier_ContactPerson,''',''',@Entity_Gid,''',
              ''',ls_Createby,'''
                )');

				               set @Insert_query = Query_Insert;
								#SELECT @Insert_query;
								PREPARE stmt FROM @Insert_query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;

							  if countRow > 0 then
									select LAST_INSERT_ID() into @Last_Courier_Id;
                                    set Message = 'SUCCESS';
							   else
									set Message = 'FAIL';
                                    leave SP_Courier_Set;
							  End if;

			call sp_Address_Set('Insert',0,'COURIER',@Add1,@Add2,@Add3,@Pincode,@District_Gid,
		     @City_Gid,@State_Gid,@Entity_Gid,ls_Createby,@Message);
			select @Message into @Out_Message_Address;

		   select SUBSTRING_INDEX(@Out_Message_Address,',',1) into @out_msg_Add;


	       if @out_msg_Add = 'FAIL' or @out_msg_Add = 0  THEN
	          set Message = concat('Error on Address Insert.-',@Out_Message_Address);
	          rollback;
	          leave SP_Courier_Set;
	       elseif  @out_msg_Add is null then
	          set Message = 'Error on Address Insert';
	          rollback;
	          leave SP_Courier_Set;
	       End if;

			select SUBSTRING_INDEX(@Out_Message_Address,',',1) into @add_max_gid;

		   ### TO DO No Hard Code
		   	call sp_Contact_Set('Insert',0,'COURIER',44,@ContactType_Gid,@Person_Name,@Designation_Gid,@LandLine_1,
		   	@LandLine_2, @Mobile_1,@Mobile_2,
			@Email,@Dob,@WD,@Entity_gid,ls_Createby,@Message);
			select @Message into @Out_Message_Contact;
		   select SUBSTRING_INDEX(@Out_Message_Contact,',',1) into @contact_max_gid;


		    select SUBSTRING_INDEX(@Out_Message_Contact,',',1) into @out_msg_Con;

	       if @out_msg_Con = 'FAIL' or @out_msg_Add = 0  THEN
	          set Message = concat('Error on Contcat Insert.-',@out_msg_Con);
	          rollback;
	          leave SP_Courier_Set;
	       elseif  @out_msg_Con is null then
	          set Message = 'Error on Contact Insert';
	          rollback;
	          leave SP_Courier_Set;
	       End if;


		  update dis_mst_tcourier set courier_addressgid = @add_max_gid,courier_contactgid = @contact_max_gid
		  where courier_gid = @Last_Courier_Id;

		  set countRow = (select ROW_COUNT());

        		  if countRow > 0 then
                        set Message = 'SUCCESS';
				   else
						set Message = 'FAIL';
                            leave SP_Courier_Set;
					  End if;


End if;

if Message = 'SUCCESS' then
	commit;
else
    rollback;
    set Message = concat('FAIL-',Message);
End if;


END