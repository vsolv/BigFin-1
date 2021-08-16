CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Pending_To_Approval_profile_Set`(in li_Action  varchar(50),
in lj_filter json,in Partner_Gid int,in lj_classification json,out Message varchar(1000))
sp_Atma_Pending_To_Approval_profile_Set:BEGIN
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
							set Message = concat(Error_Level,':No-',errno,msg);
							ROLLBACK;
						END;

	#set @Main_partner_gid=6;
	IF li_Action='insert' then


	select JSON_LENGTH(lj_filter,'$') into @lj_filter_json_count;
	select JSON_LENGTH(lj_classification,'$') into @lj_classification_json_count;

	if @lj_filter_json_count = 0 or @lj_filter_json_count is null then
		set Message = 'No Data In filter Json. ';
		leave sp_Atma_Pending_To_Approval_profile_Set;
	End if;

	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Gid')))
	into @Partner_Gid;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Update_By')))
    into @Update_By;


    if @Partner_Gid = '' or @Partner_Gid is null  or @Partner_Gid=0 then
			set Message = 'Partner Is Not Provided';
			leave sp_Atma_Pending_To_Approval_profile_Set;
	End if;
    select main_partnerprofile_gid from  atma_tmp_mst_tpartnerprofile
    where partnerprofile_partnergid=@Partner_Gid into @Main_PartnerProfile_Gid;

    if @Main_PartnerProfile_Gid = '' or @Main_PartnerProfile_Gid is null  or @Main_PartnerProfile_Gid=0 then


	set Query_Insert='';
set Error_Level='ATMA56.1';
	set Query_Insert=concat('INSERT INTO  atma_mst_tpartnerprofile (partnerprofile_partnergid, partnerprofile_noofyears,
							partnerprofile_associateyears, partnerprofile_awarddetails, partnerprofile_noofempper,
							partnerprofile_noofemptmp, partnerprofile_totemp, partnerprofile_branchcount,
                            partnerprofile_factorycount,partnerprofile_remarks, partnerprofile_isactive,
                            partnerprofile_isremoved,entity_gid,create_by,
							create_date, update_by, update_date)
								select ',Partner_Gid,', partnerprofile_noofyears,
							ifnull(partnerprofile_associateyears,0),ifnull(partnerprofile_awarddetails,''''),
                            ifnull(partnerprofile_noofempper,0),ifnull(partnerprofile_noofemptmp,0),
                            ifnull(partnerprofile_totemp,0),ifnull(partnerprofile_branchcount,0),
                            ifnull(partnerprofile_factorycount,0),ifnull(partnerprofile_remarks,''''),
                            partnerprofile_isactive,partnerprofile_isremoved,entity_gid,create_by,
							now(),update_by,update_date from atma_tmp_mst_tpartnerprofile
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
		leave sp_Atma_Pending_To_Approval_profile_Set;
	end if;


    else
set Error_Level='ATMA56.2';
		set sql_safe_updates=0;
        set Query_Update = concat(' Update atma_mst_tpartnerprofile as A,
									atma_tmp_mst_tpartnerprofile as B set
                                    A.partnerprofile_noofyears=B.partnerprofile_noofyears,
									A.partnerprofile_associateyears=ifnull(B.partnerprofile_associateyears,0),
                                    A.partnerprofile_awarddetails=ifnull(B.partnerprofile_awarddetails,''''),
    								A.partnerprofile_noofempper=ifnull(B.partnerprofile_noofempper,0),
                                    A.partnerprofile_noofemptmp=ifnull(B.partnerprofile_noofemptmp,0),
									A.partnerprofile_totemp=ifnull(B.partnerprofile_totemp,0),
                                    A.partnerprofile_branchcount=ifnull(B.partnerprofile_branchcount,0),
   								    A.partnerprofile_factorycount=ifnull(B.partnerprofile_factorycount,0),
                                    A.partnerprofile_remarks=ifnull(B.partnerprofile_remarks,''''),
    								A.partnerprofile_isactive=B.partnerprofile_isactive,
                                    A.partnerprofile_isremoved=B.partnerprofile_isremoved,
   								    A.entity_gid=B.entity_gid,
                                    A.create_by=B.create_by,
                                    A.create_date=B.create_date,
                                    A.update_by=',@Update_By,',
									A.update_date=now()
									where A.partnerprofile_gid= B.main_partnerprofile_gid
                                    and A.partnerprofile_gid=',@Main_PartnerProfile_Gid,'');



	#select Query_Update;
	set @Insert_query = Query_Update;
	PREPARE stmt FROM @Insert_query;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
    if countRow >  0 then
		set Message = 'SUCCESS';
	else
		set Message = 'UPDATE FAILED Profile';
		leave sp_Atma_Pending_To_Approval_profile_Set;
	end if;
End if;


			SET SQL_SAFE_UPDATES = 0;
				set Query_delete=concat('DELETE FROM atma_tmp_mst_tpartnerprofile
											WHERE partnerprofile_partnergid=',@Partner_Gid,'');
    set @Insert_query = Query_delete;
	PREPARE stmt FROM @Insert_query;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
    if countRow >  0 then
		set Message = 'SUCCESS';
	else
		set Message = ' FAILED_profile deletion';
		leave sp_Atma_Pending_To_Approval_profile_Set;
	end if;


END IF;



END