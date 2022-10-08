from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from .models import Adverts
from .forms import CreateUserForm, AdPostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import geocoder
import folium




# Rendering signup page

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, 'Account created successfully for ' + username)
                return redirect('login')
    context = {'form': form}
    return render(request, 'signup.html', context)

# Rendering login page

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Incorrect username or password')
    return render(request, 'login.html')

# Handling logout
def logoutuser(request):
    logout(request)
    return redirect('home')

def about(request):
    return render(request, 'about.html')

def profile(request):
    return render(request, 'profile.html')

def bookmarks(request):
    return render(request, 'bookmarks.html')

# Rendering landing/home page
def home(request):
    return render(request, 'home.html')

# library for converting placholder currency texts to integers
unit = {
    "million": 1000000,
    "lakh": 100000,
    "lac": 100000,
    "thousand": 1000,
    "crore": 10000000,
    "koti": 10000000
}

# library for converting placholder room number texts to integers
count = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5
}

area = ['Agargaon', 'Hazaribag', 'Khilgaon', 'Eskaton', 'Uttara', 'North Shahjahanpur', 'Shegunbagicha', 'Badda', 'Banani', 'Mirpur', 'Maniknagar', 'Bashundhara', 'Mohammadpur', 'Maghbazar', 'Motijheel', 'Kalachandpur', 'Malibagh', 'Savar', 'Lalmatia', 'Sutrapur', 'Keraniganj', 'Dhanmondi', 'Shiddheswari', 'Kalabagan', 'Shyamoli', 'Baridhara', 'Shahjahanpur', 'Banasree', 'Rampura', 'Demra', 'Gulshan', 'Kotwali', 'Shyampur', 'Kathalbagan', 'Adabor', 'Tejgaon', 'Cantonment', 'Bashabo', 'Lalbagh', 'Bangshal', 'Shantinagar', 'Niketan', 'Hatirpool', 'Mugdapara', 'Kuril', 'Ibrahimpur', 'Kafrul', 'Nikunja']


def search(request):
    try: 
        output = request.POST.get('output')
        command = output.split()
        # Checking if voice command is for exact amount or below the amount
        try:
            for i in range(len(command)):
                if command[i] == 'under':
                    budget_finder = output.split("under")
                    limit_check = command[i]
                elif command[i] == 'exactly':
                    budget_finder = output.split("for exactly")
                    limit_check = 'for exactly'
            if 'budget_finder' in locals():
                for j in range(len(command)):
                    if command[j] == 'taka' or command[j] == 'Taka':
                        if command[j] == 'taka':
                            s1 = budget_finder[1].split('taka')
                            s2 = s1[0].split()
                        elif command[j] == 'Taka':
                            s1 = budget_finder[1].split('Taka')
                            s2 = s1[0].split()
            if 's2' in locals():
                try:
                    budget = int(s2[0]) * unit[s2[1]]
                except:
                    budget = int(s2[0])
            taka_limit = None
            if 'budget' in locals():
                taka_limit = int(budget)
            # Checking for listing category
            category = None
            for j1 in range(len(command)):
                if command[j1] == 'rent' or command[j1] == 'Rent':
                    category = 'RENT'
                elif command[j1] == 'sale' or command[j1] == 'Sale':
                    category = 'SALE'
            # Voice checking for bedroom parameters
            bed_limit = None
            for bed in range(len(command)):
                if command[bed] == 'bed' or command[bed] == 'beds' or command[bed] == 'bedroom' or command[bed] == 'bedrooms':
                    try:
                        bed_limit = int(command[bed - 1])
                    except:
                     bed_limit = count[command[bed - 1]]
            # Checking if command has an area as a parameter
            apartment_area = None
            for a in range(len(command)):
                for b in range(len(area)):
                    if command[a].title() == area[b].title():
                        apartment_area = command[a].title()
            # Checking is budget is under or exactly the amount given & filtering out for each parameter given or not scenario
            if limit_check == 'under':
                if taka_limit is not None and category is not None and bed_limit is not None and apartment_area is not None:
                    products = Adverts.objects.filter(price__lt=taka_limit, listing_category=category, bed_rooms=bed_limit, Address=apartment_area).order_by('price')
                elif taka_limit is not None and category is not None and bed_limit is not None and apartment_area is None:
                    products = Adverts.objects.filter(price__lt=taka_limit, listing_category=category, bed_rooms=bed_limit).order_by('price')
                elif taka_limit is not None and category is not None and bed_limit is None and apartment_area is not None:
                    products = Adverts.objects.filter(price__lt=taka_limit, listing_category=category, Address=apartment_area).order_by('price')
                elif taka_limit is not None and category is None and bed_limit is not None and apartment_area is not None:
                    products = Adverts.objects.filter(price__lt=taka_limit, bed_rooms=bed_limit, Address=apartment_area).order_by('price')
                elif taka_limit is not None and category is not None and bed_limit is None and apartment_area is None:
                    products = Adverts.objects.filter(price__lt=taka_limit, listing_category=category).order_by('price')
                elif taka_limit is not None and category is None and bed_limit is None and apartment_area is not None:
                    products = Adverts.objects.filter(price__lt=taka_limit, Address=apartment_area).order_by('price')
                elif taka_limit is not None and category is None and bed_limit is not None and apartment_area is None:
                    products = Adverts.objects.filter(price__lt=taka_limit, bed_rooms=bed_limit).order_by('price')
                elif taka_limit is not None and category is None and bed_limit is None and apartment_area is None:
                    products = Adverts.objects.filter(price__lt=taka_limit).order_by('price')
            elif limit_check == 'for exactly':
                if taka_limit is not None and category is not None and bed_limit is not None and apartment_area is not None:
                    products = Adverts.objects.filter(price=taka_limit, listing_category=category,
                                                  bed_rooms=bed_limit, Address=apartment_area).order_by('price')
                elif taka_limit is not None and category is not None and bed_limit is not None and apartment_area is None:
                    products = Adverts.objects.filter(price=taka_limit, listing_category=category, bed_rooms=bed_limit).order_by('price')
                elif taka_limit is not None and category is not None and bed_limit is None and apartment_area is not None:
                    products = Adverts.objects.filter(price=taka_limit, listing_category=category, Address=apartment_area).order_by('price')
                elif taka_limit is not None and category is None and bed_limit is not None and apartment_area is not None:
                    products = Adverts.objects.filter(price=taka_limit, bed_rooms=bed_limit, Address=apartment_area).order_by('price')
                elif taka_limit is not None and category is not None and bed_limit is None and apartment_area is None:
                    products = Adverts.objects.filter(price=taka_limit, listing_category=category).order_by('price')
                elif taka_limit is not None and category is None and bed_limit is None and apartment_area is not None:
                    products = Adverts.objects.filter(price=taka_limit, Address=apartment_area).order_by('price')
                elif taka_limit is not None and category is None and bed_limit is not None and apartment_area is None:
                    products = Adverts.objects.filter(price=taka_limit, bed_rooms=bed_limit).order_by('price')
                elif taka_limit is not None and category is None and bed_limit is None and apartment_area is None:
                    products = Adverts.objects.filter(price=taka_limit).order_by('price')

        except:
            if taka_limit is None and category is not None and bed_limit is not None and apartment_area is not None:
                products = Adverts.objects.filter(listing_category=category, bed_rooms=bed_limit, Address=apartment_area).order_by('price')
            elif taka_limit is None and category is not None and bed_limit is not None and apartment_area is None:
                products = Adverts.objects.filter(listing_category=category, bed_rooms=bed_limit).order_by('price')
            elif taka_limit is None and category is not None and bed_limit is None and apartment_area is not None:
                products = Adverts.objects.filter(listing_category=category, Address=apartment_area).order_by('price')
            elif taka_limit is None and category is None and bed_limit is not None and apartment_area is not None:
                products = Adverts.objects.filter(bed_rooms=bed_limit, Address=apartment_area).order_by('price')
            elif taka_limit is None and category is not None and bed_limit is None and apartment_area is None:
                products = Adverts.objects.filter(listing_category=category).order_by('price')
            elif taka_limit is None and category is None and bed_limit is None and apartment_area is not None:
                products = Adverts.objects.filter(Address=apartment_area).order_by('price')
            elif taka_limit is None and category is None and bed_limit is not None and apartment_area is None:
                products = Adverts.objects.filter(bed_rooms=bed_limit).order_by('price')

        if request.user.is_authenticated:
            user_bookmarks = Adverts.objects.filter(bookmarked__username = request.user.username).values_list('price', flat=True)
            context = {
            'products': products,
            'fav': user_bookmarks,
        } 
        else:
            context = {
            # 'page_obj': page_obj,
            'products': products
        }
    
        return render(request, 'search.html', context)
        
    except:
        return redirect('error')
    

# This page needs users to be authenticated
@login_required(login_url='login')
def postadvert(request):
    form = AdPostForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        messages.success(request, 'Your AD has been posted successfully!😃')
        return redirect('home')
    context = {'form': form}
    return render(request, 'postad.html', context)



# Rendering maps with folium 
def mapview(request):
    # taking users latitude and longitude (Not sure if this pings the users machine or the server)
    g = geocoder.ip('me')
    lat = g.lat
    long = g.lng
    latitude = lat + 0.041
    longitude = long + 0.041
    # filtering out the apartments only for 8KM radius around the user
    apartments_in_area = Adverts.objects.filter(lat__gt=lat, lat__lte=latitude, longi__gt=long, longi__lte=longitude).distinct()
    m = folium.Map([lat, long], zoom_start=14)
    # placing a marker in map for every apartment within range from the user
    for apartment in apartments_in_area:
        info = "<b>Title: </b>" + apartment.Ad_Title + "<br><b>Price: </b>" + str(apartment.price) + "  Taka" + "<br><b>BedRooms: </b>" + apartment.bed_rooms + "<br><b>Area: </b>" + apartment.sq_ft + "<br><b>Link: <a href="+apartment.property_url+">Click Here</a>"
        icon_url = "https://pngbas.com/images/bt/cartoon-houses-clipart-5.png"
        house_icon = folium.features.CustomIcon(icon_url, icon_size=(28, 28))
        popup = folium.Popup(info, max_width=2650)
        folium.Marker(
            location=[apartment.lat, apartment.longi],
            popup=popup,
            icon=house_icon
            ).add_to(m)

    m = m._repr_html_()
    context = {'my_map': m}

    return render(request, 'mapview.html', context)
    



@login_required 
def add_bookmark(request, id): 
    item = get_object_or_404(Adverts, id=id)
    if item.bookmarked.filter(id=request.user.id).exists():
        item.bookmarked.remove(request.user) 
    else:
        item.bookmarked.add(request.user) 
    
    return HttpResponseRedirect(reverse(bookmarks))
    



@login_required 
def bookmarks(request):
    bookmarks = Adverts.objects.filter(bookmarked=request.user) 
    context = {
        'bookmarks': bookmarks,
    }
    
    return render(request,'bookmarks.html', context) 



def handler404(request):
    return render(request, '404.html') 




