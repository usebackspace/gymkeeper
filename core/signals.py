from .models import SubscriptionPlan

def create_subscription_plans(sender, **kwargs):
    plans = [
        {'name': 'FREE', 'price': 0},
        {'name': 'STANDARD', 'price': 499},
        {'name': 'PREMIUM', 'price': 999},
    ]
    for plan in plans:
        SubscriptionPlan.objects.get_or_create(name=plan['name'], defaults={'price': plan['price']})


# ==Every Time we don't have create object for drop -down menu ===
# SubscriptionPlan.objects.bulk_create([
#     SubscriptionPlan(name='FREE', price=0.0),
#     SubscriptionPlan(name='STANDARD', price=499.0),
#     SubscriptionPlan(name='PREMIUM', price=999.0),
# ])
