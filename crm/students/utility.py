import uuid
import string
import random

from .models import Students

def get_admission_number():
    
    while True:
        
        pattern=str(uuid.uuid4().int)[:7]
        
        admission_number =f'LM-{pattern}'
        
        if not Students.objects.filter(adm_num = admission_number).exists():
            
            return admission_number
        
def get_password():
    
    password = ''.join(random.choices(string.ascii_letters+string.digits,k=8))
    
    return password
    
