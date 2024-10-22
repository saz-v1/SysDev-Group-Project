# Horizon Restaurant Management System

## Overview

The **Horizon Restaurant Management System** (HRMS) is a web-based application developed as part of the Systems Development Group Project for the UFCF7S-30-2 module. The primary goal is to improve the efficiency of restaurant operations and enhance customer experience by providing a streamlined solution for managing reservations, orders, payments, inventory, and more.

## Features

- **User Account Registration**: Users can register an account with essential details.
- **Reservation Management**: Users can create, modify, and delete table reservations.
- **Order Placement**: Customers can browse the menu, add items to the cart, and place orders.
- **Online Payments**: Secure payment gateway integrated with receipt generation.
- **Inventory Management**: Admins can manage restaurant inventory and track stock levels.
- **Order Management**: Staff can manage incoming orders, update their statuses, and track progress.
- **Discount Management**: Admins can create and manage discounts and promotions.
- **Menu Management**: Admins can add, update, and delete menu items dynamically.
- **Reporting**: Generate reports for sales, orders, and customer analytics.
- **Kitchen Functions**: Organize orders for kitchen staff with menu categorization and stock availability.

## Technologies Used

### Frontend:
- **HTML/CSS**: For designing the user interface.
- **Bootstrap**: Framework for creating a responsive UI.

### Backend:
- **Flask**: A lightweight Python web framework used for backend development.
- **MySQL**: The relational database management system (RDBMS) used to manage the application’s data.

### Payment Integration:
- Supports secure payment handling with options for integrating multiple payment gateways.

### Deployment:
- Can be deployed on local or cloud servers with scalability in mind for multi-branch operations.

## Requirements

### Functional Requirements:
- User account management
- Reservations management
- Menu browsing and order placement
- Inventory and order management for staff
- Discounts and offers management
- Sales and performance reporting
- Kitchen staff support (menu categorization, stock monitoring)

### Non-functional Requirements:
- Must have a user-friendly interface
- Must be responsive and adaptable to all screen sizes
- Pages must load within a 3-second time frame

## System Architecture

The system follows a client-server architecture where:
- The **frontend** handles user interaction.
- The **backend** processes data, connects to the MySQL database, and handles business logic.
- The **database** stores user information, menu items, orders, inventory, etc.

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://gitlab.uwe.ac.uk/a22-osman/systems-development-group-project.git
   ```

2. Navigate to the project directory:
   ```bash
   cd systems-development-group-project
   ```

3. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up the MySQL database and configure the database settings in the Flask application.

6. Run the application:
   ```bash
   flask run
   ```

7. Open your browser and navigate to `http://127.0.0.1:5000` to use the application.

## Testing

The application includes tests for:
- Ensuring the correct flow of user interactions.
- Handling errors for invalid inputs.
- Integrity of order and booking information.
- Testing the user interface and database connections.

## Challenges and Future Improvements

### Challenges:
- Managing feature dependencies such as reservation management relying on pre-inserted restaurants.
- Maintaining performance while adding new features.

### Future Improvements:
- Improve the visual design with enhanced UI elements.
- Implement personalized menu recommendations using machine learning.
- Optimize the system for larger datasets and multiple restaurant locations.

## Contributors

- **Sumanth Kasthuri**
- **Abdalle Omar**
- **Mohameed Hussein**
- **Syed Zaheer**
- **Aden Osman**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```
