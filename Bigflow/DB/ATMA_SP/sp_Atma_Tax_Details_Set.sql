 CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Tax_Details_Set`(in Action  varchar(16),
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_Atma_Tax_Details_Set:BEGIN

declare Query_Insert varchar(1000);
Declare countRow varchar(6000);
declare Query_Update varchar(1000);
Declare t_taxdetails_gid,t_taxdetails_tax_gid,t_taxdetails_subtax_gid,t_taxdetails_ref_gid,t_taxdetails_type,
		t_taxdetails_ismsme,t_taxdetails_reftablecode,t_taxdetails_taxno,t_taxdetails_isactive,
        t_taxdetails_isremoved,t_entity_gid,t_create_by,t_create_date,t_update_by,t_Update_date,
        t_main_taxdetails_gid varchar (150);
DECLARE finished INTEGER DEFAULT 0;
Declare errno int;
Declare msg varchar(1000);

						DECLARE EXIT HANDLER FOR SQLEXCEPTION
						BEGIN
							GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
							set Message = concat(errno , msg);
							ROLLBACK;
						END;

if Action = 'TAX_INSERT'  then

	start transaction;

    select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Entity_gid'))) into @Entity_gid;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.TaxSubDetails_IsExcempted'))) into @TaxSubDetails_IsExcempted;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Tax_Gid'))) into @Tax_Gid;
	select SUBSTRING_INDEX(@Tax_Gid,' - ',1) into @TaxDetails_Tax_Gid;
	select SUBSTRING_INDEX(@Tax_Gid,' - ',-1) into @TaxDetails_Subtax_Gid;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.TaxDetails_TaxNo')))into @TaxDetails_TaxNo;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Create_By')))into @Create_By;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.TaxDetails_Partner_Code')))into @TaxDetails_Partner_Code;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.TaxDetails_Partnerbranchcode')))into @TaxDetails_Partnerbranchcode;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.TaxSubDetails_TaxRate_Gid')))into @TaxSubDetails_TaxRate_Gid;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.TaxSubDetails_TaxRate')))into @TaxSubDetails_TaxRate;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.TaxDetails_Is_MSME'))) into @TaxDetails_Is_MSME;

	if @Tax_Gid = '' or @Tax_Gid is null  or @Tax_Gid =0  then
		set Message ='Tax Gid Is Not Given';
		rollback;
		leave sp_Atma_Tax_Details_Set;
		end if;

    if @TaxSubDetails_TaxRate is null or  @TaxSubDetails_TaxRate = ''
    or @TaxSubDetails_TaxRate='undefined'  then
		set @TaxSubDetails_IsExcempted='N';
		set @TaxSubDetails_TaxRate=0;
		set @TaxSubDetails_TaxRate_Gid=0;
    end if;

    if @TaxDetails_Is_MSME='YES' then
		  set @TaxDetails_Is_MSME='Y' ;
	elseif @TaxDetails_Is_MSME='NO' then
		  set @TaxDetails_Is_MSME='N' ;
	 end if;

    if @TaxSubDetails_IsExcempted='Y' then

		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.TaxSubDetails_ExcemFrom')))into @TaxSubDetails_ExcemFrom;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.TaxSubDetails_ExcemTo')))into @TaxSubDetails_ExcemTo;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.TaxSubDetails_ExcemthroSold')))into @TaxSubDetails_ExcemthroSold;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.TaxSubDetails_ExcemRate')))into @TaxSubDetails_ExcemRate;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.FileName')))into @FileName;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.FilePath')))into @FilePath;
    	set @TaxSubDetails_ExcemFrom=date_format(@TaxSubDetails_ExcemFrom,'%Y-%m-%d');
		set @TaxSubDetails_ExcemTo=date_format(@TaxSubDetails_ExcemTo,'%Y-%m-%d');

		if convert(@TaxSubDetails_TaxRate,decimal(16,2))<convert(@TaxSubDetails_ExcemRate,decimal(16,2)) then
			set Message ='TaxRate should be greater than ExcemRate ';
			rollback;
			leave sp_Atma_Tax_Details_Set;
		end if;

		if @TaxSubDetails_ExcemFrom >= @TaxSubDetails_ExcemTo then
			set Message ='To date should be greater than From date ';
			rollback;
			leave sp_Atma_Tax_Details_Set;
		end if;

	end if;
     set @Su_Cu_group='';
    #set @TaxDetails_Ref_Gid=23;
    #set @TaxDetails_Type='C';
    select fn_REFGid('SUPPLIER_TAX') into @TaxDetails_Ref_Gid_S;
	select fn_REFGid('CUST_GST') into @TaxDetails_Ref_Gid_C;

    select partner_group from atma_tmp_tpartner
    where partner_code=@TaxDetails_Partner_Code into @Su_Cu_group;

    if @Su_Cu_group ='Customer' then
    set @TaxDetails_Type='C';
    set @TaxDetails_Ref_Gid=@TaxDetails_Ref_Gid_C;
    else
	set @TaxDetails_Type='S';
    set @TaxDetails_Ref_Gid=@TaxDetails_Ref_Gid_S;
	end if;



	set Query_Insert='';
	set Query_Insert=concat('insert into atma_tmp_mst_ttaxdetails(taxdetails_tax_gid,
			 taxdetails_subtax_gid,taxdetails_ref_gid,taxdetails_type,taxdetails_ismsme,
             taxdetails_reftablecode,taxdetails_taxno,entity_gid,create_by)
			values(',@TaxDetails_Tax_Gid,',',@TaxDetails_Subtax_Gid,',
                    ',@TaxDetails_Ref_Gid,',''',@TaxDetails_Type,''',''',@TaxDetails_Is_MSME,''',
                    ''',@TaxDetails_Partnerbranchcode,''',''',ifnull(@TaxDetails_TaxNo,''),''',
                    ',@Entity_gid,',',@Create_By,')'
                    );
   #select Query_Insert;
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

	if  @TaxSubDetails_IsExcempted='Y' then

		select LAST_INSERT_ID() into @TaxDetails_Gid ;
        set Query_Insert='';
		set Query_Insert=concat('insert into gal_mst_tfile(file_name,
							file_path,entity_gid,create_by)
					values(''',@FileName,''',''',@FilePath,''',
                    ',@Entity_gid,',',@Create_By,')'
                    );

      #select Query_Insert;
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

		select  LAST_INSERT_ID() into @Attachment_Gid ;
		set Query_Insert='';
		set Query_Insert=concat('insert into atma_tmp_mst_ttaxsubdetails(taxsubdetails_taxdetails_gid,
				taxsubdetails_subtax_gid, taxsubdetails_taxrate_gid,
				taxsubdetails_taxrate, taxsubdetails_isexcempted, taxsubdetails_excemfrom,
				taxsubdetails_excemto, taxsubdetails_excemthrosold, taxsubdetails_excemrate,
				taxsubdetails_attachment_gid,
				entity_gid, create_by)
				values(',@TaxDetails_Gid,',',@TaxDetails_Subtax_Gid,',
						',@TaxSubDetails_TaxRate_Gid,',',@TaxSubDetails_TaxRate,',
						''',@TaxSubDetails_IsExcempted,''',
                        ',if(ifnull(@TaxSubDetails_ExcemFrom,null) IS NULL,'NULL',CONCAT('''',@TaxSubDetails_ExcemFrom,'''')),',
						',if(ifnull(@TaxSubDetails_ExcemTo,null) IS NULL,'NULL',CONCAT('''',@TaxSubDetails_ExcemTo,'''')),',
                        ',@TaxSubDetails_ExcemthroSold,',
						',@TaxSubDetails_ExcemRate,',',@Attachment_Gid,',
						',@Entity_gid,',',@Create_By,')'
						);

         # select Query_Insert;
		set @Insert_query = Query_Insert;

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
    if  @TaxSubDetails_IsExcempted='N' then

		select LAST_INSERT_ID() into @TaxDetails_Gid ;
        set Query_Insert='';
		set Query_Insert=concat("insert into atma_tmp_mst_ttaxsubdetails(taxsubdetails_taxdetails_gid,
				taxsubdetails_subtax_gid, taxsubdetails_taxrate_gid,
				taxsubdetails_taxrate, taxsubdetails_isexcempted,
				entity_gid, create_by)
				values(",@TaxDetails_Gid,","
                ,@TaxDetails_Subtax_Gid,","
				,@TaxSubDetails_TaxRate_Gid,","
                ,@TaxSubDetails_TaxRate,",
				'",@TaxSubDetails_IsExcempted,"',"
				,@Entity_gid,",",@Create_By,")"
						);

		set @Insert_query = Query_Insert;

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
End if;



if Action='TAX_UPDATE' then

	START TRANSACTION;
	select JSON_LENGTH(lj_filter,'$') into @li_jsoncount;
	select JSON_LENGTH(lj_classification,'$') into @li_classification_json_count;
	if @li_jsoncount = 0 or @li_jsoncount is null or @li_jsoncount = ''  then
		set Message = 'No Data In filter Json - Update.';
		leave sp_Atma_Tax_Details_Set;
	End if;
    if @li_classification_json_count = 0  or @li_classification_json_count = ''
		or @li_classification_json_count is null  then
				set Message = 'No Data In classification Json - Update.';
				leave sp_Atma_Tax_Details_Set;
	End if;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.TaxDetails_Gid'))) into @TaxDetails_Gid;
	if @TaxDetails_Gid is null or @TaxDetails_Gid = '' or @TaxDetails_Gid = 0 then
		set Message = 'TaxDetails_Gid Is Not Given Json - Update.';
		leave sp_Atma_Tax_Details_Set;
	end if;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.TaxDetails_Partnerbranchcode')))into @TaxDetails_Partnerbranchcode;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.TaxSubDetails_IsExcempted'))) into @TaxSubDetails_IsExcempted;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Tax_Gid'))) into @Tax_Gid;
    select SUBSTRING_INDEX(@Tax_Gid,' - ',1) into @TaxDetails_Tax_Gid;
    select SUBSTRING_INDEX(@Tax_Gid,' - ',-1) into @taxdetails_subtax_gid;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.TaxDetails_Is_MSME'))) into @TaxDetails_Is_MSME;

	 if @TaxDetails_Is_MSME='YES' then
		  set @TaxDetails_Is_MSME='Y' ;
	   elseif @TaxDetails_Is_MSME='NO' then
		  set @TaxDetails_Is_MSME='N' ;
	 end if;

	if @TaxSubDetails_IsExcempted='Y' then
		set @TaxSubDetails_IsExcempted='Y' ;
	elseif @TaxSubDetails_IsExcempted='N' then
		set @TaxSubDetails_IsExcempted='N' ;
	else
		set Message = 'Invalid TaxSubDetails_IsExcempted In- Update.';
		leave sp_Atma_Tax_Details_Set;
	end if;

	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.TaxDetails_TaxNo'))) into @TaxDetails_TaxNo;


	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.File_Name'))) into @FileName;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.FilePath')))  into @FilePath;

	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.TaxSubDetails_TaxRate_Gid')))
            into @TaxSubDetails_TaxRate_Gid;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.TaxSubDetails_TaxRate')))
            into @TaxSubDetails_TaxRate;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.TaxSubDetails_ExcemthroSold')))
            into @TaxSubDetails_ExcemthroSold;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.TaxSubDetails_ExcemRate')))
            into @TaxSubDetails_ExcemRate;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.TaxSubDetails_ExcemTo')))
            into @TaxSubDetails_ExcemTo;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.TaxSubDetails_ExcemFrom')))
            into @TaxSubDetails_ExcemFrom;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Entity_gid'))) into @Entity_gid;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Update_By')))
            into @Update_By;

	set Query_Update = '';
    set Query_Update = concat(Query_Update, ',taxdetails_tax_gid = ''',@TaxDetails_Tax_Gid,''' ');
	set Query_Update = concat(Query_Update, ',taxdetails_reftablecode = ''',@TaxDetails_Partnerbranchcode,''' ');
	set Query_Update = concat(Query_Update, ',taxdetails_subtax_gid = ''',@TaxDetails_Subtax_Gid,''' ');
	set Query_Update = concat(Query_Update, ',taxdetails_ismsme = ''',@TaxDetails_Is_MSME,''' ');
	set Query_Update = concat(Query_Update, ',taxdetails_taxno = ''',@TaxDetails_TaxNo,''' ');

	SET SQL_SAFE_UPDATES = 0;
	set Query_Update = concat('Update atma_tmp_mst_ttaxdetails
				 set update_date = CURRENT_TIMESTAMP,update_by=',@Update_By,'
				 ',Query_Update,'
				 Where taxdetails_gid = ',@TaxDetails_Gid,'
				 and taxdetails_isactive = ''Y'' and taxdetails_isremoved = ''N'';
				 ');
	#select Query_Update;
	set @Query_Update = '';
	set @Query_Update = Query_Update;
	PREPARE stmt FROM @Query_Update;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
	if countRow <= 0 then
		set Message = 'Error On Update1.';
		rollback;
		leave sp_Atma_Tax_Details_Set;
	elseif    countRow > 0 then
		set Message = 'SUCCESSFULLY UPDATED';
	end if;


	if  @TaxSubDetails_IsExcempted = 'Y' then
		set Query_Insert=concat('insert into gal_mst_tfile(file_name,
							file_path,entity_gid,create_by)
					values(''',@FileName,''',''',@FilePath,''',
                    ',@Entity_gid,',',@Update_By,')'
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
		select  LAST_INSERT_ID() into @Attachment_Gid ;
        set Query_Update = '';
        set Query_Update = concat(Query_Update, ',taxsubdetails_isexcempted = ''',@TaxSubDetails_IsExcempted,''' ');
        set Query_Update = concat(Query_Update, ',taxsubdetails_excemthrosold = ',@TaxSubDetails_ExcemthroSold,' ');
        set Query_Update = concat(Query_Update, ',taxsubdetails_excemrate = ''',@TaxSubDetails_ExcemRate,''' ');
		set Query_Update = concat(Query_Update, ',taxsubdetails_taxrate_gid = ''',@TaxSubDetails_TaxRate_Gid,''' ');
		set Query_Update = concat(Query_Update, ',taxsubdetails_taxrate = ''',@TaxSubDetails_TaxRate,''' ');
		set Query_Update = concat(Query_Update, ',taxsubdetails_excemfrom = ''',@TaxSubDetails_ExcemFrom,''' ');
		set Query_Update = concat(Query_Update, ',taxsubdetails_excemto = ''',@TaxSubDetails_ExcemTo,''' ');
        set Query_Update = concat(Query_Update, ',taxsubdetails_attachment_gid = ',@Attachment_Gid,' ');
        #select Query_Update,1;
		set Query_Update = concat('Update atma_tmp_mst_ttaxsubdetails
			 set update_date = CURRENT_TIMESTAMP,update_by=',@Update_By,'
			 ',Query_Update,'
			 Where taxsubdetails_taxdetails_gid = ',@TaxDetails_Gid,'
			 and taxsubdetails_isactive = ''Y'' and taxsubdetails_isremoved = ''N''
			 ');
	#select Query_Update;
	set @Query_Update = '';

	set @Query_Update = Query_Update;
	PREPARE stmt FROM @Query_Update;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
	if countRow <= 0 then
		set Message = 'Error On Update3.';
		rollback;
		leave sp_Atma_Tax_Details_Set;
	elseif    countRow > 0 then
		commit;
		set Message = 'SUCCESSFULLY UPDATED';
	end if;
    end if;

	if  @TaxSubDetails_IsExcempted = 'N'   then
		set Query_Update = '';
		set Query_Update = concat(Query_Update, ',taxsubdetails_isexcempted = ''',@TaxSubDetails_IsExcempted,''' ');
		set Query_Update = concat(Query_Update, ',taxsubdetails_excemrate = ''0.00'' ');
		set Query_Update = concat(Query_Update, ',taxsubdetails_excemfrom = null ');
		set Query_Update = concat(Query_Update, ',taxsubdetails_excemto = null ');
		set Query_Update = concat(Query_Update, ',taxsubdetails_excemthrosold = ''0.00'' ');
		set Query_Update = concat(Query_Update, ',taxsubdetails_attachment_gid = null ');
        set Query_Update = concat(Query_Update, ',taxsubdetails_taxrate_gid = ''',@TaxSubDetails_TaxRate_Gid,''' ');
		set Query_Update = concat(Query_Update, ',taxsubdetails_taxrate = ''',@TaxSubDetails_TaxRate,''' ');

        set Query_Update = concat('Update atma_tmp_mst_ttaxsubdetails
                         set update_date = CURRENT_TIMESTAMP,update_by=',@Update_By,'
                         ',Query_Update,'
						 Where taxsubdetails_taxdetails_gid = ',@TaxDetails_Gid,'
						 and taxsubdetails_isactive = ''Y'' and taxsubdetails_isremoved = ''N''
                         ');
	#select Query_Update,3;
	set @Query_Update = '';
	set @Query_Update = Query_Update;
	PREPARE stmt FROM @Query_Update;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;

		if countRow <= 0 then
				set Message = 'Error On Update_n2.';
				rollback;
				leave sp_Atma_Tax_Details_Set;
		elseif    countRow > 0 then
				commit;
				set Message = 'SUCCESSFULLY UPDATED';
        end if;
	end if;
End if;



END