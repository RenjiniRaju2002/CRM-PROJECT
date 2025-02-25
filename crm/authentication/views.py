from django.shortcuts import render,redirect

from django .views .generic  import View

from django .contrib .auth .models import User

from .forms import LoginForm

from django.contrib.auth import authenticate ,login,logout

# Create your views here.

class LoginView(View):

    def get(self,request,*args,**kwags):

        form = LoginForm()

        data = {'form' : form}

        return render(request,'authentication/login.html',context=data)
    
    def post(self,request,*args,**kwargs):

        form = LoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data.get('username')

            password = form.cleaned_data.get('password')
            
            user = authenticate(username=username,password=password)
            
            print(user)

            if user:
                
                login(request,user)
                
                role =user.role
                
                if role in ['Admin','Sales']:
                    
                    return redirect ('dashboard')
                
                elif role in ['Academic counselor','Trainer']:
                    
                    return redirect('Student')
                
                elif role in['Student']:
                
                    return redirect('recordings')
            
          
                
        error ='user does not exist'
                
        data ={'form':form , 'error':error}
                
        return render(request,'authentication/login.html',context=data)
    
class LogoutView(View):
    
    def get(self,request,*args,**kwargs):
        
        logout(request)
        
        return redirect('login')
        
            
       