const API = {
    baseUrl: '/api',

    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCookie('csrftoken')
            }
        };

        const mergedOptions = { ...defaultOptions, ...options };
        if (mergedOptions.headers && options.headers) {
            mergedOptions.headers = { ...defaultOptions.headers, ...options.headers };
        }

        const response = await fetch(url, mergedOptions);

        if (response.status === 204) return null;

        const data = await response.json();

        if (!response.ok) {
            throw { status: response.status, data };
        }

        return data;
    },

    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },

    async ensureCsrfToken() {
        // Just make a request to the root or any endpoint to ensure we have the CSRF cookie
        await fetch('/');
    },

    // Auth
    async login(username, password) {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        formData.append('csrfmiddlewaretoken', this.getCookie('csrftoken'));

        const response = await fetch('/api-auth/login/', {
            method: 'POST',
            body: formData,
            headers: {
                // If we don't have a CSRF token yet, we might need to get it first
                // but the cookie should be there after the first GET /
                'X-CSRFToken': this.getCookie('csrftoken')
            },
            redirect: 'manual' // Prevent following redirect
        });

        if (response.ok || response.status === 400 || response.status === 0 || response.status === 302) {
            // DRF login might redirect (302) or return 400 if it's already logged in or has issues.
            // redirect: 'manual' might result in status 0 or 302
            return true;
        } else {
            throw new Error('Login failed');
        }
    },

    async logout() {
        const formData = new FormData();
        formData.append('csrfmiddlewaretoken', this.getCookie('csrftoken'));
        await fetch('/api-auth/logout/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': this.getCookie('csrftoken')
            }
        });
        window.location.reload();
    },

    async getCurrentUser() {
        try {
            const users = await this.request('/users/');
            // If authenticated, /users/ returns at least the current user
            return users.length > 0 ? users[0] : null;
        } catch (e) {
            return null;
        }
    },

    // Resources
    getProperties() { return this.request('/properties/'); },
    createProperty(data) { return this.request('/properties/', { method: 'POST', body: JSON.stringify(data) }); },

    getTenants() { return this.request('/users/'); }, // Owner sees tenants they have agreements with
    createTenant(data) { return this.request('/users/', { method: 'POST', body: JSON.stringify(data) }); },

    getAgreements() { return this.request('/agreements/'); },
    createAgreement(data) { return this.request('/agreements/', { method: 'POST', body: JSON.stringify(data) }); },

    getPayments() { return this.request('/payments/'); },
    payRent(paymentId, paymentDetails) {
        return this.request(`/payments/${paymentId}/pay/`, {
            method: 'POST',
            body: JSON.stringify({ payment_details: paymentDetails })
        });
    },
    approvePayment(paymentId) { return this.request(`/payments/${paymentId}/approve/`, { method: 'POST' }); }
};
