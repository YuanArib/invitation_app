from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from members.models import AccountDB, Template
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models.query_utils import Q
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .forms import NewUserForm
from .forms import SetPasswordForm
from .forms import PasswordResetForm
from .token import account_activation_token

# Create your views here.

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                        """
                        <h2>Password reset sent</h2><hr>
                        <p>
                            We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                            You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address 
                            you registered with, and check your spam folder.
                        </p>
                        """
                    )
                else:
                    messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")

            return redirect('dashboard')

        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "You must pass the reCAPTCHA test")
                continue

    form = PasswordResetForm()
    return render(
        request=request, 
        template_name="password_reset.html", 
        context={"form": form}
        )

def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and <b>log in </b> now.")
                return redirect('homepage')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'password_change.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("homepage")

@login_required
def password_change(request):
    user = request.user
    form = SetPasswordForm(user)
    return render(request, 'password_change.html', {'form': form})

def password_change_request(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            print("Password Changed!")
            return redirect('dashboard')
        # else:
        #     for error in list(form.errors.values()):
        #         messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'password_change.html', {'form': form})

def validate_username(username):
    if User.objects.filter(username=username).exists():
        return False
    else:
        return True

def get_username(username):
    try:
        User.objects.get(username=username)
        return True
    except User.DoesNotExist:
        return False

def register(request):
    if not request.user.is_authenticated:
        # template = loader.get_template('register.html')
        # return HttpResponse(template.render({}, request)) 
        form = NewUserForm()
        return render(request, 'register.html', {'register_form': form})  
    else:
        messages.error(request, 'you are logged in already')
        return redirect(dashboard)

def register_request(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        print("Received POST Request... At: " + str(datetime.now()))
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            print("Form validated with username and password. At:" + str(datetime.now()))
            if get_username(username) == False:
                messages.error(request, 'Username already exists. Please choose a different one.')
                print("Username Already Exist. At:" + str(datetime.now()))
                # form = NewUserForm()
                # return render(request, 'register.html', {'register_form': form})
                return redirect(register)
            else:
                # save user info in database
                user = authenticate(username=username, password=raw_password)
                AccountDB.objects.create(username=username)
                login(request, user)
                print("Registration completed with username and password. At: " + str(datetime.now()))
                messages.success(request, 'Registration complete!')
                return redirect(dashboard)
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
            print("Invalid Information. At: " + str(datetime.now()))
            return render(request, 'register.html')
    else:
        return render(request, 'index.html')

@login_required
def dashboard(request):
    username = request.user.username
    username_obj = AccountDB.objects.get(username=username)
    templatedb = Template.objects.filter(owner=username_obj)
    # templatedb = Template.objects.raw('SELECT female_name, male_name FROM members_template WHERE owner = %s',[username_obj])
    context = {
        'templatedb': templatedb,
    }
    template = loader.get_template('dashboard.html')
    return HttpResponse(template.render(context, request))

@login_required
def edit(request, id):
    username = request.user.username
    username_obj = AccountDB.objects.get(username=username)
    user = Template.objects.get(owner=username_obj)
    templatedb = Template.objects.get(id_global=id)
    template_date = templatedb.date
    date = template_date.strftime("%m/%d/%Y")
    time = template_date.strftime("%H:%M")
    template = loader.get_template('edit.html')
    context = {
    'templatedb': templatedb,
    'templatedate': date,
    'templatetime': time,
    }
    return HttpResponse(template.render(context, request))

@login_required
def edit_request(request, id):
    id_str = str(id)
    # male_name = request.POST['male_name']
    # female_name = request.POST['female_name']
    # date_html = request.POST['date']
    # time_html = request.POST['time']
    male_name = request.POST.get('male_name', False)
    female_name = request.POST.get('female_name', False)
    date_html = request.POST.get('date', False)
    time_html = request.POST.get('time', False)
    html_datetime = f'{date_html} {time_html}'
    date_datetime = datetime.strptime(html_datetime, '%Y-%m-%d %H:%M')

    #templatedb
    templatedb = Template.objects.get(id_global=id)
    templatedb.male_name = male_name
    templatedb.female_name = female_name
    templatedb.date = date_datetime
    templatedb.save()

    context = {
        'male_name':male_name,
        'female_name':female_name,
        'date':str(date_html),
        'time':str(time_html)
    }
    content = render_to_string('template1.html', context)
    template = loader.get_template('template1.html')
    # return HttpResponseRedirect(reverse('edit'))
    with open('C:\\Users\\Alaikal Hamdi\\Documents\\Alaikal Hamdi\\Yuan X Taiga\\invitation_app\\templates\\invite_templates\\ts_test' + id_str + '.html', 'w') as static_file:
        static_file.write(content)

    return HttpResponse(template.render(context, request))

@login_required
def add_request(request, id):
    username = request.user.username
    username_obj = AccountDB.objects.get(username=username)
    date_html = request.POST['date']
    time_html = request.POST['time']
    html_datetime = f'{date_html} {time_html}'
    date_datetime = datetime.strptime(html_datetime, '%Y-%m-%d %H:%M')

    # publicTemplate_obj = publicTemplate.objects.all().values()
    male_name = request.POST['male_name']
    female_name = request.POST['female_name']
    id_n = id + 1
    id_str = str(id_n)
    context = {
        'male_name':male_name,
        'female_name':female_name,
        'date':str(date_html),
        'time':str(time_html),
    }
    templatedb = Template.objects.create(owner=username_obj, male_name=male_name, female_name=female_name, date=date_datetime)
    # public_templatedb = publicTemplate(id_n)

    content = render_to_string('template1.html', context) 
    template = loader.get_template('template1.html')               
    with open('C:\\Users\\Alaikal Hamdi\\Documents\\Alaikal Hamdi\\Yuan X Taiga\\invitation_app\\templates\\invite_templates\\ts_test' + id_str + '.html', 'w') as static_file:
        static_file.write(content)

    return HttpResponse(template.render(context, request))

    # try:
    #     username_obj = AccountDB.objects.get(username=username)
    # except:
    #     print("Variable username is not defined")
    #     username_obj = AccountDB.objects.create(username=username)
    #     print("Created new username")
    # else:
    #     username_obj = AccountDB.objects.get(username=username)
    #     print("username found")
    #     print(username)
    # username_obj = AccountDB.objects.create(username=username)