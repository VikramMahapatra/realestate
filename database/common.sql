--Auth
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL, -- admin, broker, tenant, resident, etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT UNIQUE NOT NULL, -- e.g. broker, security, maintenance
    description TEXT
);

CREATE TABLE permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role_id UUID REFERENCES roles(id),
    service_name TEXT NOT NULL,
    permission TEXT NOT NULL, -- e.g. SELL, RENT, LEASE, MANAGE_GATE_PASS
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Properties
CREATE TABLE properties (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_name TEXT NOT NULL,
    address TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    status TEXT, -- Available, Sold, Leased, Rented
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE flats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id UUID NOT NULL,
    unit_number TEXT NOT NULL,
    floor INTEGER,
    area_sqft NUMERIC(10,2),
    bedrooms INTEGER,
    bathrooms INTEGER,
    price NUMERIC(15,2),
    status TEXT, -- Available, Sold, Leased, Rented
    FOREIGN KEY (property_id) REFERENCES properties(id)
);

--Brokrage
CREATE TABLE brokerage_firms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    license_no TEXT,
    contact TEXT,
    agreement_terms TEXT,
    active_until DATE
);

CREATE TABLE brokerage_access (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    brokerage_id UUID REFERENCES brokerage_firms(id),
    flat_id UUID REFERENCES flats(id),
    allowed_actions TEXT[], -- Sell, Rent, Lease
    commission_rule TEXT,
    start_date DATE,
    end_date DATE
);

--Gate pass
CREATE TABLE gate_passes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    visitor_name TEXT NOT NULL,
    visitor_contact TEXT,
    flat_id UUID REFERENCES flats(id),
    issued_by UUID REFERENCES users(id),
    purpose TEXT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    status TEXT, -- pending, approved, checked_in, checked_out
    qr_code TEXT
);

CREATE TABLE gate_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    gate_pass_id UUID REFERENCES gate_passes(id),
    check_in_time TIMESTAMP,
    check_out_time TIMESTAMP,
    verified_by UUID REFERENCES users(id)
);

--Leasing and Renting
CREATE TABLE leases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    flat_id UUID REFERENCES flats(id),
    tenant_id UUID REFERENCES users(id),
    start_date DATE,
    end_date DATE,
    monthly_rent NUMERIC(15,2),
    security_deposit NUMERIC(15,2),
    agreement_doc_url TEXT
);

CREATE TABLE rentals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    flat_id UUID REFERENCES flats(id),
    renter_id UUID REFERENCES users(id),
    rent_start DATE,
    rent_end DATE,
    rent_amount NUMERIC(15,2)
);

--Maintenence
CREATE TABLE maintenance_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    flat_id UUID REFERENCES flats(id),
    description TEXT,
    status TEXT, -- pending, in_progress, completed
    assigned_to UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE maintenance_bills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    flat_id UUID REFERENCES flats(id),
    bill_month DATE,
    amount NUMERIC(15,2),
    paid BOOLEAN DEFAULT FALSE
);

--Cust Feedback
CREATE TABLE feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    flat_id UUID REFERENCES flats(id),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--CRM & Lead Management Service
CREATE TABLE leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    contact TEXT,
    email TEXT,
    source TEXT, -- website, portal, broker, referral
    interested_property_id UUID REFERENCES properties(id),
    status TEXT, -- new, contacted, visited, closed
    assigned_to UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



