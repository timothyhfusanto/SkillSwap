from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Count, F, Avg
from django.db.models.functions import Round

# Create your views here.

@login_required
def edit_profile(request):
    return HttpResponse("edit profile")

@login_required
def create_service_listing(request):
    if request.method == 'POST':
        form = ServiceListingForm(request.POST, request.FILES)
        if form.is_valid():
                
            service_listing = form.save(commit=False)
            service_listing.student_user = request.user
           
            service_listing.save()
            for skill_tag in form.cleaned_data['relatedskilltag']:
                service_listing.relatedskilltag.add(skill_tag)
            return redirect('service_listing')
        else:
            print(form.errors)
    else:
        form = ServiceListingForm()
    return render(request, 'create_listing.html', {'form': form})

@login_required
def edit_service(request, listing_id):
    service_listing = get_object_or_404(ServiceListing, id=listing_id)
    if request.method == 'POST':
        form = EditServiceForm(request.POST, request.FILES, instance=service_listing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service edited successfully.')
            return redirect("manage_listing")
    else:
        form = EditServiceForm(instance=service_listing)
    return render(request, 'edit_service.html', {'form': form, "service_listing":service_listing})

@login_required
def edit_skillswap(request, listing_id):
    skillswap_listing = get_object_or_404(SkillSwapListing, id=listing_id)
    if request.method == 'POST':
        form = EditSkillSwapForm(request.POST, request.FILES, instance=skillswap_listing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skillswap edited successfully.')
            return redirect("manage_listing")
    else:
        form = EditSkillSwapForm(instance=skillswap_listing)
    return render(request, 'edit_skillswap.html', {'form': form, "skillswap_listing":skillswap_listing})

def view_service_listings(request):
    service_listings = ServiceListing.objects.all()
    if request.method == 'GET' and 'skill_tag' in request.GET:
        skill_tag_id = request.GET.get('skill_tag')
        if(skill_tag_id == 'all'):
            service_listings = ServiceListing.objects.all()
        else:
            service_listings = ServiceListing.objects.filter(relatedskilltag=skill_tag_id)
    else:
        service_listings = ServiceListing.objects.all()
    
    skill_tags = skilltag.objects.all()
    review_count = []
    average_tag = []
    
    for service in service_listings:
        serviceid = service.id
        reviews = Reviews.objects.filter(service_listing=service)
        count = reviews.count()
        review_count.append((serviceid, count))
        sum = 0.0

        for r in reviews:
            sum += r.rating
        
        if count != 0:
            average_rating = round(sum / count, 1)
        else:
            average_rating = 0
            
        average_tag.append((serviceid, average_rating))
        
    context = {
        "service_listings": service_listings,
        "review_count" : review_count,
        "average_tag" : average_tag,
        "skill_tags": skill_tags
    }
    
    return render(request, 'service_listing.html', context)

@login_required
def edit_service_listing(request, listing_id):
    service_listing = get_object_or_404(ServiceListing, id=listing_id)
    if request.method == 'POST':
        form = ServiceListingForm(request.POST, request.FILES, instance=service_listing)
        if form.is_valid():
            form.save()
            return redirect('view_service_listings')
    else:
        form = ServiceListingForm(instance=service_listing)
    return render(request, 'edit_service_listing.html', {'form': form})

@login_required
def delete_service_listing(request, listing_id):
    service_listing = get_object_or_404(ServiceListing, id=listing_id)
    if request.method == 'POST':
        service_listing.delete()
        return redirect('view_service_listings')
    return render(request, 'delete_service_listing.html', {'service_listing.html': service_listing})

@login_required
def view_service_detail(request, listing_id):
    listing = get_object_or_404(ServiceListing, id=listing_id)
    reviews = Reviews.objects.filter(service_listing=listing).order_by("-date")
    has_reviewed = Reviews.objects.filter(service_listing=listing, creator=request.user).first()
    
    sum = 0.0
    for r in reviews:
        sum += r.rating

    if reviews.count() != 0:
        average_rating = round(sum / reviews.count(), 1)
    else:
        average_rating = 0
    
    purchases = ServiceListingPurchase.objects.filter(service_listing=listing)
    has_purchased = purchases.filter(client_user=request.user, status="Completed").exists() if request.user.is_authenticated else False
    service_type = 'Service'

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.creator = request.user
            review.service_type = service_type
            reviews.rating = int(request.POST.get('rating'))
            if service_type == 'Service':
                review.service_listing = listing
            review.save()
            listing_id = listing.id  

            if service_type == 'Service':
                messages.success(request, "Your review has been added")
                return redirect(reverse('service_detail', kwargs={'listing_id': listing_id}))

        else:
            print(form.errors)

    else:
        form = ReviewForm()
        
    context = {
        "listing":listing,
        "reviews":reviews,
        "purchases":purchases,
        "has_purchased":has_purchased,
        "has_reviewed":has_reviewed,
        "form" : form,
        "average_rating":average_rating
    }
    return render(request, 'service_detail.html',  context)

@login_required
def delete_review_service(request, listing_id, review_id):
    review = get_object_or_404(Reviews, id=review_id)
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, "Review has been deleted")
        return redirect(reverse('service_detail', kwargs={'listing_id':listing_id}))
    return render(request, 'service_detail.html', {'service_listing.html': service_listing})

@login_required
def delete_review_skillswap(request, listing_id, review_id):
    review = get_object_or_404(Reviews, id=review_id)
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, "Review has been deleted")
        return redirect(reverse('skillswap_detail', kwargs={'listing_id':listing_id}))
    return render(request, 'skillswap_detail.html', {'skillswap_listing.html': skillswap_listing})

@login_required
def purchase_listing(request, listing_id):
    listing = get_object_or_404(ServiceListing, id=listing_id)
    form = ServiceListingPurchaseForm()

    if request.method == 'POST':
        form = ServiceListingPurchaseForm(request.POST)
        if form.is_valid():
            # Create a ServiceListingPurchase object
            purchase = form.save(commit=False)
            purchase.client_user = request.user
            purchase.service_listing = listing
            purchase.save()
            return redirect('thank_you')  # Redirect to thank you page or wherever you want

    return render(request, 'purchase_listing.html', {'listing': listing, 'form': form})

@login_required
def change_status(request):
    if request.method == 'POST' and request.is_ajax():
        job_id = request.POST.get('job_id')
        new_status = request.POST.get('new_status')

        try:
            job = ServiceListingPurchase.objects.get(id=job_id)
            job.status = new_status
            job.save()
            return JsonResponse({'success': True})
        except ServiceListingPurchase.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Job does not exist'}, status=404)

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@login_required
def offer_skillswap(request, listing_id):
    listing = get_object_or_404(SkillSwapListing, id=listing_id)
    form = SkillSwapOfferForm()

    if request.method == 'POST':
        form = SkillSwapOfferForm(request.POST)
        if form.is_valid():
            # Create a ServiceListingPurchase object
            offer = form.save(commit=False)
            offer.client_user = request.user
            offer.skillswap_listing = listing
            offer.save()
            return redirect('thank_you_skillswap')  # Redirect to thank you page or wherever you want

    return render(request, 'offer_skillswap.html', {'listing': listing, 'form': form})

@login_required
def create_review(request, listing_id):
    if ServiceListing.objects.filter(id=listing_id).exists():
        listing = get_object_or_404(ServiceListing, id=listing_id)
        service_type = 'Service'
    elif SkillSwapListing.objects.filter(id=listing_id).exists():
        listing = get_object_or_404(SkillSwapListing, id=listing_id)
        service_type = 'SkillSwap'
    else:
        return redirect('home')  

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.creator = request.user
            review.service_type = service_type
            if service_type == 'Service':
                review.service_listing = listing
            elif service_type == 'SkillSwap':
                review.skillswap_listing = listing
            review.save()
            listing_id = listing.id  

            return JsonResponse({'success':True})

        else:
            print(form.errors)
    else:
        form = ReviewForm()
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@login_required
def create_skill_swap_listing(request):
    if request.method == 'POST':
        form = SkillSwapListingForm(request.POST, request.FILES)
        if form.is_valid():
            new_skill_name_offered = form.cleaned_data['new_skill_name']
            new_skill_name_wanted = form.cleaned_data['new_skill_name_wanted']

            if new_skill_name_offered:
                new_skill_offered = Skill.objects.create(name=new_skill_name_offered)
                form.instance.skill_offered = new_skill_offered

            if new_skill_name_wanted:
                new_skill_wanted = Skill.objects.create(name=new_skill_name_wanted)
                form.instance.optional_skill_wanted = new_skill_wanted

            form.instance.student_user = request.user

            form.save()
            return redirect('skillswap_listing')
        else:
            print(form.errors)
    else:
        form = SkillSwapListingForm()
    return render(request, 'create_skillswap.html', {'form': form})

def view_skill_swap_listings(request):
    skill_swap_listings = SkillSwapListing.objects.all()
    review_count = []
    average_tag = []
    
    for service in skill_swap_listings:
        serviceid = service.id
        reviews = Reviews.objects.filter(skillswap_listing=service)
        count = reviews.count()
        review_count.append((serviceid, count))
        sum = 0.0

        for r in reviews:
            sum += r.rating
        
        if count != 0:
            average_rating = round(sum / count, 1)
        else:
            average_rating = 0
            
        average_tag.append((serviceid, average_rating))
        
    context = {
        'skill_swap_listings': skill_swap_listings,
        'review_count' : review_count,
        'average_tag' : average_tag
    }
    return render(request, 'skillswap_listing.html', context)

@login_required
def edit_skill_swap_listing(request, listing_id):
    skill_swap_listing = get_object_or_404(SkillSwapListing, id=listing_id)
    if request.method == 'POST':
        form = SkillSwapListingForm(request.POST, request.FILES, instance=skill_swap_listing)
        if form.is_valid():
            form.save()
            return redirect('view_skill_swap_listings')
    else:
        form = SkillSwapListingForm(instance=skill_swap_listing)
    return render(request, 'coreapp/edit_skill_swap_listing.html', {'form': form})

@login_required
def delete_skill_swap_listing(request, listing_id):
    skill_swap_listing = get_object_or_404(SkillSwapListing, id=listing_id)
    if request.method == 'POST':
        skill_swap_listing.delete()
        return redirect('view_skill_swap_listings')
    return render(request, 'coreapp/delete_skill_swap_listing.html', {'skill_swap_listing': skill_swap_listing})

@login_required
def view_skillswap_detail(request, listing_id):
    listing = get_object_or_404(SkillSwapListing, id=listing_id)
    reviews = Reviews.objects.filter(skillswap_listing=listing).order_by("-date")
    has_reviewed = Reviews.objects.filter(skillswap_listing=listing, creator=request.user).first()
    sum = 0.0
    for r in reviews:
        sum += r.rating

    if reviews.count() != 0:
        average_rating = round(sum / reviews.count(), 1)
    else:
        average_rating = 0
    offers = SkillSwapOffer.objects.filter(skillswap_listing=listing)
    has_offered = offers.filter(client_user=request.user, status="Accepted").exists() if request.user.is_authenticated else False
    
    service_type = 'SkillSwap'

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.creator = request.user
            review.service_type = service_type
            reviews.rating = int(request.POST.get('rating'))
            if service_type == 'SkillSwap':
                review.skillswap_listing = listing
            review.save()
            listing_id = listing.id  

            if service_type == 'SkillSwap':
                messages.success(request, "Your review has been added")
                return redirect(reverse('skillswap_detail', kwargs={'listing_id': listing_id}))

        else:
            print(form.errors)

    else:
        form = ReviewForm()
        
    context = {
        "listing":listing,
        "reviews":reviews,
        "offers":offers,
        "has_offered": has_offered,
        "has_reviewed":has_reviewed,
        "form" : form,
        "average_rating":average_rating
    }
    return render(request, 'skillswap_detail.html',  context)

def user_dashboard(request):
    # Fetch notifications for the current user
    notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'user_dashboard.html', {'notifications': notifications})


def home(request):
    categories = skilltag.objects.all().order_by('-created')[:10]
    services = ServiceListing.objects.all().order_by('created')[:10]
    print(categories)
    review_count = []
    average_tag = []
    user_ratings = Reviews.objects.values('service_listing__student_user').annotate(
        rating_count = Count('service_listing__student_user')).annotate(
        student_user_name=F('service_listing__student_user__name')).annotate(
        average = Round(Avg('rating'),1)).annotate(
        image_student = F('service_listing__student_user__image')).order_by('-rating_count')[:5]
    
    print(user_ratings)
    for service in services:
        serviceid = service.id
        reviews = Reviews.objects.filter(service_listing=service)
        count = reviews.count()
        review_count.append((serviceid, count))
        sum = 0.0

        for r in reviews:
            sum += r.rating
        
        if count != 0:
            average_rating = round(sum / count, 1)
        else:
            average_rating = 0
            
        average_tag.append((serviceid, average_rating))
    
    tag_count = []
    for category in categories:
        category_name = category.skilltagname
        count = ServiceListing.objects.filter(relatedskilltag=category).count()
        tag_count.append((category_name, count))
        
    context = {
        'categories' : categories,
        "tag_count" : tag_count,
        "services" : services,
        "review_count" : review_count,
        "average_tag" : average_tag,
        "user_ratings" : user_ratings
    }

    return render(request, 'index.html', context)

def signin(request):
    return render(request, 'signin.html')

def signup(request):
    return render(request, 'signup.html')

@login_required
def dashboard(request):
    user_purchases = ServiceListingPurchase.objects.filter(client_user=request.user).count() + SkillSwapOffer.objects.filter(client_user=request.user).count()
    user_jobs_active = ServiceListingPurchase.objects.filter(service_listing__student_user=request.user, status="In Progress").count() + SkillSwapOffer.objects.filter(skillswap_listing__student_user=request.user, status="Offered").count()
    user_jobs_done = ServiceListingPurchase.objects.filter(service_listing__student_user=request.user, status="Completed").count() + SkillSwapOffer.objects.filter(skillswap_listing__student_user=request.user, status="Accepted").count()
    user_jobs = ServiceListingPurchase.objects.filter(service_listing__student_user=request.user)

    context = {
        "jobs_active" : user_jobs_active,
        "user_purchases" : user_purchases,
        "jobs_done" : user_jobs_done,
        "user_jobs" : user_jobs
    }
    return render(request, 'dashboard.html', context)

@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')  # Redirect to the profile page after saving
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'profile.html', {'form': form, 'user': user})

@login_required
def manage_listing(request):
    # Retrieve user's skill swap listings and service listings
    skill_swap_listings = SkillSwapListing.objects.filter(student_user=request.user)
    service_listings = ServiceListing.objects.filter(student_user=request.user)

    context = {
        'skill_swap_listings': skill_swap_listings,
        'service_listings': service_listings
    }
    return render(request, 'manage_listing.html', context)

@login_required
def change_password(request):
    return render(request, 'change_password.html')

@login_required
def view_my_order(request):
    user_purchases = ServiceListingPurchase.objects.filter(client_user=request.user)
    user_skillswap_offer = SkillSwapOffer.objects.filter(client_user=request.user)

    return render(request, 'my_order.html', {'user_purchases': user_purchases, 'user_skillswap_offer': user_skillswap_offer})

@login_required
def view_my_job(request):
    user_jobs = ServiceListingPurchase.objects.filter(service_listing__student_user=request.user)
    user_skillswap = SkillSwapOffer.objects.filter(skillswap_listing__student_user=request.user)
    return render(request, 'my_job.html', {'user_jobs': user_jobs, 'user_skillswap': user_skillswap})

def about_us(request):
    return render(request, 'about.html')


def view_freelancer(request, user_id):
    freelancer = get_object_or_404(User, pk=user_id)
    listings_owned = ServiceListing.objects.filter(student_user=user_id)
    skillswap_owned = SkillSwapListing.objects.filter(student_user=user_id)
        
    service_review = Reviews.objects.filter(service_listing__student_user=freelancer)
    skillswap_review = Reviews.objects.filter(skillswap_listing__student_user=freelancer)
    
    service_review_count = service_review.count()
    skillswap_review_count = skillswap_review.count()
    review_count = service_review_count + skillswap_review_count
    
    service_sum = 0.0
    skillswap_sum = 0.0
    
    for r in service_review:
        service_sum += r.rating
    
    for r in skillswap_review:
        skillswap_sum += r.rating
        
    all_sum = skillswap_sum + service_sum
    average_rating = 0.0
    
    if review_count != 0:
        average_rating = round(all_sum / review_count,1)
    else:
        average_rating = 0

    context = {
        "freelancer" : freelancer,
        "listings_owned" : listings_owned,
        "skillswap_owned" : skillswap_owned,
        "review_count" : review_count,
        "average_rating" : average_rating
    }
    return render(request, 'freelancer_details.html', context)

def thank_you(request):
    return render(request, 'thankyou.html')

def thank_you_skillswap(request):
    return render(request, 'thankyou_skillswap.html')

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@login_required
def change_status(request):
    if request.method == 'POST' and is_ajax(request):
        job_id = request.POST.get('job_id')
        new_status = request.POST.get('new_status')
        if ServiceListingPurchase.objects.filter(id=job_id).exists():
            job = ServiceListingPurchase.objects.get(id=job_id)
        elif SkillSwapOffer.objects.filter(id=job_id).exists():
            job = SkillSwapOffer.objects.get(id=job_id)
        else:
            # Handle the case where no listing with the given ID exists
            return redirect('home')

        try:
            job.status = new_status
            job.save()
            return JsonResponse({'success': True})
        except ServiceListingPurchase.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Job does not exist'}, status=404)

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@login_required
def delete_listing(request, listing_id):
    if ServiceListing.objects.filter(id=listing_id).exists():
        listing = get_object_or_404(ServiceListing, id=listing_id)
    elif SkillSwapListing.objects.filter(id=listing_id).exists():
        listing = get_object_or_404(SkillSwapListing, id=listing_id)
    else:
        # Handle the case where no listing with the given ID exists
        return redirect('home')

    if request.method == 'POST':
        # Check if the current user is the owner of the service listing
        if request.user == listing.student_user:
            # Delete the service listing
            listing.delete()
            messages.success(request, 'Service listing deleted successfully.')
            return redirect('home')  # Redirect to desired URL after deletion
        else:
            messages.error(request, 'You are not authorized to delete this service listing.')
            return redirect('service_detail', listing_id=listing_id)  # Redirect to the service detail page
    else:
        return render(request, 'confirm_delete.html', {'listing': listing})