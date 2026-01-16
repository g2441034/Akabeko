CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,                     -- ユーザーのID
    username VARCHAR(50) NOT NULL,            -- ユーザー名
    email VARCHAR(100) NOT NULL UNIQUE,       -- メールアドレス
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- 作成日時
);

INSERT INTO users (username, email) VALUES 
('admin', 'admin@example.com'),               -- サンプルデータ1
('testuser', 'testuser@example.com');         -- サンプルデータ2