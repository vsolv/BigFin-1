CREATE  PROCEDURE `sp_SupplierSPS_Set`(IN `Action` varchar(32),IN `lj_supplier` json,
IN `lj_address` json,IN `lj_contact` json,IN `lj_classification` json,OUT `Message` varchar(1000))
sp_SupplierSPS_Set:BEGIN
declare Query_Insert varchar(1000);
declare Query_Column varchar(1000);
declare Query_Value varchar(1000);
declare Query_Update varchar(1000);
declare ls_error varchar(100);
declare countRow int;
declare errno int;
declare msg varchar(1000);
### Santhosh
#### Ramesh Nov Kvb 2019
DECLARE EXIT HANDLER FOR SQLEXCEPTION
BEGIN
	GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
	set Message = concat(errno , msg);
	ROLLBACK;
END;

		select JSON_LENGTH(lj_classification,'$')into @li_classification_count;

		if  @li_classification_count is not null or @li_classification_count <> ''then
		   select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Entity_Gid'))) into @Entity_gid;
		   select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Entity_Detail_Gid'))) into @Entity_Detail_Gid;
		   select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Create_By'))) into @Create_by;

		   if @Entity_gid ='' or @Entity_gid =0 then
				set Message='Entity gid is Empty';
				leave sp_SupplierSPS_Set;
		   end if;
	  else
		  set Message='Classification Json is Empty';
		  leave sp_SupplierSPS_Set;
	  end if;

if Action='SUPP_INSERT' OR Action = 'SUPPLIER_GROUP_INSERT' then

	select JSON_LENGTH(lj_supplier,'$') into @li_supplier_count;
	select JSON_LENGTH(lj_contact,'$')into @li_contact_count;
	select JSON_LENGTH(lj_address,'$')into @li_address_count;

	select lj_supplier,lj_contact,lj_address,lj_classification,Action;
	if @li_address_count is not null or @li_address_count <>'' then
		select JSON_UNQUOTE(JSON_EXTRACT(lj_address,CONCAT('$.supplier_add_gid'))) into @supplier_add_gid;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_address,CONCAT('$.Address1'))) into @address1;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_address,CONCAT('$.Address2'))) into @address2;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_address,CONCAT('$.Address3'))) into @address3;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_address,CONCAT('$.Pincode'))) into @pincode;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_address,CONCAT('$.District_Gid'))) into @district_gid;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_address,CONCAT('$.City_Gid'))) into @city_gid;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_address,CONCAT('$.State_Gid'))) into @state_gid;

		if @supplier_add_gid is not null and @supplier_add_gid<>'0' then
			set @add_max_gid=@supplier_add_gid;
		else
			call sp_Address_Set('Insert',0,'SUPPLIER',@address1,@address2,@address3,@pincode,@district_gid,@city_gid,@state_gid,@Entity_gid,@Create_by,@Message);
			select @Message into @Out_Message_Address;
			select SUBSTRING_INDEX(@Out_Message_Address,',',1) into @add_max_gid;
		end if;
	end if;
	if  @li_contact_count is not null or @li_contact_count <>'' then
		select JSON_UNQUOTE(JSON_EXTRACT(lj_contact,CONCAT('$.supplier_contact_gid'))) into @supplier_contact_gid;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_contact,CONCAT('$.Contacttype_Gid'))) into @contacttype_gid;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_contact,CONCAT('$.Contact_Name'))) into @contact_name;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_contact,CONCAT('$.Designation_Gid'))) into @desig_gid;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_contact,CONCAT('$.Landline_No1'))) into @landline_no1;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_contact,CONCAT('$.Landline_No2'))) into @landline_no2;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_contact,CONCAT('$.Mobile_No1'))) into @mobile_no1;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_contact,CONCAT('$.Mobile_No2'))) into @mobile_no2;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_contact,CONCAT('$.Email'))) into @email;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_contact,CONCAT('$.Contact_Dob'))) into @contact_dob;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_contact,CONCAT('$.Contact_Wd'))) into @contact_wd;
		if @supplier_contact_gid is not null and @supplier_contact_gid<>'0' then
			set @contact_max_gid=@supplier_contact_gid;
		else
			call sp_Contact_Set('Insert',0,'SUPPLIER',12,@contacttype_gid,@contact_name,@desig_gid,@landline_no1,@landline_no2, @mobile_no1,@mobile_no2,
			@email,@contact_dob,@contact_wd,@Entity_gid,@Create_by,@Message);
			select @Message into @Out_Message_Contact;
		   select SUBSTRING_INDEX(@Out_Message_Contact,',',1) into @contact_max_gid;
	   end if;
	end if;

	if Action = 'SUPP_INSERT' then
		#select 'calling supp insert';
		if @li_supplier_count is  null or @li_supplier_count = '' and @li_supplier_count = 0  then
				set Message='Supplier Json is Empty';
				leave sp_SupplierSPS_Set;
		end if;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_supplier, CONCAT('$.atmaSupplier_Code'))) into @atmaSupplier_Code;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_supplier, CONCAT('$.Supplier_Name'))) into @Supplier_name;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_supplier, CONCAT('$.Supplier_Capacity'))) into @Supplier_capacity;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_supplier, CONCAT('$.Supplier_Group_Gid'))) into @Supplier_Group_Gid;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_supplier, CONCAT('$.Supplier_Branch_Name'))) into @Supplier_Branch_Name;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_supplier, CONCAT('$.Supplier_GST_No'))) into @Supplier_GST_No;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_supplier, CONCAT('$.Supplier_Panno'))) into @Supplier_Panno;
        #select @Supplier_Group_Gid,@Supplier_name,@Supplier_capacity;
	    if @Supplier_name is null or @Supplier_name = '0' then
			set Message='Supplier Name is Empty';
			leave sp_SupplierSPS_Set;
		end if;
		if @Supplier_capacity is null or @Supplier_capacity = '' then
			set @Supplier_capacity='0';
		end if;
		if @Supplier_Group_Gid is null or @Supplier_Group_Gid = '' then
			set Message = 'Supplier Group  Gid Is Needed. ';
			leave sp_SupplierSPS_Set;
		End if;
		if @Supplier_Branch_Name is null or @Supplier_Branch_Name = '' then
			set Message = 'Supplier Branch Is Needed. ';
			leave sp_SupplierSPS_Set;
		End if;
		set Query_Column = '';
		set Query_Value = '';

		if @Supplier_GST_No is not null or @Supplier_GST_No <> '' then
			#set Query_Column = '';
			#set Query_Value = '';
			set Query_Column = concat(Query_Column, ' supplier_gstno,');
			set Query_Value = concat(Query_Value, '''',@Supplier_GST_No,''',');
		End if;

        if @Supplier_Panno is not null or @Supplier_Panno <> '' then

			set Query_Column = concat(Query_Column, ' supplier_panno,');
			set Query_Value = concat(Query_Value, '''',@Supplier_Panno,''',');
		End if;


		if @atmaSupplier_Code is not null and @atmaSupplier_Code <>'0' then
			set @Supplier_code=@atmaSupplier_Code;
		else
			set @codes = '';
			select ifnull(substring(supplier_code,5),'')  from gal_mst_tsupplier where supplier_gid =(select max(supplier_gid)
			from gal_mst_tsupplier where supplier_isremoved='N') into @codes;
			 call sp_Generatecode_Get('WITHOUT_DATE','SUPP','000',@codes,@Message) ;
			 select @Message into @Supplier_code;
			 #select @Supplier_code,@Supplier_name,@contact_max_gid,@add_max_gid,@Supplier_capacity,@Entity_gid,@Create_by;
		end if;

		/*select  count(supplier_gid) into @dup from gal_mst_tsupplier where supplier_name=@Supplier_name;
		if @dup >0 then
				set message='Supplier Name Already Exits';
				leave sp_SupplierSPS_Set;
		end if;*/

		#select @Supplier_code,@Supplier_Group_Gid,@Supplier_Branch_Name,@Supplier_name,
		#@contact_max_gid,@add_max_gid,@Supplier_capacity,@Entity_gid,@Create_by,@Query_Column,@Query_Value;
		set @query_insert =concat('insert into gal_mst_tsupplier (supplier_code,supplier_groupgid,supplier_name,supplier_branchname,
					supplier_contact_gid,supplier_add_gid,supplier_capacity,
					',Query_Column,'entity_gid,create_by) values(''',@Supplier_code,''',''',@Supplier_Group_Gid,''',''',@Supplier_name,''',''',@Supplier_Branch_Name,''',
					',@contact_max_gid,',',@add_max_gid,',''',@Supplier_capacity,''',',Query_Value,'',@Entity_gid,',''',@Create_by,''')');

					#select @Supplier_Group_Gid, @contact_max_gid;
                   #select  @query_insert;
		set @supp_srch = @query_insert;
		SELECT @supp_srch;
		PREPARE stmt FROM @supp_srch;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;

		if countRow >  0 then
			select MAX(Supplier_gid) from gal_mst_tsupplier where supplier_isremoved='N' into @Supplier_max_gid;
			select supplier_code from gal_mst_tsupplier where supplier_gid =(select MAX(Supplier_gid) from gal_mst_tsupplier where supplier_isremoved='N') into @Supplier_code;
			Update gal_mst_tcontact set contact_reftable_gid =@Supplier_max_gid,contact_reftablecode=@Supplier_code
			where contact_gid=@contact_max_gid;
			select row_count() into @rowcount;
             #set @suppliergid='';
			#select LAST_INSERT_ID() into @suppliergid;
			if @rowcount > 0 then
				set Message=concat('SUCCESS',',',@Supplier_max_gid);
				if @atmaSupplier_Code is null then
					#SELECT 'COMMIT DONE';
					commit;
				#ELSE
					#SELECT CONCAT('SUPP CODE',@atmaSupplier_Code);
				end if;
			else
				set Message='FAIL';
				leave sp_SupplierSPS_Set;
				#rollback;
			end if;
		else
			set Message = 'FAIL';
			leave sp_SupplierSPS_Set;
			#rollback;
		end if;
    elseif Action = 'SUPPLIER_GROUP_INSERT' then

		select JSON_LENGTH(lj_supplier,'$') into @li_SupplierGrp_count;
		### Supplier Group
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_supplier, CONCAT('$.AtmaSupplierGrp_Code'))) into @AtmaSupplierGrp_Code;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_supplier, CONCAT('$.Supplier_Group_Name'))) into @Supplier_Group_Name;

		if @Entity_Detail_Gid is null or @Entity_Detail_Gid = 0 then
			set Message = 'Entity Details Gid Is Needed.';
			leave sp_SupplierSPS_Set;
		End if;

		if @Supplier_Group_Name is null or @Supplier_Group_Name = '' then
			set Message = 'Supplier Group Name Is Needed';
			leave sp_SupplierSPS_Set;
		End if;
		#select 'calling SUPPLIER_GROUP_INSERT';
		set @SuppGrp_NameCheck = '';
		Select ifnull(suppliergroup_name,'') into @SuppGrp_NameCheck  from gal_mst_tsuppliergroup
		where suppliergroup_name = @Supplier_Group_Name  and entity_gid = @Entity_gid limit 1 ;

		if @SuppGrp_NameCheck <> '' then
			 set Message = 'Supplier Group Name Already Exists.';
			 leave sp_SupplierSPS_Set;
		End if;
		#select @AtmaSupplierGrp_Code;
	   # set @AtmaSupplierGrp_Code = '';
		set @SupplierGrp_Code = '';
		set @codes = '';

		if @AtmaSupplierGrp_Code is not null and @AtmaSupplierGrp_Code <>'0' and @AtmaSupplierGrp_Code <> '' then
				set @SupplierGrp_Code=@AtmaSupplierGrp_Code;
		  else
				select ifnull(substring(suppliergroup_code,5),'')  from gal_mst_tsuppliergroup where suppliergroup_gid =(select max(suppliergroup_gid)
				 from gal_mst_tsuppliergroup where suppliergroup_isremoved='N') into @codes;

				 call sp_Generatecode_Get('WITHOUT_DATE','SUPG','000',@codes,@Message) ;
				 select @Message into @SupplierGrp_Code;

					 #select @Supplier_code,@Supplier_name,@contact_max_gid,@add_max_gid,@Supplier_capacity,@Entity_gid,@Create_by;
		end if;

                #            select @SupplierGrp_Code,@Supplier_Group_Name,@add_max_gid,@contact_max_gid,@Entity_gid,@Entity_Detail_Gid,@Create_by;

		set Query_Insert = '';
		set Query_Insert = concat('Insert into gal_mst_tsuppliergroup (suppliergroup_code,suppliergroup_name,suppliergroup_addgid,suppliergroup_contactgid,
			entity_gid,entity_detailsgid,create_by )
			values (''',@SupplierGrp_Code,''',''',@Supplier_Group_Name,''',''',@add_max_gid,''',''',@contact_max_gid,''',''',@Entity_gid,''',''',@Entity_Detail_Gid,''',
						''',@Create_by,'''
						)' );


		set @Query_InsertGrp = Query_Insert;
		PREPARE stmt FROM @Query_InsertGrp;

		EXECUTE stmt;

		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;

		  if countRow <= 0 then
          select countRow;
				set Message = 'Error On Supplier Group Insert ';
				if @AtmaSupplierGrp_Code is null then
					rollback;
					leave sp_SupplierSPS_Set;
				end if;
		   Else
           set @NEWgroup_gid='';
			select LAST_INSERT_ID() into @NEWgroup_gid;
			   #set Message = 'SUCCESS';
			   set Message = @NEWgroup_gid;
               if @AtmaSupplierGrp_Code is null then
               commit;
               end if;
		  End if;
	End if; ### end of Action Check - Sup group and Supplier


end if;
if  Action='SUPP_UPDATE' or Action = 'SUPPLIER_GROUP_UPDATE' then

	select JSON_LENGTH(lj_classification,'$')into @li_classification_count;
	select JSON_LENGTH(lj_contact,'$')into @li_contact_count;
	select JSON_LENGTH(lj_address,'$')into @li_address_count;
	select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Entity_Gid'))) into @Entity_gid;
	select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Create_By'))) into @Update_by;
	select  JSON_UNQUOTE(JSON_EXTRACT(lj_supplier, CONCAT('$.AtmaSupplierGrp_Code'))) into @AtmaSupplierGrp_Code;
    select  JSON_UNQUOTE(JSON_EXTRACT(lj_supplier, CONCAT('$.atmaSupplier_Code'))) into @atmaSupplier_Code;

	if @AtmaSupplierGrp_Code is null and @atmaSupplier_Code is null then
    if @li_address_count is not null or @li_address_count <>'' then
		 select JSON_UNQUOTE(JSON_EXTRACT(lj_address,CONCAT('$.Address_Gid'))) into @address_gid_Edit;
		 select JSON_UNQUOTE(JSON_EXTRACT(lj_address,CONCAT('$.Address1'))) into @address1_Edit;
		 select JSON_UNQUOTE(JSON_EXTRACT(lj_address,CONCAT('$.Address2'))) into @address2_Edit;
		 select JSON_UNQUOTE(JSON_EXTRACT(lj_address,CONCAT('$.Address3'))) into @address3_Edit;
		 select JSON_UNQUOTE(JSON_EXTRACT(lj_address,CONCAT('$.Pincode'))) into @pincode_Edit;
		 select JSON_UNQUOTE(JSON_EXTRACT(lj_address,CONCAT('$.District_Gid'))) into @district_gid_Edit;
		 select JSON_UNQUOTE(JSON_EXTRACT(lj_address,CONCAT('$.City_Gid'))) into @city_gid_Edit;
		 select JSON_UNQUOTE(JSON_EXTRACT(lj_address,CONCAT('$.State_Gid'))) into @state_gid_Edit;
		 # select @address_gid_Edit,@address1_Edit,@address2_Edit,@address3_Edit,@pincode_Edit,@district_gid_Edit,@city_gid_Edit,@state_gid_Edit;
		call sp_Address_Set('Update',@address_gid_Edit,'',@address1_Edit,@address2_Edit,@address3_Edit,@pincode_Edit,@district_gid_Edit,@city_gid_Edit,@state_gid_Edit,
		@Entity_gid,@Update_by,@Message);
		select @Message into @Out_Message_Address_Edit;
		if @Out_Message_Address_Edit <> 'SUCCESS' then
			set Message='Address Not Update';
		end if;
	end if;
	end if ;
    if @AtmaSupplierGrp_Code is null and @atmaSupplier_Code is null then
	if  @li_contact_count is not null or @li_contact_count <>'' then
		select JSON_UNQUOTE(JSON_EXTRACT(lj_contact,CONCAT('$.Contact_Gid'))) into @contact_gid;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_contact,CONCAT('$.Contacttype_Gid'))) into @contacttype_gid;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_contact,CONCAT('$.Contact_Name'))) into @contact_name;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_contact,CONCAT('$.Designation_Gid'))) into @desig_gid;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_contact,CONCAT('$.Landline_No1'))) into @landline_no1;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_contact,CONCAT('$.Landline_No2'))) into @landline_no2;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_contact,CONCAT('$.Mobile_No1'))) into @mobile_no1;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_contact,CONCAT('$.Mobile_No2'))) into @mobile_no2;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_contact,CONCAT('$.Email'))) into @email;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_contact,CONCAT('$.Contact_Dob'))) into @contact_dob;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_contact,CONCAT('$.Contact_Wd'))) into @contact_wd;
		if @contact_wd is null then
			set @contact_wd='';
		end if;
		#select @contact_gid,@contacttype_gid,@contact_name,@desig_gid,@landline_no1,@landline_no2, @mobile_no1,@mobile_no2,
		#@email,@contact_dob,@contact_wd,@Entity_gid,@Update_by; ### Remove it
		#select 1;
		call sp_Contact_Set('Update',@contact_gid,'',0,@contacttype_gid,@contact_name,@desig_gid,@landline_no1,@landline_no2, @mobile_no1,@mobile_no2,
		@email,@contact_dob,@contact_wd,@Entity_gid,@Update_by,@Message);
		select @Message into @Out_Message_Contact;
	end if;
	end if;
   if Action = 'SUPP_UPDATE' then
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_supplier, CONCAT('$.Supplier_Gid'))) into @Supplier_gid;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_supplier, CONCAT('$.Supplier_Name'))) into @Supplier_name;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_supplier, CONCAT('$.Supplier_Capacity'))) into @Supplier_capacity;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_supplier, CONCAT('$.Supplier_Group_Gid'))) into @Supplier_Group_Gid;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_supplier, CONCAT('$.Supplier_Branch_Name'))) into @Supplier_Branch_Name;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_supplier, CONCAT('$.Supplier_GST_No'))) into @Supplier_GST_No;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_supplier, CONCAT('$.Supplier_Panno'))) into @Supplier_Panno;
		#select @Supplier_gid, @Supplier_name, @Supplier_capacity;
        #select lj_supplier,'supplier';
        #SELECT @Supplier_gid,@Supplier_name,@Supplier_capacity,@Supplier_Group_Gid,
		#@Supplier_Branch_Name,@Supplier_GST_No;
		if @Supplier_gid is null or @Supplier_gid ='0' then
			set Message='Supplier Gid is Not Given';
			leave sp_SupplierSPS_Set;
		end if;
		if @Supplier_name is null or @Supplier_name = '0' then
			set Message='Supplier name is Empty';
			leave sp_SupplierSPS_Set;
		end if;
		if @Supplier_capacity is null  then
			set @Supplier_capacity='0';
		end if;

		select JSON_LENGTH(lj_supplier,'$') into @li_supplier_count;
		if @li_supplier_count is  null or @li_supplier_count = '' then
			set Message='Supplier Json is Empty';
			leave sp_SupplierSPS_Set;
		end if;
		### Duplicate Check
		/*select  count(supplier_gid) into @dup from gal_mst_tsupplier where supplier_name=@Supplier_name
		and supplier_gid <> @Supplier_gid ;
		if @dup >0 then
			set Message='Supplier_name Already Exits';
			leave sp_SupplierSPS_Set;
		end if;*/
		set @query_insert = '';
		set @query_insert =concat('update gal_mst_tsupplier set supplier_name=''',@Supplier_name,''',
        supplier_capacity=''',@Supplier_capacity,''',
		supplier_groupgid = ''',@Supplier_Group_Gid,''',supplier_branchname = ''',@Supplier_Branch_Name,''',
        supplier_gstno = ''',IFNULL(@Supplier_GST_No,''),''',supplier_panno=''',IFNULL(@Supplier_Panno,''),''',
		update_by=''',@Update_by,''', Update_date = now()
			where supplier_gid=''',@Supplier_gid,''' ');

	#SELECT @query_insert;
		set @Update_Query = @query_insert;
		PREPARE stmt FROM @Update_Query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;

		if countRow > 0 then
			set Message = 'SUCCESS';
		else
			set Message = 'FAIL';
			rollback;
		end if;
	elseif Action = 'SUPPLIER_GROUP_UPDATE' then
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_supplier, CONCAT('$.SupplierGrp_Gid'))) into @SupplierGrp_Gid;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_supplier, CONCAT('$.SupplierGrp_Name'))) into @SupplierGrp_Name;

		if @SupplierGrp_Gid is null or @SupplierGrp_Gid = 0 or @SupplierGrp_Gid = '' then
				set Message = 'Supplier Group Gid Is Needed.';
				leave sp_SupplierSPS_Set;
		End if;
		if @SupplierGrp_Name is null or @SupplierGrp_Name = '' then
			set Message = 'Supplier Group Name Is Needed.';
			leave sp_SupplierSPS_Set;
		End if;
		### Duplicate Check.
		set @SupplierGrp_Duplicate = 0 ;
		select ifnull(count(suppliergroup_gid),0) into @SupplierGrp_Duplicate
		from gal_mst_tsuppliergroup where suppliergroup_name = @SupplierGrp_Name
		and suppliergroup_isremoved = 'N'  and suppliergroup_gid <> @SupplierGrp_Gid ;

		if @SupplierGrp_Duplicate <> 0 then
			Set Message = 'The Supplier Group Already Exist.';
			leave sp_SupplierSPS_Set;
		End if;
		set Query_Update = '';
		set Query_Update = concat('Update gal_mst_tsuppliergroup set suppliergroup_name = ''',@SupplierGrp_Name,''',
		update_by = ''',@Update_by,''' , Update_date = now()
		where suppliergroup_gid = ''',@SupplierGrp_Gid,'''
		');
        #select Query_Update;
		set @Update_Query = Query_Update;
		PREPARE stmt FROM @Update_Query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow > 0 then
			set Message = 'SUCCESS';
		else
			set Message = 'FAIL';
			rollback;
		end if;
	End if;
end if;

if Action = 'Delete' then
    select JSON_LENGTH(lj_supplier,'$') into @li_supplier_count;
    select JSON_LENGTH(lj_classification,'$')into @li_classification_count;

  if @li_classification_count is not null or @li_classification_count <> ''then
       select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Entity_Gid'))) into @Entity_gid;
       select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Update_By'))) into @Update_by;
   if @Entity_gid ='' or @Entity_gid =0 then
        set Message='Entity gid is Empty';
        leave sp_SupplierSPS_Set;
   end if;
  else
      set Message='Classification Json is Empty';
      leave sp_SupplierSPS_Set;
  end if;

  if @li_supplier_count is not null or @li_supplier_count <>'' then

      select  JSON_UNQUOTE(JSON_EXTRACT(lj_supplier, CONCAT('$.Supplier_Gid'))) into @Supplier_gid;

    if @Supplier_gid > 0 then
         set Message='Supplier gid not came';
         leave sp_SupplierSPS_Set;
    end if;
  else
      set Message='Supplier Json is Empty';
      leave sp_SupplierSPS_Set;
  end if;
    select count(*) into @cnt from gal_trn_tpoheader where poheader_isremoved='N' and poheader_isactive='Y' and poheader_supplier_gid=@Supplier_gid;

    if @cnt > 0 then
        set Message = 'Supplier Cannot Delete';
        leave sp_SupplierSPS_Set;
    end if;

        start transaction;

        Update gal_mst_tsupplier set supplier_isremoved = 'Y', update_by =@Update_by, Update_date = now()
        where supplier_isremoved = 'N' and supplier_isactive = 'Y' and supplier_gid = @Supplier_gid;

        set countRow = (select row_count());

        if countRow > 0 then
            set Message = 'SUCCESS';
           # commit;
        else
            set Message = 'FAIL';
            rollback;
        end if;
end if;
if Action = 'Inactive' then
    select JSON_LENGTH(lj_supplier,'$') into @li_supplier_count;
    select JSON_LENGTH(lj_classification,'$')into @li_classification_count;

    if  @li_classification_count is not null or @li_classification_count <> ''then
       select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Entity_Gid'))) into @Entity_gid;
       select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Update_By'))) into @Update_by;
   if @Entity_gid ='' or @Entity_gid =0 then
        set Message='Entity gid is Empty';
        leave sp_SupplierSPS_Set;
   end if;
  else
      set Message='Classification Json is Empty';
      leave sp_SupplierSPS_Set;
  end if;

    if @li_supplier_count is not null or @li_supplier_count <>'' then

      select  JSON_UNQUOTE(JSON_EXTRACT(lj_supplier, CONCAT('$.Supplier_Gid'))) into @Supplier_gid;
      #select @Supplier_gid;

    if @Supplier_gid < 0 then
         set Message='Supplier gid not came';
         leave sp_SupplierSPS_Set;
    end if;
   else
      set Message='Supplier Json is Empty';
      leave sp_SupplierSPS_Set;
  end if;


        start transaction;

        Update gal_mst_tsupplier set supplier_isactive = 'N', update_by =@Supplier_gid, Update_date = now()
        where supplier_isremoved = 'N' and supplier_isactive = 'Y' and supplier_gid = @Supplier_gid ;

        set countRow = (select row_count());

        if countRow > 0 then
            set Message = 'SUCCESS';
            commit;
        else
            set Message = 'FAIL';
            rollback;
        end if;


end if;
if Action = 'Active' then
    select JSON_LENGTH(lj_supplier,'$') into @li_supplier_count;
    select JSON_LENGTH(lj_classification,'$')into @li_classification_count;

    if  @li_classification_count is not null or @li_classification_count <> ''then
       select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Entity_Gid'))) into @Entity_gid;
       select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Update_By'))) into @Update_by;
    if @Entity_gid ='' or @Entity_gid =0 then
        set Message='Entity gid is Empty';
        leave sp_SupplierSPS_Set;
    end if;
  else
      set Message='Classification Json is Empty';
      leave sp_SupplierSPS_Set;
  end if;

    if @li_supplier_count is not null or @li_supplier_count <>'' then

      select  JSON_UNQUOTE(JSON_EXTRACT(lj_supplier, CONCAT('$.Supplier_Gid'))) into @Supplier_gid;

      if @Supplier_gid < 0 then
         set Message='Supplier gid not came';
         leave sp_SupplierSPS_Set;
      end if;
    else
      set Message='Supplier Json is Empty';
      leave sp_SupplierSPS_Set;
    end if;

        start transaction;

        Update gal_mst_tsupplier set supplier_isactive = 'Y', update_by =@Update_by , Update_date = now()
        where supplier_isremoved = 'N' and supplier_isactive = 'N' and supplier_gid = @Supplier_gid;

        set countRow = (select row_count());

        if countRow > 0 then
            set Message = 'SUCCESS';
            commit;
        else
            set Message = 'FAIL';
            rollback;
        end if;
end if;

if Action = 'SUPPGRP_STATUS_UPDATE' then
        	select  JSON_UNQUOTE(JSON_EXTRACT(lj_supplier, CONCAT('$.SupplierGrp_Gid'))) into @SupplierGrp_Gid;
        	select  JSON_UNQUOTE(JSON_EXTRACT(lj_supplier, CONCAT('$.SupplierGrp_ISActive'))) into @SupplierGrp_ISActive;
            #Create_by

            if @SupplierGrp_Gid = 0 or @SupplierGrp_Gid is null then
					set Message = 'Supplier Group Gis Is Needed.';
                    leave sp_SupplierSPS_Set;
            End if;

            if @SupplierGrp_ISActive = 'Y' then
					set @SupplierGrp_ISActive = 'Y' ;
            elseif @SupplierGrp_ISActive = 'N' then
                   set @SupplierGrp_ISActive = 'N';

                   set @suppplier_gid_exists = 0 ;
                   Select ifnull(count(supplier_gid),0) into @suppplier_gid_exists from gal_mst_tsupplier
                   where supplier_groupgid = @SupplierGrp_Gid  and supplier_isactive = 'Y' and supplier_isremoved  = 'N'
                   and entity_gid = @Entity_gid ;

                   if @suppplier_gid_exists <> 0 then
						 set Message = 'For The Selected Supplier Group There Is Active Supplier Data Found.';
                         leave sp_SupplierSPS_Set;
                   End if;

             else
                  set Message = 'Incorrect Active Inactive Status.';
                  leave sp_SupplierSPS_Set;
            End if;

            Update gal_mst_tsuppliergroup set suppliergroup_isactive = @SupplierGrp_ISActive ,
				update_by = @Create_by , Update_date = now()
			where suppliergroup_gid = @SupplierGrp_Gid ;

            set countRow = (select row_count());

				if countRow > 0 then
					set Message = 'SUCCESS';
				else
					set Message = 'FAIL';
					rollback;
				end if;




End if;


END