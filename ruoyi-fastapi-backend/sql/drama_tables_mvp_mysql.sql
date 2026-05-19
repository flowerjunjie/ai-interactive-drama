-- 短剧 MVP 表结构（MySQL）；若已由 ORM create_all 建表可跳过
CREATE TABLE IF NOT EXISTS drama_app_user (
  user_id BIGINT NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  user_name VARCHAR(64) NOT NULL COMMENT '登录账号',
  nick_name VARCHAR(64) NOT NULL COMMENT '昵称',
  password VARCHAR(100) NOT NULL COMMENT '密码hash',
  avatar VARCHAR(512) DEFAULT '' COMMENT '头像',
  status CHAR(1) NOT NULL DEFAULT '0' COMMENT '0正常1停用',
  create_time DATETIME NULL,
  update_time DATETIME NULL,
  PRIMARY KEY (user_id),
  UNIQUE KEY uk_drama_app_user_name (user_name)
) ENGINE=InnoDB COMMENT '短剧 C 端用户';

CREATE TABLE IF NOT EXISTS drama (
  drama_id BIGINT NOT NULL AUTO_INCREMENT,
  title VARCHAR(200) NOT NULL,
  cover_url VARCHAR(1024) NULL,
  description TEXT NULL,
  drama_type VARCHAR(32) NOT NULL DEFAULT 'comic_drama',
  status VARCHAR(32) NOT NULL DEFAULT 'draft',
  sort INT NOT NULL DEFAULT 0,
  create_by VARCHAR(64) DEFAULT '',
  create_time DATETIME NULL,
  update_by VARCHAR(64) DEFAULT '',
  update_time DATETIME NULL,
  remark VARCHAR(500) NULL,
  tags VARCHAR(512) NULL COMMENT '标签 JSON 或逗号分隔',
  heat INT NOT NULL DEFAULT 0 COMMENT '热度',
  PRIMARY KEY (drama_id)
) ENGINE=InnoDB COMMENT '短剧';

CREATE TABLE IF NOT EXISTS drama_video_node (
  node_id BIGINT NOT NULL AUTO_INCREMENT,
  drama_id BIGINT NOT NULL,
  parent_node_id BIGINT NULL,
  title VARCHAR(200) NULL,
  video_url VARCHAR(1024) NULL,
  cover_url VARCHAR(1024) NULL,
  tos_key VARCHAR(512) NULL COMMENT 'TOS 对象键',
  duration_sec INT NULL,
  episode_no INT NULL COMMENT '集序号',
  sort INT NOT NULL DEFAULT 0,
  is_entry CHAR(1) NOT NULL DEFAULT '0',
  is_interactive CHAR(1) NOT NULL DEFAULT '0' COMMENT '互动节点',
  choice_trigger_sec DOUBLE NULL COMMENT '分支弹出时刻(秒)',
  status VARCHAR(32) NOT NULL DEFAULT 'draft',
  review_status VARCHAR(32) NOT NULL DEFAULT 'pending' COMMENT 'pending/approved/rejected',
  reject_reason VARCHAR(500) NULL COMMENT '审核拒绝原因',
  create_time DATETIME NULL,
  update_time DATETIME NULL,
  PRIMARY KEY (node_id),
  KEY idx_dvn_drama (drama_id)
) ENGINE=InnoDB COMMENT '剧情视频节点';

CREATE TABLE IF NOT EXISTS drama_video_choice (
  choice_id BIGINT NOT NULL AUTO_INCREMENT,
  node_id BIGINT NOT NULL,
  choice_code VARCHAR(8) NULL COMMENT '选项编码 A/B/C',
  label VARCHAR(200) NOT NULL,
  next_node_id BIGINT NOT NULL,
  sort INT NOT NULL DEFAULT 0,
  create_time DATETIME NULL,
  PRIMARY KEY (choice_id),
  KEY idx_dvc_node (node_id)
) ENGINE=InnoDB COMMENT '分支选项';

CREATE TABLE IF NOT EXISTS drama_video_review (
  review_id BIGINT NOT NULL AUTO_INCREMENT,
  app_user_id BIGINT NOT NULL,
  drama_id BIGINT NOT NULL,
  node_id BIGINT NULL,
  rating INT NULL,
  content TEXT NULL,
  status VARCHAR(32) NOT NULL DEFAULT 'pending',
  admin_remark VARCHAR(500) NULL,
  create_time DATETIME NULL,
  audit_time DATETIME NULL,
  PRIMARY KEY (review_id)
) ENGINE=InnoDB COMMENT '用户评价审核';

CREATE TABLE IF NOT EXISTS drama_ad (
  ad_id BIGINT NOT NULL AUTO_INCREMENT,
  title VARCHAR(200) NOT NULL,
  media_type VARCHAR(16) NOT NULL DEFAULT 'image' COMMENT 'image/video',
  media_url VARCHAR(1024) NULL COMMENT '主素材',
  image_url VARCHAR(1024) NULL COMMENT '兼容旧字段',
  cover_url VARCHAR(1024) NULL COMMENT '视频封面',
  link_url VARCHAR(1024) NULL,
  slot_type VARCHAR(32) NOT NULL DEFAULT 'feed',
  weight INT NOT NULL DEFAULT 0,
  start_time DATETIME NULL,
  end_time DATETIME NULL,
  impression_count BIGINT NOT NULL DEFAULT 0,
  click_count BIGINT NOT NULL DEFAULT 0,
  status CHAR(1) NOT NULL DEFAULT '0',
  create_time DATETIME NULL,
  PRIMARY KEY (ad_id)
) ENGINE=InnoDB COMMENT '短剧广告';

CREATE TABLE IF NOT EXISTS drama_user_watch_history (
  history_id BIGINT NOT NULL AUTO_INCREMENT,
  app_user_id BIGINT NOT NULL,
  drama_id BIGINT NOT NULL,
  node_id BIGINT NULL,
  progress_sec INT NOT NULL DEFAULT 0,
  update_time DATETIME NULL,
  PRIMARY KEY (history_id),
  UNIQUE KEY uq_drama_watch_user_drama (app_user_id, drama_id)
) ENGINE=InnoDB COMMENT '观看进度';

CREATE TABLE IF NOT EXISTS drama_user_favorite (
  fav_id BIGINT NOT NULL AUTO_INCREMENT,
  app_user_id BIGINT NOT NULL,
  drama_id BIGINT NOT NULL,
  create_time DATETIME NULL,
  PRIMARY KEY (fav_id),
  UNIQUE KEY uq_drama_fav_user_drama (app_user_id, drama_id)
) ENGINE=InnoDB COMMENT '收藏';

CREATE TABLE IF NOT EXISTS drama_user_like (
  like_id BIGINT NOT NULL AUTO_INCREMENT,
  app_user_id BIGINT NOT NULL,
  target_type VARCHAR(32) NOT NULL,
  target_id BIGINT NOT NULL,
  create_time DATETIME NULL,
  PRIMARY KEY (like_id),
  UNIQUE KEY uq_drama_like_target (app_user_id, target_type, target_id)
) ENGINE=InnoDB COMMENT '点赞';

CREATE TABLE IF NOT EXISTS drama_comment (
  comment_id BIGINT NOT NULL AUTO_INCREMENT,
  app_user_id BIGINT NOT NULL,
  drama_id BIGINT NOT NULL,
  node_id BIGINT NULL,
  content TEXT NOT NULL,
  status CHAR(1) NOT NULL DEFAULT '0',
  create_time DATETIME NULL,
  PRIMARY KEY (comment_id),
  KEY idx_dc_drama (drama_id)
) ENGINE=InnoDB COMMENT '评论';

CREATE TABLE IF NOT EXISTS drama_user_choice_log (
  log_id BIGINT NOT NULL AUTO_INCREMENT,
  app_user_id BIGINT NOT NULL,
  drama_id BIGINT NOT NULL,
  from_node_id BIGINT NULL,
  choice_id BIGINT NOT NULL,
  to_node_id BIGINT NOT NULL,
  create_time DATETIME NULL,
  PRIMARY KEY (log_id)
) ENGINE=InnoDB COMMENT '分支选择记录';

CREATE TABLE IF NOT EXISTS drama_upload_file (
  file_id BIGINT NOT NULL AUTO_INCREMENT,
  object_key VARCHAR(512) NOT NULL,
  bucket VARCHAR(256) NOT NULL,
  mime_type VARCHAR(128) NULL,
  size_bytes BIGINT NULL,
  drama_id BIGINT NULL,
  node_id BIGINT NULL,
  status VARCHAR(32) NOT NULL DEFAULT 'pending',
  create_by VARCHAR(64) DEFAULT '',
  create_time DATETIME NULL,
  PRIMARY KEY (file_id)
) ENGINE=InnoDB COMMENT '上传文件记录';

-- 初始化演示数据友好：已发布节点默认审核通过；广告 media_url 回填
UPDATE drama_video_node SET review_status = 'approved' WHERE status = 'published';
UPDATE drama_ad SET media_url = image_url WHERE media_url IS NULL AND image_url IS NOT NULL;
