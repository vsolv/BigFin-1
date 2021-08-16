CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Pending_To_Approval_PR_Client_Set`(
in lj_filter json,in Partner_Gid int,in lj_classification json,out Message varchar(1000))
sp_Atma_Pending_To_Approval_PR_Client_Set:BEGIN

declare Query_Insert varchar(10000);
Declare countRow varchar(6000);
declare Query_Update varchar(10000);
declare Query_delete varchar(1000);
declare Query_Value varchar(1000);
declare Query_Column varchar(1000);

Declare  c_partnerclient_gid,c_partnerclient_partnergid,c_partnerclient_name,
		 c_partnerclient_addressgid,c_partnerclient_isactive,c_partnerclient_isremoved,
		 c_entity_gid,c_create_by,c_update_by,c_main_partnerclient_gid varchar(150);

Declare  a_address_gid, a_address_ref_code,a_address_1,a_address_2,a_address_3,a_address_pincode,
		 a_address_district_gid,a_address_city_gid,a_address_state_gid,a_entity_gid,a_create_by,
		 a_update_by,a_main_address_gid varchar(150);

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
		leave sp_Atma_Pending_To_Approval_PR_Client_Set;
	End if;

	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Gid')))
	into @Partner_Gid;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Update_By')))
    into @Update_By;

	if @Partner_Gid = '' or @Partner_Gid is null  or @Partner_Gid=0 then
			set Message = 'Partner Is Not Provided';
			leave sp_Atma_Pending_To_Approval_PR_Client_Set;
	End if;

 SET finished =0;

BEGIN
	Declare Cursor_atma CURSOR FOR

		select	    partnerclient_gid, partnerclient_partnergid, partnerclient_name,
			    	partnerclient_addressgid, partnerclient_isactive, partnerclient_isremoved,
				    entity_gid, create_by,  update_by,  main_partnerclient_gid
					from atma_tmp_mst_tpartnerclient
					where partnerclient_partnergid=@Partner_Gid;

	DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;
	OPEN Cursor_atma;
	atma_looop:loop
		fetch Cursor_atma into  c_partnerclient_gid,c_partnerclient_partnergid,c_partnerclient_name,
								c_partnerclient_addressgid,c_partnerclient_isactive,c_partnerclient_isremoved,
								c_entity_gid,c_create_by,c_update_by,c_main_partnerclient_gid ;
            SET @Address_Gid=1;
	 if finished = 1 then
			leave atma_looop;
		End if;

						select  address_gid, address_ref_code,address_1,address_2,address_3,address_pincode,
								address_district_gid,address_city_gid,address_state_gid,entity_gid,create_by,
								update_by,main_address_gid
						into    a_address_gid, a_address_ref_code,a_address_1,a_address_2,a_address_3,
								a_address_pincode,a_address_district_gid,a_address_city_gid,
								a_address_state_gid,a_entity_gid,a_create_by,a_update_by,a_main_address_gid
							from atma_tmp_mst_taddress
							where address_gid=c_partnerclient_addressgid ;


		if a_main_address_gid = '' or a_main_address_gid is null  or a_main_address_gid=0 then
			 set Query_Column='';
				set Query_Value ='';

				if a_address_1 is not null and a_address_1 <>'' then
					set Query_Column = concat(Query_Column,',address_1 ');
					set Query_Value=concat(Query_Value,', ''',a_address_1,''' ');
				end if;

                if a_address_2 is not null and a_address_2 <>'' then
					set Query_Column = concat(Query_Column,',address_2 ');
					set Query_Value=concat(Query_Value,', ''',a_address_2,''' ');
				end if;

                if a_address_3 is not null and a_address_3 <>'' then
					set Query_Column = concat(Query_Column,',address_3 ');
					set Query_Value=concat(Query_Value,', ''',a_address_3,''' ');
				end if;

                if a_address_pincode is not null  and a_address_pincode <>'' then
					set Query_Column = concat(Query_Column,',address_pincode ');
					set Query_Value=concat(Query_Value,', ',a_address_pincode,' ');
				end if;

				if a_address_city_gid is not null and a_address_city_gid <>'' then
					set Query_Column = concat(Query_Column,',address_city_gid ');
					set Query_Value=concat(Query_Value,', ',a_address_city_gid,' ');
				end if;

				if a_address_state_gid is not null and a_address_state_gid <>'' then
					set Query_Column = concat(Query_Column,',address_state_gid ');
					set Query_Value=concat(Query_Value,', ',a_address_state_gid,' ');
				end if;
            #select Query_Column,Query_Value;
set Error_Level='ATMA55.1';
			set Query_Update = concat('INSERT INTO gal_mst_taddress
											  ( address_ref_code,address_district_gid,
                                                entity_gid, create_by, create_date ',Query_Column,')
									    values (''',a_address_ref_code,''',',a_address_district_gid,',
												',a_entity_gid,',',a_create_by,',''',Now(),'''
												',Query_Value,')'
									  );
			#select p_partnerbranch_remarks;
			#select Query_Update;



		else
set Error_Level='ATMA55.2';
		 	set Query_Update = concat('Update gal_mst_taddress
									   set  address_1 = ''',ifnull(a_address_1,''),''',
										    address_2 = ''',ifnull(a_address_2,''),''',
										    address_3 = ''',ifnull(a_address_3,''),''',
										    address_pincode =',ifnull(a_address_pincode,''),',
											address_city_gid = ',ifnull(a_address_city_gid,''),',
											address_state_gid = ',ifnull(a_address_state_gid,''),',
                                            address_district_gid =  ',a_address_district_gid,',
                                            update_date = CURRENT_TIMESTAMP,
											Update_By = ',@Update_By,'
											where address_gid=',a_main_address_gid,'
                                              ');

			/*SET SQL_SAFE_UPDATES = 0;
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
		set Message = ' FAILED_PARTNER deletion';
		leave sp_Atma_Pending_To_Approval_PR_Client_Set;
	end if;*/


		end if;

        #select Query_Update;
		set @Insert_query = Query_Update;
		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'SUCCESS';
		else
			set Message = 'FAILED_CL';
			leave sp_Atma_Pending_To_Approval_PR_Client_Set;
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
		set Message = ' FAILED_PARTNER deletion';
		leave sp_Atma_Pending_To_Approval_PR_Client_Set;
	end if;

        set @Address_Gid='';
		select LAST_INSERT_ID() into @Address_Gid ;

  #------------------------------------------------
  #------------------------------------------------
  #------------------------------------------------
  #------------------------------------------------



		if c_main_partnerclient_gid = '' or c_main_partnerclient_gid is null  or c_main_partnerclient_gid=0 then
set Error_Level='ATMA55.3';

			set Query_Update = concat('INSERT INTO atma_mst_tpartnerclient
												(partnerclient_partnergid,partnerclient_name,
												partnerclient_addressgid,partnerclient_isactive,
                                                partnerclient_isremoved,entity_gid,create_by)
									    values(',Partner_Gid,',''',c_partnerclient_name,''',
												',@Address_Gid,',''',c_partnerclient_isactive,''',
                                                ''',c_partnerclient_isremoved,''',',c_entity_gid,',
                                                ',c_create_by,')'
							);
			#select p_main_partnerproduct_gid;


		#select Query_Update;
		 else
set Error_Level='ATMA55.4';
		set Query_Update = concat('Update atma_mst_tpartnerclient
											set
											Partnerclient_name = ''',c_partnerclient_name,''',
                                            update_by = ',@Update_By,',
											update_date = ''',NOW(),'''
											Where partnerclient_gid = ',c_main_partnerclient_gid,' ');



		end if;
        #select Query_Update;
		set @Insert_query = Query_Update;
		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'SUCCESS';
		else
			set Message = 'FAILED_CL';
			leave sp_Atma_Pending_To_Approval_PR_Client_Set;
		end if;
	End loop atma_looop;
	close Cursor_atma;
	end;  #Endof Cursor



    SET SQL_SAFE_UPDATES = 0;
				set Query_delete=concat('DELETE FROM atma_tmp_mst_tpartnerclient
											WHERE partnerclient_gid=',c_partnerclient_gid,'');

    set @Insert_query = Query_delete;
	PREPARE stmt FROM @Insert_query;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
    if countRow >  0 then
		set Message = 'SUCCESS';
	else
		set Message = ' FAILED_PARTNER deletion';
		leave sp_Atma_Pending_To_Approval_PR_Client_Set;
	end if;


END