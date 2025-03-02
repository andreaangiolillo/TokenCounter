import tiktoken
from tokenizers.tokenizer import Tokenizer

class TokenUsageCalculator(Tokenizer):
    AVAILABLE_MODELS = ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"]
    
    """ 
    Site: https://platform.openai.com/docs/pricing
    Update date: 02/03/2025 
    Prices are stored in dollars and represented in cents (1 dollar = 100 cents).
    After performing calculations, results must be converted back to the original unit by multiplying by 10^(-6).
    """
    MODELS_COST = {"gpt-4o": 250, "gpt-4o-mini": 15, "gpt-4-turbo": 1000, 
                   "gpt-4": 30000, "gpt-4-32k": 60000, "gpt-3.5-turbo": 50,
                   "o1": 15000, "o1-mini": 110, "o3-mini": 110}
    
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
        print(f"content: {content}")
        if content:
            self._validate_model(model)
            encoding = tiktoken.encoding_for_model(model)
            return len(encoding.encode(content))

        return 0
    
    """Returns an estimate of the cost associated with the token in input"""
    def calculate_cost(self, model:str, n_tokens: int) -> str:
        self._validate_model(model)
        cost_per_token = self.MODELS_COST[model]
        return str(cost_per_token * n_tokens * 10**(-6))



    def is_model_supported(self, model: str) -> bool:
        return model in self.AVAILABLE_MODELS
    
