-- Configuração recomendada para Docker/PostgreSQL
SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET default_tablespace = '';
SET default_with_oids = false;

DROP TABLE IF EXISTS google_gmail_emails_extended;

CREATE TABLE google_gmail_emails_extended (
  id_user INT PRIMARY KEY,
  from_user VARCHAR(50),
  to_user VARCHAR(50),
  day_send INT
);

-- Inserts de exemplo
INSERT INTO google_gmail_emails_extended (id_user, from_user, to_user, day_send) VALUES
(1, 'ana', 'bruno', 1),
(2, 'ana', 'carlos', 1),
(3, 'bruno', 'daniela', 1),
(4, 'carlos', 'ana', 2),
(5, 'ana', 'daniela', 2),
(6, 'bruno', 'carlos', 2),
(7, 'ana', 'erica', 3),
(8, 'daniela', 'ana', 3),
(9, 'erica', 'bruno', 3),
(10, 'felipe', 'ana', 4),
(11, 'gabriela', 'daniela', 4),
(12, 'helena', 'bruno', 4),
(13, 'ana', 'gabriela', 5),
(14, 'bruno', 'helena', 5),
(15, 'carlos', 'erica', 5),
(16, 'daniela', 'felipe', 6),
(17, 'erica', 'gabriela', 6),
(18, 'felipe', 'helena', 6),
(19, 'gabriela', 'carlos', 7),
(20, 'helena', 'ana', 7),
(21, 'ana', 'bruno', 8),
(22, 'bruno', 'carlos', 8),
(23, 'carlos', 'daniela', 8),
(24, 'daniela', 'erica', 9),
(25, 'erica', 'felipe', 9),
(26, 'felipe', 'gabriela', 9),
(27, 'gabriela', 'helena', 10),
(28, 'helena', 'ana', 10),
(29, 'ana', 'carlos', 10),
(30, 'bruno', 'daniela', 10),
(31, 'Alfred', 'daniela', 10);

