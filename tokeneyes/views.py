from django.http import HttpResponse
from django.template import loader
from django import forms
from django.shortcuts import render
from token_usage_calculators.openapi import token_usage_calculator as OpenAITokenUsageCalculator
from token_usage_calculators.deepseek import token_usage_calculator as DeepseekTokenUsageCaculator
from ordered_set import OrderedSet

import PyPDF2    # For PDF text extraction

MODELS_AVAILABLE_FORM = OrderedSet(["GPT-4", "GPT-4o", "GPT-4-Turbo","GPT-4o-Mini", "GPT-3.5-Turbo", "Deepseek-V3", "Deepseek-R1"])

def index(request):
    template = loader.get_template("tokeneyes/index.html")
    context = {
        "models": MODELS_AVAILABLE_FORM,
        "selected_model": MODELS_AVAILABLE_FORM[0]
    }
    return HttpResponse(template.render(context, request))


def calculate_tokens(request):
    if request.method == 'POST':
        input_type = request.POST.get('input_type')
        model = request.POST.get('model')
        text_content:str = request.POST.get('text_content')
        file_name = None
        error = None
        result = None
        print(f'input_type: {input_type}, model: {model}, text_content:{text_content}' )
        words_count=len(text_content.split())

        
        open_ai = OpenAITokenUsageCalculator.TokenUsageCalculator()
        if open_ai.is_model_supported(model):
            n_tokens = open_ai.calculate_tokens(model=model, content=text_content)
            cost =  open_ai.calculate_cost(model=model, n_tokens=n_tokens)
            result = {
                    'input_type': 'PDF' if input_type == 'pdf' else 'Text',
                    'model': model,
                    'token_count': n_tokens,
                    'words_count':words_count,
                    'token_words_ratio': round(n_tokens/words_count, 3),
                    'cost': cost,
                    'text_content': text_content
            }

        deepseek = DeepseekTokenUsageCaculator.TokenUsageCalculator()
        if deepseek.is_model_supported(model):
            n_tokens = deepseek.calculate_tokens(model=model, content=text_content)
            cost =  deepseek.calculate_cost(model=model, n_tokens=n_tokens)
            result = {
                    'input_type': 'PDF' if input_type == 'pdf' else 'Text',
                    'model': model,
                    'token_count': n_tokens,
                    'words_count': words_count,
                    'token_words_ratio': round(n_tokens/words_count, 3),
                    'cost': cost,
                    'text_content': text_content
            }

         # Render the same template with results or error
        return render(request, 'tokeneyes/index.html', {
            'result': result,
            'error': error,
            'models': MODELS_AVAILABLE_FORM,
            'selected_model': model
        })
    
    # If not a POST request, redirect to index
    return render(request, 'tokeneyes/index.html', {
        "models": MODELS_AVAILABLE_FORM,
        'selected_model': MODELS_AVAILABLE_FORM[0]
    })


