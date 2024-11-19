#!/bin/bash

host=$1
shift
until curl --silent --head --fail http://$host; do
  echo "Waiting for $host to become available..."
  sleep 2
done
echo "$host is available, starting Nginx"
exec "$@"