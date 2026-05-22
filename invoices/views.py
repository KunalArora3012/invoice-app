from django.shortcuts import render,redirect
from .models import Invoice , InvoiceItem, Customer
from products.models import Product
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse

def create_invoice(request):
    if 'user' not in request.session:
        return redirect('login')

    products = Product.objects.all()

    if request.method == "POST":
        # Customer
        customer = Customer.objects.create(
            name=request.POST['name'],
            contact=request.POST['contact'],
            address=request.POST['address']
        )

        payment_method = request.POST['payment']

        product_ids = request.POST.getlist('product')
        quantities = request.POST.getlist('quantity')

        total = 0

        invoice = Invoice.objects.create(
            customer=customer,
            payment_method=payment_method,
            tax=0,
            total_amount=0
        )

        for i in range(len(product_ids)):
            product = Product.objects.get(id=product_ids[i])
            qty = int(quantities[i])

            if product.quantity < qty:
                return render(request, 'invoice.html', {
                    'products': products,
                    'error': f'Not enough stock for {product.name}'
                })

            price = product.price * qty
            total += price

            # Save item
            InvoiceItem.objects.create(
                invoice=invoice,
                product=product,
                quantity=qty,
                price=price
            )

            #  Reduce stock
            product.quantity -= qty
            product.save()

        # Tax (example: 18%)
        tax = total * 0.18
        grand_total = total + tax

        invoice.tax = tax
        invoice.total_amount = grand_total
        invoice.save()

        return redirect('invoice')

    return render(request, 'invoice.html', {'products': products})

def invoice_history(request):
    invoices = Invoice.objects.all().order_by('-id')
    return render(request, 'invoice_history.html', {'invoices': invoices})

def invoice_detail(request, id):
    invoice = Invoice.objects.get(id=id)
    items = InvoiceItem.objects.filter(invoice=invoice)

    return render(request, 'invoice_detail.html', {
        'invoice': invoice,
        'items': items
    })


def download_invoice(request, id):
    invoice = Invoice.objects.get(id=id)
    items = InvoiceItem.objects.filter(invoice=invoice)

    template = get_template('invoice_pdf.html')

    html = template.render({
        'invoice': invoice,
        'items': items
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{id}.pdf"'

    pisa.CreatePDF(html, dest=response)

    return response