-- opendcan_v2.task_record definition

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