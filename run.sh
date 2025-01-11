#!/bin/bash

alembic -c src/config/alembic.ini upgrade head

python3 main.py
