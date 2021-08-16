CREATE DEFINER=`developer`@`%` PROCEDURE `galley`.`sp_State_Set`(IN `Action` varchar(16),IN `Type` varchar(16),IN `lj_filter` json,
IN `lj_classification` json,IN `ls_create_by` int, OUT `Message` varchar(1000))
sp_State_Set:BEGIN
#sakthivel
#Updated by Bala
declare ls_error varchar(100);
declare countRow int;
declare errno int;
declare msg varchar(1000);
declare Query_Update varchar(1000);

	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
    set Message = concat(errno , msg);
    ROLLBACK;
    END;

set ls_error = '';

if Action = 'Insert' and Type='State_Insert' then

	select JSON_LENGTH(lj_filter,'$') into @li_json_count;
	select JSON_LENGTH(lj_classification,'$') into @li_json_lj_classification_count;

    if @li_json_count = 0 or @li_json_count = '' or @li_json_count is null  then
		   set Message = 'No Filter Data Json ';
		leave sp_State_Set;
	end if;

    if @li_json_lj_classification_count = 0 or @li_json_lj_classification_count = ''
		or @li_json_lj_classification_count is null  then
		   set Message = 'No Classification Data In Json. ';
		leave sp_State_Set;
	end if;

    select JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Entity_gid'))) into @Entity_gid;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.State_name'))) into @State_name;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.State_country_gid'))) into @State_country_gid;


	if @State_country_gid = 0 or @State_country_gid = '' or @State_country_gid is null  then
		   set Message = 'State Country Gid Is Not Given';
		leave sp_State_Set;
	end if;

    if @State_name = '' or @State_name is null  then
		   set Message = 'State Name Is Not Given';
		leave sp_State_Set;
	end if;

    if @Entity_gid =0 or @Entity_gid = '' or @Entity_gid is null  then
		   set Message = 'Entity Gid is Not Givern';
		leave sp_State_Set;
	end if;

	select exists(select state_name from gal_mst_tstate
			where state_name=@State_name and state_isremoved='N') as Test INTO @STATE_NAME_TEST;

    if @STATE_NAME_TEST = 1  then
		   set Message = 'This State Name Is Already Exist';
		leave sp_State_Set;
	end if;

    select max(state_code) into @Statecode from gal_mst_tstate ;
    call sp_Generatecode_Get('WITHOUT_DATE', 'SN', '0000', @Statecode, @Message);
	select @Message into @state_code;

	start transaction;


		set Query_Update = concat('INSERT INTO gal_mst_tstate( state_code,state_name,state_country_gid,
								entity_gid,create_by) VALUES
                                    (''',@State_code,''',''' ,@State_name, ''',',@State_country_gid,','
                                    ,@Entity_gid, ',',ls_create_by, ')');

			set @Query_Update = Query_Update;
			PREPARE stmt FROM @Query_Update;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;

			if countRow > 0 then
				set Message = 'SUCCESS';
				commit;
			else
				set Message = 'FAIL';
				rollback;
			end if;


end if;
if Action = 'Insert' and Type='District_Insert' then

	select JSON_LENGTH(lj_filter,'$') into @li_json_count;
	select JSON_LENGTH(lj_classification,'$') into @li_json_lj_classification_count;

    if @li_json_count = 0 or @li_json_count = ''
		or @li_json_count is null  then
		   set Message = 'No Filter Data Json ';
		leave sp_State_Set;
	end if;

	select JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Entity_gid'))) into @Entity_gid;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.district_state_gid'))) into @district_state_gid;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.district_name'))) into @district_name;

    if @district_state_gid = 0 or @district_state_gid = ''
		or @district_state_gid is null  then
		   set Message = 'State Gid Is Not Given';
		leave sp_State_Set;
	end if;

    if @district_name = '' or @district_name is null  then
		   set Message = 'State Name Is Not Given';
		leave sp_State_Set;
	end if;

    if @Entity_gid =0 or @Entity_gid = '' or @Entity_gid is null  then
		   set Message = 'Entity Gid is Not Givern';
		leave sp_State_Set;
	end if;

    select max(district_code) into @districtcode from gal_mst_tdistrict ;

    call sp_Generatecode_Get('WITHOUT_DATE', 'DT', '0000', @districtcode, @Message);
	select @Message into @district_code;


		start transaction;

		set Query_Update = concat('INSERT INTO gal_mst_tdistrict( district_code,district_name,district_state_gid,
								entity_gid,create_by) VALUES
                                    (''',@district_code,''',''' ,@district_name, ''',',@district_state_gid,','
                                    ,@Entity_gid, ',',ls_create_by, ')');


               # select  Query_Update;
			set @Query_Update = Query_Update;
			PREPARE stmt FROM @Query_Update;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;

			if countRow > 0 then
				set Message = 'SUCCESS';
				commit;
			else
				set Message = 'FAIL';
				rollback;
			end if;

end if;

END