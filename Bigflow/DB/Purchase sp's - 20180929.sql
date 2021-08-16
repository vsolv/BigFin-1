

 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_GRNApproval_Get` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_GRNApproval_Get`(IN `li_grnhdr_gid` int,IN `ls_sup_gid` int)
BEGIN

#Vigneshwari       16-12-2017

declare Query_search varchar(1000);
declare GRN_Headersrch Text;

set Query_search = '';
if li_grnhdr_gid <> '' then
	set Query_search = concat(' and grninwardheader_gid =' , li_grnhdr_gid); 
else
	set Query_search = '';
end if;

if ls_sup_gid <> '' then
	set Query_search = concat(Query_search , ' and supplier_gid =' , ls_sup_gid);
else
	set Query_search = concat(Query_search , '');
end if;

set GRN_Headersrch = ' 	select distinct grninwardheader_gid , supplier_gid ,
			grninwardheader_code , grninwardheader_dcnote , grninwardheader_invoiceno , sum(grninwarddetails_qty) as grninwarddetails_qty , supplier_name , 
            podetails_uom , poheader_no,grninwardheader_status
            from gal_trn_tgrninwardheader inner join gal_trn_tgrninwarddetails on grninwardheader_gid = grninwarddetails_grninwardheader_gid 
            left join gal_trn_tpoheader on grninwarddetails_poheader_gid = poheader_gid and poheader_isremoved = ''N''
            left join gal_trn_tpodetails on grninwarddetails_podetails_gid = podetails_gid and poheader_gid = podetails_poheader_gid and podetails_isremoved = ''N''
            left join gal_mst_tsupplier on poheader_supplier_gid = supplier_gid and supplier_isremoved = ''N''
            where grninwarddetails_isremoved = ''N'' and grninwardheader_isremoved = ''N'' and grninwardheader_isactive = ''Y'' 
            and grninwardheader_status = ''Pending for Approval''';

set @stmt = concat(GRN_Headersrch , Query_search , ' group by grninwardheader_gid ');
#select @stmt;
PREPARE stmt FROM @stmt;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_GRNApproval_Set` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_GRNApproval_Set`(IN `Action` varchar(16) , IN `li_GRNHdr_gid` int,
IN `ls_update_by` int ,IN `remarks` varchar(256) ,OUT `Message` varchar(128))
BEGIN

#Vigneshwari       16-12-2017

declare Qry_Header varchar(1000);
declare ls_error varchar(100);
declare countRow int;
declare errno int;

	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO;
    SELECT errno AS MYSQL_ERROR;
    set Message = errno;
    set Message = 'Error';
    ROLLBACK;
    END;

set ls_error = '';

if li_GRNHdr_gid = 0 then
	set ls_error = 'PR Header gid not given';
end if;

if ls_error = '' then
	if Action = 'Approve' then
		start transaction;
		update gal_trn_tgrninwardheader set grninwardheader_status = 'Approved' ,grninwardheader_remarks=remarks,update_by = ls_update_by , Update_date = now()
        where grninwardheader_gid = li_GRNHdr_gid and grninwardheader_isremoved  ='N';
                       
		set countRow = (select ROW_COUNT());

		if countRow >= 0 then
			set Message = 'Success';
			commit;
		else
			set Message = 'FAIL';
			rollback;
		end if;
    end if;
    
    if Action = 'Reject' then
		start transaction;
		update gal_trn_tgrninwardheader set grninwardheader_status = 'Rejected' ,grninwardheader_remarks=remarks, update_by = ls_update_by , Update_date = now()
        where grninwardheader_gid = li_GRNHdr_gid and grninwardheader_isremoved  ='N';
                       
		set countRow = (select ROW_COUNT());

		if countRow >= 0 then
			set Message = 'Success';
			commit;
		else
			set Message = 'FAIL';
			rollback;
		end if;
    end if;
else
	set Message = ls_error;
end if;
END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_GRNDelete_Set` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_GRNDelete_Set`(IN `li_GRNDet_gid` int ,
IN `ls_emp_gid` int, OUT `Message` varchar(100))
BEGIN

#Vigneshwari       01-12-2017

declare chk varchar(1000);
declare GRN_DelSrch varchar(1000);
declare countrow int;
declare ls_error varchar(100);
declare grndet_gid int;

set chk = '';
set ls_error = '';

if li_GRNDet_gid = 0 then
	set ls_error = ' GRN Detail Gid not Given. ';
end if;

if ls_emp_gid = 0 then
	set ls_error = ' Employee Gid not Given. ';
end if;

if ls_error = '' then

	select case when isnull(grninwarddetails_grninwardheader_gid) then 0 else grninwarddetails_grninwardheader_gid end into grndet_gid 
		from gal_trn_tgrninwarddetails where grninwarddetails_isremoved = 'N' and grninwarddetails_gid = li_GRNDet_gid;

	set @Srch = concat('select grninwarddetails_gid from gal_trn_tgrninwarddetails where grninwarddetails_isremoved = ''N'' 
						and grninwarddetails_grninwardheader_gid = ',grndet_gid);
	PREPARE stmtt FROM @Srch;
	EXECUTE stmtt ;
	set countrow = (select found_rows());
	DEALLOCATE PREPARE stmtt;
    
if countrow = 1 then

	start transaction;
    
        Update gal_trn_tgrninwarddetails set grninwarddetails_isremoved = 'Y' , update_by = ls_emp_gid , 
					 Update_date = now() where grninwarddetails_gid = li_GRNDet_gid;
    
	set GRN_DelSrch = concat('  Update gal_trn_tgrninwardheader set grninwardheader_isremoved = ''Y'' , update_by = ''' ,ls_emp_gid , 
					''' , Update_date = now() where grninwardheader_gid = ',grndet_gid );
    
	set @q = GRN_DelSrch;
	PREPARE stmtt FROM @q;
	EXECUTE stmtt ;
	set countrow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmtt;
	if countrow > 0 then
		set  Message = 'DELETION_DONE';
        commit;
	else
		set Message = 'NO_DELETION';
        rollback;
	end if;
else

	start transaction;
    
	set GRN_DelSrch = concat('  Update gal_trn_tgrninwarddetails set grninwarddetails_isremoved = ''Y'' , update_by = ''' ,ls_emp_gid , 
					''' , Update_date = now() where grninwarddetails_gid = ',li_GRNDet_gid );
	set @q = GRN_DelSrch;
	PREPARE stmtt FROM @q;
	EXECUTE stmtt ;
	set countrow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmtt;
	if countrow > 0 then
		set  Message = 'DELETION_DONE';
        commit;
	else
		set Message = 'NO_DELETION';
        rollback;
	end if;
end if;
else
	set Message = ls_error; 
end if;

END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_GRNDetail_Get` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_GRNDetail_Get`(IN `li_GRNHdr_gid` int,IN `ls_sup_gid` varchar(50),
OUT `Message` varchar(128))
BEGIN

#Vigneshwari       01-12-2017

declare Query_search varchar(1000);
declare GRN_Detailssrch text;
declare ls_error varchar(64);

set ls_error = '';

if li_grnhdr_gid <> 0 then
	set Query_search = concat(' and grninwardheader_gid = ' , li_grnhdr_gid);
else
	set ls_error = 'GRN Header No Not Given.';
end if;

if ls_sup_gid <> 0 then
	set Query_search = concat(Query_search , ' and supplier_gid = ' , ls_sup_gid );
else
	set Query_search = concat(Query_search , '');
end if;

if ls_error = '' then

	set GRN_Detailssrch = ' select grninwardheader_gid , grninwarddetails_gid ,grninwardheader_code, poheader_gid , podetails_gid , supplier_gid, 
							product_gid, poheader_no , product_name , supplier_name , product_code , podetails_uom ,uom_name, podelivery_godown_gid ,
                            grninwarddetails_qty ,sum(podelivery_qty) as podelivery_qty,grninwardheader_dcnote,grninwardheader_invoiceno,grninwardheader_date,grninwardheader_remarks from gal_trn_tgrninwardheader 
                            inner join gal_trn_tgrninwarddetails on grninwardheader_gid = grninwarddetails_grninwardheader_gid
                            left join gal_trn_tpoheader on grninwarddetails_poheader_gid = poheader_gid and poheader_isremoved = ''N''
                            left join gal_trn_tpodetails on grninwarddetails_podetails_gid = podetails_gid and podetails_isremoved = ''N''
                            left join gal_trn_tpodelivery on poheader_gid = podelivery_poheader_gid and podetails_gid = podelivery_podetails_gid and podelivery_isremoved = ''N''
                            left join gal_mst_tsupplier on poheader_supplier_gid = supplier_gid and supplier_isremoved = ''N''
                            left join gal_mst_tproduct on podetails_product_gid = product_gid and product_isremoved = ''N''
                            left join gal_mst_tuom on uom_gid=product_uom_gid and uom_isremoved=''N'' 
                            where grninwardheader_isremoved = ''N'' and grninwarddetails_isremoved = ''N'' and poheader_gid not in (select poclose_poheader_gid from gal_trn_tpoclose where poclose_status = ''Approved'') ';

	set @stmt = concat(GRN_Detailssrch , Query_search,' group by grninwardheader_gid,grninwarddetails_gid');
    #select @stmt;
	PREPARE stmt FROM @stmt;
	EXECUTE stmt;
	DEALLOCATE PREPARE stmt;
	set Message = 'done';
else
	set Message = ls_error ;
end if;
END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_GRNDetail_Set` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_GRNDetail_Set`(IN `Action` varchar(64),IN `li_GRNHeaderMAX_gid` int,
IN `li_GRNDetail_gid` int,IN `li_GRNpohdr_gid` int,IN `li_GRNpodtl_gid` int,IN `li_quantity` int,IN `li_godown_gid` int,
IN `li_entity_gid` int,IN `ls_create_by` int ,OUT `Message` varchar(128))
BEGIN

#Vigneshwari       30-11-2017

declare Qry_Header varchar(1000);
declare ls_error varchar(100);
declare countRow int;
declare errno int;
declare ls_no varchar(64);

	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO;
    SELECT errno AS MYSQL_ERROR;
    set Message = errno;
    ROLLBACK;
    END;

set ls_error = '';
if Action = 'Insert' then

if li_GRNHeaderMAX_gid = 0 or li_GRNHeaderMAX_gid = '' then
	set ls_error = 'GRN Header Not Selected.';
else 
	set @err = concat('select grninwardheader_gid from gal_trn_tgrninwardheader where grninwardheader_gid =''', li_GRNHeaderMAX_gid ,'''' , ' group by grninwardheader_gid' );
    PREPARE stmt1 FROM @err;
	EXECUTE stmt1;  
	set countRow = (select found_rows());
	DEALLOCATE PREPARE stmt1;
    if countRow <= 0 then
		set ls_error = 'GRN Header not found in Header';
	end if;
end if;

if li_quantity <= 0 then
	set ls_error = 'Quantity entered is not in correct form.';
end if;

if li_GRNpohdr_gid = 0 then
	set ls_error = 'PO Header gid  not given';
end if;

if li_GRNpodtl_gid = 0 then
	set ls_error = 'PO Detail gid  not given';
end if;

if ls_error = '' then
	start transaction;
	set Qry_Header = concat('INSERT INTO gal_trn_tgrninwarddetails(grninwarddetails_grninwardheader_gid, grninwarddetails_poheader_gid, 
						grninwarddetails_podetails_gid,grninwarddetails_qty, grninwarddetails_date, grninwarddetails_godownincharge_gid, 
						entity_gid, create_by) VALUES
                        (',li_GRNHeaderMAX_gid,',',li_GRNpohdr_gid,',',li_GRNpodtl_gid,',',li_quantity,',now(),
                        ',li_godown_gid,',',li_entity_gid,',',ls_create_by,')');
     select   Qry_Header;                
	set @Qry_Header = Qry_Header;
    PREPARE stmt FROM @Qry_Header;
	EXECUTE stmt;  
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt; 

	if countRow > 0 then
		select LAST_INSERT_ID() into Message ;
        set Message = CONCAT(Message,',SUCCESS');
        commit;
	else
		set Message = 'FAIL';
        rollback;
	end if;
else
	set Message = ls_error;
end if;
end if;

if Action = 'update' then

	if li_GRNDetail_gid = '' then
		set ls_error = 'GRN Header Gid not given';
	end if;
    
    	if li_quantity = '' then
		set ls_error = 'Quantity not given';
	end if;
    
    if ls_error = '' then
		start transaction;
        
        Update gal_trn_tgrninwarddetails set grninwarddetails_qty = li_quantity , update_by = li_entity_gid , 
					 Update_date = now() where grninwarddetails_gid = li_GRNDetail_gid;
	
		set countRow = (select found_rows());
	
		if countRow > 0 then
			set Message = ''',SUCCESS';
			commit;
		else
			set Message = 'FAIL';
			rollback;
		end if;
	else
		set Message = ls_error;
	end if;
    
end if;
END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_GRNHeaderUpdate_Set` */;
 
 CREATE DEFINER=`root`@`%` PROCEDURE `sp_GRNHeaderUpdate_Set`(IN `Action` varchar(16),IN `li_grnhdr_gid` int,
IN `li_date` datetime,IN `ls_Dc_no` varchar(64),IN `ls_inv_no` varchar(64),IN `ls_remarks` varchar(256),
OUT `Message` varchar(1000))
BEGIN

#Vigneshwari       30-11-2017

declare ls_error varchar(100);
declare countRow int;
declare errno int;
declare msg varchar(1000);

	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
    #SELECT errno AS MYSQL_ERROR;
    set Message = concat(errno , msg);
    set Message = 'Error';
    ROLLBACK;
    END;
    
if li_grnhdr_gid = 0  then
	set ls_error = 'GRN Header Gid not given';
end if;

#if li_date 


if Action = 'submit' then
		start transaction;
			Update gal_trn_tgrninwardheader set grninwardheader_status = 'Pending for Approval' ,grninwardheader_dcnote = ls_Dc_no,
            grninwardheader_invoiceno = ls_inv_no , grninwardheader_date = li_date , grninwardheader_remarks = ls_remarks 
            where grninwardheader_gid  = li_grnhdr_gid
				and grninwardheader_isremoved  ='N';

		set countRow = (select ROW_COUNT());
		if countRow >=  0 then
			set Message = '0,Success';
			commit;
		else
			set Message = 'FAIL';
			rollback;
		end if;
end if;

if Action = 'draft' then
		start transaction;
			Update gal_trn_tgrninwardheader set grninwardheader_status = 'Draft' ,grninwardheader_dcnote = ls_Dc_no,
            grninwardheader_invoiceno = ls_inv_no , grninwardheader_date = li_date , grninwardheader_remarks = ls_remarks
            where grninwardheader_gid  = li_grnhdr_gid
				and grninwardheader_isremoved  ='N';

		set countRow = (select ROW_COUNT());
		if countRow >=  0 then
			set Message = '0,Success';
			commit;
		else
			set Message = 'FAIL';
			rollback;
		end if;
end if;

END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_GRNHeader_Get` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_GRNHeader_Get`(IN `ls_no` varchar(16),IN `ls_gid` varchar(16),IN `li_sup_name` varchar(64))
BEGIN

#Vigneshwari       30-11-2017

declare Query_search varchar(1000);
declare GRN_Headersrch varchar(1000);

set Query_search = '';
if ls_no <> '' then
	set Query_search = concat(' and grninwardheader_code like ''%' , ls_no , '%'''); 
else
	set Query_search = '';
end if;


if ls_gid <> '' then
	set Query_search = concat(' and grninwardheader_gid = ''' , ls_gid , ''''); 
else
	set Query_search = '';
end if;

if li_sup_name <> '' then
	set Query_search = concat(Query_search , ' and supplier_name like ''%' , li_sup_name , '%''' );
else
	set Query_search = concat(Query_search , '');
end if;

set GRN_Headersrch = ' 	select distinct grninwardheader_gid , supplier_gid ,
			grninwardheader_code , grninwardheader_dcnote , grninwardheader_invoiceno , sum(grninwarddetails_qty) as grninwarddetails_qty , supplier_name , 
            podetails_uom , poheader_no , grninwardheader_status , grninwardheader_date,grninwardheader_remarks
            from gal_trn_tgrninwardheader inner join gal_trn_tgrninwarddetails on grninwardheader_gid = grninwarddetails_grninwardheader_gid 
            left join gal_trn_tpoheader on grninwarddetails_poheader_gid = poheader_gid and poheader_isremoved = ''N''
            left join gal_trn_tpodetails on grninwarddetails_podetails_gid = podetails_gid and poheader_gid = podetails_poheader_gid and podetails_isremoved = ''N''
            left join gal_mst_tsupplier on poheader_supplier_gid = supplier_gid and supplier_isremoved = ''N''
            where grninwarddetails_isremoved = ''N'' and grninwardheader_isremoved = ''N'' and grninwardheader_isactive = ''Y'' ';

set @stmt = concat(GRN_Headersrch , Query_search , ' group by grninwardheader_gid order by grninwardheader_gid desc');
#select @stmt;
PREPARE stmt FROM @stmt;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_GRNHeader_Set` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_GRNHeader_Set`(IN `Action` varchar(16),IN `li_date` datetime,
IN `ls_Dc_no` varchar(64),IN `ls_inv_no` varchar(64),IN `ls_remarks` varchar(256),IN `li_entity_gid` int,
IN `ls_create_by` int,OUT `Message` varchar(128))
BEGIN

#Vigneshwari       30-11-2017

declare Qry_Header varchar(1000);
declare ls_error varchar(100);
declare countRow int;
declare errno int;
declare ls_no varchar(64);

	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO;
    SELECT errno AS MYSQL_ERROR;
    set Message = errno;
    ROLLBACK;
    END;

set ls_error = '';


call sp_Generate_number_get('GRN','000',@Message);
select @Message into ls_no from dual;

if ls_no = '' then
	set ls_error = ' GRN Header Code not Given. ';
else 
	set @err = concat('select * from gal_trn_tgrninwardheader where grninwardheader_code =''', ls_no ,'''' , ' group by grninwardheader_code' );
    #select @err;
    PREPARE stmt1 FROM @err;
	EXECUTE stmt1;  
	set countRow = (select found_rows());
	DEALLOCATE PREPARE stmt1;
    if countRow > 0 then
		set ls_error = ' Duplicate GRN Header Code ';
    end if;
end if;

if li_date = 0 then
	set ls_error = ' GRN Header Date Not Given. ';
end if;

if ls_Dc_no = '' then
	set ls_error = ' DC No not Given. ';
end if;

if ls_inv_no = '' then
	set ls_error = ' Invoice No not Given. ';
end if;

if ls_remarks = '' then
	set ls_error = ' Remarks not Given. ';
end if;

if ls_error = '' then
if Action = 'submit' then
	start transaction;
	set Qry_Header = concat('INSERT INTO gal_trn_tgrninwardheader(grninwardheader_code , grninwardheader_dcnote , grninwardheader_invoiceno , 
							grninwardheader_date , grninwardheader_status , grninwardheader_remarks , entity_gid , create_by) VALUES 
                            (''' , ls_no , ''',''' , ls_Dc_no , ''',''' , ls_inv_no , ''',''' , li_date , ''',''Pending for Approval''
                            ,''' , ls_remarks , ''',' , li_entity_gid , ',' , ls_create_by , ')');
#select Qry_Header;
	set @Qry_Header = Qry_Header;
	PREPARE stmt FROM @Qry_Header;
	EXECUTE stmt;  
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt; 

	if countRow >  0 then
		select LAST_INSERT_ID() into Message ;
        set Message = CONCAT(Message,',SUCCESS');
		commit;
	else
		set Message = 'FAIL';
        rollback;
	end if;
end if;

if Action = 'draft' then
	start transaction;
	set Qry_Header = concat('INSERT INTO gal_trn_tgrninwardheader(grninwardheader_code , grninwardheader_dcnote , grninwardheader_invoiceno , 
							grninwardheader_date , grninwardheader_status ,grninwardheader_remarks, entity_gid , create_by) VALUES 
                            (''' , ls_no , ''',''' , ls_Dc_no , ''',''' , ls_inv_no , ''',''' , li_date , ''',''Draft''
                            ,''' , ls_remarks , ''',' , li_entity_gid , ',' , ls_create_by , ')');

	set @Qry_Header = Qry_Header;
	PREPARE stmt FROM @Qry_Header;
	EXECUTE stmt;  
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt; 

	if countRow >  0 then
		select LAST_INSERT_ID() into Message ;
        set Message = CONCAT(Message,',SUCCESS');
		commit;
	else
		set Message = 'FAIL';
        rollback;
	end if;
end if;

if Action = 'request' then
	start transaction;
	set Qry_Header = concat('INSERT INTO gal_trn_tgrninwardheader(grninwardheader_code , grninwardheader_dcnote , grninwardheader_invoiceno , 
							grninwardheader_date , grninwardheader_status ,grninwardheader_remarks, entity_gid , create_by) VALUES 
                            (''' , ls_no , ''',''' , ls_Dc_no , ''',''' , ls_inv_no , ''',''' , li_date , ''',''Pending for Approval''
                            ,''' , ls_remarks , ''',' , li_entity_gid , ',' , ls_create_by , ')');

	set @Qry_Header = Qry_Header;
	PREPARE stmt FROM @Qry_Header;
	EXECUTE stmt;  
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt; 

	if countRow >  0 then
		select LAST_INSERT_ID() into Message ;
        set Message = CONCAT(Message,',SUCCESS');
		commit;
	else
		set Message = 'FAIL';
        rollback;
	end if;
end if;
else
	set Message = ls_error;
end if;

END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_GRNQtyList_Get` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_GRNQtyList_Get`(IN `li_grnhdr_gid` int,IN `ls_sup_gid` int,
OUT `Message` varchar(128))
BEGIN

#Vigneshwari       13-12-2017

declare Query_search varchar(1000);
declare GRN_Qtysrch text;
declare ls_error varchar(64);

set ls_error = '';
set Query_search = '';
set @stmt = '';
/*
if li_grnhdr_gid <> 0 then
	set Query_search = concat(' and grninwardheader_gid = ' , li_grnhdr_gid);
else
	set ls_error = 'GRN Header gid not given';
end if;
*/
if ls_sup_gid <> 0 then
	set Query_search = concat(Query_search , ' and supplier_gid = ' , ls_sup_gid );
else
	set Query_search = concat(Query_search , '');
end if;

if ls_error = '' then

	set GRN_Qtysrch = concat(' select poheader_gid , podetails_gid , podetails_product_gid ,podelivery_godown_gid ,supplier_gid ,uom_name, 
						grninwarddetails_gid,podetails_uom,supplier_name,poheader_no,product_name,product_code ,poheader_date, 
                        case when isnull(podetails_qty) then 0 else podetails_qty end as total_qty,
                        case when isnull(podelivery_qty) then 0 else sum(podelivery_qty) end as dlvry_qty ,
                        case when isnull(grninwarddetails_qty) then 0 else sum(grninwarddetails_qty) end as allreceive_qty,
                        ''0'' as current_qty,case when isnull(podelivery_qty) then 0 else (podelivery_qty) end - 
                        case when isnull(grninwarddetails_qty) then 0 else sum(grninwarddetails_qty) end as rem_qty
                        FROM gal_trn_tpoheader 
                        inner join gal_trn_tpodetails on poheader_gid = podetails_poheader_gid
                        left join gal_trn_tpodelivery on podetails_gid = podelivery_podetails_gid and podelivery_isremoved = ''N''
                        left join gal_trn_tgrninwarddetails on podelivery_podetails_gid = grninwarddetails_podetails_gid and grninwarddetails_isremoved = ''N''
                        left join gal_mst_tproduct on podetails_product_gid = product_gid and product_isremoved = ''N''
                        left join gal_mst_tsupplier on poheader_supplier_gid = supplier_gid and supplier_isremoved = ''N''
                        left join gal_mst_tuom on uom_gid = product_uom_gid and uom_isremoved = ''N'' and uom_isactive = ''Y''
                        where poheader_isremoved = ''N'' and poheader_isactive = ''Y'' and podetails_isremoved = ''N''
                        and poheader_status in (''Approved'',''REOPENED'')
                        and poheader_gid not in (select poclose_poheader_gid from gal_trn_tpoclose where poclose_isremoved = ''N''
                        and poclose_isactive = ''Y'')
                        
                         ', Query_search ,'
                        group by podetails_product_gid,poheader_gid
						 having rem_qty > 0');
#and poheader_status = ''Approved''
	if li_grnhdr_gid <> 0 then
		set @stmt = concat('select main.poheader_gid , main.podetails_gid , main.podetails_product_gid ,main.podelivery_godown_gid ,main.uom_name,
						main.supplier_gid ,main.grninwarddetails_gid, main.podetails_uom,main.supplier_name,main.poheader_no,main.poheader_date,
                        main.product_name,main.product_code ,main.total_qty,main.dlvry_qty ,main.allreceive_qty,main. rem_qty,
                        a.grninwarddetails_qty as current_qty
                        from (' ,GRN_Qtysrch , ') as main
						left join gal_trn_tgrninwarddetails as a on main.grninwarddetails_gid = a.grninwarddetails_gid
						and grninwarddetails_grninwardheader_gid = ' , li_grnhdr_gid );
	else
		set @stmt = concat(GRN_Qtysrch);
    end if;
    #select @stmt;
	PREPARE stmt FROM @stmt;
	EXECUTE stmt;
	DEALLOCATE PREPARE stmt;
	set Message = 'done';
else
	set Message = ls_error ;
end if;
END ;;

 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_POAmendApproval_Get` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_POAmendApproval_Get`(IN `ls_POAmd_no` varchar(50),IN `ls_POAmd_status` varchar(50))
BEGIN

#Vigneshwari       25-11-2017

declare Query_search varchar(1000);
declare POAmd_Headersrch varchar(1000);

if ls_POAmd_status <> '' then
	set Query_search = concat(' and poheader_status like ''%' , ls_POAmd_status , '%''');
else
	set Query_search = '';
end if;

if ls_POAmd_no <> '' then
	set Query_search = concat(Query_search , ' and poheader_no like ''%' , ls_POAmd_no , '%''');
else
	set Query_search = concat(Query_search , '');
end if;

set POAmd_Headersrch = ' select distinct poheader_gid , poheader_no , poheader_date , employee_name , poheader_status 
				from gal_trn_tpoheader inner join gal_trn_tpodetails on poheader_gid = podetails_poheader_gid
                left join gal_mst_temployee on employee_gid = poheader_employee_gid and employee_isremoved = ''N''
				where poheader_isremoved = ''N'' and poheader_isactive = ''Y''and podetails_isremoved = ''N'' 
                and poheader_amendment = ''Y'' and poheader_status = ''Pending for Approval'' ';

set @stmt = concat(POAmd_Headersrch , Query_search);

PREPARE stmt FROM @stmt;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_POAmendApproval_Set` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_POAmendApproval_Set`(IN `Action` varchar(16) , IN `li_POAmdHeader_gid` int,
IN `ls_update_by` int ,OUT `Message` varchar(128))
BEGIN

#Vigneshwari       27-11-2017

declare Qry_Header varchar(1000);
declare ls_error varchar(100);
declare countRow int;
declare errno int;

	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO;
    SELECT errno AS MYSQL_ERROR;
    set Message = errno;
    set Message = 'Error';
    ROLLBACK;
    END;

set ls_error = '';

if li_POAmdHeader_gid = 0 then
	set ls_error = 'PR Header gid not given';
end if;

if ls_error = '' then
	if Action = 'Approve' then
		start transaction;
		update gal_trn_tpoamendheader set poamendheader_status = 'Approved' , update_by = ls_update_by , Update_date = now()
        where poamendheader_gid = li_POAmdHeader_gid and poamendheader_isremoved  ='N';
                       
		set countRow = (select ROW_COUNT());

		if countRow >= 0 then
			set Message = 'Success';
			commit;
		else
			set Message = 'FAIL';
			rollback;
		end if;
    end if;
    
    if Action = 'Reject' then
		start transaction;
		update gal_trn_tpoamendheader set poamendheader_status = 'Rejected' , update_by = ls_update_by , Update_date = now()
        where poamendheader_gid = li_POAmdHeader_gid and poamendheader_isremoved  ='N';
                       
		set countRow = (select ROW_COUNT());

		if countRow >= 0 then
			set Message = 'Success';
			commit;
		else
			set Message = 'FAIL';
			rollback;
		end if;
    end if;
else
	set Message = ls_error;
end if;
END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_POAmendDelete_Set` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_POAmendDelete_Set`(IN `li_POAmdDet_gid` int ,
IN `ls_emp_gid` int, OUT `Message` varchar(100))
BEGIN

#Vigneshwari       24-11-2017

declare chk varchar(1000);
declare POAmd_DelSrch varchar(1000);
declare countrow int;
declare ls_error varchar(100);
declare poamddet_gid int;

set chk = '';
set ls_error = '';

if li_POAmdDet_gid = 0 then
	set ls_error = ' PO Amendment Detail Gid not Given. ';
end if;

if ls_emp_gid = 0 then
	set ls_error = ' Employee Gid not Given. ';
end if;

if ls_error = '' then

	select case when isnull(poamenddetails_poamendheader_gid) then 0 else poamenddetails_poamendheader_gid end into poamddet_gid 
		from gal_trn_tpoamenddetails where poamenddetails_isremoved = 'N' and poamenddetails_gid = li_POAmdDet_gid;

	set @Srch = concat('select poamenddetails_gid from gal_trn_tpoamenddetails where poamenddetails_isremoved = ''N'' 
						and poamenddetails_poamendheader_gid =', poamddet_gid);
	PREPARE stmtt FROM @Srch;
	EXECUTE stmtt ;
	set countrow = (select found_rows());
	DEALLOCATE PREPARE stmtt;
    
if countrow = 1 then

	start transaction;
    
        Update gal_trn_tpoamenddetails set poamenddetails_isremoved = 'Y' , update_by = ls_emp_gid , 
					 Update_date = now() where poamenddetails_gid = li_POAmdDet_gid;
    
	set POAmd_DelSrch = concat('  Update gal_trn_tpoamendheader set poamendheader_isremoved = ''Y'' , update_by = ''' ,ls_emp_gid , 
					''' , Update_date = now() where poamendheader_gid = ',poamddet_gid );
    
	set @q = POAmd_DelSrch;
	PREPARE stmtt FROM @q;
	EXECUTE stmtt ;
	set countrow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmtt;
	if countrow > 0 then
		set  Message = 'DELETION_DONE';
        commit;
	else
		set Message = 'NO_DELETION';
        rollback;
	end if;
else

	start transaction;
    
	set POAmd_DelSrch = concat('  Update gal_trn_tpoamenddetails set poamenddetails_isremoved = ''Y'' , update_by = ''' ,ls_emp_gid , 
					''' , Update_date = now() where poamenddetails_gid = ',li_POAmdDet_gid );
	set @q = POAmd_DelSrch;
	PREPARE stmtt FROM @q;
	EXECUTE stmtt ;
	set countrow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmtt;
	if countrow > 0 then
		set  Message = 'DELETION_DONE';
        commit;
	else
		set Message = 'NO_DELETION';
        rollback;
	end if;
end if;
else
	set Message = ls_error; 
end if;

END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_POAmendDelivery_Get` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_POAmendDelivery_Get`(IN `ls_no` varchar(64),OUT `Message` varchar(128))
BEGIN

#Vigneshwari       28-11-2017

declare Query_search varchar(1000);
declare POAmd_Headersrch varchar(1000);
declare ls_error varchar(64);

set ls_error ='';

if ls_no <> '' then
	set Query_search = concat(' and poamenddelivery_gid =' , ls_no ); 
else
	set Query_search = '';
	set ls_error = 'PO Delivery Not Selected';
end if;

if ls_error = '' then
set POAmd_Headersrch = ' 	select poamenddelivery_gid , poamenddelivery_poamendheader_gid , poamenddelivery_poamenddetails_gid , godown_name ,
						employee_name , address_1 , uom_name , podelivery_qty
                        from gal_trn_tpoamenddelivery inner join gal_mst_tgodown on podelivery_godown_gid = godown_gid 
                        left join gal_mst_taddress on godown_address_gid = address_gid 
                        left join gal_mst_tproduct on podelivery_product_gid = product_gid and product_isremoved = ''N'' and product_isactive = ''Y''
                        left join gal_mst_tuom on product_uom_gid = uom_gid and uom_isremoved = ''N'' and uom_isactive = ''Y''
                        left join gal_mst_temployee on godown_inchage_gid = employee_gid and employee_isremoved = ''N''
                        where poamenddelivery_isremoved = ''N'' and godown_isremoved = ''N'' and godown_isactive = ''Y'' ';

set @stmt = concat(POAmd_Headersrch , Query_search);
PREPARE stmt FROM @stmt;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

set Message = 'done';
else

set Message = ls_error ;

end if;

END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_POAmendDelivery_Set` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_POAmendDelivery_Set`(IN `li_POAmdHeader_gid` int,IN `li_POAmdDetail_gid` int,
IN `li_product_gid` int,IN `li_quantity` int,IN `li_godown_gid` int,IN `li_entity_gid` int,IN `ls_create_by` int ,OUT `Message` varchar(128))
BEGIN

#Vigneshwari       28-11-2017

declare Qry_Header varchar(1000);
declare ls_error varchar(100);
declare countRow int;
declare errno int;

	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO;
    SELECT errno AS MYSQL_ERROR;
    set Message = errno;
    ROLLBACK;
    END;

set ls_error = '';
/*
if li_POAmdHeader_gid = 0 or li_POAmdHeader_gid = '' then
	set ls_error = 'PO Header Not Selected.';
else 
	set @err = concat('select * from gal_trn_tpoheader where poheader_gid =''', li_POAmdHeader_gid ,''' group by poheader_gid' );
    PREPARE stmt1 FROM @err;
	EXECUTE stmt1;  
	set countRow = (select found_rows());
	DEALLOCATE PREPARE stmt1;
    if countRow <= 0 then
		set ls_error = 'PO Header No not found in Header';
	end if;
end if;

if li_POAmdDetail_gid = 0 or li_POAmdDetail_gid = '' then
	set ls_error = 'PO Detail Not Selected.';
else 
	set @err = concat('select * from gal_trn_tpodetails where podetails_gid =''', li_PODetail_gid ,''' group by podetails_gid' );
    PREPARE stmt1 FROM @err;
	EXECUTE stmt1;  
	set countRow = (select found_rows());
	DEALLOCATE PREPARE stmt1;
    if countRow <= 0 then
		set ls_error = 'PO detail No not found in Detail';
	end if;
end if;

if li_product_gid = 0 then
	set ls_error = 'Product Not Selected.';
end if;

if li_quantity <= 0 then
	set ls_error = 'Quantity entered is Not in correct form.';
end if;

if li_godown_gid = 0 then
	set ls_error = 'Godown Name Not Selected.';
end if;
*/
if ls_error = '' then
	start transaction;
	set Qry_Header = concat('INSERT INTO gal_trn_tpodelivery(podelivery_poheader_gid, podelivery_podetails_gid, 
						podelivery_product_gid, podelivery_qty,podelivery_godown_gid,entity_gid, create_by) VALUES
                        (',li_POAmdHeader_gid,',',li_POAmdDetail_gid,',',li_product_gid,',',li_quantity,',',li_godown_gid,
                        ',',li_entity_gid,',',ls_create_by,')');
                  
	set @Qry_Header = Qry_Header;
    PREPARE stmt FROM @Qry_Header;
	EXECUTE stmt;  
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt; 

	if countRow > 0 then
		select LAST_INSERT_ID() into Message ;
        commit;
	else
		set Message = 'FAIL';
        rollback;
	end if;
else
	set Message = ls_error;
end if;





END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_POAmendDetailUpdate_Set` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_POAmendDetailUpdate_Set`(IN `li_POAmdDtil_gid` int,
IN `li_prod_gid` int,IN `li_qty` int,OUT `Message` varchar(100))
BEGIN

#Vigneshwari       17-11-2017

declare Qry_Header varchar(1000);
declare countRow int;
declare ls_error varchar(100);
declare errno int;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO;
    SELECT errno AS MYSQL_ERROR;
    set Message = errno;
    ROLLBACK;
    END;

set ls_error = '';
if li_POAmdDtil_gid = 0 then
	set ls_error = 'PO Amendment Details Data Not Passed.';
end if;

if li_qty = 0 then
	set ls_error = 'Quantity Not Correct.';
end if;

if li_prod_gid = 0 then
	set ls_error = 'Product Not Selected.';
end if;

if ls_error = '' then
	start transaction;

	Update gal_trn_tpoamenddetails set poamenddetails_qty = li_qty , poamenddetails_product_gid = li_prod_gid
	where poamenddetails_gid  = li_POAmdDtil_gid and poamenddetails_isremoved  ='N';

	set countRow = (select ROW_COUNT()) ;
	set Message = countRow;

	if countRow = 1 then
		set Message = 'SUCCESS';
		commit;
	else 
		set Message = 'NO CHANGE';
        rollback;
	end if;
else
	set Message = ls_error;
end if;
END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_POAmendDetail_Get` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_POAmendDetail_Get`(IN `li_poamddetail_gid` int,IN `ls_prod_name` varchar(50),IN `li_emp_gid` int,
OUT `Message` varchar(128))
BEGIN

#Vigneshwari       24-11-2017

declare Query_search varchar(1000);
declare POAmd_Detailssrch varchar(1000);
declare ls_error varchar(64);

set ls_error = '';

if li_poamddetail_gid <> 0 then
	set Query_search = concat(' and podetails_gid = ' , li_poamddetail_gid);
else
	set ls_error = 'PO Detail Not Given.';
end if;

if ls_prod_name <> '' then
	set Query_search = concat(Query_search , ' and product_name like ''%' , ls_prod_name , '%''');
else
	set Query_search = concat(Query_search , '');
end if;

if li_emp_gid <> 0 then
	set Query_search = concat(Query_search , ' and a.create_by = ' , li_emp_gid);
else
	set Query_search = concat(Query_search , '');
end if;

if ls_error = '' then

	set POAmd_Detailssrch = 'select productcategory_name ,producttype_name ,product_name ,uom_name ,podetails_qty ,
		case 
			when avg(supplierproduct_unitprice) is null then 0 
		else  
			round(avg(supplierproduct_unitprice),2) 
		end as prod_price ,
		product_gid , producttype_gid , productcategory_gid , poamendheader_gid , poamenddetails_gid 
		from gal_trn_tpoamendheader as a 
		inner join gal_trn_tpoamenddetails on poamendheader_gid = poamenddetails_poamendheader_gid 
		left join gal_mst_tproduct on poamenddetails_product_gid = product_gid and product_isremoved = ''N''
		left join gal_mst_tproducttype on product_producttype_gid = producttype_gid and producttype_isremoved = ''N''
		left join gal_mst_tproductcategory on producttype_productcategory_gid = productcategory_gid and product_isremoved = ''N''
		left join gal_mst_tuom on product_uom_gid = uom_gid and uom_isremoved = ''N''
		left join gal_map_tsupplierproduct on product_gid = supplierproduct_product_gid and supplierproduct_isremoved = ''N''
		where poamendheader_isremoved = ''N'' and poamendheader_isactive = ''Y'' and poamenddetails_isremoved = ''N''
		group by supplierproduct_product_gid';

	set @stmt = concat(POAmd_Detailssrch , Query_search);
	PREPARE stmt FROM @stmt;
	EXECUTE stmt;
	DEALLOCATE PREPARE stmt;
	set Message = 'done';
else
	set Message = ls_error ;
end if;
END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_POAmendDetail_Set` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_POAmendDetail_Set`(IN `li_POAmdHeaderMAX_gid` int,
IN `li_product_gid` int,IN `li_quantity` int,IN `li_entity_gid` int,IN `ls_create_by` int ,OUT `Message` varchar(128))
BEGIN

#Vigneshwari       24-11-2017

declare Qry_Header varchar(1000);
declare ls_error varchar(100);
declare countRow int;
declare errno int;

	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO;
    SELECT errno AS MYSQL_ERROR;
    set Message = errno;
    ROLLBACK;
    END;

set ls_error = '';

if li_POAmdHeaderMAX_gid = 0 or li_POAmdHeaderMAX_gid = '' then
	set ls_error = 'PO Amendment Header Not Selected.';
else 
	set @err = concat('select * from gal_trn_tpoamendheader where poamendheader_gid =''', li_POAmdHeaderMAX_gid ,'''' , 
						' group by poamendheader_gid' );
    PREPARE stmt1 FROM @err;
	EXECUTE stmt1;  
	set countRow = (select found_rows());
	DEALLOCATE PREPARE stmt1;
    if countRow <= 0 then
		set ls_error = 'PO Amendment Header No not found in Header';
	end if;
end if;

if li_product_gid = 0 then
	set ls_error = 'Product Not Selected.';
end if;

if li_quantity <= 0 then
	set ls_error = 'Quantity entered is not in correct form.';
end if;
if ls_error = '' then
	start transaction;
	set Qry_Header = concat('INSERT INTO gal_trn_tpoamenddetails(poamenddetails_poamendheader_gid, poamenddetails_product_gid, 
						poamenddetails_qty, entity_gid, create_by) VALUES
                        (',li_POAmdHeaderMAX_gid,',',li_product_gid,',',li_quantity,',',li_entity_gid,',',ls_create_by,')');
                       
	set @Qry_Header = Qry_Header;
    PREPARE stmt FROM @Qry_Header;
	EXECUTE stmt;  
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt; 

	if countRow > 0 then
		select LAST_INSERT_ID() into Message ;
        set Message = CONCAT(Message,',SUCCESS');
        commit;
	else
		set Message = 'FAIL';
        rollback;
	end if;
else
	set Message = ls_error;
end if;
END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_POAmendHeaderUpdate_Set` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_POAmendHeaderUpdate_Set`(IN `Action` varchar(16),IN `li_poamdhdr_gid` int,
OUT `Message` varchar(1000))
BEGIN

#Vigneshwari       24-11-2017

declare ls_error varchar(100);
declare countRow int;
declare errno int;
declare msg varchar(1000);

	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
    #SELECT errno AS MYSQL_ERROR;
    set Message = concat(errno , msg);
    set Message = 'Error';
    ROLLBACK;
    END;

if Action = 'submit' then
		start transaction;
			Update gal_trn_tpoamendheader set poamendheader_status = 'Pending for Approval' where poamendheader_gid  = li_poamdhdr_gid
				and poamendheader_isremoved  ='N';

		set countRow = (select ROW_COUNT());
		if countRow >=  0 then
			set Message = 'Success';
			commit;
		else
			set Message = 'FAIL';
			rollback;
		end if;
end if;

if Action = 'draft' then
		start transaction;
			Update gal_trn_tpoamendheader set poamendheader_status = 'Draft' where poamendheader_gid  = li_poamdhdr_gid
				and poamendheader_isremoved  ='N';

		set countRow = (select ROW_COUNT());
		if countRow >=  0 then
			set Message = 'Success';
			commit;
		else
			set Message = 'FAIL';
			rollback;
		end if;
end if;

END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_POAmendHeader_Get` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_POAmendHeader_Get`(IN `ls_no` varchar(64),IN `li_sup_name` varchar(64),
IN `ld_amnt` decimal,IN `ls_status` varchar(50),IN `li_emp_gid` int)
BEGIN

#Vigneshwari       14-12-2017

declare Query_search varchar(1000);
declare PO_Headersrch varchar(1000);

set Query_search = '';
if ls_no <> '' then
	set Query_search = concat(' and poheader_no like ''%' , ls_no , '%'''); 
else
	set Query_search = '';
end if;

if li_sup_name <> '' then
	set Query_search = concat(Query_search , ' and supplier_name like ''%' , li_sup_name , '%''' );
else
	set Query_search = concat(Query_search , '');
end if;

if ld_amnt <> 0.00  and ld_amnt <> 0 then
	set Query_search = concat(Query_search , ' and poheader_amount like ''%' , ld_amnt  , '%''');
else
	set Query_search = concat(Query_search , '');
end if;

if ls_status <> '' then
	set Query_search = concat(Query_search , ' and poheader_status like ''%' , ls_status , '%''');
else
	set Query_search = concat(Query_search , '');
end if;

if li_emp_gid <> 0 then
	set Query_search = concat(Query_search , ' and a.create_by = ' , li_emp_gid);
else
	set Query_search = concat(Query_search , '');
end if;

set PO_Headersrch = ' 	select distinct poheader_gid , poheader_no , poheader_date , poheader_amount , poheader_status ,supplier_name
						from gal_trn_tpoheader as a inner join gal_trn_tpodetails on poheader_gid = podetails_poheader_gid
                        left join gal_mst_tsupplier on poheader_supplier_gid = supplier_gid and supplier_isremoved = ''N''
                        where poheader_isactive = ''Y'' and poheader_isremoved = ''N'' and podetails_isremoved = ''N'' 
                        and poheader_status = ''Approved'' and poheader_close = ''N'' and poheader_cancel = ''N'' 
						and poheader_gid not in (select grninwarddetails_poheader_gid from gal_trn_tgrninwardheader 
                        inner join gal_trn_tgrninwarddetails on grninwardheader_gid = grninwarddetails_grninwardheader_gid 
                        where grninwardheader_isremoved = ''N'') ';

set @stmt = concat(PO_Headersrch , Query_search);
PREPARE stmt FROM @stmt;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_POAmendHeader_Set` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_POAmendHeader_Set`(IN `Action` varchar(16),IN `li_pohdr_gid` int,
IN `li_entity_gid` int,IN `ls_create_by` int,OUT `Message` varchar(128))
BEGIN

#Vigneshwari       24-11-2017

declare Qry_Header text;
declare Qry_Detail text;
declare Qry_Deliery text;
declare ls_error varchar(100);
declare countRow int;
declare errno int;
declare ls_no varchar(64);


	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO;
    SELECT errno AS MYSQL_ERROR;
    set Message = errno;
    ROLLBACK;
    END;

set ls_error = '';
set @poamend_hdr = '';
set @poamend_det = '';

if li_pohdr_gid = 0 then
	set ls_error = 'PO Header Gid Not Given';
end if;

if ls_error = '' then
if Action = 'submit' then
	start transaction;
	set Qry_Header = concat('INSERT INTO gal_trn_tpoamendheader(poamendheader_no , poamendheader_date , poamendheader_supplier_gid , 
							poamendheader_poterms_gid , poamendheader_amount , poamendheader_amendment , poamendheader_version , 
                            poamendheader_status , poamendheader_remarks , poamendheader_close , poamendheader_cancel ,
                            entity_gid , create_by)
                            (select poheader_no , poheader_date , poheader_supplier_gid , poheader_poterms_gid , poheader_amount , poheader_amendment , poheader_version ,
							poheader_status , poheader_remarks , poheader_close , poheader_cancel ,' , li_entity_gid , ',' 
                            , ls_create_by , ' from gal_trn_tpoheader where poheader_isremoved = ''N'' 
                            and poheader_gid = ' , li_pohdr_gid , ' )');

	set @Qry_Header = Qry_Header;
    #select @Qry_Header;
	PREPARE stmt FROM @Qry_Header;
	EXECUTE stmt;  
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt; 

	if countRow >  0 then
		select LAST_INSERT_ID() into @poamend_hdr ;
        
        set Qry_Detail = concat('INSERT INTO gal_trn_tpoamenddetail(poamenddetail_poamendheader_gid, poamenddetail_product_gid, 
								poamenddetail_qty,poamenddetail_uom, poamenddetail_unitprice, poamenddetail_amount, 
                                poamenddetail_taxamount, poamenddetail_totalamount, poamenddetail_remarks, entity_gid, 
                                create_by) 
                                (select ' , @poamend_hdr , ' , podetails_product_gid , podetails_qty , podetails_uom , 
                                podetails_unitprice , podetails_amount , podetails_taxamount , podetails_totalamount , 
                                podetails_remarks ,' , li_entity_gid , ',' , ls_create_by , '
                                from gal_trn_tpodetails where podetails_isremoved = ''N'' 
                                and podetails_poheader_gid = ' , li_pohdr_gid , ' )');
        
		set @Qry_Detail = Qry_Detail;
		#select @Qry_Detail;
        PREPARE stmt FROM @Qry_Detail;
		EXECUTE stmt;  
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt; 

		if countRow >  0 then
			select LAST_INSERT_ID() into @poamend_det;
            
            set Qry_Deliery = concat(' INSERT INTO gal_trn_tpoamenddelivery(poamenddelivery_poamendheader_gid, 
										poamenddelivery_poamenddetail_gid, poamenddelivery_product_gid, poamenddelivery_qty, 
                                        poamenddelivery_godown_gid, poamenddelivery_remarks, entity_gid, create_by) 
                                        (select podelivery_poheader_gid , podelivery_podetails_gid , podelivery_product_gid , 
                                        podelivery_qty , podelivery_godown_gid , podelivery_remarks ,' , li_entity_gid , ',' 
                                        , ls_create_by , '
                                        from gal_trn_tpodelivery where podelivery_isremoved = ''N'' 
                                        and podelivery_poheader_gid = ' , li_pohdr_gid , ') ');

			set @Qry_Deliery = Qry_Deliery;	
			#select @Qry_Deliery;
            PREPARE stmt FROM @Qry_Deliery;
			EXECUTE stmt;  
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt; 

			if countRow >  0 then
				select LAST_INSERT_ID() into Message;
                set Message = CONCAT(Message,',SUCCESS');
                #set Message = 'SUCCESS';
				commit;
			else
				set Message = 'FAIL';
				rollback;
			end if;
		else
			set Message = 'FAIL';
			rollback;
		end if;
	else
		set Message = 'FAIL';
		rollback;
    end if;
end if;
else
	set Message = ls_error;
end if;

END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_POApprovalView_Update_set` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_POApprovalView_Update_set`(IN `Action` varchar(64),IN `Actionsts` varchar(64),
IN `li_POHdr_gid` int,IN `ls_remarks` varchar(256),IN `ls_update_by` int ,OUT `Message` varchar(128))
BEGIN

#Vigneshwari       11-12-2017

declare Qry_Header varchar(1000);
declare countRow int;
declare countRow1 int;
declare ls_error varchar(100);
declare errno int;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO;
    SELECT errno AS MYSQL_ERROR;
    set Message = errno;
    ROLLBACK;
    END;

set ls_error = '';
if li_POHdr_gid = 0 then
	set ls_error = 'PO Header Data Not Passed.';
end if;

if Actionsts = 'Reject' then
	if ls_remarks = '' then
		set ls_error = 'Remarks not given';
	end if;
end if;
	
    SET SQL_SAFE_UPDATES = 0;
    
if Action ='close' then
	if ls_error = '' then
    
    if Actionsts = 'Approve' then
		start transaction;
               
		update gal_trn_tpoclose set poclose_status = 'Approved' , update_by = ls_update_by , Update_date = now()
        where poclose_poheader_gid = li_POHdr_gid and poclose_isremoved  ='N' and poclose_isactive = 'Y';
                       
		set countRow = (select found_rows());
		if countRow > 0 then
        
			Update gal_trn_tpoheader set poheader_close = 'Y' where poheader_gid  = li_POHdr_gid;

			set countRow = (select found_rows()) ;
			if countRow = 1 then
				set Message = 'Success';
				commit;
			else
				set Message = 'FAIL';
				rollback;
			end if;
        end if;
    end if;
    
    if Actionsts = 'Reject' then
    
		start transaction;
        
		update gal_trn_tpoclose set poclose_status = 'Rejected' , poclose_Remarks = ls_remarks , poclose_isactive = 'N' ,
        update_by = ls_update_by , Update_date = now()
        where poclose_poheader_gid = li_POHdr_gid and poclose_isremoved  ='N' and poclose_isactive = 'Y';
		
        set countRow = (select found_rows()) ;
        #select countRow;
		if countRow > 0 then   
        
			Update gal_trn_tpoheader set poheader_close = 'N', poheader_closeremarks = ls_remarks , update_by = ls_update_by , Update_date = now()
			where poheader_gid  = li_POHdr_gid;
	
			set countRow1 = (select found_rows());
			#select countRow1;
			if countRow1 > 0 then
				set Message = 'Success';
				commit;
			else
				set Message = 'FAIL';
				rollback;
			end if;
		end if;
    end if;

	else
		set Message = ls_error;
	end if;
end if;

if Action ='cancel' then
	if ls_error = '' then
    
    if Actionsts = 'Approve' then
		start transaction;
        
		update gal_trn_tpocancel set pocancel_status = 'Approved' , update_by = ls_update_by , Update_date = now()
        where pocancel_poheader_gid = li_POHdr_gid and pocancel_isremoved  ='N' and pocancel_isactive = 'Y';
                       
		set countRow = (select found_rows());

		if countRow > 0 then
        
        	Update gal_trn_tpoheader set poheader_cancel = 'Y' where poheader_gid  = li_POHdr_gid;

			set countRow = (select found_rows()) ;
			if countRow > 0 then
				set Message = 'Success';
				commit;
			else
				set Message = 'FAIL';
				rollback;
			end if;
		else
			set Message = 'FAIL';
			rollback;
		end if;
    end if;
    
    if Actionsts = 'Reject' then
		start transaction;
        
		update gal_trn_tpocancel set pocancel_status = 'Rejected' , pocancel_Remarks = ls_remarks , pocancel_isactive = 'N' ,
        update_by = ls_update_by , Update_date = now()
        where pocancel_poheader_gid = li_POHdr_gid and pocancel_isremoved  ='N' and pocancel_isactive = 'Y';
		
        
      
        set countRow = (select ROW_COUNT()) ;
		if countRow = 1 then   
        
			Update gal_trn_tpoheader set poheader_cancel = 'N',poheader_cancelremarks = ls_remarks , update_by = ls_update_by , Update_date = now()
			where poheader_gid  = li_POHdr_gid;
	
			set countRow = (select ROW_COUNT());
			if countRow >= 1 then
				set Message = 'Success';
				commit;
			else
				set Message = 'FAIL';
				rollback;
			end if;
		else
			set Message = 'FAIL';
			rollback;
		end if;
    end if;

	else
		set Message = ls_error;
	end if;
end if;

if Action = 'Maker' then

if ls_error = '' then
	if Actionsts = 'Approve' then
    
		start transaction;
        
		update gal_trn_tpoheader set poheader_status = 'Approved' , update_by = ls_update_by , Update_date = now()
        where poheader_gid = li_POHdr_gid and poheader_isremoved  ='N';
                       
		set countRow = (select found_rows());

		if countRow >= 0 then
			set Message = 'Success';
			commit;
		else
			set Message = 'FAIL';
			rollback;
		end if;
    end if;
    
    if Actionsts = 'Reject' then
    
		start transaction;
        
		update gal_trn_tpoheader set poheader_status = 'Rejected' ,poheader_remarks = ls_remarks , update_by = ls_update_by , Update_date = now()
        where poheader_gid = li_POHdr_gid and poheader_isremoved  ='N';
                       
		set countRow = (select ROW_COUNT());

		if countRow >= 0 then
			set Message = 'Success';
			commit;
		else
			set Message = 'FAIL';
			rollback;
		end if;
        
    end if;
    
else
	set Message = ls_error;
end if;

end if;
END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_POApproval_Get` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_POApproval_Get`(IN `ls_no` varchar(50),IN `ls_status` varchar(50),IN `li_emp_gid` int,
IN `li_sup_name` varchar(50),IN `ld_amnt` varchar(50))
BEGIN

#Vigneshwari       25-11-2017

declare Query_search varchar(1000);
declare PO_Headersrch varchar(1000);

if ls_status <> '' then
	set Query_search = concat(' and prheader_status like ''%' , ls_status , '%''');
else
	set Query_search = '';
end if;

if ls_no <> '' then
	set Query_search = concat(Query_search , ' and prheader_no like ''%' , ls_no , '%''');
else
	set Query_search = concat(Query_search , '');
end if;

if li_sup_name <> '' then
	set Query_search = concat(Query_search , ' and supplier_name like ''%' , li_sup_name , '%''');
else
	set Query_search = concat(Query_search , '');
end if;

if ld_amnt <> '' then
	set Query_search = concat(Query_search , ' and poheader_amount like ''%' , ld_amnt , '%''');
else
	set Query_search = concat(Query_search , '');
end if;

if li_emp_gid <> 0 then
	set Query_search = concat(Query_search , ' and a.create_by = ' , li_emp_gid);
else
	set Query_search = concat(Query_search , '');
end if;

set PO_Headersrch = ' 	select distinct poheader_gid , poheader_no , poheader_date , poheader_status , poheader_amount , supplier_name
				from gal_trn_tpoheader as a inner join gal_trn_tpodetails on poheader_gid = podetails_poheader_gid
                left join gal_mst_tsupplier on supplier_gid = poheader_supplier_gid and supplier_isremoved = ''N''
                where poheader_isremoved = ''N'' and poheader_isactive = ''Y''and podetails_isremoved = ''N'' 
                and poheader_amendment = ''N'' and poheader_close = ''N'' and poheader_cancel = ''N''
                and poheader_status = ''Pending for Approval'' ';

set @stmt = concat(PO_Headersrch , Query_search);

PREPARE stmt FROM @stmt;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_POApproval_Set` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_POApproval_Set`(IN `Action` varchar(16) , IN `li_POHeader_gid` int,
IN `ls_update_by` int ,OUT `Message` varchar(128))
BEGIN

#Vigneshwari       25-11-2017

declare Qry_Header varchar(1000);
declare ls_error varchar(100);
declare countRow int;
declare errno int;

	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO;
    SELECT errno AS MYSQL_ERROR;
    set Message = errno;
    set Message = 'Error';
    ROLLBACK;
    END;

set ls_error = '';

if li_POHeader_gid = 0 then
	set ls_error = 'PR Header gid not given';
end if;

if ls_error = '' then
	if Action = 'Approve' then
		start transaction;
		update gal_trn_tpoheader set poheader_status = 'Approved' , update_by = ls_update_by , Update_date = now()
        where poheader_gid = li_POHeader_gid and poheader_isremoved  ='N';
                       
		set countRow = (select ROW_COUNT());

		if countRow >= 0 then
			set Message = 'Success';
			commit;
		else
			set Message = 'FAIL';
			rollback;
		end if;
    end if;
    
    if Action = 'Reject' then
		start transaction;
		update gal_trn_tpoheader set poheader_status = 'Rejected' , update_by = ls_update_by , Update_date = now()
        where poheader_gid = li_POHeader_gid and poheader_isremoved  ='N';
                       
		set countRow = (select ROW_COUNT());

		if countRow >= 0 then
			set Message = 'Success';
			commit;
		else
			set Message = 'FAIL';
			rollback;
		end if;
    end if;
else
	set Message = ls_error;
end if;
END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_POApproval_Update_set` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_POApproval_Update_set`(IN `Action` varchar(64),IN `li_POHdr_gid` int,
IN `ls_remarks` varchar(256),IN `li_entity_gid` int,IN `ls_create_by` int, OUT `Message` varchar(100))
BEGIN

#Vigneshwari       21-11-2017

declare Qry_Header varchar(1000);
declare countRow int;
declare ls_error varchar(100);
declare errno int;
declare msg varchar(1000);

	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
    set Message = concat(errno , msg);
    ROLLBACK;
    END;

set ls_error = '';
if li_POHdr_gid = 0 then
	set ls_error = 'PO Header Data Not Passed.';
end if;

if ls_remarks = '' then
	set ls_error = 'Remarks not given';
end if;

if Action ='close' then
	if ls_error = '' then
		start transaction;

			insert into gal_trn_tpoclose (poclose_poheader_gid,poclose_date,poclose_status,poclose_Remarks,entity_gid,create_by)
            values (li_POHdr_gid , now() , 'Pending for Approval' , ls_remarks , ls_create_by , ls_create_by);
            
            set countRow = (select ROW_COUNT()) ;
			if countRow = 1 then
				select last_insert_id() into Message;
				update gal_trn_tpoheader set poheader_closeremarks = ls_remarks where poheader_gid = li_POHdr_gid;
				set Message=concat(Message,',Success');
                commit;
			else 
				set Message = 'NO CHANGE';
				rollback;
		end if;
	else
		set Message = ls_error;
	end if;
end if;

if Action = 'cancel' then
	if ls_error = '' then
		start transaction;
			
            insert into gal_trn_tpocancel (pocancel_poheader_gid,pocancel_date,pocancel_status,pocancel_Remarks,entity_gid,create_by) values 
            (li_POHdr_gid , now() , 'Pending for Approval' , ls_remarks , li_entity_gid , ls_create_by);
           
			set countRow = (select ROW_COUNT()) ;
			if countRow = 1 then
				select last_insert_id() into Message;
                update gal_trn_tpoheader set poheader_cancelremarks = ls_remarks where poheader_gid = li_POHdr_gid;
				set Message=concat(Message,',Success');
                commit;
			else 
				set Message = 'NO CHANGE';
				rollback;
			end if;
	else
		set Message = ls_error;
	end if;
end if;

if Action = 'reopen' then
	SET SQL_SAFE_UPDATES = 0;
	if ls_error = '' then
		start transaction;

		Update gal_trn_tpoheader set poheader_close = 'N' ,poheader_status = 'REOPENED', poheader_reopenremarks = ls_remarks , update_by = ls_create_by
        where poheader_gid  = li_POHdr_gid and poheader_close = 'Y';
        
		set countRow = (select ROW_COUNT()) ;
		if countRow = 1 then
        
			Update gal_trn_tpoclose set poclose_isactive = 'N' 
			where poclose_poheader_gid  = li_POHdr_gid and poclose_isremoved = 'N' and poclose_isactive = 'Y';

			set countRow = (select ROW_COUNT()) ;
			set Message = countRow;

			if countRow = 1 then
				set Message = ''',SUCCESS';
				commit;
			else 
				set Message = 'NO CHANGE';
				rollback;
			end if;
            
		end if;
	else
		set Message = ls_error;
	end if;
end if;

END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_POCancelApprovalview_Get` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_POCancelApprovalview_Get`(IN `ls_PO_no` varchar(50),IN `li_emp_gid` int,OUT `Message` varchar(128))
BEGIN

#Vigneshwari       29-11-2017

declare Query_search varchar(1000);
declare POcnclapp_Headersrch varchar(1000);
declare ls_error varchar(64);

set ls_error = '';

if ls_PO_no <> '' then
	set Query_search = concat(Query_search , ' and podetails_poheader_gid =' , ls_PO_no);
else
	set ls_error = 'PO Detail Not Given.';
end if;                                                                                                  

if li_emp_gid <> 0 then
	set Query_search = concat(Query_search , ' and a.create_by = ' , li_emp_gid);
else
	set Query_search = concat(Query_search , '');
end if;

if ls_error = '' then

	set POcnclapp_Headersrch = ' select distinct poheader_gid , podetails_gid , poheader_no , poheader_poterms_gid , 
				podetails_product_gid , product_name , producttype_name , 
				productcategory_name , podetails_unitprice , podetails_qty , poterms_name , uom_name , 
				podetails_amount from gal_trn_tpoheader as a inner join gal_trn_tpodetails on poheader_gid = podetails_poheader_gid
                left join gal_mst_tproduct on podetails_product_gid = product_gid and product_isremoved = ''N''
                left join gal_mst_tproducttype on product_producttype_gid = producttype_gid and producttype_isremoved = ''N''
                left join gal_mst_tproductcategory on product_productcategory_gid = productcategory_gid and productcategory_isremoved = ''N''
                left join gal_mst_tpoterms on poheader_poterms_gid = poterms_gid and poterms_isremoved = ''N''
                left join gal_trn_tpocancel on poheader_gid = pocancel_poheader_gid and pocancel_isremoved = ''N''
                left join gal_mst_tuom on product_uom_gid = uom_gid and uom_isremoved = ''N''
				where poheader_isremoved = ''N'' and poheader_isactive = ''Y''and podetails_isremoved = ''N''
                and poheader_cancel = ''Y'' and pocancel_status = ''Pending for Approval'' ';

	set @stmt = concat(POcnclapp_Headersrch , Query_search);
	PREPARE stmt FROM @stmt;
	EXECUTE stmt;
	DEALLOCATE PREPARE stmt;
	set Message = 'done';
else
	set Message = ls_error ;
end if;
END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_POCancelApproval_Get` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_POCancelApproval_Get`(IN `ls_no` varchar(16),IN `ld_amnt` int,IN `li_emp_gid` int,
IN `ls_status` varchar(64))
BEGIN

#Vigneshwari       29-11-2017

declare Query_search varchar(1000);
declare POcnclapp_Headersrch varchar(1000);

set Query_search = '';

if ls_no <> '' then
	set Query_search = concat(Query_search , ' and poheader_no like ''%' , ls_no , '%''');
else
	set Query_search = '';
end if;

if ls_status <> '' then
	set Query_search = concat(' and pocancel_status like ''%' , ls_status , '%''');
else
	set Query_search = concat(Query_search , '');
end if;

if ld_amnt <> '' then
	set Query_search = concat(Query_search , ' and poheader_amount like ''%' , ld_amnt , '%''');
else
	set Query_search = concat(Query_search , '');
end if;

if li_emp_gid <> 0 then
	set Query_search = concat(Query_search , ' and a.create_by = ' , li_emp_gid);
else
	set Query_search = concat(Query_search , '');
end if;

set POcnclapp_Headersrch = ' select distinct poheader_gid , poheader_no , poheader_date , pocancel_status AS poheader_status , supplier_name ,
				poheader_amount,pocancel_gid from gal_trn_tpoheader as a inner join gal_trn_tpodetails on poheader_gid = podetails_poheader_gid
                left join gal_trn_tpocancel on poheader_gid = pocancel_poheader_gid and pocancel_isremoved = ''N''
                left join gal_mst_tsupplier on poheader_supplier_gid = supplier_gid and supplier_isremoved = ''N''
				where poheader_isremoved = ''N'' and poheader_isactive = ''Y''and podetails_isremoved = ''N'' 
                and pocancel_status is not null and pocancel_status = ''Pending for Approval'' ';

set @stmt = concat(POcnclapp_Headersrch , Query_search);

PREPARE stmt FROM @stmt;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_POCancelView_Get` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_POCancelView_Get`(IN `ls_no` varchar(64),IN `li_sup_name` varchar(128),IN `li_emp_gid` int,
IN `ld_amnt` decimal,IN `ls_status` varchar(64))
BEGIN

#Vigneshwari       21-11-2017

declare Query_search varchar(1000);
declare PO_Cancelsrch text;

set @stmt = '';
set Query_search = '';
if ls_no <> '' then
	set Query_search = concat(' and poheader_no like ''%' , ls_no , '%'''); 
else
	set Query_search = '';
end if;

if li_sup_name <> '' then
	set Query_search = concat(Query_search , ' and supplier_name like ''%' , li_sup_name , '%''' );
else
	set Query_search = concat(Query_search , '');
end if;

if ld_amnt <> 0.00  and ld_amnt <> 0 then
	set Query_search = concat(Query_search , ' and poheader_amount like ''%' , ld_amnt  , '%''');
else
	set Query_search = concat(Query_search , '');
end if;

if ls_status <> '' then
	set Query_search = concat(Query_search , ' and poheader_status like ''%' , ls_status , '%''');
else
	set Query_search = concat(Query_search , '');
end if;

if li_emp_gid <> 0 then
	set Query_search = concat(Query_search , ' and a.create_by = ' , li_emp_gid);
else
	set Query_search = concat(Query_search , '');
end if;

set PO_Cancelsrch = ' 	select distinct poheader_gid , poheader_no , poheader_date , poheader_amount , poheader_status ,supplier_name,
						pocancel_status , pocancel_gid
						from gal_trn_tpoheader as a inner join gal_trn_tpodetails on poheader_gid = podetails_poheader_gid
                        left join gal_trn_tpocancel on pocancel_poheader_gid = poheader_gid  and pocancel_isremoved = ''N''
                        left join gal_mst_tsupplier on poheader_supplier_gid = supplier_gid and supplier_isremoved = ''N''
                        where poheader_isactive = ''Y'' and poheader_isremoved = ''N'' and podetails_isremoved = ''N''
                        and poheader_status = ''Approved'' and poheader_close = ''N'' 
                        and poheader_gid not in (select grninwarddetails_poheader_gid from gal_trn_tgrninwardheader 
                        inner join gal_trn_tgrninwarddetails on grninwardheader_gid = grninwarddetails_grninwardheader_gid 
                        where grninwardheader_isremoved = ''N'') ';

set @stmt = concat(PO_Cancelsrch , Query_search,'order by pocancel_gid desc');
#select @stmt;
PREPARE stmt FROM @stmt;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_POCloseApprovalview_Get` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_POCloseApprovalview_Get`(IN `ls_PO_no` varchar(50),IN `li_emp_gid` int,
OUT `Message` varchar(128))
BEGIN

#Vigneshwari       29-11-2017

declare Query_search varchar(1000);
declare POclsapp_Headersrch Text;
declare ls_error varchar(64);

set ls_error = '';

if ls_PO_no <> '' then
	set Query_search = concat(Query_search , ' and podetails_poheader_gid =' , ls_PO_no);
else
	set ls_error = 'PO Detail Not Given.';
end if;                                                                                                  

if li_emp_gid <> 0 then
	set Query_search = concat(Query_search , ' and a.create_by = ' , li_emp_gid);
else
	set Query_search = concat(Query_search , '');
end if;

if ls_error = '' then

	set POclsapp_Headersrch = ' select distinct poheader_gid , podetails_gid , poheader_no , poheader_poterms_gid , 
				podetails_product_gid , product_name , producttype_name , 
				productcategory_name , podetails_unitprice , podetails_qty , poterms_name , uom_name , 
				podetails_amount from gal_trn_tpoheader inner join gal_trn_tpodetails on poheader_gid = podetails_poheader_gid
                left join gal_mst_tproduct on podetails_product_gid = product_gid and product_isremoved = ''N''
                left join gal_mst_tproducttype on product_producttype_gid = producttype_gid and producttype_isremoved = ''N''
                left join gal_mst_tproductcategory on product_productcategory_gid = productcategory_gid and productcategory_isremoved = ''N''
                left join gal_mst_tpoterms on poheader_poterms_gid = poterms_gid and poterms_isremoved = ''N''
                left join gal_trn_tpoclose on poheader_gid = poclose_poheader_gid and poclose_isremoved = ''N''
                left join gal_mst_tuom on product_uom_gid = uom_gid and uom_isremoved = ''N''
				where poheader_isremoved = ''N'' and poheader_isactive = ''Y''and podetails_isremoved = ''N''
                and poheader_close = ''Y'' and poclose_status = ''Pending for Approval'' ';

	set @stmt = concat(POclsapp_Headersrch , Query_search);
    #select @stmt;
	PREPARE stmt FROM @stmt;
	EXECUTE stmt;
	DEALLOCATE PREPARE stmt;
	set Message = 'done';
else
	set Message = ls_error ;
end if;
END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_POCloseApproval_Get` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_POCloseApproval_Get`(IN `ls_no` varchar(50),IN `ld_amnt` int,IN `li_emp_gid` int,
IN `ls_status` varchar(64))
BEGIN

#Vigneshwari       29-11-2017

declare Query_search varchar(1000);
declare POclsapp_Headersrch varchar(1000);

set Query_search = '';

if ls_no <> '' then
	set Query_search = concat(Query_search , ' and poheader_no like ''%' , ls_no , '%''');
else
	set Query_search = '';
end if;                                                                                                  

if ls_status <> '' then
	set Query_search = concat(' and poclose_status like ''%' , ls_status , '%''');
else
	set Query_search = concat(Query_search , '');
end if;

if ld_amnt <> '' then
	set Query_search = concat(Query_search , ' and poheader_amount like ''%' , ld_amnt , '%''');
else
	set Query_search = concat(Query_search , '');
end if;

if li_emp_gid <> 0 then
	set Query_search = concat(Query_search , ' and a.create_by = ' , li_emp_gid);
else
	set Query_search = concat(Query_search , '');
end if;

set POclsapp_Headersrch = ' select distinct poheader_gid , poheader_no , poheader_date , poclose_status AS poheader_status , supplier_name ,
				poheader_amount,poclose_gid from gal_trn_tpoheader inner join gal_trn_tpodetails on poheader_gid = podetails_poheader_gid
                left join gal_trn_tpoclose on poheader_gid = poclose_poheader_gid and poclose_isremoved = ''N''
                left join gal_mst_tsupplier on poheader_supplier_gid = supplier_gid and supplier_isremoved = ''N''
				where poheader_isremoved = ''N'' and poheader_isactive = ''Y''and podetails_isremoved = ''N'' 
                and poclose_status is not null and poclose_status = ''Pending for Approval'' ';

set @stmt = concat(POclsapp_Headersrch , Query_search);
#select @stmt;
PREPARE stmt FROM @stmt;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_POCloseView_Get` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_POCloseView_Get`(IN `ls_no` varchar(64),IN `li_sup_name` varchar(128),
IN `ld_amnt` decimal,IN `ls_status` varchar(64),IN `li_emp_gid` int)
BEGIN

#Vigneshwari       21-11-2017

declare Query_search varchar(1000);
declare PO_Closesrch Text;

set Query_search = '';
if ls_no <> '' then
	set Query_search = concat(' and poheader_no like ''%' , ls_no , '%'''); 
else
	set Query_search = '';
end if;

if li_sup_name <> '' then
	set Query_search = concat(Query_search , ' and supplier_name like ''%' , li_sup_name , '%''' );
else
	set Query_search = concat(Query_search , '');
end if;

if ld_amnt <> 0.00  and ld_amnt <> 0 then
	set Query_search = concat(Query_search , ' and poheader_amount like ''%' , ld_amnt  , '%''');
else
	set Query_search = concat(Query_search , '');
end if;

if ls_status <> '' then
	set Query_search = concat(Query_search , ' and poheader_status like ''%' , ls_status , '%''');
else
	set Query_search = concat(Query_search , '');
end if;

if li_emp_gid <> 0 then
	set Query_search = concat(Query_search , ' and a.create_by = ' , li_emp_gid);
else
	set Query_search = concat(Query_search , '');
end if;

set PO_Closesrch = ' 	select distinct poheader_gid , poheader_no , poheader_date , poheader_amount ,poclose_status, 
						poheader_status ,supplier_name,poclose_gid
						from gal_trn_tpoheader as a inner join gal_trn_tpodetails on poheader_gid = podetails_poheader_gid
                        left join gal_trn_tpoclose on poheader_gid = poclose_poheader_gid and poclose_isremoved = ''N''
                        left join gal_mst_tsupplier on poheader_supplier_gid = supplier_gid and supplier_isremoved = ''N''
                        left join (select grninwarddetails_poheader_gid,grninwarddetails_podetails_gid , grninwarddetails_qty 
                        from gal_trn_tgrninwarddetails where grninwarddetails_isremoved = ''N'') as b 
                        on b.grninwarddetails_poheader_gid = poheader_gid and b.grninwarddetails_podetails_gid = podetails_gid
						where poheader_isactive = ''Y'' and poheader_isremoved = ''N'' and podetails_isremoved = ''N''
                        and poheader_status in (''Approved'',''REOPENED'') and poheader_cancel = ''N''
                        and podetails_qty > case when isnull(b.grninwarddetails_qty) then 0 else b.grninwarddetails_qty end 
                        and poheader_gid not in (select pocancel_poheader_gid from gal_trn_tpocancel where pocancel_isremoved = ''N''
                        and pocancel_status not in( ''Rejected''))';

set @stmt = concat(PO_Closesrch , Query_search,'order by poclose_gid desc');
#select @stmt;
PREPARE stmt FROM @stmt;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_PODelete_Set` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_PODelete_Set`(IN `li_PODet_gid` int ,
IN `ls_emp_gid` int,IN `li_entity_gid` int, OUT `Message` varchar(100))
BEGIN

#Vigneshwari       17-11-2017

declare chk varchar(1000);
declare PO_DelSrch varchar(1000);
declare countrow int;
declare ls_error varchar(100);
declare podet_gid int;

set chk = '';
set ls_error = '';

if li_PODet_gid = 0 then
	set ls_error = ' PO Detail Gid not Given. ';
end if;

if ls_emp_gid = 0 then
	set ls_error = ' Employee Gid not Given. ';
end if;

if ls_error = '' then

	select case when isnull(podetails_poheader_gid) then 0 else podetails_poheader_gid end into podet_gid 
		from gal_trn_tpodetails where podetails_isremoved = 'N' and podetails_gid = li_PODet_gid;

	set @Srch = concat('select podetails_gid from gal_trn_tpodetails where podetails_isremoved = ''N'' 
						and podetails_poheader_gid =', podet_gid);
	PREPARE stmtt FROM @Srch;
	EXECUTE stmtt ;
	set countrow = (select found_rows());
	DEALLOCATE PREPARE stmtt;
    
if countrow = 1 then

	start transaction;
    
UPDATE gal_trn_tpodetails 
SET 
    podetails_isremoved = 'Y',
    update_by = ls_emp_gid,
    Update_date = NOW()
WHERE
    podetails_gid = li_PODet_gid;
    
	set PO_DelSrch = concat('  Update gal_trn_tpoheader set poheader_isremoved = ''Y'' , update_by = ''' ,ls_emp_gid , 
					''' , Update_date = now() where poheader_gid = ',podet_gid );
    
	set @q = PO_DelSrch;
	PREPARE stmtt FROM @q;
	EXECUTE stmtt ;
	set countrow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmtt;
	if countrow > 0 then
		set  Message = 'DELETION_DONE';
        
        commit;
	else
		set Message = 'NO_DELETION';
        rollback;
	end if;
else

	start transaction;
    
	set PO_DelSrch = concat('  Update gal_trn_tpodetails set podetails_isremoved = ''Y'' , update_by = ''' ,ls_emp_gid , 
					''' , Update_date = now() where podetails_gid = ',li_PODet_gid );
	set @q = PO_DelSrch;
	PREPARE stmtt FROM @q;
	EXECUTE stmtt ;
	set countrow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmtt;
	
    if countrow > 0 then
		call sp_PRPOQty_Set('delete', 0, li_PODet_gid, 0, 0, 1, ls_emp_gid, 1, @Message);
		SELECT @Message INTO @prpo;
        if @prpo='SUCCESS' then
			select * from gal_trn_tpodelivery where podelivery_podetails_gid = li_PODet_gid;
			set @cntrows = (select found_rows());
			SELECT @cntrows;
        
			if @cntrows >0 then
				call sp_PODelivery_Set('Delete', 0, li_PODet_gid, 0, 0, 0, 1, ls_emp_gid,1, @Message1);
				SELECT @Message1 INTO @podelivery;
				if @podelivery='SUCCESS' then
					set  Message = 'DELETION_DONE';
					commit;
				else
					set Message = 'NO_DELETION IN PODELIVERY';
					rollback;
				end if;
			else
				set  Message = 'DELETION_DONE';
				commit;
			end if;
		else
				set Message = 'NO_DELETION IN PRPOQTY';
				rollback;
		end if;      
        
	else
		set Message = 'NO_DELETION';
        rollback;
	end if;
end if;
else
	set Message = ls_error; 
end if;

END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_PODelivery_Get` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_PODelivery_Get`(IN `ls_no` varchar(64),OUT `Message` varchar(128))
BEGIN

#Vigneshwari       18-11-2017

declare Query_search varchar(1000);
declare PO_Headersrch varchar(1000);
declare ls_error varchar(64);

set ls_error ='';

if ls_no <> '' then
	set Query_search = concat(' and podelivery_podetails_gid =' , ls_no ); 
else
	set Query_search = '';
	set ls_error = 'PO Delivery Not Selected';
end if;

if ls_error = '' then
set PO_Headersrch = ' 	select podelivery_gid , podelivery_poheader_gid , podelivery_podetails_gid,godown_gid, employee_gid,
						address_gid ,uom_gid ,godown_name ,employee_name , address_1 , uom_name , podelivery_qty
                        from gal_trn_tpodelivery inner join gal_mst_tgodown on podelivery_godown_gid = godown_gid 
                        left join gal_mst_taddress on godown_address_gid = address_gid 
                        left join gal_mst_tproduct on podelivery_product_gid = product_gid and product_isremoved = ''N'' and product_isactive = ''Y''
                        left join gal_mst_tuom on product_uom_gid = uom_gid and uom_isremoved = ''N''
                        left join gal_mst_temployee on godown_inchage_gid = employee_gid and employee_isremoved = ''N''
                        where podelivery_isremoved = ''N'' and godown_isremoved = ''N'' and godown_isactive = ''Y'' ';

set @stmt = concat(PO_Headersrch , Query_search);
PREPARE stmt FROM @stmt;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

set Message = 'done';
else

set Message = ls_error ;

end if;

END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_PODelivery_Set` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_PODelivery_Set`(IN `Action` varchar(16),IN `li_POHeader_gid` int,
IN `li_PODetail_gid` int,IN `li_product_gid` int,IN `li_quantity` int,IN `li_godown_gid` int,IN `li_entity_gid` int,
IN `ls_create_by` int ,IN `li_podel_gid` int,OUT `Message` varchar(128))
BEGIN

#Vigneshwari       18-11-2017
#Vigneshwari       06-12-2017

declare Qry_Header varchar(1000);
declare ls_error varchar(100);
declare countRow int;
declare errno int;

	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO;
    SELECT errno AS MYSQL_ERROR;
    set Message = errno;
    ROLLBACK;
    END;

set ls_error = '';
if Action = 'Insert' then

if li_POHeader_gid = 0 or li_POHeader_gid = '' then
	set ls_error = 'PO Header Not Selected.';
else 
	set @err = concat('select * from gal_trn_tpoheader where poheader_gid =''', li_POHeader_gid ,''' group by poheader_gid' );
    PREPARE stmt1 FROM @err;
	EXECUTE stmt1;  
	set countRow = (select found_rows());
	DEALLOCATE PREPARE stmt1;
    if countRow <= 0 then
		set ls_error = 'PO Header No not found in Header';
	end if;
end if;

if li_PODetail_gid = 0 or li_PODetail_gid = '' then
	set ls_error = 'PO Detail Not Selected.';
else 
	set @err = concat('select * from gal_trn_tpodetails where podetails_gid =''', li_PODetail_gid ,''' group by podetails_gid' );
    PREPARE stmt1 FROM @err;
	EXECUTE stmt1;  
	set countRow = (select found_rows());
	DEALLOCATE PREPARE stmt1;
    if countRow <= 0 then
		set ls_error = 'PO detail No not found in Detail';
	end if;
end if;

if li_product_gid = 0 then
	set ls_error = 'Product Not Selected.';
end if;

if li_quantity <= 0 then
	set ls_error = 'Quantity entered is Not in correct form.';
end if;

if li_godown_gid = 0 then
	set ls_error = 'Godown Name Not Selected.';
end if;

if ls_error = '' then
	start transaction;
	set Qry_Header = concat('INSERT INTO gal_trn_tpodelivery(podelivery_poheader_gid, podelivery_podetails_gid, 
						podelivery_product_gid, podelivery_qty,podelivery_godown_gid,entity_gid, create_by) VALUES
                        (',li_POHeader_gid,',',li_PODetail_gid,',',li_product_gid,',',li_quantity,',',li_godown_gid,
                        ',',li_entity_gid,',',ls_create_by,')');
                  
	set @Qry_Header = Qry_Header;
    PREPARE stmt FROM @Qry_Header;
	EXECUTE stmt;  
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt; 

	if countRow > 0 then
		select LAST_INSERT_ID() into Message ;
        set Message = CONCAT(Message,',SUCCESS');
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

if li_podel_gid = 0 then
	set ls_error = 'PO Delivery gid Not Selected.';
end if;

if ls_error = '' then
	start transaction;
    
    update gal_trn_tpodelivery set podelivery_qty = li_quantity, podelivery_godown_gid = li_godown_gid , 
    update_by = ls_create_by , Update_date = now() where podelivery_gid = li_podel_gid;
 
	set countRow = (select ROW_COUNT()) ;
		if countRow = 1 then
		
			set Message = 'SUCCESS';
			commit;
		else 
			set Message = 'NO CHANGE';
			rollback;
		end if;
else
	set Message = ls_error;
end if;
end if;


if Action = 'Delete' then

if li_podel_gid = 0 then
	set ls_error = 'PO Delivery gid Not Selected.';
end if;

if ls_error = '' then
	start transaction;
    set SQL_SAFE_UPDATES=0;
    
    update gal_trn_tpodelivery set podelivery_isremoved = 'Y' , 
    update_by = ls_create_by , Update_date = now() where podelivery_podetails_gid = li_PODetail_gid;
 
	set countRow = (select ROW_COUNT()) ;
		if countRow = 1 then
		
			set Message = 'SUCCESS';
			
		else 
			set Message = 'NO CHANGE';
			
		end if;
else
	set Message = ls_error;
end if;
end if;

END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_PODetailUpdate_Set` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_PODetailUpdate_Set`(IN `li_PODtil_gid` int,IN `li_prod_gid` int,
IN `li_qty` int,IN `ld_unitprice` decimal(18,0),IN `ld_amount` decimal(18,0),IN `ld_taxamount` decimal(18,0),
IN `ld_totalamount` decimal(18,0),IN `ls_create_by` int,OUT `Message` varchar(128))
BEGIN

#Vigneshwari       17-11-2017

declare Qry_Header varchar(1000);
declare countRow int;
declare ls_error varchar(100);
declare errno int;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO;
    SELECT errno AS MYSQL_ERROR;
    set Message = errno;
    ROLLBACK;
    END;

set ls_error = '';
if li_PODtil_gid = 0 then
	set ls_error = 'Purchase Order Details Data Not Passed.';
end if;

if li_qty = 0 then
	set ls_error = 'Quantity Not Correct.';
end if;

if li_prod_gid = 0 then
	set ls_error = 'Product Not Selected.';
end if;

if ld_unitprice = 0 then
	set ls_error = 'Unit Price Not Correct.';
end if;

if ld_amount = 0 then
	set ls_error = 'Amount Not Selected.';
end if;


if ld_totalamount = 0 then
	set ls_error = 'Total Amount Not Selected.';
end if;

if ls_error = '' then
	start transaction;

	Update gal_trn_tpodetails set podetails_qty = li_qty , podetails_product_gid = li_prod_gid,podetails_unitprice = ld_unitprice,
    podetails_amount = ld_amount,podetails_taxamount = ld_taxamount,podetails_totalamount = ld_totalamount,update_by = ls_create_by,update_date = now()
	where podetails_gid  = li_PODtil_gid and podetails_isremoved  ='N';

	set countRow = (select ROW_COUNT()) ;
	set Message = countRow;

	if countRow = 1 then
		set Message = ''',SUCCESS';
		commit;
	else 
		set Message = 'NO CHANGE';
        rollback;
	end if;
else
	set Message = ls_error;
end if;
END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_PODetail_Get` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_PODetail_Get`(IN `li_podetail_gid` int,IN `ls_prod_name` varchar(128),IN `li_emp_gid` int,
OUT `Message` varchar(128))
BEGIN

#Vigneshwari       18-11-2017

declare Query_search varchar(1000);
declare PO_Detailssrch text;
declare ls_error varchar(64);

set ls_error = '';

if li_podetail_gid <> 0 then
	set Query_search = concat(' and podetails_poheader_gid = ' , li_podetail_gid);
else
	set ls_error = 'PO Detail Not Given.';
end if;

if ls_prod_name <> '' then
	set Query_search = concat(Query_search , ' and product_name like ''%' , ls_prod_name , '%''');
else
	set Query_search = concat(Query_search , '');
end if;

if li_emp_gid <> 0 then
	set Query_search = concat(Query_search , ' and a.create_by = ' , li_emp_gid);
else
	set Query_search = concat(Query_search , '');
end if;

if ls_error = '' then

	set PO_Detailssrch = 'select poheader_gid,podetails_gid ,product_gid , producttype_gid , productcategory_gid , 
		poterms_gid,poheader_supplier_gid ,poheader_no ,productcategory_name ,producttype_name ,product_name ,uom_name ,
        podetails_qty , podetails_uom , podetails_unitprice ,podetails_amount ,podetails_taxamount ,podetails_totalamount ,	
        poterms_name,poheader_remarks ,poheader_status,supplier_name,poheader_date ,poheader_validfrom,poheader_validto,poheader_approvallater
		from gal_trn_tpoheader 
		inner join gal_trn_tpodetails on poheader_gid = podetails_poheader_gid 
		left join gal_mst_tproduct on podetails_product_gid = product_gid and product_isremoved = ''N''
		left join gal_mst_tproducttype on product_producttype_gid = producttype_gid and producttype_isremoved = ''N''
		left join gal_mst_tproductcategory on producttype_productcategory_gid = productcategory_gid and product_isremoved = ''N''
		left join gal_mst_tuom on product_uom_gid = uom_gid and uom_isremoved = ''N''
        left join gal_mst_tpoterms on poheader_poterms_gid = poterms_gid and poterms_isremoved = ''N''
        left join gal_mst_tsupplier on supplier_gid = poheader_supplier_gid and supplier_isremoved = ''N''
		where poheader_isremoved = ''N'' and poheader_isactive = ''Y'' and podetails_isremoved = ''N'' ';

	set @stmt = concat(PO_Detailssrch , Query_search);
    #select @stmt;
	PREPARE stmt FROM @stmt;
	EXECUTE stmt;
	DEALLOCATE PREPARE stmt;
	set Message = 'done';
else
	set Message = ls_error ;
end if;
END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_PODetail_Set` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_PODetail_Set`(IN `li_POHeaderMAX_gid` int,IN `li_product_gid` int,IN `li_quantity` int,
IN `ls_UOM` varchar(64),IN `ld_UnitPrice` decimal(10,2),IN `ld_Amount` decimal(10,2),IN `ld_Taxamt` decimal(10,2),
IN `ld_Netamount` decimal(10,2), IN `li_entity_gid` int,IN `ls_create_by` int ,OUT `Message` varchar(128))
BEGIN

#Vigneshwari       17-11-2017

declare Qry_Header varchar(1000);
declare ls_error varchar(100);
declare countRow int;
declare errno int;

	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO;
    SELECT errno AS MYSQL_ERROR;
    set Message = errno;
    ROLLBACK;
    END;

set ls_error = '';

if li_POHeaderMAX_gid = 0 or li_POHeaderMAX_gid = '' then
	set ls_error = 'PO Header Not Selected.';
else 
	set @err = concat('select * from gal_trn_tpoheader where poheader_gid =''', li_POHeaderMAX_gid ,'''' , ' group by poheader_gid' );
    PREPARE stmt1 FROM @err;
	EXECUTE stmt1;  
	set countRow = (select found_rows());
	DEALLOCATE PREPARE stmt1;
    if countRow <= 0 then
		set ls_error = 'PO Header No not found in Header';
	end if;
end if;

if li_product_gid = 0 then
	set ls_error = 'Product Not Selected.';
end if;

if li_quantity <= 0 then
	set ls_error = 'Quantity entered is not in correct form.';
end if;
if ls_error = '' then
	start transaction;
	set Qry_Header = concat('INSERT INTO gal_trn_tpodetails(podetails_poheader_gid, podetails_product_gid, podetails_qty, 
							podetails_uom , podetails_unitprice ,podetails_amount ,podetails_taxamount ,podetails_totalamount ,
						entity_gid, create_by) VALUES
                        (',li_POHeaderMAX_gid,',',li_product_gid,',',li_quantity,',''',ls_UOM , ''',
                        ',ld_UnitPrice,',',ld_Amount,',',ld_Taxamt,',',ld_Netamount,',',li_entity_gid,',',ls_create_by,')');

	set @Qry_Header = Qry_Header;
    PREPARE stmt FROM @Qry_Header;
	EXECUTE stmt;  
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt; 

	if countRow > 0 then
		select LAST_INSERT_ID() into Message ;
        set Message = CONCAT(Message,',SUCCESS');
        commit;
	else
		set Message = 'FAIL';
        rollback;
	end if;
else
	set Message = ls_error;
end if;





END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_PODlvrygodown_Get` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_PODlvrygodown_Get`(IN `ls_no` varchar(64),OUT `Message` varchar(128))
BEGIN

#Vigneshwari       29-11-2017

declare Query_search varchar(1000);
declare PO_Deliverysrch varchar(1000);
declare ls_error varchar(64);

set ls_error ='';

if ls_no <> '' then
	set Query_search = concat(' and godown_gid =' , ls_no ); 
else
	set ls_error = 'Godown Not Selected';
end if;

if ls_error = '' then
set PO_Deliverysrch = ' 	select godown_gid , employee_gid , address_gid , godown_name ,employee_name , address_1 
                        from  gal_mst_tgodown  
                        left join gal_mst_taddress on godown_address_gid = address_gid 
                        left join gal_mst_temployee on godown_inchage_gid = employee_gid and employee_isremoved = ''N''
                        where godown_isremoved = ''N'' and godown_isactive = ''Y'' ';

set @stmt = concat(PO_Deliverysrch , Query_search);
PREPARE stmt FROM @stmt;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

set Message = 'done';
else

set Message = ls_error ;

end if;

END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_POHdr_Get` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_POHdr_Get`(IN `li_podetail_gid` int,IN `ls_prod_name` varchar(50),IN `li_emp_gid` int,
OUT `Message` varchar(128))
BEGIN

#Vigneshwari       18-11-2017

declare Query_search varchar(1000);
declare PO_Detailssrch varchar(1000);
declare ls_error varchar(64);

set ls_error = '';

if li_podetail_gid <> 0 then
	set Query_search = concat(' and podetails_gid = ' , li_podetail_gid);
else
	set ls_error = 'PO Detail Not Given.';
end if;

if ls_prod_name <> '' then
	set Query_search = concat(Query_search , ' and product_name like ''%' , ls_prod_name , '%''');
else
	set Query_search = concat(Query_search , '');
end if;

if li_emp_gid <> 0 then
	set Query_search = concat(Query_search , ' and a.create_by = ' , li_emp_gid);
else
	set Query_search = concat(Query_search , '');
end if;

if ls_error = '' then

	set PO_Detailssrch = 'select poheader_gid , poheader_no , poheader_date , poheader_amount , poheader_status 
						from gal_trn_tpoheader as a inner join gal_mst_tsupplier on poheader_supplier_gid = supplier_gid
                        where poheader_isactive = ''Y'' and poheader_isremoved = ''N''';

	set @stmt = concat(PO_Detailssrch , Query_search);
	select @stmt;
	PREPARE stmt FROM @stmt;
	EXECUTE stmt;
	DEALLOCATE PREPARE stmt;
	set Message = 'done';
else
	set Message = ls_error ;
end if;
END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_POHeaderUpdate_Set` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_POHeaderUpdate_Set`(IN `Action` varchar(16),IN `li_pohdr_gid` int,IN `li_terms` int, 
IN `ld_fromdate` varchar(64),IN `ld_todate` varchar(64),IN `ld_amount` decimal(10,2),OUT `Message` varchar(1000))
BEGIN

#Vigneshwari       23-11-2017

declare ls_error varchar(100);
declare countRow int;
declare errno int;
declare msg varchar(1000);

	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
    set Message = concat(errno , msg);
    ROLLBACK;
    END;

if Action = 'submit' then
		start transaction;
			Update gal_trn_tpoheader set poheader_status = 'Pending for Approval' , poheader_amount = ld_amount,
					poheader_poterms_gid = li_terms,poheader_validfrom = ld_fromdate,poheader_validto = ld_todate
            where poheader_gid  = li_pohdr_gid and poheader_isremoved  ='N';

		set countRow = (select ROW_COUNT());
		if countRow >=  0 then
			set Message = ''',Success';
			commit;
		else
			set Message = 'FAIL';
			rollback;
		end if;
end if;

if Action = 'draft' then
		start transaction;
			Update gal_trn_tpoheader set poheader_status = 'Draft'  , poheader_amount = ld_amount,
				poheader_poterms_gid = li_terms,poheader_validfrom = ld_fromdate,poheader_validto = ld_todate
            where poheader_gid  = li_pohdr_gid and poheader_isremoved  ='N';

		set countRow = (select ROW_COUNT());
		if countRow >=  0 then
			set Message = ''',Success';
			commit;
		else
			set Message = 'FAIL';
			rollback;
		end if;
end if;

END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_POHeader_Get` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_POHeader_Get`(IN `ls_no` varchar(64),IN `li_sup_name` varchar(64),
IN `ld_amnt` decimal,IN `ls_status` varchar(50),IN `li_emp_gid` int)
BEGIN

#Vigneshwari       16-11-2017

declare Query_search varchar(1000);
declare PO_Headersrch varchar(1000);

set Query_search = '';
if ls_no <> '' then
	set Query_search = concat(' and poheader_no like ''%' , ls_no , '%'''); 
else
	set Query_search = '';
end if;

if li_sup_name <> '' then
	set Query_search = concat(Query_search , ' and supplier_name like ''%' , li_sup_name , '%''' );
else
	set Query_search = concat(Query_search , '');
end if;

if ld_amnt <> 0.00  and ld_amnt <> 0 then
	set Query_search = concat(Query_search , ' and poheader_amount like ''%' , ld_amnt  , '%''');
else
	set Query_search = concat(Query_search , '');
end if;

if ls_status <> '' then
	set Query_search = concat(Query_search , ' and poheader_status like ''%' , ls_status , '%''');
else
	set Query_search = concat(Query_search , '');
end if;

if li_emp_gid <> 0 then
	set Query_search = concat(Query_search , ' and a.create_by = ' , li_emp_gid);
else
	set Query_search = concat(Query_search , '');
end if;


set PO_Headersrch = ' 	select distinct poheader_gid , poheader_no , poheader_date , poheader_amount , poheader_status ,supplier_name
						from gal_trn_tpoheader as a inner join gal_trn_tpodetails on poheader_gid = podetails_poheader_gid
                        left join gal_mst_tsupplier on poheader_supplier_gid = supplier_gid and supplier_isremoved = ''N''
                         where poheader_isactive = ''Y'' and poheader_isremoved = ''N'' and podetails_isremoved = ''N'' 
                         and poheader_amendment = ''N'' and poheader_close = ''N'' and poheader_cancel = ''N'' 
                         ';

set @stmt = concat(PO_Headersrch , Query_search,'order by poheader_gid desc');
PREPARE stmt FROM @stmt;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_POHeader_Set` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_POHeader_Set`(IN `Action` varchar(16),IN `li_date` datetime,
IN `li_sup_gid` int,IN `li_term_gid` int,IN `li_amt` float,IN `ls_amenment` char(8),IN `ls_version` varchar(64),
IN `ls_status` varchar(64),IN `ld_validfrom` varchar(16),IN `ld_validto` datetime,IN `li_entity_gid` int,
IN `ls_create_by` int,OUT `Message` varchar(1000))
BEGIN

#Vigneshwari       17-11-2017

declare Qry_Header varchar(1000);
declare ls_error varchar(100);
declare countRow int;
declare errno int;
declare msg varchar(1000);
declare ls_no varchar(64);

	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO , msg = MESSAGE_TEXT;
    set Message = concat(errno , msg);
    ROLLBACK;
    END;

set ls_error = '';


call sp_Generate_number_get('PO','000',@Message);
select @Message into ls_no from dual;

if ls_no = '' then
	set ls_error = ' PO Header No not Given. ';
else 
	set @err = concat('select * from gal_trn_tpoheader where poheader_no =''', ls_no ,'''' , ' group by poheader_no' );
    PREPARE stmt1 FROM @err;
	EXECUTE stmt1;  
	set countRow = (select found_rows());
	DEALLOCATE PREPARE stmt1;
    if countRow > 0 then
		set ls_error = ' Duplicate PO Header No ';
    end if;
end if;

if li_date = '' then
	set ls_error = ' PO Header Date Not Given. ';
end if;

if li_sup_gid = 0 then
	set ls_error = ' Supplier Not Selected. ';
end if;

#if li_term_gid = 0 then
#	set ls_error = ' Terms and Conditions not selected. ';
#end if;

#if li_amt = 0.00 then
#	set ls_error = ' Amount is empty. ';
#end if;

if ls_amenment = '' then
	set ls_error = ' Amendment is not given.';
end if;

if ls_version = '' then
	set ls_error = ' Version not Mentioned. ';
end if;

if ls_status = '' then
	set ls_error = ' Status Not Selected.';
end if;

if ld_validfrom = '' then
	set ld_validfrom = curdate();
end if;

if ld_validto = '' then
	set ls_error = ' Valid To Date Not Given. ';
end if;

if ls_error = '' then
if Action = 'submit' then
	start transaction;
    set ls_status='Pending For Approval';
    
	set Qry_Header = concat('INSERT INTO gal_trn_tpoheader(poheader_no , poheader_date , poheader_supplier_gid , 
							poheader_poterms_gid , poheader_amount , poheader_amendment , poheader_version , poheader_status , 
                            poheader_validfrom,poheader_validto,entity_gid , create_by) VALUES 
                            (''' , ls_no , ''',''' , li_date , ''',' , li_sup_gid , ',' , li_term_gid , ',''' , li_amt , 
                            ''',''' , ls_amenment , ''',''' , ls_version , ''',''' , ls_status , ''',''' , ld_validfrom , ''',''' 
                            , ld_validto , ''',' , li_entity_gid , ',' , ls_create_by , ')');

	set @Qry_Header = Qry_Header;
	PREPARE stmt FROM @Qry_Header;
	EXECUTE stmt;  
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt; 

	if countRow >  0 then
		select LAST_INSERT_ID() into Message ;
        set Message = CONCAT(Message,',SUCCESS');
		commit;
	else
		set Message = 'FAIL';
        rollback;
	end if;
end if;

if Action = 'draft' then
	start transaction;
	set Qry_Header = concat('INSERT INTO gal_trn_tpoheader(poheader_no , poheader_date , poheader_supplier_gid , 
							poheader_poterms_gid , poheader_amount , poheader_amendment , poheader_version , poheader_status , 
                            poheader_validfrom,poheader_validto,entity_gid , create_by) VALUES 
                            (''' , ls_no , ''',''' , li_date , ''',' , li_sup_gid , ',' , li_term_gid , ',''' , li_amt , 
                            ''',''' , ls_amenment , ''',''' , ls_version , ''',''' , ls_status , ''',''' , ld_validfrom , ''',''' 
                            , ld_validto , ''',' , li_entity_gid , ',' , ls_create_by , ')');

	set @Qry_Header = Qry_Header;
	PREPARE stmt FROM @Qry_Header;
	EXECUTE stmt;  
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt; 

	if countRow >  0 then
		select LAST_INSERT_ID() into Message ;
		commit;
	else
		set Message = 'FAIL';
        rollback;
	end if;
end if;

if Action = 'request' then
	start transaction;
	set Qry_Header = concat('INSERT INTO gal_trn_tpoheader(poheader_no , poheader_date , poheader_supplier_gid , 
							poheader_poterms_gid , poheader_amount , poheader_amendment , poheader_version , poheader_status , 
                            poheader_validfrom,poheader_validto,entity_gid , create_by) VALUES 
                            (''' , ls_no , ''',''' , li_date , ''',' , li_sup_gid , ',' , li_term_gid , ',''' , li_amt , 
                            ''',''' , ls_amenment , ''',''' , ls_version , ''',''' , ls_status , ''',''' , ld_validfrom , ''',''' 
                            , ld_validto , ''',' , li_entity_gid , ',' , ls_create_by , ')');

	set @Qry_Header = Qry_Header;
	PREPARE stmt FROM @Qry_Header;
	EXECUTE stmt;  
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt; 

	if countRow >  0 then
		select LAST_INSERT_ID() into Message ;
		commit;
	else
		set Message = 'FAIL';
        rollback;
	end if;
end if;

if Action = 'polater' then
	start transaction;
	set Qry_Header = concat('INSERT INTO gal_trn_tpoheader(poheader_no , poheader_date , poheader_supplier_gid , 
							poheader_poterms_gid , poheader_amount , poheader_amendment , poheader_version , poheader_status , 
                            poheader_approvallater,poheader_validfrom,poheader_validto,entity_gid , create_by) VALUES 
                            (''' , ls_no , ''',''' , li_date , ''',' , li_sup_gid , ',' , li_term_gid , ',''' , li_amt , 
                            ''',''' , ls_amenment , ''',''' , ls_version , ''',''Approved'',''Y'',''' , ld_validfrom , ''',''' 
                            , ld_validto , ''',' , li_entity_gid , ',' , ls_create_by , ')');

	set @Qry_Header = Qry_Header;
	#select @Qry_Header;
    PREPARE stmt FROM @Qry_Header;
	EXECUTE stmt;  
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt; 

	if countRow >  0 then
		select LAST_INSERT_ID() into Message;
        set Message = CONCAT(Message,',SUCCESS');
		commit;
	else
		set Message = 'FAIL';
        rollback;
	end if;
end if;

else
	set Message = ls_error;
end if;

END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_POQtyList_Get` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_POQtyList_Get`(IN `Action` varchar(16),IN `ls_sup_gid` int,IN `li_Prod_gid` int,
IN `ls_prod_name` varchar(64),IN `li_podtl_gid` int,OUT `Message` varchar(1000))
BEGIN

#Vigneshwari       20-11-2017

declare Query_search varchar(1000);
declare Qty_srch text;
declare ls_error varchar(64);

set ls_error = '';
set Query_search = '';

if Action = 'PRODUCTWISE' then

	if ls_sup_gid <> 0 then
		set Query_search = concat(' and supplierproduct_supplier_gid = ' ,ls_sup_gid);
	else
		set ls_error = 'supplier not given';
	end if;

	if li_Prod_gid <> 0 then
		set Query_search = concat(Query_search , ' and prdetails_product_gid = ' ,li_Prod_gid);
	else
		set ls_error = 'Product not given';
	end if;

	if ls_prod_name <> '' then
		set Query_search = concat(Query_search , ' and product_name like ''%' , ls_prod_name , '%''' );
	else
		set Query_search = concat(Query_search , '');
	end if;



	if ls_error = '' then

		set Qty_srch = concat(' select prheader_gid,prheader_date,prdetails_gid,prpoqty_gid,product_gid,product_name , producttype_name , 
						productcategory_name , prheader_no , prdetails_qty , uom_name , supplierproduct_unitprice , 
						sum(prpoqty_qty)as current_qty,prpoqty_qty,
						case when isnull(prdetails_qty) then 0 else prdetails_qty end -
						case when isnull(prpoqty_qty) then 0 else sum(prpoqty_qty) end as req_qty,''0'' as all_qty
						FROM gal_trn_tprheader 
						inner join gal_trn_tprdetails on prheader_gid = prdetails_prheader_gid
						left join gal_trn_tprpoqty on prdetails_gid = prpoqty_prdetails_gid and prpoqty_isremoved = ''N'' 
						left join gal_mst_tproduct on product_gid = prdetails_product_gid and product_isremoved = ''N''
						left join gal_mst_tproducttype on product_producttype_gid = producttype_gid and producttype_isremoved = ''N''
						left join gal_mst_tproductcategory on product_productcategory_gid = productcategory_gid and productcategory_isremoved = ''N''
						left join gal_mst_tuom on product_uom_gid = uom_gid and uom_isremoved = ''N''
						left join gal_map_tsupplierproduct on supplierproduct_product_gid = product_gid and supplierproduct_isremoved = ''N'' and supplierproduct_isactive = ''Y''
						where prheader_status in( ''Approved'') and prheader_isremoved = ''N'' and prdetails_isremoved = ''N'' ',
						Query_search , ' group by prdetails_product_gid,prdetails_gid 
						');
		
                    
		if li_podtl_gid <> 0 then
			set @stmt = concat('select distinct main.prheader_gid , main.prdetails_gid , main.product_gid , main.prpoqty_gid ,
								main.product_name , main.producttype_name , main.productcategory_name , main.prheader_no , 
								main.uom_name , main.supplierproduct_unitprice ,main.prdetails_qty, 
								case when isnull(main.prdetails_qty) then 0 else main.prdetails_qty end - ( 
								case when isnull(main.current_qty) then 0 else main.current_qty end - 
								case when isnull(a.prpoqty_qty) then 0 else a.prpoqty_qty end) as req_qty , 
								case when isnull(a.prpoqty_qty) then 0 else a.prpoqty_qty end as all_qty
								from (' , Qty_srch , ') as main
								left join gal_trn_tprpoqty as a on main.prdetails_gid = a.prpoqty_prdetails_gid and a.prpoqty_isremoved = ''N'' 
								and a.prpoqty_podetails_gid = ' , li_podtl_gid);
		else
			set @stmt = concat(Qty_srch,'having req_qty >0');
		end if;
		#select @stmt;
		PREPARE stmt FROM @stmt;
		EXECUTE stmt;
		DEALLOCATE PREPARE stmt;
	else 
		set Message = ls_error;
	end if;
end if;

if Action = 'ALL' then

	if ls_prod_name <> '' then
		set Query_search = concat(Query_search , ' and product_name like ''%' , ls_prod_name , '%''' );
	else
		set Query_search = concat(Query_search , '');
	end if;



	if ls_error = '' then
/*
		set Qty_srch = concat(' select prheader_gid,prheader_date,prheader_remarks,prdetails_gid,prpoqty_gid,product_gid,product_name , product_displayname,producttype_name , 
						productcategory_name , prheader_no , prdetails_qty , uom_name , supplierproduct_unitprice , 
						(prpoqty_qty)as current_qty,prpoqty_qty,
						case when isnull(prdetails_qty) then 0 else prdetails_qty end -
						case when isnull(prpoqty_qty) then 0 else (prpoqty_qty) end as req_qty,''0'' as all_qty
						FROM gal_trn_tprheader 
						inner join gal_trn_tprdetails on prheader_gid = prdetails_prheader_gid
						left join gal_trn_tprpoqty on prdetails_gid = prpoqty_prdetails_gid and prpoqty_isremoved = ''N'' 
						left join gal_mst_tproduct on product_gid = prdetails_product_gid and product_isremoved = ''N''
						left join gal_mst_tproducttype on product_producttype_gid = producttype_gid and producttype_isremoved = ''N''
						left join gal_mst_tproductcategory on product_productcategory_gid = productcategory_gid and productcategory_isremoved = ''N''
						left join gal_mst_tuom on product_uom_gid = uom_gid and uom_isremoved = ''N''
						left join gal_map_tsupplierproduct on supplierproduct_product_gid = product_gid and supplierproduct_isremoved = ''N''
						where prheader_status in( ''Approved'',''Draft'') and prheader_isremoved = ''N'' and prdetails_isremoved = ''N'' 
						group by prdetails_product_gid,prdetails_gid 
						');*/
                        
		set Qty_srch = concat(' select prheader_gid,prheader_date,prheader_remarks,prdetails_gid,prpoqty_gid,product_gid,product_name , product_displayname, 
						 prheader_no , prdetails_qty ,  
						sum(prpoqty_qty)as current_qty,prpoqty_qty,
						case when isnull(prdetails_qty) then 0 else prdetails_qty end -
						case when isnull(prpoqty_qty) then 0 else sum(prpoqty_qty) end as req_qty,''0'' as all_qty
						FROM gal_trn_tprheader 
						inner join gal_trn_tprdetails on prheader_gid = prdetails_prheader_gid
						left join gal_trn_tprpoqty on prdetails_gid = prpoqty_prdetails_gid and prpoqty_isremoved = ''N'' 
						inner join gal_mst_tproduct on product_gid = prdetails_product_gid 
						where prheader_status in( ''Approved'',''Draft'') and prheader_isremoved = ''N'' and prdetails_isremoved = ''N'' and product_isremoved = ''N''
						group by prdetails_product_gid,prdetails_gid 
						');
		
                    
		if li_podtl_gid <> 0 then
			set @stmt = concat('select distinct main.prheader_gid , main.prdetails_gid , main.product_gid , main.prpoqty_gid ,main.prheader_date,
								main.product_name , main.prheader_no ,main.prdetails_qty, main.product_displayname,prheader_remarks,
								case when isnull(main.prdetails_qty) then 0 else main.prdetails_qty end - ( 
								case when isnull(main.current_qty) then 0 else main.current_qty end - 
								case when isnull(a.prpoqty_qty) then 0 else a.prpoqty_qty end) as req_qty , 
								case when isnull(a.prpoqty_qty) then 0 else a.prpoqty_qty end as all_qty
								from (' , Qty_srch , ') as main
								left join gal_trn_tprpoqty as a on main.prdetails_gid = a.prpoqty_prdetails_gid and a.prpoqty_isremoved = ''N'' 
                                and a.prpoqty_poheader_gid = ' , li_podtl_gid ,' having req_qty >0');
		else
			set @stmt = concat(Qty_srch,'having req_qty >0');
		end if;
		#select @stmt;
		PREPARE stmt FROM @stmt;
		EXECUTE stmt;
		DEALLOCATE PREPARE stmt;
	else 
		set Message = ls_error;
	end if;
end if;

END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_POReopenView_Get` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_POReopenView_Get`(IN `ls_no` varchar(64),IN `li_sup_name` varchar(64),
IN `ld_amnt` decimal,IN `ls_status` varchar(50),IN `li_emp_gid` int)
BEGIN

#Vigneshwari       22-11-2017

declare Query_search varchar(1000);
declare PO_Reopensrch Text;

set Query_search = '';
if ls_no <> '' then
	set Query_search = concat(' and poheader_no like ''%' , ls_no , '%'''); 
else
	set Query_search = '';
end if;

if li_sup_name <> '' then
	set Query_search = concat(Query_search , ' and supplier_name like ''%' , li_sup_name , '%''' );
else
	set Query_search = concat(Query_search , '');
end if;

if ld_amnt <> 0.00  and ld_amnt <> 0 then
	set Query_search = concat(Query_search , ' and poheader_amount like ''%' , ld_amnt  , '%''');
else
	set Query_search = concat(Query_search , '');
end if;

if ls_status <> '' then
	set Query_search = concat(Query_search , ' and poheader_status like ''%' , ls_status , '%''');
else
	set Query_search = concat(Query_search , '');
end if;

if li_emp_gid <> 0 then
	set Query_search = concat(Query_search , ' and a.create_by = ' , li_emp_gid);
else
	set Query_search = concat(Query_search , '');
end if;

set PO_Reopensrch = ' 	select distinct poheader_gid , poheader_no , poheader_date , poheader_amount , poheader_status ,supplier_name
						from gal_trn_tpoheader as a inner join gal_trn_tpodetails on poheader_gid = podetails_poheader_gid
                        left join gal_mst_tsupplier on poheader_supplier_gid = supplier_gid and supplier_isremoved = ''N''
                        left join gal_trn_tpoclose on poclose_poheader_gid = poheader_gid and poclose_isactive = ''Y'' and poclose_isremoved = ''N''
                        where poheader_isactive = ''Y'' and poheader_isremoved = ''N'' and podetails_isremoved = ''N''
                        and poheader_status in (''Approved'',''REOPENED'') and poheader_close = ''Y'' and poheader_cancel = ''N'' and poheader_approvallater = ''N'' ';

set @stmt = concat(PO_Reopensrch , Query_search,' order by poclose_gid desc');
#select @stmt;
PREPARE stmt FROM @stmt;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_POStatus_Get` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_POStatus_Get`()
BEGIN

#Vigneshwari     21-11-2017

declare query1 varchar(1000);

set query1 =' select poheader_status as status from gal_trn_tpoheader 
				inner join gal_trn_tpodetails on poheader_gid = podetails_poheader_gid
                where poheader_isremoved = ''N'' 
				and poheader_isactive = ''Y'' group by poheader_status ';

set @p = query1;

PREPARE stmt FROM @p;
EXECUTE stmt; 
DEALLOCATE PREPARE stmt;

END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_PRApproval_Get` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_PRApproval_Get`(IN `PR_no` varchar(50),IN `PR_status` varchar(50),IN `li_emp_gid` int)
BEGIN

#Vigneshwari       22-11-2017

declare Query_search varchar(1000);
declare PR_Headersrch varchar(1000);

if PR_status <> '' then
	set Query_search = concat(' and prheader_status like ''%' , PR_status , '%''');
else
	set Query_search = '';
end if;

if PR_no <> '' then
	set Query_search = concat(Query_search , ' and prheader_no like ''%' , PR_no , '%''');
else
	set Query_search = concat(Query_search , '');
end if;

if li_emp_gid <> 0 then
	set Query_search = concat(Query_search , ' and prheader_employee_gid = ' , li_emp_gid);
else
	set Query_search = concat(Query_search , '');
end if;

set PR_Headersrch = ' 	select distinct prheader_gid , prheader_no , prheader_date , employee_name , prheader_status 
				from gal_trn_tprheader inner join gal_trn_tprdetails on prheader_gid = prdetails_prheader_gid
                left join gal_mst_temployee on employee_gid = prheader_employee_gid and employee_isremoved = ''N''
				where prheader_isremoved = ''N'' and prheader_isactive = ''Y''and prdetails_isremoved = ''N'' 
                and (prheader_status = ''Pending for Approval'' )';

set @stmt = concat(PR_Headersrch , Query_search);

PREPARE stmt FROM @stmt;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_PRApproval_Set` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_PRApproval_Set`(IN `Action` varchar(16) , IN `li_PRHeader_gid` int,
IN `ls_remarks` varchar(256),IN `ls_update_by` int ,OUT `Message` varchar(128))
BEGIN

#Vigneshwari       23-11-2017

declare Qry_Header varchar(1000);
declare ls_error varchar(100);
declare countRow int;
declare errno int;

	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO;
    SELECT errno AS MYSQL_ERROR;
    set Message = errno;
    set Message = 'Error';
    ROLLBACK;
    END;

set ls_error = '';

if li_PRHeader_gid = 0 then
	set ls_error = 'PR Header gid not given';
end if;

    if Action = 'Reject' then
		if ls_remarks = '' then
			set ls_error = 'Remarks not Given';
		end if;
	end if;

if ls_error = '' then
	if Action = 'Approve' then
		start transaction;
		update gal_trn_tprheader set prheader_status = 'Approved', prheader_remarks = ls_remarks , update_by = ls_update_by , Update_date = now()
        where prheader_gid = li_PRHeader_gid and prheader_isremoved  ='N';
                       
		set countRow = (select ROW_COUNT());

		if countRow >= 0 then
			set Message = 'Success';
			commit;
		else
			set Message = 'FAIL';
			rollback;
		end if;
    end if;
    
    if Action = 'Reject' then
    
		start transaction;
		update gal_trn_tprheader set prheader_status = 'Rejected' , prheader_remarks = ls_remarks ,
        update_by = ls_update_by , Update_date = now()
        where prheader_gid = li_PRHeader_gid and prheader_isremoved  ='N';
                       
		set countRow = (select ROW_COUNT());

		if countRow >= 0 then
			set Message = 'Success';
			commit;
		else
			set Message = 'FAIL';
			rollback;
		end if;
    end if;
else
	set Message = ls_error;
end if;
END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_PRDelete_Set` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_PRDelete_Set`(IN `li_PRDet_gid` int , IN `ls_emp_gid` varchar(64) , OUT `Message` varchar(100))
BEGIN

#Vigneshwari       14-11-2017

declare chk varchar(1000);
declare PR_DelSrch varchar(1000);
declare countrow int;
declare ls_error varchar(100);
declare prdet_gid int;

set chk = '';
set ls_error = '';

if li_PRDet_gid = 0 then
	set ls_error = ' PR Detail Gid not Given. ';
end if;

if ls_emp_gid = 0 then
	set ls_error = ' Employee Gid not Given. ';
end if;



if ls_error = '' then

select case when isnull(prdetails_prheader_gid) then 0 else prdetails_prheader_gid end into prdet_gid 
		from gal_trn_tprdetails where prdetails_isremoved = 'N' and prdetails_gid = li_PRDet_gid;
select prdet_gid;
	set @Srch = concat('select prdetails_gid from gal_trn_tprdetails where prdetails_isremoved = ''N'' 
						and prdetails_prheader_gid =', prdet_gid);
	PREPARE stmtt FROM @Srch;
	EXECUTE stmtt ;
	set countrow = (select found_rows());
	DEALLOCATE PREPARE stmtt;
select countrow;
if countrow = 1 then

	start transaction;
    
    Update gal_trn_tprdetails set prdetails_isremoved = 'Y' , update_by = ls_emp_gid , 
					 Update_date = now() where prdetails_gid = li_PRDet_gid;
    
	set PR_DelSrch = concat('  Update gal_trn_tprheader set prheader_isremoved = ''Y'' , update_by = ''' ,ls_emp_gid , 
					''' , Update_date = now() where prheader_gid = ',prdet_gid );
	set @q = PR_DelSrch;
	PREPARE stmtt FROM @q;
	EXECUTE stmtt ;
	set countrow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmtt;
	if countrow > 0 then
		set  Message = 'DELETION_DONE';
        commit;
	else
		set Message = 'NO_DELETION';
        rollback;
	end if;
else

	start transaction;
	set PR_DelSrch = concat('  Update gal_trn_tprdetails set prdetails_isremoved = ''Y'' , update_by = ''' ,ls_emp_gid , 
					''' , Update_date = now() where prdetails_gid = ',li_PRDet_gid );
	set @q = PR_DelSrch;
	PREPARE stmtt FROM @q;
	EXECUTE stmtt ;
	set countrow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmtt;
	if countrow > 0 then
		set  Message = 'DELETION_DONE';
        commit;
	else
		set Message = 'NO_DELETION';
        rollback;
	end if;

end if;


else
	set Message = ls_error; 
end if;

END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_PRDetailUpdate_Set` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_PRDetailUpdate_Set`(IN `li_PRDtil_gid` int,
IN `li_prod_gid` int,IN `li_qty` int,OUT `Message` varchar(128))
BEGIN

#Vigneshwari       14-11-2017

declare Qry_Header varchar(1000);
declare countRow int;
declare ls_error varchar(100);
declare errno int;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO;
    SELECT errno AS MYSQL_ERROR;
    set Message = errno;
    ROLLBACK;
    END;

set ls_error = '';
if li_PRDtil_gid = 0 then
	set ls_error = 'Purchase Request Details Data Not Passed.';
end if;

if li_qty = 0 then
	set ls_error = 'Quantity Not Correct.';
end if;

if li_prod_gid = 0 then
	set ls_error = 'Product Not Selected.';
end if;

if ls_error = '' then
	start transaction;

	Update gal_trn_tprdetails set prdetails_qty = li_qty , prdetails_product_gid = li_prod_gid
	where prdetails_gid  = li_PRDtil_gid and prdetails_isremoved  ='N';

	set countRow = (select ROW_COUNT()) ;
	set Message = countRow;

	if countRow = 1 then
		set Message = ''',SUCCESS';
		commit;
	else 
		set Message = 'NO CHANGE';
        rollback;
	end if;
else
	set Message = ls_error;
end if;
END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_PRDetail_Get` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_PRDetail_Get`(IN `li_prheader_gid` int,IN `ls_prod_name` varchar(128),IN `li_emp_gid` int,
OUT `Message` varchar(128))
BEGIN

#Vigneshwari       18-11-2017

declare Query_search varchar(1000);
declare PR_Headersrch Text;
declare ls_error varchar(128);

set ls_error = '';

if li_prheader_gid <> 0 then
	set Query_search = concat(' and prheader_gid = ' , li_prheader_gid);
else
	set ls_error = '';
end if;

if ls_prod_name <> '' then
	set Query_search = concat(Query_search , ' and product_name like ''%' , ls_prod_name , '%''');
else
	set Query_search = concat(Query_search , '');
end if;

if li_emp_gid <> '' then
	set Query_search = concat(Query_search , ' and prheader_employee_gid ' , li_emp_gid);
else
	set Query_search = concat(Query_search , '');
end if;

if ls_error = '' then

	set PR_Headersrch = ' 	select distinct prheader_gid ,prdetails_gid, prdetails_qty , product_name ,producttype_name , employee_name,prheader_remarks,
						prheader_date,productcategory_name ,uom_name,prheader_no ,product_gid ,producttype_gid ,productcategory_gid,prheader_status 
                        from gal_trn_tprheader inner join gal_trn_tprdetails on prheader_gid = prdetails_prheader_gid
                        left join gal_mst_tproduct on prdetails_product_gid = product_gid and product_isremoved = ''N''
                        left join gal_mst_tproducttype on product_producttype_gid = producttype_gid and producttype_isremoved = ''N''
                        left join gal_mst_tproductcategory on producttype_productcategory_gid = productcategory_gid and productcategory_isremoved = ''N''
                        left join gal_mst_tuom on product_uom_gid = uom_gid and uom_isremoved = ''N''
                        left join gal_mst_temployee on employee_gid = prheader_employee_gid and employee_isremoved = ''N''
                        where prheader_isremoved = ''N'' and prheader_isactive = ''Y'' and prdetails_isremoved = ''N''';

	set @stmt = concat(PR_Headersrch , Query_search);
    #select @stmt;
	PREPARE stmt FROM @stmt;
	EXECUTE stmt;
	DEALLOCATE PREPARE stmt;
	set Message = 'done';
else
	set Message = ls_error ;
end if;

END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_PRDetail_Set` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_PRDetail_Set`(IN `li_PRHeaderMAX_gid` int,
IN `li_product_gid` int,IN `li_quantity` int,IN `li_entity_gid` int,IN `ls_create_by` int ,OUT `Message` varchar(128))
BEGIN

#Vigneshwari       14-11-2017

declare Qry_Header varchar(1000);
declare ls_error varchar(100);
declare countRow int;
declare errno int;

	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO;
    SELECT errno AS MYSQL_ERROR;
    set Message = errno;
    ROLLBACK;
    END;

set ls_error = '';

if li_PRHeaderMAX_gid = 0 or li_PRHeaderMAX_gid = '' then
	set ls_error = 'PR Header Not Selected.';
else 
	set @err = concat('select prheader_gid from gal_trn_tprheader where prheader_gid =''', li_PRHeaderMAX_gid ,'''' , ' group by prheader_gid' );
    PREPARE stmt1 FROM @err;
	EXECUTE stmt1;  
	set countRow = (select found_rows());
	DEALLOCATE PREPARE stmt1;
    if countRow <= 0 then
		set ls_error = 'PR Header No not found in Header';
	end if;
end if;

if li_product_gid = 0 then
	set ls_error = 'Product Not Selected.';
end if;

if li_quantity <= 0 then
	set ls_error = 'Quantity entered is not in correct form.';
end if;
if ls_error = '' then
	start transaction;
	set Qry_Header = concat('INSERT INTO gal_trn_tprdetails(prdetails_prheader_gid, prdetails_product_gid, prdetails_qty, 
						entity_gid, create_by) VALUES
                        (',li_PRHeaderMAX_gid,',',li_product_gid,',',li_quantity,',',li_entity_gid,',',ls_create_by,')');
                       
	set @Qry_Header = Qry_Header;
    PREPARE stmt FROM @Qry_Header;
	EXECUTE stmt;  
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt; 

	if countRow > 0 then
		select LAST_INSERT_ID() into Message ;
        set Message = CONCAT(Message,',SUCCESS');
        commit;
	else
		set Message = 'FAIL';
        rollback;
	end if;
else
	set Message = ls_error;
end if;





END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_PRHeaderUpdate_Set` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_PRHeaderUpdate_Set`(IN `Action` varchar(16),IN `li_prhdr_gid` int,
OUT `Message` varchar(1000))
BEGIN

#Vigneshwari       22-11-2017

declare ls_error varchar(100);
declare countRow int;
declare errno int;
declare msg varchar(1000);

	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
    set Message = concat(errno , msg);
    ROLLBACK;
    END;

if Action = 'submit' then
		start transaction;
			Update gal_trn_tprheader set prheader_status = 'Pending for Approval' where prheader_gid  = li_prhdr_gid
				and prheader_isremoved  ='N';

		set countRow = (select ROW_COUNT());
		if countRow >=  0 then
			set Message = 'Success';
			commit;
		else
			set Message = 'FAIL';
			rollback;
		end if;
end if;

if Action = 'draft' then
		start transaction;
			Update gal_trn_tprheader set prheader_status = 'Draft' where prheader_gid  = li_prhdr_gid
				and prheader_isremoved  ='N';

		set countRow = (select ROW_COUNT());
		if countRow >=  0 then
			set Message = 'Success';
			commit;
		else
			set Message = 'FAIL';
			rollback;
		end if;
end if;

END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_PRHeader_Get` */;
 CREATE DEFINER=`root`@`%` PROCEDURE `sp_PRHeader_Get`(IN `PR_no` varchar(50),IN `PR_status` varchar(64),IN `li_emp_gid` int)
BEGIN

#Vigneshwari       14-11-2017

declare Query_search varchar(1000);
declare PR_Headersrch varchar(1000);

if PR_status <> '' then
	set Query_search = concat(' and prheader_status like ''%' , PR_status , '%''');
else
	set Query_search = '';
end if;

if PR_no <> '' then
	set Query_search = concat(Query_search , ' and prheader_no like ''%' , PR_no , '%''');
else
	set Query_search = concat(Query_search , '');
end if;

if li_emp_gid <> '' then
	set Query_search = concat(Query_search , ' and prheader_employee_gid =' , li_emp_gid);
else
	set Query_search = concat(Query_search , '');
end if;

set PR_Headersrch = ' 	select distinct prheader_gid , prheader_no , prheader_date , employee_name , prheader_status 
				from gal_trn_tprheader inner join gal_trn_tprdetails on prheader_gid = prdetails_prheader_gid
                left join gal_mst_temployee on employee_gid = prheader_employee_gid and employee_isremoved = ''N''
				where prheader_isremoved = ''N'' and prheader_isactive = ''Y''and prdetails_isremoved = ''N'' 
                and prheader_status in (''Approved'',''Pending for Approval'',''Draft'',''Rejected'')
                ';

set @stmt = concat(PR_Headersrch , Query_search);

PREPARE stmt FROM @stmt;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_PRHeader_Set` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_PRHeader_Set`(IN `Action` varchar(16),IN `li_date` datetime,
IN `li_emp_gid` int,IN `ls_status` varchar(64),IN `li_entity_gid` varchar(10),IN `ls_create_by` int,OUT `Message` varchar(1000))
BEGIN

#Vigneshwari       14-11-2017

declare Qry_Header varchar(1000);
declare ls_error varchar(100);
declare countRow int;
declare ls_no varchar(64);
declare errno int;
declare msg varchar(1000);

	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
    set Message = concat(errno ,',', msg);
    ROLLBACK;
    END;

set ls_error = '';

if Action = 'submit' then

	call sp_Generate_number_get('PR','000',@Message);
	select @Message into ls_no from dual;
    
    if ls_no = '' then
		set ls_error = ' PR Header No not Given. ';
	else 
		set @err = concat('select prheader_gid from gal_trn_tprheader where prheader_no =''', ls_no ,'''' , ' group by prheader_no' );
		#select @err;
        PREPARE stmt1 FROM @err;
		EXECUTE stmt1;  
		set countRow = (select found_rows());
		DEALLOCATE PREPARE stmt1;
		if countRow > 0 then
			set ls_error = ' Duplicate PR Header No ';
		end if;
	end if;

	if li_date = 0 or li_date = '' then
		set ls_error = ' PR Header Date Not Given. ';
	end if;
	
	if li_emp_gid = 0 then
		set ls_error = ' Employee Not Selected. ';
	end if;
	
	if ls_status = '' then
		set ls_error = 'Status Not Selected.';
	end if;
	
    
    if ls_status='submit' then
    
    set ls_status='Pending for Approval';
      end if;
      
   
	if ls_error = '' then
		start transaction;
		set Qry_Header = concat('INSERT INTO gal_trn_tprheader(prheader_no, prheader_date, prheader_employee_gid,
								prheader_status, entity_gid, create_by)VALUES
								(''',ls_no,''',''',li_date,''',',li_emp_gid,',''Pending for Approval'',',li_entity_gid,',',ls_create_by,')');

		set @Qry_Header = Qry_Header;
		PREPARE stmt FROM @Qry_Header;
		EXECUTE stmt;  
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt; 

		if countRow >  0 then
			select LAST_INSERT_ID() into Message ;
            set Message = CONCAT(Message,',SUCCESS');
			commit;
		else
			set Message = 'FAIL';
			rollback;
		end if;
	else
		set Message = ls_error;
	end if;
end if;

if Action = 'draft' then

	call sp_Generate_number_get('PR','000',@Message);
	select @Message into ls_no from dual;
    
    if ls_no = '' then
		set ls_error = ' PR Header No not Given. ';
	else 
		set @err = concat('select prheader_gid from gal_trn_tprheader where prheader_no =''', ls_no ,'''' , ' group by prheader_no' );
		#select @err;
        PREPARE stmt1 FROM @err;
		EXECUTE stmt1;  
		set countRow = (select found_rows());
		DEALLOCATE PREPARE stmt1;
		if countRow > 0 then
			set ls_error = ' Duplicate PR Header No ';
		end if;
	end if;

	if li_date = 0 or li_date = '' then
		set ls_error = ' PR Header Date Not Given. ';
	end if;
	
	if li_emp_gid = 0 then
		set ls_error = ' Employee Not Selected. ';
	end if;
	
	if ls_status = '' then
		set ls_error = 'Status Not Selected.';
	end if;
	 if ls_status='draft' then
     set ls_status='Draft';
    end if;
	if ls_error = '' then
		start transaction;
		set Qry_Header = concat('INSERT INTO gal_trn_tprheader(prheader_no, prheader_date, prheader_employee_gid,
								prheader_status, entity_gid, create_by)VALUES
								(''',ls_no,''',''',li_date,''',',li_emp_gid,',''Draft'',',li_entity_gid,',',ls_create_by,')');
	
	
		set @Qry_Header = Qry_Header;
		PREPARE stmt FROM @Qry_Header;
		EXECUTE stmt;  
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt; 

		if countRow >  0 then
			select LAST_INSERT_ID() into Message ;
            set Message = CONCAT(Message,',SUCCESS');
			commit;
		else
			set Message = 'FAIL';
			rollback;
		end if;
	else
		set Message = ls_error;
	end if;
end if;

if Action = 'request' then

	call sp_Generate_number_get('PR','000',@Message);
	select @Message into ls_no from dual;
    
    if ls_no = '' then
		set ls_error = ' PR Header No not Given. ';
	else 
		set @err = concat('select prheader_gid from gal_trn_tprheader where prheader_no =''', ls_no ,'''' , ' group by prheader_no' );
		PREPARE stmt1 FROM @err;
		EXECUTE stmt1;  
		set countRow = (select found_rows());
		DEALLOCATE PREPARE stmt1;
		if countRow > 0 then
			set ls_error = ' Duplicate PR Header No ';
		end if;
	end if;

	if li_date = 0 or li_date = '' then
		set ls_error = ' PR Header Date Not Given. ';
	end if;
	
	if li_emp_gid = 0 then
		set ls_error = ' Employee Not Selected. ';
	end if;
	
	if ls_status = '' then
		set ls_error = 'Status Not Selected.';
	end if;
	
	if ls_error = '' then
		start transaction;
		set Qry_Header = concat('INSERT INTO gal_trn_tprheader(prheader_no, prheader_date, prheader_employee_gid,
								prheader_status, entity_gid, create_by)VALUES
								(''',ls_no,''',''',li_date,''',',li_emp_gid,',''',ls_status,''',',li_entity_gid,',',ls_create_by,')');
	
	
		set @Qry_Header = Qry_Header;
		PREPARE stmt FROM @Qry_Header;
		EXECUTE stmt;  
		set countRow = (select found_rows());
		DEALLOCATE PREPARE stmt; 

		if countRow >  0 then
			select LAST_INSERT_ID() into Message ;
            set Message = CONCAT(Message,',SUCCESS');
			commit;
		else
			set Message = 'FAIL';
			rollback;
		end if;
	else
		set Message = ls_error;
	end if;
end if;

END ;;

 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_PRPOQty_Set` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_PRPOQty_Set`(IN `Action` varchar(16),IN `li_POHdr_gid` int,
IN `li_PODtl_gid` int,IN `li_PRDtl_gid` int,IN `li_qty_gid` int,IN `li_entity_gid` int,IN `ls_create_by` int,
IN `li_prpo_gid` int,OUT `Message` varchar(128))
BEGIN

#Vigneshwari       20-11-2017

declare Qry_Header varchar(1000);
declare ls_error varchar(100);
declare countRow int;
declare errno int;
declare msg varchar(1000);

	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
    set Message = concat(errno , msg);
    ROLLBACK;
    END;

set ls_error = '';

if Action = 'Insert' then

if li_POHdr_gid = 0 then
	set li_POHdr_gid = ' PO Header gid not Given. ';
else 
	set @err = concat('select * from gal_trn_tpoheader where poheader_gid =''', li_POHdr_gid ,'''' , ' group by poheader_gid' );
    PREPARE stmt1 FROM @err;
	EXECUTE stmt1;  
	set countRow = (select found_rows());
	DEALLOCATE PREPARE stmt1;
    if countRow = 0 then
		set ls_error = ' PO Header gid is not in table ';
    end if;
end if;

if li_PODtl_gid = 0 then
	set li_PODtl_gid = ' PO detail gid not Given. ';
else 
	set @err = concat('select * from gal_trn_tpodetails where podetails_gid =''', li_PODtl_gid ,'''' , ' group by podetails_gid' );
    PREPARE stmt1 FROM @err;
	EXECUTE stmt1;  
	set countRow = (select found_rows());
	DEALLOCATE PREPARE stmt1;
    if countRow = 0 then
		set ls_error = ' PO Detail gid is not in table ';
    end if;
end if;

if li_PRDtl_gid = 0 then
	set li_PRDtl_gid = ' PR detail gid not Given. ';
else 
	set @err = concat('select * from gal_trn_tprdetails where prdetails_gid =''', li_PRDtl_gid ,'''' , ' group by prdetails_gid' );
    PREPARE stmt1 FROM @err;
	EXECUTE stmt1;  
	set countRow = (select found_rows());
	DEALLOCATE PREPARE stmt1;
    if countRow = 0 then
		set ls_error = ' PR Detail gid is not in table ';
    end if;
end if;

if li_qty_gid = 0 then
	set ls_error = 'Quantity not given ';
end if;

if ls_error = '' then
	start transaction;
	set Qry_Header = concat('INSERT INTO gal_trn_tprpoqty(prpoqty_poheader_gid , prpoqty_podetails_gid , prpoqty_prdetails_gid , 
							prpoqty_qty , entity_gid , create_by) VALUES 
                            (''' , li_POHdr_gid , ''',''' , li_PODtl_gid , ''',' , li_PRDtl_gid , ',' , li_qty_gid , ',
                            ' , li_entity_gid , ',' , ls_create_by , ')');

	set @Qry_Header = Qry_Header;
	PREPARE stmt FROM @Qry_Header;
	EXECUTE stmt;  
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt; 

	if countRow >  0 then
		select LAST_INSERT_ID() into Message ;
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

if li_prpo_gid = 0 then
	set ls_error = 'PRPO gid Not Selected.';
end if;

if ls_error = '' then
	start transaction;
    
    update gal_trn_tprpoqty set prpoqty_qty = li_qty_gid , 
    update_by = ls_create_by , Update_date = now() where prpoqty_gid = li_prpo_gid;
 
	set countRow = (select ROW_COUNT()) ;
		if countRow = 1 then
		
			set Message = 'SUCCESS';
			commit;
		else 
			set Message = 'NO CHANGE';
			rollback;
		end if;
else
	set Message = ls_error;
end if;
end if;


if Action = 'Delete' then

if li_prpo_gid = 0 then
	set ls_error = 'PRPO gid Not Selected.';
end if;

if ls_error = '' then
	start transaction;
	set SQL_SAFE_UPDATES=0;

    update gal_trn_tprpoqty set prpoqty_isremoved = 'Y' , 
    update_by = ls_create_by , Update_date = now()  where prpoqty_podetails_gid = li_PODtl_gid;
 
	set countRow = (select ROW_COUNT()) ;
		if countRow = 1 then
		
			set Message = 'SUCCESS';
			
		else 
			set Message = 'NO CHANGE';
		
		end if;
else
	set Message = ls_error;
end if;
end if;


END ;;
 
 
/*!50003 DROP PROCEDURE IF EXISTS `sp_PRStatus_Get` */;
 

CREATE DEFINER=`root`@`%` PROCEDURE `sp_PRStatus_Get`()
BEGIN

#Vigneshwari     21-11-2017

declare query1 varchar(1000);

set query1 =' select prheader_status as status from gal_trn_tprheader 
				inner join gal_trn_tprdetails on prheader_gid = prdetails_prheader_gid 
                where prheader_isremoved = ''N'' 
				and prheader_isactive = ''Y'' group by prheader_status ';

set @p = query1;

PREPARE stmt FROM @p;
EXECUTE stmt; 
DEALLOCATE PREPARE stmt;

END ;;
 