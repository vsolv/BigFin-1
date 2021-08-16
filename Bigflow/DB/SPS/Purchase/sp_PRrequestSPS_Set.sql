CREATE DEFINER=`developer`@`%` PROCEDURE `sp_PRrequestSPS_Set`(in `Action` varchar(64),in `Type` varchar(64),
in `lj_Header` json,in `lj_Details` json,in `lj_Status` json,IN `lj_Classification` json, in `li_create_by` int,
 out `Message` varchar(10000)
)
sp_PRrequestSPS_Set:BEGIN

declare errno int;
declare msg varchar(1000);
declare lj_inv_details json;

	DECLARE EXIT HANDLER FOR SQLEXCEPTION,sqlwarning
    BEGIN
    
    GET CURRENT DIAGNOSTICS CONDITION 1 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
    set Message = concat(errno , msg);
    ROLLBACK;
    END;   

SET autocommit = 0; 
start transaction;


if Action = 'Insert' then

		  select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid[0]'))) into @Entity_Gid;
             
             if @Entity_Gid is  null or @Entity_Gid = 0 or @Entity_Gid = '' then
					set Message = 'Entity Gid Is Needed.';
                    leave sp_PRrequestSPS_Set;
             End if;
		
			call sp_PRrequest_Set('INSERT',Type,lj_Header,lj_Details,'{}',lj_Status,li_create_by,lj_Classification,@Message);
			select @Message into @Out_Message_InvDebit;
				select  @Message;
					if @Message <> 'SUCCESS' or @Message is null then
						set Message = 'Error While Insert';
						rollback;
						leave sp_PRrequestSPS_Set;
					else
						set Message = 'SUCCESS';
                         commit;
					End if;

elseif Action = 'Update' then	
				
						
			select JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid[0]'))) into @Entity_Gid;
             
             if @Entity_Gid is  null or @Entity_Gid = 0 or @Entity_Gid = '' then
					set Message = 'Entity Gid Is Needed.';
                    leave sp_PRrequestSPS_Set;
             End if;
		select Type;
			call sp_PRrequest_Set('INSERT',Type,lj_Header,lj_Details,'{}',lj_Status,li_create_by,lj_Classification,@Message);
			select @Message into @Out_Message_InvDebit;
					#select @Message;
                    if @Message <> 'SUCCESS' then
						set Message = 'Error While Insert';
						rollback;
						leave sp_PRrequestSPS_Set;
					else
						set Message = 'SUCCESS';
                         commit;
					End if;
						


End if; ### If of Action and Type
   

END