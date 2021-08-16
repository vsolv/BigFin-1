CREATE DEFINER=`developer`@`%` PROCEDURE `sp_APInvoice_Set`(In `Action` Varchar(64),In `Type` Varchar(64),
In `lj_Header` json, In `lj_Details` json,In `lj_Debits` json,In `lj_Status` json,
in `li_create_by` int,in `li_entity_gid` int,
Out `Message` varchar(1024)
 )
sp_APInvoice_Set:BEGIN
# Ramesh : 2018-May-12
# Rames : Edit : Nov 2018 : EDIT.
# Action : Insert, Update, 
# Type : Invoice,Advance, Remove_ALL, 
## Ramesh FA - Edit Oct 2019
declare Query_Insert varchar(1000); 
declare Query_Update varchar(1000);
declare countRow int;
declare Updated_Row int;
declare errno int;
declare msg varchar(1000);
#declare ls_INW_code varchar(16);
declare Query_column varchar(1000);
declare Query_value varchar(1000);
declare Query_Count varchar(1000);
declare i int;
declare j int;
declare update_count int;
declare dedupe_invoice varchar(128);
declare CR_NO varchar(128);
Declare Inwarddetails_Count  int;
Declare Invoice_Count int;

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
    
#SET autocommit = 0; 
#start transaction;    

if Type = 'INVOICE_HEADER' then

	select JSON_LENGTH(lj_Header,'$.HEADER') into @li_jsonHeader_count;
      
			
		if @li_jsonHeader_count = 0 or @li_jsonHeader_count is null  then
			set Message = 'No Data In Json For Invoice Process In Header Data.';            
			leave sp_APInvoice_Set;
		End if;   
	
		select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Invoice_Type[0]'))) into @Invoice_Type;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Supplier_gid[0]'))) into @Supplier_gid;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Sup_state_gid[0]'))) into @Sup_state_gid;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Inwarddetails_gid[0]'))) into @Inwarddetails_gid;        #
        select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Is_GST[0]'))) into @Is_GST;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Invoice_Date[0]'))) into @Invoice_Date;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Invoice_No[0]'))) into @Invoice_No;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Invoice_Other_Amount[0]'))) into @Invoice_Other_Amount;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Invoice_Tot_Amount[0]'))) into @Invoice_Tot_Amount;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Supplier_GST_No[0]'))) into @Supplier_GST_No;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Header_Status[0]'))) into @Header_Status;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Remark[0]'))) into @Remark;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Reprocessed[0]'))) into @Reprocessed;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Employee_gid[0]'))) into @Emp_gid;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].branch_gid[0]'))) into @Branch_gid;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].IS_ECF[0]'))) into @IS_ECF;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].ECF_NO[0]'))) into @ECF_NO;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].BAR_CODE[0]'))) into @BAR_CODE;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].RMU_CODE[0]'))) into @RMU_CODE;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].BANK_CODE[0]'))) into @BANK_CODE;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Due_Adjustment[0]'))) into @Due_Adjustment;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Advance_incr[0]'))) into @Advance_incr;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Is_onward[0]'))) into @Is_onward;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Is_amort[0]'))) into @Is_amort;

        
        
       if Action <> 'DELETE' then
			set @Invoice_Date = @Invoice_Date;
			## validation Pending.
        
			if @Inwarddetails_gid is null or @Invoice_Type is null or  @Supplier_gid is null 
                     or @Is_GST is null or @Invoice_Date is null or @Invoice_No is null or  @Invoice_Tot_Amount is null 
                     or @Header_Status is null or @BAR_CODE is null or @RMU_CODE is null then
				set Message = 'Some Values Is Null In Json Data.'; 
				leave sp_APInvoice_Set;
			End if;   
        
        if @Inwarddetails_gid = 0  or @Invoice_Tot_Amount = 0 then
			set Message = 'Some Values Is Zero In Json Data.';
            leave sp_APInvoice_Set;
        End if;
        
        if Action = 'INSERT' then
			set Query_column = '';
			set Query_value = '';
			set Query_Insert = '';
          select count(*) into @invoicechk from ap_trn_tinvoiceheader where invoiceheader_invoiceno =@Invoice_No
           and invoiceheader_suppliergid = @Supplier_gid and invoiceheader_isremoved = 'N' 
           and invoiceheader_status <> 'Rejected' and invoiceheader_invoicedate =@Invoice_Date ;
         if @invoicechk > 0 and @Invoice_No<>"PPX-no" and @Invoice_No > 0 then 
         set Message = 'INVOICE ALREADY EXISTS.';
                    rollback;
                    leave sp_APInvoice_Set;
         end if;
			set dedupe_invoice =  regex_replace('DEDUBE','[^A-Za-z0-9]', '', @Invoice_No);
         
         if @Invoice_Type = 'PO' then
			set @inv_type_code = 'PO' ;
            set @code_no = '500';
             set @code_start = 'CR';
		elseif @Invoice_Type = 'Non PO' then
			set @inv_type_code = 'Non PO' ;	
            set @code_no = '000';
            set @code_start = 'CR';
		elseif @Invoice_Type = 'PPX' then
			set @inv_type_code = 'PPX' ;	
            set @code_no = '001';
            set @code_start = 'PPX';
		elseif @Invoice_Type = 'EMP Claim' then
			set @inv_type_code = 'EMP Claim' ;	
            set @code_no = '500';
            set @code_start = 'PPX';		
		elseif @Invoice_Type = 'BRANCH EXP' then
			set @inv_type_code = 'BRANCH EXP' ;	
            set @code_no = '002';
            set @code_start = 'CR';
      	
		elseif @Invoice_Type = 'IMPREST' then
			set @inv_type_code = 'IMPREST' ;	
            set @code_no = '4000';
            set @code_start = 'IM';
            set @Invoice_Type = 'IMPREST';
		elseif @Invoice_Type = 'AMORT' then
			set @inv_type_code = 'AMORT' ;	
            set @code_no = '7000';
            set @code_start = 'AM';
            set @Invoice_Type = 'AMORT'; 
		elseif @Invoice_Type = 'SI' then
			set @inv_type_code = 'SI' ;	
            set @code_no = '8000';
            set @code_start = 'SI';
            set @Invoice_Type = 'SI';     
            
         End if;
         # 
         #select @inv_type_code;
         set @CRcode = concat('select ifnull(max(SUBSTRING(invoiceheader_crno,-4)),0) into @code1 from ap_trn_tinvoiceheader
							where 	invoiceheader_isremoved = ''N''	and invoiceheader_invoicetype = ''',@inv_type_code,'''
					          and invoiceheader_crno not like ''ECF%'' and date_format(create_date,''%Y-%m-%d'') = curdate() ' );
	#select @CRcode;
			PREPARE stmt1 FROM @CRcode;
			EXECUTE stmt1;  
			DEALLOCATE PREPARE stmt1;
			#select @code1;
			#call sp_Generatecode_Get('WITH_DATE',@code_start,@code_no,@code1,@Message);
            #select @BANK_CODE,@code_no,@code1;
			call sp_Generatecode_Get('WITH_DATE',@BANK_CODE,@code_no,@code1,@Message);
			select @Message into CR_NO from dual;    
         
         
			if @Remark <> '' then
				set Query_column = concat(Query_column , ' invoiceheader_remarks,');
				set Query_value = concat(Query_value , '''',@Remark,''',');
			else 
				set Query_column = concat(Query_column,'');
				set Query_value = concat(Query_value,'');
			end if;	       
            
            if @Invoice_Other_Amount <> 0 then
				set Query_column = concat(Query_column , ' invoiceheader_otheramount,');
				set Query_value = concat(Query_value , '''',@Invoice_Other_Amount,''',');
			else 
				set Query_column = concat(Query_column,'');
				set Query_value = concat(Query_value,'');
            end if;
            
            if @Emp_gid <> '' then
               set Query_column = concat(Query_column , ' invoiceheader_employeegid,');
				set Query_value = concat(Query_value , '''',@Emp_gid,''',');
			else 
				set Query_column = concat(Query_column,'');
				set Query_value = concat(Query_value,'');
            end if;
            
            if @Is_onward <> '' then
               set Query_column = concat(Query_column , ' invoiceheader_onwardinvoice,');
				set Query_value = concat(Query_value , '''',@Is_onward,''',');
			else 
				set Query_column = concat(Query_column,'');
				set Query_value = concat(Query_value,'');
            end if;           
            if @Is_amort <> '' then
               set Query_column = concat(Query_column , ' invoiceheader_amortinvoice,');
				set Query_value = concat(Query_value , '''',@Is_amort,''',');
			else 
				set Query_column = concat(Query_column,'');
				set Query_value = concat(Query_value,'');
            end if;
            
			if @BAR_CODE <> '' then
               set Query_column = concat(Query_column , ' invoiceheader_barcode,');
				set Query_value = concat(Query_value , '''',@BAR_CODE,''',');
			else 
				set Query_column = concat(Query_column,'');
				set Query_value = concat(Query_value,'');
            end if;
            
			if @RMU_CODE <> '' then
               set Query_column = concat(Query_column , ' invoiceheader_rmubarcode,');
				set Query_value = concat(Query_value , '''',@RMU_CODE,''',');
			else 
				set Query_column = concat(Query_column,'');
				set Query_value = concat(Query_value,'');
            end if;
            
			if @IS_ECF = 'Y' then
               set Query_column = concat(Query_column , ' invoiceheader_crno,');
				set Query_value = concat(Query_value , '''',@ECF_NO,''',');
			else 
				set Query_column = concat(Query_column,'invoiceheader_crno,');
				set Query_value = concat(Query_value,'''',CR_NO,''',');
            end if;
      
                                
                                
         set Query_Insert = Concat('Insert into ap_trn_tinvoiceheader(invoiceheader_inwarddetailsgid,invoiceheader_invoicetype,
								invoiceheader_suppliergid,invoiceheader_supplierstategid,invoiceheader_gst,
                                invoiceheader_invoicedate,invoiceheader_invoiceno,invoiceheader_dedupeinvoiceno,
                                ',Query_column,'invoiceheader_amount,invoiceheader_branchgid,invoiceheader_status,invoiceheader_dueadjustment,invoiceheader_ppx,entity_gid,create_by)
								values(',@Inwarddetails_gid,',''',@Invoice_Type,''',',@Supplier_gid,',
                                ',@Sup_state_gid,',''',@Is_GST,''',
                                ''',@Invoice_Date,''',''',@Invoice_No,''',''',dedupe_invoice,''',',Query_value,'
                                ',@Invoice_Tot_Amount,',''',@Branch_gid,''',''',@Header_Status,''',''',@Due_Adjustment,''',''',@Advance_incr,''',',li_entity_gid,',',li_create_by,'
                                )'
                                );
                                
                        
                  
				set @Insert_query = Query_Insert;				
				#select Query_Insert;
                PREPARE stmt FROM @Insert_query;
				EXECUTE stmt;  
				set countRow = (select ROW_COUNT());
				DEALLOCATE PREPARE stmt;           
                
                if countRow >  0 then
					select LAST_INSERT_ID() into @li_Header_gid_Max ;
                    
                    #Insert In ttran
                    set @ls_Remarks = '';
					 call sp_Trans_Set('Insert','AP_INVOICE',@li_Header_gid_Max,'NEW','I','MAKER',@ls_Remarks,
                     li_entity_gid,li_create_by,@message);
						select @message into @tran;
                        
					if @tran <>0 or @tran <> '' then
						set Message = @tran;
                        if @IS_ECF = 'Y' then
                        SET SQL_SAFE_UPDATES = 0;
							Update ecf_trn_tinvoiceheader  set invoiceheader_status = 'APProcess' 
								where invoiceheader_crno = @ECF_NO ;
                           if @Invoice_Type = 'AMORT' then
								set Message = CONCAT(@li_Header_gid_Max,',SUCCESS');	
                                commit;
                                leave sp_APInvoice_Set;
                           end if;
                                
                        end if;        
						#commit;
					else
						set Message = 'FAIL in tran';
						rollback;
					end if;	
			#Tran   
            
			#### Inward Details Status Changed.
				 select count(invoiceheader_gid) into @Invoice_Count from ap_trn_tinvoiceheader where invoiceheader_isactive = 'Y'
					and invoiceheader_isremoved = 'N' and invoiceheader_inwarddetailsgid = @Inwarddetails_gid 
					and entity_gid = li_entity_gid;
                
                select @Invoice_Count;
               # select inwarddetails_count into @Inwarddetails_Count from inw_trn_tinwarddetails 
                #where inwarddetails_isactive = 'Y' 
				#	and inwarddetails_isremoved = 'N' and inwarddetails_gid = 2
                 #   and entity_gid = 1 ;    
                    
                  set Query_Count = concat('select inwarddetails_count into @Inwarddetails_Count 
							from inw_trn_tinwarddetails 
							where inwarddetails_isactive = ''Y'' 
							and inwarddetails_isremoved = ''N'' and inwarddetails_gid = ',@Inwarddetails_gid,'
							and entity_gid = ',li_entity_gid,'' );  
                    
                    set @Query_Count = Query_Count;				
				#select Query_Insert;
                PREPARE stmt FROM @Query_Count;
				EXECUTE stmt;  
				set countRow = (select found_rows());
				DEALLOCATE PREPARE stmt;                        
                    
                  #   select Inwarddetails_Count,Invoice_Count,@Inwarddetails_gid,@Inwarddetails_Count;
                   # leave sp_APInvoice_Set;
                
                 set Inwarddetails_Count = @Inwarddetails_Count;   
                set Invoice_Count = @Invoice_Count;
                
                if Inwarddetails_Count > Invoice_Count then
					set @Inward_Details_Status = 'Partial';
                elseif  Inwarddetails_Count = Invoice_Count then
					set @Inward_Details_Status = 'Completed';
                else 
					set Message = 'Error On Inward Detail Status Generate.';
                    #select Inwarddetails_Count,Invoice_Count,@Inwarddetails_gid,@Inwarddetails_Count;
                    rollback;
                    leave sp_APInvoice_Set;
                End if;
                                
               if  ( select inwarddetails_status from inw_trn_tinwarddetails 
                       where inwarddetails_gid = @Inwarddetails_gid) = @Inward_Details_Status then
                  
                  set Message = '';
                
                else  
                 
					Update inw_trn_tinwarddetails set inwarddetails_status = @Inward_Details_Status
					where inwarddetails_gid = @Inwarddetails_gid ;
					
					set countRow = 0 ;
					set countRow = (select ROW_COUNT());
					
					if countRow = 0 then
						set Message = 'Error On Inward Status Update.';
						rollback;
						leave sp_APInvoice_Set;
					End if;
                end if;                      
                    
            ### Inward Status Ends            
            
            
						set Message = CONCAT(@li_Header_gid_Max,',SUCCESS');			
				else
					set Message = 'FAIL IN HEADER INSERT.';   ### Error On Header Insert
					rollback;
				end if;
         
		elseif Action = 'UPDATE' then
				select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Invoice_Header_Gid[0]'))) into @Invoice_Header_Gid;
                ## Validation Of Json Data
                
                if @Invoice_Header_Gid is null or @Invoice_Header_Gid <= 0 then
						set Message = 'Invoice Header Gid Is Needed To Update.';
                        leave sp_APInvoice_Set;
                End if;
                
                select ifnull(invoiceheader_status,'') into @Inv_Header_Status from ap_trn_tinvoiceheader where invoiceheader_gid = @Invoice_Header_Gid;    
                
                if @Inv_Header_Status <> '' and @Inv_Header_Status <> 'REPROCESS' then
					set Message = 'Only Reprocessed Data Can Be Edited.';
                    leave sp_APInvoice_Set;
                End if;
                                
                set Query_Update = '';
                
                set Query_Update = concat('Update ap_trn_tinvoiceheader set update_by = ',li_create_by,', ');
                
                if @Invoice_Type <> '' then
					set Query_Update = concat(Query_Update, ' invoiceheader_invoicetype = ''',@Invoice_Type,''', ');
                End if;
                
                  if @Sup_state_gid <> 0 then
					set Query_Update = concat(Query_Update, ' invoiceheader_supplierstategid = ',@Sup_state_gid,', ');
                End if;
                
                  if @Is_GST <> '' then
					set Query_Update = concat(Query_Update, ' invoiceheader_gst = ''',@Is_GST,''', ');
                End if;
                                 
                  if @Invoice_Date <> '' then
					set Query_Update = concat(Query_Update, ' invoiceheader_invoicedate = ''',@Invoice_Date,''', ');
                End if;
                
                  if @Invoice_No <> '' then
					set Query_Update = concat(Query_Update, ' invoiceheader_invoiceno = ''',@Invoice_No,''', ');
                    
                    set dedupe_invoice =  regex_replace('DEDUBE','[^A-Za-z0-9]', '', @Invoice_No);
                    
                    set Query_Update = concat(Query_Update, ' invoiceheader_dedupeinvoiceno = ''',dedupe_invoice,''', '); 
                    
                End if;
					
                  if @Invoice_Tot_Amount <> '' then
					set Query_Update = concat(Query_Update, ' invoiceheader_amount = ''',@Invoice_Tot_Amount,''', ');
                End if;    
                
                  if @Supplier_GST_No <> '' then
					set Query_Update = concat(Query_Update, ' invoiceheader_gst = ''',@Is_GST,''', ');
                End if;    
                
               set Query_Update = concat(Query_Update, 'Update_date = current_timestamp()  where invoiceheader_gid = ',@Invoice_Header_Gid,'  ' );
                   
                   
                   
                    set @Query_Update = '';
					set @Query_Update = Query_Update;		                
                   #select @Query_Update; ### Remove IT
					PREPARE stmt FROM @Query_Update;
					EXECUTE stmt;  
					set countRow = (select ROW_COUNT());
					DEALLOCATE PREPARE stmt;                         
                    
					if countRow <= 0 then
						set Message = 'Error On Invoice Header Update.';
                        rollback;
                        leave sp_APInvoice_Set;
                     elseif    countRow > 0 then
						set Message = 'SUCCESS';
                    End if;

                
        End if;
		
       # commit;
     
     End if; # Check is Delete Ends            



elseif Type = 'INVOICE_DETAILS' then
	
    set i = 0 ;
 
	select JSON_LENGTH(lj_Details,'$.DETAIL') into @li_jsonDetail_count;  
    
    if  @li_jsonDetail_count is null or @li_jsonDetail_count = 0 then
			set Message = 'No Data In Json For Invoice Process In Details Data.';            
			leave sp_APInvoice_Set;
	End if;  
    

		WHILE i <= @li_jsonDetail_count - 1 DO
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].Item_Name[0]'))) into @Item_Name;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].Description[0]'))) into @Description;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].HSN_Code[0]'))) into @HSN_Code;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].Unit_Price[0]'))) into @Unit_Price;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].Quantity[0]'))) into @Quantity;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].Amount[0]'))) into @Amount;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].IGST[0]'))) into @IGST;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].CGST[0]'))) into @CGST;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].SGST[0]'))) into @SGST;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].Total_Amount[0]'))) into @Total_Amount;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].Discount[0]'))) into @Discount;
            
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].PO_Header_Gid[0]'))) into @PO_Header_Gid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].PO_Detail_Gid[0]'))) into @PO_Detail_Gid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].GRN_Header_Gid[0]'))) into @GRN_Header_Gid;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].GRN_Detail_Gid[0]'))) into @GRN_Detail_Gid;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].Invoice_Header_gid[0]'))) into @li_Header_gid_Max;            
            
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].Invoice_Sno[0]'))) into @Invoice_Sno; 
            
		   #  select @li_Header_gid_Max,@Item_Name,@Description,@HSN_Code,@Unit_Price,@Discount,@Amount,@Total_Amount,@IGST,@CGST;

             if Action <> 'DELETE' then
				## validation Pending
                ## Check for Null Value too
                if Action = 'INSERT' then
					set @IGST =  ROUND( @IGST,2);
					set @CGST =  ROUND( @CGST,2);
					set @SGST =  ROUND( @SGST,2);
					set Query_column = '';
					set Query_value = '';
					set Query_Insert = '';
					set Query_Insert = Concat('Insert into ap_trn_tinvoicedetails (invoicedetails_headergid,invoicedetails_item,
						invoicedetails_desc,invoicedetails_hsncode,invoicedetails_unitprice,invoicedetails_qty,invoicedetails_discount,invoicedetails_taxamt,
						invoicedetails_amount,invoicedetails_totalamt,invoicedetails_igst,invoicedetails_cgst,invoicedetails_sgst,
                        entity_gid,create_by)
                        Values(',@li_Header_gid_Max,',''',@Item_Name,''',''',@Description,''',''',@HSN_Code,''',
                        ''',@Unit_Price,''',''',@Quantity,''',''',@Discount,''',''0'',''',@Amount,''',''',@Total_Amount,''',
                        ''',@IGST,''',''',@CGST,''',''',@SGST,''',
                        ',li_entity_gid,',',li_create_by,')'
											);		 
                                            
					set @Insert_Detail_query = Query_Insert;		
				# select Query_Insert; ## remove It
					PREPARE stmt FROM @Insert_Detail_query;
					EXECUTE stmt;  
					set countRow = (select ROW_COUNT());
					DEALLOCATE PREPARE stmt;                          
                    
                
					if countRow >  0 then
                       
                    
						select LAST_INSERT_ID() into @li_Detail_gid_Max ;
                        if @IGST > 0 then 
                             select tax_gid,subtax_gid,taxrate_rate into @tax_gid,@subtax_gid,@taxrate_rate from  gal_mst_thsn as a 
							inner join gal_mst_ttaxrate as b on b.taxrate_gid = a.hsn_igsttaxrategid
							inner join gal_mst_tsubtax as c on c.subtax_gid = b.taxrate_subtax_gid
							inner join gal_mst_ttax as d on d.tax_gid = c.subtax_tax_gid
							where 
							 a.hsn_isremoved = 'N' and a.hsn_isactive = 'Y'
							and b.taxrate_isremoved = 'N' and b.taxrate_isactive = 'Y'
							and c.subtax_isremoved = 'N' and c.subtax_isactive = 'Y'
							and d.tax_isremoved = 'N' and d.tax_isactive = 'Y'
							and a.entity_gid = li_entity_gid and hsn_code = @HSN_Code;
                        
										
							  set @inv_data = concat('{"TAXINVOICE": [{"taxinvoice_reftablegid": "',@li_Detail_gid_Max,'", "taxinvoice_tax_gid": "',@tax_gid,'",
																	"taxinvoice_subtax_gid":  "',@subtax_gid,'","taxinvoice_rate": "',@taxrate_rate,'","taxinvoice_taxamount": "',@IGST,'",
																	  "debit_amount":1,"taxinvoice_type": "Y","taxinvoice_inputcrtaken": "N"
																		}]}');
																		
                             call sp_Taxinvoice_Set('INSERT','AP_INPUT_TAX',@inv_data,'Y',li_create_by,li_entity_gid,@Message);
								if @Message <> 'SUCCESS' then
										set Message = 'Error On gst Insert.';
										rollback;
										leave sp_APInvoice_Set;
								End if;
						end if;
                        if @SGST > 0 then 
							select tax_gid,subtax_gid,taxrate_rate into @tax_gid,@subtax_gid,@taxrate_rate from  gal_mst_thsn as a 
							inner join gal_mst_ttaxrate as b on b.taxrate_gid = a.hsn_sgsttaxrategid
							inner join gal_mst_tsubtax as c on c.subtax_gid = b.taxrate_subtax_gid
							inner join gal_mst_ttax as d on d.tax_gid = c.subtax_tax_gid
							where 
							 a.hsn_isremoved = 'N' and a.hsn_isactive = 'Y'
							and b.taxrate_isremoved = 'N' and b.taxrate_isactive = 'Y'
							and c.subtax_isremoved = 'N' and c.subtax_isactive = 'Y'
							and d.tax_isremoved = 'N' and d.tax_isactive = 'Y'
							and a.entity_gid = li_entity_gid and hsn_code = @HSN_Code;
                       
										
							 set @inv_data = concat('{"TAXINVOICE": [{"taxinvoice_reftablegid": "',@li_Detail_gid_Max,'", "taxinvoice_tax_gid": "',@tax_gid,'",
																	"taxinvoice_subtax_gid":  "',@subtax_gid,'","taxinvoice_rate": "',@taxrate_rate,'","taxinvoice_taxamount": "',@SGST,'",
																	  "debit_amount":1,"taxinvoice_type": "Y","taxinvoice_inputcrtaken": "N"
																		}]}');
																		
                             call sp_Taxinvoice_Set('INSERT','AP_INPUT_TAX',@inv_data,'Y',li_create_by,li_entity_gid,@Message);
                                                                  
								if @Message <> 'SUCCESS' then
										set Message = 'Error On gst Insert.';
										rollback;
										leave sp_APInvoice_Set;
								End if;
						end if;
                        if @CGST > 0 then 
							select tax_gid,subtax_gid,taxrate_rate into @tax_gid,@subtax_gid,@taxrate_rate from  gal_mst_thsn as a 
							inner join gal_mst_ttaxrate as b on b.taxrate_gid = a.hsn_cgsttaxrategid
							inner join gal_mst_tsubtax as c on c.subtax_gid = b.taxrate_subtax_gid
							inner join gal_mst_ttax as d on d.tax_gid = c.subtax_tax_gid
							where 
							 a.hsn_isremoved = 'N' and a.hsn_isactive = 'Y'
							and b.taxrate_isremoved = 'N' and b.taxrate_isactive = 'Y'
							and c.subtax_isremoved = 'N' and c.subtax_isactive = 'Y'
							and d.tax_isremoved = 'N' and d.tax_isactive = 'Y'
							and a.entity_gid = li_entity_gid and hsn_code = @HSN_Code;
							  				
							 set @inv_data = concat('{"TAXINVOICE": [{"taxinvoice_reftablegid": "',@li_Detail_gid_Max,'", "taxinvoice_tax_gid": "',@tax_gid,'",
																	"taxinvoice_subtax_gid":  "',@subtax_gid,'","taxinvoice_rate": "',@taxrate_rate,'","taxinvoice_taxamount": "',@CGST,'",
																	  "debit_amount":1,"taxinvoice_type": "Y","taxinvoice_inputcrtaken": "N"
																		}]}');
																		
                             call sp_Taxinvoice_Set('INSERT','AP_INPUT_TAX',@inv_data,'Y',li_create_by,li_entity_gid,@Message);
                                                                  
								if @Message <> 'SUCCESS' then
										set Message = 'Error On gst Insert.';
										rollback;
										leave sp_APInvoice_Set;
								End if;
						end if;
                        
                        if @PO_Header_Gid <> 0 then # It will Change
							set Query_Insert = '';   
							set Query_Insert = Concat('insert into ap_map_tinvoicepo(invoicepo_invoiceheadergid,
											invoicepo_invoicedetailsgid,invoicepo_poheadergid,invoicepo_podetailsgid,
                                            invoicepo_grninwardheadergid,invoicepo_grninwarddetailsgid,
											invoicepo_qty,entity_gid,create_by)
											values(',@li_Header_gid_Max,',',@li_Detail_gid_Max,',',@PO_Header_Gid,',
                                            ',@PO_Detail_Gid,',',@GRN_Header_Gid,',',@GRN_Detail_Gid,',''',@Quantity,''',
                                             ',li_entity_gid,',',li_create_by,')'
												);
                                         #select Query_Insert; ## Remove It       
                                set @Insert_Detail_query = Query_Insert;				
								
                                PREPARE stmt FROM @Insert_Detail_query;
								EXECUTE stmt;  
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;                                    
								
                            #    select countRow; ## Remove It
                                 if countRow >  0 then
									#select LAST_INSERT_ID() into @li_Header_gid_Max ;
									set Message = 'SUCCESS';
								else
									set Message = 'FAIL IN INVOICE MAP.';
									rollback;
								end if;
                        elseif @PO_Header_Gid = '' or @PO_Header_Gid is null then
                          set Message = 'Problem With Data In Checking PO or Non PO.';
                          leave sp_APInvoice_Set;
                          
                        else
                          set Message = 'SUCCESS';
                        end if;## Map Insert Check
                        
					else
						set Message = 'FAIL IN INVOICE DETAILS.';
						rollback;
					end if;              
                    
                    
                    #### To Insert Debit Start.
                    
                     select JSON_LENGTH(lj_Debits,'$.DEBIT') into @li_json_debit_count;
							if @li_json_debit_count is null or @li_json_debit_count = 0 then
								set Message = 'No Data In Json - Debit.';
								leave sp_APInvoice_Set;
							end if;
						
                   set j = 0 ;
                   
                   WHILE j <= @li_json_debit_count - 1 DO
					set lj_Debits =  JSON_SET(lj_Debits,CONCAT('$.DEBIT[',j,'].Invoice_Details_Gid[0]'),@li_Detail_gid_Max);
                    set j = j + 1;
                   END WHILE;
                    
                    
                    call sp_APDebit_Set('Insert','',lj_Debits,'N',@Invoice_Sno,li_create_by,li_entity_gid,@Message);
						Select @Message;
                        
                        select @Message into @Out_message_debits;
                        
                        if @Out_message_debits <> 'SUCCESS' then
							set Message = 'FAIL';
                            leave sp_APInvoice_Set;
                        End if;
						
                    #### To Insert Debit Ends
	
		elseif Action = 'UPDATE' then
                     select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].EDIT[0]'))) into @EDIT;       
                     
                     if @EDIT is not null and @EDIT = 'INSERT' then
							###  Insert while Update Starts.. :: Same as Insert : Copied.
								set Query_column = '';
								set Query_value = '';
								set Query_Insert = '';
								set Query_Insert = Concat('Insert into ap_trn_tinvoicedetails (invoicedetails_headergid,invoicedetails_item,
									invoicedetails_desc,invoicedetails_hsncode,invoicedetails_unitprice,invoicedetails_qty,
									invoicedetails_amount,invoicedetails_totalamt,invoicedetails_igst,invoicedetails_cgst,invoicedetails_sgst,
									entity_gid,create_by)
									Values(',@li_Header_gid_Max,',''',@Item_Name,''',''',@Description,''',''',@HSN_Code,''',
									''',@Unit_Price,''',''',@Quantity,''',''',@Amount,''',''',@Total_Amount,''',
									''',@IGST,''',''',@CGST,''',''',@SGST,''',
									',li_entity_gid,',',li_create_by,')'
											);		 
                                            
                                            
                                            select @HSN_Code;
                                            
									set @Insert_Detail_query = Query_Insert;		
									  select Query_Insert; ## remove It
									PREPARE stmt FROM @Insert_Detail_query;
									EXECUTE stmt;  
									set countRow = (select ROW_COUNT());
									DEALLOCATE PREPARE stmt;                          
                
                
								if countRow >  0 then
										select LAST_INSERT_ID() into @li_Detail_gid_Max ;                           
									if @PO_Header_Gid <> 0 then # It will Change
											set Query_Insert = '';   
											set Query_Insert = Concat('insert into ap_map_tinvoicepo(invoicepo_invoiceheadergid,
											invoicepo_invoicedetailsgid,invoicepo_poheadergid,invoicepo_podetailsgid,
                                            invoicepo_grninwardheadergid,invoicepo_grninwarddetailsgid,
											invoicepo_qty,entity_gid,create_by)
											values(',@li_Header_gid_Max,',',@li_Detail_gid_Max,',',@PO_Header_Gid,',
                                            ',@PO_Detail_Gid,',',@GRN_Header_Gid,',',@GRN_Detail_Gid,',''',@Quantity,''',
                                             ',li_entity_gid,',',li_create_by,')'
												);
                                         #select Query_Insert; ## Remove It       
											set @Insert_Detail_query = Query_Insert;				
								
											PREPARE stmt FROM @Insert_Detail_query;
											EXECUTE stmt;  
											set countRow = (select ROW_COUNT());
											DEALLOCATE PREPARE stmt;                                    
								
											#    select countRow; ## Remove It
											if countRow >  0 then
												#select LAST_INSERT_ID() into @li_Header_gid_Max ;
												set Message = 'SUCCESS';
											else
												set Message = 'FAIL IN INVOICE MAP.';
												rollback;
											end if;
								elseif @PO_Header_Gid = '' or @PO_Header_Gid is null then
										set Message = 'Problem With Data In Checking PO or Non PO.';
										leave sp_APInvoice_Set;
                          
								else
									set Message = 'SUCCESS';
								end if;## Map Insert Check
                        
						else
							set Message = 'FAIL'; ## Fail on detail Insert
							rollback;
                            	leave sp_APInvoice_Set;
						end if;                                 
                    
                    #### To Insert Debit Start.                    
                     select JSON_LENGTH(lj_Debits,'$.DEBIT') into @li_json_debit_count;                     
                        
							if @li_json_debit_count is null or @li_json_debit_count = 0 then
								set Message = 'No Data In Json - Debit.';
								leave sp_APInvoice_Set;
							end if;
						
                   set j = 0 ;                  
                   
                   WHILE j <= @li_json_debit_count - 1 DO
					set lj_Debits =  JSON_SET(lj_Debits,CONCAT('$.DEBIT[',j,'].Invoice_Details_Gid[0]'),@li_Detail_gid_Max);
                    set j = j + 1;
                   END WHILE;
                    
                    
                    call sp_APDebit_Set('Insert','',lj_Debits,'N',@Invoice_Sno,li_create_by,li_entity_gid,@Message);
						Select @Message;
                        
                        select @Message into @Out_message_debits;
                        
                        if @Out_message_debits <> 'SUCCESS' then
							#set Message = 'FAIL IN DEBITsdfdsfdsfsdfsd.'; ## Remove it ## To DO To Remove
                            leave sp_APInvoice_Set;
                        End if;
						
                    #### To Insert Debit Ends
                            ### Insert while Update Ends.
                            
                     elseif @EDIT = 'UPDATE' then
							select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].Inv_Details_Gid[0]'))) into @Inv_Details_Gid; 
                            select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].Is_Removed[0]'))) into @Is_Removed; 
                            
                            if @Inv_Details_Gid is null and @Inv_Details_Gid <= 0 then
								set Message = 'Invoice Detail Gid Is Needed To Upadte.';
                                rollback;
                                leave sp_APInvoice_Set;
                            End if;
                            
						if @Is_Removed is not null and @Is_Removed = 'Y' then
								 
									update ap_trn_tinvoicedetails set invoicedetails_isactive = 'N' , invoicedetails_isremoved = 'Y' ,
									update_by = li_create_by,Update_date = current_timestamp()
									where invoicedetails_gid = @Inv_Details_Gid ;
                                    
                                    	
										set countRow = (select ROW_COUNT());
										
									if countRow = 0 then
										set Message = 'Error On Invoice Detail Remove.';
										rollback;
										leave sp_APInvoice_Set;
									end if;
                                        
                                        
										SET SQL_SAFE_UPDATES = 0;
										update ap_trn_tdebit set debit_isactive = 'N', debit_isremoved = 'Y' ,update_by = li_create_by,Update_date = current_timestamp()
										where debit_invoicedetailsgid = @Inv_Details_Gid    ;
                                    
                                    	set countRow = (select ROW_COUNT());
										
									if countRow = 0 then
										set Message = 'Error On Invoice Debit  Remove.';
										rollback;
										leave sp_APInvoice_Set;
									end if;
                                  
                                 if @PO_Header_Gid <> 0 and @PO_Header_Gid > 0 and @PO_Header_Gid is not null  then
											SET SQL_SAFE_UPDATES = 0;
									update ap_map_tinvoicepo set invoicepo_isactive = 'N',invoicepo_isremoved = 'Y' ,update_by = li_create_by,
									Update_date = current_timestamp() where invoicepo_invoicedetailsgid = @Inv_Details_Gid    ;
                                 
									set countRow = (select ROW_COUNT());
										
									if countRow = 0 then
										set Message = 'Error On Invoice Map  Remove.';
										rollback;
										leave sp_APInvoice_Set;
									end if;
                                 End if;
										
									
                                    
						elseif  @Is_Removed is not null and @Is_Removed = 'N' then
								
									set Query_Update = '';
									set Query_Update = concat('update ap_trn_tinvoicedetails set update_by = ',li_create_by,',');
                                
									if @Item_Name <> '' then
										set Query_Update = concat(Query_Update, ' invoicedetails_item = ''',@Item_Name,''', '  );
									End if;
                                
									if @Description <> '' then
										set Query_Update = concat(Query_Update, ' invoicedetails_desc = ''',@Description,''', '  );
									End if;
                                   
									if @HSN_Code <> '' then
										set Query_Update = concat(Query_Update, ' invoicedetails_hsncode = ''',@HSN_Code,''', '  );
									End if;
                                   
									if @Unit_Price <> '' then
										set Query_Update = concat(Query_Update, ' invoicedetails_unitprice = ''',@Unit_Price,''', '  );
									End if;
                                   
									if @Quantity <> '' then
										set Query_Update = concat(Query_Update, ' invoicedetails_qty = ''',@Quantity,''', '  );
									End if;
                                   
									if @Amount <> '' then
										set Query_Update = concat(Query_Update, ' invoicedetails_amount = ''',@Amount,''', '  );
									End if;
                                   
									if @IGST <> '' then
										set Query_Update = concat(Query_Update, ' invoicedetails_igst = ''',@IGST,''', '  );
									End if;
                                
									if @CGST <> '' then
										set Query_Update = concat(Query_Update, ' invoicedetails_cgst = ''',@CGST,''', '  );
									End if;
                                
									if @SGST <> '' then
										set Query_Update = concat(Query_Update, ' invoicedetails_sgst = ''',@SGST,''', '  );
									End if;
                                    
									if @Total_Amount <> '' then
										set Query_Update = concat(Query_Update, ' invoicedetails_totalamt = ''',@Total_Amount,''', '  );
									End if;    
                                
									set Query_Update = concat(Query_Update, ' Update_date = current_timestamp() where invoicedetails_gid = ',@Inv_Details_Gid,' ' );
                                
											set @Query_Update = '';
											set @Query_Update = Query_Update;		 
                                             #select Query_Update;  # Remove it
											PREPARE stmt FROM @Query_Update;
											EXECUTE stmt;  
											set countRow = (select ROW_COUNT());
											DEALLOCATE PREPARE stmt;                          

									if countRow <= 0 then
											set Message = 'Error On Invoice Details Update.';
											rollback;
											leave sp_APInvoice_Set;
									elseif    countRow > 0 then
											set Message = 'SUCCESS';
									End if;

                                    
                            End if; ### Check Remove of Alter
                            
                     End if;
                    
                End if;  ### Action Ends
                
                
             End if; ## Check Action delete Ends
                       
            
            
            set i = i + 1;
        END WHILE;  
        
elseif Type = 'STATUS' then
	if Action = 'UPDATE' then
		select JSON_LENGTH(lj_Status,'$') into @li_jsonStatus_count;  
        
        if @li_jsonStatus_count = 0 then
			set Message = 'Status Data Is Needed.';
            leave sp_APInvoice_Set;
        End if;
        
        select JSON_UNQUOTE(JSON_EXTRACT(lj_Status, CONCAT('$.Invoice_Header_Gid[0]'))) into @Header_Gid;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_Status, CONCAT('$.Status[0]'))) into @ls_Status;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_Status, CONCAT('$.Remark[0]'))) into @Remark;
         select fn_AP_Data('MULTIUSER',@Header_Gid,'AP_Invoice',@ls_Status,li_entity_gid,'{}')  into @check_multiuser; 
        if  @check_multiuser = 'FAIL' then
			 set Message = 'ALREADY PROCESSED';
             leave sp_APInvoice_Set;

		end if;
        ## Validate Json Data
        
			Update ap_trn_tinvoiceheader set invoiceheader_status = @ls_Status, 
			update_by = li_create_by, Update_date = now()
			where invoiceheader_gid = @Header_Gid ;            
            
         set Updated_Row = (select ROW_COUNT());
         
       #  select Updated_Row; Remove it
         
         if Updated_Row = 0 then
			set Message = 'Error On Status Update.';
            leave sp_APInvoice_Set;
		 else
          # Tran Starts
          if  @Remark = '' or @Remark is null then
                        set @Remarks = '';

          end if;
          set @tran = '';
                       
			   call sp_Trans_Set('update','AP_INVOICE',@Header_Gid,@ls_Status,'I','CHECKER',@Remarks,li_entity_gid,li_create_by,@message);
                select @message into @tran;
          
          
          
          #select @Header_Gid,@ls_Status,'I',@ls_Status,@Remarks,li_entity_gid,li_create_by,@message;
		#	call sp_Trans_Set('update','AP_INVOICE',@Header_Gid,@ls_Status,'I','CHECKER',@Remarks,li_entity_gid,li_create_by,@message);
        #    select @message into @tran;
         #   select @tran;
            # C Instead Of I if tat is the Last Status.
            # APPROVE Instead Of MAKER if tat is the Last Status.
            #select @tran; # Remove IT
            
            if @tran > 0 or @tran = '' then## Gives Error.. Need to Check
				set Message = 'SUCCESS';
				#commit;
			else
            				set Message = 'SUCCESS';

				set Message = 'FAIL IN TRAN.';
				rollback;
			leave sp_APInvoice_Set;
			end if;
        ## Tran Ends
	
           set Message = 'SUCCESS';
         End if;


   
    End if;


elseif Type = 'FILE' then
      	select JSON_LENGTH(lj_Status,'$') into @li_jsonStatus_count;  
        
        if @li_jsonStatus_count = 0 then
			set Message = 'File Data Is Needed.';
            leave sp_APInvoice_Set;
        End if;
        
        select JSON_UNQUOTE(JSON_EXTRACT(lj_Status, CONCAT('$.Barcode_Name[0]'))) into @Barcodename;
		select JSON_UNQUOTE(JSON_EXTRACT(lj_Status, CONCAT('$.File_name[0]'))) into @ls_Filename;
        ## Validate Json Data
        set @gid = 0;
        select invoiceheader_gid into @gid from ap_trn_tinvoiceheader where
            invoiceheader_barcode = @Barcodename ;
			Update ap_trn_tinvoiceheader set invoiceheader_imagepath = @ls_Filename, 
			update_by = li_create_by, Update_date = now()
			where invoiceheader_gid = @gid ;            
            
         set Updated_Row = (select ROW_COUNT());
         
       #  select Updated_Row; Remove it
         
         if Updated_Row = 0 then
			set Message = 'Error On File Update.';
            leave sp_APInvoice_Set;
		 else
          
           set Message = 'SUCCESS';
           commit;
         End if;
	
elseif Type = 'AMOUNT' then
	
		select JSON_LENGTH(lj_Header,'$.HEADER') into @li_jsonHeader_count;
      
			
		if @li_jsonHeader_count = 0 or @li_jsonHeader_count is null  then
			set Message = 'No Data In Json For Invoice Process In Header Data.';            
			leave sp_APInvoice_Set;
		End if;   
  
			select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Invoice_Other_Amount[0]'))) into @Invoice_Other_Amount;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Invoice_Header_Gid[0]'))) into @Invoice_Header_Gid;
  
		#select Action,@Invoice_Other_Amount,@Invoice_Header_Gid; ## remove It.
  
		if Action = 'UPDATE' then
			if @Invoice_Other_Amount is null or @Invoice_Other_Amount = 0 or @Invoice_Header_Gid is null or @Invoice_Header_Gid = 0  then
				set Message = 'Invoice Other Amount Is Required.';
				leave sp_APInvoice_Set;
			End if;
    
				update ap_trn_tinvoiceheader set invoiceheader_otheramount = @Invoice_Other_Amount , update_by =  li_create_by , Update_date = current_timestamp()
				where invoiceheader_gid = @Invoice_Header_Gid;
    
				set countRow = (select ROW_COUNT());
                	  
			if countRow > 0 then
					set Message = 'SUCCESS';
			else
				set Message = 'FAIL IN INVOICE HEADER.';
				leave sp_APInvoice_Set;
			end if;
    
    End if;


elseif Type = 'Remove_ALL' then

			if Action = 'UPDATE' then
                ### On Clicking The PO --- Delete the Invocie details, Debit and Credit..  
							select JSON_LENGTH(lj_Header,'$.HEADER') into @li_jsonHeader_count;      
			
		                 if @li_jsonHeader_count = 0 or @li_jsonHeader_count is null  then
								set Message = 'No Data In Json For Invoice Process In Header Data.';            
								leave sp_APInvoice_Set;
						End if;   
                        
						select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Invoice_Header_Gid[0]'))) into @Invoice_Header_Gid;
                        
                        ### Get the Invoice Details To Remove flag
							select ifnull(group_concat( distinct invoicedetails_gid),'EMPTY') into @Invoice_Details_gids   from ap_trn_tinvoicedetails 
							where invoicedetails_headergid = @Invoice_Header_Gid and invoicedetails_isactive = 'Y' and invoicedetails_isremoved = 'N'; 
                                                        
                            if @Invoice_Details_gids = 'EMPTY' then
								set Message = 'No Data Found To Delete.';
                                leave sp_APInvoice_Set;
                            End if;
                            ### Update The Invoice Details.[Remove]
                            set countRow = 0 ;                            
                             set Query_Update = '';                
								set Query_Update = concat('Update ap_trn_tinvoicedetails set invoicedetails_isactive = ''N'',invoicedetails_isremoved = ''Y''
                                                 where invoicedetails_gid in (',@Invoice_Details_gids,')  ');                                	
												set @Query_Update = '';
												set @Query_Update = Query_Update;		                
												PREPARE stmt FROM @Query_Update;
												EXECUTE stmt;  
												set countRow = (select ROW_COUNT());
												DEALLOCATE PREPARE stmt;                          

														if countRow <= 0 then
																set Message = 'Error On Invoice Details Remove.';
																rollback;
																leave sp_APInvoice_Set;
														elseif    countRow > 0 then
																	set Message = 'SUCCESS';
														End if;							
                      
                                ### Update the Invocie Po Map
                                ## TO DO - Process for Non PO.
											set countRow = 0 ;
											SET SQL_SAFE_UPDATES = 0;
                                            set countRow = 0 ;                            
											set Query_Update = '';                
											set Query_Update = concat('Update ap_map_tinvoicepo set invoicepo_isactive = ''N'',invoicepo_isremoved = ''Y''
															where invoicepo_invoicedetailsgid in (',@Invoice_Details_gids,')  ');                                	
																set @Query_Update = '';
																set @Query_Update = Query_Update;		                
																PREPARE stmt FROM @Query_Update;
																EXECUTE stmt;  
																set countRow = (select ROW_COUNT());
																DEALLOCATE PREPARE stmt;                          

																		if countRow <= 0 then
																				set Message = 'Error On Invoice Map PO Details Remove.';
																				rollback;
																				leave sp_APInvoice_Set;
																		elseif    countRow > 0 then
																				set Message = 'SUCCESS';
																		End if;							
                      											
                                #### Update The Debit Details[Remove].                                
								
															SET SQL_SAFE_UPDATES = 0;
															set countRow = 0 ;                            
															set Query_Update = '';                
															set Query_Update = concat('Update ap_trn_tdebit set debit_isactive = ''N'',debit_isremoved = ''Y''
																			where debit_invoicedetailsgid in (',@Invoice_Details_gids,')  ');                                	
																				set @Query_Update = '';
																				set @Query_Update = Query_Update;		                
																				PREPARE stmt FROM @Query_Update;
																				EXECUTE stmt;  
																				set countRow = (select ROW_COUNT());
																				DEALLOCATE PREPARE stmt;                          

																		if countRow <= 0 then
																				set Message = 'Error On Debit Details Remove.';
																				rollback;
																				leave sp_APInvoice_Set;
																		elseif    countRow > 0 then
																				set Message = 'SUCCESS';
																		End if;				
																	#### Update the Credit [Remove]
																	set countRow = 0 ;
																	SET SQL_SAFE_UPDATES = 0;
																			update ap_trn_tcredit set credit_isactive = 'N' , credit_isremoved = 'Y' where credit_invoiceheadergid = @Invoice_Header_Gid;
                                
																			set countRow = (select ROW_COUNT());
																				if countRow > 0 then
																							set Message = 'SUCCESS';
																				else
																							set Message = 'FAIL4';
																							rollback;
																							leave sp_APInvoice_Set;
																				end if;
																						#commit;
				End if;## ACTION ENDS
 elseif Type = 'CAPTILIZE_UPDATE' then
        if Action = 'UPDATE' then
				select JSON_LENGTH(lj_Details,'$') into @li_jsonDetail_count;  
    
				if  @li_jsonDetail_count is null or @li_jsonDetail_count = 0 then
						set Message = 'No Data In Json For Invoice Process In Details Data.';            
						leave sp_APInvoice_Set;
				End if;  
                
          select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Invoice_Detail_Gid'))) into @Invoice_Detail_Gid;       
          
          if @Invoice_Detail_Gid is null or @Invoice_Detail_Gid = 0  then
				set Message = 'Invoice Detail Gid Is Needed.';
                leave sp_APInvoice_Set;
          End if;
					SET SQL_SAFE_UPDATES = 0;
									update ap_map_tinvoicepo set invoicepo_capitalised = 'Y' ,update_by = li_create_by,
									Update_date = current_timestamp() where invoicepo_invoicedetailsgid = @Invoice_Detail_Gid    ;
                                 
									set countRow = (select ROW_COUNT());
									#	select countRow;
									if countRow = 0 then
										set Message = 'Error On Invoice Map  Remove.';		
										leave sp_APInvoice_Set;
                                      else 
                                        set Message = 'SUCCESS';
									end if;
								
 
                
        End if;
	  
End if; # Type Ends

END
