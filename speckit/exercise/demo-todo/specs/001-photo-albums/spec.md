# Feature Specification: 照片相册整理器

**Feature Branch**: `001-photo-albums`

**Created**: 2026-10-03

**Status**: Draft

**Input**: User description: "Build a photo organizer with albums grouped by date and a tile preview of each album"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 按日期分组浏览相册 (Priority: P1)

用户打开应用，看到所有相册按拍摄日期分组（如"2026-09"），每组一个折叠区块。

**Why this priority**: 这是产品核心价值——没有分组浏览，后续功能无意义。

**Independent Test**: 导入 3 张不同月份的照片后，页面出现 2 个日期分组且各含正确照片。

**Acceptance Scenarios**:

1. **Given** 相册库里有 2026-08 和 2026-09 的照片，**When** 用户打开首页，**Then** 看到 2 个按月份倒序排列的分组
2. **Given** 某分组没有照片，**When** 用户打开首页，**Then** 该分组不显示

### User Story 2 - 相册瓷砖预览 (Priority: P2)

每个相册以瓷砖网格展示缩略图，点击进入大图查看。

**Why this priority**: 提升浏览体验，但不阻塞核心分组功能。

**Independent Test**: 含 5 张照片的相册以网格展示 5 个可点击缩略图。

**Acceptance Scenarios**:

1. **Given** 相册含 5 张照片，**When** 用户进入相册，**Then** 看到瓷砖网格且点击任一图可放大

### User Story 3 - 照片元数据本地存储 (Priority: P3)

照片本体留在本地磁盘，仅元数据（路径、拍摄时间、所在相册）存 SQLite。

**Why this priority**: 保证不复制文件、低占用，属工程约束而非用户可见功能。

**Independent Test**: 导入照片后磁盘无副本，SQLite 中有对应记录。

**Acceptance Scenarios**:

1. **Given** 用户导入本地照片，**When** 导入完成，**Then** SQLite metadata 表新增一条含 EXIF 时间的记录且原文件未被移动

## Requirements

- 照片不复制、不移动，原始文件只读
- 支持常见格式：JPEG / PNG / HEIC
- 无 EXIF 拍摄时间的照片按文件修改时间归组

## Review & Acceptance Checklist

- [ ] 每条用户故事可独立测试
- [ ] 分组规则无歧义（时区、无 EXIF 兜底）
