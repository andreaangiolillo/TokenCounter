import os
import transformers
from token_usage_calculators.token_usage_calculator import Tokenizer

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
       
    """Returns the cost per single token"""
    def get_cost_per_token(self, model:str) -> str:
        self._validate_model(model)
        cost = self.MODELS_COST[model]
        return str(cost * 10**(-6))
    
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
    
    """Returns an estimate of the cost associated with the token in input"""
    def calculate_cost(self, model:str, n_tokens: int) -> str:
        self._validate_model(model)
        cost_per_token = self.MODELS_COST[model]
        return str(cost_per_token * n_tokens * 10**(-6))



    def is_model_supported(self, model: str) -> bool:
        return model in self.AVAILABLE_MODELS
    