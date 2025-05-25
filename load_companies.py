import csv
from core.models import Company

limit = 1000
count = 0

with open("master.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if count >= limit:
            break
        Company.objects.get_or_create(
            company_name=row['company_name'],
            symbol=row['symbol'],
            scripcode=row['scripcode']
        )
        count += 1

print(f"{count} entries loaded")
