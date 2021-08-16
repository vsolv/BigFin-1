CREATE DEFINER=`developer`@`%` PROCEDURE `galley`.`sp_Campaign_Get`(IN `ls_Type` varchar(64),IN `ls_Sub_Type` varchar(64),
IN `lj_Filters` json,IN `lj_Classification` json,OUT `Message` varchar(1024)
)
Campaign_Get:BEGIN

### Ramesh Dec 2018
#### Type : CAMPAIGN       #### CAMPAIGN_INVOICE
#Edit Prakash  31-jan-2019
## Ramesh :: Aug 14 2019, Feb 2020 - Rate Card Gid in Join
### SP Not Completed
Declare Query_Select varchar(5000);
Declare Query_Condition1 varchar(1024);
Declare Query_Condition2 varchar(1024);
Declare Query_ALL varchar(9000);
Declare Query_Where varchar(2000);
Declare Query_Group varchar(1024);
Declare li_count int;
declare entity_gid varchar(64);
declare i int;


        select JSON_LENGTH(lj_Classification, '$') into @li_jsonclass_count;

			if @li_jsonclass_count <=0 then
				set Message = 'Entity Gid Not Given';
				leave Campaign_Get;
			end if;

			set i = 0 ;

			select JSON_LENGTH(lj_Classification, CONCAT('$.Entity_Gid')) into @entity_cnt;

				if @entity_cnt <> 0 then
					WHILE i<= @entity_cnt - 1 Do

						select  JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid[',i,']')) into @entity_gid;
						if @entity_cnt  <> '' then
							 if @entity_gid <> 0 then
								if entity_gid <> '' then
									set entity_gid = concat(entity_gid,',',@entity_gid);
								else
									set entity_gid = @entity_gid;
								end if;

							end if;

						end if;
						set i = i + 1;

					END WHILE;
				end if;

set li_count = 0 ;

if ls_Type= 'INVOICE' and ls_Sub_Type ='SALES' then
		set Query_Select = '';
		set Query_Select = concat('Select a.campaign_name,a.campaign_gid,a.campaign_remarks,
													date_format(a.campaign_validfrom,''%d-%b-%Y'') as campaign_validfrom ,
													date_format(a.campaign_validto,''%d-%b-%Y'') as campaign_validto ,
													a.campaign_creditperiod,
                                                    case
                                                         When a.campaign_name = ''DEALER PRICE''  then ''Y''
														else ''N''
                                                     end as ''IS_Default''
                                                    from gal_mst_tcampaign as a where a.campaign_isactive = ''Y'' and a.campaign_isremoved = ''N''
													and now() between a.campaign_validfrom and a.campaign_validto and a.entity_gid =  ',entity_gid,'
                                                    Order by a.campaign_name asc
                                                    ' );

															set @Query_Select = Query_Select;
													#select @Query_Select; ## Remove It.
													PREPARE stmt1 FROM @Query_Select;
													EXECUTE stmt1;
													Select found_rows() into li_count;
													DEALLOCATE PREPARE stmt1;

													if li_count > 0 then
														set Message = 'FOUND';
													else
														set Message = 'NOT_FOUND';
													end if;

 elseif ls_Type= 'INVOICE' and ls_Sub_Type ='CUSTOMERGROUP' then

                              	select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Customer_Group_Gid'))) into @Customer_Group_Gid;
                                select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Customer_Gid'))) into @Customer_Gid;
                                select JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Product_Gid'))) into @Product_Gid;
								##select  @Customer_Group_Gid,@Customer_Gid,@Product_Gid;


                                 #check in customer_gid ;;;;
								if  @Customer_Gid is not null and @Customer_Gid <> 0  and @Customer_Gid = '' then
									if @Customer_Group_Gid = 0 or @Customer_Group_Gid = '' or @Customer_Group_Gid is null then
                                                    set @Customer_Group_Gid = 0 ;
												select ifnull(customer_custgroup_gid,0) into @Customer_Group_Gid from gal_mst_tcustomer
                                                where customer_gid = @Customer_Gid and customer_isactive = 'Y' and customer_isremoved = 'N';

										 if @Customer_Group_Gid is null or @Customer_Group_Gid = '' or @Customer_Group_Gid = 0 then
												set Message = 'Error On Customer Group Gid.';
                                                leave Campaign_Get;
                                         End if;
                              end if;

                                end if;



                                   select customer_gid into @Customer_Gid from gal_mst_tcustomer
                                    where customer_custgroup_gid = @Customer_Group_Gid and customer_isactive = 'Y' and customer_isremoved = 'N' limit 1;

                                    if @Customer_Gid = 0 or @Customer_Gid = '' or @Customer_Gid is null then
											set Message = 'Customer Gid Is Needed.';
											leave Campaign_Get;
									End if;


                          if @Customer_Group_Gid = 0 or @Customer_Group_Gid = '' or @Customer_Group_Gid is null then

                                                    set @Customer_Group_Gid = 0 ;
												select ifnull(customer_custgroup_gid,0) into @Customer_Group_Gid from gal_mst_tcustomer
                                                where customer_gid = @Customer_Gid and customer_isactive = 'Y' and customer_isremoved = 'N';

										 if @Customer_Group_Gid is null or @Customer_Group_Gid = '' or @Customer_Group_Gid = 0 then
												set Message = 'Error On Customer Group Gid.';
                                                leave Campaign_Get;
                                         End if;
                              end if;

					set Query_Select = '';
                    set Query_Condition1 = '';
                    set Query_Condition2 = '';
                    set Query_Where = '';
                    set Query_Group = '';
                    set Query_ALL = '';

						if @Product_Gid is not null and @Product_Gid <> '' and @Product_Gid <> 0 then
										set @Product_Gids = @Product_Gid;
                         else
                                         set @Product_Gids = 0 ;
                               			select group_concat(distinct ifnull(b.sodetails_product_gid,0)) into @Product_Gids from gal_trn_tsoheader as a
													inner join gal_trn_tsodetails as b on b.sodetails_soheader_gid = a.soheader_gid
                                                    	inner join gal_mst_tcustomer as c on c.customer_gid = a.soheader_customer_gid and c.customer_isactive = 'Y' and c.customer_isremoved = 'N'
													where c.customer_custgroup_gid = @Customer_Group_Gid
													 and a.soheader_isremoved = 'N'
                                                    and b.sodetails_isremoved = 'N' and a.entity_gid in  (entity_gid);
                        End if;

                        if @Product_Gids = 0  or @Product_Gids is null then
								#set Message = 'NOT_FOUND';
                                #leave Campaign_Get;
                                select group_concat(distinct product_gid) into @Product_Gids from gal_mst_tproduct
                                where product_tradingitem = 'Y' and product_isactive = 'Y' and product_isremoved = 'N';

                        End if;

				set Query_Select = concat('Select
                                                               #ifnull(c.dealerprice_gid,0) as dealer_price_gid ,
																#	ifnull(b.ratecard_gid,0) as ratecard_gid,
                                                                    #group_concat(distinct ifnull(b.ratecard_productgid,0)) as product_gidS,
																	#ifnull(b.ratecard_finalrate,0) as final_rate,
													a.campaign_name,a.campaign_gid,
                                                    (select group_concat(distinct ifnull(z.ratecard_productgid,0)) from gal_map_tratecard as z where z.ratecard_isactive = ''Y''
                                                      and z.ratecard_isremoved = ''N'' and z.ratecard_campaigngid = a.campaign_gid and now() between z.ratecard_validfrom and z.ratecard_validto
                                                      and z.ratecard_status = ''APPROVED'' and z.ratecard_productgid in (',@Product_Gids,') and (z.ratecard_customergroupgid = 0
                                                      or z.ratecard_customergroupgid is null
                                                      or z.ratecard_customergroupgid = ',@Customer_Group_Gid,' )
                                                    ) as product_gidS ,
													#a.campaign_remarks,date_format(a.campaign_validfrom,''%d-%b-%Y'') as campaign_validfrom ,
													#date_format(a.campaign_validto,''%d-%b-%Y'') as campaign_validto ,
													#a.campaign_creditperiod,
                                                      case
                                                           When a.campaign_name = ''DEALER PRICE''    then ''Y''
                                                           else ''N''
                                                      end as ''IS_Default''

                                                    from gal_mst_tcampaign as a
                                                     inner join gal_map_tratecard as b on b.ratecard_campaigngid = a.campaign_gid and
                                                    b.ratecard_isactive = ''Y'' and b.ratecard_isremoved = ''N'' and now() between b.ratecard_validfrom and b.ratecard_validto
                                                    and b.ratecard_status = ''APPROVED''
                                                    inner join gal_mst_tdealerprice as c on c.dealerprice_statepricegid  =
														fn_Customer_Data(''CUSTOMER_STATEPRICE'',',@Customer_Gid,',a.entity_gid)
                                                     and now() between c.dealerprice_validfrom and c.dealerprice_validto and c.dealerprice_isactive = ''Y'' and c.dealerprice_isremoved = ''N''
                                                     and c.dealerprice_productgid = b.ratecard_productgid and c.dealerprice_status = ''APPROVED'' ' );

                                                     set Query_Condition1 = concat('and b.ratecard_customergroupgid = ',@Customer_Group_Gid,'');
                                                     set Query_Condition2 = concat('and (b.ratecard_customergroupgid is null or b.ratecard_customergroupgid = 0) ');

                                                     set Query_Where = concat('where a.campaign_isactive = ''Y'' and a.campaign_isremoved = ''N''
                                                     and b.ratecard_productgid in (',@Product_Gids,')
                                                     and c.dealerprice_gid = b.ratecard_dealerpricegid
													and now() between a.campaign_validfrom and a.campaign_validto and a.entity_gid =  ',entity_gid,' ');
                                                    set Query_Group = concat(' group by a.campaign_name,a.campaign_gid
													#,a.campaign_remarks,date_format(a.campaign_validfrom,''%d-%b-%Y'')  ,
													#date_format(a.campaign_validto,''%d-%b-%Y'') ,
													#a.campaign_creditperiod

                                                    ' );

                                                    set Query_ALL = concat(Query_Select,Query_Where,Query_Condition1,Query_Group,
                                                                                                                                 ' Union ',
                                                                                              Query_Select,Query_Where,Query_Condition2,Query_Group
                                                                                             );


															set @Query_Select = Query_ALL;
													#select @Query_Select; ## Remove It.

													PREPARE stmt1 FROM @Query_Select;
													EXECUTE stmt1;
													Select found_rows() into li_count;
													DEALLOCATE PREPARE stmt1;

													if li_count > 0 then
														set Message = 'FOUND';
													else
														set Message = 'NOT_FOUND';
													end if;




 end if;
END