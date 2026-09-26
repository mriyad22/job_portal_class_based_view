from django.urls import path
from .views import *


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register_page'),
    path('login/', UserLoginView.as_view(), name='login_page'),
    path('logout/', LogoutView.as_view() , name='logout_page'),
    path('', HomePageView.as_view(), name='home'),

    path('profile/', DisplayProfileView.as_view(), name='profile'),
    path('profile-update/', UserProfileView.as_view(), name='profile_update'),

    path('job-post/', JobPostView.as_view(), name='jb_post'),
    path('job-list/', DisplayJobsView.as_view(), name='jb_list'),

    path("update/<int:u_id>/", UpdateJobView.as_view(), name="update"),
    path("delete/<int:d_id>/", DeleteJobView.as_view(), name="delete"),

    path('job-apply/<int:a_id>/', JobApplyView.as_view(), name='jb_apply'),
    path('candidate/<int:c_id>/', CandidateView.as_view(), name='candidate')
]
