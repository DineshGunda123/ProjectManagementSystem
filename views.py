from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Profile,create_team_member,create_project,Task,Review
from django.contrib.auth.decorators import login_required

# Create your views here.
def login_view(request):
            if request.method == 'POST':
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request,'logged successfully...')
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')
def about_us_view(request):
    return render(request,'aboutus.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        phone = request.POST['phone']
        city = request.POST['city']

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        profile = Profile(user=user, phone=phone, city=city)
        user.save()
        profile.save()
        login(request, user)
        return redirect('login')

    return render(request, 'register.html') 
@login_required
def dashboard_view(request):
    return render(request,'dashbord.html')
@login_required
def createnewteammember_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        contact = request.POST['contact']
        image = request.FILES.get('image')
        gender = request.POST['gender']
        categories = request.POST['categories']
        designations = request.POST['designations']
        
        # Get the current logged-in user
        user = request.user
        
        # Save the team member with the associated user
        team_member = create_team_member.objects.create(
            name=name,
            email=email,
            address=address,
            contact=contact,
            image=image,
            gender=gender,
            categories=categories,
            designations=designations,
            created_by=user 
        )
        team_member.save()
        messages.success(request, 'Team member created successfully.')
        return redirect('home')
    
    return render(request, "createnewteammember.html")
@login_required
def teamembers_view(request):
    post=create_team_member.objects.all()
    return render(request,'teammembers.html',{'post':post})
@login_required
def delete_item(request, item_id):
    item = create_team_member.objects.get(id=item_id)
    item.delete()
    messages.success(request, 'Team member deleted successfully.')
    return redirect('teammembers')  
@login_required
def edit_item(request, item_id):
    item = get_object_or_404(create_team_member, id=item_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        gender = request.POST.get('gender')
        categories = request.POST.get('categories')
        designations = request.POST.get('designations')

        # Updating item fields
        item.name = name
        item.email = email
        item.address = address
        item.contact = contact
        item.gender = gender
        item.categories = categories
        item.designations = designations

        # Handling file upload if any
        if 'image' in request.FILES:
            item.image = request.FILES['image']

        messages.success(request, 'Team member updated successfully.')
        item.save()
        return redirect('teammembers')
    else:
        return render(request, 'editteammember.html', {'item': item})
    
@login_required    
def show_item(request,item_id):
    currentuser=request.user
    item=create_team_member.objects.get(id=item_id)
    return render(request,'show_member_info.html',{'item':item})
@login_required
def createproject_view(request):
    if request.method == 'POST':
        projectname = request.POST['projectname']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        project_manager_id = request.POST['projectmanager']
        project_manager = create_team_member.objects.get(id=project_manager_id)
        team_member_ids = request.POST.getlist('teammembers')
        categories = request.POST['categories']
        comments = request.POST['comments']

        user = request.user

        project = create_project(
            projectname=projectname,
            start_date=start_date,
            end_date=end_date,
            project_manager=project_manager,
            categories=categories,
            comments=comments,
            created_by=user
        )
        project.save()

        for team_member_id in team_member_ids:
            team_member = create_team_member.objects.get(id=team_member_id)
            project.team_members.add(team_member)

        project.save()

        reviewers = [user] 
        for i in range(6):
            reviewer = reviewers[i % len(reviewers)]
            Review.objects.create(
                project=project,
                order=i + 1,
                completed=False,
                reviewer=reviewer,
                suggesionsonpreviouspreviousrevie="",
                algorithmandblockdiagram="",
                datasets="",
                resultanlysis="",
                statusofpape="",
                feedback=""

            )

        messages.success(request, 'Project created successfully.')
        return redirect('home')

    team_members = create_team_member.objects.all()
    return render(request, 'createproject.html', {'team_members': team_members})
@login_required
def search_team_members(request):
    query = request.GET.get('q', '')
    if query:
        members = create_team_member.objects.filter(name__icontains=query)
    else:
        members = create_team_member.objects.all()
    results = [{'id': member.id, 'name': member.name} for member in members]
    return JsonResponse(results, safe=False)
@login_required
def delete_project(request, item_id):
    item = create_project.objects.get(id=item_id)
    item.delete()
    messages.success(request, 'Project deleted successfully.')
    return redirect('projectteams')
@login_required
def edit_project(request, item_id):
    item = get_object_or_404(create_project, id=item_id)
    if request.method == 'POST':
        projectname = request.POST.get('projectname')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        projectmanager_id = request.POST.get('projectmanager')
        comments = request.POST.get('comments')
        status = request.POST.get('status')
        categories = request.POST.get('categories')
        teammembers_ids = request.POST.getlist('teammembers')

        item.projectname = projectname
        item.start_date = start_date
        item.end_date = end_date
        item.projectmanager_id = projectmanager_id
        item.comments = comments
        item.status = status
        item.categories = categories

        item.save()

        # Clear existing team members
        item.team_members.clear()

        # Add new team members
        for member_id in teammembers_ids:
            member = get_object_or_404(create_team_member, id=member_id)
            item.team_members.add(member)

        messages.success(request, 'Project updated successfully.')
        return redirect('projectteams')  

    return render(request, 'createproject.html', {'item': item})
@login_required
def show_project(request,item_id):
    item = get_object_or_404(create_project, id=item_id)
    team_members = item.team_members.all()
    print(team_members)
    return render(request,'show_project_info.html',{'item':item,'team_members':team_members})  
@login_required  
def projectteams_view(request):
    projects = create_project.objects.all()
    project_reviews = []
    for project in projects:
        reviews = project.reviews.all().order_by('order')
        project_reviews.append({'project': project, 'reviews': reviews})

    return render(request, 'projectteams.html', {'project_reviews': project_reviews})
@login_required
def createtask_view(request):
    if request.method == 'POST':
        task_name = request.POST['task']
        project_name = request.POST['project']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        status = request.POST['status']
        comments = request.POST['comments']

        task = Task(
            task=task_name,
            project=project_name,
            start_date=start_date,
            end_date=end_date,
            status=status,
            comments=comments
        )
        task.save()
        messages.success(request, 'Task created successfully.')
        return redirect('home')
    return render(request,'createtask.html')
@login_required
def task_view(request):
    post=Task.objects.all()
    return render(request,'tasks.html',{'post':post})
@login_required
def delete_task_view(request, item_id):
    item = Task.objects.get(id=item_id)
    item.delete()
    messages.success(request, 'Task deleted successfully.')
    return redirect('tasks')
@login_required
def edit_task_view(request,item_id):
    item = get_object_or_404(Task, id=item_id)
    
    if request.method == 'POST':
        item.task = request.POST.get('task')
        item.project_name = request.POST.get('project')
        item.start_date = request.POST.get('start_date')
        item.end_date = request.POST.get('end_date')
        item.status = request.POST.get('status')
        item.comments = request.POST.get('comments')
        item.save()
        messages.success(request, 'Task updated successfully.')
        return redirect('tasks')
    else:
        return render(request, 'createtask.html', {'item': item})

@login_required
def tasks_data_view(request):
    items = Task.objects.all()
    pending = items.filter(status='pending').count()
    completed = items.filter(status='completed').count()
    return render(request, 'tasks_data.html', {'completed': completed, 'pending': pending})

@login_required   
def categories_data_view(request):
    items = create_team_member.objects.all()
    
    webdevelopment_count = items.filter(categories='Webdevelopment').count()
    appdevelopment_count = items.filter(categories='Appdevelopment').count()
    ios_count = items.filter(categories='Ios').count()
    mobileapp_count = items.filter(categories='MobileApp').count()
    ecommerce_count = items.filter(categories='Ecommerce').count()
    design_count = items.filter(categories='Design').count()
    research_count = items.filter(categories='Research').count()
    dataanalysis_count = items.filter(categories='DataAnalysis').count()
    softwaredevelopment_count = items.filter(categories='SoftwareDevelopment').count()
    gamedevelopment_count = items.filter(categories='GameDevelopment').count()
    iot_count = items.filter(categories='IoT').count()
    blockchain_count = items.filter(categories='Blockchain').count()
    aiandml_count = items.filter(categories='AIandML').count()
    
    return render(request, 'categories_data.html', {
        'webdevelopment_count': webdevelopment_count,
        'appdevelopment_count': appdevelopment_count,
        'ios_count': ios_count,
        'mobileapp_count': mobileapp_count,
        'ecommerce_count': ecommerce_count,
        'design_count': design_count,
        'research_count': research_count,
        'dataanalysis_count': dataanalysis_count,
        'softwaredevelopment_count': softwaredevelopment_count,
        'gamedevelopment_count': gamedevelopment_count,
        'iot_count': iot_count,
        'blockchain_count': blockchain_count,
        'aiandml_count': aiandml_count,
    })
@login_required   
def designations_view_data(request):
    items = create_team_member.objects.all()

    designations_count = {
        'Backend_developer_sr': items.filter(designations='Back_end developer(sr)').count(),
        'Backend_developer_jr': items.filter(designations='Back_end developer(jr)').count(),
        'Frontend_developer_sr': items.filter(designations='Frontend developer(sr)').count(),
        'Frontend_developer_jr': items.filter(designations='Frontend developer(jr)').count(),
        'Java_developer_sr': items.filter(designations='Java developer(sr)').count(),
        'Java_developer_jr': items.filter(designations='Java developer(jr)').count(),
        'Kotlin_developer_sr': items.filter(designations='Kotlin developer(sr)').count(),
        'Kotlin_developer_jr': items.filter(designations='Kotlin developer(jr)').count(),
        'Flutter_developer_sr': items.filter(designations='Flutter developer(sr)').count(),
        'Flutter_developer_jr': items.filter(designations='Flutter developer(jr)').count(),
        'Swift_developer_sr': items.filter(designations='Swift developer(sr)').count(),
        'Swift_developer_jr': items.filter(designations='Swift developer(jr)').count(),
        'Android_developer_sr': items.filter(designations='Android developer(sr)').count(),
        'Android_developer_jr': items.filter(designations='Android developer(jr)').count(),
        'iOS_developer_sr': items.filter(designations='iOS developer(sr)').count(),
        'iOS_developer_jr': items.filter(designations='iOS developer(jr)').count(),
        'Ecommerce_backend_sr': items.filter(designations='E-commerce backend developer(sr)').count(),
        'Ecommerce_backend_jr': items.filter(designations='E-commerce backend developer(jr)').count(),
        'Ecommerce_frontend_sr': items.filter(designations='E-commerce frontend developer(sr)').count(),
        'Ecommerce_frontend_jr': items.filter(designations='E-commerce frontend developer(jr)').count(),
        'UIUX_designer_sr': items.filter(designations='UI/UX Designer(sr)').count(),
        'UIUX_designer_jr': items.filter(designations='UI/UX Designer(jr)').count(),
        'Graphic_designer_sr': items.filter(designations='Graphic Designer(sr)').count(),
        'Graphic_designer_jr': items.filter(designations='Graphic Designer(jr)').count(),
        'Research_analyst_sr': items.filter(designations='Research Analyst(sr)').count(),
        'Research_analyst_jr': items.filter(designations='Research Analyst(jr)').count(),
        'Research_assistant_sr': items.filter(designations='Research Assistant(sr)').count(),
        'Research_assistant_jr': items.filter(designations='Research Assistant(jr)').count(),
        'Data_scientist_sr': items.filter(designations='Data Scientist(sr)').count(),
        'Data_scientist_jr': items.filter(designations='Data Scientist(jr)').count(),
        'Data_analyst_sr': items.filter(designations='Data Analyst(sr)').count(),
        'Data_analyst_jr': items.filter(designations='Data Analyst(jr)').count(),
        'Full_stack_developer_sr': items.filter(designations='Full Stack Developer(sr)').count(),
        'Full_stack_developer_jr': items.filter(designations='Full Stack Developer(jr)').count(),
        'Backend_developer_sr': items.filter(designations='Backend Developer(sr)').count(),
        'Backend_developer_jr': items.filter(designations='Backend Developer(jr)').count(),
        'Frontend_developer_sr': items.filter(designations='Frontend Developer(sr)').count(),
        'Frontend_developer_jr': items.filter(designations='Frontend Developer(jr)').count(),
        'Game_developer_sr': items.filter(designations='Game Developer(sr)').count(),
        'Game_developer_jr': items.filter(designations='Game Developer(jr)').count(),
        'Game_designer_sr': items.filter(designations='Game Designer(sr)').count(),
        'Game_designer_jr': items.filter(designations='Game Designer(jr)').count(),
        'IoT_engineer_sr': items.filter(designations='IoT Engineer(sr)').count(),
        'IoT_engineer_jr': items.filter(designations='IoT Engineer(jr)').count(),
        'IoT_developer_sr': items.filter(designations='IoT Developer(sr)').count(),
        'IoT_developer_jr': items.filter(designations='IoT Developer(jr)').count(),
        'Blockchain_developer_sr': items.filter(designations='Blockchain Developer(sr)').count(),
        'Blockchain_developer_jr': items.filter(designations='Blockchain Developer(jr)').count(),
        'Blockchain_analyst_sr': items.filter(designations='Blockchain Analyst(sr)').count(),
        'Blockchain_analyst_jr': items.filter(designations='Blockchain Analyst(jr)').count(),
        'AI_engineer_sr': items.filter(designations='AI Engineer(sr)').count(),
        'AI_engineer_jr': items.filter(designations='AI Engineer(jr)').count(),
        'ML_engineer_sr': items.filter(designations='ML Engineer(sr)').count(),
        'ML_engineer_jr': items.filter(designations='ML Engineer(jr)').count(),
    }

    return render(request, 'designations_data.html', designations_count)
@login_required                                                 
def projects_data_view(request):
    projects = create_project.objects.all()
    pending = 0
    ongoing = 0
    completed = 0
    
    for project in projects:
        reviews = Review.objects.filter(project=project)
        num_reviews = reviews.count()
        num_completed_reviews = reviews.filter(completed=True).count()
        
        if num_completed_reviews == num_reviews:
            completed += 1
        elif num_completed_reviews > 0:
            ongoing += 1
        else:
            pending += 1
    
    return render(request, 'project_status_data.html', {
        'pending': pending,
        'ongoing': ongoing,
        'completed': completed
    })

@login_required  
def project_categories_view(request):
    items = create_project.objects.all()
    
    webdevelopment_count = items.filter(categories='WebDevelopment').count()
    appdevelopment_count = items.filter(categories='AppDevelopment').count()
    mobileapp_count = items.filter(categories='MobileApp').count()
    ecommerce_count = items.filter(categories='Ecommerce').count()
    design_count = items.filter(categories='Design').count()
    research_count = items.filter(categories='Research').count()
    dataanalysis_count = items.filter(categories='DataAnalysis').count()
    softwaredevelopment_count = items.filter(categories='SoftwareDevelopment').count()
    gamedevelopment_count = items.filter(categories='GameDevelopment').count()
    iot_count = items.filter(categories='IoT').count()
    blockchain_count = items.filter(categories='Blockchain').count()
    aiandml_count = items.filter(categories='AIandML').count()
    
    return render(request, 'project_data1.html', {
        'webdevelopment_count': webdevelopment_count,
        'appdevelopment_count': appdevelopment_count,
        'mobileapp_count': mobileapp_count,
        'ecommerce_count': ecommerce_count,
        'design_count': design_count,
        'research_count': research_count,
        'dataanalysis_count': dataanalysis_count,
        'softwaredevelopment_count': softwaredevelopment_count,
        'gamedevelopment_count': gamedevelopment_count,
        'iot_count': iot_count,
        'blockchain_count': blockchain_count,
        'aiandml_count': aiandml_count,
    })
@login_required
def members_data_view(request):
    items = create_team_member.objects.all()
    senior_developer = items.filter(
        designations__in=[
            'Back_end developer(sr)', 
            'Frontend developer(sr)', 
            'Java developer(sr)',
            'Kotlin developer(sr)', 
            'Flutter developer(sr)',  
            'Swift developer(sr)'
        ]
    ).count()
    junior_developer = items.count() - senior_developer
    return render(request, 'members_data.html', {'senior_developer': senior_developer, 'junior_developer': junior_developer})
@login_required
def project_detail(request, project_id):
    project = get_object_or_404(create_project, pk=project_id)
    reviews = Review.objects.filter(project=project).order_by('order')
    
    # Calculate project status
    num_reviews = reviews.count()
    num_completed_reviews = reviews.filter(completed=True).count()
    
    if num_completed_reviews == num_reviews:
        project_status = 'Completed'
    elif num_completed_reviews > 0:
        project_status = 'Ongoing'
    else:
        project_status = 'Pending'
    
    return render(request, 'project_detail.html', {
        'project': project,
        'reviews': reviews,
        'project_status': project_status
    })
@login_required
def review_detail(request, project_id, review_id):
    review = get_object_or_404(Review, pk=review_id, project_id=project_id)
    
    if request.method == 'POST':
        # Handle form submission for review
        review.feedback = request.POST.get('feedback', '')
        review.completed = True
        review.save()
        
        # Redirect to the next review or project detail
        next_review = Review.objects.filter(project_id=project_id, order=review.order + 1).first()
        if next_review:
            return redirect('projectteams')
        else:
            return redirect('project_detail', project_id=project_id)
    
    return render(request, 'review_detail.html', {'review': review})


