from django.shortcuts import render, redirect , get_object_or_404
from .models import Product


def product_view(request):
    if 'user' not in request.session:
        return redirect('login')

    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})


def add_product(request):
    if request.method == "POST":
        Product.objects.create(
            name=request.POST['name'],
            price=request.POST['price'],
            quantity=request.POST['quantity']
        )
    return redirect('products')


def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('products')


def edit_product(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        product.name = request.POST['name']
        product.price = request.POST['price']
        product.quantity = request.POST['quantity']
        product.save()
        return redirect('products')

    return render(request, 'edit_product.html', {'product': product})