#!/bin/bash

echo "$(date)" >> sales.txt

Cartes="rtx3060 rtx3070 rtx3080 rtx3090 rx6700"

Ventes () {
    curl "http://0.0.0.0:5000/$x"
}



for x in $Cartes
do
echo  "$x : $(Ventes)" >> sales.txt
done


