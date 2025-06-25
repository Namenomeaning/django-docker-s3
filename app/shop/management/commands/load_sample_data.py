from django.core.management.base import BaseCommand
from django.utils.text import slugify
from shop.models import Category, Product
from decimal import Decimal


class Command(BaseCommand):
    help = 'Load sample data for the shop'

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {
                'name': 'Electronics',
                'description': 'Electronic devices and gadgets'
            },
            {
                'name': 'Clothing',
                'description': 'Fashion and apparel'
            },
            {
                'name': 'Books',
                'description': 'Books and literature'
            },
            {
                'name': 'Home & Garden',
                'description': 'Home improvement and garden supplies'
            },
            {
                'name': 'Sports',
                'description': 'Sports equipment and gear'
            }
        ]

        self.stdout.write('Creating categories...')
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'description': cat_data['description']
                }
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create products
        products_data = [
            # Electronics
            {
                'category': 'Electronics',
                'name': 'Smartphone Pro Max',
                'description': 'Latest flagship smartphone with advanced camera system and 5G connectivity.',
                'price': '999.99',
                'stock': 25
            },
            {
                'category': 'Electronics',
                'name': 'Wireless Headphones',
                'description': 'Premium noise-cancelling wireless headphones with 30-hour battery life.',
                'price': '299.99',
                'stock': 50
            },
            {
                'category': 'Electronics',
                'name': 'Laptop Ultrabook',
                'description': 'Lightweight laptop with powerful processor and all-day battery.',
                'price': '1299.99',
                'stock': 15
            },
            {
                'category': 'Electronics',
                'name': 'Smart Watch',
                'description': 'Fitness tracking smartwatch with GPS and heart rate monitor.',
                'price': '399.99',
                'stock': 30
            },
            
            # Clothing
            {
                'category': 'Clothing',
                'name': 'Premium Cotton T-Shirt',
                'description': 'Comfortable and breathable cotton t-shirt in various colors.',
                'price': '29.99',
                'stock': 100
            },
            {
                'category': 'Clothing',
                'name': 'Denim Jeans',
                'description': 'Classic fit denim jeans made from sustainable materials.',
                'price': '79.99',
                'stock': 75
            },
            {
                'category': 'Clothing',
                'name': 'Winter Jacket',
                'description': 'Warm and waterproof winter jacket for cold weather.',
                'price': '199.99',
                'stock': 40
            },
            
            # Books
            {
                'category': 'Books',
                'name': 'Python Programming Guide',
                'description': 'Comprehensive guide to Python programming for beginners and experts.',
                'price': '49.99',
                'stock': 60
            },
            {
                'category': 'Books',
                'name': 'Science Fiction Novel',
                'description': 'Bestselling science fiction novel about space exploration.',
                'price': '19.99',
                'stock': 80
            },
            {
                'category': 'Books',
                'name': 'Cookbook Collection',
                'description': 'Collection of healthy recipes from around the world.',
                'price': '34.99',
                'stock': 45
            },
            
            # Home & Garden
            {
                'category': 'Home & Garden',
                'name': 'Smart Home Hub',
                'description': 'Central hub for controlling all your smart home devices.',
                'price': '149.99',
                'stock': 35
            },
            {
                'category': 'Home & Garden',
                'name': 'Indoor Plant Set',
                'description': 'Set of 3 low-maintenance indoor plants perfect for any room.',
                'price': '59.99',
                'stock': 70
            },
            
            # Sports
            {
                'category': 'Sports',
                'name': 'Yoga Mat Premium',
                'description': 'Non-slip premium yoga mat with carrying strap.',
                'price': '89.99',
                'stock': 55
            },
            {
                'category': 'Sports',
                'name': 'Running Shoes',
                'description': 'Lightweight running shoes with advanced cushioning technology.',
                'price': '159.99',
                'stock': 40
            },
        ]

        self.stdout.write('Creating products...')
        for prod_data in products_data:
            try:
                category = Category.objects.get(name=prod_data['category'])
                product, created = Product.objects.get_or_create(
                    name=prod_data['name'],
                    defaults={
                        'category': category,
                        'slug': slugify(prod_data['name']),
                        'description': prod_data['description'],
                        'price': Decimal(prod_data['price']),
                        'stock': prod_data['stock'],
                        'available': True
                    }
                )
                if created:
                    self.stdout.write(f'Created product: {product.name}')
            except Category.DoesNotExist:
                self.stdout.write(f'Category {prod_data["category"]} not found')

        self.stdout.write(
            self.style.SUCCESS('Successfully loaded sample data!')
        )
