CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Par_Set`(in ls_Action varchar(160), in ls_Create_By int,
in lj_filter json,in lj_pardetails json,
in lj_classification json,
out Message varchar(10000))
sp_Par_Set:BEGIN
declare Query_Insert varchar(1000);
declare Query_Column varchar(500);
declare Query_Value varchar(500);
declare li_Query varchar(1000);
Declare Query_Update varchar(6000);
Declare countRow varchar(6000);
Declare errno int;
Declare msg varchar(1000);

DECLARE done INT DEFAULT 0;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
#...

  DECLARE EXIT HANDLER FOR SQLEXCEPTION,sqlwarning

						BEGIN
							GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
							set Message = concat(errno,msg);
							ROLLBACK;
						END;


	select JSON_LENGTH(lj_filter,'$') into @li_filtercount;
	select JSON_LENGTH(lj_classification,'$') into @li_classification_jsoncount;
	select JSON_LENGTH(lj_pardetails,'$.pardetails_insert') into @lj_pardetails_jsoncount;
	if @li_filtercount = 0 or @li_filtercount is null  then
		set Message = 'No Data In Json. ';
		leave sp_Par_Set;
	 End if;
        if @li_classification_jsoncount = 0 or @li_classification_jsoncount is null  then
		set Message = 'No Entity_Gid In Json. ';
		leave sp_Par_Set;
	End if;
	if @li_classification_jsoncount is not null or @li_classification_jsoncount	<> ''
		   or @li_classification_jsoncount	<> 0 then
		select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Entity_Gid')))into @Entity_Gid;
	End if;

if ls_Action = 'INSERT'  then
  start transaction;
			if @li_filtercount is not null or @li_filtercount <> '' then
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.par_no')))into @par_no;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.par_date')))into @par_date;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.par_year')))into @par_year;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.par_amount')))into @par_amount;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.par_utilized')))into @par_utilized;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.par_balance')))into @par_balance;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.par_isbudgeted')))into @par_isbudgeted;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.par_burstlinewise')))into @par_burstlinewise;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.par_burstmepwise')))into @par_burstmepwise;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.par_desc')))into @par_desc;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.par_status')))into @par_status;
			end if;
  select max(par_no) into @par_number from gal_mst_tpar;

			if @par_number is null or @par_number<>0 or @par_number='' then
				call sp_Generatecode_Get('WITHOUT_DATE', 'PAR', '000','000', @Message);
				select @Message into @parnumber_Generate;
			else
				call sp_Generatecode_Get('WITHOUT_DATE', 'PAR', '000',@par_number, @Message);
				select @Message into @parnumber_Generate;
			end if;
	set Query_Insert ='';
	set Query_Insert = concat('INSERT INTO gal_mst_tpar
						(par_no, par_date, par_year, par_amount, par_isbudgeted,
						 par_burstlinewise, par_burstmepwise, par_desc,par_status, entity_gid,
						 create_by) VALUES
						(''',@parnumber_Generate,''',''',@Par_date,''',''',@par_year,''',''',@par_amount,''',
						''',@par_isbudgeted,''',''',@par_burstlinewise,''',
						''',@par_burstmepwise,''',''',ifnull(@par_desc,''),''',
						''',@par_status,''',''',@Entity_Gid,''',''',ls_Create_By,''')');

	#select  Query_Insert ,1 ;
	set @Query_Update = Query_Insert;
	PREPARE stmt FROM @Query_Update;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
	if countRow >  0 then
		set Message = 'SUCCESS';
        select LAST_INSERT_ID() into @par_gid;
	else
		set Message = 'FAILED';
		rollback;
        leave sp_Par_Set;
	end if;
        #select @par_gid;

if Message ='SUCCESS' then#####gal_mst_tpar
        set @i=0;
        While @i <=  @lj_pardetails_jsoncount -1 do
			select JSON_UNQUOTE(JSON_EXTRACT(lj_pardetails,CONCAT('$.pardetails_insert[',@i,'].pardetails_exptype'))) into @pardetails_exptype;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_pardetails,CONCAT('$.pardetails_insert[',@i,'].pardetails_requestfor'))) into @pardetails_requestfor;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_pardetails,CONCAT('$.pardetails_insert[',@i,'].pardetails_budgeted'))) into @pardetails_budgeted;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_pardetails,CONCAT('$.pardetails_insert[',@i,'].pardetails_desc'))) into @pardetails_desc;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_pardetails,CONCAT('$.pardetails_insert[',@i,'].pardetails_year'))) into @pardetails_year;#### Not Used :: Select From The Table
			select JSON_UNQUOTE(JSON_EXTRACT(lj_pardetails,CONCAT('$.pardetails_insert[',@i,'].pardetails_amount'))) into @pardetails_amount;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_pardetails,CONCAT('$.pardetails_insert[',@i,'].pardetails_remarks'))) into @pardetails_remarks; ### date Validations TO DO
			select JSON_UNQUOTE(JSON_EXTRACT(lj_pardetails,CONCAT('$.pardetails_insert[',@i,'].file_name'))) into @file_name;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_pardetails,CONCAT('$.pardetails_insert[',@i,'].file_path'))) into @file_path;

				if @pardetails_exptype = '' or @pardetails_exptype is null  then
				set Message ='Pardetails Exptype  Is Not Given';
				rollback;
				leave sp_Par_Set;
				end if;

				if @pardetails_requestfor = '' or @pardetails_requestfor is null  then
				set Message ='Pardetails Requestfor  Is Not Given';
				rollback;
				leave sp_Par_Set;
				end if;

                if @pardetails_budgeted = '' or @pardetails_budgeted is null  then
				set Message ='Pardetails Budgeted  Is Not Given';
				rollback;
				leave sp_Par_Set;
				end if;

                if @pardetails_year = '' or @pardetails_year is null  then
				set Message ='Pardetails Year  Is Not Given';
				rollback;
				leave sp_Par_Set;
				end if;

                if @pardetails_amount = '' or @pardetails_amount is null  then
				set Message ='Pardetails Amount  Is Not Given';
				rollback;
				leave sp_Par_Set;
				end if;


				if @file_name = '' or @file_name is null  then
				set Message ='FileName  Is Not Given';
				rollback;
				leave sp_Par_Set;
				end if;

                if @file_path = '' or @file_path is null  then
				set Message ='FilePath  Is Not Given';
				rollback;
				leave sp_Par_Set;
				end if;

				call sp_File_Set('Insert','a',@file_Id,@file_name,@file_path,
								lj_Classification, '{}',ls_Create_By ,@Message);
				select @Message into @Out_Msg_filegid;
                #select @Out_Msg_filegid;
                if @Out_Msg_filegid='FAIL'then
                set Message='FAIL FILE';
                rollback;
                end if;
				SET @Out_Msg_file_gid = (SELECT SPLIT_STR((@Out_Msg_filegid), ',', 1));select @Out_Msg_file_gid;
				SET @Out_Msg_file_msg = (SELECT SPLIT_STR((@Out_Msg_filegid), ',', 2));select @Out_Msg_file_msg;


if @Out_Msg_file_msg ='SUCCESS' then

				set Query_Insert='';
				set Query_Insert = concat('INSERT INTO gal_mst_tpardetails
				( pardetails_pargid, pardetails_exptype, pardetails_requestfor,
				pardetails_budgeted, pardetails_desc, pardetails_year, pardetails_amount, pardetails_remarks,
				pardetails_filegid, entity_gid, create_by) VALUES
				(''',@par_gid,''',''',@pardetails_exptype,''',
                ''',@pardetails_requestfor,''',
                ''',@pardetails_budgeted,''',
				''',ifnull(@pardetails_desc,''),''',
                ''',@pardetails_year,''',
				''',@pardetails_amount,''',
                ''',ifnull(@pardetails_remarks,''),''',
                ''',@Out_Msg_file_gid,''',
                ''',@Entity_Gid,''',
                ''',ls_Create_By,''')');

				set @Query_Update = Query_Insert;
				PREPARE stmt FROM @Query_Update;
				EXECUTE stmt;
				set countRow = (select ROW_COUNT());
				DEALLOCATE PREPARE stmt;
				if countRow >  0 then
				set @Message1 = 'SUCCESS';
				else
				set @Message1 = ' FAILED';
				rollback;
				leave sp_Par_Set;
				end if;
				end if;#Out_Msg_file_msg
        set @i = @i+1;
		End while;
end if;####gal_mst_tpar
        if @Message1='SUCCESS' then
        call sp_Trans_Set('Insert','PAR_STATUS',@par_gid,
										'PENDING-APPROVAL','G','PAR_CHECKER',
                                        'MAKER',@Entity_Gid,ls_Create_By, @Message);
					select @Message into @out_msg_tran ;
                    if @out_msg_tran = 'FAIL' then
					set Message = 'Failed On Tran Insert';
					rollback;
					leave sp_Par_Set;
                    end if;
                    if countRow >  0 then
                    commit;
                    END IF;

		end if;
    #commit;
end if;

if ls_Action = 'UPDATE'  then
  start transaction;
  #####par_table update
			if @li_filtercount is not null or @li_filtercount <> '' then
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.new_insert')))into @new_insert;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.par_gid')))into @par_gid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.par_no')))into @par_no;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.par_date')))into @par_date;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.par_year')))into @par_year;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.par_amount')))into @par_amount;select @par_amount;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.par_utilized')))into @par_utilized;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.par_balance')))into @par_balance;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.par_isbudgeted')))into @par_isbudgeted;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.par_burstlinewise')))into @par_burstlinewise;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.par_burstmepwise')))into @par_burstmepwise;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.par_desc')))into @par_desc;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.par_status')))into @par_status;

			end if;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Update_By')))into @Update_By;
            #select @Update_By;
			#select par_gid from gal_mst_tpar where par_gid=@par_gid and par_isactive='Y' into @pargid;

		set Query_Update = '';

			#if @par_gid is null or @par_gid = '' or @par_gid = 0 then
			#set @par_gid=@par_gid;
            #set Message = 'Par Gid Is Needed. ';
			#leave sp_Par_Set;
			#end if;


            if  @par_date <> '' and @par_date <> 'null' then
			set @par_date=date_format(@par_date,'%Y-%m-%d');
            else
            set Message='Par Date Is Needed.' ;
			leave sp_Par_Set;
			end if;

            if @par_year <>'null' and @par_year <> '' then
			set Query_Update = concat(Query_Update,',par_year = ''',@par_year,'''  ');
			else
			set Message='Par Year Is Needed.' ;
			leave sp_Par_Set;
			End if;

            if @par_amount <>'null' and @par_amount <> '' then
			set Query_Update = concat(Query_Update,',par_amount = ''',@par_amount,'''  ');
			else
			set Message='Par Amount Is Needed.' ;
			leave sp_Par_Set;
			End if;

            if @par_utilized <>'null' and @par_utilized <> '' then
			set Query_Update = concat(Query_Update,',par_utilized = ''',@par_utilized,'''  ');
			else
			set Message='Par Utilized Is Needed.' ;
			leave sp_Par_Set;
			End if;
            select @par_balance;
            if @par_balance <>'null' and @par_balance <> '' then
			set Query_Update = concat(Query_Update,',par_balance = ''',@par_balance,'''  ');
			else
            set Message='Par Balance Is Needed.' ;
			leave sp_Par_Set;
			End if;

            if @par_isbudgeted <>'null' and @par_isbudgeted <> '' then
			set Query_Update = concat(Query_Update,',par_isbudgeted = ''',@par_isbudgeted,'''  ');
			else
			set Message='Par Isbudgeted Is Needed.' ;
			leave sp_Par_Set;
			End if;

            if @par_burstlinewise <>'null' and @par_burstlinewise <> '' then
			set Query_Update = concat(Query_Update,',par_burstlinewise = ''',@par_burstlinewise,'''  ');
			else
			set Message='Par Burstlinewise Is Needed.' ;
			leave sp_Par_Set;
			End if;

			if @par_burstmepwise <>'null' and @par_burstmepwise <> '' then
			set Query_Update = concat(Query_Update,',par_burstmepwise = ''',@par_burstmepwise,'''  ');
			else
			set Message='Par Burstmepwise Is Needed.' ;
			leave sp_Par_Set;
			End if;

            if @par_desc <>'null' and @par_desc <> '' then
			set Query_Update = concat(Query_Update,',par_desc = ''',@par_desc,'''  ');
			else
			set Query_Update = concat(Query_Update,',par_desc = null  ');
			End if;

            if @par_status <>'null' and @par_status <> '' then
			set Query_Update = concat(Query_Update,',par_status = ''',@par_status,'''  ');
			else
            set Message='Par Status Is Needed.' ;
			leave sp_Par_Set;

			End if;


 set Query_Insert = '';

				set Query_Insert = concat('Update gal_mst_tpar
							  set update_date = CURRENT_TIMESTAMP,
                              update_by=',ls_Create_By,'',Query_Update,'
							  Where par_gid = ',@par_gid,'
							  and par_isactive = ''Y'' and par_isremoved = ''N'' ');

		select  @Query_Update,1;
		set @Query_Update = Query_Insert;
        select @Query_Update;
		PREPARE stmt FROM @Query_Update;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow > 0 then
		set Message = 'SUCCESS';
        #select LAST_INSERT_ID() into @newpargid;
        #select Message;
        #commit;#####pardetails and files
        set @i=0;
        While @i <=  @lj_pardetails_jsoncount -1 do
        select 1;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_pardetails,CONCAT('$.pardetails_insert[',@i,'].file_name'))) into @file_name; SELECT @file_name;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_pardetails,CONCAT('$.pardetails_insert[',@i,'].file_path'))) into @file_path; SELECT @file_path;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_pardetails,CONCAT('$.pardetails_insert[',@i,'].pardetails_gid'))) into @pardetails_gid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_pardetails,CONCAT('$.pardetails_insert[',@i,'].pardetails_exptype'))) into @pardetails_exptype;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_pardetails,CONCAT('$.pardetails_insert[',@i,'].pardetails_requestfor'))) into @pardetails_requestfor;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_pardetails,CONCAT('$.pardetails_insert[',@i,'].pardetails_budgeted'))) into @pardetails_budgeted;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_pardetails,CONCAT('$.pardetails_insert[',@i,'].pardetails_desc'))) into @pardetails_desc;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_pardetails,CONCAT('$.pardetails_insert[',@i,'].pardetails_year'))) into @pardetails_year;#### Not Used :: Select From The Table
			select JSON_UNQUOTE(JSON_EXTRACT(lj_pardetails,CONCAT('$.pardetails_insert[',@i,'].pardetails_amount'))) into @pardetails_amount;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_pardetails,CONCAT('$.pardetails_insert[',@i,'].pardetails_remarks'))) into @pardetails_remarks; ### date Validations TO DO
			select JSON_UNQUOTE(JSON_EXTRACT(lj_pardetails,CONCAT('$.pardetails_insert[',@i,'].pardetails_filegid'))) into @pardetails_filegid; ### date Validations TO DO

		set Query_Update='';
			if @file_name is not null or @file_name <> '' then
			set Query_Update = concat(Query_Update,',file_name = ''',@file_name,'''  ');
			End if;

  			if @file_path is not null or @file_path <> '' then
			set Query_Update = concat(Query_Update,',file_path = ''',@file_path,'''  ');
			End if;
            select Query_Update;
            #set @pardetailsfilegid='';
			select pardetails_filegid from gal_mst_tpardetails
			where pardetails_pargid=@par_gid and pardetails_gid=@pardetails_gid into @pardetailsfilegid;
        #select @pardetailsfilegid;

if @pardetails_filegid is null or @pardetails_filegid='' then
set Query_Update='';
			call sp_File_Set('Insert','a',@file_Id,@file_name,@file_path,
								lj_Classification, '{}',ls_Create_By ,@Message);
				select @Message into @Out_Msg_filegid;
                #select @Out_Msg_filegid;
                if @Out_Msg_filegid='FAIL'then
                set Message='FAIL FILE';
                rollback;
                end if;
				SET @Out_Msg_file_gid = (SELECT SPLIT_STR((@Out_Msg_filegid), ',', 1));select @Out_Msg_file_gid;
				SET @Out_Msg_file_msg = (SELECT SPLIT_STR((@Out_Msg_filegid), ',', 2));select @Out_Msg_file_msg;

select @Out_Msg_file_msg;

else
select 11;
#set Query_Update='';

			set Query_Update = concat('Update gal_mst_tfile
										set update_date = CURRENT_TIMESTAMP,update_by=',ls_Create_By,'
                                        ',Query_Update,'
										Where file_gid = ',@pardetailsfilegid,' ');
                                        select Query_Update;
			set @Insert_query = Query_Update;
            select @Insert_query;
			PREPARE stmt FROM @Insert_query;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;
			if countRow >  0 then
			set Message = 'SUCCESS';
            #select Message;
			else
			set Message = 'FAILED';
			rollback;
			end if;

end if;


set Query_Update='';
			if @pardetails_exptype <>'null' and @pardetails_exptype <> '' then
			set Query_Update = concat(Query_Update,',pardetails_exptype = ''',@pardetails_exptype,'''  ');
			else
			set Message='Pardetails Exptype Is Needed.' ;
			leave sp_Par_Set;
			End if;

            if @pardetails_requestfor <>'null' and @pardetails_requestfor <> '' then
			set Query_Update = concat(Query_Update,',pardetails_requestfor = ''',@pardetails_requestfor,'''  ');
			else
			set Message='Pardetails Requestfor Is Needed.' ;
			leave sp_Par_Set;
			End if;

            if @pardetails_budgeted <>'null' and @pardetails_budgeted <> '' then
			set Query_Update = concat(Query_Update,',pardetails_budgeted = ''',@pardetails_budgeted,'''  ');
			else
			set Message='Pardetails Budgeted Is Needed.' ;
			leave sp_Par_Set;
			End if;

            if @pardetails_desc <>'null' and @pardetails_desc <> '' then
			set Query_Update = concat(Query_Update,',pardetails_desc = ''',@pardetails_desc,'''  ');
			End if;

            if @pardetails_remarks <>'null' and @pardetails_remarks <> '' then
			set Query_Update = concat(Query_Update,',pardetails_remarks = ''',@pardetails_remarks,'''  ');
			End if;

            if @pardetails_year <>'null' and @pardetails_year <> '' then
			set Query_Update = concat(Query_Update,',pardetails_year = ''',@pardetails_year,'''  ');
			else
			set Message='Pardetails Year Is Needed.' ;
			leave sp_Par_Set;
			End if;

            if @pardetails_amount <>'null' and @pardetails_amount <> '' then
			set Query_Update = concat(Query_Update,',pardetails_amount = ''',@pardetails_amount,'''  ');
			else
			set Message='Pardetails Amount Is Needed.' ;
			leave sp_Par_Set;
			End if;
                     select  Query_Update;
if @pardetails_gid is null or @pardetails_gid=''then
select 12233;
	set Query_Insert='';
    set Query_Insert = concat('INSERT INTO gal_mst_tpardetails
				( pardetails_pargid, pardetails_exptype, pardetails_requestfor,
				pardetails_budgeted, pardetails_desc, pardetails_year, pardetails_amount, pardetails_remarks,
				pardetails_filegid, entity_gid, create_by) VALUES
				(''',@par_gid,''',''',@pardetails_exptype,''',
                ''',@pardetails_requestfor,''',
                ''',@pardetails_budgeted,''',
				''',ifnull(@pardetails_desc,''),''',
                ''',@pardetails_year,''',
				''',@pardetails_amount,''',
                ''',ifnull(@pardetails_remarks,''),''',
                ''',@Out_Msg_file_gid,''',
                ''',@Entity_Gid,''',
                ''',ls_Create_By,''')');



else
select 123;


				set Query_Insert = concat('Update gal_mst_tpardetails
								set update_date = CURRENT_TIMESTAMP,
								update_by=',ls_Create_By,'',Query_Update,'
								Where pardetails_gid= ',@pardetails_gid,'
								and par_isactive = ''Y'' and par_isremoved = ''N'' ');
end if;
				select Query_Insert;
				set @Query_Update = Query_Insert;
				PREPARE stmt FROM @Query_Update;
				EXECUTE stmt;
				set countRow = (select ROW_COUNT());
				DEALLOCATE PREPARE stmt;
				if countRow >  0 then
					set Message = 'SUCCESS';
					commit;
				else
				set Message = ' FAILED';
				rollback;
				leave sp_Par_Set;
				end if;

#end if;#Out_Msg_file_msg
        set @i = @i+1;
		End while;
        commit;

        else###par_table update
        set Message = 'FAILED';
        rollback;
		end if;

  end if;###ls_Action update
  if ls_Action = 'Approvel'  then
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Par_Gid')))into @Par_Gid;select @Par_Gid;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Par_status')))into @Par_status;select @Par_status;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.tran_remark')))into @tran_remark;select @tran_remark;

		set Query_Insert='';
				set Query_Insert = concat('Update gal_mst_tpar
								set par_status=''',@Par_status,'''
								Where par_gid= ',@Par_Gid,'
								and par_isactive = ''Y'' and par_isremoved = ''N'' ');

                                select Query_Insert;
				set @Query_Update = Query_Insert;
				PREPARE stmt FROM @Query_Update;
				EXECUTE stmt;
				set countRow = (select ROW_COUNT());
				DEALLOCATE PREPARE stmt;
				if countRow >  0 then
					set Message = 'SUCCESS';
                    call sp_Trans_Set('Update','PAR_STATUS',@Par_Gid,
			@Par_Status,'C',ls_Create_By,ifnull(@tran_remark,''),@Entity_Gid,ls_Create_By,@message);
			select @message into @out_msg_tran ;
				else
				set Message = ' FAILED';
				rollback;
				leave sp_Par_Set;
				end if;


  end if;
END