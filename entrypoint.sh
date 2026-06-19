#!/bin/sh
trap exit SIGTERM SIGINT

sed -e "s|__DOMAIN__|${CFDDNS_DOMAIN}|g" \
    -e "s|__API_KEY__|${CFDDNS_API_KEY}|g" \
    -e "s|__RECORD_TYPE__|${CFDDNS_RECORD_TYPE}|g" \
    /etc/crontabs/root.template > /etc/crontabs/root
chmod 0600 /etc/crontabs/root

crond -f -l 2 &
wait
