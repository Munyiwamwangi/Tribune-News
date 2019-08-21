from django.db import models

# Create your models here.
class Editor(models.Model):
    first_name = models.CharField(max_length =30)
    last_name = models.CharField(max_length =30)
    email = models.EmailField()
    phone_number = models.CharField(max_length = 10,blank =True)

    def __str__(self):
        return self.first_name

    def save_editor(self):
        self.save()

    # def delete_editor(self):
    # 	self.delete()

class tags(models.Model):
    name = models.CharField(max_length =30)


    # def save_tags(self):
    #     self.save()

    # def delete_tags(self):
    # 	self.delete()

class Article(models.Model):
    title = models.CharField(max_length =60)
    post = models.TextField()
    editor = models.ForeignKey('Editor',on_delete=models.DO_NOTHING)
    tags = models.ManyToManyField(tags)
    pub_date = models.DateTimeField(auto_now_add=True)


    # def save_article(self):
    #     self.save()

    # def delete_article(self):
    # 	self.delete()


