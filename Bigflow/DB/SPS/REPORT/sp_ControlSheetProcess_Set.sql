CREATE DEFINER=`root`@`%` PROCEDURE `sp_ControlSheetProcess_Set`(IN `ls_Action` varchar(32),IN `ls_Type` varchar(32),
IN `ls_SubType` varchar(32),IN `lj_Data` json,IN `lj_File` JSON,IN `lj_Classification` JSON,IN `li_Create_By` INT ,OUT `Message` varchar(5000)
)
sp_ControlSheetProcess_Set:BEGIN
### Ramesh June 22 2019,Aug 27 2019
### Vignesh Sep 2019 Stock + Ramesh
Declare Query_Select varchar(5000);
Declare li_count int;
declare errno int;
declare msg varchar(1000);
Declare v_InvDetail_Gid,v_Date,v_Stockbalance_Gid,v_Product_Gid,v_Inv_No,v_Cb,v_Customer_Name,v_Product_Name,v_Qty,v_Price,v_Amount,v_Dump_Gid,v_Status,v_Balance_Amount,v_OutStand_Gid
		varchar(128);

DECLARE finished INTEGER DEFAULT 0;
DECLARE done INT DEFAULT FALSE;
#DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;


	DECLARE EXIT HANDLER FOR SQLEXCEPTION,sqlwarning
    BEGIN

    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
    set Message = concat(errno , msg);
    ROLLBACK;
    END;


SET SESSION group_concat_max_len=4294967295;
Select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification,'$.Entity_Gid')) into @Entity_Gid;
#select @Entity_Gid;

start transaction;
set autocommit = 0 ;

if ls_Action = 'INSERT' and ls_Type = 'CONTROL_SALES' then

             call sp_ControlSheet_Set('INSERT','CONTROL_SALES','TALLY',lj_Data,lj_File,lj_Classification,li_Create_By,@Message);
             select @Message into @Out_Msg_CtrlDump;
             #select @Out_Msg_CtrlDump;
             if @Out_Msg_CtrlDump <> 'SUCCESS' then
					set Message = concat('Error On Sales Dump Upload - ',@Out_Msg_CtrlDump);
                    rollback;
                    leave sp_ControlSheetProcess_Set;
             End if;

             #### It will Insert Already by Above
            select max(ctldump_version) into @max_dump_version from gal_trn_tctldump
            where ctldump_source = 'TALLY' and ctldump_type = 'SALES' and entity_gid = @Entity_Gid
            and date_format(create_date,'%Y-%b-%d') = date_format(current_date(),'%Y-%b-%d') ;

            select min(ctldump_invdate) into @Min_Inv_Date from gal_trn_tctldump where ctldump_source = 'TALLY' and ctldump_type = 'SALES'
            and ctldump_version = @max_dump_version and entity_gid = @Entity_Gid
            and date_format(create_date,'%Y-%b-%d') = date_format(current_date(),'%Y-%b-%d')
            ;

            set @Ctrl_Date = @Min_Inv_Date;
            set @Ctrl_Version = @max_dump_version;
            set @Dump_Type = 'SALES';

            if @Ctrl_Date is  null or @Ctrl_Date = '' then
					set Message = 'Date Is Needed To Compare.';
                    leave sp_ControlSheetProcess_Set;
            End if;

            if @Ctrl_Version is  null or @Ctrl_Version = '' then
					set Message = 'Version Is Needed To Compare';
                    leave sp_ControlSheetProcess_Set;
            End if;

            if @Dump_Type is null or @Dump_Type = '' then
				set Message = 'Dump Type Is Needed.';
                leave sp_ControlSheetProcess_Set;
            End if;

		##### Cursor Starts Here
        	Begin
				Declare Cursor_Ctrl CURSOR FOR
								#### Include the Date ## TO DO
					 Select c.invoicedetails_gid,a.invoiceheader_date,a.invoiceheader_no,b.customer_name,d.product_name,invoicedetails_qty,c.invoicedetails_nrpprice,
                     (c.invoicedetails_qty*c.invoicedetails_nrpprice) as detail_amount,
					ifnull(e.ctldump_gid,0) as ctldump_gid,
					Case
							when ifnull(e.ctldump_gid,0) <> 0 then 'MATCHED'
							when ifnull(e.ctldump_gid,0) = 0 then 'NOT_MATCHED'
					 End as 'CTRL_STATUS'

					 from gal_trn_tinvoiceheader as a
					inner join gal_mst_tcustomer as b on b.customer_gid = a.invoiceheader_customer_gid
					inner join gal_trn_tinvoicedetails as c on c.invoicedetails_invoice_gid = a.invoiceheader_gid
					inner join gal_mst_tproduct as d on d.product_gid = c.invoicedetails_product_gid
					left join gal_trn_tctldump as e on e.ctldump_customername = b.customer_name and e.ctldump_productname = d.product_name
					and e.ctldump_invdate = a.invoiceheader_date
					and e.ctldump_qty = c.invoicedetails_qty
					and e.ctldump_unitrate = c.invoicedetails_nrpprice
					and e.ctldump_invdate >= @Ctrl_Date
                    and e.ctldump_invoiceno = a.invoiceheader_no
                    and e.ctldump_version = @Ctrl_Version
                    and e.ctldump_type = @Dump_Type
                    and e.entity_gid = @Entity_Gid
					and e.ctldump_source = 'TALLY'
                    and date_format(e.create_date,'%Y-%b-%d')  = date_format(current_timestamp(),'%Y-%b-%d')
					where a.invoiceheader_date >= @Ctrl_Date
                    and a.invoiceheader_status <> 'CANCEL'
                    and a.entity_gid = @Entity_Gid

				#	union

					#Select z.ctldump_invdate,z.ctldump_customername,z.ctldump_productname,z.ctldump_qty,z.ctldump_unitrate,
                    #z.ctldump_gid,'TEMP'
					#from gal_trn_tctldump as z
					#where z.ctldump_invdate >= '2019-06-03'
					;


								DECLARE CONTINUE HANDLER
								FOR NOT FOUND SET finished = 1;
								#### Looping.
								#set done = 0;
								OPEN Cursor_Ctrl;
								ctrl_looop:loop
								fetch Cursor_Ctrl into v_InvDetail_Gid,v_Date,v_Inv_No,v_Customer_Name,v_Product_Name,v_Qty,v_Price,v_Amount,v_Dump_Gid,v_Status;

                                     if finished = 1 then
										leave ctrl_looop;
									End if;

					If cast(v_Dump_Gid as decimal(16,2) ) > 0 then
												set @lj_UpdateDetail = '';
												set @lj_UpdateDetail = concat(
												'{"CtrlDump_Gid":',v_Dump_Gid,',
												   "Status":"MATCHED"
												}'
												);

											call sp_ControlSheet_Set('UPDATE','STATUS_UPDATE','UPDATE',@lj_UpdateDetail,'{}',lj_Classification,li_Create_By,@Message);
											select @Message into @Out_Msg_CtrlUpdate ;

                             #set @Out_Msg_CtrlUpdate = 'SUCCESS';

								if @Out_Msg_CtrlUpdate = 'SUCCESS' then
									set Message = 'SUCCESS';
								else
									Set Message = @Out_Msg_CtrlUpdate;
									close Cursor_Ctrl;
									leave sp_ControlSheetProcess_Set;
								End if;

				elseif cast(v_Dump_Gid as decimal(16,2))= 0 and cast(v_InvDetail_Gid as decimal(16,2)) > 0  then
							set @lj_SystemData = '';
                            set v_Product_Name = JSON_QUOTE(v_Product_Name);
							set @lj_SystemData = concat('
													{
								"SALE_DETAILS":[
								{
								"Customer_Name":"',v_Customer_Name,'",
								"Product_Name":',v_Product_Name,',
								"Invoice_Date":"',v_Date,'",
								"Invoice_No":"',v_Inv_No,'",
								"Quantity":"',v_Qty,'",
								"Per_Rate":"',v_Price,'",
								"Amount":"',v_Amount,'",
                                "Status":"MISMATCHED"
								}
								]
								}
                    '
                    );

			#  select v_Date,v_Inv_No,v_Customer_Name,v_Product_Name,v_Qty,v_Price,v_Amount,v_Status;
                    call sp_ControlSheet_Set('INSERT','CONTROL_SALES','SYSTEM',@lj_SystemData,'{}',lj_Classification,li_Create_By,@Message);
						select @Message into @Out_Msg_CtrlUpdate ;

					 if @Out_Msg_CtrlUpdate = 'SUCCESS' then
							set Message = 'SUCCESS';
                      else
						#	select @Out_Msg_CtrlUpdate;
							set Message = @Out_Msg_CtrlUpdate;
							close Cursor_Ctrl;
							leave sp_ControlSheetProcess_Set;
					 End if;
             else
                  #set Message = 'Error Occured.';
                  #select v_InvDetail_Gid,v_Date,v_Inv_No,v_Customer_Name,v_Product_Name,v_Qty,v_Price,v_Amount,v_Dump_Gid,v_Status;
               #select  @Ctrl_Date,@Ctrl_Version,@Dump_Type;

                #  close Cursor_Ctrl;
                 # leave sp_ControlSheetProcess_Set;
                  set Message = 'SUCCESS';

            End if;

            if finished = 1 then
				leave ctrl_looop;
            End if;

            End loop ctrl_looop;
            close Cursor_Ctrl;
			commit;
         end;

         #### Check and Update the Dumptable Mismatched

					set @Ctl_Dump_Gids = 0;
					Select group_concat(ctldump_gid) into @Ctl_Dump_Gids from gal_trn_tctldump
					where ctldump_source = 'TALLY' and ctldump_type = 'SALES' and ctldump_status is null and entity_gid = @Entity_Gid and ctldump_version = @Ctrl_Version ;

                    If @Ctl_Dump_Gids <> 0 then
								set @lj_UpdateDetail = '';
								set @lj_UpdateDetail = concat(
								'{"CtrlDump_Gid":"',@Ctl_Dump_Gids,'",
								   "Status":"MISMATCHED"
								}'
								);

								call sp_ControlSheet_Set('UPDATE','STATUS_UPDATE','UPDATE',@lj_UpdateDetail,'{}',lj_Classification,li_Create_By,@Message);
								select @Message into @Out_Msg_CtrlUpdate ;

									if @Out_Msg_CtrlUpdate = 'SUCCESS' then
										set Message = 'SUCCESS';
									else
										Set Message = @Out_Msg_CtrlUpdate;
										leave sp_ControlSheetProcess_Set;
									End if;
                    End if;

        #### Check and Insert in Summary Table
			Select ifnull(count(ctldump_gid),0) into @Count_Mismatch
			from gal_trn_tctldump as a
			where ctldump_version = @Ctrl_Version and ctldump_type = 'SALES' and ctldump_status = 'MISMATCHED' and a.entity_gid = @Entity_Gid ;

            if cast(@Ctrl_Version as decimal(16,2)) > 0 then
					set @Summary_Status = 'NOT_MATCHED';
             else
                 set @Summary_Status = 'FULLY_MATCHED';
            End if;

           set @lj_Summary_Data = '';
           set @lj_Summary_Data = concat('
           {"Ctl_Type":"SALES",
             "Ctl_Status":"',@Summary_Status,'",
             "Ctl_Version":',@Ctrl_Version,'
           }
           ');

				call sp_ControlSheet_Set('INSERT','SUMMARY_INSERT','',@lj_Summary_Data,'{}',lj_Classification,li_Create_By,@Message);
                select @Message into @Out_Msg_Summary;

                if @Out_Msg_Summary = 'SUCCESS' then
						set Message = 'SUCCESS';
                 else
                      set Message = concat('Error Occured On Summary Save - ',@Out_Msg_Summary);
                      rollback;
                      leave sp_ControlSheetProcess_Set;
				End if;


        if Message = 'SUCCESS' then
				commit;
                set Message = 'SUCCESS';
        End if;


elseif ls_Action = 'INSERT' and 	ls_Type = 'CONTROL_OUTSTANDING' then

            call sp_ControlSheet_Set('INSERT','CONTROL_OUTSTANDING','TALLY',lj_Data,lj_File,lj_Classification,li_Create_By,@Message);
             select @Message into @Out_Msg_CtrlDump;

             if @Out_Msg_CtrlDump <> 'SUCCESS' then
					set Message = concat('Error On Outstanding Dump Upload - ',@Out_Msg_CtrlDump);
                    rollback;
                    leave sp_ControlSheetProcess_Set;
             End if;

            select max(ctldump_version) into @max_dump_version from gal_trn_tctldump
            where ctldump_source = 'TALLY' and ctldump_type = 'OUTSTANDING' and entity_gid = @Entity_Gid
            and date_format(create_date,'%Y-%b-%d') = date_format(current_date(),'%Y-%b-%d')
            ;

            select min(ctldump_invdate) into @Min_Inv_Date from gal_trn_tctldump where ctldump_source = 'TALLY' and ctldump_type = 'OUTSTANDING'
            and ctldump_version = @max_dump_version and entity_gid = @Entity_Gid
            and date_format(create_date,'%Y-%b-%d') = date_format(current_date(),'%Y-%b-%d')
            ;

            set @Ctrl_Date = @Min_Inv_Date;
            set @Ctrl_Version = @max_dump_version;
            set @Dump_Type = 'OUTSTANDING';

            if @Ctrl_Date is  null or @Ctrl_Date = '' then
					set Message = 'Date Is Needed To Compare.';
                    leave sp_ControlSheetProcess_Set;
            End if;

            if @Ctrl_Version is  null or @Ctrl_Version = '' then
					set Message = 'Version Is Needed To Compare';
                    leave sp_ControlSheetProcess_Set;
            End if;

            if @Dump_Type is null or @Dump_Type = '' then
				set Message = 'Dump Type Is Needed.';
                leave sp_ControlSheetProcess_Set;
            End if;

				##### Cursor Starts Here
        	Begin
				Declare Cursor_Ctrl CURSOR FOR
                ##v_InvDetail_Gid,v_Date,v_Inv_No,v_Customer_Name,v_Product_Name,v_Qty,v_Price,v_Amount,v_Dump_Gid,v_Status,v_Balance_Amount,v_OutStand_Gid
									Select a.fetsoutstanding_gid,c.customer_name,a.fetsoutstanding_invoiceno,a.fetsoutstanding_invoicedate,a.fetsoutstanding_netamount,
										ifnull((a.fetsoutstanding_netamount  - ifnull(sum(b.fetsoutstandingdtl_amount),0)),0) as Balance_Amount, ifnull(d.ctldump_gid,0) as ctldump_gid,
															Case
																when ifnull(d.ctldump_gid,0) <> 0 then 'MATCHED'
																when ifnull(d.ctldump_gid,0) = 0 then 'NOT_MATCHED'
														  End as 'CTRL_STATUS'
									 from fet_trn_tfetsoutstanding as a
									left join fet_trn_tfetsoutstandingdtl as b on b.fetsoutstandingdtl_fetsoutstanding_gid = a.fetsoutstanding_gid
                                     and b.fetsoutstandingdtl_isremoved = 'N'
									inner join gal_mst_tcustomer as c on c.customer_gid = a.fetsoutstanding_customer_gid
									left join gal_trn_tctldump as d on d.ctldump_customername = c.customer_name
										and d.ctldump_invoiceno = mid(a.fetsoutstanding_invoiceno,1,11)
										and d.ctldump_type = 'OUTSTANDING'
										and d.ctldump_version = @max_dump_version
										and d.ctldump_source = 'TALLY'
                                        and date_format(d.create_date,'%Y-%b-%d')  = date_format(current_timestamp(),'%Y-%b-%d')
									Where a.fetsoutstanding_status <> 'PAID' and a.fetsoutstanding_status <> 'CANCEL'
									and a.fetsoutstanding_isremoved = 'N'
                                    and a.entity_gid = @Entity_Gid
									group by  a.fetsoutstanding_gid,c.customer_name,a.fetsoutstanding_invoiceno,a.fetsoutstanding_invoicedate,a.fetsoutstanding_netamount
									;

								DECLARE CONTINUE HANDLER
								FOR NOT FOUND SET finished = 1;
								#### Looping.
								set done = 0;
								OPEN Cursor_Ctrl;
								ctrl_looop:loop
								fetch Cursor_Ctrl into v_OutStand_Gid,v_Customer_Name,v_Inv_No,v_Date,v_Amount,v_Balance_Amount,v_Dump_Gid,v_Status;
										if finished = 1 then
											leave ctrl_looop;
										End if;

					If cast(v_Dump_Gid as decimal(16,2) ) > 0 then

							set @lj_UpdateDetail = '';
							set @lj_UpdateDetail = concat(
							'{"CtrlDump_Gid":',v_Dump_Gid,',
							   "Status":"MATCHED"
							}'
							);

							call sp_ControlSheet_Set('UPDATE','STATUS_UPDATE','UPDATE',@lj_UpdateDetail,'{}',lj_Classification,li_Create_By,@Message);
							select @Message into @Out_Msg_CtrlUpdate ;

								if @Out_Msg_CtrlUpdate = 'SUCCESS' then
									set Message = 'SUCCESS';
								else
									Set Message = @Out_Msg_CtrlUpdate;
									close Cursor_Ctrl;
									leave sp_ControlSheetProcess_Set;
								End if;

				elseif cast(v_Dump_Gid as decimal(16,2))= 0 and cast(v_OutStand_Gid as decimal(16,2)) > 0  then
							set @lj_SystemData = '';
							set @lj_SystemData = concat('
													{
								"OUTSTANDING_DETAILS":[
								{
								"Customer_Name":"',v_Customer_Name,'",
								"Invoice_Date":"',v_Date,'",
								"Invoice_No":"',v_Inv_No,'",
                                "Amount":"',v_Amount,'",
								"Pending_Amount":"',v_Balance_Amount,'",
								"Status":"MISMATCHED"
								}
								]
								}
                    '
                    );

                   # select v_Balance_Amount;

			#  select v_Date,v_Inv_No,v_Customer_Name,v_Product_Name,v_Qty,v_Price,v_Amount;
                    call sp_ControlSheet_Set('INSERT','CONTROL_OUTSTANDING','SYSTEM',@lj_SystemData,'{}',lj_Classification,li_Create_By,@Message);
						select @Message into @Out_Msg_CtrlUpdate ;

                      #select @Out_Msg_CtrlUpdate;
					 if @Out_Msg_CtrlUpdate = 'SUCCESS' then
							set Message = 'SUCCESS';
                      else
						#	select @Out_Msg_CtrlUpdate;
							set Message = @Out_Msg_CtrllUpdate;
							close Cursor_Ctrl;
							leave sp_ControlSheetProcess_Set;
					 End if;
             else
                  set Message = 'Error Occured.';
                  close Cursor_Ctrl;
                  leave sp_ControlSheetProcess_Set;

            End if;


            End loop ctrl_looop;
            close Cursor_Ctrl;
			commit;
         end;



         #### Check and Update the Dumptable Mismatched

					set @Ctl_Dump_Gids = 0;
					Select group_concat(ctldump_gid) into @Ctl_Dump_Gids from gal_trn_tctldump
					where ctldump_source = 'TALLY' and ctldump_type = 'OUTSTANDING' and ctldump_status is null and entity_gid = @Entity_Gid and ctldump_version = @Ctrl_Version ;

                    If @Ctl_Dump_Gids <> 0 then
								set @lj_UpdateDetail = '';
								set @lj_UpdateDetail = concat(
								'{"CtrlDump_Gid":"',@Ctl_Dump_Gids,'",
								   "Status":"MISMATCHED"
								}'
								);

								call sp_ControlSheet_Set('UPDATE','STATUS_UPDATE','UPDATE',@lj_UpdateDetail,'{}',lj_Classification,li_Create_By,@Message);
								select @Message into @Out_Msg_CtrlUpdate ;

									if @Out_Msg_CtrlUpdate = 'SUCCESS' then
										set Message = 'SUCCESS';
									else
										Set Message = @Out_Msg_CtrlUpdate;
										leave sp_ControlSheetProcess_Set;
									End if;
                    End if;


        #### Check and Insert in Summary Table
			Select ifnull(count(ctldump_gid),0) into @Count_Mismatch
			from gal_trn_tctldump as a
			where ctldump_version = @Ctrl_Version and ctldump_type = 'OUTSTANDING' and ctldump_status = 'MISMATCHED' and a.entity_gid = @Entity_Gid ;

            if cast(@Ctrl_Version as decimal(16,2)) > 0 then
					set @Summary_Status = 'NOT_MATCHED';
             else
                 set @Summary_Status = 'FULLY_MATCHED';
            End if;

           set @lj_Summary_Data = '';
           set @lj_Summary_Data = concat('
           {"Ctl_Type":"OUTSTANDING",
             "Ctl_Status":"',@Summary_Status,'",
             "Ctl_Version":',@Ctrl_Version,'
           }
           ');

				call sp_ControlSheet_Set('INSERT','SUMMARY_INSERT','',@lj_Summary_Data,'{}',lj_Classification,li_Create_By,@Message);
                select @Message into @Out_Msg_Summary;

                if @Out_Msg_Summary = 'SUCCESS' then
						set Message = 'SUCCESS';
                 else
                      set Message = concat('Error Occured On Summary Save - ',@Out_Msg_Summary);
                      rollback;
                      leave sp_ControlSheetProcess_Set;
				End if;


        if Message = 'SUCCESS' then
				commit;
                set Message = 'SUCCESS';
        End if;

elseif ls_Action = 'INSERT' and ls_Type = 'CONTROL_STOCK' then

            if ls_SubType = 'GODOWN' then
				 set @SubType = 'GODOWN';
			elseif ls_SubType = 'TALLY' then
                 set @SubType = 'TALLY';
            End if;

             call sp_ControlSheet_Set('INSERT','CONTROL_STOCK',@SubType,lj_Data,lj_File,lj_Classification,li_Create_By,@Message);
             select @Message into @Stk_Msg_CtrlDump;

			 select  JSON_UNQUOTE(JSON_EXTRACT(lj_Data, CONCAT('$.Godown_Gid'))) into @Godown_Gid;

            	if @Godown_Gid = '' or @Godown_Gid is null then
						set Message = 'Godown Gid Is Needed in Uploaded Data.';
						rollback;
						leave sp_ControlSheetProcess_Set;
				End if;


             if @Stk_Msg_CtrlDump <> 'SUCCESS' then
			 		set Message = concat('Error On Stock Dump Upload - ',@Stk_Msg_CtrlDump);
                    rollback;
                    leave sp_ControlSheetProcess_Set;
             End if;

            select max(ctldump_version) into @max_dump_version from gal_trn_tctldump
            where
            ctldump_type = 'STOCK' and entity_gid = @Entity_Gid
            and date_format(create_date,'%Y-%b-%d') = date_format(current_date(),'%Y-%b-%d')
            ;


            #### Not Needed
            #select min(ctldump_invdate) into @Min_Inv_Date from gal_trn_tctldump where ctldump_source = 'TALLY' and ctldump_type = 'STOCK'
            #and ctldump_version = @max_dump_version and entity_gid = @Entity_Gid
            #and date_format(create_date,'%Y-%b-%d') = date_format(current_date(),'%Y-%b-%d')
            #;

            set @Ctrl_Version = @max_dump_version;
            set @Dump_Type = 'STOCK';


            if @Ctrl_Version is  null or @Ctrl_Version = '' then
					set Message = 'Version Is Needed To Compare';
                    leave sp_ControlSheetProcess_Set;
            End if;

            if @Dump_Type is null or @Dump_Type = '' then
				set Message = 'Dump Type Is Needed.';
                leave sp_ControlSheetProcess_Set;
            End if;

				set @Check_System_Data = 0 ;
                Select ifnull(count(ctldump_gid),0) into @Check_System_Data
				from gal_trn_tctldump where ctldump_source = 'BIGFLOW' and ctldump_type = 'STOCK' and ctldump_version = @max_dump_version
                 and date_format(create_date,'%Y-%b-%d') = date_format(current_date(),'%Y-%b-%d') ;



				##### Cursor Starts Here
        	Begin
				Declare Cursor_Ctrl CURSOR FOR
                #v_InvDetail_Gid,v_Date,v_Inv_No,v_Customer_Name,v_Product_Name,v_Qty,v_Price,v_Amount,v_Dump_Gid,v_Status,v_Balance_Amount,v_OutStand_Gid
									Select  b.product_name,stockbalance_gid,stockbalance_productgid,stockbalance_cb,ifnull(c.ctldump_gid,0)as ctldump_gid,stockbalance_date,
															Case
																when ifnull(c.ctldump_gid,0) <> 0 then 'MATCHED'
																when ifnull(c.ctldump_gid,0) = 0 then 'NOT_MATCHED'
														  End as 'CTRL_STATUS'
									from gal_trn_tstockbalance as a
									inner join gal_mst_tproduct as b on a.stockbalance_productgid = b.product_gid and product_isremoved='N' and product_isactive='Y'
									left join gal_trn_tctldump as c on b.product_gid = c.ctldump_productgid
										and c.ctldump_qty = a.stockbalance_cb
										and c.ctldump_type = 'STOCK'
                                        and c.ctldump_godown_gid = a.stockbalance_godown_gid
										and c.ctldump_version = @max_dump_version
										and c.ctldump_source = @SubType
                                        and date_format(c.create_date,'%Y-%b-%d')  = date_format(current_timestamp(),'%Y-%b-%d')  ### check
									Where stockbalance_gid in(select max(stockbalance_gid) from gal_trn_tstockbalance group by stockbalance_productgid)
                                    and stockbalance_godown_gid = @Godown_Gid
                                    and a.entity_gid = @Entity_Gid
                                    ;


								DECLARE CONTINUE HANDLER
								FOR NOT FOUND SET finished = 1;


								#### Looping.
								set done = 0;
								OPEN Cursor_Ctrl;
								ctrl_looop:loop
								fetch Cursor_Ctrl into v_Product_Name,v_Stockbalance_Gid,v_Product_Gid,v_Cb,v_Dump_Gid,v_Date,v_Status;
										if finished = 1 then
											leave ctrl_looop;
										End if;
             #  select @max_dump_version,@SubType,@Entity_Gid;
				#select v_Stockbalance_Gid,v_Product_Gid,v_Cb,v_Dump_Gid,v_Date,v_Status;




					If cast(v_Dump_Gid as decimal(16,2) ) > 0 then

							set @lj_UpdateDetail = '';
							set @lj_UpdateDetail = concat(
							'{"CtrlDump_Gid":',v_Dump_Gid,',
							   "Status":"MATCHED"
							}'
							);

							call sp_ControlSheet_Set('UPDATE','STATUS_UPDATE','UPDATE',@lj_UpdateDetail,'{}',lj_Classification,li_Create_By,@Message);
							select @Message into @Out_Msg_CtrlUpdate;
                           # SELECT @Out_Msg_CtrlUpdate;

								if @Out_Msg_CtrlUpdate = 'SUCCESS' then
									set Message = 'SUCCESS';
								else
									Set Message = @Out_Msg_CtrlUpdate;
									close Cursor_Ctrl;
									leave sp_ControlSheetProcess_Set;
								End if;

				elseif cast(v_Dump_Gid as decimal(16,2))= 0 and cast(v_Stockbalance_Gid as decimal(16,2)) > 0  then

                ### TO DO Need Pdct Name
						if 	@Check_System_Data = 0 then
                        #set v_Product_Name = JSON_QUOTE(v_Product_Name);

								set @lj_SystemData = '';
                                set v_Product_Name = JSON_QUOTE(v_Product_Name);
												set @lj_SystemData = concat('
																	{
												"STOCK_DETAILS":[
												{
												 "Particulars":',v_Product_Name,',
												 "Product_Gid":"',v_Product_Gid,'",
												 "Quantity":"',v_Cb,'",
												 "Status":"MISMATCHED"
												}
												],
												"Date": "',v_Date,'"
												}
									'
									);


								call sp_ControlSheet_Set('INSERT','CONTROL_STOCK','SYSTEM',@lj_SystemData,'{}',lj_Classification,li_Create_By,@Message);
								select @Message into @Out_Msg_CtrlUpdate ;

								elseif @Check_System_Data > 0 then
                                     set @Message = 'SUCCESS';
                          End if;

					 if @Out_Msg_CtrlUpdate = 'SUCCESS' then
							set Message = 'SUCCESS';
					 else
							set Message = @Out_Msg_CtrlUpdate;
							close Cursor_Ctrl;
							leave sp_ControlSheetProcess_Set;
					 End if;
             else
                  set Message = 'Error Occured.';
                  close Cursor_Ctrl;
				  leave sp_ControlSheetProcess_Set;

            End if;


            End loop ctrl_looop;
            close Cursor_Ctrl;
			commit;
         end;



         #### Check and Update the Dumptable Mismatched

					set @Ctl_Dump_Gids = 0;
					Select group_concat(ctldump_gid) into @Ctl_Dump_Gids from gal_trn_tctldump
					where ctldump_source = @SubType and ctldump_type = 'STOCK' and ctldump_status is null and entity_gid = @Entity_Gid and ctldump_version = @Ctrl_Version ;

                    If @Ctl_Dump_Gids <> 0 then
								set @lj_UpdateDetail = '';
								set @lj_UpdateDetail = concat(
								'{"CtrlDump_Gid":"',@Ctl_Dump_Gids,'",
								   "Status":"MISMATCHED"
								}'
								);

								call sp_ControlSheet_Set('UPDATE','STATUS_UPDATE','UPDATE',@lj_UpdateDetail,'{}',lj_Classification,li_Create_By,@Message);
								select @Message into @Out_Msg_CtrlUpdate ;

									if @Out_Msg_CtrlUpdate = 'SUCCESS' then
										set Message = 'SUCCESS';
									else
										Set Message = @Out_Msg_CtrlUpdate;
										leave sp_ControlSheetProcess_Set;
									End if;
                    End if;


				#### Check and Insert in Summary Table
					Select ifnull(count(ctldump_gid),0) into @Count_Mismatch
					from gal_trn_tctldump as a
					where ctldump_version = @Ctrl_Version and ctldump_type = 'STOCK' and ctldump_status = 'MISMATCHED' and a.entity_gid = @Entity_Gid
                    and date_format(create_date,'%Y-%b-%d') = date_format(current_date(),'%Y-%b-%d')
                    ;

					if cast(@Ctrl_Version as decimal(16,2)) > 0 then
							set @Summary_Status = 'NOT_MATCHED';
					 else
						 set @Summary_Status = 'FULLY_MATCHED';
					End if;

				   set @lj_Summary_Data = '';
				   set @lj_Summary_Data = concat('
				   {"Ctl_Type":"STOCK",
					 "Ctl_Status":"',@Summary_Status,'",
					 "Ctl_Version":',@Ctrl_Version,'
				   }
				   ');

					#### Added By Ramesh Sep 14 2019 ::: To Check for 3 + Way Matching
					set @ctl_summary_count = 0;
                    set @ctl_summary_gid = 0;
					Select ifnull(count(ctlsummary_gid),0),ifnull(ctlsummary_status,''),ifnull(ctlsummary_gid,0) into @ctl_summary_count,@ctl_summary_status,@ctl_summary_gid
					from gal_trn_tctlsummary where ctlsummary_version = @Ctrl_Version
					and ctlsummary_ctltype = 'STOCK' and  date_format(create_date,'%Y-%b-%d') = date_format(current_date(),'%Y-%b-%d')  ;

                   if @ctl_summary_count = 0 then
							call sp_ControlSheet_Set('INSERT','SUMMARY_INSERT','',@lj_Summary_Data,'{}',lj_Classification,li_Create_By,@Message);
							select @Message into @Out_Msg_Summary;
					elseif  @Summary_Status = 'NOT_MATCHED'    and @ctl_summary_status = 'FULLY_MATCHED'  then

                             set @lj_Summary_Data = '';
							set @lj_Summary_Data = concat('
								{"Ctl_Type":"STOCK",
								"Ctl_Status":"',@Summary_Status,'",
								"Ctl_Version":',@Ctrl_Version,',
                                "Ctl_Summary_Gid":"',@ctl_summary_gid,'"
								}
								');

                            call sp_ControlSheet_Set('UPDATE','SUMMARY_UPDATE','',@lj_Summary_Data,'{}',lj_Classification,li_Create_By,@Message);
							select @Message into @Out_Msg_Summary;
                     elseif @ctl_summary_count > 0 then
                           set @Out_Msg_Summary = 'SUCCESS';
                   End if;



					if @Out_Msg_Summary = 'SUCCESS' then
							set Message = 'SUCCESS';
					 else
						  set Message = concat('Error Occured On Summary Save - ',@Out_Msg_Summary);
						  rollback;
						  leave sp_ControlSheetProcess_Set;
					End if;


        if Message = 'SUCCESS' then
				commit;
                set Message = 'SUCCESS';
        End if;

End if;

END