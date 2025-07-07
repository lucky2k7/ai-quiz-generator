from django.shortcuts import render,  HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json

from .models import PDFDocument, QuestionType

# Create your views here.

def home(request):
    return render(request, "quiz/home.html")

def create_quiz(request):
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        return handle_ajax_upload(request)
        
    return render(request, 'quiz/create_quiz.html')

def handle_ajax_upload(request):
    try:
        print("try block to validate required files")
        # validate rquired fields
        required_fields = ['quiz_title', 'pdf_file']
        for field in required_fields:
            if field not in request.POST and field not in request.FILES:
                return JsonResponse({
                    'success':False,
                    'message': f"{field.replace('_',' ').title()} is required"
                }, status=400)
            
        # validate file
        if 'pdf_file' not in request.FILES:
            return JsonResponse({
                'success':False,
                'message':"Select only pdf file"
            }, status=400)
        
        pdf_file = request.FILES['pdf_file']

        # file validation
        if not pdf_file.name.lower().endswith('.pdf'):
            return JsonResponse({
                'success': False,
                'message': 'Only PDF files are allowed.'
            }, status=400)
        
        if pdf_file.size > 10 * 1024 * 1024:  # 10MB
            return JsonResponse({
                'success': False,
                'message': 'File size must be less than 10MB.'
            }, status=400)

        # parse question types
        question_types= request.POST.getlist('question_types') 
        if  not question_types:
            return JsonResponse({
                'success':False,
                'message':"Pelese select at least one question type."
            }, status=400)
        print("Point 1")
        # create pdf document instance
        pdf_document = PDFDocument.objects.create(
            user = request.user,
            quiz_title=request.POST.get('quiz_title').strip(),
            pdf_file = pdf_file,
            subject = request.POST.get('subject',''),
            difficulty_level = request.POST.get('defficult_level', 'medium'),
            num_questions = int(request.POST.get('no_questions', 10)),

            description = request.POST.get('description','').strip(),
            processing_status = 'uploaded'
        )
        print("point 2")
        # save question types
        for question_type in question_types:
            if question_type in dict(PDFDocument.QUESTION_TYPE_CHOICES):
                QuestionType.objects.create(
                    pdf_document = pdf_document,
                    question_type = question_type 
                )
        
        pdf_document.processing_status = 'processing'
        pdf_document.save()

        # TODO: Implement actual PDF processing and quiz generation
        # This is where you would integrate with AI/ML service to:
        # 1. Extract text from PDF
        # 2. Generate questions based on content
        # 3. Create Quiz and Question objects

        return JsonResponse({
                'success': True,
                'message': f'Quiz generated successfully!.',
                'pdf_document_id': pdf_document.id,
                'redirect_url' : f'/view/{pdf_document.id}/'
             })
    except Exception as e:
        print("Exception block")
        print(str(e))
        return JsonResponse({
            'success':False,
            'message':f"A error is occurred: {str(e)}"
        }, status=500)

    
    print((request.POST.getlist('question_types')))
    print(request.FILES)
    

def view_quiz(request, pdf_id):
    pdf_document = get_object_or_404(PDFDocument, id=pdf_id, user=request.user)
    print(pdf_document.user)
    context = {
        'pdf_document':pdf_document,
        'quiz':getattr(pdf_document, 'quiz', None)
    }
    return render(request, 'quiz/view_quiz.html', context)