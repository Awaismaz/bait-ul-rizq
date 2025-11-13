#!/usr/bin/env python
"""Create remaining critical templates"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Donate template with payment methods
DONATE_TEMPLATE = '''{% extends 'base.html' %}
{% load static %}
{% load i18n %}

{% block title %}{% trans "Donate Now" %} - Bait ul Rizq{% endblock %}

{% block content %}
<section class="bg-gradient py-5" style="background: linear-gradient(135deg, #2c5282 0%, #1e4d7b 100%); color: white;">
    <div class="container text-center">
        <h1 class="display-3 fw-bold mb-3">{% trans "Let Me Serve Allah" %}</h1>
        <p class="display-6 mb-4 urdu-text">مجھے اللہ کی خدمت کرنے دیں</p>
        <p class="lead">{% trans "Your donation helps needy families establish sustainable businesses" %}</p>
    </div>
</section>

<section class="py-5">
    <div class="container">
        <div class="row">
            <div class="col-lg-8">
                <div class="card border-0 shadow-lg">
                    <div class="card-body p-5">
                        <h3 class="fw-bold mb-4">{% trans "Make Your Donation" %}</h3>
                        <form method="post">
                            {% csrf_token %}
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label fw-bold">{% trans "Full Name" %} *</label>
                                    <input type="text" class="form-control" name="name" required>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label fw-bold">{% trans "Email" %} *</label>
                                    <input type="email" class="form-control" name="email" required>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label fw-bold">{% trans "Phone" %} *</label>
                                    <input type="tel" class="form-control" name="phone" required>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label fw-bold">{% trans "Community" %} *</label>
                                    <select class="form-select" name="community" required>
                                        <option value="1">{% trans "International" %}</option>
                                        <option value="2">{% trans "Pakistani" %}</option>
                                    </select>
                                </div>
                                <div class="col-12 mb-3">
                                    <label class="form-label fw-bold">{% trans "Address" %}</label>
                                    <textarea class="form-control" name="address" rows="2"></textarea>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label fw-bold">{% trans "Amount" %} *</label>
                                    <input type="number" class="form-control" name="amount" min="1" step="0.01" required>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label fw-bold">{% trans "Currency" %} *</label>
                                    <select class="form-select" name="currency" required>
                                        <option value="USD">USD</option>
                                        <option value="PKR">PKR</option>
                                        <option value="EUR">EUR</option>
                                        <option value="GBP">GBP</option>
                                    </select>
                                </div>
                                <div class="col-12 mb-3">
                                    <label class="form-label fw-bold">{% trans "Payment Method" %} *</label>
                                    <select class="form-select" name="payment_method" id="paymentMethod" required>
                                        <option value="MOBILE">JazzCash / EasyPaisa</option>
                                        <option value="BANK">Bank Transfer (UBL/Askari)</option>
                                        <option value="CARD">Credit/Debit Card</option>
                                        <option value="CASH">Cash</option>
                                    </select>
                                </div>
                            </div>

                            <div id="paymentInstructions" class="alert alert-info mt-3" style="display: none;">
                                <h6 class="fw-bold">{% trans "Payment Instructions" %}:</h6>
                                <div id="mobilePayment" style="display: none;">
                                    <p><strong>JazzCash:</strong> 0300-XXXXXXX</p>
                                    <p><strong>EasyPaisa:</strong> 0321-XXXXXXX</p>
                                </div>
                                <div id="bankPayment" style="display: none;">
                                    <p><strong>UBL:</strong> PK00XXXXXXXXXXXXXXXXXXXX</p>
                                    <p><strong>Askari:</strong> PK00XXXXXXXXXXXXXXXXXXXX</p>
                                </div>
                            </div>

                            <div class="form-check mb-4">
                                <input class="form-check-input" type="checkbox" name="is_anonymous">
                                <label class="form-check-label">{% trans "Anonymous donation" %}</label>
                            </div>

                            <button type="submit" class="btn btn-primary btn-lg w-100">
                                <i class="bi bi-heart-fill"></i> {% trans "Complete Donation" %}
                            </button>
                        </form>
                    </div>
                </div>
            </div>

            <div class="col-lg-4">
                <div class="card border-0 bg-light">
                    <div class="card-body p-4">
                        <h5 class="fw-bold mb-3">{% trans "Why Donate?" %}</h5>
                        <ul class="list-unstyled">
                            <li class="mb-2"><i class="bi bi-check-circle-fill text-success me-2"></i> {% trans "100%% to beneficiaries" %}</li>
                            <li class="mb-2"><i class="bi bi-check-circle-fill text-success me-2"></i> {% trans "Verified projects" %}</li>
                            <li class="mb-2"><i class="bi bi-check-circle-fill text-success me-2"></i> {% trans "Track your impact" %}</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<script>
document.getElementById('paymentMethod').addEventListener('change', function() {
    const instructions = document.getElementById('paymentInstructions');
    const mobile = document.getElementById('mobilePayment');
    const bank = document.getElementById('bankPayment');
    mobile.style.display = 'none';
    bank.style.display = 'none';
    if (this.value === 'MOBILE') {
        instructions.style.display = 'block';
        mobile.style.display = 'block';
    } else if (this.value === 'BANK') {
        instructions.style.display = 'block';
        bank.style.display = 'block';
    } else {
        instructions.style.display = 'none';
    }
});
</script>
{% endblock %}
'''

DONATE_SUCCESS_TEMPLATE = '''{% extends 'base.html' %}
{% load static %}
{% load i18n %}

{% block title %}{% trans "Thank You" %} - Bait ul Rizq{% endblock %}

{% block content %}
<section class="py-5">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-6 text-center">
                <i class="bi bi-check-circle-fill text-success display-1 mb-4"></i>
                <h1 class="display-4 fw-bold mb-3">{% trans "Jazak Allah Khair!" %}</h1>
                <p class="lead mb-4">{% trans "Thank you for your generous donation!" %}</p>

                <div class="card border-0 shadow-lg mb-4">
                    <div class="card-body p-5">
                        <h5 class="fw-bold mb-3">{% trans "Your Unique Donor ID" %}</h5>
                        <div class="bg-light p-4 rounded-3 mb-3">
                            <h2 class="display-5 font-monospace fw-bold text-primary">{{ donor_id }}</h2>
                        </div>
                        <p class="text-muted mb-3">{% trans "Save this ID to track your donations" %}</p>
                        <p class="fw-bold">{% trans "Amount Donated" %}: {{ donation_currency }} {{ donation_amount }}</p>
                    </div>
                </div>

                <div class="d-grid gap-2">
                    <a href="{% url 'core:donor_detail' donor_id %}" class="btn btn-primary btn-lg">
                        <i class="bi bi-eye"></i> {% trans "View My Donations" %}
                    </a>
                    <a href="{% url 'core:home' %}" class="btn btn-outline-secondary">
                        <i class="bi bi-house"></i> {% trans "Return to Homepage" %}
                    </a>
                </div>
            </div>
        </div>
    </div>
</section>
{% endblock %}
'''

# Write templates
templates = {
    'templates/core/donate.html': DONATE_TEMPLATE,
    'templates/core/donate_success.html': DONATE_SUCCESS_TEMPLATE,
}

for path, content in templates.items():
    full_path = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {path}")

print(f"\\nCreated {len(templates)} templates!")
