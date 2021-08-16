CREATE DEFINER=`developer`@`%` PROCEDURE `sp_AP_Category_Set`(IN `Action` varchar(16),IN `Type` varchar(16),IN `lj_filter` json, 
IN `lj_classification` json,IN `ls_create_by` int, OUT `Message` varchar(1000))
sp_AP_Category_Set:BEGIN

declare ls_error varchar(100);
declare countRow int;
declare errno int;
declare msg varchar(1000);
declare Query_Update varchar(1000);


	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
    set Message = concat(errno , msg);
    ROLLBACK;
    END;

set ls_error = '';

if Action = 'Insert' and Type='Category' then

	select JSON_LENGTH(lj_filter,'$') into @li_json_count;
	select JSON_LENGTH(lj_classification,'$') into @li_json_lj_classification_count;
    
    if @li_json_count = 0 or @li_json_count = '' or @li_json_count is null  then
		   set Message = 'No Filter Data Json ';            
		leave sp_AP_Category_Set;
	end if;
        
    if @li_json_lj_classification_count = 0 or @li_json_lj_classification_count = '' 
		or @li_json_lj_classification_count is null  then
		   set Message = 'No Classification Data In Json. ';            
		leave sp_AP_Category_Set;
	end if;

    select JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.entity_gid'))) into @entity_gid;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.category_no'))) into @category_no;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.category_name'))) into @category_name;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.category_glno'))) into @category_glno;

    


	if @entity_gid = 0 or @entity_gid = '' or @entity_gid is null  then
		   set Message = 'Entity Gid Is Not Given';            
		leave sp_AP_Category_Set;
	end if;
    
    if @category_no = '' or @category_no is null  then
		   set Message = 'Category Number Is Not Given';            
		leave sp_AP_Category_Set;
	end if;
    
    if @category_name = '' or @category_name is null  then
		   set Message = 'Category Name is Not Givern';            
		leave sp_AP_Category_Set;
	end if;
    
    if @category_glno = 0 or @category_glno = '' or @category_glno is null  then
		   set Message = 'Category  GLNO Is Not Given';            
		leave sp_AP_Category_Set;
	end if;
	
    #call sp_Generate_number_get('CAT','000',@Message);
	#select @Message into @category_code from dual;
    
    select max(category_code) into @categorycode from ap_mst_tcategory;
    call sp_Generatecode_Get('WITHOUT_DATE', 'CAT', '00000', @categorycode, @Message);
	select @Message into @category_code;
	start transaction;  


		set Query_Update = concat('INSERT INTO ap_mst_tcategory(category_code,category_no,category_name,
								category_glno,entity_gid,create_by) VALUES 
                                    (''',@category_code,''',',@category_no,',''',@category_name,''','
                                    ,@category_glno,',',@entity_gid, ',',ls_create_by, ')');

			set @Query_Update = Query_Update;
            select Query_Update;
			PREPARE stmt FROM @Query_Update;
			EXECUTE stmt;  
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;  
		
			if countRow > 0 then
				set Message = 'SUCCESS';
				commit;
			else
				set Message = 'FAIL';
				rollback;
			end if;
	 
    
end if;

if Action = 'Insert' and Type='Sub_Category' then

	select JSON_LENGTH(lj_filter,'$') into @li_json_count;
	select JSON_LENGTH(lj_classification,'$') into @li_json_lj_classification_count;
    
    if @li_json_count = 0 or @li_json_count = '' or @li_json_count is null  then
		   set Message = 'No Filter Data Json ';            
		leave sp_AP_Category_Set;
	end if;
        
    if @li_json_lj_classification_count = 0 or @li_json_lj_classification_count = '' 
		or @li_json_lj_classification_count is null  then
		   set Message = 'No Classification Data In Json. ';            
		leave sp_AP_Category_Set;
	end if;

    select JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.entity_gid'))) into @entity_gid;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.subcategory_no'))) into @subcategory_no;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.subcategory_name'))) into @subcategory_name;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.subcategory_categorygid'))) into @subcategory_categorygid;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.subcategory_glno'))) into @subcategory_glno;

    


	if @entity_gid = 0 or @entity_gid = '' or @entity_gid is null  then
		   set Message = 'Entity Gid Is Not Given';            
		leave sp_AP_Category_Set;
	end if;
    
    if @subcategory_no = '' or @subcategory_no is null  then
		   set Message = 'Sub Category Number Is Not Given';            
		leave sp_AP_Category_Set;
	end if;
    
    if @subcategory_name = '' or @subcategory_name is null  then
		   set Message = 'Sub Category Name is Not Givern';            
		leave sp_AP_Category_Set;
	end if;
    
    if @subcategory_categorygid = 0 or @subcategory_categorygid = '' or @subcategory_categorygid is null  then
		   set Message = 'Sub Category Gid Is Not Given';            
		leave sp_AP_Category_Set;
	end if;
    
    if @subcategory_glno = 0 or @subcategory_glno = '' or @subcategory_glno is null  then
		   set Message = 'Sub Category  GLNO Is Not Given';            
		leave sp_AP_Category_Set;
	end if;

    select max(subcategory_code) into @subcategorycode from ap_mst_tsubcategory;
    call sp_Generatecode_Get('WITHOUT_DATE', 'SUBCAT', '0000', @subcategorycode, @Message);
	select @Message into @subcategory_code;
	start transaction;  


		set Query_Update = concat('INSERT INTO ap_mst_tsubcategory(subcategory_code,subcategory_no,subcategory_name,
								subcategory_categorygid,subcategory_glno,entity_gid,create_by) VALUES 
                                    (''',@subcategory_code,''',',@subcategory_no,',''',@subcategory_name,''','
                                    ,@subcategory_categorygid,',''',@subcategory_glno,''','
                                    ,@entity_gid, ',',ls_create_by, ')');

			set @Query_Update = Query_Update;
			PREPARE stmt FROM @Query_Update;
			EXECUTE stmt;  
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;  
		
			if countRow > 0 then
				set Message = 'SUCCESS';
				commit;
			else
				set Message = 'FAIL';
				rollback;
			end if;
	 
    
end if;

END
