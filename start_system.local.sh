docker-compose -f docker-compose.local.yml up -d rabbitmq redis

sleep 15

docker-compose -f docker-compose.local.yml up -d opendcan-vue runner-train runner-inference opendcan-backend