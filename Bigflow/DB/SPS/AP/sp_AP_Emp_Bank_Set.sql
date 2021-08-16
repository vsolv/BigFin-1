CREATE  PROCEDURE `sp_AP_Emp_Bank_Set`(IN `ls_Action` varchar(32),IN `ls_Type` varchar(32),
IN `ls_Sub_Type` varchar(32),IN `lj_Details` json,IN `lj_Classification` json,
IN `ls_Createby` varchar(32),OUT `Message` varchar(1024))
sp_AP_Emp_Bank_Set:BEGIN
#Vishnu
declare Query_Insert varchar(9000);
declare Query_Update varchar(9000);
Declare errno int;
Declare msg varchar(1000);
declare countRow int;
Declare i int;


 if ls_Action='INSERT' and ls_Type = 'EMP' and ls_Sub_Type = 'BANK_DATA'   then

					select JSON_LENGTH(lj_Details,'$') into @li_Detailjson_count;
						if @li_Detailjson_count is null or @li_Detailjson_count = 0 then
							set Message = 'No Data In Json - Employee Bank Data.';
                            leave sp_AP_Emp_Bank_Set;
						end if;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Emp_Code'))) into @Emp_Code;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Emp_Gid'))) into @Emp_Gid;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Pay_Mode'))) into @Pay_Mode;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Bank_Name'))) into @Bank_Name;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Branch_Name'))) into @Branch_Name;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Ac_No'))) into @Ac_No;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, CONCAT('$.Beneficiary_Name'))) into @Beneficiary_Name;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid'))) into @Entity_Gid;


						if @Entity_Gid is null or @Entity_Gid = 0 or @Entity_Gid = '' then
							set Message = 'Entity Gid Is Needed.';
							leave sp_AP_Emp_Bank_Set;
						End if;

						if @Emp_Code is null or @Emp_Code = '' then
							set Message = 'Emp_Code Is Needed.';
							leave sp_AP_Emp_Bank_Set;
						End if;
                        set @Ref_Gid = '';
                        set @Ref_Gid = (select ref_gid from gal_mst_tref where ref_name = 'EMPLOYEE_PAYMENT');
               set Query_Insert = '';
			   set Query_Insert = concat('insert into gal_trn_tbankdetails (bankdetails_ref_gid,bankdetails_reftable_gid,
               bankdetails_reftable_code,bankdetails_paymode_gid,bankdetails_bank_gid,bankdetails_bankbranch_gid,bankdetails_acno,
               bankdetails_beneficiaryname,entity_gid,create_by)values(''',@Ref_Gid,''', ''',@Emp_Gid,''',
			   ''',@Emp_Code,''', ''',@Pay_Mode,''',''',@Bank_Name,''', ''',@Branch_Name,''',
			   ''',@Ac_No,''',''',@Beneficiary_Name,''',''',@Entity_Gid,''',''',ls_Createby,''')');

                                set @Insert_query = Query_Insert;
								#SELECT @Insert_query;
								PREPARE stmt FROM @Insert_query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;

                                if countRow > 0 then
                                  select LAST_INSERT_ID() into @Loaction_Maxgid ;
									set Message = 'SUCCESS';
                               else
                                    set Message = 'FAIL';
                              End if;
    End if;
END