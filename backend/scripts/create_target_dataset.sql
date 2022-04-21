-- opendcan_v2.target_dataset_record definition

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