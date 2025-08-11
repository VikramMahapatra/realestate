
Real Estate CRM microservices
=====================================

Services included: auth-service, property-service, brokerage-service, maintenance-service, support-service, feedback-service, inventory-service

Run locally (requires docker-compose):
> docker-compose up --build

Auth service available at: http://localhost:8001


API End Points:
Property
Property Service API Endpoints
1. Developer Management
Method	Endpoint	Description
POST	/developers	Create new developer
GET	/developers	List all developers (with pagination/filter by name)
GET	/developers/{developer_id}	Get developer details
PUT	/developers/{developer_id}	Update developer info
DELETE	/developers/{developer_id}	Delete developer

2. RERA Details
Method	Endpoint	Description
POST	/rera-details	Add RERA detail
GET	/rera-details	List all RERA registrations
GET	/rera-details/{rera_id}	Get specific RERA detail
PUT	/rera-details/{rera_id}	Update RERA detail
DELETE	/rera-details/{rera_id}	Delete RERA record

3. Property Management
Method	Endpoint	Description
POST	/properties	Create new property/project
GET	/properties	List/search/filter properties (by status, location, developer, RERA, amenities)
GET	/properties/{property_id}	Get property details (with buildings, amenities, RERA info)
PUT	/properties/{property_id}	Update property details
DELETE	/properties/{property_id}	Delete property
PATCH	/properties/{property_id}/status	Change property status (log in history table)
GET	/properties/{property_id}/status-history	Get property status change history

4. Building Management
Method	Endpoint	Description
POST	/properties/{property_id}/buildings	Add new building to property
GET	/properties/{property_id}/buildings	List buildings for a property
GET	/buildings/{building_id}	Get building details
PUT	/buildings/{building_id}	Update building details
DELETE	/buildings/{building_id}	Delete building

5. Flat Management
Method	Endpoint	Description
POST	/buildings/{building_id}/flats	Add flat/unit
GET	/buildings/{building_id}/flats	List flats in a building (filter by availability, price, unit type)
GET	/flats/{flat_id}	Get flat details
PUT	/flats/{flat_id}	Update flat details
DELETE	/flats/{flat_id}	Delete flat
PATCH	/flats/{flat_id}/status	Change flat status (log in history table)
GET	/flats/{flat_id}/status-history	Get flat status change history

6. Flat Images
Method	Endpoint	Description
POST	/flats/{flat_id}/images	Upload flat images
GET	/flats/{flat_id}/images	Get flat images
DELETE	/flat-images/{image_id}	Delete flat image

7. Amenities
Method	Endpoint	Description
POST	/amenities	Add amenity
GET	/amenities	List amenities
DELETE	/amenities/{amenity_id}	Delete amenity
POST	/properties/{property_id}/amenities	Assign amenities to property
DELETE	/properties/{property_id}/amenities/{amenity_id}	Remove amenity from property

8. Pricing & History
Method	Endpoint	Description
POST	/flats/{flat_id}/pricing	Add pricing entry
GET	/flats/{flat_id}/pricing-history	Get flat price history
GET	/properties/{property_id}/pricing-summary	Get min/max/average prices for property

9. Document Management
Method	Endpoint	Description
POST	/properties/{property_id}/documents	Upload property document
GET	/properties/{property_id}/documents	List property documents
GET	/documents/{document_id}	Download property document
DELETE	/documents/{document_id}	Delete document

10. Search & Public APIs
Method	Endpoint	Description
GET	/search/properties	Search properties by location, price range, status
GET	/search/flats	Search flats by location, price range, status
GET	/public/properties	Public property listings (no auth, basic details)
GET	/public/flats	Public flat listings
