CREATE DEFINER=`developer`@`%` PROCEDURE `sp_GRNDetails_Set`(IN `ls_Action` varchar(64),IN `ls_Type` varchar(64),
IN `lj_filter` json,IN `IS_Commit` char,IN `lj_Classification` json,
IN `ls_create_by` varchar(16) , OUT `Message` varchar(2014)
)
sp_GRNDetails_Set:BEGIN
### SELVA SEP 20 2018

declare Updated_Row int;
declare Query_Insert varchar(1000);
declare ls_no varchar(1000);
declare Qry_Header varchar(1000);
declare Query_Update varchar(9000);
declare errno int;
declare msg varchar(1000);
declare countRow int;
declare z int;
declare i int;
declare j int;
declare x int;
declare lj json;

# Null Selected Output
DECLARE done INT DEFAULT 0;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
#...

	DECLARE EXIT HANDLER FOR SQLEXCEPTION,sqlwarning
    BEGIN

    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
    set Message = concat(errno , msg);
    ROLLBACK;
    END;

    SET SESSION group_concat_max_len=4294967295;
    #### Check The Classification data Received or Not :: Validations.

     select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid[0]'))) into @Entity_Gid;

             if @Entity_Gid is  null or @Entity_Gid = 0 or @Entity_Gid = '' then
					set Message = 'Entity Gid Is Needed.';
                    leave sp_GRNDetails_Set;
             End if;

        ## TO DO :: Also Check Entity Details Level
start transaction;
set autocommit = 0 ;
if ls_Type = 'GRN_INSERT' then

		select JSON_LENGTH(lj_filter,'$') into @lj_filter_count;

        if @lj_filter_count is null or @lj_filter_count = 0 then
			set Message = 'No Data In Json - Filter.';
            rollback;
			leave sp_GRNDetails_Set;
        end if;

        Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.grnheader_dcno'))) into @grnheader_dcno ;
        Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.grnheader_invno'))) into @grnheader_invno ;
        Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.grnheader_received'))) into @grnheader_received ;
        Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.grnheader_remark'))) into @ls_remarks ;
		if @grnheader_received = 0 then
			set Message = ' GRN Header Date Not Given. ';
            leave sp_GRNDetails_Set;
		end if;
        if @grnheader_dcno = '' or @grnheader_dcno is null then
			set @grnheader_dcno = '';
		end if;

		if @grnheader_invno = '' or @grnheader_invno is null then
			set @grnheader_invno = '';
		end if;

		if @ls_remarks = '' or @ls_remarks is null then
			set  @ls_remarks='';
		end if;
				Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.GRNDETAILS'))) into @GRNDETAILS ;
		select JSON_LENGTH(lj_filter,'$.GRNDETAILS') into @li_json_GRNDETAILS_count;


		call sp_Generate_number_get('GRN','000',@Message);
		select @Message into @ls_no from dual;
		if @ls_no = '' then
			set Message = ' GRN Header Code not Given. ';
		else
			set @err = concat('select * from gal_trn_tgrninwardheader where grninwardheader_code =''', @ls_no ,'''' , ' group by grninwardheader_code' );
			#select @err;
			PREPARE stmt1 FROM @err;
			EXECUTE stmt1;
			set countRow = (select found_rows());
			DEALLOCATE PREPARE stmt1;
			if countRow > 0 then
				set Message = ' Duplicate GRN Header Code ';
				leave sp_GRNDetails_Set;
			end if;
		end if;

		set Qry_Header = concat('INSERT INTO gal_trn_tgrninwardheader(grninwardheader_code , grninwardheader_dcnote , grninwardheader_invoiceno ,
							grninwardheader_date , grninwardheader_status , grninwardheader_remarks , entity_gid , create_by) VALUES
                            (''' , @ls_no , ''',''' , @grnheader_dcno , ''',''' , @grnheader_invno , ''',''' , @grnheader_received , ''',''Pending for Approval''
                            ,''' , @ls_remarks , ''',' , @Entity_Gid , ',' , ls_create_by , ')');
		#select Qry_Header;
		set @Qry_Header = Qry_Header;
		PREPARE stmt FROM @Qry_Header;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;

		if countRow >  0 then
		   set Message = 'SUCCESS';
           		select LAST_INSERT_ID() into @li_Header_gid_Max ;
               call sp_Trans_Set('Insert','GRN',@li_Header_gid_Max,'Pending for Approval','G','MAKER','',
                     @Entity_Gid,ls_create_by,@message);
					select @message into @tran;
                        #select @tran;
					if @tran <>0 or @tran <> '' then
                               		#select LAST_INSERT_ID() ;

						set Message = CONCAT(@li_Header_gid_Max,',SUCCESS');

						#commit;
					else
						set Message = 'FAIL in tran';
						rollback;
						leave sp_GRNDetails_Set;
					end if;

		else
		   set Message = 'FAIL';
			rollback;
			leave sp_GRNDetails_Set;
		end if;

       set z = 0;
       select @li_json_GRNDETAILS_count;

		While z <= @li_json_GRNDETAILS_count -1 Do
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.GRNDETAILS[',z,'].poheader_gid[0]'))) into @poheader_gid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.GRNDETAILS[',z,'].podetails_gid[0]'))) into @podetails_gid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.GRNDETAILS[',z,'].current_qty[0]'))) into @current_qty;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.GRNDETAILS[',z,'].podelivery_refgid[0]'))) into @podelivery_refgid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.GRNDETAILS[',z,'].podelivery_reftablegid[0]'))) into @podelivery_reftablegid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.GRNDETAILS[',z,'].podelivery_gid[0]'))) into @podelivery_gid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.GRNDETAILS[',z,'].columnvalue[0]'))) into @columnvalue;
            select @poheader_gid;

             set Query_Insert = '';
					set Query_Insert = concat('INSERT INTO gal_trn_tgrninwarddetails(grninwarddetails_grninwardheader_gid, grninwarddetails_poheader_gid,
						grninwarddetails_podetails_gid,grninwarddetails_podelivary_gid,grninwarddetails_qty, grninwarddetails_date,grninwarddetails_refgid,grninwarddetails_reftablegid, grninwarddetails_godownincharge_gid,
						entity_gid, create_by) VALUES
                        (',@li_Header_gid_Max,',',@poheader_gid,',',@podetails_gid,',',@podelivery_gid,',',@current_qty,',now(),',@podelivery_refgid,',',@podelivery_reftablegid,',
                        ',ls_create_by,',',@Entity_Gid,',',ls_create_by,')');

					set @Insert_Detail_query = Query_Insert;
				 select Query_Insert; ## remove It
					PREPARE stmt FROM @Insert_Detail_query;
					EXECUTE stmt;
					set countRow = (select ROW_COUNT());
					DEALLOCATE PREPARE stmt;


					if countRow >  0 then
                       set Message = 'SUCCESS';
					else
                       set Message = 'FAIL';
						rollback;
						leave sp_GRNDetails_Set;
					end if;
         set z = z+1;
		END WHILE;





End  if;

      if IS_Commit='Y' then
        commit;
	  else
		rollback;
        leave sp_GRNDetails_Set;
	  end if;
END