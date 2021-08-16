CREATE  PROCEDURE `galley`.`sp_Address_Set`(IN `Action` varchar(16),IN `li_add_gid` int, iN `ls_add_refcode` VARCHAR(16),
IN `ls_address1` varchar(128), IN `ls_address2` varchar(128),IN `ls_address3` varchar(128),
IN `li_add_pincode` int ,IN `li_add_districtgid` int,IN `li_add_citygid` int,IN `li_add_stategid` int,
IN `li_entity_gid` int,IN `ls_create_by` int, OUT `Message` varchar(1000))
sp_Address_Set:BEGIN

#Vigneshwari       06-02-2018

declare Add_srch varchar(1000);
declare ls_error varchar(100);
declare countRow int;
declare errno int;
declare msg varchar(1000);
declare ls_no varchar(64);
Declare Query_Column varchar(500);
Declare Query_Value varchar(500);
declare Query_Update varchar(1000);
	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
    #SELECT errno AS MYSQL_ERROR;
    set Message = concat(errno , msg);
    #set Message = 'Error';
    ROLLBACK;
    END;

set ls_error = '';
set @ls_ref_code = '';

if Action = 'Insert' then

	if ls_add_refcode = '' then
		set ls_error = 'Ref Code Not Given ';
	else
		set @srch = concat('select case when isnull(ref_code) then 0 else ref_code end into @ls_ref_code from gal_mst_tref where ref_name = ''',ls_add_refcode,'_address''');
        #select @srch;
        PREPARE stmt FROM @srch;
		EXECUTE stmt;
		DEALLOCATE PREPARE stmt;

        set ls_add_refcode = @ls_ref_code;
        #select ls_add_refcode;
        if ls_add_refcode = '' then
			set ls_error = 'Given ref not in ref table';
		end if;
	end if;

    if ls_address1 = '' then
		set ls_error = 'Address1 Not Given';
	end if;

	if li_add_pincode = 0 then
		set ls_error = 'Pincode Not Given';
	end if;

	if li_add_districtgid = 0 then
		set ls_error = 'District Gid Not Given';
	end if;

	if li_add_citygid = 0 then
		set ls_error = 'City Gid Not Given';
	end if;

	if li_add_stategid = 0 then
		set ls_error = 'State Gid Not Given';
	end if;

    set Query_Column = '';
    set Query_Value = '';

    if ls_address2 <> '' then
		set Query_Column = concat(Query_Column, ' address_2,');
        set Query_Value = concat(Query_Value, '''',ls_address2,''',');
	else
        set Query_Column = concat(Query_Column,'');
        set Query_Value = concat(Query_Value );
    end if;

    if ls_address3 <> '' then
		set Query_Column = concat(Query_Column, ' address_3,');
        set Query_Value = concat(Query_Value, '''',ls_address3,''',');
	else
        set Query_Column = concat(Query_Column,'');
        set Query_Value = concat(Query_Value);
    end if;


	if ls_error = '' then



			set Add_srch = concat('INSERT INTO gal_mst_taddress (address_ref_code, address_1, ',Query_Column,'
									address_pincode, address_district_gid, address_city_gid, address_state_gid,
                                    entity_gid, create_by) VALUES (''',ls_add_refcode,''',''' ,ls_address1, ''','
									,Query_Value,'' ,li_add_pincode, ',' ,li_add_districtgid, ','
                                    ,li_add_citygid, ',' ,li_add_stategid, ',' ,li_entity_gid, ',' ,ls_create_by, ')');

		set @Add_srch = Add_srch;
        #SELECT @Add_srch;
		PREPARE stmt FROM @Add_srch;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;

		if countRow >  0 then
			select LAST_INSERT_ID() into Message ;
            set Message = concat(Message,',SUCCESS');
		    leave sp_Address_Set;
		else
			set Message = 'FAIL';
			#rollback;
		    leave sp_Address_Set;
		end if;
	else
		set Message = ls_error;
	end if;
end if;

if Action = 'Update' then


	if li_add_gid = 0 then
		set ls_error = 'Address Gid Not Given';
        leave sp_Address_Set;
	end if;

   /*if ls_address1 = '' and ls_address1 is null then
		set ls_error = 'Address1 Not Given';

	end if;

     if ls_address2 = '' and ls_address2 is null then
		set ls_error = 'Address2 Not Given';
	end if;

     if ls_address3 = '' and ls_address3 is null then
		set ls_error = 'Address3 Not Given';
	end if;

	if li_add_pincode = 0 then
		set ls_error = 'Pincode Not Given';
	end if;

	if li_add_districtgid = 0 then
		set ls_error = 'District Gid Not Given';
	end if;

	if li_add_citygid = 0 then
		set ls_error = 'City Gid Not Given';
	end if;

	if li_add_stategid = 0 then
		set ls_error = 'State Gid Not Given';
	end if; */

	if ls_error = '' then



        set  Query_Update = Concat('update gal_mst_taddress set  update_by = ',ls_create_by,',update_date = now()');

                 if ls_address1 = 'null' then
					set Query_Update = Concat(Query_Update, ',address_1 = null' );
                elseif ls_address1 <> '' then
					set Query_Update = Concat(Query_Update, ',address_1 = ''', ls_address1 ,'''' );
                end if;

                 if ls_address2 = 'null' then
					set Query_Update = Concat(Query_Update, ',address_2 = null' );
                    elseif ls_address2 <> '' then
					set Query_Update = Concat(Query_Update, ',address_2 = ''', ls_address2 ,'''');
                    else
                    set Query_Update = Concat(Query_Update,',address_2 = ''' ''' ');
                end if;


                if ls_address3 = 'null' then
					set Query_Update = Concat(Query_Update, ',address_3 = null' );
                    elseif ls_address3 <> '' then
					set Query_Update = Concat(Query_Update, ',address_3 = ''', ls_address3 ,'''');
                    else
                    set Query_Update = Concat(Query_Update,',address_3 = ''' ''' ');
                end if;


                if li_add_pincode = 'null' then
					set Query_Update = Concat(Query_Update, ',address_pincode = null' );
                elseif li_add_pincode <> '' then
					set Query_Update = Concat(Query_Update, ',address_pincode= ''', li_add_pincode ,'''' );
                end if;

                if li_add_districtgid = 'null' then
					set Query_Update = Concat(Query_Update, ',address_district_gid = null' );
                elseif li_add_districtgid <> '' then
					set Query_Update = Concat(Query_Update, ',address_district_gid= ''', li_add_districtgid ,'''' );
                end if;

                if li_add_citygid = 'null' then
					set Query_Update = Concat(Query_Update, ',address_city_gid = null' );
                elseif li_add_citygid <> '' then
					set Query_Update = Concat(Query_Update, ',address_city_gid= ''', li_add_citygid ,'''' );
                end if;

                 if li_add_stategid = 'null' then
					set Query_Update = Concat(Query_Update, ',address_state_gid = null' );
                elseif li_add_stategid <> '' then
					set Query_Update = Concat(Query_Update, ',address_state_gid= ''', li_add_stategid ,'''' );
                end if;

				set Query_Update = Concat(Query_Update, ' where address_gid = ''', li_add_gid ,'''');

                #select Query_Update;#.....................

                set @Query_Update = Query_Update;
        		PREPARE stmt FROM @Query_Update;
				EXECUTE stmt;
				set countRow = (select ROW_COUNT());
				DEALLOCATE PREPARE stmt;

        #select ls_address1,ls_address2,ls_address3,li_add_pincode,li_add_districtgid,li_add_citygid,li_add_stategid,ls_create_by,li_add_gid;
		/*update gal_mst_taddress set address_1 = ls_address1, address_2 = ls_address2, address_3 = ls_address3,
				address_pincode = li_add_pincode, address_district_gid = li_add_districtgid, address_city_gid = li_add_citygid,
                address_state_gid = li_add_stategid, update_by = ls_create_by , update_date = now()
                where address_gid = li_add_gid;*/




		set countRow = (select found_rows());

		if countRow > 0 then
			set Message = 'SUCCESS';

		else
			set Message = 'FAIL';
			rollback;
		end if;
	else
		set Message = ls_error;
	end if;
end if;

END