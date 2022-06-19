DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS recipes;
DROP TABLE IF EXISTS weeks;
DROP TABLE IF EXISTS menus;
PRAGMA foreign_keys = ON;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    groceries TEXT DEFAULT '',

    -- How many weeks there are in the user's planner
    weeks_count INTEGER DEFAULT 1
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT (32) UNIQUE NOT NULL,
    description TEXT(512),
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Text data
    title VARCHAR(32) NOT NULL,
    description TEXT (512),
    ingredients TEXT (512) NOT NULL,
    directions TEXT (512) NOT NULL,
    links TEXT,
    notes TEXT,

    -- Numerical data
    servings INTEGER,
    prep_t INTEGER (4),
    cook_t INTEGER (4),
    total_t INTEGER (5),

    -- Foreign keys
    category_id INTEGER,
    user_id INTEGER NOT NULL,

    -- When the category is deleted, set the key to NULL
    CONSTRAINT fk_category
        FOREIGN KEY(category_id) 
        REFERENCES categories(id)
        ON DELETE SET NULL, 

    -- When the user is deleted, delete all his recipes as well
    CONSTRAINT fk_user
        FOREIGN KEY (user_id) 
        REFERENCES users(id)
        ON DELETE CASCADE
);

CREATE TABLE weeks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week_n INTEGER NOT NULL,
    
    -- 0-No course, 1-Breakfast, 2-Lunch, 3-Dinner, 4-Snack
    Monday      TEXT DEFAULT ',,,,',
    Tuesday     TEXT DEFAULT ',,,,',
    Wednsday    TEXT DEFAULT ',,,,',
    Thursday    TEXT DEFAULT ',,,,',
    Friday      TEXT DEFAULT ',,,,',
    Saturday    TEXT DEFAULT ',,,,',
    Sunday      TEXT DEFAULT ',,,,',

    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE menus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT (32),
    description TEXT (512),
    recipes TEXT DEFAULT ',,,,',

    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id)
);