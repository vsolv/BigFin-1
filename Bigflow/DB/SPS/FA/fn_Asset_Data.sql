CREATE  FUNCTION `galley`.`fn_Asset_Data`(ls_Type varchar(64),Asset_Gid int,Entity_Gid int,lj_data json) RETURNS varchar(1024) CHARSET utf8
BEGIN
### Ramesh Oct 2019

Declare Out_Message varchar(1024);
Declare i varchar(1024);
Declare ls_count varchar(1024);

	if ls_Type = 'ASSET_TRAN' then

                        if Asset_Gid <> 0 then
							Select concat('[',json_object( 'product_dname',b.product_displayname,'product_name',b.product_name,
							'branch_name',c.branch_name,'location_name',d.assetlocation_name,'location_floor',d.assetlocation_floor,
                            'asset_cat_name',e.assetcat_subcatname
							), ']' )
							into @lj_default_details
							 from fa_trn_tassetdetails as a
							inner join gal_mst_tproduct as b on b.product_gid = a.assetdetails_productgid
							inner join gal_mst_tbranch as c on c.branch_gid = a.assetdetails_branchgid
							inner join fa_mst_tassetloaction as d on d.assetlocation_gid = a.assetdetails_assetlocationgid
							inner join fa_mst_tassetcat as e on e.assetcat_gid = a.assetdetails_assetcatgid
							where a.assetdetails_isactive = 'Y' and a.assetdetails_isremoved = 'N'
							and b.product_isactive = 'Y' and b.product_isremoved = 'N'
							and c.branch_isactive = 'Y' and c.branch_isremoved = 'N'
							and d.assetlocation_isactive = 'Y' and d.assetlocation_isremoved = 'N'
							and e.assetcat_isactive = 'Y' and e.assetcat_isremoved = 'N'
							and a.assetdetails_gid = Asset_Gid
							and a.entity_gid = Entity_Gid
							;

                        set   Out_Message = @lj_default_details;

                        else
                               set Out_Message = 0;
                       End if;

    elseif ls_Type = 'ASSET_TMP' then
					if Asset_Gid <> 0 then
							Select concat('[',json_object( 'product_name',b.product_displayname,'product_name',b.product_name,
							'branch_name',c.branch_name,'location_name',d.assetlocation_name,'location_floor',d.assetlocation_floor,'asset_cat_name',e.assetcat_subcatname), ']' )
							into @lj_default_details
							 from fa_tmp_tassetdetails as a
							inner join gal_mst_tproduct as b on b.product_gid = a.assetdetails_productgid
							inner join gal_mst_tbranch as c on c.branch_gid = a.assetdetails_branchgid
							inner join fa_mst_tassetloaction as d on d.assetlocation_gid = a.assetdetails_assetlocationgid
							inner join fa_mst_tassetcat as e on e.assetcat_gid = a.assetdetails_assetcatgid
							where a.assetdetails_isactive = 'Y' and a.assetdetails_isremoved = 'N'
							and b.product_isactive = 'Y' and b.product_isremoved = 'N'
							and c.branch_isactive = 'Y' and c.branch_isremoved = 'N'
							and d.assetlocation_isactive = 'Y' and d.assetlocation_isremoved = 'N'
							and e.assetcat_isactive = 'Y' and e.assetcat_isremoved = 'N'
							and a.assetdetails_gid = Asset_Gid
							and a.entity_gid = Entity_Gid
							;

                        set   Out_Message = @lj_default_details;

                        else
                               set Out_Message = 0;
                       End if;
    ELSEIF ls_Type = 'ASSET_REQUEST_CHECK' then

          set Out_Message = '{}';
          select JSON_UNQUOTE(JSON_EXTRACT(lj_Details,CONCAT('$.Asset_Details_Gids'))) into @Asset_Details_Gidsfn;

         if @Asset_Details_Gidsfn is null or @Asset_Details_Gidsfn = 0 THEN
         	set Out_Message = 'ERROR';
         End if;

        Select ifnull(COUNT(assetdetails_gid),0) into @asset_count_inprocess from fa_trn_tassetdetails
        where assetdetails_gid in (@Asset_Details_Gidsfn)
        and assetdetails_isactive = 'Y' and assetdetails_isremoved = 'N'
        and entity_gid = Entity_Gid and assetdetails_requestfor = ''  ;

       set Out_Message = @asset_count_inprocess;

    ELSEIF ls_Type = 'ASSET_PARENT_CHECK' then

			if Asset_Gid <> 0 then

					SELECT EXISTS (select assetdetails_parentgid from fa_trn_tassetdetails
						where assetdetails_parentgid<>0
						and assetdetails_gid=Asset_Gid and assetdetails_isactive='Y'
                        and assetdetails_isremoved='N' and entity_gid=Entity_Gid) INTO @Test;

							if @Test=1 then
								  set Out_Message = 'SUCCESS';
                            else
								  set Out_Message = 'FAIL';
                            end if;
			end if;

	ELSEIF ls_Type = 'ASSET_CLUB_DATA' then

			if Asset_Gid <> 0 then

						select group_concat(assetdetails_gid) into @AssetDetails_Gids
							from fa_trn_tassetdetails
								where assetdetails_parentgid=Asset_Gid
									  and assetdetails_isactive='Y'  and assetdetails_isremoved='N'
									  and entity_gid=Entity_Gid;


							if @AssetDetails_Gids is not null and @AssetDetails_Gids<>'' then
								 set Out_Message = @AssetDetails_Gids;
							else
								 set Out_Message = 'FAIL';
                            end if;
			end if;

   else
         set Out_Message = '{}';
End if;


RETURN Out_Message;
END