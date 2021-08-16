CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Approval_To_Draft_PR_Contractor_Set`(in lj_filter json,
in Partner_Gid int,in lj_classification json,out Message varchar(1000))
sp_Atma_Approval_To_Draft_PR_Contractor_Set:BEGIN

declare Query_Insert varchar(10000);
Declare countRow varchar(6000);
declare Query_Update varchar(10000);
declare Query_delete varchar(1000);
declare Query_Value varchar(1000);
declare Query_Column varchar(1000);
Declare contra_partnercontractor_gid,contra_partnercontractor_partnergid,
		contra_partnercontractor_code,contra_partnercontractor_name,
		contra_partnercontractor_service,contra_partnercontractor_remarks,
        contra_partnercontractor_isactive,contra_partnercontractor_isremoved,
		contra_entity_gid,contra_create_by,contra_update_by,
        contra_main_partnercontractor_gid varchar(150);

DECLARE finished INTEGER DEFAULT 0;
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
	leave sp_Atma_Approval_To_Draft_PR_Contractor_Set;
End if;

select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Gid'))) into @Partner_Gid;

if @Partner_Gid = '' or @Partner_Gid is null  or @Partner_Gid=0 then
		set Message = 'Partner Is Not Provided';
		leave sp_Atma_Approval_To_Draft_PR_Contractor_Set;
End if;


BEGIN
	Declare Cursor_atma CURSOR FOR

	select  partnercontractor_gid,partnercontractor_partnergid,partnercontractor_code,
						partnercontractor_name,partnercontractor_service,partnercontractor_remarks,
                        partnercontractor_isactive,partnercontractor_isremoved,
						entity_gid,create_by,update_by
                        from atma_mst_tpartnercontractor
					where partnercontractor_partnergid=@Partner_Gid;

	DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;
	OPEN Cursor_atma;
	atma_looop:loop
		fetch Cursor_atma into contra_partnercontractor_gid,contra_partnercontractor_partnergid,
						  contra_partnercontractor_code,contra_partnercontractor_name,
						  contra_partnercontractor_service,contra_partnercontractor_remarks,
						  contra_partnercontractor_isactive,contra_partnercontractor_isremoved,
						  contra_entity_gid,contra_create_by,contra_update_by;


	    if finished = 1 then
			leave atma_looop;
		End if;
        set Error_Level='ATMA13.1';
		set Query_Update=concat('insert into atma_tmp_mst_tpartnercontractor
						(partnercontractor_partnergid,partnercontractor_code,
                        partnercontractor_name,partnercontractor_service,
                        partnercontractor_remarks,partnercontractor_isactive,
                        partnercontractor_isremoved,entity_gid,create_by,
                        create_date,main_partnercontractor_gid)
				  values(',Partner_Gid,',''',contra_partnercontractor_code,''',
						''',contra_partnercontractor_name,''',
						''',contra_partnercontractor_service,''',
                        ''',contra_partnercontractor_remarks,''',
                        ''',contra_partnercontractor_isactive,''',
                        ''',contra_partnercontractor_isremoved,''',
						',contra_entity_gid,',',contra_create_by,',
                        ''',now(),''',
                        ',contra_partnercontractor_gid,'
                        )'
						 );

		#select Query_Update;
		set @Insert_query = Query_Update;
		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
		set Message = 'SUCCESS';
		else
		set Message = ' FAILED';
		leave sp_Atma_Approval_To_Draft_PR_Contractor_Set;
		end if;
	End loop atma_looop;
	close Cursor_atma;
	end;  #Endof Cursor


END