from django.db import models
from datetime import datetime, timedelta, date
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User

class skilltag(models.Model):
    skilltagname = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True, null=True)
    image = models.ImageField(upload_to='listingpics', default="listingpics/notavailable.png")

    class Meta:
        verbose_name = ("Skill Tag")


    def __str__(self):
        return f'{self.skilltagname}'
    
class Listing_abstract(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings_created', default=None)
    nameofservice = models.CharField(max_length=255, null=True,
                                     help_text="Please state directly the service you will provide EG. I will help/create/do...")
    image = models.ImageField(upload_to='listingpics', default="listingpics/notavailable.png")
    details = models.TextField(null=True)
    relatedskilltag = models.ManyToManyField(skilltag, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)


class ServiceListing(Listing_abstract):
    hourlyCharge = models.DecimalField(max_digits=10, decimal_places=2)
    skill = models.CharField(null=True, max_length=128)

    class Meta:
        verbose_name = ("Service Listing")

    def __str__(self):
        return f'{self.nameofservice} | {self.student_user}'


class SkillSwapListing(Listing_abstract):
    skill_offered = models.CharField(null=True, max_length=128)
    optional_skill_wanted = models.CharField(null=True, max_length=128)

    class Meta:
        verbose_name = ("Skill Swap Listing")


    def __str__(self):
        return f'{self.nameofservice}'


class ServiceListingPurchase(models.Model):
    STATUS_CHOICES = (
        ('Completed', 'Completed'),
        ('In Progress', 'In Progress'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases_made')
    service_listing = models.ForeignKey(ServiceListing, on_delete=models.CASCADE, related_name='purchases')
    message = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='In Progress')

    class Meta:
        verbose_name = "Service Listing Purchase"

    def __str__(self):
        return f'Purchase of {self.service_listing.nameofservice} by {self.client_user.username} ({self.status})'
    
class SkillSwapOffer(models.Model):
    STATUS_CHOICES = (
        ('Offered', 'Offered'),
        ('Rejected', 'Rejected'),
        ('Accepted', 'Accepted')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offer_made')
    skillswap_listing = models.ForeignKey(SkillSwapListing, on_delete=models.CASCADE, related_name='offers')
    skill_offered = models.CharField(null=True, max_length=128)
    message = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Offered')

    class Meta:
        verbose_name = "Skill Swap Offer"

    def __str__(self):
        return f'SkillSwap Offer of {self.skillswap_listing.nameofservice} by {self.client_user.username} ({self.status})'

class Reviews(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('Service', 'Service Listing'),
        ('SkillSwap', 'Skill Swap Listing'),
    ]

    service_type = models.CharField(max_length=10, choices=SERVICE_TYPE_CHOICES, null=True)
    service_listing = models.ForeignKey(ServiceListing, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    skillswap_listing = models.ForeignKey(SkillSwapListing, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_made', default=None)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        verbose_name = "Review"

    def __str__(self):
        if self.service_type == 'Service':
            return f"Review for Service Listing: {self.service_listing.nameofservice}"
        elif self.service_type == 'SkillSwap':
            return f"Review for Skill Swap Listing: {self.skillswap_listing.nameofservice}"
        else:
            return "Invalid review"
        

class Notification(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_notifications')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.recipient}: {self.message}"




