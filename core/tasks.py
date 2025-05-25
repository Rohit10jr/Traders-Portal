import csv
import os
from celery import shared_task
from core.models import Company
from django.conf import settings

@shared_task
def load_all_companies_from_csv():
    try:
        file_path = os.path.join(settings.BASE_DIR, 'master.csv')

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0

            # Optional: Delete all existing entries
            Company.objects.all().delete()

            for row in reader:
                Company.objects.get_or_create(
                    company_name=row['company_name'],
                    symbol=row['symbol'],
                    scripcode=row['scripcode']
                )
                count += 1

        return f"{count} companies loaded successfully."

    except Exception as e:
        import logging
        logger = logging.getLogger('critical_api')
        logger.error("CSV Load Error: %s", str(e), exc_info=True)
        return f"Failed: {str(e)}"


# -------------------- test celery --------------------

# from celery import shared_task

# @shared_task
# def print_hello():
#     print("Hello from Celery!")

# from celery import shared_task
# import requests
# from .models import Company

# @shared_task
# def update_company_data():
#     print("Fetching latest company data...")
#     # Example: pretend API call
#     sample_data = [
#         {'company_name': 'New Co', 'symbol': 'NEWCO', 'scripcode': '123456'},
#     ]
#     for data in sample_data:
#         Company.objects.update_or_create(
#             symbol=data['symbol'],
#             defaults={
#                 'company_name': data['company_name'],
#                 'scripcode': data['scripcode']
#             }
#         )
#     return "Company data updated"
