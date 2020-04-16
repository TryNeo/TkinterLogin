drop database if exists login;
create database if not exists login;
use login;
create table usuario(
id_usuario int auto_increment,
email varchar(50),
username varchar(50),
password TEXT,
primary key(id_usuario));
