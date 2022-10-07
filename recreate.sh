export $(grep -v '^#' EDIT.env | xargs)
cmd="docker ps -aqf \"name=${NAME}\""
id=$(docker ps -aqf "name=${NAME}")

docker container stop $id
docker container rm $id

git pull

docker build -t ${NAME}:latest .
docker-compose up -d
