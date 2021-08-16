CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Customergroup_Set`(IN `Action` varchar(16),IN `li_custgrp_gid` int,
IN `ls_custgrp_code` VARCHAR(8),IN `ls_custgrp_name` varchar(128),IN `li_add_gid` int,IN `ls_cpname1` varchar(64),
IN `ls_desig1` varchar(64),IN `ls_Mobile1` varchar(16),IN `ls_landln1` varchar(16),IN `ls_cpname2` varchar(64),
IN `ls_desig2` varchar(64),IN `ls_Mobile2` varchar(16),IN `ls_landln2` varchar(16),IN `li_client_gid` int,IN `li_entity_gid` int,
IN `ls_create_by` int,OUT `Message` varchar(1000))
BEGIN

#Vigneshwari       26-03-2018
#meenakshi edited SUPP_INSERT 13-02-2020

declare custgrp_srch text;
declare Query1 varchar(1000);
declare Query2 varchar(1000);
declare ls_error varchar(100);
declare countRow int;
declare errno int;
declare msg varchar(1000);
declare ls_no varchar(64);
declare Query_Update varchar(9000);

	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
    set Message = concat(errno , msg);
    ROLLBACK;
    END;

set ls_error = '';
set Query1 = '';
set Query2 = '';

if Action = 'Insert' then

	if ls_custgrp_code = '' then
		set ls_error = 'Customer Group Code Not Given ';
	end if;

    if ls_custgrp_name = '' then
		set ls_error = 'Customer Group Name Not Given';
	end if;

	if ls_cpname1 <> '' then
		set Query1 = concat(Query1,'customergroup_cpname,');
        set Query2 = concat(Query2,'''' ,ls_cpname1, ''',');
	else
		set Query1 = concat(Query1,'');
		set Query2 = concat(Query2,'');
	end if;

    if ls_desig1 <> '' then
		set Query1 = concat(Query1,'customergroup_cpdesignation,');
        set Query2 = concat(Query2,'''' ,ls_desig1, ''',');
	else
		set Query1 = concat(Query1,'');
		set Query2 = concat(Query2,'');
	end if;

	if ls_Mobile1 <> '' then
		set Query1 = concat(Query1,'customergroup_cpmobileno,');
        set Query2 = concat(Query2,'''' ,ls_Mobile1, ''',');
	else
		set Query1 = concat(Query1,'');
		set Query2 = concat(Query2,'');
	end if;

	if ls_landln1 <> '' then
		set Query1 = concat(Query1,'customergroup_cplandline,');
        set Query2 = concat(Query2,'''' ,ls_landln1, ''',');
	else
		set Query1 = concat(Query1,'');
		set Query2 = concat(Query2,'');
	end if;

	if ls_cpname2 <> '' then
		set Query1 = concat(Query1,'customergroup_cpname2,');
        set Query2 = concat(Query2,'''' ,ls_cpname1, ''',');
	else
		set Query1 = concat(Query1,'');
		set Query2 = concat(Query2,'');
	end if;

    if ls_desig2 <> '' then
		set Query1 = concat(Query1,'customergroup_cpdesignation2,');
        set Query2 = concat(Query2,'''' ,ls_desig1, ''',');
	else
		set Query1 = concat(Query1,'');
		set Query2 = concat(Query2,'');
	end if;

	if ls_Mobile2 <> '' then
		set Query1 = concat(Query1,'customergroup_cpmobileno2,');
        set Query2 = concat(Query2,'''' ,ls_Mobile1, ''',');
	else
		set Query1 = concat(Query1,'');
		set Query2 = concat(Query2,'');
	end if;

	if ls_landln2 <> '' then
		set Query1 = concat(Query1,'customergroup_cplandline2,');
        set Query2 = concat(Query2,'''' ,ls_landln2, ''',');
	else
		set Query1 = concat(Query1,'');
		set Query2 = concat(Query2,'');
	end if;

     if li_client_gid = 0 then
		set ls_error = 'Client Gid Not Given';
	end if;

	if ls_error = '' then

		start transaction;

			set custgrp_srch = concat('insert into gal_mst_tcustomergroup (customergroup_code,customergroup_name , customergroup_add_gid, '
									,Query1,' entity_gid , create_by,customergroup_clientgid) values (''',ls_custgrp_code,''',''' ,ls_custgrp_name,
                                    ''',' ,li_add_gid,',' ,Query2, '' ,li_entity_gid, ',' ,ls_create_by, ',',li_client_gid,')');

		set @custgrp_srch = custgrp_srch;
        #SELECT @custgrp_srch;
		PREPARE stmt FROM @custgrp_srch;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;

		if countRow >  0 then
			select LAST_INSERT_ID() into Message ;
            set Message = concat(Message,',SUCCESS');
			commit;
		else
			set Message = 'FAIL';
			rollback;
		end if;
	else
		set Message = ls_error;
	end if;
end if;

if Action = 'Update' then

	if li_custgrp_gid = 0 then
		set ls_error = 'Customer Group gid Not Given ';
	end if;

	if ls_custgrp_code = '' then
		set ls_error = 'Customer Group Code Not Given ';
	end if;

    if ls_custgrp_name = '' then
		set ls_error = 'Customer Group Name Not Given';
	end if;

	if li_add_gid = 0 then
		set ls_error = 'Address Gid Not Given ';
	end if;

    if ls_error = '' then
		start transaction;

         set  Query_Update = Concat('Update gal_mst_tcustomergroup set customergroup_code =''', ls_custgrp_code,''', customergroup_name = ''',ls_custgrp_name,''',
						customergroup_add_gid = ',li_add_gid,',	update_by = ',ls_create_by,', Update_date = now()');

		if ls_cpname1 <> '' then
			set Query_Update = Concat(Query_Update, ',customergroup_cpname = ''', ls_cpname1 ,'''');
		end if;

		if ls_desig1 <> '' then
			set Query_Update = Concat(Query_Update, ',customergroup_cpdesignation = ''', ls_desig1 ,'''');
		end if;

		if ls_Mobile1 <> '' then
			set Query_Update = Concat(Query_Update, ',customergroup_cpmobileno = ''', ls_Mobile1 ,'''');
		end if;

		if ls_landln1 <> '' then
			set Query_Update = Concat(Query_Update, ',customergroup_cplandline = ''', ls_landln1 ,'''');
		end if;

		if ls_cpname2 <> '' then
			set Query_Update = Concat(Query_Update, ',customergroup_cpname2 = ''', ls_cpname2 ,'''');
		end if;

		if ls_desig2 <> '' then
			set Query_Update = Concat(Query_Update, ',customergroup_cpdesignation2 = ''', ls_desig2 ,'''');
		end if;

		if ls_Mobile2 <> '' then
			set Query_Update = Concat(Query_Update, ',customergroup_cpmobileno2 = ''', ls_Mobile2 ,'''');
		end if;

		if ls_landln2 <> '' then
			set Query_Update = Concat(Query_Update, ',customergroup_cplandline2 = ''', ls_landln2 ,'''');
		end if;

        if li_client_gid <> 0 then
			set Query_Update = Concat(Query_Update, ',customergroup_clientgid = ''', li_client_gid ,'''');
        end if;

        set Query_Update = Concat(Query_Update, 'where customergroup_isremoved = ''N'' and customergroup_isactive = ''Y''
                        and customergroup_gid = ',li_custgrp_gid) ;
		set @Query_Update = Query_Update;
		PREPARE stmt FROM @Query_Update;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;

		if countRow > 0 then
			set Message = 'SUCCESS';
			commit;
		else
			set Message = 'FAIL';
			rollback;
		end if;
	else
		set Message = ls_error;
	end if;

end if;


if Action = 'SUPP_INSERT' then
	if li_custgrp_gid = 0 then
		set ls_error = 'Customer Group gid Not Given ';
	end if;

    if ls_custgrp_name = '' then
		set ls_error = 'Customer Group Name Not Given';
	end if;

     select substring(supplier_code,5)  from gal_mst_tsupplier where supplier_gid =(select max(supplier_gid)
	 from gal_mst_tsupplier where supplier_isremoved='N') into @codes;

    call sp_Generatecode_Get('WITHOUT_DATE','SUPP','000',@codes,@Message) ;
	 select @Message into @Supplier_code;

      set @query_insert =concat('insert into gal_mst_tsupplier (supplier_code,supplier_name,supplier_contact_gid,supplier_add_gid,supplier_capacity,supplier_customergroupgid,
                                entity_gid,create_by) values(''',@Supplier_code,''',''',ls_custgrp_name,''',
                                0,0,0,''',li_custgrp_gid,''',',li_entity_gid,',''',ls_create_by,''')');
        #select ls_custgrp_name;
        set @supp_srch = @query_insert;

        #SELECT @supp_srch;
        PREPARE stmt FROM @supp_srch;
        EXECUTE stmt;
        set countRow = (select ROW_COUNT());
       #select countRow;
		if countRow > 0 then
			set Message = 'SUCCESS';

	  select customergroup_gid,customergroup_code,customergroup_cpname,customergroup_add_gid,customergroup_cpmobileno,
	  customergroup_cplandline, customergroup_cplandline2,customergroup_cpmobileno2
	  into @cust_gid,@cust_code,@cust_cp,@cust_add,@cust_mob,@cust_landline,@cust_mob2,@cust_landline2  from gal_mst_tcustomergroup
	  where customergroup_gid=li_custgrp_gid;

	  #select  @cust_gid,@cust_code,@cust_cp,@cust_add,@cust_mob,@cust_landline,@cust_mob2,@cust_landline2 ;
	if @cust_cp <> '' then
		set query1 = concat('Contact_personname ',query1);
        set query2 = concat(',''' ,@cust_cp, '''',query2);
        else
		set query1 = concat(query1,'');
		set query2 = concat(query2,'');
	end if;

    if @cust_mob<> '' then
		set query1 = concat('Contact_mobileno ,',query1);
        set query2 = concat(',''' ,@cust_mob, '''',query2);
        else
		set query1 = concat(query1,'');
		set query2 = concat(query2,'');
	end if;

    if @cust_landline<> '' then
		set query1 = concat(',Contact_landline, ',query1);
        set query2 = concat(',''' ,@cust_landline, '''',query2);
        else
		set query1 = concat(query1,'');
		set query2 = concat(query2,'');
	end if;


   if @cust_mob2<> '' then
		set query1 = concat('Contact_mobileno2 ',query1);
        set query2 = concat(',''' ,@cust_mob2, '''',query2);
        else
		set query1 = concat(query1,'');
		set query2 = concat(query2,'');
	end if;

    if @cust_landline2<> '' then
		set query1 = concat('Contact_landline2,',query1);
        set query2 = concat(',''' ,@cust_landline2, '''',query2);
        else
		set query1 = concat(query1,'');
		set query2 = concat(query2,'');
	end if;

    #select query1,query2;
             set @Cont_srch1 = concat('INSERT INTO gal_mst_tcontact (Contact_ref_gid, Contact_reftable_gid, contact_reftablecode,
									   Contact_contacttype_gid, Contact_designation_gid,Contact_email,Contact_DOB,Contact_WD,entity_gid, create_by ',query1,')
                                       VALUES (8,' , @cust_gid, ','''
                                       ,@cust_code, ''',2,15,
                                       ''' ''',0000-00-00,0000-00-00,',li_entity_gid, ',
                                       ' ,ls_create_by,'',query2,' )');

		#select @Cont_srch1;  ### Remove It
		PREPARE stmt FROM @Cont_srch1;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;

          #select @cust_code;

          select contact_gid into @cont_gid from gal_mst_tcontact where contact_reftablecode =  @cust_code;
          SET SQL_SAFE_UPDATES = 0;



            set @Query_Update = concat('update gal_mst_tsupplier set supplier_contact_gid = ', @cont_gid,' ,supplier_add_gid=',@cust_add,'  where supplier_name=''',ls_custgrp_name,''' ');
            #select @Query_Update;
             PREPARE stmt FROM @Query_Update;
		     EXECUTE stmt;

			commit;
        end if;
end if;

/*
if Action = 'Update' then

	if li_dept_gid = 0 then
		set ls_error = 'Department gid Not Given ';
	end if;

	if ls_dept_code = '' then
		set ls_error = 'Department Code Not Given ';
	end if;

    if ls_dept_name = '' then
		set ls_error = 'Department Name Not Given';
	end if;

    if ls_error = '' then
		start transaction;

        Update gal_mst_tdept set dept_name = ls_dept_name, dept_code = ls_dept_code,
						update_by = li_entity_gid, Update_date = now() where dept_isremoved = 'N' and dept_isactive = 'Y'
                        and dept_gid = li_dept_gid ;

		set countRow = (select found_rows());

		if countRow > 0 then
			set Message = 'SUCCESS';
			commit;
		else
			set Message = 'FAIL';
			rollback;
		end if;
	else
		set Message = ls_error;
	end if;

end if;

if Action = 'Delete' then

	if li_dept_gid = 0 then
		set ls_error = 'Department gid Not Given ';
	end if;

    if ls_error = '' then
		start transaction;

        Update gal_mst_tdept set dept_isremoved = 'Y', update_by = li_entity_gid, Update_date = now()
        where dept_isremoved = 'N' and dept_isactive = 'Y' and dept_gid = li_dept_gid ;

		set countRow = (select found_rows());

		if countRow > 0 then
			set Message = 'SUCCESS';
			commit;
		else
			set Message = 'FAIL';
			rollback;
		end if;
	else
		set Message = ls_error;
	end if;

end if;

if Action = 'Inactive' then

	if li_dept_gid = 0 then
		set ls_error = 'Department gid Not Given ';
	end if;

    if ls_error = '' then
		start transaction;

        Update gal_mst_tdept set dept_isactive = 'N', update_by = li_entity_gid, Update_date = now()
        where dept_isremoved = 'N' and dept_isactive = 'Y' and dept_gid = li_dept_gid ;

		set countRow = (select found_rows());

		if countRow > 0 then
			set Message = 'SUCCESS';
			commit;
		else
			set Message = 'FAIL';
			rollback;
		end if;
	else
		set Message = ls_error;
	end if;

end if;

if Action = 'active' then

	if li_dept_gid = 0 then
		set ls_error = 'Department gid Not Given ';
	end if;

    if ls_error = '' then
		start transaction;

        Update gal_mst_tdept set dept_isactive = 'Y', update_by = li_entity_gid, Update_date = now()
        where dept_isremoved = 'N' and dept_isactive = 'N' and dept_gid = li_dept_gid ;

		set countRow = (select found_rows());

		if countRow > 0 then
			set Message = 'SUCCESS';
			commit;
		else
			set Message = 'FAIL';
			rollback;
		end if;
	else
		set Message = ls_error;
	end if;

end if;

*/
END