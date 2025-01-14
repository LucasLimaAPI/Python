import os
from datetime import datetime, timedelta

# Data inicial
start_date = datetime(2024, 10, 1)
end_date = datetime(2024, 12, 30)

# Criar pastas
current_date = start_date
while current_date <= end_date:
    date_string = current_date.strftime("%Y-%m-%d")
    os.makedirs(date_string, exist_ok=True)
    current_date += timedelta(days=1)