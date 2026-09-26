from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserModel(AbstractUser):
    USER_CHOICH = [
        ('Recruiter', 'Recruiter'),
        ('Seeker', 'Seeker')
    ]

    display_name = models.CharField(max_length=255, null=True)
    user_type = models.CharField(max_length=100, choices=USER_CHOICH, null=True)

    def __str__(self):
        return f'{self.username}'
    


class RecruiterProfileModel(models.Model):
    company_name = models.CharField(max_length=255, null=True)
    logo = models.ImageField(upload_to='cmp_logo', null=True)
    address = models.TextField()
    phone = models.CharField(max_length=15, null=True)
    recruiter = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        related_name='recruiter_profile',
        null=True
    )

    def __str__(self):
        return f"{self.company_name}"
    


class SeekerProfileModel(models.Model):
    image = models.ImageField(upload_to='skr_img', null=True)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    seeker = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        related_name='seeker_profile',
        null=True
    )
    def __str__(self):
        return f"{self.seeker.display_name}"
    



class CategoryModel(models.Model):
    cate_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.cate_name
    

class JobPostModel(models.Model):
    SHIFT = [
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Remote', 'Remote')
    ]
    
    title = models.CharField(max_length=255, null=True)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, related_name='ch_category', null=True)
    description = models.TextField()
    skills = models.TextField()
    shift = models.CharField(max_length=100, choices=SHIFT, default='Full Time', null=True)
    opening = models.PositiveBigIntegerField(null=True)
    salary = models.FloatField(null=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    deadline = models.DateField(null=True)
    posted_by = models.ForeignKey(
        RecruiterProfileModel,
        on_delete=models.CASCADE,
        related_name='rec_job_post',
        null=True
    )

    def __str__(self):
        return f'{self.posted_by.company_name} - {self.title}'



class ApplyJobModel(models.Model):
    applied_at = models.DateField(auto_now_add=True)
    resume = models.FileField(upload_to='resume', null=True)

    applied_by = models.ForeignKey(
        SeekerProfileModel,
        on_delete=models.CASCADE,
        related_name='seeker_job_apply',
        null=True
    )

    apply_to = models.ForeignKey(
        JobPostModel,
        on_delete=models.CASCADE,
        related_name='applied',
        null=True
    )

    def __str__(self):
        return f'{self.applied_by.seeker.display_name}'


