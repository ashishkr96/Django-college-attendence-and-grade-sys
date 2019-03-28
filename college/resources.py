from import_export import resources
from .models import Submarks


class SubmarksResource(resources.ModelResource):
    class Meta:
        model = Submarks
        fields = ('subject', 'student', 'attendence',)
