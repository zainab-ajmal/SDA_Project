from django.contrib import admin
from django.urls import path, include
from app1 import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index_page, name='index'),
    path('signup/',views.signup_page,name='signup'), 
    path('login/',views.login_page,name='login'),
    path('home/',views.home_page,name='home'),
    path('quotes/',views.quotes_page,name='quotes'),
    path('prompts/',views.prompts_page,name='prompts'),
    path('stickynotes/',views.stickynotes_list.as_view(),name="stickynotes.list"),
    path ('stickynotes/<int:pk>/',views.stickynotes_detailview.as_view(),name="stickynotes.detail"),
    path ('stickynotes/<int:pk>/edit/',views.stickynotes_updateview.as_view(),name="stickynotes.update"),
    path ('stickynotes/<int:pk>/delete/',views.stickynotes_deleteview.as_view(),name="stickynotes.delete"),
    path('stickynotes/new/',views.stickynotes_createview.as_view(),name="stickynotes.new"),
    path('notes/', views.notes_listview.as_view(), name="notes.list"),
    path('notes/new/',views.notes_createview.as_view(),name="notes.new"),
    path('notes/<int:pk>/', views.notes_detailview.as_view(), name="notes.detail"),
    path('notes/<int:pk>/edit/', views.notes_updateview.as_view(), name="notes.update"),
    path('notes/<int:pk>/delete/', views.notes_deleteview.as_view(), name="notes.delete"),
    path('tinymce/', include('tinymce.urls')), #for using tinymce editor
    path('leaderboard/', views.leaderboard, name="leaderboard"),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'), 


   

    path('timetable/', views.timetable, name='timetable'),
    path('add_event/', views.add_event, name='add_event'),
    path('todo_home/', views.index, name='todo_home'),  # Main Todo List page
    path('add/', views.add_task, name='add_task'),
    path('update/<int:task_id>/', views.update_task, name='update_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('reminder_view/', views.reminder_view, name='reminder_view'),
    path('add/', views.add_reminder, name='add_reminder'),
    path('delete/<int:reminder_id>/', views.delete_reminder, name='delete_reminder'),
    path('books/', views.book_view, name='book_view'),  # New book view
    path('upload/', views.upload_book, name='upload_book'),
    path('books/', views.get_books, name='get_books'),
    path('search/', views.search_books, name='search_books'),

    
]
