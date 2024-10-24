from django.db import models
from django.utils import html 
from django.urls import reverse

#Managers
class SupplyManager(models.Manager):
     
     def Available(self):
          return Supply.objects.filter(status='A')


class Category(models.Model):

    id = models.BigAutoField(verbose_name='شناسه دسته', primary_key=True)
    # position = models.PositiveBigIntegerField(verbose_name="موقعیت", blank=True)
    children = models.ForeignKey('self', default=None, null=True, blank=True,\
             on_delete=models.SET_NULL, related_name='subsets', verbose_name='زیردسته')
    title = models.CharField(max_length=200, verbose_name='عنوان دسته بندی‍')
    status = models.BooleanField(default=True, verbose_name='وضعیت نمایش')



    class Meta:
            
            verbose_name = 'دسته بندی '
            verbose_name_plural = 'دسته بندی ها '
            # ordering = ['position']
            

    def __str__(self):
         return self.title
    
    def get_absolute_url(self):
        return reverse("product:category_list")

class Supply(models.Model):

    STATUS_CHOICE = (
        ('A', 'موجود' ),  
        ('N', 'ناموجود')
    )   

    image = models.ImageField(verbose_name='تصویر محصول', upload_to='media', null=True)
    category = models.ManyToManyField(Category, verbose_name='دسته بندی', related_name='cat')
    title = models.CharField(max_length=100, verbose_name='نام محصول')
    status = models.CharField(max_length=1, verbose_name='وضعیت محصول', choices=STATUS_CHOICE)
    description = models.TextField(verbose_name="توضیحی درباره محصول", blank=True, null=True)
    type = models.ManyToManyField('Type', verbose_name='مدل محصول', related_name='supply_types')
    size = models.ManyToManyField('Size', verbose_name='اندازه محصول', related_name='supply_size')

    #initializing the manager
    objects = SupplyManager()


    class Meta:
    
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'


    def __str__(self):
         return self.title
    
    def image_tag(self):
         return html.format_html("<img width=100; height=75; style='border-radius:10px;'src='{}'>".format(self.image.url))
    image_tag.short_description = short_decsription = 'تصویر محصول'

    def get_absolute_url(self):
        return reverse("product:supply_variant_list", args=[self.id])
    
    def category_to_str(self):
         return " - ".join([category.title for category in self.category.all()])
    category_to_str.short_description = 'دسته بندی'

    def type_to_str(self):
         return " - ".join([type.name for type in self.type.all()])
    type_to_str.short_description = 'مدل ها'

    def size_to_str(self):
         return " - ".join([size.name for size in self.size.all()])
    type_to_str.short_description = 'اندازه ها '


class Type(models.Model):
    
    name = models.CharField('نام مدل', max_length=255, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
      
        verbose_name = 'نوع'
        verbose_name_plural = 'انواع '

    def get_absolute_url(self):
        return reverse("product:variant_list")


class Size(models.Model):
    
    name = models.CharField('عنوان اندازه', max_length=255, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        
        verbose_name = 'اندازه'
        verbose_name_plural = 'اندازه ها'

    def get_absolute_url(self):
        return reverse("product:variant_list")
    


class Variant(models.Model):

    supply=models.ForeignKey(Supply, verbose_name='نام محصول', on_delete=models.CASCADE, related_name='variant_supply')
    type=models.ForeignKey(Type, verbose_name='نوع محصول',  related_name='variant_type', on_delete=models.SET_NULL, blank=True, null=True)
    size=models.ForeignKey(Size, verbose_name='سایز محصول',  related_name='variant_size', on_delete=models.SET_NULL, blank=True, null=True)
    price_buy = models.PositiveIntegerField(verbose_name='قیمت خرید محصول')
    price = models.PositiveIntegerField(verbose_name='قیمت فروش محصول')
    inventory=models.PositiveIntegerField(verbose_name='تعداد', default=1)

    def __str__(self):
        return self.supply.title 

    def __unicode__(self):
        return 'supply id: {}'.format(self.supply.id)
    
    class Meta:
    
        verbose_name = 'محصول با ویژگی'
        verbose_name_plural = ' محصولات با ویژگی'

    def get_absolute_url(self):
        return reverse("product:variant_detail", args=[self.id])
    
