import os
from django.conf import settings
from django.http import HttpResponse, Http404

def upload(request):
    if request.POST:
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render_to_response('project/upload_successful.html')
    else:
        form = FileForm()
    args = {}
    args.update(csrf(request))
    args['form'] = form

    return render_to_response('project/create.html', args)


def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read())
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
