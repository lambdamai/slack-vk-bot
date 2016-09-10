#!/bin/bash

CURL='/usr/bin/curl'
RVMHTTP="http://0.0.0.0:5000/callback/xE4sA"

$CURL -H "Content-Type: application/json" -X POST -d '{"type":"wall_post_new","object":{"id":"291","from_id":"-105873414", "owner_id":"-105873414","date":"1473457177","post_type":"post","text":"welcome to the rice fields, motherfucker"}}' $RVMHTTP