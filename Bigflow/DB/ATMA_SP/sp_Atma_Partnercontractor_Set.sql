CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Partnercontractor_Set`(in ls_Action varchar(16),
in lj_filter json,in lj_classification json,
out Message varchar(1000))
sp_Atma_Partnercontractor_Set:BEGIN
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
		leave sp_Atma_Partnercontractor_Set;
	End if;
	if @li_classification_jsoncount = 0 or @li_classification_jsoncount = ''
		or @li_classification_jsoncount is null  then
		set Message = 'No Entity_Gid and Create by In Json. ';
		leave sp_Atma_Partnercontractor_Set;
	End if;
	if @li_classification_jsoncount is not null or @li_classification_jsoncount	<> ''  or @li_classification_jsoncount	<> 0 then
		select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Entity_Gid')))into @Entity_Gid;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Create_By')))into @Create_By;
	End if;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnercontractor_Partnergid')))into @Partnercontractor_Partnergid;
	#select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnercontractor_Code')))into @Partnercontractor_Code;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnercontractor_Name')))into @Partnercontractor_Name;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnercontractor_Service')))into @Partnercontractor_Service;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnercontractor_Remarks')))into @Partnercontractor_Remarks;

	if @Entity_Gid = 0 or @Entity_Gid = '' or @Entity_Gid is null then
		set Message ='Entity Gid Is Not Given';
		rollback;
		leave sp_Atma_Partnercontractor_Set;
	end if;
    if @Create_By = 0 or @Create_By = '' or @Create_By is null  then
		set Message ='Create By Is Not Given';
		rollback;
		leave sp_Atma_Partnercontractor_Set;
	end if;
	#if @Partnercontractor_Code = 0 or @Partnercontractor_Code = '' or @Partnercontractor_Code is null then
	#	set Message =' Partnercontractor Code Is Not Given';
		#rollback;
		#leave sp_Atma_Partnercontractor_Set;
	#end if;
	if  @Partnercontractor_Name = '' or @Partnercontractor_Name is null  then
		set Message =' Partnercontractor Name Code Is Not Given';
		rollback;
		leave sp_Atma_Partnercontractor_Set;
	end if;

	if  @Partnercontractor_Service = '' or @Partnercontractor_Service is null  then
		set Message =' Partnercontractor Service  Code Is Not Given';
		rollback;
		leave sp_Atma_Partnercontractor_Set;
	end if;

	if  @Partnercontractor_Remarks = ''  or @Partnercontractor_Remarks is null then
		set Message =' Partnercontractor Remarks  Code Is Not Given';
		rollback;
		leave sp_Atma_Partnercontractor_Set;
	end if;

    select codesequence_no from gal_mst_tcodesequence where
			codesequence_type='partnercontractor_code' into @AT_partnercontractcode;

			set @contractcode = concat('00',SUBSTRING(CONCAT('000',@AT_partnercontractcode),-4));

    set Query_Insert='';
	set Query_Insert=concat('insert into atma_tmp_mst_tpartnercontractor(Partnercontractor_Partnergid,partnercontractor_code,
			partnercontractor_name,partnercontractor_service,partnercontractor_remarks
			,entity_gid,create_by)
			values(',@Partnercontractor_Partnergid,',',@contractcode,',''',@Partnercontractor_Name,''',''',@Partnercontractor_Service,''',''',@Partnercontractor_Remarks,''',
			',@Entity_Gid,',',@Create_By,')'
		);
	#select Query_Insert;
	set @Insert_query = Query_Insert;
	PREPARE stmt FROM @Insert_query;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
	if countRow >  0 then
		set Message = 'SUCCESSFULLY INSERTED';
        Update gal_mst_tcodesequence
				set  codesequence_no= codesequence_no+1
				Where codesequence_type = 'partnercontractor_code';
		commit;
	else
		set Message = 'INSERT FAILED';
		rollback;
	end if;
end if;


if ls_Action='UPDATE' then

	START TRANSACTION;
    select JSON_LENGTH(lj_filter,'$') into @li_filter_jsoncount;
	select JSON_LENGTH(lj_classification,'$') into @li_classification_jsoncount;
	if @li_filter_jsoncount = 0 or @li_filter_jsoncount is null  then
		set Message = 'No Data In Json. ';
		leave sp_Atma_Partnercontractor_Set;
	End if;
    if @li_classification_jsoncount = 0 or @li_classification_jsoncount = ''
		or @li_classification_jsoncount is null  then
		set Message = ' Update By In Json. ';
		leave sp_Atma_Partnercontractor_Set;
	End if;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnercontractor_Gid')))into @Partnercontractor_Gid;
	#select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnercontractor_Code')))into @Partnercontractor_Code;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnercontractor_Name')))into @Partnercontractor_Name;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnercontractor_Service')))into @Partnercontractor_Service;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnercontractor_Remarks')))into @Partnercontractor_Remarks;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Update_By')))into @Update_By;

    set Query_Update = '';
    if lower(@Partnercontractor_Name) <> 'null' or @Partnercontractor_Name <> '' then
		set Query_Update = concat(Query_Update,',Partnercontractor_Name = ''',@Partnercontractor_Name,'''  ');
	else
		set Message =' Partnercontractor Name Is Not Given';
		rollback;
		leave sp_Atma_Partnercontractor_Set;
	End if;

	if lower(@Partnercontractor_Service) <> 'null' or @Partnercontractor_Service <> '' then
		set Query_Update = concat(Query_Update,',Partnercontractor_Service = ''',@Partnercontractor_Service,'''  ');
	else
		set Message =' Partnercontractor Service Is Not Given';
		rollback;
		leave sp_Atma_Partnercontractor_Set;
	End if;
    #select @Partnercontractor_Remarks;
	if lower(@Partnercontractor_Remarks) <>'null' and @Partnercontractor_Remarks <> '' then
		set Query_Update = concat(Query_Update,',Partnercontractor_Remarks = ''',@Partnercontractor_Remarks,'''  ');
        #select concat(Query_Update,',Partnercontractor_Remarks = ''',@Partnercontractor_Remarks,'''  ');
	else
		set Message =' Partnercontractor Remarks Is Not Given';
		rollback;
		leave sp_Atma_Partnercontractor_Set;
	End if;
	if @Update_By is not null or @Update_By <> '' then
		set Query_Update = concat(Query_Update,',Update_By = ',@Update_By,'  ');
	End if;
	set Query_Update = concat('Update atma_tmp_mst_tpartnercontractor
											set update_date = CURRENT_TIMESTAMP ',Query_Update,'
											Where partnercontractor_gid = ',@Partnercontractor_Gid,'');
	set @Query_Update = Query_Update;
	PREPARE stmt FROM @Query_Update;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
	if countRow <= 0 then
		set Message = 'Error On Update.';
		rollback;
		leave sp_Atma_Partnercontractor_Set;
	elseif countRow > 0 then
		set Message = 'SUCCESSFULLY UPDATED';
		commit;
	end if;
end if;
END