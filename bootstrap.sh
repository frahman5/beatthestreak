#!/usr/bin/env bash

# Variables
GOROOT=/usr/local/go
GOPKG=go1.2.2.linux-amd64.tar.gz
NGINX_CONF=https://gist.githubusercontent.com/tantastik/d504b0d73f0c97a74403/raw/e21fac5d16cd23694395fdf54eb5488b1811dcaa/nginx-cors.conf

# Dependencies
apt-get -q -y update
apt-get install -y python-software-properties
apt-get install -y git bzr mercurial
apt-get install -y curl
apt-get install vim
apt-get install gdb
