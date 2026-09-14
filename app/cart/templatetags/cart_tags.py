from django import template

register = template.Library()

@register.filter
def get_item(cart,product_id):
    return cart.get(str(product_id),{}).get('quantity',0)
