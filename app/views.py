from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .face_recognition import compare
from .utils import encode_str, decode_str
from .forms import UserForm, StaffUserForm, LoginUserForm, AddCourseForm, CourseRegForm, GenerateLinkForm, OTPForm
from .models import User, Course, TempLink, AttendanceRecord, OTP
from .utils import token_generator

from attendance_management_system.settings import BASE_URL
import geopy.distance


# Create your views here.

def register_student(request):
    """

    :param request:
    :return:
    """
    form = UserForm()
    if request.method == "GET":
        return render(request, 'app/register.html', context={"form": form})

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, auto_id=True)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            student = authenticate(username=username, password=password)

            login(request, student)
            return redirect(dashboard)

        else:
            print(form.error_messages, "This is the error============")

            return render(request, 'app/register.html', context={"form": form})


def register_staff(request):
    """

    :param request:
    :return:
    """
    form = StaffUserForm()
    if request.method == "GET":
        return render(request, 'app/register_staff.html', context={"form": form})

    if request.method == "POST":
        form = StaffUserForm(request.POST, request.FILES, auto_id=True)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            try:
                user = User.objects.get(username=username)
                user.is_student = False
                user.save()
            except Exception as e:
                raise e

            staff = authenticate(username=username, password=password)

            login(request, staff)
            return redirect(dashboard)

        else:
            print(form.errors, "This is the error============")

            return render(request, 'app/register_staff.html', context={"form": form})


@login_required(login_url="/login")
def dashboard(request):
    """

    :param request:
    :return:
    """
    form = AddCourseForm()
    user = request.user
    user = User.objects.get(pk=user.pk)
    context = {"form": form}
    if request.method == "POST":
        form = AddCourseForm(request.POST, request.FILES, auto_id=True)
        if form.is_valid():
            form.save()
            course_code = form.cleaned_data.get('course_code')
            try:
                course = Course.objects.get(course_code=course_code)
                course.lecturer = user
                course.save()
            except Exception as e:
                raise e

        else:
            print(form.errors, "errors=====================")
    courses_students = Course.objects.filter(students=user)
    print(courses_students, "HELLOO+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    courses_teachers = Course.objects.filter(lecturer=user)
    values = ["bg-info", "bg-warning", "bg-success", "bg-danger"]
    context = {"form": form, "user": user, "courses_student": courses_students, "courses_lecturer": courses_teachers,
               "value": values}

    if not user.is_student:
        return render(request, 'app/index.html', context=context)

    return render(request, 'app/dashboard.html', context=context)


def sign_in(request):
    """

    :param request:
    :return:
    """
    form = LoginUserForm()
    if request.method == "POST":
        form = LoginUserForm(request.POST, request.FILES, auto_id=True)

        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                # checking to see if there's a next url in the link
                if "next" in request.POST:
                    return redirect(request.POST.get("next"))

                return redirect(dashboard)
            else:
                context = {'error': "The username or password is wrong",
                           'form': form, }
            return render(request, "app/login.html", context)
        else:
            context = {'error': "The username or password is wrong",
                       'form': form, }
            return render(request, "app/login.html", context)

    context = {'error': "",
               'form': form, }
    return render(request, "app/login.html", context)


def landing_register(request):
    """

    :param request:
    :return:
    """
    return render(request, "app/landing_registration.html")


def sign_out(request):
    """

    :param request:
    :return:
    """
    logout(request)
    return redirect(sign_in)


def add_course(request):
    """

    :param request:
    :return:
    """
    form = AddCourseForm()
    if request.method == "POST":
        form = AddCourseForm(request.POST, request.FILES, auto_id=True)

        if form.is_valid():
            form.save()

    return redirect(dashboard)


@login_required(login_url="/login", )
def success_page(request):
    return render(request, 'app/success_page.html')


@login_required(login_url="/login")
def sign_attendance(request, course_code, hassh):
    """

    :param course_code:
    :param hassh:
    :param request:
    :return:
    """
    decoded_value = decode_str(hassh)
    course_code = decoded_value[:6]  # Get the course_code from the decoded value
    user = request.user
    url = BASE_URL + request.path
    print(url)
    attendance_link = TempLink.objects.get(url=url)
    if attendance_link.active:
        tm = datetime.now()
        now = tm.replace(hour=tm.hour + 1)
        # if not attendance_link.end_time > now:
        #     return render(request, "app/error_page.html")

        # check if the user has registered the attendance already
        try:

            previous = AttendanceRecord.objects.get(attendance_link=attendance_link, user=user)
            if previous.logout and previous.login:
                return render(request, 'app/new_att.html',
                              context={"error": "Your Attendance has been recorded already", })

        except Exception as e:
            pass

        try:

            course = Course.objects.get(course_code=course_code)
            print(course, "course---------------------------")
            # check if the student has registered for the course
            print("Checking if the students has registered for the course...............")
            student = course.students.get(first_name=user.first_name)
            print(student.first_name, "The first name=============")

            user_image = user.image.path

            if request.method == "POST":

                realtime = request.FILES["ul[0][camera]"]  # get the image file from the request
                lat = request.POST.get("latitude")
                lng = request.POST.get("longitude")
                print(f"this is the LAT {lat}==============, while this the LNG{lng}=====")
                print(
                    f"This is the attendance lat{attendance_link.latitude}, this is  the {attendance_link.longitude}======================")
                coords_1 = (attendance_link.latitude, attendance_link.longitude)
                coords_2 = (lat, lng)
                distance = geopy.distance.geodesic(coords_1, coords_2)
                if distance > 0.1:
                    return redirect(otp_verification, course=course, attendance_link=attendance_link.pk)
                try:
                    answer = compare(user_image, realtime)  # make the image comparisons

                except Exception as e:
                    return redirect(otp_verification, course=course, attendance_link=attendance_link.pk)

                if answer:
                    try:
                        previous = AttendanceRecord.objects.get(attendance_link=attendance_link, user=user)
                        if previous:
                            tm = datetime.now()
                            timestamp = tm.replace(hour=tm.hour + 1)
                            previous.logout = timestamp
                            previous.save()

                    except AttendanceRecord.DoesNotExist as e:
                        print(course, user, attendance_link)
                        tm = datetime.now()
                        timestamp = tm.replace(hour=tm.hour + 1)
                        AttendanceRecord.objects.create(course=course, user=user, login=timestamp,
                                                        attendance_link=attendance_link).save()

                    return redirect(success_page)

                else:
                    return redirect('otp_verification', course=course, attendance_link=attendance_link.pk)

        except Course.DoesNotExist as e:
            # print("Not registered...............................")
            return render(request, 'app/att_error.html', context={"error": "You are not registered for this course"})
            # raise e
        except User.DoesNotExist as e:
            return render(request, 'app/att_error.html', context={"error": "You are not registered for this course"})

            # return render(request, 'app/new_att.html', context={"error": "You are not registered for this course"})
            # raise e
        answer = ""

        return render(request, 'app/sign_attendance.html', context=dict(result=answer, course_code=course_code))

    else:
        return render(request, 'app/att_error.html', context={"error": "THIS LINK HAS EXPIRED!!"})


def course_info(request, course_code):
    """

    :param course_code:
    :param request:
    :return:
    """
    try:
        course = Course.objects.get(course_code=course_code)

        students = course.students.all()
        url = ""

        if request.method == "POST":
            form = GenerateLinkForm(request.POST, request.FILES, auto_id=True)
            if form.is_valid():
                last = TempLink.objects.filter(course=course).last()
                if last:
                    last.active = False
                    last.save()

                temp_model = TempLink()
                start_time = form.cleaned_data.get("start_time")
                end_time = form.cleaned_data.get("end_time")
                lat = form.cleaned_data.get("lat")
                lng = form.cleaned_data.get("lng")
                temp_model.start_time = start_time
                temp_model.end_time = end_time
                temp_model.active = True
                temp_model.course = course
                temp_model.latitude = lat
                temp_model.longitude = lng
                print(f"This is the lat{lat}, this is  the {lng}======================")

                str_encode = str(course_code) + str(end_time)
                str_encode = encode_str(str_encode)
                url = BASE_URL + "/" + str.lower(course_code) + "/" + str_encode.decode("utf-8")
                temp_model.url = url
                temp_model.save()

            else:
                print(form.errors, "FORM ERROR==================================")
                context = {"students": students, "course": course, "base_ulr": BASE_URL, "form": form,
                           "attendance_link": url}

                return render(request, 'app/course_info.html', context=context)

        form = GenerateLinkForm()
        context = {"students": students, "course": course, "base_ulr": BASE_URL, "form": form,
                   "attendance_link": url}

        return render(request, 'app/course_info.html', context=context)

    except Exception as e:
        raise e


@login_required(login_url="/login")
def course_info_reg(request, course_code):
    """

    :param course_code:
    :param request:
    :return:
    """
    try:
        course = Course.objects.get(course_code=course_code)
        user = request.user
        form = CourseRegForm()
        context = {"form": form, "course_code": course_code}
        print("Hello WORLD========================")
        if request.method == "POST":
            form = CourseRegForm(request.POST, request.FILES, auto_id=True)

            if form.is_valid():
                print("This MAT NUMBER DOES NOT MATCH THIS USER")
                mat_number = form.cleaned_data.get('mat_number')
                print("This MAT NUMBER DOES NOT MATCH THIS USER")
                if mat_number == user.mat_number:
                    try:
                        course = Course.objects.get(course_code=course_code)
                        course.students.add(user)
                        course.save()
                        return redirect(dashboard)
                    except Exception as e:
                        print(e)
                        raise e
                else:
                    print("This MAT NUMBER DOES NOT MATCH THIS USER")
                    context = {"form": form, "errors": "This MAT NUMBER DOES NOT MATCH THIS USER",
                               "course_code": course_code}
                    return render(request, 'app/course_reg.html', context=context)

        print(form.errors, "heetoototo================")
        return render(request, 'app/course_reg.html', context=context)
    except Exception as e:
        context = {"the_error": "Invalid Link"}
        return render(request, 'app/error_page.html', context=context)


@login_required(login_url="/login")
def single_attendance_record(request, course_code, pk, ):
    """

    :param course_code:
    :param pk:
    :param request:
    :return:
    """
    admin = request.user
    attendance_record = None
    try:
        user = User.objects.get(pk=pk)
        attendance_record = AttendanceRecord.objects.filter(course__course_code=course_code, user=user)
        attendance_record_count = AttendanceRecord.objects.filter(course__course_code=course_code, user=user,
                                                                  logout__isnull=False).count()
        course = Course.objects.get(course_code=course_code)
        all_attendance = TempLink.objects.filter(course=course).count()
        average_attendance_percentage = round((attendance_record_count / all_attendance) * 100,
                                              2) if attendance_record_count > 0 and all_attendance > 0 else 0

        print(f'the class held {all_attendance}')
        print(f'You attended {attendance_record_count}')

    except Exception as e:
        raise e
    context = {"user": user, "record": attendance_record, "course": course, "admin": admin,
               "percentage": average_attendance_percentage}

    return render(request, 'app/single_record.html', context=context)


@login_required(login_url="/login")
def generate_otp(request):
    """

    :param request:
    :return:
    """
    user = request.user
    if not user.is_student:
        otp = token_generator()
        try:
            old_token = OTP.objects.get(active=True)
            old_token.delete()
        except Exception as e:
            pass
        token = OTP.objects.create(password=otp, active=True, user=user).save()
        print(otp, "Token  PAssord=====================")
        return render(request, 'app/otp.html', context={"token": otp})
    return redirect(dashboard)


def otp_verification(request, course, attendance_link, error=None):
    """

    :param error:
    :param course:
    :param attendance_link:
    :param request:
    :return:
    """
    form = OTPForm()
    user = request.user
    course = Course.objects.get(title=course)
    att_obj = TempLink.objects.get(pk=attendance_link)
    # user = User.objects.get(first_name=req.email)
    if request.method == "POST":
        form = OTPForm(request.POST, request.FILES)

        if form.is_valid():
            print("It is Vslid========================")
            password = form.cleaned_data.get('password')
            try:
                otp = OTP.objects.get(password=password)

                # check if the user has registered the attendance already
                try:

                    previous = AttendanceRecord.objects.get(attendance_link=attendance_link, user=user)
                    if previous.logout and previous.login:
                        return render(request, 'app/new_att.html',
                                      context={
                                          "error": "Your Attendance has been recorded already", })

                except Exception as e:
                    print(e, "LEVEL 1")
                    pass

                try:
                    previous = AttendanceRecord.objects.get(attendance_link=attendance_link, user=user)
                    if previous:
                        tm = datetime.now()
                        timestamp = tm.replace(hour=tm.hour + 1)
                        previous.logout = timestamp
                        previous.save()

                except AttendanceRecord.DoesNotExist as e:
                    print(e, "LEVEL 2")
                    print(course, user, attendance_link)
                    tm = datetime.now()
                    timestamp = tm.replace(hour=tm.hour + 1)
                    AttendanceRecord.objects.create(course=course, user=user, login=timestamp,
                                                    attendance_link=att_obj).save()

                otp.delete()
                return redirect(dashboard)
            except Exception as e:
                print(e, "LEVEL 3")
                return render(request, 'app/attendance_error.html',
                              context={"form_error": "Invalid or expired  OTP", "form": form,
                                       "error": "Your Face didn't match Meanwhile, if you're sure you're the one you can ask the lecturer to give you an OTP to successfully sign the attendance" if not error else error, })
        print("IT is NOt!!!!")

    return render(request, 'app/attendance_error.html', context={"form": form,
                                                                 "error": "Your Face didn't match Meanwhile, if you're sure you're the one you can ask the lecturer to give you an OTP to successfully sign the attendance" if not error else error,
                                                                 "form_error": ""})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    print(ip, "The IP................................")
    return render(request, "app/admin_dashboard.html", context={"ip": ip})

# def make_attendance_url(request):
#     """
#
#     :param request:
#     :return:
#     """
#     if request.is_ajax and request.method == "POST":
