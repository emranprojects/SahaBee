#!/bin/bash

set -euo pipefail

function main(){
    
    python manage.py migrate
    
    readonly ACCESS_LOG_FILE=/var/log/sahabee/access.log
    readonly ERROR_LOG_FILE=/var/log/sahabee/error.log

    create_file_if_not_exists $ACCESS_LOG_FILE
    create_file_if_not_exists $ERROR_LOG_FILE

    FULL_CHAIN_FILE=/etc/ssl-files/fullchain.pem
    PRIVKEY_FILE=/etc/ssl-files/privkey.pem
    if [ ! -f $FULL_CHAIN_FILE ] || [ ! -f $PRIVKEY_FILE ]; then
        echo "Using temp ssl certificates..."
        FULL_CHAIN_FILE=/sahabee/temp-certificate/localhost.cert.temp
        PRIVKEY_FILE=/sahabee/temp-certificate/localhost.key.temp
    fi

    gunicorn --bind 0.0.0.0:8000 \
    --access-logfile $ACCESS_LOG_FILE \
    --error-logfile $ERROR_LOG_FILE \
    --workers 16 \
    --certfile=$FULL_CHAIN_FILE \
    --keyfile=$PRIVKEY_FILE \
    sahabee.wsgi:application
    
}

function create_file_if_not_exists() {
    file_path="$1"
    file_dir=`dirname $file_path`
    if [ ! -d $file_dir ]; then
        mkdir -p $file_dir
    fi

    if [ ! -f $file_path ]; then
        touch $file_path
    fi
}

main "$@"