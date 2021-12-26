#!/usr/bin/env bash
export PYTHONPATH=.:libs

if [ ! -e keys/key.pem ]; then
    mkdir keys
    # generate key and cert
    openssl req -newkey rsa:2048 -nodes -keyout keys/key.pem -x509 -days 365 -out keys/cert.pem
fi

python3 server/server.py
