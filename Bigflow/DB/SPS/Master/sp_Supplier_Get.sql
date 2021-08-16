CREATE DEFINER=`developer`@`%` PROCEDURE `galley`.`sp_Supplier_Get`(IN `ls_Type` varchar(32),IN `ls_SubType` varchar(32),
IN `lj_Filters` json, IN `lj_Classification` json,Out `Message` varchar(1000))
sp_Supplier_Get:BEGIN
# Santhosh 10-07-2019
# Ramesh Nov 22 2019
    Declare Query_Select text;
    Declare Query_Search varchar(1000);
    Declare li_Count int;

	set Query_Select ='';
    set Query_Search ='';
    set li_Count=0;

				select JSON_LENGTH(lj_Classification,'$') into @li_classfication_count;

				if  @li_classfication_count is not null or  @li_classfication_count <>'' then
					select  JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid'))) into @Entity_gid;

					if @Entity_gid <= 0 or @Entity_gid='' then
						set Message='Entity gid is Needed';
						leave sp_Supplier_Get;
					end if;
				else
					 set Message='Classification Json is Empty';
					 leave sp_Supplier_Get;
				end if;

  if ls_Type='SUMMARY' and ls_SubType='SUPPLIER' then

				select JSON_LENGTH(lj_Filters,'$') into @li_json_count;

				if @li_json_count is not null or @li_json_count <> '' then

					 select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Supplier_Gid'))) into @Supplier_gid;
					 select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Supplier_Code'))) into @Supplier_code;

				 if @Supplier_gid is not null or @Supplier_gid <> 0 or @Supplier_gid<>''  then
					   set Query_Search=concat(Query_Search,' and supplier_gid = ''',@Supplier_gid,'''');
				 end if;
				 if @Supplier_code is not null or @Supplier_code <> 0 or @Supplier_code<>'' then
					   set Query_Search=concat(Query_Search,' and supplier_code = ''',@Supplier_code,'''');
				 end if;
				end if;

					set Query_Select=concat('select z.suppliergroup_gid,z.suppliergroup_code,supplier_gid,supplier_isactive,supplier_name,z.suppliergroup_name,
                    supplier_capacity,supplier_code,a.supplier_branchname,a.supplier_gstno,address_gid,address_ref_code,address_1,address_2,address_3,address_pincode,
					district_name,city_name,state_name,address_district_gid,address_city_gid,address_state_gid,contact_gid,contact_ref_gid,
					contact_reftable_gid,contact_reftablecode,contact_contacttype_gid,contact_personname,contact_designation_gid,
					contact_landline,contact_landline2,contact_mobileno,contact_mobileno2,contact_email,date_format(contact_Dob,''%Y-%m-%d '') as contact_Dob ,
                    date_format(contact_Wd,''%Y-%m-%d '') as contact_Wd
                    from gal_mst_tsupplier as a
					inner join gal_mst_tsuppliergroup as z on z.suppliergroup_gid = a.supplier_groupgid
                    left join gal_mst_taddress as b on a.supplier_add_gid=b.address_gid and address_ref_code=''REF013''
					left join gal_mst_tcontact as c on a.supplier_gid=c.contact_reftable_gid and contact_ref_gid=12
					left join gal_mst_tcity as d on b.address_city_gid=d.city_gid
					left join gal_mst_tdistrict as e on b.address_district_gid=e.district_gid
					left join gal_mst_tstate as f on b.address_state_gid=f.state_gid and state_isremoved=''N''
					where  z.suppliergroup_isactive = ''Y'' and z.suppliergroup_isremoved = ''N''
				   # supplier_isactive=''Y'' and supplier_isremoved=''N''
                   and a.entity_gid = ',@Entity_gid,'
				   ', Query_Search,' ');

					set @p = Query_Select;
					 #select @p; ### Remove it
					PREPARE stmt FROM @p;
					EXECUTE stmt;
					select found_rows() into li_count;
					DEALLOCATE PREPARE stmt;

					if li_count > 0 then
						set Message = 'FOUND';
						commit;
					else
						set Message = 'NOT_FOUND';
					end if;

   elseif ls_Type='DDL' and ls_SubType='SUPPLIER_GROUP' then

        select  JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Detail_Gid'))) into @Entity_Detail_Gid;

			Select a.suppliergroup_gid,a.suppliergroup_name
				from gal_mst_tsuppliergroup as a
				where a.suppliergroup_isactive = 'Y' and a.suppliergroup_isremoved = 'N'
				and a.entity_gid = @Entity_gid and a.entity_detailsgid = @Entity_Detail_Gid ;

				set Message = 'FOUND';
	elseif ls_Type='DDL' and ls_SubType='SUPPLIER' then

        select  JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Detail_Gid'))) into @Entity_Detail_Gid;

			Select a.supplier_gid,a.supplier_name
				from gal_mst_tsupplier as a
				where a.supplier_isactive = 'Y' and a.supplier_isremoved = 'N'
				and a.entity_gid = @Entity_gid;

				set Message = 'FOUND';

    elseif ls_Type='EDIT_DETAIL' and ls_SubType='SUPPLIER_GROUP' then

			select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.SupplierGrp_Gid'))) into @SupplierGrp_Gid;
			select  JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Detail_Gid'))) into @Entity_Detail_Gid;

         if @SupplierGrp_Gid is null or @SupplierGrp_Gid = 0 or @SupplierGrp_Gid = '' then
				set Message = 'Supplier Group Gid Is Needed.';
                leave sp_Supplier_Get;
         End if;

		Select a.suppliergroup_gid,a.suppliergroup_code,a.suppliergroup_name,a.suppliergroup_addgid,a.suppliergroup_contactgid,d.city_gid,
		 e.district_gid,f.state_gid,g.contacttype_gid,
		 b.address_1,b.address_2,b.address_3,b.address_pincode,d.City_Name,e.district_name,f.state_name,g.contacttype_Name,

         contact_landline,contact_landline2,contact_mobileno,contact_mobileno2,
         c.contact_personname,c.contact_designation_gid,c.contact_email,date_format(c.contact_Dob,'%Y-%m-%d ') as contact_Dob ,
                    date_format(c.contact_Wd,'%Y-%m-%d ') as contact_Wd

		 from gal_mst_tsuppliergroup as a
		 inner join gal_mst_taddress as b on b.address_gid = a.suppliergroup_addgid
		 inner join gal_mst_tcontact as c on c.contact_gid = a.suppliergroup_contactgid
		 inner join gal_mst_tcity as d on d.city_gid = b.address_city_gid
		 inner join gal_mst_tdistrict as e on e.district_gid = b.address_district_gid
		 inner join gal_mst_tstate as f on f.state_gid = b.address_state_gid
		 inner join gal_mst_tcontacttype as g on g.contacttype_gid = c.Contact_contacttype_gid
         left join gal_mst_tdesignation as h on h.designation_gid = c.Contact_designation_gid
		 where a.suppliergroup_isactive = 'Y' and a.suppliergroup_isremoved = 'N'
		 and a.entity_gid = @Entity_Gid and a.entity_detailsgid = @Entity_Detail_Gid
		and a.suppliergroup_gid = @SupplierGrp_Gid
		 ;

         set Message = 'FOUND';

  end if;
END