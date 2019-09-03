#!/usr/bin/env bash

echo "Installing Requirements"
pip install -r requirements.txt

echo "Auto-formatting code"
#black .

echo "Running Unit Tests"
if ! pytest; then
    echo "One or more unit tests failed"
    exit 1
fi

echo "Running System Tests"
if ! behave; then
    echo "One or more system tests failed"
    exit 1
fi
echo "Build Done!"
