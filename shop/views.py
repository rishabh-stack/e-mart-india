from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from math import ceil
from .models import Product,Contact,Order,OrderUpdate
from django.contrib.auth import authenticate,login,logout
import json

# Create your views here.

def index(request):
    # products=Product.objects.all()
    # print(products)
    # params={"no_of_slides":ns,'range':range(1,ns),"product":products}
    # allprods=[[products,range(1,n),ns],
    #      [products,range(1,ns),ns]]
    allprods=[]
    catprods=Product.objects.values("category","id")
    cats={item["category"] for item in catprods}
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        n=len(prod)
        ns=n//4 + ceil((n/4)-(n//4))
        allprods.append([prod,range(1,ns),ns])

    params={"allprods":allprods}
    return render(request,"shop/index.html",params)
def searchMatch(query,item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query=request.GET.get('search')
    allprods=[]
    message=''
    catprods=Product.objects.values("category","id")
    cats={item["category"] for item in catprods}
    for cat in cats:
        prodtemp=Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query,item)]
        n=len(prod)
        ns=n//4 + ceil((n/4)-(n//4))
        if len(prod)==0:
            message="result not found"
        if len(prod)!=0:
            allprods.append([prod,range(1,ns),ns])
            message="result found"
    params={"allprods":allprods,"message":message}
    return render(request,"search.html",params)
def about(request):
    return render(request,"shop/about.html")

def contact(request):
    thanks=False
    if request.method=="POST":
        name=request.POST.get("name","")
        email=request.POST.get("email","")
        phone=request.POST.get("phone","")
        desc=request.POST.get("desc","")
        contact=Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        thanks=True
    return render(request,"shop/contact.html", {'thanks':thanks})
def checkout(request):
    if  request.method=="POST":
        items_json=request.POST.get("itemsJson","")
        name=request.POST.get("name","")
        email=request.POST.get("email","")
        phone=request.POST.get("phone","")
        address=request.POST.get("address","")
        city=request.POST.get("city","")
        state=request.POST.get("state","")
        zip_code=request.POST.get("zip_code","")
        order=Order(items_json=items_json,name=name,email=email,phone=phone,address=address,city=city,state=state,zip_code=zip_code)
        order.save()
        update=OrderUpdate(order_id=order.order_id,update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
    return render(request,"shop/checkout.html")
    
def prodview(request,myid):
    product=Product.objects.filter(id=myid)
    print(product)
    dic={"product":product[0]}
    return render(request,"shop/prodview.html",dic)

def privacy(request):
    return render(request,"shop/privacy.html")

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email25 = request.POST.get('email25', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email25)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse(f'{e}')

    return render(request, 'shop/tracker.html')

def handlesignUp(request):
    if request.method == 'POST':
        username=request.POST['username']
        first=request.POST['first']
        last=request.POST['last']
        email=request.POST['email']
        password=request.POST['pass1']

        myuser=User.objects.create_user(username,email,password)
        myuser.first_name=first
        myuser.last_name=last
        myuser.save()
        messages.success(request,f" {first} -- Your E-mart account has been successfully created")
        return redirect('/')
        


    else:
        return render(request, 'shop/404.html')

def handlelogin(request):
    if request.method == 'POST':
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']
        user=authenticate(username=loginusername,passsword=loginpassword)
        if user is not None:
            login(request,user)
            messages.success(request," successfully logged in")
            return redirect('/')
        else:
            messages.error(request,"Sorry invalid credentials please try again")
            return redirect('/')
    return HttpResponse('handle loginin')


def handlelogout(request):
    return HttpResponse("logout")
