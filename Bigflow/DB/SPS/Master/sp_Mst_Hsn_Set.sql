CREATE DEFINER=`developer`@`%` PROCEDURE `galley`.`sp_Mst_Hsn_Set`(IN `ls_Action` varchar(32),IN `ls_Type` varchar(32),
IN `ls_Sub_Type` varchar(32),IN `lj_Details` json,IN `lj_Classification` json,
IN `ls_Createby` varchar(32),OUT `Message` varchar(1024))
sp_Mst_Hsn_Set:BEGIN
#### BALA 27-01-2020
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



 if ls_Action='INSERT' and ls_Type = 'HSN' and ls_Sub_Type = 'DETAILS'   then

					select JSON_LENGTH(lj_Details,'$') into @li_Detailjson_count;
						if @li_Detailjson_count is null or @li_Detailjson_count = 0 then
							set Message = 'No Data In Json';
                            leave sp_Mst_Hsn_Set;
						end if;


                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.HSN_Code'))) into @HSN_Code;
					select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.HSN_Desc'))) into @HSN_Desc;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.CGST_Gid'))) into @CGST_Gid;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.SGST_Gid'))) into @SGST_Gid;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.IGST_Gid'))) into @IGST_Gid;
					select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid[0]'))) into @Entity_Gid;

						if @Entity_Gid is  null or @Entity_Gid = 0 or @Entity_Gid = '' then
							set Message = 'Entity Gid Is Needed.';
							leave sp_Mst_Hsn_Set;
						End if;

						if @HSN_Code is null or @HSN_Code = '' then
							set Message = 'HSN Code Is Not Given';
                            leave sp_Mst_Hsn_Set;
						end if;

                        if @CGST_Gid is null or @CGST_Gid = '' then
							set Message = 'CGST Gid Is Not Given';
                            leave sp_Mst_Hsn_Set;
						end if;

                        if @SGST_Gid is null or @SGST_Gid = '' then
							set Message = 'SGST Gid Is Not Given';
                            leave sp_Mst_Hsn_Set;
						end if;

                        if @IGST_Gid is null or @IGST_Gid = '' then
							set Message = 'IGST Gid Is Not Given';
                            leave sp_Mst_Hsn_Set;
						end if;

                        if @HSN_Desc is null or @HSN_Desc = '' then
							set Message = 'HSN Desc Is Not Given';
                            leave sp_Mst_Hsn_Set;
						end if;


					select taxrate_rate  from gal_mst_ttaxrate where taxrate_gid=@CGST_Gid
								and taxrate_isactive='Y' and taxrate_isremoved='N' into @HSN_CGST_Rate;
					select taxrate_rate from gal_mst_ttaxrate where taxrate_gid=@SGST_Gid
								and taxrate_isactive='Y' and taxrate_isremoved='N' into @HSN_SGST_Rate;
					select taxrate_rate from gal_mst_ttaxrate where taxrate_gid=@IGST_Gid
								and taxrate_isactive='Y' and taxrate_isremoved='N' into @HSN_IGST_Rate;



				set Query_Insert = '';
				set Query_Insert = concat('INSERT INTO gal_mst_thsn
													   (hsn_code,hsn_description,hsn_cgstrate,hsn_sgstrate,
														hsn_igstrate,hsn_cgsttaxrategid,hsn_sgsttaxrategid,
														hsn_igsttaxrategid,entity_gid,create_by)
												VALUES (''',@HSN_Code,''',''',@HSN_Desc,''',''',@HSN_CGST_Rate,''',
														''',@HSN_SGST_Rate,''', ''',@HSN_IGST_Rate,''', ',@CGST_Gid,',
														',@SGST_Gid,', ''',@IGST_Gid,''',''',@Entity_Gid,''',
														''',ls_Createby,''')');

                                set @Insert_query = Query_Insert;
								#SELECT @Insert_query;
                                PREPARE stmt FROM @Insert_query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;

                                if countRow > 0 then
									set Message = 'SUCCESS';
                                 Else
                                     set Message = 'FAIL';
                                End if;


 end if;


END