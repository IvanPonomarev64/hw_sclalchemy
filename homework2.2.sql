create table if not exists genre (
	id serial primary key,
	genre_name varchar(100) not null unique
);
create table if not exists executor (
	id serial primary key,
	executor_name varchar(100) not null,
	genre_id integer references genre(id)
);
create table if not exists album (
	id serial primary key,
	album_name varchar(100) not null,
	year_of_release integer not null,
	executor_id integer references executor(id)
);
create table if not exists track (
	id serial primary key,
	track_name varchar(100) not null unique,
	duration integer not null,
	album_id integer references album(id)
);