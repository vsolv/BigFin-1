CREATE DEFINER=`root`@`%` PROCEDURE `sp_ClaimProcess_Get`(IN `ls_Type` varchar(64),IN `ls_Sub_Type` varchar(64),
IN `lj_Filters` json,IN `lj_Classification` json, OUT `Message` varchar(1024))
sp_ClaimProcess_Get:BEGIN
### Ramesh March 19 2019
### Ramesh Aug 25 2019 :: Initial Search, Search Travel Date Sep 2019
### Karthiga - REJECTED - INITIAL SUMMARY -24 oct 19 ---- DayWise_amt edited karthiga 30 dec 19
#### WIP
### TA Date 6144 1024
Declare Query_Select varchar(100000);
Declare Query_Search varchar(1024);
Declare Query_Search1 varchar(1024);
Declare i int;
declare errno int;
declare msg varchar(1000);
declare li_count int;

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

    select fn_Classification('ENTITY_ONLY',lj_Classification) into @OutMsg_Classification ;
        select  JSON_UNQUOTE(JSON_EXTRACT(@OutMsg_Classification, '$.Entity_Gid[0]')) into @Entity_Gids;
        if @Entity_Gids is  null or @Entity_Gids = '' then
				select  JSON_UNQUOTE(JSON_EXTRACT(@OutMsg_Classification, '$.Message')) into @Message;
				set Message = concat('Error On Classification Data - ',@Message);
                leave sp_ClaimProcess_Get;
        End if;


if ls_Type = 'INITIAL_SUMMARY' and ls_Sub_Type = 'TEMP' then

		  	set Query_Select = '';
            set Query_Search = '';
            select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Claim_Status'))) into @Claim_Status;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.Employee_Gid'))) into @Employee_Gid;

            select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.From_Date'))) into @From_Date;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.TO_Date'))) into @TO_Date;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.Claim_Type'))) into @Claim_Type;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.Amount_Min'))) into @Amount_Min;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.Amount_Max'))) into @Amount_Max;
            #select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.tadetails_remarks'))) into @tadetails_remarks;
            #select @Amount_Max,@Claim_Status,@Employee_Gid,@From_Date,@TO_Date,@Claim_Type,@Amount_Min;
            if @Claim_Status is null or @Claim_Status = '' then
					set Message = 'Claim Status Is Needed.';
                    leave sp_ClaimProcess_Get;
            End if;

             #if @tadetails_remarks is not null and @tadetails_remarks <> '' then
				#set Message = 'tadetails remarks Is Needed.';
                  #  leave sp_ClaimProcess_Get;
           # End if;


            if @Employee_Gid is not null and @Employee_Gid <> '' and @Employee_Gid <> 0  then
                   set Query_Search = concat(Query_Search,' and tadetails_employeegid = ',@Employee_Gid,' ');
            End if;

            if @From_Date is not null and @From_Date <> '' then
				set Query_Search = concat(Query_Search,' and date_format(tadetails_fromdate,''%Y-%m-%d'') >= ''',@From_Date,''' ');
            End if;

            if @TO_Date is not null and @TO_Date <> '' then
				set Query_Search = concat(Query_Search,' and date_format(tadetails_todate,''%Y-%m-%d'') <= ''',@TO_Date,''' ');
            End if;

            if @Claim_Type is not null and @Claim_Type <> '' then
				set Query_Search = concat(Query_Search,' and ta_type = ''',@Claim_Type,''' ');
            End if;

            if @Amount_Min is not null and @Amount_Min <> '' and @Amount_Max  is not null and @Amount_Max <> ' ' then
				set Query_Search = concat(Query_Search, 'and tadetails_totalamount between'  '''',@Amount_Min,''''  'and'  '''',@Amount_Max,'''');
            End if;
        # select Query_Search;
         #select tran_remarks into @remarks from  gal_trn_ttran where tran_ref_gid='70' and tran_status='REJECTED';

          select ref_gid from gal_mst_tref where ref_name='CLAIM_PROCESS' into @ref;
		  #select @ref;
           # select 1;
           set @Query_Sel='';

		   set @Query_Sel = concat('select #t.tran_remarks,
           a.tadetails_gid,b.employee_gid,b.employee_name,tadetails_invoceavailable,
					  ta_type,ta_subtype,
					  ifnull(tadetails_travelmode,'''') as tadetails_travelmode,
					  tadetails_vendorcode,tadetails_vendorname,
					  tadetails_gstapplicable,tadetails_gstno,
					  tadetails_gststate,
					  ifnull(tadetails_invoiceno,'''') as tadetails_invoiceno,
					  ifnull(tadetails_lodge,'''') as tadetails_lodge,
					  ifnull(tadetails_location,'''') as tadetails_location,
					  ifnull(date_format(tadetails_fromdate,''%d-%b-%Y''),'''') as tadetails_fromdate,
					  ifnull(date_format(tadetails_todate,''%d-%b-%Y''),'''') as tadetails_todate,
					  ifnull(tadetails_placefrom,'''') as tadetails_placefrom,
					  ifnull(tadetails_placeto,'''') tadetails_placeto,
					  ifnull(tadetails_km,'''') as tadetails_km,
					  tadetails_amountclaimed,
					  ifnull(tadetails_otheramount,'''') as tadetails_otheramount,
					  tadetails_totalamount,tadetails_amountprocessed,
					  ifnull(tadetails_imagepath,'''') as tadetails_imagepath,
					  ifnull(tadetails_remarks,'''') as tadetails_remarks,
					  tadetails_status,t.tran_remarks
                      from ecf_tmp_ttadetails as a
						inner join gal_mst_temployee as b on b.employee_gid = a.tadetails_employeegid
                       left join (select tran_remarks,tran_reftable_gid from gal_trn_ttran
                        left join ecf_tmp_ttadetails on tran_reftable_gid = tadetails_gid where tran_status=''REJECTED'' and tran_ref_gid = 70 ) as t
                        on t.tran_reftable_gid = tadetails_gid
						where a.tadetails_status = ''',@Claim_Status,'''
                        and a.entity_gid in (',@Entity_Gids,')  ',Query_Search,'





                      ');
                           # select @ref;
                          # select @Claim_Status;
                           #select @Query_Sel;
							set @Query_Select = @Query_Sel;
			      			 ### Remove It
			      			#select @Query_Sel; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;

elseif ls_Type = 'CLAIM_RATES' and ls_Sub_Type = 'TA' then
			set Query_Select = '';
            select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Employee_Gid'))) into @Employee_Gid;

            set Query_Select = concat('
											select a.tadetails_gid,b.employee_gid,b.employee_name,tadetails_invoceavailable,
					  ta_type,ta_subtype,
					  ifnull(tadetails_travelmode,'''') as tadetails_travelmode,
					  tadetails_vendorcode,tadetails_vendorname,
					  tadetails_gstapplicable,tadetails_gstno,
					  tadetails_gststate,
					  ifnull(tadetails_invoiceno,'''') as tadetails_invoiceno,
					  ifnull(tadetails_lodge,'''') as tadetails_lodge,
					  ifnull(tadetails_location,'''') as tadetails_location,
					  ifnull(date_format(tadetails_fromdate,''%d-%b-%Y %H-%i''),'''') as tadetails_fromdate,
					  ifnull(date_format(tadetails_todate,''%d-%b-%Y %H-%i''),'''')  tadetails_todate,
					  ifnull(tadetails_placefrom,'''') as tadetails_placefrom,
					  ifnull(tadetails_placeto,'''') tadetails_placeto,
					  ifnull(tadetails_km,'''') as tadetails_km,
					  tadetails_amountclaimed,
					  ifnull(tadetails_otheramount,'''') as tadetails_otheramount,
					  tadetails_totalamount,tadetails_amountprocessed,
					  ifnull(tadetails_imagepath,'''') as tadetails_imagepath,
					  ifnull(tadetails_remarks,'''') as tadetails_remarks,
					  tadetails_status
                      from ecf_tmp_ttadetails as a
						inner join gal_mst_temployee as b on b.employee_gid = a.tadetails_employeegid
						where a.tadetails_status = ''',@Claim_Status,''' and a.entity_gid in (',@Entity_Gids,')
							');

                            set @Query_Select = Query_Select;
								##select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;

  #karthiga  28 nov 19 edited ----------->

 elseif ls_Type = 'CLAIM' and ls_Sub_Type = 'Allowance' then
 #select 1;
			set Query_Select = '';
            set Query_Search='';
            set Query_Search1='';
            select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Employee_Gid'))) into @Employee_Gid;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.From_Date'))) into @From_Date;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.TO_Date'))) into @TO_Date;

             if @Employee_Gid is not null and @Employee_Gid <> '' and @Employee_Gid <> 0  then
                   set Query_Search = concat(Query_Search,' and employee_gid = ',@Employee_Gid,' ');
                   else
                   set Query_Search = concat(Query_Search,' ');
            End if;

             if @From_Date is not null and @From_Date <> '' and @TO_Date  is not null and @TO_Date <> ' ' then
				set Query_Search1 = concat(Query_Search1, 'and  tadetails_fromdate between'  '''',@From_Date,''''  'and'  '''',@TO_Date,'''');
                else
                set Query_Search1 = concat(Query_Search1, '');
            End if;



            set Query_Select = concat('select distinct
												c.employee_gid,c.employee_name,d.ta_gid,
												ifnull(date_format(tadetails_fromdate,''%d-%b-%Y''),'''') as tadetails_fromdate,
                                                ifnull(date_format(tadetails_todate,''%d-%b-%Y ''),'''') as tadetails_todate,
												d.ta_amountclaimed,a.invoiceheader_crno,a.invoiceheader_gid,
                                                e.ta_type,
                                                #e.ta_subtype,

												(select concat (''['',group_concat(json_object(''type'',ta_type,''subtype'',ta_subtype,
												''taamountclaimed'',tadetails_amountclaimed)),'']'')
													from ecf_trn_ttadetails
													inner join ecf_trn_tta on ta_gid=tadetails_tagid and ta_isactive=''Y'' and ta_isremoved=''N''
													inner join ecf_trn_tinvoiceheader  on invoiceheader_gid=ta_invoiceheaadergid and invoiceheader_isactive=''Y'' and invoiceheader_isremoved=''N''
													where  ta_gid =d.ta_gid  ',Query_Search1,' and tadetails_isactive=''Y'' and tadetails_isremoved=''N''
                                                    and ta_type=e.ta_type
												)as split_amt

											from ecf_trn_tinvoiceheader as a
											inner join ecf_trn_tinvoicedetails as b on b.invoicedetails_invoiceheadergid=a.invoiceheader_gid and b.invoicedetails_isactive=''Y'' and b.invoicedetails_isremoved=''N''
											inner join gal_mst_temployee as c on c.employee_gid = a.invoiceheader_employeegid and c.employee_isactive=''Y'' and c.employee_isremoved=''N''
											inner join ecf_trn_tta as d on d.ta_invoiceheaadergid=a.invoiceheader_gid and d.ta_isactive=''Y'' and d.ta_isremoved=''N''
											inner join ecf_trn_ttadetails as e on e.tadetails_tagid=d.ta_gid and e.tadetails_isactive=''Y'' and e.tadetails_isremoved=''N''
											where  a.entity_gid in(',@Entity_Gids,') ',Query_Search,' ',Query_Search1,'
                                            and a.invoiceheader_isactive=''Y'' and a.invoiceheader_isremoved=''N''
											group by tadetails_gid,ta_gid,ta_type;
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
							  end if;

#karthiga  06 dec 19 edited -----DayWise_amt edited karthiga 30 dec 19----- invoicedate wise search edited 31 dec 19-

elseif ls_Type = 'Summary_Details' and ls_Sub_Type = 'Details' then
 #select 1;
			SET SESSION group_concat_max_len=4294967295;
			set Query_Select = '';
            set Query_Search='';
            set Query_Search1='';
            set @f='';
            set @t='';
            select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Employee_Gid'))) into @Employee_Gid;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.From_Date'))) into @From_Date;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.TO_Date'))) into @TO_Date;

             if @Employee_Gid is not null and @Employee_Gid <> '' and @Employee_Gid <> 0  then
                   set Query_Search = concat(Query_Search,' and tadetails_employeegid = ',@Employee_Gid,' ');
                   else
                   set Query_Search = concat(Query_Search,' ');
            End if;

             if @From_Date is not null and @From_Date <> '' and @TO_Date  is not null and @TO_Date <> ' ' then
				set Query_Search1 = concat(Query_Search1, 'and  invoiceheader_invoicedate between'  '''',@From_Date,''''  'and'  '''',@TO_Date,'''');
                else
                set Query_Search1 = concat(Query_Search1, '');
            End if;

            set @f=date_format(@From_Date,'%Y-%m-%d');
			set @t=date_format(@TO_Date,'%Y-%m-%d');


            set @demo = concat('select ta_gid from ecf_trn_tta where ta_employeegid =',@Employee_Gid,' and date_format(ta_date,''%Y-%m-%d'') between
											''',@f,''' and ''',@t,'''');


			set Query_Select = concat(' select distinct c.Employee_gid,c.Employee_name,
											(''',@f,''') as Fromdate, (''',@t,''') as Todate,

											total.totalamt,
											( select distinct concat(''['',group_concat(json_object(''invoiceheader_gid'',concat(invoiceheader_gid),''FromDate'',date_format(tadetails_fromdate,''%d-%m-%Y''),
															''ToDate'',date_format(detaildate,''%d-%m-%Y''),''totalamount'',concat(total))),'']'') from
															( select invoiceheader_gid,tadetails_fromdate,max(tadetails_todate) as detaildate,tadetails_tagid,sum(tadetails_totalamount) as total
                                                           from ecf_trn_ttadetails as p
															inner join ecf_trn_tta on ta_gid=tadetails_tagid and ta_isactive=''Y'' and ta_isremoved=''N''
															inner join ecf_trn_tinvoiceheader  on invoiceheader_gid=ta_invoiceheaadergid and invoiceheader_isactive=''Y'' and invoiceheader_isremoved=''N''
															where p.entity_gid in (',@Entity_Gids,') and tadetails_tagid in (',@demo,') ',Query_Search,'
                                                            and tadetails_isactive=''Y'' and tadetails_isremoved=''N''
															group by tadetails_tagid order by tadetails_fromdate,tadetails_todate ASC)as invtotal
															)totaltype_amount,

											( select distinct concat(''['',group_concat(json_object(''invoiceheader_gid'',concat(invoiceheader_gid),''type'',ta_type,''invoicedate'',date_format(invoiceheader_invoicedate,''%d-%m-%Y''),''totalamount'',concat(total))),'']'')
															from
                                                            ( select invoiceheader_gid,ta_type,invoiceheader_invoicedate,sum(tadetails_totalamount)as total
															from  ecf_trn_tinvoiceheader  as k
															inner join ecf_trn_tta as l on l.ta_invoiceheaadergid=k.invoiceheader_gid and l.ta_isactive=''Y'' and l.ta_isremoved=''N''
															inner join ecf_trn_ttadetails as m on m.tadetails_tagid=l.ta_gid and m.tadetails_isactive=''Y'' and m.tadetails_isremoved=''N''
															where k.entity_gid in (',@Entity_Gids,') and k.invoiceheader_isactive=''Y'' and k.invoiceheader_isremoved=''N''
                                                            and tadetails_tagid in (',@demo,')
															and invoiceheader_employeegid = ',@Employee_Gid,'  ',Query_Search1,'
															group by tadetails_tagid,invoiceheader_invoicedate,ta_type order by invoiceheader_invoicedate ASC )as main
												)as Daywise_Amt,

												(select distinct concat (''['',group_concat(json_object(''invoiceheader_gid'',concat(invoiceheader_gid),''type'',ta_type,''subtype'',ta_subtype,
												''totalamount'',concat(tadetails_totalamount) ,''fromdate'',date_format(tadetails_fromdate,''%d-%b-%Y''),''todate'',date_format(tadetails_todate,''%d-%b-%Y''))),'']'')
												from ecf_trn_ttadetails as a
												inner join ecf_trn_tta on ta_gid=tadetails_tagid and ta_isactive=''Y'' and ta_isremoved=''N''
												inner join ecf_trn_tinvoiceheader  on invoiceheader_gid=ta_invoiceheaadergid and invoiceheader_isactive=''Y'' and invoiceheader_isremoved=''N''
												where a.entity_gid in (',@Entity_Gids,') and tadetails_tagid in (',@demo,') ',Query_Search,'
												and tadetails_isactive=''Y'' and tadetails_isremoved=''N'' order by tadetails_fromdate,tadetails_todate ASC
												)as split_amt

											from ecf_trn_tinvoiceheader as a
											inner join ecf_trn_tinvoicedetails as b on b.invoicedetails_invoiceheadergid=a.invoiceheader_gid and b.invoicedetails_isactive=''Y'' and b.invoicedetails_isremoved=''N''
											inner join gal_mst_temployee as c on c.employee_gid = a.invoiceheader_employeegid and c.employee_isactive=''Y'' and c.employee_isremoved=''N''
											inner join ecf_trn_tta as d on d.ta_invoiceheaadergid=a.invoiceheader_gid and d.ta_isactive=''Y'' and d.ta_isremoved=''N''
											inner join ecf_trn_ttadetails as e on e.tadetails_tagid=d.ta_gid and e.tadetails_isactive=''Y'' and e.tadetails_isremoved=''N''
                                            inner join (

                                            select sum(tadetails_totalamount) as totalamt
													from  ecf_trn_tinvoiceheader  as s
													inner join ecf_trn_tta as t on t.ta_invoiceheaadergid=s.invoiceheader_gid and t.ta_isactive=''Y'' and t.ta_isremoved=''N''
													inner join ecf_trn_ttadetails as u on u.tadetails_tagid=t.ta_gid and u.tadetails_isactive=''Y'' and u.tadetails_isremoved=''N''
													where s.entity_gid in (',@Entity_Gids,') and s.invoiceheader_isactive=''Y'' and s.invoiceheader_isremoved=''N''
													and tadetails_tagid in (',@demo,') ',Query_Search,'
													and invoiceheader_employeegid =',@Employee_Gid,' ',Query_Search1,')	as total
											on a.invoiceheader_gid=d.ta_invoiceheaadergid

											#select sum(invoiceheader_amount)as totalamt  from ecf_trn_tinvoiceheader as a where a.entity_gid in (',@Entity_Gids,') and invoiceheader_employeegid=',@Employee_Gid,'
                                            #',Query_Search1,' )as total
											#on a.invoiceheader_gid=d.ta_invoiceheaadergid

											where  a.entity_gid in(',@Entity_Gids,')  and tadetails_employeegid = ',@Employee_Gid,'
                                            and a.invoiceheader_isactive=''Y'' and a.invoiceheader_isremoved=''N''
											group by ta_type order by tadetails_fromdate,tadetails_todate ASC


										');

								set @Query_Select = Query_Select;
								#select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then

									set Message = 'FOUND';
                                    #select 1;
							  else
								  set Message = 'NOT_FOUND';
							  end if;



End if;


END