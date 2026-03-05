
from django.shortcuts import render

# Import HttpResponse to send text-based responses
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem, Order, OrderItem

# Define the home view function
def home(request):
    # Send a simple HTML response
    return HttpResponse('Pizza Point Home Page')
def kitchen(request):
    return render(request, 'kitchen.html')




def order_view(request):
    """Main order-taking screen."""
    # Get or create the current open order
    order, created = Order.objects.get_or_create(status='open', defaults={'table_number': 'Walk-in'})

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add_item':
            menu_item_id = request.POST.get('menu_item_id')
            notes = request.POST.get('notes', '')
            menu_item = get_object_or_404(MenuItem, id=menu_item_id)
            # If item already in order, increase quantity
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


def kitchen_view(request):
    """Kitchen display orders we took."""
    if request.method == 'POST':
        action = request.POST.get('action')
        order_id = request.POST.get('order_id')
        order = get_object_or_404(Order, id=order_id)

        if action == 'mark_done':
            order.status = 'done'
            order.save()

        return redirect('kitchen')

    orders = Order.objects.filter(status='sent').order_by('created_at')
    return render(request, 'kitchen.html', {'orders': orders})