CREATE DEFINER=`root`@`%` PROCEDURE `sp_Collection_Get`(IN `ls_Action` varchar(64),IN `ls_Type` varchar(64),
IN `li_collect_gid` int,IN `ls_collect_name` varchar(64),
IN `ls_collect_date` varchar(16),IN `lj_Filters` json,IN `lj_classification` JSON,OUT `Message` varchar(5000))
coll_get:BEGIN

#Vigneshwari       07-03-2018
# Ramesh Edit Nov 2018 : API: MAPP :: Dec   , Feb 2019, May 2019
# Prakash Edit 27-11-2018
## Ramesh : New : Fet Review
# karthiga edit :COLLECTION_INHAND-PENDING

declare collect_srch text;
declare query_srch varchar(1000);
declare query_srch1 varchar(1000);
declare query_srch2 varchar(1000);
declare ls_error varchar(100);
declare j int;
declare entity_gid varchar(64);
declare client_gid varchar(64);
Declare Query_Select varchar(3000);
declare li_count int;
declare Query_Column varchar(1024);
declare Query_Where varchar(10000);

set query_srch = '';

select JSON_LENGTH(lj_classification, '$') into @li_jsonclass_count;
#select @li_jsonclass_count;

if @li_jsonclass_count <=0 then
	set Message = 'Entity Gid or Client Gid Not Given';
    leave coll_get;
end if;


set j = 0 ;

    select JSON_LENGTH(lj_classification, CONCAT('$.Entity_Gid')) into @entity_cnt;

    if @entity_cnt <> 0 then
		WHILE j<= @entity_cnt - 1 Do

            select  JSON_EXTRACT(lj_classification, CONCAT('$.Entity_Gid[',j,']')) into @entity_gid;
            if @entity_cnt  <> '' then
				 if @entity_gid <> 0 then
					if entity_gid <> '' then
						set entity_gid = concat(entity_gid,',',@entity_gid);
					else
                        set entity_gid = @entity_gid;
                    end if;

				end if;

			end if;
            set j = j + 1;

        END WHILE;
    end if;

#select entity_gid  ;#REGEXP '^[0-9]|[,]+$';
select JSON_EXTRACT(lj_classification, CONCAT('$.Client_Gid[0]')) into @client_gid;

set j = 0 ;
    select  JSON_LENGTH(lj_classification, CONCAT('$.Client_Gid')) into @client_cnt;
    if @client_cnt <> 0 then
		WHILE j<= @client_cnt - 1 Do

            select  JSON_EXTRACT(lj_classification, CONCAT('$.Client_Gid[',j,']')) into @client_gid;
            if @client_cnt  <> '' then
				 if @client_gid <> 0 then
					if client_gid <> '' then
						set client_gid = concat(client_gid,',',@client_gid);
					else
                        set client_gid = @client_gid;
                    end if;

				end if;

			end if;
            set j = j + 1;

        END WHILE;
    else
		set client_gid = '';
    end if;
#select client_gid;

if ls_Action = 'COLLECTION' and ls_Type = 'SUMMARY' then
              #Edit 27-11-2018
				select JSON_LENGTH(lj_Filters,'$') into @li_json_count;

                if  @li_json_count <=0  then
					set Message = 'No Data in Json Object';
					leave coll_get;
				end if;

						select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.CustGroup_Gid'))) into @CustGroup_Gid;
						select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Customer_Name '))) into @CustGroup_Name;
						select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Cheque_From_Date'))) into @Chq_from_date;
                        select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Cheque_To_date'))) into @Chq_to_date;
                        select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Status'))) into @chq_status;
                        select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Cheque_No'))) into @chq_no;
                        select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Cheque_Amount'))) into @Cheque_Amount;
                        select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Courier_Name'))) into @Courier_name;
                        select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.AWB_no'))) into @AWB_no;
						select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.CollectionLimit'))) into @CollectionLimit;

                        select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Collection_From_Date'))) into @Collection_From_Date;
                        select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Collection_To_Date'))) into @Collection_To_Date;
                        select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Deposit_From_Date'))) into @Deposit_From_Date;
                        select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Deposit_To_Date'))) into @Deposit_To_Date;
                        select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Clear_From_Date'))) into @Clear_From_Date;
                        select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Clear_To_Date'))) into @Clear_To_Date;

								if client_gid <> '' then
									set @clientgid = concat(' and customergroup_clientgid in (',client_gid,')');
								end if;

								if li_collect_gid <> 0 then
									set query_srch = concat(query_srch,' and fetcollectionheader_gid = ',li_collect_gid)	;
								end if;

								if @CustGroup_Name <> '' then
									set query_srch =concat(query_srch,' and customergroup_name like  ''%',@CustGroup_Name, '%''');
								end if;

								if @CustGroup_Gid <> '0' and @CustGroup_Gid <> '' and  @CustGroup_Gid >  0  then
									set query_srch =concat(query_srch,' and customergroup_gid =''',@CustGroup_Gid,'''');
								end if;

							if @Chq_from_date <> '' then
                                  if  @Chq_to_date <> '' then
										set query_srch = concat(query_srch,' and date_format(fetcollectionheader_chequedate, ''%Y-%m-%d'') between ''',@Chq_from_date,''' and ''',@Chq_to_date,'''');
									else
										set query_srch = concat(query_srch,' and date_format(fetcollectionheader_chequedate, ''%Y-%m-%d'') between ''',@Chq_from_date,''' and curdate()');
								end if;
							end if;

							if @chq_status <> '' then
									set query_srch = concat(query_srch,' and fetcollectionheader_status=''',@chq_status,'''');
							end if ;

							if @chq_no <> 0 then
									set query_srch = concat(query_srch,' and fetcollectionheader_chequeno=''',@chq_no,'''');
							end if ;

                            if @Cheque_Amount <> 0 then
									set query_srch = concat(query_srch,' and  fetcollectionheader_amount = ''',@Cheque_Amount,''' ');
							End if;

							if @Courier_name <> '' then
									set query_srch = concat(query_srch,' and courier_name=''',@Courier_name,'''');
							end if ;

							if @AWB_no <> '' then
									set query_srch = concat(query_srch,' and dispatch_awbno=''',@AWB_no,'''');
							end if ;

							select ref_gid into @ref from gal_mst_tref where ref_name='COLLECTION_RECEIPT';

							if @Collection_From_Date <> '' and @Collection_To_Date <>'' and @Collection_From_Date is not null and @Collection_To_Date is not null then

									set query_srch = concat(query_srch,'and date_format(fetcollectionheader_date, ''%Y-%m-%d'') between ''',@Collection_From_Date,''' and ''',@Collection_To_Date,'''
																');
									else
									set query_srch=concat(query_srch,'');
							end if;

                            if @Deposit_From_Date <> ''  then
                                  if  @Deposit_To_Date <> '' then
                            # and @Deposit_To_Date<>'' and @Deposit_From_Date is not null and @Deposit_To_Date is not null
									set query_srch = concat(query_srch,' and date_format(tran_fromdate, ''%Y-%m-%d'') between ''',@Deposit_From_Date,''' and ''',@Deposit_To_Date,'''
																		 and tran_status=''DEPOSITED'' ');
									else
									set query_srch = concat(query_srch,'and date_format(tran_fromdate, ''%Y-%m-%d'') between ''' ''' and ''' ''' ');
								end if;
							end if;

                            if @Clear_From_Date <> ''  then
                                  if  @Clear_To_Date <> '' then
                              #and @Clear_To_Date<>'' and @Clear_From_Date is not null and @Clear_To_Date is not null
									set query_srch = concat(query_srch,' and date_format(tran_fromdate, ''%Y-%m-%d'') between ''',@Clear_From_Date,''' and ''',@Clear_To_Date,'''
																		and tran_status=''CLEARED'' ');
									else
									set query_srch = concat(query_srch,'and date_format(tran_fromdate, ''%Y-%m-%d'') between ''' ''' and ''' ''' ');
								end if;
							end if;
                           # select query_srch;

                           /* if @Deposit_From_Date <> '' and @Deposit_To_Date <>'' and @Deposit_From_Date is not null and @Deposit_To_Date is not null then

											set query_srch1 = concat(query_srch1,'select * from gal_trn_ttran where tran_ref_gid = ',@ref,' and tran_status=''DEPOSITED'' and date_format(tran_fromdate, ''%Y-%m-%d'') between ''',@Deposit_From_Date,''' and ''',@Deposit_To_Date,'''
                                             ');
									else

											set query_srch1 = concat(query_srch1,'select * from gal_trn_ttran where tran_ref_gid = ',@ref,' and tran_status=''DEPOSITED''
                                            and date_format(tran_fromdate, ''%Y-%m-%d'') between ''' ''' and ''' ''' ');
									end if;


                            if @Clear_From_Date <> '' and @Clear_To_Date<>''and @Clear_From_Date is not null and @Clear_To_Date is not null then

											set query_srch2 = concat(query_srch2,'select * from gal_trn_ttran where tran_ref_gid = ',@ref,' and tran_status=''CLEARED'' and date_format(tran_fromdate, ''%Y-%m-%d'') between ''',@Clear_From_Date,''' and ''',@Clear_To_Date,'''
                                             ');
									else
											set query_srch2 = concat(query_srch2,'select * from gal_trn_ttran where tran_ref_gid = ',@ref,' and tran_status=''CLEARED'' and date_format(tran_fromdate, ''%Y-%m-%d'') between ''' ''' and ''' ''' ');
									end if;*/

							# select query_srch1;
                             #select query_srch2;

                            /*(select * from gal_trn_ttran where tran_ref_gid = 38 and tran_status='DEPOSITED' and
                                              date_format(tran_fromdate, '%Y-%m-%d') between '2019-08-01' and '2019-09-21') as tranDEPO

                                     on tranDEPO.tran_reftable_gid = a.fetcollectionheader_gid
                                    left join  (select * from gal_trn_ttran where tran_ref_gid = 38 and tran_status='CLEARED' and
                                              date_format(tran_fromdate, '%Y-%m-%d') between '2019-08-01' and '2019-09-21') as tranCLEAR

                                     on tranCLEAR.tran_reftable_gid = a.fetcollectionheader_gid */

							set @ls_count = 0 ;
                            set @ls_count = 123 ;

								set Query_Column = concat('SELECT distinct file_name,file_path,fetcollectionheader_customergroup_gid,fetcollectionheader_gid,fetcollectionheader_filegid,
									DATE_FORMAT(fetcollectionheader_date,''%d-%b-%Y'') as fetcollectionheader_date,
									fetcollectionheader_amount,fetcollectionheader_mode,ifnull(fetcollectionheader_chequeno,''0'') as fetcollectionheader_chequeno,
									DATE_FORMAT(fetcollectionheader_chequedate,''%d-%b-%Y'') as fetcollectionheader_chequedate,
									ifnull(bank_name,''-'') as bank_name,fetcollectionheader_status,
                                    c.customergroup_name,ifnull(e.courier_gid,0) as courier_gid,ifnull(e.courier_name,0) as courier_name,ifnull(d.dispatch_awbno,0) as dispatch_awbno
                                    ,@ls_count');
							    set Query_Where = concat(' FROM fet_trn_tfetcollectionheader as a
                                    left join gal_trn_ttran as tt on tt.tran_reftable_gid = a.fetcollectionheader_gid and tt.tran_ref_gid = ',@ref,'
									left join gal_mst_tcustomergroup as c on c.customergroup_gid=fetcollectionheader_customergroup_gid and customergroup_isremoved=''N''
                                    left join dis_trn_tdispatch as d on d.dispatch_gid=a.fetcollectionheader_dispatchgid and dispatch_isremoved=''N''
                                    left join dis_mst_tcourier as e on e.courier_gid=d.dispatch_courier_gid and courier_isremoved=''N''
                                    left join gal_mst_tbank on bank_gid = fetcollectionheader_bankgid and bank_isactive = ''Y'' and bank_isremoved = ''N''

                                   left join gal_mst_tfile on file_gid=fetcollectionheader_filegid and file_isactive=''Y'' and file_isremoved=''N''

                                   where fetcollectionheader_isactive = ''Y'' and fetcollectionheader_isremoved = ''N''
                                    and a.entity_gid in ( ',entity_gid,')
                                   ',query_srch,' order by fetcollectionheader_gid desc limit');
                                    #------>Query_Where
                                    #left join (',query_srch1,') as tranDEPO on tranDEPO.tran_reftable_gid = a.fetcollectionheader_gid
                                    # left join (',query_srch2,') as tranCLEAR on tranCLEAR.tran_reftable_gid = a.fetcollectionheader_gid

									if @CollectionLimit = 3 then
										set Query_Where = concat(Query_Where,' 3');
										else
										set Query_Where = concat(Query_Where,' 3000');
									end if;

									set @p = concat(Query_Column,Query_Where);
									#select @p;
									PREPARE stmt FROM @p;
									EXECUTE stmt;
                                    Select found_rows() into li_count;
									DEALLOCATE PREPARE stmt;

                                    if li_count > 0 then
										set Message = 'FOUND';
										commit;
									else
										set Message = 'NOT_FOUND';
									end if;


elseif ls_Action = 'COLLECTION' and ls_Type = 'INV_MAPPING' then
				 #### Record Show in Executive Collection Inv Mapping Page.
				select JSON_LENGTH(lj_Filters,'$') into @li_json_count;
                if @li_json_count is not null or @li_json_count <> '' then
						select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.CustGroup_Gid'))) into @CustGroup_Gid;
                        select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.REF_Name'))) into @REF_Name;

                        # Validations.
                        if @CustGroup_Gid is null or @CustGroup_Gid = '' or @CustGroup_Gid = 0 or @REF_Name = '' or @REF_Name is null then
								set Message = 'Insufficient Data In Json.';
                                leave coll_get;
                        End if;

                     select ref_gid into @ref_gid from gal_mst_tref where REF_Name = 'COLLECTION_INVMAP' and entity_gid = entity_gid and ref_active = 'Y' ;

							if @ref_gid is null then
									set Message = 'Problem In Ref Gid Generate.';
									leave coll_get;
							End if;


                End if;
					set Query_Select = '';
					set Query_Select = concat('select f.file_name,f.file_path,a.fetcollectionheader_gid,DATE_FORMAT(a.fetcollectionheader_date,''%d-%b-%Y'') as fetcollectionheader_date,
																a.fetcollectionheader_mode,DATE_FORMAT(a.fetcollectionheader_chequedate,''%d-%b-%Y'') as
																fetcollectionheader_chequedate,
                                                                ifnull(fetcollectionheader_chequeno,''0'') as fetcollectionheader_chequeno,
																a.fetcollectionheader_amount,
																sum(ifnull(b.invreceipt_amount,''0.00''))  as adjusted_amount,
																(ifnull(a.fetcollectionheader_amount,''0.00'') - sum(ifnull(b.invreceipt_amount,''0.00''))) as balance_amount,
                                                                ifnull(c.bank_name,''-'') as bank_name
																from fet_trn_tfetcollectionheader as a
																left join gal_map_tinvreceipt as b on b.invreceipt_reftablegid = a.fetcollectionheader_gid and b.invreceipt_refgid = ',@ref_gid,'
                                                                left join gal_mst_tbank as c on c.bank_gid = a.fetcollectionheader_bankgid and c.bank_isactive = ''Y'' and c.bank_isremoved = ''N''
                                                                left join gal_mst_tfile as f on f.file_gid=a.fetcollectionheader_filegid and f.file_isactive=''Y'' and f.file_isremoved=''N''

																Where   a.fetcollectionheader_isremoved = ''N''
																and a.fetcollectionheader_customergroup_gid = ',@CustGroup_Gid,'
                                                                and  fetcollectionheader_status = ''RECEIVED''
																Group By a.fetcollectionheader_date,a.fetcollectionheader_mode,a.fetcollectionheader_chequeno,a.fetcollectionheader_chequedate,
                                                                c.bank_name,
																a.fetcollectionheader_amount
																Having ifnull(sum(b.invreceipt_amount),0) < a.fetcollectionheader_amount
																order by a.fetcollectionheader_date'
																);
                                                                set @Query_Select = Query_Select;
																#select @Query_Select; ## Remove It.
																PREPARE stmt1 FROM @Query_Select;
																EXECUTE stmt1;
																Select found_rows() into li_count;
																DEALLOCATE PREPARE stmt1;

															if li_count > 0 then
																	set Message = 'FOUND';
															else
																	set Message = 'NOT_FOUND';
															end if;
elseif ls_Action = 'COLLECTION_INHAND' and ls_Type = 'PENDING' then
									select JSON_LENGTH(lj_Filters,'$') into @li_json_count;

									if  @li_json_count <=0  then
											set Message = 'No Data in Json - Filter.';
											leave coll_get;
									end if;

						select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Customer_Gid'))) into @Customer_Gid;
                       # select @Customer_Gid;

                        if @Customer_Gid is null or @Customer_Gid = '' or @Customer_Gid = 0 then
								set Message = 'Customer  Gid Is Needed.';
                                leave coll_get;
                        End if;

                        set @CustGroup_Gid = 0 ;
                        select customer_custgroup_gid into @CustGroup_Gid
                        from gal_mst_tcustomer where customer_gid = @Customer_Gid and customer_isactive = 'Y' and customer_isremoved = 'N';
                       # select @CustGroup_Gid;

                        if @CustGroup_Gid = 0 then
								set Message = 'Error On Customer Group Gid.';
                                leave coll_get;
                        End if;
					set Query_Select = '';

					set Query_Select = concat('select a.fetcollectionheader_gid,a.fetcollectionheader_customergroup_gid,a.fetcollectionheader_amount,a.fetcollectionheader_balanceamt,
					date_format(a.fetcollectionheader_date,''%d-%b-%Y'') as fetcollectionheader_date ,
					date_format(a.fetcollectionheader_chequedate,''%d-%b-%Y'') as fetcollectionheader_chequedate , ifnull(a.fetcollectionheader_chequeno,0) as cheque_no,
					a.fetcollectionheader_mode,a.fetcollectionheader_status
					 from fet_trn_tfetcollectionheader as a
					where a.fetcollectionheader_status in (''RECEIVED'', ''DEPOSITED'', ''Deposited'' )
                    and a.fetcollectionheader_isactive = ''Y'' and a.fetcollectionheader_isremoved = ''N''
                    and fetcollectionheader_customergroup_gid = ',@CustGroup_Gid,'
                    ');

													   set @Query_Select = Query_Select;
													#select @Query_Select; ## Remove It.
													PREPARE stmt1 FROM @Query_Select;
													EXECUTE stmt1;
													Select found_rows() into li_count;
													DEALLOCATE PREPARE stmt1;

												if li_count > 0 then
														set Message = 'FOUND';
												else
														set Message = 'NOT_FOUND';
												end if;
elseif ls_Action = 'FET_REVIEW' and ls_Type = 'COLLECTION' then
                ### Used to Show the Collection Details in FEt Review : POP
									select JSON_LENGTH(lj_Filters,'$') into @li_json_count;

									if  @li_json_count <=0  then
											set Message = 'No Data in Json - Filter.';
											leave coll_get;
									end if;

						select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Collection_Gid'))) into @Collection_Gid;

                        if @Collection_Gid is null or @Collection_Gid = '' or @Collection_Gid = 0 then
								set Message = 'Collection_Gid  Gid Is Needed.';
                                leave coll_get;
                        End if;


                           set @Ref_Collection_Gid = 0;
                                       select fn_REFGid('COLLECTION_INVMAP') into @Ref_Collection_Gid;

                                        if @Ref_Collection_Gid = 0 then
											set Message = 'Problem In REF Gid Generate' ;
                                            leave coll_get;
                                        End if;

					set Query_Select = '';
					set Query_Select = concat('Select ifnull(c.invoiceheader_customer_gid,0) as customer_gid,customergroup_gid,a.fetcollectionheader_amount,a.fetcollectionheader_status,
														a.fetcollectionheader_mode,a.fetcollectionheader_balanceamt,
														date_format(a.fetcollectionheader_date,''%Y-%b-%d'') as  fetcollectionheader_date ,
														 ifnull(c.invoiceheader_total,0) as invoiceheader_total
														 from fet_trn_tfetcollectionheader as a
														left join gal_map_tinvreceipt as b on b.invreceipt_reftablegid = a.fetcollectionheader_gid
														 and b.invreceipt_refgid = ',@Ref_Collection_Gid,'
														 left join gal_trn_tinvoiceheader as c on c.invoiceheader_gid = b.invreceipt_invoicegid
														  and c.invoiceheader_isremoved = ''N''
                                                          left join gal_mst_tcustomergroup as d on d.customergroup_gid=a.fetcollectionheader_customergroup_gid
														 where a.fetcollectionheader_gid = ',@Collection_Gid,' and a.fetcollectionheader_isactive = ''Y'' and a.fetcollectionheader_isremoved = ''N''
																			');

													   set @Query_Select = Query_Select;
													#select @Query_Select; ## Remove It.
													PREPARE stmt1 FROM @Query_Select;
													EXECUTE stmt1;
													Select found_rows() into li_count;
													DEALLOCATE PREPARE stmt1;

												if li_count > 0 then
														set Message = 'FOUND';
												else
														set Message = 'NOT_FOUND';
												end if;


End if;


END