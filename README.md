# Bolivia Codigo de Control

``` terminal
$ pip install bolivia-cc
$ bolivia_cc --generar \
    --autorizacion=7000000006000 \
    --factura=560001 \
    --nit=3200000 \
    --fecha=2023-01-01 \
    --total=10000 \
    --llave=SECRET \
7B-F3-48-A8
```

``` python
import bolivia_cc

codigo_control = bolivia_cc.generar(
    autorizacion=7000000006000,
    factura=560001,
    nit=3200000,
    fecha=2023-01-01,
    total=10000,
    llave="SECRET",
)

assert codigo_control == "7B-F3-48-A8"
```
