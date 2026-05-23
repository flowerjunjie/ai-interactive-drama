-- 追更订阅表（drama_user_subscribe）
-- 注意：此表未在 drama_tables_mvp_mysql.sql 中定义，仅通过 ORM model 管理
-- 若表被删除，执行此文件重建
CREATE TABLE IF NOT EXISTS drama_user_subscribe (
  subscribe_id BIGINT NOT NULL AUTO_INCREMENT COMMENT '订阅ID',
  app_user_id BIGINT NOT NULL COMMENT '用户ID',
  drama_id BIGINT NOT NULL COMMENT '剧目ID',
  notify_enabled CHAR(1) NOT NULL DEFAULT '1' COMMENT '1开启追更通知 0关闭',
  create_time DATETIME NULL COMMENT '创建时间',
  PRIMARY KEY (subscribe_id),
  UNIQUE KEY uq_subscribe_user_drama (app_user_id, drama_id)
) ENGINE=InnoDB COMMENT='追更订阅';