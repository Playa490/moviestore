"""
Script to create test data for Local Popularity Map
Run this with: python manage.py shell
Then copy and paste the code below, or use: python manage.py shell < create_test_data.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moviestore.settings')
django.setup()

from django.contrib.auth.models import User
from movies.models import Movie
from cart.models import Order, Item
import random

# Create or get a test user
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={'email': 'test@example.com'}
)
if created:
    user.set_password('testpass123')
    user.save()
    print(f"[OK] Created user: {user.username} / testpass123")
else:
    print(f"[OK] Using existing user: {user.username}")

# Get all movies
movies = list(Movie.objects.all())
if not movies:
    print("[ERROR] No movies found! Please add movies through the admin panel first.")
    print("   Go to: http://127.0.0.1:8000/admin/")
    exit()

print(f"[OK] Found {len(movies)} movies:")
for m in movies:
    print(f"  - {m.name}")

# Regions to create test data for
regions = ['Northeast', 'Southeast', 'Midwest', 'Southwest', 'West', 'International']

# Delete existing test orders (optional)
Order.objects.filter(user=user).delete()
print("\n[OK] Cleared existing test orders")

# Create orders with different regions
orders_created = 0
items_created = 0

for region in regions:
    # Create 2-3 orders per region
    for i in range(2):
        # Select 1-3 random movies
        num_movies = random.randint(1, min(3, len(movies)))
        selected_movies = random.sample(movies, num_movies)
        
        # Calculate total
        total = sum(m.price * random.randint(1, 3) for m in selected_movies)
        
        # Create order
        order = Order.objects.create(
            user=user,
            total=total,
            region=region
        )
        
        # Add items
        for movie in selected_movies:
            quantity = random.randint(1, 3)
            Item.objects.create(
                order=order,
                movie=movie,
                price=movie.price,
                quantity=quantity
            )
            items_created += 1
        
        orders_created += 1

print(f"\n[OK] Created {orders_created} orders across {len(regions)} regions")
print(f"[OK] Created {items_created} items total")
print("\n" + "="*60)
print("NOW YOU CAN:")
print("1. Start server: python manage.py runserver")
print("2. Go to: http://127.0.0.1:8000/local-popularity-map")
print("3. Login with: testuser / testpass123")
print("4. Click on region markers to see trending movies!")
print("="*60)
