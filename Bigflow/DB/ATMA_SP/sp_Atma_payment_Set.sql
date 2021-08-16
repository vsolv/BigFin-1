CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_payment_Set`(in ls_Action varchar(16),
in payment json,in lj_classification json,
out Message varchar(1000))
sp_Atma_payment_Set:BEGIN
declare Query_Insert varchar(1000);
Declare countRow varchar(6000);
Declare Query_Update varchar(1000);
Declare errno int;
Declare msg,Error_Level varchar(1000);

						DECLARE EXIT HANDLER FOR SQLEXCEPTION
						BEGIN
							GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
							set Message = concat(Error_Level,' : No-',errno , msg);
							ROLLBACK;
						END;
if ls_Action = 'INSERT'  then

         start transaction;

		select JSON_LENGTH(payment,'$') into @li_jsonpayment;
		select JSON_LENGTH(lj_classification,'$') into @li_classification_jsoncount;

		if @li_jsonpayment = 0 or @li_jsonpayment is null  then
			set Message = 'No Data In Json. ';
			leave sp_Atma_payment_Set;
		End if;

         if @li_classification_jsoncount = 0 or @li_classification_jsoncount = ''
            or @li_classification_jsoncount is null  then
			set Message = 'No Entity_Gid In Json. ';
			leave sp_Atma_payment_Set;
		End if;

        if @li_classification_jsoncount is not null or @li_classification_jsoncount	<> ''
		   or @li_classification_jsoncount	<> 0 then

		select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Entity_Gid')))into @Entity_Gid;

		End if;
			if @li_jsonpayment is not null or @li_jsonpayment <> '' then
				 select JSON_UNQUOTE(JSON_EXTRACT(payment,CONCAT('$.Payment_Partner_Gid')))into @Payment_Partner_Gid;
				 select JSON_UNQUOTE(JSON_EXTRACT(payment,CONCAT('$.Payment_Partnerbranchgid')))into @Payment_Partnerbranchgid;
				 select JSON_UNQUOTE(JSON_EXTRACT(payment,CONCAT('$.Payment_Paymodegid')))into @Payment_Paymodegid;
				 select JSON_UNQUOTE(JSON_EXTRACT(payment,CONCAT('$.Payment_Bankgid')))into @Payment_Bankgid;
				 select JSON_UNQUOTE(JSON_EXTRACT(payment,CONCAT('$.Payment_Bankbranchgid')))into @Payment_Bankbranchgid;
				 select JSON_UNQUOTE(JSON_EXTRACT(payment,CONCAT('$.Payment_Acctype')))into @Payment_Acctype;
				 select JSON_UNQUOTE(JSON_EXTRACT(payment,CONCAT('$.Payment_Accnumber')))into @Payment_Accnumber;
				 select JSON_UNQUOTE(JSON_EXTRACT(payment,CONCAT('$.Payment_Benificiaryname')))into @Payment_Benificiaryname;
				 select JSON_UNQUOTE(JSON_EXTRACT(payment,CONCAT('$.Payment_Remarks')))into @Payment_Remarks;
				 #select JSON_UNQUOTE(JSON_EXTRACT(payment,CONCAT('$.Entity_Gid')))into @Entity_Gid;
				 select JSON_UNQUOTE(JSON_EXTRACT(payment,CONCAT('$.Create_By')))into @Create_By;
			end if;

				if @Payment_Acctype='Savings' then
					set @actype='S';
				elseif @Payment_Acctype='Current' then
					set @actype='C';
				elseif @Payment_Acctype=0 then
					set @actype=0;
				end if;

                if @Payment_Partner_Gid = '' or @Payment_Partner_Gid is null  or @Payment_Partner_Gid =0  then
				set Message ='Payment Partner Gid Is Not Given';
				rollback;
				leave sp_Atma_payment_Set;
				end if;
                if @Payment_Partnerbranchgid = '' or @Payment_Partnerbranchgid is null  or @Payment_Partnerbranchgid =0  then
				set Message ='Payment Partner Branch Gid Is Not Given';
				rollback;
				leave sp_Atma_payment_Set;
				end if;
               # select @Payment_Partner_Gid;
                if @Payment_Paymodegid = '' or @Payment_Paymodegid is null  or @Payment_Paymodegid =0  then
				set Message ='Payment Paymodegid Is Not Given';
				rollback;
				leave sp_Atma_payment_Set;
				end if;

                if @Payment_Bankgid = '' or @Payment_Bankgid is null   then
				set Message ='PaymentBankgid Is Not Given';
				rollback;
				leave sp_Atma_payment_Set;
				end if;

                if @Payment_Bankbranchgid = '' or @Payment_Bankbranchgid is null   then
				set Message ='Payment Bank Branchgid Is Not Given';
				rollback;
				leave sp_Atma_payment_Set;
				end if;

               /* if @Payment_Acctype = '' or @Payment_Acctype is null  then
				set Message ='PaymentAcctype Is Not Given';
				rollback;
				leave sp_Atma_payment_Set;
				end if;

                if @Payment_Accnumber = '' or @Payment_Accnumber is null  then
				set Message ='PaymentAccnumber Is Not Given';
				rollback;
				leave sp_Atma_payment_Set;
				end if;

                if @Payment_Benificiaryname = '' or @Payment_Benificiaryname is null  then
				set Message ='PaymentBenificiaryname Is Not Given';
				rollback;
				leave sp_Atma_payment_Set;
				end if; */

                if @Entity_Gid = 0 or @Entity_Gid = '' or @Entity_Gid is null  then
				set Message ='Entity_Gid Is Not Given';
				rollback;
				leave sp_Atma_payment_Set;
				end if;
		#select max(partner_gid) from   atma_tmp_tpartner into @Payment_Partnergid;

            set Query_Insert='';
	set Error_Level='ATMA46.1';
	set Query_Insert=concat('insert into atma_tmp_mst_tpayment(payment_partnergid,payment_partnerbranchgid,
							payment_paymodegid,payment_bankgid,
							payment_bankbranchgid,payment_acctype,payment_accnumber,
							payment_benificiaryname,Payment_Remarks,entity_gid,create_by)
					values(',@Payment_Partner_Gid,',',@Payment_Partnerbranchgid,',
                    ',@Payment_Paymodegid,',',@Payment_Bankgid,',
                    ',@Payment_Bankbranchgid,',''',ifnull(@actype,''),''',
					''',ifnull(@Payment_Accnumber,''),''',''',ifnull(@Payment_Benificiaryname,''),''',
                    ''',ifnull(@Payment_Remarks,''),''',
					',@Entity_Gid,',',@Create_By,')'
                    );

                 #SELECT  Query_Insert;
	set @Insert_query = Query_Insert;

	PREPARE stmt FROM @Insert_query;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
    if countRow >  0 then
		set Message = 'SUCCESS';
        commit;
	else
		set Message = 'INSERT FAILED';
		rollback;
	end if;


end if;

if ls_Action='UPDATE' then

  select JSON_LENGTH(payment,'$') into @li_jsonpayment;
  select JSON_LENGTH(lj_classification,'$') into @li_classification_jsoncount;
			#select @li_jsonpartner;
		if @li_jsonpayment = 0 or @li_jsonpayment is null  then
			set Message = 'No Data In Json - Update.';
			leave sp_Atma_payment_Set;
		End if;

        if @li_classification_jsoncount = 0 or @li_classification_jsoncount = ''
            or @li_classification_jsoncount is null  then
			set Message = 'No Update By In Json. ';
			leave sp_Atma_payment_Set;
		End if;

        if @li_classification_jsoncount is not null or @li_classification_jsoncount	<> ''
		   or @li_classification_jsoncount	<> 0 then
           select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Update_By')))into @Update_By;
		end if;

	if @li_jsonpayment is not null or @li_jsonpayment <> '' then
    #select 1;
				 select JSON_UNQUOTE(JSON_EXTRACT(payment,CONCAT('$.Payment_Gid')))into @Payment_Gid;
				 select JSON_UNQUOTE(JSON_EXTRACT(payment,CONCAT('$.Payment_Partnerbranchgid')))into @Payment_Partnerbranchgid;
                 select JSON_UNQUOTE(JSON_EXTRACT(payment,CONCAT('$.Payment_Paymodegid')))into @Payment_Paymodegid;
				 select JSON_UNQUOTE(JSON_EXTRACT(payment,CONCAT('$.Payment_Bankgid')))into @Payment_Bankgid;
				 select JSON_UNQUOTE(JSON_EXTRACT(payment,CONCAT('$.Payment_Bankbranchgid')))into @Payment_Bankbranchgid;
				 select JSON_UNQUOTE(JSON_EXTRACT(payment,CONCAT('$.Payment_Acctype')))into @Payment_Acctype;
				 select JSON_UNQUOTE(JSON_EXTRACT(payment,CONCAT('$.Payment_Accnumber')))into @Payment_Accnumber;
				 select JSON_UNQUOTE(JSON_EXTRACT(payment,CONCAT('$.Payment_Benificiaryname')))into @Payment_Benificiaryname;
				 select JSON_UNQUOTE(JSON_EXTRACT(payment,CONCAT('$.Payment_Remarks')))into @Payment_Remarks;


			End if;

					set Query_Update = '';

					if @Payment_Gid is not null or @Payment_Gid <> '' or @Payment_Gid <> 0 then
						set @Payment_Gid=@Payment_Gid;
					end if;

                    if @Payment_Partnerbranchgid is not null or @Payment_Partnerbranchgid <> '' or @Payment_Partnerbranchgid <> 0  then

						set Query_Update = concat(Query_Update, ',payment_partnerbranchgid = ',@Payment_Partnerbranchgid,' ');

					end if;

                   if @Payment_Paymodegid is not null or @Payment_Paymodegid <> '' or @Payment_Paymodegid <> 0  then

						set Query_Update = concat(Query_Update, ',Payment_Paymodegid = ',@Payment_Paymodegid,' ');

					end if;



					if @Payment_Bankgid is not null or @Payment_Bankgid <> '' or @Payment_Bankgid <> 0 then

						set Query_Update = concat(Query_Update,',Payment_Bankgid = ',@Payment_Bankgid,'  ');

					End if;



                    if @Payment_Bankbranchgid is not null or @Payment_Bankbranchgid <> '' or @Payment_Bankbranchgid <> 0 then

						set Query_Update = concat(Query_Update,',Payment_Bankbranchgid = ',@Payment_Bankbranchgid,'  ');

					End if;

					if @Payment_Acctype='Savings' then
						set @actype='S';
					elseif @Payment_Acctype='Current' then
						set @actype='C';
					elseif @Payment_Acctype=0 then
						set @actype=0;
					end if;

                    if @actype is not null or @actype <> '' then

						set Query_Update = concat(Query_Update,',Payment_Acctype = ''',@actype,'''  ');

					End if;

                    if @Payment_Accnumber is not null or @Payment_Accnumber <> '' then

						set Query_Update = concat(Query_Update,',Payment_Accnumber = ''',@Payment_Accnumber,'''  ');

					End if;


					if @Payment_Benificiaryname is not null or @Payment_Benificiaryname <> '' then

						set Query_Update = concat(Query_Update,',Payment_Benificiaryname = ''',@Payment_Benificiaryname,'''  ');

					End if;

					if @Payment_Remarks is not null or @Payment_Remarks <> '' then

						set Query_Update = concat(Query_Update,',Payment_Remarks = ''',@Payment_Remarks,'''  ');

					End if;


					if @Update_By is not null or @Update_By <> '' then

						set Query_Update = concat(Query_Update,',Update_By = ',@Update_By,'  ');

					End if;

					set Error_Level='ATMA46.2';
						 set Query_Update = concat('Update atma_tmp_mst_tpayment
                         set update_date = CURRENT_TIMESTAMP ',Query_Update,'
						 Where payment_gid = ',@Payment_Gid,'
						 and payment_isactive = ''Y'' and payment_isremoved = ''N'' ');


#select Query_Update;
				set @Query_Update = '';

				set @Query_Update = Query_Update;

				PREPARE stmt FROM @Query_Update;

				EXECUTE stmt;

				set countRow = (select ROW_COUNT());

				DEALLOCATE PREPARE stmt;



		if countRow <= 0 then

				set Message = 'Error On Update.';

				rollback;

				leave sp_Atma_payment_Set;

		elseif    countRow > 0 then

				set Message = 'SUCCESS';
				commit;
		end if;


	end if;
end