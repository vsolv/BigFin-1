CREATE DEFINER=`developer`@`%` PROCEDURE `sp_IntegrityProcess_Get`(in ls_Type  varchar(25),
IN ls_Sub_Type varchar(25),
in lj_filter json,
in lj_classification json,
out Message varchar(1000))
sp_IntegrityProcess_Get:BEGIN
Declare Query_Select varchar(50000);
Declare errno int;
Declare msg varchar(1000	);
Declare countRow varchar(5000);
Declare ls_count int;

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
		leave sp_IntegrityProcess_Get;
End if;

if ls_Type= 'SOURCE' then

	set Query_Select = '';


set Query_Select =concat('select * from rec_trn_tintsource as a where a.entity_gid in (',@Entity_Gids,')');
	 #select Query_Select;
	 set @p = Query_Select;

     PREPARE stmt FROM @p;
	 EXECUTE stmt;
	 Select found_rows() into ls_count;
	 DEALLOCATE PREPARE stmt;
	if ls_count > 0 then
		 set Message = 'FOUND';
	else
		 set Message = 'NOT_FOUND';
	end if;

END IF;

if ls_Type='DESTINATION' then

	set Query_Select = '';

	set Query_Select =concat('select * from rec_trn_tintdestination as a where a.entity_gid in (',@Entity_Gids,')');
	 #select Query_Select;
	 set @p = Query_Select;

     PREPARE stmt FROM @p;
	 EXECUTE stmt;
	 Select found_rows() into ls_count;
	 DEALLOCATE PREPARE stmt;
	if ls_count > 0 then
		 set Message = 'FOUND';
	else
		 set Message = 'NOT_FOUND';
	end if;

END IF;


if ls_Type='FILE_GET' then

	set Query_Select = '';

	set Query_Select =concat('select * from gal_mst_tfile as a where a.entity_gid in (',@Entity_Gids,')');
	 #select Query_Select;
	 set @p = Query_Select;

     PREPARE stmt FROM @p;
	 EXECUTE stmt;
	 Select found_rows() into ls_count;
	 DEALLOCATE PREPARE stmt;
	if ls_count > 0 then
		 set Message = 'FOUND';
	else
		 set Message = 'NOT_FOUND';
	end if;

END IF;

if ls_Type='TEMPLATE_GET' then

	set Query_Select = '';

	set Query_Select =concat('select * from gal_mst_ttemplateheader as a where a.entity_gid in (',@Entity_Gids,')');
	 #select Query_Select;
	 set @p = Query_Select;

     PREPARE stmt FROM @p;
	 EXECUTE stmt;
	 Select found_rows() into ls_count;
	 DEALLOCATE PREPARE stmt;
	if ls_count > 0 then
		 set Message = 'FOUND';
	else
		 set Message = 'NOT_FOUND';
	end if;

END IF;

END