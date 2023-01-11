from base64 import b64encode
from math import floor
from re import findall
from typing import Union

from bolivia_cc.utils import arc4_encrypt
from bolivia_cc.utils import base10to64
from bolivia_cc.utils import checksum_verhoeff


def generate_control_code(
    *,
    autorizacion: str,
    factura: str,
    nitci: str,
    fecha: str,
    monto: str,
    llave: str,
) -> str:
    """Genera un codigo de control para los parametros dados."""

    factura = checksum_verhoeff(factura, 2)
    nitci = checksum_verhoeff(nitci, 2)
    fecha = checksum_verhoeff(fecha, 2)

    monto = str(int(round(float(monto))))  # Strip decimals by round
    monto = checksum_verhoeff(monto, 2)

    suma: int = sum(map(int, [factura, nitci, fecha, monto]))

    verificacion = str(checksum_verhoeff(str(suma), 5))[-5:]
    largocadenas = [int(n) + 1 for n in verificacion]

    cadenas = list(map(str, [autorizacion, factura, nitci, fecha, monto]))
    cursor = 0

    for i, largo in enumerate(largocadenas):
        cadenas[i] = f"{cadenas[i]}{llave[cursor : cursor + largo]}"
        cursor = cursor + largo

    alleged_rc4 = arc4_encrypt("".join(cadenas), llave + verificacion)

    # Paso 4
    monto_sum = 0
    partial_sum = [0, 0, 0, 0, 0]

    for i in range(len(alleged_rc4)):
        partial_sum[i % 5] += ord(alleged_rc4[i])
        monto_sum += ord(alleged_rc4[i])

    # Paso 5
    final_sum = 0

    for i in range(5):
        final_sum += floor((monto_sum * partial_sum[i]) / (1 + int(verificacion[i])))

    encoded_final_sum = base10to64(final_sum)

    encrypted = arc4_encrypt(encoded_final_sum, f"{llave}{verificacion}")
    chunks = findall(".{2}", encrypted)  # Split in pieces of two chars

    return "-".join(chunks)
