from django.urls import path
from .import views

urlpatterns = [
    
    path('student-payment-details/',views.StudentPaymentView.as_view(),name='student-payment-details'),
    
    path('razor-pay-view/',views.RazorPayView.as_view(),name='razor-pay-view'),
    
    path('payment-verify/',views.RazorPayView.as_view(),name='payment-verify'),
]


#password
#nzXKphOx
