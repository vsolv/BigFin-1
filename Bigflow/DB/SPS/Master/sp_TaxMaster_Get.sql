CREATE DEFINER=`developer`@`%` PROCEDURE `galley`.`sp_TaxMaster_Get`(IN `ls_Type` varchar(64),IN `ls_Sub_Type` varchar(64),
IN `lj_Filters` json,IN `lj_Classification` json, OUT `Message` varchar(1024))
sp_TaxMaster_Get:BEGIN
	#### Ramesh Jan 28 2020
	Declare Query_Select varchar(6144);
    Declare Query_Search varchar(1024);
    declare errno int;
    declare msg varchar(1000);
    declare li_count int;

# Null Selected Output
DECLARE done INT DEFAULT 0;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
#....

	DECLARE EXIT HANDLER FOR SQLEXCEPTION,sqlwarning

    BEGIN
		GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
		set Message = concat(errno , msg);
		ROLLBACK;
    END;

	   select fn_Classification('ENTITY_ONLY',lj_Classification) into @OutMsg_Classification ;
        select  JSON_UNQUOTE(JSON_EXTRACT(@OutMsg_Classification, '$.Entity_Gid[0]')) into @Entity_Gids;
        if @Entity_Gids is  null or @Entity_Gids = '' then
				select  JSON_UNQUOTE(JSON_EXTRACT(@OutMsg_Classification, '$.Message')) into @Message;
				set Message = concat('Error On Classification Data - ',@Message);
                leave sp_TaxMaster_Get;
        End if;

if ls_Type = 'TAX' and ls_Sub_Type = 'SUMMARY' THEN

      set Query_Select = '';
      set Query_Select = concat(' Select a.tax_gid,a.tax_name,b.subtax_gid,b.subtax_name,
			c.taxrate_name,c.taxrate_rate
			from gal_mst_ttax as a
			left join gal_mst_tsubtax as b on b.subtax_tax_gid = a.tax_gid
			 and b.subtax_isactive = ''Y'' and b.subtax_isremoved = ''N''
			left join gal_mst_ttaxrate as c on c.taxrate_subtax_gid = b.subtax_gid
			 and c.taxrate_isactive = ''Y'' and c.taxrate_isremoved = ''N''
			where a.tax_isactive = ''Y'' and a.tax_isremoved = ''N'' ');


		    					set @Query_Select = Query_Select;
	      				     #	select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;



End if;



END