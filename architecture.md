## Requirements
- Here is a rough list of requirements for this project:
- Ability for users to sign up and log in.
- Ability to add products to a cart.
- Ability to remove products from a cart.
- Ability to view and search for products.
- Ability for users to checkout and pay for products.
- You should also have some sort of admin panel where only you can add products, set the prices, manage inventory, and more.

- JWT authentication to ensure many users can interact with it.
- Implementing simple CRUD operations.
- Interaction with external services. Here you’ll be integrating with payment gateways such as Stripe.
- A complex data model that can handle products, shopping carts, and more.

## Tech Stack
- FastAPI for backend
- Postgresql for db
- Redis for cache
- poetry as package manager
- docker, docker compose 
- React, js for frontend

## Implementation
#### Authorization 
- JWT with access and refresh token 
- access token expiration 30m
- refresh token expiration 7days
- sign up and log in 

#### Admin panel 
- SQL model
- register all models 

#### Models
- Users 
- Products
- Cart
- Payments
- Order 
- OrderItems
- CartItems




#### API 
- Addding get, post, put, delete for models
- APIrouter for each model

#### Payment with Stripe
- Integrate stripe 

## Architecture
#### Onion Style 
api -> service -> repository -> db 


## Test 
### Pytest 
- test for each router 
- use sqlite for db 

## CI/CD 
- github actions 

## Containerization
- Docker 
- Docker compose 


