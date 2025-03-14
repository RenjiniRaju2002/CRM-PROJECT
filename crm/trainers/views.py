from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.db import transaction
from .models import Trainers
from .forms import TrainerRegisterForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from authentication.permissions import permission_roles
from django.db.models import Q
from .utility import get_trainer_id ,get_trainer_password
from authentication.models import Profile



class GetTrainerObject:
    
    def get_trainer(self, request, uuid):
        
        try:
            
            trainer = Trainers.objects.get(uuid=uuid)
            
            return trainer
        
        except Trainers.DoesNotExist:
            
            return None

@method_decorator(permission_roles(roles=['Admin', 'Sales','Academic counselor']), name='dispatch')

class TrainerListView(View):
    
    def get(self, request, *args, **kwargs):
        
        trainers = Trainers.objects.filter(active_status=True)
        
        query = request.GET.get('query')
        
        if query:
            
            trainers = trainers.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(email__icontains=query)
            )
        
        return render(request, 'trainers/trainer.html', {'trainers': trainers, 'query': query})


@method_decorator(permission_roles(roles=['Admin', 'Sales','Academic counselor']), name='dispatch')

class TrainerRegistrationView(View):

    def get(self, request, *args, **kwargs):
        
        form = TrainerRegisterForm()
        
        return render(request, 'trainers/registration.html', {'form': form})

    def post(self, request, *args, **kwargs):
        
        form = TrainerRegisterForm(request.POST, request.FILES)

        if form.is_valid():
            
            with transaction.atomic():
                
                trainer = form.save(commit=False)

                
                trainer.employee_id = get_trainer_id()

                
                username = trainer.email
                
                password = get_trainer_password()
                
                print(password)  

                
                profile = Profile.objects.create_user(username=username, password=password, role='Trainer')
                
                trainer.profile = profile  

                trainer.save()  

            return redirect('trainer-list')
        else:
            return render(request, 'trainers/registration.html', {'form': form})



@method_decorator(permission_roles(roles=['Admin','Sales','Academic counselor']), name='dispatch')

class TrainerDetailView(View):
    
    def get(self, request, uuid, *args, **kwargs):
        
        trainer = GetTrainerObject().get_trainer(request, uuid)
        
        if not trainer:
            
            return render(request, 'errorpages/error-404.html')
        
        return render(request, 'trainers/trainer-detail.html', {'trainer': trainer})


@method_decorator(permission_roles(roles=['Admin', 'Sales','Academic ']), name='dispatch')

class TrainerUpdateView(View):
    
    def get(self, request, uuid, *args, **kwargs):
        
        trainer = GetTrainerObject().get_trainer(request, uuid)
        
        if not trainer:
            
            return render(request, 'errorpages/error-404.html')
        
        form = TrainerRegisterForm(instance=trainer)
        
        return render(request, 'trainers/trainer-update.html', {'form': form})

    def post(self, request, uuid, *args, **kwargs):
        
        trainer = GetTrainerObject().get_trainer(request, uuid)
        
        if not trainer:
            
            return render(request, 'errorpages/error-404.html')
        
        form = TrainerRegisterForm(request.POST, request.FILES, instance=trainer)
        
        if form.is_valid():
            
            form.save()
            
            return redirect('trainer-list')
        
        return render(request, 'trainers/trainer-update.html', {'form': form})


@method_decorator(permission_roles(roles=['Admin','Sales','Academic counselor']), name='dispatch')

class TrainerDeleteView(View):
    
    def get(self, request, uuid, *args, **kwargs):
        
        trainer = GetTrainerObject().get_trainer(request, uuid)
        
        if trainer:
            
            trainer.active_status = False
            
            trainer.save()
            
        return redirect('trainer-list')

