docker-compose up -d rabbitmq mysql redis

sleep 15

docker-compose up -d opendcan-vue opendcan-backend runner-train runner-inference