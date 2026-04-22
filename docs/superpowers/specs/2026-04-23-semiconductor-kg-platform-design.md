# 半导体知识图谱平台 — 设计文档

**日期**: 2026-04-23  
**主题**: 半导体薄膜沉积知识图谱平台 Landing Page + 可视化系统  
**决策**: Next.js App Router、独立页面架构（SEO 优先）、D3.js 静态图谱预览、后续扩展后端 API

---

## 1. 项目背景与目标

### 1.1 背景
用户已构建半导体薄膜沉积领域的知识图谱数据，需要一个可对外展示的平台作为「半导体制造领域 Linux 系统」的雏形。平台需要同时服务两类核心用户：
- **工程师**：查询工艺参数、贡献数据、建立个人影响力
- **企业客户**：诊断工艺问题、外派专家、审厂预审

### 1.2 目标
- **Phase 1（本设计范围）**: 发布一个专业的 Landing Page + 知识图谱可视化演示，吸引种子用户
- **Phase 2（后续）**: 叠加后端 API、用户认证、数据贡献与审核机制
- **Phase 3（后续）**: 人才匹配引擎、支付分账、服务转化

### 1.3 成功标准
- 页面 Lighthouse 性能评分 > 90
- 首屏加载时间 < 2s
- 图谱 demo 支持 50+ 节点流畅交互
- 各页面具备完整 SEO metadata

---

## 2. 信息架构

### 2.1 站点地图

```
/                    → Landing Page
  ├── /features      → 功能特性页
  ├── /graph         → 知识图谱演示页
  └── /cases         → 案例与评价页
```

### 2.2 SEO 配置

| 路由 | Title | Description |
|------|-------|-------------|
| `/` | 半导体知识图谱平台 \| 薄膜沉积工艺专家社区 | 半导体薄膜沉积领域首个知识图谱平台，连接工艺工程师与企业客户 |
| `/features` | 平台功能 \| 工程师工具 & 企业解决方案 | 为半导体工程师提供工艺查询与数据贡献工具，为企业提供专家外派与审厂服务 |
| `/graph` | 工艺图谱 \| 交互式薄膜沉积知识网络 | 探索 CVD、PVD、ALD 等薄膜沉积工艺的交互式知识图谱 |
| `/cases` | 客户案例 \| 工艺优化成果与专家评价 | 了解平台如何帮助半导体企业解决工艺难题与提升良率 |

### 2.3 共享布局

**Navbar**
- 固定顶部，滚动超过 80px 后背景由透明变为 `bg-white/90 backdrop-blur`
- 左侧：平台 Logo + 名称
- 中间：导航链接（功能、图谱、案例）
- 右侧：CTA 按钮「免费体验」
- 移动端：汉堡菜单，展开全屏导航

**Footer**
- 四栏链接矩阵：产品（功能、图谱、定价）、资源（博客、文档、API）、公司（关于、联系、招聘）、法律（隐私、条款）
- 底部：社交媒体图标 + 版权信息

---

## 3. 页面设计

### 3.1 Landing Page (`/`)

#### 区块 A — Hero

```
┌─────────────────────────────────────────────────────────┐
│  [Navbar]                                                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│     半导体薄膜沉积知识图谱                               │
│     工艺透明化 · 人才精准化 · 方案系统化                   │
│                                                         │
│     [立即体验图谱]    [申请企业咨询]                       │
│                                                         │
│     [Hero 视觉：抽象晶圆 / 薄膜层叠插画]                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

- **主标题**: `半导体薄膜沉积知识图谱`（h1，text-4xl md:text-6xl，font-bold）
- **副标题**: `工艺透明化 · 人才精准化 · 方案系统化`（text-xl md:text-2xl，text-slate-600）
- **CTA 主按钮**: `立即体验图谱` → 跳转 `/graph`，样式 `bg-blue-600 text-white hover:bg-blue-700`
- **CTA 次按钮**: `申请企业咨询` → 弹出联系表单对话框，样式 `border border-slate-300 hover:bg-slate-50`
- **Hero 视觉**: 右侧或下方放置抽象晶圆/薄膜层叠 SVG 插画，主色调蓝/银/白

#### 区块 B — 信任背书

- **数据统计条**: `已覆盖 12 种薄膜沉积工艺 · 300+ 设备型号 · 50+ 认证工程师`
- **Logo 墙**: AMAT、LAM、TEL、ASMI、SCREEN 等设备商标识（灰色滤镜，hover 变彩色）
- **初期标注**: 数据可标注为「目标」或「持续建设中」，保持诚实

#### 区块 C — 双受众价值主张

双栏卡片布局（移动端堆叠）：

**左侧 — 工程师端**
- 图标：Wrench
- 标题：`为半导体工程师打造`
- 要点：
  - 查询工艺参数与失效模式
  - 贡献数据赚取积分与收入
  - 建立个人技术影响力
- CTA: `加入工程师社区`

**右侧 — 企业端**
- 图标：Building2
- 标题：`为企业客户赋能`
- 要点：
  - 工艺问题快速诊断
  - 专家人才按需外派
  - 审厂预审全包服务
- CTA: `预约企业演示`

#### 区块 D — 底部 CTA

- 标题：`准备好让薄膜沉积工艺更透明了吗？`
- 按钮：`立即开始` → `/graph`

---

### 3.2 功能特性页 (`/features`)

页面结构：
1. **页面标题**: `平台功能`
2. **Tab 切换**: `工程师端` | `企业端`
3. **工程师端功能网格**（3 列卡片）：
   - 工艺导航器：输入目标工艺 → 推荐工艺路线
   - 设备比对器：对比不同设备在特定工艺下的表现
   - 问题诊断器：输入不良现象 → 匹配失效模式
   - 知识贡献：一键提交工艺数据
   - 积分体系：贡献数据赚取「沉积点」
   - 专家认证：通过审核成为领域认证工程师
4. **企业端功能网格**（3 列卡片）：
   - 工艺咨询：按小时计费的专家远程诊断
   - 审厂预审：文档预审 + 远程模拟审厂
   - 设备选型：定制化设备对比与选型报告
   - 人才外派：按工艺专长匹配工程师
   - 数据服务：定制行业分析报告
   - 企业订阅：分级访问知识图谱数据

---

### 3.3 知识图谱演示页 (`/graph`)

页面布局：

```
┌─────────────────────────────────────────────────────────┐
│  [Navbar]                                                │
├──────────────────────┬──────────────────────────────────┤
│  图例与控制面板       │        交互式图谱画布              │
│                      │                                  │
│  [● 工艺节点 蓝]      │    [力导向图渲染区域]              │
│  [● 设备型号 绿]      │                                  │
│  [● 材料参数 黄]      │                                  │
│  [● 失效模式 红]      │                                  │
│                      │                                  │
│  [筛选: 全部 ▼]       │                                  │
│                      │                                  │
│  ───────────────────  │                                  │
│  节点详情             │                                  │
│  （未选中时显示提示）   │                                  │
└──────────────────────┴──────────────────────────────────┘
```

**左侧面板**（宽度 280px，可折叠）：
- **图例**: 节点类型与颜色映射
- **筛选器**: 下拉选择节点类型（全部 / 工艺 / 设备 / 材料 / 失效）
- **节点详情**: 点击节点后显示属性面板

**右侧画布**（占据剩余宽度，高度 `calc(100vh - 64px)`）：
- D3.js 力导向图渲染
- 节点带标签，边带关系类型提示
- 背景网格线（微弱，增加空间感）

**交互行为**：
- 滚轮缩放（最小 0.1x，最大 5x）
- 拖拽平移画布
- 拖拽节点调整位置（力导向模拟暂停后恢复）
- 点击节点：高亮该节点 + 其直接邻居 + 相连边，其他元素透明度降至 0.2
- 点击空白处：取消选中，恢复全部透明度
- 鼠标悬停边：显示关系类型 tooltip

---

### 3.4 案例与评价页 (`/cases`)

页面结构：
1. **页面标题**: `客户案例与专家评价`
2. **成果数据条**: `帮助企业解决 50+ 工艺难题 · 平均良率提升 12% · 覆盖 8 家 Foundry`
3. **案例卡片网格**（2 列）：
   - 每个卡片：客户类型（匿名）+ 工艺问题 + 解决方案简述 + 成果数据
4. **专家评价轮播**（3 条）：
   - 头像 + 姓名（可匿名）+ 职位 + 评价内容 + 星级

---

## 4. 技术栈

| 层级 | 技术 | 用途 |
|------|------|------|
| 框架 | Next.js 14+ (App Router) | SSR/SSG、路由、API 路由 |
| 语言 | TypeScript | 类型安全 |
| 样式 | Tailwind CSS | 原子化样式 |
| UI 库 | shadcn/ui | 基础组件（Button、Card、Dialog、Tabs） |
| 图表 | D3.js v7 | 力导向图渲染 |
| 图标 | Lucide React | 矢量图标 |
| 字体 | Inter (Google Fonts) | 正文与标题 |

---

## 5. 组件清单

### 5.1 布局组件

| 组件 | 路径 | 说明 |
|------|------|------|
| `Navbar` | `components/layout/Navbar.tsx` | 全局导航栏，响应式 |
| `Footer` | `components/layout/Footer.tsx` | 全局页脚 |
| `RootLayout` | `app/layout.tsx` | 根布局，注入字体与全局样式 |

### 5.2 页面区块组件

| 组件 | 路径 | 说明 |
|------|------|------|
| `HeroSection` | `app/sections/HeroSection.tsx` | 首屏价值主张 |
| `TrustBar` | `app/sections/TrustBar.tsx` | 数据统计与 Logo 墙 |
| `ValueProposition` | `app/sections/ValueProposition.tsx` | 双受众对比 |
| `BottomCTA` | `app/sections/BottomCTA.tsx` | 底部行动号召 |
| `FeatureGrid` | `app/sections/FeatureGrid.tsx` | 功能特性网格 |
| `CaseGrid` | `app/sections/CaseGrid.tsx` | 案例卡片网格 |
| `TestimonialCarousel` | `app/sections/TestimonialCarousel.tsx` | 评价轮播 |

### 5.3 图谱组件

| 组件 | 路径 | 说明 |
|------|------|------|
| `KnowledgeGraph` | `components/graph/KnowledgeGraph.tsx` | D3.js 力导向图封装 |
| `GraphSidebar` | `components/graph/GraphSidebar.tsx` | 左侧面板（图例+筛选+详情） |
| `NodeDetail` | `components/graph/NodeDetail.tsx` | 选中节点属性展示 |

### 5.4 通用 UI 组件

| 组件 | 路径 | 说明 |
|------|------|------|
| `FeatureCard` | `components/ui/FeatureCard.tsx` | 功能特性卡片 |
| `CaseCard` | `components/ui/CaseCard.tsx` | 案例卡片 |
| `TestimonialCard` | `components/ui/TestimonialCard.tsx` | 评价卡片 |
| `SectionTitle` | `components/ui/SectionTitle.tsx` | 区块统一标题样式 |
| `ContactDialog` | `components/ui/ContactDialog.tsx` | 企业咨询联系表单对话框 |

---

## 6. 数据模型

### 6.1 图谱节点类型

```typescript
// types/graph.ts

type NodeType = 'process' | 'equipment' | 'material' | 'parameter' | 'issue';
type NodeCategory = 'CVD' | 'PVD' | 'ALD' | '通用';

interface GraphNode {
  id: string;
  label: string;
  type: NodeType;
  category: NodeCategory;
  description?: string;
  properties?: Record<string, string | number>;
}

interface GraphLink {
  source: string;
  target: string;
  relation: string;
  description?: string;
}

interface GraphData {
  nodes: GraphNode[];
  links: GraphLink[];
}
```

### 6.2 静态数据示例（`data/graph-static.json`）

初期 demo 包含约 30-50 个节点，聚焦薄膜沉积领域：

- **工艺节点**（~10 个）: CVD、PVD、ALD、PECVD、LPCVD、溅射 PVD、蒸发 PVD、Thermal ALD、Plasma ALD...
- **设备节点**（~15 个）: AMAT Endura、LAM Vector、TEL Tactras、ASMI XP8...
- **材料节点**（~10 个）: SiH4、WF6、TiCl4、Al 靶材...
- **参数节点**（~8 个）: 温度、压力、气体流量、薄膜厚度...
- **失效节点**（~8 个）: 颗粒污染、薄膜应力、均匀性不佳、台阶覆盖差...

### 6.3 节点颜色映射

| 类型 | 颜色 | Tailwind 类 |
|------|------|-------------|
| 工艺节点 | 蓝色 | `fill-blue-500` |
| 设备节点 | 绿色 | `fill-green-500` |
| 材料节点 | 黄色 | `fill-amber-500` |
| 参数节点 | 紫色 | `fill-purple-500` |
| 失效节点 | 红色 | `fill-red-500` |

---

## 7. 交互设计

### 7.1 导航系统

- 点击 Navbar 链接平滑滚动到对应区块（Landing Page）或跳转到对应页面
- 当前页面导航项高亮（`text-blue-600`）
- 移动端菜单展开时背景遮罩，点击遮罩关闭

### 7.2 图谱交互状态机

```
[空闲] --点击节点--> [节点选中]
[空闲] --滚轮--> [缩放]
[空闲] --拖拽画布--> [平移]
[空闲] --拖拽节点--> [节点重定位]
[节点选中] --点击空白--> [空闲]
[节点选中] --点击另一节点--> [节点选中]
```

### 7.3 表单交互

- **企业咨询表单**：名称、邮箱、公司、需求描述（textarea）
- 提交后显示「感谢提交，我们会尽快联系您」
- 初期不接入真实邮件服务，仅前端模拟成功状态

---

## 8. API 预留（Phase 2 填充）

```
src/app/api/
├── graph/
│   └── route.ts              # GET    /api/graph       → 返回完整图谱数据
├── nodes/
│   └── [id]/
│       └── route.ts          # GET    /api/nodes/:id   → 返回单个节点详情
└── contact/
    └── route.ts              # POST   /api/contact     → 提交企业咨询表单
```

**Phase 1 实现方式**：API 路由存在但返回静态 JSON 数据，前端统一通过 `fetch('/api/graph')` 获取，Phase 2 替换为真实数据库查询逻辑，前端无需修改。

---

## 9. 实施阶段

### Phase 1: Landing Page + 静态图谱（当前设计范围）

| 任务 | 预估时间 |
|------|---------|
| 项目初始化（Next.js + Tailwind + shadcn/ui） | 2h |
| 共享布局（Navbar + Footer） | 3h |
| Landing Page 区块（Hero + Trust + Value + CTA） | 6h |
| 功能特性页 | 3h |
| 知识图谱页（D3.js + 静态数据 + 交互） | 8h |
| 案例评价页 | 3h |
| API 路由占位（返回静态 JSON） | 2h |
| 响应式适配与性能优化 | 4h |
| **总计** | **~31h** |

### Phase 2: 后端 API + 数据管理

- 替换 `/api/graph` 为真实数据库查询（PostgreSQL + Neo4j）
- 用户认证（NextAuth.js）
- 数据贡献提交与审核流程
- 联系表单接入邮件服务

### Phase 3: 服务转化

- 人才匹配引擎
- 支付与分账系统
- 专家认证与评级

---

## 10. 性能与可访问性

- **图片优化**: 使用 Next.js `<Image>`，所有图片提供 WebP 格式
- **代码分割**: 图谱组件动态导入（`next/dynamic`），减少首屏 bundle
- **可访问性**: 所有图片有 alt 文本，交互元素有 focus 样式，颜色对比度符合 WCAG 2.1 AA
- **PWA 预留**: `manifest.json` 和 `robots.txt` 已预留位置

---

## 11. 风险评估

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| D3.js 与 React 集成复杂 | 中 | 使用 `useRef` + `useEffect` 模式，避免频繁 setState |
| 大量节点导致性能下降 | 中 | Phase 1 限制 50 节点，后续引入 canvas 渲染或 WebGL |
| 静态数据无法展示平台价值 | 低 | 数据标注来源和可信度，诚实展示「建设中」状态 |
| shadcn/ui 组件样式调整耗时 | 低 | 遵循默认设计系统，减少自定义覆盖 |
