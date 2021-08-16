CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Partner_Approval_Get`(in Action  varchar(16),
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_Atma_Partner_Approval_Get:BEGIN

#Balamaniraja      11-07-19

Declare Query_Select varchar(5000);
Declare Query_Search varchar(5000);
Declare Query_Update varchar(5000);
Declare countRow varchar(5000);

Declare ls_count int;


if Action='Partner_Get' then


			select JSON_LENGTH(lj_filter,'$') into @li_json_count;
			select JSON_LENGTH(lj_classification,'$') into @li_json_lj_classification_count;

            if @li_json_lj_classification_count = 0 or @li_json_lj_classification_count = ''
           or @li_json_lj_classification_count is null  then
			set Message = 'No Entity_Gid In Json. ';
			leave sp_Atma_Partner_Approval_Get;
		End if;

          if @li_json_lj_classification_count is not null or @li_json_lj_classification_count <> ''
			 or @li_json_lj_classification_count <> 0 then

             select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Entity_Gid')))
             into @Entity_Gid;

		  end if;


    if @li_json_count is not null or @li_json_count <> '' or @li_json_count <> 0 then
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partner_Type'))) into @Partner_Type;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partner_Code'))) into @Partner_Code;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partner_Name'))) into @Partner_Name;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partner_Status'))) into @Partner_Status;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partner_Panno'))) into @Partner_Panno;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partner_Renewdate'))) into @Partner_Renewdate;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partner_Rmname'))) into @Partner_Rmname;


			set Query_Search = '';

        if @Partner_Type is not null or @Partner_Type <> '' then

			set Query_Search = concat(Query_Search,' and a.Partner_Type = ''',@Partner_Type,'''  ');
		End if;


        if @Partner_Code is not null or @Partner_Code <> '' then
			set Query_Search = concat(Query_Search,' and a.Partner_Code = ''',@Partner_Code,'''  ');
        End if;


        if @Partner_Name is not null or @Partner_Name <> '' then
			set Query_Search = concat(Query_Search,' and a.Partner_Name = ''',@Partner_Name,'''  ');
        End if;


        if @Partner_Status is not null or @Partner_Status <> '' then
			set Query_Search = concat(Query_Search,' and a.Partner_Status = ''',@Partner_Status,'''  ');
        End if;


        if @Partner_Panno is not null or @Partner_Panno <> '' then
			set Query_Search = concat(Query_Search,' and a.Partner_Panno = ''',@Partner_Panno,'''  ');
        End if;


        #if @Partner_Renewdate is not null or @Partner_Renewdate <> '' then
			#set Query_Search = concat(Query_Search,' and a.Partner_Renewdate = ''',@Partner_Renewdate,'''  ');
        #End if;


        if @Partner_Renewdate is not null or @Partner_Renewdate <> '' then

		set @Partner_Renewdate=date_format(@Partner_Renewdate,'%Y-%m-%d');

		set Query_Search=concat(Query_Search,'and a.Partner_Renewdate =' '''',@Partner_Renewdate,'''');
        End if;



        if @Partner_Rmname is not null or @Partner_Rmname <> '' then
			set Query_Search = concat(Query_Search,'and a.Partner_Rmname = ''',@Partner_Rmname,'''  ');
        End if;

    End if;


	set Query_Select = '';
	set Query_Select =concat('select a.partner_gid,a.partner_code, a.partner_name, a.partner_panno, a.partner_compregno,a.partner_group,
							  a.partner_custcategorygid, a.partner_Classification, a.partner_type,
							  a.partner_web,if (a.partner_activecontract =''Y'',''Yes'',''No'') partner_activecontract, a.partner_reason_no_contract,
							  a.partner_contractdatefrom,a.partner_contractdateto, a.partner_aproxspend,
							  a.partner_actualspend, a.partner_noofdir, a.partner_orgtype,
							  a.partner_renewaldate, a.partner_remarks, a.partner_status,
							  a.partner_renewdate, a.partner_rmname, e.employee_name,
                              emp.employee_name as create_by_emp_name
                              ,c.custcategory_name from atma_tmp_tpartner a
                              inner join gal_mst_temployee e on a.partner_rmname=e.employee_gid
                              inner join gal_mst_temployee emp on a.create_by=emp.employee_gid
                              inner join gal_mst_tcustcategory c on a.partner_custcategorygid=c.custcategory_gid
                              where a.partner_isactive=''Y'' and a.partner_isremoved=''N''
                              and a.entity_gid=',@Entity_Gid,' and
                              e.employee_isactive=''Y'' and e.employee_isremoved=''N''
                              and e.entity_gid=',@Entity_Gid,' and
                              c.custcategory_isactive=''Y'' and custcategory_isremoved=''N'' and
                              emp.employee_isactive=''Y'' and emp.employee_isremoved=''N''
                              and emp.entity_gid=',@Entity_Gid,' and a.partner_status=''Pending'' ',Query_Search,'
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
end if;


END