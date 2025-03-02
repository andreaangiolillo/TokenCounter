from abc import abstractmethod

class Tokenizer():

    @abstractmethod
    def calculate_cost(self, n_tokens: int) -> str:
        pass

    @abstractmethod
    def calculate_tokens(self, content: str) -> int:
        pass
    
    @abstractmethod
    def get_cost_per_token(self, model: str) -> str:
        pass
    
    @abstractmethod
    def get_available_models(self) -> list:
        pass
