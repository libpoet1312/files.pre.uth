from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from django.db.models.signals import post_delete
from django.dispatch import receiver
from taggit.managers import TaggableManager

# Create your models here.
class Tag(models.Model):
    """Model representing the Tag of a file """
    name = models.CharField(max_length=200, help_text='Enter a Tag (e.g. First year course)')
    slug = AutoSlugField(populate_from='name', unique=True, null=True, default=None)

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Course(models.Model):

    courseid = models.CharField(max_length=30, help_text='Enter the course id')
    name = models.CharField(max_length=200, help_text='Enter the course name')
    slug = AutoSlugField(populate_from='courseid', unique=True, null=True, default=None)

    def __str__(self):
        """String for representing the Model object."""
        #print("courseid=",self.courseid)
        if self.courseid:
            return self.courseid
        else:
            return None

    def get_name_courseid(self):
        return f'{self.courseid}, {self.name}'

    def get_absolute_url(self):
        """Returns the url to access a detail record for this file."""
        return reverse('www:course-detail', args=[self.slug])

    def get_course_files(self):
        return File.objects.filter(course=self)


class File(models.Model):
    """Model representing a File """
    title = models.CharField(max_length=200)

    slug = AutoSlugField(populate_from='title', unique=True, null=True, default=None)

    # Foreign Key used because a file can only have one author, but authors can have multiple files
    # Author as a string rather than object because it hasn't been declared yet in the file
    author = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)

    # Date of uploading the file #
    dateCreated = models.DateTimeField(auto_now_add=True)

    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the file')

    # ManyToManyField used because tag & course can contain many files. Files can cover many Tags & Courses.
    #tag = models.ManyToManyField(Tag, help_text='Select a tag for this file', blank=True)

    course = models.ManyToManyField(Course, help_text='Select a course for this file')

    upload = models.FileField(upload_to='', null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_course_url(self):
        course = self.course.all()
        #print("course=",course)
        if course:
            course = course[0]
            return reverse('www:course-detail', args=[course])
        return course

    def get_absolute_url(self):
        """Returns the url to access a detail record for this file."""
        return reverse('www:file-detail', args=[self.slug])

    def display_course(self):
        """Create a string for the course. This is required to display course in Admin."""
        string = ' , '.join(course.name for course in self.course.all())
        string2 = ' , '.join(course.courseid for course in self.course.all())

        return string+' '+string2
        #return ' , '.join(course.name for course in self.course.all())+' '+' , '.join(course.courseid for course in self.course.all())


    display_course.short_description = 'Course'


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'


@receiver(post_delete, sender=File)
def submission_delete(sender, instance, **kwargs):
    instance.upload.delete(False)