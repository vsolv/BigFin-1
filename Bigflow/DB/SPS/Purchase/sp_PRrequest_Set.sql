CREATE DEFINER=`developer`@`%` PROCEDURE `sp_PRrequest_Set`(In `Action` Varchar(64),In `Type` Varchar(64),
In `lj_Header` json, In `lj_Details` json,In `lj_Debits` json,In `lj_Status` json,
in `li_create_by` int,IN `lj_Classification` json,
Out `Message` varchar(1024)
 )
sp_APInvoice_Set:BEGIN
# Ramesh : 2018-May-12
# Rames : Edit : Nov 2018 : EDIT.
# Action : Insert, Update, 
# Type : Invoice,Advance, Remove_ALL, 

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
declare ls_no varchar(64);


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
           

    set Message = 'empty';

elseif Type = 'PR_DETAILS_DRAFT' or Type = 'PR_DETAILS_INSERT'  then
    	  select JSON_LENGTH(lj_Header,'$.HEADER') into @li_jsonHeader_count;
      
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid[0]'))) into @Entity_Gid;
             
             if @Entity_Gid is  null or @Entity_Gid = 0 or @Entity_Gid = '' then
					set Message = 'Entity Gid Is Needed.';
                    leave sp_APInvoice_Set;
             End if;
 
		if @li_jsonHeader_count = 0 or @li_jsonHeader_count is null  then
			set Message = 'No Data In Json For  In Header Data.';            
			leave sp_APInvoice_Set;
		End if;   
	                            
		select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Date[0]'))) into @Datee;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Emp_gid[0]'))) into @Emp_gid;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Statuss[0]'))) into @Statuss;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Branchgid[0]'))) into @Branchgid;        #
        select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Totalamount[0]'))) into @Totalamount;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Commodity_gid[0]'))) into @Commodity_gid;
         select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].dropdown_gid[0]'))) into @dropdown_gid;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].mepno[0]'))) into @mepno;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].header_img[0]'))) into @header_img;
        set Query_column = ' ';
        set Query_value = ' ';
        if  @mepno <> ''  then
		            set Query_column = concat(Query_column , ', prheader_mepno');
                    set Query_value = concat(Query_value , ',''' ,@mepno,'''');
		else 
		            set Query_column = concat(Query_column,'');
                    set Query_value = concat(Query_value,'');
		end if; 
            if  @header_img <> ''  then
		            set Query_column = concat(Query_column , ', prheader_imagepath');
                    set Query_value = concat(Query_value , ',''' ,@header_img,'''');
		else 
		            set Query_column = concat(Query_column,'');
                    set Query_value = concat(Query_value,'');
		end if; 
       if Action <> 'DELETE' then
			set @Datee = @Datee;
			## validation Pending.
        
			if @Datee is null or @Emp_gid is null or  @Statuss is null 
                     or @Branchgid is null or @Totalamount is null or @Commodity_gid is null  then
				set Message = 'Some Values Is Null In Json Data.'; 
				leave sp_APInvoice_Set;
			End if;   
        

        
          if Action = 'INSERT' then
			call sp_Generate_number_get('PR','000',@Messagee);
		    select @Messagee into ls_no from dual;
   # select ls_no;
		 
		#	         select  @mepno,@Datee, @Emp_gid ,  @Statuss,   @Branchgid , @Totalamount , @Commodity_gid, @Entity_Gid,li_create_by;
                   
          set Query_Insert = concat('INSERT INTO gal_trn_tprheader(prheader_no, prheader_date, prheader_employee_gid,
								prheader_status,prheader_branchgid,prheader_totalamount,prheader_commodity_gid,entity_gid, create_by ',Query_column,' )VALUES
								(''',ls_no,''',
                                ''',@Datee,''',
                                ',@Emp_gid,',
                                ''',@Statuss,''',
								',@Branchgid,',
                                ',@Totalamount,',
                                ',@Commodity_gid,',
                                ',@Entity_Gid,',
                                ',li_create_by,'
                                ',Query_value,'
                                )');
                                
                        
                  
				set @Insert_query = Query_Insert;				
				#select Query_Insert;
                PREPARE stmt FROM @Insert_query;
				EXECUTE stmt;  
				set countRow = (select ROW_COUNT());
				DEALLOCATE PREPARE stmt;           
				select LAST_INSERT_ID() into @li_Header_gid_Max ;
                 if countRow >  0 then
                      if @Statuss <> 'DRAFT' then
					     set @ls_Remarks = '';
						 call sp_Trans_Set('INSERT_PR','pr',@li_Header_gid_Max,'Pending For Approval','I',@dropdown_gid,@ls_Remarks,
						 @Entity_Gid,li_create_by,@message);
							select @message into @tran;
							
						if @tran <>0 or @tran <> '' then
							set Message = 'SUCCESS';
    
							#commit;
						else
							set Message = 'FAIL in tran';
							rollback;
						end if;	
                        
                      end if;  
                   end if;
		    
			end if;  
      
      end if;
      
      
      
    set i = 0 ;
 
	select JSON_LENGTH(lj_Details,'$.DETAIL') into @li_jsonDetail_count;  
    if  @li_jsonDetail_count is null or @li_jsonDetail_count = 0 then
			set Message = 'No Data In Json For Invoice Process In Details Data.';            
			leave sp_APInvoice_Set;
	End if;  
                 
                 
                 
                 
                 
                 
                 
                 
                 
                 
                 
                 
                 
                 
                 
                 
                 
                 
                 
                 
                 
                 
                 
                 
                 
                 
                 
                 
                 
                 
                 
                 
		WHILE i <= @li_jsonDetail_count - 1 DO
			#select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].PRHeader_gid[0]'))) into @PRHeader_gid;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].product_gid[0]'))) into @product_gid;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].quantity[0]'))) into @quantity;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].supplierproduct_gid[0]'))) into @supplierproduct_gid;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].supplier_gid[0]'))) into @supplier_gid;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].CCBS'))) into @CCBSdata;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].image[0].SavedFilePath[0]'))) into @SavedFilePath;
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].image[0].File_Name[0]'))) into @File_Name;
if @File_Name <> '' and @File_Name is not null then
			

        set  @file_Id=0;
#select @file_Id,@File_Name,@SavedFilePath,li_	create_by;
		call sp_File_Set('Insert','a',@file_Id,@File_Name,@SavedFilePath,
				lj_Classification, '{}',li_create_by ,@Message);
		 select @Message into @Out_Msg_Image;
      
			 else
				set @Image_Path = '';
			End if;
  if @SavedFilePath <> '' and @SavedFilePath is not null then
                                                            set @Image_Path = '';
															set @Image_Path = @SavedFilePath;
                                                         else
                                                            set @Image_Path = '';
                                                        End if;

#select @SavedFilePath,@supplier_gid;
             if Action <> 'DELETE' then
				## validation Pending
                ## Check for Null Value too
	 
                if Action = 'INSERT' then
					
					set Query_column = '';
					set Query_value = '';
					set Query_Insert = '';
					set Query_Insert = concat('INSERT INTO gal_trn_tprdetails(prdetails_prheader_gid,
						prdetails_product_gid,
						prdetails_qty, 
                        prdetails_supplierproductgid,
						prdetails_imagepath,
						entity_gid,
                        create_by) VALUES
                        (',@li_Header_gid_Max,',
                        ',@product_gid,',
                        ',@Quantity,',
                        ',@supplierproduct_gid,',
						"',@Image_Path,'",	
                        ',@Entity_Gid,',
                        ',li_create_by,')');	 
	                
                     #select Query_Insert; ## remove It
					set @Insert_Detail_query = Query_Insert;		
				
					PREPARE stmt FROM @Insert_Detail_query;
					EXECUTE stmt;  
					set countRow = (select ROW_COUNT());
					DEALLOCATE PREPARE stmt;                          
                  #  select countRow;
					select LAST_INSERT_ID() into @li_Detail_gid ;

                    if countRow >  0 then
                          #select JSON_UNQUOTE(JSON_EXTRACT(@CCBSdata, CONCAT('$[',i,']'))) into @CCBS_Json;          
                            select JSON_LENGTH(@CCBSdata,'$') into @lnth;   
                           # select @lnth;
                            set j = 0;
						    WHILE j<= @lnth - 1 Do	
								 select JSON_UNQUOTE(JSON_EXTRACT(@CCBSdata, CONCAT('$[',j,'].prccbs_cc'))) into @prccbs_cc;          
								 select JSON_UNQUOTE(JSON_EXTRACT(@CCBSdata, CONCAT('$[',j,'].prccbs_bs'))) into @prccbs_bs;          
								 select JSON_UNQUOTE(JSON_EXTRACT(@CCBSdata, CONCAT('$[',j,'].prccbs_code'))) into @prccbs_code;          
								 select JSON_UNQUOTE(JSON_EXTRACT(@CCBSdata, CONCAT('$[',j,'].prccbs_qty'))) into @prccbs_qty;          
								 select JSON_UNQUOTE(JSON_EXTRACT(@CCBSdata, CONCAT('$[',j,'].prccbs_remarks'))) into @prccbs_remarks;          
								 select JSON_UNQUOTE(JSON_EXTRACT(@CCBSdata, CONCAT('$[',j,'].prccbs_reftablegid'))) into @prccbs_reftablegid;          
								 select JSON_UNQUOTE(JSON_EXTRACT(@CCBSdata, CONCAT('$[',j,'].delivery_type'))) into @delivery_type;          
                    #select @prccbs_cc,@prccbs_bs,@prccbs_code,@prccbs_qty;
                                   select ref_gid into @refid from gal_mst_tref where  ref_name = @delivery_type;

									set @ccbs_data = concat('{"prccbs_prdetailsgid":',@li_Detail_gid,',"prccbs_refgid":',@refid,',
                                                         "prccbs_reftablegid":',@prccbs_reftablegid,',
                                                      "prccbs_cc":"',@prccbs_cc,'","prccbs_bs":"',@prccbs_bs,'",
                                                      "prccbs_code":"',@prccbs_code,'","prccbs_qty":"',@prccbs_qty,'","prccbs_remarks":"',@prccbs_remarks,'"}');
                    
									call sp_PRCCBS_Set('insert',@ccbs_data,lj_Classification,li_create_by,@Message);
											if @Message <> 'SUCCESS' then
													set Message = 'Error On ccbs Insert.';
													rollback;
													leave sp_APInvoice_Set;
                                             else
													set Message = 'SUCCESS';

											End if;
                          set j = j + 1;
							END WHILE;
                            commit;
                            
                            
				     else
                          set Message = 'Error on ccbs Insert.';
						rollback;
						leave sp_APInvoice_Set;
                     end if;
                   
	
		     elseif Action = 'UPDATE' then
						set Message = 'No Data';
                   
                    
			 End if;  ### Action Ends
                
                
             End if; ## Check Action delete Ends
                       
            
            
            set i = i + 1;
        END WHILE;  
        commit;
        
elseif Type = 'PR_DRAFT_INSERT' then
            	  select JSON_LENGTH(lj_Header,'$.HEADER') into @li_jsonHeader_count;
      
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid[0]'))) into @Entity_Gid;
             
             if @Entity_Gid is  null or @Entity_Gid = 0 or @Entity_Gid = '' then
					set Message = 'Entity Gid Is Needed.';
                    leave sp_APInvoice_Set;
             End if;
      
      
			
		if @li_jsonHeader_count = 0 or @li_jsonHeader_count is null  then
			set Message = 'No Data In Json For  In Header Data.';            
			leave sp_APInvoice_Set;
		End if;   
	                            
		select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Date[0]'))) into @Datee;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Emp_gid[0]'))) into @Emp_gid;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Statuss[0]'))) into @Statuss;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Branchgid[0]'))) into @Branchgid;        #
        select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Totalamount[0]'))) into @Totalamount;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].Commodity_gid[0]'))) into @Commodity_gid;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].dropdown_gid[0]'))) into @dropdown_gid;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].mepno[0]'))) into @mepno;
        set Query_column = ' ';
        set Query_value = ' ';
        if  @mepno <> ''  then
		            set Query_column = concat(Query_column , ', prheader_mepno');
                    set Query_value = concat(Query_value , ',''' ,@mepno,'''');
		else 
		            set Query_column = concat(Query_column,'');
                    set Query_value = concat(Query_value,'');
		end if; 
       if Action <> 'DELETE' then
			set @Datee = @Datee;
			## validation Pending.
        
			if @Datee is null or @Emp_gid is null or  @Statuss is null 
                     or @Branchgid is null or @Totalamount is null or @Commodity_gid is null  then
				set Message = 'Some Values Is Null In Json Data.'; 
				leave sp_APInvoice_Set;
			End if;   
        

        
          if Action = 'INSERT' then
							select JSON_UNQUOTE(JSON_EXTRACT(lj_header, CONCAT('$.HEADER[0].PR_Header_Gid[0]'))) into @PR_Header_Gid;
                ## Validation Of Json Data
                
                if @PR_Header_Gid is null or @PR_Header_Gid <= 0 then
						set Message = 'PR Header Gid Is Needed To Update.';
                        leave sp_APInvoice_Set;
                End if;
          		
                select ifnull(prheader_status,'') into @PR_Header_Status from gal_trn_tprheader where prheader_gid = @PR_Header_Gid;    
                
                if @PR_Header_Status <> '' and @PR_Header_Status <> 'DRAFT' then
					set Message = 'Only DRAFT Data Can Be Edited.';
                    leave sp_APInvoice_Set;
                End if;
                                
                set Query_Update = '';
                
                set Query_Update = concat('Update gal_trn_tprheader set update_by = ',li_create_by,', ');
                
                if @Datee <> '' then
					set Query_Update = concat(Query_Update, ' prheader_date = ''',@Datee,''', ');
                End if;
                
                  if @Emp_gid <> 0 then
					set Query_Update = concat(Query_Update, ' prheader_employee_gid = ',@Emp_gid,', ');
                End if;
                
                  if @Statuss <> '' then
					set Query_Update = concat(Query_Update, ' prheader_status = ''',@Statuss,''', ');
                End if;
                                 
                  if @Branchgid <> '' then
					set Query_Update = concat(Query_Update, ' prheader_branchgid = ''',@Branchgid,''', ');
                End if;
                
                  if @Totalamount <> '' then
					set Query_Update = concat(Query_Update, ' prheader_totalamount = ''',@Totalamount,''', ');
                    
                  
                End if;
					
                  if @Commodity_gid <> '' then
					set Query_Update = concat(Query_Update, ' prheader_commodity_gid = ''',@Commodity_gid,''', ');
                End if;    
                
               
                
               set Query_Update = concat(Query_Update, 'Update_date = current_timestamp()  where prheader_gid = ',@PR_Header_Gid,'  ' );
                   
                   
                   
                    set @Query_Update = '';
					set @Query_Update = Query_Update;		                
                   #select @Query_Update; ### Remove IT
					PREPARE stmt FROM @Query_Update;
					EXECUTE stmt;  
					set countRow = (select ROW_COUNT());
					DEALLOCATE PREPARE stmt;                         
                    
					if countRow <= 0 then
						set Message = 'Error On  Header Update.';
                        rollback;
                        leave sp_APInvoice_Set;
                     elseif    countRow > 0 then
                        if @Statuss <> 'DRAFT' then
							 set @ls_Remarks = '';
							 call sp_Trans_Set('INSERT_PR','pr',@PR_Header_Gid,'Pending For Approval','I',@dropdown_gid,@ls_Remarks,
							 @Entity_Gid,li_create_by,@message);
								select @message into @tran;
								
							if @tran <>0 or @tran <> '' then
								set Message = 'SUCCESS';
		
								#commit;
							else
								set Message = 'FAIL in tran';
								rollback;
							end if;	
                        
						end if;  
						set Message = 'SUCCESS';
                    End if;
		    
			end if;  
      
      end if;
      
      
      
    set i = 0 ;
 
	select JSON_LENGTH(lj_Details,'$.DETAIL') into @li_jsonDetail_count;  
    if  @li_jsonDetail_count is null or @li_jsonDetail_count = 0 then
			set Message = 'No Data In Json For Invoice Process In Details Data.';            
			leave sp_APInvoice_Set;
	End if;  
                 

		WHILE i <= @li_jsonDetail_count - 1 DO
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].PRdetail_gid[0]'))) into @PRdetail_gid;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].product_gid[0]'))) into @product_gid;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].quantity[0]'))) into @quantity;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].supplier_gid[0]'))) into @supplier_gid;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].detail_edit[0]'))) into @detail_edit;
            select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.DETAIL[',i,'].CCBS'))) into @CCBSdata;
          select @li_Header_gid_Max,@product_gid,@Quantity,@supplier_gid,@Entity_Gid,li_create_by;

             if Action <> 'DELETE' then
				## validation Pending
                ## Check for Null Value too
                if Action = 'INSERT' then
					  if @detail_edit = 'N' then
							set Query_column = '';
							set Query_value = '';
							set Query_Insert = '';
							set Query_Insert = concat('INSERT INTO gal_trn_tprdetails(prdetails_prheader_gid,
								prdetails_product_gid,
								prdetails_qty, 
								prdetails_supplierproductgid,
								entity_gid,
								create_by) VALUES
								(',@PR_Header_Gid,',
								',@product_gid,',
								',@Quantity,',
								',@supplier_gid,',
								',@Entity_Gid,',
								',li_create_by,')');	 
													
							set @Insert_Detail_query = Query_Insert;		
							select Query_Insert; ## remove It
							PREPARE stmt FROM @Insert_Detail_query;
							EXECUTE stmt;  
							set countRow = (select ROW_COUNT());
							DEALLOCATE PREPARE stmt;                          
							#  select countRow;
							select LAST_INSERT_ID() into @li_Detail_gid ;
                     elseif @detail_edit = 'Y' then
		
						if @PRdetail_gid is null or @PRdetail_gid <= 0 then
								set Message = 'PR detail Gid Is Needed To Update.';
								leave sp_APInvoice_Set;
						End if;
										
						set Query_Update = '';

						set Query_Update = concat('Update gal_trn_tprdetails set update_by = ',li_create_by,', ');
						
						if @product_gid <> '' then
							set Query_Update = concat(Query_Update, ' prdetails_product_gid = ''',@product_gid,''', ');
						End if;
						
						  if @quantity <> 0 then
							set Query_Update = concat(Query_Update, ' prdetails_qty = ',@quantity,', ');
						End if; 
                        
                        if @supplier_gid <> 0 then
							set Query_Update = concat(Query_Update, ' prdetails_supplierproductgid = ',@supplier_gid,', ');
						End if;
						
                
						set Query_Update = concat(Query_Update, 'Update_date = current_timestamp()  where prdetails_gid = ',@PRdetail_gid,'  ' );
                   
                   
                   
						set @Query_Update = '';
						set @Query_Update = Query_Update;		                
					   select @Query_Update; ### Remove IT
						PREPARE stmt FROM @Query_Update;
						EXECUTE stmt;  
						set countRow = (select ROW_COUNT());
						DEALLOCATE PREPARE stmt; 
                        set  @li_Detail_gid = @PRdetail_gid ;
                    
                    else 
                          Update gal_trn_tprdetails set update_by =li_create_by,prdetails_isremoved = 'Y',
                          Update_date = current_timestamp()  where prdetails_gid = @PRdetail_gid;
                    
					End if;      
                    if countRow >  0 then
                          #select JSON_UNQUOTE(JSON_EXTRACT(@CCBSdata, CONCAT('$[',i,']'))) into @CCBS_Json;          
                            select JSON_LENGTH(@CCBSdata,'$') into @lnth;   
                           # select @lnth;
                            set j = 0;
						    WHILE j<= @lnth - 1 Do	
								 select JSON_UNQUOTE(JSON_EXTRACT(@CCBSdata, CONCAT('$[',j,'].prccbs_cc'))) into @prccbs_cc;          
								 select JSON_UNQUOTE(JSON_EXTRACT(@CCBSdata, CONCAT('$[',j,'].prccbs_bs'))) into @prccbs_bs;          
								 select JSON_UNQUOTE(JSON_EXTRACT(@CCBSdata, CONCAT('$[',j,'].prccbs_code'))) into @prccbs_code;          
								 select JSON_UNQUOTE(JSON_EXTRACT(@CCBSdata, CONCAT('$[',j,'].prccbs_qty'))) into @prccbs_qty;          
								 select JSON_UNQUOTE(JSON_EXTRACT(@CCBSdata, CONCAT('$[',j,'].prccbs_remarks'))) into @prccbs_remarks;          
								 select JSON_UNQUOTE(JSON_EXTRACT(@CCBSdata, CONCAT('$[',j,'].prccbs_GID'))) into @prccbs_GID;          
								 select JSON_UNQUOTE(JSON_EXTRACT(@CCBSdata, CONCAT('$[',j,'].prccbs_edit'))) into @prccbs_edit;          
								 select JSON_UNQUOTE(JSON_EXTRACT(@CCBSdata, CONCAT('$[',j,'].prccbs_reftablegid'))) into @prccbs_reftablegid;          
								 select JSON_UNQUOTE(JSON_EXTRACT(@CCBSdata, CONCAT('$[',j,'].delivery_type'))) into @delivery_type;          
                                   select ref_gid into @refid from gal_mst_tref where   ref_name = @delivery_type;

                   select @prccbs_cc,@prccbs_bs,@prccbs_code,@prccbs_qty,@li_Detail_gid,@prccbs_reftablegid,@prccbs_GID,@prccbs_remarks;
                     
									set @ccbs_data = concat('{"prccbs_prdetailsgid":',@li_Detail_gid,',"prccbs_refgid":',@refid,',
                                                         "prccbs_reftablegid":',@prccbs_reftablegid,',
                                                      "prccbs_cc":"',@prccbs_cc,'","prccbs_bs":"',@prccbs_bs,'",
                                                      "prccbs_code":"',@prccbs_code,'","prccbs_qty":"',@prccbs_qty,'","prccbs_GID":"',@prccbs_GID,'","prccbs_remarks":"',@prccbs_remarks,'"}');
                                      select @prccbs_edit;
                                      if @prccbs_edit = 'N' then 
                                      select @ccbs_data;
                                      select lj_Classification;
											call sp_PRCCBS_Set('insert',@ccbs_data,lj_Classification,li_create_by,@Message);
													select @Message;
                                                    if @Message <> 'SUCCESS' then
															set Message = 'Error On ccbs Insert.';
															rollback;
															leave sp_APInvoice_Set;
													 else
															set Message = 'SUCCESS';

													End if;
										elseif  @prccbs_edit = 'Y' then
											call sp_PRCCBS_Set('update',@ccbs_data,lj_Classification,li_create_by,@Message);
                                            select @Message;
													if @Message <> 'SUCCESS' then
															set Message = 'Error On ccbs Insert.';
															rollback;
															leave sp_APInvoice_Set;
													 else
															set Message = 'SUCCESS';

													End if;
                                          
                                         elseif  @prccbs_edit = 'R' then
                                         select @prccbs_GID;
                                             Update gal_trn_tprccbs set update_by = li_create_by,prccbs_isremoved = 'Y',
                                             Update_date = current_timestamp()  where prccbs_gid = @prccbs_GID;
															set Message = 'SUCCESS';

                                         end if;           
                          set j = j + 1;
							END WHILE;
                            
                            
				     else
                          set Message = 'Error on ccbs Insert.';
						rollback;
						leave sp_APInvoice_Set;
                     end if;
                   
	
		     elseif Action = 'UPDATE' then
						set Message = 'No Data';
                   
                    
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
          set @Remarks = '';
          set @tran = '';
            if @Header_Gid > 2465 then              
			   call sp_Trans_Set('update','AP_INVOICE',@Header_Gid,@ls_Status,'I','CHECKER',@Remarks,li_entity_gid,li_create_by,@message);
                select @message into @tran;
            end if;    
          
          
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

				#set Message = 'FAIL IN TRAN.';
				#rollback;
               # leave sp_APInvoice_Set;
			end if;
        ## Tran Ends
	
           set Message = 'SUCCESS';
         End if;


   
    End if;






	  
End if; # Type Ends

END