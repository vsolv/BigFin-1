CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Mep_Get`(in Action  varchar(50), in Login_By int,
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_Mep_Get:BEGIN
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
			leave sp_Mep_Get;
		End if;

		select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Entity_Gid'))) into @Entity_Gid;



if Action='Mep_Get' then
select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.MEP_RIGHTS'))) into @MEP_RIGHTS;
	set P_status ='';
	BEGIN
	Declare Cursor_par CURSOR FOR

	select c.rolegroup_name from gal_mst_troleemployee as a
	 left join gal_mst_trole as b on a.roleemployee_role_gid=b.role_gid
     left join gal_mst_trolegroup as c on c.rolegroup_gid=b.role_rolegroup_gid
     where a.roleemployee_isremoved='N' and c.rolegroup_name in('MEP MAKER','MEP CHECKER') and a.roleemployee_employee_gid= Login_By;

	DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;
	OPEN Cursor_par;
	par_looop:loop
		fetch Cursor_par into v_role_name;
        if v_role_name is null  then
		select a.mep_gid, a.mep_no, a.mep_name, a.mep_raisor, a.mep_amount, a.mep_finyear, a.mep_type, a.mep_startdate,
    a.mep_enddate, a.mep_branchgid,a.mep_mode, a.mep_parno, a.mep_budgeted, a.mep_projectowner, a.mep_requestfor, a.mep_budgetowner,
    a.mep_justification, a.mep_status,case when a.mep_isclosed='O' then 'Open' when a.mep_isclosed='C' then 'Close'
    when a.mep_isclosed='R' then 'Reopen' end as mep_isclosed,b.branch_code,c.employee_name as mep_raisors,
    d.employee_name as mep_projectowners, e.employee_name as mep_budgetowners,
    a.mep_isactive, a.mep_isremoved, a.entity_gid, a.create_by
    from gal_mst_tmep a inner join gal_mst_tbranch  b on a.mep_branchgid=b.branch_gid
    inner join gal_mst_temployee c on a.mep_raisor=c.employee_gid
    inner join gal_mst_temployee d on a.mep_projectowner=d.employee_gid
    inner join gal_mst_temployee e on a.mep_budgetowner=e.employee_gid
    where a.mep_isactive='Y'
                            and a.mep_isremoved='N' and a.entity_gid=1 and a.mep_budgeted=11243;
          set Message = 'NOT_FOUND';
          leave sp_Mep_Get;
         end if;
		if finished = 1 then
			leave par_looop;
		End if;
		 set Query_Search='';
        if v_role_name = 'MEP CHECKER' then

			set checker_st='checker';
			set P_status = concat('''PENDING-APPROVAL''');
			set Query_Search = concat(Query_Search,' and mep_status in(',P_status,') ');
		end if;
	End loop par_looop;
	close Cursor_par;
	end;
	if @MEP_RIGHTS = 'MEP CHECKER' then

    set Query_Select = '';
    if v_role_name = 'MEP CHECKER' and checker_st='checker' then

	set Query_Select =concat('select a.mep_gid, a.mep_no, a.mep_name, a.mep_raisor, a.mep_amount, a.mep_finyear, a.mep_type, a.mep_startdate,
    a.mep_enddate, a.mep_branchgid,a.mep_mode, a.mep_parno, a.mep_budgeted, a.mep_projectowner, a.mep_requestfor, a.mep_budgetowner,
    a.mep_justification, a.mep_status,case when a.mep_isclosed=''O'' then ''Open'' when a.mep_isclosed=''C'' then ''Close''
    when a.mep_isclosed=''R'' then ''Reopen'' end as mep_isclosed,b.branch_code,c.employee_name as mep_raisors,
    d.employee_name as mep_projectowners, e.employee_name as mep_budgetowners,
    a.mep_isactive, a.mep_isremoved, a.entity_gid, a.create_by
    from gal_mst_tmep a inner join gal_mst_tbranch  b on a.mep_branchgid=b.branch_gid
    inner join gal_mst_temployee c on a.mep_raisor=c.employee_gid
    inner join gal_mst_temployee d on a.mep_projectowner=d.employee_gid
    inner join gal_mst_temployee e on a.mep_budgetowner=e.employee_gid
    where a.mep_isactive=''Y'' and a.mep_isremoved=''N'' and
    a.entity_gid=',@Entity_Gid,' and a.mep_status=''PENDING-APPROVAL''
                            ');

	else
    select a.mep_gid, a.mep_no, a.mep_name, a.mep_raisor, a.mep_amount, a.mep_finyear, a.mep_type, a.mep_startdate,
    a.mep_enddate, a.mep_branchgid,a.mep_mode, a.mep_parno, a.mep_budgeted, a.mep_projectowner, a.mep_requestfor, a.mep_budgetowner,
    a.mep_justification, a.mep_status,case when a.mep_isclosed='O' then 'Open' when a.mep_isclosed='C' then 'Close'
    when a.mep_isclosed='R' then 'Reopen' end as mep_isclosed,b.branch_code,c.employee_name as mep_raisors,
    d.employee_name as mep_projectowners, e.employee_name as mep_budgetowners,
    a.mep_isactive, a.mep_isremoved, a.entity_gid, a.create_by
    from gal_mst_tmep a inner join gal_mst_tbranch  b on a.mep_branchgid=b.branch_gid
    inner join gal_mst_temployee c on a.mep_raisor=c.employee_gid
    inner join gal_mst_temployee d on a.mep_projectowner=d.employee_gid
    inner join gal_mst_temployee e on a.mep_budgetowner=e.employee_gid
    where a.mep_isactive='Y'
	and a.mep_isremoved='N' and a.entity_gid=1 and a.mep_budgeted='mep_budgeted';
	set Message = 'NOT_FOUND';
    leave sp_Mep_Get;
                            END IF;
                           end if;
	if @MEP_RIGHTS = 'MEP MAKER' then

	if v_role_name = 'MEP MAKER' then

	set Query_Select =concat('select a.mep_gid, a.mep_no, a.mep_name, a.mep_raisor, a.mep_amount, a.mep_finyear, a.mep_type, a.mep_startdate,
    a.mep_enddate, a.mep_branchgid,a.mep_mode, a.mep_parno, a.mep_budgeted, a.mep_projectowner, a.mep_requestfor, a.mep_budgetowner,
    a.mep_justification, a.mep_status,case when a.mep_isclosed=''O'' then ''Open'' when a.mep_isclosed=''C'' then ''Close''
    when a.mep_isclosed=''R'' then ''Reopen'' end as mep_isclosed,b.branch_code,c.employee_name as mep_raisors,
    d.employee_name as mep_projectowners, e.employee_name as mep_budgetowners,
    a.mep_isactive, a.mep_isremoved, a.entity_gid, a.create_by
    from gal_mst_tmep a inner join gal_mst_tbranch  b on a.mep_branchgid=b.branch_gid
    inner join gal_mst_temployee c on a.mep_raisor=c.employee_gid
    inner join gal_mst_temployee d on a.mep_projectowner=d.employee_gid
    inner join gal_mst_temployee e on a.mep_budgetowner=e.employee_gid
    where a.mep_isactive=''Y''
                            and a.mep_isremoved=''N'' and a.entity_gid=',@Entity_Gid,'
                            ');
        else
        select a.mep_gid, a.mep_no, a.mep_name, a.mep_raisor, a.mep_amount, a.mep_finyear, a.mep_type, a.mep_startdate,
    a.mep_enddate, a.mep_branchgid,a.mep_mode, a.mep_parno, a.mep_budgeted, a.mep_projectowner, a.mep_requestfor, a.mep_budgetowner,
    a.mep_justification, a.mep_status,case when a.mep_isclosed='O' then 'Open' when a.mep_isclosed='C' then 'Close'
    when a.mep_isclosed='R' then 'Reopen' end as mep_isclosed,b.branch_code,c.employee_name as mep_raisors,
    d.employee_name as mep_projectowners, e.employee_name as mep_budgetowners,
    a.mep_isactive, a.mep_isremoved, a.entity_gid, a.create_by
    from gal_mst_tmep a inner join gal_mst_tbranch  b on a.mep_branchgid=b.branch_gid
    inner join gal_mst_temployee c on a.mep_raisor=c.employee_gid
    inner join gal_mst_temployee d on a.mep_projectowner=d.employee_gid
    inner join gal_mst_temployee e on a.mep_budgetowner=e.employee_gid
    where a.mep_isactive='Y'
                            and a.mep_isremoved='N' and a.entity_gid=1 and a.mep_budgeted='mep_budgeted';
          set Message = 'NOT_FOUND';
         leave sp_Mep_Get;

                            END IF;
                            end if;

	 set @p = Query_Select;

     PREPARE stmt FROM @p;
	 EXECUTE stmt;
	 Set ls_count =0;
	 Select found_rows() into ls_count;

	 DEALLOCATE PREPARE stmt;

	 if ls_count > 0 then
		 set Message = 'FOUND';
	else
		 set Message = 'NOT_FOUND';
	end if;


END IF;
if Action='MepDetails_Get' then
select JSON_LENGTH(lj_filter,'$') into @li_json_lj_filter_count;
        if @li_json_lj_filter_count = 0 or @li_json_lj_filter_count is null  then
			set Message = 'No Filter Json. ';
			leave sp_Mep_Get;
		End if;
        select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Mep_Gid'))) into @Mep_Gid;
	set Query_Select = '';
	set Query_Select =concat('select a.mepdetails_gid,a.mepdetails_mepgid,a.mepdetails_productgid,a.mepdetails_desc,a.mepdetails_qty,
    a.mepdetails_unitprice,a.mepdetails_totalamt,a.mepdetails_isactive, a.mepdetails_isremoved, a.entity_gid,b.product_code,
    b.product_code as mepdetails_productcode,b.product_uom_gid,c.uom_name, b.product_name,
   a.create_by from gal_mst_tmepdetails a inner join gal_mst_tproduct b on a.mepdetails_productgid=b.product_gid inner join
   gal_mst_tuom c on b.product_uom_gid=c.uom_gid
   where a.mepdetails_mepgid=',@Mep_Gid,' and a.mepdetails_isactive=''Y'' and a.mepdetails_isremoved=''N''
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

if Action='ParAmount_Get' then
select JSON_LENGTH(lj_filter,'$') into @li_json_lj_filter_count;
        if @li_json_lj_filter_count = 0 or @li_json_lj_filter_count is null  then
			set Message = 'No Filter Json. ';
			leave sp_Mep_Get;
		End if;
        select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.par_no'))) into @par_no;
        select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.exp_type'))) into @exp_type;
        #select @par_no,@exp_type;
        select par_gid from gal_mst_tpar where par_no=@par_no into @Par_Gid;
        #select @Par_Gid;
       set Query_Select = '';
	set Query_Select = concat('select a.par_amount,ifnull(sum(b.pardetails_amount),0) as pardetails_amount,
							ifnull(ss.qq,0) as Approved_amount,ifnull(s1.q1,0)
							as PendingApproved_Aoumnt from gal_mst_tpar a
							inner join gal_mst_tpardetails b on b.pardetails_pargid=a.par_gid
							left join (select d.mep_parno,ifnull(sum(d.mep_amount),0) as qq from gal_mst_tmep d
							inner join gal_mst_tpar e on d.mep_parno=e.par_no
                            where d.mep_type=''',@exp_type,''' and d.mep_parno=''',@par_no,''' and d.mep_status=''APPROVED''
							and d.mep_isactive=''Y'' and d.mep_isremoved=''N'') as ss
							on ss.mep_parno=a.par_no
							left join (select d.mep_parno,ifnull(sum(d.mep_amount),0) as q1 from gal_mst_tmep d
							inner join gal_mst_tpar e on d.mep_parno=e.par_no
                            where d.mep_type=''',@exp_type,''' and d.mep_parno=''',@par_no,''' and d.mep_status=''PENDING-APPROVAL''
							and d.mep_isactive=''Y'' and d.mep_isremoved=''N'')as s1
							on s1.mep_parno=a.par_no
							where a.par_no=''',@par_no,''' and b.pardetails_exptype=''',@exp_type,'''
                            and a.par_isactive=''Y'' and a.par_isremoved=''N'' ');

	set @Query_Select = Query_Select;
	#select  @Query_Select ;

     PREPARE stmt FROM @Query_Select;
	 EXECUTE stmt;
	 Select found_rows() into ls_count;
	 DEALLOCATE PREPARE stmt;

     select ls_count;

	 if ls_count > 0 then
		 set Message = 'FOUND';
	else
		 set Message = 'NOT_FOUND';
	end if;
end if;#action= ParAmount_Get;

if Action='Product_Get' then
select JSON_LENGTH(lj_filter,'$') into @li_json_lj_filter_count;

       set Query_Select = '';
	set Query_Select = concat('select a.product_gid,a.product_code,a.product_name,b.uom_name from gal_mst_tproduct as a
inner join gal_mst_tuom as b on  a.product_uom_gid=b.uom_gid where a.product_isactive=''Y'' and a.product_isremoved=''N'' ');

	set @Query_Select = Query_Select;
	#select  @Query_Select ;

     PREPARE stmt FROM @Query_Select;
	 EXECUTE stmt;
	 Select found_rows() into ls_count;
	 DEALLOCATE PREPARE stmt;


	 if ls_count > 0 then
		 set Message = 'FOUND';
	else
		 set Message = 'NOT_FOUND';
	end if;
end if;#action= Product_Get;
END