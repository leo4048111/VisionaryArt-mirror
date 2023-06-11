#!/bin/sh

cd visionary-art-platform/
python3 server.py &

cd ../visionary-art-ai-service/
python3 run.py &

cd ../visionary-art-admin-service/
python3 server.py &

cd -
