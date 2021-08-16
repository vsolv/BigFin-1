CREATE  PROCEDURE `sp_Mst_Data_Get`(IN `ls_Type` varchar(32),IN `ls_SubType` varchar(32),
IN `lj_Filters` json,IN `ls_Limit` varchar(32)  ,IN `lj_Classification` json, OUT Message varchar(1024)
)
sp_Mst_Data_Get:BEGIN
### Vishnu 18 2020
Declare Query_Select varchar(5000);
Declare Query_Limit varchar(500);
Declare Query_Search varchar(1024);
declare errno int;
declare i int;
declare msg varchar(1000);
declare li_count int;
declare li_entity_gid int;


       set Query_Limit = '';
       set Query_Search = '';
   if ls_Limit <> '' then
            set @Limit_Start = (SELECT SPLIT_STR((ls_Limit), ',', 1));
            set @Limit_End = (SELECT SPLIT_STR((ls_Limit), ',', 2));

           if @Limit_Start = '' or @Limit_Start < 0 then
                        set Message = 'Error On Supplied Limit Data.';
                       leave sp_Mst_Data_Get;
           End if;

           if @Limit_End = '' or @Limit_End <= 0 then
                        set Message = 'Error On Supplied Limit Data.';
                       leave sp_Mst_Data_Get;
           End if;

           set Query_Limit = concat(' Limit ',@Limit_Start,' , ',@Limit_End,' ' );

           ##select Query_Limit ;

   End if;

   select fn_Classification('ENTITY_ONLY',lj_Classification) into @OutMsg_Classification ;
        select  JSON_UNQUOTE(JSON_EXTRACT(@OutMsg_Classification, '$.Entity_Gid[0]')) into @Entity_Gids;
        if @Entity_Gids is  null or @Entity_Gids = '' then
				select  JSON_UNQUOTE(JSON_EXTRACT(@OutMsg_Classification, '$.Message')) into @Message;
				set Message = concat('Error On Classification Data - ',@Message);
                leave sp_Mst_Data_Get;
        End if;

if ls_Type = 'EMPLOYEE' and ls_SubType = 'EMPLOYEE_ALL' then

				Select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters,CONCAT('$.Employee_name'))) into @Employee_name ;
				if @Employee_name is not null and @Employee_name <> '' then
						set Query_Search = concat(Query_Search, ' and employee_name like ''%',@Employee_name,'%'' ');
						set Query_Limit = '';
				End if;


				set Query_Select = '';
				set Query_Select = concat('select employee_code,employee_gid,employee_name from gal_mst_temployee where employee_isactive = ''Y''
							and employee_isremoved = ''N'' and entity_gid in (',@Entity_Gids,')
							 ',Query_Search,' ',Query_Limit,'');

						    set @p = Query_Select;
							##select @p;
							PREPARE stmt FROM @p;
							EXECUTE stmt;
							Select found_rows() into li_count;
							DEALLOCATE PREPARE stmt;

									if li_count > 0 then
											set Message = 'FOUND';
									else
											set Message = 'NOT_FOUND';
									end if;
end if;

END