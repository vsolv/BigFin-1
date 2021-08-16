CREATE DEFINER=`developer`@`%` PROCEDURE `sp_EmployeeSync_Set`(in ls_Action varchar(16),in ls_Type varchar(32),
in lj_filter json,in ls_create_by int,out Message varchar(1000))
sp_EmployeeSync_Set:BEGIN
declare Query_Insert varchar(6000);
declare Query_Update varchar(6000);
declare Query_ varchar(6000);
declare Query_Column varchar(6000);
declare Query_Value varchar(6000);
declare Query_Store varchar(6000);
declare ls_error varchar(100);
declare countRow int;
declare errno int;
declare msg varchar(1000);
declare ls_no varchar(64);
declare i int;
declare ls_count varchar(2000);
DECLARE EXIT HANDLER FOR SQLEXCEPTION
BEGIN
GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
set Message = concat(errno , msg);
ROLLBACK;
END;
set ls_error = '';
set @Emp_srch = '';

start transaction;
set autocommit=0;
SET SESSION group_concat_max_len=4294967295;

if ls_Action = 'INSERT' and ls_Type='EMPLOYEE_SET' then

				select JSON_LENGTH(lj_filter,'$.ESM_EMP_Master') into @li_filter_Count ;

					if @li_filter_Count is null or @li_filter_Count = 0 then
							set Message = 'No Data In Json - data.';
							rollback;
							leave sp_EmployeeSync_Set;
					end if;

		set i=0;

    loopemp:while i<@li_filter_Count do

    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_EMP_Master[',i,'].V_TYPE')))into @V_TYPE;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_EMP_Master[',i,'].EMP_CCBS')))into @EMP_CCBS;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_EMP_Master[',i,'].SUPERVISOR')))into @SUPERVISOR;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_EMP_Master[',i,'].STATE')))into @STATE;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_EMP_Master[',i,'].PINCODE')))into @PINCODE;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_EMP_Master[',i,'].PRESENT_BRANCH')))into @PRESENT_BRANCH;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_EMP_Master[',i,'].NAME')))into @Emp_NAME;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_EMP_Master[',i,'].EMPLOYEE_TYPE')))into @EMPLOYEE_TYPE;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_EMP_Master[',i,'].DISTRICT')))into @DISTRICT;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_EMP_Master[',i,'].CODE')))into @Emp_CODE;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_EMP_Master[',i,'].V_EMP_MAIL')))into @V_EMP_MAIL;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_EMP_Master[',i,'].ENTITY')))into @ENTITY;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_EMP_Master[',i,'].CITY')))into @CITY;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_EMP_Master[',i,'].DOB')))into @DOB;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_EMP_Master[',i,'].DESIGNATION')))into @DESIGNATION;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_EMP_Master[',i,'].GENDER')))into @GENDER;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_EMP_Master[',i,'].DEPT')))into @DEPT;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_EMP_Master[',i,'].ENTITY_DETAIL')))into @ENTITY_DETAIL;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_EMP_Master[',i,'].DORESIGNATION')))into @DORESIGNATION;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_EMP_Master[',i,'].ADDRESS1')))into @ADDRESS1;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_EMP_Master[',i,'].DOJ')))into @DOJ;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_EMP_Master[',i,'].ADDRESS2')))into @ADDRESS2;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_EMP_Master[',i,'].ADDRESS3')))into @ADDRESS3;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_EMP_Master[',i,'].MOBILE')))into @MOBILE;
    #Select JSON_UNQUOTE(JSON_EXTRACT(lj_classification, CONCAT('$.ENTITY'))) into @ENTITY;
    # select EXISTS(select empgid from gal_mst_temployeesync WHERE empcode=@Emp_CODE) INTO @V_TYPE_1;



    # select @V_TYPE_1;

    if @EMP_CCBS is null then set @EMP_CCBS='NA' ; end if ;
    if @SUPERVISOR is null then set @SUPERVISOR='P. PON SIVAKUMAR'; end if ;
    if @STATE is null then set @STATE='NA'; end if ;
    if @PINCODE is null then set @PINCODE='111111'; end if ;
    if @DISTRICT is null then set @DISTRICT='NA'; end if ;
    if @CITY is null then set @CITY='NA'; end if ;
    if @ADDRESS1 is null then set @ADDRESS1='NA'; end if ;
    if @ADDRESS2 is null then set @ADDRESS2='NA'; end if ;
    if @ADDRESS3 is null then set @ADDRESS3='NA'; end if ;
    if @MOBILE is null then set @MOBILE='NA'; end if ;
    if @ENTITY is null then set @ENTITY='NA'; end if ;
    if @ENTITY_DETAIL is null then set @ENTITY_DETAIL='NA'; end if ;




    /*select @V_TYPE,@EMP_CCBS,@SUPERVISOR,
			@STATE,@PINCODE,@PRESENT_BRANCH,
				@Emp_NAME,@EMPLOYEE_TYPE,@DISTRICT,
				@Emp_CODE,@V_EMP_MAIL,@ENTITY,
				@CITY,@DOB,@DESIGNATION,@GENDER,
				@DEPT,@ENTITY_DETAIL,@DOJ,@DORESIGNATION,
				@MOBILE,@ADDRESS1,@ADDRESS2,
					@ADDRESS3,ls_create_by,@Staus,@Remarks;*/

                    set Query_Column ='';
                    set Query_Value ='';

                    if @DORESIGNATION is not null or @DORESIGNATION <>'' then
						set Query_Column =CONCAT(',empdor');
						set Query_Value =CONCAT(',',@DORESIGNATION);
					end if;

			set @Staus='NEW';
			set @Remarks='NEW';



		set Query_Insert='';
		set Query_Insert=concat('INSERT INTO gal_mst_temployeesync
										(empvtype, empccbs, empsupervisor, empstate, emppincode,
										 empbranch, empname, emptype, empdistrict,empcode, empemail,
                                         empentity, empcity, empdob,empdesignation,
										 empgender, empdept, empentitydetail, empdoj,
                                         empmobile, empaddress1, empaddress2, empaddress3,
										 create_by,staus,remarks ',Query_Column,')
								VALUES (''',@V_TYPE,''',''',@EMP_CCBS,''',''',@SUPERVISOR,''',
									    ''',@STATE,''',''',@PINCODE,''',''',@PRESENT_BRANCH,''',
                                        ''',@Emp_NAME,''',''',@EMPLOYEE_TYPE,''',''',@DISTRICT,''',
                                        ''',@Emp_CODE,''',''',@V_EMP_MAIL,''',''',@ENTITY,''',
										''',@CITY,''',''',@DOB,''',''',@DESIGNATION,''',''',@GENDER,''',
                                        ''',@DEPT,''',''',@ENTITY_DETAIL,''',''',@DOJ,''',
                                        ''',@MOBILE,''',''',@ADDRESS1,''',''',@ADDRESS2,''',
										''',@ADDRESS3,''',',ls_create_by,',''',@Staus,''',''',@Remarks,'''
                                         ',Query_Value,')');

							#select Query_Insert;
							set @p=Query_Insert;
							prepare stmt from @p;
							execute stmt;
							select row_count() into ls_count;

							if ls_count>0 then
								set Message='SUCCESS';
							else
							   set Message='NOT SUCCESS';
							  rollback;
							end if;
								 set i=i+1;
							end while;

			if Message = 'SUCCESS' then
                set Message = 'SUCCESS';
            else
                set Message = 'FAIL';
                rollback;
            end if;

					select concat('{' '"' ,'DATA' ,'"' ':'  '[',group_concat(empgid),']' ,'}') into @data_json
							from gal_mst_temployeesync where empisremoved='N' and staus='NEW';

       Select count(empgid)into @data_json_count from gal_mst_temployeesync
						where empisremoved='N' and staus='NEW' ;


	   set i=0;

       loopemp_sync:while i<@data_json_count do

			Select JSON_UNQUOTE(JSON_EXTRACT(@data_json ,CONCAT('$.DATA[',i,']')))into @Emp_Gid;


         select empvtype into @Emp_type from gal_mst_temployeesync where empgid=@Emp_Gid and staus='NEW';
         select empdept into @Emp_Dept from gal_mst_temployeesync where empgid=@Emp_Gid and staus='NEW';
         select empbranch into @Emp_Branch from gal_mst_temployeesync where empgid=@Emp_Gid and staus='NEW';
         select empdesignation into @Emp_Designation from gal_mst_temployeesync where empgid=@Emp_Gid and staus='NEW';


          # set @dept_sync1='', @branch_sync1='', @designation_sync1='',
			#   @dept_sync='', @branch_sync='', @designation_sync='';


			select exists(select dept_code from gal_mst_tdept where dept_code=@Emp_Dept) into @dept_test;
            select exists(select branch_code from gal_mst_tbranch where branch_code=@Emp_Branch) into @branch_test;
            select exists(select designation_name from gal_mst_tdesignation where designation_name=@Emp_Designation) into @designation_test;

            set Query_Column='';


            if @dept_test=0  then
				set Query_Column = concat(Query_Column,'Invalid Dept');
			end if;


            if @branch_test=0  then
				if @dept_test=0 then
					set Query_Column = concat(Query_Column,',');
				end if;
					set Query_Column = concat(Query_Column,'Invalid Branch');
			end if;


            if @designation_test=0  then

			select exists(select designation_code from gal_mst_tdesignation) into @Code_Test;

			#select max(substr(bankbranch_code,3)) from gal_mst_tbankbranch  into @BankBr_Code;


            if @Code_Test=0 then
				call sp_Generatecode_Get('WITHOUT_DATE', 'DES', '00','000', @Message);
				select @Message into @Desig_Code;
			else
				select max(substr(designation_code,4)) from gal_mst_tdesignation into @Desig_Value;
				call sp_Generatecode_Get('WITHOUT_DATE', 'DES', '00',@Desig_Value, @Message);
				select @Message into @Desig_Code;
			end if;


             set @Entity_Gid=1;
             set Query_Insert = '';
             set Query_Insert = concat('INSERT INTO gal_mst_tdesignation
											(designation_code,designation_name,
                                             entity_gid,create_by)
										VALUES (''',@Desig_Code,''',''' ,@Emp_Designation,
                                        ''',' ,@Entity_Gid,',' ,ls_create_by, ')');

						set @Query_Insert = Query_Insert;
						#SELECT @Query_Insert;
						PREPARE stmt FROM @Query_Insert;
						EXECUTE stmt;
						set countRow = (select ROW_COUNT());
						DEALLOCATE PREPARE stmt;

				if countRow >  0 then
					set Message='SUCCESS';
					select LAST_INSERT_ID() into @Emp_Designation ;
				else
					set Message = 'FAIL';
					rollback;
				end if;

				end if;#  if @designation_test=0  then

            #HERE CHECK THE CONDITION

            #select  @dept_test, @branch_test,@designation_test,@Emp_type,@Emp_Dept,@Emp_Branch, @Emp_Designation ;

			if @dept_test=0 or @branch_test=0 then
						set i=i+1;
						set Query_Column = concat(',remarks=','''',Query_Column,'''');

                        set @sync_status='FAILED';

				set Query_Update='';
				set Query_Update=concat('update gal_mst_temployeesync
											set staus=''',@sync_status,''',
												create_by =',ls_create_by,',
                                                create_date = now()
                                                ',Query_Column,'
											where empgid=',@Emp_Gid,'
												  and empisremoved= ''N'' ');

						set @Query_Updates = Query_Update;
						#select Query_Update;
						PREPARE stmt FROM @Query_Updates;
						EXECUTE stmt;
						set countRow = (select ROW_COUNT());
						DEALLOCATE PREPARE stmt;

					if countRow>0 then
						set message='SUCCESS';
					else
						  set message='NOT SUCCESS';
						  rollback;
					end if;

					ITERATE loopemp_sync;
			end if;



			set @sync_status='SUCCESS';

            set Query_Update='';
            set Query_Update=concat('update gal_mst_temployeesync
											set staus=''',@sync_status,''',
												create_by =',ls_create_by,',
                                                create_date = now()
                                                ',Query_Column,'
											where empgid=',@Emp_Gid,'
												  and empisremoved= ''N'' ');

						set @Query_Updates = Query_Update;
						#select Query_Update;
						PREPARE stmt FROM @Query_Updates;
						EXECUTE stmt;
						set countRow = (select ROW_COUNT());
						DEALLOCATE PREPARE stmt;

					if countRow>0 then
						set message='SUCCESS';
					else
						  set message='NOT SUCCESS';
						  rollback;
					end if;




	#select empaddress1,empaddress2,empaddress3,emppincode,empdistrict,empcity,empstate,@Emp_Gid
				#	from gal_mst_temployeesync where  empgid=@Emp_Gid;


	select empaddress1,empaddress2,empaddress3,emppincode,empdistrict,empcity,empstate
		into @Emp_Address1,@Emp_Address2,@Emp_Address3,@Emp_PinCode,@Emp_District,@Emp_City,@Emp_State
					from gal_mst_temployeesync where  empgid=@Emp_Gid;



      select dept_gid into @Dept_Gid from gal_mst_tdept
			where dept_code=@DEPT and dept_isactive='Y'
				and dept_isremoved='N' group by dept_gid;


      select designation_gid into @Designation_Gid from gal_mst_tdesignation
			where designation_name=@DESIGNATION and designation_isactive='Y'
				and designation_isremoved='N' group by designation_gid;


      select branch_gid into @Branch_Gid from gal_mst_tbranch
			where branch_code=@PRESENT_BRANCH and branch_isactive='Y'
				and branch_isremoved='N' group by branch_gid;


      select employee_supervisor_gid into @Employee_Supervisor_gid from gal_mst_temployee
			where employee_supervisor=@SUPERVISOR and employee_isactive='Y'
				and employee_isremoved='N' group by employee_supervisor  ;


      select city_gid into @City_Gid from gal_mst_tcity
			where City_Name=@Emp_City  and city_isremoved='N' group by city_gid;


      select district_gid into @District_Gid from gal_mst_tdistrict
			where district_name=@Emp_District
				and district_isremoved='N' group by district_gid;


      select state_gid into @State_Gid from gal_mst_tstate
			where state_name=@Emp_State
				and state_isremoved='N' group by state_gid;


     # select pincode_gid into @Pincode_Gid from gal_mst_tpincode
		#	where pincode_no=@PINCODE
			#	and pincode_isremoved='N' group by pincode_gid;


            #select @Emp_Address1,@Emp_Address2,@Emp_Address3,
						#	   @Emp_PinCode,@District_Gid,@City_Gid,
							#   @State_Gid;

      set @Address_Gid='0';
      call sp_Address_Set('INSERT',0,'BRANCH',@Emp_Address1,@Emp_Address2,@Emp_Address3,
							   @Emp_PinCode,@District_Gid,@City_Gid,
							   @State_Gid,@ENTITY,ls_create_by,@Message);

                          #select @ADDRESS1,@ADDRESS2,@ADDRESS3,@PINCODE,@District_Gid,
                          #@City_Gid,@State_Gid,@ENTITY,ls_create_by;
      select  substring_index(@Message,',',-1) into @Address_Msg;
      #select   @Message,@Address_Msg;

                  if @Address_Msg='SUCCESS'then
					  set message='SUCCESS';
					  select LAST_INSERT_ID() into @Address_Id;
					  #select  @Address_Id;
                  else
					  set message=CONCAT('FAIL -',@Message);
					  rollback;
                  end if;



                #select @Emp_Designation,@DEPT,@PRESENT_BRANCH,@designation_test;


            #select empcode,empname,empgender, empdob, empdoj,empdor,
           # @Dept_Gid,@Designation_Gid,empsupervisor,
           #@Employee_Supervisor_gid, empmobile,empemail,@Address_Id,1,create_by,0,@Branch_Gid
           # from gal_mst_temployeesync  where empgid=@Emp_Gid;

            if @Emp_type='A' then




                set Query_Store='';
                set Query_Store=concat('INSERT INTO gal_mst_temployee
											  (employee_code,employee_name,employee_gender,employee_dob,
											   employee_doj,employee_dor, employee_dept_gid,employee_designation_gid,
                                               employee_supervisor,employee_supervisor_gid,employee_mobileno,
                                               employee_emailid,employee_add_gid,entity_gid,create_by,
                                               employee_hierarchygid,branch_gid)
										(select empcode,empname,empgender, empdob, empdoj,empdor,
											    ',@Dept_Gid,',',@Designation_Gid,',empsupervisor,
											    ',@Employee_Supervisor_gid,', empmobile,empemail,
                                                ',@Address_Id,',1,create_by,0,',@Branch_Gid,'
											from gal_mst_temployeesync
                                            where empgid=',@Emp_Gid,' ) ');

            #select empcode,empname,empgender,empdob,empdoj,empdor,@Dept_Gid,@Designation_Gid,empsupervisor,
            #@Employee_Supervisor_gid,empmobile,empemail,@Address_Id,create_by,@Branch_Gid;

            #select Query_Store;
            set @Query_Stores= Query_Store;
            PREPARE stmt FROM @Query_Stores;
            EXECUTE stmt;
            set countRow = (select ROW_COUNT());
            DEALLOCATE PREPARE stmt;

            if countRow>0 then
                set message='SUCCESS';
            else
            set message='NOT SUCCESS';
              rollback;
                   end if;

            elseif @Emp_type='M'  then

					set SQL_SAFE_UPDATES=0;
					SET Query_Update='';
					set Query_Update = concat(' Update gal_mst_temployee
													  set employee_name =''',@Emp_NAME,''',
														  employee_gender = ''',@GENDER,''',
														  employee_dob = ''',@DOB,''',
                                                          employee_doj = ''',@DOJ,''',
                                                          employee_dor=''',@DORESIGNATION,''',
                                                          employee_dept_gid = ',@Dept_Gid,',
														  branch_gid=',@Branch_Gid,',
                                                          employee_designation_gid = ',@Designation_Gid,',
                                                          employee_supervisor_gid = ',@Employee_Supervisor_gid,',
														  employee_mobileno = ''',@MOBILE,''',
                                                          employee_emailid = ''',@V_EMP_MAIL,''',
                                                          employee_add_gid =',@Address_Id,',
														  update_by =',ls_create_by,',
                                                          Update_date = now()
												where employee_isremoved = ''N''
													  and employee_isactive = ''Y''
                                                      and employee_code =''',@Emp_CODE,''' ');

						set @Query_Updates = Query_Update;
					    #select Query_Update;
						PREPARE stmt FROM @Query_Updates;
						EXECUTE stmt;
						set countRow = (select ROW_COUNT());
						DEALLOCATE PREPARE stmt;
						if countRow>0 then
								set message='SUCCESS';
							else
								  set message='NOT SUCCESS';
								  rollback;
							end if;



            end if;
              set i=i+1;

        end while;


			if message='SUCCESS' then
                set message='SUCCESS';
                commit;
            else
				set message='NOT SUCCESS';
                rollback;
			end if;


end if;
end