CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Pending_To_Approval_Taxdetails_Set`(in li_Action  varchar(30),
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_Atma_Pending_To_Approval_Taxdetails_Set:BEGIN
declare Query_Insert varchar(10000);
Declare countRow varchar(6000);
declare Query_Update varchar(10000);
declare Query_delete varchar(1000);
declare Query_Value varchar(1000);
declare Query_Column varchar(1000);
declare p_partnerbranch_code varchar(8);
Declare t_taxdetails_gid,t_taxdetails_tax_gid,t_taxdetails_subtax_gid,t_taxdetails_ref_gid,t_taxdetails_type,t_taxdetails_ismsme,t_taxdetails_reftablecode,
		t_taxdetails_taxno,t_taxdetails_isactive,t_taxdetails_isremoved,t_entity_gid,t_create_by,t_update_by,t_main_taxdetails_gid varchar (150);
Declare tsd_taxsubdetails_gid,tsd_taxsubdetails_taxdetails_gid,tsd_taxsubdetails_subtax_gid,tsd_taxsubdetails_taxrate_gid,tsd_taxsubdetails_taxrate,tsd_taxsubdetails_isexcempted,
		tsd_taxsubdetails_excemfrom,tsd_taxsubdetails_excemto,tsd_taxsubdetails_excemthrosold,tsd_taxsubdetails_excemrate,tsd_taxsubdetails_attachment_gid,tsd_taxsubdetails_isactive,
		tsd_taxsubdetails_isremoved,tsd_entity_gid,tsd_create_by,tsd_update_by,tsd_main_taxsubdetails_gid varchar(150);
DECLARE finished INTEGER DEFAULT 0;
DECLARE finished1 INTEGER DEFAULT 0;
DECLARE finished3 INTEGER DEFAULT 0;
Declare errno int;
Declare msg,Error_Level varchar(1000);

						DECLARE EXIT HANDLER FOR SQLEXCEPTION
						BEGIN
							GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
							set Message = concat(Error_Level,':No-',errno,msg);
							ROLLBACK;
						END;

IF li_Action='Insert' then



	select JSON_LENGTH(lj_filter,'$') into @lj_filter_json_count;
	select JSON_LENGTH(lj_classification,'$') into @lj_classification_json_count;

	if @lj_filter_json_count = 0 or @lj_filter_json_count is null then
		set Message = 'No Data In filter Json. ';
		leave sp_Atma_Pending_To_Approval_Taxdetails_Set;
	End if;

	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Gid')))
	into @Partner_Gid;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Update_By')))
	into @Update_By;

	if @Partner_Gid = '' or @Partner_Gid is null  or @Partner_Gid=0 then
			set Message = 'Partner Is Not Provided';
			leave sp_Atma_Pending_To_Approval_Taxdetails_Set;
	End if;


      #SET finished =0;
     # set @Main_partner_gid=4;
       select partner_code from atma_tmp_tpartner
          where partner_gid=@Partner_Gid into @partnercode;
 #SET finished =0;

BEGIN
	Declare Cursor_atma CURSOR FOR

	select taxdetails_gid,taxdetails_tax_gid,taxdetails_subtax_gid,taxdetails_ref_gid,taxdetails_type,
    taxdetails_ismsme,taxdetails_reftablecode,taxdetails_taxno,taxdetails_isactive,taxdetails_isremoved,
    b.entity_gid,b.create_by,b.update_by,b.main_taxdetails_gid
	 from atma_tmp_mst_ttaxdetails b
     inner join  atma_tmp_mst_tpartnerbranch  on taxdetails_reftablecode=partnerbranch_code
            and partnerbranch_partnergid=@Partner_Gid;


	DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;

	OPEN Cursor_atma;
	atma_looop:loop
		fetch Cursor_atma into t_taxdetails_gid,t_taxdetails_tax_gid,t_taxdetails_subtax_gid,t_taxdetails_ref_gid,
        t_taxdetails_type,t_taxdetails_ismsme,t_taxdetails_reftablecode,
		t_taxdetails_taxno,t_taxdetails_isactive,t_taxdetails_isremoved,t_entity_gid,t_create_by,t_update_by,
        t_main_taxdetails_gid;
		if finished = 1 then
			leave atma_looop;
		End if;


	if t_main_taxdetails_gid = '' or t_main_taxdetails_gid is null  or t_main_taxdetails_gid=0 then

				set Query_Column='';
				set Query_Value ='';

				if t_taxdetails_type is not null then
					set Query_Column = concat(Query_Column,',taxdetails_type ');
					set Query_Value=concat(Query_Value,', ''',t_taxdetails_type,''' ');
				else
					set Query_Column = concat('');
					set Query_Value=concat('');
				end if;

                if t_taxdetails_reftablecode is not null then
					set Query_Column = concat(Query_Column,',taxdetails_reftablecode ');
					set Query_Value=concat(Query_Value,', ''',t_taxdetails_reftablecode,''' ');
				else
					set Query_Column = concat('');
					set Query_Value=concat('');
				end if;

                if t_taxdetails_taxno is not null then
					set Query_Column = concat(Query_Column,',taxdetails_taxno ');
					set Query_Value=concat(Query_Value,', ''',t_taxdetails_taxno,''' ');
				else
					set Query_Column = concat('');
					set Query_Value=concat('');
				end if;

 set Error_Level='ATMA59.1';
			set Query_Update = concat('INSERT INTO gal_mst_ttaxdetails (taxdetails_tax_gid,taxdetails_subtax_gid,taxdetails_ref_gid,taxdetails_ismsme,taxdetails_isactive,
            taxdetails_isremoved,entity_gid,create_by ',Query_Column,')values (',t_taxdetails_tax_gid,',',t_taxdetails_subtax_gid,',',t_taxdetails_ref_gid,',''',t_taxdetails_ismsme,''',
			''',t_taxdetails_isactive,''',''',t_taxdetails_isremoved,''',',t_entity_gid,',',t_create_by,'
            ',Query_Value,')');
			#select Query_Update;

	else
set Error_Level='ATMA59.2';

        SET SQL_SAFE_UPDATES = 0;
		 	set Query_Update = concat('Update gal_mst_ttaxdetails  set
			taxdetails_tax_gid=',t_taxdetails_tax_gid,',taxdetails_subtax_gid=',t_taxdetails_subtax_gid,',taxdetails_ref_gid=',t_taxdetails_ref_gid,'
            ,taxdetails_type=''',ifnull(t_taxdetails_type,''),''',taxdetails_ismsme=''',t_taxdetails_ismsme,''',taxdetails_taxno=''',ifnull(t_taxdetails_taxno,''),''',
            taxdetails_reftablecode=''',ifnull(t_taxdetails_reftablecode,''),''',
			entity_gid=',t_entity_gid,',update_by=',@Update_By,',update_date=''',now(),''' where
			taxdetails_gid=',t_main_taxdetails_gid,'');

         # select Query_Update;
		end if;

		set @Insert_query = Query_Update;
		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;

		if countRow >  0 then
			set Message = 'SUCCESS';
		else
			set Message = ' FAILED Tax';
            leave sp_Atma_Pending_To_Approval_Taxdetails_Set;

		end if;
        select last_insert_id() into @tsd_taxsubdetails_taxdetails_gid;
 SET finished1 =0;
BEGIN
	Declare Cursor_atma1 CURSOR FOR

	select taxsubdetails_gid,taxsubdetails_taxdetails_gid,taxsubdetails_subtax_gid,taxsubdetails_taxrate_gid,
	taxsubdetails_taxrate,taxsubdetails_isexcempted,taxsubdetails_excemfrom,taxsubdetails_excemto,
	taxsubdetails_excemthrosold,taxsubdetails_excemrate,taxsubdetails_attachment_gid,taxsubdetails_isactive,
	taxsubdetails_isremoved,entity_gid,create_by,update_by,main_taxsubdetails_gid
    from atma_tmp_mst_ttaxsubdetails where taxsubdetails_taxdetails_gid=t_taxdetails_gid ;

	DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished1 = 1;
    #select 1;
	OPEN Cursor_atma1;
	atma_looop1:loop
		fetch Cursor_atma1 into tsd_taxsubdetails_gid,tsd_taxsubdetails_taxdetails_gid,tsd_taxsubdetails_subtax_gid,
        tsd_taxsubdetails_taxrate_gid,tsd_taxsubdetails_taxrate,tsd_taxsubdetails_isexcempted,
		tsd_taxsubdetails_excemfrom,tsd_taxsubdetails_excemto,tsd_taxsubdetails_excemthrosold,
        tsd_taxsubdetails_excemrate,tsd_taxsubdetails_attachment_gid,tsd_taxsubdetails_isactive,
		tsd_taxsubdetails_isremoved,tsd_entity_gid,tsd_create_by,tsd_update_by,tsd_main_taxsubdetails_gid;
        #select Cursor_atma;


		if finished1 = 1 then
			leave atma_looop1;
		End if;


	if tsd_main_taxsubdetails_gid = '' or tsd_main_taxsubdetails_gid is null  or tsd_main_taxsubdetails_gid=0 then

				set Query_Column='';
				set Query_Value ='';

				if tsd_taxsubdetails_isexcempted is not null then
					set Query_Column = concat(Query_Column,',taxsubdetails_isexcempted ');
					set Query_Value=concat(Query_Value,', ''',tsd_taxsubdetails_isexcempted,''' ');
				else
					set Query_Column = concat('');
					set Query_Value=concat('');
				end if;
                /*
                if tsd_taxsubdetails_excemfrom is not null then
					set Query_Column = concat(Query_Column,',taxsubdetails_excemfrom ');
					set Query_Value=concat(Query_Value,', ''',tsd_taxsubdetails_excemfrom,''' ');
				else
					set Query_Column = concat('');
					set Query_Value=concat('');
				end if;

                if tsd_taxsubdetails_excemto is not null then
					set Query_Column = concat(Query_Column,',taxsubdetails_excemto ');
					set Query_Value=concat(Query_Value,', ''',tsd_taxsubdetails_excemto,''' ');
				else
					set Query_Column = concat('');
					set Query_Value=concat('');
				end if;
				*/

                if tsd_taxsubdetails_attachment_gid is not null then
					set Query_Column = concat(Query_Column,',taxsubdetails_attachment_gid ');
					set Query_Value=concat(Query_Value,', ',tsd_taxsubdetails_attachment_gid,' ');
				else
					set Query_Column = concat('');
					set Query_Value=concat('');
				end if;

  set Error_Level='ATMA59.3';

			set Query_Update = concat('INSERT INTO gal_mst_ttaxsubdetails (taxsubdetails_taxdetails_gid,
            taxsubdetails_subtax_gid,taxsubdetails_taxrate_gid,taxsubdetails_taxrate,
            taxsubdetails_excemfrom,
            taxsubdetails_excemto,
            taxsubdetails_excemthrosold,
            taxsubdetails_excemrate,taxsubdetails_isactive,taxsubdetails_isremoved,
            entity_gid,create_by ',Query_Column,')values (',@tsd_taxsubdetails_taxdetails_gid,',
			',tsd_taxsubdetails_subtax_gid,',',tsd_taxsubdetails_taxrate_gid,',''',tsd_taxsubdetails_taxrate,''',
            ',if(ifnull(tsd_taxsubdetails_excemfrom,null) IS NULL,'NULL',CONCAT('''',tsd_taxsubdetails_excemfrom,'''')),',
            ',if(ifnull(tsd_taxsubdetails_excemto,null) IS NULL,'NULL',CONCAT('''',tsd_taxsubdetails_excemto,'''')),',
            ''',tsd_taxsubdetails_excemthrosold,''',''',tsd_taxsubdetails_excemrate,''',
            ''',tsd_taxsubdetails_isactive,''',''',tsd_taxsubdetails_isremoved,''',',tsd_entity_gid,',
            ',tsd_create_by,' ',Query_Value,')');
            #select tsd_taxsubdetails_attachment_gid;
           #select Query_Update;
           SET SQL_SAFE_UPDATES = 0;
            set Query_delete=concat('DELETE FROM atma_tmp_mst_ttaxsubdetails
									 WHERE taxsubdetails_gid=',tsd_taxsubdetails_gid,'
                                     ');
                                     #select Query_delete;
			set @Insert_query = Query_delete;
			PREPARE stmt FROM @Insert_query;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;
			if countRow >  0 then
			set Message = 'DELETED TAXSUB';
			else
			set Message = ' FAILED DELETION_TS';
            leave sp_Atma_Pending_To_Approval_Taxdetails_Set;
			end if;

	else
set Error_Level='ATMA59.4';

        SET SQL_SAFE_UPDATES = 0;
		 	set Query_Update = concat('Update gal_mst_ttaxsubdetails  set
            taxsubdetails_subtax_gid=',tsd_taxsubdetails_subtax_gid,',
            taxsubdetails_taxrate_gid=',tsd_taxsubdetails_taxrate_gid,',
            taxsubdetails_taxrate=''',tsd_taxsubdetails_taxrate,''',
            taxsubdetails_isexcempted=''',ifnull(tsd_taxsubdetails_isexcempted,''),''',
            taxsubdetails_excemfrom=',if(ifnull(tsd_taxsubdetails_excemfrom,null) IS NULL,'NULL',CONCAT('''',tsd_taxsubdetails_excemfrom,'''')),',
            taxsubdetails_excemto=',if(ifnull(tsd_taxsubdetails_excemto,null) IS NULL,'NULL',CONCAT('''',tsd_taxsubdetails_excemto,'''')),',
            taxsubdetails_excemthrosold=''',tsd_taxsubdetails_excemthrosold,''',
            taxsubdetails_excemrate=''',tsd_taxsubdetails_excemrate,''',
            taxsubdetails_attachment_gid=',ifnull(tsd_taxsubdetails_attachment_gid,'0'),',
            update_by=',@Update_By,',update_date=''',now(),'''
            where taxsubdetails_gid=',tsd_main_taxsubdetails_gid,'');
          # select tsd_taxsubdetails_taxrate_gid;

           SET SQL_SAFE_UPDATES = 0;
            set Query_delete=concat('DELETE FROM atma_tmp_mst_ttaxsubdetails
									 WHERE taxsubdetails_gid=',tsd_taxsubdetails_gid,'
                                     ');
                                     #select Query_delete;
			set @Insert_query = Query_delete;
			PREPARE stmt FROM @Insert_query;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;
			if countRow >  0 then
			set Message = 'DELETED TAXSUB';
			else
			set Message = ' FAILED DELETION_TS';
            leave sp_Atma_Pending_To_Approval_Taxdetails_Set;
			end if;

	end if;

		#select Query_Update;
		set @Insert_query = Query_Update;
		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());

		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'SUCCESS ';

		else
			set Message = ' FAILED Sub_Tax ';
            leave sp_Atma_Pending_To_Approval_Taxdetails_Set;

		end if;


	End loop atma_looop1;
	close Cursor_atma1;
	end;  #Endof Cursor SUB TAX

   End loop atma_looop;
	close Cursor_atma;
	end;  #Endof Cursor TAX
   # select tsd_taxsubdetails_gid;


			BEGIN
            Declare Cursor_atma3 CURSOR FOR
            select partnerbranch_code from atma_tmp_mst_tpartnerbranch
            where partnerbranch_partnergid=@Partner_Gid;
            DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished3 = 1;
			OPEN Cursor_atma3;
			atma_looop3:loop
			fetch Cursor_atma3 into p_partnerbranch_code;
            if finished3 = 1 then
				leave atma_looop3;
			End if;
            SET SQL_SAFE_UPDATES = 0;
            set Query_delete=concat('DELETE FROM atma_tmp_mst_ttaxdetails WHERE
            taxdetails_reftablecode=''',p_partnerbranch_code ,'''');

			set @Insert_query = Query_delete;
			PREPARE stmt FROM @Insert_query;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;
			if countRow >  0 then
			set Message = 'SUCCESS';
			else
			set Message = concat('1.1.FAILED DELETION ' ,countRow,@Insert_query);
            leave sp_Atma_Pending_To_Approval_Taxdetails_Set;
			end if;
			End loop atma_looop3;
	close Cursor_atma3;
	end;  #Endof Cursor_atma3

END IF;

END