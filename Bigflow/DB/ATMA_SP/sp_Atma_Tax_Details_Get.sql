CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Tax_Details_Get`(in Action  varchar(16),
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_Atma_Tax_Details_Get:BEGIN

#Balamaniraja      06-07-19

Declare Query_Select varchar(5000);
Declare Query_Search varchar(5000);
Declare Query_Column varchar(50);
Declare Query_Column1 varchar(50);
Declare Query_Table,PartnerBranch_Table varchar(50);
Declare Query_Table1 varchar(50);
Declare Query_Table2 varchar(50);
Declare countRow varchar(5000);
Declare ls_count int;

if Action='Tax_Details_Get' then


		select JSON_LENGTH(lj_classification,'$') into @li_classification_json_count;
		select JSON_LENGTH(lj_filter,'$') into @li_json_count;


        if @li_classification_json_count = 0 or @li_classification_json_count = ''
           or @li_classification_json_count is null  then
			set Message = 'No Data In classification Json. ';
			leave sp_Atma_Tax_Details_Get;
		End if;

        if @li_json_count = 0 or @li_json_count = '' or @li_json_count is null  then
			set Message = 'No Data In filter Json. ';
			leave sp_Atma_Tax_Details_Get;
		End if;


			select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Mst_Table')))into @Mst_Table;
			select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.TaxDetails_Partner_gid')))into @TaxDetails_Partner_gid;
			select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Entity_Gid'))) into @Entity_Gid;
			select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.TaxDetails_TaxNo'))) into @TaxDetails_TaxNo;
			select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Tax_Gid'))) into @Tax_Gid;

				select SUBSTRING_INDEX(@Tax_Gid,' - ',1)
				into @split_tax_gid;

				select SUBSTRING_INDEX(@Tax_Gid,' - ',-1)
				into @split_subtax_gid;

            set Query_Table='';
			if @Mst_Table='Mst' then
				set Query_Table = concat('gal_mst_ttaxdetails');
                set PartnerBranch_Table='atma_mst_tpartnerbranch';
			else
				set Query_Table = concat('atma_tmp_mst_ttaxdetails');
                set PartnerBranch_Table='atma_tmp_mst_tpartnerbranch';
			End if;

            if @Mst_Table='Mst' then
				set Query_Table1 = concat('gal_mst_ttaxsubdetails');
			else
				set Query_Table1 = concat('atma_tmp_mst_ttaxsubdetails');
			End if;

             set Query_Column='';
            if @Mst_Table is null or @Mst_Table=''   then
				set Query_Column = concat(',taxdetails.main_taxdetails_gid');
			End if;

            set Query_Column1='';
            if @Mst_Table is null or @Mst_Table=''   then
				set Query_Column1 = concat(',taxsubdetails.main_taxsubdetails_gid');
			End if;


        set Query_Search = '';


        if @split_tax_gid is not null or @split_tax_gid <> ''
           or @split_tax_gid <> 0 then
			set Query_Search = concat(Query_Search,' and tax.tax_gid = ',@split_tax_gid,' ');
		End if;

        if @split_subtax_gid is not null or @split_subtax_gid <> ''
           or @split_subtax_gid <> 0 then
			set Query_Search = concat(Query_Search,' and subtax.subtax_gid = ',@split_subtax_gid,' ');
		End if;

        if @TaxDetails_TaxNo is not null or @TaxDetails_TaxNo <> '' then

			set Query_Search = concat(Query_Search,' and taxdetails.TaxDetails_TaxNo = ''',@TaxDetails_TaxNo,''' ');
		End if;

			set Query_Select = '';
			set Query_Select =concat('select
            taxdetails.taxdetails_reftablecode,taxdetails.taxdetails_subtax_gid,
			taxdetails.taxdetails_tax_gid,taxdetails.taxdetails_taxno,
			IF( taxdetails.taxdetails_ismsme="Y", "YES", "NO") taxdetails_ismsme,
			concat(tax.tax_name, '' - '' ,subtax.subtax_name) tax_type,
			IF(taxsubdetails.taxsubdetails_isexcempted="Y", "YES", "NO") taxsubdetails_isexcempted,
			taxdetails.taxdetails_gid,taxsubdetails.taxsubdetails_taxdetails_gid,
			taxsubdetails.taxsubdetails_gid,taxsubdetails.taxsubdetails_excemfrom,
			taxsubdetails.taxsubdetails_excemto,taxsubdetails.taxsubdetails_excemthrosold,
			taxsubdetails.taxsubdetails_excemrate,taxsubdetails.taxsubdetails_taxrate,
            PB.partnerbranch_name,
			taxsubdetails.taxsubdetails_taxrate_gid,tfile.file_name,
            concat(''/media/'',substring_index(tfile.file_path,''/media/'',-1)) as file_path
            ',Query_Column,'',Query_Column1,'
			from ',Query_Table,' taxdetails
            inner join ',PartnerBranch_Table,' PB on taxdetails.taxdetails_reftablecode=PB.partnerbranch_code
            and PB.partnerbranch_partnergid=',@TaxDetails_Partner_gid,'
            and taxdetails.taxdetails_isactive = "Y" and   taxdetails.taxdetails_isremoved=''N''
            and PB.partnerbranch_isactive = "Y" and   PB.partnerbranch_isremoved=''N''
			inner join gal_mst_ttax tax on taxdetails.taxdetails_tax_gid=tax.tax_gid
			and tax.tax_isremoved=''N''  and tax.tax_isactive =''Y''  and tax.entity_gid=',@Entity_Gid,'
			inner join gal_mst_tsubtax subtax on taxdetails.taxdetails_subtax_gid=subtax.subtax_gid
			and subtax.subtax_isactive = ''Y'' and subtax.subtax_isremoved=''N'' and subtax.entity_gid=',@Entity_Gid,'
			left join ',Query_Table1,' taxsubdetails on taxdetails.taxdetails_gid=taxsubdetails.taxsubdetails_taxdetails_gid
			and taxsubdetails.taxsubdetails_isactive=''Y'' and taxsubdetails.taxsubdetails_isremoved=''N''
			and taxsubdetails.entity_gid=',@Entity_Gid,'
			left join gal_mst_tfile tfile on tfile .file_gid=taxsubdetails.taxsubdetails_attachment_gid
			and tfile.file_isactive=''Y'' and tfile.file_isremoved=''N'' and tfile.entity_gid=',@Entity_Gid,'
			where taxdetails.entity_gid=',@Entity_Gid,Query_Search,' order by taxdetails.taxdetails_gid ');


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

END IF;
END