---
name: sota-finder
description: >-
  为研究任务或 benchmark 搜索有证据支持的 SOTA，并构建可实践的多 scope Leaderboard。适用于用户要求查找最新或历史 SOTA、建立 benchmark 排行榜、比较跨论文结果，或根据自然语言、论文、URL、仓库、表格和既有结果文件生成结构化证据交付物。Skill 将可比主结果、参考结果和冲突分开，AMiner 仅作为可选增强，并输出极简聊天结果以及 Markdown、自包含 HTML、XLSX 和 evidence JSON 文件。
license: MIT
metadata:
  openclaw:
    requires:
      bins: [python3]
---

# SOTA Finder

目标是快速形成可信、可用的结果，而不是建立僵硬的审查系统。宿主模型负责研究判断，附带脚本只负责确定性的交付物生成。

## 核心口径

- SOTA 只在特定且实质可比的 scope 内成立。
- 一个主题可以产生多个 scope 和多个 SOTA。
- 用户可见结果只分为 `Main Leaderboard`、`Reference Results`、`Conflicts / Unavailable` 三层。
- 主榜 claim 必须具有足够完整的比较 setting，并至少有一个原始、官方或作者控制来源支持。
- 聚合站用于发现和交叉核对，不能单独作为主榜充分证据。
- 必须标注绝对证据截止日期，例如 `Evidence checked through August 25, 2026`。

## 输入

主要入口是自然语言目标，例如“找这个任务的 SOTA”“建立最新 Leaderboard”“比较近期论文结果”。可选输入包括 PDF、论文或 benchmark URL、arXiv/DOI、官方榜单、项目仓库、CSV/XLSX/Markdown/JSON、粘贴表格、旧榜单和 evidence。

显式输入优先，开放世界搜索补充。只有用户明确要求“只使用给定来源”时才关闭外部搜索。

## 必须执行的工作方式

### 1. 建立暂定 scope

固定核心字段包括 task、benchmark/version、dataset/subtask、split、metric/variant/unit/direction 和 evaluation protocol。training regime、external data、shot setting、tool access、ensemble、model scale、retrieval condition 等仅在 materially affects comparability 时成为动态比较轴。不要建立通用刚性规则库。

### 2. Fast-first 广泛发现

非简单任务先读 `references/research-playbook.md`。默认搜索官方榜单与 benchmark 文档、论文与预印本、作者/官方仓库以及高质量聚合站。

先快速发现 scope、头部候选、最新声明和 setting 差异，再定向核验头部、近期 SOTA 声明和冲突。未指定年份时使用全历史候选池，优先检索近两到三年，但历史方法若仍领先则保留。

### 3. 核验证据并分层

每条结果记录 method、variant、score、source、evidence locator、setting 和 comparability notes。

- `main`: 可比性足够且有原始/官方/作者证据；
- `reference`: 有参考价值但 setting 不完整、证据较弱或存在实质不可比；
- `unavailable`: 相关但证据或结果无法获取；
- conflict: 来源数值、setting 或解释相互矛盾。

不要把 reference 或 unavailable 与主榜混排，也不要静默选择冲突值。

### 4. 模型判断停止

不设置固定轮数。scope 覆盖可信、头部候选收敛、新结果不再实质改变榜首、gaps/conflicts 已记录时停止。网络或单个来源失败时 best-effort 继续；只有完全无法形成有意义结果，或缺失决定显著改变范围/风险时才询问用户。

### 5. AMiner 是可选增强

没有 `AMINER_API_KEY` 也必须完整运行。token 可用时，可用 AMiner 加强论文发现、元数据、相关论文和引用扩展，但不得缩窄其他来源搜索。

免费或低费用最短调用可自动执行；预计累计费用约达到人民币 5 元、需要明显大批量调用，或付费计划无法估计时，先确认一次。不得拆分调用规避累计费用护栏。记录 AMiner 用途、费用信息和跳过的 enrichment。

### 6. 生成交付物

准备临时 research input 前读 `references/data-contract.md`，交付前读 `references/output-contract.md`。

```bash
python3 -c "import openpyxl" 2>/dev/null || python3 -m pip install -r "<skill-root>/requirements.txt"
python3 "<skill-root>/scripts/build_outputs.py" \
  --input "/path/to/research-input.json" \
  --output-root "outputs"
```

不要假设个人绝对路径。默认产物为：

```text
outputs/<topic-slug>/
├── brief-report.md
├── full-report.html
├── leaderboards.xlsx
└── evidence.json
```

已有产物时使用 `-2`、`-3` 等新目录，不静默覆盖。可用 `--validate-only` 只检查输入。文件生成失败时仍输出聊天极简结果，并说明未保存的文件。

## 聊天输出

聊天中只展示主 Leaderboard、非常必要的 scope/截止日期/异常说明，以及四个文件的直接链接。不要把完整版报告粘贴到聊天中。

## 语言与可移植性

用户可见内容跟随用户语言；JSON keys、ID、schema values 和稳定机器字段使用英文。Skill 必须自包含，不要求其他 Skill 已安装，不使用机器专属路径，不依赖 Codex 专属 artifact runtime。宿主可以使用自身搜索/浏览工具，Python 脚本只负责本地机械生成。

## 非目标

不建立刚性 benchmark 规则库、通用 method alias registry、审批状态机或固定搜索轮次。不得把弱可比开放世界结果混入主榜，也不得在仍有 gaps 时声称穷尽覆盖。
