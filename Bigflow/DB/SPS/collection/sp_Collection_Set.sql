CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Collection_Set`(IN `Action` varchar(16),IN `Type` varchar(64),IN `li_coll_gid` int,
IN `li_cust_gid` int,IN `li_emp_gid` int,IN `ls_coll_mode` varchar(8),IN `ld_coll_amount` decimal(18,2),
IN `ls_coll_date` varchar(16),IN `li_coll_chequeno` varchar(8),IN `ls_desc` varchar(128),
IN `lj_Cheque` json,IN `lj_File` json,
IN `li_Entity_gid` int,IN `ls_create_by` int, OUT `Message` varchar(1000))
sp_Collection_Set:BEGIN

#Vigneshwari       16-02-2018
#Ramesh      Edit  28-05-2018
#Prakash     Edit  23-11-2018,25-01-2019 ## Dispatch,Update
# Ramesh Edit Dec 2018: Bank Gid. ## Multiple Check in Header.
# Ramesh Cltn Delete :: July 4 2019
# Karthiga  File img for cheque-multiple values edit 21 nov 19
declare coll_srch Text;
declare ls_error varchar(100);
declare countRow int;
declare errno int;
declare msg varchar(1000);
declare ls_no varchar(64);
declare Query1 varchar(1000);
declare Query2 varchar(1000);
declare Balance int;
declare Query_Insert varchar(1000);
declare Query_Update text;
declare i int;
Declare j int;
Declare k int;

	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
    set Message = concat(errno , msg);
    ROLLBACK;
    END;

set ls_error = '';
set Query1 = '';
set Query2 = '';
set @li_cust_gid = '';
#select 3;
if Action = 'Insert' and Type = 'INITIAL' then
#select '';
				if li_cust_gid = 0 then
							set ls_error = 'Customer Gid Not Given';
				else
							set @srch = concat('select customer_custgroup_gid into @li_cust_gid from gal_mst_tcustomer where customer_gid = ',li_cust_gid);
							PREPARE stmt1 FROM @srch;
							EXECUTE stmt1;
							set countRow = (select found_rows());
							DEALLOCATE PREPARE stmt1;
							if countRow = 0 then
								set ls_error = 'No Such Customer Present in Customer Table';
                                leave sp_Collection_Set;
							end if;
				end if;

					if li_emp_gid = 0 then
							set ls_error = 'Employee Gid Not Given';
							leave sp_Collection_Set;
					end if;

					if ls_coll_mode = '' then
							set ls_error = 'Collection Mode Not Given';
							leave sp_Collection_Set;
					end if;

                    if ls_coll_date = '' then
							set ls_error = 'Collection Date Not Given';
							leave sp_Collection_Set;
					end if;


						if ls_desc <> '' then
								set Query1 = concat(Query1 , ' fetcollectionheader_description,');
									set Query2 = concat(Query2 , '''',ls_desc,''',');
						else
									set Query1 = concat(Query1,'');
									set Query2 = concat(Query2,'');
						end if;

                        	if ls_coll_mode <> 'cheque' then
									if ld_coll_amount = 0.00 then
										set ls_error = 'Collection Amount Not Given';
										leave sp_Collection_Set;
								end if;
                            End if;

        ## Get Data from the Json.
    				select JSON_LENGTH(lj_Cheque,'$') into @li_json_count;

						if @li_json_count is not null or @li_json_count <> 0  then
								select JSON_UNQUOTE(JSON_EXTRACT(lj_Cheque, CONCAT('$.Bank_Gid[0]'))) into @Bank_Gid;
                                select JSON_UNQUOTE(JSON_EXTRACT(lj_Cheque, CONCAT('$.Ref_No[0]'))) into @Ref_No;
                                select JSON_UNQUOTE(JSON_EXTRACT(lj_Cheque, CONCAT('$.Collection_Status[0]'))) into @Collection_Status;

                                    if @Bank_Gid is null or @Bank_Gid = '' then
											set @Bank_Gid = 0 ;
                                    End if;

                                    if  (@Ref_No = '' or @Ref_No is null) and ls_coll_mode = 'NEFT' then
											set Message = 'For NEFT - Ref No Is Mandatory.';
                                            leave sp_Collection_Set;
									else
                                            set @Ref_No = 0;
                                    End if;

                                    if @Collection_Status = '' then
										set Message = 'Collection Status Is Needed.';
                                        leave sp_Collection_Set;
                                    End if;

                         else
                               set @Bank_Gid = 0;
                               set @Ref_No = 0;
						end if;




						### Again Frame The Columns.


                        if @Bank_Gid <> '' then
									set Query1 = concat(Query1 , ' fetcollectionheader_bankgid,');
									set Query2 = concat(Query2 , '''',@Bank_Gid,''',');
						else
									set Query1 = concat(Query1,'');
									set Query2 = concat(Query2,'');
						end if;

                        if @Ref_No <> 0 then
									set Query1 = concat(Query1 , ' fetcollectionheader_refno,');
									set Query2 = concat(Query2 , '''',@Ref_No,''',');
						else
									set Query1 = concat(Query1,'');
									set Query2 = concat(Query2,'');
						end if;

							if @Collection_Status = '' then
										set Message = 'Collection Status Is Needed.';
                                        leave sp_Collection_Set;
							End if;

                               if @Collection_Status <> '' then
									set Query1 = concat(Query1 , ' fetcollectionheader_status,');
									set Query2 = concat(Query2 , '''',@Collection_Status,''',');
								else
									set Query1 = concat(Query1,'');
									set Query2 = concat(Query2,'');
								end if;

                        ### Validate the Status TEXT TOO.
                        #FILE PART




						if ls_coll_mode = 'cheque' then

											select JSON_LENGTH(lj_Cheque,'$.CHEQUE') into @li_json_count;

											if @li_json_count is null or @li_json_count = 0 then
												set Message = 'No Data In Json - Cheque Details.';
												rollback;
												leave sp_Collection_Set;
											end if;

                                      # Validate Json data


                                     #select @li_json_count;
									set i = 0 ;
                                    set  @li_json_countt =  @li_json_count;
									WHILE i<= @li_json_countt - 1 Do
												#select i;
                                                 #select @li_json_count;
														select JSON_UNQUOTE(JSON_EXTRACT(lj_Cheque, CONCAT('$.CHEQUE[',i,'].Cheque_No'))) into @Cheque_No;
														select JSON_UNQUOTE(JSON_EXTRACT(lj_Cheque, CONCAT('$.CHEQUE[',i,'].Cheque_Date'))) into @Cheque_Date;
														select JSON_UNQUOTE(JSON_EXTRACT(lj_Cheque, CONCAT('$.CHEQUE[',i,'].Cheque_Amount'))) into @Cheque_Amount;
                                   						#select @Cheque_No,@Cheque_Date,@Cheque_Amount;

															#### Validate Json - Insert Data
															if @Cheque_No = '' then
																	set ls_error = 'Cheque No Not Given';
															end if;

															if @Cheque_Date = '' then
																	set ls_error = 'Cheque Date Not Given';
															end if;

															if @Cheque_Amount = 0.00 then
																	set ls_error = 'Cheque Amount Not Given';
																	leave sp_Collection_Set;
															end if;


                                                            ##### Validate The Duplicate Cheque. May 6 2019
                                                            set @Duplicate_Cheque = 0 ;
                                                            select ifnull(max(fetcollectionheader_gid),0) into @Duplicate_Cheque from fet_trn_tfetcollectionheader
                                                            where fetcollectionheader_chequeno = @Cheque_No
                                                            and date_format(fetcollectionheader_chequedate,'%Y-%m-%d') = date_format(@Cheque_Date,'%Y-%m-%d')
                                                            and fetcollectionheader_customergroup_gid = @li_cust_gid
															and fetcollectionheader_isactive = 'Y' and fetcollectionheader_isremoved = 'N' ;

                                                            if @Duplicate_Cheque > 0 then
																	set Message = 'Duplicate Cheque No Detected.';
                                                                    leave sp_Collection_Set;
                                                            End if;

															select JSON_LENGTH(lj_File,'$.File') into @li_json_class_filepath;
                                                           # select @li_json_class_filepath;

															if  @li_json_class_filepath is null or @li_json_class_filepath = 0 then
                                                           # select 1;
																set @li_file_Id=0 ;
																#end if;
                                                                else
                                                                    #select 2;
																	set k = 0 ;
																	WHILE k<= @li_json_class_filepath - 1 Do
																	select JSON_UNQUOTE(JSON_EXTRACT(lj_File,CONCAT('$.File[',k,'].RefTable_Gid'))) into @RefTable_Gid;
                                                                    if @Cheque_No = @RefTable_Gid then
                                                                    select JSON_UNQUOTE(JSON_EXTRACT(lj_File,CONCAT('$.File[',k,'].SavedFilePath'))) into @file_Path;
																	select JSON_UNQUOTE(JSON_EXTRACT(lj_File,CONCAT('$.File[',k,'].File_Name'))) into @file_Name;

																	#select @file_Path,@file_Name;
																	set  @file_Id=0;
																	set @lj_classification = '';
																	set @lj_classification = concat('{
																										"entity_gid":"',li_Entity_gid,'"
																									  }'    );

																	select count(file_gid) into @duplicate_check from gal_mst_tfile where file_path=@file_path;
																		if @duplicate_check > 0 then
																			set Message="Duplicate File Path";
																			leave sp_Collection_Set;
																		end if;


																		call sp_File_Set('Insert','a',@file_Id,@file_Name,@file_Path,
																			@lj_classification,'{}',ls_create_by ,@Message);
																			select @Message into @Out_Msg_Ctrl;

																			select LAST_INSERT_ID() into @li_file_Id ;
                                                                            #select @li_file_Id;
															        end if;
																	Set k = k + 1;
                                                                    #select k;
                                                                   # select @li_file_Id;
																	end while;
															end if;


																#### To Insert The Data :: Code Repeats:: Starts Again [CHEQUE]
															if ls_error = '' then
																	set coll_srch = concat('INSERT INTO fet_trn_tfetcollectionheader(fetcollectionheader_customergroup_gid,
																	fetcollectionheader_emp_gid, fetcollectionheader_mode, fetcollectionheader_amount,
																	fetcollectionheader_date,fetcollectionheader_chequeno,fetcollectionheader_chequedate,fetcollectionheader_filegid, ',Query1,' entity_gid, create_by) VALUES
																	(''',@li_cust_gid,''',''' ,li_emp_gid, ''',''',ls_coll_mode,''','''
																	,@Cheque_Amount, ''',''' ,ls_coll_date, ''',''',@Cheque_No,''',''',@Cheque_Date,''', ''',@li_file_Id,''',' ,Query2,'',li_Entity_gid, ','
																	,ls_create_by, ')');

																	set @coll_srch = coll_srch;
																	#SELECT @coll_srch;
																	PREPARE stmt FROM @coll_srch;
																	EXECUTE stmt;
																	set countRow = (select ROW_COUNT());
																	DEALLOCATE PREPARE stmt;

																	if countRow >  0 then
																					select LAST_INSERT_ID() into @collection_gid_MAX ;
																					set Message = 'SUCCESS';

																	else
																					set Message = 'FAIL';
																					rollback;
																				 leave   sp_Collection_Set;
																	end if;
															else
																	set Message = ls_error;
															end if;
															#### To Insert The Data :: Code Repeats:: Ends Again

                                                            # end if;
															#else
															#	set @li_file_Id=0 ;
															# Set k = k + 1;
															#select   @li_json_count;
															# end while;
															# end if;
								 Set i = i + 1;
                                 #select i;
								 End WHILE;



                        else #### if for a Collection Mode
                                    #### To Insert The Data :: Code Repeats:: Starts Again
												if ls_error = '' then
																		start transaction;
																		set coll_srch = concat('INSERT INTO fet_trn_tfetcollectionheader(fetcollectionheader_customergroup_gid,
																		fetcollectionheader_emp_gid, fetcollectionheader_mode, fetcollectionheader_amount,
																		fetcollectionheader_date, ',Query1,' entity_gid, create_by) VALUES
																		(''',@li_cust_gid,''',''' ,li_emp_gid, ''',''',ls_coll_mode,''','''
																		,ld_coll_amount, ''',''' ,ls_coll_date, ''',' ,Query2,'',li_Entity_gid, ','
																		,ls_create_by, ')');

																		set @coll_srch = coll_srch;
																		PREPARE stmt FROM @coll_srch;
																		EXECUTE stmt;
																		set countRow = (select ROW_COUNT());
																		DEALLOCATE PREPARE stmt;

																		if countRow >  0 then
																				 select LAST_INSERT_ID() into @collection_gid_MAX ;
																				 set Message = 'SUCCESS';
																		else
																				 set Message = 'FAIL';
																				 rollback;
																				leave sp_Collection_Set;
																		end if;
												else
														set Message = ls_error;
														leave sp_Collection_Set;
												end if;
                                                #### To Insert The Data :: Code Repeats:: Ends Again
									end if;

                                    #### To Affect in the Schedule
                                    set @Schedule_Affect = 'YES';
											if @Schedule_Affect = 'YES' and @collection_gid_MAX is not null and @collection_gid_MAX <> 0 and @collection_gid_MAX <> '' then
															set @followup_reason_gid = 0 ;
															select ifnull(followupreason_gid,0) into @followup_reason_gid from fet_mst_tfollowupreason
																where followupreason_name = ls_coll_mode  and followupreason_isactive = 'Y' and followupreason_isremoved = 'N' ;

                                                                if @followup_reason_gid = 0 then
																		set Message = 'Error On Schedule Update For Collection,No Follow Up Reason.';
                                                                        rollback;
                                                                        leave sp_Collection_Set;
                                                                End if;

												call sp_FETScheduleSPS_Set('SCHEDULE','REFERENCE','{}','COLLECTION',0,'',li_cust_gid ,li_emp_gid,0,
													'Remarks',@followup_reason_gid,@collection_gid_MAX,'','','{}','{}',li_Entity_gid,ls_create_by,@Message);
													if @Message = 'SUCCESS' then
															commit;
															set Message = 'SUCCESS';
													else
															set Message = @Message;
															rollback;
															leave sp_Collection_Set;
													End if;
                                    End if;  #### Check Schedule Affect

                                    #### Tran Affect.

                                      	call sp_Trans_Set('Insert','COLLECTION_RECEIPT',@collection_gid_MAX,'OPEND','I','MAKER','ONE',li_Entity_gid,ls_create_by,@message);
										select @message into @out_msg_tran ;

                                        if @out_msg_tran = 'FAIL' then
												set Message = 'Failed On Tran Update';
                                                rollback;
												leave sp_Collection_Set;
                                        End if;

    if ls_coll_mode = 'ChequeZZZZZZZZZZ' then

          #### Not In Use
		set Query_Insert = '';
		if 1=1 then
			select JSON_LENGTH(lj_Cheque,'$.CHEQUE') into @li_json_count;
            #select @li_json_count;

        if @li_json_count is null or @li_json_count = 0 then
			set Message = 'No Data In Json - Cheque Details.';
            rollback;
			leave sp_Collection_Set;
        end if;

        # Validate Json data
        set i = 0 ;
         WHILE i<= @li_json_count - 1 Do
         #select i;
			 select JSON_UNQUOTE(JSON_EXTRACT(lj_Cheque, CONCAT('$.CHEQUE[',i,'].Cheque_No[0]'))) into @Cheque_No;
             select JSON_UNQUOTE(JSON_EXTRACT(lj_Cheque, CONCAT('$.CHEQUE[',i,'].Cheque_Date[0]'))) into @Cheque_Date;
             select JSON_UNQUOTE(JSON_EXTRACT(lj_Cheque, CONCAT('$.CHEQUE[',i,'].Cheque_Amount[0]'))) into @Cheque_Amount;
             select JSON_UNQUOTE(JSON_EXTRACT(lj_Cheque, CONCAT('$.CHEQUE[',i,'].Bank_Name[0]'))) into @Bank_Name;

             set Query_Insert = concat('insert into fet_trn_tfetcollectionchq (fetcollectionchq_fetcollectionheadergid,fetcollectionchq_chqno,
					fetcollectionchq_chqdate,fetcollectionchq_chqamt,fetcollectionchq_bankname,entity_gid,
					create_by)
					values(',@coll_gid,',''',@Cheque_No,''',''',@Cheque_Date,''',''',@Cheque_Amount,''',''',@Bank_Name,''',
                    ',li_Entity_gid,',',ls_create_by,'
                    )');

            set @Insert_query = Query_Insert;
			#SELECT @Insert_query;
			PREPARE stmt FROM @Insert_query;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;

            if countRow <=0 then
				set Message = 'Error On Cheque Details Insert.';
                rollback;
                leave sp_Collection_Set;
            End if;

             set i = i + 1;


		END While;

        End if;
    End if;
    #set Message = CONCAT(@coll_gid,',SUCCESS');
    commit;
end if;

 if Action = 'Update'  and Type = 'SINGLE'then
					 if Action = 'Update' and Type = 'MULTIPLE_UPDATE' then
									select JSON_LENGTH(lj_Cheque,'$') into @li_json_count;
									if @li_json_count = 0 or @li_json_count is null then
											Set Message = 'No Data In JSON-To Update.';
											leave sp_Collection_Set;
									End if;
									select JSON_UNQUOTE(JSON_EXTRACT(lj_Cheque, CONCAT('$.Status[0]'))) into @lsStatus;
					 End if;
        #start
        select JSON_LENGTH(lj_Cheque,'$.CHEQUE') into @lj_Cheque_count;
		        if @lj_Cheque_count is null or @lj_Cheque_count = 0 then
						set Message = 'No status In Json - data.';
		        end if;
         select JSON_UNQUOTE(JSON_EXTRACT(lj_Cheque, CONCAT('$.CHEQUE.fetcollectionheader_dispatchgid[0]'))) into @lj_fetcollectionheader_dispatchgid;
		 select JSON_UNQUOTE(JSON_EXTRACT(lj_Cheque, CONCAT('$.CHEQUE.fetcollectionheader_status[0]'))) into @lj_fetcollectionheader_status;

			if li_coll_gid = 0 then
				set ls_error = 'Collection Gid Not Given';
			end if;

	if ls_error = '' then
        start transaction;
        set  Query_Update = Concat('update fet_trn_tfetcollectionheader set  update_by = ',ls_create_by,',update_date = now()');

                if ls_coll_date <> '' then
					set Query_Update = Concat(Query_Update, ',fetcollectionheader_date = ''', ls_coll_date ,'''');
                end if;

                if ld_coll_amount <> 0.00 then
					set Query_Update = Concat(Query_Update, ',fetcollectionheader_amount = ''', ld_coll_amount ,'''');
                end if;

                if ls_coll_mode <> '' then
					set Query_Update = Concat(Query_Update, ',fetcollectionheader_mode = ''', ls_coll_mode ,'''' );
                end if;

                if li_coll_chequeno <> '' then
					set Query_Update = Concat(Query_Update, ',fetcollectionheader_chequeno = ''', li_coll_chequeno ,'''' );
                end if;

                #add 2 condition
                if @lj_fetcollectionheader_status <>'' then
                   set Query_Update = Concat(Query_Update,',fetcollectionheader_status=''',@lj_fetcollectionheader_status,'''');
                end if;

                if @lj_fetcollectionheader_dispatchgid <> '' then
                   set Query_Update = Concat(Query_Update,',fetcollectionheader_dispatchgid=''',@lj_fetcollectionheader_dispatchgid,'''');
				end if;

				set Query_Update = Concat(Query_Update, ' where fetcollectionheader_gid = ''', li_coll_gid ,'''');

		set @coll_srch = Query_Update;
        #SELECT @coll_srch;
		PREPARE stmt FROM @coll_srch;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;

		if countRow >  0 then
			set Message = 'SUCCESS';

                #### Tran Update.

                 if @lj_fetcollectionheader_status <> '' and @lj_fetcollectionheader_status is not null then
							call sp_Trans_Set('update','COLLECTION_RECEIPT',li_coll_gid,@lj_fetcollectionheader_status,'I','CHECKER','STATUS',li_Entity_gid,ls_create_by,@message);
										select @message into @out_msg_tran ;
                                        if @out_msg_tran = 'FAIL' then
												set Message = 'Failed On Tran Update';
                                                rollback;
												leave sp_Collection_Set;
                                        End if;
                 End if;

		else
			set Message = 'FAIL';
			rollback;
		end if;
	else
		set Message = ls_error;
	end if;
    #/////////////////////////////////end ////
    if ls_coll_mode = 'Cheque' then
		set Query_Update = '';
		if 1=1 then
			select JSON_LENGTH(lj_Cheque,'$.CHEQUE') into @li_json_count;
           # select @li_json_count;

        if @li_json_count is null or @li_json_count = 0 then
			set Message = 'No Data In Json - Cheque Details.';
            rollback;
			leave sp_Collection_Set;
        end if;

        # Validate Json data
        set i = 0 ;
         WHILE i<= @li_json_count - 1 Do


			 select JSON_UNQUOTE(JSON_EXTRACT(lj_Cheque, CONCAT('$.CHEQUE[',i,'].Cheque_No[0]'))) into @Cheque_No;
             select JSON_UNQUOTE(JSON_EXTRACT(lj_Cheque, CONCAT('$.CHEQUE[',i,'].Cheque_Date[0]'))) into @Cheque_Date;
             select JSON_UNQUOTE(JSON_EXTRACT(lj_Cheque, CONCAT('$.CHEQUE[',i,'].Cheque_Amount[0]'))) into @Cheque_Amount;
             select JSON_UNQUOTE(JSON_EXTRACT(lj_Cheque, CONCAT('$.CHEQUE[',i,'].Bank_Name[0]'))) into @Bank_Name;
             select JSON_UNQUOTE(JSON_EXTRACT(lj_Cheque, CONCAT('$.CHEQUE[',i,'].Cheque_gid[0]'))) into @Cheque_gid;
             select JSON_UNQUOTE(JSON_EXTRACT(lj_Cheque, CONCAT('$.CHEQUE[',i,'].flag[0]'))) into @flag;


             if @flag = 'y' then

				if @Cheque_gid = 0 then
					set Message = 'cheque gid not given';
					leave sp_Collection_Set;
				end if;

				set  Query_Update = Concat('update fet_trn_tfetcollectionchq set  update_by = ',ls_create_by,',update_date = now()');

					if @Cheque_Date <> '' then
						set Query_Update = Concat(Query_Update, ',fetcollectionchq_chqdate = ''', @Cheque_Date ,'''');
					end if;

					if @Cheque_Amount <> 0.00 then
						set Query_Update = Concat(Query_Update, ',fetcollectionchq_chqamt = ''', @Cheque_Amount ,'''');
					end if;

					if @Bank_Name <> '' then
						set Query_Update = Concat(Query_Update, ',fetcollectionchq_bankname = ''', @Bank_Name ,'''' );
					end if;

					if @Cheque_No <> '' then
						set Query_Update = Concat(Query_Update, ',fetcollectionchq_chqno = ''', @Cheque_No ,'''' );
					end if;

					set Query_Update = Csp_StatePrice_getoncat(Query_Update, ' where fetcollectionchq_gid = ''', @Cheque_gid ,'''');

				set @Insert_query = Query_Update;
				#SELECT @Insert_query;
				PREPARE stmt FROM @Insert_query;
				EXECUTE stmt;
				set countRow = (select ROW_COUNT());
				DEALLOCATE PREPARE stmt;

				if countRow <=0 then
					set Message = 'Error On Cheque Details Update.';
					rollback;
					leave sp_Collection_Set;
				End if;
             elseif @flag = 'n' then
				set Query_Insert = '';
				set @Insert_query = '';
				set Query_Insert = concat('insert into fet_trn_tfetcollectionchq (fetcollectionchq_fetcollectionheadergid,fetcollectionchq_chqno,
						fetcollectionchq_chqdate,fetcollectionchq_chqamt,fetcollectionchq_bankname,entity_gid,create_by)
						values(',li_coll_gid,',''',@Cheque_No,''',''',@Cheque_Date,''',''',@Cheque_Amount,''',''',@Bank_Name,''',
						',li_Entity_gid,',',ls_create_by,'
						)');

				set @Insert_query = Query_Insert;
				#SELECT @Insert_query;
				PREPARE stmt FROM @Insert_query;
				EXECUTE stmt;
				set countRow = (select ROW_COUNT());
				DEALLOCATE PREPARE stmt;
            select last_insert_id();
				if countRow <=0 then
					set Message = 'Error On Cheque Details Insert.';
					rollback;
					leave sp_Collection_Set;
				End if;
			end if;
             set i = i + 1;

		END While;

        End if;
    End if;
    set Message = CONCAT('SUCCESS');
    commit;
end if;
### Multiple Update of the Collection.
 if Action = 'Update' and Type = 'MULTIPLE_UPDATE' then

						select JSON_LENGTH(lj_Cheque,'$') into @li_json_Cltn_count;
						if @li_json_Cltn_count = 0 or @li_json_Cltn_count is null then
								Set Message = 'No Data In JSON-To Update.';
								leave sp_Collection_Set;
						End if;

			select JSON_UNQUOTE(JSON_EXTRACT(lj_Cheque, CONCAT('$.COLLECTION[0].Status[0]'))) into @lsStatus;

                if @lsStatus is null or @lsStatus = '' then
								Set Message = 'No Data In JSON Status -To Update.';
								leave sp_Collection_Set;
                End if;

                 select JSON_LENGTH(lj_Cheque, CONCAT('$.COLLECTION[0].Collection_Gid')) into @Collection_GidCount;

                 if @Collection_GidCount = 0 or @Collection_GidCount = '' then
						set Message = 'No Collection Gid In JSON -Data.';
                        Leave sp_Collection_Set;
                 End if;

				set j = 0;

                While j <= @Collection_GidCount -1 Do
								select JSON_UNQUOTE(JSON_EXTRACT(lj_Cheque, CONCAT('$.COLLECTION[0].Collection_Gid[',j,']'))) into @Collection_Gid;
                                select JSON_UNQUOTE(JSON_EXTRACT(lj_Cheque, CONCAT('$.COLLECTION[0].Collection_Dispatch_Gid[0]'))) into @Collection_Dispatch_Gid;
                                select JSON_UNQUOTE(JSON_EXTRACT(lj_Cheque, CONCAT('$.COLLECTION[0].Collection_HODispatch_Gid[0]'))) into @Collection_HODispatch_Gid;

                                set Query_Update = '';
                                set Query_Update = concat('Update fet_trn_tfetcollectionheader set fetcollectionheader_status = ''',@lsStatus,''',Update_date = current_timestamp() ,');

																					if @Collection_Dispatch_Gid is not null and @Collection_Dispatch_Gid >  0 then
																								set Query_Update = concat(Query_Update,'fetcollectionheader_dispatchgid = ',@Collection_Dispatch_Gid,', ');
                                                                                    End if;
																					if @Collection_HODispatch_Gid is not null and @Collection_HODispatch_Gid >  0 then
																								set Query_Update = concat(Query_Update,'fetcollectionheader_hodispatchgid = ',@Collection_HODispatch_Gid,', ');
                                                                                    End if;

																	set  Query_Update = concat(Query_Update,'update_by = ',ls_create_by,'
																where fetcollectionheader_gid = ''',@Collection_Gid,''' '
                                                                );

																set @Query_Update = '';
																set @Query_Update = Query_Update;

																PREPARE stmt FROM @Query_Update;
																EXECUTE stmt;
																set countRow = (select ROW_COUNT());
																DEALLOCATE PREPARE stmt;


																		if countRow <= 0 then
																				set Message = 'Error On Collection Status Update.';
																				rollback;
																				leave sp_Collection_Set;
																		elseif    countRow > 0 then
																				set Message = 'SUCCESS';

                                                                                 #### Tran Update.
																				 if @lsStatus <> '' and @lsStatus is not null then
																				   call sp_Trans_Set('update','COLLECTION_RECEIPT',@Collection_Gid,@lsStatus,'I','CHECKER','STATUS',li_Entity_gid,ls_create_by,@message);
																					select @message into @out_msg_tran ;

																								if @out_msg_tran = 'FAIL' then
																									set Message = 'Failed On Tran Update';
																										rollback;
																										leave sp_Collection_Set;
																								End if;
																				 End if;

																		End if;


						set j = j + 1;
                End While;
                commit;

 elseif Action='Update' and Type='RECEIPT_CANCEL' then

            if li_coll_gid ='' then
                set Message ='Collection Gid Is Not Given';
                leave sp_Collection_Set;
			end if;

            if ld_coll_amount ='' then
                set Message ='Collection Amount Is Not Given';
                leave sp_Collection_Set;
			end if;

            select fetcollectionheader_balanceamt,fetcollectionheader_amount into @Balance,@Amount from fet_trn_tfetcollectionheader where fetcollectionheader_gid=li_coll_gid;
            set Balance =@Balance+ld_coll_amount;

            if Balance < @Amount then
                    set  Query_Update = Concat('update fet_trn_tfetcollectionheader set  fetcollectionheader_balanceamt=',Balance,',update_by = ',ls_create_by,
																		',update_date = now() where fetcollectionheader_gid=',li_coll_gid,'');

					set @Query_Update = '';
					set @Query_Update = Query_Update;

					PREPARE stmt FROM @Query_Update;
					EXECUTE stmt;
					set countRow = (select ROW_COUNT());
					DEALLOCATE PREPARE stmt;
                    if countRow > 0 then
							set Message = 'SUCCESS';
					else
						   set Message ='FAIL';
						   rollback;
						   leave sp_Collection_Set;
					end if;
            end if;

 elseif Action='Update' and Type='COLLECTION_DELETE' then

                        if li_coll_gid  = 0 then
								set Message = 'Collection Gid Is Needed.';
                                leave sp_Collection_Set;
                        End if;

                        set @fetcollectionheader_gid = 0 ;
				   Select a.fetcollectionheader_gid into @fetcollectionheader_gid
                   from fet_trn_tfetcollectionheader as a
					where a.fetcollectionheader_status = 'RECEIVED'
					and fetcollectionheader_isactive = 'Y' and a.fetcollectionheader_isremoved = 'N'
					and a.fetcollectionheader_gid = li_coll_gid ;

                    if @fetcollectionheader_gid = 0 then
                        set Message = 'This Collection Cannot Be Deleted.';
                        leave sp_Collection_Set;
                    End if;

                    set Query_Update = '';
                    set Query_Update = concat('
							Update fet_trn_tfetcollectionheader set fetcollectionheader_isremoved = ''Y'' , fetcollectionheader_isactive = ''N'' ,
                            update_by = ',ls_create_by,',Update_date = current_timestamp()
							where fetcollectionheader_gid = ',@fetcollectionheader_gid,'
                    ');

													set @Query_Update = '';
																set @Query_Update = Query_Update;
                                                              # select Query_Update;
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
                                              End if;


 End if;



END