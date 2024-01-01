from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Orders, OrderUpdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum
MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'
# Create your views here.

def index(request):
    # product = Product.objects.all()
    # print(products)
    allprod = []
    catprods = Product.objects.values('Category')
    print(catprods)
    cats = {item['Category'] for item in catprods}
    print(cats)

    for cat in cats:
        prod = Product.objects.filter(Category=cat)
        print(prod)
        n = len(prod)
        nslides = n//4 + ceil((n/4) - (n//4))
        allprod.append([prod, range(1, nslides)])
    # allprod = [[product, range(1, nslides)],
    #            [product, range(1, nslides)]]
    params = {
        'allprod': allprod
    }
    return render(request, 'shop/index.html', params)

def searchMatch(query, item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.Category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allprod = []
    catprods = Product.objects.values('Category')
    print(catprods)
    cats = {item['Category'] for item in catprods}
    print(cats)

    for cat in cats:
        prodtemp = Product.objects.filter(Category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        print(prod)
        n = len(prod)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allprod.append([prod, range(1, nslides)])
    # allprod = [[product, range(1, nslides)],
    #            [product, range(1, nslides)]]
    params = {
        'allprod': allprod
    }
    return render(request, 'shop/index.html', params)

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', 0000)
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()

        print(name, email, phone, desc)
    return render(request, 'shop/contact.html')

def tracker(request):
    if request.method == "POST":
        order_id = request.POST.get('orderid', '')
        email = request.POST.get('email', '')
        # return HttpResponse(f"{order_id} and {email}")
        try:
            order = Orders.objects.filter(order_id=order_id, email=email)
            print(order)
            # print(order)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id = order_id)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].item_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')
    return render(request, 'shop/tracker.html')


def productview(request, myid):
    #Fetching id
    product = Product.objects.filter(id=myid)
    print(product)
    return render(request, 'shop/productview.html', {'product': product[0]})

def checkout(request):
    if request.method=="POST":
        item_json = request.POST.get('inputJson', '')
        amount = request.POST.get('amount', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip = request.POST.get('zip', '')
        phone = request.POST.get('phone', 0000)
        order = Orders(item_json=item_json, amount=amount, name=name, email=email, phone=phone, address=address,
                       city=city, state=state, zip_code=zip)
        order.save()
        update = OrderUpdate(order_id = order.order_id, update_desc='Order Placed')
        update.save()
        thank = True
        id = order.order_id
        # return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
        # request paytm to transfer the amount to your account after payment by user
        param_dict = {

            'MID': 'WorldP64425807474247',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})
    return render(request, 'shop/checkout.html')


@csrf_exempt
def handlerequest(request):
    #Paytm will send post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == "01":
            print("Order Successful")
        else:
            print("Order unsuccesful because" + response_dict['RESPMSG'])
    # PayTmparams["body"] = {
    #     'requestType' :'Payment',
    #     "merchant_id": "Merchant id here",
    #     'order_id': Orders.order_id,
    #     'website_name': 127.0.0.1:8000/shop,
    #     'CallBackUrl': 127.0.0.1:8000/checkout,
    #     "Transaction_amount": {
    #         "value": "1.00",
    #         "currency": "USD","INR"
    #     },
    #     "User_info": {
    #         "Customer_id": "cust_01",
    #     },
    # }

    # PayTmparams["body"]: {
    #     "signature": checksum
    # }
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})
