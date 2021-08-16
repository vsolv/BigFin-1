CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Document_Set`(in ls_Action varchar(16),
in Document json,
out Message varchar(1000))
sp_Atma_Document_Set:BEGIN
declare Query_Insert varchar(1000);
Declare countRow varchar(6000);
declare Query_Update varchar(1000);
Declare errno int;
Declare msg,Error_Level varchar(1000);

						DECLARE EXIT HANDLER FOR SQLEXCEPTION
						BEGIN
							GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
							set Message = concat(Error_Level,' : No-',errno , msg);
							ROLLBACK;
						END;

if ls_Action = 'INSERT'  then

         start transaction;

		select JSON_LENGTH(Document,'$') into @li_jsonDocument;

		if @li_jsonDocument = 0 or @li_jsonDocument is null  then
			set Message = 'No Data In Json. ';
			leave sp_Atma_Document_Set;
		End if;
			if @li_jsonDocument is not null or @li_jsonDocument <> '' then

				 select JSON_UNQUOTE(JSON_EXTRACT(Document,CONCAT('$.Documents_Partnergid')))into @DocumentsPartnergid;
				 select JSON_UNQUOTE(JSON_EXTRACT(Document,CONCAT('$.Documents_Docgroupgid')))into @DocumentsDocgroupgid;
				 #select JSON_UNQUOTE(JSON_EXTRACT(Document,CONCAT('$.Documents_Period')))into @DocumentsPeriod;
				 select JSON_UNQUOTE(JSON_EXTRACT(Document,CONCAT('$.Description')))into @Description;
				 #select JSON_UNQUOTE(JSON_EXTRACT(Document,CONCAT('$.Documents_Filegid')))into @DocumentsFilegid;
				 select JSON_UNQUOTE(JSON_EXTRACT(Document,CONCAT('$.File_Name')))into @FileName;
				 select JSON_UNQUOTE(JSON_EXTRACT(Document,CONCAT('$.File_Path')))into @FilePath;
				 select JSON_UNQUOTE(JSON_EXTRACT(Document,CONCAT('$.Entity_Gid')))into @EntityGid;
				 select JSON_UNQUOTE(JSON_EXTRACT(Document,CONCAT('$.Create_By')))into @CreateBy;


				if @DocumentsPartnergid = '' or @DocumentsPartnergid is null  or @DocumentsPartnergid =0 then
				set Message ='Documents Partnergid Is Not Given';
				rollback;
				leave sp_Atma_Document_Set;
				end if;

				if @DocumentsDocgroupgid = '' or @DocumentsDocgroupgid is null  or @DocumentsDocgroupgid =0 then
				set Message ='Documents Docgroupgid Is Not Given';
				rollback;
				leave sp_Atma_Document_Set;
				end if;

                if @Description = '' or @Description is null  then
				set Message ='Description  Is Not Given';
				rollback;
				leave sp_Atma_Document_Set;
				end if;

                if @FileName = '' or @FileName is null  then
				set Message ='FileName  Is Not Given';
				rollback;
				leave sp_Atma_Document_Set;
				end if;

                if @FilePath = '' or @FilePath is null  then
				set Message ='FilePath  Is Not Given';
				rollback;
				leave sp_Atma_Document_Set;
				end if;


				end if;



    set Query_Insert='';
    set Error_Level='ATMA23.1';
	set Query_Insert=concat('insert into gal_mst_tfile(file_name,
							file_path,entity_gid,create_by)
					values(''',@FileName,''',''',@FilePath,''',',@EntityGid,',',@CreateBy,')'
                    );

	set @Insert_query = Query_Insert;

	PREPARE stmt FROM @Insert_query;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
    if countRow >  0 then
		set Message = 'SUCCESSFULLY INSERTED';


	else
		set Message = 'INSERT FAILED';
		rollback;
	end if;


	set Query_Insert='';

    #set @DocumentsPeriod='One time';

    select LAST_INSERT_ID() into @filegid ;
  # select max(partner_gid) from   atma_tmp_tpartner into @DocumentsPartnergid;
		set @DocumentsPeriod='';
		select partner_Classification from atma_tmp_tpartner
		where partner_gid=@DocumentsPartnergid into @DocumentsPeriod ;
   set Error_Level='ATMA23.2';
	set Query_Insert=concat('insert into atma_tmp_trn_tdocuments(documents_partnergid,
							documents_docgroupgid,documents_period,
							documents_remarks,documents_filegid,entity_gid,create_by)
					values(',@DocumentsPartnergid,',',@DocumentsDocgroupgid,',''',@DocumentsPeriod,
                    ''',''',@Description,''',',@filegid,',',@EntityGid,',',@CreateBy,')'
                    );

	set @Insert_query = Query_Insert;

    #select @Insert_query;


	PREPARE stmt FROM @Insert_query;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;

    if countRow >  0 then
		set Message = 'SUCCESSFULLY INSERTED';
        commit;
	else
		set Message = 'INSERT FAILED';
		rollback;
	end if;
end if;


if ls_Action='UPDATE' then


  select JSON_LENGTH(Document,'$') into @li_jsonDocument;


			#select @li_jsonDocument;
		if @li_jsonDocument = 0 or @li_jsonDocument is null  then
			set Message = 'No Data In Json - Update.';
			leave sp_Atma_Document_Set;
		End if;

	if @li_jsonDocument is not null or @li_jsonDocument <> '' then
    #select 1;
				 select JSON_UNQUOTE(JSON_EXTRACT(Document,CONCAT('$.Documents_Gid')))into @DocumentsGid;
				 #select JSON_UNQUOTE(JSON_EXTRACT(Document,CONCAT('$.Documents_Filegid')))into @documentsfilegid;
				 #select JSON_UNQUOTE(JSON_EXTRACT(Document,CONCAT('$.Documents_Partnergid')))into @DocumentsPartnergid;
				 select JSON_UNQUOTE(JSON_EXTRACT(Document,CONCAT('$.Documents_Docgroupgid')))into @DocumentsDocgroupgid;
				 select JSON_UNQUOTE(JSON_EXTRACT(Document,CONCAT('$.Documents_Period')))into @DocumentsPeriod;
				 select JSON_UNQUOTE(JSON_EXTRACT(Document,CONCAT('$.Description')))into @DocumentsRemarks;
				 #select JSON_UNQUOTE(JSON_EXTRACT(Document,CONCAT('$.Documents_Filegid')))into @DocumentsFilegid;
				 select JSON_UNQUOTE(JSON_EXTRACT(Document,CONCAT('$.File_Name')))into @FileName;
				 select JSON_UNQUOTE(JSON_EXTRACT(Document,CONCAT('$.File_Path')))into @FilePath;
				 select JSON_UNQUOTE(JSON_EXTRACT(Document,CONCAT('$.Update_By')))into @UpdateBy;
                 #select 1;

			End if;

            if @DocumentsRemarks = '' or @DocumentsRemarks is null  then
				set Message ='Description  Is Not Given';
				rollback;
				leave sp_Atma_Document_Set;
			end if;

					set Query_Update = '';

					  if @DocumentsGid is not null or @DocumentsGid <> '' or @DocumentsGid <> 0 then
						set @DocumentsGid=@DocumentsGid;
					end if;



					if @FileName is not null or @FileName <> '' then

						set Query_Update = concat(Query_Update,',File_Name = ''',@FileName,'''  ');

					End if;



					if @FilePath is not null or @FilePath <> '' then

						set Query_Update = concat(Query_Update,',File_Path = ''',@FilePath,'''  ');

					End if;

					if @UpdateBy is not null or @Update_By <> '' then

						set Query_Update = concat(Query_Update,',Update_By = ',@UpdateBy,'  ');

					End if;
#select Query_Update;
				select documents_filegid from atma_tmp_trn_tdocuments
                where documents_gid=@DocumentsGid into @DocumentsGidfile;

                 set Error_Level='ATMA23.3';
						 set Query_Update = concat('Update gal_mst_tfile

                         set update_date = CURRENT_TIMESTAMP ',Query_Update,'

                            Where file_gid = ',@DocumentsGidfile,'

							 ');

				set @Query_Update = Query_Update;

				PREPARE stmt FROM @Query_Update;

				EXECUTE stmt;

				set countRow = (select ROW_COUNT());

				DEALLOCATE PREPARE stmt;



		if countRow <= 0 then

				set Message = 'Error On Update.';

				rollback;

				leave sp_Atma_Document_Set;

		elseif    countRow > 0 then

				set Message = 'SUCCESSFULLY UPDATED';

		end if;

set Query_Update = '';


					if @DocumentsGid is not null or @DocumentsGid <> '' or @DocumentsGid <> 0 then
						set @DocumentsGid=@DocumentsGid;
					end if;

                   #if @DocumentsPeriod is not null or @DocumentsPeriod <> '' then

						#set Query_Update = concat(Query_Update,',Documents_Period = ''',@DocumentsPeriod,'''  ');

					#End if;

					if @DocumentsDocgroupgid <>'null' and @DocumentsDocgroupgid <> '' or @DocumentsDocgroupgid <> 0 then

						set Query_Update = concat(Query_Update,',Documents_Docgroupgid = ',@DocumentsDocgroupgid,'  ');
					else
						set Message='Please Enter The Documentgroup ' ;
						leave sp_Atma_Document_Set;
					End if;



                   if @DocumentsRemarks <>'null' and @DocumentsRemarks <> '' then

						set Query_Update = concat(Query_Update,',Documents_Remarks = ''',@DocumentsRemarks,'''  ');
					else
						set Message='Please Enter The Document Remarks ' ;
						leave sp_Atma_Document_Set;

					end if;

                 set Error_Level='ATMA23.4';
					set Query_Update = concat('Update atma_tmp_trn_tdocuments

                         set update_date = CURRENT_TIMESTAMP ',Query_Update,'

                            Where documents_gid = ',@DocumentsGid,'

							');
#select Query_Update;
				set @Query_Update = Query_Update;

				PREPARE stmt FROM @Query_Update;

				EXECUTE stmt;

				set countRow = (select ROW_COUNT());

				DEALLOCATE PREPARE stmt;



		if countRow <= 0 then

				set Message = 'Error On Update.';

				rollback;

				leave sp_Atma_Document_Set;

		elseif    countRow > 0 then

				set Message = 'SUCCESSFULLY UPDATED';
				commit;
		end if;



	end if;

END