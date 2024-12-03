from django.db import models
from django.contrib.auth.models import User  # For associating notes with users
from tinymce.models import HTMLField #for notebook's editor
from django.utils.timezone import now

#for study prompts and quotes
class StudyContent(models.Model):
    CONTENT_TYPES = [
        ('quote', 'Quote'),
        ('prompt', 'Prompt'),
    ]

    content = models.TextField()  # The actual quote or prompt
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES)  # Type: Quote/Prompt
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically adds timestamp

    def __str__(self):
        return f"{self.get_content_type_display()}: {self.content[:50]}"


#for sticky notes
class stickyNote(models.Model):
    title = models.CharField(max_length=200)  
    text = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)  # timestamp for note creation
    updated_at = models.DateTimeField(auto_now=True)  # timestamp for note updates

    user= models.ForeignKey(User,on_delete=models.CASCADE, related_name='stickynotes') #associating multiple sticky notes to users

#for notebook
class Notebook(models.Model):
    title = models.CharField(max_length=200)
    text= HTMLField()  #using tinycme
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')


class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    time_from = models.TimeField()
    time_to = models.TimeField()

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=255)  # The task's title
    is_completed = models.BooleanField(default=False)  # Task status
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for task creation

    def __str__(self):
        return self.title


class Reminder(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.title
    

from django.db.models.signals import post_save
from django.dispatch import receiver

# UserProfile model to extend the User model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    points = models.IntegerField(default=0)  # Points field for users

    def __str__(self):
        return self.user.username

# Signal to create UserProfile automatically when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


    


class Book(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='uploads/')  # Save files in media/uploads/
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Field causing the issue

    def __str__(self):
        return self.name