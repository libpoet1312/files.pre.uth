from django.shortcuts import render, redirect
from .models import File, Author, User, Tag, Course
from django.views import generic
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import FileForm
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .filters import FileFilter
from django.shortcuts import get_object_or_404, get_list_or_404


def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_files = File.objects.all().count()
    num_courses = Course.objects.all().count()
    num_authors = Author.objects.count()
    files = File.objects.all()
    context = {
        'num_files': num_files,
        'num_courses': num_courses,
        'num_authors': num_authors,
        'files': files,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class RegisterView(CreateView):
    model = User
    fields = ['username', 'password', 'first_name', 'last_name', 'email']
    template_name = 'www/registration.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Hash password before sending it to super
        form.instance.password = make_password(form.instance.password)
        return super().form_valid(form)
'''
class CourseDetail(generic.DetailView):
    slug_url_kwarg = 'the_slug'
    template_name = "course_detail.html"
    context_object_name = 'file_list'

    def get_queryset(self):
        print(self.kwargs['the_slug'])
        self.course = get_object_or_404(Course, courseid=self.kwargs['the_slug'])

        file_list = File.objects.filter(course=self.course)
        print("edw",Course.get_course_files(self.course))
        return Course.get_course_files(self.course)'''

def filter(request):
    qs = File.objects.all()
    courses = Course.objects.all()

    text_contains_query = request.GET.get('text_contains')
    course = request.GET.get('course')


    if is_valid_queryparam(text_contains_query):
        print('skata')
        qs = qs.filter(Q(title__icontains=text_contains_query) |
                       Q(summary__icontains=text_contains_query),
                       )
    print(course)
    if is_valid_queryparam(course) and course != 'Choose...':
        print('edw')
        qs = qs.filter(course__courseid=course)

    return qs

class CourseListView(generic.ListView):
    model = Course
    template_name = "course_list.html"
    context_object_name = 'course_list'
    paginate_by = 10

class FileListViewbyCourse(ListView):
    context_object_name = 'file_list'
    template_name = 'www/course_detail.html'

    def get_queryset(self):
        print("edw")
        return File.objects.all().filter(course__slug=self.kwargs['the_slug'])

    def get_context_data(self, **kwargs):
        context = super(FileListViewbyCourse, self).get_context_data(**kwargs)
        context['course'] = Course.objects.get(slug=self.kwargs['the_slug'])
        context['courses'] = Course.objects.all()
        print(context['course'])

        context['file_list'] = self.get_queryset()
        print(context)
        return context

def FileListView(request):
    qs = filter(request)
    print('skata')
    print(qs)
    context = {
        'file_list': qs,
        'courses': Course.objects.all()
    }
    return render(request, "www/file_list.html", context)



'''
class FileListView(generic.ListView):
    model = File
    template_name = "file_list.html"
    #context_object_name = 'file_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['file_list'] = File.objects.all()
        context['course_list'] = Course.objects.all()
        return context

    def get_queryset(self):
        file_list = File.objects.all()
        text_search = self.request.GET.get('search_query',)

        course = self.request.GET.get('course',)
        tag = self.request.GET.get('tag',)
        print(course)
        c = Course.objects.all().filter(name__exact=course)
        print(c)
        if text_search:
            file_list = File.objects.all().filter(
                Q(title__icontains=text_search) |
                Q(summary__icontains=text_search),
            )

        print(file_list)
        return file_list

'''


class FileDetailView(generic.DetailView):
    slug_url_kwarg = 'the_slug'
    model = File


class Info(generic.TemplateView):
    template_name = 'www/info.html'

@login_required(login_url='')
def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST,request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.save()
            return redirect('www:index')
    else:
        form = FileForm()
    return render(request, 'www/create_file.html', {
    'form':form
    })

    """Display User Profile"""
@login_required(login_url='')
def get_user_profile(request):
    user = request.user
    return render(request, 'www/user_profile.html', {"user": user})

def is_valid_queryparam(param):
    return param != '' and param is not None



def BootstrapFilterView(request):
    qs = filter(request)
    print('skata')
    print(qs)
    context = {
        'queryset': qs,
        'courses': Course.objects.all()
    }
    return render(request, "www/search.html", context)