#!/bin/bash
if [[   $(docker ps --filter name=credivo* -aq) ]]; then
    echo 'Stopping Container...'
    docker ps --filter name=credivo* -aq | xargs docker stop
    echo 'All Container Stopped...'
    echo 'Removing Container...'
    docker ps --filter name=credivo* -aq | xargs docker rm
    echo 'All Container Removed...'
    docker network inspect credivo-network >/dev/null 2>&1
else
    echo "All Cleaned UP!"
fi