CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Pending_To_Approval_PR_Branch_Set`(
in lj_filter json,in Partner_Gid int,in lj_classification json,out Message varchar(1000))
sp_Atma_Pending_To_Approval_PR_Branch_Set:BEGIN

declare Query_Insert varchar(10000);
Declare countRow varchar(6000);
declare Query_Update varchar(10000);
declare Query_delete varchar(1000);
declare Query_Update1 varchar(1000);
declare Query_Value varchar(1000);
declare Query_Column varchar(1000);

Declare  p_partnerbranch_gid,p_partnerbranch_gstno,p_partnerbranch_panno,p_partnerbranch_code,p_partnerbranch_partnergid,p_partnerbranch_name,
		 p_partnerbranch_addressgid,p_partnerbranch_contactgid,
         p_partnerbranch_creditperiod,p_partnerbranch_creditlimit,p_partnerbranch_paymentterms,
         p_partnerbranch_remarks,
		 p_partnerbranch_isactive,p_partnerbranch_isremoved,p_entity_gid,p_create_by,
		 p_create_date,p_update_by,p_update_date,p_main_partnerbranch_gid varchar(150);

Declare  a_address_gid,a_address_ref_code,a_address_1, a_address_2, a_address_3, a_address_pincode,
		 a_address_district_gid,a_address_city_gid, a_address_state_gid, a_entity_gid,
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
							set Message = concat(Error_Level,':No-',errno,msg);
							ROLLBACK;
						END;

	select JSON_LENGTH(lj_filter,'$') into @lj_filter_json_count;
	select JSON_LENGTH(lj_classification,'$') into @lj_classification_json_count;

	if @lj_filter_json_count = 0 or @lj_filter_json_count is null then
		set Message = 'No Data In filter Json. ';
		leave sp_Atma_Pending_To_Approval_PR_Branch_Set;
	End if;

	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Gid')))
	into @Partner_Gid_tmp;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Update_By')))
    into @Update_By;


	if @Partner_Gid_tmp = '' or @Partner_Gid_tmp is null  or @Partner_Gid_tmp=0 then
			set Message = 'Partner Is Not Provided';
			leave sp_Atma_Pending_To_Approval_PR_Branch_Set;
	End if;

   SELECT EXISTS(
         select true from  atma_tmp_mst_tpartnerbranch
						where partnerbranch_partnergid=@Partner_Gid_tmp) into @pp_branch;

	if @pp_branch=1 then



    		SET finished =0;

BEGIN
	Declare Cursor_atma1 CURSOR FOR

	select partnerbranch_gid,partnerbranch_gstno,partnerbranch_panno,partnerbranch_code,partnerbranch_partnergid,partnerbranch_name,
		   partnerbranch_addressgid,partnerbranch_contactgid,partnerbranch_creditperiod,partnerbranch_creditlimit,
           partnerbranch_paymentterms,partnerbranch_remarks,
		   partnerbranch_isactive,partnerbranch_isremoved,entity_gid,create_by,
		   create_date,update_by,update_date,main_partnerbranch_gid
		   from atma_tmp_mst_tpartnerbranch where partnerbranch_partnergid=@Partner_Gid_tmp ;

	DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;
	OPEN Cursor_atma1;
	atma_loop1:loop
		fetch Cursor_atma1 into p_partnerbranch_gid,p_partnerbranch_gstno,p_partnerbranch_panno,p_partnerbranch_code,p_partnerbranch_partnergid,p_partnerbranch_name,
							    p_partnerbranch_addressgid,p_partnerbranch_contactgid,
                                p_partnerbranch_creditperiod,p_partnerbranch_creditlimit,p_partnerbranch_paymentterms,
                                p_partnerbranch_remarks,
							    p_partnerbranch_isactive,p_partnerbranch_isremoved,p_entity_gid,p_create_by,
							    p_create_date,p_update_by,p_update_date,p_main_partnerbranch_gid;

	 if finished = 1 then
			leave atma_loop1;
		End if;




        select  address_gid,address_ref_code,address_1,address_2,address_3,address_pincode,
						address_district_gid,address_city_gid,address_state_gid,entity_gid,
						create_by,update_by,main_address_gid
                        into a_address_gid,a_address_ref_code,a_address_1,a_address_2,a_address_3,
							 a_address_pincode,a_address_district_gid,a_address_city_gid,
							 a_address_state_gid,a_entity_gid,a_create_by ,a_update_by,a_main_address_gid
						from atma_tmp_mst_taddress
                        where address_gid=p_partnerbranch_addressgid ;

            #select a_main_address_gid;
		if a_main_address_gid = '' or a_main_address_gid is null  or a_main_address_gid=0 then

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
            #select Query_Column,Query_Value;
set Error_Level='ATMA54.1';
			set Query_Update = concat('INSERT INTO gal_mst_taddress
											  ( address_ref_code,address_district_gid,
                                                entity_gid, create_by, create_date ',Query_Column,')
									    values (''',a_address_ref_code,''',',a_address_district_gid,',
												',a_entity_gid,',',a_create_by,',''',Now(),'''
												',Query_Value,')'
									  );

			#select p_partnerbranch_remarks;



		else
				if a_update_by is null then
					set message = concat('a_update_by cant be null');
				end if;
set Error_Level='ATMA54.2';
		 	set Query_Update = concat('Update gal_mst_taddress
									   set  address_1 = ''',ifnull(a_address_1,''),''',
										    address_2 = ''',ifnull(a_address_2,''),''',
										    address_3 = ''',ifnull(a_address_3,''),''',
										    address_pincode =''',ifnull(a_address_pincode,''),''',
											address_city_gid = ',ifnull(a_address_city_gid,0),',
											address_state_gid = ',ifnull(a_address_state_gid,0),',
                                            address_district_gid =  ',a_address_district_gid,',
                                            update_date = CURRENT_TIMESTAMP,
											Update_By = ',@Update_By,'
										where address_gid=',a_main_address_gid,'
                                              ');



		end if;



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
			leave sp_Atma_Pending_To_Approval_PR_Branch_Set;
		end if;

        SET SQL_SAFE_UPDATES = 0;
			set Query_delete=concat('DELETE FROM atma_tmp_mst_taddress
											WHERE address_gid=',a_address_gid,'');
    set @Insert_query = Query_delete;

	PREPARE stmt FROM @Insert_query;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
    if countRow >  0 then
		set Message = 'SUCCESS';
	else
		set Message = ' FAILED_PARTNER_Add deletion';
		leave sp_Atma_Pending_To_Approval_PR_Branch_Set;
	end if;

			set @Address_Gid='';
            select last_insert_id() into @Address_Gid;
			#select max(address_gid) from gal_mst_taddress  into @Address_Gid;


				select  contact_gid,Contact_ref_gid,Contact_reftable_gid,
						contact_reftablecode,Contact_contacttype_gid,
						Contact_personname,Contact_designation_gid,Contact_landline,
						Contact_landline2,Contact_mobileno,
						Contact_mobileno2,Contact_email,Contact_DOB,Contact_WD,
						entity_gid,create_by,update_by,main_contact_gid
                        into c_contact_gid,c_Contact_ref_gid,c_Contact_reftable_gid,
							 c_contact_reftablecode,c_Contact_contacttype_gid,
							 c_Contact_personname,c_Contact_designation_gid,c_Contact_landline,
							 c_Contact_landline2,c_Contact_mobileno,
							 c_Contact_mobileno2,c_Contact_email,c_Contact_DOB,c_Contact_WD,
							 c_entity_gid,c_create_by,c_update_by,c_main_contact_gid
						from   atma_tmp_mst_tcontact
                        where contact_gid=p_partnerbranch_contactgid ;



		if c_main_contact_gid = '' or c_main_contact_gid is null  or c_main_contact_gid=0 then

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

set Error_Level='ATMA54.3';
			set Query_Update = concat('INSERT INTO gal_mst_tcontact
											  ( Contact_ref_gid, Contact_reftable_gid, contact_reftablecode,
                                              Contact_contacttype_gid, Contact_designation_gid,
                                              entity_gid, create_by, create_date ',Query_Column,')
									    values (',c_Contact_ref_gid,',',c_Contact_reftable_gid,',
												''',c_contact_reftablecode,''',',c_Contact_contacttype_gid,',
												',c_Contact_designation_gid,',',c_entity_gid,',',c_create_by,' ,
												''',Now(),''' ',Query_Value,')'
									 );
			#select p_partnerbranch_remarks;
			#select Query_Update;


		else
				set Query_Update1='';
				if c_Contact_DOB is null  then
					set Query_Update1 = concat('Contact_DOB = null,');
                else
					set Query_Update1 = concat('Contact_DOB = ''',c_Contact_DOB,''',');
				end if;

                if c_Contact_WD is null  then
					set Query_Update1 = concat(Query_Update1,'Contact_WD = null,');
                else
					set Query_Update1 = concat(Query_Update1,'Contact_WD = ''',c_Contact_WD,''',');
				end if;
                    #Contact_DOB = ''',ifnull(c_Contact_DOB,'0000-00-00 00:00:00'),''',
					# Contact_WD = ''',ifnull(C_Contact_WD,'0000-00-00 00:00:00'),''',
set Error_Level='ATMA54.4';
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
                                        Update_By=',@Update_By,',
                                        update_date = ''',now(),'''
										Where contact_gid = ',c_main_contact_gid,'
                                              ');


		end if;



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
			leave sp_Atma_Pending_To_Approval_PR_Branch_Set;
		end if;

         SET SQL_SAFE_UPDATES = 0;
			set Query_delete=concat('DELETE FROM atma_tmp_mst_tcontact
											WHERE contact_gid=',c_contact_gid,'');
    #select Query_delete,c_contact_gid;
    set @Insert_query = Query_delete;
	PREPARE stmt FROM @Insert_query;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
    if countRow >  0 then
		set Message = 'SUCCESS';
	else
		set Message = ' FAILED_PARTNER_C deletion';
		leave sp_Atma_Pending_To_Approval_PR_Branch_Set;
	end if;




        set @Contact_Gid='';
            select last_insert_id() into @Contact_Gid;

            #select max(contact_gid) from gal_mst_tcontact  into @Contact_Gid;




		if p_main_partnerbranch_gid = '' or p_main_partnerbranch_gid is null  or p_main_partnerbranch_gid=0 then



				set Query_Column='';
				set Query_Value ='';

            if p_partnerbranch_remarks is not null and p_partnerbranch_remarks <>'' then
				set Query_Column = concat(Query_Column,',partnerbranch_remarks');
				set Query_Value=concat(Query_Value,', ''',p_partnerbranch_remarks,''' ');
            end if;

            if p_partnerbranch_gstno is not null and p_partnerbranch_gstno <>'' then
				set Query_Column = concat(Query_Column,',partnerbranch_gstno');
				set Query_Value=concat(Query_Value,', ''',p_partnerbranch_gstno,''' ');
            end if;
            if p_partnerbranch_panno is not null and p_partnerbranch_panno <>'' then
				set Query_Column = concat(Query_Column,',partnerbranch_panno');
				set Query_Value=concat(Query_Value,', ''',p_partnerbranch_panno,''' ');
            end if;
set Error_Level='ATMA54.5';
			set Query_Update = concat('INSERT INTO atma_mst_tpartnerbranch
											  (
                                              partnerbranch_code,partnerbranch_partnergid, partnerbranch_name,
                                              partnerbranch_addressgid,partnerbranch_contactgid,
                                              partnerbranch_creditperiod,partnerbranch_creditlimit,
                                              partnerbranch_paymentterms,
                                              partnerbranch_isactive,partnerbranch_isremoved,entity_gid,
                                              create_by,create_date ',Query_Column,')
										values (''',p_partnerbranch_code,''',',Partner_Gid,',''',p_partnerbranch_name,''',
                                        ',@Address_Gid,',',@Contact_Gid,',''',p_partnerbranch_creditperiod,''',
                                        ''',p_partnerbranch_creditlimit,'''
                                        ,''',ifnull(p_partnerbranch_paymentterms,''),''',
                                          ''',p_partnerbranch_isactive,''',
                                          ''',p_partnerbranch_isremoved,''',',p_entity_gid,'
											,',p_create_by,',''',Now(),''' ',Query_Value,'
                                          )');
			#select p_partnerbranch_remarks;
           # select Query_Update;

		else
					if p_update_by is null then
						set message = concat('p_update_by cant be null');
					end if;

set Error_Level='ATMA54.6';
		 	set Query_Update = concat('Update atma_mst_tpartnerbranch
										  set
											  partnerbranch_gstno=''',ifnull(p_partnerbranch_gstno,''),''',
											  partnerbranch_panno=''',ifnull(p_partnerbranch_panno,''),''',
											  partnerbranch_creditperiod=''',p_partnerbranch_creditperiod,''',
                                              partnerbranch_creditlimit=''',p_partnerbranch_creditlimit,''',
                                              partnerbranch_paymentterms=''',ifnull(p_partnerbranch_paymentterms,''),''',
											  partnerbranch_remarks=''',ifnull(p_partnerbranch_remarks,''),''',
											  partnerbranch_isactive=''',p_partnerbranch_isactive,''',
                                              partnerbranch_isremoved=''',p_partnerbranch_isremoved,''',
                                              entity_gid=',p_entity_gid,',
                                              update_by=',@Update_By,',
                                              update_date=''',now(),'''
                                              where partnerbranch_gid=',p_main_partnerbranch_gid,'
                                              ');


		end if;

        #select Query_Update ,'BR';
		set @Insert_query = Query_Update;
		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'SUCCESS';
            #select 1;
		else
			set Message = ' FAILED_BR';
			leave sp_Atma_Pending_To_Approval_PR_Branch_Set;
		end if;



    set @NEWpartnerbranchgid='';
	select LAST_INSERT_ID() into @NEWpartnerbranchgid;

		select main_partnerbranch_gid from atma_tmp_mst_tpartnerbranch
		where partnerbranch_partnergid=@Partner_Gid into @maingid_branch;

        if @maingid_branch > 0 then
		set @NEWpartnerbranchgid=@maingid_branch;
       # else
        #set @NEWpartnerbranchgid=@NEWpartnerbranchgid;
		end if;




	set @lj_filter='';

    set @lj_filter= concat('{"Partner_Gid":"',@Partner_Gid_tmp,'","newpartnerbranchgid":',@NEWpartnerbranchgid,',
    "oldpartnerbranchgid":',p_partnerbranch_gid,'
							}');

#select @lj_filter,1;
#select 'Insert',@lj_filter,Partner_Gid,lj_classification;
#select 1;
set Error_Level='ATMA54.7';
call sp_Atma_Pending_To_Approval_payment_Set('Insert',@lj_filter,Partner_Gid,lj_classification,@Message);
select @Message into @Out_Message_payment;

	if  @Out_Message_payment <> 'SUCCESS' then
    #select @Out_Message_payment;
			set Message = @Out_Message_payment;
            #select @Out_Message_payment;
			leave sp_Atma_Pending_To_Approval_PR_Branch_Set;
	End if;
set Error_Level='ATMA54.8';
call sp_Atma_Pending_To_Approval_Activity_Set('Insert',@lj_filter,Partner_Gid,lj_classification,@Message);
	select @Message into @Out_Message_Activity;
	if  @Out_Message_Activity <> 'SUCCESS' then
		#select @Out_Message_Activity;
		set Message = @Out_Message_Activity;
		#rollback;
		leave sp_Atma_Pending_To_Approval_PR_Branch_Set;
	End if;

    End loop atma_loop1;
	close Cursor_atma1;
	end;  #Endof Cursor1

     #####set Message ='FAIL';
     #####rollback;
     #####leave sp_Atma_Pending_To_Approval_PR_Branch_Set;

        SET SQL_SAFE_UPDATES = 0;
		set Query_delete=concat('DELETE FROM atma_tmp_mst_tpartnerbranch
											WHERE partnerbranch_partnergid=',@Partner_Gid_tmp,'');
    set @Insert_query = Query_delete;
	PREPARE stmt FROM @Insert_query;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
    if countRow >  0 then
		set Message = 'SUCCESS';
	else
		set Message = ' FAILED_PARTNER deletion';
        leave sp_Atma_Pending_To_Approval_PR_Branch_Set;
	end if;


end if; ###@pp_branch

END