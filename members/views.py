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

# Create your views here.

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

def validate_username(username):
    if User.objects.filter(username=username).exists():
        return False
    else:
        return True

def register(request):
    if not request.user.is_authenticated:
        template = loader.get_template('register.html')
        return HttpResponse(template.render(request))   
    else:
        return render(request, 'index.html')
        messages.error(request, 'you are logged in already')



def register_request(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            if validate_username(username) == False:
                messages.error(request, 'Username already exists. Please choose a different one.')
                return render(request, 'register.html')
            else:
                # save user info in database
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('home')
    else:
        form = UserCreationForm()
    return HttpResponseRedirect(reverse('index'))

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
    templatedb = Template.objects.get(id_global=id)
    template = loader.get_template('update.html')
    context = {
    'templatedb': templatedb,
    }
    return HttpResponse(template.render(context, request))

def request_edit(request, id):
    male_name = request.POST['male_name']
    female_name = request.POST['female_name']
    date_html = request.POST['date']
    time_html = request.POST['time']
    html_datetime = f'{date_html} {time_html}'
    date_datetime = datetime.strptime(html_datetime, '%Y-%m-%d %H:%M')
    templatedb = Template.objects.get(id_global=id)
    templatedb.male_name = male_name
    templatedb.female_name = female_name
    templatedb.date = date_datetime
    templatedb.save()
    return HttpResponseRedirect(reverse('edit'))

@login_required
def test(request, id):
    username = request.user.username
    username_obj = AccountDB.objects.get(username=username)
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