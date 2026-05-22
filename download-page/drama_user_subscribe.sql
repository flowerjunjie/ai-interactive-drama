-- 追更订阅表 drama_user_subscribe
-- 用于用户追更剧目后获得新集更新通知
CREATE TABLE IF NOT EXISTS drama_user_subscribe (
    subscribe_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    app_user_id BIGINT NOT NULL COMMENT '用户ID',
    drama_id BIGINT NOT NULL COMMENT '剧目ID',
    notify_enabled CHAR(1) NOT NULL DEFAULT '1' COMMENT '1开启通知 0关闭',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_subscribe_user_drama (app_user_id, drama_id),
    KEY idx_app_user (app_user_id),
    KEY idx_drama (drama_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='追更订阅';
