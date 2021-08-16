CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_payment_Get`(in Action  varchar(16),
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_Atma_payment_Get:BEGIN



Declare Query_Select varchar(5000);
Declare Query_Search varchar(5000);
Declare Query_Table varchar(60);
Declare Query_Table1 varchar(60);
Declare Query_Column varchar(60);
Declare countRow varchar(5000);
Declare ls_count int;

if Action='Payment_Get' then

	select JSON_LENGTH(lj_filter,'$') into @li_json_count;
    select JSON_LENGTH(lj_classification,'$') into @li_classification_json_count;

    if @li_classification_json_count = 0 or @li_classification_json_count = ''
           or @li_classification_json_count is null  then
			set Message = 'No Entity_Gid In Json. ';
            leave sp_Atma_payment_Get;
	End if;

		select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Entity_Gid'))) into @Entity_Gid;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Mst_Table')))into @Mst_Table;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Payment_Gid'))) into @Payment_Gid;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Paymode_Gid'))) into @Paymode_Gid;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Payment_Partnergid'))) into @Payment_Partnergid;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Bank_Gid'))) into @Bank_Gid;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Bankbranch_Gid'))) into @Bankbranch_Gid;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Bankbranch_Ifsccode'))) into @Bankbranch_Ifsccode;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Payment_Acctype'))) into @Payment_Acctype;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Payment_Accnumber'))) into @Payment_Accnumber;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Payment_Benificiaryname'))) into @Payment_Benificiaryname;

			    set Query_Table='';
			if @Mst_Table='Mst' then
				set Query_Table = concat('atma_mst_tpayment');
			else
				set Query_Table = concat('atma_tmp_mst_tpayment');
			End if;

            set Query_Table1='';
			if @Mst_Table='Mst' then
				set Query_Table1 = concat('atma_mst_tpartnerbranch');
			else
				set Query_Table1 = concat('atma_tmp_mst_tpartnerbranch');
			End if;

             set Query_Column='';
            if @Mst_Table is null or @Mst_Table=''   then
				set Query_Column = concat(',pm.main_payment_gid');
			End if;

        set Query_Search = '';

		if @Payment_Gid is not null or @Payment_Gid <> '' or @Payment_Gid <> 0 then
			set Query_Search = concat(Query_Search,' and pm.payment_gid = ''',@Payment_Gid,''' ');
		End if;

        if @Paymode_Gid is not null or @Paymode_Gid <> '' or @Paymode_Gid <> 0 then
			set Query_Search = concat(Query_Search,' and pmd.Paymode_Gid = ''',@Paymode_Gid,''' ');
		End if;

        if @Bank_Gid is not null or @Bank_Gid <> '' then
			set Query_Search = concat(Query_Search,' and b.Bank_Gid = ''',@Bank_Gid,''' ');
		End if;

        if @Bankbranch_Gid is not null or @Bankbranch_Gid <> '' then
			set Query_Search = concat(Query_Search,' and bb.Bankbranch_Gid = ''',@Bankbranch_Gid,''' ');
		End if;

        if @Bankbranch_Ifsccode is not null or @Bankbranch_Ifsccode <> '' then
			set Query_Search = concat(Query_Search,' and bb.Bankbranch_Ifsccode = ''',@Bankbranch_Ifsccode,''' ');
		End if;

        if @Payment_Acctype is not null or @Payment_Acctype <> ''
        then
			if @Payment_Acctype = 'Current' then
                set @Payment_Acctype = 'C';
                set Query_Search = concat(Query_Search,' and pm.payment_acctype =''',@Payment_Acctype,''' ');
			elseif @Payment_Acctype='Savings' then
                set @Payment_Acctype = 'S';
				set Query_Search = concat(Query_Search,' and pm.payment_acctype =''',@Payment_Acctype,''' ');
            end if;
	    End if;

        if @Payment_Accnumber is not null or @Payment_Accnumber <> '' then
			set Query_Search = concat(Query_Search,' and pm.Payment_Accnumber = ''',@Payment_Accnumber,''' ');
		End if;

        if @Payment_Benificiaryname is not null or @Payment_Benificiaryname <> '' then
			set Query_Search = concat(Query_Search,' and pm.Payment_Benificiaryname = ''',@Payment_Benificiaryname,''' ');
		End if;


					 if @Payment_Partnergid = 0 or @Payment_Partnergid = ''
						or @Payment_Partnergid is null  then
							  set Message = 'No Payment_Partnergid In Json. ';
							  leave sp_Atma_payment_Get;
					 End if;


	set Query_Select = '';
	set Query_Select =concat('select pb.partnerbranch_name,pm.payment_partnergid,pmd.paymode_gid,pmd.Paymode_name,b.bank_gid,
        bb.bankbranch_bank_gid,b.bank_name,bb.bankbranch_gid,bb.bankbranch_name,
        bb.bankbranch_ifsccode,
								CASE
									WHEN pm.payment_acctype= ''C''THEN ''Current''
									WHEN pm.payment_acctype= ''S''THEN ''Savings''
                                END   payment_acctype,
        pm.payment_accnumber,pm.payment_benificiaryname,pm.payment_remarks,pm.payment_gid
        ',Query_Column,'
		from ',Query_Table,' pm inner join ',Query_Table1,' pb on pm.payment_partnerbranchgid=pb.partnerbranch_gid
        and pb.partnerbranch_isactive=''Y'' and pb.partnerbranch_isremoved=''N''
		inner join gal_mst_tpaymode pmd on pm.payment_paymodegid=pmd.paymode_gid and
        pm.payment_isactive=''Y'' and pm.payment_isremoved=''N'' and pm.entity_gid=',@Entity_Gid,' and
		pmd.paymode_isactive=''Y'' and pmd.paymode_isremoved=''N'' and pmd.entity_gid=',@Entity_Gid,'
		left join gal_mst_tbank b on pm.payment_bankgid=b.bank_gid
		left join gal_mst_tbankbranch bb on pm.payment_bankbranchgid=bb.bankbranch_gid
        and b.bank_isactive=''Y'' and b.bank_isremoved=''N'' and b.entity_gid=',@Entity_Gid,' and
		bb.bankbranch_isactive=''Y'' and bb.bankbranch_isremoved=''N'' and bb.entity_gid=',@Entity_Gid,'

		where   pm.payment_partnergid=',@Payment_Partnergid,'
         ',Query_Search,'
						');

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
End if;


END