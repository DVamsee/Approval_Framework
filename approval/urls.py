from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name='homepage'),
    path('register/',views.registration_view,name = 'registration vieew'),
    path('login/',views.login,name = 'login view'),
    path('logout/',views.logout,name = 'logout view'),
    path('profile/',views.profile,name = 'profile page'),
    path('company/',views.company,name = 'company profile'),
    path('company/create/',views.company_create,name = 'company create'),
    path('company/<int:id>/remove/',views.remove_company,name = 'company remove'),
    path('workflow/',views.workflow,name = 'workflow page'),
    path('workflow/create/',views.workflow_create,name = 'workflow create page'),
    path('workflow/<int:id>/remove/',views.delete_workflow,name = 'workflow delete'),
    path('approval/',views.approval,name = 'approval page'),
    path('approval/create/',views.approval_create, name = 'approval create page'),
    path('approval/<int:id>/comment/add/',views.comment_create,name = 'comment create'),
    path('approval/<int:id>/approve/',views.approval_approve,name='approval approve'),
    path('approval/<int:id>/reject/',views.approval_reject,name = 'approval reject'),

]