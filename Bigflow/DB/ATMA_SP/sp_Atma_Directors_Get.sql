CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Directors_Get`(in Type  varchar(16),
in lj_filter json,in lj_classification json,out Message varchar(1000))
BEGIN
Declare Query_Table varchar(1000);
Declare Query_Select varchar(5000);
Declare Query_Search varchar(5000);
Declare Query_Update varchar(5000);
Declare countRow varchar(5000);
Declare ls_count int;

if  Type ='Directors_Get' then

		select JSON_LENGTH(lj_filter,'$') into @li_json_count;
		select JSON_LENGTH(lj_classification,'$') into @li_json_lj_classification_count;

		if @li_json_lj_classification_count is not null or @li_json_lj_classification_count <> ''
			 or @li_json_lj_classification_count <> 0 then
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Entity_Gid'))) into @entity_gid;
		end if;
        select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Mst_Table')))into @Mst_Table;


        if @li_json_count is not null or @li_json_count <> '' or @li_json_count <> 0 then

		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Director_Partnergid'))) into @Director_Partnergid;

		  #select @Director_Partnergid;
		#set Query_Search = '';

       End if;
       set Query_Table='';
			if @Mst_Table='Mst' then
				set Query_Table = concat('atma_mst_tdirectors');
			else
				set Query_Table = concat('atma_tmp_mst_tdirectors');
			End if;
set Query_Select = '';
	set Query_Select =concat('select director_name as directorName1
								from ',Query_Table,' where director_partnergid=',@Director_Partnergid,'
                                and director_isactive=''Y'' and director_isremoved=''N'' and
                                entity_gid = ',@entity_gid,'');


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