from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils import timezone
import os

def pdf_upload_path(instance, filename):
    """Generate upload path for pdf files"""
    return f'pdfs/{instance.user.id}/{timezone.now().strftime("%Y/%m")}/{filename}'

class PDFDocument(models.Model):
    SUBJECT_CHOICES = [
        ('mathematics', 'Mathematics'),
        ('science', 'Science'),
        ('history', 'History'),
        ('literature', 'Literature'),
        ('computer_science', 'Computer Science'),
        ('other', 'Other'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    QUESTION_TYPE_CHOICES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('short_answer', 'Short Answer'),
        ('fill_blank', 'Fill in the Blank'),
    ]

    ## Basic Fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pdf_documents')
    quiz_title = models.CharField(max_length=200)
    pdf_file = models.FileField(
        upload_to=pdf_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text='Upload PDF file (max 10MB)'
    )

    # configration fields
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES, blank=True)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='medium')
    num_questions = models.IntegerField(default=10)
    description = models.TextField(blank=True, null=True)

    # status and processing fields
    is_processed = models.BooleanField(default=False)
    processing_status = models.CharField(max_length=50, default='pending')
    error_message = models.TextField(blank=True, null=True)

     # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'PDF Document'
        verbose_name_plural = 'PDF Documents'
    
    @property
    def file_size(self):
        """Return file size in MB"""

        if self.pdf_file:
            return round(self.pdf_file.size/(1024*1024),2)
        return 0
    
    def delete(self, *args, **kwargs):
        """Delete file when model instance is deleted"""
        if self.pdf_file:
            if os.path.isfile(self.pdf_file.path):
                os.remove(self.pdf_file.path)
        super().delete(*args, **kwargs)

class QuestionType(models.Model):
    """Store selected question type for each pdf document"""
    pdf_document = models.ForeignKey(PDFDocument, on_delete=models.CASCADE, related_name='question_types')
    question_type = models.CharField(max_length=50, choices=PDFDocument.QUESTION_TYPE_CHOICES)

    class Meta:
        unique_together = ['pdf_document', 'question_type']

    def __str__(self):
        return f"{self.pdf_document.quiz_title} - {self.get_question_type_display()}"