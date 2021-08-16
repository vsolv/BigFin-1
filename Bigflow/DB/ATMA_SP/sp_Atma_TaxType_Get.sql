CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_TaxType_Get`(in Action  varchar(16),
in lj_filter json,in lj_classification json,out Message varchar(1000))
BEGIN

#Balamaniraja      06-07-19

Declare Query_Select varchar(5000);
Declare Query_Search varchar(5000);
Declare countRow varchar(5000);
Declare ls_count int;

if Action = 'TaxType_Get' then

set Query_Select = '';
	set Query_Select =concat('select concat(tax.tax_gid,'' - '',subtax.subtax_gid) tax_type_gid ,
							  concat(tax.tax_name,'' - '',subtax.subtax_name) tax_type
							  from gal_mst_ttax tax inner join gal_mst_tsubtax subtax
							  on tax.tax_gid=subtax.subtax_tax_gid
							  where tax.tax_isactive = ''Y'' and tax.tax_isremoved = ''N'' and
							  subtax.subtax_isactive = ''Y'' and subtax.subtax_isremoved = ''N''
							  and tax.entity_gid = 1 and subtax.entity_gid = 1
							  Order by tax.tax_name asc;
                               ');

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

End if;


END