-- opendcan_v2.target_dataset_record definition

CREATE TABLE `target_dataset_record` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(120) DEFAULT NULL COMMENT '数据集名称',
  `description` varchar(800) DEFAULT NULL COMMENT '数据集详情描述',
  `file_path` varchar(128) DEFAULT NULL COMMENT '文件在系统中的路径位置',
  `create_name` varchar(100) DEFAULT NULL COMMENT '上传数据集的人',
  `update_name` varchar(100) DEFAULT NULL COMMENT '更新数据集信息的人',
  `is_active` tinyint NOT NULL DEFAULT '0' COMMENT '1 active; 2 deleted',
  `create_time` bigint DEFAULT NULL,
  `update_time` bigint DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;