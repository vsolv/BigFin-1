CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_PartnerBranch_Get`(in li_Action  varchar(20),
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_Atma_PartnerBranch_Get:BEGIN



Declare Query_Select varchar(5000);
Declare Query_Table varchar(60);
Declare Query_Table1 varchar(60);
Declare Query_Table2 varchar(60);
Declare Query_Column varchar(60);
Declare Query_Column1 varchar(60);
Declare countRow varchar(5000);
Declare ls_count int;


IF li_Action='Atma_Branch_Get' then

		select JSON_LENGTH(lj_classification,'$') into @lj_classification_json_count;
		select JSON_LENGTH(lj_filter,'$') into @json_count;

                    if @json_count is null or  @json_count = 0
						or @lj_classification_json_count =''  then
							set Message = 'No Data In Filter Json. ';
							leave sp_Atma_PartnerBranch_Get;
					End if;

					if @lj_classification_json_count is null or  @lj_classification_json_count = 0
						or @lj_classification_json_count =''  then
							set Message = 'No Data In Classification Json. ';
							leave sp_Atma_PartnerBranch_Get;
					End if;

                select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.main_PartnerBranch_Gid')))into @main_PartnerBranch_Gid;
                select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Mst_Table')))into @Mst_Table;
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Branch_PartnerGid')))
				into @Branch_PartnerGid;
                select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Entity_Gid')))
				into @Entity_Gid;

					set Query_Table='';
				if @Mst_Table='Mst' then
					set Query_Table = concat('atma_mst_tpartnerbranch');
				else
					set Query_Table = concat('atma_tmp_mst_tpartnerbranch');
				End if;

					set Query_Table1='';
				if @Mst_Table='Mst' then
					set Query_Table1 = concat('gal_mst_tcontact');
				else
					set Query_Table1 = concat('atma_tmp_mst_tcontact');
				End if;

					set Query_Table2='';
				if @Mst_Table='Mst' then
					set Query_Table2 = concat('gal_mst_taddress');
				else
					set Query_Table2 = concat('atma_tmp_mst_taddress');
				End if;

                 set Query_Column='';
				if @Mst_Table is null or @Mst_Table=''   then
					set Query_Column = concat(',pb.main_partnerbranch_gid');
				End if;

                set Query_Column1='';
				if @Mst_Table='Mst'  then
					set Query_Column1 = concat('partnerbranch_gid=',@main_PartnerBranch_Gid,'');
				End if;

					if @Entity_Gid = ''   or @Entity_Gid is null  then
						set Message = 'Entity_Gid Is Not Given In classification Json. ';
						leave sp_Atma_PartnerBranch_Get;
					End if;

                   if @Mst_Table is null or @Mst_Table=''   then
                    if  @Branch_PartnerGid = ''  or @Branch_PartnerGid is null  then
						set Message = 'Branch_PartnerGid Is Not Given In  ';
						leave sp_Atma_PartnerBranch_Get;
					End if;
					End if;


			set Query_Select = '';

			set Query_Select =concat('select pb.partnerbranch_gid,pb.partnerbranch_gstno,pb.partnerbranch_panno,pb.partnerbranch_partnergid,pb.partnerbranch_code,
									  pb.partnerbranch_name,pb.partnerbranch_remarks,pb.partnerbranch_creditperiod,
                                      pb.partnerbranch_paymentterms,
                                      c.contact_reftablecode,c.Contact_contacttype_gid,
									  c.Contact_personname,c.Contact_mobileno,c.Contact_email,c.Contact_designation_gid,
                                      c.Contact_landline,c.Contact_landline2,c.Contact_mobileno2,
                                      c.Contact_DOB,c.Contact_WD,a.address_1,a.address_2,a.address_3,
                                      a.address_pincode,a.address_city_gid,cty.City_Name,
                                      a.address_state_gid,s.state_name,a.address_district_gid,dis.district_name
                                      ,ct.contacttype_Name,des.designation_name',Query_Column,'
                                      from ',Query_Table,' pb
                                      left join  ',Query_Table1,' c on c.contact_gid=pb.partnerbranch_contactgid
									  and pb.partnerbranch_isactive=''Y'' and pb.partnerbranch_isremoved=''N''
                                      and pb.entity_gid=',@Entity_Gid,' and c.entity_gid=',@Entity_Gid,'
									  left join  ',Query_Table2,' a on a.address_gid=pb.partnerbranch_addressgid
                                      and a.entity_gid=',@Entity_Gid,'
                                      left join  gal_mst_tstate s on a.address_state_gid=s.state_gid
                                      and s.entity_gid=',@Entity_Gid,'
                                      left join  gal_mst_tcity cty  on a.address_city_gid=cty.city_gid
                                      and cty.entity_gid=',@Entity_Gid,'
                                      left join  gal_mst_tdistrict dis  on a.address_district_gid=dis.district_gid
                                      and dis.entity_gid=',@Entity_Gid,'
                                      inner join  gal_mst_tcontacttype ct  on c.Contact_contacttype_gid=ct.contacttype_gid
                                      and ct.contacttype_isactive=''Y'' and ct.contacttype_isremoved=''N'' and ct.entity_gid=',@Entity_Gid,'
                                      inner join  gal_mst_tdesignation des  on c.Contact_designation_gid=des.designation_gid
                                      and des.designation_isactive=''Y'' and des.designation_isremoved=''N'' and des.entity_gid=',@Entity_Gid,'
                                      where partnerbranch_partnergid=',@Branch_PartnerGid,'
                                       ');


	 set @p = Query_Select;
    # select @p;
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