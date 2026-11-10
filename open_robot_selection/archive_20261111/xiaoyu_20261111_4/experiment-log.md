# experiment-log：真实云端运行

运行日：2026-11-11（Asia/Shanghai）。CPU 元数据与 URDF 解析正运动学；没有真机、没有付费 API、没有下载 AgiBot 视频/parquet，也没有在 MuJoCo/PyBullet 中带网格加载。

## 六步主实验
完整命令、目的、结果与验证已写入指南第 9–10 页；下面保留实际标准输出，而非手写预期输出。

```text

=== 2026-11-11T01:22:32+0800 | python3 exercise/lab.py env ===
{
  "python": "3.13.5",
  "numpy": "2.5.4",
  "platform": "Linux-6.12.113+-x86_64-with-glibc2.41",
  "cwd": "/workspace/learn-batch/04-open-robots",
  "lab": "/workspace/learn-batch/04-open-robots/exercise",
  "cuda_devices": 0,
  "scope": "CPU metadata + URDF FK; no hardware, no paid API, no MuJoCo runtime required",
  "when": "2026-11-11T01:22:32+08:00"
}

=== 2026-11-11T01:22:32+0800 | python3 exercise/lab.py survey ===
{
  "n_post_robots": 18,
  "n_cached_repos": 21,
  "categories": {
    "人形": 4,
    "人形/双足": 1,
    "四足": 6,
    "机械臂": 3,
    "移动操作": 1,
    "移动平台": 3
  },
  "flags": {
    "api_license_unreliable": 4,
    "redirect": 2
  },
  "redirects": [
    {
      "requested": "OttoDIY/OttoDIY",
      "full_name": "OttoDIY/OttoNinja",
      "label": "Otto DIY site/repo"
    },
    {
      "requested": "PetoiCamp/OpenCat",
      "full_name": "PetoiCamp/OpenCat-Quadruped-Robot",
      "label": "Petoi Bittle / OpenCat"
    },
    {
      "requested": "isl-org/OpenBot",
      "full_name": "ob-f/OpenBot",
      "label": "OpenBot"
    }
  ],
  "table": [
    {
      "name": "Microban",
      "category": "人形",
      "repo": "Rhoban/microban",
      "requested": "Rhoban/microban",
      "redirected": false,
      "stars": 682,
      "branch": "main",
      "sha": "d0a128d180ecfce69eaaf31b295a0fce31280bfd",
      "created_at": "2026-05-06T11:13:44Z",
      "pushed_at": "2026-11-01T10:25:04Z",
      "license_api": "NOASSERTION",
      "note": "硬件 CC BY-NC-SA 4.0，软件 GPL-3.0"
    },
    {
      "name": "MiniLoong",
      "category": "人形",
      "repo": "loongOpen/MiniLoong",
      "requested": "loongOpen/MiniLoong",
      "redirected": false,
      "stars": 38,
      "branch": "main",
      "sha": "50d93a5912553d8c5bc568e497031a54aa938352",
      "created_at": "2025-12-17T07:25:23Z",
      "pushed_at": "2025-12-17T07:54:56Z",
      "license_api": "Apache-2.0",
      "note": "OpenLoong/青龙 Mini，GitHub 镜像 loongOpen/MiniLoong"
    },
    {
      "name": "Poppy Humanoid",
      "category": "人形",
      "repo": "poppy-project/poppy-humanoid",
      "requested": "poppy-project/poppy-humanoid",
      "redirected": false,
      "stars": 1103,
      "branch": "master",
      "sha": "d66c8fbd6aa3ebbf9e38399cc56aae3c155ee991",
      "created_at": "2015-01-09T10:23:33Z",
      "pushed_at": "2021-12-06T18:19:35Z",
      "license_api": null,
      "note": "硬件 CC BY-SA 4.0，软件 GPL-3.0；根目录无单一 LICENSE"
    },
    {
      "name": "Otto DIY",
      "category": "人形/双足",
      "repo": "OttoDIY/OttoDIYLib",
      "requested": "OttoDIY/OttoDIYLib",
      "redirected": false,
      "stars": 216,
      "branch": "main",
      "sha": "f384c00a641e11c8741487320c6f1d82ad72e6d5",
      "created_at": "2019-06-06T20:19:07Z",
      "pushed_at": "2024-06-08T00:54:34Z",
      "license_api": "GPL-3.0",
      "note": "软件库 GPL-3.0；OttoDIY/OttoDIY 现重定向到 OttoNinja，不是同一款机器人"
    },
    {
      "name": "pib",
      "category": "人形",
      "repo": "pib-rocks/pib-backend",
      "requested": "pib-rocks/pib-backend",
      "redirected": false,
      "stars": 14,
      "branch": "main",
      "sha": "1a35eb0266abcfb29e0030ecf83eb38747fc5b90",
      "created_at": "2024-02-15T08:58:08Z",
      "pushed_at": "2026-11-10T12:37:27Z",
      "license_api": "AGPL-3.0",
      "note": "软件 AGPL-3.0，STL 仓 GPL-3.0；官网 FAQ 写硬件也是 AGPL-3.0，与 STL 仓文件不一致"
    },
    {
      "name": "Mini Pupper",
      "category": "四足",
      "repo": "mangdangroboticsclub/mini_pupper",
      "requested": "mangdangroboticsclub/mini_pupper",
      "redirected": false,
      "stars": 1201,
      "branch": "main",
      "sha": "5a76f233f8626887d0942ed7ad2ce0083cc55f0a",
      "created_at": "2021-01-15T13:02:56Z",
      "pushed_at": "2026-11-06T02:53:51Z",
      "license_api": "Apache-2.0",
      "note": "Apache-2.0"
    },
    {
      "name": "Petoi Bittle",
      "category": "四足",
      "repo": "PetoiCamp/OpenCat-Quadruped-Robot",
      "requested": "PetoiCamp/OpenCat-Quadruped-Robot",
      "redirected": true,
      "stars": 5556,
      "branch": "main",
      "sha": "24563ca2e0218150f6299d013cd3a20c45433467",
      "created_at": "2021-01-03T15:42:00Z",
      "pushed_at": "2026-09-08T04:50:11Z",
      "license_api": "MIT",
      "note": "OpenCat 仓库已改名；MIT"
    },
    {
      "name": "Stanford Doggo",
      "category": "四足",
      "repo": "Nate711/StanfordDoggoProject",
      "requested": "Nate711/StanfordDoggoProject",
      "redirected": false,
      "stars": 2577,
      "branch": "master",
      "sha": "ce5716b5941739a006ec604669bca5676f265dc1",
      "created_at": "2018-09-13T04:43:31Z",
      "pushed_at": "2024-07-08T02:08:11Z",
      "license_api": "MIT",
      "note": "MIT；官网活动仓在 Nate711，不是 stanfordroboticsclub 下的旧路径"
    },
    {
      "name": "SpotMicro",
      "category": "四足",
      "repo": "mike4192/spotMicro",
      "requested": "mike4192/spotMicro",
      "redirected": false,
      "stars": 2163,
      "branch": "master",
      "sha": "2a34f5d303dff91b62180031b31ef512a672f3c3",
      "created_at": "2020-03-31T00:54:50Z",
      "pushed_at": "2021-03-20T21:07:18Z",
      "license_api": "MIT",
      "note": "该仓是社区 ROS 实现（MIT）。原帖署名的设计是 Deok-yeon Kim / KDY0523，CC BY 3.0，不在该 GitHub 仓"
    },
    {
      "name": "OpenQuadruped",
      "category": "四足",
      "repo": "adham-elarabawy/open-quadruped",
      "requested": "adham-elarabawy/open-quadruped",
      "redirected": false,
      "stars": 524,
      "branch": "master",
      "sha": "b0ab4fa599f94460828bf3aa4514240ae917ed38",
      "created_at": "2020-05-12T13:24:52Z",
      "pushed_at": "2024-08-23T17:10:44Z",
      "license_api": "NOASSERTION",
      "note": "根目录 LICENSE 以 MIT 开头；GitHub API 标记为 NOASSERTION"
    },
    {
      "name": "Puguette",
      "category": "四足",
      "repo": "haruto89610/puguette",
      "requested": "haruto89610/puguette",
      "redirected": false,
      "stars": 18,
      "branch": "main",
      "sha": "2694b129a74ee80bfc4f2c607e402c4d7bc4480f",
      "created_at": "2021-11-02T09:51:31Z",
      "pushed_at": "2024-03-13T20:57:51Z",
      "license_api": "MIT",
      "note": "MIT"
    },
    {
      "name": "SO-ARM100",
      "category": "机械臂",
      "repo": "TheRobotStudio/SO-ARM100",
      "requested": "TheRobotStudio/SO-ARM100",
      "redirected": false,
      "stars": 8074,
      "branch": "main",
      "sha": "a758567c3978dfeefe282ede0500085a48fe8f78",
      "created_at": "2024-05-10T22:07:52Z",
      "pushed_at": "2026-10-06T07:26:52Z",
      "license_api": "Apache-2.0",
      "note": "Apache-2.0；当前 README 以 SO-101 为主，SO-100 文档标为 deprecated"
    },
    {
      "name": "RoArm-M2",
      "category": "机械臂",
      "repo": "waveshareteam/roarm_m2",
      "requested": "waveshareteam/roarm_m2",
      "redirected": false,
      "stars": 40,
      "branch": "main",
      "sha": "c6ccc5bda2eb92df2f0850d3e63cc42b81557f4f",
      "created_at": "2024-05-10T09:31:05Z",
      "pushed_at": "2025-01-13T13:54:01Z",
      "license_api": "AGPL-3.0",
      "note": "AGPL-3.0"
    },
    {
      "name": "OpenMANIPULATOR-X",
      "category": "机械臂",
      "repo": "ROBOTIS-GIT/open_manipulator",
      "requested": "ROBOTIS-GIT/open_manipulator",
      "redirected": false,
      "stars": 678,
      "branch": "main",
      "sha": "7addeda59bbdf9c84247b16e2c3350880623f394",
      "created_at": "2017-01-20T08:25:15Z",
      "pushed_at": "2026-11-10T09:34:03Z",
      "license_api": "Apache-2.0",
      "note": "Apache-2.0"
    },
    {
      "name": "LeKiwi",
      "category": "移动操作",
      "repo": "SIGRobotics-UIUC/LeKiwi",
      "requested": "SIGRobotics-UIUC/LeKiwi",
      "redirected": false,
      "stars": 1515,
      "branch": "main",
      "sha": "efa608d7ee5a495a4803b1d28cd0c955b4f1e033",
      "created_at": "2025-02-04T22:01:58Z",
      "pushed_at": "2026-08-05T09:25:59Z",
      "license_api": "Apache-2.0",
      "note": "Apache-2.0；移动底盘+臂，不宜只算纯机械臂或纯移动平台"
    },
    {
      "name": "TurtleBot3 Burger",
      "category": "移动平台",
      "repo": "ROBOTIS-GIT/turtlebot3",
      "requested": "ROBOTIS-GIT/turtlebot3",
      "redirected": false,
      "stars": 2103,
      "branch": "main",
      "sha": "faf695dfffe2a264f6149091fdf241f825169245",
      "created_at": "2016-06-21T07:14:22Z",
      "pushed_at": "2026-11-10T08:49:37Z",
      "license_api": "Apache-2.0",
      "note": "Apache-2.0"
    },
    {
      "name": "OpenBot",
      "category": "移动平台",
      "repo": "ob-f/OpenBot",
      "requested": "ob-f/OpenBot",
      "redirected": true,
      "stars": 3658,
      "branch": "master",
      "sha": "db044a7d2e50d204cf6e6f9dc80492a484ad5441",
      "created_at": "2020-07-31T09:46:23Z",
      "pushed_at": "2026-11-04T14:53:34Z",
      "license_api": "MIT",
      "note": "MIT；isl-org/OpenBot 重定向至此"
    },
    {
      "name": "Duckiebot",
      "category": "移动平台",
      "repo": "duckietown/Hardware",
      "requested": "duckietown/Hardware",
      "redirected": false,
      "stars": 0,
      "branch": "master",
      "sha": "b31bff1a557aca709215197417bb3cedf27c2bb4",
      "created_at": "2018-09-25T12:45:59Z",
      "pushed_at": "2018-09-25T12:53:55Z",
      "license_api": "NOASSERTION",
      "note": "Hardware 仓 LICENSE.pdf 为 Software Terms of Use v1.2，禁止未经授权的商业使用，不是 OSI 开源许可"
    }
  ],
  "scope": "GitHub 公开 API 元数据 + git ls-remote SHA + 已读 LICENSE 注释；不是法律意见，也不是 BOM/价格审计"
}

=== 2026-11-11T01:22:32+0800 | python3 exercise/lab.py licenses ===
{
  "n_findings": 20,
  "n_need_manual_read": 7,
  "api_or_scope_cautions": [
    {
      "repo": "Rhoban/microban",
      "api": "NOASSERTION",
      "file": "LICENSE 首部声明硬件 CC BY-NC-SA 4.0、软件 GPL-3.0"
    },
    {
      "repo": "poppy-project/poppy-humanoid",
      "api": null,
      "file": "hardware/LICENSE.md = CC BY-SA 4.0；software/LICENSE = GPL-3.0；根目录无 LICENSE"
    },
    {
      "repo": "OttoDIY/OttoNinja",
      "api": "MIT",
      "file": "由 OttoDIY/OttoDIY 重定向得到，是另一款机器人，不能当作 Otto DIY 本体许可"
    },
    {
      "repo": "pib-rocks/pib-stls",
      "api": "GPL-3.0",
      "file": "LICENSE.txt 为 GPL-3.0，与 FAQ「硬件 AGPL-3.0」表述不一致"
    },
    {
      "repo": "mike4192/spotMicro",
      "api": "MIT",
      "file": "LICENSE 为 MIT，覆盖该软件仓，不自动覆盖 Thingiverse 设计"
    },
    {
      "repo": "adham-elarabawy/open-quadruped",
      "api": "NOASSERTION",
      "file": "LICENSE 以 MIT License 开头，API 未识别为 MIT"
    },
    {
      "repo": "duckietown/Hardware",
      "api": "NOASSERTION",
      "file": "LICENSE.pdf 是 Software Terms of Use v1.2 摘要：允许个人教育/认证高校课程/研究（需署名），明确禁止未经书面授权的商业使用"
    }
  ],
  "commercial_caution": [
    "Rhoban/microban 硬件 NC",
    "pib / RoArm-M2 的 AGPL 对网络服务有源码提供义务",
    "Duckiebot 非商用条款",
    "AgiBot World 2026 数据集 CC BY-NC-SA 4.0（与 18 个机器人清单是不同对象）"
  ],
  "findings": [
    {
      "repo": "Rhoban/microban",
      "api": "NOASSERTION",
      "file": "LICENSE 首部声明硬件 CC BY-NC-SA 4.0、软件 GPL-3.0"
    },
    {
      "repo": "loongOpen/MiniLoong",
      "api": "Apache-2.0",
      "file": "LICENSE 为 Apache 2.0 全文"
    },
    {
      "repo": "poppy-project/poppy-humanoid",
      "api": null,
      "file": "hardware/LICENSE.md = CC BY-SA 4.0；software/LICENSE = GPL-3.0；根目录无 LICENSE"
    },
    {
      "repo": "OttoDIY/OttoDIYLib",
      "api": "GPL-3.0",
      "file": "LICENSE 为 GPL-3.0"
    },
    {
      "repo": "OttoDIY/OttoNinja",
      "api": "MIT",
      "file": "由 OttoDIY/OttoDIY 重定向得到，是另一款机器人，不能当作 Otto DIY 本体许可"
    },
    {
      "repo": "pib-rocks/pib-backend",
      "api": "AGPL-3.0",
      "file": "LICENSE 为 AGPL-3.0"
    },
    {
      "repo": "pib-rocks/pib-stls",
      "api": "GPL-3.0",
      "file": "LICENSE.txt 为 GPL-3.0，与 FAQ「硬件 AGPL-3.0」表述不一致"
    },
    {
      "repo": "mangdangroboticsclub/mini_pupper",
      "api": "Apache-2.0",
      "file": "LICENSE 为 Apache 2.0"
    },
    {
      "repo": "PetoiCamp/OpenCat-Quadruped-Robot",
      "api": "MIT",
      "file": "LICENSE 为 MIT；由 PetoiCamp/OpenCat 改名"
    },
    {
      "repo": "Nate711/StanfordDoggoProject",
      "api": "MIT",
      "file": "LICENSE 为 MIT"
    },
    {
      "repo": "mike4192/spotMicro",
      "api": "MIT",
      "file": "LICENSE 为 MIT，覆盖该软件仓，不自动覆盖 Thingiverse 设计"
    },
    {
      "repo": "adham-elarabawy/open-quadruped",
      "api": "NOASSERTION",
      "file": "LICENSE 以 MIT License 开头，API 未识别为 MIT"
    },
    {
      "repo": "haruto89610/puguette",
      "api": "MIT",
      "file": "LICENSE 为 MIT"
    },
    {
      "repo": "TheRobotStudio/SO-ARM100",
      "api": "Apache-2.0",
      "file": "LICENSE 为 Apache 2.0"
    },
    {
      "repo": "waveshareteam/roarm_m2",
      "api": "AGPL-3.0",
      "file": "LICENSE 为 AGPL-3.0"
    },
    {
      "repo": "ROBOTIS-GIT/open_manipulator",
      "api": "Apache-2.0",
      "file": "LICENSE 为 Apache 2.0"
    },
    {
      "repo": "SIGRobotics-UIUC/LeKiwi",
      "api": "Apache-2.0",
      "file": "LICENSE.txt 为 Apache 2.0"
    },
    {
      "repo": "ROBOTIS-GIT/turtlebot3",
      "api": "Apache-2.0",
      "file": "LICENSE 为 Apache 2.0"
    },
    {
      "repo": "ob-f/OpenBot",
      "api": "MIT",
      "file": "LICENSE 为 MIT"
    },
    {
      "repo": "duckietown/Hardware",
      "api": "NOASSERTION",
      "file": "LICENSE.pdf 是 Software Terms of Use v1.2 摘要：允许个人教育/认证高校课程/研究（需署名），明确禁止未经书面授权的商业使用"
    }
  ],
  "claim": "GitHub license API 不能替代打开 LICENSE 文件；设计仓与软件仓可能不是同一许可"
}

=== 2026-11-11T01:22:32+0800 | python3 exercise/lab.py agibot ===
{
  "dataset": "agibot-world/AgiBotWorld2026",
  "dataset_sha": "95b159a10305a0385f369aba5d4b16242526d17b",
  "dataset_last_modified_utc": "2026-10-24T13:41:37Z",
  "license": "CC BY-NC-SA 4.0",
  "theme": "Physical Reasoning / Release 4, folder PhysicalReasoning/opensourcev4-20261001 and 20261003",
  "verification_receipt": {
    "ok": true,
    "products": 98,
    "completedEpisodes": 8146,
    "preservedEpisodes": 126,
    "verifiedInSegmentElements": 1434686,
    "supplementalElements": 31,
    "opaqueFieldsPreserved": true,
    "outputInfoBytes": 792269339
  },
  "export_readme": "原 LeRobot 相对路径的未压缩 meta/info.json 发布。仅更新快照中人工完成的 Episode；其余保留源 OSS 当前标注。\n视频、parquet、原文本/分段/相机和 audit/brush 不变。当前完成凭据见 completions.json。\n原格式无法容纳的元素见 additional-annotations.json；覆盖 info.json 不会加载这些元素。\n须存在 publication.json 且核验其中的完整文件 SHA256 清单，才是成功发布。\n应用到下游前比对 manifest 的 originalSha256，备份原文件；不匹配时先做合并，不能盲目覆盖。",
  "completions": {
    "file": "/workspace/learn-batch/04-open-robots/sources/hf/PhysicalReasoning__.dataset_build__snapshot___datahub_export__completions.json",
    "sha256": "e07de62ec7da56ef8736afdbfd89b6a055030c8830f0ba685a6a42fc34e85089",
    "format": "datahub-completion-receipts-v1",
    "n_items": 8146,
    "isResultSucceed": {
      "False": 8146
    },
    "present": {
      "False": 8146
    },
    "n_tasks": 18,
    "interpretation": "全部 8146 条收据的 isResultSucceed 与 present 都是 false。这更像未填写的 interval 占位，不能当成 8146 次任务失败。成功/失败要以 info.json 的 key_frame.frame_type_name 与 frame_detail 为准。"
  },
  "sample_info": {
    "file": "/workspace/learn-batch/04-open-robots/sources/hf/info-samples/task_100347_02_info.json",
    "sha256": "bf65894cfeaa944ae5b51073ee8d9c1f5df8c292dea99cd01f016d837c9bd3cc",
    "bytes": 4586365,
    "robot_type": "g2a",
    "codebase_version": "v2.1",
    "total_episodes": 170,
    "total_frames": 75828,
    "fps": 30,
    "n_keyframe_entries": 167,
    "frame_type_name": {
      "Success Frame": 167
    },
    "entries_with_error_cause": 0,
    "entries_with_restorable": 0,
    "comments": {
      "Command executed successfully": 167
    },
    "schema_keys": [
      "affordance_annotations",
      "camera_parameters",
      "chunks_size",
      "codebase_version",
      "data_path",
      "data_version",
      "features",
      "fps",
      "h5_path",
      "instruction_segments",
      "key_frame",
      "robot_type",
      "splits",
      "take_over",
      "total_chunks",
      "total_episodes",
      "total_frames",
      "total_tasks",
      "total_videos",
      "video_path"
    ],
    "has_take_over": true,
    "take_over_nonempty": 170,
    "instruction_segment_episodes": 170,
    "affordance_schema": "lerobot_affordance_annotations_v1"
  },
  "info_scan": {
    "files_ok": 98,
    "files_fail": [],
    "n_keyframe_entries": 8263,
    "frame_type_name": {
      "Success Frame": 8259,
      "Error Frame": 2,
      "Intervention Frame": 2
    },
    "files_with_error_frame": 2,
    "has_error_cause_entries": 2,
    "error_causes": {
      "Operation Process Issue - Operation Pause": 1,
      "Operation process problem - Operation pause": 1
    },
    "restorable": {
      "True": 2
    },
    "task_frame_is_result_succeed": {},
    "retry_note": "9 SSL failures retried with curl --retry 5; recovered added to per_file",
    "n_per_file": 98,
    "by_task": {
      "100347": {
        "Success Frame": 298
      },
      "100448": {
        "Success Frame": 646
      },
      "104212": {
        "Success Frame": 129
      },
      "104214": {
        "Success Frame": 169
      },
      "111349": {
        "Success Frame": 550
      },
      "69701": {
        "Success Frame": 620
      },
      "75089": {
        "Success Frame": 560
      },
      "75271": {
        "Success Frame": 495
      },
      "75540": {
        "Success Frame": 476
      },
      "86305": {
        "Success Frame": 701
      },
      "86632": {
        "Success Frame": 372,
        "Error Frame": 1
      },
      "87252": {
        "Success Frame": 608,
        "Intervention Frame": 2
      },
      "87261": {
        "Success Frame": 700
      },
      "87262": {
        "Success Frame": 699
      },
      "87264": {
        "Success Frame": 279
      },
      "87265": {
        "Success Frame": 402
      },
      "87266": {
        "Success Frame": 200
      },
      "96812": {
        "Success Frame": 355,
        "Error Frame": 1
      }
    }
  },
  "info_scan_complete": true,
  "schema_documented_fields": {
    "key_frame.frame_type_name": [
      "Error Frame",
      "Success Frame",
      "Intervention Frame",
      "Single Frame",
      "2D Bounding Box",
      "Task Frame"
    ],
    "frame_detail.error_cause": "documented in README, may be absent in actual Release 4 entries",
    "frame_detail.restorable": "documented in README, may be absent in actual Release 4 entries",
    "frame_detail.is_result_succeed": "documented on Task Frame examples"
  }
}

=== 2026-11-11T01:22:33+0800 | python3 exercise/lab.py fk ===
{
  "highlights": {
    "so100_home_all_child_frames": {
      "lower_arm": [
        0.0,
        0.040188,
        0.120691
      ],
      "gripper": [
        0.0,
        -0.14663,
        0.136274
      ],
      "upper_arm": [
        0.0,
        -0.075799,
        0.119
      ],
      "jaw": [
        -0.0,
        -0.176386,
        0.147134
      ],
      "wrist": [
        0.0,
        -0.090002,
        0.156406
      ],
      "shoulder": [
        0.0,
        -0.0452,
        0.0165
      ]
    },
    "so101_home_selected": {
      "base_link": [
        0.0,
        0.0,
        0.0
      ],
      "wrist_link": [
        0.232134,
        -0.018277,
        0.23437
      ],
      "gripper_link": [
        0.293234,
        -0.000177,
        0.23437
      ],
      "gripper_frame_link": [
        0.391361,
        -9e-06,
        0.22647
      ],
      "moving_jaw_so101_v1_link": [
        0.316634,
        0.017618,
        0.255461
      ]
    },
    "burger_sensor_frames": {
      "base_footprint": [
        0.0,
        0.0,
        0.0
      ],
      "base_link": [
        0.0,
        0.0,
        0.01
      ],
      "wheel_left_link": [
        0.0,
        0.08,
        0.033
      ],
      "wheel_right_link": [
        0.0,
        -0.08,
        0.033
      ],
      "caster_back_link": [
        -0.081,
        0.0,
        0.006
      ],
      "imu_link": [
        -0.032,
        0.0,
        0.078
      ],
      "base_scan": [
        -0.032,
        0.0,
        0.182
      ]
    },
    "omx_home": {
      "world": [
        0.0,
        0.0,
        0.0
      ],
      "link1": [
        0.0,
        0.0,
        0.0
      ],
      "link2": [
        0.012,
        0.0,
        0.0
      ],
      "link3": [
        0.012,
        0.0,
        0.0595
      ],
      "link4": [
        0.036,
        0.0,
        0.1875
      ],
      "link5": [
        0.16,
        0.0,
        0.1875
      ],
      "gripper_left_link": [
        0.2417,
        0.021,
        0.1875
      ],
      "gripper_right_link": [
        0.2417,
        -0.021,
        0.1875
      ],
      "end_effector_link": [
        0.286,
        0.0,
        0.1875
      ]
    },
    "burger_lidar_invariant_to_wheel": true,
    "scope": "纯解析正运动学，未加载网格、未做碰撞/动力学、未运行 MuJoCo/PyBullet。缺网格不阻止关节链计算。实物复刻与标定待验证。"
  },
  "models": {
    "so100": {
      "file": "so100.urdf",
      "sha256": "f7050417ebbb79358f113ddd4bca2b457b2c6d5048193331db5a04a0066439ed",
      "n_links": 7,
      "n_joints": 6,
      "movable": [
        {
          "name": "shoulder_pan",
          "type": "revolute",
          "parent": "base",
          "child": "shoulder",
          "axis": [
            0.0,
            1.0,
            0.0
          ],
          "origin_xyz": [
            0.0,
            -0.0452,
            0.0165
          ],
          "limit": {
            "lower": "-2",
            "upper": "2",
            "effort": "35",
            "velocity": "1"
          }
        },
        {
          "name": "shoulder_lift",
          "type": "revolute",
          "parent": "shoulder",
          "child": "upper_arm",
          "axis": [
            1.0,
            0.0,
            0.0
          ],
          "origin_xyz": [
            0.0,
            0.1025,
            0.0306
          ],
          "limit": {
            "lower": "0",
            "upper": "3.5",
            "effort": "35",
            "velocity": "1"
          }
        },
        {
          "name": "elbow_flex",
          "type": "revolute",
          "parent": "upper_arm",
          "child": "lower_arm",
          "axis": [
            1.0,
            0.0,
            0.0
          ],
          "origin_xyz": [
            0.0,
            0.11257,
            0.028
          ],
          "limit": {
            "lower": "-3.14158",
            "upper": "0",
            "effort": "35",
            "velocity": "1"
          }
        },
        {
          "name": "wrist_flex",
          "type": "revolute",
          "parent": "lower_arm",
          "child": "wrist",
          "axis": [
            1.0,
            0.0,
            0.0
          ],
          "origin_xyz": [
            0.0,
            0.0052,
            0.1349
          ],
          "limit": {
            "lower": "-2.5",
            "upper": "1.2",
            "effort": "35",
            "velocity": "1"
          }
        },
        {
          "name": "wrist_roll",
          "type": "revolute",
          "parent": "wrist",
          "child": "gripper",
          "axis": [
            0.0,
            1.0,
            0.0
          ],
          "origin_xyz": [
            0.0,
            -0.0601,
            0.0
          ],
          "limit": {
            "lower": "-3.14158",
            "upper": "3.14158",
            "effort": "35",
            "velocity": "1"
          }
        },
        {
          "name": "gripper",
          "type": "revolute",
          "parent": "gripper",
          "child": "jaw",
          "axis": [
            0.0,
            0.0,
            1.0
          ],
          "origin_xyz": [
            -0.0202,
            -0.0244,
            0.0
          ],
          "limit": {
            "lower": "-0.2",
            "upper": "2.0",
            "effort": "35",
            "velocity": "1"
          }
        }
      ],
      "cases": [
        {
          "case": "home_zero",
          "q": {},
          "frames": {
            "lower_arm": [
              0.0,
              0.04018834565650026,
              0.1206910536325244
            ],
            "gripper": [
              0.0,
              -0.14662961436296498,
              0.13627419998189816
            ],
            "upper_arm": [
              0.0,
              -0.07579935150291064,
              0.11900019359787238
            ],
            "jaw": [
              -1.2780125691270306e-07,
              -0.17638646269829736,
              0.1471337569310418
            ],
            "wrist": [
              0.0,
              -0.09000179694127353,
              0.15640627126270723
            ],
            "shoulder": [
              0.0,
              -0.0452,
              0.0165
            ]
          }
        },
        {
          "case": "shoulder_pan_90deg",
          "q": {
            "shoulder_pan": 1.5707963267948966
          },
          "frames": {
            "lower_arm": [
              -0.08538768645936487,
              -0.04519934080115565,
              0.12069159386290333
            ],
            "gripper": [
              0.10143037214773219,
              -0.04519924221726288,
              0.1362735582527373
            ],
            "upper_arm": [
              0.0306,
              -0.04519935150352309,
              0.11899999999794854
            ],
            "jaw": [
              0.1311872891886585,
              -0.04519930131352143,
              0.14713292693677862
            ],
            "wrist": [
              0.044802682098659924,
              -0.04519911484351032,
              0.15640598780532677
            ],
            "shoulder": [
              0.0,
              -0.0452,
              0.0165
            ]
          }
        },
        {
          "case": "elbow_neg90",
          "q": {
            "elbow_flex": -1.5707963267948966
          },
          "frames": {
            "lower_arm": [
              0.0,
              0.04018834565650026,
              0.1206910536325244
            ],
            "gripper": [
              0.0,
              0.05577149200587403,
              0.3075090136519897
            ],
            "upper_arm": [
              0.0,
              -0.07579935150291064,
              0.11900019359787238
            ],
            "jaw": [
              -1.2780125691270306e-07,
              0.06663104895501766,
              0.33726586198732206
            ],
            "wrist": [
              0.0,
              0.07590356328668309,
              0.2508811962302982
            ],
            "shoulder": [
              0.0,
              -0.0452,
              0.0165
            ]
          }
        }
      ]
    },
    "so101_new_calib": {
      "file": "so101_new_calib.urdf",
      "sha256": "3a65d2d35e68a8d2f0c2cc176d19b884506543c93ba72980145b80abe276022c",
      "n_links": 8,
      "n_joints": 7,
      "movable": [
        {
          "name": "gripper",
          "type": "revolute",
          "parent": "gripper_link",
          "child": "moving_jaw_so101_v1_link",
          "axis": [
            0.0,
            0.0,
            1.0
          ],
          "origin_xyz": [
            0.0202,
            0.0188,
            -0.0234
          ],
          "limit": {
            "lower": "-0.174533",
            "upper": "1.74533",
            "effort": "10",
            "velocity": "10"
          }
        },
        {
          "name": "wrist_roll",
          "type": "revolute",
          "parent": "wrist_link",
          "child": "gripper_link",
          "axis": [
            0.0,
            0.0,
            1.0
          ],
          "origin_xyz": [
            5.55112e-17,
            -0.0611,
            0.0181
          ],
          "limit": {
            "lower": "-2.74385",
            "upper": "2.84121",
            "effort": "10",
            "velocity": "10"
          }
        },
        {
          "name": "wrist_flex",
          "type": "revolute",
          "parent": "lower_arm_link",
          "child": "wrist_link",
          "axis": [
            0.0,
            0.0,
            1.0
          ],
          "origin_xyz": [
            -0.1349,
            0.0052,
            3.62355e-17
          ],
          "limit": {
            "lower": "-1.65806",
            "upper": "1.65806",
            "effort": "10",
            "velocity": "10"
          }
        },
        {
          "name": "elbow_flex",
          "type": "revolute",
          "parent": "upper_arm_link",
          "child": "lower_arm_link",
          "axis": [
            0.0,
            0.0,
            1.0
          ],
          "origin_xyz": [
            -0.11257,
            -0.028,
            1.73763e-16
          ],
          "limit": {
            "lower": "-1.69",
            "upper": "1.69",
            "effort": "10",
            "velocity": "10"
          }
        },
        {
          "name": "shoulder_lift",
          "type": "revolute",
          "parent": "shoulder_link",
          "child": "upper_arm_link",
          "axis": [
            0.0,
            0.0,
            1.0
          ],
          "origin_xyz": [
            -0.0303992,
            -0.0182778,
            -0.0542
          ],
          "limit": {
            "lower": "-1.74533",
            "upper": "1.74533",
            "effort": "10",
            "velocity": "10"
          }
        },
        {
          "name": "shoulder_pan",
          "type": "revolute",
          "parent": "base_link",
          "child": "shoulder_link",
          "axis": [
            0.0,
            0.0,
            1.0
          ],
          "origin_xyz": [
            0.0388353,
            -8.97657e-09,
            0.0624
          ],
          "limit": {
            "lower": "-1.91986",
            "upper": "1.91986",
            "effort": "10",
            "velocity": "10"
          }
        }
      ],
      "cases": [
        {
          "case": "home_zero",
          "q": {},
          "frames": {
            "base_link": [
              0.0,
              0.0,
              0.0
            ],
            "shoulder_link": [
              0.0388353,
              -8.97657e-09,
              0.0624
            ],
            "upper_arm_link": [
              0.06923454850205815,
              -0.01827787213400125,
              0.11659995149802566
            ],
            "lower_arm_link": [
              0.09723413500940303,
              -0.01827799369971717,
              0.2291700543468857
            ],
            "wrist_link": [
              0.2321341350067397,
              -0.018277154013682226,
              0.23437005434818228
            ],
            "gripper_link": [
              0.29323402049011704,
              -0.00017676744753576668,
              0.23437032681134062
            ],
            "gripper_frame_link": [
              0.39136147022015794,
              -9.212063114602824e-06,
              0.22646971024033283
            ],
            "moving_jaw_so101_v1_link": [
              0.3166337054106509,
              0.01761820217711514,
              0.25546141027515284
            ]
          }
        },
        {
          "case": "shoulder_pan_90deg",
          "q": {
            "shoulder_pan": 1.5707963267948966
          },
          "frames": {
            "base_link": [
              0.0,
              0.0,
              0.0
            ],
            "shoulder_link": [
              0.0388353,
              -8.97657e-09,
              0.0624
            ],
            "upper_arm_link": [
              0.020557580667452852,
              -0.030399401302706273,
              0.11659991933280232
            ],
            "lower_arm_link": [
              0.020557757817405556,
              -0.05839928652403588,
              0.22916994788197248
            ],
            "wrist_link": [
              0.02055861130214405,
              -0.1932993003195279,
              0.23436958991269105
            ],
            "gripper_link": [
              0.03865899786894979,
              -0.2543991858032857,
              0.23436965221111863
            ],
            "gripper_frame_link": [
              0.03882653228831924,
              -0.3525266145680401,
              0.22646877480623395
            ],
            "moving_jaw_so101_v1_link": [
              0.056454023460770365,
              -0.2777989266905471,
              0.25546062636110695
            ]
          }
        }
      ]
    },
    "turtlebot3_burger": {
      "file": "turtlebot3_burger.urdf",
      "sha256": "bc453d08d6a3f2da1530201a15807edafffa5158c291dc40f5edb19ae35ca603",
      "n_links": 7,
      "n_joints": 6,
      "movable": [
        {
          "name": "wheel_left_joint",
          "type": "continuous",
          "parent": "base_link",
          "child": "wheel_left_link",
          "axis": [
            0.0,
            0.0,
            1.0
          ],
          "origin_xyz": [
            0.0,
            0.08,
            0.023
          ],
          "limit": {}
        },
        {
          "name": "wheel_right_joint",
          "type": "continuous",
          "parent": "base_link",
          "child": "wheel_right_link",
          "axis": [
            0.0,
            0.0,
            1.0
          ],
          "origin_xyz": [
            0.0,
            -0.08,
            0.023
          ],
          "limit": {}
        }
      ],
      "cases": [
        {
          "case": "home_zero",
          "q": {},
          "frames": {
            "base_footprint": [
              0.0,
              0.0,
              0.0
            ],
            "base_link": [
              0.0,
              0.0,
              0.01
            ],
            "wheel_left_link": [
              0.0,
              0.08,
              0.033
            ],
            "wheel_right_link": [
              0.0,
              -0.08,
              0.033
            ],
            "caster_back_link": [
              -0.081,
              0.0,
              0.006
            ],
            "imu_link": [
              -0.032,
              0.0,
              0.078
            ],
            "base_scan": [
              -0.032,
              0.0,
              0.182
            ]
          }
        },
        {
          "case": "wheels_pi",
          "q": {
            "wheel_left_joint": 3.141592653589793,
            "wheel_right_joint": 3.141592653589793
          },
          "frames": {
            "base_footprint": [
              0.0,
              0.0,
              0.0
            ],
            "base_link": [
              0.0,
              0.0,
              0.01
            ],
            "wheel_left_link": [
              0.0,
              0.08,
              0.033
            ],
            "wheel_right_link": [
              0.0,
              -0.08,
              0.033
            ],
            "caster_back_link": [
              -0.081,
              0.0,
              0.006
            ],
            "imu_link": [
              -0.032,
              0.0,
              0.078
            ],
            "base_scan": [
              -0.032,
              0.0,
              0.182
            ]
          }
        }
      ]
    },
    "open_manipulator_x": {
      "file": "open_manipulator_x.urdf",
      "sha256": "784078c2a5bb16accd2ca4cbcf0d340403d6d343f047b433b503aeae85ef17d3",
      "n_links": 9,
      "n_joints": 8,
      "movable": [
        {
          "name": "joint1",
          "type": "revolute",
          "parent": "link1",
          "child": "link2",
          "axis": [
            0.0,
            0.0,
            1.0
          ],
          "origin_xyz": [
            0.012,
            0.0,
            0.0
          ],
          "limit": {
            "lower": "-3.141592653589793",
            "upper": "3.141592653589793",
            "effort": "1000",
            "velocity": "4.8"
          }
        },
        {
          "name": "joint2",
          "type": "revolute",
          "parent": "link2",
          "child": "link3",
          "axis": [
            0.0,
            1.0,
            0.0
          ],
          "origin_xyz": [
            0.0,
            0.0,
            0.0595
          ],
          "limit": {
            "lower": "-1.5",
            "upper": "1.5",
            "effort": "1000",
            "velocity": "4.8"
          }
        },
        {
          "name": "joint3",
          "type": "revolute",
          "parent": "link3",
          "child": "link4",
          "axis": [
            0.0,
            1.0,
            0.0
          ],
          "origin_xyz": [
            0.024,
            0.0,
            0.128
          ],
          "limit": {
            "lower": "-1.5",
            "upper": "1.4",
            "effort": "1000",
            "velocity": "4.8"
          }
        },
        {
          "name": "joint4",
          "type": "revolute",
          "parent": "link4",
          "child": "link5",
          "axis": [
            0.0,
            1.0,
            0.0
          ],
          "origin_xyz": [
            0.124,
            0.0,
            0.0
          ],
          "limit": {
            "lower": "-1.7",
            "upper": "1.97",
            "effort": "1000",
            "velocity": "4.8"
          }
        },
        {
          "name": "gripper_left_joint",
          "type": "prismatic",
          "parent": "link5",
          "child": "gripper_left_link",
          "axis": [
            0.0,
            1.0,
            0.0
          ],
          "origin_xyz": [
            0.0817,
            0.021,
            0.0
          ],
          "limit": {
            "lower": "-0.011",
            "upper": "0.02",
            "effort": "1000",
            "velocity": "4.8"
          }
        },
        {
          "name": "gripper_right_joint",
          "type": "prismatic",
          "parent": "link5",
          "child": "gripper_right_link",
          "axis": [
            0.0,
            -1.0,
            0.0
          ],
          "origin_xyz": [
            0.0817,
            -0.021,
            0.0
          ],
          "limit": {
            "lower": "-0.011",
            "upper": "0.02",
            "effort": "1000",
            "velocity": "4.8"
          }
        }
      ],
      "cases": [
        {
          "case": "home_zero",
          "q": {},
          "frames": {
            "world": [
              0.0,
              0.0,
              0.0
            ],
            "link1": [
              0.0,
              0.0,
              0.0
            ],
            "link2": [
              0.012,
              0.0,
              0.0
            ],
            "link3": [
              0.012,
              0.0,
              0.0595
            ],
            "link4": [
              0.036000000000000004,
              0.0,
              0.1875
            ],
            "link5": [
              0.16,
              0.0,
              0.1875
            ],
            "gripper_left_link": [
              0.2417,
              0.021,
              0.1875
            ],
            "gripper_right_link": [
              0.2417,
              -0.021,
              0.1875
            ],
            "end_effector_link": [
              0.28600000000000003,
              0.0,
              0.1875
            ]
          }
        },
        {
          "case": "joint2_45deg",
          "q": {
            "joint2": 0.7853981633974483
          },
          "frames": {
            "world": [
              0.0,
              0.0,
              0.0
            ],
            "link1": [
              0.0,
              0.0,
              0.0
            ],
            "link2": [
              0.012,
              0.0,
              0.0
            ],
            "link3": [
              0.012,
              0.0,
              0.0595
            ],
            "link4": [
              0.11948023074035521,
              0.0,
              0.13303910524340096
            ],
            "link5": [
              0.2071614716074871,
              0.0,
              0.04535786437626907
            ],
            "gripper_left_link": [
              0.264932095630428,
              0.021,
              -0.012412759646671857
            ],
            "gripper_right_link": [
              0.264932095630428,
              -0.021,
              -0.012412759646671857
            ],
            "end_effector_link": [
              0.2962569260369921,
              0.0,
              -0.04373759005323591
            ]
          }
        }
      ]
    }
  }
}

=== 2026-11-11T01:22:33+0800 | python3 exercise/lab.py verify ===
{
  "python": "3.13.5",
  "numpy": "2.5.4",
  "platform": "Linux-6.12.113+-x86_64-with-glibc2.41",
  "cwd": "/workspace/learn-batch/04-open-robots",
  "lab": "/workspace/learn-batch/04-open-robots/exercise",
  "cuda_devices": 0,
  "scope": "CPU metadata + URDF FK; no hardware, no paid API, no MuJoCo runtime required",
  "when": "2026-11-11T01:22:33+08:00"
}
{
  "groups_passed": 9,
  "groups_total": 9,
  "checks": [
    {
      "name": "catalog_18",
      "ok": true,
      "detail": 18
    },
    {
      "name": "categories_cover_four",
      "ok": true,
      "detail": {
        "人形": 4,
        "人形/双足": 1,
        "四足": 6,
        "机械臂": 3,
        "移动操作": 1,
        "移动平台": 3
      }
    },
    {
      "name": "so100_six_revolute",
      "ok": true,
      "detail": 6
    },
    {
      "name": "burger_lidar_invariant",
      "ok": true,
      "detail": true
    },
    {
      "name": "completions_8146",
      "ok": true,
      "detail": 8146
    },
    {
      "name": "completions_not_treated_as_fail_rate",
      "ok": true,
      "detail": {
        "False": 8146
      }
    },
    {
      "name": "sample_only_success_frames",
      "ok": true,
      "detail": {
        "Success Frame": 167
      }
    },
    {
      "name": "so100_home_has_positive_z",
      "ok": true,
      "detail": 0.156406
    },
    {
      "name": "duckie_not_osi",
      "ok": true,
      "detail": true
    }
  ],
  "scope": "author-written deterministic checks, not independent audit or upstream tests",
  "when": "2026-11-11T01:22:33+08:00"
}
```

## 执行边界
- survey/licenses 使用 exercise/data/repos-slim.json（公开 API 精简缓存）与已读 LICENSE 笔记，不在每次运行时重新打 GitHub API。
- agibot 读取 sources/hf 下已落盘文件。98 个 info.json 的类型统计在 info-scan-stats.json：第一次 urllib 扫描有 9 个 SSL 中断，随后用 `curl -fL --retry 5` 全部找回。最终 98/98，Success 8259 + Error 2 + Intervention 2。Intervention Frame 出现在重试文件中。
- completions.json 的 8146 条 isResultSucceed=false 被解释为占位，不当失败率。
- FK 为纯解析，跳过没有 parent/child 的占位关节；未加载网格，未运行 MuJoCo/PyBullet。
- verify 的 9 组是同一作者自写检查，不能称独立审核或上游测试套件通过。

## 非主实验的工具过程
- GitHub 公开 API 无凭据只读成功；没有尝试认证、使用密钥、提交或推送。部分仓 301 重定向（OttoDIY/OttoDIY→OttoNinja，OpenCat 改名，isl-org/OpenBot→ob-f/OpenBot）。
- Hugging Face 数据集文件用公开 resolve URL 下载；未使用付费 API，未购买服务。
- 官方 URDF 从固定 SHA 的 raw.githubusercontent.com 获取。TurtleBot3 URDF 含 `${namespace}` 宏，实验中替换为空字符串后解析。

## PDF 真实打印
2026-11-11 01:21:54（Asia/Shanghai），Chromium 158.0.8127.18 经 Playwright 输出 A4 PDF，pdfinfo 确认 11 页，约 970 KB。
打印命令：`/workspace/learn-batch/01-lingbot-map/.print-env/bin/python print_guide.py`。
逐页渲染命令：`pdftoppm -scale-to 1200 -png 开源机器人筛选-增量学习指南.pdf qa/page`。
检查方法：逐一读取 qa/page-01.png 至 page-11.png；各页中文、图、表、命令完整可见，无横向溢出、截字或额外空白页。完整检查见 qa/page-check.md。
