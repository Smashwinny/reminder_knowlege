-- exercise/seed.sql — 给本地 D1 造混合源测试数据
-- 目的：验证 hype 的三大核心机制
--   ① 跨源评分归一化 scorePost（github/hf 原值, reddit*0.3, replicate^0.6）
--   ② BANNED_STRINGS 黑名单过滤
--   ③ created_at 时间窗过滤（past_day / past_week）
-- 现在时间 2026-10-03，past_week 窗口起点 ≈ 2026-09-26

DELETE FROM repositories;

-- ① 评分对比组（期望最终排序 gh-a > gh-b > reddit-hot > hf-model > repl-hot）
INSERT INTO repositories (id, source, username, name, description, stars, url, created_at, inserted_at) VALUES
 ('1','github','alice','gh-a','Raw 2000 stars github repo',2000,'https://github.com/alice/gh-a','2026-10-02T10:00:00Z',datetime('now')),
 ('2','github','bob','gh-b','Raw 1000 stars github repo',1000,'https://github.com/bob/gh-b','2026-10-02T11:00:00Z',datetime('now')),
 ('3','reddit','u/researcher','Hot thread with raw score 3000','/r/MachineLearning',3000,'https://www.reddit.com/r/MachineLearning/comments/abc','2026-10-02T12:00:00Z',datetime('now')),
 ('4','huggingface','org','hf-model','Model with 800 likes',800,'https://huggingface.co/org/hf-model','2026-10-02T13:00:00Z',datetime('now')),
 ('5','replicate','vendor','repl-hot','Model run 32000 times',32000,'https://replicate.com/vendor/repl-hot','2026-10-02T14:00:00Z',datetime('now'));

-- ② 黑名单组：stars 极高但命中 banned 串，期望被过滤不出现在榜单
INSERT INTO repositories (id, source, username, name, description, stars, url, created_at, inserted_at) VALUES
 ('6','github','spammer','moon-crypto-bot','best crypto signals',99999,'https://github.com/spammer/moon-crypto-bot','2026-10-02T15:00:00Z',datetime('now')),
 ('7','github','spammer','nft-minter','mint nft fast',88888,'https://github.com/spammer/nft-minter','2026-10-02T16:00:00Z',datetime('now'));

-- ③ 时间窗组：old-repo 建于 9 天前（任何窗口都不可见），day-old 建于 2 天前（past_week 可见 / past_day 不可见）
INSERT INTO repositories (id, source, username, name, description, stars, url, created_at, inserted_at) VALUES
 ('8','github','carol','old-repo','Created 9 days ago',5000,'https://github.com/carol/old-repo','2026-09-24T10:00:00Z',datetime('now')),
 ('9','github','dave','day-old','Created 2 days ago',600,'https://github.com/dave/day-old','2026-10-01T10:00:00Z',datetime('now'));
