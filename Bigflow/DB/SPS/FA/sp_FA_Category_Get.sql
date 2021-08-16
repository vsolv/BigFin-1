CREATE  PROCEDURE `sp_FA_Category_Get`(IN `ls_Type` varchar(64),IN `ls_Sub_Type` varchar(64),
IN `lj_Filters` json,IN `lj_Classification` json, OUT `Message` varchar(1024))
sp_FA_Category_Get:BEGIN
### BALA Nov 05 2019 - Created
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

			select JSON_LENGTH(lj_classification, '$.Entity_Gid[0]') into @Entity_Gid;
				if @Entity_Gid=0 or @Entity_Gid='' or @Entity_Gid is null then
					set Message = 'Entity Gid Is Not Given';
					leave sp_FA_Category_Get;
				end if;

if ls_Type = 'CATEGORY' and ls_Sub_Type = 'SUB_CATEGORY' then

			set Query_Select = '';
            set Query_Search = '';


                set Query_Select = concat('
							SELECT a.category_gid, a.category_code, a.category_no,
								   a.category_glno, a.category_isasset,a.category_name,
								   b.subcategory_gid,b.subcategory_code,
								   b.subcategory_no,b.subcategory_categorygid,
								   b.subcategory_glno,b.subcategory_name
								FROM ap_mst_tcategory a
								inner join ap_mst_tsubcategory b
								on a.category_gid=b.subcategory_categorygid
							where a.category_isasset=''Y'' and a.category_isactive=''Y''
								and a.category_isremoved=''N'' and a.entity_gid in (',@Entity_Gid,')
								and b.subcategory_isactive=''Y'' and b.subcategory_isremoved=''N''
								and a.entity_gid in (',@Entity_Gid,')
							');
                     	set @Query_Select = Query_Select;
			      		#select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;

elseif ls_Type = 'ASSETCAT' and ls_Sub_Type = 'SUMMARY' THEN
          set Query_Select = '';
            set Query_Search = '';


                set Query_Select = concat('
							Select a.assetcat_gid,a.assetcat_subcatname,b.subcategory_name,c.category_name,
							a.assetcat_deprate_ca,a.assetcat_deprate_itc,a.assetcat_deprate_mgmt,
							a.assetcat_depgl_ca,a.assetcat_depgl_itc,a.assetcat_depgl_mgmt,
							a.assetcat_depresgl_ca,a.assetcat_depresgl_itc,a.assetcat_depresgl_mgmt,
                            a.assetcat_lifetime,a.assetcat_barcoderequired,a.assetcat_deptype,a.assetcat_remarks
							from fa_mst_tassetcat as a
							inner join ap_mst_tsubcategory as b on b.subcategory_gid = a.assetcat_subcategorygid
							inner join ap_mst_tcategory as c on c.category_gid = b.subcategory_categorygid
							where a.assetcat_isactive = ''Y''
							and a.assetcat_isremoved = ''N''
							and b.subcategory_isactive = ''Y'' and b.subcategory_isremoved = ''N''
							and c.category_isactive = ''Y''
							and c.category_isremoved = ''N''
							and a.entity_gid in (',@Entity_Gid,')
							');
                     	set @Query_Select = Query_Select;
			      		#select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;




 End if;

END