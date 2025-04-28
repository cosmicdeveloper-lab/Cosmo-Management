from django.db import models


class Branch(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    crowd_level = models.FloatField(default=0.0)  # 0 to 1 scale

    def __str__(self):
        return self.name


class Employee(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('seller', 'Seller'),
    ]
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    current_branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='employees')

    def __str__(self):
        return f"{self.name} ({self.role})"


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    season = models.CharField(max_length=50)
    fashion_tag = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, null=True, blank=True, on_delete=models.CASCADE)
    is_online_warehouse = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} @ {self.branch.name if self.branch else 'Online'}"


class Sale(models.Model):
    SALE_TYPE = [
        ('online', 'Online'),
        ('offline', 'Offline')
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, null=True, blank=True, on_delete=models.SET_NULL)
    sale_type = models.CharField(max_length=10, choices=SALE_TYPE)
    quantity = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} ({self.sale_type})"


class Event(models.Model):
    name = models.CharField(max_length=100)
    event_type = models.CharField(max_length=50)  # e.g., holiday, sale, fashion
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name


class WebsiteView(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    views = models.PositiveIntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.views} views for {self.product.name} on {self.date}"
