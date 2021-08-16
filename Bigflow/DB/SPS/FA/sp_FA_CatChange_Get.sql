CREATE DEFINER=`developer`@`%` PROCEDURE `sp_FA_CatChange_Get`(
IN `ls_Type` varchar(32),IN `ls_Sub_Type` varchar(32),IN `lj_Details` json,IN `lj_Classification` json,
IN `ls_Createby` varchar(32),OUT `Message` varchar(1024))
sp_FA_CatChange_Get:BEGIN
### Bala Oct 31 2019 - Created
Declare Query_Select varchar(6144);
Declare Query_Search varchar(1024);
declare errno int;
declare msg varchar(1000);
declare li_count int;

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




if ls_Type = 'CAT_CHANGE' and ls_Sub_Type = 'SUMMARY' then

				select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid[0]'))) into @Entity_Gid;

             if @Entity_Gid is  null or @Entity_Gid = 0 or @Entity_Gid = '' then
					set Message = 'Entity Gid Is Needed.';
                    leave sp_FA_CatChange_Get;
             End if;



                set Query_Select ='';

                set Query_Select = concat('select assetcatchange_gid, assetcatchange_assetdetailsid,
												  assetcatchange_date,assetcatchange_status,
                                                  assetcatchange_reason,assetcatchange_cat,
												  assetcatchange_oldcat
											from fa_trn_tassetcatchange where assetcatchange_isactive=''Y''
												 and assetcatchange_isremoved=''N'' and entity_gid=',@Entity_Gid,'
										');

	set @p = Query_Select;
    #select @p;
	PREPARE stmt FROM @p;
	EXECUTE stmt;
	Select found_rows() into li_count;
	DEALLOCATE PREPARE stmt;

    	if li_count > 0 then
					set Message = 'FOUND';
				else
					set Message = 'NOT_FOUND';
				end if;
End if;
END