CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_PartnerProduct_Checker_Get`(in ls_Action  varchar(16),
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_Atma_PartnerProduct_Checker_Get:BEGIN

#Balamaniraja      13-08-19

Declare Query_Select varchar(5000);
Declare Query_Search varchar(5000);
Declare ls_count int;

IF ls_Action='Checker_Get' then

		select JSON_LENGTH(lj_classification,'$') into @lj_classification_json_count;
		select JSON_LENGTH(lj_filter,'$') into @json_count;

			if @lj_classification_json_count is null or  @lj_classification_json_count = 0
            or @lj_classification_json_count =''  then
				set Message = 'No Data In Json. ';
				leave sp_Atma_PartnerProduct_Checker_Get;
			End if;

		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partner_Gid')))
		into @Partner_Gid;
        select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Entity_Gid')))
		into @Entity_Gid;

			if @Entity_Gid = 0 or @Entity_Gid = '' or @Entity_Gid is null  then
				set Message = 'Entity_Gid Is Not Given In classification Json. ';
				leave sp_Atma_PartnerProduct_Checker_Get;
			end if;

        set @Main_Partner_Gid ='';
		select main_partner_gid  from atma_tmp_tpartner where partner_gid= @Partner_Gid
        into @Main_Partner_Gid;


		set Query_Search='';
		if @Main_Partner_Gid is not null or @Main_Partner_Gid <> '' then
			set Query_Search = concat(Query_Search,' and pa.partner_gid = ',@Main_Partner_Gid,' ');
		End if;



		set Query_Select = '';

		set Query_Select =concat('select mp.mpartnerproduct_gid,pa.partner_gid,
        mp.mpartnerproduct_partner_gid,
		pr.product_gid,mp.mpartnerproduct_product_gid,
        pr.product_name,pa.partner_name,

        mp.mpartnerproduct_unitprice,mp.mpartnerproduct_packingprice,
        mp.mpartnerproduct_validfrom,mp.mpartnerproduct_validto,
        mp.mpartnerproduct_deliverydays,mp.mpartnerproduct_capacitypw,
        mp.mpartnerproduct_dts,mp.mpartnerproduct_status,
        em.employee_name
        from  atma_tmp_map_tpartnerproduct mp
        left join atma_mst_tpartner pa on pa.partner_gid=mp.mpartnerproduct_partner_gid
        inner join gal_mst_tproduct pr on pr.product_gid=mp.mpartnerproduct_product_gid
        inner join gal_mst_temployee em on em.employee_gid=mp.mpartnerproduct_product_gid
        where mp.mpartnerproduct_isactive=''Y'' and mp.mpartnerproduct_isremoved=''N''
        and mp.entity_gid=',@Entity_Gid ,' and pa.partner_isactive=''Y''
        and pa.partner_isremoved=''N'' and pa.entity_gid=',@Entity_Gid ,' and
        pr.product_isactive=''Y'' and pr.product_isremoved=''N''
        and pr.entity_gid=',@Entity_Gid ,' and em.employee_isactive=''Y''
        and em.employee_isremoved=''N''and em.entity_gid=',@Entity_Gid ,'
        and mp.mpartnerproduct_status=''Pending'' ',Query_Search,'
                                    ');

     set @p = Query_Select;
    # select Query_Select;  ## Remove It
     PREPARE stmt FROM @p;
	 EXECUTE stmt;
	 DEALLOCATE PREPARE stmt;
     Select found_rows() into ls_count;

	if ls_count > 0 then
		 set Message = 'FOUND';
	else
		 set Message = 'NOT_FOUND';
	end if;
End if;

END