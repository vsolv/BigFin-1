CREATE  PROCEDURE `galley`.`sp_AllTableValues_Get`(
In `Type` varchar(64),
in `lj_table_values` json,
in `li_entity_gid` int,
Out `Message` varchar(1000)
)
sp_AllTableValues_Get:BEGIN
# Ramesh : May 28 2018

Declare Query_Limit varchar(500);
declare Query_Select varchar(1000);
 set Query_Select = '';
	select JSON_LENGTH(lj_table_values,'$') into @li_json_count;

    if @li_json_count = 0 then
		set Message = 'No Table Datas.';
        leave sp_AllTableValues_Get;
    End if;

    select JSON_UNQUOTE(JSON_EXTRACT(lj_table_values, CONCAT('$.Table_name[0]'))) into @lsTable_Name;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_table_values, CONCAT('$.Column_1[0]'))) into @Column_1;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_table_values, CONCAT('$.Where_Common[0]'))) into @Common;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_table_values, CONCAT('$.Where_Primary[0]'))) into @Primary_Column;
	select JSON_UNQUOTE(JSON_EXTRACT(lj_table_values, CONCAT('$.Primary_Value[0]'))) into @Primary_value;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_table_values, CONCAT('$.Where_Data[0]'))) into @Where_Data;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_table_values, CONCAT('$.Primary_Data[0]'))) into @Primary_Data;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_table_values, CONCAT('$.Limits[0]'))) into @Limits;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_table_values, CONCAT('$.Order_by[0]'))) into @Order_by;

    set Query_Limit = '';
		if @Limits <> '' then
		   set @Limit_Start = (SELECT SPLIT_STR((@Limits), ',', 1));
		   set @Limit_End = (SELECT SPLIT_STR((@Limits), ',', 2));

			   if @Limit_Start = '' or @Limit_Start < 0 then
							set Message = 'Error On Supplied Limit Data.';
						   leave sp_AllTableValues_Get;
			   End if;

			   if @Limit_End = '' or @Limit_End <= 0 then
							set Message = 'Error On Supplied Limit Data.';
						   leave sp_AllTableValues_Get;
			   End if;

           	set Query_Limit = concat(' Limit ',@Limit_Start,' , ',@Limit_End,' ' );

           ##select Query_Limit ;
	    End if;

      #select  @Primary_value;
      set Query_Select = concat('select ',@Column_1, ' from ',@lsTable_Name,'
								where ',@Common, '_isactive = ''Y'' and ',@Common,'_isremoved = ''N''
                                and entity_gid = ',li_entity_gid,'
                                ');

		 if  @Primary_value <> '' then
				set Query_Select = concat(Query_Select, ' and ',@Common,'_',@Primary_Column ,' in (''',@Primary_value,''')' );
		 End if;

		 if @Where_Data <> '' and @Where_Data is not null and @Primary_Data <> '' and @Primary_Data is not null THEN
		    	set Query_Select = concat(Query_Select, ' and ',@Common,'_',@Where_Data ,' like ''','%',@Primary_Data,'%',''' ' );
		 End if;

         set Query_Select = concat(Query_Select, ' Order by ',@Common,'_',@Order_by, ' asc' ,Query_Limit );#


   # select Query_Select;
	set @p = Query_Select;
	PREPARE stmt FROM @p;
	EXECUTE stmt;
	DEALLOCATE PREPARE stmt;

END