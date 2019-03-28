from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.db import IntegrityError
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import heapq
import statistics
from work import settings
import xlwt
import requests
import json

URL = 'http://www.way2sms.com/api/v1/sendCampaign'


# Create your views here.


def index(request):
    a = Assignments.objects.all().order_by('-id')
    context = {
        'a': a,
    }
    return render(request, 'college/index.html', context)


@login_required
def studentreg(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = UserRegForm(request.POST)
            s_form = StudentRegForm(request.POST)
            if form.is_valid() and s_form.is_valid():
                k = form.save()
                print(k)
                usn = s_form.cleaned_data['usn']
                mobile = s_form.cleaned_data['mobile']
                address = s_form.cleaned_data['address']
                sem = s_form.cleaned_data['sem']
                s = Student.objects.create(name=k, usn=usn, mobile=mobile, address=address, sem=sem)
                s.save()
                messages.success(request, f'All set,You can now Log In your account')
                return HttpResponseRedirect(reverse('student-reg'))
            else:
                messages.warning(request, f'USN or Address or mobile number already exists')
                return HttpResponseRedirect(reverse('student-reg'))
        else:
            form = UserRegForm()
            s_form = StudentRegForm()

        context = {
            'form': form,
            'sform': s_form,

        }
        return render(request, 'college/user_reg_form.html', context)
    else:
        return HttpResponseRedirect(reverse('index'))


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))


        else:
            messages.warning(request, f'Username or Password is incorrect')
            return HttpResponseRedirect(reverse('login'))
    else:
        form = LoginForm()
        context = {
            'form': form,
        }
        return render(request, 'college/login.html', context)


@login_required
def student_display(request):
    if request.user.is_staff:
        return HttpResponseRedirect(reverse('professor-page'))

    else:
        s = Student.objects.get(name=request.user)
        student = Submarks.objects.filter(student=s)
        k = []
        for subject in student:
            avg = [subject.I, subject.II, subject.III]

            k.append(statistics.mean(heapq.nlargest(2, avg)))

        context = {
            'students': student,
            'avg': k,
            's': s,
        }
        return render(request, 'college/student_detail.html', context)


def create_marks(request):
    if request.user.is_staff:
        s = Professor.objects.get(name=request.user)

        if request.method == 'POST':
            form = CreateSubmark(request.POST)
            if form.is_valid():
                sem = form.cleaned_data['subject']
                if sem.professor == s:
                    form.save()
                    messages.success(request, f'student entry succesfully created.')
                    return HttpResponseRedirect(reverse('professor-page'))
                else:
                    messages.warning(request,
                                     f'You are not teaching this subject contact the professor taking this subject')
                    return HttpResponseRedirect(reverse('student-add'))
        else:
            form = CreateSubmark()
        context = {
            's_form': form,
        }
        return render(request, 'college/semesteradd.html', context)


@login_required
def professor_display(request):
    if request.user.is_staff:
        s = Professor.objects.get(name=request.user)
        prof = SemesterSub.objects.filter(professor=s)
        student_list = []
        for subject in prof:
            student_list.append(Submarks.objects.filter(subject=subject))

        context = {
            'students': student_list,
            'prof': prof,
        }
        return render(request, 'college/students_particular.html', context)
    else:
        return HttpResponseRedirect(reverse('student-detail'))


@login_required
def edit_student(request, id):
    if request.user.is_staff:
        ind = get_object_or_404(Submarks, id=id)
        if request.method == 'POST':
            form = MarksForm(request.POST, instance=ind)
            if form.is_valid():
                form.save()
                messages.success(request, f'Record updated sucessfully')
                return HttpResponseRedirect(reverse('professor-page'))
        else:
            form = MarksForm(instance=ind)
        context = {
            'form': form,
            'student': ind,
        }
        return render(request, 'college/attendencegrades.html', context)


@login_required
def assignmentadd(request):
    if request.user.is_staff:
        p = Professor.objects.get(name=request.user)
        if request.method == 'POST':
            form = AddAssignment(request.POST, request.FILES)
            if form.is_valid():
                assignment = form.cleaned_data['assignment']
                title = form.cleaned_data['title']
                deadline = form.cleaned_data['deadline']
                a = Assignments.objects.create(title=title, assignment=assignment, professor=p, deadline=deadline)
                a.save()
                messages.success(request, f'Assignment updated sucessfully')
                return HttpResponseRedirect(reverse('index'))
        else:
            form = AddAssignment()

        context = {
            'form': form,
        }
        return render(request, 'college/assignmentadd.html', context)
    else:
        return HttpResponseRedirect(reverse('student-detail'))


def professorreview(request):
    if not request.user.is_staff:

        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, f'Review added sucessfully')
                return HttpResponseRedirect(reverse('professor-review'))

        else:
            form = ReviewForm()
        context = {
            'form': form,
        }
        return render(request, 'college/rating.html', context)
    else:
        return HttpResponseRedirect(reverse('assignment-add'))


def delete_student_record(request, id):
    if request.user.is_staff:
        Submarks.objects.filter(id=id).delete()
        messages.success(request, f'Record deleted sucessfully')
        return HttpResponseRedirect(reverse('professor-page'))


def delete_assignment(request, id):
    if request.user.is_staff:
        assign = Assignments.objects.get(id=id)
        if request.user == assign.professor.name:
            Assignments.objects.filter(id=id).delete()
            messages.success(request, f'Assignment deleted sucessfully')
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.warning(request, f'Only the subject professor can delete assignment')
            return HttpResponseRedirect(reverse('index'))


def sendsms(request, id):
    if request.user.is_staff:
        studentmark = Submarks.objects.get(id=id)
        subject = studentmark.subject.subject.subject
        IA1 = str(studentmark.I)
        IA2 = str(studentmark.II)
        IA3 = str(studentmark.III)
        attendence = str(studentmark.attendence)
        student_name = studentmark.student.name.username
        student_usn = studentmark.student.usn
        student_number = str(studentmark.student.mobile)
        total_attendence = str(studentmark.subject.subject.total_classes)
        req_params = {
            'apikey': settings.WAY2SMS_API_KEY,
            'secret': settings.WAY2SMS_SECRET,
            'usetype': 'stage',
            'phone': student_number,
            'message': 'This is attendence and marks report of ' + student_name + ' with USN ' + student_usn + '.\n He has attended ' + attendence +
                       ' out of ' + total_attendence + ' classes in SUBJECT : ' + subject + '\n First Internal marks : ' + IA1 + '\nSecond Internal Marks :'
                       + IA2 + '\nThird Internal Marks : ' + IA3 + '\n HMSIT ,Tumakuru',
            'senderid': 'WAYSMS'
        }
        resp = requests.post(URL, req_params)
        print(resp.text)
        messages.success(request, f'message sent sucessfully')
        return HttpResponseRedirect(reverse('professor-page'))


def reset_confirmation(request):
    if request.user.is_staff:
        return render(request, 'college/reset_warning.html')
    else:
        return HttpResponseRedirect(reverse('index'))


def reset_all(request):
    if request.user.is_staff:
        s = Professor.objects.get(name=request.user)
        prof = SemesterSub.objects.filter(professor=s)
        if prof:
            if request.method == 'POST':
                for subject in prof:
                    Submarks.objects.filter(subject=subject).delete()
                messages.success(request, f'All records deleted sucessfully')
                return HttpResponseRedirect(reverse('professor-page'))
        else:
            messages.info(request, f'Records are already empty')
            return HttpResponseRedirect(reverse('professor-page'))




    else:
        return HttpResponseRedirect(reverse('student-detail'))


def updateprocess(request):
    if request.user.is_staff:
        return render(request, 'college/batchupdate.html')
    else:
        return HttpResponseRedirect(reverse('index'))


def deletebatch(request, id):
    if request.user.is_staff:
        if request.method == 'POST':
            batch = BatchAdd.objects.get(id=id).delete()
            messages.success(request, f'Batch deleted sucessfully')
            return HttpResponseRedirect(reverse('batch-list'))
    else:
        return HttpResponseRedirect(reverse('index'))


def updatebatch(request):
    if request.user.is_staff:
        batch = request.POST.get('batch')
        sem = request.POST.get('sem')
        students = Batch.objects.filter(batch=batch)
        for student in students:
            student.student.sem = sem
        messages.success(request, f'Batch updated successfully')
        return HttpResponseRedirect(reverse('batch-list'))
    else:
        return HttpResponseRedirect(reverse('index'))


def addbatch(request):
    if request.user.is_staff:

        if request.method == 'POST':

            s = Professor.objects.get(name=request.user)
            batch = request.POST.get('batch')
            batch = BatchAdd.objects.get(batch_name=batch)

            subj = request.POST.get('sub')

            try:
                subject = SemesterSub.objects.get(subject__subject__iexact=subj)

                batch_list = []
                batch_list = Batch.objects.filter(batch__exact=batch)
                if batch_list:
                    if subject.professor == s:
                        for batch in batch_list:
                            Submarks.objects.create(subject=subject, student=batch.student)
                        messages.success(request, f'Students record created sucessfully')
                        return HttpResponseRedirect(reverse('professor-page'))
                    else:
                        messages.warning(request,
                                         f'You are not teaching this subject contact the professor taking this subject')
                        return HttpResponseRedirect(reverse('bulk-add'))
                else:
                    messages.warning(request, f'Pls type batch year properly or no batch exist with that year')
                    return HttpResponseRedirect(reverse('bulk-add'))




            except Exception:
                messages.warning(request, f'Pls check the subject name properly or subject does not exists')
                return HttpResponseRedirect(reverse('bulk-add'))




        else:
            return render(request, 'college/bulk_add_student.html')

    else:

        return HttpResponseRedirect(reverse('index'))


def create_batch(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = CreateBatch(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, f'Batch sucessfully created')
                return HttpResponseRedirect(reverse('professor-page'))
        else:
            form = CreateBatch()
        context = {
            'form': form,
        }
        return render(request, 'college/createbatch.html', context)
    else:
        return HttpResponseRedirect(reverse('index'))


def add_student_batch(request):
    if request.user.is_staff:
        if request.method == 'POST':
            try:
                batch = request.POST.get('batch')
                batch = BatchAdd.objects.get(batch_name=batch)
                student_list = []
                usn = request.POST.get('usn')
                student_list = Student.objects.filter(usn__istartswith=usn)
                if student_list:
                    for student in student_list:
                        Batch.objects.create(batch=batch, student=student)
                    messages.success(request, f'Students sucessfully added to batch')
                    return HttpResponseRedirect(reverse('professor-page'))
                else:
                    messages.warning(request, f'Pls check USN or no students USN starts with this number')
                    return HttpResponseRedirect(reverse('add-student-batch'))
            except IntegrityError:
                messages.warning(request, f'Duplicate entry of batch or student is forbidden, Pls check batch list')
                return HttpResponseRedirect(reverse('add-student-batch'))
            except Exception:
                messages.warning(request, f'Batch not found,Pls check the batch number')
                return HttpResponseRedirect(reverse('add-student-batch'))
        else:
            return render(request, 'college/student_batch_add.html')
    else:
        return HttpResponseRedirect(reverse('index'))


def batch_list(request):
    batch = BatchAdd.objects.all()
    context = {
        'batch': batch,
    }
    return render(request, 'college/batchlist.html', context)


def batch_detail(request):
    if request.user.is_staff:
        if request.method == 'POST':
            b = request.POST.get('batch')

            batch = BatchAdd.objects.get(batch_name__iexact=b)

            student_list = Batch.objects.filter(batch=batch)

            context = {
                'students': student_list,
            }
            return render(request, 'college/student_list.html', context)
        else:
            return HttpResponseRedirect(reverse('batch-list'))
    else:
        return HttpResponseRedirect(reverse('index'))


def studentdelete(request, id):
    if request.user.is_staff:

        get_object_or_404(Batch, id=id).delete()
        messages.success(request, f'Student deleted successfully')
        return HttpResponseRedirect(reverse('batch-list'))

    else:
        return HttpResponseRedirect(reverse('index'))


def studentupdate(request, id):
    if request.user.is_staff:
        student = get_object_or_404(Student, id=id)

        if request.method == 'POST':

            form = StudentRegForm(request.POST, instance=student)
            if form.is_valid():
                form.save()
                messages.success(request, f'Student record updated successfully')
                return HttpResponseRedirect(reverse('batch-list'))
            else:
                messages.warning(request, f'Details not filled properly')
                return HttpResponseRedirect(reverse('batch-list'))
        else:
            form = StudentRegForm(instance=student)
            context = {
                'form': form,
            }
            return render(request, 'college/studentreg.html', context)
    else:
        return HttpResponseRedirect(reverse('index'))


def excel_data_export(request):
    sem = request.POST.get('sem')
    sem = Semester.objects.get(semester=sem)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="studentdata.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('student', cell_overwrite_ok=True)
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = []
    subsem = SemesterSub.objects.filter(semester=sem)
    subject_name = ['First Name', 'Last Name', 'USN']

    for i in subsem:
        subject_name.append(i.subject.subject)

    columns = subject_name
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    firstname = []
    lastname = []
    usn = []

    r = 1
    c = 0
    for subject in subsem:
        rows = Submarks.objects.filter(subject=subject)
        print(rows)
        for row in rows:
            firstname.append(row.student.name.first_name)
            lastname.append(row.student.name.last_name)
            usn.append(row.student.usn)

    firstname = remove_duplicates(firstname)
    lastname = remove_duplicates(lastname)
    usn = remove_duplicates(usn)
    r = 1

    for name in firstname:
        ws.write(r, c, name, font_style)
        r += 1

    c = 1
    r = 1
    for name in lastname:
        ws.write(r, c, name, font_style)
        r += 1

    c = 2
    r = 1
    for num in usn:
        ws.write(r, c, num, font_style)
        r += 1

    c = 2
    for subject in subsem:
        rows = Submarks.objects.all().filter(subject=subject)
        r = 1
        c += 1
        for row in rows:
            ws.write(r, c, row.attendence, font_style)
            r += 1

    wb.save(response)
    return response


def remove_duplicates(li):
    my_set = set()
    res = []
    for e in li:
        if e not in my_set:
            res.append(e)
            my_set.add(e)
    #
    return res


def semesterlist(request):
    semester = Semester.objects.all()
    context = {
        'semester': semester,
    }
    return render(request, 'college/semesterlist.html', context)


def semesterdetail(request):
    sem = request.POST.get('sem')
    print(sem)
    subjects = SemesterSub.objects.filter(semester=sem)
    context = {
        'subjects': subjects,
    }
    return render(request, 'college/semesterdetail.html', context)
