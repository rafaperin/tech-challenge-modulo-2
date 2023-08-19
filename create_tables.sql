create table if not exists customers (
	customer_id uuid primary key,
	cpf varchar(14) unique,
    first_name varchar(30),
    last_name varchar(30),
    email varchar(80),
    phone varchar(20)
);

create table if not exists products (
	product_id uuid primary key,
	name varchar(30) not null,
    description varchar(150) not null,
    category varchar(30) not null,
    price decimal(7,2) not null,
    image_url varchar(150)
);

create table if not exists orders (
	order_id uuid primary key,
	customer_id uuid not null,
    creation_date timestamp default now(),
    order_total decimal(7,2),
    status varchar(20) not null
);

create table if not exists order_items (
	id serial primary key,
	order_id uuid references orders(order_id) on delete cascade,
	product_id uuid not null,
	product_quantity integer not null
);

alter table orders
add constraint constraint_customer_id
foreign key (customer_id)
references customers (customer_id);

alter table order_items
add constraint constraint_order_id
foreign key (order_id)
references orders (order_id);

alter table order_items
add constraint constraint_product_id
foreign key (product_id)
references products (product_id);