CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Memo_Process_Get`(IN `ls_Type` varchar(64),IN `ls_Sub_Type` varchar(64),
IN `lj_Filters` json,IN `lj_Classification` json, OUT `Message` varchar(1024))
sp_Memo_Process_Get:BEGIN
### Bala Feb 25 2020 - Created
Declare Query_Select varchar(4024);
Declare Query_Search varchar(1024);
Declare Query_Column varchar(1024);
Declare Query_Status varchar(1024);
Declare Query_Limit varchar(1024);
declare errno int;
declare msg varchar(1000);
declare li_count int;

# Null Selected Output
DECLARE done INT DEFAULT 0;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
#....

	DECLARE EXIT HANDLER FOR SQLEXCEPTION,sqlwarning

    BEGIN
		GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
		set Message = concat(errno , msg);
		ROLLBACK;
    END;
			  SET SESSION group_concat_max_len=4294967295;

		select  JSON_UNQUOTE(JSON_EXTRACT(lj_Classification,'$.Entity_Gid[0]')) into @Entity_Gids;

        if @Entity_Gids is  null or @Entity_Gids = '' then
				set Message = 'Entity_Gid Is Not Given';
                leave sp_Memo_Process_Get;
        End if;

IF ls_Type = 'MEMO' and ls_Sub_Type = 'REQUEST_SUMMARY' then

				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Request_Code'))) into @Request_Code;
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Request_Name'))) into @Request_Name;
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Request_ION'))) into @Request_ION;
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Request_Status'))) into @Request_Status;
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Page_Index'))) into @Page_Index;
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Page_Size'))) into @Page_Size;


						if @Page_Index is  null or @Page_Index = '' then
							set Message = 'Page Index Is Not Given';
							leave sp_Memo_Process_Get;
						End if;

                        if @Page_Size is  null or @Page_Size = '' then
							set Message = 'Page Size Is Not Given';
							leave sp_Memo_Process_Get;
						End if;


					set Query_Search = '';

					if @Request_Code <> '' and @Request_Code is not null  then
                         set Query_Search = concat(Query_Search,'and A.request_code like ''','%',@Request_Code,'%','''  ');
                    End if;

                    if @Request_Name <> '' and @Request_Name is not null  then
                         set Query_Search = concat(Query_Search,'and A.request_name like ''','%',@Request_Name,'%','''  ');
                    End if;

                    if @Request_ION <> '' and @Request_ION is not null  then
                         set Query_Search = concat(Query_Search,'and A.request_ion like ''','%',@Request_ION,'%','''  ');
                    End if;

                     if @Request_Status <> '' and @Request_Status is not null  then
                         set Query_Search = concat(Query_Search,'and A.request_status like ''','%',@Request_Status,'%','''  ');
                    End if;



                    set Query_Limit='';
                    if @Page_Index <> '' and @Page_Index is not null and @Page_Size <> '' and @Page_Size is not null  then
                         set @total_size= @Page_Index*@Page_Size;
						 set Query_Limit = concat(Query_Limit,' LIMIT ',@Page_Size,' OFFSET ',@total_size,'  ');
					end if;

                    set Query_Column='';

					if @Page_Index=0 and @Page_Size=10 then
						set Query_Column = (',@Total_Row as Total_Row');
					end if;




           SELECT ifnull(group_concat(A.requesttran_gid),0) into @Requesttran_Gid
											from (SELECT requesttran_gid
                                              #,G.requesttran_comments
												 FROM mem_trn_trequest A
													inner join mem_trn_trequesttran B on B.requesttran_requestgid=A.request_gid
														where A.request_isactive='Y' and A.request_isremoved='N'
														  and A.entity_gid in(1)
                                                          and B.requesttran_isremoved='N'
														  and B.entity_gid in(1)
                                                          group by requesttran_requestgid) A;


			set Query_Select = '';
			set Query_Select = concat('SELECT A.request_gid, A.request_code, A.request_name,
											  A.request_approvergid,A.request_closed,
											  A.request_status,A.request_ion,A.create_by,
                                              A.request_isactive,A.request_isremoved,
                                              B.memosubcategory_name,C.memocategory_name,
                                              E.employee_name  create_by_name,F.file_name,
											  concat(''/media/'',substring_index(F.file_path,''/media/'',-1)) as file_path,
                                              G.requesttran_comments ,H.Type_CC,CC_Emp_Name,I.Type_TO,I.TO_Emp_Name ',Query_Column,'
												 FROM mem_trn_trequest A
													inner join mem_mst_tmemosubcategory B on B.memosubcategory_gid=A.request_memosubcategorygid
                                                    inner join mem_mst_tmemocategory C on C.memocategory_gid=B.memosubcategory_memocategorygid
                                                    inner join gal_mst_temployee E on E.employee_gid=A.create_by
                                                    left join gal_mst_tfile F on F.file_gid=A.request_filegid
															   and F.file_isactive=''Y'' and F.file_isremoved=''N''
                                                               and F.entity_gid in(',@Entity_Gids,')
													inner join mem_trn_trequesttran G on G.requesttran_requestgid=A.request_gid
                                                    inner join
														(select requesttran_totype Type_CC,
																group_concat(B.employee_name) CC_Emp_Name,
																requesttran_requestgid,requesttran_isremoved,
																employee_isactive,employee_isremoved from mem_trn_trequesttran  A
															inner join gal_mst_temployee B on B.employee_gid=A.requesttran_to
																where requesttran_totype=''CC''
																	and requesttran_isremoved=''N''
																	and employee_isactive=''Y'' and employee_isremoved=''N''
																		group by requesttran_requestgid) H on H.requesttran_requestgid=G.requesttran_requestgid
													inner join
														(select requesttran_totype Type_TO,
																group_concat(B.employee_name) TO_Emp_Name,
																requesttran_requestgid,requesttran_isremoved,
																employee_isactive,employee_isremoved from mem_trn_trequesttran  A
															inner join gal_mst_temployee B on B.employee_gid=A.requesttran_to
																where requesttran_totype=''TO''
																	and requesttran_isremoved=''N''
																	and employee_isactive=''Y'' and employee_isremoved=''N''
																		group by requesttran_requestgid) I on I.requesttran_requestgid=G.requesttran_requestgid
													 where A.request_isactive=''Y'' and A.request_isremoved=''N''
														  and A.entity_gid in(',@Entity_Gids,')
														  and B.memosubcategory_isactive=''Y'' and B.memosubcategory_isremoved=''N''
														  and B.entity_gid in(',@Entity_Gids,')
                                                          and C.memocategory_isactive=''Y'' and C.memocategory_isremoved=''N''
														  and C.entity_gid in(',@Entity_Gids,')
                                                          and E.employee_isactive=''Y'' and E.employee_isremoved=''N''
														  and E.entity_gid in(',@Entity_Gids,')
                                                          and G.requesttran_isremoved=''N''
														  and G.entity_gid in(',@Entity_Gids,')
                                                          and requesttran_gid in (',@Requesttran_Gid,')
                                                          ',Query_Search,'

												 ');

								if @Page_Index=0 and @Page_Size=10 then
									set @Query_Count = '';
									set @Query_Count = concat('select count(A.request_gid)
																into @Total_Row from (',Query_Select,') A ');
										#select @Query_Count;
										PREPARE stmt FROM @Query_Count;
										EXECUTE stmt;
										DEALLOCATE PREPARE stmt;
								end if;

								set @Query_Select = concat(Query_Select,Query_Limit);
			      		        #select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

								if li_count > 0 then
									set Message = 'FOUND';
								else
									set Message = 'NOT_FOUND';
									leave sp_Memo_Process_Get;
								end if;



ELSEIF ls_Type = 'MEMO' and ls_Sub_Type = 'APPROVAL_SUMMARY' then


			select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Login_By'))) into @Login_By;
            select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Request_Code'))) into @Request_Code;
			select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Request_Name'))) into @Request_Name;
			select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Request_ION'))) into @Request_ION;
			select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Category_Name'))) into @Category_Name;
            select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Page_Index'))) into @Page_Index;
			select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Page_Size'))) into @Page_Size;


						if @Page_Index is  null or @Page_Index = '' then
							set Message = 'Page Index Is Not Given';
							leave sp_Memo_Process_Get;
						End if;

                        if @Page_Size is  null or @Page_Size = '' then
							set Message = 'Page Size Is Not Given';
							leave sp_Memo_Process_Get;
						End if;


                        if @Login_By is  null or @Login_By = '' then
							set Message = 'Login By Is Not Given';
							leave sp_Memo_Process_Get;
						End if;


               set Query_Search = '';

					if @Request_Code <> '' and @Request_Code is not null  then
                         set Query_Search = concat(Query_Search,'and A.request_code like ''','%',@Request_Code,'%','''  ');
                    End if;

                    if @Request_Name <> '' and @Request_Name is not null  then
                         set Query_Search = concat(Query_Search,'and A.request_name like ''','%',@Request_Name,'%','''  ');
                    End if;

                    if @Request_ION <> '' and @Request_ION is not null  then
                         set Query_Search = concat(Query_Search,'and A.request_ion like ''','%',@Request_ION,'%','''  ');
                    End if;

                    if @Category_Name <> '' and @Category_Name is not null  then
                         set Query_Search = concat(Query_Search,'and C.memocategory_name like ''','%',@Category_Name,'%','''  ');
                    End if;


                    set Query_Limit='';
                    if @Page_Index <> '' and @Page_Index is not null and @Page_Size <> '' and @Page_Size is not null  then
                         set @total_size= @Page_Index*@Page_Size;
						 set Query_Limit = concat(Query_Limit,' LIMIT ',@Page_Size,' OFFSET ',@total_size,'  ');
					end if;

                    set Query_Column='';

					if @Page_Index=0 and @Page_Size=10 then
						set Query_Column = (',@Total_Row as Total_Row');
					end if;

                #request_code,request_name,request_ion,request_status,


                /*select distinct(requesttran_from),group_concat(requesttran_requestgid)
					into @Tran_From, @Request_Gid from mem_trn_trequesttran
                    where requesttran_status in ('PENDING-APPROVAL' ,'REJECTED') and requesttran_to=@Login_By;*/
                    #select @Login_By,@Request_Gid,@Tran_From;

				#select @Comments;

			set Query_Select = '';
			set Query_Select = concat('SELECT A.request_gid, A.request_code, A.request_name,
											  A.request_approvergid,A.request_closed,
											  A.request_status,A.request_ion,A.create_by,
                                              B.memosubcategory_name,C.memocategory_name,D.employee_name,
                                              E.employee_name  create_by_name,F.file_name,
											  concat(''/media/'',substring_index(F.file_path,''/media/'',-1)) as file_path,
                                              G.requesttran_status,G.requesttran_from,
                                              G.requesttran_comments ,G.create_date ',Query_Column,'
												 FROM mem_trn_trequest A
													inner join mem_mst_tmemosubcategory B on B.memosubcategory_gid=A.request_memosubcategorygid
                                                    inner join mem_mst_tmemocategory C on C.memocategory_gid=B.memosubcategory_memocategorygid
                                                    inner join gal_mst_temployee E on E.employee_gid=A.create_by
													inner join mem_trn_trequesttran G on G.requesttran_requestgid=A.request_gid
													inner join gal_mst_temployee D on D.employee_gid=G.requesttran_to
                                                    left join gal_mst_tfile F on F.file_gid=G.requesttran_filegid
															  and F.file_isactive=''Y'' and F.file_isremoved=''N''
															  and F.entity_gid in(',@Entity_Gids,')
														where G.requesttran_to=',@Login_By,' and requesttran_by=0
														   and A.request_isactive=''Y'' and A.request_isremoved=''N''
														   and A.entity_gid in(',@Entity_Gids,')
														   and B.memosubcategory_isactive=''Y'' and B.memosubcategory_isremoved=''N''
														   and B.entity_gid in(',@Entity_Gids,')
                                                           and C.memocategory_isactive=''Y'' and C.memocategory_isremoved=''N''
														   and C.entity_gid in(',@Entity_Gids,')
                                                           and D.employee_isactive=''Y'' and D.employee_isremoved=''N''
														   and D.entity_gid in(',@Entity_Gids,')
                                                           and E.employee_isactive=''Y'' and E.employee_isremoved=''N''
														   and E.entity_gid in(',@Entity_Gids,')
                                                           and G.requesttran_isremoved=''N''
														   and G.entity_gid in(',@Entity_Gids,')
                                                           and A.request_status =''PENDING-APPROVAL''
                                                           ',Query_Search,'
												 ');


                                if @Page_Index=0 and @Page_Size=10 then
									set @Query_Count = '';
									set @Query_Count = concat('select count(A.request_gid)
																into @Total_Row from (',Query_Select,') A ');
										#select @Query_Count;
										PREPARE stmt FROM @Query_Count;
										EXECUTE stmt;
										DEALLOCATE PREPARE stmt;
								end if;


								set @Query_Select = concat(Query_Select,Query_Limit);
			      		        #select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

								if li_count > 0 then
									set Message = 'FOUND';
								else
									set Message = 'NOT_FOUND';
									leave sp_Memo_Process_Get;
								end if;


ELSEIF ls_Type = 'MEMO' and ls_Sub_Type = 'TRANSACTION_TRACK' then


			select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Request_Gid'))) into @Request_Gid;

						if @Request_Gid is  null or @Request_Gid = '' then
							set Message = 'Request Gid Is Not Given';
							leave sp_Memo_Process_Get;
						End if;

            set Query_Select = '';
			set Query_Select = concat('select A.requesttran_gid,A.requesttran_requestgid,A.requesttran_to,
											  A.requesttran_totype,
										      A.requesttran_status,A.requesttran_date,
                                              A.create_date,A.requesttran_by ,B.employee_name,null file_name,
											  null file_path,A.requesttran_comments
													from mem_trn_trequesttran A
														left join gal_mst_temployee B on A.requesttran_to=B.employee_gid
															  and B.employee_isactive=''Y'' and B.employee_isremoved=''N''
															  and B.entity_gid in(',@Entity_Gids,')
															where A.requesttran_requestgid=',@Request_Gid,'
                                                            and requesttran_by=0 and
                                                            requesttran_status =''PENDING-APPROVAL''
																and A.requesttran_isremoved=''N''
                                                                and A.entity_gid in(',@Entity_Gids,')

                                                          union all

									select A.requesttran_gid,A.requesttran_requestgid,A.requesttran_to,A.requesttran_totype,
										      A.requesttran_status,A.create_date  requesttran_date,
                                              A.create_date ,A.requesttran_by,B.employee_name,F.file_name,
											  concat(''/media/'',substring_index(F.file_path,''/media/'',-1)) as file_path,
                                              A.requesttran_comments
													from mem_trn_trequesttran A
														left join gal_mst_temployee B on A.requesttran_from=B.employee_gid
															  and B.employee_isactive=''Y'' and B.employee_isremoved=''N''
															  and B.entity_gid in(',@Entity_Gids,')
                                                        left join gal_mst_tfile F on F.file_gid=A.requesttran_filegid
															  and F.file_isactive=''Y'' and F.file_isremoved=''N''
															  and F.entity_gid in(',@Entity_Gids,')
															where A.requesttran_requestgid=',@Request_Gid,'
																and requesttran_to=0
                                                                and requesttran_by=0
                                                                and requesttran_status in (''APPROVED'',''REJECTED'')
																and A.requesttran_isremoved=''N''
                                                                and A.entity_gid in(',@Entity_Gids,')
																 ');


								set @Query_Select = Query_Select;
			      		        #select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

								if li_count > 0 then
									set Message = 'FOUND';
								else
									set Message = 'NOT_FOUND';
									leave sp_Memo_Process_Get;
								end if;


end if;

END