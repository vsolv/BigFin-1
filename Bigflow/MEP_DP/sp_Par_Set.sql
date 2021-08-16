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

						DECLARE EXIT HANDLER FOR SQLEXCEPTION
						BEGIN
							GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
							set Message = concat(errno , msg);
							ROLLBACK;
						END;
if ls_Action = 'INSERT'  then
	start transaction;
	select JSON_LENGTH(lj_filter,'$') into @li_filtercount;
	select JSON_LENGTH(lj_classification,'$') into @li_classification_jsoncount;
	select JSON_LENGTH(lj_pardetails,'$.pardetails_insert') into @lj_pardetails_jsoncount;
	if @li_filtercount = 0 or @li_filtercount is null  then
		set Message = 'No Data In Json. ';
		leave sp_Par_Set;
	End if;
    /*if @lj_pardetails_jsoncount = 0 or @lj_pardetails_jsoncount is null  then
		set Message = 'No Data For Par Details. ';
		leave sp_Par_Set;
	End if;*/
	if @li_classification_jsoncount = 0 or @li_classification_jsoncount is null  then
		set Message = 'No Entity_Gid In Json. ';
		leave sp_Par_Set;
	End if;
	if @li_classification_jsoncount is not null or @li_classification_jsoncount	<> ''
		   or @li_classification_jsoncount	<> 0 then
		select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Entity_Gid')))into @Entity_Gid;
	End if;
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

	set Query_Insert ='';
	set Query_Insert = concat('INSERT INTO gal_mst_tpar
	( par_no, par_date, par_year, par_amount, par_isbudgeted,
	par_burstlinewise, par_burstmepwise, par_desc,par_status, entity_gid,
	create_by) VALUES
	(''',@par_no,''',''',@par_date,''',''',@par_year,''',''',@par_amount,''',
    ''',@par_isbudgeted,''',''',@par_burstlinewise,''',
	''',@par_burstmepwise,''',''',@par_desc,''',''',@par_status,''',''',@Entity_Gid,''',''',ls_Create_By,''')');

	#select  Query_Insert ,1 ;
	set @Query_Update = Query_Insert;
	PREPARE stmt FROM @Query_Update;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
	if countRow >  0 then
		set Message = 'SUCCESS';
        select LAST_INSERT_ID() into @par_gid;
        select @par_gid;

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

                        call sp_File_Set('Insert','a',@file_Id,@file_name,@file_path,
																lj_Classification, '{}',ls_Create_By ,@Message);
														 select @Message into @Out_Msg_filegid;
                                                         select @Out_Msg_filegid;

							SET @Out_Msg_file_gid = (SELECT SPLIT_STR((@Out_Msg_filegid), ',', 1));select @Out_Msg_file_gid;
							SET @Out_Msg_file_msg = (SELECT SPLIT_STR((@Out_Msg_filegid), ',', 2));select @Out_Msg_file_msg;
                            if @Out_Msg_file_msg ='SUCCESS' then
							set Query_Insert='';
                            set Query_Insert = concat('INSERT INTO gal_mst_tpardetails
									( pardetails_pargid, pardetails_exptype, pardetails_requestfor,
									pardetails_budgeted, pardetails_desc, pardetails_year, pardetails_amount, pardetails_remarks,
									pardetails_filegid, entity_gid, create_by
									) VALUES
									(''',@par_gid,''',''',@pardetails_exptype,''',''',@pardetails_requestfor,''',''',@pardetails_budgeted,''',
									''',@pardetails_desc,''',''',@pardetails_year,''',
									''',@pardetails_amount,''',''',@pardetails_remarks,''',''',@Out_Msg_file_gid,''',''',@Entity_Gid,''',''',ls_Create_By,''')');
                            SELECT @par_gid,@pardetails_exptype,@pardetails_requestfor,@pardetails_budgeted,@pardetails_desc,@pardetails_year,
                            @pardetails_amount,@pardetails_remarks,@Out_Msg_file_gid,@Entity_Gid,ls_Create_By;
                            set @Query_Update = Query_Insert;
							PREPARE stmt FROM @Query_Update;
							EXECUTE stmt;
							set countRow = (select ROW_COUNT());
							DEALLOCATE PREPARE stmt;
							if countRow >  0 then
								set Message = 'SUCCESS';
                            else
								set Message = ' FAILED';
								rollback;
								end if;
                            end if;#Out_Msg_file_msg


        set @i = @i+1;
		End while;





else
		set Message = ' FAILED';
		rollback;
	end if;
end if;

END