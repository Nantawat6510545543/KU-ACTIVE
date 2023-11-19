#!/bin/bash

# Run Gunicorn
gunicorn --bind :8000 --workers 2 mysite.wsgi

# Swap setup
fallocate -l 512M /swapfile
chmod 0600 /swapfile
mkswap /swapfile
echo 10 > /proc/sys/vm/swappiness
swapon /swapfile
echo 1 > /proc/sys/vm/overcommit_memory