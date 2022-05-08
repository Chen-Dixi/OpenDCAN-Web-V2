CREATE USER `opendcan_web`@`%` IDENTIFIED BY 'password';
grant select, insert, delete, update on opendcan_v2.* to 'opendcan_web'@'%';
