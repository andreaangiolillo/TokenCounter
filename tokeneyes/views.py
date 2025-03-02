from django.http import HttpResponse
from django.template import loader
from django import forms
from django.shortcuts import render
from tokenizers.openapi import token_usage_calculator as OpenAITokenUsageCalculator
from tokenizers import tokenizer

import PyPDF2    # For PDF text extraction


def index(request):
    template = loader.get_template("tokeneyes/index.html")
    context = {
        "model": "gpt-4"
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
        
        if not issubclass(OpenAITokenUsageCalculator.TokenUsageCalculator, tokenizer.Tokenizer):
            raise ValueError("OpenAITokenUsageCalculator does not implment Tokenizer")
        
        open_ai = OpenAITokenUsageCalculator.TokenUsageCalculator()
        n_tokens = open_ai.calculate_tokens(model=model, content=text_content)
        cost =  open_ai.calculate_cost(model=model, n_tokens=n_tokens)
        result = {
                'input_type': 'PDF' if input_type == 'pdf' else 'Text',
                'model': model,
                'token_count': n_tokens,
                'cost': cost,
                'text_content': text_content
        }

         # Render the same template with results or error
        return render(request, 'tokeneyes/index.html', {
            'result': result,
            'error': error,
        })
    
    # If not a POST request, redirect to index
    return render(request, 'tokeneyes/index.html', {})

