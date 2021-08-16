CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Branchsync_Set`(in ls_Action varchar(16),in ls_Type varchar(32),
in lj_filter json,in ls_create_by int,out Message varchar(1000))
sp_Branchsync_Set:BEGIN
declare Query_Insert varchar(6000);
declare Query_Update varchar(6000);
declare Query_ varchar(6000);
declare Query_Column varchar(6000);
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
set autocommit=off;

SET SESSION group_concat_max_len=4294967295;

if ls_Action = 'Insert' and ls_Type='BRANCH_SET' then
     # select JSON_LENGTH(lj_classification,'$')into @lj_classification_stmt;
      select JSON_LENGTH(lj_filter,'$.ESM_BRANCH_Master') into @li_filter_Stmt ;
      if @li_filter_Stmt is null or @li_filter_Stmt = 0 then
      set Message = 'No Data In Json - data.';
      rollback;
      leave sp_Branchsync_Set;
      end if;
      /*if @lj_classification_stmt is null or @lj_classification_stmt =0 then
      set message ='no classification In Json - classification';
      rollback;
      end if;*/
    set i=0;
    loopemp:while i<@li_filter_Stmt do

    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_BRANCH_Master[',i,'].BRANCH_TAN')))into @BRANCH_TAN;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_BRANCH_Master[',i,'].GSTIN')))into @GSTIN;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_BRANCH_Master[',i,'].MOBILE2')))into @MOBILE2;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_BRANCH_Master[',i,'].STATE')))into @STATE;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_BRANCH_Master[',i,'].CONTACT_PERSON')))into @CONTACT_PERSON;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_BRANCH_Master[',i,'].LANDLINE1')))into @LANDLINE1;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_BRANCH_Master[',i,'].EMAIL')))into @EMAIL;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_BRANCH_Master[',i,'].PINCODE')))into @PINCODE;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_BRANCH_Master[',i,'].LANDLINE2')))into @LANDLINE2;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_BRANCH_Master[',i,'].DISTRICT')))into @DISTRICT;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_BRANCH_Master[',i,'].ENTITY')))into @ENTITY;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_BRANCH_Master[',i,'].CONTACT_TYPE')))into @CONTACT_TYPE;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_BRANCH_Master[',i,'].STD_CODE')))into @STD_CODE;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_BRANCH_Master[',i,'].INCHARGE')))into @INCHARGE;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_BRANCH_Master[',i,'].ADDRESS1')))into @ADDRESS1;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_BRANCH_Master[',i,'].MOBILE1')))into @MOBILE1;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_BRANCH_Master[',i,'].ADDRESS3')))into @ADDRESS3;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_BRANCH_Master[',i,'].ADDRESS2')))into @ADDRESS2;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_BRANCH_Master[',i,'].V_TYPE')))into @V_TYPE;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_BRANCH_Master[',i,'].CONTROL_OFFICE_BRANCH')))into @CONTROL_OFFICE_BRANCH;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_BRANCH_Master[',i,'].NAME')))into @Branch_Name;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_BRANCH_Master[',i,'].CODE')))into @Branch_CODE;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_BRANCH_Master[',i,'].CONTACT_PERSON_DESIGNATION'))) into @CONTACT_PERSON_DESIGNATION ;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_BRANCH_Master[',i,'].CITY')))into @CITY;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_BRANCH_Master[',i,'].ENTITY_DETAIL')))into @ENTITY_DETAIL;
    Select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.ESM_BRANCH_Master[',i,'].PAN')))into @PAN;


        set Query_Insert='';
        set @Branch_Status='NEW';
        set @Remarks='NEW';
        set Query_Insert=concat('INSERT INTO gal_mst_tbranchsync (branch_tan, branch_GSTIN,
                                        branch_mobile2, branch_state, branch_contactperson,
                                        branch_landline1, branch_email, branch_pincode,
                                        branch_landline2, branch_district, branch_entity,
                                        branch_contacttype, branch_stdcode, branch_incharge,
                                        branch_address1, branch_mobile1, branch_address2,
                                        branch_address3, branch_Vtype, branch_cob, branch_name,
                                        branch_code,branch_cpd, branch_city, branch_entity_detail,
                                        branch_pan,branch_status,remarks,create_by
            ) VALUES (''',@BRANCH_TAN,''',''',@GSTIN,''',''',@MOBILE2,''',
        ''',@STATE,''',''',@CONTACT_PERSON,''',''',@LANDLINE1,''',''',@EMAIL,''',''',@PINCODE,''',
        ''',@LANDLINE2,''',''',@DISTRICT,''',''',@ENTITY,''',''',@CONTACT_TYPE,''',
        ''',@STD_CODE,''',''',@INCHARGE,''',''',@ADDRESS1,''',''',@MOBILE1,''',''',@ADDRESS2,''',''',@ADDRESS3,''',
        ''',@V_TYPE,''',''',@CONTROL_OFFICE_BRANCH,''',''',@Branch_Name,''',''',@Branch_CODE,''',''',@CONTACT_PERSON_DESIGNATION,''',
        ''',@CITY,''',''',@ENTITY_DETAIL,''',''',@PAN,''',''',@Branch_Status,''',''',@Remarks,''',',ls_create_by,')');


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
           leave sp_Branchsync_Set;
        end if;
            set i=i+1;
      end while;



      select concat('{' '"' ,'DATA' ,'"' ':'  '[',group_concat(branch_gid),']' ,'}') into @data_json
      from gal_mst_tbranchsync where branch_status='NEW';

       Select count(branch_gid)into @data_json_count from gal_mst_tbranchsync where branch_status='NEW';

        #select @data_json_count;

        set i=0;
        loopbranch_sync:while i<@data_json_count do
        Select JSON_UNQUOTE(JSON_EXTRACT(@data_json ,CONCAT('$.DATA[',i,']')))into @Branch_Gid;
        #select @Branch_Gid;

         select branch_cpd into @Branch_Cpd from gal_mst_tbranchsync
                where branch_gid= @Branch_Gid and branch_status='NEW';

         select branch_incharge into @branch_incharge from gal_mst_tbranchsync
                WHERE branch_gid= @Branch_Gid and branch_status='NEW';



		#HERE Branch_ContactType IS A DESIGNATION
		select branch_contacttype,branch_address1,branch_address2,branch_address3,branch_pincode,
			   branch_district,branch_city,branch_state,branch_contactperson,
               branch_landline1,branch_landline2,branch_mobile1,branch_mobile2,branch_email
			   into @Branch_ContactType ,@Branch_Address1,@Branch_Address2,@Branch_Address3,@Branch_PinCode,
					@Branch_District,@Branch_City,@Branch_State,@Branch_ContactPerson,
                    @Branch_LandLine1,@Branch_LandLine2,@Branch_Mobile1,@Branch_Mobile2,@Branch_Email
			from gal_mst_tbranchsync  where branch_gid=@Branch_Gid and branch_status='NEW' ;


		 select city_gid into @City_Gid from gal_mst_tcity
                where City_Name=@Branch_City  and city_isremoved='N' group by city_gid;
      #select @City_Gid;

      select district_gid into @District_Gid from gal_mst_tdistrict
      where district_name=@Branch_District
      and district_isremoved='N' group by district_gid;

      #select  @District_Gid;

      select state_gid into @State_Gid from gal_mst_tstate
      where state_name=@Branch_State
      and state_isremoved='N' group by state_gid;
      #select  @State_Gid;

      select pincode_gid into @Pincode_Gid from gal_mst_tpincode
      where pincode_no=@Branch_PinCode
      and pincode_isremoved='N' group by pincode_gid;


      select designation_gid into @Designation_Gid from gal_mst_tdesignation
      where designation_name=@Branch_ContactType and designation_isactive='Y'
      and designation_isremoved='N' group by designation_gid;



      select designation_name into @Des_Name from gal_mst_tdesignation  where
      designation_gid=@CONTACT_PERSON_DESIGNATION
      and designation_isactive='Y' and designation_isremoved='N';


       #select exists(select contacttype_Name  from gal_mst_tcontacttype
            #where contacttype_Name=@CONTACT_PERSON_DESIGNATION) into @ConType_Test;

        select exists(select designation_name  from gal_mst_tdesignation
            where designation_name=@CONTACT_PERSON_DESIGNATION) into @Desig_Test;

          select exists(select employee_name from gal_mst_temployee
             where employee_name=@INCHARGE) into @Incharge_Test;

            set Query_Column='';

            if @Incharge_Test=0  then
                set Query_Column = concat(Query_Column,'Invalid Incharge_Name');
            end if;

            select @Incharge_Test;

            if @Desig_Test=0  then
                if @Incharge_Test=0 then
                    set Query_Column = concat(Query_Column,',');
                end if;
                    set Query_Column = concat(Query_Column,'Invalid Designation');
            end if;


           if @Incharge_Test=0 or @Desig_Test=0 then

                set Query_Column = concat(',remarks=','''',Query_Column,'''');

                        set @Temp_Status='FAILED';

                set Query_Update='';
                set Query_Update=concat('update gal_mst_tbranchsync
                                            set branch_status=''',@Temp_Status,''',
                                                create_date = now()
                                                ',Query_Column,'
                                              where branch_gid=',@Branch_Gid,'' );

                        set @Query_Updates = Query_Update;
                        #select Query_Update;
                        PREPARE stmt FROM @Query_Updates;
                        EXECUTE stmt;
                        set countRow = (select ROW_COUNT());
                        DEALLOCATE PREPARE stmt;

                    if countRow>0 then
                        set Message='SUCCESS';
                    else
                          set Message='NOT SUCCESS';
                          rollback;
                          leave sp_Branchsync_Set;
                    end if;

                set i =i+1;
                ITERATE  loopbranch_sync;
           end if; #if @Incharge_Test=0 or @Desig_Test=0 then







      set @Address_Gid=0;
      call sp_Address_Set('INSERT',@Address_Gid,'BRANCH',@Branch_Address1,@Branch_Address2,@Branch_Address3,
                          @Branch_PinCode,@District_Gid,@City_Gid,
                          @State_Gid,@ENTITY,ls_create_by,@Message);

                          select @Message;

      select  substring_index(@Message,',',-1) into @Address_Msg;

                  if @Address_Msg='SUCCESS'then
					  set Message='SUCCESS';
					  select LAST_INSERT_ID() into @Address_Id;
				  else
					  set Message=@Message;
					  rollback;
					  leave sp_Branchsync_Set;
                  end if;



      set @li_cont_gid=0;
      call sp_Contact_Set('Insert',@li_cont_gid,'BRANCH',1,1,@CONTACT_PERSON,
                                 @Designation_Gid,@LANDLINE1,@LANDLINE2,@MOBILE1,
                                 @MOBILE2,@EMAIL,'','',
                                '1',ls_create_by,@Message);

              select  substring_index(@Message,',',-1) into @Contact_Msg;

      # select 11;
                  if @Contact_Msg='SUCCESS'then
					  set Message='SUCCESS';
					  select LAST_INSERT_ID() into @li_Cont_Gid;
					else
					  set Message=@Message;
					  rollback;
					  leave sp_Branchsync_Set;
                  end if;



             set @Temp_Status='SUCCESS';
             set Query_Update='';
           #set @sync_status='success';
            set Query_Update=concat('update gal_mst_tbranchsync
                                        set branch_status=''',@Temp_Status,''',
                                        create_date = now() ',Query_Column,'
                                            where branch_gid=',@Branch_Gid,'');

              set @Query_Updates = Query_Update;
              select Query_Update;
              PREPARE stmt FROM @Query_Updates;
              EXECUTE stmt;
              set countRow = (select ROW_COUNT());
              DEALLOCATE PREPARE stmt;
            if countRow>0 then
                set Message='SUCCESS';
            else
                  set Message='NOT SUCCESS';
                  rollback;
                  leave sp_Branchsync_Set;
            end if;



             #set @branch_add_gid=000;
                  #set @branch_con_id=000;

                 #branch_entity_detail hot code for column branch_entitydetailsgid
                 #branch_incharge hot code for column branch_inchargegid

          if @V_TYPE='A' and @Temp_Status='success'  then

              set Query_Store='';
                set Query_Store=concat('INSERT INTO gal_mst_tbranch
              (branch_entitydetailsgid, branch_code, branch_name, branch_tanno, branch_glno,
               branch_inchargegid, branch_stdcode, branch_addressgid, branch_contactgid,
               entity_gid,create_by)
            (select 1,branch_code,branch_name, branch_tan,0,',@INCHARGE_TEST,',branch_stdcode,
            ',@Address_Id,',',@li_Cont_Gid,',1,1 from gal_mst_tbranchsync where branch_gid=',@Branch_Gid,') ');


			set @Query_Stores= Query_Store;
            PREPARE stmt FROM @Query_Stores;
            EXECUTE stmt;
            set countRow = (select ROW_COUNT());
            DEALLOCATE PREPARE stmt;

            if countRow>0 then
                set Message='SUCCESS';
				set @Branch_Last_Gid=LAST_INSERT_ID();
            else
				set Message='NOT SUCCESS';
				rollback;
                leave sp_Branchsync_Set;
            end if;




		select metadata_gid into @Meta_Gst from gal_mst_tmetadata where metadata_value='GSTNO';
        select metadata_gid into @Meta_Phone from gal_mst_tmetadata where metadata_value='PHONENO';
        select metadata_gid into @Meta_State from gal_mst_tmetadata where metadata_value='State_gid';


        insert into gal_mst_tbranchinfo(branchinfo_branchgid,branchinfo_metadatagid,branch_metadatavalue,entity_gid,create_by)
        values(@Branch_Gid,@Meta_Gst,@GSTIN,@ENTITY,ls_create_by);

        insert into gal_mst_tbranchinfo(branchinfo_branchgid,branchinfo_metadatagid,branch_metadatavalue,entity_gid,create_by)
        values(@Branch_Gid,@Meta_Phone,@MOBILE1,@ENTITY,ls_create_by);

        insert into gal_mst_tbranchinfo(branchinfo_branchgid,branchinfo_metadatagid,branch_metadatavalue,entity_gid,create_by)
        values(@Branch_Gid,@Meta_State,@State_Gid,@ENTITY,ls_create_by);

          #select 10000000;



            elseif @V_TYPE='M' and @Temp_Status='success' then

            #select empcode,empname,empgender,empdob,empdoj,empdor,@Dept_Gid,@Designation_Gid,empsupervisor,
            #@Employee_Supervisor_gid,empmobile,empemail,@Address_Id,create_by,@Branch_Gid;
              set SQL_SAFE_UPDATES=0;
             SET Query_Update='';

  set Query_Update = concat( ' Update gal_mst_tbranch set branch_entitydetailsgid =1, branch_code = ''',@Branch_CODE,''',
                             branch_name = ''',@Branch_Name,''', branch_tanno = ''',@BRANCH_TAN,''',branch_inchargegid = ',@INCHARGE_TEST,',
                            branch_stdcode=',@STD_CODE,', branch_addressgid = ',@Address_Id,', branch_contactgid = ',@li_Cont_Gid,',
                            entity_gid = ''',@ENTITY,''', create_date = now()

                            where branch_isremoved = ''N'' and branch_isactive = ''Y''and branch_gid=',@Branch_Gid,'');
        set @Query_Updates = Query_Update;
      # select Query_Update;
        PREPARE stmt FROM @Query_Updates;
        EXECUTE stmt;
        set countRow = (select ROW_COUNT());
        DEALLOCATE PREPARE stmt;
        if countRow>0 then
                set Message='SUCCESS';
            else
                  set Message='NOT SUCCESS';
                  rollback;
                  leave sp_Branchsync_Set;
            end if;

            end if;
              set i=i+1;

        end while;


			if Message='SUCCESS' then
                set Message='SUCCESS';
                commit;
            else
				set Message='NOT SUCCESS';
				rollback;
			end if;






end if;
end