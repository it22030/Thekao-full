# ঠেকাও Super App

A comprehensive Django-based super app providing four main services: Food Delivery, Ride Sharing, Parcel Delivery, and Shopping Mall.

## 🚀 Features

### 🍔 Food Delivery
- Browse restaurants and menus
- Shopping cart functionality
- Order placement and tracking
- Rider assignment and delivery

### 🚗 Ride Sharing
- Request rides with interactive map
- Automatic fare calculation
- Driver assignment
- Real-time ride tracking

### 📦 Parcel Delivery
- Create delivery requests
- Automatic tracking numbers
- Status tracking (requested → accepted → picked_up → delivered)
- Rider assignment

### 🛍️ Shopping Mall
- 4 shops with 20 products
- Shopping cart and checkout
- Order tracking
- Stock management

## 🏗️ Tech Stack

- **Backend:** Django 5.x
- **Database:** SQLite (development)
- **Frontend:** HTML, CSS, JavaScript
- **Maps:** Leaflet.js
- **Icons:** Lucide Icons

## 📦 Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd Food_delivery
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create superuser**
```bash
python manage.py createsuperuser
```

6. **Seed sample data**
```bash
python manage.py seed_mall
```

7. **Run server**
```bash
python manage.py runserver
```

8. **Access the app**
- Home: http://localhost:8000/
- Admin: http://localhost:8000/dashboard/

## 👥 User Roles

### Customer
- Order food, book rides, send parcels, shop at mall

### Rider
- **Food Delivery Riders:** Handle food orders
- **Parcel Delivery Riders:** Handle parcel deliveries
- **Both:** Can handle both types

### Admin
- Full system management
- Assign riders to orders/parcels
- Configure global settings

## 📁 Project Structure

```
Food_delivery/
├── accounts/          # User authentication
├── cart/              # Food cart
├── core/              # Global settings
├── dashboard/         # Admin & rider dashboards
├── mall/              # Shopping mall
├── menu/              # Restaurant menus
├── orders/            # Food orders
├── parcels/           # Parcel delivery
├── restaurants/       # Restaurant management
├── rides/             # Ride sharing
└── templates/         # HTML templates
```

## 🎨 Design

- **Primary Color:** #D70F64 (Pink)
- **Typography:** Poppins + Hind Siliguri
- **Modern UI:** Cards, shadows, smooth animations
- **Responsive:** Works on all screen sizes

## 💰 Revenue Model

- **Food Delivery:** Commission-based
- **Rides:** Fare-based with commission
- **Parcels:** Base fee + weight pricing
- **Mall:** Commission from shops

All percentages configurable in GlobalSettings.

## 🔧 Configuration

Access global settings at `/dashboard/settings/` to configure:
- Delivery charges
- Commission percentages
- Rider fees

## 📝 License

This project is for educational purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or support, please open an issue.

---

**Status:** ✅ Production Ready

Built with ❤️ using Django
