#!/bin/bash

set -euo pipefail

readonly CWD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
readonly PUBLIC_KEY="$CWD/id_rsa.pub"
SERVER=
SSH_PORT=22
USER=
PASS=
CHECK_FINGERPRINT_FLAG='-o StrictHostKeyChecking=ask'

function main() {
    inflate_args "$@"
    precheck

    sshpass -p $PASS ssh $CHECK_FINGERPRINT_FLAG $USER@$SERVER '[ -d ~/.ssh/ ] || mkdir ~/.ssh/'
    cat "$PUBLIC_KEY" | sshpass -p $PASS ssh $CHECK_FINGERPRINT_FLAG -p $SSH_PORT $USER@$SERVER 'cat >> ~/.ssh/authorized_keys'
}

function inflate_args() {
    while [ $# -gt 0 ]; do
        case "$1" in
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
            --no-check-fingerprint | -f)
                shift
                CHECK_FINGERPRINT_FLAG='-o StrictHostKeyChecking=no'
                ;;
            --ssh-port)
                shift
                SSH_PORT=$1
                ;;
            *)
                ercho "Unknown option: $1"
                exit 3
                ;;
        esac

    done
}

function precheck() {
    if [ ! -f "$PUBLIC_KEY" ]; then
        ercho "Public key file not found: $PUBLIC_KEY"
        exit 1
    fi

    if [ -z "$SERVER" ] || [ -z "$USER" ] || [ -z "$PASS" ]; then
        ercho "Usage: $0 -s server_ip -u user -p pass"
        exit 2
    fi
}

function ercho() {
    echo >&2 "$@"
}

main "$@"