from django.conf.urls.static import static
from django.urls import path

from attendance_management_system import settings
from .views import register_student as register, dashboard, register_staff, landing_register, sign_in, add_course, \
    sign_out, sign_attendance, success_page, course_info, course_info_reg, single_attendance_record, generate_otp, \
    otp_verification

urlpatterns = [
    path('', dashboard, name=""),
    path('student_register', register, name="register_student"),
    path('staff_register', register_staff, name="register_staff"),
    path('register', landing_register, name="register"),
    path('dashboard', dashboard, name="dashboard"),
    path('login', sign_in, name="login"),
    path('logut', sign_out, name="logout"),
    path('add_course', add_course, name="add_course"),
    path('sign_attendance', sign_attendance, name="attendance"),
    path('success_page', success_page, name="success"),
    path('course_info/<str:course_code>', course_info, name="course_info"),
    path('<str:course_code>/register', course_info_reg, name="course_info_reg"),
    path('dashboard/<str:course_code>/<int:pk>', single_attendance_record, name="single"),
    path('<str:course_code>/<str:hassh>', sign_attendance, name="sign_attendance"),
    path('generate_otp', generate_otp, name="otp"),
    path('verify_otp/<str:course>/<str:attendance_link>', otp_verification, name="otp_verification"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



