from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import MenuItem, Order, OrderItem


def login_view(request):
    """Clock-in / login page."""
    if request.user.is_authenticated:
        return redirect('order')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('order')
        else:
            error = 'Invalid username or password.'

    return render(request, 'login.html', {'error': error})


def logout_view(request):
    """Clock out."""
    logout(request)
    return redirect('login')
## secret view easter egg for fun, not linked anywhere in the UI
def secret_view(request):
    return render(request, 'secret.html')


@login_required(login_url='login')
def order_view(request):
    """Main order-taking screen."""
    order, created = Order.objects.get_or_create(status='open', defaults={'table_number': 'Walk-in'})

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add_item':
            menu_item_id = request.POST.get('menu_item_id')
            notes = request.POST.get('notes', '')
            menu_item = get_object_or_404(MenuItem, id=menu_item_id)
            order_item, created = OrderItem.objects.get_or_create(
                order=order,
                menu_item=menu_item,
                defaults={'quantity': 1, 'notes': notes}
            )
            if not created:
                order_item.quantity += 1
                order_item.save()

        elif action == 'remove_item':
            item_id = request.POST.get('item_id')
            OrderItem.objects.filter(id=item_id, order=order).delete()

        elif action == 'send_to_kitchen':
            order.notes = request.POST.get('kitchen_notes', '')
            order.status = 'sent'
            order.save()
            return redirect('order')

        elif action == 'clear_order':
            order.items.all().delete()

        elif action == 'toggle_rush':
            order.rush = not order.rush
            order.save()

        return redirect('order')

    menu_items = MenuItem.objects.all().order_by('category', 'name')
    categories = {}
    for item in menu_items:
        categories.setdefault(item.get_category_display(), []).append(item)

    context = {
        'order': order,
        'order_items': order.items.all(),
        'categories': categories,
        'total': order.total(),
    }
    return render(request, 'order.html', context)


@login_required(login_url='login')
def kitchen_view(request):
    """Kitchen display showing sent orders."""
    if request.method == 'POST':
        action = request.POST.get('action')
        order_id = request.POST.get('order_id')
        order = get_object_or_404(Order, id=order_id)

        if action == 'mark_done':
            order.status = 'done'
            order.save()

        elif action == 'delete_order':
            order.delete()

        elif action == 'remove_item':
            item_id = request.POST.get('item_id')
            OrderItem.objects.filter(id=item_id, order=order).delete()

        elif action == 'update_quantity':
            item_id = request.POST.get('item_id')
            quantity = int(request.POST.get('quantity', 1))
            item = get_object_or_404(OrderItem, id=item_id, order=order)
            if quantity <= 0:
                item.delete()
            else:
                item.quantity = quantity
                item.save()

        elif action == 'update_notes':
            order.notes = request.POST.get('kitchen_notes', '')
            order.save()

        elif action == 'add_item':
            menu_item_id = request.POST.get('menu_item_id')
            menu_item = get_object_or_404(MenuItem, id=menu_item_id)
            order_item, created = OrderItem.objects.get_or_create(
                order=order,
                menu_item=menu_item,
                defaults={'quantity': 1}
            )
            if not created:
                order_item.quantity += 1
                order_item.save()

        return redirect('kitchen')

    orders = Order.objects.filter(status='sent').order_by('created_at')
    menu_items = MenuItem.objects.all().order_by('category', 'name')
    return render(request, 'kitchen.html', {'orders': orders, 'menu_items': menu_items})