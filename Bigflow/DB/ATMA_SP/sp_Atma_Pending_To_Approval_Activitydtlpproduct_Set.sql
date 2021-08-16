CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Pending_To_Approval_Activitydtlpproduct_Set`(in li_Action  varchar(30),
in lj_filter json,in Mst_Partner_Gid int,in Mst_activitydetails int,in Newpartnerbranchgid int,in Oldpartnerbranchgid int,
in  Activitydetail_old_gid int,
in lj_classification json,out Message varchar(1000))
sp_Atma_Pending_To_Approval_Activitydtlpproduct_Set:BEGIN
declare Query_Insert varchar(10000);
Declare countRow varchar(6000);
declare Query_Update varchar(10000);
declare Query_delete varchar(1000);
declare Query_Value varchar(1000);
declare Query_Column varchar(1000);
Declare cat_activitydtlpproduct_gid,cat_activitydtlpproduct_activitydetailsgid,cat_activitydtlpproduct_mpartnerproductgid,cat_activitydtlpproduct_category,
		cat_activitydtlpproduct_subcategory,cat_activitydtlpproduct_name,cat_activitydtlpproduct_spec,cat_activitydtlpproduct_size,cat_activitydtlpproduct_remarks,
		cat_activitydtlpproduct_uomgid,cat_activitydtlpproduct_rate,cat_activitydtlpproduct_validfrom,cat_activitydtlpproduct_validto,cat_activitydtlpproduct_isactive,
		cat_activitydtlpproduct_isremoved,cat_entity_gid,cat_create_by,cat_main_activitydtlpproduct_gid varchar(150);
Declare m_mpartnerproduct_gid,m_mpartnerproduct_partner_gid,m_mpartnerproduct_partnerbranch_gid,
		m_mpartnerproduct_product_gid,m_mpartnerproduct_unitprice,m_mpartnerproduct_packingprice,
		m_mpartnerproduct_validfrom,m_mpartnerproduct_validto,m_mpartnerproduct_deliverydays,m_mpartnerproduct_capacitypw,m_mpartnerproduct_dts,
		m_mpartnerproduct_status,m_mpartnerproduct_isactive,m_mpartnerproduct_isremoved,m_entity_gid,m_create_by,
		m_main_mpartnerproduct_gid  varchar(150);
DECLARE finished INTEGER DEFAULT 0;
DECLARE finished1 INTEGER DEFAULT 0;

Declare errno int;
Declare msg,Error_Level varchar(1000);

						DECLARE EXIT HANDLER FOR SQLEXCEPTION
						BEGIN
							GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
							set Message = concat(Error_Level,' :No-',errno,msg);
							ROLLBACK;
						END;

IF li_Action='Insert' then



	select JSON_LENGTH(lj_filter,'$') into @lj_filter_json_count;
	select JSON_LENGTH(lj_classification,'$') into @lj_classification_json_count;

	if @lj_filter_json_count = 0 or @lj_filter_json_count is null then
		set Message = 'No Data In filter Json. ';
		leave sp_Atma_Pending_To_Approval_Activitydtlpproduct_Set;
	End if;

	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Gid')))
	into @Partner_Gid;
    #select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Status')))
	#into @Partner_Status;
    select JSON_UNQUOTE(JSON_EXTRACT(lj_classification,CONCAT('$.Update_By')))
	into @Update_By;
#SET @Partner_Status='APPROVED';
	select partner_status from atma_mst_tpartner where partner_gid=Mst_Partner_Gid
    into @mst_partner_status;

	#if @Partner_Gid = '' or @Partner_Gid is null  or @Partner_Gid=0 then
			#set Message = 'Partner Is Not Provided';
			#leave sp_Atma_Pending_To_Approval_Activitydtlpproduct_Set;
	#End if;

	#set @activitydetailsgid=4;
      #SET finished =0;
  SELECT EXISTS(
         select true from  atma_tmp_map_tpartnerproduct
						where mpartnerproduct_partner_gid=@Partner_Gid) into @pp_MAP;
                           # select @pp_MAP;
	#if @pp_MAP=0 then
		#set Message = 'SUCCESS';
		#leave sp_Atma_Pending_To_Approval_Activitydtlpproduct_Set;
    #end if;
	if @pp_MAP=1 then
    SET finished =0;

	BEGIN

		Declare Cursor_atma CURSOR FOR
				select mpartnerproduct_gid,mpartnerproduct_partner_gid,mpartnerproduct_partnerbranch_gid,
                mpartnerproduct_product_gid,mpartnerproduct_unitprice,mpartnerproduct_packingprice,
				mpartnerproduct_validfrom,mpartnerproduct_validto,mpartnerproduct_deliverydays,mpartnerproduct_capacitypw,mpartnerproduct_dts,
				mpartnerproduct_status,mpartnerproduct_isactive,mpartnerproduct_isremoved,entity_gid,create_by,main_mpartnerproduct_gid
				from  atma_tmp_map_tpartnerproduct
				where mpartnerproduct_partner_gid=@Partner_Gid and mpartnerproduct_partnerbranch_gid=Oldpartnerbranchgid ;

		DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;

		OPEN Cursor_atma;
		atma_looop:loop
			fetch Cursor_atma into m_mpartnerproduct_gid,m_mpartnerproduct_partner_gid,m_mpartnerproduct_partnerbranch_gid,
            m_mpartnerproduct_product_gid,m_mpartnerproduct_unitprice,m_mpartnerproduct_packingprice,
			m_mpartnerproduct_validfrom,m_mpartnerproduct_validto,m_mpartnerproduct_deliverydays,m_mpartnerproduct_capacitypw,m_mpartnerproduct_dts,
			m_mpartnerproduct_status,m_mpartnerproduct_isactive,m_mpartnerproduct_isremoved,m_entity_gid,m_create_by,m_main_mpartnerproduct_gid ;

        #select concat('m_mpartnerproduct_partner_gid:',m_mpartnerproduct_partner_gid,'finished:',finished);
		if finished = 1 then
			leave atma_looop;
		End if;
                #select Oldpartnerbranchgid,Mst_Partner_Gid,Newpartnerbranchgid;
	if m_main_mpartnerproduct_gid = '' or m_main_mpartnerproduct_gid is null  or m_main_mpartnerproduct_gid=0 then
set Error_Level='ATMA48.1';
			set Query_Update = concat('INSERT INTO atma_map_tpartnerproduct (mpartnerproduct_partner_gid,
            mpartnerproduct_product_gid,mpartnerproduct_partnerbranch_gid,mpartnerproduct_unitprice,
			mpartnerproduct_packingprice,mpartnerproduct_validfrom,mpartnerproduct_validto,mpartnerproduct_deliverydays,mpartnerproduct_capacitypw,
			mpartnerproduct_dts,mpartnerproduct_status,mpartnerproduct_isactive,mpartnerproduct_isremoved,entity_gid,create_by)
            values (',Mst_Partner_Gid,',',m_mpartnerproduct_product_gid,',
            ',Newpartnerbranchgid,',
            ''',m_mpartnerproduct_unitprice,''',
            ''',m_mpartnerproduct_packingprice,''',''',m_mpartnerproduct_validfrom,''',''',m_mpartnerproduct_validto,''',
            ',m_mpartnerproduct_deliverydays,',',m_mpartnerproduct_capacitypw,',''',m_mpartnerproduct_dts,''',''',@mst_partner_status,''',
            ''',m_mpartnerproduct_isactive,''',''',m_mpartnerproduct_isremoved,''',',m_entity_gid,',
            ',m_create_by,')');


            SET SQL_SAFE_UPDATES = 0;
            set Query_delete=concat('DELETE FROM atma_tmp_map_tpartnerproduct WHERE mpartnerproduct_gid=',m_mpartnerproduct_gid,'');
			set @Insert_query = Query_delete;
			PREPARE stmt FROM @Insert_query;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;
			if countRow >  0 then
			set Message = 'DELETED';
			else
			set Message = ' FAILED DELETION';
			leave sp_Atma_Pending_To_Approval_Activitydtlpproduct_Set;
			end if;

	else
set Error_Level='ATMA48.2';
		 	set Query_Update = concat('Update atma_map_tpartnerproduct  set
            mpartnerproduct_product_gid=',m_mpartnerproduct_product_gid,',
            mpartnerproduct_unitprice=''',m_mpartnerproduct_unitprice,''',
            mpartnerproduct_packingprice=''',m_mpartnerproduct_packingprice,''',
            mpartnerproduct_validfrom=''',m_mpartnerproduct_validfrom,''',
            mpartnerproduct_validto=''',m_mpartnerproduct_validto,''',
            mpartnerproduct_deliverydays=''',m_mpartnerproduct_deliverydays,''',
            mpartnerproduct_capacitypw=''',m_mpartnerproduct_capacitypw,''',
            mpartnerproduct_dts=''',m_mpartnerproduct_dts,''',
            mpartnerproduct_status=''',@mst_partner_status,''',
            mpartnerproduct_isactive=''',m_mpartnerproduct_isactive,''',
            mpartnerproduct_isremoved=''',m_mpartnerproduct_isremoved,''',
			update_by=',@Update_By,',update_date=''',now(),'''
			where mpartnerproduct_gid=',m_main_mpartnerproduct_gid,'');

           #select Query_Update;
			SET SQL_SAFE_UPDATES = 0;
			set Query_delete=concat('DELETE FROM atma_tmp_map_tpartnerproduct WHERE mpartnerproduct_gid=',m_mpartnerproduct_gid,'');
			set @Insert_query = Query_delete;
			PREPARE stmt FROM @Insert_query;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;
			if countRow >  0 then
			set Message = 'DELETED';
			else
			set Message = ' FAILED DELETION';
			leave sp_Atma_Pending_To_Approval_Activitydtlpproduct_Set;
			end if;


	end if;
			select Query_Update;
			set @Insert_query = Query_Update;
			PREPARE stmt FROM @Insert_query;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;
			if countRow >  0 then
			set Message = 'SUCCESS';
            #select Message;
            #rollback;##remove
			else
			set Message = ' FAILED pp';
            #select Message;
			leave sp_Atma_Pending_To_Approval_Activitydtlpproduct_Set;
			end if;

            set  @Mst_partnerproduct='';
			select last_insert_id() into @Mst_partnerproduct;



	SET finished1 =0;

BEGIN
	Declare Cursor_atma1 CURSOR FOR

								select activitydtlpproduct_gid,activitydtlpproduct_activitydetailsgid,activitydtlpproduct_mpartnerproductgid,activitydtlpproduct_category,
								activitydtlpproduct_subcategory,activitydtlpproduct_name,activitydtlpproduct_spec,activitydtlpproduct_size,activitydtlpproduct_remarks,
								activitydtlpproduct_uomgid,activitydtlpproduct_rate,activitydtlpproduct_validfrom,activitydtlpproduct_validto,activitydtlpproduct_isactive,
								activitydtlpproduct_isremoved,entity_gid,create_by,main_activitydtlpproduct_gid
								from  atma_tmp_map_tactivitydtlpproduct
								where activitydtlpproduct_activitydetailsgid=Activitydetail_old_gid ;
                                # and activitydtlpproduct_mpartnerproductgid=m_mpartnerproduct_gid ;

	DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished1 = 1;
	OPEN Cursor_atma1;
	atma_looop1:loop
		fetch Cursor_atma1 into cat_activitydtlpproduct_gid,cat_activitydtlpproduct_activitydetailsgid,cat_activitydtlpproduct_mpartnerproductgid,cat_activitydtlpproduct_category,
			cat_activitydtlpproduct_subcategory,cat_activitydtlpproduct_name,cat_activitydtlpproduct_spec,cat_activitydtlpproduct_size,cat_activitydtlpproduct_remarks,
			cat_activitydtlpproduct_uomgid,cat_activitydtlpproduct_rate,cat_activitydtlpproduct_validfrom,cat_activitydtlpproduct_validto,cat_activitydtlpproduct_isactive,
			cat_activitydtlpproduct_isremoved,cat_entity_gid,cat_create_by,cat_main_activitydtlpproduct_gid ;
	# select concat('m_mpartnerproduct_gid:',m_mpartnerproduct_gid,'finished1:',finished1);
     if finished1 = 1 then
			leave atma_looop1;
		End if;
	if cat_main_activitydtlpproduct_gid = '' or cat_main_activitydtlpproduct_gid is null  or cat_main_activitydtlpproduct_gid=0 then

				set Query_Column='';
				set Query_Value ='';

				if cat_activitydtlpproduct_spec is not null then
					set Query_Column = concat(Query_Column,',activitydtlpproduct_spec ');
					set Query_Value=concat(Query_Value,', ''',cat_activitydtlpproduct_spec,''' ');
				else
					set Query_Column = concat('');
					set Query_Value=concat('');
				end if;


				if cat_activitydtlpproduct_size is not null then
					set Query_Column = concat(Query_Column,',activitydtlpproduct_size ');
					set Query_Value=concat(Query_Value,', ''',cat_activitydtlpproduct_size,''' ');
				else
					set Query_Column = concat('');
					set Query_Value=concat('');
				end if;

				if cat_activitydtlpproduct_remarks is not null then
					set Query_Column = concat(Query_Column,',activitydtlpproduct_remarks ');
					set Query_Value=concat(Query_Value,', ''',cat_activitydtlpproduct_remarks,''' ');
				else
					set Query_Column = concat('');
					set Query_Value=concat('');
				end if;

set Error_Level='ATMA48.3';
			set Query_Update = concat('INSERT INTO atma_map_tactivitydtlpproduct (activitydtlpproduct_activitydetailsgid,activitydtlpproduct_mpartnerproductgid,activitydtlpproduct_category,
			activitydtlpproduct_subcategory,activitydtlpproduct_name,activitydtlpproduct_uomgid,activitydtlpproduct_rate,activitydtlpproduct_validfrom,
			activitydtlpproduct_validto,activitydtlpproduct_isactive,activitydtlpproduct_isremoved,entity_gid,create_by ',Query_Column,')
            values (',Mst_activitydetails,',',@Mst_partnerproduct,',',cat_activitydtlpproduct_category,',
            ',cat_activitydtlpproduct_subcategory,',''',cat_activitydtlpproduct_name,''',',cat_activitydtlpproduct_uomgid,',''',cat_activitydtlpproduct_rate,''',
            ''',cat_activitydtlpproduct_validfrom,''',''',cat_activitydtlpproduct_validto,''',
            ''',cat_activitydtlpproduct_isactive,''',''',cat_activitydtlpproduct_isremoved,''',',cat_entity_gid,',
            ',cat_create_by,'',Query_Value,')');




            SET SQL_SAFE_UPDATES = 0;
			set Query_delete=concat('DELETE FROM atma_tmp_map_tactivitydtlpproduct WHERE activitydtlpproduct_gid=',cat_activitydtlpproduct_gid,'');
			set @Insert_query = Query_delete;
			PREPARE stmt FROM @Insert_query;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;
			if countRow >  0 then
			set Message = 'DELETED';
			else
			set Message = ' FAILED DELETION';
			leave sp_Atma_Pending_To_Approval_Activitydtlpproduct_Set;
			end if;

	else

        /*
        activitydtlpproduct_activitydetailsgid=',cat_activitydtlpproduct_activitydetailsgid,',
            activitydtlpproduct_mpartnerproductgid=''',cat_activitydtlpproduct_mpartnerproductgid,''',*/
set Error_Level='ATMA48.4';
		 	set Query_Update = concat('Update atma_map_tactivitydtlpproduct  set

            activitydtlpproduct_category=''',cat_activitydtlpproduct_category,''',
            activitydtlpproduct_subcategory=',cat_activitydtlpproduct_subcategory,',
            activitydtlpproduct_name=''',cat_activitydtlpproduct_name,''',
            activitydtlpproduct_spec=''',ifnull(cat_activitydtlpproduct_spec,''),''',
            activitydtlpproduct_size=''',ifnull(cat_activitydtlpproduct_size,''),''',
            activitydtlpproduct_remarks=''',ifnull(cat_activitydtlpproduct_remarks,''),''',
            activitydtlpproduct_uomgid=''',cat_activitydtlpproduct_uomgid,''',
            activitydtlpproduct_rate=''',cat_activitydtlpproduct_rate,''',
            activitydtlpproduct_validfrom=''',cat_activitydtlpproduct_validfrom,''',
            activitydtlpproduct_validto=''',cat_activitydtlpproduct_validto,''',
			update_by=',@Update_By,',update_date=''',now(),'''
			where activitydtlpproduct_gid=',cat_main_activitydtlpproduct_gid,'');

           select Query_Update;
           SET SQL_SAFE_UPDATES = 0;
			set Query_delete=concat('DELETE FROM atma_tmp_map_tactivitydtlpproduct WHERE activitydtlpproduct_gid=',cat_activitydtlpproduct_gid,'');
			set @Insert_query = Query_delete;
			PREPARE stmt FROM @Insert_query;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;
			if countRow >  0 then
			set Message = 'DELETED';
			else
			set Message = ' FAILED DELETION';
			leave sp_Atma_Pending_To_Approval_Activitydtlpproduct_Set;
			end if;

	end if;
       select Query_Update;
		set @Insert_query = Query_Update;
		PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt;
		if countRow >  0 then
			set Message = 'SUCCESS';
           # rollback; ##remove#select Message;
		else
			set Message = ' FAILED cat';
            #select Message;
			leave sp_Atma_Pending_To_Approval_Activitydtlpproduct_Set;
		end if;
      ######new####


        #####new#####


	End loop atma_looop1;
	close Cursor_atma1;
	end;  #Endof Cursor

End loop atma_looop;
close Cursor_atma;
#-------------------
end;  #Endof Cursor
end if; ###@pp_MAP
End if;

END