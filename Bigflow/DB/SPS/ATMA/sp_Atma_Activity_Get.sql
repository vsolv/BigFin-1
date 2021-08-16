CREATE  PROCEDURE `sp_Atma_Activity_Get`(in Type  varchar(16),
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_Atma_Activity_Get:BEGIN

Declare Query_Select varchar(5000);
Declare Query_Search varchar(5000);
Declare Query_Table varchar(60);
Declare Query_Table1 varchar(60);
Declare Query_Table2 varchar(60);
Declare Query_Table3 varchar(60);
Declare Query_Update varchar(5000);
Declare Query_Column varchar(500);
Declare countRow varchar(5000);
Declare ls_count int;

if  Type ='Activity_Get' then

		select JSON_LENGTH(lj_filter,'$') into @li_json_count;
		select JSON_LENGTH(lj_classification,'$') into @li_json_lj_classification_count;


			select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Entity_Gid'))) into @Entity_Gid;
			select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Mst_Table')))into @Mst_Table;
			select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Activity_Partnergid'))) into @Activity_Partnergid;
			select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Activity_Main_Gid'))) into @Activity_Main_Gid;
			select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Activity_Type'))) into @Activity_Type;
			select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Activity_Name'))) into @Activity_Name;
			select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Activity_Desc'))) into @Activity_Desc;
			select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Activity_Rm'))) into @Activity_Rm;

                    set Query_Table='';
				if @Mst_Table='Mst' then
					set Query_Table = concat('atma_mst_tactivity');
				else
					set Query_Table = concat('atma_tmp_mst_tactivity');
				End if;

                if @Mst_Table='Mst' then
					set Query_Table1 = concat('gal_mst_tcontact');
				else
					set Query_Table1 = concat('atma_tmp_mst_tcontact');
				End if;

                 if @Mst_Table='Mst' then
					set Query_Table2 = concat('atma_mst_tpartner');
				else
					set Query_Table2 = concat('atma_tmp_tpartner');
				End if;

                if @Mst_Table='Mst' then
					set Query_Table3 = concat('atma_mst_tpartnerbranch');
				else
					set Query_Table3 = concat('atma_tmp_mst_tpartnerbranch');
				End if;


					 set Query_Column='';
            if @Mst_Table is null or @Mst_Table=''   then
				set Query_Column = concat(',main_activity_gid');
			End if;


            #if @Mst_Table ='Mst'   then
				set Query_Column = concat(',  CASE
													WHEN activity_bidding= ''N''THEN ''NO''
													WHEN activity_bidding= ''Y''THEN ''YES''
											  END   activity_bidding');
				set Query_Column = concat(Query_Column,',  CASE
																 WHEN activity_fidiinsur= ''N''THEN ''NO''
																 WHEN activity_fidiinsur= ''Y''THEN ''YES''
														   END   activity_fidiinsur');
		    #End if;


					if  @Activity_Partnergid = 0 or @Activity_Partnergid = ''
						or @Activity_Partnergid is null then
						set Message ='Activity Partnergid Is Not Given';
						rollback;
						leave sp_Atma_Activity_Get;
					end if;


		set Query_Search = '';

        if @Activity_Main_Gid is not null or @Activity_Main_Gid <> '' then
			set Query_Search = concat(Query_Search,' and a.activity_gid = ',@Activity_Main_Gid,'  ');
        End if;

        if @Activity_Type is not null or @Activity_Type <> '' then
			set Query_Search = concat(Query_Search,' and a.Activity_Type = ''',@Activity_Type,'''  ');
        End if;

        if @Activity_Name is not null or @Activity_Name <> '' then
			set Query_Search = concat(Query_Search,' and a.Activity_Name = ''',@Activity_Name,'''  ');
        End if;

        if @Activity_Desc is not null or @Activity_Desc <> '' then
			set Query_Search = concat(Query_Search,' and a.Activity_Desc = ''',@Activity_Desc,'''  ');
        End if;

		if @Activity_Rm is not null or @Activity_Rm <> '' then
			set Query_Search = concat(Query_Search,' and a.Activity_Rm = ',@Activity_Rm,' ');
        End if;



		set Query_Select = '';
		set Query_Select =concat('select pb.partnerbranch_gid,pb.partnerbranch_name,p.partner_status,p.create_by,activity_partnergid,activity_code,activity_gid,
								 case
								when activity_type =''P'' then ''Product''
								when activity_type =''S'' then ''Service'' end
								activity_type,
                                activity_name,activity_desc,activity_startdate,activity_enddate,activity_projectedspend,activity_rm,
									 concat(employee_name,''-'',employee_code) employee_name,
                                activity_reason,activity_status,Contact_personname,contact_gid,
                                Contact_contacttype_gid,Contact_designation_gid,Contact_landline, Contact_landline2,
								Contact_mobileno,Contact_mobileno2,Contact_email,Contact_DOB,Contact_WD,
                                designation_name,designation_gid ,contacttype_Name
                                ',Query_Column,'
                                from ',Query_Table,' as a
                                left join ',Query_Table1,' as b on b.contact_gid =a.activity_contactgid and a.activity_isactive=''Y'' and
                                a.activity_isremoved =''N''and b.entity_gid = ',@Entity_Gid,'
                                inner join ',Query_Table3,' as pb on a.activity_partnerbranchgid=pb.partnerbranch_gid
                                and pb.partnerbranch_isactive=''Y'' and pb.partnerbranch_isremoved=''N''
                                inner join gal_mst_temployee as c on c.employee_gid= a.activity_rm and c.employee_isactive=''Y''
                                and c.employee_isremoved =''N''and c.entity_gid = ',@Entity_Gid,'
                                left join gal_mst_tdesignation as d on d.designation_gid = b.Contact_designation_gid and d.designation_isactive=''Y''
                                and d.designation_isremoved =''N'' and d.entity_gid =',@Entity_Gid,'
								left join gal_mst_tcontacttype as ct on ct.contacttype_gid = b.Contact_contacttype_gid

                                and ct.contacttype_isactive=''Y''
                                and ct.contacttype_isremoved =''N'' and ct.entity_gid =',@Entity_Gid,'
								inner join ',Query_Table2,' as p on p.partner_gid= a.activity_partnergid
								where  a.entity_gid=',@Entity_Gid,' and a.activity_partnergid=',@Activity_Partnergid,'
                                ',Query_Search,'');


	 set @p = Query_Select;
	#select  @p;
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