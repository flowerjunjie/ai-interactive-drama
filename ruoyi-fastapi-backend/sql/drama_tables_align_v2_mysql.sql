-- 短剧 MVP 规格对齐增量 DDL（MySQL，可重复执行）
-- 新建库请直接使用 drama_tables_mvp_mysql.sql 全量 CREATE。
--
-- 手动执行（Navicat / MySQL Workbench / mysql CLI）：请整文件运行。
-- 若客户端不支持 DELIMITER，可用 Alembic：`alembic upgrade head`（revision 250516_drama_align）。

DROP PROCEDURE IF EXISTS proc_drama_align_v2;

DELIMITER //
CREATE PROCEDURE proc_drama_align_v2()
BEGIN
  DECLARE db VARCHAR(64);
  SET db = DATABASE();

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = db AND table_name = 'drama' AND column_name = 'tags') THEN
    ALTER TABLE drama ADD COLUMN tags VARCHAR(512) NULL COMMENT '标签 JSON 或逗号分隔';
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = db AND table_name = 'drama' AND column_name = 'heat') THEN
    ALTER TABLE drama ADD COLUMN heat INT NOT NULL DEFAULT 0 COMMENT '热度';
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = db AND table_name = 'drama_video_node' AND column_name = 'episode_no') THEN
    ALTER TABLE drama_video_node ADD COLUMN episode_no INT NULL COMMENT '集序号';
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = db AND table_name = 'drama_video_node' AND column_name = 'tos_key') THEN
    ALTER TABLE drama_video_node ADD COLUMN tos_key VARCHAR(512) NULL COMMENT 'TOS 对象键';
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = db AND table_name = 'drama_video_node' AND column_name = 'is_interactive') THEN
    ALTER TABLE drama_video_node ADD COLUMN is_interactive CHAR(1) NOT NULL DEFAULT '0' COMMENT '是否互动 0否1是';
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = db AND table_name = 'drama_video_node' AND column_name = 'choice_trigger_sec') THEN
    ALTER TABLE drama_video_node ADD COLUMN choice_trigger_sec DOUBLE NULL COMMENT '分支弹出时刻(秒)';
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = db AND table_name = 'drama_video_node' AND column_name = 'review_status') THEN
    ALTER TABLE drama_video_node ADD COLUMN review_status VARCHAR(32) NOT NULL DEFAULT 'pending' COMMENT 'pending/approved/rejected';
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = db AND table_name = 'drama_video_node' AND column_name = 'reject_reason') THEN
    ALTER TABLE drama_video_node ADD COLUMN reject_reason VARCHAR(500) NULL COMMENT '审核拒绝原因';
  END IF;

  IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = db AND table_name = 'drama_video_node' AND column_name = 'review_status') THEN
    UPDATE drama_video_node SET review_status = 'approved' WHERE status = 'published' AND review_status = 'pending';
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = db AND table_name = 'drama_video_choice' AND column_name = 'choice_code') THEN
    ALTER TABLE drama_video_choice ADD COLUMN choice_code VARCHAR(8) NULL COMMENT '选项编码如 A/B/C';
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = db AND table_name = 'drama_ad' AND column_name = 'media_type') THEN
    ALTER TABLE drama_ad ADD COLUMN media_type VARCHAR(16) NOT NULL DEFAULT 'image' COMMENT 'image/video';
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = db AND table_name = 'drama_ad' AND column_name = 'media_url') THEN
    ALTER TABLE drama_ad ADD COLUMN media_url VARCHAR(1024) NULL COMMENT '主素材 URL';
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = db AND table_name = 'drama_ad' AND column_name = 'cover_url') THEN
    ALTER TABLE drama_ad ADD COLUMN cover_url VARCHAR(1024) NULL COMMENT '视频封面';
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = db AND table_name = 'drama_ad' AND column_name = 'start_time') THEN
    ALTER TABLE drama_ad ADD COLUMN start_time DATETIME NULL COMMENT '生效开始';
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = db AND table_name = 'drama_ad' AND column_name = 'end_time') THEN
    ALTER TABLE drama_ad ADD COLUMN end_time DATETIME NULL COMMENT '生效结束';
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = db AND table_name = 'drama_ad' AND column_name = 'impression_count') THEN
    ALTER TABLE drama_ad ADD COLUMN impression_count BIGINT NOT NULL DEFAULT 0 COMMENT '曝光';
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = db AND table_name = 'drama_ad' AND column_name = 'click_count') THEN
    ALTER TABLE drama_ad ADD COLUMN click_count BIGINT NOT NULL DEFAULT 0 COMMENT '点击';
  END IF;

  IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = db AND table_name = 'drama_ad' AND column_name = 'media_url')
     AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = db AND table_name = 'drama_ad' AND column_name = 'image_url') THEN
    UPDATE drama_ad SET media_url = image_url WHERE media_url IS NULL AND image_url IS NOT NULL;
  END IF;

END //
DELIMITER ;

CALL proc_drama_align_v2();
DROP PROCEDURE IF EXISTS proc_drama_align_v2;
