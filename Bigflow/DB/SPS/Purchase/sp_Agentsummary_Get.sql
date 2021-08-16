CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Agentsummary_Get`(IN `ls_Type` varchar(64),IN `ls_Sub_Type` varchar(64),
IN `lj_Filters` json,IN `lj_Classification` json, OUT `Message` varchar(1024)
)
sp_Agentsummary_Get:BEGIN

## Aswani
Declare Query_Select varchar(6144);
Declare Query_Search varchar(1024);
declare Query_Insert varchar(10000); 
Declare countRow varchar(6000);
declare Query_Update varchar(10000);
declare Query_delete varchar(1000);
declare Query_Value varchar(1000);
declare Query_Column varchar(1000);
Declare cust  text;
Declare i int;
#Declare i int;
declare errno int;
declare msg varchar(1000);
declare li_count int;
declare ls_count varchar(1000);
Declare  r_ref_fieldname,r_tran_reftable_gid,r_ref_tablename varchar(150);
DECLARE finished INTEGER DEFAULT 0;

#declare Entity_Gid int;
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

if ls_Type = 'Tran_status' and ls_Sub_Type = 'SINGLE' then
		select JSON_LENGTH(lj_Filters,'$') into @li_json_INVProcess_count;
        
           if @li_json_INVProcess_count is null or @li_json_INVProcess_count = 0 then
			set Message = 'No Data In Json - Filter.';
            rollback;
			leave sp_Agentsummary_Get;
        end if;
        
        Select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.ref_gid'))) into @ref_gid ;  
        Select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.employee_gid'))) into @employee_gid ;  ### GET By SIngle Product
        Select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.from_date'))) into @from_date ;
        Select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.to_date'))) into @to_date ;
        set @from_date=date_format(@from_date,'%Y-%m-%d');
        set @to_date=date_format(@to_date,'%Y-%m-%d');
        
        if @ref_gid = 0 then
				set Message = 'SO ref_gid  Is Needed.';
                leave sp_Agentsummary_Get;
        End if;
        
      
        
        set Query_Search = '';
        if @ref_gid is not null and  @ref_gid <> 0  then
			set Query_Search = concat(Query_Search,'and a.tran_ref_gid = ',@ref_gid,' ');
		
				
        End if;
        if @employee_gid is not null and  @employee_gid <> 0  then
				set Query_Search = concat(Query_Search,'  and a.tran_from = ',@employee_gid,' ');
		End if;
         
        
								set Query_Select = '';
								
								
                                SET session group_concat_max_len=50000000;                                            
								set Query_Select=concat('
                                select a.tran_by,a.tran_from, b.ref_name,b.ref_gid,c.employee_code,c.employee_name,a.tran_date,
                                b.ref_tablename,b.ref_fieldname, a.tran_fromdate,(select 
								concat(''['',group_concat( JSON_OBJECT(''tran_reftable_gid'',a.tran_reftable_gid,
									''bb.ref_gid'',a.tran_ref_gid)),'']'')) 
									as good,JSON_LENGTH(concat(''['',group_concat( JSON_OBJECT(''tran_reftable_gid'',
                                    a.tran_reftable_gid,
									''ref_gid'',a.tran_ref_gid)),'']'')) as process_count from gal_trn_ttran  as a
									left join gal_mst_tref b on a.tran_ref_gid=b.ref_gid
									left join gal_mst_temployee c on a.tran_from=c.employee_gid
									 where date_format(a.tran_fromdate,''%Y-%m-%d'') between
									''',@from_date,''' AND ''', @to_date,'''
									and a.tran_isactive=''Y''and a.tran_isremoved=''N''',Query_Search,'
									#and a.tran_ref_gid = ''',@ref_gid,''' and a.tran_from=''',@employee_gid,''' 
                                    
                                    group by date_format(a.tran_fromdate,''%Y-%m-%d'');
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                ');

                              										
                
	
													set @Query_Select = Query_Select;#									                
													#select @Query_Select; ### Remove It
													PREPARE stmt FROM @Query_Select;
													EXECUTE stmt; 
													Select found_rows() into li_count;
									
												  if li_count > 0 then
														set Message = 'FOUND';
												  else 
														set Message = 'NOT_FOUND';
												  end if; 
        

#
	
elseif ls_Type = 'Tran_status' and ls_Sub_Type = 'Details' then
		select JSON_LENGTH(lj_Filters,'$') into @li_json_INVProcess_count;
        
           if @li_json_INVProcess_count is null or @li_json_INVProcess_count = 0 then
			set Message = 'No Data In Json - Filter.';
            rollback;
			leave sp_Agentsummary_Get;
        end if;
        
        Select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.ref_gid'))) into @ref_gid ;  
        Select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.ref_tablename'))) into @ref_tablename ;
        Select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.ref_fieldname'))) into @ref_fieldname ;
      
        
        if @ref_gid = 0 then
				set Message = 'SO ref_gid  Is Needed.';
                leave sp_Agentsummary_Get;
        End if;
        
      
      
      	select JSON_LENGTH(lj_Filters,'$.tran_reftable_gid') into @gid_count;
        set cust='';
        set i=0;
        if @gid_count is not null or @gid_count <> '' then
        #select @li_json_count;#
			while i<@gid_count do
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.tran_reftable_gid[',i,']')))into @tran_reftable_gid;
                if i=0 then
					set cust=concat(@tran_reftable_gid);
			    else
					set cust=concat(cust,',',@tran_reftable_gid);
                end if;
					set i=i+1;
			end while;
            #select cust;
        end if;
        
 

	    set @i=0;
		set @count1=0;
        
        set Query_Select = '';
        
		while @i<@gid_count do
			set Query_Select = concat(' select * from  ',@ref_tablename,'  where  ',@ref_fieldname,' in (',cust,') ',' ');
            set @i=@i+1;
		end while;
       # select Query_Select; 
        
								
					
								set @Query_Select = Query_Select;									                
								#select Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt; 
								Select found_rows() into li_count;
				
							  if li_count > 0 then
									set Message = 'FOUND';
							  else 
									set Message = 'NOT_FOUND';
							  end if; 
                              
   
elseif ls_Type = 'Tran'  and ls_Sub_Type='get'  then

     select  JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid'))) into @Entity_Gid;
	 select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.tran_by'))) into @tran_by;
     #select JSON_LENGTH(lj_filters,'$.category_gid') into @li_json;
     
    
    
    set Query_Select = concat('  select a.ref_name,ifnull(count1,0) as count11,c.employee_name,c.employee_code
												from gal_mst_tref as a
												left join 
												(select a1.ref_name,count(*) as count1,b1.tran_ref_gid,b1.tran_by,b1.tran_gid,c1.employee_name  from gal_mst_tref as a1
												 left join gal_trn_ttran as b1 on a1.ref_gid=b1.tran_ref_gid
                                                 left join gal_mst_temployee as c1 on c1.employee_gid =b1.tran_by
												 where  b1.tran_by=',@tran_by,' group by tran_ref_gid)
												 as b 
												on b.tran_ref_gid=a.ref_gid
												and b.tran_by=',@tran_by,' 
                                                left join gal_mst_temployee as c on c.employee_gid =',@tran_by,' 
                                                group by ref_gid');

					set @p = Query_Select;
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
                     
                     
  elseif  ls_Type = 'Tran'  and ls_Sub_Type='Sub_Get' then
		  set Query_Search = '';
  
		 select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.employee_gid'))) into @employee_gid;
         select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.from_date'))) into @from_date;
         select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.to_date'))) into @to_date;
         
         if  @employee_gid is null  or @employee_gid =0 or @employee_gid =''  then
			 set Query_Search = concat(Query_Search,'');
         else
            set Query_Search = concat(Query_Search,' where main1.employee_gid=',@employee_gid,' ');
         end if;
         
  
	set Query_Select = concat('select   main1.employee_gid,
																main1.employee_code,
																main1.employee_name,
																main1.ref_name,
																main1.ref_gid,
																main1.tran_by,
																main1.number_of_count,
																main2.tran_from,
																main2.number_of_count1,
																main1.tran_fromdate,
																main2.tran_fromdate1,
                                                               
                                                                 
                                                            
																(main1.number_of_count+main2.number_of_count1) as total from

													(select employee_gid,employee_code,employee_name,ref_gid,ref_name,ifnull(number_of_count,0) as number_of_count ,ifnull(tran_by,0) as tran_by,tran_fromdate
													from
													(select employee_gid,employee_code,employee_name,ref_gid,ref_name from gal_mst_temployee join gal_mst_tref) as a
														left join
														(
																select if(tran_by is null,0,count(*)) as number_of_count,tran_by,tran_ref_gid,tran_fromdate from gal_trn_ttran
																inner join gal_mst_tref on ref_gid=tran_ref_gid
																inner join gal_mst_temployee on employee_gid=tran_by
																group by tran_ref_gid
														) as b
													on b.tran_by=a.employee_gid
													and b.tran_ref_gid=a.ref_gid
													and date_format(b.tran_fromdate,''%Y-%m-%d'') between date_format(''',@from_date,''',''%Y-%m-%d'') and date_format(''',@to_date,''',''%Y-%m-%d'')
													) 
													as main1
													left join
													(select employee_gid,employee_code,employee_name,ref_gid,ref_name,ifnull(number_of_count1,0) as number_of_count1 ,ifnull(tran_from,0) as tran_from,tran_fromdate as tran_fromdate1
													from
													(select employee_gid,employee_code,employee_name,ref_gid,ref_name from gal_mst_temployee join gal_mst_tref) as a
														left join
														(
																select if(tran_from is null,0,count(*)) as number_of_count1,tran_by,tran_ref_gid,tran_from,tran_fromdate from gal_trn_ttran
																inner join gal_mst_tref on ref_gid=tran_ref_gid
																inner join gal_mst_temployee on employee_gid=tran_from
																group by tran_ref_gid
														) as b
													on b.tran_from=a.employee_gid
													and b.tran_ref_gid=a.ref_gid
													and date_format(b.tran_fromdate,''%Y-%m-%d'') between date_format(''',@from_date,''',''%Y-%m-%d'') and date_format(''',@to_date,''',''%Y-%m-%d'')
													) as main2 

													on main2.employee_gid=main1.employee_gid
													and main2.ref_gid=main1.ref_gid  ',Query_Search,'
													');

					set @p = Query_Select;
					select @p;
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