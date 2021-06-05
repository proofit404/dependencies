#!/bin/bash

cd $1

python -m pip install $2

patch lib/python3.9/site-packages/blacken_docs.py ../../blacken-docs.patch
