CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Pending_To_Approval_PR_Product_Set`(
in lj_filter json,in Partner_Gid int,in lj_classification json,out Message varchar(1000))
sp_Atma_Pending_To_Approval_PR_Product_Set:BEGIN

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
							set Message = concat(Error_Level,':No-',errno,msg);
							ROLLBACK;
						END;


	select JSON_LENGTH(lj_filter,'$') into @lj_filter_json_count;
	select JSON_LENGTH(lj_classification,'$') into @lj_classification_json_count;

	if @lj_filter_json_count = 0 or @lj_filter_json_count is null then
		set Message = 'No Data In filter Json. ';
		leave sp_Atma_Pending_To_Approval_PR_Product_Set;
	End if;

	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Gid')))
	into @Partner_Gid;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Update_By')))
	into @Update_By;

	if @Partner_Gid = '' or @Partner_Gid is null  or @Partner_Gid=0 then
			set Message = 'Partner Is Not Provided';
			leave sp_Atma_Pending_To_Approval_PR_Product_Set;
	End if;


 SET finished =0;


BEGIN
	Declare Cursor_atma CURSOR FOR



	select  partnerproduct_gid, partnerproduct_type, partnerproduct_name,
			partnerproduct_age, partnerproduct_clientcontactgid1, partnerproduct_clientcontactgid2,
			partnerproduct_customercontactgid1, partnerproduct_customercontactgid2, partnerproduct_isactive,
			partnerproduct_isremoved, entity_gid, create_by,update_by,
			main_partnerproduct_gid
		   from atma_tmp_mst_tpartnerproduct where partnerproduct_partnergid=@Partner_Gid ;

	DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;
	OPEN Cursor_atma;
	atma_looop:loop
		fetch Cursor_atma into  p_partnerproduct_gid,p_partnerproduct_type,
								p_partnerproduct_name,p_partnerproduct_age,p_partnerproduct_clientcontactgid1,
                                p_partnerproduct_clientcontactgid2,p_partnerproduct_customercontactgid1,
                                p_partnerproduct_customercontactgid2,p_partnerproduct_isactive,
                                p_partnerproduct_isremoved,p_entity_gid,p_create_by,p_update_by,
								p_main_partnerproduct_gid;

	 if finished = 1 then
			leave atma_looop;
		End if;


			select  contact_gid,Contact_ref_gid,Contact_reftable_gid,
						contact_reftablecode,Contact_contacttype_gid,
						Contact_personname,Contact_designation_gid,Contact_landline,
						Contact_landline2,Contact_mobileno,
						Contact_mobileno2,Contact_email,Contact_DOB,Contact_WD,
						entity_gid,create_by,update_by,main_contact_gid

			into    c_contact_gid,c_Contact_ref_gid,c_Contact_reftable_gid,
						c_contact_reftablecode,c_Contact_contacttype_gid,
						c_Contact_personname,c_Contact_designation_gid,c_Contact_landline,
						c_Contact_landline2,c_Contact_mobileno,
						c_Contact_mobileno2,c_Contact_email,c_Contact_DOB,c_Contact_WD,
						c_entity_gid,c_create_by,c_update_by,c_main_contact_gid
			from  atma_tmp_mst_tcontact where contact_gid=p_partnerproduct_clientcontactgid1 ;


		if c_main_contact_gid = '' or c_main_contact_gid is null  or c_main_contact_gid=0 then

				 set Query_Column='';
				 set Query_Value ='';

            if c_Contact_personname is not null and c_Contact_personname<>'' then
				set Query_Column = concat(Query_Column,',Contact_personname');
				set Query_Value=concat(Query_Value,', ''',c_Contact_personname,''' ');
            end if;

            if c_Contact_landline is not null and c_Contact_landline<>'' then
				set Query_Column = concat(Query_Column,',Contact_landline');
				set Query_Value=concat(Query_Value,', ',c_Contact_landline,' ');
            end if;

            if c_Contact_landline2 is not null and c_Contact_landline2<>'' then
				set Query_Column = concat(Query_Column,',Contact_landline2');
				set Query_Value=concat(Query_Value,', ',c_Contact_landline2,' ');
            end if;

            if c_Contact_mobileno is not null and c_Contact_mobileno<>'' then
				set Query_Column = concat(Query_Column,',Contact_mobileno');
				set Query_Value=concat(Query_Value,', ',c_Contact_mobileno,' ');
            end if;

			if c_Contact_mobileno2 is not null and c_Contact_mobileno2<>'' then
				set Query_Column = concat(Query_Column,',Contact_mobileno2');
				set Query_Value=concat(Query_Value,', ',c_Contact_mobileno2,' ');
            end if;

            if c_Contact_email is not null and c_Contact_email<>'' then
				set Query_Column = concat(Query_Column,',Contact_email');
				set Query_Value=concat(Query_Value,', ''',c_Contact_email,''' ');
            end if;

            if c_Contact_DOB is not null and c_Contact_DOB<>'' then
				set Query_Column = concat(Query_Column,',Contact_DOB');
				set Query_Value=concat(Query_Value,', ''',c_Contact_DOB,''' ');
            end if;

            if c_Contact_WD is not null and c_Contact_WD<>'' then
				set Query_Column = concat(Query_Column,',Contact_WD');
				set Query_Value=concat(Query_Value,', ''',c_Contact_WD,''' ');
            end if;





         #select p_partnerproduct_clientcontactgid1;
 set Error_Level='ATMA57.1';
			set Query_Update = concat('INSERT INTO gal_mst_tcontact
											  ( Contact_ref_gid, Contact_reftable_gid, contact_reftablecode,
                                              Contact_contacttype_gid, Contact_designation_gid,
                                              entity_gid, create_by, create_date ',Query_Column,')
									    values (',c_Contact_ref_gid,',',c_Contact_reftable_gid,',
                                        ''',c_contact_reftablecode,''',',c_Contact_contacttype_gid,',
                                        ',c_Contact_designation_gid,',''',c_entity_gid,''',
                                        ''',c_create_by,''' ,''',Now(),''' ',Query_Value,'
                                          )');



          #select Query_Update;

		else
                set Query_Update1='';

				if c_Contact_DOB is null then
					set Query_Update1 = concat('Contact_DOB = null,');
                else
					set Query_Update1 = concat('Contact_DOB = ''',c_Contact_DOB,''',');
				end if;

                if C_Contact_WD is null then
					set Query_Update1 = concat(Query_Update1,'Contact_WD = null,');
                else
					set Query_Update1 = concat(Query_Update1,'Contact_WD = ''',C_Contact_WD,''',');
				end if;



    set Error_Level='ATMA57.2';
		 	set Query_Update = concat(' Update gal_mst_tcontact
										set Contact_contacttype_gid = ',c_Contact_contacttype_gid,',
                                        Contact_designation_gid = ',c_Contact_designation_gid,',
                                        Contact_personname = ''',ifnull(c_Contact_personname,''),''',
                                        Contact_landline = ''',ifnull(c_Contact_landline,''),''',
                                        Contact_landline2 = ''',ifnull(c_Contact_landline2,''),''',
                                        Contact_mobileno = ''',ifnull(c_Contact_mobileno,''),''',
                                        Contact_mobileno2 = ''',ifnull(c_Contact_mobileno2,''),''',
                                        Contact_email = ''',ifnull(c_Contact_email,''),''',
                                        ',Query_Update1,'
                                        update_by=',@Update_By,',
                                        update_date = ''',now(),'''
										Where contact_gid = ',c_main_contact_gid,'
                                              ');




		end if;

        #select Query_Update,1;
		set @Insert_query = Query_Update;
		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'SUCCESS';
		else
			set Message = 'FAILED_CON1';
            leave sp_Atma_Pending_To_Approval_PR_Product_Set;
		end if;

         SET SQL_SAFE_UPDATES = 0;
			set Query_delete=concat('DELETE FROM atma_tmp_mst_tcontact
											WHERE contact_gid=',c_contact_gid,'');
    set @Insert_query = Query_delete;
	PREPARE stmt FROM @Insert_query;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
    if countRow >  0 then
		set Message = 'SUCCESS';
	else
		set Message = ' FAILED_PARTNER deletion1';
        leave sp_Atma_Pending_To_Approval_PR_Product_Set;
	end if;

		set  @Contact_Gid1='';
		select last_insert_id() into @Contact_Gid1;








				select  contact_gid,Contact_ref_gid,Contact_reftable_gid,
						contact_reftablecode,Contact_contacttype_gid,
						Contact_personname,Contact_designation_gid,Contact_landline,
						Contact_landline2,Contact_mobileno,
						Contact_mobileno2,Contact_email,Contact_DOB,Contact_WD,
						entity_gid,create_by,update_by,main_contact_gid

				into    c_contact_gid,c_Contact_ref_gid,c_Contact_reftable_gid,
						c_contact_reftablecode,c_Contact_contacttype_gid,
						c_Contact_personname,c_Contact_designation_gid,c_Contact_landline,
						c_Contact_landline2,c_Contact_mobileno,
						c_Contact_mobileno2,c_Contact_email,c_Contact_DOB,c_Contact_WD,
						c_entity_gid,c_create_by,c_update_by,c_main_contact_gid
				from  atma_tmp_mst_tcontact where contact_gid=p_partnerproduct_clientcontactgid2 ;




		if c_main_contact_gid = '' or c_main_contact_gid is null  or c_main_contact_gid=0 then

				 set Query_Column='';
				 set Query_Value ='';

            if c_Contact_personname is not null and c_Contact_personname<>'' then
				set Query_Column = concat(Query_Column,',Contact_personname');
				set Query_Value=concat(Query_Value,', ''',c_Contact_personname,''' ');
            end if;

            if c_Contact_landline is not null and c_Contact_landline<>'' then
				set Query_Column = concat(Query_Column,',Contact_landline');
				set Query_Value=concat(Query_Value,', ',c_Contact_landline,' ');
            end if;

            if c_Contact_landline2 is not null and c_Contact_landline2<>'' then
				set Query_Column = concat(Query_Column,',Contact_landline2');
				set Query_Value=concat(Query_Value,', ',c_Contact_landline2,' ');
            end if;

            if c_Contact_mobileno is not null and c_Contact_mobileno<>'' then
				set Query_Column = concat(Query_Column,',Contact_mobileno');
				set Query_Value=concat(Query_Value,', ',c_Contact_mobileno,' ');
            end if;

			if c_Contact_mobileno2 is not null and c_Contact_mobileno2<>'' then
				set Query_Column = concat(Query_Column,',Contact_mobileno2');
				set Query_Value=concat(Query_Value,', ',c_Contact_mobileno2,' ');
            end if;

            if c_Contact_email is not null and c_Contact_email<>'' then
				set Query_Column = concat(Query_Column,',Contact_email');
				set Query_Value=concat(Query_Value,', ''',c_Contact_email,''' ');
            end if;

            if c_Contact_DOB is not null and c_Contact_DOB<>'' then
				set Query_Column = concat(Query_Column,',Contact_DOB');
				set Query_Value=concat(Query_Value,', ''',c_Contact_DOB,''' ');
            end if;

            if c_Contact_WD is not null and c_Contact_WD<>'' then
				set Query_Column = concat(Query_Column,',Contact_WD');
				set Query_Value=concat(Query_Value,', ''',c_Contact_WD,''' ');
            end if;

 set Error_Level='ATMA57.3';
			set Query_Update = concat('INSERT INTO gal_mst_tcontact
											  ( Contact_ref_gid, Contact_reftable_gid, contact_reftablecode,
                                              Contact_contacttype_gid, Contact_designation_gid,
                                              entity_gid, create_by, create_date ',Query_Column,')
									    values (',c_Contact_ref_gid,',',c_Contact_reftable_gid,',
                                        ''',c_contact_reftablecode,''',',c_Contact_contacttype_gid,',
                                        ',c_Contact_designation_gid,',''',c_entity_gid,''',
                                        ''',c_create_by,''' ,''',Now(),''' ',Query_Value,'
                                          )');



         # select c_Contact_ref_gid;

		else
				if c_Contact_DOB is null then
					set Query_Update1 = concat('Contact_DOB = null,');
                else
					set Query_Update1 = concat('Contact_DOB = ''',c_Contact_DOB,''',');
				end if;

                if C_Contact_WD is null then
					set Query_Update1 = concat(Query_Update1,'Contact_WD = null,');
                else
					set Query_Update1 = concat(Query_Update1,'Contact_WD = ''',C_Contact_WD,''',');
				end if;



  set Error_Level='ATMA57.4';
		 	set Query_Update = concat(' Update gal_mst_tcontact
										set Contact_contacttype_gid = ',c_Contact_contacttype_gid,',
                                        Contact_designation_gid = ',c_Contact_designation_gid,',
                                        Contact_personname = ''',ifnull(c_Contact_personname,''),''',
                                        Contact_landline = ''',ifnull(c_Contact_landline,''),''',
                                        Contact_landline2 = ''',ifnull(c_Contact_landline2,''),''',
                                        Contact_mobileno = ''',ifnull(c_Contact_mobileno,''),''',
                                        Contact_mobileno2 = ''',ifnull(c_Contact_mobileno2,''),''',
                                        Contact_email = ''',ifnull(c_Contact_email,''),''',
										',Query_Update1,'
                                        update_by=',@Update_By,',
                                        update_date = ''',now(),'''
										Where contact_gid = ',c_main_contact_gid,'
                                              ');




		end if;
       #select Query_Update,2;
		set @Insert_query = Query_Update;
		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'SUCCESS';
		else
			set Message = 'FAILED_CON2';
			leave sp_Atma_Pending_To_Approval_PR_Product_Set;
		end if;

         SET SQL_SAFE_UPDATES = 0;
			set Query_delete=concat('DELETE FROM atma_tmp_mst_tcontact
											WHERE contact_gid=',c_contact_gid,'');
    set @Insert_query = Query_delete;
	PREPARE stmt FROM @Insert_query;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
    if countRow >  0 then
		set Message = 'SUCCESS';
	else
		set Message = ' FAILED_PARTNER deletion2';
		leave sp_Atma_Pending_To_Approval_PR_Product_Set;
	end if;

        set @Contact_Gid2='';
		select last_insert_id() into @Contact_Gid2;








			select  contact_gid,Contact_ref_gid,Contact_reftable_gid,
						contact_reftablecode,Contact_contacttype_gid,
						Contact_personname,Contact_designation_gid,Contact_landline,
						Contact_landline2,Contact_mobileno,
						Contact_mobileno2,Contact_email,Contact_DOB,Contact_WD,
						entity_gid,create_by,update_by,main_contact_gid

		    into    c_contact_gid,c_Contact_ref_gid,c_Contact_reftable_gid,
						c_contact_reftablecode,c_Contact_contacttype_gid,
						c_Contact_personname,c_Contact_designation_gid,c_Contact_landline,
						c_Contact_landline2,c_Contact_mobileno,
						c_Contact_mobileno2,c_Contact_email,c_Contact_DOB,c_Contact_WD,
						c_entity_gid,c_create_by,c_update_by,c_main_contact_gid
			from  atma_tmp_mst_tcontact where contact_gid=p_partnerproduct_customercontactgid1 ;




		if c_main_contact_gid = '' or c_main_contact_gid is null  or c_main_contact_gid=0 then

				set Query_Column='';
				 set Query_Value ='';

            if c_Contact_personname is not null and c_Contact_personname<>'' then
				set Query_Column = concat(Query_Column,',Contact_personname');
				set Query_Value=concat(Query_Value,', ''',c_Contact_personname,''' ');
            end if;

            if c_Contact_landline is not null and c_Contact_landline<>'' then
				set Query_Column = concat(Query_Column,',Contact_landline');
				set Query_Value=concat(Query_Value,', ',c_Contact_landline,' ');
            end if;

            if c_Contact_landline2 is not null and c_Contact_landline2<>'' then
				set Query_Column = concat(Query_Column,',Contact_landline2');
				set Query_Value=concat(Query_Value,', ',c_Contact_landline2,' ');
            end if;

            if c_Contact_mobileno is not null and c_Contact_mobileno<>'' then
				set Query_Column = concat(Query_Column,',Contact_mobileno');
				set Query_Value=concat(Query_Value,', ',c_Contact_mobileno,' ');
            end if;

			if c_Contact_mobileno2 is not null and c_Contact_mobileno2<>'' then
				set Query_Column = concat(Query_Column,',Contact_mobileno2');
				set Query_Value=concat(Query_Value,', ',c_Contact_mobileno2,' ');
            end if;

            if c_Contact_email is not null and c_Contact_email<>'' then
				set Query_Column = concat(Query_Column,',Contact_email');
				set Query_Value=concat(Query_Value,', ''',c_Contact_email,''' ');
            end if;

            if c_Contact_DOB is not null and c_Contact_DOB<>'' then
				set Query_Column = concat(Query_Column,',Contact_DOB');
				set Query_Value=concat(Query_Value,', ''',c_Contact_DOB,''' ');
            end if;

            if c_Contact_WD is not null and c_Contact_WD<>'' then
				set Query_Column = concat(Query_Column,',Contact_WD');
				set Query_Value=concat(Query_Value,', ''',c_Contact_WD,''' ');
            end if;
 set Error_Level='ATMA57.5';
			set Query_Update = concat('INSERT INTO gal_mst_tcontact
											  ( Contact_ref_gid, Contact_reftable_gid, contact_reftablecode,
                                              Contact_contacttype_gid, Contact_designation_gid,
                                              entity_gid, create_by, create_date ',Query_Column,')
									    values (',c_Contact_ref_gid,',',c_Contact_reftable_gid,',
                                        ''',c_contact_reftablecode,''',',c_Contact_contacttype_gid,',
                                        ',c_Contact_designation_gid,',''',c_entity_gid,''',
                                        ''',c_create_by,''' ,''',Now(),''' ',Query_Value,'
                                          )');





		else
					if c_Contact_DOB is null then
					set Query_Update1 = concat('Contact_DOB = null,');
                else
					set Query_Update1 = concat('Contact_DOB = ''',c_Contact_DOB,''',');
				end if;

                if C_Contact_WD is null then
					set Query_Update1 = concat(Query_Update1,'Contact_WD = null,');
                else
					set Query_Update1 = concat(Query_Update1,'Contact_WD = ''',C_Contact_WD,''',');
				end if;



   set Error_Level='ATMA57.6';
		 	set Query_Update = concat(' Update gal_mst_tcontact
										set Contact_contacttype_gid = ',c_Contact_contacttype_gid,',
                                        Contact_designation_gid = ',c_Contact_designation_gid,',
                                        Contact_personname = ''',ifnull(c_Contact_personname,''),''',
                                        Contact_landline = ''',ifnull(c_Contact_landline,''),''',
                                        Contact_landline2 = ''',ifnull(c_Contact_landline2,''),''',
                                        Contact_mobileno = ''',ifnull(c_Contact_mobileno,''),''',
                                        Contact_mobileno2 = ''',ifnull(c_Contact_mobileno2,''),''',
                                        Contact_email = ''',ifnull(c_Contact_email,''),''',
										',Query_Update1,'
                                        update_by=',@Update_By,',
                                        update_date = ''',now(),'''
										Where contact_gid = ',c_main_contact_gid,'
                                              ');




		end if;
        #select Query_Update,3;
		set @Insert_query = Query_Update;
		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'SUCCESS';
		else
			set Message = 'FAILED_CON3';
			leave sp_Atma_Pending_To_Approval_PR_Product_Set;
		end if;

        SET SQL_SAFE_UPDATES = 0;
			set Query_delete=concat('DELETE FROM atma_tmp_mst_tcontact
											WHERE contact_gid=',c_contact_gid,'');
    set @Insert_query = Query_delete;
	PREPARE stmt FROM @Insert_query;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
    if countRow >  0 then
		set Message = 'SUCCESS';
	else
		set Message = ' FAILED_PARTNER deletion3';
		leave sp_Atma_Pending_To_Approval_PR_Product_Set;
	end if;

        set @Contact_Gid3='';
		select last_insert_id() into @Contact_Gid3;


			select  contact_gid,Contact_ref_gid,Contact_reftable_gid,
						contact_reftablecode,Contact_contacttype_gid,
						Contact_personname,Contact_designation_gid,Contact_landline,
						Contact_landline2,Contact_mobileno,
						Contact_mobileno2,Contact_email,Contact_DOB,Contact_WD,
						entity_gid,create_by,update_by,main_contact_gid

			into    c_contact_gid,c_Contact_ref_gid,c_Contact_reftable_gid,
						c_contact_reftablecode,c_Contact_contacttype_gid,
						c_Contact_personname,c_Contact_designation_gid,c_Contact_landline,
						c_Contact_landline2,c_Contact_mobileno,
						c_Contact_mobileno2,c_Contact_email,c_Contact_DOB,c_Contact_WD,
						c_entity_gid,c_create_by,c_update_by,c_main_contact_gid
				from  atma_tmp_mst_tcontact where contact_gid=p_partnerproduct_customercontactgid2 ;




		if c_main_contact_gid = '' or c_main_contact_gid is null  or c_main_contact_gid=0 then


				set Query_Column='';
				 set Query_Value ='';

            if c_Contact_personname is not null and c_Contact_personname<>'' then
				set Query_Column = concat(Query_Column,',Contact_personname');
				set Query_Value=concat(Query_Value,', ''',c_Contact_personname,''' ');
            end if;

            if c_Contact_landline is not null and c_Contact_landline<>'' then
				set Query_Column = concat(Query_Column,',Contact_landline');
				set Query_Value=concat(Query_Value,', ',c_Contact_landline,' ');
            end if;

            if c_Contact_landline2 is not null and c_Contact_landline2<>'' then
				set Query_Column = concat(Query_Column,',Contact_landline2');
				set Query_Value=concat(Query_Value,', ',c_Contact_landline2,' ');
            end if;

            if c_Contact_mobileno is not null and c_Contact_mobileno<>'' then
				set Query_Column = concat(Query_Column,',Contact_mobileno');
				set Query_Value=concat(Query_Value,', ',c_Contact_mobileno,' ');
            end if;

			if c_Contact_mobileno2 is not null and c_Contact_mobileno2<>'' then
				set Query_Column = concat(Query_Column,',Contact_mobileno2');
				set Query_Value=concat(Query_Value,', ',c_Contact_mobileno2,' ');
            end if;

            if c_Contact_email is not null and c_Contact_email<>'' then
				set Query_Column = concat(Query_Column,',Contact_email');
				set Query_Value=concat(Query_Value,', ''',c_Contact_email,''' ');
            end if;

            if c_Contact_DOB is not null and c_Contact_DOB<>'' then
				set Query_Column = concat(Query_Column,',Contact_DOB');
				set Query_Value=concat(Query_Value,', ''',c_Contact_DOB,''' ');
            end if;

            if c_Contact_WD is not null and c_Contact_WD<>'' then
				set Query_Column = concat(Query_Column,',Contact_WD');
				set Query_Value=concat(Query_Value,', ''',c_Contact_WD,''' ');
            end if;
  set Error_Level='ATMA57.7';
			set Query_Update = concat('INSERT INTO gal_mst_tcontact
											  ( Contact_ref_gid, Contact_reftable_gid, contact_reftablecode,
                                              Contact_contacttype_gid, Contact_designation_gid,
                                              entity_gid, create_by, create_date ',Query_Column,')
									    values (',c_Contact_ref_gid,',',c_Contact_reftable_gid,',
                                        ''',c_contact_reftablecode,''',',c_Contact_contacttype_gid,',
                                        ',c_Contact_designation_gid,',''',c_entity_gid,''',
                                        ''',c_create_by,''' ,''',Now(),''' ',Query_Value,'
                                          )');





		else
                if c_Contact_DOB is null then
					set Query_Update1 = concat('Contact_DOB = null,');
                else
					set Query_Update1 = concat('Contact_DOB = ''',c_Contact_DOB,''',');
				end if;

                if C_Contact_WD is null then
					set Query_Update1 = concat(Query_Update1,'Contact_WD = null,');
                else
					set Query_Update1 = concat(Query_Update1,'Contact_WD = ''',C_Contact_WD,''',');
				end if;



   set Error_Level='ATMA57.8';
		 	set Query_Update = concat(' Update gal_mst_tcontact
										set Contact_contacttype_gid = ',c_Contact_contacttype_gid,',
											Contact_designation_gid = ',c_Contact_designation_gid,',
											Contact_personname = ''',ifnull(c_Contact_personname,''),''',
											Contact_landline = ''',ifnull(c_Contact_landline,''),''',
											Contact_landline2 = ''',ifnull(c_Contact_landline2,''),''',
											Contact_mobileno = ''',ifnull(c_Contact_mobileno,''),''',
											Contact_mobileno2 = ''',ifnull(c_Contact_mobileno2,''),''',
											Contact_email = ''',ifnull(c_Contact_email,''),''',
											',Query_Update1,'
											update_by=',@Update_By,',
											update_date = ''',now(),'''
										Where contact_gid = ',c_main_contact_gid,'
                                              ');




		end if;
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
			leave sp_Atma_Pending_To_Approval_PR_Product_Set;
		end if;


         SET SQL_SAFE_UPDATES = 0;
			set Query_delete=concat('DELETE FROM atma_tmp_mst_tcontact
											WHERE contact_gid=',c_contact_gid,'');
    set @Insert_query = Query_delete;
	PREPARE stmt FROM @Insert_query;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
    if countRow >  0 then
		set Message = 'SUCCESS';
	else
		set Message = ' FAILED_PARTNER deletion4';
		leave sp_Atma_Pending_To_Approval_PR_Product_Set;
	end if;

        set  @Contact_Gid4='';
		select last_insert_id() into @Contact_Gid4;





		if p_main_partnerproduct_gid = '' or p_main_partnerproduct_gid is null  or p_main_partnerproduct_gid=0 then

				set Query_Column ='';
				set Query_Value ='';

			if p_partnerproduct_age is not null and p_partnerproduct_age<>'' then
				set Query_Column = concat(Query_Column,',partnerproduct_age');
				set Query_Value=concat(Query_Value,', ',p_partnerproduct_age,' ');
            end if;

			if @Contact_Gid2 is not null and @Contact_Gid2<>'' then
				set Query_Column = concat(Query_Column,',partnerproduct_clientcontactgid2');
				set Query_Value=concat(Query_Value,', ',@Contact_Gid2,' ');
            end if;

			if @Contact_Gid4 is not null and @Contact_Gid4<>'' then
				set Query_Column = concat(Query_Column,',partnerproduct_customercontactgid2');
				set Query_Value=concat(Query_Value,', ',@Contact_Gid4,' ');
            end if;
   set Error_Level='ATMA57.9';
			set Query_Update = concat('INSERT INTO atma_mst_tpartnerproduct
											  (partnerproduct_partnergid, partnerproduct_type, partnerproduct_name,
                                              partnerproduct_clientcontactgid1,partnerproduct_customercontactgid1,
                                              partnerproduct_isactive, partnerproduct_isremoved, entity_gid,
                                              create_by,create_date ',Query_Column,')
										values (',Partner_Gid,',''',p_partnerproduct_type,''',
                                        ''',p_partnerproduct_name,''',',@Contact_Gid1,',',@Contact_Gid3,',
                                        ''',p_partnerproduct_isactive,''',''',p_partnerproduct_isremoved,''',
                                        ',p_entity_gid,',',p_create_by,',''',Now(),''' ',Query_Value,'
                                          )');


           # select Query_Update;

		 else
  set Error_Level='ATMA57.10';
		set Query_Update = concat('Update atma_mst_tpartnerproduct
										  set partnerproduct_type = ''',p_partnerproduct_type,''',
                                          partnerproduct_age = ''',ifnull(p_partnerproduct_age,0),''',
                                          partnerproduct_name = ''',p_partnerproduct_name,''',
                                          update_date = ''',now(),''',
                                          update_by=',@Update_By,'
										  Where partnerproduct_gid = ',p_main_partnerproduct_gid,'
                                              ');



		end if;

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
			leave sp_Atma_Pending_To_Approval_PR_Product_Set;
		end if;
	End loop atma_looop;
	close Cursor_atma;
	end;


     SET SQL_SAFE_UPDATES = 0;
				set Query_delete=concat('DELETE FROM atma_tmp_mst_tpartnerproduct
											WHERE partnerproduct_gid=',p_partnerproduct_gid,'');

    set @Insert_query = Query_delete;
	PREPARE stmt FROM @Insert_query;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
    if countRow >  0 then
		set Message = 'SUCCESS';
	else
		set Message = ' FAILED_PARTNER deletion5';
		leave sp_Atma_Pending_To_Approval_PR_Product_Set;
	end if;




END