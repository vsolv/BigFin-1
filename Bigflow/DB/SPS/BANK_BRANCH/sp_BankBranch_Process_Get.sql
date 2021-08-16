CREATE DEFINER=`developer`@`%` PROCEDURE `sp_BankBranch_Process_Get`(IN `ls_Type` varchar(64),IN `ls_Sub_Type` varchar(64),
IN `lj_Filters` json,IN `lj_Classification` json, OUT `Message` varchar(1024))
sp_BankBranch_Process_Get:BEGIN
### Bala Mar 13 2020 - Created
Declare Query_Select varchar(4024);
Declare Query_Search varchar(1024);
Declare Query_Status varchar(1024);
Declare Query_Column varchar(1024);
Declare Query_Limit varchar(1024);
declare errno int;
declare msg varchar(1000);
declare li_count int;

# Null Selected Output
DECLARE done INT DEFAULT 0;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
#....

	DECLARE EXIT HANDLER FOR SQLEXCEPTION,sqlwarning

    BEGIN
		GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
		set Message = concat(errno , msg);
		ROLLBACK;
    END;


		select  JSON_UNQUOTE(JSON_EXTRACT(lj_Classification,'$.Entity_Gid[0]')) into @Entity_Gids;

        if @Entity_Gids is  null or @Entity_Gids = '' then
				set Message = 'Entity_Gid Is Not Given';
                leave sp_BankBranch_Process_Get;
        End if;

IF ls_Type = 'BANK_BRANCH' and ls_Sub_Type = 'SUMMARY' then


							select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Bank_Name'))) into @Bank_Name;
							select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.BankBranch_Name'))) into @BankBranch_Name;
							select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.BankBr_ifsccode'))) into @BankBr_ifsccode;

							set Query_Search = '';


                             if @Bank_Name <> '' and @Bank_Name is not null  then
								set Query_Search = concat(Query_Search,' and F.bank_name like ''','%',@Bank_Name,'%','''  ');
							 End if;

                             if @BankBranch_Name <> '' and @BankBranch_Name is not null  then
								set Query_Search = concat(Query_Search,' and A.bankbranch_name like ''','%',@BankBranch_Name,'%','''  ');
							 End if;

                             if @BankBr_ifsccode <> '' and @BankBr_ifsccode is not null  then
								set Query_Search = concat(Query_Search,' and A.bankbranch_ifsccode like ''','%',@BankBr_ifsccode,'%','''  ');
							 End if;


                             # A.bankbranch_isactive=''Y'' and A.bankbranch_isremoved=''N''  and


						set Query_Select = '';
                        set Query_Select = concat(' select  A.bankbranch_gid, A.bankbranch_bank_gid, A.bankbranch_code, A.bankbranch_name,
															A.bankbranch_ifsccode, A.bankbranch_microcode, A.bankbranch_address_gid,
															A.bankbranch_isactive, A.bankbranch_isremoved, A.create_by,
															B.address_gid,B.address_1,B.address_2,B.address_3,
															B.address_pincode,C.district_gid,C.district_name,
                                                            D.city_gid,D.City_Name,E.state_gid,E.state_name,F.bank_name
															   from gal_mst_tbankbranch A
														  left join gal_mst_taddress B on B.address_gid=A.bankbranch_address_gid
																and B.entity_gid in (',@Entity_Gids,')
														  left join gal_mst_tdistrict C on C.district_gid=B.address_district_gid
															    and C.district_isremoved=''N''
															    and C.entity_gid in (',@Entity_Gids,')
														  left join gal_mst_tcity D on D.city_gid=B.address_city_gid
															    and D.city_isremoved=''N''
															    and D.entity_gid in (',@Entity_Gids,')
														  left join gal_mst_tstate E on E.state_gid=B.address_state_gid
														  inner join gal_mst_tbank F on F.bank_gid=A.bankbranch_bank_gid
															  and E.state_isremoved=''N''
															  and E.entity_gid in (',@Entity_Gids,')
																	where A.entity_gid in (',@Entity_Gids,')
                                                                        and F.bank_isactive=''Y'' and F.bank_isremoved=''N''
																	    and F.entity_gid in (',@Entity_Gids,')
																	',Query_Search,'
												 ');


								set @Query_Select = Query_Select;
			      		        #select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
                                    leave sp_BankBranch_Process_Get;
							  end if;



END IF;

END