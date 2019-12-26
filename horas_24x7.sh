#!/bin/bash

MES="$(date +%m)"
TIEMPOS_REALES=0
ODOO_STRING=""

last_inci=""
last_inci_tiempo=0

# usage() { echo "Usage: $0 -m MONTH" }

# while getopts ":m" opt; do
#    case $opt in
#       m)
#          if [ -z $opt ]; then
#             usage
#             exit 1
#          else
#             if [[ $opt =~ ^[0-9]+$ ]]; then
#                MES=$opt
#             else
#                usage
#                exit 1
#             fi
#          fi
#          ;;
#       \?)
#          echo "Error"
#          usage
#          exit 1
#          ;;
#    esac
# done

if [ -z $1 ]; then
    echo "Mes no recibido. Calculamos con el mes actual: $(date +%B)"
else
    echo "Mes $1 recibido. Calculamos con el mes de $(date -d 2019-$1-01 +%B)"
    MES=$1
fi

# Ultimo dia del mes
ULTIMO_DIA="$(cal $MES 2019 | awk 'NF {DAYS = $NF}; END {print DAYS}')"
for inci in $(mquery -C -B -p 24x7 -fu acarreno 01/$MES $ULTIMO_DIA/$MES); do
    TAM="$(echo -n $ODOO_STRING | wc -c)"
    if [ $TAM -eq 0 ]; then
        ODOO_STRING=$inci
    else
        ODOO_STRING="$ODOO_STRING, $inci"
    fi
    for tiempo in $(mquery -C -v $inci | grep Nota | grep acarreno | awk '{print $12}'); do
        if [ $(echo "$tiempo == 0" | bc -l) -ne 1 ]; then
            TIEMPOS_REALES=$(echo -n $TIEMPOS_REALES+$tiempo)
            echo $inci: $tiempo
        fi
    done
done
TIEMPOS_REALES=$(echo "$TIEMPOS_REALES" | bc)
TIEMPOS_MULTIPLO=$(echo "$TIEMPOS_REALES * 1.5" | bc)
echo "Tiempos reales: $TIEMPOS_REALES"
echo "Tiempos múltiplo: $TIEMPOS_MULTIPLO"
DIAS_TOTALES=$(echo "scale=2; $TIEMPOS_MULTIPLO / 8" | bc)
echo "Dias totales: $DIAS_TOTALES"
echo "Para Odoo: $ODOO_STRING"
