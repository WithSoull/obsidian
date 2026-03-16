
Атака, когда пользователь заполняет формы на сайте, логинится например, в этот момент хакер выполняет разные действия от лица этого пользователя

# Как исправить? (На примере [[90 - Archive/Django/Плюсы и минусы Django|Django]], в ее ОRM)

https://docs.djangoproject.com/en/4.0/ref/csrf/

```html
<!-- templates/post_new.html -->

{% extends "base.html" %}

{% block content %}
<h1>New post</h1>
	<form action="" method="post">{% csrf_token %}
		{{ form.as_p }}
		<input type="submit" value="Save">
	</form>
{% endblock content %}
```
