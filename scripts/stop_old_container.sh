#!/bin/bash
docker stop flaskapp || true
docker rm flaskapp || true
