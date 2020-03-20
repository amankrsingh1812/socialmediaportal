from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import Dashboardform
from .forms import AdminForm
from .models import Employee
from .newscrap import run
from authy.api import AuthyApiClient

# authy_api = AuthyApiClient('rTXVoZCwu7fgZXa5EahpsMqb4aYqcvIW')

# Create your views here.
from django.contrib.auth import authenticate, login, logout


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        # sms = authy_api.users.request_sms(authy_id)
        # if sms.ok():
        #     print(sms.content)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if request.GET.get('next') is not None:
                return redirect(request.GET.get('next'))
            return redirect("/dashboard")
        else:
            return render(request, 'login.html', {'failed_login': 'yes'})
        # print(request.GET.get('next'))
    else:
        if request.user.is_authenticated:
            return redirect("/dashboard")
        return render(request, 'login.html', {'failed_login': 'no'})


@login_required
def home1(request):
    if request.method == 'POST':
        # logout(request)
        form = Dashboardform(request.POST, request.FILES)
        ans=""
        if form.is_valid():
            if request.POST.get("inputtextFacebook") != '':
                facebook_id = request.POST.get("inputtextFacebook")
                facebook_id = facebook_id.strip()
                # print(len(facebook_id))
                ans = abcd(facebook_id)
                # ans="hhh"
                # ans="****************************posts-section********************************\nPost Details: 1 Deb Ris You are too good to handle !!! 03/03/2020, 06:47 no emotions no likes no loves no wowes no hahas no sads no angries no shares 2 comments\nComment is :"
                # print(ans)
                a=ans
                print(a[0:4])
            print(request.POST.get("inputtextTwitter"))
            if 'inputfileTwitter' in request.FILES.keys():
                print(request.FILES['inputfileTwitter'])
        response = HttpResponse(ans, content_type="text/plain")
        return response
    return render(request, 'dashboard.html')


@login_required
def home2(request):
    employees = Employee.objects.filter()
    emp = []
    for e in employees:
        emp.append(e.emp_name)
        print(e.emp_name)
    cemp=employees[0]
    # if request.method == 'POST':
    # logout(request)

    return render(request, 'dashboardn.html', {'emp': emp,'pname':emp[0],'cemp':cemp})

@login_required
def home4(request,pname):
    employees=Employee.objects.filter()
    emp=[]
    for e in employees:
        emp.append(e.emp_name)
        print(e.emp_name)
    print(pname)
    cemp=Employee.objects.get(emp_name=pname)
    # if request.method == 'POST':
        # logout(request)
    return render(request, 'dashboardn.html',{'emp':emp,'pname':pname,'cemp':cemp})

@login_required
def home3(request):
    if request.method == 'POST':
        # logout(request)

        form = AdminForm(request.POST, request.FILES)
        print(request.POST)
        ans=""
        if form.is_valid():
            print("valid")
            form.save(commit=True)
            return render(request, 'dashboardn.html')
        else:
            print('Invalid')
            return HttpResponse("Please Fill Correct Details")
    return render(request, 'admindashboard.html')

def output(request):
    if request.method == "POST":
        d={}
        e={}
        f={'Terror bend of mind': {'affin_score': -11.0, 'vader_score': {'neg': 0.407, 'neu': 0.593, 'pos': 0.0, 'compound': -0.8625}}, 'Discrimination': {'affin_score': -35.0, 'vader_score': {'neg': 0.12, 'neu': 0.69, 'pos': 0.19, 'compound': 0.3239}}, 'Abusive': {'affin_score': -101.0, 'vader_score': {'neg': 0.294, 'neu': 0.507, 'pos': 0.198, 'compound': -0.4738}}, 'Interpersonal conflict': {'affin_score': -50.0, 'vader_score': {'neg': 0.482, 'neu': 0.518, 'pos': 0.0, 'compound': -0.9847}}, 'Communication problems': {'affin_score': -3.0, 'vader_score': {'neg': 0.174, 'neu': 0.712, 'pos': 0.114, 'compound': -0.1779}}, 'Violent tendency': {'affin_score': -6.0, 'vader_score': {'neg': 0.114, 'neu': 0.636, 'pos': 0.25, 'compound': 0.6237}}, 'Gossip': {'affin_score': -11.0, 'vader_score': {'neg': 0.069, 'neu': 0.755, 'pos': 0.176, 'compound': 0.503}}}
        for i in range(26):
            d[i]="a"
            e[i]="b"
        print(request.POST.get('fb_id'))
        facebook_id = "https://www.facebook.com/profile.php?id=100041648746887&__tn__=%2Cd-]-h-R&eid=ARBl5E-jNndxZu4Pob1DHEdPY4lyyJmBV1V6wDyb7JyGPcNNaVpsXLjGD__XajvKlGxD61FsaxIUysG9"
        facebook_id=request.POST.get('fb_id')
        return run(request,facebook_id)
        # g={}
        # print(f)
        # for key in f:
        #     g[key]={'1':f[key],'2':f[key]}
        # s1="asdfgffffffffffffffffffffffffffffffffffffffxdffffffffffffffffffffffzfsdddddddddddd \n hftttttttttttttt"
        # print(zip(f,f))
        # return render(request,'result.html',{'kfpa':d,'kfo':e,'g':g,'s1':s1,'s2':s1})
    return HttpResponse("Invalid Request")
#
# def zipread():
#     import pandas as pd
#     import zipfile
#
#     zf = zipfile.ZipFile('C:/Users/Desktop/THEZIPFILE.zip')
#     df = pd.read_csv(zf.open('intfile.csv'))
def abcd(f_id):
    from .scrap import run
    return run(f_id)
    # return run("https://www.facebook.com/profile.php?id=100041648746887&__tn__=%2Cd-]-h-R&eid=ARBl5E-jNndxZu4Pob1DHEdPY4lyyJmBV1V6wDyb7JyGPcNNaVpsXLjGD__XajvKlGxD61FsaxIUysG9")


def logout1(request):
    logout(request)
    return redirect("/login")
