docker build -f .\owner.dockerfile --tag owner .
docker build -f .\courier.dockerfile --tag courier .
docker build -f .\customer.dockerfile --tag customer .

docker compose -f .\deployment.yaml up

# pokrece brzo aplikacije u deployment
# SWARM - nece nam trebati za ispit!
