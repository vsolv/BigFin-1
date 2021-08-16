CREATE DEFINER=`developer`@`%` PROCEDURE `galley`.`sp_FA_TFR_Asset_Set`(IN `ls_Action` varchar(32),
IN `ls_Type` varchar(32),IN `ls_Sub_Type` varchar(32),IN `lj_Details` json,IN `lj_Classification` json,
IN `ls_Createby` varchar(32),OUT `Message` varchar(1024))
sp_FA_TFR_Asset_Set:BEGIN

#### Bala Oct 16 2019
### Ramesh Edit Nov 7 2019
Declare errno int;
Declare msg varchar(1000);
Declare countRow int;
Declare Query_Update varchar(9000);
Declare Query_Insert varchar(9000);
Declare Query_Column varchar(9000);

DECLARE EXIT HANDLER FOR SQLEXCEPTION,sqlwarning

	 BEGIN
		GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
		set Message = concat(errno , msg);
		ROLLBACK;
     END;

	select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid[0]'))) into @Entity_Gid;

             if @Entity_Gid is  null or @Entity_Gid = 0 or @Entity_Gid = '' then
					set Message = 'Entity Gid Is Needed.';
                    leave sp_FA_TFR_Asset_Set;
             End if;

if ls_Type = 'TFR_MAKER' and  ls_Sub_Type = 'TRAN' then
      if ls_Action = 'INSERT' then

                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_TFR_To'))) into @Asset_TFR_To;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_TFR_Reason'))) into @Asset_TFR_Reason;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_Detail_Gids'))) into @Asset_Detail_Gids;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_TFR_DATE'))) into @Asset_TFR_DATE;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.AssetDetails_Location_Gid'))) into @AssetDetails_Location_Gid;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_TFR_BS'))) into @Asset_TFR_BS;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_TFR_CC'))) into @Asset_TFR_CC;

                   if @Asset_TFR_To is null or @Asset_TFR_To = '' then
						set Message = 'Asset_TFR_To Is Needed.';
						leave sp_FA_TFR_Asset_Set;
					End if;

					if @Asset_TFR_Reason is null or @Asset_TFR_Reason = '' then
						set Message = 'Asset Transfer Reason Is Needed.';
						leave sp_FA_TFR_Asset_Set;
					End if;

					if @Asset_Detail_Gids is null or @Asset_Detail_Gids = '' then
						set Message = 'Asset_Detail_Gids Is Needed.';
						leave sp_FA_TFR_Asset_Set;
					End if;

				    if @Asset_TFR_BS is null or @Asset_TFR_BS = '' THEN
				      set Message = 'Asset Transfer BS Is Needed.';
				      leave sp_FA_TFR_Asset_Set;
				    End if;

				    if @Asset_TFR_CC is null or @Asset_TFR_CC = '' THEN
				      set Message  = 'Asset Transfer CC Is Needed.';
				      leave sp_FA_TFR_Asset_Set;
				    End if;


                    set @ls_Status = 'IN_ACTIVE';
                    set @ls_Request_For = 'TRANSFER';
                    set @ls_Request_Status = 'SUBMITTED';
                    set @New_Asset_Id = '';


					#call sp_Auto_Incrementer('next', @out_number);
                    #select @out_number into @increment;
                     #select @out_number;

                    #select MAX(assetdetails_id)+@increment into @New_Asset_Id from fa_tmp_tassetdetails;
                    ##### Creation Of New Asset
                     #select @New_Asset_Id,@ls_Status,@ls_Request_For,@ls_Request_Status,@Asset_TFR_To,
                     #@AssetDetails_Location_Gid,@Asset_Detail_Gids;

                     select assetdetails_id into @Asset_Id
								from fa_trn_tassetdetails  where
										assetdetails_gid in (@Asset_Detail_Gids) and assetdetails_isactive='Y'
											and assetdetails_isremoved='N';

                         select concat('',@Asset_Id,'')  like concat('%-%') into @Test;
								#select @Asset_Id,@Test,@Asset_Detail_Gids;
                                set Query_Column='';
                                if @Test=0 then
								    set Query_Column=concat('assetdetails_id');
                                elseif @Test=1 then
									set Query_Column=(SUBSTRING_INDEX(@Asset_Id ,'-', 1))  ;
                                end if;
                               #select Query_Column;

                    set Query_Insert = '';
						 set Query_Insert = concat('
						  INSERT INTO fa_tmp_tassetdetails
							(assetdetails_id,assetdetails_qty,assetdetails_barcode,assetdetails_date,assetdetails_assetgroupid,
                            assetdetails_assetcatgid,assetdetails_cat,assetdetails_subcat,assetdetails_productgid,assetdetails_value,
                            assetdetails_cost,assetdetails_description,assetdetails_capdate,assetdetails_source,assetdetails_status,
                            assetdetails_requestfor,assetdetails_requeststatus,assetdetails_assettfrgid,assetdetails_assetsalegid,
                            assetdetails_not5k,assetdetails_assetowner,assetdetails_lease_startdate,assetdetails_lease_enddate,
                            assetdetails_impairassetgid,assetdetails_impairasset,assetdetails_writeoffgid,assetdetails_assetcatchangegid,
                            assetdetails_assetvaluegid,assetdetails_assetcapdategid,assetdetails_assetsplitgid,assetdetails_assetmergegid,
                            assetdetails_assetcatchangedate,assetdetails_reducedvalue,assetdetails_branchgid,assetdetails_bs,assetdetails_cc,assetdetails_deponhold,
                            assetdetails_deprate,assetdetails_parentgid,assetdetails_assetserialno,assetdetails_invoicegid,
							assetdetails_inwheadergid,assetdetails_inwdetailgid,assetdetails_inwarddate,assetdetails_mepno,assetdetails_ponum,
                            assetdetails_crnum,assetdetails_imagepath,assetdetails_vendorname,assetdetails_mainassetdetailsgid,assetdetails_isactive,
                            assetdetails_isremoved,entity_gid,create_by,assetdetails_assetlocationgid)
								(select ',Query_Column,',assetdetails_qty,assetdetails_barcode,assetdetails_date,assetdetails_assetgroupid,
                                assetdetails_assetcatgid,assetdetails_cat,assetdetails_subcat,assetdetails_productgid,assetdetails_value,
                                assetdetails_cost,assetdetails_description,assetdetails_capdate,assetdetails_source,''',@ls_Status,''',
                                ''',@ls_Request_For,''',''',@ls_Request_Status,''',assetdetails_assettfrgid,assetdetails_assetsalegid,
                                assetdetails_not5k,assetdetails_assetowner,assetdetails_lease_startdate,assetdetails_lease_enddate,
                                assetdetails_impairassetgid,assetdetails_impairasset,assetdetails_writeoffgid,assetdetails_assetcatchangegid,
                                assetdetails_assetvaluegid,assetdetails_assetcapdategid,assetdetails_assetsplitgid,assetdetails_assetmergegid,
                                assetdetails_assetcatchangedate,assetdetails_reducedvalue,''',@Asset_TFR_To,''',''',@Asset_TFR_BS,''',''',@Asset_TFR_BS,''',assetdetails_deponhold,
                                assetdetails_deprate,assetdetails_parentgid,assetdetails_assetserialno,assetdetails_invoicegid,
                                assetdetails_inwheadergid,assetdetails_inwdetailgid,assetdetails_inwarddate,assetdetails_mepno,
								assetdetails_ponum,assetdetails_crnum,assetdetails_imagepath,assetdetails_vendorname,assetdetails_gid,
                                assetdetails_isactive,assetdetails_isremoved,entity_gid,create_by,',@AssetDetails_Location_Gid,'
								from fa_trn_tassetdetails  where assetdetails_gid in (',@Asset_Detail_Gids,')
								)
						 ');

								set @Insert_query = Query_Insert;
							#	SELECT @Insert_query;
								PREPARE stmt FROM @Insert_query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;

                              if countRow > 0 then
									set Message = 'SUCCESS';
                                    select LAST_INSERT_ID() into @New_Asset_Id;
                               else
                                    set Message = 'FAIL';
                              End if;



			set @ls_Status = 'SUBMITTED';



					set Query_Insert = '';
					set Query_Insert = concat('
							INSERT INTO fa_trn_tassettfr
									(assettfr_assetdetailsid, assettfr_date,
                                     assettfr_from, assettfr_to,
                                     assettfr_status, assettfr_reason,
                                     assettfr_value, assettfr_newassetdetailsid,
                                     entity_gid,create_by)
							(select ',Query_Column,',''',@Asset_TFR_DATE,''',
									assetdetails_branchgid,''',@Asset_TFR_To,''',
									''',@ls_Status,''',''',@Asset_TFR_Reason,''',
									assetdetails_value,''',@New_Asset_Id,''',
                                    entity_gid,''',ls_Createby,'''
							from fa_trn_tassetdetails
							where assetdetails_gid in (',@Asset_Detail_Gids,')
								 )');

							set @Insert_query = Query_Insert;
							#SELECT @Insert_query;
							PREPARE stmt FROM @Insert_query;
							EXECUTE stmt;
							set countRow = (select ROW_COUNT());
							DEALLOCATE PREPARE stmt;

                              if countRow > 0 then
                                  select LAST_INSERT_ID() into @Asset_TFR_Maxgid ;

                                  #### Update im Tmp Table
                                  set sql_safe_updates = 0;
                                  Update fa_tmp_tassetdetails set assetdetails_assettfrgid = @Asset_TFR_Maxgid
                                  where assetdetails_mainassetdetailsgid = @Asset_Detail_Gids;

                                  set countRow = (select ROW_COUNT());

										if  countRow <= 0 then
											set Message = 'FAIL On Asset Temp Data Update.';
                                            leave sp_FA_TFR_Asset_Set;
                                        End if;


									set Message = 'SUCCESS';

						call sp_Trans_Set('Insert','FA_TRANSFER',@Asset_TFR_Maxgid,'NEW',
										  'G','MAKER',@Asset_TFR_Reason,@Entity_Gid,ls_Createby,@message);
									select @message into @tran;
									#select @message; #remove it
									if @tran <>0 or @tran <> '' then
											set Message = 'SUCCESS';
									else
											set Message = 'FAIL in tran';
											leave sp_FA_TFR_Asset_Set;
									end if;
                               else
                                    set Message = 'FAIL';
                              End if;

      End if;


  elseif ls_Type = 'TFR_CHECKER' and  ls_Sub_Type = 'TRANSFER' then
         if ls_Action = 'UPDATE' then

				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_TFR_Gid'))) into @Asset_TFR_Gid;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_Detail_Gids'))) into @Asset_Detail_Gids;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_TFR_Status'))) into @Asset_TFR_Status;

                #select  @Asset_TFR_Gid,'trf';
                #select  @Asset_Detail_Gids;



                if @Asset_TFR_Gid is null or cast(@Asset_TFR_Gid as decimal(16,2))  = 0 then
						set Message = 'Asset_TFR_Gid Is Needed.';
                        leave sp_FA_TFR_Asset_Set;
                End if;

                if @Asset_TFR_Status is null or @Asset_TFR_Status = '' then
						set Message = 'Asset_TFR_Status Is Needed.';
                        leave sp_FA_TFR_Asset_Set;
                End if;


		if @Asset_TFR_Status='APPROVED' then

                /*select assetdetails_id into  @AssetDetails_Id
                from fa_trn_tassetdetails where
                assetdetails_isactive='Y' and assetdetails_isremoved='N' and
                assetdetails_gid in (@Asset_Tran_Gid);

			   select ('',@AssetDetails_Id,'')  like '%-%' into @test;

               if @test=1 then
				    SELECT (SUBSTRING_INDEX(@AssetDetails_Id ,'-', -1)) into @AssetDetails_Id1 ;
                    set @AssetDetails_Id1=@AssetDetails_Id1+1;

               elseif @test=0 then
					   set @Asset_Detail_Gids=concat(@Asset_Detail_Gids,'-',1);
               end if;*/
               ###To DO IN_ACTIVE is not Affect in fa_trn_tassetdetails when APPROVED TRNFR


               Select assetdetails_mainassetdetailsgid into @TRF_Gid 	from fa_tmp_tassetdetails
					  where assetdetails_isactive='Y' and assetdetails_isremoved='N'
                      and assetdetails_gid=@Asset_Detail_Gids;

                select assetdetails_id into  @AssetDetails_Id
                from fa_trn_tassetdetails where
                assetdetails_isactive='Y' and assetdetails_isremoved='N' and
                assetdetails_gid in (@TRF_Gid);

               select ifnull(max(assetdetails_id),0)
					  from fa_trn_tassetdetails where assetdetails_id like  concat('%',@AssetDetails_Id,'-%') into @test;

               if @test<>0 and @test is not null then
				    SELECT (SUBSTRING_INDEX(@test ,'-', -1)) into @AssetDetails_Id1 ;
				    SELECT (SUBSTRING_INDEX(@test ,'-', 1)) into @AssetDetails_Id2 ;
                    set @AssetDetails_Id1=@AssetDetails_Id1+1;
                    set @AssetDetails_Id=concat(@AssetDetails_Id2,'-',@AssetDetails_Id1);
               elseif @test=0 then
					set @AssetDetails_Id=concat(@AssetDetails_Id,'-',1);
               end if;
				#select @AssetDdetails_Id,'TEST';
				#select @AssetDetails_Id2,'TEST';
				#select @AssetDetails_Id,'TEST',@test;
				#select @TRF_Gid,@test,@AssetDetails_Id1,@AssetDetails_Id;
              ##########---------------
			SET SQL_SAFE_UPDATES = 0;
			set Query_Update = '';
			set Query_Update = concat('update fa_trn_tassetdetails
										set
											update_date=now(),
											update_by=',ls_Createby,',
                                            assetdetails_requeststatus = ''APPROVED'',
                                            assetdetails_id=''',@AssetDetails_Id,'''
										where assetdetails_gid in (',@TRF_Gid,')
									');

			set @Update_query = '';
			set @Update_query = Query_Update;
			#SELECT @Update_query,'update';
			PREPARE stmt FROM @Update_query;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;

			if countRow > 0 then
					set Message = 'SUCCESS';
			elseif countRow<=0 then
					set Message = 'FAIL In Asset_Details';
			End if;



                select assetdetails_id into @Trn_Asset_id
						from fa_trn_tassetdetails order by assetdetails_gid desc limit 1;

							#select @Trn_Asset_id;
							#select @Asset_Detail_Gids;

						 set @AssetDetails_Status='ACTIVE';
						 set @Request_Status='APPROVED';
                         set @RequestFor='';
						 set Query_Insert = '';
						 set Query_Insert = concat('
						  INSERT INTO fa_trn_tassetdetails
							(assetdetails_id,assetdetails_qty,assetdetails_barcode,assetdetails_date,assetdetails_assetgroupid,
                            assetdetails_assetcatgid,assetdetails_cat,assetdetails_subcat,assetdetails_productgid,assetdetails_value,
                            assetdetails_cost,assetdetails_description,assetdetails_capdate,assetdetails_source,assetdetails_status,
                            assetdetails_requestfor,assetdetails_requeststatus,assetdetails_assettfrgid,assetdetails_assetsalegid,
                            assetdetails_not5k,assetdetails_assetowner,assetdetails_lease_startdate,assetdetails_lease_enddate,
                            assetdetails_impairassetgid,assetdetails_impairasset,assetdetails_writeoffgid,assetdetails_assetcatchangegid,
                            assetdetails_assetvaluegid,assetdetails_assetcapdategid,assetdetails_assetsplitgid,assetdetails_assetmergegid,
                            assetdetails_assetcatchangedate,assetdetails_reducedvalue,assetdetails_branchgid,assetdetails_bs,assetdetails_cc,assetdetails_deponhold,
                            assetdetails_deprate,assetdetails_parentgid,assetdetails_assetserialno,assetdetails_invoicegid,
							assetdetails_inwheadergid,assetdetails_inwdetailgid,assetdetails_inwarddate,assetdetails_mepno,assetdetails_ponum,
                            assetdetails_crnum,assetdetails_imagepath,assetdetails_vendorname,assetdetails_isactive,
                            assetdetails_isremoved,entity_gid,create_by,assetdetails_assetlocationgid)
								(select assetdetails_id,assetdetails_qty,assetdetails_barcode,assetdetails_date,assetdetails_assetgroupid,
                                assetdetails_assetcatgid,assetdetails_cat,assetdetails_subcat,assetdetails_productgid,assetdetails_value,
                                assetdetails_cost,assetdetails_description,assetdetails_capdate,assetdetails_source,''',@AssetDetails_Status,''',
                                ''',@RequestFor,''', ''',@Request_Status,''',assetdetails_assettfrgid,assetdetails_assetsalegid,
                                assetdetails_not5k,assetdetails_assetowner,assetdetails_lease_startdate,assetdetails_lease_enddate,
                                assetdetails_impairassetgid,assetdetails_impairasset,assetdetails_writeoffgid,assetdetails_assetcatchangegid,
                                assetdetails_assetvaluegid,assetdetails_assetcapdategid,assetdetails_assetsplitgid,assetdetails_assetmergegid,
                                assetdetails_assetcatchangedate,assetdetails_reducedvalue,assetdetails_branchgid,assetdetails_bs,assetdetails_cc,assetdetails_deponhold,
                                assetdetails_deprate,assetdetails_parentgid,assetdetails_assetserialno,assetdetails_invoicegid,
                                assetdetails_inwheadergid,assetdetails_inwdetailgid,assetdetails_inwarddate,assetdetails_mepno,
								assetdetails_ponum,assetdetails_crnum,assetdetails_imagepath,assetdetails_vendorname,
                                assetdetails_isactive,assetdetails_isremoved,entity_gid,create_by,assetdetails_assetlocationgid
								from fa_tmp_tassetdetails  where assetdetails_gid in (',@Asset_Detail_Gids,')
                                )
						 ');

							set @Insert_query = Query_Insert;
							#SELECT @Insert_query;
							PREPARE stmt FROM @Insert_query;
							EXECUTE stmt;
							set countRow = (select ROW_COUNT());
							#select countRow;
							DEALLOCATE PREPARE stmt;

						    if countRow > 0 then
								set Message = 'SUCCESS';
								select LAST_INSERT_ID() into @New_Asset_Id;
						    else
								set Message = 'FAIL';
						    End if;




			   set Query_Update = '';
               set Query_Update = concat('Update fa_trn_tassettfr
											  set assettfr_status = ''',@Asset_TFR_Status,''',
                                                  assettfr_assetdetailsid=''',@AssetDetails_Id,''',
												  update_by = ''',ls_Createby,''' ,
                                                  update_date = current_timestamp()
											  Where assettfr_gid = ',@Asset_TFR_Gid,'
												  and entity_gid = ',@Entity_Gid,'
												');

									set @Query_Update = '';
								    set @Query_Update = Query_Update;
								 #    select @Query_Update; ### Remove IT
									PREPARE stmt FROM @Query_Update;
									EXECUTE stmt;
									set countRow = (select ROW_COUNT());
									DEALLOCATE PREPARE stmt;

									if countRow <= 0 then
										set Message = 'Error On TFR Asset Update.';
										leave sp_FA_TFR_Asset_Set;
									 elseif    countRow > 0 then
										set Message = 'SUCCESS';
									End if;

         elseif  @Asset_TFR_Status='REJECTED' then

					set Query_Update = '';
               set Query_Update = concat('Update fa_trn_tassettfr
											  set assettfr_status = ''',@Asset_TFR_Status,''' ,
												  update_by = ''',ls_Createby,''' ,
                                                  update_date = current_timestamp()
											  Where assettfr_gid = ',@Asset_TFR_Gid,'
												  and entity_gid = ',@Entity_Gid,'
												');

									set @Query_Update = '';
								    set @Query_Update = Query_Update;
								    # select @Query_Update; ### Remove IT
									PREPARE stmt FROM @Query_Update;
									EXECUTE stmt;
									set countRow = (select ROW_COUNT());
									DEALLOCATE PREPARE stmt;

									if countRow <= 0 then
										set Message = 'Error On TFR Asset Update.';
										leave sp_FA_TFR_Asset_Set;
									 elseif    countRow > 0 then
										set Message = 'SUCCESS';
									End if;
		  End if;#######APPROVE AND REJECED END IF
End if; #UPADET END IF
End if; #MAIN END IF


END