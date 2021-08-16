CREATE  FUNCTION `fn_supplier`(supplier varchar(64)) RETURNS int(11)
BEGIN

declare out_message varchar(64);
set out_message = '';
set @suppliergid='';
#set @REF_Gid = 0;
if supplier <> '' then
			select supplier_gid into @suppliergid  from gal_mst_tsupplier where supplier_code=supplier;



     set out_message =@suppliergid;
End if;


RETURN out_message;
END