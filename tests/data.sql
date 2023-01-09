insert into user(username, password) values
('test', 'pbkdf2:sha256:260000$fmtF8gjhgC5f16jn$1b379117049e38b8657f6a943dc64479ed1cba394b05c1238945a3ec5c6531e2'),
-- ID: test, pass: test
('other', 'pbkdf2:sha256:260000$i1LO7xmWA7Ht4Hc3$399fbfae46f9d379e220c2730ece223b61675592ad25110dae24f9bd1359282d');
-- ID: other, pass: other

insert into post(title, body, author_id, created) values
('test title', 'test' || x'0a' || 'body',1, '2018-01-01 00:00:00');