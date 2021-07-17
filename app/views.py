from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from attendance_management_system.settings import BASE_URL
from .face_recognition import compare
from .forms import UserForm, StaffUserForm, LoginUserForm, AddCourseForm, CourseRegForm
from .models import User, Course


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
    context = {"form": form, "user": user, "courses_student": courses_students, "courses_lecturer": courses_teachers}

    if not user.is_student:
        return render(request, 'app/admin_dashboard.html', context=context)

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
                return redirect(dashboard)

            else:
                context = {'error': "The username or password is wrong",
                           'form': form, }
                return render(request, "app/login.html", context)

    return render(request, "app/login.html", context=dict(form=form))


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


@login_required(login_url="/login")
def success_page(request):
    return render(request, 'app/success_page.html')


@login_required(login_url="/login")
def sign_attendance(request):
    """

    :param request:
    :return:
    """
    answer = ""
    user = request.user
    user_image = user.image.path
    print(user_image, "user_imga11111111111111......................")
    if request.method == "POST":
        realtime = request.FILES["ul[0][camera]"]

        answer = compare(user_image, realtime)
        print(answer, "answer================")
        if answer:
            print("I got here, this thing worked...........................................")
            return redirect(success_page)
        else:
            return render(request, 'app/new_att.html', context={"error": "Verification failed"})

    return render(request, 'app/new_att.html', context=dict(result=answer))


def course_info(request, course_code):
    """

    :param course_code:
    :param request:
    :return:
    """
    try:
        course = Course.objects.get(course_code=course_code)
        print(course_code, "course_code==================")
        students = course.students.all()
        print(students, "students=====================================")
        context = {"students": students, "course": course, "base_ulr": BASE_URL}
        return render(request, 'app/course_info.html', context=context)

    except Exception as e:
        raise e


def course_info_reg(request, course_code):
    """

    :param course_code:
    :param request:
    :return:
    """
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


def single_attendance_record(request, pk):
    """

    :param pk:
    :param request:
    :return:
    """
    user = None
    admin = request.user
    try:
        user = User.objects.get(pk=pk)

    except Exception as e:
        raise e
    context = {"user": user, "admin": admin}

    return render(request, 'app/single_record.html', context=context)
