from django.core.management.base import BaseCommand
from store.models import Category, Testimonial


class Command(BaseCommand):
    help = 'Seeds initial categories and testimonials for Sundari Silk Palace (safe to run multiple times)'

    def handle(self, *args, **options):
        # --- Categories ---
        self.stdout.write('Seeding categories...')
        categories = [
            ('Saree', 'saree'),
            ('Kurti', 'kurti'),
            ('Lehenga', 'lehenga'),
            ('Chaniya Choli', 'chaniya-choli'),
            ('Patola', 'patola'),
            ('Banarasi', 'banarasi'),
        ]
        for name, slug in categories:
            obj, created = Category.objects.get_or_create(slug=slug, defaults={'name': name})
            if created:
                self.stdout.write(f'  Created category: {name}')
            else:
                self.stdout.write(f'  Already exists: {name}')

        # --- Testimonials ---
        self.stdout.write('Seeding testimonials...')
        testimonials = [
            {
                'author': 'Priya S.',
                'quote': 'Amazing collection and very reasonable prices. A must-visit in Ahmedabad!',
                'rating': 5,
            },
            {
                'author': 'Neha M.',
                'quote': 'The designs are unique and the quality is top-notch. Highly recommended.',
                'rating': 5,
            },
            {
                'author': 'Rina P.',
                'quote': 'I have been a customer for years. Sundari Silk Palace never disappoints.',
                'rating': 5,
            },
            {
                'author': 'Kavita D.',
                'quote': 'Best saree collection in Ahmedabad. The staff is also very helpful and kind.',
                'rating': 5,
            },
        ]
        for t in testimonials:
            obj, created = Testimonial.objects.get_or_create(
                author=t['author'],
                defaults={'quote': t['quote'], 'rating': t['rating'], 'is_active': True}
            )
            if created:
                self.stdout.write(f'  Created testimonial: {t["author"]}')
            else:
                self.stdout.write(f'  Already exists: {t["author"]}')

        self.stdout.write(self.style.SUCCESS('\nSeeding complete!'))