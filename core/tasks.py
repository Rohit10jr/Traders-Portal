from celery import shared_task

@shared_task
def print_hello():
    print("Hello from Celery!")


# core/tasks.py

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
