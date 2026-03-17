from django.db import models
from .choice_select import AI_MODEL

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseAIModel(models.Model):
    model = models.CharField(max_length=20, choices=AI_MODEL.choices, default=AI_MODEL.OPENAPI)
    instructions_rules = models.TextField(blank=True, null=True)




