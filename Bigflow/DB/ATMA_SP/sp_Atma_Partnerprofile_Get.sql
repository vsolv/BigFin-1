CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Partnerprofile_Get`(in Action  varchar(70),
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_Atma_Partnercontractor_Get:BEGIN
Declare Query_Select varchar(5000);
Declare Query_Search varchar(5000);
Declare Query_Update varchar(5000);
Declare Query_Table varchar(5000);
Declare Query_Column varchar(5000);
Declare countRow varchar(5000);
Declare ls_count int;

if Action='Partnerprofile_Get' then

		select JSON_LENGTH(lj_filter,'$') into @li_json_count;
		select JSON_LENGTH(lj_classification,'$') into @li_json_lj_classification_count;



        if @li_json_lj_classification_count = 0 or @li_json_lj_classification_count is null  then
			set Message = 'No Entity_Gid In Json. ';
			leave sp_Atma_Partnercontractor_Get;
		End if;


		select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Entity_Gid'))) into @entity_gid;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Mst_Table'))) into @Mst_Table;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partnerprofile_Partnergid'))) into @Partnerprofile_Partnergid;



				if @Mst_Table='Mst' then
					set Query_Table = concat('atma_mst_tpartnerprofile');
				else
					set Query_Table = concat('atma_tmp_mst_tpartnerprofile');
				End if;

            set Query_Column='';
            if @Mst_Table is null or @Mst_Table=''   then
				set Query_Column = concat(',main_partnerprofile_gid');
			End if;

	set Query_Select = '';
	set Query_Select =concat('select partnerprofile_gid, partnerprofile_partnergid,
								 partnerprofile_noofyears, partnerprofile_associateyears, partnerprofile_awarddetails,
   								 partnerprofile_noofempper, partnerprofile_noofemptmp, partnerprofile_totemp,
                                 partnerprofile_branchcount, partnerprofile_factorycount, partnerprofile_remarks,
                                 partnerprofile_isactive, partnerprofile_isremoved, entity_gid,
                                 create_by, create_date, update_by, update_date ',Query_Column,'
                                 from ',Query_Table,'
                                 where	partnerprofile_isactive=''Y'' and partnerprofile_isremoved=''N'' and
                                entity_gid =',@entity_gid,' and partnerprofile_partnergid=',@Partnerprofile_Partnergid,'
                            ');

                    #select  Query_Select;
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