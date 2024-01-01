from django.db import models

# Create your models here.
class Blogpost(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500, default="")
    head0 = models.CharField(max_length=500)
    chead0 = models.TextField(max_length=50000)
    head1 = models.CharField(max_length=500)
    chead1 = models.TextField(max_length=50000)
    head2 = models.CharField(max_length=50)
    chead2 = models.TextField(max_length=50000)
    pub_date = models.DateField()
    thumbnail = models.ImageField(upload_to="blog/images", default="")

    def __str__(self):
        return self.title