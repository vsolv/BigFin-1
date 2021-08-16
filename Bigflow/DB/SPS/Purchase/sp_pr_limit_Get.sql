CREATE DEFINER=`developer`@`%` PROCEDURE `sp_pr_limit_Get`(IN `Type` varchar(64),
IN `Sub_type` varchar(64),
IN `lj_filters` JSON,
IN `lj_classification` JSON,
IN `total_amt` varchar(100), 
 OUT `Message` varchar(5000))
sp_pr_limit_Get:BEGIN

#Akshay 16-aug-2019
declare limit_srch text;
declare Query_srch text;
#declare qry_srch text;
declare ls_error varchar(100);
declare li_count int;
declare cust  text;
declare i int;

			select JSON_LENGTH(lj_filters,'$') into @li_json_count;
			select JSON_LENGTH(lj_classification,'$') into @li_json_count1;
			
            #select @li_json_count,@li_json_count1;
            #select lj_filters;
            #select lj_classification;

		   if  @li_json_count <=0  then
				set Message = 'No Data in Json Object';
				leave sp_pr_limit_Get;
		  end if;
     
			if  @li_json_count1 <=0  then
				set Message = 'No classification in Json Object';
				leave sp_pr_limit_Get;
			end if;

         
  if  Type = 'limit'  and Sub_type='pr_limit'  then       
	 #select 1;
     #select lj_filters;
     #select lj_classification;
     select  JSON_UNQUOTE(JSON_EXTRACT(lj_filters, '$.prheader_gid')) into @prheader_gid;
     select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, '$.Entity_Gid')) into @Entity_Gid;

	set Query_srch='';
    
    #select @prheader_gid,@Entity_Gid;
	if @prheader_gid is  null or  @prheader_gid=0 then
	set Message='prheader_gid is not Given';
    leave sp_pr_limit_Get;
    else 
    set Query_srch = concat('and b.prheader_gid =',@prheader_gid,' ');
	end if;
    
    select metadata_gid into @meta_gid1 from gal_mst_tmetadata 
    where metadata_value='PR' 
    and metadata_tablename='gal_mst_tdelmat'
    and metadata_columnname='delmat_tran';
    
    if @meta_gid1 = 0 or @meta_gid1 ='' then
    set Message='meta_gid is empty';
    leave sp_pr_limit_Get;
    end if;
	
    
	set limit_srch = concat('select employee_gid, employee_code,commodity_gid,commodity_name,delmat_limit,delmat_tran
               from gal_mst_temployee
               left join gal_mst_tdelmat on delmat_employeegid=employee_gid
                   and delmat_tran=133 and delmat_isactive=''Y'' and delmat_isremoved=''N''
               left join ap_mst_tcommodity on delmat_commoditygid=commodity_gid
                   and commodity_isactive=''Y'' and commodity_isremoved=''N''
                  and employee_isactive=''Y''  and employee_isremoved=''N'';');

									set @p = limit_srch;
									#select @p;
									PREPARE stmt FROM @p;
									EXECUTE stmt; 
									DEALLOCATE PREPARE stmt;
									select found_rows() into li_count;
									if li_count>0 then
										set Message='FOUND';
									 else
										set Message='NOT FOUND';
									 end if;
                                     
                                     
 
elseif  Type = 'limit'  and Sub_type='po_limit'  then       
        
     select  JSON_UNQUOTE(JSON_EXTRACT(lj_filters, '$.poheader_gid')) into @poheader_gid;
     select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, '$.Entity_Gid')) into @Entity_Gid;
	 #select 1;
	set Query_srch='';
    
    #select @commodity_gid;
	if @poheader_gid is  null or  @poheader_gid=0 then
	set Message='poheader_gid is not Given';
    leave sp_pr_limit_Get;
    else 
    set Query_srch = concat('and b.poheader_gid =',@poheader_gid,' ');
	end if;
    
     select metadata_gid into @meta_gid2 from gal_mst_tmetadata 
     where metadata_value='PO'
     and metadata_tablename='gal_mst_tdelmat'
     and metadata_columnname='delmat_tran';
    
    if @meta_gid2 = 0 or @meta_gid2 ='' then
    set Message='meta_gid is empty';
    leave sp_pr_limit_Get;
    end if;
	
    
	set limit_srch = concat('select a.commodity_gid,
											 a.commodity_code,
                                             a.commodity_name,
                                             b.poheader_amount,
                                             b.poheader_commodity_gid,
                                             c.delmat_limit,
                                             d.employee_gid,
                                             d.employee_name
											 from  ap_mst_tcommodity as a
											 inner join  gal_trn_tpoheader as b on b.poheader_commodity_gid=a.commodity_gid
                                             and b.poheader_isactive=''Y'' and  b.poheader_isremoved=''N''
											 inner join  gal_mst_tdelmat as c on c.delmat_commoditygid = b.poheader_commodity_gid
											 and c.delmat_tran=',@meta_gid2,'
                                             and c.delmat_isactive=''Y'' and  c.delmat_isremoved=''N''
											 inner join  gal_mst_temployee as d on d.employee_gid=c.delmat_employeegid
                                             and d.employee_isactive=''Y''  and d.employee_isremoved=''N''
                                             where a.entity_gid=',@Entity_Gid,' ',Query_srch,' ');

									set @p = limit_srch;
									#select @p;
									PREPARE stmt FROM @p;
									EXECUTE stmt; 
									DEALLOCATE PREPARE stmt;
									select found_rows() into li_count;
									if li_count>0 then
										set Message='FOUND';
									 else
										set Message='NOT FOUND';
									 end if;  
         
elseif  Type = 'limit'  and Sub_type='pr_Dir_limit'  then             
     
	 #select  JSON_UNQUOTE(JSON_EXTRACT(lj_filters, '$.delmat_commoditygid')) into @delmat_commoditygid;
       # select  JSON_UNQUOTE(JSON_EXTRACT(lj_filters, '$.delmat_employeegid')) into @delmat_employeegid;
     select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, '$.Entity_Gid')) into @Entity_Gid;
	 
	#set Query_srch='';
    
      
	/*if @delmat_commoditygid is  null or  @delmat_commoditygid=0 then
	set Message='delmat_commoditygid is not Given';
    leave sp_pr_limit_Get;
    else 
    set Query_srch = concat('and c.delmat_commoditygid =',@delmat_commoditygid,' ');
	end if;
    
		/*if total_amt <> '' then
			set Query_srch = concat(Query_srch,'and c.delmat_limit>=',total_amt,'');
		end if;*/
        
		
    
    select metadata_gid into @meta_gid3 from gal_mst_tmetadata 
		where metadata_value='PR' 
		and metadata_tablename='gal_mst_tdelmat'
		and metadata_columnname='delmat_tran';
    
    
    if @meta_gid3 = 0 or @meta_gid3 ='' then
		set Message='meta_gid is empty';
		leave sp_pr_limit_Get;
    end if;
   
       
	set limit_srch = concat('select employee_gid, 
									employee_code,
                                    employee_name,
                                    commodity_gid,
									commodity_name,
                                    delmat_limit,
                                    delmat_tran
									from gal_mst_temployee
									left join gal_mst_tdelmat on delmat_employeegid=employee_gid
										and delmat_tran=',@meta_gid3,' and delmat_isactive=''Y'' and delmat_isremoved=''N''
									left join ap_mst_tcommodity on delmat_commoditygid=commodity_gid
										and commodity_isactive=''Y'' and commodity_isremoved=''N''
										and employee_isactive=''Y''  and employee_isremoved=''N''');
                                             
															
                                              
									#select limit_srch;
									set @p = limit_srch;
									PREPARE stmt FROM @p;
									EXECUTE stmt; 
									DEALLOCATE PREPARE stmt;
									select found_rows() into li_count;
									if li_count>0 then
										set Message='FOUND';
									 else
										set Message='NOT FOUND';
									 end if;  
elseif  Type = 'limit'  and Sub_type='po_Dir_limit'  then             
     
	 #select  JSON_UNQUOTE(JSON_EXTRACT(lj_filters, '$.delmat_commoditygid')) into @delmat_commoditygid;
       # select  JSON_UNQUOTE(JSON_EXTRACT(lj_filters, '$.delmat_employeegid')) into @delmat_employeegid;
     select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, '$.Entity_Gid')) into @Entity_Gid;
	 
	#set Query_srch='';
    
      
	/*if @delmat_commoditygid is  null or  @delmat_commoditygid=0 then
	set Message='delmat_commoditygid is not Given';
    leave sp_pr_limit_Get;
    else 
    set Query_srch = concat('and c.delmat_commoditygid =',@delmat_commoditygid,' ');
	end if;
    
		/*if total_amt <> '' then
			set Query_srch = concat(Query_srch,'and c.delmat_limit>=',total_amt,'');
		end if;*/
        
		
    
    select metadata_gid into @meta_gid3 from gal_mst_tmetadata 
		where metadata_value='PO' 
		and metadata_tablename='gal_mst_tdelmat'
		and metadata_columnname='delmat_tran';
    
    
    if @meta_gid3 = 0 or @meta_gid3 ='' then
		set Message='meta_gid is empty';
		leave sp_pr_limit_Get;
    end if;
   
       
	set limit_srch = concat('select employee_gid, 
									employee_code,
                                    employee_name,
                                    commodity_gid,
									commodity_name,
                                    delmat_limit,
                                    delmat_tran
									from gal_mst_temployee
									left join gal_mst_tdelmat on delmat_employeegid=employee_gid
										and delmat_tran=',@meta_gid3,' and delmat_isactive=''Y'' and delmat_isremoved=''N''
									left join ap_mst_tcommodity on delmat_commoditygid=commodity_gid
										and commodity_isactive=''Y'' and commodity_isremoved=''N''
										and employee_isactive=''Y''  and employee_isremoved=''N''');
                                             
															
                                              
									#select limit_srch;
									set @p = limit_srch;
									PREPARE stmt FROM @p;
									EXECUTE stmt; 
									DEALLOCATE PREPARE stmt;
									select found_rows() into li_count;
									if li_count>0 then
										set Message='FOUND';
									 else
										set Message='NOT FOUND';
									 end if;  
         

         
end if;
    
 
END
