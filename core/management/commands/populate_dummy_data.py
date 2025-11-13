#!/usr/bin/env python
"""Django management command to populate dummy data for Bait ul Rizq"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
import random
from datetime import date, timedelta

from core.models import Community, CustomUser, Donor, Volunteer
from donations.models import Donation, DonationAllocation
from projects.models import ProjectCategory, Project, Recovery
from blog.models import BlogPost, BlogCategory


class Command(BaseCommand):
    help = 'Populate database with dummy data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting to populate dummy data...'))

        # Clear existing data (optional - comment out if you want to keep existing data)
        self.stdout.write('Clearing existing data...')
        Recovery.objects.all().delete()
        DonationAllocation.objects.all().delete()
        Donation.objects.all().delete()
        Project.objects.all().delete()
        ProjectCategory.objects.all().delete()
        BlogPost.objects.all().delete()
        BlogCategory.objects.all().delete()
        Donor.objects.all().delete()
        Volunteer.objects.all().delete()
        CustomUser.objects.filter(is_superuser=False).delete()
        Community.objects.all().delete()

        # Create Communities
        self.stdout.write('Creating communities...')
        intl_community = Community.objects.create(
            name='International Community',
            community_type='INTL',
            description='International donors and beneficiaries'
        )
        pak_community = Community.objects.create(
            name='Pakistani Community',
            community_type='PAK',
            description='Pakistani donors and beneficiaries'
        )

        # Create Users
        self.stdout.write('Creating users...')
        director = CustomUser.objects.create_user(
            username='director',
            email='director@baitulrizq.org',
            password='director123',
            first_name='Ahmed',
            last_name='Director',
            role='DIRECTOR',
            is_staff=True
        )

        intl_manager = CustomUser.objects.create_user(
            username='intl_manager',
            email='intl.manager@baitulrizq.org',
            password='manager123',
            first_name='Sarah',
            last_name='Manager',
            role='INTL_MANAGER',
            community=intl_community,
            is_staff=True
        )

        pak_manager = CustomUser.objects.create_user(
            username='pak_manager',
            email='pak.manager@baitulrizq.org',
            password='manager123',
            first_name='Ali',
            last_name='Manager',
            role='PAK_MANAGER',
            community=pak_community,
            is_staff=True
        )

        # Create Project Categories
        self.stdout.write('Creating project categories...')
        categories = [
            ProjectCategory.objects.create(name='Food Cart', description='Small food carts and stalls'),
            ProjectCategory.objects.create(name='Fruit & Vegetable', description='Selling fresh produce'),
            ProjectCategory.objects.create(name='Tailoring', description='Sewing and tailoring business'),
            ProjectCategory.objects.create(name='General Store', description='Small neighborhood stores'),
            ProjectCategory.objects.create(name='Rickshaw', description='Auto rickshaw for transport')
        ]

        # Create Donors and Donations
        self.stdout.write('Creating donors and donations...')
        donor_names_intl = [
            ('John Smith', 'john.smith@example.com', 'USD'),
            ('Emma Johnson', 'emma.j@example.com', 'USD'),
            ('Michael Brown', 'michael.b@example.com', 'EUR'),
            ('Sarah Davis', 'sarah.d@example.com', 'GBP'),
            ('David Wilson', 'david.w@example.com', 'USD'),
            ('Lisa Anderson', 'lisa.a@example.com', 'EUR'),
        ]

        donor_names_pak = [
            ('Muhammad Ali', 'mali@example.com', 'PKR'),
            ('Fatima Khan', 'fkhan@example.com', 'PKR'),
            ('Ahmed Hassan', 'ahssan@example.com', 'PKR'),
            ('Ayesha Malik', 'amalik@example.com', 'PKR'),
            ('Usman Tariq', 'utariq@example.com', 'PKR'),
            ('Zainab Raza', 'zraza@example.com', 'PKR'),
        ]

        donors = []

        # Create international donors
        for name, email, currency in donor_names_intl:
            donor = Donor.objects.create(
                name=name,
                email=email,
                phone=f'+1-555-{random.randint(1000000, 9999999)}',
                address=f'{random.randint(100, 9999)} Main Street, City, Country',
                community=intl_community,
                is_anonymous=random.choice([True, False])
            )
            donors.append(donor)

            # Create 1-3 donations for each donor
            for _ in range(random.randint(1, 3)):
                amount = Decimal(random.randint(100, 2000))
                Donation.objects.create(
                    donor=donor,
                    amount=amount,
                    currency=currency,
                    payment_method=random.choice(['CARD', 'BANK', 'MOBILE']),
                    date_received=date.today() - timedelta(days=random.randint(1, 180)),
                    notes=f'Donation from {name}'
                )

        # Create Pakistani donors
        for name, email, currency in donor_names_pak:
            donor = Donor.objects.create(
                name=name,
                email=email,
                phone=f'03{random.randint(10, 49)}-{random.randint(1000000, 9999999)}',
                address=f'House #{random.randint(1, 999)}, Street {random.randint(1, 50)}, Karachi/Lahore',
                community=pak_community,
                is_anonymous=random.choice([True, False])
            )
            donors.append(donor)

            # Create 1-3 donations for each donor
            for _ in range(random.randint(1, 3)):
                amount = Decimal(random.randint(5000, 100000))
                Donation.objects.create(
                    donor=donor,
                    amount=amount,
                    currency=currency,
                    payment_method=random.choice(['MOBILE', 'BANK', 'CASH']),
                    date_received=date.today() - timedelta(days=random.randint(1, 180)),
                    notes=f'Donation from {name}'
                )

        # Create Projects (Beneficiaries)
        self.stdout.write('Creating projects...')

        project_data_intl = [
            ('Help Sarah Start Tea Stall', 'Sarah is a widow with 3 children. She wants to start a small tea and snacks stall.', 800, 'USD'),
            ('Fruit Cart for James', 'James lost his job and wants to sell fresh fruits to support his family.', 1200, 'USD'),
            ('Tailor Shop for Maria', 'Maria has good sewing skills and needs a sewing machine to start home-based tailoring.', 600, 'EUR'),
        ]

        project_data_pak = [
            ('Samosa Cart for Rashid', 'محمد راشد ایک محنت کش آدمی ہے جو سموسے بیچنا چاہتا ہے', 25000, 'PKR'),
            ('Fruit Stall for Amina', 'آمنہ اپنے بچوں کی کفالت کے لیے پھل بیچنا چاہتی ہے', 30000, 'PKR'),
            ('General Store for Bilal', 'بلال کو ایک چھوٹا کریانہ سٹور کھولنا ہے', 50000, 'PKR'),
            ('Vegetable Cart for Hamza', 'حمزہ تازہ سبزیاں بیچ کر اپنا گھر چلانا چاہتا ہے', 20000, 'PKR'),
            ('Rickshaw for Khalid', 'خالد رکشا چلا کر اپنی فیملی کا خرچہ اٹھانا چاہتا ہے', 150000, 'PKR'),
        ]

        projects = []
        statuses = ['PENDING', 'APPROVED', 'FUNDED', 'ESTABLISHED', 'RECOVERING']

        # Create international projects
        for idx, (title, desc, amount, currency) in enumerate(project_data_intl):
            status = statuses[min(idx, len(statuses) - 1)]
            project = Project.objects.create(
                beneficiary_name=title.split('for ')[-1] if 'for ' in title else f'Beneficiary {idx+1}',
                title=title,
                description=desc,
                requested_amount=Decimal(amount),
                approved_amount=Decimal(amount) if status != 'PENDING' else None,
                currency=currency,
                category=random.choice(categories),
                status=status,
                community=intl_community,
                is_public=True,
                is_featured=random.choice([True, False]),
                beneficiary_phone=f'+1-555-{random.randint(1000000, 9999999)}',
                beneficiary_email=f'beneficiary{idx+1}@example.com',
                beneficiary_address=f'{random.randint(100, 999)} Street, City, Country',
                family_size=random.randint(2, 6)
            )
            projects.append(project)

        # Create Pakistani projects
        for idx, (title, desc, amount, currency) in enumerate(project_data_pak):
            status = statuses[min(idx, len(statuses) - 1)]
            project = Project.objects.create(
                beneficiary_name=title.split('for ')[-1] if 'for ' in title else f'Beneficiary {idx+10}',
                title=title,
                description=desc,
                requested_amount=Decimal(amount),
                approved_amount=Decimal(amount) if status != 'PENDING' else None,
                currency=currency,
                category=random.choice(categories),
                status=status,
                community=pak_community,
                is_public=True,
                is_featured=random.choice([True, False]),
                beneficiary_phone=f'03{random.randint(10, 49)}-{random.randint(1000000, 9999999)}',
                beneficiary_email=f'beneficiary{idx+10}@example.com',
                beneficiary_address=f'House #{random.randint(1, 999)}, Street {random.randint(1, 50)}, Karachi',
                family_size=random.randint(2, 8)
            )
            projects.append(project)

        # Create Donation Allocations
        self.stdout.write('Creating donation allocations...')
        all_donations = list(Donation.objects.all())

        for project in projects:
            if project.status in ['FUNDED', 'ESTABLISHED', 'RECOVERING']:
                # Allocate donations to funded projects
                needed = project.approved_amount or project.requested_amount
                allocated = Decimal('0.00')

                # Match community donations to community projects
                matching_donations = [d for d in all_donations if d.donor.community == project.community]

                for donation in random.sample(matching_donations, min(3, len(matching_donations))):
                    if allocated >= needed:
                        break

                    remaining_in_donation = donation.remaining_amount()
                    if remaining_in_donation > 0:
                        allocation_amount = min(remaining_in_donation, needed - allocated)

                        DonationAllocation.objects.create(
                            donation=donation,
                            project=project,
                            amount=allocation_amount,
                            allocated_date=project.application_date + timedelta(days=random.randint(5, 30))
                        )
                        allocated += allocation_amount

        # Create Recoveries for established/recovering projects
        self.stdout.write('Creating recoveries...')
        for project in projects:
            if project.status in ['RECOVERING']:
                # Create 2-6 monthly recoveries
                for month in range(random.randint(2, 6)):
                    recovery_amount = Decimal(random.randint(10, 30)) / 100 * (project.approved_amount or project.requested_amount)
                    Recovery.objects.create(
                        project=project,
                        amount=recovery_amount,
                        recovery_date=date.today() - timedelta(days=30 * (month + 1)),
                        notes=f'Monthly contribution - Month {month + 1}'
                    )

        # Create Blog Categories
        self.stdout.write('Creating blog categories...')
        success_category = BlogCategory.objects.create(
            name='Success Story',
            slug='success-story',
            description='Success stories from beneficiaries'
        )
        info_category = BlogCategory.objects.create(
            name='Information',
            slug='information',
            description='Information about our programs and processes'
        )
        community_category = BlogCategory.objects.create(
            name='Community',
            slug='community',
            description='Community updates and volunteer stories'
        )
        report_category = BlogCategory.objects.create(
            name='Report',
            slug='report',
            description='Transparency reports and financial updates'
        )

        # Create Blog Posts
        self.stdout.write('Creating blog posts...')
        blog_posts = [
            {
                'title': 'Success Story: How Rashid Built His Samosa Business',
                'excerpt': 'From struggling to feed his family to running a successful samosa cart',
                'content': '''
                <h2>A Journey of Transformation</h2>
                <p>Muhammad Rashid, a father of four, was struggling to make ends meet. After losing his job,
                he approached Bait ul Rizq with a dream - to start a small samosa cart.</p>

                <p>With support from our generous donors, Rashid received funding to purchase a cart, cooking
                equipment, and initial inventory. Today, just 6 months later, he's not only supporting his family
                but also contributing back to help others.</p>

                <blockquote>"This opportunity changed my life. Now I can provide for my family with dignity and
                help others like me." - Muhammad Rashid</blockquote>
                ''',
                'category': success_category,
                'featured': True
            },
            {
                'title': 'Understanding Our Self-Sustaining Model',
                'excerpt': 'How donations create a continuous cycle of giving',
                'content': '''
                <h2>The Power of Sustainable Charity</h2>
                <p>At Bait ul Rizq, we believe in empowering people, not just providing handouts. Our unique
                model ensures that every donation creates lasting impact.</p>

                <p>When a beneficiary's business becomes established, they begin making monthly contributions
                back to the fund. These contributions then fund new businesses, creating a self-sustaining
                cycle of prosperity.</p>
                ''',
                'category': info_category,
                'featured': True
            },
            {
                'title': 'Meet Our Volunteers: The Heart of Bait ul Rizq',
                'excerpt': 'Dedicated volunteers who make everything possible',
                'content': '''
                <h2>Community Volunteers</h2>
                <p>Our volunteers are the backbone of our organization. They verify beneficiaries, mentor
                new business owners, and ensure transparency in every transaction.</p>

                <p>From conducting field visits to providing business guidance, our volunteers dedicate
                countless hours to transform lives.</p>
                ''',
                'category': community_category,
                'featured': False
            },
            {
                'title': 'Transparency Report: Q1 2025',
                'excerpt': 'Complete breakdown of donations and allocations',
                'content': '''
                <h2>Quarterly Transparency Report</h2>
                <p>In Q1 2025, we received donations totaling $45,000 and PKR 2,500,000. Here's how
                every penny was utilized:</p>

                <ul>
                    <li>85% directly funded new businesses</li>
                    <li>10% used for business training and mentorship</li>
                    <li>5% for administrative and verification costs</li>
                </ul>

                <p>Every donor can track their specific contribution using their unique donor ID.</p>
                ''',
                'category': report_category,
                'featured': True
            }
        ]

        for post_data in blog_posts:
            BlogPost.objects.create(
                title=post_data['title'],
                slug=post_data['title'].lower().replace(' ', '-').replace(':', ''),
                excerpt=post_data['excerpt'],
                content=post_data['content'],
                category=post_data['category'],
                author=director,
                is_published=True,
                is_featured=post_data['featured'],
                published_date=timezone.now() - timedelta(days=random.randint(1, 90))
            )

        # Create Volunteers
        self.stdout.write('Creating volunteers...')
        volunteer_data = [
            ('Omar Farooq', 'omar.f@example.com', '0321-7654321', pak_community, 'Field verification, mentoring'),
            ('Aisha Siddiqui', 'aisha.s@example.com', '0333-1234567', pak_community, 'Documentation, follow-up'),
            ('Jennifer Wilson', 'jen.w@example.com', '+1-555-2345678', intl_community, 'Online coordination'),
        ]

        for name, email, phone, community, skills in volunteer_data:
            Volunteer.objects.create(
                name=name,
                email=email,
                phone=phone,
                address='Volunteer address',
                community=community,
                skills=skills,
                availability='Weekends',
                message='Passionate about helping the community',
                is_approved=True
            )

        # Print Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('SUMMARY OF CREATED DATA'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(f'Communities: {Community.objects.count()}')
        self.stdout.write(f'Users: {CustomUser.objects.count()}')
        self.stdout.write(f'Donors: {Donor.objects.count()}')
        self.stdout.write(f'Donations: {Donation.objects.count()}')
        self.stdout.write(f'Projects: {Project.objects.count()}')
        self.stdout.write(f'Allocations: {DonationAllocation.objects.count()}')
        self.stdout.write(f'Recoveries: {Recovery.objects.count()}')
        self.stdout.write(f'Blog Posts: {BlogPost.objects.count()}')
        self.stdout.write(f'Volunteers: {Volunteer.objects.count()}')
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(self.style.SUCCESS('\nDummy data populated successfully!'))
        self.stdout.write(self.style.WARNING('\nTest Login Credentials:'))
        self.stdout.write('Director: username=director, password=director123')
        self.stdout.write('Intl Manager: username=intl_manager, password=manager123')
        self.stdout.write('Pak Manager: username=pak_manager, password=manager123')
