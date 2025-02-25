from django.shortcuts import render,redirect ,get_list_or_404# type: ignore
from django.views.generic import View # type: ignore
from .models import DistrictChoices,CourseChoices,BatchChoices,TrainerChoices
from .utility import get_admission_number,get_password
from .models import Students
from .forms import StudentRegisterform
from django.db.models import Q
from authentication.models import Profile
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from authentication.permissions import permission_roles

# Create your views here.

class GetStudentObject:

    def get_student(self,request,uuid):

        
        try:
            
            student = Students.objects.get(uuid=uuid)

            return student

        except:

            return render(request,'errorpages/error-404')
        
# @method_decorator(login_required(login_url='login'),name='dispatch')
# @method_decorator(permission_roles(roles=['Admin','Sales']),name='dispatch')
class DashboardView(View):
    
    def get(self,request,*args,**kwargs):
        
        
        
        return render(request,'students/dashboard.html')
# @method_decorator(permission_roles(roles=['Admin','Sales','Trainer','Academic counselor']),name='dispatch')
class StudentsView(View):
    
    def get(self,request,*args,**kwargs):
        # students =Students.objects.all()
        # print(students)
        
        query=request.GET.get('query')
        
        students =Students.objects.filter(active_status =True)
        
        if query:
            
            students = Students.objects.filter(Q(active_status = True)& (Q(first_name__icontains=query)|Q(last_name__icontains =query)|Q(adm_num__icontains=query)|Q(contact_num__icontains=query)|Q(house_name__icontains=query)|Q(post_office__icontains=query)|Q(pincode__icontains=query|Q(course__code__icontains=query))))
            
        
        
        data ={'students':students,'query':query}
        
        return render(request,'students/students.html',context=data)
    
@method_decorator(permission_roles(roles=['Admin','Sales']),name='dispatch')  
class CourseView(View):
    
    def get(self,request,*args,**kwargs):
        
        return render(request,'students/course.html')
    
@method_decorator(permission_roles(roles=['Admin','Sales']),name='dispatch') 
class StudentRegistrationView(View):
    
    def get(self,request,*args,**kwargs):
        
      
        
        form = StudentRegisterform
        
        # data = {'districts':DistrictChoices,'courses':CourseChoices,'batches':BatchChoices,'trainers':TrainerChoices,'forms':form}
        
        data ={'forms':form}
        return render(request,'students/course.html',context=data)
    
    def post(self,request,*args,**kwargs):
        
        form = StudentRegisterform(request.POST,request.FILES)
        
        if form.is_valid():
            
            with transaction.atomic():
            
                student = form.save(commit=False)
                
                student.adm_num =get_admission_number()
                
                username = student.email
                
                password =get_password()
                
                print(password)
                
                profile = Profile.objects.create_user(username=username,password=password,role='Student')
                
                student.profile = profile
                
                student.save()
            
            return redirect('students-list')
        else:
            data ={'forms':form}
            return render(request,'students/course.html',context=data)
            
    #     form_data =request.POST
        
    #     first_name = form_data.get('first_name')
    #     last_name = form_data.get('last_name')
    #     photo = request.FILES.get('photo')
    #     email = form_data.get('email')
    #     contact_number = form_data.get('contact_number')
    #     house_name = form_data.get('house_name')
    #     post_office = form_data.get('post_office')
    #     districts = form_data.get('districts')
    #     pin_code = form_data.get('pin_code')
    #     course= form_data.get('course')
    #     batch = form_data.get('batch')
    #     batch_date = form_data.get('batch_date')
    #     trainer = form_data.get('trainer')
        
    #     adm_num = get_admission_number()
        
    #     join_date ='2024-08-16'
         
    #     Students.objects.create(first_name=first_name,
    #                             last_name =last_name,
    #                             photo=photo,
    #                             email=email,
    #                             contact_num=contact_number,
    #                             house_name=house_name,
    #                             post_office=post_office,
    #                             district =districts,
    #                             pincode=pin_code,
    #                             adm_num=adm_num,
    #                             course=course,
    #                             batch=batch,
    #                            join_date=join_date,
    #                             trainer_name =trainer)
        
    #     print(adm_num)
        
    #     print(first_name)
    #     print(last_name)
    #     print(photo)
    #     print(email)
    #     print(contact_number)
    #     print(house_name)
    #     print(post_office)
    #     print(districts)
    #     print(pin_code)
    #     print(course)
    #     print(batch)
    #     print(batch_date)
    #     print(trainer)
    
@method_decorator(permission_roles(roles=['Admin','Sales','Trainer','Academic counselor']),name='dispatch')        
class StudentDetailView(View) :
    
    def get(self,request,*args,**kwargs):
        
        uuid= kwargs.get('uuid')
        
        # student = get_list_or_404(Students,pk=pk)
        
        student =GetStudentObject().get_student(request,uuid)
        data ={'student':student}
        
        return render(request,"students/student-detail.html",context=data)
    
    
    # error view
    
# class Error404View(View):
    
#     def get(self,request,*args,**kwargs):
        
#         return render(request,'students/error-404.html')

# student delete view
@method_decorator(permission_roles(roles=['Admin','Sales']),name='dispatch') 
class StudentDeleteView(View):
    
    def get(self,request,*args,**kwargs):
        
        uuid = kwargs.get('uuid')
        
      
            
        student = Students.objects.get(uuid=uuid)
        
        student.active_status =False
        
        student.save()
            
       
        
        # student.delete()
        
        return redirect('students-list')
    
@method_decorator(permission_roles(roles=['Admin','Sales']),name='dispatch')    
class StudentUpdateView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        student=GetStudentObject().get_student(request,uuid)

        form = StudentRegisterform(instance=student)

        data={'form':form}

        return render (request,'students/student-update.html',context=data)  

    def post(self,request,*args,**kwargs):

        uuid=kwargs.get('uuid')

        student = GetStudentObject().get_student(request,uuid)

        form=StudentRegisterform(request.POST,request.FILES,instance=student)

        if form.is_valid():

            form.save()

            return redirect('students-list')

        else:
            
            data={'form':form}

            return render(request,'students/student-update.html')
        

