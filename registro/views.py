from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import viewsets

from registro.models import *
from registro.serializers import *
from registro.forms import SignUpForm, CompanyForm
from registro.tokens import account_activation_token
from . import logger


# ViewSets define the view behavior.
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

# ViewSets define the view behavior.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# ViewSets define the view behavior.
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

# ViewSets define the view behavior.
class WorkedHoursViewSet(viewsets.ModelViewSet):
    queryset = WorkedHours.objects.all()
    serializer_class = WorkedHoursSerializer

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Registro Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')

@login_required
def home(request):
    context = {'page_title': 'home'}
    return render(request, 'home.html', context=context)

@login_required
def profile(request):
    context = {'page_title': 'profile'}
    return render(request, 'registration/profile.html', context=context)

@login_required
def manageCompanies(request):
    form = None
    user = request.user
    companies = Company.objects.filter(auth_user_id=user.id)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CompanyForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = request.POST['name']
            company = Company()
            company.name = name
            company.auth_user_id = user.id
            company.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/manage/companies')
    elif request.method == 'DELETE':
        dict = QueryDict(request.body)
        companyId = dict['companyId']
        company = Company.objects.get(pk=companyId)
        if company.auth_user_id != user.id:
            msg = "Questa Company non ti appartiene. Non la puoi eliminare"
            logger.warning(msg)
        else:
            msg = "Eliminazione della Company #{} da parte dell'utente #{}"
            logger.info(msg.format(companyId, user.id))
            company.delete()
    else:
        # if a GET (or any other method) we'll create a blank formelse:
        form = CompanyForm()

    context = {
        'page_title': 'Companies',
        'form': form,
        'companies': companies
    }
    return render(request, 'manageCompanies.html', context=context)
