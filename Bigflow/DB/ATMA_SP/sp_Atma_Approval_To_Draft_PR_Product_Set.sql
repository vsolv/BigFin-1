CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Approval_To_Draft_PR_Product_Set`(
in lj_filter json,in Partner_Gid int,in lj_classification json,out Message varchar(1000))
sp_Atma_Approval_To_Draft_PR_Product_Set:BEGIN

declare Query_Insert varchar(10000);
Declare countRow varchar(6000);
declare Query_Update varchar(10000);
declare Query_Update1 varchar(10000);
declare Query_delete varchar(1000);
declare Query_Value varchar(1000);
declare Query_Column varchar(1000);
Declare p_partnerproduct_gid,p_partnerproduct_type,
		p_partnerproduct_name,p_partnerproduct_age,p_partnerproduct_clientcontactgid1,
		p_partnerproduct_clientcontactgid2,p_partnerproduct_customercontactgid1,
		p_partnerproduct_customercontactgid2,p_partnerproduct_isactive,
		p_partnerproduct_isremoved,p_entity_gid,p_create_by,p_update_by,
		p_main_partnerproduct_gid varchar(150);

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


select JSON_LENGTH(lj_filter,'$') into @lj_filter_json_count;
select JSON_LENGTH(lj_classification,'$') into @lj_classification_json_count;

if @lj_filter_json_count = 0 or @lj_filter_json_count is null then
	set Message = 'No Data In filter Json. ';
	leave sp_Atma_Approval_To_Draft_PR_Product_Set;
End if;

select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Gid'))) into @Partner_Gid;


if @Partner_Gid = '' or @Partner_Gid is null  or @Partner_Gid=0 then
		set Message = 'Partner Is Not Provided';
		leave sp_Atma_Approval_To_Draft_PR_Product_Set;
End if;


SET finished =0;

BEGIN
	Declare Cursor_atma CURSOR FOR
	select  partnerproduct_gid, partnerproduct_type, partnerproduct_name,
			partnerproduct_age, partnerproduct_clientcontactgid1, partnerproduct_clientcontactgid2,
			partnerproduct_customercontactgid1, partnerproduct_customercontactgid2, partnerproduct_isactive,
			partnerproduct_isremoved, entity_gid, create_by,update_by
		   from atma_mst_tpartnerproduct where partnerproduct_partnergid=@Partner_Gid ;

	DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;
	OPEN Cursor_atma;
	atma_looop:loop
		fetch Cursor_atma into  p_partnerproduct_gid,p_partnerproduct_type,
								p_partnerproduct_name,p_partnerproduct_age,p_partnerproduct_clientcontactgid1,
                                p_partnerproduct_clientcontactgid2,p_partnerproduct_customercontactgid1,
                                p_partnerproduct_customercontactgid2,p_partnerproduct_isactive,
                                p_partnerproduct_isremoved,p_entity_gid,p_create_by,p_update_by;

	 	if finished = 1 then
			leave atma_looop;
		End if;


		select contact_gid,Contact_ref_gid,Contact_reftable_gid,
						contact_reftablecode,Contact_contacttype_gid,
						Contact_personname,Contact_designation_gid,Contact_landline,
						Contact_landline2,Contact_mobileno,
						Contact_mobileno2,Contact_email,Contact_DOB,Contact_WD,
						entity_gid,create_by,update_by
		into   c_contact_gid,c_Contact_ref_gid,c_Contact_reftable_gid,
						c_contact_reftablecode,c_Contact_contacttype_gid,
						c_Contact_personname,c_Contact_designation_gid,c_Contact_landline,
						c_Contact_landline2,c_Contact_mobileno,
						c_Contact_mobileno2,c_Contact_email,c_Contact_DOB,c_Contact_WD,
						c_entity_gid,c_create_by,c_update_by
		from  gal_mst_tcontact where contact_gid=p_partnerproduct_clientcontactgid1 ;



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
       	set Error_Level='ATMA14.1';
		set Query_Update = concat('INSERT INTO atma_tmp_mst_tcontact
					  (Contact_ref_gid, Contact_reftable_gid, contact_reftablecode,
                          Contact_contacttype_gid, Contact_designation_gid,
                          entity_gid, create_by, create_date ,main_contact_gid
                          ',Query_Column,')
				   values (',c_Contact_ref_gid,',',c_Contact_reftable_gid,',
						''',c_contact_reftablecode,''',',c_Contact_contacttype_gid,',
						',c_Contact_designation_gid,',''',c_entity_gid,''',
						''',c_create_by,''' ,''',Now(),''',',c_contact_gid,'
						',Query_Value,'
                          )');

		set @Insert_query = Query_Update;
		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'SUCCESS';
		else
			set Message = 'FAILED_CON1';
            leave sp_Atma_Approval_To_Draft_PR_Product_Set;
		end if;


		set  @Contact_Gid1='';
		select last_insert_id() into @Contact_Gid1;

		select  contact_gid,Contact_ref_gid,Contact_reftable_gid,
						contact_reftablecode,Contact_contacttype_gid,
						Contact_personname,Contact_designation_gid,Contact_landline,
						Contact_landline2,Contact_mobileno,
						Contact_mobileno2,Contact_email,Contact_DOB,Contact_WD,
						entity_gid,create_by,update_by
		into    c_contact_gid,c_Contact_ref_gid,c_Contact_reftable_gid,
						c_contact_reftablecode,c_Contact_contacttype_gid,
						c_Contact_personname,c_Contact_designation_gid,c_Contact_landline,
						c_Contact_landline2,c_Contact_mobileno,
						c_Contact_mobileno2,c_Contact_email,c_Contact_DOB,c_Contact_WD,
						c_entity_gid,c_create_by,c_update_by
		from    gal_mst_tcontact where contact_gid=p_partnerproduct_clientcontactgid2 ;



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
        set Error_Level='ATMA14.2';
		set Query_Update = concat('INSERT INTO atma_tmp_mst_tcontact
					  ( Contact_ref_gid, Contact_reftable_gid, contact_reftablecode,
                      Contact_contacttype_gid, Contact_designation_gid,
                      entity_gid, create_by, create_date ,main_contact_gid
                      ',Query_Column,')
			   values (',c_Contact_ref_gid,',',c_Contact_reftable_gid,',
					''',c_contact_reftablecode,''',',c_Contact_contacttype_gid,',
					',c_Contact_designation_gid,',''',c_entity_gid,''',
					''',c_create_by,''' ,''',Now(),''' ,',c_contact_gid,'
					',Query_Value,'
					   )');

		set @Insert_query = Query_Update;
		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'SUCCESS';
		else
			set Message = 'FAILED_CON2';
			leave sp_Atma_Approval_To_Draft_PR_Product_Set;
		end if;

        set @Contact_Gid2='';
		select last_insert_id() into @Contact_Gid2;

		select  contact_gid,Contact_ref_gid,Contact_reftable_gid,
						contact_reftablecode,Contact_contacttype_gid,
						Contact_personname,Contact_designation_gid,Contact_landline,
						Contact_landline2,Contact_mobileno,
						Contact_mobileno2,Contact_email,Contact_DOB,Contact_WD,
						entity_gid,create_by,update_by
		into    c_contact_gid,c_Contact_ref_gid,c_Contact_reftable_gid,
						c_contact_reftablecode,c_Contact_contacttype_gid,
						c_Contact_personname,c_Contact_designation_gid,c_Contact_landline,
						c_Contact_landline2,c_Contact_mobileno,
						c_Contact_mobileno2,c_Contact_email,c_Contact_DOB,c_Contact_WD,
						c_entity_gid,c_create_by,c_update_by
		from   gal_mst_tcontact where contact_gid=p_partnerproduct_customercontactgid1 ;


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
        set Error_Level='ATMA14.3';
		set Query_Update = concat('INSERT INTO atma_tmp_mst_tcontact
					  ( Contact_ref_gid, Contact_reftable_gid, contact_reftablecode,
                      Contact_contacttype_gid, Contact_designation_gid,
                      entity_gid, create_by, create_date ,main_contact_gid
                      ',Query_Column,')
			    values (',c_Contact_ref_gid,',',c_Contact_reftable_gid,',
                ''',c_contact_reftablecode,''',',c_Contact_contacttype_gid,',
                ',c_Contact_designation_gid,',''',c_entity_gid,''',
                ''',c_create_by,''' ,''',Now(),''' ,',c_contact_gid,'
                ',Query_Value,'
                  )');

		set @Insert_query = Query_Update;
		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'SUCCESS';
		else
			set Message = 'FAILED_CON3';
			leave sp_Atma_Approval_To_Draft_PR_Product_Set;
		end if;


        set @Contact_Gid3='';
		select last_insert_id() into @Contact_Gid3;


			select  contact_gid,Contact_ref_gid,Contact_reftable_gid,
						contact_reftablecode,Contact_contacttype_gid,
						Contact_personname,Contact_designation_gid,Contact_landline,
						Contact_landline2,Contact_mobileno,
						Contact_mobileno2,Contact_email,Contact_DOB,Contact_WD,
						entity_gid,create_by,update_by

			into    c_contact_gid,c_Contact_ref_gid,c_Contact_reftable_gid,
						c_contact_reftablecode,c_Contact_contacttype_gid,
						c_Contact_personname,c_Contact_designation_gid,c_Contact_landline,
						c_Contact_landline2,c_Contact_mobileno,
						c_Contact_mobileno2,c_Contact_email,c_Contact_DOB,c_Contact_WD,
						c_entity_gid,c_create_by,c_update_by
			from  gal_mst_tcontact where contact_gid=p_partnerproduct_customercontactgid2 ;




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
			set Error_Level='ATMA14.4';
           set Query_Update = concat('INSERT INTO atma_tmp_mst_tcontact
											  ( Contact_ref_gid, Contact_reftable_gid, contact_reftablecode,
                                              Contact_contacttype_gid, Contact_designation_gid,
                                              entity_gid, create_by, create_date ,main_contact_gid
                                              ',Query_Column,')
									    values (',c_Contact_ref_gid,',',c_Contact_reftable_gid,',
                                        ''',c_contact_reftablecode,''',',c_Contact_contacttype_gid,',
                                        ',c_Contact_designation_gid,',''',c_entity_gid,''',
                                        ''',c_create_by,''' ,''',Now(),''' ,',c_contact_gid,'
                                        ',Query_Value,'
                                          )');
			#select p_partnerbranch_remarks;
			#select Query_Update;




        #select Query_Update,4;
		set @Insert_query = Query_Update;
		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'SUCCESS';
		else
			set Message = 'FAILED_CON4';
			leave sp_Atma_Approval_To_Draft_PR_Product_Set;
		end if;


        set  @Contact_Gid4='';
		select last_insert_id() into @Contact_Gid4;





				set Query_Column ='';
				set Query_Value ='';

			if p_partnerproduct_age is not null and p_partnerproduct_age <>'' then
				set Query_Column = concat(Query_Column,',partnerproduct_age');
				set Query_Value=concat(Query_Value,', ',p_partnerproduct_age,' ');
            end if;

			if @Contact_Gid2 is not null and @Contact_Gid2 <>'' then
				set Query_Column = concat(Query_Column,',partnerproduct_clientcontactgid2');
				set Query_Value=concat(Query_Value,', ',@Contact_Gid2,' ');
            end if;

			if @Contact_Gid4 is not null and @Contact_Gid4 <>'' then
				set Query_Column = concat(Query_Column,',partnerproduct_customercontactgid2');
				set Query_Value=concat(Query_Value,', ',@Contact_Gid4,' ');
            end if;
            set Error_Level='ATMA14.5';
			set Query_Update = concat('INSERT INTO atma_tmp_mst_tpartnerproduct
											  (partnerproduct_partnergid, partnerproduct_type, partnerproduct_name,
                                              partnerproduct_clientcontactgid1,partnerproduct_customercontactgid1,
                                              partnerproduct_isactive, partnerproduct_isremoved, entity_gid,
                                              create_by,create_date ,main_partnerproduct_gid
                                              ',Query_Column,')
										values (',Partner_Gid,',''',p_partnerproduct_type,''',
                                        ''',p_partnerproduct_name,''',',@Contact_Gid1,',',@Contact_Gid3,',
                                        ''',p_partnerproduct_isactive,''',''',p_partnerproduct_isremoved,''',
                                        ',p_entity_gid,',',p_create_by,',''',Now(),''' ,',p_partnerproduct_gid,'
                                        ',Query_Value,'
                                          )');
			#select p_main_partnerproduct_gid;

        #select Query_Update,5;
		set @Insert_query = Query_Update;
		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'SUCCESS';
		else
			set Message = ' FAILED_PR';
			leave sp_Atma_Approval_To_Draft_PR_Product_Set;
		end if;
	End loop atma_looop;
	close Cursor_atma;
	end;  #Endof Cursor


END