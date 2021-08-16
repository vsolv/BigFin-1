CREATE  PROCEDURE `sp_Atma_Partner_Get`(in Action  varchar(25),
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_Atma_Partner_Get:BEGIN



Declare Query_Select varchar(50000);
Declare Query_Search varchar(50000);
Declare Query_Table varchar(50000);
Declare Query_Table1 varchar(50000);
Declare Query_Table2 varchar(50000);
Declare Query_Column varchar(5000);
Declare Query_Limit varchar(5000);
Declare Query_Update varchar(5000);
Declare countRow varchar(5000);
declare v_role_name varchar(128);
DECLARE finished INTEGER DEFAULT 0;
Declare ls_count int;
declare P_status varchar(5000);

select JSON_LENGTH(lj_filter,'$') into @li_json_count;
	select JSON_LENGTH(lj_classification,'$') into @li_json_lj_classification_count;
    if @li_json_lj_classification_count = 0 or @li_json_lj_classification_count = ''
		or @li_json_lj_classification_count is null  then
		   set Message = 'No Data In Json. ';
		leave sp_Atma_Partner_Get;
	End if;
	select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Entity_Gid')))  into @Entity_Gid;
    select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Login_By')))  into @Login_By;
    select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Create_By')))  into @Create_By;
	select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Mst_Table')))into @Mst_Table;
	select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partner_Gid'))) into @Partner_Gid;
	select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partner_Status'))) into @Partner_Status;
	select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partner_RequestFor'))) into @Partner_RequestFor;
	select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partner_Main_Status'))) into @Partner_Main_Status;
	select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partner_Type'))) into @Partner_Type;
	select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partner_Code'))) into @Partner_Code;
	select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partner_Name'))) into @Partner_Name;
	select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partner_Panno'))) into @Partner_Panno;
	select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partner_Renewdate'))) into @Partner_Renewdate;
	select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partner_Rmname'))) into @Partner_Rmname;


   set Query_Table='';

	if @Mst_Table='Mst' then
		set Query_Table = concat('atma_mst_tpartner');
	else
		set Query_Table = concat('atma_tmp_tpartner');
	End if;

    if @Mst_Table='Mst' then
		set Query_Table1 = concat('gal_mst_taddress');
	else
		set Query_Table1 = concat('atma_tmp_mst_taddress');
	End if;

	if @Mst_Table='Mst' then
		set Query_Table2 = concat('gal_mst_tcontact');
	else
		set Query_Table2 = concat('atma_tmp_mst_tcontact');
	End if;

            set Query_Column='';
            if @Mst_Table is null or @Mst_Table=''   then
				set Query_Column = concat(',a.main_partner_gid');
			End if;


		set Query_Search = '';

        if @Partner_Gid is not null or @Partner_Gid <> '' then
			set Query_Search = concat(Query_Search,' and p.partner_gid = ''',@Partner_Gid,'''  ');
		End if;

        if @Partner_Type is not null or @Partner_Type <> '' then
			set Query_Search = concat(Query_Search,' and a.Partner_Type = ''',@Partner_Type,'''  ');
		End if;

        if @Partner_Code is not null or @Partner_Code <> '' then
			set Query_Search = concat(Query_Search,' and p.Partner_Code = ''',@Partner_Code,'''  ');
        End if;

        if @Partner_Name is not null or @Partner_Name <> '' then
			set Query_Search = concat(Query_Search,' and p.Partner_Name = ''',@Partner_Name,'''  ');
        End if;

        if @Partner_RequestFor is not null or @Partner_RequestFor <> '' then
			set Query_Search = concat(Query_Search,' and a.partner_requestfor = ''',@Partner_RequestFor,'''  ');
        End if;

        if @Partner_Main_Status is not null or @Partner_Main_Status <> '' then
			set Query_Search = concat(Query_Search,' and p.partner_mainstatus = ''',@Partner_Main_Status,'''  ');
        End if;

        if @Partner_Panno is not null or @Partner_Panno <> '' then
			set Query_Search = concat(Query_Search,' and p.Partner_Panno = ''',@Partner_Panno,'''  ');
        End if;

        if @Partner_Renewdate is not null or @Partner_Renewdate <> '' then
			set @Partner_Renewdate=date_format(@Partner_Renewdate,'%Y-%m-%d');
			set Query_Search=concat(Query_Search,'and p.Partner_Renewdate =' '''',@Partner_Renewdate,'''');
        End if;


        if @Create_By is not null or @Create_By <> '' then
			set Query_Search = concat(Query_Search,' and p.create_by = ',@Create_By,'  ');
        End if;

if Action='Partner_Get' then

		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Page_Index'))) into @Page_Index ;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Page_Size'))) into @Page_Size ;

	if @Partner_Rmname is not null or @Partner_Rmname <> '' then
		set Query_Search = concat(Query_Search,'and p.Partner_Rmname = ''',@Partner_Rmname,'''  ');
	End if;
	if @Partner_Status is not null or @Partner_Status <> '' then
		set Query_Search = concat(Query_Search,' and p.Partner_Status =''',@Partner_Status,'''');
    End if;



					set Query_Limit='';
				#select @Page_Index,@Page_Size;
					if @Page_Index <> '' and @Page_Index is not null and @Page_Size <> '' and @Page_Size is not null  then

									 set @total_size= @Page_Index*@Page_Size;
                                     set @Page_Size=@Page_Size;
									 set Query_Limit = concat(Query_Limit,' LIMIT ',@Page_Size,' OFFSET ',@total_size,'  ');

					else
									#select 1;
									set @Page_Index=2,@Page_Size=5;
									#select @Page_Index,@Page_Size;
									set @total_size= @Pae_Index*@Page_Size;
									#select @total_size;
									set Query_Limit = concat(Query_Limit,' LIMIT ',@Page_Size,' OFFSET ',@total_size,'  ');
					End if;

			#select @Page_Index,@Page_Size, Query_Limit;

	set Query_Select = '';
	set Query_Select =concat('select p.partner_gid,p.contact_reftablecode,p.Contact_contacttype_gid,
									  p.Contact_personname,p.Contact_mobileno,p.Contact_email,p.Contact_designation_gid,
                                      p.Contact_landline,p.Contact_landline2,p.Contact_mobileno2,
                                      p.Contact_DOB,p.Contact_WD,p.address_1,p.address_2,p.address_3,
                                      p.address_pincode,p.address_city_gid,
                                      p.address_state_gid,p.address_district_gid,dis.district_name,s.state_name,cty.City_Name
                                      ,ct.contacttype_Name,des.designation_name,p.partner_code,p.partner_name,p.partner_panno,
								p.partner_compregno,p.partner_group, p.partner_custcategorygid,p.partner_compositevendor,
								p.partner_Classification, p.partner_type, p.partner_web,
								 p.partner_activecontract
                                , p.partner_reason_no_contract,
								p.partner_contractdatefrom, p.partner_contractdateto,
								p.partner_aproxspend, p.partner_actualspend, p.partner_noofdir,
								p.partner_orgtype, p.partner_renewaldate, p.partner_remarks,
								p.partner_requestfor, p.partner_status, p.partner_mainstatus,
								p.partner_renewdate, p.partner_rmname, p.partner_isactive,
								p.partner_isremoved, p.entity_gid, p.create_by, p.create_date,
								p.update_by, p.update_date,
								e.employee_name,emp.employee_name as create_by_emp_name,
							    c.custcategory_name   from
							(select partner_addressgid,partner_contactgid,partner_gid, partner_code, partner_name,
                            case
                            when partner_compositevendor =''R'' then ''Registered-Regular''
                            when partner_compositevendor =''C'' then ''Registered-Composite''
                            when partner_compositevendor =''U'' then ''UnRegistered'' end
                            partner_compositevendor,
							partner_panno, partner_compregno, partner_group,
                            partner_custcategorygid, partner_Classification, partner_type,
                            partner_web, case
                            when partner_activecontract =''Y'' then ''Yes''
                            when partner_activecontract =''N'' then ''No'' end
                            partner_activecontract, partner_reason_no_contract,
                            partner_contractdatefrom, partner_contractdateto, partner_aproxspend,
                            partner_actualspend, partner_noofdir, partner_orgtype, partner_renewaldate,
                            partner_remarks, partner_requestfor, partner_status, partner_mainstatus,
                            partner_renewdate, partner_rmname, partner_isactive, partner_isremoved,
                            mst.entity_gid,mst.create_by,mst.create_date,mst.update_by,
                            mst.update_date,null as main_partner_gid,
                            mcon.contact_reftablecode,mcon.Contact_contacttype_gid,
									  mcon.Contact_personname,mcon.Contact_mobileno,mcon.Contact_email,mcon.Contact_designation_gid,
                                      mcon.Contact_landline,mcon.Contact_landline2,mcon.Contact_mobileno2,
                                      mcon.Contact_DOB,mcon.Contact_WD,ma.address_1,ma.address_2,ma.address_3,
                                      ma.address_pincode,ma.address_city_gid,
                                      ma.address_state_gid,ma.address_district_gid

                            from atma_mst_tpartner mst
                            inner join  gal_mst_tcontact mcon on mcon.contact_gid=mst.partner_contactgid
							inner join gal_mst_taddress ma on mst.partner_addressgid=ma.address_gid
                            where mst.create_by=',@Create_By,'
							and mst.partner_code not in
								(SELECT   m.partner_code
								FROM  atma_tmp_tpartner t inner join atma_mst_tpartner m
								on m.partner_code=t.partner_code
								where m.create_by=',@Create_By,')
							union
								select tmp.partner_addressgid,tmp.partner_contactgid,tmp.partner_gid,tmp.partner_code,
                                tmp.partner_name,case
							when tmp.partner_compositevendor =''R'' then ''Registered-Regular''
                            when tmp.partner_compositevendor =''C'' then ''Registered-Composite''
                            when tmp.partner_compositevendor =''U'' then ''UnRegistered'' end
                            partner_compositevendor,
							tmp.partner_panno,tmp.partner_compregno,tmp.partner_group,
                            tmp.partner_custcategorygid, tmp.partner_Classification, tmp.partner_type,
                            tmp.partner_web,case
                            when tmp.partner_activecontract =''Y'' then ''Yes''
                            when tmp.partner_activecontract =''N'' then ''No'' end
                            partner_activecontract,tmp.partner_reason_no_contract,
                            tmp.partner_contractdatefrom,tmp.partner_contractdateto,tmp.partner_aproxspend,
                            tmp.partner_actualspend,tmp.partner_noofdir,tmp.partner_orgtype, tmp.partner_renewaldate,
                            tmp.partner_remarks, tmp.partner_requestfor, tmp.partner_status, tmp.partner_mainstatus,
                            tmp.partner_renewdate, tmp.partner_rmname, tmp.partner_isactive, tmp.partner_isremoved,
                            tmp.entity_gid,tmp.create_by,tmp.create_date, tmp.update_by, tmp.update_date, tmp.main_partner_gid ,
							tcon.contact_reftablecode,tcon.Contact_contacttype_gid,
									  tcon.Contact_personname,tcon.Contact_mobileno,tcon.Contact_email,tcon.Contact_designation_gid,
                                      tcon.Contact_landline,tcon.Contact_landline2,tcon.Contact_mobileno2,
                                      tcon.Contact_DOB,tcon.Contact_WD,ta.address_1,ta.address_2,ta.address_3,
                                      ta.address_pincode,ta.address_city_gid,
                                      ta.address_state_gid,ta.address_district_gid
                            from atma_tmp_tpartner tmp
                            inner join  atma_tmp_mst_tcontact tcon on tcon.contact_gid=tmp.partner_contactgid
							inner join atma_tmp_mst_taddress ta on tmp.partner_addressgid=ta.address_gid
                            where tmp.create_by=',@Create_By,') p

                                inner join  gal_mst_tstate s on p.address_state_gid=s.state_gid
								inner join  gal_mst_tcity cty  on p.address_city_gid=cty.city_gid
								inner join  gal_mst_tdistrict dis  on p.address_district_gid=dis.district_gid
								inner join  gal_mst_tcontacttype ct  on p.Contact_contacttype_gid=ct.contacttype_gid
                                and ct.contacttype_isactive=''Y'' and ct.contacttype_isremoved=''N'' and ct.entity_gid=',@Entity_Gid,'
								inner join  gal_mst_tdesignation des  on p.Contact_designation_gid=des.designation_gid
                                and des.designation_isactive=''Y'' and des.designation_isremoved=''N'' and des.entity_gid=',@Entity_Gid,'
							    inner join gal_mst_temployee e on p.partner_rmname=e.employee_gid
								inner join gal_mst_temployee emp on p.create_by=emp.employee_gid
								inner join gal_mst_tcustcategory c on p.partner_custcategorygid=c.custcategory_gid

							where p.partner_isactive=''Y'' and p.partner_isremoved=''N''
							and p.entity_gid=',@Entity_Gid,' and
							e.employee_isactive=''Y'' and e.employee_isremoved=''N''
							and e.entity_gid=',@Entity_Gid,' and
							c.custcategory_isactive=''Y'' and c.custcategory_isremoved=''N'' and
							emp.employee_isactive=''Y'' and emp.employee_isremoved=''N''
							and emp.entity_gid=',@Entity_Gid,' ',Query_Search,'  order by p.partner_gid
                               ');
	 #select Query_Select;
	 set @p = Query_Select;

     PREPARE stmt FROM @p;
	 EXECUTE stmt;
	 Select found_rows() into ls_count;
	 DEALLOCATE PREPARE stmt;

	 if ls_count > 0 then
		 set Message = 'FOUND';
	else
		 set Message = 'NOT_FOUND';
	end if;
end  if;


if Action='Partner_GetAPP' then
	set P_status ="";
	BEGIN
	Declare Cursor_atma CURSOR FOR

	select c.rolegroup_name from gal_mst_troleemployee as a
	 left join gal_mst_trole as b on a.roleemployee_role_gid=b.role_gid
     left join gal_mst_trolegroup as c on c.rolegroup_gid=b.role_rolegroup_gid
     where a.roleemployee_isremoved='N' and a.roleemployee_employee_gid= @Login_By;

	DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;
	OPEN Cursor_atma;
	atma_looop:loop
		fetch Cursor_atma into v_role_name;
		if finished = 1 then
			leave atma_looop;
		End if;

		if v_role_name = 'VMU CHECKER'  then
			set P_status = concat('''PENDING-CHECKER''');
		end if;
        if v_role_name='VMU HEAD' then
        #select v_role_name;
			IF P_status<>"" THEN

				set P_status=concat(P_status,',''PENDING-HEAD''');
            else

				set P_status=concat(P_status,'''PENDING-HEAD''');
                #select P_status;
            End if;
        End if;

	End loop atma_looop;
	close Cursor_atma;
	end;



    set Query_Search = concat(Query_Search,' and a.Partner_Status in(',P_status,')  ');
#select Query_Search;
	set Query_Select = '';
	set Query_Select =concat('(select con.contact_reftablecode,con.Contact_contacttype_gid,
									  con.Contact_personname,con.Contact_mobileno,con.Contact_email,con.Contact_designation_gid,
                                      con.Contact_landline,con.Contact_landline2,con.Contact_mobileno2,
                                      con.Contact_DOB,con.Contact_WD,add1.address_1,add1.address_2,add1.address_3,
                                      add1.address_pincode,add1.address_city_gid,
                                      add1.address_state_gid,add1.address_district_gid,dis.district_name,s.state_name,cty.City_Name
                                      ,ct.contacttype_Name,des.designation_name,
		  a.partner_gid,a.partner_code, a.partner_name, a.partner_panno,
		  a.partner_compregno,a.partner_group,
		  a.partner_custcategorygid,
          case
                            when partner_compositevendor =''R'' then ''Registered-Regular''
                            when partner_compositevendor =''C'' then ''Registered-Composite''
                            when partner_compositevendor =''U'' then ''UnRegistered'' end
                            partner_compositevendor,
          a.partner_Classification, a.partner_type,
		  a.partner_web,case
                            when partner_activecontract =''Y'' then ''Yes''
                            when partner_activecontract =''N'' then ''No'' end
                            partner_activecontract,
		  a.partner_reason_no_contract,a.partner_contractdatefrom,
		  a.partner_contractdateto, a.partner_aproxspend,
		  a.partner_actualspend, a.partner_noofdir,a.partner_orgtype,
		  a.partner_remarks, a.partner_status,a.partner_mainstatus,a.partner_requestfor,
		  a.partner_renewdate, a.partner_rmname, e.employee_name, emp.employee_name
		  as create_by_emp_name,c.custcategory_name ',Query_Column,'
		  from ',Query_Table,' a
          inner join ',Query_Table1,' add1 on a.partner_addressgid=add1.address_gid
          inner join  ',Query_Table2,' con on con.contact_gid=a.partner_contactgid
								inner join  gal_mst_tstate s on add1.address_state_gid=s.state_gid
								inner join  gal_mst_tcity cty  on add1.address_city_gid=cty.city_gid
								inner join  gal_mst_tdistrict dis  on add1.address_district_gid=dis.district_gid
								inner join  gal_mst_tcontacttype ct  on con.Contact_contacttype_gid=ct.contacttype_gid
                                and ct.contacttype_isactive=''Y'' and ct.contacttype_isremoved=''N'' and ct.entity_gid=',@Entity_Gid,'
								inner join  gal_mst_tdesignation des  on con.Contact_designation_gid=des.designation_gid
                                and des.designation_isactive=''Y'' and des.designation_isremoved=''N'' and des.entity_gid=',@Entity_Gid,'
		  inner join gal_mst_temployee e on a.partner_rmname=e.employee_gid
		  inner join gal_mst_temployee emp on a.create_by=emp.employee_gid
		  inner join gal_mst_tcustcategory c on a.partner_custcategorygid=c.custcategory_gid
		  where a.partner_isactive=''Y'' and a.partner_isremoved=''N''
		  and a.entity_gid=',@Entity_Gid,' and
		  e.employee_isactive=''Y'' and e.employee_isremoved=''N''
		  and e.entity_gid=',@Entity_Gid,' and
		  c.custcategory_isactive=''Y'' and custcategory_isremoved=''N'' and
		  emp.employee_isactive=''Y'' and emp.employee_isremoved=''N''
		  and emp.entity_gid=',@Entity_Gid,' ',Query_Search,')');
	if P_status<>"" then
		SET Query_Select =concat(Query_Select,'union all');
    else
		set Query_Select="";
    end if;
    set Query_Select =concat(Query_Select,'(select con.contact_reftablecode,con.Contact_contacttype_gid,
									  con.Contact_personname,con.Contact_mobileno,con.Contact_email,con.Contact_designation_gid,
                                      con.Contact_landline,con.Contact_landline2,con.Contact_mobileno2,
                                      con.Contact_DOB,con.Contact_WD,add1.address_1,add1.address_2,add1.address_3,
                                      add1.address_pincode,add1.address_city_gid,
                                      add1.address_state_gid,add1.address_district_gid,dis.district_name,s.state_name,cty.City_Name
                                      ,ct.contacttype_Name,des.designation_name
                                      ,a.partner_gid,a.partner_code, a.partner_name, a.partner_panno,
		  a.partner_compregno,a.partner_group,
		  a.partner_custcategorygid,
          case
							when partner_compositevendor =''R'' then ''Registered-Regular''
                            when partner_compositevendor =''C'' then ''Registered-Composite''
                            when partner_compositevendor =''U'' then ''UnRegistered'' end
                            partner_compositevendor,
          a.partner_Classification, a.partner_type,
		  a.partner_web,case
                            when partner_activecontract =''Y'' then ''Yes''
                            when partner_activecontract =''N'' then ''No'' end
                            partner_activecontract,
		  a.partner_reason_no_contract,a.partner_contractdatefrom,
		  a.partner_contractdateto, a.partner_aproxspend,
		  a.partner_actualspend, a.partner_noofdir,a.partner_orgtype,
		  a.partner_remarks, a.partner_status,a.partner_mainstatus,a.partner_requestfor,
		  a.partner_renewdate, a.partner_rmname, e.employee_name, emp.employee_name
		  as create_by_emp_name,c.custcategory_name ',Query_Column,'
		  from ',Query_Table,' a
          inner join ',Query_Table1,' add1 on a.partner_addressgid=add1.address_gid
          inner join  ',Query_Table2,' con on con.contact_gid=a.partner_contactgid

								inner join  gal_mst_tstate s on add1.address_state_gid=s.state_gid
								inner join  gal_mst_tcity cty  on add1.address_city_gid=cty.city_gid
								inner join  gal_mst_tdistrict dis  on add1.address_district_gid=dis.district_gid
								inner join  gal_mst_tcontacttype ct  on con.Contact_contacttype_gid=ct.contacttype_gid
                                and ct.contacttype_isactive=''Y'' and ct.contacttype_isremoved=''N'' and ct.entity_gid=',@Entity_Gid,'
								inner join  gal_mst_tdesignation des  on con.Contact_designation_gid=des.designation_gid
                                and des.designation_isactive=''Y'' and des.designation_isremoved=''N'' and des.entity_gid=',@Entity_Gid,'

		  inner join gal_mst_temployee e on a.partner_rmname=e.employee_gid
		  inner join gal_mst_temployee emp on a.create_by=emp.employee_gid
		  inner join gal_mst_tcustcategory c on a.partner_custcategorygid=c.custcategory_gid
		  where a.partner_isactive=''Y'' and a.partner_isremoved=''N''
		  and a.entity_gid=',@Entity_Gid,' and
		  e.employee_isactive=''Y'' and e.employee_isremoved=''N''
		  and e.entity_gid=',@Entity_Gid,' and
		  c.custcategory_isactive=''Y'' and custcategory_isremoved=''N'' and
		  emp.employee_isactive=''Y'' and emp.employee_isremoved=''N''
		  and emp.entity_gid=',@Entity_Gid,' and a.partner_rmname=',@Login_By,' and a.partner_status=''PENDING-RM'')');

    #select Query_Select;
	 set @p = Query_Select;

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

if Action='Partner_GetAPP_Mst' then

	select JSON_LENGTH(lj_filter,'$') into @li_json_count;
	select JSON_LENGTH(lj_classification,'$') into @li_json_lj_classification_count;
    if @li_json_lj_classification_count = 0 or @li_json_lj_classification_count = ''
		or @li_json_lj_classification_count is null  then
		   set Message = 'No Data In Json. ';
	leave sp_Atma_Partner_Get;
	End if;

	select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Entity_Gid')))  into @Entity_Gid;
    select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Create_By')))  into @Create_By;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Page_Index'))) into @Page_Index ;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Page_Size'))) into @Page_Size ;

	select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partner_Main_Status')))into @Partner_Main_Status;


				    set Query_Limit='';
				#select @Page_Index,@Page_Size;
					if @Page_Index <> '' and @Page_Index is not null and @Page_Size <> '' and @Page_Size is not null  then

									 set @total_size= @Page_Index*@Page_Size;
                                     set @Page_Size=@Page_Size;
									 set Query_Limit = concat(Query_Limit,' LIMIT ',@Page_Size,' OFFSET ',@total_size,'  ');

					else
									#select 1;
									set @Page_Index=2,@Page_Size=5;
									#select @Page_Index,@Page_Size;
									set @total_size= @Page_Index*@Page_Size;
									#select @total_size;
									set Query_Limit = concat(Query_Limit,' LIMIT ',@Page_Size,' OFFSET ',@total_size,'  ');
					End if;


	set Query_Select = '';
	set Query_Select =concat('select con.contact_reftablecode,con.Contact_contacttype_gid,
									  con.Contact_personname,con.Contact_mobileno,con.Contact_email,con.Contact_designation_gid,
                                      con.Contact_landline,con.Contact_landline2,con.Contact_mobileno2,
                                      con.Contact_DOB,con.Contact_WD,a.address_1,a.address_2,a.address_3,
                                      a.address_pincode,a.address_city_gid,cty.City_Name,
                                      a.address_state_gid,s.state_name,a.address_district_gid,dis.district_name
                                      ,ct.contacttype_Name,des.designation_name,p.partner_gid,p.partner_code,p.partner_name, p.partner_panno,
		  p.partner_compregno,p.partner_group,
		  p.partner_custcategorygid,
          case
							when partner_compositevendor =''R'' then ''Registered-Regular''
                            when partner_compositevendor =''C'' then ''Registered-Composite''
                            when partner_compositevendor =''U'' then ''UnRegistered'' end
                            partner_compositevendor,
          p.partner_Classification, p.partner_type,
		  p.partner_web,case
                            when partner_activecontract =''Y'' then ''Yes''
                            when partner_activecontract =''N'' then ''No'' end
                            partner_activecontract,
		  p.partner_reason_no_contract,p.partner_contractdatefrom,
		  p.partner_contractdateto,p.partner_aproxspend,
		  p.partner_actualspend, p.partner_noofdir,p.partner_orgtype,
		  p.partner_remarks, p.partner_status,p.partner_mainstatus,p.partner_requestfor,
		  p.partner_renewdate,p.partner_rmname,e.employee_name, emp.employee_name
		  as create_by_emp_name,c.custcategory_name
		  from atma_mst_tpartner p
          inner join  gal_mst_tcontact con on con.contact_gid=p.partner_contactgid
		  inner join  gal_mst_taddress a on p.partner_addressgid=a.address_gid
		  inner join  gal_mst_tstate s on a.address_state_gid=s.state_gid
		  inner join  gal_mst_tcity cty  on a.address_city_gid=cty.city_gid
		  inner join  gal_mst_tdistrict dis  on a.address_district_gid=dis.district_gid
		  inner join  gal_mst_tcontacttype ct  on con.Contact_contacttype_gid=ct.contacttype_gid
		  and ct.contacttype_isactive=''Y'' and ct.contacttype_isremoved=''N'' and ct.entity_gid=',@Entity_Gid,'
		  inner join  gal_mst_tdesignation des  on con.Contact_designation_gid=des.designation_gid
		  and des.designation_isactive=''Y'' and des.designation_isremoved=''N'' and des.entity_gid=',@Entity_Gid,'

		  inner join gal_mst_temployee e on p.partner_rmname=e.employee_gid
		  inner join gal_mst_temployee emp on a.create_by=emp.employee_gid
		  inner join gal_mst_tcustcategory c on p.partner_custcategorygid=c.custcategory_gid
		  where p.partner_isactive=''Y'' and p.partner_isremoved=''N''
		  and a.entity_gid=',@Entity_Gid,' and
		  e.employee_isactive=''Y'' and e.employee_isremoved=''N''
		  and e.entity_gid=',@Entity_Gid,' and
		  c.custcategory_isactive=''Y'' and custcategory_isremoved=''N'' and
		  emp.employee_isactive=''Y'' and emp.employee_isremoved=''N''
		  and emp.entity_gid=',@Entity_Gid,' and p.partner_mainstatus=''',@Partner_Main_Status,''' and p.create_by=',@Create_By,'
					    ');
                    ###
 #select Query_Select;
 set @p = Query_Select;

     PREPARE stmt FROM @p;
	 EXECUTE stmt;
     #select stmt;
	 Select found_rows() into ls_count;
	 DEALLOCATE PREPARE stmt;

	 if ls_count > 0 then
		 set Message = 'FOUND';
	else
		 set Message = 'NOT_FOUND';
	end if;

END IF;

if Action='Partner_Renewal' then

	select JSON_LENGTH(lj_filter,'$') into @li_json_count;
	select JSON_LENGTH(lj_classification,'$') into @li_json_lj_classification_count;
    if @li_json_lj_classification_count = 0 or @li_json_lj_classification_count = ''
		or @li_json_lj_classification_count is null  then
		   set Message = 'No Data In Json. ';
	leave sp_Atma_Partner_Get;
	End if;

	select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Entity_Gid')))  into @Entity_Gid;
    select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Create_By')))  into @Create_By;

	#select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partner_Main_Status')))into @Partner_Main_Status;
    select date_format(now(),'%Y-%m-%d') into @current_date;

	set Query_Select = '';
	set Query_Select =concat('select a.partner_gid,a.partner_code, a.partner_name, a.partner_panno,
		  a.partner_compregno,a.partner_group,
		  a.partner_custcategorygid,
          case
                            when partner_compositevendor =''R'' then ''Registered-Regular''
                            when partner_compositevendor =''C'' then ''Registered-Composite''
                            when partner_compositevendor =''U'' then ''UnRegistered'' end
                            partner_compositevendor,
          a.partner_Classification, a.partner_type,
		  a.partner_web,case
                            when partner_activecontract =''Y'' then ''Yes''
                            when partner_activecontract =''N'' then ''No'' end
                            partner_activecontract,
		  a.partner_reason_no_contract,a.partner_contractdatefrom,
		  a.partner_contractdateto, a.partner_aproxspend,
		  a.partner_actualspend, a.partner_noofdir,a.partner_orgtype,
		  a.partner_remarks, a.partner_status,a.partner_mainstatus,a.partner_requestfor,
		  a.partner_renewdate, a.partner_rmname, e.employee_name, emp.employee_name
		  as create_by_emp_name,c.custcategory_name ,
          con.contact_reftablecode,con.Contact_contacttype_gid,
									  con.Contact_personname,con.Contact_mobileno,con.Contact_email,con.Contact_designation_gid,
                                      con.Contact_landline,con.Contact_landline2,con.Contact_mobileno2,
                                      con.Contact_DOB,con.Contact_WD,addr.address_1,addr.address_2,addr.address_3,
                                      addr.address_pincode,addr.address_city_gid,cty.City_Name,
                                      addr.address_state_gid,s.state_name,addr.address_district_gid,dis.district_name
                                      ,ct.contacttype_Name,des.designation_name
		  from atma_mst_tpartner a
          inner join  gal_mst_tcontact con on con.contact_gid=a.partner_contactgid
		  inner join  gal_mst_taddress addr on a.partner_addressgid=addr.address_gid
		  inner join  gal_mst_tstate s on addr.address_state_gid=s.state_gid
		  inner join  gal_mst_tcity cty  on addr.address_city_gid=cty.city_gid
		  inner join  gal_mst_tdistrict dis  on addr.address_district_gid=dis.district_gid
		  inner join  gal_mst_tcontacttype ct  on con.Contact_contacttype_gid=ct.contacttype_gid

		  inner join  gal_mst_tdesignation des  on con.Contact_designation_gid=des.designation_gid


		  inner join gal_mst_temployee e on a.partner_rmname=e.employee_gid
		  inner join gal_mst_temployee emp on a.create_by=emp.employee_gid
		  inner join gal_mst_tcustcategory c on a.partner_custcategorygid=c.custcategory_gid
		  where a.partner_isactive=''Y'' and a.partner_isremoved=''N''
		  and a.entity_gid=',@Entity_Gid,' and
		  e.employee_isactive=''Y'' and e.employee_isremoved=''N''
		  and e.entity_gid=',@Entity_Gid,' and
		  c.custcategory_isactive=''Y'' and custcategory_isremoved=''N'' and
		  emp.employee_isactive=''Y'' and emp.employee_isremoved=''N''
		  and emp.entity_gid=',@Entity_Gid,' and a.partner_renewdate <=''',@current_date,'''
          and a.create_by=',@Create_By,'
           and ct.contacttype_isactive=''Y'' and ct.contacttype_isremoved=''N'' and ct.entity_gid=',@Entity_Gid,'
            and des.designation_isactive=''Y'' and des.designation_isremoved=''N'' and des.entity_gid=',@Entity_Gid,'
          ');
	set @p = Query_Select;
   # select Query_Select;
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