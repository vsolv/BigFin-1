CREATE DEFINER=`developer`@`%` PROCEDURE `sp_FALocation_Get`(IN `ls_Type` varchar(64),IN `ls_Sub_Type` varchar(64),
IN `lj_Filters` json,IN `lj_Classification` json,
OUT `Message` varchar(1024))
sp_FALocation_Get:BEGIN
### Ramesh Oct 15 2019
### wip TO DO
Declare Query_Select varchar(6144);
Declare Query_Search varchar(1024);
declare errno int;
declare msg varchar(1000);
declare li_count int;

	DECLARE EXIT HANDLER FOR SQLEXCEPTION,sqlwarning
    BEGIN

    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
    set Message = concat(errno , msg);
    ROLLBACK;
    END;

select fn_Classification('ENTITY_ONLY',lj_Classification) into @OutMsg_Classification ;
        select  JSON_UNQUOTE(JSON_EXTRACT(@OutMsg_Classification, '$.Entity_Gid[0]')) into @Entity_Gids;
        if @Entity_Gids is  null or @Entity_Gids = '' then
				select  JSON_UNQUOTE(JSON_EXTRACT(@OutMsg_Classification, '$.Message')) into @Message;
				set Message = concat('Error On Classification Data - ',@Message);
                leave sp_FALocation_Get;
        End if;

if ls_Type = 'FA_LOCATION' and ls_Sub_Type = 'DDL' then
						set Query_Select = '';
            set Query_Search = '';
            select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Reftable_Gid'))) into @Reftable_Gid;
            select  JSON_UNQUOTE(JSON_EXTRACT(lj_Filters, CONCAT('$.Ref_Name'))) into @Ref_Name;

			set Query_Select = concat('
							Select a.assetlocation_gid,a.assetlocation_name,a.assetlocation_floor,ifnull(a.assetlocation_remarks,'''') as remarks
								from fa_mst_tassetloaction as a
								where a.assetlocation_refgid = 67 and a.assetlocation_reftablegid = ',@Reftable_Gid,'
								and a.assetlocation_isactive = ''Y'' and a.assetlocation_isremoved = ''N''
                            ',Query_Search,' and a.entity_gid in (',@Entity_Gids,')
							');
                     	set @Query_Select = Query_Select;
			      		#select @Query_Select; ### Remove It
								PREPARE stmt FROM @Query_Select;
								EXECUTE stmt;
								Select found_rows() into li_count;
                                DEALLOCATE PREPARE stmt;

							  if li_count > 0 then
									set Message = 'FOUND';
							  else
									set Message = 'NOT_FOUND';
							  end if;
End if;


END