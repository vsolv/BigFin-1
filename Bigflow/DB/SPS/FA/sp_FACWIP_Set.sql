CREATE DEFINER=`developer`@`%` PROCEDURE `sp_FACWIP_Set`(IN `ls_Action` varchar(32),IN `ls_Type` varchar(32),
IN `ls_Sub_Type` varchar(32),IN `lj_Details` json,IN `lj_File` json,IN `lj_Classification` json,IN `ls_Createby` varchar(32),
OUT `Message` varchar(1024))
sp_FACWIP_Set:BEGIN

	### Ramesh Dec 19 2019
Declare Query_Insert varchar(9000);
Declare Query_Update varchar(9000);
Declare errno int;
Declare msg varchar(1000);
Declare countRow int;
Declare i int;
# Null Selected Output
DECLARE done INT DEFAULT 0;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
#...

  DECLARE EXIT HANDLER FOR SQLEXCEPTION,sqlwarning

    BEGIN

     GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
     set Message = concat(errno , msg);
     ROLLBACK;
     END;

    	 select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid[0]'))) into @Entity_Gid;

             if @Entity_Gid is  null or @Entity_Gid = 0 or @Entity_Gid = '' then
					set Message = 'Entity Gid Is Needed.';
                    leave sp_FACWIP_Set;
             End if;

 if ls_Type = 'CWIP_INITIAL' and ls_Sub_Type = 'MAKER' THEN

        select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.CWIP_Qty')) into @CWIP_Qty;
       	select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.CWIP_Date')) into @CWIP_Date;
      	select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.CWIP_Asset_Group_Gid')) into @CWIP_Asset_Group_Gid;
     	select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.Asset_CatGid')) into @Asset_CatGid;
   		select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.CWIPProduct_Gid')) into @CWIPProduct_Gid;
   		select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.GL_Cat')) into @GL_Cat;
  		select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.GL_SubCat')) into @GL_SubCat;
 		select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.Asset_Value')) into @Asset_Value;
 		select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.Asset_Cost')) into @Asset_Cost;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.CWIP_Description')) into @CWIP_Description;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.CWIP_Status')) into @CWIP_Status;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.CWIP_RequestStatus')) into @CWIP_Request_Status;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.CWIP_Owner')) into @CWIP_Owner;
        #select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.CWIP_SNo')) into @CWIP_SNo;
       	select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.CWIP_Inv_Gid')) into @CWIP_Inv_Gid;
      	select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.CWIP_Inw_Gid')) into @CWIP_Inw_Gid;
     	select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.CWIP_InwDetails_Gid')) into @CWIP_InwDetails_Gid;
    	select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.CWIP_Inw_Date')) into @CWIP_Inw_Date;
   		select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.CWIP_Mep_No')) into @CWIP_Mep_No;
  		select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.CWIP_PONo')) into @CWIP_PONo;
  	    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.CWIP_CRNo')) into @CWIP_CRNo;
  	    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.CWIP_ImagePath')) into @CWIP_ImagePath;
  	    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.CWIP_VendorName')) into @CWIP_VendorName;
  	    select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.CWIP_Group_Gid')) into @CWIP_Group_Gid;


  	    if @CWIP_ImagePath is null THEN
  	      set @CWIP_ImagePath = '';
  	    End if;
  	   ### Validation TO DO
  	   set i = 0 ;
  	   While i <= @CWIP_Qty - 1 DO

  	     #select @CWIP_ID,@CWIP_Date,@CWIP_Asset_Group_Gid,@Asset_CatGid,@CWIPProduct_Gid,@GL_Cat,@GL_SubCat,@Asset_Value,@Asset_Cost,
     	  #      @CWIP_Description,@CWIP_Status,@CWIP_Request_Status,@CWIP_Owner,@CWIP_SNo,@CWIP_Inv_Gid,@CWIP_Inw_Gid,@CWIP_InwDetails_Gid,
  	       # @CWIP_Inw_Date,@CWIP_Mep_No,@CWIP_PONo,@CWIP_PONo,@CWIP_CRNo,@CWIP_ImagePath,@CWIP_VendorName,@CWIP_Group_Gid,
  	       #@Entity_Gid,ls_Createby;

  	        Select ifnull(max(cast(cwipasset_id as decimal)),0)+1 into @CWIP_ID from fa_trn_tcwipasset;
	    	 set @CWIP_SNo = '212';
 		  	set Query_Insert = '';
 	 	 	set Query_Insert = concat('
			insert into fa_trn_tcwipasset (cwipasset_id,cwipasset_qty,cwipasset_date,cwipasset_assetgroupid,cwipasset_assetcatgid,
			  cwipasset_productgid,cwipasset_cat,cwipasset_subcat,cwipasset_value,cwipasset_cost,cwipasset_description,
              cwipasset_status,cwipasset_requeststatus,cwipasset_assetowner,cwipasset_assetserialno,cwipasset_invoicegid,
              cwipasset_inwheadergid,cwipasset_inwdetailgid,cwipasset_inwarddate,cwipasset_mepno,
			  cwipasset_ponum,cwipasset_crnum,cwipasset_imagepath,cwipasset_vendorname,cwipasset_cwipgroupgid,entity_gid,create_by)
			 values (''',@CWIP_ID,''',''1'',''',@CWIP_Date,''',''',@CWIP_Asset_Group_Gid,''',''',@Asset_CatGid,''',
                   ''',@CWIPProduct_Gid,''',''',@GL_Cat,''',''',@GL_SubCat,''',''',@Asset_Value,''',''',@Asset_Cost,''',
                   ''',@CWIP_Description,''',''',@CWIP_Status,''',''',@CWIP_Request_Status,''',''',@CWIP_Owner,''',
                   ''',@CWIP_SNo,''',''',@CWIP_Inv_Gid,''',''',@CWIP_Inw_Gid,''',''',@CWIP_InwDetails_Gid,''',
                   ''',@CWIP_Inw_Date,''',''',@CWIP_Mep_No,''',''',@CWIP_PONo,''',''',@CWIP_CRNo,''',''',@CWIP_ImagePath,''',
                   ''',@CWIP_VendorName,''',''',@CWIP_Group_Gid,''',''',@Entity_Gid,''',''',ls_Createby,''')');

                  				set @Insert_query = Query_Insert;
								#SELECT @Insert_query;
								PREPARE stmt FROM @Insert_query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
							    select LAST_INSERT_ID() into @Trn_CWIP_Gid ;
								DEALLOCATE PREPARE stmt;

                                if countRow > 0 then
									set Message = 'SUCCESS';

								  	call sp_Trans_Set('Insert','CWIP_ASSET',@Trn_CWIP_Gid,
										 'MAKER','G', 'MAKER',
                                         'CWIP',@Entity_Gid, ls_Createby, @Message);
				   					select @Message into @out_msg_tran ;

									if @out_msg_tran = 'FAIL' then
										set Message = 'Failed On Tran Insert';
										leave sp_FACWIP_Set;
									ELSEIF @out_msg_tran is not null and LENGTH(@out_msg_tran) < 12 then
									   set Message ='SUCCESS';
									End if;


                                Else
                                     set Message = 'FAIL In CWIP Insert.';
                                    leave sp_FACWIP_Set;
                                End if;


  	    set i = i+1;
  	   End While;



  ELSEIF ls_Type = 'CWIP_CHECKER' and ls_Sub_Type = 'CHECKER' THEN

       select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.CWIP_Gids')) into @CWIP_Gids;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.CWIP_Status')) into @CWIP_Status;


        set Query_Update = '';
        set Query_Update = concat('Update fa_trn_tcwipasset set cwipasset_requeststatus = ''',@CWIP_Status,''',
        update_by = ''',ls_Createby,''', update_date = now()
        where cwipasset_gid in (',@CWIP_Gids,')');

						       set @Update_query = Query_Update;
								#SELECT @Insert_query;
								PREPARE stmt FROM @Update_query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;

                                if countRow > 0 then
									set Message = 'SUCCESS';
                                Else
                                     set Message = 'FAIL In CWIP Update.';
                                    leave sp_FACWIP_Set;
                                End if;
 ELSEIF ls_Type = 'CWIP_TOASSET' and ls_Sub_Type = 'ASSET_MAKE' THEN

        select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.CWIP_Gids')) into @CWIP_Gids;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.CWIP_RequestNo')) into @CWIP_RequestNo;
         select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.CWIP_CPDATE')) into @CWIP_CPDATE;


           set Query_Update = '';
          set Query_Update = concat('Update fa_trn_tcwipasset set cwipasset_releaserequestno = ''',@CWIP_RequestNo,''',
            cwipasset_capdate = ''',@CWIP_CPDATE,''',
            update_by = ''',ls_Createby,''', update_date = now()
            where cwipasset_gid in (',@CWIP_Gids,')');

						       set @Update_query = Query_Update;
								#SELECT @Insert_query;
								PREPARE stmt FROM @Update_query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
								DEALLOCATE PREPARE stmt;

                                if countRow > 0 then
									set Message = 'SUCCESS';
                                Else
                                     set Message = 'FAIL In CWIP Update.';
                                    leave sp_FACWIP_Set;
                                End if;

 ELSEIF ls_Action  = 'INSERT' and ls_Type = 'CWIP_GROUP' THEN


        select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.CWIP_Name')) into @CWIP_Name;
        select JSON_UNQUOTE(JSON_EXTRACT(lj_Details, '$.CWIP_Gl')) into @CWIP_Gl;


        if @CWIP_Name is null or @CWIP_Name ='' then
				set Message='CWIP Name is Not Given';
                leave sp_FACWIP_Set;
        end if;

        if @CWIP_Gl is null or @CWIP_Gl ='' then
				set Message='CWIP Gl is Not Given';
                leave sp_FACWIP_Set;
        end if;

        if ls_Createby is null or ls_Createby ='' or ls_Createby =0 then
				set Message='Create_By is Not Given';
                leave sp_FACWIP_Set;
        end if;

        set @CWIP_Code='';
        select max(cwipgroup_code) into @CWIP_Code from fa_mst_tcwipgroup;

		if  @CWIP_Code='' or @CWIP_Code is null  then
			call sp_Generatecode_Get('WITHOUT_DATE', 'CWG', '00','000', @Message);
			select @Message into @CWIP_Code;
		else
			call sp_Generatecode_Get('WITHOUT_DATE', 'CWG', '00',@CWIP_Code, @Message);
			select @Message into @CWIP_Code;
		end if;


		set Query_Insert = '';
		set Query_Insert = concat('insert into fa_mst_tcwipgroup
														(cwipgroup_code, cwipgroup_name,
														 cwipgroup_gl,entity_gid,create_by)
												 values (''',@CWIP_Code,''',''',@CWIP_Name,''',
														 ''',@CWIP_Gl,''',',@Entity_Gid,',
																		   ',ls_Createby,') ');

                  				set @Insert_query = Query_Insert;
								#SELECT @Insert_query;
								PREPARE stmt FROM @Insert_query;
								EXECUTE stmt;
								set countRow = (select ROW_COUNT());
							    #select LAST_INSERT_ID() into @LAST_INSERT_Gid ;
								DEALLOCATE PREPARE stmt;

                                if countRow > 0 then
									set Message = 'SUCCESS';
								else
									set Message = 'FAIL';
									leave sp_FACWIP_Set;
								End if;


 End if;


END