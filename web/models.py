from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator




class RestorantCategory(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='restorant_categorys')

    class Meta:
        db_table = 'web_restorant_category'
        verbose_name = ('restorant_category')
        verbose_name_plural = ('restorant_categorys')
        ordering = ['-id']

    def __str__(self):
        return self.name
    
class Restorant(models.Model):
    name = models.CharField(max_length=255)
    discription = models.CharField(max_length=255)
    rating = models.FloatField(max_length=255)
    time = models.CharField(max_length=255)
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Enter a discount value between 0 and 100"
    )
    image = models.ImageField(upload_to='restorants')
    category = models.ForeignKey(RestorantCategory, on_delete=models.CASCADE)
    class Meta:
        db_table = 'web_restorant'
        verbose_name = ('restorant')
        verbose_name_plural = ('restorants')
        ordering = ['-id']

    def __str__(self):
        return self.name

class Slide(models.Model):
    image = models.ImageField(upload_to='slides')
    restorant = models.ForeignKey(Restorant, on_delete=models.CASCADE)

    class Meta:
        db_table = 'web_slide'
        verbose_name = ('slide')
        verbose_name_plural = ('slides')
        ordering = ['-id']

    def __str__(self):
        return str(self.id)
    


    

class Foodcategory(models.Model):
    name = models.CharField(max_length=255)
    restorant = models.ForeignKey(Restorant, on_delete=models.CASCADE)

    class Meta:
        db_table = 'web_foodcategory'
        verbose_name = ('foodcategory')
        verbose_name_plural = ('foodcategories')
        ordering = ['-id']

    def __str__(self):
        return self.name


class Fooditem(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='fooditems')
    price = models.FloatField()
    is_veg = models.BooleanField(default=False)
    restorant = models.ForeignKey(Restorant, on_delete=models.CASCADE)
    foodcategory = models.ForeignKey(Foodcategory, on_delete=models.CASCADE)

    class Meta:
        db_table = 'web_fooditem'
        verbose_name = ('fooditem')
        verbose_name_plural = ('fooditems')
        ordering = ['-id']

    def __str__(self):
        return self.name