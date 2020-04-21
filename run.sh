#!/bin/bash

set -euo pipefail

function main(){
    
    python manage.py migrate
    
    readonly ACCESS_LOG_FILE=/var/log/sahabee/access.log
    readonly ERROR_LOG_FILE=/var/log/sahabee/error.log

    create_file_if_not_exists $ACCESS_LOG_FILE
    create_file_if_not_exists $ERROR_LOG_FILE
    
    gunicorn --bind 0.0.0.0:8000 \
    --access-logfile $ACCESS_LOG_FILE \
    --error-logfile $ERROR_LOG_FILE \
    --workers 16 \
    --certfile=/etc/ssl-files/fullchain.pem \
    --keyfile=/etc/ssl-files/privkey.pem \
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