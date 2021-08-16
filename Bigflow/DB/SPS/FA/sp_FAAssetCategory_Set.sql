CREATE PROCEDURE `sp_FAAssetCategory_Set`(IN `ls_Action` varchar(32),IN `ls_Type` varchar(32),
IN `ls_Sub_Type` varchar(32),IN `lj_Details` json,IN `lj_Classification` json,IN `ls_Createby` varchar(32),
OUT `Message` varchar(1024))
sp_FAAssetCategory:BEGIN

#### Bala Oct 25 2019
Declare errno int;
Declare msg varchar(1000);
Declare Query_Update varchar(1000);
Declare Update_Column varchar(1000);
Declare countRow int;
Declare Query_Insert varchar(9000);

DECLARE EXIT HANDLER FOR SQLEXCEPTION,sqlwarning

		BEGIN
			GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
			set Message = concat(errno , msg);
			ROLLBACK;
		END;

		select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid[0]'))) into @Entity_Gid;
             if @Entity_Gid is  null or @Entity_Gid = 0 or @Entity_Gid = '' then
					set Message = 'Entity Gid Is Needed.';
                    leave sp_FAAssetCategory;
             End if;

		select JSON_LENGTH(lj_Details,'$') into @li_json_count_Details ;
             if @li_json_count_Details is  null or @li_json_count_Details = 0 or @li_json_count_Details = '' then
					set Message = 'No Data In lj_Details Json';
                    leave sp_FAAssetCategory;
             End if;

START TRANSACTION;
set autocommit=0;

if ls_Type = 'ASSET_CAT' and  ls_Sub_Type = 'MST' and ls_Action = 'INSERT' then


                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_SubCategory_Gid'))) into @AssetCat_SubCategory_Gid;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_SubCatName'))) into @AssetCat_SubCatName;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_LifeTime'))) into @Asset_LifeTime;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_DepType'))) into @Asset_DepType;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.AssetCat_Remarks'))) into @AssetCat_Remarks;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_ITC_DepRate'))) into @Dep_Rate_ITC;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_CA_DepRate'))) into @Dep_Rate_CA;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_MGMT_DepRate'))) into @Dep_Rate_MGMT;


					if @AssetCat_SubCategory_Gid is  null or @AssetCat_SubCategory_Gid = '' then
						set Message = 'Asset_SubCategory_Gid Is Needed.';
						leave sp_FAAssetCategory;
					End if;

					if @AssetCat_SubCatName is  null or @AssetCat_SubCatName = '' then
						set Message = 'AssetCat_SubCatName Is Needed.';
						leave sp_FAAssetCategory;
					End if;

					if @Asset_LifeTime is  null or @Asset_LifeTime = '' then
						set Message = 'Asset_LifeTime Is Needed.';
						leave sp_FAAssetCategory;
					End if;

                    if @Asset_DepType is  null or @Asset_DepType = '' then
						set Message = 'Asset_DepType Is Needed.';
						leave sp_FAAssetCategory;
					End if;

                    if @Dep_Rate_ITC is  null or @Dep_Rate_ITC = '' then
						set Message = 'Asset_ITC_DepRate Is Needed.';
						leave sp_FAAssetCategory;
					End if;

                    if @Dep_Rate_CA is  null or @Dep_Rate_CA = '' then
						set Message = 'Asset_CA_DepRate Is Needed.';
						leave sp_FAAssetCategory;
					End if;

                    if @Dep_Rate_MGMT is  null or @Dep_Rate_MGMT = '' then
						set Message = 'Asset_MGMT_DepRate Is Needed.';
						leave sp_FAAssetCategory;
					End if;

                    if @AssetCat_Remarks is  null or @AssetCat_Remarks = '' then
						set Message = 'AssetCat_Remarks Is Needed.';
						leave sp_FAAssetCategory;
					End if;

				set @Asset_DepRate=0;#REMOVE THIS Column in future
				set Query_Insert = '';
				set Query_Insert = concat('
							INSERT INTO fa_mst_tassetcat
									(assetcat_subcategorygid,assetcat_subcatname,
									 assetcat_lifetime,assetcat_deptype,
									 assetcat_deprate_itc,assetcat_deprate_ca,
                                     assetcat_deprate_mgmt,assetcat_deprate,
									 assetcat_remarks,entity_gid,create_by)
							  values(',@AssetCat_SubCategory_Gid,',''',@AssetCat_SubCatName,''',
                                     ''',@Asset_LifeTime,''',''',@Asset_DepType,''',
                                     ''',@Dep_Rate_ITC,''',''',@Dep_Rate_CA,''',
                                     ''',@Dep_Rate_MGMT,''',''',@Asset_DepRate,''',
                                     ''',@AssetCat_Remarks,''',',@Entity_Gid,',',ls_Createby,')');

								set @Insert_query = Query_Insert;
								#SELECT @Insert_query;
								PREPARE stmt FROM @Insert_query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;

                              if countRow > 0 then
									set Message = 'SUCCESS';
                                    commit;
							  else
									set Message = 'FAIL Asset_Cat';
                                    rollback;
                                    leave sp_FAAssetCategory;
                              End if;


ElseIf ls_Type = 'DEP_SETTINGS' and  ls_Sub_Type = 'MST' and ls_Action = 'INSERT' then


                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Dep_Setting_Type'))) into @Dep_Setting_Type;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Dep_Setting_gl'))) into @Dep_Setting_gl;
                select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Dep_Setting_Resrv_gl'))) into @Dep_Setting_Resrv_gl;



                if @Dep_Setting_Type is  null or @Dep_Setting_Type = '' then
						set Message = ' Depreciation setting Type Is Needed.';
						leave sp_FAAssetCategory;
				End if;

                if @Dep_Setting_gl is  null or @Dep_Setting_gl = '' then
						set Message = 'Depreciation Setting gl Is Needed.';
						leave sp_FAAssetCategory;
				End if;

                if @Dep_Setting_Resrv_gl is  null or @Dep_Setting_Resrv_gl = '' then
						set Message = 'Depreciation Setting Resrvgl Is Needed.';
						leave sp_FAAssetCategory;
				End if;


				select exists (select depsettings_depgl from fa_mst_tdepsettings
				where depsettings_isactive='Y' and
					  depsettings_isremoved='N') into @Test;

                select exists (select depsettings_depgl from fa_mst_tdepsettings
				where  depsettings_deptype=@Dep_Setting_Type and
					   depsettings_depgl=@Dep_Setting_gl and
					   depsettings_depreservegl=@Dep_Setting_Resrv_gl and
					   depsettings_isactive='Y' and
					   depsettings_isremoved='N') into @Dep_Test;

                if @Dep_Setting_Type='ITC' and @Dep_Test=1  then
						set Message = 'ITC Is already Exists';
						leave sp_FAAssetCategory;
				elseif @Dep_Setting_Type = 'CA' and @Dep_Test=1  then
						set Message = 'CA Is already Exists';
						leave sp_FAAssetCategory;
				elseif @Dep_Setting_Type = 'MGMT' and @Dep_Test=1  then
						set Message = 'MGMT Is already Exists';
						leave sp_FAAssetCategory;
				End if;


			if @Test=1 then
                set sql_safe_updates=0;
				set Query_Update = '';
				set Query_Update = concat('UPDATE fa_mst_tdepsettings
											  SET   depsettings_isactive=''N'' ,
                                                    depsettings_isremoved=''Y'',
                                                    update_date=now(),
                                                    update_by=',ls_Createby,'
											  WHERE depsettings_isactive=''Y'' and
                                                    depsettings_isremoved=''N''
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
									set Message = 'FAIL In Depsettings-Update';
                                    rollback;
                                    leave sp_FAAssetCategory;
                              End if;
			End if;


			set Query_Insert = '';
			set Query_Insert = concat('
							INSERT INTO fa_mst_tdepsettings
									(depsettings_deptype, depsettings_depgl,
									 depsettings_depreservegl, entity_gid,
									 create_by)
							  values(''',@Dep_Setting_Type,''',''',@Dep_Setting_gl,''',
                                     ''',@Dep_Setting_Resrv_gl,''',
                                     ',@Entity_Gid,',',ls_Createby,')');

								set @Insert_query = Query_Insert;
								#SELECT @Insert_query;
								PREPARE stmt FROM @Insert_query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;

                              if countRow > 0 then
									set Message = 'SUCCESS';
									select last_insert_id() into @last_insert_id;
							  else
									set Message = 'FAIL In Dep_setting';
                                    rollback;
                                    leave sp_FAAssetCategory;
                              End if;

			set Update_Column='';

			if @Dep_Setting_Type='ITC'  then
					set Update_Column=concat('
						   ,cat.assetcat_depgl_itc = setg.depsettings_depgl,
							cat.assetcat_depresgl_itc = setg.depsettings_depreservegl,
                            cat.assetcat_depgl_ca= '''',
							cat.assetcat_depresgl_ca= '''',
							cat.assetcat_depgl_mgmt='''',
							cat.assetcat_depresgl_mgmt='''' ');
            elseif @Dep_Setting_Type='CA'  then
					set Update_Column=concat('
						   ,cat.assetcat_depgl_itc = '''',
							cat.assetcat_depresgl_itc = '''',
                            cat.assetcat_depgl_ca= setg.depsettings_depgl,
							cat.assetcat_depresgl_ca= setg.depsettings_depreservegl,
							cat.assetcat_depgl_mgmt='''',
							cat.assetcat_depresgl_mgmt='''' ');
			elseif @Dep_Setting_Type='MGMT'  then
					set Update_Column=concat('
						   ,cat.assetcat_depgl_itc = '''',
							cat.assetcat_depresgl_itc = '''',
                            cat.assetcat_depgl_ca='''' ,
							cat.assetcat_depresgl_ca='''' ,
							cat.assetcat_depgl_mgmt=setg.depsettings_depgl,
							cat.assetcat_depresgl_mgmt=setg.depsettings_depreservegl ');
			end if;

             	set sql_safe_updates=0;
				set Query_Update = '';
				set Query_Update = concat('
								   UPDATE  fa_mst_tassetcat cat,
										   fa_mst_tdepsettings setg
								   SET     cat.update_by=',ls_Createby,',
										   cat.update_date=NOW()
										   ',Update_Column,'
								   WHERE  setg.depsettings_gid =',@last_insert_id,' and
										  cat.assetcat_isactive=''Y'' and
										  cat.assetcat_isremoved=''N''
										');
								set @Query_Update = Query_Update;
								#SELECT @Query_Update;
								PREPARE stmt FROM @Query_Update;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;

                              if countRow > 0 then
									set Message = 'SUCCESS';
									commit;
							  else
									set Message = 'FAIL';
                              End if;

ELSEIF ls_Action  = 'INSERT' and ls_Type = 'CWIP_GROUP' THEN


        select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.CWIP_Name')) into @CWIP_Name;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.CWIP_Gl')) into @CWIP_Gl;


        if @CWIP_Name is null or @CWIP_Name ='' then
				set Message='CWIP Name is Not Given';
                leave sp_FAAssetCategory;
        end if;

        if @CWIP_Gl is null or @CWIP_Gl ='' then
				set Message='CWIP Gl is Not Given';
                leave sp_FAAssetCategory;
        end if;

        if ls_Createby is null or ls_Createby ='' or ls_Createby =0 then
				set Message='Create_By is Not Given';
                leave sp_FAAssetCategory;
        end if;

        set @CWIP_Code='';
        select max(cwipgroup_code) into @CWIP_Code from fa_mst_tcwipgroup;


		if  @CWIP_Code='' or @CWIP_Code is null  then
			call sp_Generatecode_Get('WITHOUT_DATE', 'CWG', '00','000', @Message);
			select @Message into @CWIP_Code;
		else
			call sp_Generatecode_Get('WITHOUT_DATE', 'CWG', '00',@CWIP_Code, @Message);
			select @Message into @CWIP_Code;
		end if;


		set Query_Insert = '';
		set Query_Insert = concat('insert into fa_mst_tcwipgroup
														(cwipgroup_code, cwipgroup_name,
														 cwipgroup_gl,entity_gid,create_by)
												 values (''',@CWIP_Code,''',''',@CWIP_Name,''',
														 ''',@CWIP_Gl,''',',@Entity_Gid,',
																		   ',ls_Createby,') ');

                  				set @Insert_query = Query_Insert;
								#SELECT @Insert_query;
								PREPARE stmt FROM @Insert_query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
							    #select LAST_INSERT_ID() into @LAST_INSERT_Gid ;
								DEALLOCATE PREPARE stmt;

                                if countRow > 0 then
									set Message = 'SUCCESS';
                                    commit;
								else
									set Message = 'FAIL';
									leave sp_FAAssetCategory;
								End if;



      End if;

END