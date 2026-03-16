В доках написано брать *AbstaractBaseUser*, но есть вариант проще и не нужно переписывать Django и это -**AbstaractUser**. Оно все надо чтобы добавлять прочие поля пользователям, так как изначальное Django использует чет свое там под капотом.

Вот так можно создать модельку пользователя:
```python
# accounts/models.py
from django.contrib.auth.models import AbstractUser  
from django.db import models  
  
  
class CustomUser(AbstractUser):  
    age = models.PositiveIntegerField(null=True, blank=True)
```

Далее сделаем формы для регистрации и изменения:

>Напоминание о том что такое **Мета-данные:** Это данные о данных, например дата создания файла, дата последнего редактирования, это как бы то что идет вместе с ним а не внутри него.

``` python
from django.contrib.auth.forms import UserCreationForm, UserChangeForm  
  
from .models import CustomUser  
  
  
class CustomUserCreationForm(UserCreationForm):  
    class Meta(UserChangeForm):  
        model = CustomUser  
        fields =  (  
            'username',  
            'email',  
            'age',  
        )  
  
class CustomUserChangeForm(UserChangeForm):  
    class Meta(UserChangeForm):  
        model = CustomUser  
        fields =  (  
            'username',  
            'email',  
            'age',  
        )
```
При этом чтобы все работало чики-пуки, надо прописать что "мы используем *CustomUser*".

``` python
from django.contrib import admin  
from django.contrib.auth.admin import UserAdmin  
  
from .forms import CustomUserChangeForm, CustomUserCreationForm  
from .models import CustomUser  
  
  
class CustomUserAdmin(UserAdmin):  
    add_form = CustomUserCreationForm  # форма для создания пользователя 
    form = CustomUserChangeForm        # форма чтобы изменять пользователя
    model = CustomUser                 # наша моделька
    list_display = [                   # то что отображается в админке (рисунок 1 снизу)
        "email",  
        "username",  
        "age",  
        "is_staff",  
    ]  
    
	# вот эти поля мы сможем менять при создании пользователя
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("age",)}),) 
    
    # а эти поля мы сможем менять при изменение пользователя, после создания то есть
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("age",)}),)  
  
  
admin.site.register(CustomUser, CustomUserAdmin)
```

*Рисунок 1 - list_display:* ![[99 - Meta/02 - Медиа/Pasted image 20231128104806.png]]
Здесь как раз отображается почта, никнейм, возраст и стаф статус. То что мы и прописали в коде.

Как это дело все тестится...
``` python
from django.contrib.auth import get_user_model  
from django.test import TestCase  
from django.urls import reverse  
  
  
class SignupPageTest(TestCase):  
    def test_url_exists_at_correct_location_signupview(self):     # просто проверяем расположение
        response = self.client.get("/accounts/signup/")  
        self.assertEqual(response.status_code, 200)  
  
    def test_signup_view_name(self):                              
        response = self.client.get(reverse("signup"))             
		self.assertEqual(response.status_code, 200)               # проверяем по имени
        self.assertTemplateUsed(response, "registration/signup.html")  # проверяем как связан запрос и 
        #                                                              # шаблон который вызывается
  
    def test_signup_form(self):  
        response = self.client.post(  
            reverse("signup"),  
            {                "username": "testuser",  
                "email": "testuser@email.com",  
                "password1": "testpass123",                     # создаем пользователя
                'age': 15,  
                "password2": "testpass123",  
            },        )  
        self.assertEqual(response.status_code, 302)             # проверяем получилось или нет
        self.assertEqual(get_user_model().objects.all().count(), 1)  # проверяем что создан всего один пользователь
        
        # get_user_model().objects.all() -> это какой-то итерируемый контеинер где хранятся новые созданные
        #                                   пользователи, внутри него объект у которого есть атрибуты, с 
	    #                                   характеристиками пользователя
	    
        self.assertEqual(get_user_model().objects.all()[0].age, 15)  
        self.assertEqual(get_user_model().objects.all()[0].username, "testuser")    # проверяем все его свойства
        self.assertEqual(get_user_model().objects.all()[0].email, "testuser@email.com")
```
