from django.http import HttpResponse
from django.template import loader
from django import forms
from django.shortcuts import render
from token_usage_calculators.openapi import token_usage_calculator as OpenAITokenUsageCalculator
from token_usage_calculators.deepseek import token_usage_calculator as DeepseekTokenUsageCaculator
from ordered_set import OrderedSet
from tokenizers import Tokenizer

import PyPDF2    # For PDF text extraction

MODELS_AVAILABLE_FORM = OrderedSet(["GPT-4", "GPT-4o", "GPT-4-Turbo","GPT-4o-Mini", "GPT-3.5-Turbo", "Deepseek-V3", "Deepseek-R1"])

def index(request):
    template = loader.get_template("tokeneyes/index.html")
    context = {
        "models": MODELS_AVAILABLE_FORM,
        "selected_model": MODELS_AVAILABLE_FORM[0],
        'input_type': 'text'
    }
    return HttpResponse(template.render(context, request))

def _getContentFromPdf(pdf_file) -> str:
    pdf_reader = PyPDF2.PdfReader(pdf_file)
                
    # Extract text from all pages
    text_content = ""
    for page in pdf_reader.pages:
        text_content += page.extract_text()
    
    return text_content


def _getTokenizer(model: str) -> Tokenizer:
    open_ai = OpenAITokenUsageCalculator.TokenUsageCalculator()
    if open_ai.is_model_supported(model):
        return open_ai
    return DeepseekTokenUsageCaculator.TokenUsageCalculator()

def calculate_tokens(request):
    if request.method == 'POST':
        input_type = request.POST.get('input_type')
        model = request.POST.get('model')
        text_content = request.POST.get('text_content')
        error = None
        result = None
        
        input_type = request.POST.get('input_type')
        text_content = request.POST.get('text_content')

        if input_type == "pdf":
            pdf_file = request.FILES['pdf_file']
            text_content = _getContentFromPdf(pdf_file)

        words_count = 0
        if text_content:
            words_count=len(text_content.split())

        tokenizer = _getTokenizer(model)
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

         # Render the same template with results or error
        return render(request, 'tokeneyes/index.html', {
            'input_type': 'pdf' if input_type == 'pdf' else 'text',
            'result': result,
            'error': error,
            'models': MODELS_AVAILABLE_FORM,
            'selected_model': model
        })
    
    # If not a POST request, redirect to index
    return render(request, 'tokeneyes/index.html', {
        "models": MODELS_AVAILABLE_FORM,
        'selected_model': MODELS_AVAILABLE_FORM[0],
        'input_type': 'pdf' if input_type == 'pdf' else 'text'
    })
