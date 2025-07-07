from django.contrib import admin
from .models import PDFDocument, QuestionType

# Register your models here.

admin.site.register(PDFDocument)
admin.site.register(QuestionType)