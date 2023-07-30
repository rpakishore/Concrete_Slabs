#export $(grep -v '^#' EDIT.env | xargs)
cmd="docker ps -aqf \"name=slabs\""
id=$(docker ps -aqf "name=slabs")

git pull

docker build -t slabs:latest .
docker container stop $id
docker container rm $id

docker compose up -d
