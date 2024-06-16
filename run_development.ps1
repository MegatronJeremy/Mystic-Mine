Start-Process docker -ArgumentList "compose", "-f", "development.yaml", "up"
Read-Host -Prompt "Press enter to start applications when services are up"

./venv/Scripts/activate.ps1
$env:PORT = 5000
Start-Process python -ArgumentList "owner.py" 
$env:PORT = 5001
Start-Process python -ArgumentList "courier.py" 
$env:PORT = 5002
Start-Process python -ArgumentList "customer.py" 
Start-Process python -ArgumentList "redis_listener.py"

# ovo - pokrece servise i tri pajton procesa - izvrsavaju svi po jednu od ove tri skripte
# aplikacije  u debug rezimu - mogu da menjam kod i da ne pokrecem opet