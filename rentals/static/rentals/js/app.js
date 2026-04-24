document.addEventListener('DOMContentLoaded', () => {
    const state = {
        user: null,
        currentSection: 'login'
    };

    // DOM Elements
    const sections = {
        login: document.getElementById('login-section'),
        dashboard: document.getElementById('dashboard-section'),
        properties: document.getElementById('properties-section'),
        tenants: document.getElementById('tenants-section'),
        payments: document.getElementById('payments-section')
    };

    const navLinks = document.getElementById('nav-links');
    const loginForm = document.getElementById('login-form');
    const loginError = document.getElementById('login-error');
    const logoutBtn = document.getElementById('logout-btn');
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const modal = document.getElementById('modal-container');
    const modalBody = document.getElementById('modal-body');
    const closeBtn = document.querySelector('.close-btn');

    // Initialization
    async function init() {
        await API.ensureCsrfToken();
        state.user = await API.getCurrentUser();
        if (state.user) {
            updateUIForRole();
            showSection('dashboard');
            console.log('Logged in as', state.user.username);
        } else {
            showSection('login');
        }
    }

    // Navigation
    function showSection(sectionId) {
        Object.keys(sections).forEach(key => {
            sections[key].classList.add('hidden');
        });
        if (sections[sectionId]) {
            sections[sectionId].classList.remove('hidden');
            state.currentSection = sectionId;

            // Highlight active nav link
            document.querySelectorAll('#nav-links a').forEach(a => {
                if (a.dataset.section === sectionId) {
                    a.style.color = 'var(--secondary-color)';
                } else {
                    a.style.color = 'var(--white)';
                }
            });

            loadSectionData(sectionId);
        }

        // Close mobile menu if open
        navLinks.classList.remove('active');
    }

    function updateUIForRole() {
        const role = state.user.role;
        document.body.classList.remove('role-owner', 'role-tenant', 'role-superuser');
        document.body.classList.add(`role-${role.toLowerCase()}`);

        document.querySelectorAll('.auth-only').forEach(el => el.classList.remove('hidden'));
        document.querySelectorAll('.guest-only').forEach(el => el.classList.add('hidden'));

        const loginLink = document.querySelector('a[data-section="login"]');
        if (loginLink) loginLink.parentElement.classList.add('hidden');

        if (role === 'OWNER' || role === 'SUPERUSER') {
            document.querySelectorAll('.owner-only').forEach(el => el.classList.remove('hidden'));
            document.querySelectorAll('.tenant-only').forEach(el => el.classList.add('hidden'));
        } else {
            document.querySelectorAll('.owner-only').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.tenant-only').forEach(el => el.classList.remove('hidden'));
        }
    }

    async function loadSectionData(sectionId) {
        switch (sectionId) {
            case 'dashboard':
                renderDashboard();
                break;
            case 'properties':
                renderProperties();
                break;
            case 'tenants':
                renderTenants();
                break;
            case 'payments':
                renderPayments();
                break;
        }
    }

    // Section Renderers
    async function renderDashboard() {
        const container = document.getElementById('user-info');
        container.innerHTML = `
            <p>Welcome, <strong>${state.user.username}</strong>!</p>
            <p>Role: ${state.user.role}</p>
        `;

        const statsContainer = document.querySelector('.stats-container');
        // Add some summary stats here if desired
    }

    async function renderProperties() {
        const list = document.getElementById('properties-list');
        list.innerHTML = 'Loading...';
        try {
            const properties = await API.getProperties();
            list.innerHTML = properties.map(p => `
                <div class="card">
                    <h3>${p.title}</h3>
                    <p><strong>Address:</strong> ${p.address}</p>
                    <p>${p.description}</p>
                </div>
            `).join('');
        } catch (e) {
            list.innerHTML = '<p class="error">Failed to load properties.</p>';
        }
    }

    async function renderTenants() {
        const list = document.getElementById('tenants-list');
        list.innerHTML = 'Loading...';
        try {
            const [tenants, agreements] = await Promise.all([API.getTenants(), API.getAgreements()]);
            // Filter out self from tenants list if it's the owner
            const actualTenants = tenants.filter(t => t.id !== state.user.id);

            list.innerHTML = agreements.map(a => `
                <div class="card">
                    <h3>${a.tenant_username}</h3>
                    <p><strong>Property:</strong> ${a.property_title}</p>
                    <p><strong>Rent:</strong> $${a.monthly_rent}</p>
                    <p><strong>Period:</strong> ${a.start_date} to ${a.end_date}</p>
                    <button class="view-payments-btn" data-agreement-id="${a.id}">View Payments</button>
                </div>
            `).join('');

            document.querySelectorAll('.view-payments-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const agreementId = e.target.dataset.agreementId;
                    // For simplicity, we just show the payments section filtered
                    // or we could show a modal. Let's just go to payments.
                    showSection('payments');
                });
            });

        } catch (e) {
            list.innerHTML = '<p class="error">Failed to load tenants.</p>';
        }
    }

    async function renderPayments() {
        const tbody = document.querySelector('#payments-table tbody');
        tbody.innerHTML = '<tr><td colspan="4">Loading...</td></tr>';
        try {
            const payments = await API.getPayments();
            tbody.innerHTML = payments.map(p => `
                <tr>
                    <td>${p.month}</td>
                    <td>$${p.amount}</td>
                    <td>
                        ${p.is_approved ? '<span class="status-approved">Approved</span>' :
                          p.is_paid ? '<span class="status-paid">Paid (Pending Approval)</span>' :
                          '<span class="status-pending">Unpaid</span>'}
                    </td>
                    <td>
                        ${state.user.role === 'TENANT' && !p.is_paid ?
                            `<button class="pay-btn" data-id="${p.id}">Pay Now</button>` : ''}
                        ${(state.user.role === 'OWNER' || state.user.role === 'SUPERUSER') && p.is_paid && !p.is_approved ?
                            `<button class="approve-btn" data-id="${p.id}">Approve</button>` : ''}
                    </td>
                </tr>
            `).join('');

            document.querySelectorAll('.pay-btn').forEach(btn => {
                btn.addEventListener('click', async (e) => {
                    const id = e.target.dataset.id;
                    await API.payRent(id);
                    renderPayments();
                });
            });

            document.querySelectorAll('.approve-btn').forEach(btn => {
                btn.addEventListener('click', async (e) => {
                    const id = e.target.dataset.id;
                    await API.approvePayment(id);
                    renderPayments();
                });
            });

        } catch (e) {
            tbody.innerHTML = '<tr><td colspan="4" class="error">Failed to load payments.</td></tr>';
        }
    }

    // Event Listeners
    navLinks.addEventListener('click', (e) => {
        if (e.target.tagName === 'A' && e.target.dataset.section) {
            e.preventDefault();
            showSection(e.target.dataset.section);
        }
    });

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = loginForm.username.value;
        const password = loginForm.password.value;
        try {
            await API.login(username, password);
            state.user = await API.getCurrentUser();
            updateUIForRole();
            showSection('dashboard');
        } catch (err) {
            loginError.textContent = 'Invalid username or password.';
        }
    });

    logoutBtn.addEventListener('click', (e) => {
        e.preventDefault();
        API.logout();
    });

    mobileMenuBtn.addEventListener('click', () => {
        navLinks.classList.toggle('active');
    });

    // Modals
    function showModal(contentHtml) {
        modalBody.innerHTML = contentHtml;
        modal.classList.remove('hidden');
    }

    closeBtn.addEventListener('click', () => {
        modal.classList.add('hidden');
    });

    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.add('hidden');
        }
    });

    // Handle "Add Property"
    document.getElementById('add-property-btn').addEventListener('click', () => {
        showModal(`
            <h3>Add New Property</h3>
            <form id="add-property-form">
                <div class="form-group">
                    <label>Title</label>
                    <input type="text" name="title" required>
                </div>
                <div class="form-group">
                    <label>Address</label>
                    <input type="text" name="address" required>
                </div>
                <div class="form-group">
                    <label>Description</label>
                    <textarea name="description"></textarea>
                </div>
                <button type="submit">Save Property</button>
            </form>
        `);

        document.getElementById('add-property-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData.entries());
            await API.createProperty(data);
            modal.classList.add('hidden');
            renderProperties();
        });
    });

    // Handle "Add Tenant"
    document.getElementById('add-tenant-btn').addEventListener('click', async () => {
        const properties = await API.getProperties();
        showModal(`
            <h3>Add New Tenant & Agreement</h3>
            <form id="add-tenant-form">
                <h4>Tenant Account</h4>
                <div class="form-group">
                    <label>Username</label>
                    <input type="text" name="username" required>
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" name="password" required>
                </div>
                <hr>
                <h4>Rental Agreement</h4>
                <div class="form-group">
                    <label>Property</label>
                    <select name="property" required>
                        ${properties.map(p => `<option value="${p.id}">${p.title}</option>`).join('')}
                    </select>
                </div>
                <div class="form-group">
                    <label>Monthly Rent</label>
                    <input type="number" name="monthly_rent" required>
                </div>
                <div class="form-group">
                    <label>Start Date</label>
                    <input type="date" name="start_date" required>
                </div>
                <div class="form-group">
                    <label>End Date</label>
                    <input type="date" name="end_date" required>
                </div>
                <button type="submit">Create Tenant & Agreement</button>
            </form>
        `);

        document.getElementById('add-tenant-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const rawData = Object.fromEntries(formData.entries());

            try {
                // 1. Create Tenant User
                const tenant = await API.createTenant({
                    username: rawData.username,
                    password: rawData.password,
                    role: 'TENANT'
                });

                // 2. Create Agreement
                await API.createAgreement({
                    property: rawData.property,
                    tenant: tenant.id,
                    monthly_rent: rawData.monthly_rent,
                    start_date: rawData.start_date,
                    end_date: rawData.end_date
                });

                modal.classList.add('hidden');
                renderTenants();
            } catch (err) {
                alert('Error creating tenant/agreement: ' + JSON.stringify(err.data || err.message));
            }
        });
    });

    init();
});
