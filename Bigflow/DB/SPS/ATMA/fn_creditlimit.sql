CREATE  FUNCTION `fn_creditlimit`(creditlimit varchar(64)) RETURNS int(11)
BEGIN

declare out_message varchar(64);
set out_message = '';
set @creditlimitgid='';
#set @REF_Gid = 0;
if creditlimit <> '' then

		select creditlimit_gid into @creditlimitgid from gal_trn_tcreditlimit
        where creditlimit_reftable_code=creditlimit;
     set out_message =@creditlimitgid;
End if;


RETURN out_message;
END