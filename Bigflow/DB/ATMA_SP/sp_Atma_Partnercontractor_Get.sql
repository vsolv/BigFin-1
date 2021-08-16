CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Partnercontractor_Get`(in Action  varchar(70),
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_Atma_Partnercontractor_Get:BEGIN
Declare Query_Select varchar(5000);
Declare Query_Search varchar(5000);
Declare Query_Update varchar(5000);
Declare Query_Column varchar(1000);
Declare Query_Table varchar(100);
Declare countRow varchar(5000);
Declare ls_count int;

if Action='Partnercontractor_Get' then

		select JSON_LENGTH(lj_filter,'$') into @li_json_count;
		select JSON_LENGTH(lj_classification,'$') into @li_json_lj_classification_count;



        if @li_json_lj_classification_count = 0 or @li_json_lj_classification_count is null  then
			set Message = 'No Entity_Gid In Json. ';
			leave sp_Atma_Partnercontractor_Get;
		End if;


		select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Entity_Gid'))) into @entity_gid;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Mst_Table')))into @Mst_Table;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.main_PartnerContractor_Gid')))into @main_PartnerContractor_Gid;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnercontractor_Partnergid')))into @Partnercontractor_Partnergid;

                    set Query_Table='';
			if @Mst_Table='Mst' then
				set Query_Table = concat('atma_mst_tpartnercontractor');
			else
				set Query_Table = concat('atma_tmp_mst_tpartnercontractor');
			End if;

             set Query_Column='';
            if @Mst_Table is null or @Mst_Table=''   then
				set Query_Column = concat(',main_partnercontractor_gid');
			End if;

            set Query_Search='';
            #if @Mst_Table is null or @Mst_Table=''   then
				#set Query_Search = concat('and Partnercontractor_Partnergid=',@Partnercontractor_Partnergid,'');
			#End if;

            if @Mst_Table='Mst'   then
				set Query_Search = concat('and partnercontractor_gid=',@main_PartnerContractor_Gid,'');
			End if;



set Query_Select = '';
	set Query_Select =concat('select partnercontractor_gid,partnercontractor_partnergid,partnercontractor_code,
							  partnercontractor_name,partnercontractor_service,
							  partnercontractor_remarks ',Query_Column,'
                              from ',Query_Table,'
                              where partnercontractor_isactive=''Y''
                              and partnercontractor_isremoved =''N'' and partnercontractor_partnergid=',@Partnercontractor_Partnergid,'
                              and entity_gid=',@entity_gid,'

                            ');


	 set @p = Query_Select;
	#select @p;
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