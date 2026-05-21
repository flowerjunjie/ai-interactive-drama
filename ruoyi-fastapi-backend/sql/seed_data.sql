-- AI Interactive Drama Seed Data
-- 创建时间: 2026-05-21
-- 用途: 数据库初始化/重建数据
-- 使用: mysql -u root -p ai_video < sql/seed_data.sql

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ============================================
-- 1. drama 表 - 6部短剧
-- ============================================
TRUNCATE TABLE drama;
INSERT INTO drama (title, cover_url, description, drama_type, status, sort, tags, heat) VALUES
('都市狂想', 'https://picsum.photos/seed/d1/400/600', '都市青年意外获得读心术，在职场与情感中层层闯关', 'urban', 'published', 10, '都市异能职场', 8500),
('古风奇缘', 'https://picsum.photos/seed/d2/400/600', '穿越古代成为王妃，宫廷权谋中寻找真爱', 'costume', 'published', 9, '古风穿越宫斗', 6200),
('浪漫满屋', 'https://picsum.photos/seed/d3/400/600', '欢喜冤家合租一屋檐下，日久生情的爆笑爱情', 'romance', 'published', 8, '甜宠合租都市', 9100),
('时光穿越', 'https://picsum.photos/seed/d4/400/600', '意外穿越到20年前，改写命运的奇幻之旅', 'fantasy', 'published', 7, '穿越悬疑', 7800),
('心跳职场', 'https://picsum.photos/seed/d5/400/600', '职场新人逆袭，成长与爱情并行', 'urban', 'published', 6, '职场成长', 7300),
('星际恋歌', 'https://picsum.photos/seed/d6/400/600', '跨越星系的爱情，宇宙级别的浪漫', 'sci_fi', 'published', 5, '科幻星际', 8600);

-- ============================================
-- 2. drama_video_node 表 - 视频节点
-- drama_id=1 is 都市狂想, 2 is 古风奇缘, etc.
-- ============================================
TRUNCATE TABLE drama_video_node;
INSERT INTO drama_video_node (drama_id, title, video_url, cover_url, duration_sec, episode_no, sort, is_entry, is_interactive, choice_trigger_sec, status, review_status) VALUES
-- Drama 1: 都市狂想 (4个节点, 2个interactive)
(1, '第1集-意外觉醒', 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8', 'https://picsum.photos/seed/n1/400/225', 120, 1, 1, '1', '0', NULL, 'published', 'approved'),
(1, '第2集-选择时刻', 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8', 'https://picsum.photos/seed/n2/400/225', 120, 2, 1, '0', '1', 30, 'published', 'approved'),
(1, '第3集-暗流涌动', 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8', 'https://picsum.photos/seed/n3/400/225', 120, 3, 2, '0', '1', 30, 'published', 'approved'),
(1, '第4集-结局', 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8', 'https://picsum.photos/seed/n4/400/225', 120, 4, 3, '0', '0', NULL, 'published', 'approved'),

-- Drama 2: 古风奇缘 (4个节点, 2个interactive)
(2, '第1集-穿越之初', 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8', 'https://picsum.photos/seed/n5/400/225', 120, 1, 1, '1', '0', NULL, 'published', 'approved'),
(2, '第2集-宫廷初入', 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8', 'https://picsum.photos/seed/n6/400/225', 120, 2, 1, '0', '1', 30, 'published', 'approved'),
(2, '第3集-权谋抉择', 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8', 'https://picsum.photos/seed/n7/400/225', 120, 3, 2, '0', '1', 30, 'published', 'approved'),
(2, '第4集-大结局', 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8', 'https://picsum.photos/seed/n8/400/225', 120, 4, 3, '0', '0', NULL, 'published', 'approved'),

-- Drama 3: 浪漫满屋 (3个节点, 1个interactive)
(3, '第1集-合租开始', 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8', 'https://picsum.photos/seed/n9/400/225', 120, 1, 1, '1', '0', NULL, 'published', 'approved'),
(3, '第2集-鸡飞狗跳', 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8', 'https://picsum.photos/seed/n10/400/225', 120, 2, 1, '0', '1', 30, 'published', 'approved'),
(3, '第3集-圆满结局', 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8', 'https://picsum.photos/seed/n11/400/225', 120, 3, 2, '0', '0', NULL, 'published', 'approved'),

-- Drama 4: 时光穿越 (3个节点, 1个interactive)
(4, '第1集-意外重生', 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8', 'https://picsum.photos/seed/n12/400/225', 120, 1, 1, '1', '0', NULL, 'published', 'approved'),
(4, '第2集-命运交叉', 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8', 'https://picsum.photos/seed/n13/400/225', 120, 2, 1, '0', '1', 30, 'published', 'approved'),
(4, '第3集-大结局', 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8', 'https://picsum.photos/seed/n14/400/225', 120, 3, 2, '0', '0', NULL, 'published', 'approved'),

-- Drama 5: 心跳职场 (3个节点, 1个interactive)
(5, '第1集-入职第一天', 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8', 'https://picsum.photos/seed/n15/400/225', 120, 1, 1, '1', '0', NULL, 'published', 'approved'),
(5, '第2集-转正之争', 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8', 'https://picsum.photos/seed/n16/400/225', 120, 2, 1, '0', '1', 30, 'published', 'approved'),
(5, '第3集-职场巅峰', 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8', 'https://picsum.photos/seed/n17/400/225', 120, 3, 2, '0', '0', NULL, 'published', 'approved'),

-- Drama 6: 星际恋歌 (4个节点, 2个interactive)
(6, '第1集-相遇', 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8', 'https://picsum.photos/seed/n18/400/225', 120, 1, 1, '1', '0', NULL, 'published', 'approved'),
(6, '第2集-选择', 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8', 'https://picsum.photos/seed/n19/400/225', 120, 2, 1, '0', '1', 30, 'published', 'approved'),
(6, '第3集-深入', 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8', 'https://picsum.photos/seed/n20/400/225', 120, 3, 2, '0', '1', 30, 'published', 'approved'),
(6, '第4集-告别', 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8', 'https://picsum.photos/seed/n21/400/225', 120, 4, 3, '0', '0', NULL, 'published', 'approved');

-- ============================================
-- 3. drama_video_choice 表 - 分支选项
-- node_id 2,3 are from drama 1; node_id 6,7 from drama 2; etc.
-- After INSERT, node_id mapping:
-- Drama 1: node 1=ep1, 2=ep2(interactive), 3=ep3(interactive), 4=ep4
-- Drama 2: node 5=ep1, 6=ep2(interactive), 7=ep3(interactive), 8=ep4
-- Drama 3: node 9=ep1, 10=ep2(interactive), 11=ep3
-- Drama 4: node 12=ep1, 13=ep2(interactive), 14=ep3
-- Drama 5: node 15=ep1, 16=ep2(interactive), 17=ep3
-- Drama 6: node 18=ep1, 19=ep2(interactive), 20=ep3(interactive), 21=ep4
-- ============================================
TRUNCATE TABLE drama_video_choice;
INSERT INTO drama_video_choice (node_id, label, next_node_id, sort) VALUES
-- Node 2 (Drama 1 - 第2集) 分支选项
(2, 'A: 接受安排', 3, 1),
(2, 'B: 自主创业', 4, 2),

-- Node 3 (Drama 1 - 第3集) 分支选项
(3, 'A: 留下来', 4, 1),
(3, 'B: 跳槽', 4, 2),

-- Node 6 (Drama 2 - 第2集) 分支选项
(6, 'A: 入宫选秀', 7, 1),
(6, 'B: 出宫创业', 8, 2),

-- Node 7 (Drama 2 - 第3集) 分支选项
(7, 'A: 争夺后位', 8, 1),
(7, 'B: 归隐山林', 8, 2),

-- Node 10 (Drama 3 - 第2集) 分支选项
(10, 'A: 表白', 11, 1),
(10, 'B: 继续暗恋', 11, 2),

-- Node 13 (Drama 4 - 第2集) 分支选项
(13, 'A: 改变历史', 14, 1),
(13, 'B: 顺其自然', 14, 2),

-- Node 16 (Drama 5 - 第2集) 分支选项
(16, 'A: 努力表现', 17, 1),
(16, 'B: 另寻高就', 17, 2),

-- Node 19 (Drama 6 - 第2集) 分支选项
(19, 'A: 留在舰队', 20, 1),
(19, 'B: 寻找真相', 21, 2),

-- Node 20 (Drama 6 - 第3集) 分支选项
(20, 'A: 接受使命', 21, 1),
(20, 'B: 回到过去', 21, 2);

-- ============================================
-- 4. drama_ad 表 - 广告数据
-- ============================================
TRUNCATE TABLE drama_ad;
INSERT INTO drama_ad (title, media_type, image_url, slot_type, weight, status) VALUES
('热门新剧推荐', 'image', 'https://picsum.photos/seed/ad1/400/225', 'feed', 1, '1'),
('古风穿越剧', 'image', 'https://picsum.photos/seed/ad2/400/225', 'feed', 2, '1'),
('甜宠剧推荐', 'image', 'https://picsum.photos/seed/ad3/400/225', 'feed', 3, '1');

SET FOREIGN_KEY_CHECKS = 1;