# context processor 

def show_user_name (request):
    
    username = request.user.username
    
    name = username.split('@')[0]
    
    print(name)
    
    return {'name_of_user':name}