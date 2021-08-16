CREATE DEFINER=`developer`@`%` PROCEDURE `sp_APExpenseLine_Set`(in ls_action varchar(2000),in ls_type varchar(2000),
in ls_filter json,in ls_classification json,in ls_created_by varchar(2000),out message varchar(2000))
sp_APExpense_set:BEGIN

declare Query_Store varchar(2000);
declare Query_Update varchar(2000);
declare ls_count varchar(2000);
declare errno varchar(200);
declare msg varchar(200);
               
    
                 
                         DECLARE done INT DEFAULT 0;
                         DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
						 DECLARE EXIT HANDLER FOR SQLEXCEPTION,sqlwarning
		                BEGIN
                         GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
                            set Message = concat(errno , msg);
						 ROLLBACK;
                       END;       
        

        if ls_action='INSERT' and ls_type='INSERT_EXPENSE_LINE' then
 
                 select json_length(ls_filter,'$')into @ls_filter;
                 select json_length(ls_classification,'$')into @ls_classification;
  
                 if @ls_filter='' or @ls_filter is null then
                       set message='NO DATA IN JSON-sp_APExpense_set.';
                        leave sp_APExpense_set;
                end if;
  
                if @ls_classification='' or @ls_classification is null then
                    set message='NO DATA IN JSON-sp_APExpense_set.';
                    leave sp_APExpense_set;
                end if;
						
				 Select JSON_UNQUOTE(JSON_EXTRACT(ls_filter,CONCAT('$.Expense_Head'))) into @Expense_Head ;    
				 Select JSON_UNQUOTE(JSON_EXTRACT(ls_filter,CONCAT('$.Expense_Linedesc'))) into @Expense_Linedesc ;    
				 Select JSON_UNQUOTE(JSON_EXTRACT(ls_filter,CONCAT('$.Expense_Group'))) into @Expense_Group ;    
				 Select JSON_UNQUOTE(JSON_EXTRACT(ls_filter,CONCAT('$.Expense_Sch16'))) into @Expense_Sch16 ;    
				 Select JSON_UNQUOTE(JSON_EXTRACT(ls_filter,CONCAT('$.Expense_Sch16desc'))) into @Expense_Sch16desc ;    
				 Select JSON_UNQUOTE(JSON_EXTRACT(ls_classification,CONCAT('$.Entity_Gid'))) into @Entity_Gid ;    
				 
	 
				 if @Expense_Head='' or @Expense_Head is null then 
						   set message='Expense_Head is not given - sp_APExpense_set.';
					  leave sp_APExpense_set;
				end if;
				
				if @Expense_Linedesc='' or @Expense_Linedesc is null then 
						   set message='Expense_Linedesc is not given - sp_APExpense_set.';
					  leave sp_APExpense_set;
				end if;
			  
			  if @Expense_Group='' or @Expense_Group is null then 
						   set message='Expense_Group is not given - sp_APExpense_set.';
					  leave sp_APExpense_set;
				end if;
				
				
				 if @Expense_Sch16='' or @Expense_Sch16 is null then 
						   set message='Expense_Sch16 is not given - sp_APExpense_set.';
					  leave sp_APExpense_set;
				end if;
	 
			   if @Expense_Sch16desc='' or @Expense_Sch16desc is null then 
						   set message='Expense_Sch16desc is not given - sp_APExpense_set.';
					  leave sp_APExpense_set;
				end if;
				
				 if @Entity_Gid='' or @Entity_Gid is null then 
						   set message='Entity_Gid is not given - sp_APExpense_set.';
					  leave sp_APExpense_set;
				end if;
	
                 set Query_Store=' ';
                
                 set Query_Store=concat('insert into ap_mst_texpense
                                                          (expense_head,expense_linedesc,expense_group,
                                                           expense_sch16,expense_sch16desc,
                                                           entity_gid,create_by)
                                                           value
                                                           (''',@Expense_Head,''',''',@Expense_Linedesc,''',''',@Expense_Group,''',
                                                             ''',@Expense_Sch16,''',''',@Expense_Sch16desc,''',
                                                             ',@Entity_Gid,',',ls_created_by,')');
                        # select query_store;
				  set @p=Query_Store;
                  prepare stmt from @p;
                  execute stmt;
                  select row_count() into ls_count;
						 if ls_count>0 then
							 set message='SUCCESS';
					    else
						   set message='NOT SUCCESS- sp_SVSProcess_Set';
						  rollback;
						  leave sp_APExpense_set;
					    end if;       
                                 
       
           
		elseif  ls_action='UPDATE' and ls_type='UPDATE_EXPENSE_LINE' then
         
                 select json_length(ls_filter,'$')into @ls_filter;
                 select json_length(ls_classification,'$')into @ls_classification;
  
                 if @ls_filter='' or @ls_filter is null then
                       set message='NO DATA IN JSON-sp_APExpense_set.';
                       rollback;
                        leave sp_APExpense_set;
                end if;
  
                 if @ls_classification='' or @ls_classification is null then
                     set message='NO DATA IN JSON-sp_APExpense_set.';
                     rollback;
                    leave sp_APExpense_set;
			    end if;

				Select JSON_UNQUOTE(JSON_EXTRACT(ls_filter,CONCAT('$.Expense_Gid'))) into @Expense_Gid ;                   
				Select JSON_UNQUOTE(JSON_EXTRACT(ls_filter,CONCAT('$.Expense_Head'))) into @Expense_Head ;    
				Select JSON_UNQUOTE(JSON_EXTRACT(ls_filter,CONCAT('$.Expense_Linedesc'))) into @Expense_Linedesc ;    
				Select JSON_UNQUOTE(JSON_EXTRACT(ls_filter,CONCAT('$.Expense_Group'))) into @Expense_Group ;    
				Select JSON_UNQUOTE(JSON_EXTRACT(ls_filter,CONCAT('$.Expense_Sch16'))) into @Expense_Sch16 ;    
				Select JSON_UNQUOTE(JSON_EXTRACT(ls_filter,CONCAT('$.Expense_Sch16desc'))) into @Expense_Sch16desc ;    
						 

				if @Expense_Gid='' or @Expense_Gid is null then 
						   set message='Expense_Gid is not given - sp_APExpense_set.';
					  leave sp_APExpense_set;
				end if;
				
				if @Expense_Head='' or @Expense_Head is null then 
						   set message='Expense_Head is not given - sp_APExpense_set.';
					  leave sp_APExpense_set;
				end if;
				
				if @Expense_Linedesc='' or @Expense_Linedesc is null then 
						   set message='Expense_Linedesc is not given - sp_APExpense_set.';
					  leave sp_APExpense_set;
				end if;
				
				if @Expense_Group='' or @Expense_Group is null then 
						   set message='Expense_Group is not given - sp_APExpense_set.';
					  leave sp_APExpense_set;
				end if;
				
				if @Expense_Sch16='' or @Expense_Sch16 is null then 
						   set message='Expense_Sch16 is not given - sp_APExpense_set.';
					  leave sp_APExpense_set;
				end if;
				
				if @Expense_Sch16desc='' or @Expense_Sch16desc is null then 
						   set message='Expense_Sch16desc is not given - sp_APExpense_set.';
					  leave sp_APExpense_set;
				end if;
					  
			 
			   set  Query_Update=' ';
                  
               set Query_Update=concat('UPDATE ap_mst_texpense SET Expense_Head=''',@Expense_Head,''', 
																												  Expense_Linedesc=''',@Expense_Linedesc,''',
										                                                                          Expense_Group=''',@Expense_Group,''',
                                                                                                                  Expense_Sch16=''',@Expense_Sch16,''',
                                                                                                                  Expense_Sch16desc=''',@Expense_Sch16desc,''',
                                                                                                                  Update_by=',ls_created_by,',
                                                                                                                  Update_date= now()                                                                                                                  
                                                              WHERE Expense_Gid in (',@Expense_Gid,')');
			   #select Query_Update;
			   set @p=Query_Update;
			   prepare stmt from @p;
			   execute stmt;
               select row_count() into ls_count;
						 if ls_count>0 then
							  set message='SUCCESS';
					    else
						      set message='NOT SUCCESS- sp_SVSProcess_Set';
						     rollback;
						    leave sp_APExpense_set;
					    end if;       
                    
          end if;      

END
