#!/usr/bin/env bash

set -euo pipefail

readonly CWD="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
readonly SMTP_CLI="./smtp-cli"

SERVER=
USER=
PASS=
RECIPIENTS=()
VERBOSE=
YEAR_MONTH=
SAHABEE_USER=

function main() {
    cd $CWD
    download_smtp_cli_if_needed
    inflate_args "$@"
    check_args
    download_timesheet
    send_mail
}

function err() {
    echo >&2 "ERROR: $1"
    exit 1
}

function inflate_args() {
    while [ $# -gt 0 ]; do
        case "$1" in
        --help | -h)
            print_usage
            exit 0
            ;;
        --server | -s)
            shift
            SERVER=$1
            shift
            ;;
        --user | -u)
            shift
            USER=$1
            shift
            ;;
        --pass | -p)
            shift
            PASS=$1
            shift
            ;;
        --to)
            shift
            RECIPIENTS+=("$1")
            shift
            ;;
        --sahabee-user)
            shift
            SAHABEE_USER=$1
            shift
            ;;
        --year-month | -y | -m)
            shift
            YEAR_MONTH=$1
            shift
            ;;
        --cc1)
            shift
            CC1=$1
            shift
            ;;
        --cc2)
            shift
            CC2=$1
            shift
            ;;
        --verbose | -v)
            shift
            VERBOSE=--verbose
            ;;
        *)
            ercho "Unknown option: $1"
            exit 1
            ;;
        esac

    done
}

function print_usage() {
    echo "
Usage:
  ./send-timesheet.sh --server <SMTP_SERVER:PORT> --user <USER> --pass <PASS> --to <RECIPIENT> --year-month <LIKE 1400/01> --sahabee-user <user of sahabee.ir>
    "
}

function check_args() {
    if [ -z "$SERVER" ] || [ -z "$USER" ] || [ -z "$PASS" ] || [ ${#RECIPIENTS[@]} -eq 0 ] || [ -z "$YEAR_MONTH" ] || [ -z "$SAHABEE_USER" ]; then
        print_usage
        exit 2
    fi
}

function download_smtp_cli_if_needed() {
    if [ ! -f $SMTP_CLI ]; then
        wget https://github.com/mludvig/smtp-cli/archive/refs/tags/v3.10.tar.gz
        tar xzf v3.10.tar.gz
        cp smtp-cli-3.10/smtp-cli $SMTP_CLI
        rm -rf smtp-cli-3.10/
        rm v3.10.tar.gz
    fi
}

function download_timesheet() {
    if [ -f "./timesheet.xlsx" ]; then
        rm ./timesheet.xlsx
    fi
    wget "https://sahabee.ir/$SAHABEE_USER/$YEAR_MONTH/timesheet.xlsx"
}

function send_mail() {
    local to_part=""
    local rcpt_to_part=""
    for r in ${RECIPIENTS[@]}; do
        to_part="$to_part --to $r"
        rcpt_to_part="$rcpt_to_part --rcpt-to $r"
    done

    $SMTP_CLI \
        --missing-modules-ok \
        --server=$SERVER \
        --ipv4 \
        --user=$USER \
        --pass=$PASS \
        --subject="Remote Work Timesheet" \
        --body-plain="Hello,
Here's my remote worksheet in $YEAR_MONTH.

This message is sent by SahaBee Soldier, an agent for mailing the timesheets, instead of the real sender!

Sincerely,
SahaBee Soldier
https://gitlab.com/emran.bm/sahabee" \
        $to_part \
        $VERBOSE \
        --mail-from=$USER \
        $rcpt_to_part \
        --attach="./timesheet.xlsx@application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
}

main "$@"
