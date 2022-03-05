from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Subscriber
from .forms import SubscriberForm
import random
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.db import IntegrityError
from django.views.generic import ListView, DetailView



# Helper Functions
def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)


@csrf_exempt
def home(request):
    if request.method == 'POST':
        sub = Subscriber(email=request.POST['email'], conf_num=random_digits())
        try:
            sub.save()
        except IntegrityError:
            return render(request, 'news/index.html', {'email': sub.email, 'action': 'registered, try another one',
                                                       'form': SubscriberForm()})
        message = Mail(
            from_email= settings.FROM_EMAIL,
            to_emails=sub.email,
            subject='Confirm Your Subscription',
            html_content='<strong>Welcome to Market Popcorn!</strong> <br><br>\
                Please complete the subscription by \
                <a href="{}?email={}&conf_num={}"> clicking here\
                </a>. <br>  After confirming the subscription, please do us a favour to get \
                         the popcorn before it became cold, we recommend \
                         following these quick steps:<br><br>\
                         <strong>Gmail users</strong> — move us to your primary inbox <br>\
                         <ul><li> <strong>On your phone?</strong> Hit the 3 dots at top right corner, click "Move to" then "Primary"</li>\
                         <li> <strong>On desktop?</strong> Back out of this email then drag and drop this email into the "Primary" tab \
                         near the top left of your screen</li></ul><br>\
                         <strong>Apple mail users</strong> — tap on our email address at the top of this email\
                         (next to "From:" on mobile) and click “Add to VIPs” <br><br>\
                         <strong>For other users</strong> — follow <a href="https://help.aweber.com/hc/en-us/articles/204029246">these \
                        instructions</a><br><br>We will deliver the wrap-up fresh and hot every morning (7 a.m. US time) from Monday to Friday, we hope you will enjoy it.\
                         Welcome to Market Popcorn again and congratulations on no more waste of time reading the financial news'.format(request.build_absolute_uri('/confirm/'),
                                                    sub.email,
                                                    sub.conf_num))
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        return render(request, 'news/index.html', {'email': sub.email, 'action': 'added! please check your mailbox to'
                                                                                 ' confirm the subscription', 'form': SubscriberForm()})
    else:
        return render(request, 'news/index.html', {'form': SubscriberForm()})


def confirm(request):
    sub = Subscriber.objects.get(email=request.GET['email'])
    if sub.conf_num == request.GET['conf_num']:
        sub.confirmed = True
        sub.save()
        return render(request, 'news/index.html', {'email': sub.email, 'action': 'confirmed'})
    else:
        return render(request, 'news/index.html', {'email': sub.email, 'action': 'denied'})



def delete(request):
    sub = Subscriber.objects.get(email=request.GET['email'])
    if sub.conf_num == request.GET['conf_num']:
        sub.delete()
        return render(request, 'news/index.html', {'email': sub.email, 'action': 'unsubscribed'})
    else:
        return render(request, 'news/index.html', {'email': sub.email, 'action': 'denied'})


def news(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'news/news.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'posts'
    ordering = ['-post_date']
    paginate_by = 4


class PostDetailView(DetailView):
    model = Post