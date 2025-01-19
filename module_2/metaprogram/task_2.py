

def create_class_with_methods(name: str, attributes: dict, methods: dict):
    
    return type(
    name,
    (),  
    {  
        '__doc__': 'This is demo of dynamic Class',  
        **attributes,
        **methods
    }  
)  



class_attributes = {'species':'Human', 'age':25}
class_methods = {'greet': lambda self: f"Hello, I am a {self.species} and I am {self.age} years old."}
DynamicClass = create_class_with_methods('DynamicClass', class_attributes, class_methods )

instance = DynamicClass()
print(instance.greet())