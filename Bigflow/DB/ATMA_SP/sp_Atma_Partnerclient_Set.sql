CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Partnerclient_Set`(in ls_Action varchar(20),
in lj_filter json,in lj_classification json,
out Message varchar(1000))
sp_Atma_Partnerclient_Set:BEGIN
declare Query_Insert varchar(1000);
Declare countRow varchar(6000);
Declare Query_Update varchar(1000);
Declare Query_Value varchar(1000);
Declare Query_Column varchar(1000);
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
	select JSON_LENGTH(lj_filter,'$') into @li_filter_jsoncount;
	select JSON_LENGTH(lj_classification,'$') into @li_classification_jsoncount;

	if @li_filter_jsoncount = 0 or @li_filter_jsoncount is null  then
		set Message = 'No Data In Json. ';
		leave sp_Atma_Partnerclient_Set;
	End if;

    if @li_classification_jsoncount = 0 or @li_classification_jsoncount = '' or @li_classification_jsoncount is null  then
			set Message = 'No Entity_Gid and Create by In Json. ';
			leave sp_Atma_Partnerclient_Set;
	End if;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Entity_Gid')))into @Entity_Gid;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Create_By')))into @Create_By;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Address_1')))into @Address_1;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Address_2')))into @Address_2;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Address_3')))into @Address_3;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Address_Pincode')))into @Address_Pincode;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Address_District_gid')))into @Address_District_gid;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Address_City_gid')))into @Address_City_gid;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Address_State_gid')))into @Address_State_gid;

	select fn_REFCode('PARTNERCLIENT_ADDRESS') INTO @Address_Ref_Code ;
	if @Entity_Gid = 0 or @Entity_Gid = '' or @Entity_Gid is null  then
		set Message ='Entity Gid Is Not Given';
		rollback;
		leave sp_Atma_Partnerclient_Set;
	end if;

	if @Create_By = 0 or @Create_By = '' or @Create_By is null  then
		set Message ='Create By Is Not Given';
		rollback;
		leave sp_Atma_Partnerclient_Set;
	end if;

	if @Address_District_gid = 0 or @Address_District_gid = '' or @Address_District_gid is null  then
		set Message ='Address District Is Not Given';
		rollback;
		leave sp_Atma_Partnerclient_Set;
	end if;

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
    set Query_Insert='';

	set Query_Insert=concat('insert into atma_tmp_mst_taddress(address_ref_code,address_district_gid,
		entity_gid,create_by',Query_Column,')
		values(''',@Address_Ref_Code,''',',@Address_District_gid,',
		',@Entity_Gid,',',@Create_By,'',Query_Value,')'
	);
	#select Query_Insert;
	set @Insert_query = Query_Insert;
	PREPARE stmt FROM @Insert_query;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
	if countRow >  0 then
		set Message = 'SUCCESSFULLY INSERTED';
	else
		set Message = 'INSERT FAILED';
		rollback;
        leave sp_Atma_Partnerclient_Set;
	end if;

	select LAST_INSERT_ID() into @Address_Gid ;
	#set @Partnerclient_Partnergid=011;
	###partnerclient_Table###
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnerclient_Name')))into @Partnerclient_Name;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnerclient_Partnergid')))into @Partnerclient_Partnergid;

	if  @Partnerclient_Partnergid = '' or @Partnerclient_Partnergid is null  then
		set Message ='Partnerclient Partnergid Is Not Given';
		rollback;
		leave sp_Atma_Partnerclient_Set;
	end if;

	if  @Partnerclient_Name = '' or @Partnerclient_Name is null  then
		set Message ='Partnerclient Name Is Not Given';
		rollback;
		leave sp_Atma_Partnerclient_Set;
	end if;
	set Query_Insert='';

	set Query_Insert=concat('insert into atma_tmp_mst_tpartnerclient(partnerclient_partnergid,partnerclient_name,partnerclient_addressgid,
		entity_gid,create_by)
		values(',@Partnerclient_Partnergid,',''',@Partnerclient_Name,''',',@Address_Gid,',
		',@Entity_Gid,',',@Create_By,')'
	);

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
        leave sp_Atma_Partnerclient_Set;
	end if;

end if;

if ls_Action='UPDATE' then

	START TRANSACTION;
    select JSON_LENGTH(lj_filter,'$') into @li_filter_jsoncount;
	select JSON_LENGTH(lj_classification,'$') into @li_classification_jsoncount;

	if @li_filter_jsoncount = 0 or @li_filter_jsoncount is null  then
		set Message = 'No Data In Json. ';
		leave sp_Atma_Partnerclient_Set;
	End if;

	if @li_classification_jsoncount = 0 or @li_classification_jsoncount = ''
		or @li_classification_jsoncount is null  then
		set Message = ' Update By In Json. ';
		leave sp_Atma_Partnerclient_Set;
	End if;

	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnerclient_Gid')))into @Partnerclient_Gid;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnerclient_Name')))into @Partnerclient_Name;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Address_1')))into @Address_1;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Address_2')))into @Address_2;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Address_3')))into @Address_3;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Address_Pincode')))into @Address_Pincode;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Address_District_gid')))into @Address_District_gid;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Address_City_gid')))into @Address_City_gid;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Address_State_gid')))into @Address_State_gid;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Update_By'))) into @Update_By;

	set Query_Update = '';
    if @Partnerclient_Gid is not null or @Partnerclient_Gid <> ''or @Partnerclient_Gid <> 0 then
			set @Partnerclient_Gid=@Partnerclient_Gid;
	end if;
	if lower(@Address_1) <>'null' and @Address_1 <> '' then
		set Query_Update = concat(Query_Update,',address_1 = ''',@Address_1,'''  ');
	else
		set Query_Update = concat(Query_Update,',address_1 = null  ');
	End if;
	select Query_Update;
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
		leave sp_Atma_Partnerclient_Set;
	End if;

	if lower(@Address_City_Gid) <> 'null' and @Address_City_Gid <> '' then
		set Query_Update = concat(Query_Update,',address_city_gid = ',@Address_City_Gid,'  ');
	else
		set Message='Address_City can not be null' ;
		leave sp_Atma_Partnerclient_Set;
	End if;

	if lower(@Address_State_Gid) <> 'null' and @Address_State_Gid <> '' then
		set Query_Update = concat(Query_Update,',address_state_gid = ',@Address_State_Gid,'  ');
	else
		set Message='Address_State can not be null' ;
		leave sp_Atma_Partnerclient_Set;
	End if;
	if @Update_By is not null or @Update_By <> '' then
		set Query_Update = concat(Query_Update,',Update_By = ',@Update_By,'  ');
	End if;

	select partnerclient_addressgid from atma_tmp_mst_tpartnerclient
                where partnerclient_gid=@Partnerclient_Gid into @client_addressgid ;

	set Query_Update = concat('Update atma_tmp_mst_taddress
					set update_date = CURRENT_TIMESTAMP ',Query_Update,'
					Where address_gid = ',@client_addressgid,'');
	set @Query_Update = Query_Update;
	PREPARE stmt FROM @Query_Update;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;

	if countRow <= 0 then
		set Message = 'Error On Update.';
		rollback;
		leave sp_Atma_Partnerclient_Set;
	elseif    countRow > 0 then
		set Message = 'SUCCESSFULLY UPDATED';
	end if;

	set Query_Update = '';

	if @Partnerclient_Name is not null or @Partnerclient_Name <> '' then
		set Query_Update = concat(Query_Update,',Partnerclient_name = ''',@Partnerclient_Name,'''  ');
	elseif @Partnerclient_Name is null or @Partnerclient_Name = '' then
        set Message='Partnerclient Name can not be null' ;
		leave sp_Atma_Partnerclient_Set;
	end if;

	if @Update_By is not null or @Update_By <> '' then
		set Query_Update = concat(Query_Update,',Update_By = ',@Update_By,'  ');
	End if;
    set Query_Update = concat('Update atma_tmp_mst_tpartnerclient
					set update_date = CURRENT_TIMESTAMP ',Query_Update,'
					Where partnerclient_gid = ',@Partnerclient_Gid,' ');

	set @Query_Update = Query_Update;
	PREPARE stmt FROM @Query_Update;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
	if countRow <= 0 then
		set Message = 'Error On Update.';
		rollback;
		leave sp_Atma_Partnerclient_Set;
	elseif countRow > 0 then
		set Message = 'SUCCESSFULLY UPDATED';
		commit;
	end if;
end if;

END