#!/bin/sh

set -eu

main(){
    
    python manage.py migrate
    
    readonly ACCESS_LOG_FILE=/var/log/sahabee/access.log
    readonly ERROR_LOG_FILE=/var/log/sahabee/error.log

    readonly CELERY_LOG_FILE_OUT=/var/log/sahabee/celery/out.log
    readonly CELERY_LOG_FILE_ERR=/var/log/sahabee/celery/err.log
    readonly CELERY_BEAT_LOG_FILE_OUT=/var/log/sahabee/celery_beat/out.log
    readonly CELERY_BEAT_LOG_FILE_ERR=/var/log/sahabee/celery_beat/err.log

    create_file_if_not_exists $ACCESS_LOG_FILE
    create_file_if_not_exists $ERROR_LOG_FILE
    create_file_if_not_exists $CELERY_LOG_FILE_OUT
    create_file_if_not_exists $CELERY_LOG_FILE_ERR
    create_file_if_not_exists $CELERY_BEAT_LOG_FILE_OUT
    create_file_if_not_exists $CELERY_BEAT_LOG_FILE_ERR

    sync_static_files

    supervisord -c sahabee/configs/celery-supervisord.conf
    supervisord -c sahabee/configs/celery-beat-supervisord.conf

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