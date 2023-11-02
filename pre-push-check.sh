#!bin/bash

main_branch="main"
dev_branch="dev"

if [ "$1" == $main_branch || "$1" == $dev_branch ]; then
    echo "Running tests to push to $1 branch"
    pytest -v tests
else
    echo "Pushing to $1 branch"
fi
