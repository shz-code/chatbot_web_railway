import json
import random
import nltk
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from chatbot_model.response import chatbot
from conversation.models import User, Conversation

from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent
file_path = BASE_DIR / "chatbot_web/download.txt"

def handle_page_not_found(request, exception):
    return render(request, "404.html")


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# Create your views here.
def index(request):
    try:
        nltk.data.find("tokenizers/punkt")
    except:
        nltk.download("punkt")
    return render(request, "index.html")

def chat_download(request):
    if request.user.is_authenticated:
        conversations = Conversation.objects.all()
        if os.path.exists(file_path):
            os.remove(file_path)
        
        with open(file_path, 'w+') as file:
            for con in conversations:
                file.write(f'{con.msg} \n')
        
        content = open(file_path).read()
        return HttpResponse(content, content_type='text/plain')
    return render(request, "no_permission.html")

def bot_response(request):
    notFount = [
        "Sorry I don't understand your question currently. It will be stored for my training purpose.",
        "I do not know the answer of this question. I will learn it shortly."
    ]
    if request.method == "POST":
        data = json.loads(request.body)
        msg = data['msg']
        username = data['username']
        user , created = User.objects.get_or_create(name=username)
        Conversation.objects.create(
            user = user,
            msg = msg,
            user_ip = get_client_ip(request),
            user_device = request.META['HTTP_USER_AGENT']
        )
        res = chatbot(msg)
        if res == "404":
            res = random.choice(notFount)
    return JsonResponse({'msg': res}, safe=False)