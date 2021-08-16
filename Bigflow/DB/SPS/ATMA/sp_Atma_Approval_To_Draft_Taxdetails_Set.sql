CREATE  PROCEDURE `sp_Atma_Approval_To_Draft_Taxdetails_Set`(in li_Action  varchar(30),
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_Atma_Approval_To_Draft_Taxdetails_Set:BEGIN
declare Query_Insert varchar(10000);
Declare countRow varchar(6000);
declare Query_Update varchar(10000);
declare Query_delete varchar(1000);
declare Query_Value varchar(1000);
declare Query_Column varchar(1000);
Declare  t_taxdetails_gid,t_taxdetails_tax_gid,t_taxdetails_subtax_gid,t_taxdetails_ref_gid,t_taxdetails_type,t_taxdetails_ismsme,t_taxdetails_reftablecode,
		t_taxdetails_taxno,t_taxdetails_isactive,t_taxdetails_isremoved,t_entity_gid,t_create_by,t_create_date varchar(150);
Declare tsd_taxsubdetails_gid,tsd_taxsubdetails_taxdetails_gid,tsd_taxsubdetails_subtax_gid,tsd_taxsubdetails_taxrate_gid,tsd_taxsubdetails_taxrate,tsd_taxsubdetails_isexcempted,
		tsd_taxsubdetails_excemfrom,tsd_taxsubdetails_excemto,tsd_taxsubdetails_excemthrosold,tsd_taxsubdetails_excemrate,tsd_taxsubdetails_attachment_gid,tsd_taxsubdetails_isactive,
		tsd_taxsubdetails_isremoved,tsd_entity_gid,tsd_create_by,tsd_create_date varchar(150);
DECLARE finished INTEGER DEFAULT 0;
DECLARE finished1 INTEGER DEFAULT 0;
Declare errno int;
Declare msg varchar(1000);

						DECLARE EXIT HANDLER FOR SQLEXCEPTION
						BEGIN
							GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
							set Message = concat(errno , msg);
							ROLLBACK;
						END;

IF li_Action='Insert' then



	select JSON_LENGTH(lj_filter,'$') into @lj_filter_json_count;
	select JSON_LENGTH(lj_classification,'$') into @lj_classification_json_count;

	if @lj_filter_json_count = 0 or @lj_filter_json_count is null then
		set Message = 'No Data In filter Json. ';
		leave sp_Atma_Approval_To_Draft_Taxdetails_Set;
	End if;

	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Gid')))
	into @Partner_Gid;

	if @Partner_Gid = '' or @Partner_Gid is null  or @Partner_Gid=0 then
			set Message = 'Partner Is Not Provided';
			leave sp_Atma_Approval_To_Draft_Taxdetails_Set;
	End if;

    SELECT EXISTS(
         select true from  atma_mst_tpartnerbranch inner join  gal_mst_ttaxdetails
         on taxdetails_reftablecode=partnerbranch_code
						where partnerbranch_partnergid=@Partner_Gid) into @pt_tax;

	if @pt_tax=1 then



      SET finished =0;
     # set @Main_partner_gid=4;

  ############TAXDETAILS
 #set @PARTNERCODE='';
 select partner_code from atma_mst_tpartner
          where partner_gid=@Partner_Gid into @PARTNERCODE;

# SET finished =0;

	BEGIN

	Declare Cursor_atma CURSOR FOR

	select taxdetails_gid,taxdetails_tax_gid,taxdetails_subtax_gid,taxdetails_ref_gid,taxdetails_type,
    taxdetails_ismsme,taxdetails_reftablecode,taxdetails_taxno,taxdetails_isactive,taxdetails_isremoved,
    a.entity_gid,a.create_by,a.create_date
	 from gal_mst_ttaxdetails a
	 inner join atma_mst_tpartnerbranch on taxdetails_reftablecode=partnerbranch_code
            and partnerbranch_partnergid=@Partner_Gid;

	DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;
    #select @PARTNERCODE;

	OPEN Cursor_atma;
	atma_looop:loop
		fetch Cursor_atma into t_taxdetails_gid,t_taxdetails_tax_gid,t_taxdetails_subtax_gid,t_taxdetails_ref_gid,t_taxdetails_type,t_taxdetails_ismsme,t_taxdetails_reftablecode,
		t_taxdetails_taxno,t_taxdetails_isactive,t_taxdetails_isremoved,t_entity_gid,t_create_by,t_create_date;

		if finished = 1 then
			leave atma_looop;
		End if;


			set Query_Insert = concat('INSERT INTO atma_tmp_mst_ttaxdetails (taxdetails_tax_gid,taxdetails_subtax_gid,taxdetails_ref_gid,
            taxdetails_type,taxdetails_ismsme,taxdetails_reftablecode,taxdetails_taxno,taxdetails_isactive,
			taxdetails_isremoved,entity_gid,create_by,create_date,main_taxdetails_gid)values (',t_taxdetails_tax_gid,',
			',t_taxdetails_subtax_gid,',
            ',t_taxdetails_ref_gid,',
            ''',ifnull(t_taxdetails_type,''),''',
            ''',t_taxdetails_ismsme,''',
            ''',ifnull(t_taxdetails_reftablecode,''),''',
            ''',ifnull(t_taxdetails_taxno,''),''',
            ''',t_taxdetails_isactive,''',
            ''',t_taxdetails_isremoved,''',
            ',t_entity_gid,',
            ',t_create_by,',
            ''',t_create_date,''',
            ',t_taxdetails_gid,')');

		#select Query_Insert;
		set @Insert_query = Query_Insert;
		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'SUCCESS';
		else
			set Message = ' FAILED TAXDETAILS';
			leave sp_Atma_Approval_To_Draft_Taxdetails_Set;
		end if;
	set @taxsubdetails_taxdetails_gid='';
	select LAST_INSERT_ID() into @taxsubdetails_taxdetails_gid;


 ########TAXSUBDETAILS

 SET finished1 =0;

	BEGIN

	Declare Cursor_atma1 CURSOR FOR

	select taxsubdetails_gid,taxsubdetails_taxdetails_gid,taxsubdetails_subtax_gid,taxsubdetails_taxrate_gid,
	taxsubdetails_taxrate,taxsubdetails_isexcempted,taxsubdetails_excemfrom,taxsubdetails_excemto,
	taxsubdetails_excemthrosold,taxsubdetails_excemrate,taxsubdetails_attachment_gid,taxsubdetails_isactive,
	taxsubdetails_isremoved,entity_gid,create_by,create_date from gal_mst_ttaxsubdetails
    where taxsubdetails_taxdetails_gid=t_taxdetails_gid;

	DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished1 = 1;
    #select @PARTNERCODE;

	OPEN Cursor_atma1;
	atma_looop1:loop
		fetch Cursor_atma1 into tsd_taxsubdetails_gid,tsd_taxsubdetails_taxdetails_gid,tsd_taxsubdetails_subtax_gid,tsd_taxsubdetails_taxrate_gid,tsd_taxsubdetails_taxrate,tsd_taxsubdetails_isexcempted,
		tsd_taxsubdetails_excemfrom,tsd_taxsubdetails_excemto,tsd_taxsubdetails_excemthrosold,tsd_taxsubdetails_excemrate,tsd_taxsubdetails_attachment_gid,tsd_taxsubdetails_isactive,
		tsd_taxsubdetails_isremoved,tsd_entity_gid,tsd_create_by,tsd_create_date;



		if finished1 = 1 then
			leave atma_looop1;
		End if;


			set Query_Insert = concat('INSERT INTO atma_tmp_mst_ttaxsubdetails (taxsubdetails_taxdetails_gid,taxsubdetails_subtax_gid,
            taxsubdetails_taxrate_gid,taxsubdetails_taxrate,taxsubdetails_isexcempted,taxsubdetails_excemfrom,taxsubdetails_excemto,
            taxsubdetails_excemthrosold,taxsubdetails_excemrate,taxsubdetails_attachment_gid,taxsubdetails_isactive,taxsubdetails_isremoved,
            entity_gid,create_by,create_date,main_taxsubdetails_gid)values (',@taxsubdetails_taxdetails_gid,',
			',tsd_taxsubdetails_subtax_gid,',
            ',tsd_taxsubdetails_taxrate_gid,',
            ''',tsd_taxsubdetails_taxrate,''',
            ''',ifnull(tsd_taxsubdetails_isexcempted,''),''',
			',if(ifnull(tsd_taxsubdetails_excemfrom,null) IS NULL,'NULL',CONCAT('''',tsd_taxsubdetails_excemfrom,'''')),',
			',if(ifnull(tsd_taxsubdetails_excemto,null) IS NULL,'NULL',CONCAT('''',tsd_taxsubdetails_excemto,'''')),',
            ''',ifnull(tsd_taxsubdetails_excemthrosold,''),''',
            ''',ifnull(tsd_taxsubdetails_excemrate,''),''',
            ',ifnull(tsd_taxsubdetails_attachment_gid,0),',
            ''',tsd_taxsubdetails_isactive,''',
            ''',tsd_taxsubdetails_isremoved,''',
            ',tsd_entity_gid,',
            ',tsd_create_by,',
            ''',tsd_create_date,''',
            ',tsd_taxsubdetails_gid,')');

		#select Query_Insert;
		set @Insert_query = Query_Insert;
		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'SUCCESS';
		else
			set Message = ' FAILED TAXSUBDETAILS';
			leave sp_Atma_Approval_To_Draft_Taxdetails_Set;
		end if;
End loop atma_looop1;
close Cursor_atma1;
end;  #Endof Cursor SUBTAX

     End loop atma_looop;
close Cursor_atma;
end;  #Endof Cursor TAX
   end if; ###@pt_tax
END If;
END