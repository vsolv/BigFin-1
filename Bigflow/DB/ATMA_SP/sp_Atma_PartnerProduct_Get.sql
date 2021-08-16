CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_PartnerProduct_Get`(in li_Action  varchar(20),
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_Atma_PartnerProduct_Get:BEGIN

#Balamaniraja      06-08-2019

Declare Query_Select varchar(5000);
Declare Query_Search varchar(5000);
Declare Query_Table varchar(100);
Declare Query_Table1 varchar(100);
Declare Query_Column varchar(100);
Declare countRow varchar(5000);
Declare ls_count int;

IF li_Action='Atma_Product_Get' then

		select JSON_LENGTH(lj_classification,'$') into @lj_classification_json_count;
		select JSON_LENGTH(lj_filter,'$') into @json_count;

			if @lj_classification_json_count is null or  @lj_classification_json_count = 0
            or @lj_classification_json_count =''  then
				set Message = 'No Data In Json. ';
				leave sp_Atma_PartnerProduct_Get;
			End if;


				select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Entity_Gid')))into @Entity_Gid;
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.PartnerProduct_Gid')))into @PartnerProduct_Gid;
				select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Mst_Table')))into @Mst_Table;

                    set Query_Table='';
						if @Mst_Table='Mst' then
					set Query_Table = concat('atma_mst_tpartnerproduct');
						else
					set Query_Table = concat('atma_tmp_mst_tpartnerproduct');
					End if;

                    set Query_Table1='';
						if @Mst_Table='Mst' then
					set Query_Table1 = concat('gal_mst_tcontact');
						else
					set Query_Table1 = concat('atma_tmp_mst_tcontact');
					End if;

                    set Query_Column='';
            if @Mst_Table is null or @Mst_Table=''   then
				set Query_Column = concat(',pp.main_partnerproduct_gid');
			End if;


			if @Entity_Gid = 0 or @Entity_Gid = ''
            or @Entity_Gid is null  then
				set Message = 'Entity_Gid Is Not Given In classification Json. ';
				leave sp_Atma_PartnerProduct_Get;
			End if;



            set Query_Search = '';

        if @PartnerProduct_Gid is not null or @PartnerProduct_Gid <> '' then
			set Query_Search = concat(Query_Search,' and pp.partnerproduct_partnergid= ',@PartnerProduct_Gid,'  ');
		End if;


		set Query_Select = '';

		set Query_Select =concat('select pp.partnerproduct_partnergid,c1.contact_gid contact_gid1,
	pp.partnerproduct_clientcontactgid1,
	c2.contact_gid contact_gid2,pp.partnerproduct_clientcontactgid2,
	c3.contact_gid contact_gid3,pp.partnerproduct_customercontactgid1,
    c4.contact_gid contact_gid4,pp.partnerproduct_customercontactgid2,

    pp.partnerproduct_gid,pp.partnerproduct_type,pp.partnerproduct_name,pp.partnerproduct_age,

	c1.Contact_ref_gid,c1.Contact_reftable_gid,c1.contact_reftablecode,
    c1.Contact_contacttype_gid,c1.Contact_personname,c1.Contact_designation_gid,
    c1.Contact_landline,c1.Contact_landline2,c1.Contact_mobileno,c1.Contact_mobileno2,
    c1.Contact_email,c1.Contact_DOB,c1.Contact_WD,

	c2.Contact_ref_gid Contact_ref_gid_2,c2.Contact_reftable_gid Contact_reftable_gid_2,
    c2.contact_reftablecode contact_reftablecode_2, c2.Contact_contacttype_gid Contact_contacttype_gid_2,
    c2.Contact_personname Contact_personname_2,c2.Contact_designation_gid Contact_designation_gid_2,
    c2.Contact_landline Contact_landline_2,c2.Contact_landline2 Contact_landline2_2,
    c2.Contact_mobileno Contact_mobileno_2,c2.Contact_mobileno2 Contact_mobileno2_2,
    c2.Contact_email Contact_email_2,c2.Contact_DOB Contact_DOB_2,c2.Contact_WD Contact_WD_2,


	c3.Contact_ref_gid Contact_ref_gid_3,c3.Contact_reftable_gid Contact_reftable_gid_3,
    c3.contact_reftablecode contact_reftablecode_3, c3.Contact_contacttype_gid Contact_contacttype_gid_3,
    c3.Contact_personname Contact_personname_3,c3.Contact_designation_gid Contact_designation_gid_3,
    c3.Contact_landline Contact_landline_3,c3.Contact_landline2 Contact_landline2_3,
    c3.Contact_mobileno Contact_mobileno_3,c3.Contact_mobileno2 Contact_mobileno2_3,
    c3.Contact_email Contact_email_3,c3.Contact_DOB Contact_DOB_3,c3.Contact_WD Contact_WD_3,


    c4.Contact_ref_gid Contact_ref_gid_4,c4.Contact_reftable_gid Contact_reftable_gid_4,
    c4.contact_reftablecode contact_reftablecode_4, c4.Contact_contacttype_gid Contact_contacttype_gid_4,
    c4.Contact_personname Contact_personname_4,c4.Contact_designation_gid Contact_designation_gid_4,
    c4.Contact_landline Contact_landline_4,c4.Contact_landline2 Contact_landline2_4,
    c4.Contact_mobileno Contact_mobileno_4,c4.Contact_mobileno2 Contact_mobileno2_4,
    c4.Contact_email Contact_email_4,c4.Contact_DOB Contact_DOB_4,c4.Contact_WD Contact_WD_4,
    mt.metadata_value

	from ',Query_Table,' pp
	left join ',Query_Table1,' c1 on c1.contact_gid=pp.partnerproduct_clientcontactgid1
	and pp.partnerproduct_isactive=''Y'' and pp.partnerproduct_isremoved=''N'' and c1.entity_gid=',@Entity_gid,'
	inner join ',Query_Table1,' c2 on c2.contact_gid=pp.partnerproduct_clientcontactgid2
	inner join ',Query_Table1,' c3 on c3.contact_gid=pp.partnerproduct_customercontactgid1
	inner join ',Query_Table1,' c4 on c4.contact_gid=pp.partnerproduct_customercontactgid2
    inner join gal_mst_tmetadata mt on mt.metadata_gid=pp.partnerproduct_type
	where  c2.entity_gid=',@Entity_gid,' and c3.entity_gid=',@Entity_gid,'
 	and c4.entity_gid=',@Entity_gid,'   ',Query_Search,'
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