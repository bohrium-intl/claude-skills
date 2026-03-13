# Bohrium Blog Content Pipeline v2

## 一、示范稿大纲：GROMACS vs LAMMPS

### 元数据
- **Title**: GROMACS vs LAMMPS: Which Molecular Dynamics Software Should You Use?
- **Slug**: gromacs-vs-lammps-comparison
- **Category**: Research Notes
- **Tag**: Tool Comparison
- **Target Keywords**: GROMACS vs LAMMPS, molecular dynamics software comparison, LAMMPS vs GROMACS, best MD simulation software
- **Long-tail**: GROMACS vs LAMMPS for protein simulation, LAMMPS vs GROMACS performance, which MD software for materials science
- **Word Count Target**: 2500-3500
- **SciencePedia Terms to Link**: molecular dynamics, force field, GROMACS, LAMMPS, ab initio, Monte Carlo simulation

---

### 正文结构

#### H1: GROMACS vs LAMMPS: Which Molecular Dynamics Software Should You Use?

**Intro (150-200 words)**
- Hook: "Choosing between GROMACS and LAMMPS is one of the first decisions every computational researcher faces"
- 简述两者都是开源、主流、但设计哲学完全不同
- 本文要回答的问题：哪个更适合你的研究场景

#### H2: What Are GROMACS and LAMMPS?

**GROMACS 简介 (100-150 words)**
- 起源：University of Groningen
- 核心定位：生物分子模拟（蛋白质、脂质、核酸）
- 关键特性：极致的单节点性能优化、GPU加速
- [Link to SciencePedia: GROMACS]

**LAMMPS 简介 (100-150 words)**
- 起源：Sandia National Laboratories
- 核心定位：材料科学、通用分子模拟
- 关键特性：模块化设计、极强的可扩展性、支持从原子到连续介质尺度
- [Link to SciencePedia: LAMMPS]

#### H2: Key Differences at a Glance

**对比表格（核心差异速览）**

| Aspect | GROMACS | LAMMPS |
|--------|---------|--------|
| Primary Domain | Biomolecular (proteins, lipids) | Materials science, polymers, coarse-grained |
| Force Fields | AMBER, CHARMM, OPLS (bio-focused) | Extensible (EAM, ReaxFF, AIREBO, etc.) |
| GPU Acceleration | Native, highly optimized | Available via KOKKOS/GPU packages |
| Ease of Use | Structured workflow (grompp → mdrun) | Flexible scripting (steeper learning curve) |
| Parallelization | Excellent single-node; good multi-node | Excellent multi-node scaling (MPI-native) |
| Extensibility | Limited (C++ core) | Highly modular (plug-in packages) |
| License | LGPL (free, open-source) | GPL (free, open-source) |

#### H2: Performance Comparison

**(300-400 words)**
- 单节点性能：GROMACS通常更快（针对生物体系优化极致）
- 多节点扩展：LAMMPS的MPI并行设计天然适合大规模集群
- GPU利用率：GROMACS的GPU offloading更成熟
- 引用benchmark数据（Bohrium论文库 > arXiv > publisher）
- 关键结论：性能差异高度依赖于模拟体系，没有绝对赢家

#### H2: When to Choose GROMACS

**(200-300 words)**
- 蛋白质、脂质膜、核酸等生物分子模拟
- 药物设计、蛋白-配体相互作用
- 需要极致单节点性能
- 偏好结构化工作流（适合新手）
- 已有AMBER/CHARMM/OPLS力场参数

#### H2: When to Choose LAMMPS

**(200-300 words)**
- 材料科学：金属、聚合物、纳米材料
- 需要反应力场（ReaxFF）
- 粗粒度模拟或多尺度建模
- 需要高度自定义的模拟流程
- 大规模并行计算场景

#### H2: Can You Use Both?

**(150-200 words)**
- 提到GRO2LAM等转换工具
- 实际科研中两者互补的案例
- 很多课题组同时使用两者

#### H2: Getting Started

**(150-200 words)**
- GROMACS: 官方tutorial链接 + 推荐入门资源
- LAMMPS: lammpstutorials.github.io + 官方文档
- 提到云平台可以降低环境配置门槛（自然引到Bohrium，不硬推）
- [如果有Bohrium教程则在此内链]

#### H2: Summary

**对比总结表格**

| Your Research Focus | Recommended Tool |
|---|---|
| Protein dynamics, drug design | GROMACS |
| Metal alloys, nanomaterials | LAMMPS |
| Polymer systems | Both work; LAMMPS slightly more flexible |
| Reactive chemistry | LAMMPS (ReaxFF) |
| New to MD simulation | GROMACS (gentler learning curve) |

**Closing (50-100 words)**
- 没有"最好的"MD软件，只有最适合你研究的
- 鼓励读者先明确研究需求再选工具

---

## 二、通用Pipeline模板

### 内容类型A：工具/概念对比（Tool Comparison）

```
模板结构：
1. [H1] {Tool A} vs {Tool B}: {决策问题}
2. [H2] What Are {Tool A} and {Tool B}?
   - 各100-150词简介
   - SciencePedia链接
3. [H2] Key Differences at a Glance
   - 对比表格（6-8个维度）
4. [H2] Performance Comparison（如适用）
   - 引用公开benchmark（优先Bohrium论文库来源）
5. [H2] When to Choose {Tool A}
   - 3-5个场景，每个1-2句
6. [H2] When to Choose {Tool B}
   - 3-5个场景，每个1-2句
7. [H2] Can You Use Both?（可选）
8. [H2] Getting Started
   - 资源链接 + 自然引入Bohrium
9. [H2] Summary
   - 场景→推荐 速查表
```

**可批量选题：**
- GROMACS vs LAMMPS ✓
- VASP vs Quantum ESPRESSO
- DFT vs MD: When to Use Which
- AMBER vs CHARMM Force Field
- OpenMM vs GROMACS
- Ab Initio vs Semi-Empirical Methods
- Classical MD vs Machine Learning Potentials

---

### 内容类型B：概念科普（Concept Guide）

```
模板结构：
1. [H1] What is {Concept}? A Practical Guide for Researchers
2. [H2] {Concept} in Simple Terms
   - 2-3段，从直觉到定义
   - SciencePedia定义引用
3. [H2] How Does {Concept} Work?
   - 核心原理（不需要公式，讲逻辑）
   - 图解或流程描述
4. [H2] Key Applications
   - 3-5个领域，每个2-3句
5. [H2] Common Methods / Software
   - 列出主流工具
   - 链接到已有的Tool Comparison文章
6. [H2] Limitations and Challenges
   - 2-3个常见问题
7. [H2] Further Reading
   - 推荐教材/综述/官方文档
   - 内链到相关blog文章
```

**可批量选题：**
- What is Density Functional Theory (DFT)?
- What is Molecular Dynamics Simulation?
- What is a Force Field in Computational Chemistry?
- What is Ab Initio Calculation?
- What is Coarse-Grained Simulation?
- What is Monte Carlo Simulation in Materials Science?
- What is the Born-Oppenheimer Approximation?

---

## 三、Pipeline技术实现（6步）

### Step 1: 选题生成（Claude Code）

```python
# 输入：种子关键词列表 + 内容类型（comparison / concept）
# 输出：选题列表 with 元数据

topic_schema = {
    "title": str,
    "slug": str,
    "type": "comparison" | "concept",
    "primary_keyword": str,
    "secondary_keywords": [str],
    "long_tail_keywords": [str],
    "sciencepedia_terms": [str],
    "template": str,
}
```

### Step 2: SciencePedia词条抓取（Claude Code）

```python
# 输入：sciencepedia_terms列表
# 输出：每个词条的定义、描述、相关词条
# 复用已有的SciencePedia fuzzy-match lookup skill
# 如果 term 是科研工具名（如 GROMACS/LAMMPS），并行走 agent-tools lookup：
#   - sitemap: https://cdn.bohrium.com/bohrium/web/static/sitemap/sp-tools/sitemap_1.xml
#              https://cdn.bohrium.com/bohrium/web/static/sitemap/sp-tools/sitemap_2.xml
#   - URL pattern: https://www.bohrium.com/en/sciencepedia/agent-tools/{slug}
#   - 建本地缓存库 + lookup（和 keyword lookup 相同思路）
```

### Step 3: Fact Sheet搜索（Claude Code）⭐ 新增

```python
# 输入：选题元数据（primary_keyword + secondary_keywords）
# 输出：verified fact sheet for each topic

fact_sheet_schema = {
    "topic": str,
    "key_facts": [
        {
            "fact": str,           # 具体事实（benchmark数据、版本号等）
            "source": str,         # 来源名称
            "url": str,            # 来源URL
            "bohrium_url": str,    # Bohrium论文库URL（如有收录）
            "confidence": "high" | "medium",  # 来源可信度
        }
    ],
    "official_doc_links": [str],   # 官方文档URL（作为外链）
    "benchmark_data": [str],       # 性能对比数据
    "latest_version_info": {       # 软件最新版本信息
        "tool_name": str,
        "version": str,
        "release_date": str,
    }
}

# 搜索逻辑：
# 1. Web search: "{tool} benchmark performance 2024 2025"
# 2. Web search: "{tool} latest version release"
# 3. Web search: "{tool A} vs {tool B} comparison study"
# 4. 对每条论文先做 Bohrium 映射（推荐复用 paper-post-prep/scripts/bohrium_lookup.py）
#    - 有 DOI_API_ACCESS_KEY/SECRET：查 Bohrium API，命中则返回 bohrium_url
#    - 无凭据或未命中：自动 fallback 到原始 arXiv/publisher URL（不中断 pipeline）
# 5. 在 fact_sheet 中记录 resolution_status（bohrium/fallback）和 resolution_reason
# 5. 只保留 confidence=high 的事实进入生成环节
```

建议实现一个独立 resolver（例如 `pipeline_bohrium_paper_resolver.py`），输入论文列表，输出：
- `bohrium_url`
- `resolution_status`: `bohrium` | `fallback`
- `resolution_reason`: `matched` | `missing_credentials` | `not_found` | `lookup_error:*`

### Step 4: 内容生成（Gemini API）

```python
prompt_template = """
You are writing a blog post for Bohrium (bohrium.com), an AI for Science platform.

## Article Metadata
Title: {title}
Type: {type}
Primary Keyword: {primary_keyword}
Secondary Keywords: {secondary_keywords}

## Template Structure
{template_content}

## SciencePedia Reference Content
{sciencepedia_content}

## Verified Fact Sheet (USE THESE NUMBERS, DO NOT INVENT)
{fact_sheet}

## Linking Rules
1. SciencePedia terms → link to: https://www.bohrium.com/en/sciencepedia/feynman/keyword/{term-slug}
2. Paper citations → FIRST check bohrium_url, if exists use it; else use original URL
3. Official docs (GROMACS.org, LAMMPS.org etc.) → use as external links
4. Bohrium platform → mention at most ONCE, naturally in Getting Started section
5. Target: ≥5 SciencePedia links + 2-3 paper links（优先 Bohrium URL，失败时允许 fallback）+ 2 external doc links

## Writing Guidelines
- English, academic but accessible tone
- Target audience: graduate students and early-career researchers
- Word count: 2500-3500 for comparison, 2000-2500 for concept
- Include comparison tables as markdown tables
- ALL data/numbers MUST come from the Fact Sheet above — do not hallucinate
- End with clear, practical recommendation
- Meta description (under 155 chars) in YAML frontmatter
- Do NOT hard-sell Bohrium
"""
```

### Step 5: QA评分（Claude Code）⭐ 新增

分两层执行：

#### 第一层：硬性门槛（Pass/Fail）

不过任何一条 → 打回Step 4重新生成（最多retry 2次）

```python
hard_checks = {
    # 事实准确性
    "all_numbers_match_fact_sheet": bool,     # 所有数字都能追溯到fact sheet
    "no_hallucinated_versions": bool,         # 软件版本号与fact sheet一致
    "sciencepedia_definitions_accurate": bool, # SP词条引用准确

    # 结构完整性
    "follows_template_structure": bool,       # 所有必需H2都存在
    "comparison_table_present": bool,         # 对比表格存在且完整
    "word_count_in_range": bool,              # 字数在目标范围内
    "has_yaml_frontmatter": bool,             # Hugo frontmatter完整

    # SEO基本面
    "title_contains_primary_keyword": bool,
    "meta_desc_under_155_chars": bool,
    "sciencepedia_links_gte_5": bool,         # SP内链 ≥ 5
    "has_external_doc_links": bool,           # 有官方文档外链
    "no_broken_links": bool,                  # 链接格式正确
}
# 全部True才Pass
```

#### 第二层：质量评分（0-100分）

80+ 直接发布 | 60-80 人工润色 | <60 打回重写

```python
quality_score = {

    # ===== 引用权威性（35分）=====
    "paper_citations_from_bohrium": {         # 论文引用优先指向Bohrium论文库
        "weight": 10,
        "scoring": "0 links: 4分 | 1-2 links: 7分 | 3+ links: 10分（fallback 不判失败）"
    },
    "cites_official_docs": {                  # 引用官方文档/一手来源
        "weight": 10,
        "scoring": "0 external: 3分 | 1: 6分 | 2+: 10分"
    },
    "sciencepedia_integration_quality": {     # SP词条引用是否自然、准确
        "weight": 10,
        "scoring": "生硬插入: 3分 | 语境恰当: 7分 | 增强理解: 10分"
    },
    "avoids_secondary_sources": {             # 是否避开了二手来源（博客、论坛）
        "weight": 5,
        "scoring": "引用博客/论坛: 1分 | 全部一手来源: 5分"
    },

    # ===== 信息密度（30分）=====
    "unique_info_vs_competitors": {           # 相比竞品有多少独特信息点
        "weight": 10,
        "scoring": "0-1 new points: 3分 | 2-3: 7分 | 4+: 10分"
    },
    "comparison_table_completeness": {        # 对比表格维度是否全面
        "weight": 8,
        "scoring": "<5 dimensions: 3分 | 5-7: 6分 | 8+: 8分"
    },
    "no_filler_paragraphs": {                 # 每段都有实质内容，无水话
        "weight": 7,
        "scoring": "有明显水段: 2分 | 基本紧凑: 5分 | 全篇干货: 7分"
    },
    "actionable_recommendations": {           # 读完能直接做决策
        "weight": 5,
        "scoring": "无建议: 1分 | 泛泛建议: 3分 | 场景化推荐: 5分"
    },

    # ===== 可读性（20分）=====
    "jargon_explained_on_first_use": {        # 术语首次出现有解释
        "weight": 7,
        "scoring": "多处未解释: 2分 | 大部分解释: 5分 | 全部解释: 7分"
    },
    "logical_flow": {                         # 从具体到抽象、有逻辑递进
        "weight": 7,
        "scoring": "跳跃混乱: 2分 | 基本通顺: 5分 | 层层递进: 7分"
    },
    "appropriate_paragraph_length": {         # 段落长度适中（3-6句）
        "weight": 6,
        "scoring": "大段堆砌: 2分 | 偶有过长: 4分 | 均匀适中: 6分"
    },

    # ===== 结构可扫描性（15分）=====
    "h2_standalone_answerable": {             # 每个H2能独立回答一个问题
        "weight": 6,
        "scoring": "H2模糊: 2分 | 基本清晰: 4分 | 完全自明: 6分"
    },
    "summary_table_placement": {              # 总结表格在关键位置
        "weight": 5,
        "scoring": "无总结表: 1分 | 只在末尾: 3分 | 首尾呼应: 5分"
    },
    "scannable_without_reading": {            # 只看H2+表格能获得80%核心信息
        "weight": 4,
        "scoring": "必须全读: 1分 | 看标题知大意: 3分 | 扫H2+表格全懂: 4分"
    },
}

# 总分 = sum of all scores
# 输出格式：
# {
#   "total_score": 82,
#   "grade": "PUBLISH",  # PUBLISH | REVISE | REWRITE
#   "breakdown": { ... },
#   "improvement_suggestions": ["建议补充一条benchmark数据来源", ...]
# }
```

### Step 6: 后处理 & 输出（Claude Code）

```python
# 输入：通过QA的markdown文章
# 处理：
# 1. 注入Hugo frontmatter
#    ---
#    title: "GROMACS vs LAMMPS: Which MD Software Should You Use?"
#    date: 2026-03-10
#    categories: ["Research Notes"]
#    tags: ["Tool Comparison"]
#    description: "Compare GROMACS and LAMMPS for molecular dynamics..."
#    sciencepedia_terms: ["molecular-dynamics", "force-field", ...]
#    ---
#
# 2. 验证所有链接格式
#    - SciencePedia: https://www.bohrium.com/en/sciencepedia/feynman/keyword/{slug}
#    - Bohrium papers: 使用 resolver 产出的 bohrium_url（不要硬编码 URL pattern）
#    - External: https://www.gromacs.org/... etc.
#
# 3. 生成QA报告（附在文章末尾的注释中，不渲染）
#    <!-- QA_SCORE: 85 | GRADE: PUBLISH | CHECKED: 2026-03-10 -->
#
# 4. 输出到Hugo content目录
#    ./content/blog/research-notes/{slug}.md
```

---

## 四、链接策略

### 链接类型优先级

```
1. SciencePedia词条内链（≥5/篇）
   → https://www.bohrium.com/en/sciencepedia/feynman/keyword/{term}
   → 作用：给SP页面传权重、建立概念网络

2. Bohrium论文库内链（目标2-3/篇）
   → 使用 resolver 返回的 `bohrium_url`（paper-details 直链）
   → 作用：引用来源留在站内、提升论文页流量

3. Blog互链（2/篇）
   → https://bohrium.com/blog/{slug}
   → 作用：内容矩阵互相支撑

4. 外链 - 官方文档（2/篇）
   → GROMACS.org, LAMMPS.org, VASP wiki, etc.
   → 作用：E-E-A-T信号、引用一手来源

5. 外链 - arXiv/publisher（仅Bohrium未收录时）
   → 作用：补充引用，但尽量避免
```

### 内链网络结构

```
Tool Comparison 文章群
  ├── GROMACS vs LAMMPS
  ├── VASP vs QE
  ├── AMBER vs CHARMM
  └── ... (互相引用)
        ↕
Concept Guide 文章群
  ├── What is DFT?
  ├── What is MD Simulation?
  ├── What is Force Field?
  └── ... (互相引用)
        ↕
Paper Review 文章群（已有几十篇）
  └── 具体论文解读 → 链到相关Comparison和Concept文章
        ↕
SciencePedia 词条（权威定义锚点）
        ↕
Bohrium 论文库页面（引用来源留存）
```

---

## 五、Anti-Hallucination规则（Gemini生成专用）

```
🚫 绝对禁止：
- 编造benchmark数字（所有数字必须来自Fact Sheet）
- 编造论文引用（DOI/作者/年份必须真实）
- 编造软件版本号
- 编造用户数/下载量等metrics
- 声称"Bohrium是最好的XX"

✅ 必须遵守：
- 所有数据引用标注来源
- 不确定的信息用"generally", "typically"等hedge words
- 版本号/release date以Fact Sheet为准
- 对比必须公平，不能贬低任何一方
- 承认每个工具的局限性
```

---

## 六、批量执行

```bash
# 一键跑完整个pipeline
python pipeline.py \
  --topics topics.json \           # 选题列表
  --template comparison \          # 模板类型
  --output ./content/blog/ \       # Hugo content目录
  --sp-cache ./sp_cache/ \         # SciencePedia缓存
  --bohrium-resolver ./pipeline_bohrium_paper_resolver.py \
  --bohrium-env ~/.env \           # 可选：含 DOI_API_ACCESS_KEY/SECRET
  --gemini-model gemini-2.0-flash \
  --qa-threshold 80 \              # QA分数阈值
  --max-retry 2 \                  # 低于阈值最多重试次数
  --batch-size 5
```

---

## 七、产出节奏

| 阶段 | 时间 | 产出 | 内容 |
|------|------|------|------|
| 验证 | Week 1 | 手动写1篇 | GROMACS vs LAMMPS（验证模板+QA） |
| 搭建 | Week 2 | 搭pipeline | Claude Code脚本 + Gemini调用 + QA |
| 冷启动 | Week 3-4 | 批量5-10篇 | 剩余comparison + concept选题 |
| 稳态 | 持续 | 每周2-3篇 | Pipeline自动化 + 人工review |
| 补充 | 待公司批测试账号 | 3-5篇教程 | 平台实操tutorial（手动） |

### KPI预估

- 10篇长尾内容上线后，预计2-4周开始获得impression
- 每篇稳定排名后日均100-500 impression
- 10篇 × 200平均 = 2000/天 = 60K/月
- 远超1万曝光KPI（1万是月还是日？）
