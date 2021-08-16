CREATE PROCEDURE `sp_AP_Emp_Bank_Get`(IN ls_action varchar(64),IN ls_type varchar(64),
IN lj_Filters json,IN lj_Classification json, OUT Message varchar(1024))
BEGIN
Declare Query_Select varchar(6144);
declare ls_count int;
##Vishnu
if ls_action='EMP' and ls_type='BANK_DATA' then
		select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid'))) into @Entity_Gid;

		set Query_Select=' ';
					set Query_Select=concat('select b.employee_name,a.bankdetails_reftable_code,c.Paymode_name,
												d.bank_name,e.bankbranch_name,a.bankdetails_acno,
												a.bankdetails_beneficiaryname  from gal_trn_tbankdetails as a
												left join gal_mst_temployee as b on b.employee_gid = a.bankdetails_reftable_gid
												left join gal_mst_tpaymode as c on c.paymode_gid = a.bankdetails_paymode_gid
												left join gal_mst_tbank as d on d.bank_gid = a.bankdetails_bank_gid
												left join gal_mst_tbankbranch as e on e.bankbranch_gid = a.bankdetails_bankbranch_gid
												where bankdetails_ref_gid =40 and a.entity_gid in (',@Entity_Gid,')');

					  #select Query_Select;
					  set @p= Query_Select;
					  prepare stmt from @p;
					  execute stmt;
					  select found_rows() into ls_count;
					 # select ls_count;
					   if ls_count >0 then
							 set message='FOUND';
						else
							set message='NOT FOUND-sp_AP_Emp_Bank_Set';
					  end if;
end if;
END