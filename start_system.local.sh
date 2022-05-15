docker-compose -f docker-compose.local.yml up -d rabbitmq redis

sleep 15

docker-compose -f docker-compose.local.yml up -d runner-train runner-inference runner-inference-dataset opendcan-backend #opendcan-vue