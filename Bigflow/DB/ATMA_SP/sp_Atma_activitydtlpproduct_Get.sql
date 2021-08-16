CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_activitydtlpproduct_Get`(in Action  varchar(20),
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_Atma_activitydtlpproduct_Get:BEGIN

Declare Query_Table varchar(1000);
Declare Query_Table1 varchar(1000);
Declare Query_Table2 varchar(1000);
Declare Query_Select varchar(5000);
Declare Query_Search varchar(5000);
Declare Query_Update varchar(5000);
Declare countRow varchar(5000);
Declare ls_count int;

IF Action='activitydtlpp_GET' then


        select JSON_LENGTH(lj_filter,'$') into @li_json_count;
		select JSON_LENGTH(lj_classification,'$') into @li_json_lj_classification_count;

        if @li_json_count = 0 or @li_json_count = ''
           or @li_json_count is null  then
			set Message = 'No Data In filter Json. ';
			leave sp_Atma_activitydtlpproduct_Get;
		End if;

        if @li_json_lj_classification_count = 0 or @li_json_lj_classification_count = ''
           or @li_json_lj_classification_count is null  then
			set Message = 'No Data In classification Json. ';
			leave sp_Atma_activitydtlpproduct_Get;
		End if;



		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.activitydtlpproduct_activitydetailsgid'))) into @activitydtlpproduct_activitydetailsgid;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.activitydtlpproduct_Category'))) into @activitydtlpproduct_Category;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.activitydtlpproduct_SubCategory'))) into @activitydtlpproduct_SubCategory;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.activitydtlpproduct_Name'))) into @Catlog_Name;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.activitydtlpproduct_Spec'))) into @activitydtlpproduct_Spec;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.activitydtlpproduct_Size'))) into @activitydtlpproduct_Size;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.activitydtlpproduct_Remarks'))) into @activitydtlpproduct_Remarks;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.activitydtlpproduct_UomGid'))) into @activitydtlpproduct_UomGid;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.activitydtlpproduct_Rate'))) into @activitydtlpproduct_Rate;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.activitydtlpproduct_ValidFrom'))) into @activitydtlpproduct_ValidFrom;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.activitydtlpproduct_ValidTo'))) into @activitydtlpproduct_ValidTo;
			select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Mst_Table')))into @Mst_Table;

			select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Activitydtlpproduct_Partner_Gid')))
            into @Activitydtlpproduct_Partner_Gid;
            select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.mPartnerProduct_Status')))
            into @mPartnerProduct_Status;

            select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Entity_Gid')))
            into @Entity_Gid;

            set Query_Table='';
			if @Mst_Table='Mst' then
				set Query_Table = concat('atma_map_tactivitydtlpproduct');
			else
				set Query_Table = concat('atma_tmp_map_tactivitydtlpproduct');
			End if;

			set Query_Table1='';
			if @Mst_Table='Mst' then
				set Query_Table1 = concat('atma_mst_tactivitydetails');

			else
				set Query_Table1 = concat('atma_tmp_mst_tactivitydetails');
			End if;

            set Query_Table2='';
			if @Mst_Table='Mst' then
				set Query_Table2 = concat('atma_map_tpartnerproduct');
			else
				set Query_Table2 = concat('atma_tmp_map_tpartnerproduct');
			End if;



        set Query_Search = '';
        #if @Activitydtlpproduct_Partner_Gid is not null or @Activitydtlpproduct_Partner_Gid <> '' then
			#set Query_Search = concat(Query_Search,' and pr.partner_gid = ',@Activitydtlpproduct_Partner_Gid,' ');
		#End if;

        #if @activitydtlpproduct_activitydetailsgid is not null or @activitydtlpproduct_activitydetailsgid <> '' then
			#set Query_Search = concat(Query_Search,' and activitydtlpproduct_activitydetailsgid = ',@activitydtlpproduct_activitydetailsgid,' ');
		#End if;
        if @mPartnerProduct_Status is not null or @mPartnerProduct_Status <> '' then
			set Query_Search = concat(Query_Search,' and pp.mpartnerproduct_status = ''',@mPartnerProduct_Status,''' ');
		End if;

        if @activitydtlpproduct_Category is not null or @activitydtlpproduct_Category <> '' then
			set Query_Search = concat(Query_Search,' and activitydtlpproduct_category = ''',@activitydtlpproduct_Category,''' ');
		End if;

        if @activitydtlpproduct_SubCategory is not null or @activitydtlpproduct_SubCategory <> '' then
			set Query_Search = concat(Query_Search,' and activitydtlpproduct_subcategory = ''',@activitydtlpproduct_SubCategory,''' ');
		End if;

        if @Catlog_Name is not null or @Catlog_Name <> '' then
			set Query_Search = concat(Query_Search,' and activitydtlpproduct_name = ''',@Catlog_Name,''' ');
		End if;

        if @activitydtlpproduct_Spec is not null or @activitydtlpproduct_Spec <> '' then
			set Query_Search = concat(Query_Search,' and activitydtlpproduct_spec = ''',@activitydtlpproduct_Spec,''' ');
		End if;

        if @activitydtlpproduct_Size is not null or @activitydtlpproduct_Size <> '' then
			set Query_Search = concat(Query_Search,' and activitydtlpproduct_size = ''',@activitydtlpproduct_Size,''' ');
		End if;

        if @activitydtlpproduct_Remarks is not null or @activitydtlpproduct_Remarks <> '' then
			set Query_Search = concat(Query_Search,' and activitydtlpproduct_remarks = ''',@activitydtlpproduct_Remarks,''' ');
		End if;

        if @activitydtlpproduct_Rate is not null or @activitydtlpproduct_Rate <> '' then
			set Query_Search = concat(Query_Search,' and activitydtlpproduct_rate = ''',@activitydtlpproduct_Rate,''' ');
		End if;

        if @activitydtlpproduct_ValidFrom is not null or @activitydtlpproduct_ValidFrom <> '' then
			set Query_Search = concat(Query_Search,' and activitydtlpproduct_validfrom = ''',@activitydtlpproduct_ValidFrom,''' ');
		End if;

        if @activitydtlpproduct_ValidTo is not null or @activitydtlpproduct_ValidTo <> '' then
			set Query_Search = concat(Query_Search,' and activitydtlpproduct_validto = ''',@activitydtlpproduct_ValidTo,''' ');
		End if;

       # select mpartnerproduct_gid from atma_tmp_map_tpartnerproduct where mpartnerproduct_partner_gid=@mpartnerproduct_partner_gid
       # into @partnerproductgid;

		#select activitydtlpproduct_gid from atma_tmp_map_tactivitydtlpproduct where activitydtlpproduct_mpartnerproductgid=@partnerproductgid
        #into @activitydtlpproduct;
       # select @activitydtlpproduct;

	set Query_Select = '';
	set Query_Select =concat('select adtlp.activitydtlpproduct_gid,adtlp.activitydtlpproduct_activitydetailsgid,
							  adtlp.activitydtlpproduct_category,adtlp.activitydtlpproduct_mpartnerproductgid,
                              adtlp.activitydtlpproduct_subcategory,adtlp.activitydtlpproduct_name,adtlp.activitydtlpproduct_spec,
                              adtlp.activitydtlpproduct_size,adtlp.activitydtlpproduct_remarks,adtlp.activitydtlpproduct_uomgid,
                              adtlp.activitydtlpproduct_rate,adtlp.activitydtlpproduct_validfrom,adtlp.activitydtlpproduct_validto
                              ,cat.category_name,sub.subcategory_name,uom.uom_name,ad.activitydetails_name,p.product_name,
                              pp.mpartnerproduct_unitprice,pp.mpartnerproduct_packingprice,pp.mpartnerproduct_deliverydays,
								pp.mpartnerproduct_capacitypw,pp.mpartnerproduct_dts,pp.mpartnerproduct_status
							  from ',Query_Table,' adtlp
                              inner join ap_mst_tcategory cat on adtlp.activitydtlpproduct_category= cat.category_gid
                              inner join ap_mst_tsubcategory sub on adtlp.activitydtlpproduct_subcategory=sub.subcategory_gid
                              inner join gal_mst_tuom uom on adtlp.activitydtlpproduct_uomgid=uom.uom_gid
                              inner join ',Query_Table1,' ad on adtlp.activitydtlpproduct_activitydetailsgid =ad.activitydetails_gid
							  inner join ',Query_Table2,' pp  on pp.mpartnerproduct_gid=adtlp.activitydtlpproduct_mpartnerproductgid
                              inner join gal_mst_tproduct p on pp.mpartnerproduct_product_gid= p.product_gid
                              where adtlp.activitydtlpproduct_isactive=''Y''
                              and adtlp.activitydtlpproduct_isremoved =''N'' and cat.category_isactive =''Y'' and cat.category_isremoved=''N'' and sub.subcategory_isactive=''Y''
                              and sub.subcategory_isremoved =''N'' and uom.uom_isactive=''Y'' and uom.uom_isremoved=''N'' and  ad.activitydetails_isactive=''Y''and
                              ad.activitydetails_isremoved =''N'' and p.product_isactive=''Y'' and p.product_isremoved=''N'' and
                              pp.mpartnerproduct_isactive=''Y'' and pp.mpartnerproduct_isremoved=''N'' and adtlp.entity_gid=',@Entity_Gid,' and
                              cat.entity_gid=',@Entity_Gid,' and sub.entity_gid=',@Entity_Gid,' and uom.entity_gid=',@Entity_Gid,' and ad.entity_gid=',@Entity_Gid,'
							  and p.entity_gid=',@Entity_Gid,'  and pp.entity_gid=',@Entity_Gid,'
                              and adtlp.activitydtlpproduct_activitydetailsgid=',@activitydtlpproduct_activitydetailsgid,'

                              ',Query_Search,'
                              ');


	 set @p = Query_Select;
	#select Query_Select;  ## Remove It
     PREPARE stmt FROM @p;
	 EXECUTE stmt;
	 DEALLOCATE PREPARE stmt;

     Select found_rows() into ls_count;
	 if ls_count > 0 then
		 set Message = 'FOUND';
	else
		 set Message = 'NOT_FOUND';
	end if;



END IF;

END