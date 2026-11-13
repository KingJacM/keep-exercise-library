# keep-exercise-library

Keep（calorietech.com）公开动作库的完整清单：5405 个动作，JSON 格式，附抓取脚本。

Complete catalog of the public Keep exercise library: 5,405 exercises in JSON, with the scraper used to collect them.

## 数据 / Data

完整数据因单文件大小限制拆成两个文件，拼起来即全量：`data/keep_exercises_part1.json`（2703 条）与 `data/keep_exercises_part2.json`（2702 条）。2026-11-13 从 Keep 官网动作库 10 个部位分类页抓取，去重后 **5405 个动作**。分类条目合计 6930，差值是同一动作挂在多个分类下。

The full dataset is split into two files (single-file size limits): `data/keep_exercises_part1.json` (2,703 records) + `data/keep_exercises_part2.json` (2,702 records). Concatenate the two arrays to get all 5,405 exercises.

| 分类 | 条目数 |
|---|---|
| 全身 | 625 |
| 胸部 | 460 |
| 肩部 | 407 |
| 背部 | 730 |
| 腿部 | 1712 |
| 腹部 | 1039 |
| 臀部 | 1437 |
| 手臂 | 463 |
| 颈部 | 53 |
| 腰部 | 4 |

每个动作的字段：

| 字段 | 说明 |
|---|---|
| `id` | 动作 ID，24 位十六进制 |
| `name` | 动作中文名 |
| `url` | 官网动作页地址 |
| `image` | 缩略图地址（Keep CDN） |
| `gender` | 源页面演示版本，f 或 m |
| `level` | 官网难度星数，0 到 5 |
| `categories` | 所属部位分类，可多个 |

字段说明的机器可读版本在 `data/category_summary.json` 里，含每类计数和总数。

## 使用示例 / Usage

```python
import json

exercises = (json.load(open("data/keep_exercises_part1.json"))
             + json.load(open("data/keep_exercises_part2.json")))

print(len(exercises))  # 5405

# 按部位筛
neck = [e for e in exercises if "颈部" in e["categories"]]
# 按难度筛
easy = [e for e in exercises if e["level"] <= 1]
# 按名字搜
hits = [e for e in exercises if "死虫" in e["name"]]
```

## 覆盖范围 / Coverage

这是官网口径的完整库。Keep App 内的「全部动作」列表走登录接口，无法匿名获取；App 里另有「热身动作」分类，官网没有，如果有只挂在该分类下、任何部位分类都没有的动作，这一小部分不在本库内。

校验方式：本库腹部 1039 个 ID 与单独抓取的腹部全量 ID 集合完全一致，每个分类抓到的数量与官网页面标注的总数一致。

## 抓取 / Scraping

抓取脚本在 `tools/scrape.py`，按官网分类页的翻页接口逐分类抓取，再按动作 ID 合并去重，输出一个完整的 JSON 数组（本仓库里的两个 part 文件就是把这个数组对半拆开）。重新运行时官网数据可能已经变化，总数以官网当时标注为准。

## 许可与来源 / License and attribution

动作名称、难度和分类等数据来自 Keep 官网（calorietech.com）的公开页面，权利归原平台所有，本仓库只做整理汇编，图片仅以链接形式引用，未复制图片文件。本仓库自己的文档和代码以 MIT 协议开源，见 `LICENSE`。

Exercise data comes from the public pages of calorietech.com (Keep). All rights in the underlying data belong to the original platform; images are referenced by URL only. Documentation and code in this repository are released under the MIT License.
