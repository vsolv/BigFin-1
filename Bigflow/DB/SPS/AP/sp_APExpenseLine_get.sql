CREATE DEFINER=`developer`@`%` PROCEDURE `sp_APExpenseLine_Get`(in ls_action varchar(2000),in ls_Sub_Type varchar(2000),
in ls_filter json,out message varchar(2000))
sp_APExpense_get:BEGIN

declare Query_Select varchar(2000);
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
		   
                    
                    
      if ls_action='GET' and ls_Sub_Type='EXPENSE_LINE' then
 
				select json_length(ls_filter,'$')into @ls_filter;
              
				if @ls_filter='' or @ls_filter is null then
					set message='NO DATA IN JSON-sp_APExpense_get.';
					leave sp_APExpense_get;
				end if;
                      
				select JSON_UNQUOTE(JSON_EXTRACT(ls_filter, CONCAT('$.Entity_Gid'))) into @Entity_Gid;
          
					#select @Entity_Gids;
          
				set Query_Select=concat('select expense_gid,expense_head,expense_linedesc,
                                                            expense_group,expense_sch16,expense_sch16desc,
															create_by,create_date
                                                            from ap_mst_texpense
                                                            where expense_isactive="Y" and expense_isremoved="N"and
															entity_gid in (',@Entity_Gid,')');
                                                       
				   #SELECT Query_Select;
				  set @p= Query_Select;
				  prepare stmt from @p;
				  execute stmt;
				  select found_rows() into ls_count;
                   # select ls_count;
						  if ls_count>0 then
							   set message='FOUND';
						  else
								set message='NOT FOUND';
						 end if;     
			
      end if;
END
