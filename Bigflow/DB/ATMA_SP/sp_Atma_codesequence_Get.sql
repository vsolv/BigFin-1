CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_codesequence_Get`(in Action  varchar(25),
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_Atma_codesequence_Get:BEGIN

Declare Query_Select varchar(5000);
Declare Query_Search varchar(5000);
Declare Query_Table varchar(5000);
Declare Query_Column varchar(5000);
Declare Query_Update varchar(5000);
Declare countRow varchar(5000);
Declare ls_count int;

	select JSON_LENGTH(lj_filter,'$') into @li_json_count;
	select JSON_LENGTH(lj_classification,'$') into @li_json_lj_classification_count;

    set @AT_partnercode='';
	select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.codesequence_type')))into @codesequence_type;

		select codesequence_no from gal_mst_tcodesequence
        where codesequence_type=@codesequence_type
        into @AT_partnercode;

   set @code_partner = concat('PA',SUBSTRING(CONCAT('0000',@AT_partnercode),-5));

   SET Message=@code_partner;
  /*
  set @code_partner = concat('PA',SUBSTRING(CONCAT('000',codesequence_no),-4));
	select @code_partner;
	set Query_Select =concat('select concat(''PA'',SUBSTRING(CONCAT(''000'',''codesequence_no''),-4))) as PARNERCODE
						 from gal_mst_tcodesequence
						where codesequence_type=''',@codesequence_type,'''
                        ');

	 set @p = @code_partner;
     PREPARE stmt FROM @p;
	 EXECUTE stmt;
	 Select found_rows() into ls_count;
	 DEALLOCATE PREPARE stmt;

	 if ls_count > 0 then
		 set Message = 'FOUND';
	else
		 set Message = 'NOT_FOUND';

end  if;
*/
END