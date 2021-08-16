CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Document_Get`(in Action  varchar(16),
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_Atma_Document_Get:BEGIN

#Balamaniraja      05-07-19

Declare Query_Select varchar(5000);
Declare Query_Search varchar(5000);
Declare Query_Table varchar(5000);
Declare Query_Column varchar(5000);
Declare countRow varchar(5000);
Declare ls_count int;


if Action='Document_Get' then

	select JSON_LENGTH(lj_filter,'$') into @li_filter_jsoncount;
    select JSON_LENGTH(lj_classification,'$') into @li_classification_jsoncount;


         if @li_classification_jsoncount = 0 or @li_classification_jsoncount is null  then
			set Message = 'No Data In classification Json. ';
			leave sp_Atma_Document_Get;
		End if;

		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Mst_Table')))into @Mst_Table;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Docgroup_Gid'))) into @Docgroup_Gid;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Document_Gid'))) into @Document_Gid;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Documents_Partnergid'))) into @Documents_Partnergid;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Entity_Gid'))) into @Entity_Gid;

            set Query_Table='';
			if @Mst_Table='Mst' then
				set Query_Table = concat('atma_trn_tdocuments');
			else
				set Query_Table = concat('atma_tmp_trn_tdocuments');
			End if;


					  set Query_Column='';
				if @Mst_Table is null or @Mst_Table=''   then
					set Query_Column = concat(',dcmts.main_documents_gid');
				End if;


            if @Entity_Gid = 0 or @Entity_Gid = ''
            or @Entity_Gid is null  then
				set Message = 'Entity_Gid Is Not Given In classification Json. ';
				leave sp_Atma_Document_Get;
			End if;

            if @Documents_Partnergid = 0 or @Documents_Partnergid = ''
            or @Documents_Partnergid is null  then
				set Message = 'Documents_Partnergid Is Not Given In classification Json. ';
				leave sp_Atma_Document_Get;
			End if;


		set Query_Search = '';

		if @Docgroup_Gid is not null or @Docgroup_Gid <> '' then
			set Query_Search = concat(Query_Search,' and docgp.docgroup_gid = ''',@Docgroup_Gid,''' ');
		End if;

        if @Document_Gid is not null or @Document_Gid <> '' then
			set Query_Search = concat(Query_Search,' and docgrp.docgroup_gid = ''',@Document_Gid,''' ');
		End if;

			set Query_Select = '';
			set Query_Select =concat('select dcmts.documents_gid,docgp.docgroup_name,
							docgrp.docgroup_gid,docgrp.docgroup_name Document_Name,
                            concat(''/media/'',substring_index(file_path,''/media/'',-1)) as file_path,
							fl.file_name,dcmts.documents_remarks ',Query_Column,'
							FROM   atma_mst_tdocgroup docgp
							inner join atma_mst_tdocgroup docgrp
							on docgp.docgroup_gid=docgrp.docgroup_parentgid
                            inner join ',Query_Table,' dcmts
                            on dcmts.documents_docgroupgid=docgrp.docgroup_gid
                            left join gal_mst_tfile fl
                            on dcmts.documents_filegid=fl.file_gid
							where docgp.docgroup_isparent=''Y'' and docgrp.docgroup_isparent=''N''
							and docgp.docgroup_isactive=''Y'' and docgp.docgroup_isremoved=''N''
							and docgp.entity_gid=',@Entity_Gid,' and dcmts.docments_isactive=''Y''
                            and dcmts.documents_isremoved=''N'' and  dcmts.entity_gid=',@Entity_Gid,'
                            and fl.file_isactive=''Y''
                            and fl.file_isremoved=''N'' and fl.entity_gid=',@Entity_Gid,'
                            and documents_partnergid=',@Documents_Partnergid,'
                            ',Query_Search,'   ');


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