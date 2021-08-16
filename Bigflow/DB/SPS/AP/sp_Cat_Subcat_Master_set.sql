CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Cat_Subcat_Master_set`(
IN `Type` varchar(16),
IN `Sub_Type` varchar(16),
IN `lj_filters` json,
IN `lj_classification` json,
OUT `Message` text )
Cat_Subcat_Master_Set :BEGIN

#Akshay       2-08-2019
#Vishnu 	Jan-24-2020
declare Query_Insert text;
declare Query_Update varchar(1000);
declare errno int;
declare msg varchar(1000);
declare PV_NO varchar(16);
declare countRow int;
declare i int;
declare find int;
declare lj_Inv_Status json;

DECLARE done INT UNSIGNED DEFAULT 0;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
DECLARE EXIT HANDLER FOR SQLEXCEPTION,sqlwarning
    BEGIN

    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
    set Message = concat(errno , msg);
    ROLLBACK;
    END;

		SET autocommit = 0;
		start transaction;

		select JSON_LENGTH(lj_filters,'$') into @li_json_count;
		select JSON_LENGTH(lj_classification,'$') into @li_json_count1;

         if  @li_json_count <=0  then
			set Message = 'No Data in Json Object';
			leave Cat_Subcat_Master_Set;
        end if;

		if  @li_json_count1 <=0  then
			set Message = 'No classification in Json Object';
			leave Cat_Subcat_Master_Set;
		end if;

         select JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Entity_Gid'))) into @Entity_Gid;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Create_by'))) into @Create_by;

 if Type = 'INSERT' and  Sub_Type='add_category'  then

		#select lj_filters;
		#select lj_classification;

        select JSON_UNQUOTE(JSON_EXTRACT(lj_filters, CONCAT('$.category_name'))) into @category_name;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filters, CONCAT('$.category_no'))) into @category_no;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filters, CONCAT('$.category_code'))) into @category_code;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filters, CONCAT('$.category_glno'))) into @category_glno;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filters, CONCAT('$.category_isactive'))) into @category_isactive;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filters, CONCAT('$.category_isasset'))) into @category_isasset;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filters, CONCAT('$.category_isremoved'))) into @category_isremoved;
       #select  @category_name,@category_no,@category_code,@category_glno,@category_isactive,@category_isremoved,@Entity_Gid,@Create_by;

						# if exists (select 'true'
						#							from ap_mst_tcategory
						#							where
                         #                           lower(category_no)=lower(@category_no)
                         #                           or  lower(category_name)=lower(@category_name)
                         #                           or  lower(category_code)=lower(@category_code))  then
						#			   set Message = 'This Record Is Exists ';
						#			   leave Cat_Subcat_Master_Set;

				         #end if;


       set  Query_Insert = '';
       set Query_Insert = concat('insert into ap_mst_tcategory
                                                   (category_code,
                                                    category_no,
                                                    category_name,
                                                    category_glno,
                                                    category_isactive,
                                                    category_isasset,
													entity_gid,
                                                    create_by
													)
                                                    values(''',@category_code,''',
                                                               ''',@category_no,''',
                                                               ''',@category_name,''',
                                                               ''',@category_glno,''',
                                                               ''',@category_isactive,''',
                                                               ''',@category_isasset,''',
															   ''',@Entity_Gid,''',
                                                               ''',@Create_by,''')');

							set @Insert_query = Query_Insert;
							#select Query_Insert; ## Remove It
							PREPARE stmt FROM @Insert_query;
							EXECUTE stmt;
							set countRow = (select ROW_COUNT());
							DEALLOCATE PREPARE stmt;



							if countRow > 0 then
							set Message = 'SUCCESS';
							commit;

							 else
							set Message = 'FAIL';
							leave Cat_Subcat_Master_Set;
							End if;
elseif Type = 'UPDATE' and  Sub_Type='add_category'  then
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filters, CONCAT('$.Category_Gid'))) into @Category_Gid;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filters, CONCAT('$.Category_isasset'))) into @Category_isasset;

        #if @Category_Gid is null or @Category_Gid = 0 THEN
			#set Message  = 'Category Gid Is Needed.';
		 #  leave  sp_Cat_Subcat_Master_set;
		#End if;

		#if @Category_isasset is null or @Category_isasset = 0 THEN
		  #set Message = 'Category isasset Is Needed.';
		  #leave sp_Cat_Subcat_Master_set;
		#End if;

       set  Query_Insert = '';
       set Query_Insert = concat('UPDATE ap_mst_tcategory
											SET category_isasset = ''',@Category_isasset,'''
                                            WHERE category_gid =''',@Category_Gid,'''');

							set @Insert_query = Query_Insert;
							#select Query_Insert; ## Remove It
							PREPARE stmt FROM @Insert_query;
							EXECUTE stmt;
							set countRow = (select ROW_COUNT());
							DEALLOCATE PREPARE stmt;

							if countRow > 0 then
							set Message = 'SUCCESS';
							commit;

							 else
							set Message = 'FAIL';
							leave Cat_Subcat_Master_Set;
							End if;

elseif  Type = 'INSERT' and  Sub_Type='add_subcategory'  then

	    select lj_filters;
		select lj_classification;
        select JSON_LENGTH(lj_filters,'$.subcategory_categorygid') into @li_json_count;
        select  @li_json_count;
		set @i=0;
        set @count1=0;
        while @i<@li_json_count do
		set find=0;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filters, CONCAT('$.subcategory_code'))) into @subcategory_code;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filters, CONCAT('$.subcategory_no'))) into @subcategory_no;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filters, CONCAT('$.subcategory_name'))) into @subcategory_name;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filters, CONCAT('$.subcategory_categorygid[',@i,']'))) into @subcategory_categorygid;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filters, CONCAT('$.subcategory_glno'))) into @subcategory_glno;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filters, CONCAT('$.subcategory_isactive'))) into @subcategory_isactive;
        select  @subcategory_code,@subcategory_no,@subcategory_name,@subcategory_categorygid,@subcategory_glno,@subcategory_isactive,@Entity_Gid,@Create_by;
         select category_glno,category_no into @glno,@catno from ap_mst_tcategory where category_gid = @subcategory_categorygid;
		set @final_gl = concat(@glno,@catno,@subcategory_no);
                    #if exists (select 'true'
						#							from ap_mst_tsubcategory
						#							where
                        #                            lower(subcategory_no)=lower(@subcategory_no)
                         #                           or  lower(subcategory_name)=lower(@subcategory_name)
                         #                           or  lower(subcategory_code)=lower(@subcategory_code)
                         #                           )  then
						#			   set find=1;

				        # end if;

                         if find=0 then

						   set  Query_Insert = '';
						   set Query_Insert = concat('insert into ap_mst_tsubcategory
                                                   (subcategory_name,
                                                    subcategory_code,
                                                    subcategory_no,
                                                    subcategory_categorygid,
                                                    subcategory_glno,
                                                    subcategory_isactive,
                                                    entity_gid,
                                                    create_by
                                                    )
                                                    values(''',@subcategory_name,''',
                                                               ''',@subcategory_code,''',
                                                               ''',@subcategory_no,''',
                                                               ''',@subcategory_categorygid,''',
                                                               ''',@final_gl,''',
                                                               ''',@subcategory_isactive,''',
                                                               ''',@Entity_Gid,''',
                                                               ''',@Create_by,''')');

							set @Insert_query = Query_Insert;
							#select Query_Insert; ## Remove It
							PREPARE stmt FROM @Insert_query;
							EXECUTE stmt;
							set countRow = (select ROW_COUNT());
							DEALLOCATE PREPARE stmt;

                            if countRow > 0 then
							set @count1=@count1+1;
							end if;

            end if;

							set @i=@i+1;
							end while;



							if @count1 = @li_json_count then
							set Message = 'SUCCESS';
                            #select @count1;
							commit;
							else
                            set Message='This Records is Exists';
                            leave Cat_Subcat_Master_Set;
							End if;

elseif  Type = 'INSERT' and  Sub_Type='add_cc'  then

	   #select lj_filters;
		#select lj_classification;

        select JSON_UNQUOTE(JSON_EXTRACT(lj_filters, CONCAT('$.tcc_bsgid'))) into @tcc_bsgid;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filters, CONCAT('$.tcc_code'))) into @tcc_code;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filters, CONCAT('$.tcc_no'))) into @tcc_no;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filters, CONCAT('$.tcc_name'))) into @tcc_name;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filters, CONCAT('$.tcc_remarks'))) into @tcc_remarks;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filters, CONCAT('$.tcc_isactive'))) into @tcc_isactive;
        #select JSON_UNQUOTE(JSON_EXTRACT(lj_filters, CONCAT('$.category_isremoved'))) into @category_isremoved;
       #select  @category_name,@category_no,@category_code,@category_glno,@category_isactive,@category_isremoved,@Entity_Gid,@Create_by;

                        if  @tcc_remarks  is  null then
							set  @tcc_remarks='';
					   end if;

						 if exists (select 'true'
													from ap_mst_tcc
													where
                                                    lower(tcc_no)=lower(@tcc_no)
                                                    or  lower(tcc_name)=lower(@tcc_name)
                                                    or  lower(tcc_code)=lower(@tcc_code))  then
									   set Message = 'This Record Is Exists ';
									   leave Cat_Subcat_Master_Set;

				         end if;

       set  Query_Insert = '';
       set Query_Insert = concat('insert into  ap_mst_tcc
                                                   (tcc_bsgid,tcc_code,
                                                    tcc_no,
                                                    tcc_name,
                                                    tcc_remarks,
                                                    tcc_isactive,
													entity_gid,
                                                    create_by
													)
                                                    values(''',@tcc_bsgid,''',
														   ''',@tcc_code,''',
                                                               ''',@tcc_no,''',
                                                               ''',@tcc_name,''',
                                                               ''',@tcc_remarks,''',
                                                               ''',@tcc_isactive,''',
															   ''',@Entity_Gid,''',
                                                               ''',@Create_by,''')');

							set @Insert_query = Query_Insert;
							#select Query_Insert; ## Remove It
							PREPARE stmt FROM @Insert_query;
							EXECUTE stmt;
							set countRow = (select ROW_COUNT());
							DEALLOCATE PREPARE stmt;



							if countRow > 0 then
							set Message = 'SUCCESS';
							commit;

							 else
							set Message = 'FAIL';
							leave Cat_Subcat_Master_Set;
							End if;


 elseif  Type = 'INSERT' and  Sub_Type='add_bs'  then

	   #select lj_filters;
		#select lj_classification;

        select JSON_UNQUOTE(JSON_EXTRACT(lj_filters, CONCAT('$.tbs_code'))) into @tbs_code;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filters, CONCAT('$.tbs_no'))) into @tbs_no;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filters, CONCAT('$.tbs_name'))) into @tbs_name;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filters, CONCAT('$.tbs_remarks'))) into @tbs_remarks;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_filters, CONCAT('$.tbs_isactive'))) into @tbs_isactive;
        #select JSON_UNQUOTE(JSON_EXTRACT(lj_filters, CONCAT('$.category_isremoved'))) into @category_isremoved;
       #select  @category_name,@category_no,@category_code,@category_glno,@category_isactive,@category_isremoved,@Entity_Gid,@Create_by;
							 if  @tbs_remarks  is  null then
								set  @tbs_remarks='';
							end if;

						 if exists (select 'true'
													from ap_mst_tbs
													where
                                                    lower(tbs_no)=lower(@tbs_no)
                                                    or  lower(tbs_name)=lower(@tbs_name)
                                                    or  lower(tbs_code)=lower(@tbs_code))  then
									   set Message = 'This Record Is Exists ';
									   leave Cat_Subcat_Master_Set;

				         end if;


       set  Query_Insert = '';
       set Query_Insert = concat('insert into ap_mst_tbs
                                                   (tbs_code,
                                                    tbs_name,
                                                    tbs_no,
                                                    tbs_remarks,
                                                    tbs_isactive,
													entity_gid,
                                                    create_by
													)
                                                    values(''',@tbs_code,''',
                                                               ''',@tbs_name,''',
                                                               ''',@tbs_no,''',
                                                               ''',@tbs_remarks,''',
                                                               ''',@tbs_isactive,''',
															   ''',@Entity_Gid,''',
                                                               ''',@Create_by,''')');

							set @Insert_query = Query_Insert;
                            select Query_Insert;
							#select Query_Insert; ## Remove It
							PREPARE stmt FROM @Insert_query;
							EXECUTE stmt;
							set countRow = (select ROW_COUNT());
							DEALLOCATE PREPARE stmt;



							if countRow > 0 then
							set Message = 'SUCCESS';
							commit;

							 else
							set Message = 'FAIL';
							leave Cat_Subcat_Master_Set;
							End if;


 End if;



END