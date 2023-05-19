from ..models import ApiLogs
import datetime
from django.utils import timezone

def log2db(customer, type, name, result):
    ApiLogs.objects.create(timestamp=datetime.datetime.now(tz=timezone.utc),
                           customer=customer,
                           type=type,
                           name=name, result=result)