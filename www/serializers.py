from rest_framework import serializers
from .models import File

class FileSerializers(serializers.ModelSerializer):
	class Meta:
	    model = File
	    fields = ('title','summary','course', 'author','dateCreated','tag')