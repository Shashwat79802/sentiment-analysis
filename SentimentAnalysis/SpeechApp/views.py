from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout 
from .forms import SignupForm, LoginForm
from django.views.decorators.csrf import csrf_exempt
import pickle
import numpy as np
from .utils import extract_feature
from django.http import JsonResponse


loaded_model = pickle.load(open('../modelForPrediction1.sav', 'rb')) # loading the model file from the storage


# Create your views here.
# Home page
def index(request):
    return render(request, 'index.html')

# signup page
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            print('User created successfully')
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('analyze-audio')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('login')


@csrf_exempt
def analyze_audio(request):
    if request.method == 'GET':
        return render(request, 'analyze-audio.html')

    if request.method == 'POST':
        audio_file = request.FILES['audio']

        feature = extract_feature(audio_file, mfcc=True, chroma=True, mel=True)
        feature_array = np.array(feature)
        feature_reshaped=feature_array.reshape(1,-1)

        prediction=loaded_model.predict(feature_reshaped)
    
    print(prediction[0])
    return JsonResponse({'prediction': prediction[0]})