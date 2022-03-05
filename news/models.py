from django.db import models
from django.utils import timezone
from datetime import datetime, date
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from PIL import Image
from django.utils.text import slugify
from django.core.files.storage import default_storage
from io import BytesIO

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(default='defaultthumbnail.jpg', upload_to='posts_thumbnails')
    category = models.CharField(max_length=100, default='INVESTING')
    body = models.TextField(blank=True, null=True)
    post_date = models.DateField(default=date.today)

    def __str__(self):
        return self.title

    #def save(self, *args, **kwargs):
        # run save of parent class above to save original image to disk
     #   super().save(*args, **kwargs)

      #  memfile = BytesIO()

       # img = Image.open(self.image)
        #if img.height > 1000 or img.width > 1000:
         #   output_size = (1000, 1000)
          #  img.thumbnail(output_size, Image.ANTIALIAS)
           # img.save(memfile, 'JPEG', quality=95)
            #default_storage.save(self.image.name, memfile)
            #memfile.close()
            #img.close()


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    conf_num = models.CharField(max_length=15)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.email + " (" + ("not " if not self.confirmed else "") + "confirmed)"


class Newsletter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=150)
    contents = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.subject + " " + self.created_at.strftime("%B %d, %Y")

    def send(self, request):
        contents = self.contents.body
        subscribers = Subscriber.objects.filter(confirmed=True)
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        for sub in subscribers:
            message = Mail(
                    from_email=settings.FROM_EMAIL,
                    to_emails=sub.email,
                    subject=self.subject,
                    html_content=contents + (
                        '<br><a href="{}/delete/?email={}&conf_num={}">Unsubscribe</a>.').format(
                            request.build_absolute_uri('/delete/'),
                            sub.email,
                            sub.conf_num))
            sg.send(message)