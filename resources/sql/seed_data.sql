-- Insert test users
INSERT INTO users (username, email, first_name, last_name, password, phone, is_active)
VALUES
    ('admin', 'admin@example.com', 'Admin', 'User', '$2b$12$1234567890123456789012uOOmwM4PDBTAeUQUhTDYGfEBqbpnEZe', '+1234567890', TRUE),
    ('user1', 'user1@example.com', 'John', 'Doe', '$2b$12$1234567890123456789012uWW9ytELNfR4nq1fFx2r4JmsBnNSLDi', '+9876543210', TRUE),
    ('user2', 'user2@example.com', 'Jane', 'Smith', '$2b$12$1234567890123456789012u5JXxs.5K0TDjfKTvCpG2Z5Q4M2CQq', '+1122334455', TRUE)
ON CONFLICT (username) DO NOTHING;

-- Insert test contacts
INSERT INTO contacts (first_name, last_name, email, phone, address, notes, user_id)
VALUES
    ('Alice', 'Johnson', 'alice@example.com', '+1122334455', '123 Main St, City, Country', 'Work contact', (SELECT id FROM users WHERE username = 'admin')),
    ('Bob', 'Brown', 'bob@example.com', '+5544332211', '456 Oak St, City, Country', 'Personal contact', (SELECT id FROM users WHERE username = 'admin')),
    ('Charlie', 'Davis', 'charlie@example.com', '+9988776655', '789 Pine St, City, Country', 'Client', (SELECT id FROM users WHERE username = 'user1')),
    ('Diana', 'Wilson', 'diana@example.com', '+6677889900', '321 Elm St, City, Country', 'Supplier', (SELECT id FROM users WHERE username = 'user1')),
    ('Eva', 'Martinez', 'eva@example.com', '+1324354657', '654 Maple St, City, Country', 'Business partner', (SELECT id FROM users WHERE username = 'user2'))
ON CONFLICT DO NOTHING;
