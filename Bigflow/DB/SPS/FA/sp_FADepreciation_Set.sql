CREATE DEFINER=`developer`@`%` PROCEDURE `galley`.`sp_FADepreciation_Set`(IN `ls_Action` varchar(32),IN `ls_Type` varchar(32),
IN `ls_Sub_Type` varchar(32),IN `lj_Details` json,IN `lj_Other` json,IN `lj_Classification` json,
IN `ls_Createby` varchar(16),OUT `Message` varchar(1024)
)
sp_FADepreciation_Set:BEGIN
#### Ramesh Nov 4 2019
Declare errno int;
Declare msg varchar(1000);
Declare i int;
Declare j int;
Declare z int;
#Declare Query_Select varchar(2048);
Declare Query_Insert LONGTEXT;
Declare Query_Update varchar(2018);
Declare Query_Column varchar(1024);
Declare Query_Value varchar(1024);
Declare countRow int;
#Declare Query_Text LONGTEXT;

  declare  DepValuePerDay FLOAT8 ;
  declare  DepValueTotalD FLOAT8 ;
 declare lj_assetDataD json;
declare lj_assetDep_Grp json;
Declare asset_countD int;

#Declare AssetDetails_Gid varchar(2048);
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

     select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid[0]'))) into @Entity_Gid;

             if @Entity_Gid is  null or @Entity_Gid = 0 or @Entity_Gid = '' then
					set Message = 'Entity Gid Is Needed.';
                    leave sp_FADepreciation_Set;
             End if;

		select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid[0]'))) into @Entity_Gid;

             if @Entity_Gid is  null or @Entity_Gid = 0 or @Entity_Gid = '' then
					set Message = 'Entity Gid Is Needed.';
                    leave sp_FADepreciation_Set;
             End if;

SET SESSION group_concat_max_len=4294967295;
               set @li_json_count_Details = 0 ;
 				select JSON_LENGTH(lj_Details,'$') into @li_json_count_Details ;
                    #select @li_json_count_Details;
                   if @li_json_count_Details is null or @li_json_count_Details = 0 then
						set Message = 'No Data In Json - data.';
						leave sp_FADepreciation_Set;
					end if;

                set @Is_Commit = '';
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Is_Commit'))) into @Is_Commit;

if @Is_Commit = 'Y' THEN
  start transaction;
  set autocommit = 0 ;
 select 'Error';
End if;

if ls_Type = 'DEPRECATION' and ls_Sub_Type = 'REGULAR' then
			        ### Calculate for all

                      select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Calculate_For'))) into @Deprecation_Calculate_For;
					  select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.From_Date'))) into @DepCalFrom_DateD;
					  select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.To_Date'))) into @DepCalTo_DateD;
                      select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.DepType'))) into @DepTypeD;

                      if @DepTypeD = 'REGULAR' then
							set @DepTypeD = '1';
                      End if;

                   # ### Validation

                      if @Deprecation_Calculate_For = 'ALL' then
							#### if for all . check that no data in TMP Table.
                            set @assetdetail_exist = 0 ;
                            Select ifnull(max(a.assetdetails_gid),0) into @assetdetail_exist from fa_tmp_tassetdetails as a
							where a.assetdetails_requestfor <> 'NEW' ;

                            if @assetdetail_exist <> 0 then
									set Message = 'Some Assets Are In Process.Deprecation Will Not Calculate.' ;
                                #    leave sp_FADepreciation_Set;
                            End if;

                      End if;

                      if @DepCalFrom_DateD is null or @DepCalFrom_DateD = '' then
						set Message = 'Depreciation From Date Is Needed.';
                        leave sp_FADepreciation_Set;
                      End if;

                      if @DepCalTo_DateD is null or @DepCalTo_DateD = '' then
						set Message = 'Depreciation To Date Is Needed.';
                        leave sp_FADepreciation_Set;
                      End if;

                      #### Know the Number of Days.
                      select datediff(@DepCalTo_DateD,@DepCalFrom_DateD) into @DepDaysD ;
                      select date_format(@DepCalTo_DateD,'%m') into @DepMonthD ;
                      select date_format(@DepCalTo_DateD,'%Y') into @DepYearD ;
                      #

                     #### Get data from Dep settings
                     set @Dep_Settings_DepType = '';
                     Select ifnull(depsettings_deptype,'') into @Dep_Settings_DepType
                     from fa_mst_tdepsettings as a
                     where a.depsettings_isactive = 'Y' and a.depsettings_isremoved = 'N'
                     ;

                    if @Dep_Settings_DepType = '' or @Dep_Settings_DepType is null  then
                       set Message ='Error On Depreciation Settings Data.';
                       leave sp_FADepreciation_Set;
                    End if;
                       set Query_Column = '';
                 	   if @Dep_Settings_DepType = 'ITC' then
		                   set Query_Column = 'depreciation_itcvalue';
		                ELSEIF @Dep_Settings_DepType = 'CA' THEN
		                    set Query_Column = 'depreciation_cavalue';
		                ELSEIF @Dep_Settings_DepType = 'MGMT' THEN
		                    set Query_Column = 'depreciation_mgmtvalue';
		                ELSE
		                  set Message = '';
		                End if;


                     ### Group By Asset Cat - CP date
						       Select ifnull(concat('[',group_concat(distinct json_object('asset_cpdate',a.assetdetails_capdate,
                                'asset_cat_gid',b.assetcat_gid)),']'),'[]')
									into lj_assetDep_Grp
								 from fa_trn_tassetdetails as a
								 inner join fa_mst_tassetcat as b on b.assetcat_gid = a.assetdetails_assetcatgid
								where a.assetdetails_deponhold = 'N' and a.assetdetails_status = 'ACTIVE'
								and  a.assetdetails_isactive = 'Y' and a.assetdetails_isremoved = 'N'
								and b.assetcat_isactive = 'Y' and b.assetcat_isremoved = 'N'
                                #group by a.assetdetails_assetcatgid
                                ;

                               select JSON_LENGTH(lj_assetDep_Grp,'$') into @li_json_count_Dep_Grp ;

                                if @li_json_count_Dep_Grp = 0 or @li_json_count_Dep_Grp is null THEN
                                   set Message = 'Error On Depreciation Grouping.';
                                   leave sp_FADepreciation_Set;
                                End if;

                               set z = 0 ;
                               While z <= @li_json_count_Dep_Grp -1 DO
                                 select JSON_UNQUOTE(JSON_EXTRACT(lj_assetDep_Grp,CONCAT('$[',z,'].asset_cpdate'))) into @asset_cpdateD;
                                 select JSON_UNQUOTE(JSON_EXTRACT(lj_assetDep_Grp,CONCAT('$[',z,'].asset_cat_gid'))) into @asset_cat_gidD;


	                                if @asset_cpdateD is null or @asset_cpdateD = '' THEN
	                                  set Message = 'CP Date Error.';
	                                  leave  sp_FADepreciation_Set;
	                                End if;

	                                if @asset_cat_gidD is null or @asset_cat_gidD = 0 THEN
	                                  set Message = 'Asset Category Error.';
	                                  leave sp_FADepreciation_Set;
	                                End if;

	                            Select ifnull(concat('[',group_concat(json_object('asset_gid',a.assetdetails_gid,'asset_cost',a.assetdetails_cost,
                                'asset_value',a.assetdetails_value,'asset_cpdate',a.assetdetails_capdate,'asset_deptype',b.assetcat_deptype,
                                'asset_deprate',
                              	  case
                                      when b.assetcat_deprate_itc <> 0 then b.assetcat_deprate_itc
                                      when b.assetcat_deprate_ca <> 0 then b.assetcat_deprate_ca
                                      when b.assetcat_deprate_mgmt <> 0 then b.assetcat_deprate_mgmt
                                	end,
                                	'dep_gl',
                                	CASE
                                	   when b.assetcat_depgl_itc <> '' then b.assetcat_depgl_itc
                                	   when b.assetcat_depgl_ca <> '' then b.assetcat_depgl_ca
                                	   when b.assetcat_depgl_mgmt <> '' then b.assetcat_depgl_mgmt
                                	 end,
                                	 'dep_res_gl',
                                	CASE
                                	   when b.assetcat_depresgl_itc <> '' then b.assetcat_depresgl_itc
                                	   when b.assetcat_depresgl_ca <> '' then b.assetcat_depresgl_ca
                                	   when b.assetcat_depresgl_mgmt <> '' then b.assetcat_depresgl_mgmt
                                	 end,
	                                'asset_lifetime',b.assetcat_lifetime)),']'),'{}')
										into lj_assetDataD
									 from fa_trn_tassetdetails as a
									 inner join fa_mst_tassetcat as b on b.assetcat_gid = a.assetdetails_assetcatgid
									where a.assetdetails_deponhold = 'N' and a.assetdetails_status = 'ACTIVE'
									and  a.assetdetails_isactive = 'Y' and a.assetdetails_isremoved = 'N'
									and b.assetcat_isactive = 'Y' and b.assetcat_isremoved = 'N'
									and a.assetdetails_capdate = @asset_cpdateD and a.assetdetails_assetcatgid = @asset_cat_gidD
	                                ;
                                ### TO DO New Column - Asset Life Time
                                #### Validation as per test cases  :: TO DO

                                select JSON_LENGTH(lj_assetDataD,'$') into asset_countD ;

                                if asset_countD = 0 or asset_countD is null then
									set Message = 'No Asset Data To Deprecation.';
                                    rollback;
                                    leave sp_FADepreciation_Set;
                                End if;

                               #set Query_Text = '';
                                 set i = 0;

                                While i <= asset_countD -1 DO

                                       select JSON_UNQUOTE(JSON_EXTRACT(lj_assetDataD,CONCAT('$[',i,'].asset_gid'))) into @asset_gidD;
                                       select JSON_UNQUOTE(JSON_EXTRACT(lj_assetDataD,CONCAT('$[',i,'].asset_cost'))) into @asset_costD;
                                       select JSON_UNQUOTE(JSON_EXTRACT(lj_assetDataD,CONCAT('$[',i,'].asset_value'))) into @asset_valueD;
                                       select JSON_UNQUOTE(JSON_EXTRACT(lj_assetDataD,CONCAT('$[',i,'].asset_cpdate'))) into @asset_cpdateD;
                                       select JSON_UNQUOTE(JSON_EXTRACT(lj_assetDataD,CONCAT('$[',i,'].asset_deptype'))) into @asset_deptypeD;
                                       select JSON_UNQUOTE(JSON_EXTRACT(lj_assetDataD,CONCAT('$[',i,'].asset_deprate'))) into @asset_deprateD;
                                       select JSON_UNQUOTE(JSON_EXTRACT(lj_assetDataD,CONCAT('$[',i,'].asset_lifetime'))) into @asset_lifetimeD;
                                       select JSON_UNQUOTE(JSON_EXTRACT(lj_assetDataD,CONCAT('$[',i,'].dep_gl'))) into @Dep_Gl;
                                       select JSON_UNQUOTE(JSON_EXTRACT(lj_assetDataD,CONCAT('$[',i,'].dep_res_gl'))) into @Dep_res_Gl ;

                                       #### Know the Last Deprecation date

                                      set @Last_depDateD = '';
                                       Select ifnull(max(depreciation_todate) ,'') into @Last_depDateD
										from fa_trn_tdepreciation
										where depreciation_assetdetailsgid = @asset_gidD and depreciation_isactive = 'Y' and depreciation_isremoved = 'N' ;

                                      if @Last_depDateD <> '' and @Last_depDateD is not null then
											if @DepCalFrom_DateD <= @Last_depDateD then
													set Message = 'Already Depreciation Run For The Asset.';
                                                    #rollback;
                                                    #leave sp_FADepreciation_Set;
                                            End if;
                                      End if;


                                      if @asset_deptypeD = 'SLM' then
                                         ### Get Rate Per Day
                                         set DepValuePerDay = ((@asset_costD * @asset_deprateD) / 100)/365;
                                         set DepValueTotalD = @DepDaysD * DepValuePerDay;
                                         set DepValueTotalD = cast(DepValueTotalD as decimal(16,2));

								  		elseif @asset_deptypeD = 'WDV' then
                                            set DepValuePerDay = ((@asset_valueD * @asset_deprateD) / 100)/365;
											set DepValueTotalD = @DepDaysD * DepValuePerDay;      ### TO DO Update
											set DepValueTotalD = cast(DepValueTotalD as decimal(16,2));
                                     else
                                         set Message = 'Error On Depreciation Type.';
                                         leave sp_FADepreciation_Set;
									End if;

                                    #select @asset_valueD,@asset_deprateD,@DepValueTotalD;
                                    #leave sp_FADepreciation_Set;

                                      ### Insert Process
                                      #select @asset_gidD,@DepCalFrom_DateD,@DepCalTo_DateD,@DepMonthD,@DepYearD,@DepValueTotalD,@DepTypeD,@Entity_Gid,ls_Createby;

								       Select ifnull(max(a.depreciation_gid),0) into @Dep_Runed_Gid from fa_trn_tdepreciation as a
								       where a.depreciation_assetdetailsgid = @asset_gidD and a.depreciation_fromdate = @DepCalFrom_DateD
								       and a.depreciation_todate = @DepCalTo_DateD
								       and a.depreciation_isactive = 'Y' and a.depreciation_isremoved = 'N';

								      if @Dep_Runed_Gid = 0 THEN

								               set Query_Value = DepValueTotalD;


						         				 set Query_Insert = '';
                               					 set Query_Insert = concat('Insert into fa_trn_tdepreciation (depreciation_assetdetailsgid,depreciation_fromdate,depreciation_todate,depreciation_month,
																depreciation_year,',Query_Column,',depreciation_value,depreciation_type,depreciation_gl,depreciation_resgl,
																entity_gid,create_by
																) values (''',@asset_gidD,''',''',@DepCalFrom_DateD,''',''',@DepCalTo_DateD,''',''',@DepMonthD,''',
                                                                ''',@DepYearD,''',''',Query_Value,''',''',DepValueTotalD,''',''',@DepTypeD,''',''',@Dep_Gl,''',''',@Dep_res_Gl,''',
																''',@Entity_Gid,''',''',ls_Createby,''')
																');

                                                        set @Insert_query = Query_Insert;
														#SELECT @Insert_query;
														PREPARE stmt FROM @Insert_query;
														EXECUTE stmt;
														set countRow = (select ROW_COUNT());
														DEALLOCATE PREPARE stmt;

														if countRow > 0 then
															set Message = 'SUCCESS';
											           else
													      set Message = 'FAIL';
											           End if;
											     /*
											          if Query_Text = '' THEN
											             set Query_Text = concat('
     													(''',@asset_gidD,''',''',@DepCalFrom_DateD,''',''',@DepCalTo_DateD,''',''',@DepMonthD,''',
                                                                ''',@DepYearD,''',''',Query_Value,''',''',DepValueTotalD,''',''',@DepTypeD,''',''',@Dep_Gl,''',''',@Dep_res_Gl,''',
																''',@Entity_Gid,''',''',ls_Createby,''')
                                                        '
											          );
											         ELSE
											            set Query_Text = concat(Query_Text,',',
											            '
     													(''',@asset_gidD,''',''',@DepCalFrom_DateD,''',''',@DepCalTo_DateD,''',''',@DepMonthD,''',
                                                                ''',@DepYearD,''',''',Query_Value,''',''',DepValueTotalD,''',''',@DepTypeD,''',''',@Dep_Gl,''',''',@Dep_res_Gl,''',
																''',@Entity_Gid,''',''',ls_Createby,''')
                                                        '
											          );
											          End if;


											       */
                                      ELSEIF @Dep_Runed_Gid > 0 THEN
                                            set Query_Update = '';
                                            set Query_Update = concat('update fa_trn_tdepreciation set ',Query_Column,' = ''',DepValueTotalD,''' ,update_by = ''',ls_Createby,''',update_date = now()
												where depreciation_gid = ''',@Dep_Runed_Gid,''' and entity_gid = ''',@Entity_Gid,''' ');

													set @Update_query = Query_Update;
														#SELECT @Update_query;
														PREPARE stmt FROM @Update_query;
														EXECUTE stmt;
														set countRow = (select ROW_COUNT());
														DEALLOCATE PREPARE stmt;

														if countRow > 0 then
															set Message = 'SUCCESS';
											           else
													      set Message = 'FAIL';
											           End if;

								      End if;

                                                     UPDATE fa_trn_tassetdetails SET assetdetails_cost = assetdetails_cost - cast(DepValueTotalD as decimal(16,2))
                                                      WHERE assetdetails_gid = @asset_gidD;

                                                     set countRow = (select ROW_COUNT());
                                                     if countRow > 0 then
															set Message = 'SUCCESS';
											           else
													      set Message = 'FAIL';
											           End if;
                                                             ## TO DO

                                       set i = i+1;
                                End While;

	                               /*
                               						         				 set Query_Insert = '';
                               					 set Query_Insert = concat('Insert into fa_trn_tdepreciation (depreciation_assetdetailsgid,depreciation_fromdate,depreciation_todate,depreciation_month,
																depreciation_year,',Query_Column,',depreciation_value,depreciation_type,depreciation_gl,depreciation_resgl,
																entity_gid,create_by
																) values ',Query_Text,'
																');

                                                        set @Insert_query = '';
														set @Insert_query = Query_Insert ;
														PREPARE stmt FROM @Insert_query;
														EXECUTE stmt;
														set countRow = (select ROW_COUNT());
														DEALLOCATE PREPARE stmt;
                                                       set Query_Text = '';
														if countRow > 0 then
															set Message = 'SUCCESS';
											           else
													      set Message = 'FAIL';
											           End if;

                               */

                                #select z,now(),i;
                               set z = z+1;
                               End While;




ELSEIF ls_Action='UPDATE' and  ls_Type = 'DEPRECIATION' and ls_Sub_Type = 'FLAG' then

					select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Depreciation_Gid'))) into @Depreciation_Gid;


							if  @Depreciation_Gid is null or @Depreciation_Gid = '' or @Depreciation_Gid = 0 then
									set Message = 'Depreciation Gid Is Not Given ';
								    leave sp_FADepreciation_Set;
							end if;


                        set Query_Update = '';
						set Query_Update = concat('Update fa_trn_tdepreciation
													   set  depreciation_isactive=''N'',
														    depreciation_isremoved=''Y'',
                                                            update_by=',ls_Createby,',
                                                            update_date=now()
                                                    where depreciation_gid in (',@Depreciation_Gid,')
                                                    and depreciation_isactive=''Y'' and
														depreciation_isremoved=''N''and
                                                        entity_gid=',@Entity_Gid,'
												');

										set @Query_Update = Query_Update;
										#SELECT @Query_Update;
										PREPARE stmt FROM @Query_Update;
										EXECUTE stmt;
										set countRow = (select ROW_COUNT());
										DEALLOCATE PREPARE stmt;

													if countRow > 0 then
														set Message = 'SUCCESS';
													else
														set Message = 'FAIL';
													End if;

ELSEIF ls_Type = 'DEPRECATION' and ls_Sub_Type = 'SINGLEPROCESS' then

   select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_Gids'))) into @Asset_Gids;
   select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.From_Date'))) into @DepCalFrom_DateD;
   select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.To_Date'))) into @DepCalTo_DateD;

     if @Asset_Gids is null or @Asset_Gids = 0 then
        set Message = 'Asset Gid Is Null.';
        leave sp_FADepreciation_Set;
     End if;

    if @DepCalFrom_DateD is null or @DepCalFrom_DateD = '' then
       set Message = 'Depreciation From Date Is Needed.';
        leave sp_FADepreciation_Set;
    End if;

    if @DepCalTo_DateD is null or @DepCalTo_DateD = '' THEN
      set Message = 'Depreciation To Date Is Needed.';
      leave sp_FADepreciation_Set;
    End if;

        #### Know the Number of Days.
                      select datediff(@DepCalTo_DateD,@DepCalFrom_DateD) into @DepDaysD ;
                      select date_format(@DepCalTo_DateD,'%m') into @DepMonthD ;
                      select date_format(@DepCalTo_DateD,'%Y') into @DepYearD ;
                      #

      #### Get data from Dep settings
                     set @Dep_Settings_DepType = '';
                     Select ifnull(depsettings_deptype,'') into @Dep_Settings_DepType
                     from fa_mst_tdepsettings as a
                     where a.depsettings_isactive = 'Y' and a.depsettings_isremoved = 'N'
                     ;

                    if @Dep_Settings_DepType = '' or @Dep_Settings_DepType is null  then
                       set Message ='Error On Depreciation Settings Data.';
                       leave sp_FADepreciation_Set;
                    End if;
                       set Query_Column = '';
                 	   if @Dep_Settings_DepType = 'ITC' then
		                   set Query_Column = 'depreciation_itcvalue';
		                ELSEIF @Dep_Settings_DepType = 'CA' THEN
		                    set Query_Column = 'depreciation_cavalue';
		                ELSEIF @Dep_Settings_DepType = 'MGMT' THEN
		                    set Query_Column = 'depreciation_mgmtvalue';
		                ELSE
		                  set Message = '';
		                End if;


    	 Select ifnull(concat('[',group_concat(json_object('asset_gid',a.assetdetails_gid,'asset_cost',a.assetdetails_cost,
            'asset_value',a.assetdetails_value,'asset_cpdate',a.assetdetails_capdate,'asset_deptype',b.assetcat_deptype,
            'asset_deprate',
          	  case
                  when b.assetcat_deprate_itc <> 0 then b.assetcat_deprate_itc
                  when b.assetcat_deprate_ca <> 0 then b.assetcat_deprate_ca
                  when b.assetcat_deprate_mgmt <> 0 then b.assetcat_deprate_mgmt
            	end,
            	'dep_gl',
            	CASE
            	   when b.assetcat_depgl_itc <> '' then b.assetcat_depgl_itc
            	   when b.assetcat_depgl_ca <> '' then b.assetcat_depgl_ca
            	   when b.assetcat_depgl_mgmt <> '' then b.assetcat_depgl_mgmt
            	 end,
            	 'dep_res_gl',
            	CASE
            	   when b.assetcat_depresgl_itc <> '' then b.assetcat_depresgl_itc
            	   when b.assetcat_depresgl_ca <> '' then b.assetcat_depresgl_ca
            	   when b.assetcat_depresgl_mgmt <> '' then b.assetcat_depresgl_mgmt
            	 end,
                'asset_lifetime',b.assetcat_lifetime)),']'),'{}')
					into lj_assetDataD
				 from fa_trn_tassetdetails as a
				 inner join fa_mst_tassetcat as b on b.assetcat_gid = a.assetdetails_assetcatgid
				where a.assetdetails_deponhold = 'N' and a.assetdetails_status = 'ACTIVE'
				and  a.assetdetails_isactive = 'Y' and a.assetdetails_isremoved = 'N'
				and b.assetcat_isactive = 'Y' and b.assetcat_isremoved = 'N'
				and a.assetdetails_gid = @Asset_Gids;

			         select JSON_LENGTH(lj_assetDataD,'$') into asset_countD ;

                        if asset_countD = 0 or asset_countD is null then
							set Message = 'No Asset Data To Depreciation.';
                            leave sp_FADepreciation_Set;
                        End if;

                               #set Query_Text = '';
                                 set i = 0;

                                While i <= asset_countD -1 DO

                                       select JSON_UNQUOTE(JSON_EXTRACT(lj_assetDataD,CONCAT('$[',i,'].asset_gid'))) into @asset_gidD;
                                       select JSON_UNQUOTE(JSON_EXTRACT(lj_assetDataD,CONCAT('$[',i,'].asset_cost'))) into @asset_costD;
                                       select JSON_UNQUOTE(JSON_EXTRACT(lj_assetDataD,CONCAT('$[',i,'].asset_value'))) into @asset_valueD;
                                       select JSON_UNQUOTE(JSON_EXTRACT(lj_assetDataD,CONCAT('$[',i,'].asset_cpdate'))) into @asset_cpdateD;
                                       select JSON_UNQUOTE(JSON_EXTRACT(lj_assetDataD,CONCAT('$[',i,'].asset_deptype'))) into @asset_deptypeD;
                                       select JSON_UNQUOTE(JSON_EXTRACT(lj_assetDataD,CONCAT('$[',i,'].asset_deprate'))) into @asset_deprateD;
                                       select JSON_UNQUOTE(JSON_EXTRACT(lj_assetDataD,CONCAT('$[',i,'].asset_lifetime'))) into @asset_lifetimeD;
                                       select JSON_UNQUOTE(JSON_EXTRACT(lj_assetDataD,CONCAT('$[',i,'].dep_gl'))) into @Dep_Gl;
                                       select JSON_UNQUOTE(JSON_EXTRACT(lj_assetDataD,CONCAT('$[',i,'].dep_res_gl'))) into @Dep_res_Gl ;

                                       #### Know the Last Deprecation date

                                      set @Last_depDateD = '';
                                       Select ifnull(max(depreciation_todate) ,'') into @Last_depDateD
										from fa_trn_tdepreciation
										where depreciation_assetdetailsgid = @asset_gidD and depreciation_isactive = 'Y' and depreciation_isremoved = 'N' ;

                                      if @Last_depDateD <> '' and @Last_depDateD is not null then
											if @DepCalFrom_DateD <= @Last_depDateD then
													set Message = 'Already Depreciation Run For The Asset.';
                                                    #rollback;
                                                    #leave sp_FADepreciation_Set;
                                                    ## TO DO
                                            End if;
                                      End if;


                                      if @asset_deptypeD = 'SLM' then
                                         ### Get Rate Per Day
                                         set DepValuePerDay = ((@asset_costD * @asset_deprateD) / 100)/365;
                                         set DepValueTotalD = @DepDaysD * DepValuePerDay;
                                         set DepValueTotalD = cast(DepValueTotalD as decimal(16,2));

								  	  elseif @asset_deptypeD = 'WDV' then
                                            set DepValuePerDay = ((@asset_valueD * @asset_deprateD) / 100)/365;
											set DepValueTotalD = @DepDaysD * DepValuePerDay;      ### TO DO Update
											set DepValueTotalD = cast(DepValueTotalD as decimal(16,2));
                                      else
                                         set Message = 'Error On Depreciation Type.';
                                         leave sp_FADepreciation_Set;
									  End if;

									 if DepValueTotalD is null or DepValueTotalD = 0 THEN
									   set Message ='Error On Depreciation Calculate.';

									  leave sp_FADepreciation_Set;
									 End if;

									# select DepValueTotalD,@asset_costD,@asset_deprateD,@asset_deptypeD,@DepValuePerDay,@DepDaysD;

                                    #select @asset_valueD,@asset_deprateD,@DepValueTotalD;
                                    #leave sp_FADepreciation_Set;

                                      ### Insert Process
                                      #select @asset_gidD,@DepCalFrom_DateD,@DepCalTo_DateD,@DepMonthD,@DepYearD,@DepValueTotalD,@DepTypeD,@Entity_Gid,ls_Createby;

								       Select ifnull(max(a.depreciation_gid),0) into @Dep_Runed_Gid from fa_trn_tdepreciation as a
								       where a.depreciation_assetdetailsgid = @asset_gidD and a.depreciation_fromdate = @DepCalFrom_DateD
								       and a.depreciation_todate = @DepCalTo_DateD
								       and a.depreciation_isactive = 'Y' and a.depreciation_isremoved = 'N';

								      if @Dep_Runed_Gid = 0 THEN

								               set Query_Value = DepValueTotalD;

								           #select @asset_gidD,@DepCalFrom_DateD,@DepCalTo_DateD,@DepMonthD,@DepYearD,Query_Value,DepValueTotalD,@DepTypeD,@Dep_Gl,@Dep_res_Gl,
								            #  @Entity_Gid,ls_Createby;

								              set @DepTypeD = 1;

						         				 set Query_Insert = '';
                               					 set Query_Insert = concat('Insert into fa_trn_tdepreciation (depreciation_assetdetailsgid,depreciation_fromdate,depreciation_todate,depreciation_month,
																depreciation_year,',Query_Column,',depreciation_value,depreciation_type,depreciation_gl,depreciation_resgl,
																entity_gid,create_by
																) values (''',@asset_gidD,''',''',@DepCalFrom_DateD,''',''',@DepCalTo_DateD,''',''',@DepMonthD,''',
                                                                ''',@DepYearD,''',''',Query_Value,''',''',DepValueTotalD,''',''',@DepTypeD,''',''',@Dep_Gl,''',''',@Dep_res_Gl,''',
																''',@Entity_Gid,''',''',ls_Createby,''')
																');

                                                        set @Insert_query = Query_Insert;
														#SELECT @Insert_query;
														PREPARE stmt FROM @Insert_query;
														EXECUTE stmt;
														set countRow = (select ROW_COUNT());
														DEALLOCATE PREPARE stmt;

														if countRow > 0 then
															set Message = 'SUCCESS';
											           else
													      set Message = 'FAIL';
											           End if;

                                      ELSEIF @Dep_Runed_Gid > 0 THEN
                                            set Query_Update = '';
                                            set Query_Update = concat('update fa_trn_tdepreciation set ',Query_Column,' = ''',DepValueTotalD,''' ,update_by = ''',ls_Createby,''',update_date = now()
												where depreciation_gid = ''',@Dep_Runed_Gid,''' and entity_gid = ''',@Entity_Gid,''' ');

													set @Update_query = Query_Update;
														#SELECT @Update_query;
														PREPARE stmt FROM @Update_query;
														EXECUTE stmt;
														set countRow = (select ROW_COUNT());
														DEALLOCATE PREPARE stmt;

														if countRow > 0 then
															set Message = 'SUCCESS';
											           else
													      set Message = 'FAIL In Depreciation Update.';
													     leave sp_FADepreciation_Set;
											           End if;

								      End if;


                                                     UPDATE fa_trn_tassetdetails SET assetdetails_cost = assetdetails_cost - cast(DepValueTotalD as decimal(16,2)),update_by = ls_Createby,
                                                      update_date = now()
                                                      WHERE assetdetails_gid = @asset_gidD;
                                                    # select @asset_gidD;

                                                     set countRow = (select ROW_COUNT());
                                                     if countRow > 0 then
															set Message = 'SUCCESS';
											           else
													      set Message = 'FAIL In Asset Update';
													     leave sp_FADepreciation_Set;
											           End if;
                                                             ## TO DO

                                       set i = i+1;
                                End While;


End if;

if Message = 'SUCCESS' THEN
   commit;
ELSE
   ROLLBACK;
End if;


END