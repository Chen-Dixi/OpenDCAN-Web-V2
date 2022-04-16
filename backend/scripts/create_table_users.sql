-- opendcan_v2.users definition

CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(200) DEFAULT NULL,
  `username` varchar(100) DEFAULT NULL,
  `display_name` varchar(100) DEFAULT NULL,
  `hashed_password` varchar(100) DEFAULT NULL,
  `user_type` int DEFAULT '0' COMMENT '1: 管理员, 2:普通用户',
  `is_active` int NOT NULL DEFAULT '0' COMMENT '1 active; 2 disabled',
  `create_time` bigint DEFAULT NULL,
  `update_time` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_email_IDX` (`email`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;