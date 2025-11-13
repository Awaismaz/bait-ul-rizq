# Bait ul Rizq - Charity Management System

A comprehensive Django-based charity management system for "Bait ul Rizq" that helps manage donations, projects, and beneficiaries with transparency and accountability.

## Overview

Bait ul Rizq is a non-profit organization that collects donations to fund small businesses for needy people (like roadside food shops). Once beneficiaries are established, they contribute back to the system, making it self-sustaining.

## Key Features

### 1. **Multi-Community Support**
- **International Community**: Managed by International Manager
- **Pakistani Community**: Managed by Pakistani Manager
- **Director**: Has full visibility across both communities
- Complete data segregation between communities

### 2. **Donor Management**
- Anonymous 9-digit donor ID for privacy
- Donors can track donations without authentication
- Anonymous donation option
- Full donation history and project allocation tracking

### 3. **Project/Beneficiary Management**
- Complete workflow: Pending → Approved → Funded → Established → Recovering
- Detailed beneficiary information and verification
- Business plan tracking
- Financial tracking (requested, approved, funded amounts)
- Recovery tracking for sustainability
- Project updates and progress photos

### 4. **Donation Tracking**
- Many-to-many relationships:
  - Multiple donations can fund one project
  - One donation can be split across multiple projects
- Transparent allocation system
- Remaining amount tracking
- Validation to prevent over-allocation

### 5. **Recovery System**
- Monthly recovery tracking from established businesses
- Progress monitoring
- Contribution back to the fund

### 6. **Role-Based Access Control**
- **Director**: Full system access
- **International Manager**: International community only
- **Pakistani Manager**: Pakistani community only
- **Staff**: Basic data entry

### 7. **Bilingual Support**
- English and Urdu (اردو)
- All content fields support both languages
- Language switcher in frontend

### 8. **Blog System**
- Success stories
- Updates and announcements
- Categorized posts
- Featured posts for homepage

### 9. **Public Website**
- Homepage with featured projects
- Donor lookup portal (by 9-digit ID)
- Project listings
- Blog
- Static pages (About, Policies, etc.)
- Beneficiary application form
- Volunteer application form

## Project Structure

```
bait_ul_rizq/
├── config/              # Project settings
├── core/                # Core models (Users, Donors, Communities, Volunteers)
├── donations/           # Donation and allocation management
├── projects/            # Projects, beneficiaries, recoveries
├── blog/                # Blog system
├── pages/               # Static pages
├── templates/           # HTML templates
├── static/              # CSS, JS, images
├── media/               # Uploaded files
└── locale/              # Translation files
```

## Database Models

### Core App
- **Community**: International/Pakistani
- **CustomUser**: Extended user with roles
- **Donor**: Donor information with 9-digit ID
- **Volunteer**: Volunteer applications

### Donations App
- **Donation**: Donation records
- **DonationAllocation**: Links donations to projects (many-to-many)

### Projects App
- **ProjectCategory**: Business categories
- **Project**: Beneficiary projects/businesses
- **ProjectUpdate**: Progress updates
- **Recovery**: Monthly recoveries

### Blog App
- **BlogCategory**: Blog categories
- **BlogPost**: Blog posts with bilingual support

### Pages App
- **Page**: Static content pages

## Installation & Setup

### 1. Prerequisites
- Python 3.12.7
- Conda environment manager

### 2. Environment Setup
```bash
# Activate the bait conda environment
conda activate bait

# Install dependencies
pip install django pillow django-crispy-forms crispy-bootstrap5 django-ckeditor
```

### 3. Database Setup
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Create communities
python manage.py shell
```

```python
from core.models import Community
Community.objects.create(name="International Community", community_type="INTL", description="International donors and projects")
Community.objects.create(name="Pakistani Community", community_type="PAK", description="Pakistani donors and projects")
```

### 4. Run Development Server
```bash
python manage.py runserver
```

Access:
- Admin: http://localhost:8000/admin/
- Website: http://localhost:8000/

## Admin Features

### Dashboard
- Comprehensive overview of all activities
- Role-based data filtering
- Quick actions for common tasks

### Donor Management
- Add donors with auto-generated 9-digit ID
- Track total donations
- Privacy settings (anonymous option)
- Community assignment

### Donation Management
- Record donations with payment details
- Inline allocation to projects
- Validation prevents over-allocation
- Receipt tracking

### Project Management
- Complete beneficiary information
- Status workflow management
- Financial tracking with progress bars
- Inline updates and recoveries
- Document uploads

### Reports & Analytics
- Total donations by community
- Active projects count
- Recovery statistics
- Donor statistics

## User Workflows

### For Donors
1. Donate through organization
2. Receive 9-digit donor ID
3. Visit website → Donor Lookup
4. Enter 9-digit ID
5. View donation history and project allocations
6. See which projects benefited from their contributions

### For Beneficiaries
1. Submit application through website form
2. Team verifies and approves
3. Gets funded from donations
4. Establishes business
5. Starts monthly contributions back to system

### For Administrators
1. Receive beneficiary applications
2. Verify and approve worthy cases
3. Record donations as they come in
4. Allocate donations to approved projects
5. Track project progress
6. Record monthly recoveries
7. Generate reports

## Privacy & Security
- Donor data protected
- 9-digit ID system prevents unauthorized access
- No authentication required for donors to view own data
- Role-based access control in admin
- Community data segregation

## Future Enhancements
- SMS notifications for donors
- Email receipts
- Advanced analytics dashboard
- Mobile app
- Payment gateway integration
- Automated recovery reminders
- PDF report generation

## Technologies Used
- **Backend**: Django 5.2.8
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Frontend**: Bootstrap 5, Chart.js
- **Rich Text**: CKEditor
- **Internationalization**: Django i18n

## Support & Contact
For issues or questions, please contact the Bait ul Rizq team.

## License
This is a non-profit project for Bait ul Rizq organization.

---

**Note**: This system has been designed with transparency, accountability, and ease-of-use as core principles to help Bait ul Rizq achieve its mission of sustainable poverty alleviation.
