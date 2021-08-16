CREATE  PROCEDURE `sp_Atma_Query_Get`(in Type  varchar(16),
in lj_filter json,in lj_classification json,out Message varchar(1000))
BEGIN
Declare Query_Table varchar(1000);
Declare Query_Select varchar(5000);
Declare Query_Search varchar(5000);
Declare Query_Update varchar(5000);
Declare Query_Column varchar(5000);
Declare Query_Limit varchar(6144);
Declare countRow varchar(5000);
Declare li_count int;

if  Type ='Query' then

		select JSON_LENGTH(lj_filter,'$') into @li_json_count;
		select JSON_LENGTH(lj_classification,'$') into @li_json_lj_classification_count;

		if @li_json_lj_classification_count is not null or @li_json_lj_classification_count <> ''
			 or @li_json_lj_classification_count <> 0 then
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.Entity_Gid'))) into @entity_gid;
		end if;

        select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partner_name'))) into @partner_name;
        select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partner_Classification'))) into @partner_Classification;
        select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partner_type'))) into @partner_type;
        select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partner_contractdatefrom'))) into @partner_contractdatefrom;
        select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partner_contractdateto'))) into @partner_contractdateto;
        select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partner_mainstatus'))) into @partner_mainstatus;
        select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partnerbranch_gstno'))) into @partnerbranch_gstno;
        select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partnerbranch_panno'))) into @partnerbranch_panno;
        select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partnerbranch_name'))) into @partnerbranch_name;
        select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Activity_name'))) into @activity_name;
        select  JSON_UNQUOTE(JSON_EXTRACT(lj_filter, CONCAT('$.Partner_rmname'))) into @partner_rmname;
        Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Page_Index'))) into @Page_Index ;
		Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Page_Size'))) into @Page_Size ;
         set Query_Search = '';

                    if @partner_name <> '' and @partner_name is not null  then
                         set Query_Search = concat(Query_Search,' and part.partner_name like ''',@partner_name,'%','''  ');
                    End if;


                    if @partner_Classification <> '' and @partner_Classification is not null then
                         set Query_Search = concat(Query_Search,' and part.partner_Classification like ''',@partner_Classification,'%','''  ');
                    End if;

                    if @partner_type <> '' and @partner_type is not null then
                         set Query_Search = concat(Query_Search,' and part.partner_type like ''',@partner_type,'%','''  ');
                    End if;

					if @partner_contractdatefrom <> '' and @partner_contractdatefrom is not null  then
                        set Query_Search = concat(Query_Search,'and date_format(part.partner_contractdatefrom,''%Y-%m-%d'') = ''',@partner_contractdatefrom,'''  ');
                    End if;

                    if @partner_contractdateto <> '' and @partner_contractdateto is not null  then
                        set Query_Search = concat(Query_Search,'and date_format(part.partner_contractdateto,''%Y-%m-%d'') = ''',@partner_contractdateto,'''  ');
                    End if;

                    if @partner_mainstatus <> '' and @partner_mainstatus is not null then
                         set Query_Search = concat(Query_Search,' and part.partner_mainstatus like ''',@partner_mainstatus,'%','''  ');
                    End if;

                     if @partnerbranch_gstno <> '' and @partnerbranch_gstno is not null then
                         set Query_Search = concat(Query_Search,' and bran.partnerbranch_gstno like ''',@partnerbranch_gstno,'%','''  ');
                    End if;

                    if @partnerbranch_panno <> '' and @partnerbranch_panno is not null then
                         set Query_Search = concat(Query_Search,' and bran.partnerbranch_panno like ''',@partnerbranch_panno,'%','''  ');
                    End if;

                    if @partnerbranch_name <> '' and @partnerbranch_name is not null then
                         set Query_Search = concat(Query_Search,' and bran.partnerbranch_name like ''',@partnerbranch_name,'%','''  ');
                    End if;

                    if @activity_name <> '' and @activity_name is not null then
                         set Query_Search = concat(Query_Search,' and act.activity_name like ''',@activity_name,'%','''  ');
                    End if;

                    if @partner_rmname <> '' and @partner_rmname is not null then
                     set Query_Search = concat(Query_Search,' and part.partner_rmname like ''',@partner_rmname,'%','''  ');
                    End if;

                   set Query_Limit='';
				#select @Page_Index,@Page_Size;
					if @Page_Index <> '' and @Page_Index is not null and @Page_Size <> '' and @Page_Size is not null  then

									 set @total_size= @Page_Index*@Page_Size;
                                     set @Page_Size=@Page_Size;
									 set Query_Limit = concat(Query_Limit,' LIMIT ',@Page_Size,' OFFSET ',@total_size,'  ');

					else
									#select 1;
									set @Page_Index=2,@Page_Size=5;
									#select @Page_Index,@Page_Size;
									set @total_size= @Page_Index*@Page_Size;
									#select @total_size;
									set Query_Limit = concat(Query_Limit,' LIMIT ',@Page_Size,' OFFSET ',@total_size,'  ');
					End if;

#set Query_Select = '';
 set Query_Column='';
                     #select @Page_Index,@Page_Size;
							if @Page_Index=0 and @Page_Size=10 then
                            #select 1;
								set Query_Column = (',@Total_Row as Total_Row');
							end if;

	set Query_Select =concat('select
		  part.partner_gid,part.partner_code,part.partner_name, part.partner_panno,
		  part.partner_compregno,part.partner_group,
		  part.partner_custcategorygid, part.partner_Classification, part.partner_type,
		  part.partner_web,case
                            when partner_activecontract =''Y'' then ''Yes''
                            when partner_activecontract =''N'' then ''No'' end
                            partner_activecontract,
		  part.partner_reason_no_contract,part.partner_contractdatefrom,
		  part.partner_contractdateto,part.partner_aproxspend,
		  part.partner_actualspend, part.partner_noofdir,part.partner_orgtype,
		  part.partner_remarks, part.partner_status,part.partner_mainstatus,part.partner_requestfor,
		  part.partner_renewdate,part.partner_rmname,
          con.contact_reftablecode,con.Contact_contacttype_gid,
									  con.Contact_personname,con.Contact_mobileno,con.Contact_email,con.Contact_designation_gid,
                                      con.Contact_landline,con.Contact_landline2,con.Contact_mobileno2,
                                      con.Contact_DOB,con.Contact_WD,a.address_1,a.address_2,a.address_3,
                                      a.address_pincode,a.address_city_gid,cty.City_Name,
                                      a.address_state_gid,s.state_name,a.address_district_gid,dis.district_name
                                      ,ct.contacttype_Name,des.designation_name,
                        bran.partnerbranch_gstno,bran.partnerbranch_panno,bran.partnerbranch_name,
						act.activity_name,emp.employee_name ',Query_Column,'
						from atma_mst_tpartner part
						inner join atma_mst_tactivity act on   part.partner_code=act.activity_partnercode
                        inner join atma_mst_tpartnerbranch bran on bran.partnerbranch_gid=act.activity_partnerbranchgid
						inner join gal_mst_temployee emp on emp.employee_gid=part.partner_rmname
                        inner join  gal_mst_tcontact con on con.contact_gid=part.partner_contactgid
		  inner join  gal_mst_taddress a on part.partner_addressgid=a.address_gid
		  inner join  gal_mst_tstate s on a.address_state_gid=s.state_gid
		  inner join  gal_mst_tcity cty  on a.address_city_gid=cty.city_gid
		  inner join  gal_mst_tdistrict dis  on a.address_district_gid=dis.district_gid
		  inner join  gal_mst_tcontacttype ct  on con.Contact_contacttype_gid=ct.contacttype_gid
		  and ct.contacttype_isactive=''Y'' and ct.contacttype_isremoved=''N'' and ct.entity_gid=',@Entity_Gid,'
		  inner join  gal_mst_tdesignation des  on con.Contact_designation_gid=des.designation_gid
		  and des.designation_isactive=''Y'' and des.designation_isremoved=''N'' and des.entity_gid=',@Entity_Gid,'
						where part.partner_isactive=''Y'' and part.partner_isremoved=''N'' and part.entity_gid=',@entity_gid,'
						and bran.partnerbranch_isactive=''Y'' and bran.partnerbranch_isremoved=''N'' and bran.entity_gid=',@entity_gid,'
						and act.activity_isactive=''Y'' and act.activity_isremoved=''N'' and act.entity_gid=',@entity_gid,' and
                        emp.employee_isactive=''Y'' and emp.employee_isremoved=''N'' and emp.entity_gid=',@entity_gid,'

                        ',Query_Search,' group by partner_code ');

              #select Query_Select;
	if @Page_Index=0 and @Page_Size=10 then
						   #select 555;
							set @Query_Count = '';
							set @Query_Count = concat('select count(A.partner_gid) into @Total_Row from (',Query_Select,') A ');
								PREPARE stmt FROM @Query_Count;
									EXECUTE stmt;
								DEALLOCATE PREPARE stmt;

					   end if;
                      # select  @Total_Row;



						set @p = concat(Query_Select,Query_Limit);
                        #select @p;
						#select Query_Select; ### Remove It.
						PREPARE stmt FROM @p;
						EXECUTE stmt;
						Select found_rows() into li_count;
						DEALLOCATE PREPARE stmt;

							if li_count = 0 then
								set Message = 'NOT_FOUND';
							else
								set Message = 'FOUND';
							end if;

END IF;
END