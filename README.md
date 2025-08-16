# Mini Auction Backend

This is the backend service for the Mini Auction System, built with Django and Django REST Framework. It provides RESTful APIs for auction management, user bidding, and bidding validation.

## Features Implemented

- **User Authentication:**  
  Basic user authentication is enforced for key actions like placing bids and creating auctions.

- **Auction Management:**  
  Users (sellers) can create auctions with details such as:
- Item name and description  
  - Starting price  
  - Minimum bid increment  
  - Scheduled go-live date and bid duration  
  - Auction status tracking (pending, live, ended, closed)

- **Bid Management:**  
  Buyers can place bids on live auctions only. The system ensures:
- Bids meet minimum increment over the last highest bid or starting price  
  - Validation of auction status and timing for valid bids  
  - Proper storage of bids linked to bidders and auctions  

- **API Endpoints:**  
  - Auction listing and details  
  - Creating auctions
- Placing bids through a dedicated API endpoint (`/api/auctions/{id}/place_bid/`)  
  - Bid listing (read-only)

- **Automated Testing:**  
  Unit and API tests to verify auction creation, valid bid placement, bid rejection when below minimum, and auction listing.
