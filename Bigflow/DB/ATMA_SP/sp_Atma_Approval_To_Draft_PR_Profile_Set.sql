CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Approval_To_Draft_PR_Profile_Set`(in lj_filter json,
in Partner_Gid int,in lj_classification json,out Message varchar(1000))
sp_Atma_Approval_To_Draft_PR_Profile_Set:BEGIN

declare Query_Insert varchar(6000);
declare Query_delete varchar(6000);
declare Query_Update varchar(6000);
declare Query_Column varchar(6000);
declare Query_Value varchar(6000);
Declare countRow varchar(6000);
Declare errno int;
Declare msg,Error_Level varchar(1000);

DECLARE EXIT HANDLER FOR SQLEXCEPTION
BEGIN
	GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
	set Message = concat(Error_Level,' : No-',errno , msg);
	ROLLBACK;
END;


			select JSON_LENGTH(lj_filter,'$') into @lj_filter_json_count;
			select JSON_LENGTH(lj_classification,'$') into @lj_classification_json_count;

				if @lj_filter_json_count = 0 or @lj_filter_json_count is null then
					set Message = 'No Data In filter Json. ';
					leave sp_Atma_Approval_To_Draft_PR_Profile_Set;
				End if;

			select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Gid')))
			into @Partner_Gid;


				if @Partner_Gid = '' or @Partner_Gid is null  or @Partner_Gid=0 then
					set Message = 'Partner Is Not Provided';
				leave sp_Atma_Approval_To_Draft_PR_Profile_Set;
				End if;

	set Error_Level='ATMA15.1';
	set Query_Insert='';
    set Query_Insert=concat('INSERT INTO  atma_tmp_mst_tpartnerprofile (partnerprofile_partnergid,
									partnerprofile_noofyears,
									partnerprofile_associateyears, partnerprofile_awarddetails,
                                    partnerprofile_noofempper,partnerprofile_noofemptmp,
                                    partnerprofile_totemp,partnerprofile_branchcount,
									partnerprofile_factorycount,partnerprofile_remarks,
                                    partnerprofile_isactive,
									partnerprofile_isremoved,entity_gid,create_by,
									create_date, update_by,update_date,main_partnerprofile_gid)
							select ',Partner_Gid,', partnerprofile_noofyears,
									ifnull(partnerprofile_associateyears,0),ifnull(partnerprofile_awarddetails,''''),
									ifnull(partnerprofile_noofempper,0),ifnull(partnerprofile_noofemptmp,0),
									ifnull(partnerprofile_totemp,0),ifnull(partnerprofile_branchcount,0),
									ifnull(partnerprofile_factorycount,0),ifnull(partnerprofile_remarks,''''),
									partnerprofile_isactive,partnerprofile_isremoved,entity_gid,create_by,
									now(),update_by,update_date,partnerprofile_gid
                                    from atma_mst_tpartnerprofile
							where partnerprofile_partnergid=',@Partner_Gid,' ');


	#select Query_Insert;
	set @Insert_query = Query_Insert;
	PREPARE stmt FROM @Insert_query;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
    if countRow >  0 then
		set Message = 'SUCCESS';
	else
		set Message = 'INSERT FAILED profile';
		leave sp_Atma_Approval_To_Draft_PR_Profile_Set;
	end if;


END