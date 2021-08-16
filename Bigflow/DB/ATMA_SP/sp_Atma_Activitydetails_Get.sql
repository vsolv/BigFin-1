CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Activitydetails_Get`(in Action  varchar(50),
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_Atma_Activitydetails_Get:BEGIN
Declare Query_Select varchar(5000);
Declare Query_Search varchar(5000);
Declare Query_Table varchar(60);
Declare Query_Table1 varchar(60);
Declare Query_Table2 varchar(60);
Declare Query_Update varchar(5000);
Declare countRow varchar(5000);
Declare ls_count int;

if Action='Activitydetails_Get' then

		select JSON_LENGTH(lj_filter,'$') into @li_json_count;
		select JSON_LENGTH(lj_classification,'$') into @li_json_lj_classification_count;




        if @li_json_lj_classification_count = 0 or @li_json_lj_classification_count is null  then
			set Message = 'No Entity_Gid In Json. ';
			leave sp_Atma_Activitydetails_Get;
		End if;


		select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Entity_Gid'))) into @entity_gid;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Mst_Table')))into @Mst_Table;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Activitydetails_Activitygid'))) into @Activitydetails_Activitygid;

		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Activitydetails_Name'))) into @Activitydetails_Name;

            set Query_Table='';
			if @Mst_Table='Mst' then
				set Query_Table = concat('atma_mst_tactivitydetails');
			else
				set Query_Table = concat('atma_tmp_mst_tactivitydetails');
			End if;

            set Query_Table1='';
			if @Mst_Table='Mst' then
				set Query_Table1 = concat('atma_mst_tactivity');
			else
				set Query_Table1 = concat('atma_tmp_mst_tactivity');
			End if;

            set Query_Table2='';
			if @Mst_Table='Mst' then
				set Query_Table2 = concat('atma_mst_tpartner');
			else
				set Query_Table2 = concat('atma_tmp_tpartner');
			End if;

        set Query_Search = '';

         if @Activitydetails_Activitygid is not null or @Activitydetails_Activitygid <> '' or @Activitydetails_Activitygid <> 0  then

			set Query_Search = concat(Query_Search,' and AD.activitydetails_activitygid = ',@Activitydetails_Activitygid,'  ');

		End if;


        if @Activitydetails_Name is not null or @Activitydetails_Name <> '' then
			set Query_Search = concat(Query_Search,' and AD.activitydetails_name = ''',@Activitydetails_Name,'''  ');

        End if;


		set Query_Select = '';
	set Query_Select =concat('select p.create_by,AD.activitydetails_gid,A.activity_name,AD.activitydetails_code,AD.activitydetails_name,
								AD.activitydetails_remarks,AD.activitydetails_activitygid,A.activity_partnergid,
								AD.activitydetails_raisor,AD.activitydetails_approver,ra_emp.employee_name as Raisor ,ap_emp.employee_name as Approver from
								',Query_Table,' AD
								inner join ',Query_Table1,' A
                                on AD.activitydetails_activitygid =A.activity_gid
                                inner join gal_mst_temployee ra_emp on AD.activitydetails_raisor=ra_emp.employee_gid
                                inner join gal_mst_temployee ap_emp on AD.activitydetails_approver=ap_emp.employee_gid
                                inner join ',Query_Table2,' p on p.partner_gid=A.activity_partnergid
                                where
								AD.activitydetails_isactive=''Y'' and AD.activitydetails_isremoved=''N''
                                and A.activity_isactive=''Y''
                                and A.activity_isremoved=''N'' and A.entity_gid = ',@entity_gid,' and Activitydetails_Activitygid=',@Activitydetails_Activitygid,'

                                and AD.entity_gid = ',@entity_gid,'',Query_Search,'');

           #select  Query_Select;
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
end if;
END