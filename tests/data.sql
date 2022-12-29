insert into user(username, password) values
('test', 'pbkdf2:sha256:260000$Ys0Qwx0b6vEkSec5$e2554686d76996eea3e154dc92de91c0d9ac664bb804a9ba08f8f9b85baea9c3'),
('other', 'pbkdf2:sha256:260000$w0qJVWQJoiUrv9aQ$2cc5a67bfe51705ad72993c5138f81c2cbfcaf66de3e6dd8aa307b7b745d43ea');

insert into post(title, body, author_id, created) values
('test title', 'test' || x'0a' || 'body',1, '2018-01-01 00:00:00');