-- =========================
-- 1. DEFINE ENUMS
-- =========================
CREATE TYPE user_role AS ENUM ('buyer', 'seller', 'both');
CREATE TYPE user_status AS ENUM ('active', 'suspended');
CREATE TYPE product_condition AS ENUM ('new', 'used');
CREATE TYPE product_status AS ENUM ('available', 'sold', 'hidden');
CREATE TYPE order_status AS ENUM ('pending', 'paid', 'completed', 'cancelled');
CREATE TYPE payment_method AS ENUM ('cash', 'bank_transfer', 'e_wallet');
CREATE TYPE payment_status AS ENUM ('pending', 'paid', 'failed');

-- =========================
-- 2. TABLES
-- =========================

-- USERS
CREATE TABLE users (
    user_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    phone_number TEXT,
    profile_image TEXT,
    role user_role DEFAULT 'both',
    status user_status DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT now()
);

-- CATEGORIES
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name TEXT NOT NULL,
    parent_category_id INT REFERENCES categories(category_id) ON DELETE SET NULL
);

-- PRODUCTS
CREATE TABLE products (
    product_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    seller_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    quantity INT DEFAULT 1,
    product_condition product_condition DEFAULT 'used',
    status product_status DEFAULT 'available',
    created_at TIMESTAMPTZ DEFAULT now()
);

-- PRODUCT IMAGES
CREATE TABLE product_images (
    image_id SERIAL PRIMARY KEY,
    product_id UUID REFERENCES products(product_id) ON DELETE CASCADE,
    image_url TEXT NOT NULL
);

-- PRODUCT CATEGORY (Many-to-Many)
CREATE TABLE product_categories (
    product_id UUID REFERENCES products(product_id) ON DELETE CASCADE,
    category_id INT REFERENCES categories(category_id) ON DELETE CASCADE,
    PRIMARY KEY (product_id, category_id)
);

-- ORDERS
CREATE TABLE orders (
    order_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    buyer_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    order_status order_status DEFAULT 'pending',
    total_amount DECIMAL(10,2),
    order_date TIMESTAMPTZ DEFAULT now()
);

-- ORDER ITEMS
CREATE TABLE order_items (
    order_item_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    order_id UUID REFERENCES orders(order_id) ON DELETE CASCADE,
    product_id UUID REFERENCES products(product_id) ON DELETE CASCADE,
    seller_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    price_at_purchase DECIMAL(10,2) NOT NULL,
    quantity INT DEFAULT 1
);

-- PAYMENTS
CREATE TABLE payments (
    payment_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    order_id UUID REFERENCES orders(order_id) ON DELETE CASCADE,
    payment_method payment_method DEFAULT 'cash',
    payment_status payment_status DEFAULT 'pending',
    paid_at TIMESTAMPTZ
);

-- CHATS
CREATE TABLE chats (
    chat_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    product_id UUID REFERENCES products(product_id) ON DELETE CASCADE,
    buyer_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    seller_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- MESSAGES
CREATE TABLE messages (
    message_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    chat_id UUID REFERENCES chats(chat_id) ON DELETE CASCADE,
    sender_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    message_text TEXT NOT NULL,
    sent_at TIMESTAMPTZ DEFAULT now()
);

-- REVIEWS
CREATE TABLE reviews (
    review_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    order_item_id UUID REFERENCES order_items(order_item_id) ON DELETE CASCADE,
    reviewer_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);