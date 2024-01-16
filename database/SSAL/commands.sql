DROP USER usr_adm;
CREATE USER usr_adm WITH password '4Dm1n2023$' SUPERUSER;

DROP USER usr_ssal;
CREATE USER usr_ssal WITH password 'Ss4l2023$';
CREATE DATABASE ssal;
drop SCHEMA cat cascade;
-- conectarse a la base de datos para crear el schema
\c ssal
CREATE SCHEMA IF NOT EXISTS cat;
GRANT USAGE ON SCHEMA cat TO usr_ssal;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA cat TO usr_ssal;

-- ALTER DEFAULT PRIVILEGES IN SCHEMA cat GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO usr_ssal;

drop sequence if exists cat.seq_cat_usuario;
CREATE SEQUENCE cat.seq_cat_usuario START 3;
GRANT USAGE, SELECT ON SEQUENCE cat.seq_cat_usuario TO usr_ssal;