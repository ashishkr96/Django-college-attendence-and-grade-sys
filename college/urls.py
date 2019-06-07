from django.urls import path
from college import views

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('excel-data-export/', views.excel_data_export, name='excel-data'),
    path('student-reg/', views.studentreg, name='student-reg'),
    path('bulk-add/', views.addbatch, name='bulk-add'),
    path('batch-list/', views.batch_list, name='batch-list'),
    path('batch-update-form/', views.updateprocess, name='update-process'),
    path('batch-list/update/', views.updatebatch, name='update-batch'),
    path('semester-list/', views.semesterlist, name='semester-list'),
    path('semester-detail/', views.semesterdetail, name='semester-detail'),
    path('student-list/', views.batch_detail, name='student-list'),
    path('assignment-add/', views.assignmentadd, name='assignment-add'),
    path('professor-review/', views.professorreview, name='professor-review'),
    path('create-batch/', views.create_batch, name='create-batch'),
    path('add-student-batch/', views.add_student_batch, name='add-student-batch'),
    path('student-add/', views.create_marks, name='student-add'),
    path('student-detail/', views.student_display, name='student-detail'),
    path('student/<int:id>/edit/', views.studentupdate, name='update-student'),
    path('student-batch/<int:id>/delete/', views.studentdelete, name='student-delete-batch'),
    path('batch/<int:id>/delete/', views.deletebatch, name='delete-batch'),
    path('professor-page/', views.professor_display, name='professor-page'),
    path('reset-record-confirmation/', views.reset_confirmation, name='reset-confirmation'),
    path('reset-record/', views.reset_all, name='reset-record'),
    path('login/', views.login_user, name='login'),
    path('student-detail/<int:id>/delete/', views.delete_student_record, name='delete-student'),
    path('send-sms/<int:id>/send/', views.sendsms, name='send-sms'),
    path('assignment/<int:id>/delete/', views.delete_assignment, name='delete-assignment'),
    path('logout/', LogoutView.as_view(template_name='college/logout.html'), name='logout'),

]
