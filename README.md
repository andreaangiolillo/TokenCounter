# LLM Token Counter 
[☕ Buy me a coffee](https://buymeacoffee.com/keeptryingforfun)

LLM Token Counter calculates the number of input tokens and the associated cost incurred when processing text using an AI model via APIs.

Tokens are the basic units of text processed by AI models. The number of tokens in a given text depends on both its length and complexity.
To calculate how many tokens a piece of text contains, we use the open-source tokenizers provided by <a href="https://github.com/openai/tiktoken" target="_blank" rel="noopener noreferrer">OpenAI (tiktoken)</a> and <a href="https://api-docs.deepseek.com/quick_start/token_usage" target="_blank" rel="noopener noreferrer">DeepSeek</a>, selecting the tokenizer appropriate for the specific model.

After determining the token count, we retrieve the pricing per 1 million tokens from the <a href="https://openai.com/api/pricing/" target="_blank" rel="noopener noreferrer">OpenAI</a> and <a href="https://api-docs.deepseek.com/quick_start/pricing" target="_blank" rel="noopener noreferrer">DeepSeek</a> websites to estimate the total cost.

The tool provides an estimated token count and cost for processing your text with the selected AI model. Please note that the actual number of tokens used may vary slightly.


## Setting Up the Token Counter
The token counter is a Python Django web application, as most tokenizers are implemented in Python. To get started, follow these steps:

### Install Python
The repository includes a [.tool-versions](.tool-versions) file, which specifies the required Python version. If you use [asdf](https://asdf-vm.com), simply run the following command in the root directory of the repository after cloning it:
```bash
asdf install
```
If you’re not using asdf, visit the official [Python website](https://www.python.org/downloads/) to explore other methods for installing Python.


### Create a Virtual Environment
Once Python is installed, create a virtual environment to isolate your dependencies. Run the following command, replacing `/path/to/new/virtual/environment` with your desired path:

```bash
python -m venv /path/to/new/virtual/environment
```

### Install Dependencies
Activate your virtual environment and install the required dependencies listed in the [requirements.txt](requirements.txt) file:
```bash
# Activate the virtual environment 
source /path/to/new/virtual/environment
```

```bash
# Install the dependencies
pip install -r requirements.txt
```

### Run the App
Follow these steps to run the Django web application:

Django requires static files (like CSS, JavaScript, and images) to be gathered in a single location before serving them. Run the following command to collect the static files:
```bash
python manage.py collectstatic
```

Once the static files are collected, start the web application by running:
```bash
python manage.py runserver

Watching for file changes with StatReloader
Performing system checks...

None of PyTorch, TensorFlow >= 2.0, or Flax have been found. Models won't be available and only tokenizers, configuration and file/data utilities can be used.
System check identified no issues (0 silenced).
March 30, 2025 - 13:37:14
Django version 5.1.7, using settings 'mysite.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

The web application will now be available at: [http://localhost:8080](http://localhost:8080)
