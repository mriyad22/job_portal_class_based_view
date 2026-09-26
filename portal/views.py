from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView
from .models import *
from .forms import *

# Create your views here.


# ========================================================= 
# USER REGISTER 
# =========================================================

class UserRegisterView(View):
    def get(self, request):
        form_data = RegisterForm()

        con = {
            "data" : form_data
        }
        return render(request, 'auth/register.html', con)
    

    def post(self, request):
        form_data = RegisterForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            messages.success(request, 'Register successfully')
            return redirect('login_page')


        con = {
            'data' : form_data
        }

        return render(request, 'auth/register.html', con)



# ========================================================= 
# USER LOGIN 
# =========================================================

class UserLoginView(View):
    def get(self, request):
        form_data = LoginForm()

        con = {
            "data" : form_data
        }

        return render(request, 'auth/login.html', con)


    def post(self, request):
        form_data = LoginForm(request, request.POST)
        if form_data.is_valid():
            user = form_data.get_user()
            if user:
                login(request, user)
                messages.success(request, "Thanks for logged in")
                return redirect('home')

        con = {
            "data" : form_data
        }
        return render(request, 'auth/login.html', con)



# =========================================================
#  LOGOUT 
# =========================================================

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('login_page')




# =========================================================
#  HOME PAGE
# =========================================================

class HomePageView(TemplateView):
    template_name = "home.html"



# =========================================================
#  DISPLAY PROFILE
# =========================================================

class DisplayProfileView(LoginRequiredMixin, TemplateView):
    template_name  = "profile.html"



# =========================================================
#  USER PROFILE UPDATE
# =========================================================

class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.user_type == 'Recruiter':
            try:
                user_data = request.user.recruiter_profile
            except RecruiterProfileModel.DoesNotExist:
                user_data = None
            form_data = RecruiterProfileForm(instance = user_data)

        else:
            try:
                user_data = request.user.seeker_profile
            except SeekerProfileModel.DoesNotExist:
                user_data = None
            form_data = SeekerProfileForm(instance = user_data)

        con = {
            'data' : form_data,
            "title" : "profile update",
            "btn" : "Update"
        }
        return render(request, 'job/forms.html', con)



    def post(self, request):
        if request.user.user_type == 'Recruiter':
            try:
                user_data = request.user.recruiter_profile
            except RecruiterProfileModel.DoesNotExist:
                user_data = None

            form_data = RecruiterProfileForm(request.POST, request.FILES, instance = user_data)
            if form_data.is_valid():
                data = form_data.save(commit=False)
                data.recruiter = request.user
                data.save()
                messages.success(request, 'Profile Updated')
                return redirect('profile')

        else: 
            try:
                user_data = request.user.seeker_profile
            except SeekerProfileModel.DoesNotExist:
                user_data = None

            if request.method == 'POST':
                form_data = SeekerProfileForm(request.POST, request.FILES, instance = user_data)
                if form_data.is_valid():
                    data = form_data.save(commit=False)
                    data.seeker = request.user
                    data.save()
                    messages.success(request, 'Profile Updated')
                    return redirect('profile')

        con = {
            'data' : form_data
        }

        return render(request, 'job/forms.html', con)



# =========================================================
#  JOB POST
# =========================================================

class JobPostView(LoginRequiredMixin, View):
    def get(self, request):
        form_data = JobPostForm()

        con = {
            "data" : form_data,
            "title" : "Job Post",
            "btn" : "Post"
        }
        return render(request, 'job/forms.html', con)


    def post(self, request):
        form_data = JobPostForm(request.POST)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.posted_by = request.user.recruiter_profile
            data.save()
            messages.success(request, 'Job has been posted.')
            return redirect('jb_list')

        con = {
            "data" : form_data
        }
        return render(request, 'job/forms.html', con)



# =========================================================
#  UPDATE JOB
# =========================================================

class UpdateJobView(LoginRequiredMixin, View):
    def get(self, request, u_id):
        update_id = get_object_or_404(JobPostModel, id = u_id)
        form_data = JobPostForm(instance = update_id)
    
        con = {
            "data" : form_data,
            "title" : "job update",
            "btn" : "Update"
        }
        return render(request, 'job/forms.html', con)

    
    def post(self, request, u_id):
        update_id = get_object_or_404(JobPostModel, id = u_id)
        form_data = JobPostForm(request.POST, request.FILES, instance = update_id)
        if form_data.is_valid():
            form_data.save()
            messages.success(request, "job updated")
            return redirect("jb_list")
        
        con = {
        "data" : form_data,
        "title" : "job update",
        "btn" : "Update"
        }

        return render(request, "job/form.html", con)


# =========================================================
#  DELETE JOB
# =========================================================

class DeleteJobView(LoginRequiredMixin, View):
    def get(self, request, d_id):
        if request.user.user_type == "Recruiter":
            delete_id = get_object_or_404(JobPostModel, id = d_id)
            delete_id.delete()
            return redirect("jb_list")



# =========================================================
#  DISPLAY JOBS
# =========================================================

class DisplayJobsView(ListView):
    model = JobPostModel
    template_name = "job/jb-list.html"

    context_object_name = "data"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.user_type == "Recruiter":
                return JobPostModel.objects.filter(posted_by = self.request.user.recruiter_profile)
            else:
                return JobPostModel.objects.all()

        return JobPostModel.objects.all()




# def jb_list(request):
#     if request.user.is_authenticated:
#         if request.user.user_type == 'Recruiter':
#             data = JobPostModel.objects.filter(posted_by = request.user.recruiter_profile)
#         else:
#             data = JobPostModel.objects.all()
#     else:
#         data = JobPostModel.objects.all()

#     con = {
#         'data' : data
#     }


#     return render(request, 'job/jb-list.html', con)





# =========================================================
#  JOB APPLY
# =========================================================

class JobApplyView(LoginRequiredMixin, View):
    def get(self, request, a_id):
        if request.user.user_type != "Seeker":
            messages.error(request, "You must be a Seeker.")
            return redirect("jb_list")

        applied_id = get_object_or_404(JobPostModel, id=a_id)
        form_data = ApplyJobForm()

        con = {
            "data": form_data,
            "title": "Apply Job",
            "btn": "Apply",
            "job": applied_id
        }
        return render(request, 'job/forms.html', con)


    def post(self, request, a_id):
        appied_id = get_object_or_404(JobPostModel, id = a_id)

        if request.user.user_type != "Seeker":
            messages.error(request, "You must be a Seeker.")
            return redirect("jb_list")

        form_data = ApplyJobForm(request.POST, request.FILES)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.applied_by = request.user.seeker_profile
            data.apply_to = appied_id
            data.save()
            messages.success( request, "Thanks for applying" )
            return redirect('jb_list')

    
        con = {
            'data' : form_data
        }
        return render(request, 'job/forms.html', con)





# =========================================================
#  CANDIDATE LIST
# =========================================================

class CandidateView(ListView):
    model = ApplyJobModel
    template_name = "job/candidate.html"
    context_object_name = "data"

    def get_queryset(self):
        job = get_object_or_404(
            JobPostModel,
            id = self.kwargs["c_id"]
        )

        return ApplyJobModel.objects.filter(apply_to = job)




# def candidate(request, c_id):
#     apply = get_object_or_404(JobPostModel, id = c_id)
#     data = ApplyJobModel.objects.filter(apply_to = apply)

#     con = {
#         'data' : data
#     }


#     return render(request, 'job/candidate.html', con )