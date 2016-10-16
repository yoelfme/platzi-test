#!/bin/bash
./cp_env_dev.sh
docker-compose up -d
docker-compose logs -f
