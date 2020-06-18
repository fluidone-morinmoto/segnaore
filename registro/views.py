from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, QueryDict, JsonResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import viewsets

from registro.models import *
from registro.serializers import *
from registro.forms import *
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

    form_description = "Crea una nuova "

    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = CompanyForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            company_id = None
            logger.debug(request.POST);
            try:
                company_id = request.POST['cid']
                logger.info("Edit company #{} by user #{}".format(
                    company_id, user.id
                ));
            except Exception as e:
                logger.error(str(e))

            name = request.POST['name']

            company = Company()
            is_valid = True
            int_company_id = None

            try:
                int_company_id = int(company_id)
            except Exception as e:
                msg = "Value '{}' for company_id is not valid"
                logger.error(e)
                logger.error(msg.format(company_id))

            if int_company_id is not None:
                company = Company.objects.get(pk=int_company_id)
                if company.auth_user_id != user.id:
                    msg = "Non sei il proprietario di questa Company. Non la "
                    msg += "puoi modificare"
                    logger.error(msg)
                    is_valid = False

            company.auth_user_id = user.id
            company.name = name
            if is_valid:
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
            msg = msg.format(companyId, user.id)
            logger.info(msg)
            company.delete()
            return JsonResponse({'msg': msg})
    # If method is GET
    else:
        company = None
        company_id = None
        try:
            company_id = request.GET['cid']
        except Exception as e:
            logger.error(str(e))
        if company_id is not None:
            company = Company.objects.get(pk=company_id)
            form_description = "Modifica "
        # if a GET (or any other method) we'll create a blank formelse:
        form = CompanyForm(instance=company)

    context = {
        'page_title': 'Companies',
        'form': form,
        'companies': companies,
        'company_id': company_id,
        'form_description': form_description
    }
    return render(request, 'manageCompanies.html', context=context)

@login_required
def manageCategories(request):
    form = None
    user = request.user
    categories = Category.objects.filter(auth_user_id=user.id)

    form_description = "Crea una nuova "

    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = CategoryForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            category_id = None
            name = None
            description = None
            logger.debug(request.POST);
            try:
                category_id = request.POST['cid']
                logger.info("Edit category #{} by user #{}".format(
                    category_id, user.id
                ));
            except Exception as e:
                logger.error(str(e))

            name = request.POST['name']
            description = request.POST['description']

            category = Category()
            is_valid = True
            int_category_id = None
            try:
                int_category_id = int(category_id)
            except Exception as e:
                msg = "Value '{}' for category_id is not valid"
                logger.error(e)
                logger.error(msg.format(category_id))

            if int_category_id is not None:
                category = Category.objects.get(pk=int_category_id)
                if category.auth_user_id != user.id:
                    msg = "Non sei il proprietario di questa Category. Non la "
                    msg += "puoi modificare"
                    logger.error(msg)
                    is_valid = False

            category.auth_user_id = user.id
            category.name = name
            category.description = description
            if is_valid:
                category.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/manage/categories')
    elif request.method == 'DELETE':
        dict = QueryDict(request.body)
        categoryId = dict['categoryId']
        category = Category.objects.get(pk=categoryId)
        if category.auth_user_id != user.id:
            msg = "Questa Category non ti appartiene. Non la puoi eliminare"
            logger.warning(msg)
        else:
            msg = "Eliminazione della Category #{} da parte dell'utente #{}"
            msg = msg.format(categoryId, user.id)
            logger.info(msg)
            category.delete()
            return JsonResponse({'msg': msg})
    # If method is GET
    else:
        category = None
        category_id = None
        try:
            category_id = request.GET['cid']
        except Exception as e:
            logger.error(str(e))
        if category_id is not None:
            category = Category.objects.get(pk=category_id)
            form_description = "Modifica "
        # if a GET (or any other method) we'll create a blank formelse:
        form = CategoryForm(instance=category)

    context = {
        'page_title': 'Categories',
        'form': form,
        'categories': categories,
        'category_id': category_id,
        'form_description': form_description
    }
    return render(request, 'manageCategories.html', context=context)

@login_required
def manageProjects(request):
    form = None
    user = request.user
    projects = Project.objects.filter(auth_user_id=user.id)

    form_description = "Crea un nuovo "

    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = ProjectForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            project_id = None
            logger.debug(request.POST);
            try:
                project_id = request.POST['pid']
                logger.info("Edit project #{} by user #{}".format(
                    project_id, user.id
                ));
            except Exception as e:
                logger.error(str(e))

            name = request.POST['name']
            description = request.POST['description']
            code = request.POST['code']
            company_id = request.POST['company']

            project = Project()
            is_valid = True
            int_project_id = None
            try:
                int_project_id = int(project_id)
            except Exception as e:
                msg = "Value '{}' for project_id is not valid"
                logger.error(e)
                logger.error(msg.format(project_id))

            if int_project_id is not None:
                project = Project.objects.get(pk=int_project_id)
                if project.auth_user_id != user.id:
                    msg = "Non sei il proprietario di questo Progetto. Non lo "
                    msg += "puoi modificare"
                    logger.error(msg)
                    is_valid = False

            project.auth_user_id = user.id
            project.name = name
            project.description = description
            project.code = code
            project.company_id = company_id

            if is_valid:
                project.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/manage/projects')
    elif request.method == 'DELETE':
        dict = QueryDict(request.body)
        projectId = dict['projectId']
        project = Project.objects.get(pk=projectId)
        if project.auth_user_id != user.id:
            msg = "Questa Progetto non ti appartiene. Non lo puoi eliminare"
            logger.warning(msg)
        else:
            msg = "Eliminazione del Project #{} da parte dell'utente #{}"
            msg = msg.format(projectId, user.id)
            logger.info(msg)
            project.delete()
            return JsonResponse({'msg': msg})
    # If method is GET
    else:
        project = None
        project_id = None
        try:
            project_id = request.GET['pid']
        except Exception as e:
            logger.error(str(e))
        if project_id is not None:
            project = Project.objects.get(pk=project_id)
            form_description = "Modifica "
        # if a GET (or any other method) we'll create a blank formelse:
        form = ProjectForm(instance=project)

    context = {
        'page_title': 'Projects',
        'form': form,
        'projects': projects,
        'project_id': project_id,
        'form_description': form_description
    }
    return render(request, 'manageProjects.html', context=context)

@login_required
def manageWorkedHours(request):
    form = None
    user = request.user
    worked_hours_list = WorkedHours.objects.filter(auth_user_id=user.id)
    worked_hours_id = None

    form_description = "Aggiungi "

    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = WorkedHoursForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            logger.debug(request.POST);
            try:
                worked_hours_id = request.POST['whid']
                logger.info("Edit worked_hours #{} by user #{}".format(
                    worked_hours_id, user.id
                ));
            except Exception as e:
                logger.error(str(e))

            from_time = request.POST['from_time']
            to_time = request.POST['to_time']
            description = request.POST['description']
            category = request.POST['category']
            project = request.POST['project']

            worked_hours = WorkedHours()
            is_valid = True
            int_worked_hours_id = None
            try:
                int_worked_hours_id = int(worked_hours_id)
            except Exception as e:
                msg = "Value '{}' for worked_hours_id is not valid"
                logger.error(e)
                logger.error(msg.format(worked_hours_id))

            if int_worked_hours_id is not None:
                worked_hours = WorkedHours.objects.get(pk=int_worked_hours_id)
                if worked_hours.auth_user_id != user.id:
                    msg = "Non sei il proprietario di questa registrazione "
                    msg += "delle ore. Non la puoi modificare"
                    logger.error(msg)
                    is_valid = False

            worked_hours.from_time = from_time
            worked_hours.to_time = to_time
            worked_hours.description = description
            worked_hours.category_id = category
            worked_hours.project_id = project
            worked_hours.auth_user_id = user.id

            if is_valid:
                worked_hours.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/manage/worked_hours')
    # elif request.method == 'DELETE':
    #     dict = QueryDict(request.body)
    #     worked_hoursId = dict['worked_hoursId']
    #     worked_hours = WorkedHours.objects.get(pk=worked_hoursId)
    #     if worked_hours.auth_user_id != user.id:
    #         msg = "Questa registrazione delle ore non ti appartiene. "
    #         msg += "Non la puoi eliminare"
    #         logger.warning(msg)
    #     else:
    #         msg = "Eliminazione del WorkedHours #{} da parte dell'utente #{}"
    #         msg = msg.format(worked_hoursId, user.id)
    #         logger.info(msg)
    #         worked_hours.delete()
    #         return JsonResponse({'msg': msg})
    # If method is GET
    else:
        worked_hours = None
        worked_hours_id = None
        try:
            worked_hours_id = request.GET['whid']
        except Exception as e:
            logger.error(str(e))
        if worked_hours_id is not None:
            worked_hours = WorkedHours.objects.get(pk=worked_hours_id)
            form_description = "Modifica "
        # if a GET (or any other method) we'll create a blank formelse:
        form = WorkedHoursForm(instance=worked_hours)

    context = {
        'page_title': 'Worked Hours',
        'form': form,
        'worked_hours_list': worked_hours_list,
        'worked_hours_id': worked_hours_id,
        'form_description': form_description
    }
    return render(request, 'manageWorkedHours.html', context=context)
