-- opendcan_v2.target_dataset_record definition

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