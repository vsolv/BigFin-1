CREATE DEFINER=`developer`@`%` PROCEDURE `sp_FALocation_Set`(IN `ls_Action` varchar(32),IN `ls_Type` varchar(32),
IN `ls_Sub_Type` varchar(32),IN `lj_Details` json,IN `lj_Classification` json,
IN `ls_Createby` varchar(32),OUT `Message` varchar(1024))
sp_FALocation_Set:BEGIN
#### Bala Oct 15 2019
declare Query_Insert varchar(9000);
declare Query_Update varchar(9000);
Declare errno int;
Declare msg varchar(1000);
declare countRow int;
Declare i int;



	DECLARE EXIT HANDLER FOR SQLEXCEPTION,sqlwarning
    BEGIN

     GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
     set Message = concat(errno , msg);
     ROLLBACK;
     END;


 if ls_Action='INSERT' and ls_Type = 'FA_LOCATION' and ls_Sub_Type = 'FA_LOCATION'   then

					select JSON_LENGTH(lj_Details,'$') into @li_Detailjson_count;
						if @li_Detailjson_count is null or @li_Detailjson_count = 0 then
							set Message = 'No Data In Json - FA Location.';
                            leave sp_FALocation_Set;
						end if;


                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Ref_Gid'))) into @Ref_Gid;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.RefTable_Gid'))) into @RefTable_Gid;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Location_Name'))) into @Location_Name;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Location_Floor'))) into @Location_Floor;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Remarks'))) into @Remarks;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid'))) into @Entity_Gid;


					set @Duplicate_Location='';
						SELECT EXISTS(select assetlocation_refgid   from fa_mst_tassetloaction
											where assetlocation_refgid=@Ref_Gid
												  and assetlocation_reftablegid=@RefTable_Gid
                                                  and assetlocation_name=@Location_Name
                                                  and  assetlocation_floor=@Location_Floor
                                                  and assetlocation_remarks=@Remarks) into @Duplicate_Location;

							if @Duplicate_Location=1 then
									set Message = 'This "Location" Is Already Exist';
									leave sp_FALocation_Set;
							End if;


									if @Entity_Gid is null or @Entity_Gid = 0 or @Entity_Gid = '' then
										set Message = 'Entity Gid Is Needed.';
										leave sp_FALocation_Set;
									End if;

						if @Ref_Gid is null or @Ref_Gid = '' then
							set Message = 'Ref_Gid Is Needed.';
							leave sp_FALocation_Set;
						End if;

						if @RefTable_Gid is null or @RefTable_Gid = '' then
							set Message = 'RefTable_Gid Is Needed.';
							leave sp_FALocation_Set;
						End if;

						if @Location_Name is null or @Location_Name = '' then
							set Message = 'Location_Name Is Needed.';
							leave sp_FALocation_Set;
						End if;

						if @Location_Floor is null or @Location_Floor = '' then
							set Message = 'Location_Floor Is Needed.';
							leave sp_FALocation_Set;
						End if;

                        if @Remarks is null or @Remarks = '' then
							set Message = 'Remarks Is Needed.';
							leave sp_FALocation_Set;
						End if;


               set Query_Insert = '';
			   set Query_Insert = concat('INSERT INTO fa_mst_tassetloaction
												 (assetlocation_refgid,assetlocation_reftablegid,
                                                  assetlocation_name,assetlocation_floor,
                                                  assetlocation_remarks,entity_gid,create_by )
										   VALUES (''',@Ref_Gid,''', ''',@RefTable_Gid,''',
												  ''',@Location_Name,''', ''',@Location_Floor,''',
											      ''',@Remarks,''',''',@Entity_Gid,''',''',ls_Createby,''')');

                                set @Insert_query = Query_Insert;
								#SELECT @Insert_query;
								PREPARE stmt FROM @Insert_query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;

                                if countRow > 0 then
                                  select LAST_INSERT_ID() into @Loaction_Maxgid ;
									set Message = 'SUCCESS';
                               else
                                    set Message = 'FAIL';
                              End if;
    End if;


END