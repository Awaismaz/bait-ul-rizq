# Bait ul Rizq - Complete Setup Guide

## Quick Start Guide

### Step 1: Database Setup (Already Done ✓)
The database has been migrated and is ready to use.

### Step 2: Create Initial Data

#### A. Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```
Enter:
- Username: `admin`
- Email: `admin@baitulrizq.org`
- Password: (choose a strong password)

#### B. Create Communities
Run Python shell:
```bash
python manage.py shell
```

Then execute:
```python
from core.models import Community

# Create International Community
Community.objects.get_or_create(
    community_type='INTL',
    defaults={
        'name': 'International Community',
        'description': 'For international donors and projects',
        'is_active': True
    }
)

# Create Pakistani Community
Community.objects.get_or_create(
    community_type='PAK',
    defaults={
        'name': 'Pakistani Community',
        'description': 'For Pakistani donors and projects',
        'is_active': True
    }
)

# Verify
print(f"Communities created: {Community.objects.count()}")
for c in Community.objects.all():
    print(f"  - {c.name} ({c.community_type})")

exit()
```

### Step 3: Access the Admin Panel

1. Start the server:
```bash
python manage.py runserver
```

2. Open browser and go to: `http://localhost:8000/admin/`

3. Login with your superuser credentials

### Step 4: Configure Your Admin User

1. In admin, go to "Users" → Click on your username
2. Scroll to "Bait ul Rizq Information" section
3. Set:
   - **Role**: Director
   - **Community**: (leave blank for Director - they see all)
4. Save

## Complete System Walkthrough

### For Administrators

#### 1. Adding Project Categories
1. Go to Admin → Project Categories → Add
2. Examples:
   - Food Cart (ٹھیلا)
   - Small Shop (چھوٹی دکان)
   - Tailoring (سلائی)
   - etc.

#### 2. Adding a Donor
1. Go to Admin → Donors → Add Donor
2. Fill in:
   - Name
   - Email/Phone (optional)
   - Community (International or Pakistani)
   - Privacy settings
3. Save
4. **IMPORTANT**: Copy the auto-generated 9-digit Donor ID and provide it to the donor!

#### 3. Recording a Donation
1. Go to Admin → Donations → Add Donation
2. Select the donor
3. Enter amount, currency, payment method
4. Set date received
5. Save

#### 4. Creating/Approving a Project
1. Go to Admin → Projects → Add Project (or approve existing application)
2. Fill in all beneficiary details
3. Set status to "Approved - Awaiting Funding"
4. Set approved amount
5. Save

#### 5. Allocating Donations to Projects
1. Go to Admin → Donations → Click on a donation
2. Scroll to "Donation allocations" section at bottom
3. Click "Add another Donation allocation"
4. Select project and enter amount
5. Save

**Note**: The system prevents over-allocation. You can't allocate more than the donation amount!

#### 6. Recording Project Progress
1. Open a Project in admin
2. Scroll to "Project updates" section
3. Add updates with photos
4. Change project status as it progresses:
   - Pending Approval
   - Approved - Awaiting Funding
   - Funded - In Progress
   - Established - Operating
   - Recovering Contributions

#### 7. Recording Recoveries
1. Open an Established project
2. Scroll to "Recoveries" section
3. Add recovery records
4. The system automatically updates total recovered amount

### For Donors (Public Website)

#### Checking Donations
1. Go to website homepage
2. Click "Track My Donations" or go to `/donor-lookup/`
3. Enter your 9-digit Donor ID
4. View:
   - All your donations
   - Which projects they funded
   - Project progress

**Privacy**: Only the person with the 9-digit ID can view the donations. No authentication required!

### For Beneficiaries (Public Website)

#### Applying for Help
1. Go to `/projects/apply/`
2. Fill in the application form:
   - Personal information
   - Family details
   - Business idea
   - Amount needed
3. Submit
4. Team will verify and contact you

### For Volunteers

#### Applying to Join
1. Go to `/volunteer-application/`
2. Fill in details
3. Submit
4. Admin will review and approve

## Role-Based Access

### Director
- Sees ALL data from both communities
- Full access to everything
- Can manage users and assign roles

### International Manager
- Sees ONLY International community data
- Cannot see Pakistani data
- Can manage donors, donations, projects in their community

### Pakistani Manager
- Sees ONLY Pakistani community data
- Cannot see International data
- Can manage donors, donations, projects in their community

### Staff
- Basic data entry
- Limited permissions

## Key Features Explained

### 1. Anonymous Donor Tracking
- Each donor gets a unique 9-digit ID
- No login required to view donations
- Privacy-friendly: Only ID holder can view data
- Perfect for transparency without authentication hassle

### 2. Many-to-Many Donation Allocation
- One donation can fund multiple projects
- One project can receive from multiple donations
- Complete transparency for donors
- Validation prevents mistakes

### 3. Self-Sustaining System
- Projects start contributing back after establishment
- Recovery tracking ensures sustainability
- Progress monitoring
- Financial accountability

### 4. Bilingual System
- All public content in English & Urdu
- Easy language switching
- Accessibility for all users

## Admin Dashboard Features

### List Views
- **Filtering**: Filter by status, community, dates, etc.
- **Search**: Quick search across multiple fields
- **Sorting**: Click column headers to sort
- **Bulk Actions**: Select multiple items for bulk operations

### Detail Views
- **Inline Editing**: Edit related items without leaving the page
- **Read-only Fields**: Important fields protected from accidental changes
- **Fieldsets**: Organized into collapsible sections
- **Validation**: Automatic validation prevents errors

### Special Features
- **Autocomplete**: Fast lookup for donors, projects
- **Date Hierarchy**: Filter by year/month/day
- **Progress Bars**: Visual funding progress
- **Colored Status**: Easy-to-see project status

## Best Practices

### For Data Entry
1. Always assign correct community to donors/projects
2. Double-check donor IDs before sharing with donors
3. Keep beneficiary information complete and accurate
4. Update project status regularly
5. Add project updates with photos

### For Transparency
1. Mark featured projects for homepage visibility
2. Write clear project descriptions
3. Post regular blog updates
4. Keep recovery records up-to-date

### For Privacy
1. Use "Anonymous Donor" flag when requested
2. Never share donor IDs publicly
3. Protect beneficiary personal information
4. Only share success stories with permission

## Troubleshooting

### Can't See Data in Admin
- Check your role and assigned community
- Only Director sees all data
- Managers only see their community

### Allocation Won't Save
- Check if you're exceeding donation amount
- Verify both donation and project are in same currency
- Ensure project is approved

### Donor ID Not Working
- Verify the 9-digit ID is correct
- Check if donor exists in system
- No spaces or special characters

## Next Steps

1. ✅ Setup complete
2. Add sample data (donors, projects)
3. Test donor lookup feature
4. Customize homepage content
5. Add blog posts
6. Create static pages (About, Contact, etc.)
7. Launch!

## Support

For technical issues or questions:
- Check Django admin logs
- Review this documentation
- Contact system administrator

---

**System developed for Bait ul Rizq - Empowering Communities Through Sustainable Charity**
