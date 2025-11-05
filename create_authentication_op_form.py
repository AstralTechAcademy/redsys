import base64
from Crypto.Cipher import DES3
from Crypto.Hash import HMAC, SHA256

merchant_key = b'<YOUR_REDSYS_MERCHANT_KEY>'
merchant_code = "<YOUR_MERCHANT_CODE>"

clave_bin = base64.b64decode(clave_comercio_base64)

ds_order_str = "00014888y744"  # Ds_Order
ds_order = ds_order_str

while len(ds_order) % 8 != 0:
    ds_order += '\0'
ds_order = ds_order.encode("utf-8")

iv = bytes(8)

# DES3 requires 24 bytes so append more bytes until 24
if len(clave_bin) == 16:
    clave_bin = clave_bin + clave_bin[:8]

cipher = DES3.new(clave_bin, DES3.MODE_CBC, iv)
clave_firma = cipher.encrypt(ds_order)

# TRANSACTIONTYPE = 7 means Authentication
op = f"""{{
    "DS_MERCHANT_ORDER": "{ds_order_str}",
    "DS_MERCHANT_MERCHANTCODE": "{merchant_code}",
    "DS_MERCHANT_TERMINAL": "1",
    "DS_MERCHANT_CURRENCY": "978",
    "DS_MERCHANT_TRANSACTIONTYPE": "7",
    "DS_MERCHANT_AMOUNT": "249",
    "DS_MERCHANT_MERCHANTURL": "http://www.prueba.com/urlNotificacion.php",
    "DS_MERCHANT_URLOK": "http://www.prueba.com/urlOK.php",
    "DS_MERCHANT_URLKO": "http://www.prueba.com/urlKO.php"
}}"""

message = base64.b64encode(op.replace('\n', '').encode("utf-8")).decode("utf-8") 

# Create HMAC-SHA512 hash
h = HMAC.new(clave_firma, message.encode("utf-8"), SHA256)
firma = base64.b64encode(h.digest()).decode("utf-8")

print(f'Ds_MerchantParameters: {message}')
print(f'DS_Signature: {firma}')
