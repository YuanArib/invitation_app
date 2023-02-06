from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
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

from rest_framework import viewsets

from members.models import AccountDB, Template, Template_Event

from .forms import NewUserForm
from .forms import SetPasswordForm
from .forms import PasswordResetForm
from .token import account_activation_token
from .serializers import create_template
# Create your views here.

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

class templateapi(viewsets.ModelViewSet):
    serializer_class = create_template
    queryset = Template.objects.all()

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
                return redirect('dashboard')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'password_change.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("dashboard")

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

def get_email(email):
    try:
        User.objects.get(email=email)
        return False
    except User.DoesNotExist:
        return True

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
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        print("Received POST Request... At: " + str(datetime.now()))
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            print("Form validated with username and password. At:" + str(datetime.now()))
            if get_email(email) == False:
                messages.error(request, 'Email already exists. Please choose a different one.')
                print("This Email Already Exist. At:" + str(datetime.now()))
                return redirect(dashboard)
            elif get_username(username) == True:
                messages.error(request, 'Username already exists. Please choose a different one.')
                print("Username Already Exist. At:" + str(datetime.now()))
                # form = NewUserForm()
                # return render(request, 'register.html', {'register_form': form})
                return redirect(dashboard)
            else:
                # save user info in database
                form.save()
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
        form = NewUserForm()

    return render(
        request = request,
        template_name = "register.html",
        context={"form":form}
        )
    # else:
    #     return render(request, 'index.html')

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
    with open('C:\\Users\\Alaikal Hamdi\\Documents\\Alaikal Hamdi\\Yuan X Taiga\\invitation_app\\members\\templates\\invite_templates\\ts_test' + id_str + '.html', 'w') as static_file:
        static_file.write(content)

    return HttpResponse(template.render(context, request))

def get_id():
    def Empty():
        print("There is nothing in the record, returning 1.")
        return 1
    def Success(id_n):
        print("Successfully parsed new get_id() with the id: " + str(id_n))
        return id_n

    # id = Template.objects.last('id_global')
    
    # id = Template.objects.raw('SELECT members_template, .. FROM table_name Order By date_column Desc')
    id_template = Template.objects.all().order_by('-id_global').first()
    id_n = id_template.id_global
    if id_n == None:
        return Empty()
    else:
        id_n = id_n + 1
        return Success(id_n=id_n)

def get_id_event(id):
    def Empty():
        print("There is nothing in the record, returning 1.")
        return 1
    def Success(id_n):
        print("Successfully parsed new get_id() with the id: " + str(id_n))
        return id_n

    # id = Template.objects.last('id_global')
    
    # id = Template.objects.raw('SELECT members_template, .. FROM table_name Order By date_column Desc')
    # id_t = Template.objects.all().order_by('-id_global').first()
    id_t = Template_Event.objects.filter(template_id=id).order_by('-event_id').first()
    if id_t == None:
        return Empty()
    else:
        id_n = id_t.event_id
        id_n = id_n + 1
        return Success(id_n=id_n)

    # try:
        # id_template = Template.objects.all().order_by('-id_global').first()
        # id_n = id_template.id_global
    #     return True
    # except Template.DoesNotExist:
    #     return False

def check_ownership(username, id):
    templateid = Template.objects.get(id_global=id)
    if templateid.owner == username:
        return True
    else:
        return False

def get_template(id):
    try:
        Template.objects.get(id_global=id)
        return True
    except Template.DoesNotExist:
        return False

class temp_event_dict:
    def __init__(self, name, description, address, date_start, time_start, date_end, time_end):
        self.name = name
        self.description = description
        self.address = address
        self.date_start = date_start
        self.time_start = time_start
        self.date_end = date_end
        self.time_end = time_end
    # "name":name,
    # "event_id":id_n,
    # "description":description,
    # "date_start":date_start,
    # "time_start":time_start,
    # "date_end":date_end,
    # "time_end":time_end,

def get_template_context(id):
    template_context = Template.objects.get(id_template=id)
    return template_context

@login_required
def add_event(request, id):
    print(id)
    if request.method == 'POST':
        username = request.user.username
        username_obj = AccountDB.objects.get(username=username)
        id_n = get_id_event(id=id)
        if get_template(id) == True:
            if check_ownership(username=username_obj, id=id) == True:
                name = request.POST['name']
                description = request.POST['description']
                address = request.POST['address']
                date_start = request.POST['date_start']
                time_start = request.POST['time_start']
                date_end = request.POST['date_end']
                time_end = request.POST['time_end']

                html_datetime_start = f'{date_start} {time_start}'
                date_datetime_start = datetime.strptime(html_datetime_start, '%Y-%m-%d %H:%M')
                html_datetime_end = f'{date_end} {time_end}'
                date_datetime_end = datetime.strptime(html_datetime_end, '%Y-%m-%d %H:%M')

                # template_id = request.user.username
                # temp_id_obj = AccountDB.objects.get(username=username)
                # temp_id_obj = Template.objects.get(id_global=id)

                temp_event = Template_Event.objects.create(
                    template_id=id,
                    event_id=id_n,
                    name=name, 
                    description=description, 
                    address=address,
                    date_start=date_datetime_start,
                    date_end=date_datetime_end
                )
                temp_event_db = Template_Event.objects.filter(template_id=id)

                # temp_event_dict = {
                #     "name":name,
                #     "event_id":id_n,
                #     "description":description,
                #     "date_start":date_start,
                #     "time_start":time_start,
                #     "date_end":date_end,
                #     "time_end":time_end,
                # }
                # templatedb = get_template_context(id)
                template_context = Template.objects.get(id_global=id)

                context = {
                    'male_name':template_context.male_name,
                    'female_name':template_context.female_name,
                    'date':template_context.date,
                    'template_event':temp_event_db
                }
                content = render_to_string('template1.html', context) 
                template = loader.get_template('template1.html')               
                with open('C:\\Users\\Alaikal Hamdi\\Documents\\Alaikal Hamdi\\Yuan X Taiga\\invitation_app\\members\\templates\\invite_templates\\ts_test' + str(id) + '.html', 'w') as static_file:
                    static_file.write(content)

                return HttpResponse(template.render(context, request))
            else:
                messages.error(request, "You are not the owner of this template.")
                return redirect(dashboard)
        else:
            messages.error(request, "Template does not exist")
            return redirect(dashboard)
    else:
        context = {'template_id':id}
        template = loader.get_template('add_event.html')
        return HttpResponse(template.render(context, request))

@login_required
def add_request(request):
    username = request.user.username
    username_obj = AccountDB.objects.get(username=username)
    date_start_html = request.POST['date']
    time_start_html = request.POST['time']
    # date_end_html = request.POST['date_end']
    # time_end_html = request.POST['time_end']
    
    html_datetime = f'{date_start_html} {time_start_html}'
    date_datetime = datetime.strptime(html_datetime, '%Y-%m-%d %H:%M')

    # publicTemplate_obj = publicTemplate.objects.all().values()
    male_name = request.POST['male_name']
    female_name = request.POST['female_name']
    id_def = get_id()
    # id_n = id + 1
    id_str = str(id_def)
    # example_event_dict = {
                #     "name":"Event Name Example",
                #     "event_id":1,
                #     "description":'This is an event name description example. To create a new event, go to "+ Add Event" button in dashboard',
                #     "date_start":"1-1-2000",
                #     "time_start":"07:00 PM",
                #     "date_end":"1-2-2000",
                #     "time_end":"07:00 AM",
                # }
    context = {
        'male_name':male_name,
        'female_name':female_name,
        'date':str(date_start_html),
        'time':str(time_start_html),
        # 'template_event': example_event_dict
    }

    templatedb = Template.objects.create(
        owner=username_obj,
        male_name=male_name,
        date=date_datetime, 
        female_name=female_name, 
        id_global=id_def
    )

    # date=date_datetime,
    # public_templatedb = publicTemplate(id_n)

    content = render_to_string('template1.html', context) 
    template = loader.get_template('template1.html')               
    with open('C:\\Users\\Alaikal Hamdi\\Documents\\Alaikal Hamdi\\Yuan X Taiga\\invitation_app\\members\\templates\\invite_templates\\ts_test' + id_str + '.html', 'w') as static_file:
        static_file.write(content)

    return HttpResponse(template.render(context, request))

@login_required
def open_file(request, id):
    username = request.user.username
    username_obj = AccountDB.objects.get(username=username)
    if get_template(id=id) == True:
        if check_ownership(username=username_obj, id=id) == True:
            template = loader.get_template('invite_templates/ts_test' + str(id) + '.html')
            return HttpResponse(template.render({}, request))
        else:
            messages.error(request, "You are not the owner of this template.")
            return redirect(dashboard)
    else:
        messages.error(request, "404: Template is not found")
        return redirect(dashboard)

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