INSERT INTO users (username, email, password) VALUES
('Vanya1', 'example1@mail.ru', 'qwerty123'),
('Vanya2', 'example2@mail.ru', 'qwerty123'),
('Vanya3', 'example3@mail.ru', 'qwerty123'),
('Vanya4', 'example4@mail.ru', 'qwerty123'),
('Vanya5', 'example5@mail.ru', 'qwerty123'),
('Vanya6', 'example6@mail.ru', 'qwerty123'),
('Vanya7', 'example7@mail.ru', 'qwerty123'),
('Vanya8', 'example8@mail.ru', 'qwerty123'),
('Vanya9', 'example9@mail.ru', 'qwerty123'),
('Vanya10', 'example10@mail.ru', 'qwerty123'),
('Vanya11', 'example11@mail.ru', 'qwerty123'),
('Vanya12', 'example12@mail.ru', 'qwerty123'),
('Vanya13', 'example13@mail.ru', 'qwerty123'),
('Vanya14', 'example14@mail.ru', 'qwerty123'),
('Vanya15', 'example15@mail.ru', 'qwerty123'),
('Vanya16', 'example16@mail.ru', 'qwerty123'),
('Vanya17', 'example17@mail.ru', 'qwerty123'),
('Vanya18', 'example18@mail.ru', 'qwerty123'),
('Vanya19', 'example19@mail.ru', 'qwerty123'),
('Vanya20', 'example20@mail.ru', 'qwerty123'),
('Vanya21', 'example21@mail.ru', 'qwerty123'),
('Vanya22', 'example22@mail.ru', 'qwerty123'),
('Vanya23', 'example23@mail.ru', 'qwerty123'),
('Vanya24', 'example24@mail.ru', 'qwerty123'),
('Vanya25', 'example25@mail.ru', 'qwerty123');

INSERT INTO games (title) VALUES
('Dota2'),
('CS2'),
('Valorant');

INSERT INTO news (title, content, author_id, id_game) VALUES
('Прошел турнир', 'В игре Dota2 прошел новый турнир', (SELECT id_user FROM users WHERE username = 'Vanya1'), (SELECT id_game FROM games WHERE title = 'Dota2')),
('Ивент', 'В волоранте начался ивент', (SELECT id_user FROM users WHERE username = 'Vanya23'), (SELECT id_game FROM games WHERE title = 'Valorant')),
('Вышел новый кейс', 'С приходом новой операции', (SELECT id_user FROM users WHERE username = 'Vanya11'), (SELECT id_game FROM games WHERE title = 'CS2'));

INSERT INTO users (username, email, password, role) VALUES
('Admin', 'Admin@mail.ru', 'qwerty123', 'admin')