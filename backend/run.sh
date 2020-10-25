#!/bin/sh

set -eu

main(){
    
    python manage.py migrate
    
    readonly ACCESS_LOG_FILE=/var/log/sahabee/access.log
    readonly ERROR_LOG_FILE=/var/log/sahabee/error.log

    create_file_if_not_exists $ACCESS_LOG_FILE
    create_file_if_not_exists $ERROR_LOG_FILE

    sync_static_files

    gunicorn --bind 0.0.0.0:8000 \
    --access-logfile $ACCESS_LOG_FILE \
    --error-logfile $ERROR_LOG_FILE \
    --workers 4 \
    sahabee.wsgi:application
    
}

create_file_if_not_exists() {
    file_path="$1"
    file_dir=`dirname $file_path`
    if [ ! -d $file_dir ]; then
        mkdir -p $file_dir
    fi

    if [ ! -f $file_path ]; then
        touch $file_path
    fi
}

sync_static_files() {
    rsync -r --delete /sahabee/static/ /sahabee/static-files/
}

main "$@"