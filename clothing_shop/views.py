from collections import defaultdict

from django.db.models import Sum
from django.shortcuts import render
from datetime import datetime, timedelta
from clothing_shop.models import Branch, Product, Sale, WebsiteView, Inventory


def prediction_dashboard(request):
    recent_days = 30
    sales = Sale.objects.filter(timestamp__gte=datetime.now() - timedelta(days=recent_days))
    views = WebsiteView.objects.filter(date__gte=datetime.now().date() - timedelta(days=recent_days))

    branch_crowd_levels = {b.name: b.crowd_level for b in Branch.objects.all()}
    products = list(Product.objects.values_list('name', flat=True))
    branches = list(Branch.objects.values_list('name', flat=True))

    sales_data = [(s.product.name, s.branch.name if s.branch else "Online", s.sale_type, s.quantity, s.timestamp) for s in sales]
    website_views = defaultdict(int)
    for v in views:
        website_views[v.product.name] += v.views

    def analyze_workforce_and_inventory(sales_data, website_views, branch_crowd_levels):
        online_sales = 0
        offline_sales = 0
        branch_product_demand = defaultdict(lambda: defaultdict(int))

        for product, branch, sale_type, qty, date in sales_data:
            if sale_type == "online":
                online_sales += qty
            else:
                offline_sales += qty
            branch_product_demand[branch][product] += qty

        total_sales = online_sales + offline_sales
        online_ratio = online_sales / total_sales if total_sales else 0
        offline_ratio = offline_sales / total_sales if total_sales else 0

        if online_ratio > 0.6:
            workforce_suggestion = "Transfer some sellers to online admins"
        elif offline_ratio > 0.6:
            workforce_suggestion = "Transfer some admins to offline sellers"
        else:
            workforce_suggestion = "Maintain current workforce balance"

        inventory_distribution = {}
        stock_distribution = {}
        for branch in branches:
            product_alloc = {}
            product_stock = {}
            for product in products:
                recent_sales = branch_product_demand[branch][product]
                view_score = website_views.get(product, 0)
                crowd_bonus = branch_crowd_levels.get(branch, 0) * 10
                score = recent_sales + view_score * 0.1 + crowd_bonus
                product_alloc[product] = int(score)
                stock = Inventory.objects.filter(product__name=product, branch__name=branch).aggregate(Sum('quantity'))["quantity__sum"]
                product_stock[product] = stock
            inventory_distribution[branch] = product_alloc
            stock_distribution[branch] = product_stock
        return workforce_suggestion, inventory_distribution, stock_distribution

    def suggest_product_transfers(inventory_distribution, threshold_diff=20):
        product_scores_by_branch = defaultdict(dict)
        for branch, products in inventory_distribution.items():
            for product, score in products.items():
                product_scores_by_branch[product][branch] = score

        transfer_suggestions = []

        for product, branch_scores in product_scores_by_branch.items():
            sorted_branches = sorted(branch_scores.items(), key=lambda x: x[1])
            low_branch, low_score = sorted_branches[0]
            high_branch, high_score = sorted_branches[-1]

            if high_score - low_score >= threshold_diff:
                qty_to_transfer = min(10, int((high_score - low_score) / 2))
                transfer_suggestions.append({
                    "product": product,
                    "from_branch": low_branch,
                    "to_branch": high_branch,
                    "quantity": qty_to_transfer
                })

        return transfer_suggestions

    suggestion, distribution, stock_distribution = analyze_workforce_and_inventory(sales_data, website_views, branch_crowd_levels)
    transfer_suggestion = suggest_product_transfers(distribution)

    return render(request, 'prediction_dashboard.html', {
        'workforce_suggestion': suggestion,
        'inventory_distribution': distribution,
        'inventory_stock': stock_distribution,
        'transfer_suggestions': transfer_suggestion,
    })
