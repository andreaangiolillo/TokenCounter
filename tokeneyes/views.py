from django.http import HttpResponse
from django.template import loader
from django import forms
from django.shortcuts import render
from tokenizers.openapi import tokenizer as openAiTokenizer
import tiktoken  # For OpenAI token counting
import PyPDF2    # For PDF text extraction

def index(request):
    template = loader.get_template("tokeneyes/index.html")
    context = {
        "calculate_tokens": 100,
    }
    return HttpResponse(template.render(context, request))


def calculate_tokens(request):
    if request.method == 'POST':
        input_type = request.POST.get('input_type')
        model = request.POST.get('model')
        text_content = request.POST.get('textContent')
        file_name = None
        error = None
        result = None

        encoding = tiktoken.encoding_for_model("model")

        result = {
                'input_type': 'PDF' if input_type == 'pdf' else 'Text',
                'model': model,
                'token_count': 22,
                'cost': 222,
        }
         # Render the same template with results or error
        return render(request, 'tokeneyes/index.html', {
            'result': result,
            'error': error,
        })
    
    # If not a POST request, redirect to index
    return render(request, 'tokeneyes/index.html')

