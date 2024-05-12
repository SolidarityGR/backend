from uuid import uuid4

class Product:
    def __init__(self,
                 product_name:str,
                 quantity: int,
                 description: str,
                 photo: str,
                 location: str,
                 category: str,
                 user_rank: float,
                 username: str,
                 user_id: uuid4,                 
                 ) -> None:
        
        self.name = product_name
        
        self.price = quantity
        self.quantity = quantity
        self.description = description
        self.photo = photo
        self.location = location
        self.category = category
        self.user_rank = user_rank
        self.username = username
        self.user_id = user_id
