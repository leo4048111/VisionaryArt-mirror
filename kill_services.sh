#!/bin/sh

# 关闭visionary-art-platform服务
lsof -i :80 | grep LISTEN | awk '{print $2}' | xargs kill -9

# 关闭visionary-art-ai-service服务
lsof -i :7650 | grep LISTEN | awk '{print $2}' | xargs kill -9

# 关闭visionary-art-admin-service服务
lsof -i :8080 | grep LISTEN | awk '{print $2}' | xargs kill -9
