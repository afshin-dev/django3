from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.
class Tag(models.Model):
    label = models.CharField(max_length=255, null=False, unique=True)


class TagItem(models.Model):  # Generic relationship
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    object = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE)  # keep reference to particular object(model)

    object_id = models.PositiveIntegerField() # keep id of particular model
    content_object = GenericForeignKey() # give us actual object in database 
    

### for making a Generic relation ship ###
### we must keep to reference
# 1- type of object (Product, Video, Post)
# 2 - id of that specific object (Product(pk=400))
