CREATE PROCEDURE `sp_Courier_Mst_Get`(IN `ls_Type` varchar(64),IN `ls_Sub_Type` varchar(64),
IN `lj_Filters` json,IN `lj_Classification` json,
OUT `Message` varchar(1024))
sp_Courier_Mst_Get:BEGIN
### Vishnu Feb 18 2020
Declare Query_Select varchar(6144);
Declare Query_Search varchar(1024);
declare errno int;
declare msg varchar(1000);
declare li_count int;

	select fn_Classification('ENTITY_ONLY',lj_Classification) into @OutMsg_Classification ;
        select  JSON_UNQUOTE(JSON_EXTRACT(@OutMsg_Classification, '$.Entity_Gid[0]')) into @Entity_Gids;
        if @Entity_Gids is  null or @Entity_Gids = '' then
				select  JSON_UNQUOTE(JSON_EXTRACT(@OutMsg_Classification, '$.Message')) into @Message;
				set Message = concat('Error On Classification Data - ',@Message);
                leave sp_Courier_Mst_Get;
        End if;

if ls_Type = 'COURIER' and ls_Sub_Type = 'DATA' then
						set Query_Select = '';
            set Query_Search = '';
            select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Courier_Name'))) into @Courier_Name;
		  ##select @Courier_Name;
            set Query_Search='';
            if @Courier_Name<>'' or @Courier_Name is not null then
                 set Query_Search=concat('and a.courier_name like ''','%',@Courier_Name,'%','''');
            end if;


			set Query_Select = concat('
							 select a.courier_type,a.courier_name,a.courier_contactperson,d.contacttype_Name,c.Contact_personname,
							e.designation_name,c.Contact_landline,c.Contact_landline2,c.Contact_mobileno,
                            c.Contact_mobileno2,c.Contact_email,b.address_1,b.address_2,b.address_3,
                            b.address_pincode,f.state_name,g.district_name,h.City_Name
							from dis_mst_tcourier as a
                             inner join gal_mst_taddress as b on a.courier_addressgid = b.address_gid
							 inner join gal_mst_tcontact as c on a.courier_contactgid = c.contact_gid
							 inner join gal_mst_tcontacttype as d on c.Contact_contacttype_gid = d.contacttype_gid
							 inner join gal_mst_tdesignation as e on c.Contact_designation_gid = e.designation_gid
							 inner join gal_mst_tstate as f on b.address_state_gid = f.state_gid
							 inner join gal_mst_tdistrict as g on b.address_district_gid = g.district_gid
							 inner join gal_mst_tcity as h on b.address_city_gid = h.city_gid
                             where a.courier_isactive = ''Y'' and a.courier_isremoved = ''N'' and a.entity_gid in (',@Entity_Gids,')
							 and c.entity_gid in (',@Entity_Gids,')
							 and d.contacttype_isactive = ''Y'' and d.contacttype_isremoved = ''N'' and d.entity_gid in (',@Entity_Gids,')
							 and b.entity_gid in (',@Entity_Gids,')
							 and e.designation_isactive = ''Y'' and e.designation_isremoved = ''N'' and e.entity_gid in (',@Entity_Gids,')
							 and f.state_isremoved = ''N'' and f.entity_gid in (',@Entity_Gids,')
							 and g.district_isremoved = ''N'' and g.entity_gid in (',@Entity_Gids,')
							 and h.city_isremoved = ''N'' and h.entity_gid in (',@Entity_Gids,') ',Query_Search,'
							');
                     	set @Query_Select = Query_Select;
			      		#select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
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