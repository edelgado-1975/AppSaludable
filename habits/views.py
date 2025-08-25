

from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Routine, DailyLog, Profile, Tip
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views import generic
from .forms import ProfileForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect


@login_required
def dashboard(request):
    user_level = request.user.profile.level
    if not user_level:
        return redirect('initial_evaluation')

    routine = Routine.objects.filter(level=user_level).first()
    today = timezone.now().date()
    
    # --- ESTE ES EL CAMBIO MÁS IMPORTANTE ---
    if request.method == 'POST':
        # Volvemos a preguntar a la base de datos JUSTO AHORA, en el momento de enviar.
        # ¿Existe un registro para este usuario y este día?
        already_completed = DailyLog.objects.filter(user=request.user, date=today).exists()
        
        # Si NO existe, entonces y solo entonces, lo creamos.
        if not already_completed:
            return redirect('dashboard')
            
        # Si ya existe, simplemente no hacemos nada y dejamos que la página se recargue.
    
    # Esta parte ahora solo sirve para mostrar el estado de la página
    log_today = DailyLog.objects.filter(user=request.user, date=today).first()
    completed_today = log_today is not None
        
    # --- El resto del código se queda exactamente igual ---
    streak_count = 0
    completed_dates = DailyLog.objects.filter(user=request.user).values_list('date', flat=True)
    completed_dates_set = set(completed_dates)
    
    current_date = today
    if not completed_today:
        current_date = today - timedelta(days=1)
    
    while current_date in completed_dates_set:
        streak_count += 1
        current_date -= timedelta(days=1)
        
    if completed_today:
        streak_count += 1
    
    random_tip = Tip.objects.order_by('?').first()

    context = {
        'routine': routine,
        'completed_today': completed_today,
        'streak': streak_count,
        'tip': random_tip,
    }
    return render(request, 'dashboard.html', context)



@login_required
def initial_evaluation(request):
    if request.method == 'POST':
        level = request.POST.get('level')
        request.user.profile.level = level
        request.user.profile.save()
        return redirect('dashboard')
    
    return render(request, 'initial_evaluation.html')



class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('initial_evaluation') 
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    

@login_required
def profile_view(request):
    profile = request.user.profile
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile') 
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form
    }
    return render(request, 'profile.html', context)


@login_required
def history_view(request):
    logs = DailyLog.objects.filter(user=request.user).order_by('-date')
    
    context = {
        'logs': logs
    }
    return render(request, 'history.html', context)

def logout_request(request):
    logout(request)
    return redirect('login')