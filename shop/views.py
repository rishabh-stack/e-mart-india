from django.shortcuts import render
from django.http import HttpResponse
from math import ceil
from .models import Product,Contact,Order,OrderUpdate
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
    catprods=Product.objects.values("category","id")
    cats={item["category"] for item in catprods}
    for cat in cats:
        prodtemp=Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query,item)]
        n=len(prod)
        ns=n//4 + ceil((n/4)-(n//4))
        if len(prod)!=0:
            allprods.append([prod,range(1,ns),ns])
    params={"allprods":allprods}
    return render(request,"shop/search.html",params)
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
def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': (item.datestamp,item.timestamp)})
                    response = json.dumps({"status":"success","updates":updates, "itemsJson":order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"no items"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')