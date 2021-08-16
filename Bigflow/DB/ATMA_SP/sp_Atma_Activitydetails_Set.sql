CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Activitydetails_Set`(in ls_Action varchar(16),
in Activity json,in lj_classification json,
out Message varchar(1000))
sp_Atma_Activitydetails_Set:BEGIN
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
		select JSON_LENGTH(Activity,'$') into @li_jsonActivity;
		select JSON_LENGTH(lj_classification,'$') into @li_classification_jsoncount;

		if @li_jsonActivity = 0 or @li_jsonActivity is null  then
			set Message = 'No Data In Json. ';
			leave sp_Atma_Activitydetails_Set;
		End if;

         if @li_classification_jsoncount = 0 or @li_classification_jsoncount = ''
            or @li_classification_jsoncount is null  then
			set Message = 'No Entity_Gid and Create by In Json. ';
			leave sp_Atma_Activitydetails_Set;
		End if;

        if @li_classification_jsoncount is not null or @li_classification_jsoncount	<> ''
		   or @li_classification_jsoncount	<> 0 then

		select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Entity_Gid')))into @Entity_Gid;
          select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Create_By')))into @Create_By;
		End if;
			#if @li_jsonActivity is not null or @li_jsonActivity <> '' then
				 select JSON_UNQUOTE(JSON_EXTRACT(Activity,CONCAT('$.Activitydetails_Activitygid')))into @Activitydetails_Activitygid;
				# select JSON_UNQUOTE(JSON_EXTRACT(Activity,CONCAT('$.Activitydetails_Code')))into @Activitydetails_Code;
				 select JSON_UNQUOTE(JSON_EXTRACT(Activity,CONCAT('$.Activitydetails_Name')))into @Activitydetails_Name;
				 select JSON_UNQUOTE(JSON_EXTRACT(Activity,CONCAT('$.Activitydetails_Remarks')))into @Activitydetails_Remarks;
				 select JSON_UNQUOTE(JSON_EXTRACT(Activity,CONCAT('$.Activitydetails_Raisor')))into @Activitydetails_Raisor;
				 select JSON_UNQUOTE(JSON_EXTRACT(Activity,CONCAT('$.Activitydetails_Approver')))into @Activitydetails_Approver;

			#end if;

                if @Entity_Gid = 0 or @Entity_Gid = '' or @Entity_Gid is null  then
				set Message ='Entity Gid Is Not Given';
				rollback;
				leave sp_Atma_Activitydetails_Set;
				end if;

                if @Create_By = 0 or @Create_By = '' or @Create_By is null  then
				set Message ='Create By Is Not Given';
				rollback;
				leave sp_Atma_Activitydetails_Set;
				end if;

				if @Activitydetails_Activitygid = 0 or @Activitydetails_Activitygid = '' or @Activitydetails_Activitygid is null  then
				set Message ='Activity Details Activitygid Is Not Given';
				rollback;
				leave sp_Atma_Activitydetails_Set;
				end if;

               #if @Activitydetails_Code = 0 or @Activitydetails_Code = '' or @Activitydetails_Code is null  then
				#set Message ='Activity Details Code Is Not Given';
				#rollback;
				#leave sp_Atma_Activitydetails_Set;
				#end if;

                if @Activitydetails_Name = '' or @Activitydetails_Name is null  then
				set Message ='Activity Details Name Is Not Given';
				rollback;
				leave sp_Atma_Activitydetails_Set;
				end if;

                if @Activitydetails_Raisor = '' or @Activitydetails_Raisor = 0 OR @Activitydetails_Raisor is null  then
				set Message ='Activity Details Raisor Is Not Given';
				rollback;
				leave sp_Atma_Activitydetails_Set;
				end if;

                if @Activitydetails_Approver = '' or @Activitydetails_Approver = 0 OR @Activitydetails_Approver is null  then
				set Message ='Activity Details Approver Is Not Given';
				rollback;
				leave sp_Atma_Activitydetails_Set;
				end if;

			select codesequence_no from gal_mst_tcodesequence where
			codesequence_type='activitydetails_code' into @AT_activitydetailscode;

			set @activitydetailscode = concat('00',SUBSTRING(CONCAT('000',@AT_activitydetailscode),-4));

            set Query_Insert='';
   set Error_Level='ATMA2.1';
	set Query_Insert=concat('insert into atma_tmp_mst_tactivitydetails(activitydetails_activitygid,activitydetails_code,activitydetails_name,
							activitydetails_remarks,activitydetails_raisor,activitydetails_approver,
							entity_gid,create_by)
					values(',@Activitydetails_Activitygid,',',@activitydetailscode,',
                    ''',@Activitydetails_Name,''',''',ifnull(@Activitydetails_Remarks,''),''',',@Activitydetails_Raisor,',
					',@Activitydetails_Approver,',
					',@Entity_Gid,',',@Create_By,')'
                    );
                 # SELECT  Query_Insert;
	set @Insert_query = Query_Insert;

	PREPARE stmt FROM @Insert_query;
	EXECUTE stmt;
	set countRow = (select ROW_COUNT());
	DEALLOCATE PREPARE stmt;
    if countRow >  0 then
		set Message = 'SUCCESSFULLY INSERTED';
        Update gal_mst_tcodesequence
				set  codesequence_no= codesequence_no+1
				Where codesequence_type = 'activitydetails_code';
        commit;
	else
		set Message = 'INSERT FAILED';
		rollback;
	end if;
	end if;

if ls_Action='UPDATE' then

	  START TRANSACTION;


	select JSON_LENGTH(Activity,'$') into @li_jsoncount;
	select JSON_LENGTH(lj_classification,'$') into @li_classification_json_count;


			if @li_jsoncount = 0 or @li_jsoncount is null
               or @li_jsoncount = ''  then
					set Message = 'No Data In Json - Update.';
					leave sp_Atma_Activitydetails_Set;
			End if;

            if @li_classification_json_count = 0  or @li_classification_json_count = ''
               or @li_classification_json_count is null  then
					set Message = 'No Data In classification Json - Update.';
					leave sp_Atma_Activitydetails_Set;
			End if;


        if @li_jsoncount is not null or @li_jsoncount <> '' or @li_jsoncount <> 0 then

		select JSON_UNQUOTE(JSON_EXTRACT(Activity,CONCAT('$.Activitydetails_Gid')))into @Activitydetails_Gid;
       # select @Activitydetails_Gid;
        select JSON_UNQUOTE(JSON_EXTRACT(Activity,CONCAT('$.Activitydetails_Activitygid')))into @Activitydetails_Activitygid;
        select JSON_UNQUOTE(JSON_EXTRACT(Activity,CONCAT('$.Activitydetails_Code')))into @Activitydetails_Code;
         select JSON_UNQUOTE(JSON_EXTRACT(Activity,CONCAT('$.Activitydetails_Name')))into @Activitydetails_Name;
		select JSON_UNQUOTE(JSON_EXTRACT(Activity,CONCAT('$.Activitydetails_Remarks')))into @Activitydetails_Remarks;
        select JSON_UNQUOTE(JSON_EXTRACT(Activity,CONCAT('$.Activitydetails_Raisor')))into @Activitydetails_Raisor;
        select JSON_UNQUOTE(JSON_EXTRACT(Activity,CONCAT('$.Activitydetails_Approver')))into @Activitydetails_Approver;
		#select 1;
        end if;

            if @li_classification_json_count <> 0 OR @li_classification_json_count <> ''
               or @li_classification_json_count is NOT null  then

            select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Update_By')))
            into @Update_By;

			End if;

			if @activitydetails_gid is not null or @activitydetails_gid <> ''or @activitydetails_gid <> 0 then
					set @activitydetails_gid=@activitydetails_gid;
				end if;

			set Query_Update = '';

			if @Activitydetails_Activitygid is not null or @Activitydetails_Activitygid <> ''or @activitydetails_gid <> 0 then
				set Query_Update = concat(Query_Update, ',Activitydetails_Activitygid = ',@Activitydetails_Activitygid,' ');
			end if;

            if @Activitydetails_Code is not null or @Activitydetails_Code <> '' then
				set Query_Update = concat(Query_Update, ',Activitydetails_Code = ',@Activitydetails_Code,' ');
			end if;

            if @Activitydetails_Name is not null or @Activitydetails_Name <> '' then
				set Query_Update = concat(Query_Update, ',Activitydetails_Name = ''',@Activitydetails_Name,''' ');
			end if;

            if @Activitydetails_Remarks is not null or @Activitydetails_Remarks <> '' then
				set Query_Update = concat(Query_Update, ',Activitydetails_Remarks = ''',@Activitydetails_Remarks,''' ');
			end if;

            if @Activitydetails_Raisor is not null or @Activitydetails_Raisor <> '' or @Activitydetails_Raisor <> 0 then
				set Query_Update = concat(Query_Update, ',Activitydetails_Raisor = ',@Activitydetails_Raisor,' ');
			end if;

            if @Activitydetails_Approver is not null or @Activitydetails_Approver <> '' or @Activitydetails_Approver <> 0 then
				set Query_Update = concat(Query_Update, ',Activitydetails_Approver = ''',@Activitydetails_Approver,''' ');

			end if;

           set Error_Level='ATMA2.2';
			set Query_Update = concat('Update atma_tmp_mst_tactivitydetails
                         set update_date = CURRENT_TIMESTAMP,update_by=',@Update_By,'
                         ',Query_Update,'
						 Where Activitydetails_Gid = ',@Activitydetails_Gid,'
						 and activitydetails_isactive = ''Y'' and activitydetails_isremoved = ''N''
                         ');


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
				leave sp_Atma_Activitydetails_Set;
		elseif    countRow > 0 then
				set Message = 'SUCCESSFULLY UPDATED';
                commit;
		end if;

        end if;


END