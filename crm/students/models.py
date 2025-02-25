from django.db import models # type: ignore
import datetime
import uuid

class BaseClass(models.Model):

    uuid = models.SlugField(unique=True,default=uuid.uuid4)

    active_status = models.BooleanField(default=True)

   

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta :

        abstract = True

# Create your models here.

class CourseChoices(models.TextChoices):
    
    PY_DJANGO = 'PY_DJANGO','PY_DJANGO'
    
    MERN ='MERN','MERN'
    
    DATA_SCIENCE = 'DATA_SCIENCE','DATA_SCIENCE'
    
    SOFTWARE_TESTING = 'SOFTWARE_TESTING','SOFTWARE_TESTING'
    
class DistrictChoices(models.TextChoices):
    
    THIRUVANANTHAPURAM = 'Thiruvananthapuram', 'Thiruvananthapuram'
    KOLLAM = 'Kollam', 'Kollam'
    PATHANAMTHITTA = 'Pathanamthitta', 'Pathanamthitta'
    ALAPPUZHA = 'Alappuzha', 'Alappuzha'
    KOTTAYAM = 'Kottayam', 'Kottayam'
    IDUKKI = 'Idukki', 'Idukki'
    ERNAKULAM = 'Ernakulam', 'Ernakulam'
    THRISSUR = 'Thrissur', 'Thrissur'
    PALAKKAD = 'Palakkad', 'Palakkad'
    MALAPPURAM = 'Malappuram', 'Malappuram'
    KOZHIKODE = 'Kozhikode', 'Kozhikode'
    WAYANAD = 'Wayanad', 'Wayanad'
    KANNUR = 'Kannur', 'Kannur'
    KASARAGOD = 'Kasaragod', 'Kasaragod'

class BatchChoices(models.TextChoices):
    
    PY_NOV_2024 ='PY-NOV-2024','PY-NOV-2024'
    
    MERN_NOV_2024 ='MERN_NOV_2024 ','MERN_NOV_2024'
    
    PY_JAN_2025 ='PY_JAN_2025','PY_JAN_2025'
    
    DS_JAN_2025 ='DS_JAN_2025','DS_JAN_2025'
    
    ST_JAN_2025='ST_JAN_2025','ST_JAN_2025'
    
    MERN_JAN_2025 ='MERN_JAN_2025','MERN_JAN_2025'
    
class TrainerChoices(models.TextChoices):
    
     ANZIL_NAZER ='ANZIL_NAZER','ANZIL_NAZER'
     
     SARATH_LAL='SARATH_LAL','SARATH_LAL'
     
     ALAKHANANDA_M_N='ALAKHANANDA_M_N','ALAKHANANDA_M_N'
     
     RAHUL_MOHANAKUMAR='RAHUL_MOHANAKUMAR','RAHUL_MOHANAKUMAR'
     
     JIMITHA_SAM =' JIMITHA_SAM',' JIMITHA_SAM'
    
class Students(BaseClass):
    
    # personal details fields:
    
    profile =models.OneToOneField('authentication.profile',on_delete=models.CASCADE)
    
    first_name = models.CharField(max_length=50)
    
    last_name = models.CharField(max_length=50)
    
    photo =models.ImageField(upload_to='students')
    
    email = models.EmailField(unique=True)
    
    contact_num = models.CharField(max_length=50)
    
    house_name = models.CharField(max_length=200)
    
    post_office = models.CharField(max_length=100)
    
    district = models.CharField(max_length=50,choices=DistrictChoices.choices)
    
    pincode = models.CharField(max_length=6)
    
    
    # course details
    
    adm_num = models.CharField(max_length=50)
    
    # default =course_choice.pydjango
    
    # course = models.CharField(max_length=50,choices=CourseChoices.choices)
    course = models.ForeignKey('courses.Courses',null=True,on_delete=models.SET_NULL)
    # batch = models.CharField(max_length=50,choices=BatchChoices.choices)
    
    join_date = models.DateField(auto_now_add=True) 
    
    batch = models.ForeignKey('batches.Batches',null=True,on_delete=models.SET_NULL)
    
    trainer = models.ForeignKey('trainers.Trainers',null=True,on_delete=models.SET_NULL)
    
    
    # trainer_name = models.CharField(max_length=50,choices=TrainerChoices.choices)
    
    
    def __str__(self):
        
        return f'{self.first_name} {self.last_name} {self.batch}'
    
    class Meta:
        #representation changed by using this section
        
        verbose_name = 'Students'
        
        verbose_name_plural ='Students'
        
        #ordering used to define added data in id order ascending, -id used to set in descending order
        
        ordering=['id']
        

        

    
    