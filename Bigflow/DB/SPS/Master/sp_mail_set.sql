CREATE DEFINER=`developer`@`%` PROCEDURE `sp_Mail_Set`(in `Action` varchar(32),in `lj_Mail` json,in `lj_Classification` json,in `Create_by` int,
out `Message` varchar(1000))
sp_Mail_Set:BEGIN
declare Query_Insert varchar(1000);
declare errno int;
declare msg varchar(1000);
declare countRow int;
   #Santhosh 24-01-2020
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
    
     select JSON_LENGTH(lj_Classification,'$') into @li_json_count;
     
        if @li_json_count is null or @li_json_count = 0 then
			set Message = 'No Data In Json - Classification.';
            rollback;
			leave sp_Mail_Set;
        end if; 
        
        if Create_by = 0 or Create_by is null then
			set Message ='Create by Not Came';
		end if;
        select  JSON_UNQUOTE(JSON_EXTRACT(lj_Classification, CONCAT('$.Entity_Gid[0]'))) into @Entity_gid; 
       
          SET autocommit = 0; 
start transaction; 
    
  select JSON_LENGTH(lj_Mail,'$') into @li_json_count;
     
        if @li_json_count is null or @li_json_count = 0 then
			set Message = 'No Data In Json - Mail.';
            rollback;
			leave sp_Mail_Set;
        end if;        
 if Action = 'Insert' then
 
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_Mail, CONCAT('$.MailTemplate_Gid[0]'))) into @Mailtemplate_gid; 
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_Mail, CONCAT('$.Mail_From[0]'))) into @Mail_from; 
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_Mail, CONCAT('$.Mail_To[0]'))) into @Mail_to; 
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_Mail, CONCAT('$.Mail_Cc[0]'))) into @Mail_cc;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_Mail, CONCAT('$.Mail_Subject[0]'))) into @Mail_subject;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_Mail, CONCAT('$.Mail_Body[0]'))) into @Mail_body;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_Mail, CONCAT('$.Mail_Date[0]'))) into @Mail_date;
		select  JSON_UNQUOTE(JSON_EXTRACT(lj_Mail, CONCAT('$.Mail_Status[0]'))) into @Mail_status;
        #select @Mailtemplate_gid,@Mail_from,@Mail_to,@Mail_cc, @Mail_subject,@Mail_body,@Mail_date,@Mail_status;
        if @Mailtemplate_gid = 0 or @Mailtemplate_gid is null then
           set Message= 'Mailtemplate gid Not Given';
        end if;
        if @Mail_from = '' or @Mail_from is null then
			set Message = 'Mail From Not Given';
		end if;
		if @Mail_to = '' or @Mail_to is null then
			set Message = 'Mail To Not Given';
        end if;
		if  @Mail_subject = '' or  @Mail_subject is null then
			set Message = 'Mail Subject Not Given';
        end if;
       if @Mail_body = '' or @Mail_body is null then
			set Message = 'Mail Body Not Given';
        end if;
       if @Mail_date = '' or @Mail_date is null then
			set Message = 'Mail date Not Given';
        end if;
     
        set Query_Insert = concat('Insert into gal_trn_tmail(mail_templategid, mail_from, mail_to, mail_cc,
        mail_subject, mail_body, mail_date, mail_status,entity_gid, create_by)
		values(', @Mailtemplate_gid,',''',@Mail_from,''',''',@Mail_to,''',''',@Mail_cc,''',
        ''',@Mail_subject,''',''',@Mail_body,''',''',@Mail_date,''',''',@Mail_status,''',',@Entity_gid,',',Create_by,')');
  
		
        set @Insert_query = Query_Insert;
        #SELECT  @Insert_query;
        PREPARE stmt FROM @Insert_query;
		EXECUTE stmt;  
		set countRow = (select ROW_COUNT());
		DEALLOCATE PREPARE stmt; 		
        
              
		if countRow >  0 then
			set Message = 'SUCCESS';
			commit;
		else
			set Message = 'FAIL';
			rollback;
		end if;
 end if;
 
END