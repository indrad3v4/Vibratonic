# Overview

Vibratonic is a Python-based hackathon platform built with Streamlit that gamifies the "Hack → Demo → Fund" loop. The platform connects creators, investors, organizers, and admins in a neon-themed PWA environment. Users can create hackathons, develop MVPs, showcase projects, and secure funding through integrated payments. The application features real-time activity feeds, interactive maps for event discovery, and comprehensive admin dashboards for platform management.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Clean Architecture Pattern
The codebase follows Clean Architecture principles with four distinct layers:
- `_0_domain`: Core business entities (Hackathon, MVP, User) with no external dependencies
- `_1_use_cases`: Application business rules and services
- `_2_adapters`: Interface adapters for external services (Mollie payments, WebSocket)
- `_3_frameworks`: External interfaces and Streamlit application framework

This separation ensures testability, maintainability, and independence from external frameworks.

## Frontend Architecture
Built entirely on Streamlit with multi-page application structure:
- **Main App**: `app.py` serves as the entry point with configuration and initialization
- **Page-based Routing**: Separate files for each major feature (Create Hackathon, Map View, MVP Showcase, etc.)
- **State Management**: Centralized session state management through `utils/state_management.py`
- **Custom Styling**: Neon-themed CSS with consistent color variables and responsive design

## Data Management
Uses in-memory data storage with service classes:
- **HackathonService**: Manages hackathon CRUD operations and sample data initialization
- **MVPService**: Handles MVP lifecycle, funding goals, and media management
- **PaymentService**: Orchestrates payment processing with platform fee calculations

## User Experience Design
Implements role-based access control with five user types:
- Guest, Participant, Investor, Organizer, Admin
- Permission-based feature access (hackathon creation, investment capabilities, admin functions)
- Wizard-based flows for complex processes like hackathon creation

## Real-time Features
WebSocket adapter designed for live updates:
- Activity feed broadcasting
- Payment status notifications
- Real-time hackathon participant updates
- Channel-based messaging system

# External Dependencies

## Payment Processing
- **Mollie Payment API**: Primary payment processor supporting iDEAL, cards, SEPA, and PayPal
- **Platform Economics**: 20% platform fee automatically calculated on all transactions
- **Mock Implementation**: Demo environment with simulated payment flows for development

## Frontend Libraries
- **Streamlit**: Core web framework for Python-based applications
- **Streamlit-Folium**: Interactive map integration for hackathon venue visualization
- **Plotly**: Chart and graph generation for admin dashboards and analytics

## Development Environment
- **Python 3.11+**: Core runtime requirement
- **Custom CSS**: Neon theme implementation with CSS variables for consistent styling
- **Session State**: Streamlit's built-in state management for user sessions and application data

## Future Infrastructure
- **Database**: Architecture prepared for database integration (likely PostgreSQL with Drizzle ORM)
- **WebSocket Server**: FastAPI + Uvicorn backend planned for real-time features
- **CORS Configuration**: Middleware setup for cross-origin requests between frontend and backend