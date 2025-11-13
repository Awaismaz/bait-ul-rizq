# Bait ul Rizq - Quick Start Commands

## Essential Commands (Copy & Paste Ready)

### 1. Activate Environment
```bash
conda activate bait
```

### 2. Run Development Server
```bash
python manage.py runserver
```
Then open: http://localhost:8000/

### 3. Create Superuser (First Time Only)
```bash
python manage.py createsuperuser
```

### 4. Initialize Communities (Run Once)
```bash
python manage.py shell
```
Then paste:
```python
from core.models import Community
Community.objects.get_or_create(community_type='INTL', defaults={'name': 'International Community', 'description': 'International donors and projects'})
Community.objects.get_or_create(community_type='PAK', defaults={'name': 'Pakistani Community', 'description': 'Pakistani donors and projects'})
print("✓ Communities created successfully!")
exit()
```

### 5. Create Sample Data (Optional - for testing)
```bash
python manage.py shell
```
Then paste:
```python
from core.models import Community, Donor
from projects.models import ProjectCategory, Project
from django.utils import timezone
import random

# Get communities
intl = Community.objects.get(community_type='INTL')
pak = Community.objects.get(community_type='PAK')

# Create categories
categories = [
    ('Food Cart', 'کھانے کی ٹھیلی'),
    ('Small Shop', 'چھوٹی دکان'),
    ('Tailoring', 'سلائی کاری'),
    ('Mobile Repair', 'موبائل مرمت'),
]
for name_en, name_ur in categories:
    ProjectCategory.objects.get_or_create(name=name_en, defaults={'name_ur': name_ur})

print("✓ Sample data created!")
exit()
```

## Project Structure

```
bait_ul_rizq/
│
├── manage.py              # Django management script
├── db.sqlite3             # Database file
├── README.md              # Project overview
├── SETUP_GUIDE.md         # Detailed setup guide
├── QUICK_START.md         # This file
│
├── config/                # Project settings
│   ├── settings.py        # Main settings
│   ├── urls.py            # URL routing
│   └── wsgi.py
│
├── core/                  # Core functionality
│   ├── models.py          # Community, User, Donor, Volunteer
│   ├── admin.py           # Admin configuration
│   ├── views.py           # Views
│   └── urls.py            # URL patterns
│
├── donations/             # Donation management
│   ├── models.py          # Donation, DonationAllocation
│   ├── admin.py
│   └── ...
│
├── projects/              # Project/Beneficiary management
│   ├── models.py          # Project, Recovery, ProjectUpdate
│   ├── admin.py
│   ├── views.py
│   └── urls.py
│
├── blog/                  # Blog system
│   ├── models.py          # BlogPost, BlogCategory
│   └── ...
│
└── pages/                 # Static pages
    ├── models.py          # Page
    └── ...
```

## Important URLs

### Admin Panel
- **URL**: http://localhost:8000/admin/
- **Login**: Use superuser credentials

### Public Website
- **Homepage**: http://localhost:8000/
- **Donor Lookup**: http://localhost:8000/donor-lookup/
- **Projects**: http://localhost:8000/projects/
- **Blog**: http://localhost:8000/blog/
- **Apply for Help**: http://localhost:8000/projects/apply/
- **Volunteer**: http://localhost:8000/volunteer-application/

## Key Features Checklist

### Core System ✅
- [x] Multi-community support (International & Pakistani)
- [x] Role-based access control (Director, Managers, Staff)
- [x] Bilingual support (English & Urdu)

### Donor Management ✅
- [x] Anonymous 9-digit donor ID system
- [x] No-authentication donor lookup
- [x] Privacy controls
- [x] Total donation tracking

### Donation System ✅
- [x] Multiple currency support
- [x] Payment method tracking
- [x] Many-to-many allocation to projects
- [x] Prevents over-allocation
- [x] Receipt tracking

### Project Management ✅
- [x] Complete beneficiary workflow (Pending → Approved → Funded → Established → Recovering)
- [x] Beneficiary information & verification
- [x] Financial tracking
- [x] Project categories
- [x] Progress updates with photos
- [x] Document uploads

### Recovery System ✅
- [x] Monthly recovery tracking
- [x] Auto-calculation of total recovered
- [x] Progress monitoring
- [x] Self-sustaining model

### Public Website ✅
- [x] Donor lookup portal
- [x] Project listings
- [x] Beneficiary application form
- [x] Volunteer application form
- [x] Blog system
- [x] Static pages (About, Policies, etc.)

### Admin Features ✅
- [x] Comprehensive dashboard
- [x] Role-based data filtering
- [x] Inline editing
- [x] Autocomplete search
- [x] Progress bars & visual indicators
- [x] Export capabilities

## Workflow Examples

### Adding a New Donor
1. Admin → Donors → Add Donor
2. Fill name, email, phone, community
3. Save → Copy the 9-digit ID
4. Give ID to donor for future tracking

### Recording & Allocating a Donation
1. Admin → Donations → Add Donation
2. Select donor, enter amount & details
3. Save
4. Scroll to "Donation allocations" inline
5. Add allocation to project(s)
6. Save

### Managing a Project Lifecycle
1. **Application**: Beneficiary applies via website
2. **Verification**: Admin reviews & sets status to "Pending"
3. **Approval**: Admin verifies, sets "Approved", enters approved amount
4. **Funding**: Allocate donations, changes to "Funded" when full
5. **Establishment**: Set date, change to "Established"
6. **Recovery**: Record monthly payments, track progress

## Common Tasks

### Check System Status
```bash
python manage.py check
```

### View Database
```bash
python manage.py dbshell
```

### Create New App (if needed)
```bash
python manage.py startapp app_name
```

### Clear Cache (if needed)
```bash
python manage.py clear_cache
```

## Environment Info
- **Python**: 3.12.7
- **Django**: 5.2.8
- **Database**: SQLite3 (Development)
- **Conda Environment**: `bait`

## Next Steps After Setup

1. **Create Superuser** ✓
2. **Initialize Communities** ✓
3. **Assign Role to Admin User**
   - Login to admin
   - Edit your user
   - Set Role: Director
   - Save
4. **Add Project Categories**
5. **Test Donor Flow**
   - Add a test donor
   - Record a donation
   - Create a project
   - Allocate donation to project
   - Test donor lookup with the 9-digit ID
6. **Customize Content**
   - Add blog posts
   - Create static pages
   - Upload project photos

## Tips & Tricks

### Quick Data Entry
- Use admin inline forms for related data
- Use autocomplete for fast lookups
- Use list_editable for bulk updates

### Reporting
- Use admin filters to generate reports
- Export data using admin actions
- Use date hierarchy for time-based analysis

### Testing
- Always test donor lookup after adding donors
- Verify allocation validation works
- Check role-based access with test users

## Troubleshooting

### Server Won't Start
```bash
# Check for errors
python manage.py check

# Try a different port
python manage.py runserver 8080
```

### Database Issues
```bash
# Re-run migrations
python manage.py migrate

# Check migration status
python manage.py showmigrations
```

### Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic
```

## Support

- **Documentation**: See README.md and SETUP_GUIDE.md
- **Django Docs**: https://docs.djangoproject.com/
- **Admin Guide**: http://localhost:8000/admin/doc/ (when server running)

---

**Ready to make a difference with Bait ul Rizq!** 🌟
