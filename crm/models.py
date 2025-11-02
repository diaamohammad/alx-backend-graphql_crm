from django.db import models

# (ممكن تضيف موديل Customer و Order لو حبيت، بس ده المهم)

class Product(models.Model):
    name = models.CharField(max_length=255)
    stock = models.IntegerField(default=0) # التاسك 3 بيعتمد على الحقل ده

    def __str__(self):
        return self.name

# ضيف أي موديلز تانية مطلوبة منك هنا...