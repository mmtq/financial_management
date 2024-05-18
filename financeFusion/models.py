from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    profile_picture = models.ImageField(blank=True, upload_to='profile_pictures')
    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True) 

    def __str__(self):
        return self.name

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    date = models.DateField()
    description = models.CharField(max_length=255, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    TYPE_CHOICES = (
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    )
    transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='EXPENSE')

    def __str__(self):
        return f"{self.user.username}: {self.category} ({self.transaction_type}) - ${self.amount}"

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True) 
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True) 
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} Budget - {self.amount} ({self.start_date} - {self.end_date if self.end_date else 'Ongoing'})"

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True) 
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    due_date = models.DateField()
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name} Goal - Target: ${self.target_amount} (Due: {self.due_date}) - Current: ${self.current_amount}"
