-- 规格对齐：重命名菜单 + 新增子菜单（在已执行 drama_platform_menu_mysql.sql 的库上执行一次）

UPDATE sys_menu SET menu_name = '用户评价审核' WHERE menu_id = '2304';

INSERT INTO sys_menu VALUES (
  '2320', '评论管理', '2300', '7', 'comment', 'drama/comment/index', '', 'DramaComment',
  1, 0, 'C', '0', '0', 'sdrama:comment:list', 'chat-dot-square', 'admin', sysdate(), '', NULL, ''
);
INSERT INTO sys_menu VALUES (
  '2321', '上传文件', '2300', '8', 'upload-file', 'drama/uploadFile/index', '', 'DramaUploadFile',
  1, 0, 'C', '0', '0', 'sdrama:upload:list', 'upload', 'admin', sysdate(), '', NULL, ''
);
INSERT INTO sys_menu VALUES (
  '2322', '视频审核', '2300', '9', 'video-audit', 'drama/videoAudit/index', '', 'DramaVideoAudit',
  1, 0, 'C', '0', '0', 'sdrama:video_audit:list', 'video-camera', 'admin', sysdate(), '', NULL, ''
);

INSERT INTO sys_menu VALUES ('2325', '评论删除', '2320', '1', '', '', '', '', 1, 0, 'F', '0', '0', 'sdrama:comment:remove', '#', 'admin', sysdate(), '', NULL, '');
INSERT INTO sys_menu VALUES ('2326', '评论屏蔽', '2320', '2', '', '', '', '', 1, 0, 'F', '0', '0', 'sdrama:comment:hide', '#', 'admin', sysdate(), '', NULL, '');

INSERT IGNORE INTO sys_role_menu (role_id, menu_id)
SELECT 2, m.menu_id FROM sys_menu m WHERE m.menu_id IN ('2320','2321','2322','2325','2326');
