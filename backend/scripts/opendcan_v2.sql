SET FOREIGN_KEY_CHECKS = 0;

-- opendcan_v2.model_record definition
DROP TABLE IF EXISTS `model_record`;
CREATE TABLE `model_record` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL COMMENT '所属用户名',
  `task_id` int NOT NULL COMMENT '所属task id',
  `file_path` varchar(128) DEFAULT NULL COMMENT '文件在系统中的路径位置, 包含文件名',
  `model_type` tinyint DEFAULT NULL COMMENT '模型类型, 1 PyTorch 2 Tensorflow 暂时用不到',
  `state` tinyint NOT NULL DEFAULT '2' COMMENT '1: READY 2:InQueue, 3:TRAINING, 4: Stoped;READY状态下才能被选择用于推理标注',
  `source_id` int DEFAULT NULL COMMENT '源域数据集id',
  `source_name` varchar(120) DEFAULT NULL COMMENT '源域数据集名称, 冗余字段',
  `target_id` int DEFAULT NULL COMMENT '目标域数据集id',
  `target_name` varchar(120) DEFAULT NULL COMMENT '目标域数据集名称, 冗余字段',
  `create_name` varchar(100) DEFAULT NULL COMMENT '上传数据集的人',
  `update_name` varchar(100) DEFAULT NULL COMMENT '更新数据集信息的人',
  `is_active` tinyint NOT NULL DEFAULT '0' COMMENT '1 active; 2 deleted',
  `create_time` bigint DEFAULT NULL,
  `update_time` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `model_record_idx_task_id_update_time` (`task_id`,`update_time`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `users`;
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
  UNIQUE KEY `users_email_IDX` (`email`) USING BTREE,
  UNIQUE KEY `users_username_IDX` (`username`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS 'source_dataset_record';
CREATE TABLE `source_dataset_record` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(120) DEFAULT NULL COMMENT '数据集名称',
  `description` varchar(800) DEFAULT NULL COMMENT '数据集详情描述',
  `file_path` varchar(128) DEFAULT NULL COMMENT '文件在系统中的路径位置',
  `state` tinyint NOT NULL DEFAULT '2' COMMENT '1: 可使用 2: 未准备好',
  `labels` varchar(1000) DEFAULT NULL COMMENT '标签列表的json字符串, 标签在列表中的位置即为标签id',
  `label_num` int NOT NULL DEFAULT '0' COMMENT '标签种类数量',
  `create_name` varchar(100) DEFAULT NULL COMMENT '上传数据集的人',
  `update_name` varchar(100) DEFAULT NULL COMMENT '最近更新数据集信息的人',
  `is_active` tinyint NOT NULL DEFAULT '0' COMMENT '1 active; 2 deleted',
  `create_time` bigint DEFAULT NULL,
  `update_time` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `source_dataset_record_idx_file_path` (`file_path`) USING BTREE,
  KEY `source_dataset_record_idx_update_time` (`update_time`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS 'target_dataset_record';
CREATE TABLE `target_dataset_record` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(120) DEFAULT NULL COMMENT '数据集名称',
  `description` varchar(800) DEFAULT NULL COMMENT '数据集详情描述',
  `file_path` varchar(128) DEFAULT NULL COMMENT '文件在系统中的路径位置',
  `username` varchar(100) NOT NULL COMMENT '本数据集属于哪个用户',
  `state` tinyint NOT NULL DEFAULT '2' COMMENT '1: 准备 2: 未准备好',
  `create_name` varchar(100) DEFAULT NULL COMMENT '上传数据集的人',
  `update_name` varchar(100) DEFAULT NULL COMMENT '更新数据集信息的人',
  `is_active` tinyint NOT NULL DEFAULT '0' COMMENT '1 active; 2 deleted',
  `create_time` bigint DEFAULT NULL,
  `update_time` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `target_dataset_record_file_path_IDX` (`file_path`) USING BTREE,
  KEY `target_dataset_record_idx_username_updatetime` (`username`, `update_time`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS 'task_record';
CREATE TABLE `task_record` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL COMMENT '任务名称',
  `username` varchar(100) NOT NULL COMMENT '本属于属于哪个用户',
  `state` tinyint NOT NULL DEFAULT '2' COMMENT '1: IDLE 2: TRAINING 3: READY',
  `source_id` int DEFAULT NULL COMMENT '源域数据集id',
  `source_name` varchar(120) DEFAULT NULL COMMENT '源域数据集名称, 冗余字段',
  `target_id` int DEFAULT NULL COMMENT '目标域数据集id',
  `target_name` varchar(120) DEFAULT NULL COMMENT '目标域数据集名称, 冗余字段',
  `create_name` varchar(100) DEFAULT NULL COMMENT '上传数据集的人',
  `update_name` varchar(100) DEFAULT NULL COMMENT '更新数据集信息的人',
  `is_active` tinyint NOT NULL DEFAULT '0' COMMENT '1 active; 2 deleted',
  `create_time` bigint DEFAULT NULL,
  `update_time` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `task_record_idx_username_updatetime` (`username`,`update_time`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;