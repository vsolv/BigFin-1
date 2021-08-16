CREATE DEFINER=`root`@`%` PROCEDURE `sp_ControlSheet_Set`(IN `ls_Action` varchar(32),IN `ls_Type` varchar(32),IN `ls_SubType` varchar(32) ,
IN `lj_Data` json,IN `lj_File` JSON,IN `lj_Classification` JSON,IN `li_Create_By` INT ,OUT `Message` varchar(5000)
)
sp_ControlSheet_Set:BEGIN
#### Ramesh : June 21 2019
declare Query_Insert varchar(10000);
Declare Query_Update text;
declare Query_Column varchar(500);
declare Query_Value varchar(500);
declare errno int;
declare msg varchar(1000);
declare countRow int;
declare i int;
declare Latest_Dump_Version int;
Declare lj_Excel_count json;


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

    select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification,'$.Entity_Gid')) into @Entity_Gid;
   # select @Entity_Gid;

    if @Entity_Gid is null or @Entity_Gid =0  or @Entity_Gid = '' then
			set Message = 'Entity Gid Is Needed in Classification Data.';
            leave sp_ControlSheet_Set;
    End if;

 If ls_Type = 'CONTROL_SALES' then
        select  JSON_LENGTH(lj_Data, '$.SALE_DETAILS') into @SalesD_Count;

        if @SalesD_Count is null or @SalesD_Count = '' or @SalesD_Count = 0 then
			set Message = 'No Sale Details Found To Upload And Compare.';
            leave sp_ControlSheet_Set;
        End if;

        if ls_SubType = 'TALLY' then
				set @Dump_Source = 'TALLY';
                set @Dump_Type = 'SALES';
                select ifnull(max(ctldump_version),0)+1 into @Dump_Version from gal_trn_tctldump where ctldump_type = @Dump_Type
                 and entity_gid = @Entity_Gid
				and date_format(create_date,'%Y-%b-%d') = date_format(current_date(),'%Y-%b-%d') ;

                ### File Part
							select JSON_LENGTH(lj_File,'$') into @li_json_class_filepath;

							if  @li_json_class_filepath is null or @li_json_class_filepath=0 then
									set Message='No File Path';
									rollback;
									leave sp_ControlSheet_Set;
							end if;

								  # to do loop
							  select JSON_UNQUOTE(JSON_EXTRACT(lj_File,CONCAT('$[0].SavedFilePath'))) into @file_Path;
							  select JSON_UNQUOTE(JSON_EXTRACT(lj_File,CONCAT('$[0].File_Name'))) into @file_Name;

						   set  @file_Id=0;

					   call sp_File_Set('Insert','a',@file_Id,@file_Name,@file_Path,
									lj_Classification, '{}',li_Create_By ,@Message);
									select @Message into @Out_Msg_Ctrl;

									SELECT SUBSTRING_INDEX(@Out_Msg_Ctrl, ',', 1) into @ctrl_file_gid;

        End if;

        set @Excel_Saved_Count = 0 ;
        set i = 0 ;
        While i <= @SalesD_Count - 1 Do
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.SALE_DETAILS[',i,'].Customer_Name'))) into @Customer_Name;
                select  JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.SALE_DETAILS[',i,'].Product_Name'))) into @Product_Name;
                select  JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.SALE_DETAILS[',i,'].Invoice_Date'))) into @Invoice_Date;
                select  JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.SALE_DETAILS[',i,'].Invoice_No'))) into @Invoice_No;
                select  JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.SALE_DETAILS[',i,'].Quantity'))) into @Quantity;
                select  JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.SALE_DETAILS[',i,'].Per_Rate'))) into @Per_Rate;
                select  JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.SALE_DETAILS[',i,'].Amount'))) into @Amount;

                if @Customer_Name = '' or @Customer_Name is null then
					set Message = 'Customer Name Is Needed in Uploaded Data.';
                    rollback;
                    leave sp_ControlSheet_Set;
                End if;

                if @Product_Name = '' or @Product_Name is null then
					set Message = 'Product Name Is Needed in Uploaded Data.';
                    rollback;
                    leave sp_ControlSheet_Set;
                End if;

                if @Invoice_Date = '' or @Invoice_Date is null then
					set Message = 'Invoice Date Is Needed in Uploaded Data.';
                    rollback;
                    leave sp_ControlSheet_Set;
                End if;

                if @Quantity = '' or @Quantity is null then
					set Message = 'Quantity In Uploaded Data.';
                    rollback;
                    leave sp_ControlSheet_Set;
                End if;

				if @Invoice_No = '' or @Invoice_No is null then
					set Message = 'Invoice Is Needed In Uploaded Data.';
                    rollback;
                    leave sp_ControlSheet_Set;
                End if;

				if @Per_Rate = '' or @Per_Rate is null then
					set Message = 'Per Rate Is Needed In Uploaded Data.';
                    rollback;
                    leave sp_ControlSheet_Set;
                End if;

				if @Amount = '' or @Amount is null then
					set Message = 'Amount Is Needed In Uploaded Data.';
                    rollback;
                    leave sp_ControlSheet_Set;
                End if;


			if ls_SubType = 'TALLY' then
							#### Insert In table.

						set Query_Column = '';
								set Query_Value = '';

           elseif ls_SubType = 'SYSTEM' then
                    set  @ctrl_file_gid=0;
					set @Dump_Source = 'BIGFLOW';
					set @Dump_Type = 'SALES';

                    select ifnull(max(ctldump_version),0) into @Dump_Version from gal_trn_tctldump where ctldump_type = @Dump_Type
						and entity_gid = @Entity_Gid
						and date_format(create_date,'%Y-%b-%d') = date_format(current_date(),'%Y-%b-%d') ;

                    #### Query Column and Value

                    set Query_Column = '';
                    set Query_Value = '';

                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.SALE_DETAILS[',i,'].Status'))) into @ls_Status;

                    if @ls_Status is not null or @ls_Status <> '' then
							set Query_Column = concat(Query_Column,' ctldump_status ,');
                            set Query_Value = concat(Query_Value,' ''',@ls_Status,''', ');
                    End if;


           End if;

                set Query_Insert = '';
                set Query_Insert = concat('Insert into gal_trn_tctldump (ctldump_filegid,ctldump_customername,ctldump_productname,ctldump_qty,ctldump_unitrate,
															ctldump_invdate,ctldump_invoiceno,ctldump_invamt,ctldump_source,ctldump_version,ctldump_type,',Query_Column,' entity_gid,create_by)
															values(',@ctrl_file_gid,',''',@Customer_Name,''',''',@Product_Name,''',''',@Quantity,''',''',@Per_Rate,''',
                                                            ''',@Invoice_Date,''',''',@Invoice_No,''',''',@Amount,''',''',@Dump_Source,''',',@Dump_Version,',''',@Dump_Type,''',',Query_Value,'
                                                            ',@Entity_Gid,',',li_Create_By,'
                                                            )');

									set @Insert_query = Query_Insert;
									PREPARE stmt FROM @Insert_query;
									EXECUTE stmt;
									set countRow = (select ROW_COUNT());
									DEALLOCATE PREPARE stmt;

                                    if countRow > 0 then
										  set Message = 'SUCCESS';
                                          set @Excel_Saved_Count = @Excel_Saved_Count+1;
                                     else
                                         set Message = 'FAIL';
                                    End if;


                set i = i + 1;
        End While;

        if ls_SubType = 'TALLY' then
				set lj_Excel_count = concat('{"Excel_Count":',@SalesD_Count,',"Saved_Count":',@Excel_Saved_Count,'}');
                select lj_Excel_count;
        End if;

elseif ls_Type = 'CONTROL_OUTSTANDING' then
          select  JSON_LENGTH(lj_Data, '$.OUTSTANDING_DETAILS') into @OutstandingD_Count;

        if @OutstandingD_Count is null or @OutstandingD_Count = '' or @OutstandingD_Count = 0 then
			set Message = 'No Outstanding Details Found To Upload And Compare.';
            leave sp_ControlSheet_Set;
        End if;

        if ls_SubType = 'TALLY' then
				set @Dump_Source = 'TALLY';
                set @Dump_Type = 'OUTSTANDING';
                select ifnull(max(ctldump_version),0)+1 into @Dump_Version from gal_trn_tctldump where ctldump_type = @Dump_Type
                 and entity_gid = @Entity_Gid
				and date_format(create_date,'%Y-%b-%d') = date_format(current_date(),'%Y-%b-%d') ;

                ###### File Part.
								select JSON_LENGTH(lj_File,'$') into @li_json_class_filepath;

									if  @li_json_class_filepath is null or @li_json_class_filepath=0 then
										set Message='No File Path';
										rollback;
										leave sp_ControlSheet_Set;
									End if;
								  # to do loop
								  Select JSON_UNQUOTE(JSON_EXTRACT(lj_File,CONCAT('$[0].SavedFilePath'))) into @file_Path;
								  Select JSON_UNQUOTE(JSON_EXTRACT(lj_File,CONCAT('$[0].File_Name'))) into @file_Name;

								set  @file_Id=0;

							call sp_File_Set('Insert','a',@file_Id,@file_Name,@file_Path,
									lj_Classification, '{}',li_Create_By ,@Message);
									select @Message into @Out_Msg_Ctrl;

									SELECT SUBSTRING_INDEX(@Out_Msg_Ctrl, ',', 1) into @ctrl_file_gid;
							#### Insert In table.

			End if;

              set @Excel_Saved_Count = 0 ;
        set i = 0 ;
        While i <= @OutstandingD_Count - 1 Do
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.OUTSTANDING_DETAILS[',i,'].Customer_Name'))) into @Customer_Name;
                select  JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.OUTSTANDING_DETAILS[',i,'].Invoice_Date'))) into @Invoice_Date;
                select  JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.OUTSTANDING_DETAILS[',i,'].Invoice_No'))) into @Invoice_No;
                select  JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.OUTSTANDING_DETAILS[',i,'].Pending_Amount'))) into @Pending_Amount;
                select  JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.OUTSTANDING_DETAILS[',i,'].Amount'))) into @Amount;

                if @Customer_Name = '' or @Customer_Name is null then
					set Message = 'Customer Name Is Needed in Uploaded Data.';
                    rollback;
                    leave sp_ControlSheet_Set;
                End if;

                if @Invoice_Date = '' or @Invoice_Date is null then
					set Message = 'Invoice Date Is Needed in Uploaded Data.';
                    rollback;
                    leave sp_ControlSheet_Set;
                End if;

				if @Invoice_No = '' or @Invoice_No is null then
					set Message = 'Invoice No Is Needed In Uploaded Data.';
                    rollback;
                    leave sp_ControlSheet_Set;
                End if;

				if @Pending_Amount = '' or @Pending_Amount is null then
					set Message = 'Per Rate Is Needed In Uploaded Data.';
                    rollback;
                    leave sp_ControlSheet_Set;
                End if;

                if @Amount = '' or @Amount is null then
					set Message = 'Amount Is Needed In Uploaded Data.';
                    rollback;
                    leave sp_ControlSheet_Set;
                End if;

			if ls_SubType = 'TALLY' then

						set Query_Column = '';
								set Query_Value = '';

           elseif ls_SubType = 'SYSTEM' then
                    set  @ctrl_file_gid=0;
					set @Dump_Source = 'BIGFLOW';
					set @Dump_Type = 'OUTSTANDING';

                    select ifnull(max(ctldump_version),0) into @Dump_Version from gal_trn_tctldump where ctldump_type = @Dump_Type
                     and entity_gid = @Entity_Gid
					and date_format(create_date,'%Y-%b-%d') = date_format(current_date(),'%Y-%b-%d')
                     ;
                    #### Query Column and Value
                    set Query_Column = '';
                    set Query_Value = '';

                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.OUTSTANDING_DETAILS[',i,'].Status'))) into @ls_Status;

                    if @ls_Status is not null or @ls_Status <> '' then
							set Query_Column = concat(Query_Column,' ctldump_status ,');
                            set Query_Value = concat(Query_Value,' ''',@ls_Status,''', ');
                    End if;

           End if;
                set Query_Insert = '';
                set Query_Insert = concat('Insert into gal_trn_tctldump (ctldump_filegid,ctldump_customername,
															ctldump_invdate,ctldump_invoiceno,ctldump_balanceamt,ctldump_invamt,ctldump_source,ctldump_version,ctldump_type,
                                                            ',Query_Column,' entity_gid,create_by)
															values(',@ctrl_file_gid,',''',@Customer_Name,''',''',@Invoice_Date,''',''',@Invoice_No,''',''',@Pending_Amount,''',
                                                            ''',@Amount,''',''',@Dump_Source,''',',@Dump_Version,',''',@Dump_Type,''',',Query_Value,'',@Entity_Gid,',',li_Create_By,'
                                                            )');

									set @Insert_query = Query_Insert;
									PREPARE stmt FROM @Insert_query;
									EXECUTE stmt;
									set countRow = (select ROW_COUNT());
									DEALLOCATE PREPARE stmt;

                                    if countRow > 0 then
										  set Message = 'SUCCESS';
                                             set @Excel_Saved_Count = @Excel_Saved_Count+1;
                                     else
                                         set Message = 'FAIL';
                                    End if;


                set i = i + 1;
        End While;

				 if ls_SubType = 'TALLY' then
							set lj_Excel_count = concat('{"Excel_Count":',@OutstandingD_Count,',"Saved_Count":',@Excel_Saved_Count,'}');
							select lj_Excel_count;
					End if;


elseif ls_Type = 'CONTROL_STOCK' then
				        set Query_Column = '';
						set Query_Value = '';


			select  JSON_LENGTH(lj_Data, '$.STOCK_DETAILS') into @StockD_Count;

			if @StockD_Count is null or @StockD_Count = '' or @StockD_Count = 0 then
				set Message = 'No Stock Details Found To Upload And Compare.';
				leave sp_ControlSheet_Set;
			End if;


        if ls_SubType = 'TALLY' then

				set @Dump_Source = 'TALLY';

                ### To DO
                		set @Dump_Type = 'STOCK';
                select ifnull(max(ctldump_version),0)+1 into @Dump_Version from gal_trn_tctldump where ctldump_type = @Dump_Type
                 and entity_gid = @Entity_Gid
				and date_format(create_date,'%Y-%b-%d') = date_format(current_date(),'%Y-%b-%d') ;

					if @Dump_Version = 0 then
						set @Dump_Version = 1;
                    End if;

                ###### File Part.
								select JSON_LENGTH(lj_File,'$') into @li_json_class_filepath;

									if  @li_json_class_filepath is null or @li_json_class_filepath=0 then
										set Message='No File Path';
										rollback;
										leave sp_ControlSheet_Set;
									End if;
								  # to do loop
								  Select JSON_UNQUOTE(JSON_EXTRACT(lj_File,CONCAT('$[0].SavedFilePath'))) into @file_Path;
								  Select JSON_UNQUOTE(JSON_EXTRACT(lj_File,CONCAT('$[0].File_Name'))) into @file_Name;

								set  @file_Id=0;
                               # set @lj_classification = '';
													#set @lj_classification = concat('{
																#				"Entity_gid":"',li_Entity_gid,'"
																#						}'    );

							call sp_File_Set('Insert','a',@file_Id,@file_Name,@file_Path,
									lj_Classification, '{}',li_Create_By ,@Message);
									select @Message into @Out_Msg_Ctrl;

									SELECT SUBSTRING_INDEX(@Out_Msg_Ctrl, ',', 1) into @ctrl_file_gid;

							#### Insert In table.

                            	select  JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.Godown_Gid'))) into @Godown_Gid;
							if @Godown_Gid = '' or @Godown_Gid is null then
									set Message = 'Godown Gid Is Needed in Uploaded Data.';
									rollback;
									leave sp_ControlSheet_Set;
							End if;

			elseif ls_SubType = 'GODOWN' then

						set @Dump_Type = 'STOCK';
						select ifnull(max(ctldump_version),0) into @Dump_Version from gal_trn_tctldump where ctldump_type = @Dump_Type
					and entity_gid = @Entity_Gid
					and date_format(create_date,'%Y-%b-%d') = date_format(current_date(),'%Y-%b-%d') ;

					if @Dump_Version = 0 then
						set @Dump_Version = 1;
                    End if;


							select  JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.Godown_Gid'))) into @Godown_Gid;
							if @Godown_Gid = '' or @Godown_Gid is null then
									set Message = 'Godown Gid Is Needed in Uploaded Data.';
									rollback;
									leave sp_ControlSheet_Set;
							End if;

			End if;

					select  JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.Date'))) into @upload_date;
                    set @upload_date=date_format(@upload_date,'%Y-%c-%d') ;

                	if @upload_date = '' or @upload_date is null then
							set Message = 'Date Is Needed in Uploaded Data.';
							rollback;
							leave sp_ControlSheet_Set;
					End if;

            ##select godown_name into @godown_name from gal_mst_tgodown where godown_gid = '1';
					set @Excel_Saved_Count = 0 ;
					set i = 0 ;
			While i <= @StockD_Count - 1 Do

				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.STOCK_DETAILS[',i,'].Particulars'))) into @Particulars;
                select  JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.STOCK_DETAILS[',i,'].Quantity'))) into @Quantity;
                      ### Validations.

                if @Particulars = '' or @Particulars is null then
					set Message = 'Particulars Is Needed in Uploaded Data.';
                    rollback;
                    leave sp_ControlSheet_Set;
                End if;

                if @Quantity = '' or @Quantity is null then
					set Message = 'Quantity Is Needed in Uploaded Data.';
                    rollback;
                    leave sp_ControlSheet_Set;
                End if;



			if ls_SubType = 'TALLY' then
						set @product_gid = 0;
                        Select product_gid into @product_gid from gal_mst_tproduct where product_tallyname = @Particulars and product_isremoved = 'N' ;
                        #and product_isactive = 'Y';# have to check but now temporarily comment
						#### Validation.

                        if @product_gid = 0 or @product_gid is null then
							  set Message = 'Product Details Not Found.';
                               rollback;
                              leave sp_ControlSheet_Set;
                        End if;

              elseif ls_SubType = 'GODOWN' then
						set @ctrl_file_gid=0;
						set @Dump_Source = 'GODOWN';
						set @Dump_Type = 'STOCK';
						select  JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.STOCK_DETAILS[',i,'].Particulars_Gid'))) into @Particulars_Gid;
						### validation.

					 if @Particulars_Gid = '' or @Particulars_Gid is null then
						set Message = 'Product Gid Is Needed in Uploaded Data.';
						rollback;
						leave sp_ControlSheet_Set;
					 End if;

                        set @product_gid = @Particulars_Gid;

			elseif ls_SubType = 'SYSTEM' then

                    set @ctrl_file_gid=0;
					set @Dump_Source = 'BIGFLOW';
					set @Dump_Type = 'STOCK';

                     set @Dump_Type = 'STOCK';
                    select ifnull(max(ctldump_version),0) into @Dump_Version from gal_trn_tctldump where ctldump_type = @Dump_Type
                   and entity_gid = @Entity_Gid
				 and date_format(create_date,'%Y-%b-%d') = date_format(current_date(),'%Y-%b-%d') ;

                    #### Query Column and Value
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.STOCK_DETAILS[',i,'].Particulars'))) into @Particulars;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.STOCK_DETAILS[',i,'].Status'))) into @ls_Status;
                    select  JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.STOCK_DETAILS[',i,'].Product_Gid'))) into @product_gid;

                    #### Only for System Data Insert :: Known its is Mismatched
                    if @ls_Status is not null or @ls_Status <> '' then
							set Query_Column = concat(Query_Column,' ctldump_status ,');
                            set Query_Value = concat(Query_Value,' ''',@ls_Status,''', ');
                    End if;

           End if;

			           select godown_name into @godown_name from gal_mst_tgodown where godown_gid = @Godown_Gid and godown_isactive='Y' and godown_isremoved = 'N';
                       ### Godown Name ::
                       #set@godown_name = 'KOTTIVAKKAM';

                    #  select Query_Column,Query_Value,@ctrl_file_gid,@Godown_Gid,@product_gid,@upload_date;
                    # select  @godown_name,@Particulars,@Quantity,@Dump_Source,@Dump_Version,@Dump_Type,@Entity_Gid,li_Create_By;

                set Query_Insert = '';
                set Query_Insert = concat('Insert into gal_trn_tctldump (ctldump_filegid,ctldump_godown_gid,ctldump_productgid,ctldump_invdate,ctldump_customername,ctldump_productname,ctldump_qty,
															ctldump_source,ctldump_version,ctldump_type,
                                                            ',Query_Column,' entity_gid,create_by)
															values(',@ctrl_file_gid,',',@Godown_Gid,',',@product_gid,',''',@upload_date,''',''',@godown_name,''',''',@Particulars,''',''',@Quantity,''',
                                                            ''',@Dump_Source,''',',@Dump_Version,',''',@Dump_Type,''',',Query_Value,'',@Entity_Gid,',',li_Create_By,'
                                                            )');
                                    # select Query_Insert;
									set @Insert_query = Query_Insert;
									PREPARE stmt FROM @Insert_query;
									EXECUTE stmt;
									set countRow = (select ROW_COUNT());
									DEALLOCATE PREPARE stmt;

                                    if countRow > 0 then
										  set Message = 'SUCCESS';
                                             set @Excel_Saved_Count = @Excel_Saved_Count+1;
                                     else
                                         set Message = 'FAIL';
                                    End if;


					set i = i + 1;
			End While;

				if ls_SubType = 'TALLY' then
						set lj_Excel_count = concat('{"Excel_Count":',@StockD_Count,',"Saved_Count":',@Excel_Saved_Count,'}');
						select lj_Excel_count;
				End if;



 elseif ls_Type = 'STATUS_UPDATE' then

					select  JSON_LENGTH(lj_Data, '$') into @Update_Count;
                  #  select @Update_Count;

				if @Update_Count is null or @Update_Count = '' or @Update_Count = 0 then
					set Message = 'No Data To Update.';
					leave sp_ControlSheet_Set;
				End if;

				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.CtrlDump_Gid'))) into @CtrlDump_Gid;
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.Status'))) into @ls_Status;


                set Query_Update = '';
                set Query_Update = concat('update gal_trn_tctldump set ctldump_status = ''',@ls_Status,''',update_by = ',li_Create_By,',update_date = current_timestamp()
				where ctldump_gid in ( ',@CtrlDump_Gid,')');

						set @Query_Update = Query_Update;
                       # select Query_Update;
						PREPARE stmt FROM @Query_Update;
						EXECUTE stmt;
						set countRow = (select ROW_COUNT());
						DEALLOCATE PREPARE stmt;

						if countRow >0 then
							set Message = 'SUCCESS';
						 else
							set Message = 'FAIL';
                        #    select Query_Update;
							leave sp_ControlSheet_Set;
						End if;

				#update gal_trn_tctldump set ctldump_status = @ls_Status,update_by = li_Create_By,update_date = current_timestamp()
				#where ctldump_gid = @CtrlDump_Gid;

				set Message = 'SUCCESS';

elseif ls_Type = 'SUMMARY_INSERT' then

			select  JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.Ctl_Type'))) into @Ctl_Type;
            select  JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.Ctl_Status'))) into @Ctl_Status;
            select  JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.Ctl_Version'))) into @Ctl_Version;

        set Query_Insert = '';
        set Query_Insert = concat('Insert into gal_trn_tctlsummary(ctlsummary_ctltype,ctlsummary_status,ctlsummary_version,create_by,entity_gid)
										Values(''',@Ctl_Type,''',''',@Ctl_Status,''',''',@Ctl_Version,''',',li_Create_By,',',@Entity_Gid,'
										)');

									set @Insert_query = Query_Insert;
									PREPARE stmt FROM @Insert_query;
									EXECUTE stmt;
									set countRow = (select ROW_COUNT());
									DEALLOCATE PREPARE stmt;

                                    if countRow > 0 then
										  set Message = 'SUCCESS';
                                    else
                                         set Message = 'FAIL3';
                                    End if;

  #update on 14.09.2019
elseif ls_Type = 'SUMMARY_UPDATE' then

			select  JSON_LENGTH(lj_Summary_Data, '$') into @Update_Count;

			if @Update_Count is null or @Update_Count = '' or @Update_Count = 0 then
				set Message = 'No Data To Update.';
				leave sp_ControlSheet_Set;
			End if;


			select  JSON_UNQUOTE(JSON_EXTRACT(lj_Summary_Data, CONCAT('$.Ctl_Type'))) into @Ctl_Type;
            select  JSON_UNQUOTE(JSON_EXTRACT(lj_Summary_Data, CONCAT('$.Ctl_Status'))) into @Ctl_Status;
            select  JSON_UNQUOTE(JSON_EXTRACT(lj_Summary_Data, CONCAT('$.Ctl_Version'))) into @Ctl_Version;
			select  JSON_UNQUOTE(JSON_EXTRACT(lj_Summary_Data, CONCAT('$.Ctl_Summary_Gid'))) into @Ctl_Summary_Gid;


			if @Ctl_Summary_Gid = '' or @Ctl_Summary_Gid is null then
				set Message = 'Ctl_Summary_Gid Is Needed in Uploaded Data.';
				rollback;
				leave sp_ControlSheet_Set;
			End if;

			set Query_Update = '';
			set Query_Update = concat('update gal_trn_tctlsummary set ctlsummary_status = ''',@Ctl_Status,''',ctlsummary_version=',Ctl_Version,',ctlsummary_ctltype=''',Ctl_Type,''',ctlsummary_status=''',Ctl_Status,''',update_by = ',li_Create_By,',update_date = current_timestamp()
			where ctlsummary_gid = ',@Ctl_Summary_Gid,'');

			set @Query_Update = Query_Update;
			PREPARE stmt FROM @Query_Update;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;

			if countRow > 0 then
				  set Message = 'SUCCESS';
			else
				 set Message = 'FAIL';
			End if;


 End if;



END