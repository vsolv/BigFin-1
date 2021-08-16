CREATE  FUNCTION `fn_bankdetails`(bankdetails varchar(64)) RETURNS int(11)
BEGIN

declare out_message varchar(64);
set out_message = '';
set @bankdetailsgid='';
#set @REF_Gid = 0;
if bankdetails <> '' then

        select bankdetails_gid into @bankdetailsgid from gal_trn_tbankdetails
        where bankdetails_reftable_code=bankdetails ;
     set out_message =@bankdetailsgid;
End if;


RETURN out_message;
END