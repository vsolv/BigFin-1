CREATE DEFINER=`developer`@`%` PROCEDURE `sp_PRHeader_Get`(in `li_action` varchar(200),
 in `li_filter` json, 
 in `li_classification` json, 
in `li_create_by` int(100),
out `Message` varchar(1000))
sp_PRHeader_Get:BEGIN

declare ls_count varchar(6000);
declare Query_search varchar(1000);
declare Query_Where varchar(1000);
declare Query_Limit varchar(1000);
declare PR_Headersrch varchar(10000);


if li_action='get' then

select JSON_LENGTH(li_filter,'$') into @li_jsonfilter_count;
select JSON_LENGTH(li_classification,'$') into @li_classification_jsoncount;
    #select 1;
    # select @li_classification_jsoncount,@li_jsonfilter_count;    
         if @li_classification_jsoncount = 0 or @li_classification_jsoncount is null  then
			set Message = 'No Data In classification Json. ';            
			leave sp_PRHeader_Get;
		End if;
      
		if @li_jsonfilter_count is null or @li_jsonfilter_count = '' or @li_jsonfilter_count = 0 then
		set Message = 'No Data In li_jsonfilter_count ';            
			leave sp_PRHeader_Get;
		End if;
   #  select 2;   
       
        #select  JSON_UNQUOTE(JSON_EXTRACT(li_filter, CONCAT('$.prheader_status'))) into @prheader_status;
        #select  JSON_UNQUOTE(JSON_EXTRACT(li_filter, CONCAT('$.prheader_no'))) into @prheader_no;
        select  JSON_UNQUOTE(JSON_EXTRACT(li_filter, CONCAT('$.prheader_employee_gid'))) into @prheader_employee_gid;
        select  JSON_UNQUOTE(JSON_EXTRACT(li_filter, CONCAT('$.commodity_name'))) into @commodity_name;
        select  JSON_UNQUOTE(JSON_EXTRACT(li_filter, CONCAT('$.prheader_gid'))) into @prheader_gid;
        select  JSON_UNQUOTE(JSON_EXTRACT(li_filter, CONCAT('$.employee_gid'))) into @employee_gid;
        select  JSON_UNQUOTE(JSON_EXTRACT(li_filter, CONCAT('$.prheader_no'))) into @prheader_no;
        select  JSON_UNQUOTE(JSON_EXTRACT(li_filter, CONCAT('$.prheader_date'))) into @prheader_date;
        select  JSON_UNQUOTE(JSON_EXTRACT(li_filter, CONCAT('$.employee_name'))) into @employee_name;
        select  JSON_UNQUOTE(JSON_EXTRACT(li_filter, CONCAT('$.prheader_status'))) into @prheader_status;
        select  JSON_UNQUOTE(JSON_EXTRACT(li_filter, CONCAT('$.prheader_totalamount'))) into @prheader_totalamount;
        select  JSON_UNQUOTE(JSON_EXTRACT(li_filter, CONCAT('$.prheader_commodity_gid'))) into @prheader_commodity_gid;
        select  JSON_UNQUOTE(JSON_EXTRACT(li_classification, CONCAT('$.entity_gid'))) into @entity_gid;
        select  JSON_UNQUOTE(JSON_EXTRACT(li_filter, CONCAT('$.Page_Index'))) into @Page_Index;     
		select  JSON_UNQUOTE(JSON_EXTRACT(li_filter, CONCAT('$.Page_Size'))) into @Page_Size; 
       # select 5;    
   # select @prheader_employee_gid,@entity_gid, @Page_Index,@Page_Size;
        
            if @entity_gid = 0 or @entity_gid = '' 
				or @entity_gid is null  then
				set Message = 'Entity_Gid Is Not Given In classification Json. ';            
				leave sp_PRHeader_Get;
			End if;
        
         if @prheader_employee_gid = 0 or @prheader_employee_gid = '' 
            or @prheader_employee_gid is null  then
				set Message = 'prheader_employee_gid Is Not Given In Filter Json. ';            
				leave sp_PRHeader_Get;
			End if;
            
            
            set Query_Search = '';

                    if @commodity_name <> '' and @commodity_name is not null  then 
                         set Query_Search = concat(Query_Search,' and commodity_name like ''','%',@commodity_name,'%','''  ');
                    End if;
                    
                    if @prheader_gid <> '' and @prheader_gid is not null  then 
                         set Query_Search = concat(Query_Search,' and prheader_gid =',@prheader_gid,'  ');
                    End if;
                    
                    if @employee_gid <> '' and @employee_gid is not null  then 
                         set Query_Search = concat(Query_Search,' and employee_gid =',@employee_gid,'  ');
                    End if;
                    
                    if @prheader_employee_gid <> '' and @prheader_employee_gid is not null  then 
                         set Query_Search = concat(Query_Search,' and prheader_employee_gid =',@prheader_employee_gid,'  ');
                    End if;
                    
                    if @prheader_no <> '' and @prheader_no is not null  then 
                         set Query_Search = concat(Query_Search,' and prheader_no like ''','%',@prheader_no,'%','''  ');
                    End if;
                    
                    if @prheader_date <> '' and @prheader_date is not null  then 
                         set Query_Search = concat(Query_Search,'and date_format(prheader_date,''%Y-%m-%d'') = ''',@prheader_date,'''  ');
                       
                    End if;
                    
                    if @employee_name <> '' and @employee_name is not null  then 
                         set Query_Search = concat(Query_Search,' and employee_name like ''','%',@employee_name,'%','''  ');
                    End if;
                    
                    if @prheader_status <> '' and @prheader_status is not null  then 
                         set Query_Search = concat(Query_Search,' and prheader_status like ''','%',@prheader_status,'%','''  ');
                    End if;
                    
                    if @prheader_totalamount <> '' and @prheader_totalamount is not null  then 
                         set Query_Search = concat(Query_Search,' and prheader_totalamount like ''','%',@prheader_totalamount,'%','''  ');
                    End if;
                    
                    if @prheader_commodity_gid <> '' and @prheader_commodity_gid is not null  then 
                         set Query_Search = concat(Query_Search,' and prheader_commodity_gid =',@prheader_commodity_gid,'  ');
                    End if;
                    
                    if @prdetails_qty <> '' and @prdetails_qty is not null  then 
                         set Query_Search = concat(Query_Search,' and prdetails_qty like ''','%',@prdetails_qty,'%','''  ');
                    End if;
                    
                    if @prdetails_supplierproductgid <> '' and @prdetails_supplierproductgid is not null  then 
                         set Query_Search = concat(Query_Search,' and prdetails_supplierproductgid =',@prdetails_supplierproductgid,'  ');
                    End if;
    
        set @total_size= @Page_Index*@Page_Size;    
         #select  @total_size,  @Page_Index,@Page_Size;
        set Query_Limit='';
		
        if @Page_Index <> '' and @Page_Index is not null and @Page_Size <> '' and @Page_Size is not null  then 
      
                         set @total_size= @Page_Index*@Page_Size;
                        set @Page_Size=@Page_Size;
                         set Query_Limit = concat(Query_Limit,' LIMIT ',@Page_Size,' OFFSET ',@total_size,'  ');
		
        else
						#select 1;
						set @Page_Index=2,@Page_Size=5;
                        #select @Page_Index,@Page_Size;
                        set @total_size= @Page_Index*@Page_Size;
                        
                        #select @total_size;
                        set Query_Limit = concat(Query_Limit,' LIMIT ',@Page_Size,' OFFSET ',@total_size,'  ');
        End if; 
        
        
     # select  Query_Limit;  
  
   
   ##set Query_Limit=' LIMIT 2 OFFSET 1';
   #select Query_Limit;  

set  PR_Headersrch = '';
set PR_Headersrch = concat('select distinct commodity_name,prheader_gid,employee_gid,prheader_employee_gid,prheader_no , 
								   prheader_date,prheader_imagepath,employee_name,prheader_status,
								   prheader_totalamount,prheader_commodity_gid,sum(prdetails_qty) as prdetails_qty,
								   concat(supplier_name,''-'',supplier_branchname) as supplier_name,
								   prdetails_supplierproductgid ,@Total_Row as Total_Row 
								from gal_trn_tprheader 
							inner join gal_trn_tprdetails on prheader_gid = prdetails_prheader_gid
							inner join ap_mst_tcommodity on prheader_commodity_gid=commodity_gid
							inner join gal_mst_temployee on employee_gid = prheader_employee_gid
							inner join gal_map_tsupplierproduct on 
									supplierproduct_gid = prdetails_supplierproductgid and 
									 prdetails_product_gid= supplierproduct_product_gid and supplierproduct_isremoved = ''N'' 
									 and  supplierproduct_isactive=''Y'' and  prdetails_isremoved=''N''
							inner join gal_mst_tsupplier  on supplier_gid = supplierproduct_supplier_gid
							and employee_isremoved = ''N'' and employee_isactive=''Y''
							where 
							prheader_isremoved = ''N''
							and prheader_isactive = ''Y''
							and prdetails_isremoved = ''N'' 
							and commodity_isactive=''Y''
							and commodity_isremoved=''N''
								',Query_Search,'
							group by prheader_gid order by prheader_gid desc
							');
							 
	set @Query_Count = '';   
	set @Query_Count = concat('Select count(A.prheader_gid) into @Total_Row from (',PR_Headersrch,') A ');   
	#select PR_Headersrch ;   
	#select @Query_Count ;   
	PREPARE stmt FROM @Query_Count;
	EXECUTE stmt; 
	DEALLOCATE PREPARE stmt;					   
           
#select PR_Headersrch;

 set @p = concat(PR_Headersrch,Query_Limit);
 #set @p = PR_Headersrch;
 #select @p;
     ##select Query_Select;  ## Remove It
     PREPARE stmt FROM @p;
	 EXECUTE stmt; 
	 Select found_rows() into ls_count;
	 DEALLOCATE PREPARE stmt;
     
     
     if ls_count > 0 then
		 set Message = 'FOUND';
	else
		 set Message = 'NOT_FOUND';
	end if;

end if;


#set @stmt = concat(PR_Headersrch , Query_search,' group by prheader_gid , prheader_no , prheader_date , employee_name , prheader_status ');
#select @stmt;
#PREPARE stmt FROM @stmt;
#EXECUTE stmt;
#DEALLOCATE PREPARE stmt;

END