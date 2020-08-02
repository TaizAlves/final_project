import sqlite3

conn = sqlite3.connect('healings.db')
cur = conn.cursor()

cur.executescript('''
       
        CREATE TABLE IF NOT EXISTS 'category' (
            'id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            'name' varchar(255) NOT NULL
            );

        CREATE TABLE IF NOT EXISTS 'recipes' (
            'id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            'title' varchar(255) NOT NULL,
            'description' text NOT NULL,
            'more_info' text,
            'created_at' DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ,
            'category_id' INTEGER NOT NULL,
            'user_id' INTEGER NOT NULL,
            FOREIGN KEY (category_id) REFERENCES category(id),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

        CREATE TABLE IF NOT EXISTS 'users' (
                    'id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    'name' text NOT NULL,
                    'email' text UNIQUE NOT NULL,
                    'hash' text NOT NULL,
                    'status', text NOT NULL DEFAULT "client",
                    'created_at' DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP );

        ALTER TABLE 'recipes' ADD FOREIGN KEY ('category_id') REFERENCES 'category' ('id');

        ALTER TABLE 'recipes' ADD FOREIGN KEY ('user_id') REFERENCES 'users' ('id');
        ALTER TABLE 'products' ADD FOREIGN KEY ('category_id') REFERENCES 'category' ('id')

        CREATE TABLE IF NOT EXISTS 'produts' (
                    'id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
					'img' text,
                    'title' text NOT NULL,
					'description' text NOT NULL,
                    'category_id' INTEGER NOT NULL,
					FOREIGN KEY (category_id) REFERENCES category(id)
					);
        CREATE TABLE IF NOT EXISTS 'sales' (
                    'id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    'product_id' INTEGER NOT NULL,
					'user_id' INTEGER NOT NULL,
					FOREIGN KEY (product_id) REFERENCES produts(id),
					FOREIGN KEY (user_id) REFERENCES users(id)
					
					);
        ''')

conn.commit()


# insert company - para poder mostrar as vendas
#INSERT INTO users (name, email, hash, status) VALUES ("NaturalHealing","n@natural.com","2222","company")