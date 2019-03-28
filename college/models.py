from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Subject(models.Model):
    subject = models.CharField(max_length=15, null=False, unique=True)
    total_marks = models.IntegerField(default=0)
    total_classes = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.subject


class Semester(models.Model):
    semester = models.CharField(max_length=1, null=False, unique=True)

    def __str__(self):
        return self.semester


class Professor(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name.username


class SemesterSub(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    subject = models.OneToOneField(Subject, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return ("{}-{}").format(self.semester.semester, self.subject.subject)


class Student(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    usn = models.CharField(max_length=10, blank=False, null=True, unique=True)
    mobile = models.CharField(max_length=10, blank=False, null=True, unique=True)
    address = models.CharField(max_length=50, blank=False, null=True, unique=True)
    sem = models.ForeignKey(Semester, on_delete=models.CASCADE, null=True, blank=False)

    def __str__(self):
        return ("{} - {}").format(self.name.username, self.usn)


class BatchAdd(models.Model):
    batch_name = models.CharField(max_length=4, unique=True, null=False, blank=True)

    def __str__(self):
        return self.batch_name


class Batch(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    batch = models.ForeignKey(BatchAdd, on_delete=models.CASCADE)

    def __str__(self):
        return ("{} - {}").format(self.batch, self.student.name)


class Submarks(models.Model):
    subject = models.ForeignKey(SemesterSub, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    I = models.IntegerField(blank=True, null=True, default=0)
    II = models.IntegerField(blank=True, null=True, default=0)
    III = models.IntegerField(blank=True, null=True, default=0)
    attendence = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return ("{}-{}").format(self.student.usn, self.subject.subject)


class Assignments(models.Model):
    title = models.CharField(max_length=160, null=False, blank=False)
    assignment = models.FileField(upload_to='assignments/')
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now,blank = True)
    deadline = models.TextField(max_length=14)

    def __str__(self):
        return ("{} ").format(self.assignment)


class Review(models.Model):
    STATUS_CHOICES = {
        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)
    }
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=STATUS_CHOICES, default=1)
    feedback = models.TextField(max_length=160, blank=True, null=True)

    def __str__(self):
        return ("{}  Review = {}").format(self.professor, self.feedback)
