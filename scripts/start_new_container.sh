#!/bin/bash

# Login to ECR (replace region & account)
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 901903979633.dkr.ecr.us-east-1.amazonaws.com

# Pull the latest image
docker pull 901903979633.dkr.ecr.us-east-1.amazonaws.com/sageprojects:latest

# Run the container
docker run -d --name flaskapp -p 5000:5000 901903979633.dkr.ecr.us-east-1.amazonaws.com/sageprojects:latest
