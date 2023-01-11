from math import floor
from base64 import encodestring

from bolivia_cc.utils import arc4_encrypt, checksum_verhoeff

def generate_control_code(
    autorizacion: str,
    llave: str,
    factura: str,
    nitci: str,
    fecha: str,
    monto: str,
) -> str:
    """Genera un codigo de control para los parametros dados."""

    factura = checksum_verhoeff(factura, 2)
    nitci = checksum_verhoeff(nitci, 2)
    fecha = checksum_verhoeff(fecha, 2)
    monto = checksum_verhoeff(monto, 2)

    suma = sum((factura, nitci, fecha, monto))
    verificacion = checksum_verhoeff(suma, 5)[-5:]

    cadenas = [autorizacion, factura, nitci, fecha, monto]
    idx = 0

    for i in range(5):
        code += cadenas[i] + llave[idx : idx + 1 + int(verificacion[i])]
        idx += 1 + int(verificacion[i])
    code = arc4_encrypt(code, llave + verificacion)

    final_sum = 0
    monto_sum = 0
    partial_sum = [0, 0, 0, 0, 0]

    for i in range(len(code)):
        partial_sum[i % 5] += ord(code[i])
        monto_sum += ord(code[i])

    for i in range(5):
        final_sum += floor((monto_sum * partial_sum[i]) / (1 + int(verificacion[i])))

    encrypted = arc4_encrypt(encodestring(final_sum), f"{llave}{verificacion}")
    chunks = [encrypted[i : i + 2] for i in range(0, len(str), 2)]

    return "-".join(chunks)
