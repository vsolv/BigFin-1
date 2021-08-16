CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Memo_Mst_Process_Get`(IN `ls_Type` varchar(64),IN `ls_Sub_Type` varchar(64),
IN `lj_Filters` json,IN `lj_Classification` json, OUT `Message` varchar(1024))
sp_Memo_Mst_Process_Get:BEGIN
### Bala Mar 01 2020 - Created
Declare Query_Select varchar(4024);
Declare Query_Search varchar(1024);
Declare Query_Status varchar(1024);
Declare Query_Column varchar(1024);
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


		select  JSON_UNQUOTE(JSON_EXTRACT(lj_Classification,'$.Entity_Gid[0]')) into @Entity_Gids;

        if @Entity_Gids is  null or @Entity_Gids = '' then
				set Message = 'Entity_Gid Is Not Given';
                leave sp_Memo_Mst_Process_Get;
        End if;

IF ls_Type = 'MEMO' and ls_Sub_Type = 'CATEGORY_SUMMARY' then


				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Memo_Cat_Code'))) into @Memo_Cat_Code;
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Memo_Cat_Name'))) into @Memo_Cat_Name;


					set Query_Search = '';

					if @Memo_Cat_Code <> '' and @Memo_Cat_Code is not null  then
                         set Query_Search = concat(Query_Search,'and memocategory_code like ''','%',@Memo_Cat_Code,'%','''  ');
                    End if;

                    if @Memo_Cat_Name <> '' and @Memo_Cat_Name is not null  then
                         set Query_Search = concat(Query_Search,'and memocategory_name like ''','%',@Memo_Cat_Name,'%','''  ');
                    End if;


                   # select Query_Search;

			set Query_Select = '';
			set Query_Select = concat('SELECT memocategory_gid,memocategory_code,
											  memocategory_name,memocategory_remarks,
											  entity_gid,memocategory_isactive ,
											  memocategory_isremoved,create_by
												  from mem_mst_tmemocategory
													   where entity_gid in(',@Entity_Gids,')
                                                          ',Query_Search,'
												 ');


						set @Query_Select =Query_Select;
						#select @Query_Select; ### Remove It
						PREPARE stmt FROM @Query_Select;
						EXECUTE stmt;
						Select found_rows() into li_count;

						if li_count > 0 then
							set Message = 'FOUND';
						else
							set Message = 'NOT_FOUND';
							leave sp_Memo_Mst_Process_Get;
						end if;



ELSEIF ls_Type = 'MEMO' and ls_Sub_Type = 'SUB_CATEGORY_SUMMARY' then



				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Memo_SubCat_Code'))) into @Memo_SubCat_Code;
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Memo_SubCat_Name'))) into @Memo_SubCat_Name;
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Memo_Cat_Name'))) into @Memo_Cat_Name;



               set Query_Search = '';

					if @Memo_SubCat_Code <> '' and @Memo_SubCat_Code is not null  then
                         set Query_Search = concat(Query_Search,'and A.memosubcategory_code like ''','%',@Memo_SubCat_Code,'%','''  ');
                    End if;

                    if @Memo_SubCat_Name <> '' and @Memo_SubCat_Name is not null  then
                         set Query_Search = concat(Query_Search,'and A.memosubcategory_name like ''','%',@Memo_SubCat_Name,'%','''  ');
                    End if;

                    if @Memo_Cat_Name <> '' and @Memo_Cat_Name is not null  then
                         set Query_Search = concat(Query_Search,'and B.memocategory_name like ''','%',@Memo_Cat_Name,'%','''  ');
                    End if;




			set Query_Select = '';
			set Query_Select = concat('select A.memosubcategory_gid, A.memosubcategory_memocategorygid,
											  A.memosubcategory_code, A.memosubcategory_name,
											  A.memosubcategory_remarks, A.memosubcategory_isactive,
                                              A.memosubcategory_isremoved ,A.create_by,
                                              B.memocategory_name
												  from mem_mst_tmemosubcategory A
													  inner join mem_mst_tmemocategory B
                                                      on B.memocategory_gid= A.memosubcategory_memocategorygid
														 where  A.entity_gid in(',@Entity_Gids,')
                                                            and B.memocategory_isactive=''Y''
															and B.memocategory_isremoved=''N''
															and B.entity_gid in(',@Entity_Gids,')
													 ',Query_Search,'
												 ');




								set @Query_Select =Query_Select;
			      		        #select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

								if li_count > 0 then
									set Message = 'FOUND';
								else
									set Message = 'NOT_FOUND';
									leave sp_Memo_Mst_Process_Get;
								end if;



end if;

END