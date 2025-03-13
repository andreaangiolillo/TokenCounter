from django.http import HttpResponse
from django.template import loader
from django import forms
from django.shortcuts import render
from token_usage_calculators.openapi import token_usage_calculator as OpenAITokenUsageCalculator
from token_usage_calculators.deepseek import token_usage_calculator as DeepseekTokenUsageCaculator
from ordered_set import OrderedSet
from tokenizers import Tokenizer
import os
import logging
import PyPDF2  

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(levelname)s %(message)s')

MODELS_AVAILABLE_FORM = OrderedSet(["GPT-4", "GPT-4o", "GPT-4-Turbo","GPT-4o-Mini", "GPT-3.5-Turbo", "Deepseek-V3", "Deepseek-R1"])
GOOGLE_VERIFICATION_TOKEN=os.getenv("GOOGLE_VERIFICATION_TOKEN")

def index(request):
    template = loader.get_template("tokeneyes/index.html")
    context = {
        "models": MODELS_AVAILABLE_FORM,
        "selected_model": MODELS_AVAILABLE_FORM[0],
        'input_type': 'text',
        'google_site_verification': GOOGLE_VERIFICATION_TOKEN,
    }
    return HttpResponse(template.render(context, request))

def _get_content_from_pdf(pdf_file) -> str:
    _validate_pdf_file(pdf_file)
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    # Extract text from all pages
    text_content = ""
    for page in pdf_reader.pages:
        text_content += page.extract_text()
    
    return text_content

def _validate_pdf_file(pdf_file):
    if pdf_file.size > (10 * 10**6):
        raise ValueError("PDF file is too large.")

def _get_tokenizer(model: str) -> Tokenizer:
    open_ai = OpenAITokenUsageCalculator.TokenUsageCalculator()
    if open_ai.is_model_supported(model):
        return open_ai
    return DeepseekTokenUsageCaculator.TokenUsageCalculator()

def calculate_tokens(request):
    if request.method == 'POST':
        return calculate_token_post(request)
    
    # If not a POST request, redirect to index
    return render(request, 'tokeneyes/index.html', {
        "models": MODELS_AVAILABLE_FORM,
        'selected_model': MODELS_AVAILABLE_FORM[0],
        'input_type': 'text',
        'google_site_verification': GOOGLE_VERIFICATION_TOKEN,
    })

def calculate_token_post(request):
    input_type = request.POST.get('input_type')
    model = request.POST.get('model')
    text_content = request.POST.get('text_content')
    input_type = request.POST.get('input_type')
    text_content = request.POST.get('text_content')
    error = None
    result = None
    try: 
        if input_type == "pdf":
            pdf_file = request.FILES['pdf_file']
            text_content = _get_content_from_pdf(pdf_file)

        words_count = 0
        if text_content:
            words_count=len(text_content.split())

        tokenizer = _get_tokenizer(model)
        n_tokens = tokenizer.calculate_tokens(model=model, content=text_content)
        cost =  tokenizer.calculate_cost(model=model, n_tokens=n_tokens)
        result = {
                'model': model,
                'token_count': n_tokens,
                'words_count': words_count,
                'token_words_ratio': round(n_tokens/words_count, 3),
                'cost': cost,
                'text_content': text_content if input_type == 'text' else ""
        }
    except Exception as e:
        error = str(e)
        logging.error(e, exc_info=True)
    finally:
        return render(request, 'tokeneyes/index.html', {
            'input_type': 'pdf' if input_type == 'pdf' else 'text',
            'result': result,
            'error': error,
            'models': MODELS_AVAILABLE_FORM,
            'selected_model': model,
            'google_site_verification': GOOGLE_VERIFICATION_TOKEN,
    })

