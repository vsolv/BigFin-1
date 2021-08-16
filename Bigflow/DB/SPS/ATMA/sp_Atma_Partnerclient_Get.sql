CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Partnerclient_Get`(in Action  varchar(50),
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_Atma_Activitydetails_Get:BEGIN
Declare Query_Select varchar(5000);
Declare Query_Search varchar(5000);
Declare Query_Update varchar(5000);
Declare Query_Column varchar(1000);
Declare Query_Table varchar(1000);
Declare Query_Table1 varchar(1000);
Declare countRow varchar(5000);
Declare ls_count int;

if Action='Partnerclient_Get' then

		select JSON_LENGTH(lj_filter,'$') into @li_json_count;
		select JSON_LENGTH(lj_classification,'$') into @li_json_lj_classification_count;



        if @li_json_lj_classification_count = 0 or @li_json_lj_classification_count is null  then
			set Message = 'No Entity_Gid In Json. ';
			leave sp_Atma_Activitydetails_Get;
		End if;

		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.main_PartnerClient_Gid')))into @main_PartnerClient_Gid;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Mst_Table')))into @Mst_Table;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partnerclient_Name'))) into @Partnerclient_Name;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partnerclient_Partnergid'))) into @Partnerclient_Partnergid;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Entity_Gid'))) into @entity_gid;

        set Query_Table='';
			if @Mst_Table='Mst' then
				set Query_Table = concat('atma_mst_tpartnerclient');
			else
				set Query_Table = concat('atma_tmp_mst_tpartnerclient');
			End if;

		set Query_Table1='';
			if @Mst_Table='Mst' then
				set Query_Table1 = concat('gal_mst_taddress');
			else
				set Query_Table1 = concat('atma_tmp_mst_taddress');
			End if;

            set Query_Column='';
            if @Mst_Table is null or @Mst_Table=''   then
				set Query_Column = concat(',pc.main_partnerclient_gid');
			End if;


        set Query_Search = '';

         if @Partnerclient_Name is not null or @Partnerclient_Name <> ''  then
			set Query_Search = concat(Query_Search,' and pc.partnerclient_name = ''',@Partnerclient_Name,'''  ');
		End if;

        if @Partnerclient_Partnergid is not null or @Partnerclient_Partnergid <> ''  then
			set Query_Search = concat(Query_Search,' and pc.partnerclient_partnergid=',@Partnerclient_Partnergid,'  ');
		End if;

        if @main_PartnerClient_Gid is not null or @main_PartnerClient_Gid <> ''  then
			set Query_Search = concat(Query_Search,' and pc.partnerclient_gid=',@main_PartnerClient_Gid,'  ');
		End if;


set Query_Select = '';
	set Query_Select =concat('select pc.partnerclient_partnergid,pc.partnerclient_name,pc.partnerclient_gid,a.address_1,
							a.address_2,a.address_3,a.address_pincode,
							a.address_district_gid,a.address_city_gid,a.address_state_gid,
                            s.state_name,d.district_name,c.City_Name ',Query_Column,'
                            from ',Query_Table,' pc
                            inner join ',Query_Table1,' a on pc.partnerclient_addressgid=a.address_gid
							left join gal_mst_tstate s on a.address_state_gid=s.state_gid and  s.state_isremoved=''N''
                            and s.entity_gid=',@entity_gid,'
                            left join gal_mst_tdistrict d on a.address_district_gid=d.district_gid
							left join gal_mst_tcity c on a.address_city_gid=c.city_gid and c.city_isremoved =''N''
                            and c.entity_gid=',@entity_gid,'
                            where pc.partnerclient_isactive=''Y'' and pc.partnerclient_isremoved=''N''
							and d.district_isremoved=''N''
                            and pc.entity_gid=',@entity_gid,' and a.entity_gid=',@entity_gid,'
							and d.entity_gid=',@entity_gid,'

                            ',Query_Search,'');


	 set @p = Query_Select;
	#select Query_Select;  ## Remove It
     PREPARE stmt FROM @p;
	 EXECUTE stmt;
	 Select found_rows() into ls_count;
	 DEALLOCATE PREPARE stmt;

	 if ls_count > 0 then
		 set Message = 'FOUND';
	else
		 set Message = 'NOT_FOUND';
	end if;
end if;
END