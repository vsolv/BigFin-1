CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Supplier_Get`(IN `ls_Type` varchar(32),IN `ls_SubType` varchar(32),
IN `lj_Filters` json, IN `lj_Classification` json,Out `Message` varchar(1000))
sp_Supplier_Get:BEGIN
# Santhosh 10-07-2019
#meenakshi edit query_select 04-02-2020
    Declare Query_Select text;
    Declare Query_Search varchar(1000);
    Declare li_Count int;

	set Query_Select ='';
    set Query_Search ='';
    set li_Count=0;

  if ls_Type='SUMMARY' and ls_SubType='SUPPLIER' then

    select JSON_LENGTH(lj_Classification,'$') into @li_classfication_count;

    if  @li_classfication_count is not null or  @li_classfication_count <>'' then
        select  JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid'))) into @Entity_gid;

		if @Entity_gid <= 0 or @Entity_gid='' then
			set Message='Entity gid is Needed';
			leave sp_Supplier_Get;
		else
			 set Query_Search=concat(Query_Search,'  a.entity_gid = ''',@Entity_gid,'''');
		end if;
	else
		 set Message='Classification Json is Empty';
		 leave sp_Supplier_Get;
	end if;

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


          set Query_Select=concat('select supplier_gid,supplier_isactive,supplier_name,supplier_capacity,supplier_code, address_gid,
          address_ref_code,address_1,address_2,address_3,address_pincode,district_name,city_name,state_name,
          address_district_gid,address_city_gid,address_state_gid,contact_gid,contact_ref_gid,contact_reftable_gid,
          contact_reftablecode,contact_contacttype_gid,contact_personname,contact_designation_gid,contact_landline,
          contact_landline2,contact_mobileno,contact_mobileno2,contact_email,contact_DOb,contact_Wd
          from gal_mst_tsupplier as a
          inner join gal_mst_taddress as b on a.supplier_add_gid = b.address_gid and address_ref_code in (''REF013'',''REF017'')
		  inner join gal_mst_tcity as d on b.address_city_gid=d.city_gid
		  inner join gal_mst_tdistrict as e on b.address_district_gid=e.district_gid
          inner join gal_mst_tstate as f on b.address_state_gid=f.state_gid and state_isremoved=''N''
          inner join gal_mst_tcontact as c on a.supplier_contact_gid = c.contact_gid
           where

            #supplier_isactive=''Y'' and supplier_isremoved=''N''
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
  end if;
END