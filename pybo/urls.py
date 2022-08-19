from django.urls import path, include
from .views import base_views, answer_views, comment_views, question_views, vote_views

from . import views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

app_name = 'pybo'
urlpatterns = [

    # base_views.py
    path('', base_views.index, name='index'),
    path('question_download', base_views.question_download, name='question_download'),
    path('<int:question_id>/', base_views.detail, name='detail'),

    # question_views.py
    path('question/create/', question_views.question_create, name='question_create'),
    path('question/create/upload/', question_views.question_create_upload, name='question_create_upload'),
    path('question/file_download/<int:file_id>/', question_views.question_file_download, name='question_file_download'),
    path('question/modify/<int:question_id>/', question_views.question_modify, name='question_modify'),
    path('question/modify/<int:question_id>/delete', question_views.question_modify_delete, name='question_modify_delete'),
    path('question/modify/<int:question_id>/upload/', question_views.question_modify_upload, name='question_modify_upload'),
    path('question/delete/<int:question_id>/', question_views.question_delete, name='question_delete'),

    # answer_views.py
    path('answer/create/<int:question_id>/', answer_views.answer_create, name='answer_create'),
    path('answer/modify/<int:answer_id>/', answer_views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/', answer_views.answer_delete, name='answer_delete'),

    # comment_views.py
    path('comment/create/question/<int:question_id>/', comment_views.comment_create_question,
         name="comment_create_question"),
    path('comment/modify/question/<int:comment_id>/', comment_views.comment_modify_question,
         name="comment_modify_question"),
    path('comment/delete/question/<int:comment_id>/', comment_views.comment_delete_question,
         name="comment_delete_question"),
    path('comment/create/answer/<int:answer_id>/', comment_views.comment_create_answer,
         name="comment_create_answer"),
    path('comment/modify/answer/<int:comment_id>/', comment_views.comment_modify_answer,
         name="comment_modify_answer"),
    path('comment/delete/answer/<int:comment_id>/', comment_views.comment_delete_answer,
         name="comment_delete_answer"),
    path('vote/question/<int:question_id>/', vote_views.vote_question, name='vote_question'),
    path('vote/answer/<int:answer_id>/', vote_views.vote_answer, name='vote_answer'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
