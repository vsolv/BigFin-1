CREATE DEFINER=`developer`@`%` PROCEDURE `galley`.`sp_TaxMaster_Set`(IN `ls_Action` varchar(32),IN `ls_Type` varchar(32),
IN `ls_Sub_Type` varchar(32),IN `lj_Details` json,IN `lj_Classification` json,
IN `ls_Createby` varchar(32),OUT `Message` varchar(1024)
)
sp_TaxMaster_Set:BEGIN
	# Ramesh Jan 28 2020
	declare Query_Insert varchar(9000);
    declare Query_Update varchar(9000);
    Declare errno int;
    Declare msg varchar(1000);
    declare countRow int;


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

       select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid[0]'))) into @Entity_Gid;

             if @Entity_Gid is  null or @Entity_Gid = 0 or @Entity_Gid = '' then
					set Message = 'Entity Gid Is Needed.';
                    leave sp_TaxMaster_Set;
             End if;


 if ls_Action = 'INSERT' and ls_Type = 'TAX' and ls_Sub_Type = 'TAX_NAME' THEN
                		select JSON_LENGTH(lj_Details,'$') into @li_Detailjson_count;
					if @li_Detailjson_count is null or @li_Detailjson_count = 0 then
							set Message = 'No Data In Json - Tax Master.';
                            leave sp_TaxMaster_Set;
					end if;

                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Tax_Name'))) into @Tax_Name;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Is_Receivable'))) into @Is_Receivable;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Is_Payable'))) into @Is_Payable;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.GL_No'))) into @GL_No;

                   if @Tax_Name is null or @Tax_Name = '' THEN
                     set Message = 'Tax Name Is Needed.';
                     leave sp_TaxMaster_Set;
                   End if;

                   if @GL_No is null or @GL_No = '' THEN
                     set Message = 'GL No Is Needed.';
                     leave sp_TaxMaster_Set;
                   End if;

                   select ifnull(max(tax_code),0) into @Current_Tax_Code from gal_mst_ttax;

                  call sp_Generatecode_Get('WITHOUT_DATE','TAX','00',@Current_Tax_Code,@Message);
					select @Message  into @New_Tax_Code ;

				 if @New_Tax_Code is null or @New_Tax_Code = '' THEN
				   set Message = 'Error On Tax Code.';
				   leave sp_TaxMaster_Set;
				 End if;


                  set Query_Insert = '';
                  set Query_Insert = concat('Insert into gal_mst_ttax (tax_code,tax_name,tax_glno,entity_gid,create_by)
                               values (''',@New_Tax_Code,''',''',@Tax_Name,''',''',@GL_No,''',''',@Entity_Gid,''',''',ls_Createby,'''
                                       )');

  								set @Insert_query = Query_Insert;
								#SELECT @Insert_query;
								PREPARE stmt FROM @Insert_query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;

                              if countRow > 0 then
									set Message = 'SUCCESS';
                               else
                                    set Message = 'FAIL';
                                   leave sp_TaxMaster_Set;
                              End if;


elseif ls_Action = 'INSERT' and ls_Type = 'SUB_TAX' and ls_Sub_Type = 'SUBTAX_NAME' then
     select JSON_LENGTH(lj_Details,'$') into @li_Detailjson_count;
          if @li_Detailjson_count is null or @li_Detailjson_count = 0 then
              set Message = 'No Data In Json - Tax Master.';
                            leave sp_TaxMaster_Set;
          end if;

                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Tax_Gid'))) into @Tax_Gid;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.SubTax_Name'))) into @SubTax_Name;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.SubTax_Remarks'))) into @SubTax_Remarks;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.GL_No'))) into @GL_No;

                   if @Tax_Gid is null or @Tax_Gid = '' THEN
                     set Message = 'TaxGid Is Needed.';
                     leave sp_TaxMaster_Set;
                   End if;

                   if @SubTax_Name is null or @SubTax_Name = '' THEN
                     set Message = 'SubTax Name Is Needed.';
                     leave sp_TaxMaster_Set;
                   End if;

                   if @GL_No is null or @GL_No = '' THEN
                     set Message = 'GL No Is Needed.';
                     leave sp_TaxMaster_Set;
                   End if;

                   select ifnull(max(subtax_code),0) into @Current_SubTax_Code from gal_mst_tsubtax;

                  call sp_Generatecode_Get('WITHOUT_DATE','ST','00',@Current_SubTax_Code,@Message);
				  select @Message  into @New_SubTax_Code ;
                  #select @New_SubTax_Code ;

				 if @New_SubTax_Code is null or @New_SubTax_Code = '' THEN
				   set Message = 'Error On SubTax Code.';
				   leave sp_TaxMaster_Set;
				 End if;


                  set Query_Insert = '';
                  set Query_Insert = concat('Insert into gal_mst_tsubtax (subtax_tax_gid,subtax_code,subtax_name,subtax_remarks,subtax_glno,entity_gid,create_by)
                               values (''',@Tax_Gid,''',''',@New_SubTax_Code,''',''',@SubTax_Name,''',''',@SubTax_Remarks,''',''',@GL_No,''',
                               ''',@Entity_Gid,''',''',ls_Createby,'''
                                       )');

                  set @Insert_query = Query_Insert;
                #SELECT @Insert_query;
                PREPARE stmt FROM @Insert_query;
                EXECUTE stmt;
                set countRow = (select ROW_COUNT());
                DEALLOCATE PREPARE stmt;

                              if countRow > 0 then
                                 set Message = 'SUCCESS';
                               else
                                    set Message = 'FAIL';
                                   leave sp_TaxMaster_Set;
                              End if;

elseif ls_Action = 'INSERT' and ls_Type = 'TAX_RATE' and ls_Sub_Type = 'TAX_RATE_NAME' then
     select JSON_LENGTH(lj_Details,'$') into @li_Detailjson_count;
          if @li_Detailjson_count is null or @li_Detailjson_count = 0 then
              set Message = 'No Data In Json - Tax Master.';
                            leave sp_TaxMaster_Set;
          end if;



                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.SubTax_Gid'))) into @SubTax_Gid;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Tax_Rate_Name'))) into @Tax_Rate_Name;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Tax_Rate'))) into @Tax_Rate;

                   if @SubTax_Gid is null or @SubTax_Gid = '' THEN
                     set Message = 'SubTax_Gid Is Needed.';
                     leave sp_TaxMaster_Set;
                   End if;

                   if @Tax_Rate_Name is null or @Tax_Rate_Name = '' THEN
                     set Message = 'Tax_Rate_Name Name Is Needed.';
                     leave sp_TaxMaster_Set;
                   End if;

                   if @Tax_Rate is null or @Tax_Rate = '' THEN
                     set Message = 'Tax_Rate No Is Needed.';
                     leave sp_TaxMaster_Set;
                   End if;

                   select ifnull(max(taxrate_code),0) into @Current_Tax_Rate_Code from gal_mst_ttaxrate;

                  call sp_Generatecode_Get('WITHOUT_DATE','TR','00',@Current_Tax_Rate_Code,@Message);
				  select @Message  into @New_Tax_Rate_Code ;


				 if @New_Tax_Rate_Code is null or @New_Tax_Rate_Code = '' THEN
				   set Message = 'Error On Tax Rate Code.';
				   leave sp_TaxMaster_Set;
				 End if;


                  set Query_Insert = '';
                  set Query_Insert = concat('Insert into gal_mst_ttaxrate (taxrate_subtax_gid,taxrate_code,taxrate_name,taxrate_rate,entity_gid,create_by)
                               values (''',@SubTax_Gid,''',''',@New_Tax_Rate_Code,''',''',@Tax_Rate_Name,''',''',@Tax_Rate,''',
                               ''',@Entity_Gid,''',''',ls_Createby,'''
                                       )');

                  set @Insert_query = Query_Insert;
                #SELECT @Insert_query;
                PREPARE stmt FROM @Insert_query;
                EXECUTE stmt;
                set countRow = (select ROW_COUNT());
                DEALLOCATE PREPARE stmt;

					  if countRow > 0 then
						set Message = 'SUCCESS';
					   else
							set Message = 'FAIL';
						   leave sp_TaxMaster_Set;
					  End if;

End if;


END