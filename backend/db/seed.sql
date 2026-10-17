TRUNCATE TABLE restaurants, user_rankings, follows, users;



INSERT INTO users (id, username, display_name, created_at) VALUES
(1, 'chasepham', 'Chase', '2026-10-17 16:25:30.123456-04'),
(2, 'helenkang', 'Helen', '2026-09-17 16:25:30.123456-04'),
(3, 'foodie_sam', 'Sam Rivera', '2026-08-02 10:15-04'),
(4, 'noodle_nina', 'Nina Okafor', '2026-08-15 18:40-04'),
(5, 'taco_theo', 'Theo Brandt', '2026-08-28 12:05-04'),
(6, 'brunch_bea', 'Bea Lindqvist', '2026-09-05 09:30-04'),
(7, 'spicy_raj', 'Raj Mehta', '2026-09-10 20:00-04'),
(8, 'quiet_quinn', 'Quinn Alvarez', '2026-09-20 14:20-04');

INSERT INTO follows (follower_id, followee_id, created_at) VALUES
(1, 2, '2026-10-17 16:26:00-04'),
(2, 1, '2026-10-17 16:28:00-04'),
(1, 3, '2026-10-17 16:26:10-04'),
(3, 1, '2026-10-17 16:27:00-04'),
(1, 4, '2026-10-17 16:26:20-04'),
(1, 7, '2026-10-17 16:26:30-04'),
(5, 1, '2026-10-17 16:27:30-04'),
(6, 1, '2026-10-17 16:28:30-04'),
(2, 3, '2026-09-18 12:00-04'),
(2, 8, '2026-09-21 09:00-04'),
(3, 4, '2026-08-16 10:00-04'),
(4, 3, '2026-08-16 18:30-04'),
(4, 5, '2026-08-29 20:15-04'),
(5, 7, '2026-09-11 13:00-04'),
(7, 5, '2026-09-11 19:45-04'),
(7, 2, '2026-09-19 08:30-04'),
(6, 3, '2026-09-06 11:00-04');

INSERT INTO restaurants (id, name, cuisine, city, address) VALUES
(1, 'Lucia''s Trattoria', 'Italian', 'New York', '112 Mulberry St'),
(2, 'Sora Ramen', 'Japanese', 'New York', '45 St Marks Pl'),
(3, 'Golden Dragon', 'Chinese', 'New York', '18 Mott St'),
(4, 'La Esquina Azul', 'Mexican', 'New York', '230 Bowery'),
(5, 'Seoul Garden', 'Korean', 'New York', '32 W 32nd St'),
(6, 'The Corner Diner', 'American', 'New York', '501 2nd Ave'),
(7, 'Bangkok Basil', 'Thai', 'New York', '89 Bayard St'),
(8, 'Tony''s Pizza', 'Italian', 'New York', '77 Bleecker St'),
(9, 'Golden Dragon', 'Chinese', 'Los Angeles', '940 N Broadway'),
(10, 'Taqueria El Sol', 'Mexican', 'Los Angeles', '1520 E Cesar Chavez Ave'),
(11, 'Umi Sushi Bar', 'Japanese', 'Los Angeles', '305 E 2nd St'),
(12, 'Koreatown BBQ House', 'Korean', 'Los Angeles', '3465 W 6th St'),
(13, 'Sunset Burger Co.', 'American', 'Los Angeles', '7020 Sunset Blvd'),
(14, 'Thai Orchid', 'Thai', 'Los Angeles', '5300 Hollywood Blvd'),
(15, 'Pasta Fresca', 'Italian', 'Los Angeles', '1210 Abbot Kinney Blvd'),
(16, 'Tacos Los Primos', 'Mexican', 'Los Angeles', '4401 Whittier Blvd'),
(17, 'Lakeshore Deep Dish', 'Italian', 'Chicago', '600 N Wabash Ave'),
(18, 'Windy City Dogs', 'American', 'Chicago', '1400 W Fullerton Ave'),
(19, 'Ramen Kaze', 'Japanese', 'Chicago', '2156 N Damen Ave'),
(20, 'Little Saigon Pho', 'Vietnamese', 'Chicago', '1032 W Argyle St'),
(21, 'Casa Morelos', 'Mexican', 'Chicago', '1800 S Blue Island Ave'),
(22, 'Golden Dragon', 'Chinese', 'Chicago', '2200 S Wentworth Ave'),
(23, 'Bulgogi Brothers', 'Korean', 'Chicago', '5200 N Lincoln Ave'),
(24, 'Spice Route Thai', 'Thai', 'Chicago', '1100 W Belmont Ave');



INSERT INTO user_rankings (id, user_id, restaurant_id, rank_position, created_at) VALUES

(1, 1, 1, 1, '2026-10-17 16:26:30-04'),
(2, 1, 2, 2, '2026-10-17 16:27:45-04'),
(3, 1, 5, 3, '2026-10-17 16:29:00-04'),

(4, 2, 2, 1, '2026-09-20 19:30-04'),
(5, 2, 1, 2, '2026-10-04 20:10-04'),
(6, 2, 3, 3, '2026-09-27 13:00-04'),
(7, 2, 6, 4, '2026-10-12 09:45-04'),

(8, 3, 10, 1, '2026-08-05 21:00-04'),
(9, 3, 11, 2, '2026-08-30 19:15-04'),
(10, 3, 9, 3, '2026-09-14 12:30-04'),
(11, 3, 2, 4, '2026-10-15 20:45-04'),
(12, 3, 13, 5, '2026-09-01 13:10-04'),
(13, 3, 15, 6, '2026-10-08 19:00-04'),

(14, 4, 19, 1, '2026-08-20 18:00-04'),
(15, 4, 2, 2, '2026-10-16 21:30-04'),
(16, 4, 20, 3, '2026-09-09 12:15-04'),
(17, 4, 23, 4, '2026-09-25 19:40-04'),
(18, 4, 11, 5, '2026-10-02 20:00-04'),

(19, 5, 21, 1, '2026-08-30 19:00-04'),
(20, 5, 4, 2, '2026-10-10 21:15-04'),
(21, 5, 16, 3, '2026-09-18 13:30-04'),
(22, 5, 10, 4, '2026-10-14 12:00-04'),

(23, 6, 6, 1, '2026-09-07 10:30-04'),
(24, 6, 1, 2, '2026-09-29 19:00-04'),
(25, 6, 8, 3, '2026-10-11 22:00-04'),

(26, 7, 24, 1, '2026-09-12 19:20-04'),
(27, 7, 7, 2, '2026-10-06 20:30-04'),
(28, 7, 5, 3, '2026-09-22 18:45-04'),
(29, 7, 22, 4, '2026-10-13 19:10-04');
