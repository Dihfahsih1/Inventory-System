from import_export import resources
from .models import *


class CarResource(resources.ModelResource):
    class Meta:
        model = Car

class DriverResource(resources.ModelResource):
    class Meta:
        model = Driver

