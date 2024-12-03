from django.db.models.query import QuerySet
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from .models import StudyContent
import random #for selecting random quotes form the database
from .models import stickyNote
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView
from .forms import stickyNotesForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from .models import Notebook
from .forms import  NotesForm
from django.http import JsonResponse
from .models import Event
from .models import Task
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Reminder
from .models import UserProfile

from .function import add_points
from .models import Book
from django.core.files.storage import FileSystemStorage

# Create your views here.


#defining constant
LOGIN_URL = '/admin'
SUCCESS_URL='/notes/'

def index_page(request):
    return render(request,'index.html')
def home_page (request):
    return render (request,'home.html')
def signup_page (request):
    if request.method=='POST':
        email=request.POST.get('email')
        username=request.POST.get('username')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')

        if password1!=password2:
            return render(request, 'signup.html', {'error_message': 'Passwords do not match!'})
        else:
            my_user= User.objects.create_user(username=username, email=email, password=password1)
            my_user.save()
            return redirect('login')

    return render(request, 'signup.html')

def login_page(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('password')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
             return render(request, 'login.html', {'error_message': 'Username or Password is incorrect!'})

    return render (request,'login.html')

def quotes_page(request):
    quotes = StudyContent.objects.filter(content_type='quote')
#select if available
    quote = random.choice(quotes) if quotes else None
    content = {
        'quote': quote,
    }
    return render(request, 'quotes.html', content)

def prompts_page(request):
    prompts = StudyContent.objects.filter(content_type='prompt')
#select if available
    prompt = random.choice(prompts) if prompts else None

    content = {
        'prompt': prompt
    }
    return render(request, 'prompts.html', content)
   
class stickynotes_list (LoginRequiredMixin, ListView):
    model= stickyNote
    context_object_name="stickynotes"
    login_url=LOGIN_URL
    template_name="stickynotes_list.html"

    def get_queryset(self):
        return self.request.user.stickynotes.all()  #will make sure that the logged in user gets only their notes and not someone else's
    
class stickynotes_detailview (LoginRequiredMixin, DetailView):
    model = stickyNote
    context_object_name="stickynote"
    login_url=LOGIN_URL
    template_name="stickyNotes_detail.html"

    def get_queryset(self):
        return self.request.user.stickynotes.all() 

class stickynotes_createview (LoginRequiredMixin, CreateView):
    model=stickyNote
    success_url='/stickynotes/'
    template_name = 'stickynotes_form.html' 
    form_class= stickyNotesForm
    login_url=LOGIN_URL

    def form_valid(self,form):
        self.object=form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class stickynotes_updateview (LoginRequiredMixin, UpdateView):
    model= stickyNote
    success_url='/stickynotes/'
    template_name = 'stickynotes_form.html' 
    form_class= stickyNotesForm
    login_url=LOGIN_URL

    def get_queryset(self):
        return self.request.user.stickynotes.all() 

class stickynotes_deleteview (LoginRequiredMixin, DeleteView):
    model= stickyNote
    success_url='/stickynotes/'
    template_name = 'stickynotes_delete.html' 

class notes_listview(LoginRequiredMixin, ListView):
    model = Notebook
    context_object_name="notes"
    template_name = 'notes_list.html'
    login_url=LOGIN_URL

    def get_queryset(self):
        return self.request.user.notes.all()
    
class notes_detailview(LoginRequiredMixin, DetailView):
    model =Notebook
    context_object_name="note"
    login_url=LOGIN_URL
    template_name="notes_detail.html"

    def get_queryset(self):
        return self.request.user.notes.all() 
    
class notes_createview(LoginRequiredMixin, CreateView):
    model = Notebook
    success_url = SUCCESS_URL
    form_class = NotesForm
    template_name='notes_form.html'
    login_url=LOGIN_URL

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

         # rewards for user
        add_points(self.request.user, 10)  #10 points for creating notes

        return HttpResponseRedirect(self.get_success_url())

class notes_updateview(LoginRequiredMixin, UpdateView):
    model = Notebook
    success_url = SUCCESS_URL
    template_name = 'notes_form.html'
    form_class = NotesForm

class notes_deleteview (LoginRequiredMixin, DeleteView):
    model= Notebook
    success_url=SUCCESS_URL
    template_name = 'notes_delete.html' 


#for leaderboard
def leaderboard(request):
    top_users = UserProfile.objects.order_by('-points')[:1]
    return render(request, "leaderboard.html", {"top_users": top_users})


def timetable(request):
    events = Event.objects.all()
    add_points(request.user, 10) 
    return render(request, 'timetable.html', {'events': events})

def add_event(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('date')
        time_from = request.POST.get('time_from')
        time_to = request.POST.get('time_to')
        Event.objects.create(name=name, date=date, time_from=time_from, time_to=time_to)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'})

def index(request):
    """Render the main Todo List page."""
    tasks = Task.objects.all()  # Fetch all tasks
    return render(request, 'todolist.html', {'tasks': tasks})

@csrf_exempt
def add_task(request):
    """Add a new task."""
    if request.method == 'POST':
        data = json.loads(request.body)
        new_task = Task.objects.create(title=data['title'])
        
        return JsonResponse({'id': new_task.id, 'title': new_task.title, 'is_completed': new_task.is_completed})

@csrf_exempt
def update_task(request, task_id):
    """Mark a task as completed or pending."""
    if request.method == 'POST':
        data = json.loads(request.body)
        task = Task.objects.get(id=task_id)
        task.is_completed = data['is_completed']
        task.save()
        add_points(request.user, 10) #add points if user completes a task
        return JsonResponse({'id': task.id, 'title': task.title, 'is_completed': task.is_completed})

@csrf_exempt
def delete_task(request, task_id):
    """Delete a task."""
    if request.method == 'DELETE':
        task = Task.objects.get(id=task_id)
        task.delete()
        return JsonResponse({'status': 'Task deleted successfully'})

def reminder_view(request):
    if request.method == 'GET':
        reminders = Reminder.objects.all()
        return render(request, 'reminder.html', {'reminders': reminders})

@csrf_exempt
def add_reminder(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        description = data.get('description')
        date = data.get('date')
        time = data.get('time')

        reminder = Reminder.objects.create(title=title, description=description, date=date, time=time)
        add_points(request.user, 10) 
        return JsonResponse({'id': reminder.id, 'title': title, 'description': description, 'date': date, 'time': time})

@csrf_exempt
def delete_reminder(request, reminder_id):
    try:
        reminder = Reminder.objects.get(id=reminder_id)
        reminder.delete()
        return JsonResponse({'success': True})
    except Reminder.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Reminder not found'}, status=404)
    

def book_view(request):
    book = Book.objects.all()
    return render(request, 'book.html', {'book': book})

# Fetch all books
def get_books(request):
    books = Book.objects.all()
    if books.exists():
        data = [{"id": book.id, "name": book.name, "description": book.description, "file": book.file.url} for book in books]
        return JsonResponse(data, safe=False)
    return JsonResponse({"message": "No books found"}, status=404)

@csrf_exempt
def upload_book(request):
    if request.method == 'POST':
        # Handle book upload
        name = request.POST.get('name')
        description = request.POST.get('description')
        file = request.FILES.get('file')

        if not (name and description and file):
            return JsonResponse({"message": "All fields are required"}, status=400)

        # Save the file
        fs = FileSystemStorage(location='media/books')
        filename = fs.save(file.name, file)

        # Save the book object
        book = Book.objects.create(name=name, description=description, file=f'books/{filename}')
        return JsonResponse({"message": "Book uploaded successfully!"}, status=201)

    elif request.method == 'GET':
        # Fetch all books
        books = Book.objects.all()
        if books.exists():
            data = [{"id": book.id, "name": book.name, "description": book.description, "file": book.file.url} for book in books]
            return JsonResponse(data, safe=False)
        return JsonResponse({"message": "No books found"}, status=404)

    return JsonResponse({"message": "Invalid request"}, status=400)


# Search for a book
def search_books(request):
    query = request.GET.get('query', '')
    books = Book.objects.filter(name__icontains=query)
    if books.exists():
        data = [{"id": book.id, "name": book.name, "description": book.description, "file": book.file.url} for book in books]
        return JsonResponse(data, safe=False)
    return JsonResponse({"message": "No books found matching your query"}, status=404)
