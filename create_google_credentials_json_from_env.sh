#!/bin/sh
echo $GOOGLE_CREDENTIALS > google-credentials.json
exec "$@"