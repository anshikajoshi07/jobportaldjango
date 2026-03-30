from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from .models import StuUser
from django.contrib.auth import authenticate ,login,logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


from .models import DashboardJob
# Create your views here.

def index(request):
   return render(request,'index.html')
 

# recurater ka account create kar ne ke liye   
def recurater(request):
    error = ""
    if request.method == 'POST':
        try:
            # Retrieve form data
            n= request.POST.get('name', '')
            em= request.POST.get('email', '')
            ro = request.POST.get('role', '')
            pa = request.POST.get('password', '')
            Cpa= request.POST.get('Cpassword', '')
            # Debugging logs
            print(f"Name: {n}, Email: {em}, role: {ro},Password: {pa}, Confirm Password: {Cpa}")
            # print(f"")
           
            # Validate password and confirm password
            if pa != Cpa:
                error = "Passwords do not match"
            elif User.objects.filter(username=em).exists():
                error = "Email already exists"
            else:
                # Create the user using Django's built-in User model
                user_obj = User.objects.create_user(username=em, password=pa, first_name=n)
                
                # Save data into the StuUser table
                recuraterUser.objects.create(
                    user=user_obj,
                    name=n,
                    email=em,
                    role=ro,  # Correct field name
                    password=pa,
                    Cpassword=Cpa, 
                    type='recruiter',
                    status='pending'
                    
                )
                login(request,user_obj)
                error = "no"
                
                
        except Exception as ex:
            print(f"Error: {ex}")  # Log the exception for debugging
            error = "yes"


    return render(request, 'recurater.html', {'error': error})



# user account create kar ne ke liye
def user(request):
    error = ""
    if request.method == 'POST':
        try:
            # Retrieve form data
            n = request.POST.get('name', '')
            sn = request.POST.get('surname', '')
            e = request.POST.get('email', '')
            num = request.POST.get('number', '')
            pa = request.POST.get('password', '')
            cpa = request.POST.get('Cpassword', '')
            gen = request.POST.get('gender', '')
            co = request.POST.get('country', '')  # Correct field name
            st = request.POST.get('state', '')
            ex = request.POST.get('experience', '')

            # Debugging logs
            print(f"Name: {n}, Surname: {sn}, Email: {e}, Number: {num}")
            print(f"Password: {pa}, Confirm Password: {cpa}")
            print(f"Gender: {gen}, Country: {co}, State: {st}, Experience: {ex}")

            # Validate password and confirm password
            if pa != cpa:
                error = "Passwords do not match"
            elif User.objects.filter(username=e).exists():
                error = "Email already exists"
            else:
                # Create the user using Django's built-in User model
                user_obj = User.objects.create_user(username=e, password=pa, first_name=n, last_name=sn)
                
                # Save data into the StuUser table
                StuUser.objects.create(
                    user=user_obj,
                    name=n,
                    surname=sn,
                    email=e,
                    number=num,  # Correct field name
                    gender=gen,
                    country=co,  # Correct field name
                    state=st,
                    password=pa,
                    Cpassword=cpa,
                    experience=ex
                )
                print("Data saved successfully in StuUser table")
                error = "no"
        except Exception as ex:
            print(f"Error : {ex}")  # Log the exception for debugging
            error = "yes"

    d = {'error': error}
    return render(request, 'user.html', d)


def loginreq(request):
    error = ""
    if request.method == 'POST':
        e = request.POST.get('email', '')
        p = request.POST.get('password', '')
        user = authenticate(username=e, password=p)
        if user:
            try:
                user1 = recuraterUser.objects.get(user=user)
                if user1.type == "recruiter":
                    if user1.status.lower() == "pending":
                        error = "pending"
                    else:
                        login(request, user)
                        error = "no"
                else:
                    error = "Invalid"
            except recuraterUser.DoesNotExist:
                error = "yes"
        else:
            error = "yes"
    return render(request,'loginreq.html',{'error': error})


def about(request):
     return render(request,'about.html')

# user login ke liye
def loginuser(request):
     error=''
     if request.method == "POST":
            email=request.POST.get('email','')
            password=request.POST.get('password','')
            user=authenticate(request,username=email,password=password)
            if user is not None:
                     login(request,user)
                     error="no"
            else:
                 error="yes"

     return render(request,'loginuser.html',{'error':error})

# admin login ke liye
def loginadmin(request):
     error=''
     if request.method == 'POST':
         em=request.POST.get('email','')
         pa=request.POST.get('password','')
         user=authenticate(username=em,password=pa)
         try:
                 if user.is_staff:
                        login(request,user)
                        error="no"
                     
                 else:
                      error="yes"
         except:
                    error="yes"
     
     return render(request,'loginadmin.html',{'error':error})

# user ke home page ke liye
def user_home(request):
     if not request.user.is_authenticated:
         return redirect('loginuser')
     return render(request,'user_home.html')


# def dashboad(request):
#     if not request.user.is_authenticated:
#         return redirect('loginreq')

#     error = ""
#     if request.method == 'POST':
#         title = request.POST.get('title', '')
#         company = request.POST.get('company', '')
#         location = request.POST.get('location', '')
#         jobtype = request.POST.get('jobtype', '')
#         salary = request.POST.get('salary', '')
#         job_description = request.POST.get('jobDescription', '')

#         try:
#             recruiter = recuraterUser.objects.get(user=request.user)
#             DashboardJob.objects.create(
#                 user=recruiter,
#                 title=title,
#                 company=company,
#                 location=location,
#                 jobtype=jobtype,
#                 salary=salary,
#                 job_description=job_description,
#                 status="Active" 
#             )
#             error = "no"
#         # except:
#         except Exception as e:
#             print(f"Error: {e}")
#             error = "yes"
      
#     return render(request, 'dashboad.html',{'error': error} )


def job_list(request):
    if not request.user.is_authenticated:
        return redirect('loginreq')
    try:
        recruiter = recuraterUser.objects.get(user=request.user)
        jobs = DashboardJob.objects.filter(user=recruiter).order_by('-created_at')
    except recuraterUser.DoesNotExist:
        jobs = []
    return render(request, 'job_list.html', {'jobs':jobs})
    

def edit_job(request, job_id):
    if not request.user.is_authenticated:
        return redirect('loginreq')

    job = get_object_or_404(DashboardJob, id=job_id, user__user=request.user)

    if request.method == 'POST':
        job.title = request.POST.get('title')
        job.company = request.POST.get('company')
        job.location = request.POST.get('location')
        job.jobtype = request.POST.get('jobtype')
        job.salary = request.POST.get('salary')
        job.job_description = request.POST.get('jobDescription')
        job.save()
        messages.success(request,"Post updated successfully")
        return redirect('job_list')
                       
    return render(request, 'edit_job.html', {'job': job})


def delete_job(request, job_id):
    if not request.user.is_authenticated:
        return redirect('loginreq')

    job = get_object_or_404(DashboardJob, id=job_id, user__user=request.user)
    job.delete()
    return redirect('job_list')


def logout_view(request):
    logout(request)
    return redirect('loginuser')

def candidat_app(request):
     return render(request,'candidat_app.html')


def job_listuser(request):
     jobs=DashboardJob.objects.all()
     return render(request,'job_listuser.html',{'jobs':jobs})
  
def recu_home(request):
     if not request.user.is_authenticated:
         return redirect('loginreq')
     return render(request,'recu_home.html')

def admin_home(request):
       return render(request, 'admin_home.html')
     

def rec_nav(request):
     return render(request,'rec_nav.html')

def admin_nav(request):
     return render(request,'admin_nav.html')
  
def admin_cre(request):
      return render(request,'admin_cre.html')

def view_user(request):
       if not request.user.is_authenticated:
            return redirect('view_user')
       data = StuUser.objects.all()
       d={'data':data}
       return render(request,'view_user.html',d)

def view_recu(request):
       if not request.user.is_authenticated:
            return redirect('view_recu')
       data = recuraterUser.objects.filter(status='Accepted')
       d={'data':data}
       return render(request,'view_recu.html',d)

def nrreq(request):
       if not request.user.is_authenticated:
            return redirect('view_recu')
       data = recuraterUser.objects.filter(status='pending')
       d={'data':data}
       return render(request,'nrreq.html',d)

def delete_user(request,pid):
        if not request.user.is_authenticated:
            return redirect('view_user')
        user = StuUser.objects.get(id=pid)
        user.delete()
        return redirect('view_user')


def Change_status(request, pid):
    error = ""
    if not request.user.is_authenticated:
        return redirect('loginreq')  # Redirect to login if not authenticated

    try:
        # Get the recruiter object
        recruiter = get_object_or_404(recuraterUser, id=pid)

        if request.method == 'POST':
            # Get the new status from the form
            status = request.POST.get('status', '')

            # Validate the status
            if status == "accept":
                recruiter.status = "Accepted"
            elif status == "reject":
                recruiter.status = "Rejected"
            else:
                error = "yes"  # Invalid status
                return render(request, 'Change_status.html', {'error': error, 'recu': recruiter})

            # Save the updated status
            recruiter.save()
            error = "no"  # Success
    except Exception as ex:
        print(f"Error: {ex}")  # Log the exception for debugging
        error = "yes"  # Something went wrong

    return render(request, 'Change_status.html', {'error': error, 'recu': recruiter})



@login_required
def change_passwordreq(request):
    if request.method == 'POST':
        current = request.POST.get('current_password')
        new = request.POST.get('new_password')
        confirm = request.POST.get('confirm_password')

        user = request.user

        if not user.check_password(current):
            messages.error(request, "Current password is incorrect.")
        elif new != confirm:
            messages.error(request, "New passwords do not match.")
        else:
            user.set_password(new)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully!")
            return redirect('dashboard')

    return render(request, 'change_passwordreq.html')


@login_required
def change_passwordUser(request):
    if request.method == 'POST':
        current = request.POST.get('current_password')
        new = request.POST.get('new_password')
        confirm = request.POST.get('confirm_password')

        user = request.user

        if not user.check_password(current):
            messages.error(request, "Current password is incorrect.")
        elif new != confirm:
            messages.error(request, "New passwords do not match.")
        else:
            user.set_password(new)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully!")
            return redirect('user_home')

    return render(request, 'change_passwordUser.html')




# @login_required
# def candidate_app(request):
#     recruiter = request.user
#     jobs = DashboardJob.objects.filter(user=recruiter)
#     applications = JobApplication.objects.filter(job__in=jobs).select_related('job', 'candidate')

#     return render(request, 'candidate_app.html', {'applications': applications})

from django.shortcuts import render, redirect
from .models import applicatioForm
from django.views.decorators.csrf import csrf_exempt


# def application_form (request):
#    return render(request, 'application_form.html')

def application_form(request):
    if not request.user.is_authenticated:
        return redirect('job_listuser')

    error = ""
    if request.method == 'POST':
       resume_file = request.FILES.get('resume')
       aadhaar_file = request.FILES.get('aadhaar')

       try:
            job_id = request.POST.get('pid')
            job_instance = DashboardJob.objects.get(id=job_id) if job_id else None
            applicatioForm.objects.create(
                job=job_instance,
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                email=request.POST.get('email'),
                country_code=request.POST.get('country_code'),
                phone=request.POST.get('phone'),
                dob=request.POST.get('dob'),
                address=request.POST.get('address'),
                country=request.POST.get('country'),
                state=request.POST.get('state'),
                resume=resume_file,
                experience_level=request.POST.get('experience_level'),
                experience_details=request.POST.get('experience_details'),
                skills=request.POST.get('skills'),
                aadhaar=aadhaar_file,
                cover_letter=request.POST.get('cover_letter'),
                job_role=request.POST.get('job_role'),
                expected_salary=request.POST.get('expected_salary') or 0
            )
            error = "no"
       except Exception as ex:
            print(f"Error : {ex}")  # Log the exception for debugging
            error = "yes"

    d = {'error': error}
    return render(request, 'application_form.html', d)

from django.shortcuts import render, redirect
from .models import recuraterUser, DashboardJob
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    error = ""
    if request.method == 'POST':
        title = request.POST.get('title', '')
        company = request.POST.get('company', '')
        location = request.POST.get('location', '')
        jobtype = request.POST.get('jobtype', '')
        salary = request.POST.get('salary', '')
        job_description = request.POST.get('jobDescription', '')

        try:
            recruiter = recuraterUser.objects.get(user=request.user)
            print("Recruiter Found:", recruiter.name)  # Debug line
            DashboardJob.objects.create(
                user=recruiter,
                title=title,
                company=company,
                location=location,
                jobtype=jobtype,
                salary=salary,
                job_description=job_description,
                type="dashboard"
            )
            error = "no"
        except recuraterUser.DoesNotExist:
            print("RecruiterUser not found for this user.")
            error = "yes"
        except Exception as e:
            print("Error creating DashboardJob:", e)
            error = "yes"

    return render(request, 'dashboard.html', {'error': error})