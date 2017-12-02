#!/bin/bash

# Simple bash script that 
# sets amazon key configuration
# environment variables
echo 'Please enter your AWS ACCESS key: '
read YOUR_ACCESS_KEY

echo 'Please enter your AWS SECRET key: '
read YOUR_SECRET_KEY


# This will set the environment variables to
# be used by boto3
export AWS_ACCESS_KEY_ID=$YOUR_ACCESS_KEY
export AWS_SECRET_ACCESS_KEY=$YOUR_SECRET_KEY
echo 'Credentials has been set!'