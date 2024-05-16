from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.templatetags.static import static
from django.contrib.auth.models import User
# Create your models here.


class CarBrends(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class CarModels(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    carbrends = models.ForeignKey(CarBrends, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class CarYear(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class CarPrice(models.Model):
    price_1 = models.CharField(max_length=20, null=True, blank=True)
    price_2 = models.CharField(max_length=20, null=True, blank=True)
    price_3 = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.price_1}, {self.price_2}, {self.price_3}"


class Cars(models.Model):
    is_konditsioner = models.BooleanField()
    is_gps = models.BooleanField()
    is_bagaj = models.BooleanField()
    is_musiqa = models.BooleanField()
    is_kamar = models.BooleanField()
    is_audio_kiritsh = models.BooleanField()
    is_bluethooth = models.BooleanField()
    is_uzoq_masofa = models.BooleanField()
    is_uxlash_stoli = models.BooleanField()
    is_kalit_plut = models.BooleanField()
    is_bortli_kompyuter = models.BooleanField()

    image = models.ImageField(upload_to="static/car/image", null=True, blank=True)
    kilometers = models.IntegerField(null=True, blank=True)
    mator = models.CharField(max_length=50, null=True, blank=True)
    sat_down = models.IntegerField(null=True, blank=True)
    baggage = models.CharField(max_length=50, null=True, blank=True)
    fuel = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    carmodels = models.ForeignKey(CarModels, related_name="carmodels", on_delete=models.SET_NULL, null=True, blank=True)
    caryear = models.ForeignKey(CarYear, related_name="caryear", on_delete=models.SET_NULL, null=True, blank=True)
    carprices = models.ForeignKey(CarPrice, related_name="carprices", on_delete=models.SET_NULL, null=True, blank=True)
    update = models.DateTimeField(auto_now=True)
    carprice = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.carmodels.name)

    @property
    def get_image(self):
        return self.image.url if self.image else static('')

    def save(self, *args, **kwargs):
        # Ushbu misolda allaqachon fayl borligini tekshiring
        try:
            this = Cars.objects.get(id=self.id)
            # Agar fayl mavjud bo'lsa va yangi fayl bilan bir xil bo'lmasa, eski faylni o'chiring
            if this.image and this.image != self.image:
                this.image.delete(save=False)
        except Cars.DoesNotExist:
            pass

        super(Cars, self).save(*args, **kwargs)


class CarRentai(models.Model):
    user = models.ForeignKey(User, related_name="user_profile", on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    images = models.ImageField(upload_to="static/users/img", null=True, blank=True)
    pasport = models.ImageField(upload_to="static/users/pasport", null=True, blank=True)
    prava = models.ImageField(upload_to="static/users/prava", null=True, blank=True)
    phone = models.CharField(max_length=13, null=True, blank=True, unique=True)
    def __str__(self):
        return str(self.user)

    @property
    def get_image_user(self):
        return self.images.url if self.images else static('admins/default-profile-picture.png')
    
    @property
    def get_image_pasport(self):
        return self.pasport.url if self.pasport else static('')
    
    @property
    def get_image_prava(self):
        return self.prava.url if self.prava else static('')


class Manzil1(models.Model):
    manzil1 = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.manzil1}"

class Manzil2(models.Model):
    manzil2 = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.manzil2}"

class Booking(models.Model):
    manzil1 = models.ForeignKey(Manzil1, on_delete=models.SET_NULL, null=True, blank=True)
    manzil2 = models.ForeignKey(Manzil2, on_delete=models.SET_NULL, null=True, blank=True)
    sana1 = models.DateField()
    sana2 = models.DateField()
    vaqt = models.CharField(max_length=7, null=True, blank=True)

    def __str__(self):
        return f"{self.manzil1}"

class Review(models.Model):
    is_comentary = models.BooleanField(null=True, default=False)
    STATUS_CHOICES = (
        ('yangi', 'Yangi'),
        ('berildi', 'Berildi'),
        ('qaytarildi', 'Qaytarildi'),
        ('rad etildi', 'Rad etildi'),
    )
    carrentai = models.ForeignKey(CarRentai, related_name="carrentai", on_delete=models.CASCADE, null=True, blank=True)
    cars = models.ForeignKey(Cars, related_name="cars", on_delete=models.SET_NULL, null=True, blank=True)
    booking = models.ForeignKey(Booking, related_name="booking", on_delete=models.SET_NULL, null=True, blank=True)
    review = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='yangi', null=True)
    update = models.DateTimeField(auto_now=True)
    createdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.cars.carmodels.name)

