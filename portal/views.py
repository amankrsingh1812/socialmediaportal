from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import Dashboardform

# Create your views here.
from django.contrib.auth import authenticate, login, logout


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
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
