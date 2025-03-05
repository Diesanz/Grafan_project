#!/bin/bash
for i in $(seq 1 5); do
  echo "Creando proceso $i"
  while true; do
    # Realiza una operación matemática simple para mantener el proceso activo
    let "a = 1 + 1"
  done &
done
