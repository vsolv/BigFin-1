CREATE  FUNCTION  `fn_FA_Data`( ls_Type varchar(64),Reftable_Gid int,
Reftable_Value varchar(64),Entity_Gid int,lj_data json) RETURNS varchar(15000) CHARSET utf8
BEGIN
### Ramesh Oct 3 2019
### Used to Get The Common Data in FA

Declare Out_Message varchar(16000);
Declare i varchar(1600);
Declare ls_count varchar(1600);

if ls_Type = 'PRODUCT_ASSETCAT' then
		if Reftable_Gid is null or Reftable_Gid = 0 or Reftable_Gid = '' then
			set Out_Message = 0 ;
        End if;
        ### Asset Cat Gid

                                select ifnull(a.assetcat_gid,0) into Out_Message
								from fa_mst_tassetcat as a
								inner join ap_mst_tsubcategory as b on b.subcategory_gid = a.assetcat_subcategorygid
								inner join ap_mst_tcategory as c on c.category_gid = b.subcategory_categorygid
								inner join gal_mst_tproduct as d on d.product_category_gid = c.category_gid and d.product_subcategory_gid = b.subcategory_gid
								where d.product_gid = Reftable_Gid
								and a.assetcat_isactive = 'Y' and a.assetcat_isremoved = 'N'
								and a.entity_gid = Entity_Gid
								and b.subcategory_isactive = 'Y' and b.subcategory_isremoved = 'N'
								and c.category_isactive = 'Y' and c.category_isremoved = 'N'
								and d.product_isactive = 'Y' and d.product_isremoved = 'N'
                                limit 1
                                ;

                                if Out_Message = 0 or @Out_Message = '' or Out_Message is null then
									set Out_Message = 0 ;
                                End if;


 ELSEIF ls_Type = 'ASSET_CLUB_CHECK' then

					select JSON_LENGTH(lj_data,CONCAT('$.ASSET[0].Asset_Gid')) into @Asset_Gid_Count;
                    select JSON_UNQUOTE(JSON_EXTRACT(lj_data, CONCAT('$.ASSET[0].Asset_Gid'))) into @Asset_Check_Gids;
					set @Asset_Check_Gids=REPLACE(REPLACE(substr(@Asset_Check_Gids,2,length(@Asset_Check_Gids)-2),'"',""),' ','');




                 select exists(select group_concat(assetdetails_parentgid) from fa_trn_tassetdetails where
						 assetdetails_gid in (@Asset_Check_Gids) and assetdetails_isactive='Y'
                        and assetdetails_isremoved='N' and entity_gid=Entity_Gid) INTO @Test;

                        #set Out_Message =concat(@Test);


				 	if @Test=1 then

					SELECT group_concat(assetdetails_parentgid) from fa_trn_tassetdetails
						where assetdetails_parentgid<>0 and  assetdetails_isactive='Y'
							and assetdetails_isremoved='N' and entity_gid=Entity_Gid
							and assetdetails_gid in (@Asset_Check_Gids)  INTO @Asset_Parent_Gids;

					SELECT  group_concat(assetdetails_gid) from fa_trn_tassetdetails
						where  assetdetails_isactive='Y'
							and assetdetails_isremoved='N' and entity_gid=Entity_Gid
							and assetdetails_parentgid in (@Asset_Parent_Gids)  INTO @Asset_Club_Gids;

					SELECT  count(assetdetails_gid) from fa_trn_tassetdetails
						where  assetdetails_isactive='Y'
							and assetdetails_isremoved='N' and entity_gid=Entity_Gid
							and assetdetails_parentgid in (@Asset_Parent_Gids)  INTO @Asset_Check_Count;

                        #set Out_Message =concat(@Asset_Club_Gids);


                      set @Asset_Club_Gid_count= LENGTH(@Asset_Club_Gids) - LENGTH(REPLACE(@Asset_Club_Gids, ',', '')) + 1;

						set @Asset_Club_Gids= concat( '[', @Asset_Club_Gids,']') ;

                        #set Out_Message = '';

							set i = 1 ;
                                Set ls_count=0;
								While i < @Asset_Club_Gid_count+1  DO


                                set @Asset_Club_Gids = substring_index(replace(replace(substring_index
											(@Asset_Club_Gids,',',i),'[',''),']','' ),',',-1)  ;

                                              #set Out_Message = @Asset_Club_Gids1;

                                            set @Test1 = FIND_IN_SET(@Asset_Club_Gids,@Asset_Check_Gids)  ;

														if @Test1<>0 then
															Set ls_count=ls_count+1;
														end if;

                                set i = i+1;
								End while;

                                if @Asset_Check_Count=ls_count then
										set Out_Message =concat('SUCCESS');
								else
										set Out_Message = 'FAIL';
								end if;


                     if @Asset_Club_Gids is null then
						set Out_Message = 'FAIL';
                     end if;

                    elseif @Test=0 then
						set Out_Message = 'SUCCESS';
                    end if;

 ELSEIF ls_Type = 'ASSET_MULTIUSER' then

      if Reftable_Gid = 0 or Reftable_Gid is null THEN
        set Out_Message = 0;
       RETURN Out_Message;
      End if;

      if Reftable_Value is null or Reftable_Value = '' THEN
       set Out_Message = 0 ;
       RETURN Out_Message;
      End if;

      set @Is_data_Process = 0;
     set @ref_gid_fn = 0 ;
     select ifnull(max(ref_gid),0) into @ref_gid_fn from gal_mst_tref where ref_name = Reftable_Value ;

     if @ref_gid_fn = 0 then
      set Out_Message = 'ERROR';
      RETURN Out_Message;
     End if;

      Select ifnull(count(a.tran_gid),0) into @Is_data_Process from gal_trn_ttran as a
		where a.tran_ref_gid = @ref_gid_fn
		and a.tran_reftable_gid = Reftable_Gid
		and a.tran_by is null
		and a.tran_date is null
		and a.tran_isactive = 'Y' and a.tran_isremoved = 'N'
		;

	   if @Is_data_Process = 1 then
	    set Out_Message = 'SUCCESS';
	    RETURN Out_Message;
	   elseif @Is_data_Process = 0 then
	     set Out_Message = 'FAIL';
   	    RETURN Out_Message;
	   End if;
  ELSEIF ls_Type = 'ASSET_REQUEST_CHECK' then

     if Reftable_Gid = 0 or Reftable_Gid is null THEN
        set Out_Message = 0;
       RETURN Out_Message;
      End if;

     set @Is_data_Process = 0;
     select ifnull(count(assetdetails_gid),0) into @Is_data_Process from fa_trn_tassetdetails as a
     where assetdetails_gid = Reftable_Gid
     and assetdetails_requestfor = '' and assetdetails_isactive = 'Y'
     and assetdetails_isremoved ='N' and a.entity_gid = Entity_Gid;


     if @Is_data_Process = 1 then
	    set Out_Message = 'SUCCESS';
	    RETURN Out_Message;
	  elseif @Is_data_Process = 0 then
	     set Out_Message = 'FAIL';
   	    RETURN Out_Message;
	  End if;

ELSEIF ls_Type = 'ASSET_TRAN_COMPLETED' then
              #### Used to Show the Rejected Remarks with Employee
               if Reftable_Gid = 0 or Reftable_Gid is null THEN
                 set Out_Message = 0;
                 RETURN Out_Message;
               End if;

                if Reftable_Value is null or Reftable_Value = '' THEN
			       set Out_Message = 0 ;
			       RETURN Out_Message;
      			End if;

     			set @ref_gid_fn = 0 ;
     			select ifnull(max(ref_gid),0) into @ref_gid_fn from gal_mst_tref where ref_name = Reftable_Value ;

			     if @ref_gid_fn = 0 then
			      set Out_Message = 'ERROR';
			      RETURN Out_Message;
			     End if;

		    set @datas = "";
			set @lj_Tran_RejectRemark = ifnull((select concat('[', json_object('checker_remarks',a.tran_remarks,'Rejected_By',b.employee_name,'Employee_Code',b.employee_code
                   ) ,']') as a
               from gal_trn_ttran as a
                             left join gal_mst_temployee as b on b.employee_gid  = a.tran_from
                             where a.tran_ref_gid = @ref_gid_fn and a.tran_reftable_gid = Reftable_Gid and a.tran_totype = 'C'
                             and a.tran_isactive = 'Y' and a.tran_isremoved = 'N'
                             and b.employee_isremoved = 'N'
                             and a.entity_gid = Entity_Gid
                             order by a.tran_gid desc
                             limit 1),(select concat('[',json_object('checker_remarks',@datas),']')));
			set Out_Message = @lj_Tran_RejectRemark;

   else
        set Out_Message = 0 ;
End if;



#set Out_Message = @ref_value;
RETURN Out_Message;
END