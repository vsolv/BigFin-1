CREATE DEFINER=`developer`@`%` PROCEDURE `galley`.`sp_City_Set`(IN `Action` varchar(16),IN `lj_City` json,
IN `li_entity_gid` int,IN `ls_create_by` int, OUT `Message` varchar(1000))
sp_City_Set:BEGIN

#Vigneshwari       2018-09-04

declare city_srch Text;
declare pincode_srch Text;
declare ls_error varchar(100);
declare countRow int;
declare errno int;
declare msg varchar(1000);
declare Query_Update text;

	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
    set Message = concat(errno , msg);
    ROLLBACK;
    END;

set ls_error = '';

if Action = 'Insert' then

    select JSON_UNQUOTE(JSON_EXTRACT(lj_City, CONCAT('$.city_gid'))) into @city_gid;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_City, CONCAT('$.city_name'))) into @city_name;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_City, CONCAT('$.state_gid'))) into @state_gid;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_City, CONCAT('$.district_gid'))) into @district_gid;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_City, CONCAT('$.pincode_gid'))) into @pincode_gid;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_City, CONCAT('$.pincode_no'))) into @pincode_no;

    select max(City_code) into @citycode from gal_mst_tcity ;

    call sp_Generatecode_Get('WITHOUT_DATE', 'CY', '0000', @citycode, @Message);
	select @Message into @city_code;

    if @city_name = '' then
		set Message = 'City Name Not Given';
        leave sp_City_Set;
    end if;

	select exists(select City_Name,pincode_no from gal_mst_tcity C
					inner join gal_mst_tpincode PC on PC.pincode_City_gid=C.city_gid
						where C.City_Name=@city_name and PC.pincode_no=@pincode_no and PC.pincode_isremoved='N'
							and C.city_isremoved='N')  as Test INTO @CITY_NAME_TEST;

    if @CITY_NAME_TEST = 1  then
		set Message = 'Same City Name and pincode_no Is Already Exist';
		leave sp_City_Set;
	end if;

    if @state_gid = 0 then
		set Message = 'State gid Not Given';
        leave sp_City_Set;
    end if;

    if @district_gid = 0 then
		set Message = 'District gid Not Given';
        leave sp_City_Set;
    end if;

    if @pincode_no = 0 then
		set Message = 'Pincode Number Not Given';
        leave sp_City_Set;
    end if;
    #select @city_code,@pincode_no,@district_gid,@state_gid,@city_name;
	if ls_error = '' then

		start transaction;

		set city_srch = concat('INSERT INTO gal_mst_tcity(City_code,City_Name,city_state_gid,
									entity_gid, create_by) VALUES
                                    (''',@city_code,''',''' ,@city_name, ''',',@state_gid,','
                                    ,li_entity_gid, ',',ls_create_by, ')');

		set @city_srch = city_srch;
        #SELECT @city_srch;
		PREPARE stmt FROM @city_srch;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;

		if countRow >  0 then
			select LAST_INSERT_ID() into @city_gid ;

				set pincode_srch = concat('INSERT INTO gal_mst_tpincode(pincode_district_gid,pincode_City_gid,pincode_no,
									entity_gid, create_by) VALUES
                                    (',@district_gid,',' ,@city_gid, ',',@pincode_no,','
                                    ,li_entity_gid, ',',ls_create_by, ')');

                set @pincode_srch = pincode_srch;
				#SELECT @pincode_srch;
				PREPARE stmt FROM @pincode_srch;
				EXECUTE stmt;
				set countRow = (select ROW_COUNT());
				DEALLOCATE PREPARE stmt;

                if countRow >  0 then
					select LAST_INSERT_ID() into Message ;
					set Message = CONCAT(Message,',SUCCESS');
					commit;
				else
					set Message = 'Fail in pincode';
                    rollback;
				end if;
		else
			set Message = 'FAIL';
			rollback;
		end if;
	else
		set Message = ls_error;
	end if;
end if;

if Action = 'Update' then

	select JSON_UNQUOTE(JSON_EXTRACT(lj_City, CONCAT('$.city_gid'))) into @city_gid;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_City, CONCAT('$.city_name'))) into @city_name;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_City, CONCAT('$.state_gid'))) into @state_gid;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_City, CONCAT('$.district_gid'))) into @district_gid;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_City, CONCAT('$.pincode_gid'))) into @pincode_gid;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_City, CONCAT('$.pincode_no'))) into @pincode_no;

    if @city_gid = 0 then
		set ls_error = 'Contact Gid Not Given';
        leave sp_City_Set;
	end if;

	if ls_error = '' then

		start transaction;

		set  Query_Update = Concat('update gal_mst_tcity set  update_by = ',ls_create_by,',update_date = now()');

			if @city_name <> '' then
				set Query_Update = Concat(Query_Update, ',City_Name = ''', @city_name ,'''');
            end if;

			if @state_gid <> '' then
				set Query_Update = Concat(Query_Update, ',city_state_gid = ', @state_gid ,'');
            end if;
		set Query_Update = Concat(Query_Update, ' where city_gid = ''', @city_gid ,'''');

        set @Query_Update = Query_Update;
        PREPARE stmt FROM @Query_Update;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;

		if countRow > 0 then
			set Message = 'SUCCESS';

            set  Query_Update = Concat('update gal_mst_tpincode set  update_by = ',ls_create_by,',update_date = now()');

			if @city_name <> '' then
				set Query_Update = Concat(Query_Update, ',pincode_district_gid = ''', @district_gid ,'''');
            end if;

			if @state_gid <> '' then
				set Query_Update = Concat(Query_Update, ',pincode_City_gid = ', @city_gid ,'');
            end if;

            if @state_gid <> '' then
				set Query_Update = Concat(Query_Update, ',pincode_no = ', @pincode_no ,'');
            end if;

			set Query_Update = Concat(Query_Update, ' where pincode_gid = ''', @pincode_gid ,'''');

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
		else
			set Message = 'FAIL';
			rollback;
		end if;
	else
		set Message = ls_error;
	end if;

end if;
END
