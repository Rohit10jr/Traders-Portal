from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Company(models.Model):
    company_name = models.CharField(max_length=255, db_index=True)
    symbol = models.CharField(max_length=50, unique=True, db_index=True)
    scripcode = models.CharField(max_length=50)

    def __str__(self):
        # return f"{self.id}"
        return f"{self.symbol} - {self.company_name}"
        # return super().__str__()

    # class Meta:
    #     indexes = [models.Index(fields=['company_name']), models.Index(fields=['symbol'])]
    #     verbose_name_plural = "companies"


class WatchList(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together =  ('user', 'company')