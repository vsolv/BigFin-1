CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Partnerprofile_Set`(in ls_Action varchar(16),
in lj_filter json,in lj_classification json,
out Message varchar(1000))
sp_Atma_Partnerprofile_Set:BEGIN
declare Query_Insert varchar(1000);
Declare countRow varchar(6000);
Declare Query_Update varchar(1000);
Declare Query_Value varchar(1000);
Declare Query_Column varchar(1000);
Declare errno int;
Declare msg varchar(1000);

						DECLARE EXIT HANDLER FOR SQLEXCEPTION
						BEGIN
							GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
							set Message = concat(errno , msg);
							ROLLBACK;
						END;

start transaction;

		select JSON_LENGTH(lj_filter,'$') into @li_filter_jsoncount;
		select JSON_LENGTH(lj_classification,'$') into @li_classification_jsoncount;

        if @li_filter_jsoncount = 0 or @li_filter_jsoncount is null  then
			set Message = 'No Data In Json. ';
			leave sp_Atma_Partnerprofile_Set;
		End if;

		if @li_classification_jsoncount = 0 or @li_classification_jsoncount = ''
            or @li_classification_jsoncount is null  then
			set Message = 'No Entity_Gid and Create by In Json. ';
			leave sp_Atma_Partnerprofile_Set;
		End if;

	   select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnerprofile_Partnergid')))into @Partnerprofile_Partnergid;
       select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Create_By')))into @Create_By;

       if @Partnerprofile_Partnergid = 0 or @Partnerprofile_Partnergid = '' or @Partnerprofile_Partnergid is null  then
				set Message ='Partnerprofile Partnergid Is Not Given';
				rollback;
				leave sp_Atma_Partnerprofile_Set;
				end if;
		set @partnerprofile='';
		select partnerprofile_gid from atma_tmp_mst_tpartnerprofile where
		partnerprofile_partnergid=@Partnerprofile_Partnergid into @partnerprofile;


	   if @partnerprofile  is null or @partnerprofile= ''  then
			set ls_Action = 'INSERT';
	   elseif @partnerprofile  is not null then
			set ls_Action='UPDATE' ;
	    end if;


	   if ls_Action = 'INSERT'  then


				 select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Entity_Gid')))into @Entity_Gid;

				 select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnerprofile_Noofyears')))into @Partnerprofile_Noofyears;
				 select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnerprofile_Associateyears')))into @Partnerprofile_Associateyears;
				 select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnerprofile_Awarddetails')))into @Partnerprofile_Awarddetails;
				 select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnerprofile_Noofempper')))into @Partnerprofile_Noofempper;
				 select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnerprofile_Noofemptmp')))into @Partnerprofile_Noofemptmp;
				 select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnerprofile_Totemp')))into @Partnerprofile_Totemp;
				 select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnerprofile_Branchcount')))into @Partnerprofile_Branchcount;
				 select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnerprofile_Factorycount')))into @Partnerprofile_Factorycount;
				 select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnerprofile_Remarks')))into @Partnerprofile_Remarks;



                if @Entity_Gid = 0 or @Entity_Gid = '' or @Entity_Gid is null  then
				set Message ='Entity Gid Is Not Given';
				rollback;
				leave sp_Atma_Partnerprofile_Set;
				end if;

                if @Create_By = 0 or @Create_By = '' or @Create_By is null  then
				set Message ='Create By Is Not Given';
				rollback;
				leave sp_Atma_Partnerprofile_Set;
				end if;

                if @Partnerprofile_Noofyears = 0 or @Partnerprofile_Noofyears = '' or @Partnerprofile_Noofyears is null  then
				set Message ='Partner Profile No Of YearsIs Not Given';
				rollback;
				leave sp_Atma_Partnerprofile_Set;
				end if;

                set Query_Column='';
				set Query_Value ='';

				if @Partnerprofile_Associateyears is not null then
				set Query_Column = concat(Query_Column,',partnerprofile_associateyears ');
				set Query_Value=concat(Query_Value,', ''',@Partnerprofile_Associateyears,''' ');
				else
				set Query_Column = concat(Query_Column,'');
				set Query_Value=concat(Query_Value);
				end if;

				if @Partnerprofile_Awarddetails is not null then
				set Query_Column = concat(Query_Column,',partnerprofile_awarddetails ');
				set Query_Value=concat(Query_Value,', ''',@Partnerprofile_Awarddetails,''' ');
				else
				set Query_Column = concat(Query_Column,'');
				set Query_Value=concat(Query_Value);
				end if;

                if @Partnerprofile_Noofempper is not null then
				set Query_Column = concat(Query_Column,',partnerprofile_noofempper ');
				set Query_Value=concat(Query_Value,', ''',@Partnerprofile_Noofempper,''' ');
				else
				set Query_Column = concat(Query_Column,'');
				set Query_Value=concat(Query_Value);
				end if;

                if @Partnerprofile_Noofemptmp is not null then
				set Query_Column = concat(Query_Column,',partnerprofile_noofemptmp ');
				set Query_Value=concat(Query_Value,', ''',@Partnerprofile_Noofemptmp,''' ');
				else
				set Query_Column = concat(Query_Column,'');
				set Query_Value=concat(Query_Value);
				end if;

                if @Partnerprofile_Totemp is not null then
				set Query_Column = concat(Query_Column,',partnerprofile_totemp ');
				set Query_Value=concat(Query_Value,', ''',@Partnerprofile_Totemp,''' ');
				else
				set Query_Column = concat(Query_Column,'');
				set Query_Value=concat(Query_Value);
				end if;

                if @Partnerprofile_Branchcount is not null then
				set Query_Column = concat(Query_Column,',partnerprofile_branchcount ');
				set Query_Value=concat(Query_Value,', ''',@Partnerprofile_Branchcount,''' ');
				else
				set Query_Column = concat(Query_Column,'');
				set Query_Value=concat(Query_Value);
				end if;

                if @Partnerprofile_Factorycount is not null then
				set Query_Column = concat(Query_Column,',partnerprofile_factorycount ');
				set Query_Value=concat(Query_Value,', ''',@Partnerprofile_Factorycount,''' ');
				else
				set Query_Column = concat(Query_Column,'');
				set Query_Value=concat(Query_Value);
				end if;

                if @Partnerprofile_Remarks is not null then
				set Query_Column = concat(Query_Column,',partnerprofile_remarks ');
				set Query_Value=concat(Query_Value,', ''',@Partnerprofile_Remarks,''' ');
				else
				set Query_Column = concat(Query_Column,'');
				set Query_Value=concat(Query_Value);
				end if;


		set Query_Insert='';

		set Query_Insert=concat('insert into atma_tmp_mst_tpartnerprofile
								(Partnerprofile_Partnergid,Partnerprofile_Noofyears,
								entity_gid,create_by',Query_Column,')
								values(',@Partnerprofile_Partnergid,',',@Partnerprofile_Noofyears,',
                                ',@Entity_Gid,',',@Create_By,'',Query_Value,')'
							);
		#select Query_Insert;
		set @Insert_query = Query_Insert;

		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'SUCCESSFULLY INSERTED';
			commit;
		else
			set Message = 'INSERT FAILED';
			rollback;
		end if;
		end if;


	   if ls_Action='UPDATE' then

		#select JSON_LENGTH(lj_filter,'$') into @li_filter_jsoncount;
		#select JSON_LENGTH(lj_classification,'$') into @li_classification_jsoncount;

		#if @li_filter_jsoncount = 0 or @li_filter_jsoncount is null  then
			#set Message = 'No Data In Json. ';
			#leave sp_Atma_Partnerprofile_Set;
		#End if;

         #if @li_classification_jsoncount = 0 or @li_classification_jsoncount = ''
           # or @li_classification_jsoncount is null  then
			#set Message = 'No Update By In Json. ';
			#leave sp_Atma_Partnerprofile_Set;
		#End if;


				# select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnerprofile_Gid')))into @Partnerprofile_Gid;
				 #select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnerprofile_Partnergid')))into @Partnerprofile_Partnergid;
				 select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnerprofile_Noofyears')))into @Partnerprofile_Noofyears;
				 select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnerprofile_Associateyears')))into @Partnerprofile_Associateyears;
				 select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnerprofile_Awarddetails')))into @Partnerprofile_Awarddetails;
				 select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnerprofile_Noofempper')))into @Partnerprofile_Noofempper;
				 select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnerprofile_Noofemptmp')))into @Partnerprofile_Noofemptmp;
				 select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnerprofile_Totemp')))into @Partnerprofile_Totemp;
				 select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnerprofile_Branchcount')))into @Partnerprofile_Branchcount;
				 select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnerprofile_Factorycount')))into @Partnerprofile_Factorycount;
				 select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partnerprofile_Remarks')))into @Partnerprofile_Remarks;

				 #select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Update_By')))
				 #into @Update_By;



			#if @Partnerprofile_Gid is not null or @Partnerprofile_Gid <> ''or @Partnerprofile_Gid <> 0 then
					#set @Partnerprofile_Gid=@Partnerprofile_Gid;
				#end if;

			set Query_Update = '';

			#if @Partnerprofile_Partnergid is not null or @Partnerprofile_Partnergid <> ''or @Partnerprofile_Partnergid <> 0 then
				#set Query_Update = concat(Query_Update, ',Partnerprofile_Partnergid = ',@Partnerprofile_Partnergid,' ');
			#end if;

            if @Partnerprofile_Noofyears is not null or @Partnerprofile_Noofyears <> '' then
				set Query_Update = concat(Query_Update, ',Partnerprofile_Noofyears = ',@Partnerprofile_Noofyears,' ');
			elseif @Partnerprofile_Noofyears is null or @Partnerprofile_Noofyears = '' then
				set Message='Partner Profile No Of Years can not be null' ;
				leave sp_Atma_Partnerprofile_Set;
            end if;

            if @Partnerprofile_Associateyears is not null or @Partnerprofile_Associateyears <> '' then
				set Query_Update = concat(Query_Update, ',Partnerprofile_Associateyears = ',@Partnerprofile_Associateyears,' ');
			#else
				#set Query_Update = concat(Query_Update,'');
            elseif @Partnerprofile_Associateyears is null or @Partnerprofile_Associateyears = '' then
				 set Query_Update = concat(Query_Update,',Partnerprofile_Associateyears = 0 ');
            end if;

            if @Partnerprofile_Awarddetails is not null or @Partnerprofile_Awarddetails <> '' then
				set Query_Update = concat(Query_Update, ',Partnerprofile_Awarddetails = ''',@Partnerprofile_Awarddetails,''' ');
			elseif @Partnerprofile_Awarddetails is null or @Partnerprofile_Awarddetails = '' then
				set Query_Update = concat(Query_Update,',Partnerprofile_Awarddetails = '''' ');
            end if;

            if @Partnerprofile_Noofempper is not null or @Partnerprofile_Noofempper <> ''  then
				set Query_Update = concat(Query_Update, ',Partnerprofile_Noofempper = ',@Partnerprofile_Noofempper,' ');

			elseif @Partnerprofile_Noofempper is null or @Partnerprofile_Noofempper = '' then
				set Query_Update = concat(Query_Update,',Partnerprofile_Noofempper = 0 ');
            end if;

            if @Partnerprofile_Noofemptmp is not null or @Partnerprofile_Noofemptmp <> ''  then
				set Query_Update = concat(Query_Update, ',Partnerprofile_Noofemptmp = ',@Partnerprofile_Noofemptmp,' ');
            elseif @Partnerprofile_Noofemptmp is null or @Partnerprofile_Noofemptmp = '' then
				set Query_Update = concat(Query_Update,',Partnerprofile_Noofemptmp = 0 ');
			end if;

            if @Partnerprofile_Totemp is not null or @Partnerprofile_Totemp <> '' then
				set Query_Update = concat(Query_Update, ',Partnerprofile_Totemp = ',@Partnerprofile_Totemp,' ');
			elseif @Partnerprofile_Totemp is null or @Partnerprofile_Totemp = '' then
				set Query_Update = concat(Query_Update,',Partnerprofile_Totemp = 0 ');
			end if;

            if @Partnerprofile_Branchcount is not null or @Partnerprofile_Branchcount <> ''  then
				set Query_Update = concat(Query_Update, ',Partnerprofile_Branchcount = ',@Partnerprofile_Branchcount,' ');
            elseif @Partnerprofile_Branchcount is null or @Partnerprofile_Branchcount = '' then
				set Query_Update = concat(Query_Update,',Partnerprofile_Branchcount = 0 ');
			end if;

            if @Partnerprofile_Factorycount is not null or @Partnerprofile_Factorycount <> ''  then
				set Query_Update = concat(Query_Update, ',Partnerprofile_Factorycount = ',@Partnerprofile_Factorycount,' ');
            elseif @Partnerprofile_Factorycount is null or @Partnerprofile_Factorycount = '' then
				set Query_Update = concat(Query_Update,',Partnerprofile_Factorycount = 0 ');
			end if;

            if @Partnerprofile_Remarks is not null or @Partnerprofile_Remarks <> ''  then
				set Query_Update = concat(Query_Update, ',Partnerprofile_Remarks = ''',@Partnerprofile_Remarks,''' ');
            elseif @Partnerprofile_Remarks is null or @Partnerprofile_Remarks = '' then
				set Query_Update = concat(Query_Update,',Partnerprofile_Remarks = '''' ');
			end if;


			set Query_Update = concat('Update atma_tmp_mst_tpartnerprofile
                         set update_date = CURRENT_TIMESTAMP,update_by=',@Create_By,'
                         ',Query_Update,'
						 Where Partnerprofile_Gid = ',@partnerprofile,'
						 and partnerprofile_isactive = ''Y'' and partnerprofile_isremoved = ''N''
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
				leave sp_Atma_Partnerprofile_Set;
		elseif    countRow > 0 then
				set Message = 'SUCCESSFULLY UPDATED';
                commit;
		end if;

        end if;


END