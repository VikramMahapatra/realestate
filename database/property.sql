-- Tables
-- developer
-- properties
-- rera_details
-- buildings
-- flats
-- flat_images
-- amenities
-- Maintaince charges
-- Nearby facilities
-- Finance_bank_loans
-- property_amenities
-- parking_slots
-- flat_pricing_history
-- flat_status_history
-- property_documents
-- unit_types
-- security services
 
--0. developers
CREATE TABLE developers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    registration_no TEXT, -- Developer/Builder license number if applicable
    contact_name TEXT,
    contact_phone TEXT,
    contact_email TEXT,
    address TEXT,
    website TEXT,
    established_year INT,
    description TEXT, -- Overview of the developer
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 1. properties
-- Holds top-level project or complex details.

CREATE TABLE properties (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    description TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    latitude NUMERIC(9,6),
    longitude NUMERIC(9,6),
    developer_name TEXT,
    developer_id UUID REFERENCES developers(id),
    status TEXT, -- planned, under_construction, ready_to_move, sold_out
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--1.1 properties_status_history

CREATE TABLE property_status_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id UUID NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
    old_status TEXT, -- previous status
    new_status TEXT NOT NULL, -- updated status
    changed_by UUID, -- user_id (optional, from auth service)
    change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


--2
CREATE TABLE rera_details (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id UUID NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
    rera_registration_no TEXT NOT NULL, -- Unique RERA ID
    rera_state TEXT NOT NULL, -- State where registered
    rera_certificate_url TEXT, -- Link to uploaded PDF/image
    registration_date DATE,
    expiry_date DATE,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. buildings
-- If the project has multiple towers/blocks.

CREATE TABLE buildings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id UUID NOT NULL REFERENCES properties(id),
    name TEXT NOT NULL, -- Tower A, Block 1, etc.
    floors INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- 3. flats
-- Individual residential/commercial units.

CREATE TABLE flats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    building_id UUID REFERENCES buildings(id),
    property_id UUID NOT NULL REFERENCES properties(id),
    unit_number TEXT NOT NULL,
    floor INTEGER,
    area_sqft NUMERIC(10,2),
    bedrooms INTEGER,
    bathrooms INTEGER,
    furnishing_status TEXT, -- unfurnished, semi-furnished, furnished
    status TEXT, -- available, sold, leased, rented, blocked
    price NUMERIC(15,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. flat_images
-- Stores multiple images per flat.

CREATE TABLE flat_images (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    flat_id UUID NOT NULL REFERENCES flats(id),
    image_url TEXT NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. amenities
-- Master list of possible amenities.

CREATE TABLE amenities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL, -- swimming pool, gym, garden,yoga classes,Clubhouse events, festival celebrations, community halls.
    description TEXT
);

-- 6. property_amenities
-- Links properties to amenities.

CREATE TABLE property_amenities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id UUID NOT NULL REFERENCES properties(id),
    amenity_id UUID NOT NULL REFERENCES amenities(id)
);

-- 7. flat_pricing_history
-- Tracks price changes over time.

CREATE TABLE flat_pricing_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    flat_id UUID NOT NULL REFERENCES flats(id),
    price NUMERIC(15,2) NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. flat_status_history
-- Keeps record of status changes.


CREATE TABLE flat_status_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    flat_id UUID NOT NULL REFERENCES flats(id),
    status TEXT NOT NULL, -- available, sold, leased, rented
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    changed_by UUID
);

-- 9. property_documents
-- Stores documents like layout plans, approvals, RERA certificates.


CREATE TABLE property_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id UUID NOT NULL REFERENCES properties(id),
    doc_name TEXT NOT NULL,
    doc_url TEXT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
10. unit_types
For managing standard unit configurations.


CREATE TABLE unit_types (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id UUID NOT NULL REFERENCES properties(id),
    type_name TEXT NOT NULL, -- 2BHK, 3BHK, studio
    area_sqft NUMERIC(10,2),
    bedrooms INTEGER,
    bathrooms INTEGER,
    base_price NUMERIC(15,2)
);

-- 11. Maintaince charges
-- MOnthly Quaterly Yearly


CREATE TABLE maintenance_charges (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    flat_id UUID REFERENCES flats(id) ON DELETE CASCADE,
    charge_amount NUMERIC(12,2) NOT NULL,
    frequency TEXT CHECK (frequency IN ('monthly', 'quarterly', 'yearly')),
    due_date DATE,
    status TEXT CHECK (status IN ('pending', 'paid', 'overdue')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 12. Nearby Facillities
-- School ,hospitals ,Transport, EV charging station

CREATE TABLE nearby_facilities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id UUID REFERENCES properties(id) ON DELETE CASCADE,
    facility_type TEXT CHECK (facility_type IN ('school', 'hospital', 'transport')),
    name TEXT NOT NULL,
    distance_km NUMERIC(5,2),
    contact_info TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- 13. Parking slots
-- Covered open basement


CREATE TABLE parking_slots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id UUID REFERENCES properties(id) ON DELETE CASCADE,
    flat_id UUID REFERENCES flats(id) ON DELETE SET NULL,
    slot_number TEXT NOT NULL,
    slot_type TEXT CHECK (slot_type IN ('covered', 'open', 'basement')),
    is_reserved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--14. Finance_bank_loans
--bank name interest contact no

CREATE TABLE finance_bank_loans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id UUID REFERENCES properties(id) ON DELETE CASCADE,
    bank_name TEXT NOT NULL,
    interest_rate NUMERIC(5,2),
    max_loan_amount NUMERIC(15,2),
    tenure_years INT,
    contact_info TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--14. Booking of flats
--Reserverd confirmed cancelled


CREATE TABLE bookings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    inquiry_id UUID REFERENCES inquiries(id) ON DELETE SET NULL,
    flat_id UUID REFERENCES flats(id) ON DELETE CASCADE,
    customer_id UUID REFERENCES customers(id) ON DELETE CASCADE,
    booking_date DATE DEFAULT CURRENT_DATE,
    booking_status TEXT CHECK (booking_status IN ('reserved', 'confirmed', 'cancelled')),
    booking_amount NUMERIC(12,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--14. Inquiries of flats
--New follow up cancelled

CREATE TABLE inquiries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    flat_id UUID REFERENCES flats(id) ON DELETE CASCADE,
    customer_id UUID REFERENCES customers(id) ON DELETE CASCADE,
    inquiry_date DATE DEFAULT CURRENT_DATE,
    inquiry_status TEXT CHECK (inquiry_status IN ('new', 'follow_up', 'converted', 'closed')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--15. security_services
--24/7 guards, CCTV monitoring, visitor management, intercom system.

CREATE TABLE security_services (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id UUID NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
    service_type TEXT NOT NULL, -- e.g. "24/7 Guards", "CCTV Monitoring"
    description TEXT, -- Details about the service
    vendor_name TEXT, -- Company providing the service
    contact_info TEXT, -- Phone/email of vendor
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--15. utility_services
--Water supply, power backup (DG sets, solar), gas pipeline, Wi-Fi.

CREATE TABLE utility_services (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id UUID NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
    utility_type TEXT NOT NULL, -- e.g., "Water Supply", "Power Backup", "Gas Pipeline", "Wi-Fi"
    provider_name TEXT, -- Name of the service provider/vendor
    billing_type TEXT, -- e.g., "Monthly", "Quarterly", "Prepaid", "Included in Maintenance"
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);





