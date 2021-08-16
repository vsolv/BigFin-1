CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Atma_Pending_To_Approval_mpartnerproduct_Set`(in li_Action  varchar(30),
in lj_filter json,in lj_classification json,out Message varchar(1000))
sp_Atma_Pending_To_Approval_mpartnerproduct_Set:BEGIN
declare Query_Insert varchar(10000);
Declare countRow varchar(6000);
declare Query_Update varchar(10000);
declare Query_delete varchar(1000);
declare Query_Value varchar(1000);
declare Query_Column varchar(1000);
Declare m_mpartnerproduct_gid,m_mpartnerproduct_partner_gid,m_mpartnerproduct_partnerbranch_gid,m_mpartnerproduct_product_gid,m_mpartnerproduct_unitprice,m_mpartnerproduct_packingprice,
m_mpartnerproduct_validfrom,m_mpartnerproduct_validto,m_mpartnerproduct_deliverydays,m_mpartnerproduct_capacitypw,m_mpartnerproduct_dts,
m_mpartnerproduct_status,m_mpartnerproduct_isactive,m_mpartnerproduct_isremoved,m_entity_gid,m_create_by,m_update_by,
m_main_mpartnerproduct_gid  varchar(150);

DECLARE finished INTEGER DEFAULT 0;

Declare errno int;
Declare msg varchar(1000);

						DECLARE EXIT HANDLER FOR SQLEXCEPTION
						BEGIN
							GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
							set Message = concat(errno,msg,'APP_MPARTNERPRODUCT_SP');
							ROLLBACK;
						END;

IF li_Action='Insert' then

	START TRANSACTION;

	select JSON_LENGTH(lj_filter,'$') into @lj_filter_json_count;
	select JSON_LENGTH(lj_classification,'$') into @lj_classification_json_count;

	if @lj_filter_json_count = 0 or @lj_filter_json_count is null then
		set Message = 'No Data In filter Json. ';
		leave sp_Atma_Pending_To_Approval_mpartnerproduct_Set;
	End if;

	select JSON_UNQUOTE(JSON_EXTRACT(lj_filter,CONCAT('$.Partner_Gid')))
	into @Partner_Gid;

	if @Partner_Gid = '' or @Partner_Gid is null  or @Partner_Gid=0 then
			set Message = 'Partner Is Not Provided';
			leave sp_Atma_Pending_To_Approval_mpartnerproduct_Set;
	End if;

	#set @Main_partner_gid=4;
      #SET finished =0;

     SELECT EXISTS(
         select true from atma_tmp_map_tactivitydtlpproduct as madp
						inner join  atma_tmp_map_tpartnerproduct as mpp on
                        madp.activitydtlpproduct_mpartnerproductgid=mpp.mpartnerproduct_gid
						where mpp.mpartnerproduct_partner_gid=@Partner_Gid) into @pp_MAP;
                           # select @pp_MAP;
	if @pp_MAP=1 then
   SET finished =0;

	BEGIN

		Declare Cursor_atma CURSOR FOR

								select mpp.mpartnerproduct_gid,mpp.mpartnerproduct_partner_gid,
                                mpp.mpartnerproduct_partnerbranch_gid,
                                mpp.mpartnerproduct_product_gid,mpp.mpartnerproduct_unitprice,mpp.mpartnerproduct_packingprice,
								mpp.mpartnerproduct_validfrom,mpp.mpartnerproduct_validto,mpp.mpartnerproduct_deliverydays,mpp.mpartnerproduct_capacitypw,mpp.mpartnerproduct_dts,
								mpp.mpartnerproduct_status,mpp.mpartnerproduct_isactive,mpp.mpartnerproduct_isremoved,mpp.entity_gid,mpp.create_by,mpp.update_by,mpp.main_mpartnerproduct_gid
								from atma_tmp_map_tactivitydtlpproduct as madp
								inner join  atma_tmp_map_tpartnerproduct as mpp on madp.activitydtlpproduct_mpartnerproductgid=mpp.mpartnerproduct_gid
								where mpp.mpartnerproduct_partner_gid=@Partner_Gid;

		DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;


		OPEN Cursor_atma;
		atma_looop:loop
			fetch Cursor_atma into m_mpartnerproduct_gid,m_mpartnerproduct_partner_gid,
            m_mpartnerproduct_partnerbranch_gid,m_mpartnerproduct_product_gid,m_mpartnerproduct_unitprice,m_mpartnerproduct_packingprice,
			m_mpartnerproduct_validfrom,m_mpartnerproduct_validto,m_mpartnerproduct_deliverydays,m_mpartnerproduct_capacitypw,m_mpartnerproduct_dts,
			m_mpartnerproduct_status,m_mpartnerproduct_isactive,m_mpartnerproduct_isremoved,m_entity_gid,m_create_by,m_update_by,m_main_mpartnerproduct_gid ;

		if finished = 1 then
			leave atma_looop;
		End if;

	if m_main_mpartnerproduct_gid = '' or m_main_mpartnerproduct_gid is null  or m_main_mpartnerproduct_gid=0 then

			set Query_Update = concat('INSERT INTO atma_map_tpartnerproduct (mpartnerproduct_partner_gid,
            mpartnerproduct_partnerbranch_gid,mpartnerproduct_product_gid,mpartnerproduct_unitprice,
			mpartnerproduct_packingprice,mpartnerproduct_validfrom,mpartnerproduct_validto,mpartnerproduct_deliverydays,mpartnerproduct_capacitypw,
			mpartnerproduct_dts,mpartnerproduct_status,mpartnerproduct_isactive,mpartnerproduct_isremoved,entity_gid,create_by)
            values (',m_mpartnerproduct_partner_gid,',',m_mpartnerproduct_partnerbranch_gid,','
            ,m_mpartnerproduct_product_gid,',''',m_mpartnerproduct_unitprice,''',
            ''',m_mpartnerproduct_packingprice,''',''',m_mpartnerproduct_validfrom,''',''',m_mpartnerproduct_validto,''',
            ',m_mpartnerproduct_deliverydays,',',m_mpartnerproduct_capacitypw,',''',m_mpartnerproduct_dts,''',''',m_mpartnerproduct_status,''',
            ''',m_mpartnerproduct_isactive,''',''',m_mpartnerproduct_isremoved,''',',m_entity_gid,',
            ',m_create_by,')');
            /*
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
			rollback;
			end if;
           */
	else

		 	set Query_Update = concat('Update atma_map_tpartnerproduct  set
            mpartnerproduct_product_gid=',m_mpartnerproduct_product_gid,',
            mpartnerproduct_partnerbranch_gid=',m_mpartnerproduct_partnerbranch_gid,',
            mpartnerproduct_unitprice=''',m_mpartnerproduct_unitprice,''',
            mpartnerproduct_packingprice=''',m_mpartnerproduct_packingprice,''',
            mpartnerproduct_validfrom=''',m_mpartnerproduct_validfrom,''',
            mpartnerproduct_validto=''',m_mpartnerproduct_validto,''',
            mpartnerproduct_deliverydays=''',m_mpartnerproduct_deliverydays,''',
            mpartnerproduct_capacitypw=''',m_mpartnerproduct_capacitypw,''',
            mpartnerproduct_dts=''',m_mpartnerproduct_dts,''',
            mpartnerproduct_status=''',m_mpartnerproduct_status,''',
            mpartnerproduct_isactive=''',m_mpartnerproduct_isactive,''',
            mpartnerproduct_isremoved=''',m_mpartnerproduct_isremoved,''',
			update_by=',m_update_by,'
			where mpartnerproduct_gid=',m_main_mpartnerproduct_gid,'');

           /*SET SQL_SAFE_UPDATES = 0;
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
			rollback;
			end if;
          */

	end if;
			#select Query_Update;
			set @Insert_query = Query_Update;
			PREPARE stmt FROM @Insert_query;
			EXECUTE stmt;
			set countRow = (select ROW_COUNT());
			DEALLOCATE PREPARE stmt;
			if countRow >  0 then
			set Message = 'SUCCESS';
			else
			set Message = ' FAILED';
			#rollback;
			end if;
End loop atma_looop;
close Cursor_atma;

end;  #Endof Cursor
end if; ###@pp_MAP
end if;
END