#!/usr/bin/env python
"""
Script to create all remaining template files for Bait ul Rizq
Run with: python create_remaining_templates.py
"""

import os

# Define all template contents
TEMPLATES = {
    "templates/projects/project_detail.html": '''{% extends 'base.html' %}
{% load static %}
{% load i18n %}

{% block title %}{{ project.title }} - Bait ul Rizq{% endblock %}

{% block content %}
<section class="py-5">
    <div class="container">
        <div class="row">
            <div class="col-lg-8">
                {% if project.image %}
                <img src="{{ project.image.url }}" class="img-fluid rounded-4 shadow-lg mb-4" alt="{{ project.title }}">
                {% else %}
                <img src="https://images.unsplash.com/photo-1556740758-90de374c12ad?w=800" class="img-fluid rounded-4 shadow-lg mb-4" alt="{{ project.title }}">
                {% endif %}

                <div class="mb-4">
                    <span class="badge bg-primary me-2">{{ project.get_status_display }}</span>
                    {% if project.category %}
                    <span class="badge bg-secondary">{{ project.category }}</span>
                    {% endif %}
                </div>

                <h1 class="display-5 fw-bold mb-3">{{ project.title }}</h1>
                <p class="lead text-muted mb-4">{{ project.description }}</p>

                <div class="card border-0 bg-light mb-4">
                    <div class="card-body">
                        <h5 class="fw-bold mb-3"><i class="bi bi-person-circle"></i> {% trans "Beneficiary Information" %}</h5>
                        <div class="row">
                            <div class="col-md-6 mb-2">
                                <strong>{% trans "Name" %}:</strong> {{ project.beneficiary_name }}
                            </div>
                            <div class="col-md-6 mb-2">
                                <strong>{% trans "Family Size" %}:</strong> {{ project.family_size }}
                            </div>
                        </div>
                    </div>
                </div>

                {% if project.business_plan %}
                <div class="mb-4">
                    <h5 class="fw-bold mb-3">{% trans "Business Plan" %}</h5>
                    <p>{{ project.business_plan }}</p>
                </div>
                {% endif %}
            </div>

            <div class="col-lg-4">
                <div class="card border-0 shadow-lg sticky-top" style="top: 100px;">
                    <div class="card-body p-4">
                        <h5 class="fw-bold mb-4">{% trans "Funding Progress" %}</h5>

                        <div class="text-center mb-4">
                            <h2 class="display-4 fw-bold text-primary">{{ project.funding_progress }}%</h2>
                            <div class="progress mb-2" style="height: 20px;">
                                <div class="progress-bar bg-success" style="width: {{ project.funding_progress }}%"></div>
                            </div>
                        </div>

                        <div class="mb-3">
                            <div class="d-flex justify-content-between mb-2">
                                <span class="text-muted">{% trans "Raised" %}</span>
                                <strong class="text-success">{{ project.currency }} {{ project.total_funded }}</strong>
                            </div>
                            <div class="d-flex justify-content-between mb-2">
                                <span class="text-muted">{% trans "Goal" %}</span>
                                <strong>{{ project.currency }} {{ project.approved_amount|default:project.requested_amount }}</strong>
                            </div>
                            <div class="d-flex justify-content-between">
                                <span class="text-muted">{% trans "Donors" %}</span>
                                <strong>{{ project.donor_count }}</strong>
                            </div>
                        </div>

                        <hr>

                        <div class="d-grid">
                            <a href="{% url 'core:home' %}" class="btn btn-primary btn-lg mb-2">
                                <i class="bi bi-heart-fill"></i> {% trans "Support This Project" %}
                            </a>
                            <a href="{% url 'projects:project_list' %}" class="btn btn-outline-secondary">
                                <i class="bi bi-arrow-left"></i> {% trans "Back to Projects" %}
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
{% endblock %}''',

    "templates/projects/project_application.html": '''{% extends 'base.html' %}
{% load static %}
{% load i18n %}
{% load crispy_forms_tags %}

{% block title %}{% trans "Apply for Help" %} - Bait ul Rizq{% endblock %}

{% block content %}
<section class="py-5">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8">
                <div class="text-center mb-5">
                    <h1 class="display-5 fw-bold mb-3">{% trans "Apply for Business Support" %}</h1>
                    <p class="lead text-muted">
                        {% trans "Fill out this form to apply for help in starting your small business" %}
                    </p>
                </div>

                <div class="card border-0 shadow-lg">
                    <div class="card-body p-5">
                        <form method="post" enctype="multipart/form-data">
                            {% csrf_token %}
                            {{ form.as_p }}
                            <button type="submit" class="btn btn-primary btn-lg w-100 mt-3">
                                <i class="bi bi-send"></i> {% trans "Submit Application" %}
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
{% endblock %}''',

    "templates/projects/application_success.html": '''{% extends 'base.html' %}
{% load static %}
{% load i18n %}

{% block title %}{% trans "Application Submitted" %} - Bait ul Rizq{% endblock %}

{% block content %}
<section class="py-5">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-6 text-center">
                <i class="bi bi-check-circle-fill text-success display-1 mb-4"></i>
                <h1 class="display-4 fw-bold mb-3">{% trans "Application Submitted!" %}</h1>
                <p class="lead mb-4">
                    {% trans "Thank you for submitting your application. Our team will review it and contact you soon." %}
                </p>
                <a href="{% url 'core:home' %}" class="btn btn-primary btn-lg">
                    <i class="bi bi-house"></i> {% trans "Return to Homepage" %}
                </a>
            </div>
        </div>
    </div>
</section>
{% endblock %}''',

    "templates/core/volunteer_application.html": '''{% extends 'base.html' %}
{% load static %}
{% load i18n %}

{% block title %}{% trans "Become a Volunteer" %} - Bait ul Rizq{% endblock %}

{% block content %}
<section class="py-5">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8">
                <div class="text-center mb-5">
                    <h1 class="display-5 fw-bold mb-3">{% trans "Join Our Team" %}</h1>
                    <p class="lead text-muted">
                        {% trans "Help us make a difference in people's lives" %}
                    </p>
                </div>

                <div class="card border-0 shadow-lg">
                    <div class="card-body p-5">
                        <form method="post">
                            {% csrf_token %}
                            {{ form.as_p }}
                            <button type="submit" class="btn btn-primary btn-lg w-100 mt-3">
                                <i class="bi bi-send"></i> {% trans "Submit Application" %}
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
{% endblock %}''',

    "templates/core/volunteer_success.html": '''{% extends 'base.html' %}
{% load static %}
{% load i18n %}

{% block title %}{% trans "Thank You" %} - Bait ul Rizq{% endblock %}

{% block content %}
<section class="py-5">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-6 text-center">
                <i class="bi bi-heart-fill text-danger display-1 mb-4"></i>
                <h1 class="display-4 fw-bold mb-3">{% trans "Thank You!" %}</h1>
                <p class="lead mb-4">
                    {% trans "Your volunteer application has been received. We'll contact you soon!" %}
                </p>
                <a href="{% url 'core:home' %}" class="btn btn-primary btn-lg">
                    <i class="bi bi-house"></i> {% trans "Return to Homepage" %}
                </a>
            </div>
        </div>
    </div>
</section>
{% endblock %}''',

    "templates/blog/blog_list.html": '''{% extends 'base.html' %}
{% load static %}
{% load i18n %}

{% block title %}{% trans "Blog" %} - Bait ul Rizq{% endblock %}

{% block content %}
<section class="hero-section py-5">
    <div class="container text-center">
        <h1 class="display-4 fw-bold mb-3">{% trans "Our Blog" %}</h1>
        <p class="lead">{% trans "Success stories, updates, and news from our community" %}</p>
    </div>
</section>

<section class="py-5">
    <div class="container">
        <div class="row g-4">
            {% for post in posts %}
            <div class="col-md-6 col-lg-4">
                <div class="card h-100 border-0 shadow-sm">
                    {% if post.featured_image %}
                    <img src="{{ post.featured_image.url }}" class="card-img-top" alt="{{ post.title }}">
                    {% else %}
                    <img src="https://images.unsplash.com/photo-1532629345422-7515f3d16bb6?w=400" class="card-img-top" alt="{{ post.title }}">
                    {% endif %}
                    <div class="card-body">
                        <div class="mb-2">
                            {% if post.category %}
                            <span class="badge bg-info">{{ post.category }}</span>
                            {% endif %}
                            <small class="text-muted ms-2">
                                <i class="bi bi-calendar3"></i> {{ post.published_date|date:"M d, Y" }}
                            </small>
                        </div>
                        <h5 class="card-title fw-bold">{{ post.title }}</h5>
                        <p class="card-text text-muted">{{ post.excerpt|truncatewords:20 }}</p>
                        <a href="{% url 'blog:blog_detail' post.slug %}" class="btn btn-outline-primary">
                            {% trans "Read More" %} <i class="bi bi-arrow-right"></i>
                        </a>
                    </div>
                </div>
            </div>
            {% empty %}
            <div class="col-12">
                <div class="alert alert-info text-center">
                    <i class="bi bi-info-circle fs-1 d-block mb-3"></i>
                    <h4>{% trans "No blog posts yet" %}</h4>
                    <p class="mb-0">{% trans "Check back soon for updates!" %}</p>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</section>
{% endblock %}''',

    "templates/blog/blog_detail.html": '''{% extends 'base.html' %}
{% load static %}
{% load i18n %}

{% block title %}{{ post.title }} - Bait ul Rizq{% endblock %}

{% block content %}
<section class="py-5">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8">
                {% if post.featured_image %}
                <img src="{{ post.featured_image.url }}" class="img-fluid rounded-4 shadow-lg mb-4" alt="{{ post.title }}">
                {% endif %}

                <div class="mb-4">
                    {% if post.category %}
                    <span class="badge bg-info me-2">{{ post.category }}</span>
                    {% endif %}
                    <span class="text-muted">
                        <i class="bi bi-calendar3"></i> {{ post.published_date|date:"F d, Y" }}
                    </span>
                    <span class="text-muted ms-3">
                        <i class="bi bi-eye"></i> {{ post.views_count }} views
                    </span>
                </div>

                <h1 class="display-4 fw-bold mb-4">{{ post.title }}</h1>

                <div class="blog-content">
                    {{ post.content|safe }}
                </div>

                <hr class="my-5">

                <div class="text-center">
                    <a href="{% url 'blog:blog_list' %}" class="btn btn-outline-primary">
                        <i class="bi bi-arrow-left"></i> {% trans "Back to Blog" %}
                    </a>
                </div>
            </div>
        </div>
    </div>
</section>
{% endblock %}''',

    "templates/pages/page_detail.html": '''{% extends 'base.html' %}
{% load static %}
{% load i18n %}

{% block title %}{{ page.title }} - Bait ul Rizq{% endblock %}

{% block content %}
<section class="py-5">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8">
                <h1 class="display-4 fw-bold mb-4">{{ page.title }}</h1>
                <div class="page-content">
                    {{ page.content|safe }}
                </div>
            </div>
        </div>
    </div>
</section>
{% endblock %}''',
}

def create_templates():
    """Create all template files"""
    base_dir = os.path.dirname(os.path.abspath(__file__))

    for path, content in TEMPLATES.items():
        full_path = os.path.join(base_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✓ Created: {path}")

    print(f"\n✅ Successfully created {len(TEMPLATES)} template files!")

if __name__ == "__main__":
    create_templates()
