import os
import transformers
from token_usage_calculators.token_usage_calculator import Tokenizer
from decimal import Decimal, getcontext

class TokenUsageCalculator(Tokenizer):
    AVAILABLE_MODELS = ["deepseek-v3", "deepseek-r1"]
    
    """ 
    Site: https://api-docs.deepseek.com/quick_start/pricing/
    Update date: 02/03/2025 
    Prices are stored in dollars and represented in cents (1 dollar = 100 cents).
    After performing calculations, results must be converted back to the original unit by multiplying by 10^(-6).
    """
    MODELS_COST = {"deepseek-v3": 270, "deepseek-r1": 550}
    
    def __init__(self):
        return 
    
    def _validate_model(self, model: str):
        if model not in self.AVAILABLE_MODELS:
            raise ValueError(f"the model '{model}' is not supported")

    def get_available_models(self) -> list:
        return self.AVAILABLE_MODELS 
       
    """Returns the cost in cents per single token"""
    def get_cost_per_token(self, model:str) -> str:
        self._validate_model(model)
        getcontext().prec = 10
        cost = self.MODELS_COST[model]
        return str(Decimal(cost) * Decimal(10**(-8)))
    
    """Returns the number of tokens in a text string"""    
    def calculate_tokens(self, model:str, content: str) -> int:
        if content:
            self._validate_model(model)
            tokenizer_dir = "./token_usage_calculators/deepseek/config/r1/"
            if "v3" in model:
                tokenizer_dir = "./token_usage_calculators/deepseek/config/v3/"

            deep_seek_tokenizer = transformers.AutoTokenizer.from_pretrained(
                tokenizer_dir, 
                trust_remote_code=True,
                local_files_only=True
            )
            
            return len(deep_seek_tokenizer.encode(content))

        return 0
    
    """
    Returns an estimate of the cost in dollards associated with the token in input
    Since the price are in cents, the total cost in dollars is calculated as:
    
    tot_cost = (cost_single_token_per_model * n_tokens) * 10**(-6) * 10**(-2)

    - We multiply for 10**(-6) because prices are per 1M of tokens
    - We multiply for 10**(-2) to trasform the price from cents to dollars
    """
    def calculate_cost(self, model:str, n_tokens: int) -> str:
        self._validate_model(model)
        cost_per_token = self.MODELS_COST[model]
        getcontext().prec = 10
        result = round(Decimal(cost_per_token) * Decimal(n_tokens) * Decimal(10**(-8)), 7)
        return f"{result:.7f}"

    def is_model_supported(self, model: str) -> bool:
        return model in self.AVAILABLE_MODELS
    