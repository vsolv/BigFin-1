CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Mep_Set`(in ls_Action varchar(160), in ls_Create_By int,
in lj_filter json,in lj_pardetails json,
in lj_classification json,
out Message varchar(10000))
sp_Mep_Set:BEGIN
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
	select JSON_LENGTH(lj_pardetails,'$.mepdetails_insert') into @lj_pardetails_jsoncount;
	if @li_filtercount = 0 or @li_filtercount is null  then
		set Message = 'No Data In Json. ';
		leave sp_Mep_Set;
	 End if;
        if @li_classification_jsoncount = 0 or @li_classification_jsoncount is null  then
		set Message = 'No Entity_Gid In Json. ';
		leave sp_Mep_Set;
	End if;
	if @li_classification_jsoncount is not null or @li_classification_jsoncount	<> ''
		   or @li_classification_jsoncount	<> 0 then
		select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Entity_Gid')))into @Entity_Gid;
	End if;

if ls_Action = 'INSERT'  then
  start transaction;
			if @li_filtercount is not null or @li_filtercount <> '' then
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_no')))into @mep_no;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_name')))into @mep_name;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_raisor')))into @mep_raisor;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_amount')))into @mep_amount;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_finyear')))into @mep_finyear;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_type')))into @mep_type;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_startdate')))into @mep_startdate;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_enddate')))into @mep_enddate;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_branchgid')))into @mep_branchgid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_mode')))into @mep_mode;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_parno')))into @mep_parno;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_budgeted')))into @mep_budgeted;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_projectowner')))into @mep_projectowner;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_requestfor')))into @mep_requestfor;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_budgetowner')))into @mep_budgetowner;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_justification')))into @mep_justification;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_status')))into @mep_status;
			#select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_isclosed')))into @mep_isclosed;
			end if;

			select max(mep_no) into @mep_number from gal_mst_tmep;

			if @mep_number is null or @mep_number<>0 or @mep_number='' then
				call sp_Generatecode_Get('WITHOUT_DATE', 'MEP', '000','000', @Message);
				select @Message into @mep_number_Generate;
			else
				call sp_Generatecode_Get('WITHOUT_DATE', 'MEP', '000',@mep_number, @Message);
				select @Message into @mep_number_Generate;
			end if;
            SELECT @mep_number_Generate;

	set Query_Insert ='';
	set Query_Insert = concat('INSERT INTO gal_mst_tmep
						( mep_no, mep_name, mep_raisor, mep_amount, mep_finyear, mep_type, mep_startdate, mep_enddate, mep_branchgid,
                        mep_mode, mep_parno,mep_budgeted, mep_projectowner, mep_requestfor, mep_budgetowner, mep_justification,
                        mep_status,entity_gid, create_by) VALUES
						(''',@mep_number_Generate,''',''',@mep_name,''',''',@mep_raisor,''',''',@mep_amount,''',''',@mep_finyear,''',
						''',@mep_type,''',''',@mep_startdate,''',''',@mep_enddate,''',''',@mep_branchgid,''',''',@mep_mode,''',
                        ''',@mep_parno,''',''',@mep_budgeted,''',''',@mep_projectowner,''',''',@mep_requestfor,''',
						''',@mep_budgetowner,''',''',@mep_justification,''',''',@mep_status,''',
						''',@Entity_Gid,''',''',ls_Create_By,''')');

	select  Query_Insert ,1 ;
	set @Query_Update = Query_Insert;
	PREPARE stmt FROM @Query_Update;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
	if countRow >  0 then
		set Message = 'SUCCESS';
        select LAST_INSERT_ID() into @mep_gid;
	else
		set Message = 'FAILED';
		rollback;
        leave sp_Mep_Set;
	end if;
        #select @par_gid;

if Message ='SUCCESS' then#####gal_mst_tpar
        set @i=0;
        While @i <=  @lj_pardetails_jsoncount -1 do
			select JSON_UNQUOTE(JSON_EXTRACT(lj_pardetails,CONCAT('$.mepdetails_insert[',@i,'].mepdetails_productcode'))) into @mepdetails_productcode;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_pardetails,CONCAT('$.mepdetails_insert[',@i,'].mepdetails_desc'))) into @mepdetails_desc;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_pardetails,CONCAT('$.mepdetails_insert[',@i,'].mepdetails_qty'))) into @mepdetails_qty;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_pardetails,CONCAT('$.mepdetails_insert[',@i,'].mepdetails_unitprice'))) into @mepdetails_unitprice;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_pardetails,CONCAT('$.mepdetails_insert[',@i,'].mepdetails_totalamt'))) into @mepdetails_totalamt;#### Not Used :: Select From The Table

			select  product_gid from gal_mst_tproduct where product_code=@mepdetails_productcode into @mepdetails_productgid;
				if @mepdetails_productgid = '' or @mepdetails_productgid is null  then
				set Message ='mepdetails_productgid Is Not Given';
				rollback;
				leave sp_Mep_Set;
				end if;

				if @mepdetails_desc = '' or @mepdetails_desc is null  then
				set Message ='mepdetails_desc  Is Not Given';
				rollback;
				leave sp_Mep_Set;
				end if;

                if @mepdetails_qty = '' or @mepdetails_qty is null  then
				set Message ='mepdetails_qty  Is Not Given';
				rollback;
				leave sp_Mep_Set;
				end if;

                if @mepdetails_unitprice = '' or @mepdetails_unitprice is null  then
				set Message ='mepdetails_unitprice  Is Not Given';
				rollback;
				leave sp_Mep_Set;
				end if;



				set Query_Insert='';
				set Query_Insert = concat('INSERT INTO gal_mst_tmepdetails
				( mepdetails_mepgid, mepdetails_productgid, mepdetails_desc, mepdetails_qty, mepdetails_unitprice,
                mepdetails_totalamt,entity_gid, create_by) VALUES
				(''',@mep_gid,''',''',@mepdetails_productgid,''',
                ''',@mepdetails_desc,''',
                ''',@mepdetails_qty,''',
                ''',@mepdetails_unitprice,''',
				''',@mepdetails_totalamt,''',
                ''',@Entity_Gid,''',
                ''',ls_Create_By,''')');

				set @Query_Update = Query_Insert;
                select @Query_Update;
				PREPARE stmt FROM @Query_Update;
				EXECUTE stmt;
				set countRow = (select ROW_COUNT());
				DEALLOCATE PREPARE stmt;
				if countRow >  0 then
				set @Message1 = 'SUCCESS';
				else
				set @Message1 = ' FAILED';
				rollback;
				leave sp_Mep_Set;
				end if;

        set @i = @i+1;
		End while;
end if;####gal_mst_tmep
        if @Message1='SUCCESS' then
        call sp_Trans_Set('Insert','MEP_STATUS',@mep_gid,
										'PENDING-APPROVAL','G','PAR_CHECKER',
                                        'MAKER',@Entity_Gid,ls_Create_By, @Message);
					select @Message into @out_msg_tran ;
                    #select @out_msg_tran;
                    if @out_msg_tran = 'FAIL' then
					set Message = 'Failed On Tran Insert';
					rollback;
					leave sp_Mep_Set;
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
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_gid')))into @mep_gid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_no')))into @mep_no;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_name')))into @mep_name;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_raisor')))into @mep_raisor;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_amount')))into @mep_amount;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_finyear')))into @mep_finyear;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_type')))into @mep_type;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_startdate')))into @mep_startdate;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_enddate')))into @mep_enddate;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_branchgid')))into @mep_branchgid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_mode')))into @mep_mode;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_parno')))into @mep_parno;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_budgeted')))into @mep_budgeted;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_projectowner')))into @mep_projectowner;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_justification')))into @mep_justification;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_requestfor')))into @mep_requestfor;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.mep_budgetowner')))into @mep_budgetowner;

			end if;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.update_by')))into @update_by;
            #select @Update_By;
			#select par_gid from gal_mst_tpar where par_gid=@par_gid and par_isactive='Y' into @pargid;

		set Query_Update = '';

			#if @par_gid is null or @par_gid = '' or @par_gid = 0 then
			#set @par_gid=@par_gid;
            #set Message = 'Par Gid Is Needed. ';
			#leave sp_Mep_Set;
			#end if;

            if  @mep_startdate <> '' and @mep_startdate <> 'null' then
			set @mep_startdate=date_format(@mep_startdate,'%Y-%m-%d');
            set Query_Update = concat(Query_Update,',mep_startdate = ''',@mep_startdate,'''  ');
			end if;

            if  @mep_enddate <> '' and @mep_enddate <> 'null' then
			set @mep_enddate=date_format(@mep_enddate,'%Y-%m-%d');
            set Query_Update = concat(Query_Update,',mep_enddate = ''',@mep_enddate,'''  ');

			end if;

            if @mep_raisor <>'null' and @mep_raisor <> '' then
			set Query_Update = concat(Query_Update,',mep_raisor = ''',@mep_raisor,'''  ');
			End if;

            if @mep_requestfor <>'null' and @mep_requestfor <> '' then
			set Query_Update = concat(Query_Update,',mep_requestfor = ''',@mep_requestfor,'''  ');
			End if;

            if @mep_raisor <>'null' and @mep_raisor <> '' then
			set Query_Update = concat(Query_Update,',mep_raisor = ''',@mep_raisor,'''  ');
			End if;

            if @mep_amount <>'null' and @mep_amount <> '' then
			set Query_Update = concat(Query_Update,',mep_amount = ''',@mep_amount,'''  ');
			End if;

            if @mep_finyear <>'null' and @mep_finyear <> '' then
			set Query_Update = concat(Query_Update,',mep_finyear = ''',@mep_finyear,'''  ');
			End if;

            if @mep_type <>'null' and @mep_type <> '' then
			set Query_Update = concat(Query_Update,',mep_type = ''',@mep_type,'''  ');
			End if;

            if @mep_branchgid <>'null' and @mep_branchgid <> '' then
			set Query_Update = concat(Query_Update,',mep_branchgid = ''',@mep_branchgid,'''  ');
			End if;

            if @mep_mode <>'null' and @mep_mode <> '' then
			set Query_Update = concat(Query_Update,',mep_mode = ''',@mep_mode,'''  ');
			End if;

			if @mep_parno <>'null' and @mep_parno <> '' then
			set Query_Update = concat(Query_Update,',mep_parno = ''',@mep_parno,'''  ');

			End if;

            if @mep_budgeted <>'null' and @mep_budgeted <> '' then
			set Query_Update = concat(Query_Update,',mep_budgeted = ''',@mep_budgeted,'''  ');
			End if;

            if @mep_projectowner <>'null' and @mep_projectowner <> '' then
			set Query_Update = concat(Query_Update,',mep_projectowner = ''',@mep_projectowner,'''  ');
			End if;
			if @mep_justification <>'null' and @mep_justification <> '' then
			set Query_Update = concat(Query_Update,',mep_justification = ''',@mep_justification,'''  ');
			End if;

		select  Query_Update,11;
        select ls_Create_By;
        select @mep_gid;

	set Query_Insert='';
				set Query_Insert = concat('Update gal_mst_tmep
							  set Update_date = CURRENT_TIMESTAMP,
                              update_by=',ls_Create_By,'',Query_Update,'
							  Where mep_gid = ',@mep_gid,'
							  and mep_isactive = ''Y'' and mep_isremoved = ''N'' ');




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

			select JSON_UNQUOTE(JSON_EXTRACT(lj_pardetails,CONCAT('$.mepdetails_insert[',@i,'].mepdetails_gid'))) into @mepdetails_gid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_pardetails,CONCAT('$.mepdetails_insert[',@i,'].mepdetails_mepgid'))) into @mepdetails_mepgid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_pardetails,CONCAT('$.mepdetails_insert[',@i,'].mepdetails_productcode'))) into @mepdetails_productcode;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_pardetails,CONCAT('$.mepdetails_insert[',@i,'].mepdetails_desc'))) into @mepdetails_desc;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_pardetails,CONCAT('$.mepdetails_insert[',@i,'].mepdetails_qty'))) into @mepdetails_qty;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_pardetails,CONCAT('$.mepdetails_insert[',@i,'].mepdetails_unitprice'))) into @mepdetails_unitprice;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_pardetails,CONCAT('$.mepdetails_insert[',@i,'].mepdetails_totalamt'))) into @mepdetails_totalamt;
			select  product_gid from gal_mst_tproduct where product_code=@mepdetails_productcode into @mepdetails_productgid;


set Query_Update='';
			if @mepdetails_productcode <>'null' and @mepdetails_productcode <> '' then
			set Query_Update = concat(Query_Update,',mepdetails_productgid = ''',@mepdetails_productgid,'''  ');
            select Query_Update;
			else
			set Message='Product Details Exptype Is Needed.' ;
			leave sp_Mep_Set;
			End if;

            if @mepdetails_qty <>'null' and @mepdetails_qty <> '' then
			set Query_Update = concat(Query_Update,',mepdetails_qty = ''',@mepdetails_qty,'''  ');
			else
			set Message='Quantity Is Needed.' ;
			leave sp_Mep_Set;
			End if;

            if @mepdetails_unitprice <>'null' and @mepdetails_unitprice <> '' then
			set Query_Update = concat(Query_Update,',mepdetails_unitprice = ''',@mepdetails_unitprice,'''  ');
			else
			set Message='Unit Price Is Needed.' ;
			leave sp_Mep_Set;
			End if;

            if @mepdetails_desc <>'null' and @mepdetails_desc <> '' then
			set Query_Update = concat(Query_Update,',mepdetails_desc = ''',@mepdetails_desc,'''  ');
			else
			set Query_Update = concat(Query_Update,',mepdetails_desc = null  ');
			leave sp_Mep_Set;
			End if;

            if @mepdetails_totalamt <>'null' and @mepdetails_totalamt <> '' then
			set Query_Update = concat(Query_Update,',mepdetails_totalamt = ''',@mepdetails_totalamt,'''  ');
			else
			#set Query_Update = concat(Query_Update,',pardetails_remarks = null  ');
            set Message='Total Amount Is Needed.' ;
			leave sp_Mep_Set;
			End if;


			select  Query_Update;
if @mepdetails_gid is null or @mepdetails_gid=''then
select 12233;
	set Query_Insert='';
    set Query_Insert = concat('INSERT INTO gal_mst_tmepdetails
				( mepdetails_mepgid, mepdetails_productgid, mepdetails_desc, mepdetails_qty, mepdetails_unitprice,
                mepdetails_totalamt,entity_gid, create_by) VALUES
				(''',@mep_gid,''',''',@mepdetails_productgid,''',
                ''',@mepdetails_desc,''',
                ''',@mepdetails_qty,''',
                ''',@mepdetails_unitprice,''',
				''',@mepdetails_totalamt,''',
                ''',@Entity_Gid,''',
                ''',ls_Create_By,''')');



else
select 123;

				set Query_Insert='';
				set Query_Insert = concat('Update gal_mst_tmepdetails
								set update_date = CURRENT_TIMESTAMP,
								update_by=',ls_Create_By,'',Query_Update,'
								Where mepdetails_gid= ',@mepdetails_gid,'
								and mepdetails_isactive = ''Y'' and mepdetails_isremoved = ''N'' ');
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
				leave sp_Mep_Set;
				end if;

        set @i = @i+1;
		End while;
        commit;

        else###par_table update
        set Message = 'FAILED';
        rollback;
		end if;

  end if;###ls_Action update
  if ls_Action = 'Approvel'  then
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Mep_Gid')))into @Mep_Gid;select @Mep_Gid;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Mep_status')))into @Mep_status;select @Mep_status;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.tran_remark')))into @tran_remark;select @tran_remark;

		set Query_Insert='';
				set Query_Insert = concat('Update gal_mst_tmep
								set mep_status=''',@Mep_status,'''
								Where mep_gid= ',@Mep_Gid,'
								and mep_isactive = ''Y'' and mep_isremoved = ''N'' ');

				select Query_Insert;
				set @Query_Update = Query_Insert;
				PREPARE stmt FROM @Query_Update;
				EXECUTE stmt;
				set countRow = (select ROW_COUNT());
                select countRow;
				DEALLOCATE PREPARE stmt;
				if countRow >  0 then
					select 1;
					set Message = 'SUCCESS';
                    call sp_Trans_Set('Update','MEP_STATUS',@Mep_Gid,
			@Mep_Status,'C',ls_Create_By,ifnull(@tran_remark,''),@Entity_Gid,ls_Create_By,@message);
			select @message into @out_msg_tran ;
				else
				set Message = ' FAILED';
				rollback;
				leave sp_Mep_Set;
				end if;


  end if;
END