import datetime

from django.db.models import Q
from django.template import RequestContext
from django.shortcuts import render_to_response

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse


from RT_MW.sendInvitation import send_invitation_email
from RT_MW.models import Project, Category, Specification, Lead, Join
from RT_MW.forms import UserForm, UserProfileForm, AttributeForm, CategoryForm, ProjectForm, LeadForm, JoinForm


def index(request):
    context = RequestContext(request)

    registerInform = register(request)
    loginInform = user_login(request)
    context_dict =  dict(registerInform.items() + loginInform.items())
    return render_to_response('RT_MW/index.html', context_dict, context)

def register(request):
    context = RequestContext(request)

    registerd = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            userInform = user_form.save()

            userInform.set_password(userInform.password)
            userInform.save()

            profile = profile_form.save(commit=False)
            profile.user = userInform

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            username = userInform.username
            password = userInform.password
            registerd = True

            return render_to_response('RT_MW/index.html',{'registerd':registerd}, context)
            #return HttpResponseRedirect('/login')
        else:
            print user_form.errors, profile_form.errors
            return HttpResponseRedirect('/')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        return {'user_form': user_form, 'profile_form': profile_form}

def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/user_interface')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        return {}

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# def user_interface(request):
#     context = RequestContext(request)
#     user = request.user
#
#     if not user.is_authenticated():
#         return HttpResponseRedirect('/')
#
#     projects = Join.objects.select_related().filter(users__username__exact=user.username)
#     attrs = Specification.objects.filter(projID=projects)
#
#     proj_dict = {'projects': projects}
#     attr_dict = {'attrs': attrs}
#     context_dict =  dict(proj_dict.items() + attr_dict.items())
#
#     return render_to_response('RT_MW/user_interface.html', context_dict, context)

def user_interface(request):
    context = RequestContext(request)
    user = request.user

    if not user.is_authenticated():
        return HttpResponseRedirect('/')

    projs = []
    projects = []
    attrs = []
    join_list = Join.objects.select_related().filter(users__username__exact=user.username)
    for join in join_list:
        project = join.project
        projects.append(project.projName)
        projs.append(project)
        attr = Specification.objects.filter(projID__projName__exact = project.projName).order_by('attrDate')
        for s in attr:
            attrs.append(s)

    proj_dict = {'projects': projects}
    attr_dict = {'attrs': attrs}
    context_dict =  dict(proj_dict.items() + attr_dict.items())

    return render_to_response('RT_MW/user_interface.html', context_dict, context)


def search_project(request):
    context = RequestContext(request)
    user = request.user
    
    if not user.is_authenticated():
        return HttpResponseRedirect('/')

    projects = []
    join_list = Join.objects.select_related().filter(users__username__exact=user.username)
    for join in join_list:
        project = join.project
        projects.append(project.projName)
    searched = False
    joind = True

    if request.method == 'POST':
        keyword = request.POST['search_textfield']
        projs = Project.objects.filter(projName__contains = keyword)
        searched = True
        
        return render_to_response('RT_MW/user_interface/join_project.html',
                                  RequestContext(request, {'projs':projs,'projects':projects, 'searched':searched, 'joind':joind}))
    else:
        return render_to_response('RT_MW/user_interface/join_project.html',
                                  {'searched':searched, 'joind':joind,'projects':projects},
                                  context)

def join_project(request):
    context = RequestContext(request)
    user = request.user
    
    if not user.is_authenticated():
        return HttpResponseRedirect('/')

    projects = []
    join_list = Join.objects.select_related().filter(users__username__exact=user.username)
    for join in join_list:
        project = join.project
        projects.append(project.projName)

    joind = True

    if request.method == 'POST':
        name = request.POST['project_name']
        enrollment = request.POST['project_enrollment']

        try:
            #project = Project.objects.get(projName=name)
            if not Join.objects.filter(Q(users__username__exact = user.username), Q(project__projName__exact = name)).exists():
                project = Project.objects.get(Q(projName__exact = name), Q(enrollmentKey__exact = enrollment))
                join_form = JoinForm()
                join = join_form.save(commit=False)
                join.users = user
                join.project = project
                join.save()
                joind = True
                return HttpResponseRedirect('/user_interface')
            else:
                joind = False
                return render_to_response('RT_MW/user_interface/join_project.html',
                                          {'joind':joind,'projects':projects},
                                          context)
        except Project.DoesNotExist:
            joind = False
            return render_to_response('RT_MW/user_interface/join_project.html',
                                  {'joind':joind,'projects':projects},
                                  context)
    else:
        joind = True
        return render_to_response('RT_MW/user_interface/join_project.html',
                                  {'joind':joind,'projects':projects},
                                  context)

def create_project(request):
    context = RequestContext(request)
    user = request.user
    
    if not user.is_authenticated():
        return HttpResponseRedirect('/')
    
    projects = []
    join_list = Join.objects.select_related().filter(users__username__exact=user.username)
    for join in join_list:
        project = join.project
        projects.append(project.projName)

    if request.method == 'POST':
        project_form = ProjectForm(data=request.POST)
        lead_form = LeadForm()
        join_form = JoinForm()
        
        if project_form.is_valid():
            project = project_form.save()
            project.projName = project.projName.replace(' ', '_')
            lead = lead_form.save(commit=False)
            join = join_form.save(commit=False)
            
            lead.leader = user
            lead.projects = project

            join.users = user
            join.project = project
            
            project.save()
            lead.save()
            join.save()

            return HttpResponseRedirect('../')
        else:
            project_form = ProjectForm()
            return render_to_response('RT_MW/user_interface/create_project.html', {'project_form': project_form, 'projects':projects}, context)
            
    else:
        project_form = ProjectForm()
        return render_to_response('RT_MW/user_interface/create_project.html', {'project_form': project_form, 'projects':projects}, context)

def complete_project(request, projectid):
    context = RequestContext(request)
    user = request.user
    
    if not user.is_authenticated():
        return HttpResponseRedirect('/')
    
    try:
        email_list = []
        proj = Project.objects.filter(projName = projectid)
        
        join_list = Join.objects.filter(project__projName__exact = projectid)
        for join in join_list:
            member = join.users
            email_list.append(member.email)

        subject =  'The \'' + projectid +'\' project has been completed.'
        content = 'Congraturation! This project has been completed successfully.\n'
        content = content + 'Thank you for your participating\n\n'
        content = content + 'Regards.\n'
        content = content + '\tProject Leader: '+ user.first_name + ' ' + user.last_name +'.\n'

        send_invitation_email(subject,content,email_list)
        return HttpResponseRedirect('/project_detail/'+projectid+'/')
    except Project.DoesNotExist and Join.DoesNotExist:
        return render_to_response('RT_MW/project_detail.html',
                                  {'invited':invited,'projectid':projectid},
                                  context)

def create_todo_attr(request, projectid):
    context = RequestContext(request)
    user = request.user
    
    if not user.is_authenticated():
        return HttpResponseRedirect('/')
    
    projects = []
    join_list = Join.objects.select_related().filter(users__username__exact=user.username)
    for join in join_list:
        project = join.project
        projects.append(project.projName)
    
    if request.method == 'POST':
        new_category = request.POST['new_category']
        try:
            attr_form = AttributeForm()
            
            attr = attr_form.save(commit=False)
            attr.attrTitle = request.POST['attrTitle']
            year = request.POST['attrDate_year']
            month = request.POST['attrDate_month']
            day = request.POST['attrDate_day']
            attr.attrDate = datetime.datetime(int(year),int(month),int(day))
            attr.priority = request.POST['priority']
            attr.attrDesc = request.POST['attrDesc']
            attr.flag = False
            if not new_category.strip() == '':
                if not attr_form.fields['cateID'].queryset.filter(cateName = new_category).exists():
                    Category.objects.create(cateName = new_category)
                attr.cateID = Category.objects.get(cateName__exact = new_category)
            else:
                attr.cateID = Category.objects.get(cateID__exact = request.POST['cateID'])
            attr.projID = Project.objects.get(projName__exact = projectid)
            attr.save()

            return HttpResponseRedirect('/project_detail/'+projectid)
        except:
            attr_form = AttributeForm()
            return render_to_response('RT_MW/project_detail/create_todo_attr.html',
                                      {'attr_form':attr_form,'projectid':projectid,'projects':projects},
                                      context)
    else:
        attr_form = AttributeForm()
        return render_to_response('RT_MW/project_detail/create_todo_attr.html',
                                  {'attr_form':attr_form,'projectid':projectid,'projects':projects},
                                  context)

def delete_project(request, projectid):
    context = RequestContext(request)
    user = request.user
    
    if not user.is_authenticated():
        return HttpResponseRedirect('/')

    Lead.objects.filter(Q(leader__username__exact = user.username) & Q(projects__projName__exact = projectid)).delete()
    Join.objects.filter(project__projName__exact = projectid).delete()
    Specification.objects.filter(projID__projName__exact = projectid).delete()
    Project.objects.get(projName=projectid).delete()
    
    return HttpResponseRedirect('/user_interface')

def delete_todo_attr(request,projectid,attrid):
    context = RequestContext(request)
    user = request.user

    if not user.is_authenticated():
        return HttpResponseRedirect('/')

    Specification.objects.filter(attrID=attrid).delete()

    return HttpResponseRedirect('/project_detail/'+projectid+'/')


def detail_todo_attr(request, projectid, attrid):
    user = request.user

    if not user.is_authenticated():
        return HttpResponseRedirect('/')

    projects = []
    join_list = Join.objects.select_related().filter(users__username__exact=user.username)
    for join in join_list:
        project = join.project
        projects.append(project.projName)

    context = RequestContext(request)

    context_dict = {'attr': attrid,'projectid':projectid,'projects':projects}
    project = Project.objects.get(projName = projectid)
    
    try:
        attr = Specification.objects.get(attrID=attrid, projID=project.projID)
        attrlist = Specification.objects.filter(attrDate=attr.attrDate, projID=project.projID)

        context_dict['specs'] = attrlist
        context_dict['specification'] = attr

    except Project.DoesNotExist:
        pass

    return render_to_response('RT_MW/project_detail/detail_todo_attr.html', context_dict, context)

def single_todo_attr(request, projectid, attrid):
    user = request.user

    if not user.is_authenticated():
        return HttpResponseRedirect('/')

    projects = []
    join_list = Join.objects.select_related().filter(users__username__exact=user.username)
    for join in join_list:
        project = join.project
        projects.append(project.projName)

    context = RequestContext(request)

    context_dict = {'attr': attrid,'projectid':projectid,'projects':projects}
    project = Project.objects.get(projName = projectid)

    try:
        attr = Specification.objects.get(attrID=attrid, projID=project.projID)

        context_dict['specification'] = attr

    except Project.DoesNotExist:
        pass

    return render_to_response('RT_MW/project_detail/single_todo_attr.html', context_dict, context)

def invite_member(request, projectid):
    context = RequestContext(request)
    user = request.user
    
    if not user.is_authenticated():
        return HttpResponseRedirect('/')

    projects = []
    join_list = Join.objects.select_related().filter(users__username__exact=user.username)
    for join in join_list:
        project = join.project
        projects.append(project.projName)
        
    invited = False

    if request.method == 'POST':
        proj = Project.objects.get(projName = projectid)
        
        fullname = request.POST['member_name']
        reseivers = fullname.split(',')
        email_list = []

        for receiver in reseivers:
            try:
                name = receiver.split(' ')
                first = name[0]
                last = name[1]
                email_list.append(User.objects.get(Q(first_name = first) & Q(last_name =last)).email)
            except:
                pass

        subject = user.first_name + ' ' + user.last_name + ' has sent the invitation for the project \'' + projectid +'\''
        content = 'if you want to join the project, input the project name and enrollment key on the \'joining the project\' page.\n\n'
        content = content + '\t\tProject name   : ' + projectid +'\n'
        content = content + '\t\tEnrollment key : ' + proj.enrollmentKey +'\n\n'
        content = content + 'Thank you.\n\n'

        try:
            send_invitation_email(subject,content,email_list)
            invited = False
            return HttpResponseRedirect('/project_detail/'+projectid+'/')
        except Project.DoesNotExist:
            invited = True
            return render_to_response('RT_MW/project_detail/invite_member.html',
                                  {'invited':invited,'projectid':projectid, 'projects':projects},
                                  context)
    else:
        invited = False
        return render_to_response('RT_MW/project_detail/invite_member.html',
                                  {'invited':invited,'projectid':projectid, 'projects':projects},
                                  context)

def search_member(request, projectid):
    context = RequestContext(request)
    user = request.user
    
    if not user.is_authenticated():
        return HttpResponseRedirect('/')

    projects = []
    join_list = Join.objects.select_related().filter(users__username__exact=user.username)
    for join in join_list:
        project = join.project
        projects.append(project.projName)
        
    searched = False

    keyword = request.POST['search_textfield']
    users = User.objects.filter(Q(first_name__contains = keyword) | Q(last_name__contains = keyword))
    if users.exists():
        searched = True
        
        return render_to_response('RT_MW/project_detail/invite_member.html',
                                    RequestContext(request, {'users':users,'searched':searched,'projectid':projectid,'projects':projects}))
    else:
        searched = False
        return render_to_response('RT_MW/project_detail/invite_member.html',
                                  {'searched':searched,'projectid':projectid,'projects':projects},
                                  context)

def tick_todo_attr(request, projectid, attrid):
    context = RequestContext(request)

    user = request.user
    
    if not user.is_authenticated():
        return HttpResponseRedirect('/')
    tick = 'off'
    try:
        tick = request.POST['tick']
    except:
        pass
    #selectedAttrID = request.POST['attrID']

    attr = Specification.objects.get(attrID = attrid)
    if tick == 'on':
        attr.flag = True
    else:
        attr.flag = False
    attr.save()
    
    return HttpResponseRedirect('/project_detail/'+projectid+'/')
    

def project_detail(request,projectid):
    # def category(request, category_name_url):
    # Request our context from the request passed to us.
    context = RequestContext(request)

    user = request.user
    
    if not user.is_authenticated():
        return HttpResponseRedirect('/')

    # Create a context dictionary which we can pass to the template rendering engine.
    # We start by containing the name of the category passed by the user.
    context_dict = {'projectid': projectid}
    
    leader = False
    lead = Lead.objects.select_related().filter(Q(leader__username__exact = user.username) & Q(projects__projName__exact = projectid))
    
    if not lead.exists():
    	leader = False
    else:
    	leader = True
    context_dict['leader'] = leader

    try:
        project = Project.objects.get(projName=projectid)
        
        projects = []
        join_list = Join.objects.select_related().filter(users__username__exact=user.username)
        for join in join_list:
            proj = join.project
            projects.append(proj.projName)
        
        spec = Specification.objects.filter(projID=project)

        members = []
        joinlist = Join.objects.select_related().filter(project__projID__exact = project.projID)
        for join in joinlist:
            member = join.users
            members.append(member.username)
        
        context_dict['users'] = members
        context_dict['spec'] = spec
        context_dict['project'] = project
        context_dict['projects'] = projects

    except Project.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        print 'error'

    # Go render the response and return it to the client.
    return render_to_response('RT_MW/project_detail.html', context_dict, context)

def quit_project(request, projectid):
    context = RequestContext(request)
    user = request.user
    
    if not user.is_authenticated():
		return HttpResponseRedirect('/')
		
    Join.objects.filter(Q(users__username__exact = user.username) & Q(project__projName__exact = projectid)).delete()

    return HttpResponseRedirect('/user_interface')
