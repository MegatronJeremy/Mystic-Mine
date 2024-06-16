./venv/Scripts/activate.ps1
$env:PORT = 5000
Start-Process python -ArgumentList "owner.py" 
$env:PORT = 5001
Start-Process python -ArgumentList "courier.py" 
$env:PORT = 5002
Start-Process python -ArgumentList "customer.py" 
Start-Process python -ArgumentList "redis_listener.py"