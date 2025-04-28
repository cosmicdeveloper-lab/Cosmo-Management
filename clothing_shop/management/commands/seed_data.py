from datetime import datetime, timedelta, date
import random
from django.core.management import BaseCommand
from clothing_shop.models import *


class Command(BaseCommand):
    help = 'Seed dummy data into the database'

    def handle(self, *args, **kwargs):

        Branch.objects.all().delete()
        Employee.objects.all().delete()
        Product.objects.all().delete()
        Inventory.objects.all().delete()
        Sale.objects.all().delete()
        Event.objects.all().delete()
        WebsiteView.objects.all().delete()

        branches = [Branch.objects.create(name=f"Branch {i}", location=f"Location {i}",
                                          crowd_level=random.random())
                    for i in range(5)]

        products = [Product.objects.create(name=f"Product {i}",
                                           category=random.choice(['Shirt', 'Pants', 'Jacket']),
                                           season=random.choice(['Summer', 'Winter', 'Spring']),
                                           fashion_tag=random.choice(['New', 'Trending', 'Classic']))
                    for i in range(10)]

        for i in range(20):
            Employee.objects.create(
                name=f"Employee {i}",
                role=random.choice(['admin', 'seller']),
                current_branch=random.choice(branches)
            )

        for product in products:
            Inventory.objects.create(product=product, is_online_warehouse=True, quantity=random.randint(10, 100))
            for branch in branches:
                Inventory.objects.create(product=product, branch=branch, quantity=random.randint(5, 50))

        today = date.today()
        for i in range(60):
            day = today - timedelta(days=i)
            for _ in range(random.randint(5, 15)):
                product = random.choice(products)
                Sale.objects.create(
                    product=product,
                    sale_type=random.choice(['online', 'offline']),
                    branch=random.choice(branches),
                    quantity=random.randint(1, 5),
                    timestamp=datetime.combine(day, datetime.min.time())
                )
                WebsiteView.objects.create(
                    product=product,
                    views=random.randint(10, 500),
                    date=day
                )

        for i in range(5):
            start = today - timedelta(days=random.randint(10, 50))
            end = start + timedelta(days=random.randint(1, 7))
            Event.objects.create(
                name=f"Event {i}",
                event_type=random.choice(['Holiday', 'Fashion', 'Clearance']),
                start_date=start,
                end_date=end
            )

        self.stdout.write(self.style.SUCCESS("Dummy data seeded successfully."))
