CREATE DEFINER=`developer`@`%` PROCEDURE `galley`.`sp_FADepreciation_Get`(
IN `ls_Type` varchar(32),IN `ls_Sub_Type` varchar(32),IN `lj_Details` json,IN `lj_Classification` json,
OUT `Message` varchar(1024))
sp_FADepreciation_Get:BEGIN
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


if ls_Type = 'DEPRECIATION' and ls_Sub_Type = 'SUMMARY' then

				select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid[0]'))) into @Entity_Gid;

					if @Entity_Gid is  null or @Entity_Gid = 0 or @Entity_Gid = '' then
						set Message = 'Entity Gid Is Needed.';
						leave sp_FADepreciation_Get;
					End if;
				# TO DO Apply Limit
                set Query_Select ='';
                set Query_Select = concat('select a.depreciation_gid, b.assetdetails_id,
												  date_format(a.depreciation_fromdate,''%d-%b-%Y'') as depreciation_fromdate , date_format(a.depreciation_todate,''%d-%b-%Y'') as depreciation_todate, a.depreciation_month,
												  a.depreciation_year, a.depreciation_itcvalue, a.depreciation_cavalue,
												  a.depreciation_mgmtvalue, a.depreciation_gl, a.depreciation_resgl,
												  a.depreciation_value, a.depreciation_type from fa_trn_tdepreciation as a
											inner join fa_trn_tassetdetails as b on b.assetdetails_gid = a.depreciation_assetdetailsgid
										    where a.depreciation_isactive=''Y''
												and a.depreciation_isremoved=''N''
												and a.entity_gid in (',@Entity_Gid,') limit 100 ');

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
End if;
if ls_Type = 'FORCAST' and ls_Sub_Type = 'SUMMARY' then
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.From_Date'))) into @From_Date;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.To_Date'))) into @To_Date;
				select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid[0]'))) into @Entity_Gid;

					if @Entity_Gid is  null or @Entity_Gid = 0 or @Entity_Gid = '' then
						set Message = 'Entity Gid Is Needed.';
						leave sp_FADepreciation_Get;
					End if;
                    if @From_Date is  null or @From_Date = 0 or @From_Date = '' then
						set Message = 'From Date Is Needed.';
						leave sp_FADepreciation_Get;
					End if;
                    if @To_Date is  null or @To_Date = 0 or @To_Date = '' then
						set Message = 'To_Date Is Needed.';
						leave sp_FADepreciation_Get;
					End if;
				# TO DO
                set Query_Select ='';
                set Query_Select = concat('SELECT c.assetdetails_capdate,COUNT(d.writeoff_gid) as writeoff,
							COUNT(e.impairasset_gid) as Impair,
							COUNT(f.assettfr_gid) as Transfer,COUNT(g.assetsale_gid) as Sale,
                            sum(b.depreciation_value) depreciation_value,
							h.fiscalyear_code as fin_year FROM fa_trn_tassetdetails as c
							left join fa_trn_tdepreciation as b on c.assetdetails_id = b.depreciation_assetdetailsgid
							left join fa_trn_twriteoff as d on   c.assetdetails_id = d.writeoff_assetdetailsid
							left join fa_trn_timpairasset as e on   c.assetdetails_id = e.impairasset_assetdetailsid
							left join fa_trn_tassettfr as f on   c.assetdetails_id = f.assettfr_assetdetailsid
							left join fa_trn_tassetsale as g on   c.assetdetails_id = g.assetsale_assetdetailsid
							left join fa_trn_tfiscalyear as h on
                            DATE_FORMAT(c.assetdetails_capdate,"%Y") = h.fiscalyear_code
							where c.assetdetails_capdate between (''',@From_Date,''') and (''',@To_Date,''')
							and h.fiscalyear_status = "O"
							and c.assetdetails_isactive="Y"
							and c.assetdetails_isremoved="N"
							and c.entity_gid in (',@Entity_Gid,')
							GROUP
							BY MONTH(c.assetdetails_capdate)  order by c.assetdetails_capdate asc; ');

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
End if;
END