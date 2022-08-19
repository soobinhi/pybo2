import os, datetime
import urllib

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.conf import settings

from ..forms import QuestionForm, FileModelForm
from ..models import Question, FileModel


@login_required(login_url='common:login')
def question_create(request):
    """
    pybo 질문 등록
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()

            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

def question_create_upload(request):

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        question = form.save(commit=False)
        question.author = request.user
        question.create_date = timezone.now()
        question.save()

        for idx, file in enumerate(request.FILES.values()):
            fileform = FileModelForm()
            filemodel = fileform.save(commit=False)
            filemodel.subject = file
            filemodel.file = file
            filemodel.question = question
            filemodel.save()
        return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_file_download(request, file_id):
    """
    pybo 파일 다운로드
    """
    filemodel = get_object_or_404(FileModel, pk=file_id)
    path = str(filemodel.file)
    filename= str(filemodel.subject)
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        binary_file = open(file_path, 'rb')
        quote_file_url = urllib.parse.quote(path.encode('utf-8'))
        response = HttpResponse(binary_file.read(), content_type="application/octet-stream; charset=utf-8")
        response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % filename
        return response
    else:
        message = '알 수 없는 오류가 발행하였습니다.'
        return HttpResponse("<script>alert('" + message + "');history.back()'</script>")


@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    pybo 질문 수정
    """
    question = get_object_or_404(Question, pk=question_id)

    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', question_id=question_id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)

            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question_id)
    else:
        form = QuestionForm(instance=question)
    context = {'question': question}
    return render(request, 'pybo/question_form.html', context)

def question_modify_upload(request, question_id):
    #질문 수정
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            for idx, file in enumerate(request.FILES.values()):
                fileform = FileModelForm()
                filemodel = fileform.save(commit=False)
                filemodel.subject = file
                filemodel.file = file
                filemodel.question = question
                filemodel.save()
            return redirect('pybo:detail', question_id=question_id)
    else:
        form = QuestionForm(instance=question)
    context = {'question': question}
    return render(request, 'pybo/question_form.html', context)

def question_modify_delete(request, question_id):
    #파일 삭제
    if request.method == 'POST':
        delcode = request.POST.get('del')
        filemodel = get_object_or_404(FileModel, pk=delcode)
        os.remove(os.path.join(settings.MEDIA_ROOT, str(filemodel.file)))
        filemodel.delete()
        question = get_object_or_404(Question, pk=question_id)
        context = {'question': question}
        return render(request, 'pybo/question_form.html', context)
    return redirect('pybo:index')



@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    pybo 질문 삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    file_list = FileModel.objects.filter(question_id__exact=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('pybo:detail', question_id=question_id)
    for f in file_list:
        os.remove(os.path.join(settings.MEDIA_ROOT, str(f.file)))
    question.delete()
    return redirect('pybo:index')
