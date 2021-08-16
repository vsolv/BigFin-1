CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Par_Get`(in Action  varchar(50), in Login_By int,
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_Par_Get:BEGIN
Declare Query_Select varchar(5000);
Declare Query_Search varchar(5000);
Declare Query_Update varchar(5000);
Declare Query_Column varchar(1000);
Declare countRow varchar(5000);
declare v_role_name varchar(128);
DECLARE finished INTEGER DEFAULT 0;
Declare ls_count int;
declare P_status varchar(5000);
declare checker_st varchar(5000);
		select JSON_LENGTH(lj_classification,'$') into @li_json_lj_classification_count;

        if @li_json_lj_classification_count = 0 or @li_json_lj_classification_count is null  then
			set Message = 'No Entity_Gid In Json. ';
			leave sp_Par_Get;
		End if;

		select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Entity_Gid'))) into @Entity_Gid;



if Action='Par_Get' then

	set P_status ='';
	BEGIN
	Declare Cursor_par CURSOR FOR

	select c.rolegroup_name from gal_mst_troleemployee as a
	 left join gal_mst_trole as b on a.roleemployee_role_gid=b.role_gid
     left join gal_mst_trolegroup as c on c.rolegroup_gid=b.role_rolegroup_gid
     where a.roleemployee_isremoved='N' and c.rolegroup_name in('PAR MAKER','PAR CHECKER') and a.roleemployee_employee_gid= Login_By;

	DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;
	OPEN Cursor_par;
	par_looop:loop


		fetch Cursor_par into v_role_name;

        if v_role_name is null  then

          select par_gid, par_no, par_date, par_year, par_amount, par_utilized, par_balance,
							case when par_isbudgeted='Y' then 'Yes' when par_isbudgeted='N' then 'No' end as par_isbudgeted,
                            case when par_burstlinewise='Y' then 'Yes' when par_burstlinewise='N' then 'No' end as par_burstlinewise,
                           case when  par_burstmepwise='Y' then 'Yes' when  par_burstmepwise='N' then 'No' end as par_burstmepwise,par_desc,
                            par_status, par_isactive,
                            par_isremoved, entity_gid, create_by from gal_mst_tpar where  par_isactive='Y'
                            and par_isremoved='N' and entity_gid=1 and par_burstmepwise='par_burstmepwise';
                             set Message = 'NOT_FOUND';
          leave sp_Par_Get;
         end if;
		if finished = 1 then
			leave par_looop;
		End if;

        if v_role_name = 'PAR CHECKER'  then

			set P_status = concat('''PENDING-APPROVAL''');
			set Query_Search = concat(Query_Search,' and par_status in(',P_status,') ');
		end if;
	End loop par_looop;
	close Cursor_par;
	end;

    set Query_Search='';
    select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.PAR_RIGHTS'))) into @PAR_RIGHTS;
    if @PAR_RIGHTS = 'PAR CHECKER' then


   set checker_st='checker';

    set Query_Select = '';
    if v_role_name = 'PAR CHECKER' and checker_st='checker' then

	set Query_Select =concat('select par_gid, par_no, par_date, par_year, par_amount, par_utilized, par_balance,
							case when par_isbudgeted=''Y'' then ''Yes'' when par_isbudgeted=''N'' then ''No'' end as par_isbudgeted,
                            case when par_burstlinewise=''Y'' then ''Yes'' when par_burstlinewise=''N'' then ''No'' end as par_burstlinewise,
                           case when  par_burstmepwise=''Y'' then ''Yes'' when  par_burstmepwise=''N'' then ''No'' end as par_burstmepwise,par_desc,
                            par_status, par_isactive,
                            par_isremoved, entity_gid, create_by from gal_mst_tpar where  par_isactive=''Y''
                            and par_isremoved=''N'' and entity_gid=',@Entity_Gid,' and par_status=''PENDING-APPROVAL''
                            ');
                                #',Query_Search,'
                                else
                                select par_gid, par_no, par_date, par_year, par_amount, par_utilized, par_balance,
							case when par_isbudgeted='Y' then 'Yes' when par_isbudgeted='N' then 'No' end as par_isbudgeted,
                            case when par_burstlinewise='Y' then 'Yes' when par_burstlinewise='N' then 'No' end as par_burstlinewise,
                           case when  par_burstmepwise='Y' then 'Yes' when  par_burstmepwise='N' then 'No' end as par_burstmepwise,par_desc,
                            par_status, par_isactive,
                            par_isremoved, entity_gid, create_by from gal_mst_tpar where  par_isactive='Y'
                            and par_isremoved='N' and entity_gid=1 and par_burstmepwise='par_burstmepwise';
                             set Message = 'NOT_FOUND';
                                leave sp_Par_Get;
                              		end if;
                                    end if;
	if @PAR_RIGHTS = 'PAR MAKER' then

    set Query_Select = '';
    if v_role_name = 'PAR MAKER' then
	set Query_Select =concat('select par_gid, par_no, par_date, par_year, par_amount, par_utilized, par_balance,
							case when par_isbudgeted=''Y'' then ''Yes'' when par_isbudgeted=''N'' then ''No'' end as par_isbudgeted,
                            case when par_burstlinewise=''Y'' then ''Yes'' when par_burstlinewise=''N'' then ''No'' end as par_burstlinewise,
                           case when  par_burstmepwise=''Y'' then ''Yes'' when  par_burstmepwise=''N'' then ''No'' end as par_burstmepwise,par_desc,
                            par_status, par_isactive,
                            par_isremoved, entity_gid, create_by from gal_mst_tpar where  par_isactive=''Y''
                            and par_isremoved=''N'' and entity_gid=',@Entity_Gid,'
                            ');
                                #',Query_Search,'
                                else
                                select par_gid, par_no, par_date, par_year, par_amount, par_utilized, par_balance,
							case when par_isbudgeted='Y' then 'Yes' when par_isbudgeted='N' then 'No' end as par_isbudgeted,
                            case when par_burstlinewise='Y' then 'Yes' when par_burstlinewise='N' then 'No' end as par_burstlinewise,
                           case when  par_burstmepwise='Y' then 'Yes' when  par_burstmepwise='N' then 'No' end as par_burstmepwise,par_desc,
                            par_status, par_isactive,
                            par_isremoved, entity_gid, create_by from gal_mst_tpar where  par_isactive='Y'
                            and par_isremoved='N' and entity_gid=1 and par_burstmepwise='par_burstmepwise';
                             set Message = 'NOT_FOUND';
                                leave sp_Par_Get;
                              		end if;
                                    end if;
	 set @p = Query_Select;
   #select Query_Select;
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
if Action='ParDetails_Get' then
select JSON_LENGTH(lj_filter,'$') into @li_json_lj_filter_count;
        if @li_json_lj_filter_count = 0 or @li_json_lj_filter_count is null  then
			set Message = 'No Filter Json. ';
			leave sp_Par_Get;
		End if;
        select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Par_Gid'))) into @Par_Gid;
	set Query_Select = '';
	set Query_Select =concat('select pardetails_gid, pardetails_pargid, pardetails_exptype, pardetails_requestfor,
 pardetails_budgeted, pardetails_desc, pardetails_year, pardetails_amount, pardetails_remarks,
 pardetails_filegid, pardetails_utilized, pardetails_balance, par_isactive, par_isremoved, entity_gid,
 create_by, create_date, update_by, Update_date from gal_mst_tpardetails where pardetails_pargid=',@Par_Gid,' and par_isactive=''Y'' and par_isremoved=''N''
                            ');
                                #',Query_Search,'

	 set @p = Query_Select;
   #select Query_Select;
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