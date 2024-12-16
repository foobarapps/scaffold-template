#!/bin/bash
set -eux

alembic upgrade head

exec "$@"
