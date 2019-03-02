from django.shortcuts import render, redirect, HttpResponseRedirect
from accounts.forms import RegistrationForm, EditProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


# Create your views here.
def home(request):
    return render(request, 'accounts/home.html')



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/account/view_profile')

    else:
        form = RegistrationForm()

        args = {'form': form}
        return render(request, 'accounts/reg_form.html', args)


def view_profile(request):
    args = {'user': request.user}
    return render(request, 'accounts/view_profile.html', args)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/account/view_profile')

    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}

        return render(request, 'accounts/edit_profile.html', args)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user = request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/account/view_profile')

        else:
            return redirect('/account/change_password')

    else:
        form = PasswordChangeForm(user = request.user)

        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)


def login_success(request):
    """
    Redirects users based on whether they are in the admins group
    """
    if request.user.groups.filter(name='Manager'):
        return render(request, 'accounts/home.html')

    elif request.user.groups.filter(name='Executive'):
        return render(request, 'accounts/executive.html')

    elif request.user.groups.filter(name='Accountant'):
        return render(request,'accountantapp/Accprofile.html')

    elif request.user.groups.filter(name='Operations'):
        return render(request, 'operationsapp/operations_home.html')

    elif request.user.groups.filter(name='Receptionist'):
        return render(request, 'receptionistapp/receptionist_home.html')

    else:
        return HttpResponseRedirect('Account not found')

