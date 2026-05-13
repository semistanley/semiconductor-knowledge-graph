# 半导体知识图谱平台 Phase 1 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建一个基于 Next.js 的半导体薄膜沉积知识图谱平台 Landing Page，包含 4 个独立页面（Landing、Features、Graph、Cases）、共享布局、以及静态 D3.js 知识图谱可视化。

**Architecture:** Next.js 14 App Router + TypeScript + Tailwind CSS + shadcn/ui 组件库。D3.js 通过 `useRef` + `useEffect` 集成到 React 组件中渲染力导向图，避免与虚拟 DOM 冲突。所有页面采用 SSR/SSG，API 路由占位返回静态 JSON，Phase 2 可无缝替换为真实数据库查询。

**Tech Stack:** Next.js 14, TypeScript, Tailwind CSS, shadcn/ui, D3.js v7, Lucide React

**项目根目录:** `D:/wang/platform/`

---

## 文件结构总览

```
D:/wang/platform/
├── src/
│   ├── app/
│   │   ├── layout.tsx              # Root layout: fonts, metadata, providers
│   │   ├── page.tsx                # Landing Page
│   │   ├── features/
│   │   │   └── page.tsx            # 功能特性页
│   │   ├── graph/
│   │   │   └── page.tsx            # 知识图谱演示页
│   │   ├── cases/
│   │   │   └── page.tsx            # 案例评价页
│   │   └── api/
│   │       └── graph/
│   │           └── route.ts        # GET /api/graph (static JSON)
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Navbar.tsx          # 全局导航栏
│   │   │   └── Footer.tsx          # 全局页脚
│   │   ├── graph/
│   │   │   ├── KnowledgeGraph.tsx  # D3.js 力导向图封装
│   │   │   ├── GraphSidebar.tsx    # 左侧面板 (图例+筛选+详情)
│   │   │   └── NodeDetail.tsx      # 选中节点属性展示
│   │   └── ui/                     # shadcn/ui 组件 + 自定义 UI
│   │       ├── button.tsx          # shadcn Button
│   │       ├── card.tsx            # shadcn Card
│   │       ├── dialog.tsx          # shadcn Dialog
│   │       ├── tabs.tsx            # shadcn Tabs
│   │       ├── FeatureCard.tsx     # 功能特性卡片
│   │       ├── CaseCard.tsx        # 案例卡片
│   │       ├── TestimonialCard.tsx # 评价卡片
│   │       ├── SectionTitle.tsx    # 区块统一标题
│   │       └── ContactDialog.tsx   # 企业咨询联系表单
│   ├── data/
│   │   └── graph-static.json       # 静态图谱数据 (~50 nodes)
│   ├── types/
│   │   └── graph.ts                # 图谱类型定义
│   └── lib/
│       └── utils.ts                # cn() 工具函数
├── public/
│   └── images/                     # 静态图片资源
├── components.json                 # shadcn/ui 配置
├── tailwind.config.ts
├── next.config.js
└── package.json
```

---

## Task 1: 项目初始化

**Files:**
- Create: `D:/wang/platform/package.json`
- Create: `D:/wang/platform/tsconfig.json`
- Create: `D:/wang/platform/tailwind.config.ts`
- Create: `D:/wang/platform/next.config.js`
- Create: `D:/wang/platform/components.json`

- [ ] **Step 1: 创建 Next.js 项目**

Run:
```bash
cd D:/wang
npx create-next-app@latest platform --typescript --tailwind --eslint --app --src-dir --no-turbopack
```
Expected: 项目创建成功，`D:/wang/platform/` 目录存在。

- [ ] **Step 2: 安装依赖**

Run:
```bash
cd D:/wang/platform
npm install d3 lucide-react clsx tailwind-merge
npm install -D @types/d3
```
Expected: `package.json` 中新增 `d3`、`lucide-react`、`clsx`、`tailwind-merge`、`@types/d3`。

- [ ] **Step 3: 初始化 shadcn/ui**

Run:
```bash
cd D:/wang/platform
npx shadcn-ui@latest init --defaults
```
Expected: 生成 `components.json`，`src/lib/utils.ts` 包含 `cn()` 函数。

- [ ] **Step 4: 安装 shadcn/ui 基础组件**

Run:
```bash
cd D:/wang/platform
npx shadcn-ui@latest add button card dialog tabs
```
Expected: `src/components/ui/` 下生成 `button.tsx`, `card.tsx`, `dialog.tsx`, `tabs.tsx`。

- [ ] **Step 5: 配置 Tailwind 主题色**

Modify: `D:/wang/platform/tailwind.config.ts`

```typescript
import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};
export default config;
```

- [ ] **Step 6: 配置全局 CSS 变量**

Modify: `D:/wang/platform/src/app/globals.css`

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 221.2 83.2% 53.3%;
    --radius: 0.5rem;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
```

- [ ] **Step 7: 配置 next.config.js 为静态导出**

Modify: `D:/wang/platform/next.config.js`

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  distDir: 'dist',
  images: {
    unoptimized: true,
  },
};

module.exports = nextConfig;
```

- [ ] **Step 8: Commit**

Run:
```bash
cd D:/wang/platform
git init
git add .
git commit -m "$(cat <<'EOF'
init: Next.js project with shadcn/ui, Tailwind, D3.js

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: 类型定义与静态数据

**Files:**
- Create: `D:/wang/platform/src/types/graph.ts`
- Create: `D:/wang/platform/src/data/graph-static.json`

- [ ] **Step 1: 写图谱类型定义**

Create: `D:/wang/platform/src/types/graph.ts`

```typescript
export type NodeType = 'process' | 'equipment' | 'material' | 'parameter' | 'issue';
export type NodeCategory = 'CVD' | 'PVD' | 'ALD' | '通用';

export interface GraphNode {
  id: string;
  label: string;
  type: NodeType;
  category: NodeCategory;
  description?: string;
  properties?: Record<string, string | number>;
}

export interface GraphLink {
  source: string;
  target: string;
  relation: string;
  description?: string;
}

export interface GraphData {
  nodes: GraphNode[];
  links: GraphLink[];
}
```

- [ ] **Step 2: 写静态图谱 JSON 数据**

Create: `D:/wang/platform/src/data/graph-static.json`

```json
{
  "nodes": [
    { "id": "CVD", "label": "化学气相沉积", "type": "process", "category": "CVD", "description": "利用气态前驱体在衬底表面发生化学反应沉积薄膜" },
    { "id": "PVD", "label": "物理气相沉积", "type": "process", "category": "PVD", "description": "通过物理方法将材料转移到衬底表面形成薄膜" },
    { "id": "ALD", "label": "原子层沉积", "type": "process", "category": "ALD", "description": "通过交替暴露自限制反应实现原子级厚度控制" },
    { "id": "PECVD", "label": "等离子体增强 CVD", "type": "process", "category": "CVD", "description": "利用等离子体降低反应温度，提高沉积速率" },
    { "id": "LPCVD", "label": "低压 CVD", "type": "process", "category": "CVD", "description": "在低压环境下进行化学气相沉积，均匀性好" },
    { "id": "溅射", "label": "溅射 PVD", "type": "process", "category": "PVD", "description": "利用离子轰击靶材溅射出原子沉积到衬底" },
    { "id": "蒸发", "label": "热蒸发 PVD", "type": "process", "category": "PVD", "description": "加热使材料蒸发并在衬底上凝结成膜" },
    { "id": "Thermal_ALD", "label": "热式 ALD", "type": "process", "category": "ALD", "description": "仅依靠热能驱动表面反应的原子层沉积" },
    { "id": "Plasma_ALD", "label": "等离子体 ALD", "type": "process", "category": "ALD", "description": "利用等离子体增强反应活性的原子层沉积" },
    { "id": "AMAT_E500", "label": "AMAT Endura 5500", "type": "equipment", "category": "PVD", "description": "应用材料公司物理气相沉积设备" },
    { "id": "LAM_Vector", "label": "LAM Vector", "type": "equipment", "category": "CVD", "description": "泛林集团 CVD 设备" },
    { "id": "TEL_Tactras", "label": "TEL Tactras", "type": "equipment", "category": "CVD", "description": "东京电子 CVD 设备" },
    { "id": "ASMI_XP8", "label": "ASMI XP8", "type": "equipment", "category": "ALD", "description": "ASM International ALD 设备" },
    { "id": "AMAT_Producer", "label": "AMAT Producer", "type": "equipment", "category": "CVD", "description": "应用材料 PECVD 设备" },
    { "id": "SiH4", "label": "硅烷 SiH₄", "type": "material", "category": "CVD", "description": "常用于沉积多晶硅和氮化硅的前驱体" },
    { "id": "WF6", "label": "六氟化钨 WF₆", "type": "material", "category": "CVD", "description": "CVD 沉积钨薄膜的前驱体" },
    { "id": "TiCl4", "label": "四氯化钛 TiCl₄", "type": "material", "category": "CVD", "description": "用于沉积 Ti/TiN 阻挡层的前驱体" },
    { "id": "Al_target", "label": "铝靶材", "type": "material", "category": "PVD", "description": "PVD 溅射沉积铝互连层的靶材" },
    { "id": "Ti_target", "label": "钛靶材", "type": "material", "category": "PVD", "description": "PVD 溅射沉积钛阻挡层的靶材" },
    { "id": "温度", "label": "工艺温度", "type": "parameter", "category": "通用", "description": "沉积过程中的衬底加热温度" },
    { "id": "压力", "label": "腔体压力", "type": "parameter", "category": "通用", "description": "沉积腔内的真空度或工作压力" },
    { "id": "气体流量", "label": "反应气体流量", "type": "parameter", "category": "通用", "description": "通入反应腔的气体流量控制" },
    { "id": "功率", "label": "射频功率", "type": "parameter", "category": "通用", "description": "等离子体源或溅射靶的功率设定" },
    { "id": "颗粒", "label": "颗粒污染", "type": "issue", "category": "通用", "description": "薄膜表面或界面出现颗粒状缺陷" },
    { "id": "应力", "label": "薄膜应力", "type": "issue", "category": "通用", "description": "薄膜内部应力导致晶圆翘曲或薄膜开裂" },
    { "id": "均匀性", "label": "均匀性不佳", "type": "issue", "category": "通用", "description": "薄膜厚度或组分在晶圆表面分布不均匀" },
    { "id": "台阶覆盖", "label": "台阶覆盖差", "type": "issue", "category": "通用", "description": "高深宽比结构侧壁和底部薄膜覆盖不良" },
    { "id": "粘附性", "label": "薄膜粘附性差", "type": "issue", "category": "通用", "description": "薄膜与衬底界面结合力不足" }
  ],
  "links": [
    { "source": "CVD", "target": "AMAT_Producer", "relation": "使用设备" },
    { "source": "CVD", "target": "LAM_Vector", "relation": "使用设备" },
    { "source": "CVD", "target": "TEL_Tactras", "relation": "使用设备" },
    { "source": "PVD", "target": "AMAT_E500", "relation": "使用设备" },
    { "source": "PVD", "target": "溅射", "relation": "包含子工艺" },
    { "source": "PVD", "target": "蒸发", "relation": "包含子工艺" },
    { "source": "ALD", "target": "ASMI_XP8", "relation": "使用设备" },
    { "source": "ALD", "target": "Thermal_ALD", "relation": "包含子工艺" },
    { "source": "ALD", "target": "Plasma_ALD", "relation": "包含子工艺" },
    { "source": "CVD", "target": "SiH4", "relation": "使用材料" },
    { "source": "CVD", "target": "WF6", "relation": "使用材料" },
    { "source": "CVD", "target": "TiCl4", "relation": "使用材料" },
    { "source": "PVD", "target": "Al_target", "relation": "使用材料" },
    { "source": "PVD", "target": "Ti_target", "relation": "使用材料" },
    { "source": "CVD", "target": "温度", "relation": "关键参数" },
    { "source": "CVD", "target": "压力", "relation": "关键参数" },
    { "source": "CVD", "target": "气体流量", "relation": "关键参数" },
    { "source": "PVD", "target": "温度", "relation": "关键参数" },
    { "source": "PVD", "target": "压力", "relation": "关键参数" },
    { "source": "PVD", "target": "功率", "relation": "关键参数" },
    { "source": "CVD", "target": "颗粒", "relation": "常见问题" },
    { "source": "CVD", "target": "均匀性", "relation": "常见问题" },
    { "source": "PVD", "target": "应力", "relation": "常见问题" },
    { "source": "PVD", "target": "台阶覆盖", "relation": "常见问题" },
    { "source": "ALD", "target": "台阶覆盖", "relation": "常见问题" },
    { "source": "ALD", "target": "均匀性", "relation": "常见问题" },
    { "source": "PVD", "target": "粘附性", "relation": "常见问题" }
  ]
}
```

- [ ] **Step 3: Commit**

Run:
```bash
cd D:/wang/platform
git add src/types/graph.ts src/data/graph-static.json
git commit -m "$(cat <<'EOF'
feat: add graph types and static demo data (28 nodes, 27 edges)

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: API 路由占位

**Files:**
- Create: `D:/wang/platform/src/app/api/graph/route.ts`

- [ ] **Step 1: 写 API 路由**

Create: `D:/wang/platform/src/app/api/graph/route.ts`

```typescript
import { NextResponse } from 'next/server';
import graphData from '@/data/graph-static.json';

export async function GET() {
  return NextResponse.json(graphData);
}
```

- [ ] **Step 2: Commit**

Run:
```bash
cd D:/wang/platform
git add src/app/api/graph/route.ts
git commit -m "$(cat <<'EOF'
feat: add static graph API placeholder

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: 共享布局组件

**Files:**
- Create: `D:/wang/platform/src/components/layout/Navbar.tsx`
- Create: `D:/wang/platform/src/components/layout/Footer.tsx`
- Modify: `D:/wang/platform/src/app/layout.tsx`

- [ ] **Step 1: 写 Navbar 组件**

Create: `D:/wang/platform/src/components/layout/Navbar.tsx`

```typescript
'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Menu, X, Atom } from 'lucide-react';
import { Button } from '@/components/ui/button';

const navLinks = [
  { href: '/features', label: '功能' },
  { href: '/graph', label: '图谱' },
  { href: '/cases', label: '案例' },
];

export function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const pathname = usePathname();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 80);
    window.addEventListener('scroll', onScroll);
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled ? 'bg-white/90 backdrop-blur shadow-sm' : 'bg-transparent'
      }`}
    >
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          <Link href="/" className="flex items-center gap-2 text-xl font-bold text-slate-900">
            <Atom className="h-6 w-6 text-blue-600" />
            <span>半导体知识图谱</span>
          </Link>

          <nav className="hidden md:flex items-center gap-8">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className={`text-sm font-medium transition-colors hover:text-blue-600 ${
                  pathname === link.href ? 'text-blue-600' : 'text-slate-600'
                }`}
              >
                {link.label}
              </Link>
            ))}
            <Button asChild size="sm">
              <Link href="/graph">免费体验</Link>
            </Button>
          </nav>

          <button
            className="md:hidden p-2 text-slate-600"
            onClick={() => setMobileOpen(!mobileOpen)}
            aria-label="切换菜单"
          >
            {mobileOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>
      </div>

      {mobileOpen && (
        <div className="md:hidden bg-white border-t">
          <div className="space-y-1 px-4 py-4">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className={`block px-3 py-2 rounded-md text-base font-medium ${
                  pathname === link.href
                    ? 'bg-blue-50 text-blue-600'
                    : 'text-slate-600 hover:bg-slate-50'
                }`}
                onClick={() => setMobileOpen(false)}
              >
                {link.label}
              </Link>
            ))}
            <div className="pt-2">
              <Button asChild className="w-full">
                <Link href="/graph">免费体验</Link>
              </Button>
            </div>
          </div>
        </div>
      )}
    </header>
  );
}
```

- [ ] **Step 2: 写 Footer 组件**

Create: `D:/wang/platform/src/components/layout/Footer.tsx`

```typescript
import Link from 'next/link';
import { Atom } from 'lucide-react';

const footerLinks = {
  产品: [
    { label: '功能特性', href: '/features' },
    { label: '知识图谱', href: '/graph' },
    { label: '客户案例', href: '/cases' },
  ],
  资源: [
    { label: '技术博客', href: '#' },
    { label: 'API 文档', href: '#' },
    { label: '工艺白皮书', href: '#' },
  ],
  公司: [
    { label: '关于我们', href: '#' },
    { label: '联系我们', href: '#' },
    { label: '加入我们', href: '#' },
  ],
  法律: [
    { label: '隐私政策', href: '#' },
    { label: '服务条款', href: '#' },
  ],
};

export function Footer() {
  return (
    <footer className="bg-slate-900 text-slate-300">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-2 md:grid-cols-5 gap-8">
          <div className="col-span-2 md:col-span-1">
            <Link href="/" className="flex items-center gap-2 text-lg font-bold text-white">
              <Atom className="h-5 w-5 text-blue-400" />
              <span>半导体知识图谱</span>
            </Link>
            <p className="mt-4 text-sm text-slate-400">
              打造半导体制造领域的知识基础设施
            </p>
          </div>
          {Object.entries(footerLinks).map(([category, links]) => (
            <div key={category}>
              <h3 className="text-sm font-semibold text-white uppercase tracking-wider">{category}</h3>
              <ul className="mt-4 space-y-2">
                {links.map((link) => (
                  <li key={link.label}>
                    <Link href={link.href} className="text-sm hover:text-white transition-colors">
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        <div className="mt-12 pt-8 border-t border-slate-800 text-sm text-slate-400 text-center">
          © 2026 半导体知识图谱平台. All rights reserved.
        </div>
      </div>
    </footer>
  );
}
```

- [ ] **Step 3: 修改 Root Layout**

Modify: `D:/wang/platform/src/app/layout.tsx`

```typescript
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "半导体知识图谱平台 | 薄膜沉积工艺专家社区",
  description: "半导体薄膜沉积领域首个知识图谱平台，连接工艺工程师与企业客户，提供工艺查询、专家外派与审厂服务。",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body className={inter.className}>
        <Navbar />
        <main className="min-h-screen">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
```

- [ ] **Step 4: Commit**

Run:
```bash
cd D:/wang/platform
git add src/components/layout/ src/app/layout.tsx
git commit -m "$(cat <<'EOF'
feat: add Navbar, Footer, and Root Layout with metadata

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

## Task 5: Landing Page (`/`)

**Files:**
- Create: `D:/wang/platform/src/components/ui/SectionTitle.tsx`
- Create: `D:/wang/platform/src/components/ui/ContactDialog.tsx`
- Create: `D:/wang/platform/src/app/sections/HeroSection.tsx`
- Create: `D:/wang/platform/src/app/sections/TrustBar.tsx`
- Create: `D:/wang/platform/src/app/sections/ValueProposition.tsx`
- Create: `D:/wang/platform/src/app/sections/BottomCTA.tsx`
- Modify: `D:/wang/platform/src/app/page.tsx`

- [ ] **Step 1: 写 SectionTitle 组件**

Create: `D:/wang/platform/src/components/ui/SectionTitle.tsx`

```typescript
interface SectionTitleProps {
  title: string;
  subtitle?: string;
  centered?: boolean;
}

export function SectionTitle({ title, subtitle, centered = true }: SectionTitleProps) {
  return (
    <div className={`mb-12 ${centered ? 'text-center' : ''}`}>
      <h2 className="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">{title}</h2>
      {subtitle && (
        <p className="mt-4 text-lg text-slate-600 max-w-2xl mx-auto">{subtitle}</p>
      )}
    </div>
  );
}
```

- [ ] **Step 2: 写 ContactDialog 组件**

Create: `D:/wang/platform/src/components/ui/ContactDialog.tsx`

```typescript
'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';

export function ContactDialog({ children }: { children: React.ReactNode }) {
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <Dialog>
      <DialogTrigger asChild>{children}</DialogTrigger>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>申请企业咨询</DialogTitle>
          <DialogDescription>留下您的信息，我们的专家将在 24 小时内联系您。</DialogDescription>
        </DialogHeader>
        {submitted ? (
          <div className="py-8 text-center">
            <p className="text-green-600 font-medium">感谢提交！我们会尽快联系您。</p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4 py-4">
            <div>
              <label className="block text-sm font-medium text-slate-700">姓名</label>
              <input required type="text" className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500" />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700">邮箱</label>
              <input required type="email" className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500" />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700">公司</label>
              <input required type="text" className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500" />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700">需求描述</label>
              <textarea required rows={3} className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500" />
            </div>
            <Button type="submit" className="w-full">提交申请</Button>
          </form>
        )}
      </DialogContent>
    </Dialog>
  );
}
```

- [ ] **Step 3: 写 HeroSection 组件**

Create: `D:/wang/platform/src/app/sections/HeroSection.tsx`

```typescript
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { ContactDialog } from '@/components/ui/ContactDialog';
import { Atom, ArrowRight } from 'lucide-react';

export function HeroSection() {
  return (
    <section className="relative overflow-hidden bg-gradient-to-b from-blue-50 to-white pt-32 pb-20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div>
            <h1 className="text-4xl font-bold tracking-tight text-slate-900 sm:text-6xl">
              半导体薄膜沉积<br />
              <span className="text-blue-600">知识图谱</span>
            </h1>
            <p className="mt-6 text-xl text-slate-600">
              工艺透明化 · 人才精准化 · 方案系统化
            </p>
            <div className="mt-10 flex flex-wrap gap-4">
              <Button asChild size="lg">
                <Link href="/graph">
                  立即体验图谱 <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
              <ContactDialog>
                <Button variant="outline" size="lg">申请企业咨询</Button>
              </ContactDialog>
            </div>
          </div>
          <div className="relative flex items-center justify-center">
            <div className="relative w-80 h-80 lg:w-96 lg:h-96">
              <div className="absolute inset-0 rounded-full bg-blue-100 animate-pulse opacity-50" />
              <div className="absolute inset-4 rounded-full bg-blue-200 opacity-40" />
              <div className="absolute inset-8 rounded-full bg-blue-300 opacity-30" />
              <div className="absolute inset-0 flex items-center justify-center">
                <Atom className="h-24 w-24 text-blue-600" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
```

- [ ] **Step 4: 写 TrustBar 组件**

Create: `D:/wang/platform/src/app/sections/TrustBar.tsx`

```typescript
export function TrustBar() {
  const stats = [
    { label: '薄膜沉积工艺', value: '12+' },
    { label: '设备型号', value: '300+' },
    { label: '认证工程师', value: '50+' },
  ];

  const logos = ['AMAT', 'LAM', 'TEL', 'ASMI', 'SCREEN'];

  return (
    <section className="border-y bg-white py-10">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex flex-wrap justify-center gap-8 md:gap-16 mb-8">
          {stats.map((stat) => (
            <div key={stat.label} className="text-center">
              <div className="text-3xl font-bold text-blue-600">{stat.value}</div>
              <div className="text-sm text-slate-500 mt-1">{stat.label}</div>
            </div>
          ))}
        </div>
        <div className="flex flex-wrap justify-center gap-8 md:gap-12 opacity-40">
          {logos.map((logo) => (
            <span key={logo} className="text-lg font-bold text-slate-400 tracking-wider">
              {logo}
            </span>
          ))}
        </div>
      </div>
    </section>
  );
}
```

- [ ] **Step 5: 写 ValueProposition 组件**

Create: `D:/wang/platform/src/app/sections/ValueProposition.tsx`

```typescript
import { Wrench, Building2, CheckCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { ContactDialog } from '@/components/ui/ContactDialog';
import Link from 'next/link';
import { SectionTitle } from '@/components/ui/SectionTitle';

const engineerFeatures = [
  '查询工艺参数与失效模式',
  '贡献数据赚取积分与收入',
  '建立个人技术影响力',
];

const enterpriseFeatures = [
  '工艺问题快速诊断',
  '专家人才按需外派',
  '审厂预审全包服务',
];

export function ValueProposition() {
  return (
    <section className="py-20 bg-slate-50">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <SectionTitle
          title="为不同角色创造价值"
          subtitle="无论是深耕一线的工艺工程师，还是寻求突破的企业客户，都能在这里找到所需"
        />
        <div className="grid md:grid-cols-2 gap-8">
          <div className="bg-white rounded-2xl p-8 shadow-sm border">
            <div className="flex items-center gap-3 mb-6">
              <div className="p-3 bg-blue-50 rounded-lg">
                <Wrench className="h-6 w-6 text-blue-600" />
              </div>
              <h3 className="text-xl font-bold text-slate-900">为半导体工程师打造</h3>
            </div>
            <ul className="space-y-3 mb-8">
              {engineerFeatures.map((f) => (
                <li key={f} className="flex items-start gap-3">
                  <CheckCircle className="h-5 w-5 text-blue-500 mt-0.5 shrink-0" />
                  <span className="text-slate-600">{f}</span>
                </li>
              ))}
            </ul>
            <Button asChild variant="outline" className="w-full">
              <Link href="/graph">加入工程师社区</Link>
            </Button>
          </div>

          <div className="bg-white rounded-2xl p-8 shadow-sm border">
            <div className="flex items-center gap-3 mb-6">
              <div className="p-3 bg-green-50 rounded-lg">
                <Building2 className="h-6 w-6 text-green-600" />
              </div>
              <h3 className="text-xl font-bold text-slate-900">为企业客户赋能</h3>
            </div>
            <ul className="space-y-3 mb-8">
              {enterpriseFeatures.map((f) => (
                <li key={f} className="flex items-start gap-3">
                  <CheckCircle className="h-5 w-5 text-green-500 mt-0.5 shrink-0" />
                  <span className="text-slate-600">{f}</span>
                </li>
              ))}
            </ul>
            <ContactDialog>
              <Button variant="outline" className="w-full">预约企业演示</Button>
            </ContactDialog>
          </div>
        </div>
      </div>
    </section>
  );
}
```

- [ ] **Step 6: 写 BottomCTA 组件**

Create: `D:/wang/platform/src/app/sections/BottomCTA.tsx`

```typescript
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { ArrowRight } from 'lucide-react';

export function BottomCTA() {
  return (
    <section className="py-20 bg-blue-600">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
        <h2 className="text-3xl font-bold text-white sm:text-4xl">
          准备好让薄膜沉积工艺更透明了吗？
        </h2>
        <p className="mt-4 text-blue-100 text-lg">
          立即探索交互式知识图谱，发现工艺之间的隐藏关联
        </p>
        <div className="mt-10">
          <Button asChild size="lg" variant="secondary">
            <Link href="/graph">
              立即开始 <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </Button>
        </div>
      </div>
    </section>
  );
}
```

- [ ] **Step 7: 组装 Landing Page**

Modify: `D:/wang/platform/src/app/page.tsx`

```typescript
import { HeroSection } from './sections/HeroSection';
import { TrustBar } from './sections/TrustBar';
import { ValueProposition } from './sections/ValueProposition';
import { BottomCTA } from './sections/BottomCTA';

export default function Home() {
  return (
    <>
      <HeroSection />
      <TrustBar />
      <ValueProposition />
      <BottomCTA />
    </>
  );
}
```

- [ ] **Step 8: Commit**

Run:
```bash
cd D:/wang/platform
git add src/components/ui/SectionTitle.tsx src/components/ui/ContactDialog.tsx src/app/sections/ src/app/page.tsx
git commit -m "$(cat <<'EOF'
feat: implement Landing Page with Hero, TrustBar, ValueProposition, BottomCTA

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

## Task 6: 功能特性页 (`/features`)

**Files:**
- Create: `D:/wang/platform/src/app/sections/FeatureGrid.tsx`
- Create: `D:/wang/platform/src/components/ui/FeatureCard.tsx`
- Modify: `D:/wang/platform/src/app/features/page.tsx`

- [ ] **Step 1: 写 FeatureCard 组件**

Create: `D:/wang/platform/src/components/ui/FeatureCard.tsx`

```typescript
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { LucideIcon } from 'lucide-react';

interface FeatureCardProps {
  icon: LucideIcon;
  title: string;
  description: string;
}

export function FeatureCard({ icon: Icon, title, description }: FeatureCardProps) {
  return (
    <Card className="h-full">
      <CardHeader>
        <Icon className="h-8 w-8 text-blue-600 mb-2" />
        <CardTitle className="text-lg">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-slate-600 text-sm">{description}</p>
      </CardContent>
    </Card>
  );
}
```

- [ ] **Step 2: 写 FeatureGrid 组件**

Create: `D:/wang/platform/src/app/sections/FeatureGrid.tsx`

```typescript
'use client';

import { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { FeatureCard } from '@/components/ui/FeatureCard';
import { SectionTitle } from '@/components/ui/SectionTitle';
import {
  Compass, BarChart3, Stethoscope, Upload, Coins, Award,
  MessageSquare, ShieldCheck, FileSearch, Users, Database, GraduationCap,
} from 'lucide-react';

const engineerFeatures = [
  { icon: Compass, title: '工艺导航器', description: '输入目标工艺需求，系统推荐最优工艺路线与参数组合。' },
  { icon: BarChart3, title: '设备比对器', description: '横向对比不同厂商设备在特定工艺下的表现数据。' },
  { icon: Stethoscope, title: '问题诊断器', description: '输入不良现象，快速匹配失效模式与历史解决方案。' },
  { icon: Upload, title: '知识贡献', description: '一键提交工艺数据与经验，支持 Excel/PDF 批量导入。' },
  { icon: Coins, title: '积分体系', description: '每通过一条审核数据获得「沉积点」，可兑换培训与会议门票。' },
  { icon: Award, title: '专家认证', description: '通过贡献积累信誉，申请领域认证工程师头衔。' },
];

const enterpriseFeatures = [
  { icon: MessageSquare, title: '工艺咨询', description: '按小时计费的专家远程诊断，7×24 小时问答支持。' },
  { icon: ShieldCheck, title: '审厂预审', description: '文档预审 + 远程模拟审厂 + 关键问题清单及整改建议。' },
  { icon: FileSearch, title: '设备选型', description: '定制化设备对比分析、全生命周期成本测算与谈判建议。' },
  { icon: Users, title: '人才外派', description: '按工艺专长精准匹配工程师，提供驻场支持服务。' },
  { icon: Database, title: '数据服务', description: '定制行业分析报告、竞品对标与良率基准分析。' },
  { icon: GraduationCap, title: '企业订阅', description: '分级访问知识图谱数据，支持团队账号与权限管理。' },
];

export function FeatureGrid() {
  const [activeTab, setActiveTab] = useState('engineer');

  return (
    <section className="py-20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <SectionTitle title="平台功能" subtitle="为工程师与企业分别打造的专属工具集" />
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <div className="flex justify-center mb-10">
            <TabsList className="grid w-full max-w-md grid-cols-2">
              <TabsTrigger value="engineer">工程师端</TabsTrigger>
              <TabsTrigger value="enterprise">企业端</TabsTrigger>
            </TabsList>
          </div>
          <TabsContent value="engineer">
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {engineerFeatures.map((f) => (
                <FeatureCard key={f.title} {...f} />
              ))}
            </div>
          </TabsContent>
          <TabsContent value="enterprise">
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {enterpriseFeatures.map((f) => (
                <FeatureCard key={f.title} {...f} />
              ))}
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </section>
  );
}
```

- [ ] **Step 3: 组装功能特性页**

Modify: `D:/wang/platform/src/app/features/page.tsx`

```typescript
import type { Metadata } from 'next';
import { FeatureGrid } from '../sections/FeatureGrid';

export const metadata: Metadata = {
  title: '平台功能 | 工程师工具 & 企业解决方案',
  description: '为半导体工程师提供工艺查询与数据贡献工具，为企业提供专家外派与审厂服务。',
};

export default function FeaturesPage() {
  return <FeatureGrid />;
}
```

- [ ] **Step 4: Commit**

Run:
```bash
cd D:/wang/platform
git add src/components/ui/FeatureCard.tsx src/app/sections/FeatureGrid.tsx src/app/features/page.tsx
git commit -m "$(cat <<'EOF'
feat: implement Features page with engineer/enterprise tabs

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

## Task 7: 知识图谱页 (`/graph`) — D3.js 可视化

**Files:**
- Create: `D:/wang/platform/src/components/graph/NodeDetail.tsx`
- Create: `D:/wang/platform/src/components/graph/GraphSidebar.tsx`
- Create: `D:/wang/platform/src/components/graph/KnowledgeGraph.tsx`
- Modify: `D:/wang/platform/src/app/graph/page.tsx`

- [ ] **Step 1: 写 NodeDetail 组件**

Create: `D:/wang/platform/src/components/graph/NodeDetail.tsx`

```typescript
import { GraphNode } from '@/types/graph';

interface NodeDetailProps {
  node: GraphNode | null;
}

const typeLabels: Record<string, string> = {
  process: '工艺节点',
  equipment: '设备型号',
  material: '材料参数',
  parameter: '工艺参数',
  issue: '失效模式',
};

export function NodeDetail({ node }: NodeDetailProps) {
  if (!node) {
    return (
      <div className="text-sm text-slate-400">
        点击图谱中的节点查看详细信息
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <div>
        <span className="text-xs font-medium text-slate-400 uppercase">名称</span>
        <p className="text-sm font-semibold text-slate-900">{node.label}</p>
      </div>
      <div>
        <span className="text-xs font-medium text-slate-400 uppercase">类型</span>
        <p className="text-sm text-slate-700">{typeLabels[node.type] || node.type}</p>
      </div>
      <div>
        <span className="text-xs font-medium text-slate-400 uppercase">分类</span>
        <p className="text-sm text-slate-700">{node.category}</p>
      </div>
      {node.description && (
        <div>
          <span className="text-xs font-medium text-slate-400 uppercase">描述</span>
          <p className="text-sm text-slate-600 mt-1">{node.description}</p>
        </div>
      )}
    </div>
  );
}
```

- [ ] **Step 2: 写 GraphSidebar 组件**

Create: `D:/wang/platform/src/components/graph/GraphSidebar.tsx`

```typescript
import { GraphNode, NodeType } from '@/types/graph';
import { NodeDetail } from './NodeDetail';

interface GraphSidebarProps {
  selectedNode: GraphNode | null;
  filter: NodeType | 'all';
  onFilterChange: (type: NodeType | 'all') => void;
}

const typeOptions: { value: NodeType | 'all'; label: string; color: string }[] = [
  { value: 'all', label: '全部', color: 'bg-slate-400' },
  { value: 'process', label: '工艺节点', color: 'bg-blue-500' },
  { value: 'equipment', label: '设备型号', color: 'bg-green-500' },
  { value: 'material', label: '材料参数', color: 'bg-amber-500' },
  { value: 'parameter', label: '工艺参数', color: 'bg-purple-500' },
  { value: 'issue', label: '失效模式', color: 'bg-red-500' },
];

export function GraphSidebar({ selectedNode, filter, onFilterChange }: GraphSidebarProps) {
  return (
    <div className="w-72 bg-white border-r flex flex-col h-full shrink-0">
      <div className="p-4 border-b">
        <h3 className="font-semibold text-slate-900">图例</h3>
        <div className="mt-3 space-y-2">
          {typeOptions.map((opt) => (
            <button
              key={opt.value}
              onClick={() => onFilterChange(opt.value)}
              className={`flex items-center gap-2 w-full text-left px-2 py-1.5 rounded-md text-sm transition-colors ${
                filter === opt.value ? 'bg-slate-100 font-medium' : 'hover:bg-slate-50'
              }`}
            >
              <span className={`w-3 h-3 rounded-full ${opt.color}`} />
              <span className="text-slate-700">{opt.label}</span>
            </button>
          ))}
        </div>
      </div>
      <div className="p-4 flex-1 overflow-auto">
        <h3 className="font-semibold text-slate-900 mb-3">节点详情</h3>
        <NodeDetail node={selectedNode} />
      </div>
    </div>
  );
}
```

- [ ] **Step 3: 写 KnowledgeGraph 组件**

Create: `D:/wang/platform/src/components/graph/KnowledgeGraph.tsx`

```typescript
'use client';

import { useRef, useEffect, useCallback } from 'react';
import * as d3 from 'd3';
import { GraphData, GraphNode, NodeType } from '@/types/graph';

interface KnowledgeGraphProps {
  data: GraphData;
  filter: NodeType | 'all';
  onNodeClick: (node: GraphNode | null) => void;
}

const colorMap: Record<NodeType, string> = {
  process: '#3b82f6',
  equipment: '#22c55e',
  material: '#f59e0b',
  parameter: '#a855f7',
  issue: '#ef4444',
};

export function KnowledgeGraph({ data, filter, onNodeClick }: KnowledgeGraphProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const svgRef = useRef<SVGSVGElement | null>(null);
  const simulationRef = useRef<d3.Simulation<d3.SimulationNodeDatum, undefined> | null>(null);

  const render = useCallback(() => {
    if (!containerRef.current) return;

    const container = containerRef.current;
    const width = container.clientWidth;
    const height = container.clientHeight;

    const filteredNodes = filter === 'all'
      ? data.nodes
      : data.nodes.filter((n) => n.type === filter);

    const nodeIds = new Set(filteredNodes.map((n) => n.id));
    const filteredLinks = data.links.filter(
      (l) => nodeIds.has(l.source as string) && nodeIds.has(l.target as string)
    );

    d3.select(container).selectAll('*').remove();

    const svg = d3.select(container)
      .append('svg')
      .attr('width', width)
      .attr('height', height)
      .attr('viewBox', [0, 0, width, height])
      .style('max-width', '100%')
      .style('height', 'auto');

    svgRef.current = svg.node();

    const g = svg.append('g');

    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.1, 5])
      .on('zoom', (event) => {
        g.attr('transform', event.transform);
      });

    svg.call(zoom);

    const simulation = d3.forceSimulation(filteredNodes as d3.SimulationNodeDatum[])
      .force('link', d3.forceLink(filteredLinks).id((d: any) => d.id).distance(100))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius(40));

    simulationRef.current = simulation;

    const link = g.append('g')
      .attr('stroke', '#94a3b8')
      .attr('stroke-opacity', 0.6)
      .selectAll('line')
      .data(filteredLinks)
      .join('line')
      .attr('stroke-width', 1.5);

    const node = g.append('g')
      .selectAll('g')
      .data(filteredNodes)
      .join('g')
      .attr('cursor', 'pointer')
      .call(
        d3.drag<SVGGElement, GraphNode>()
          .on('start', (event, d) => {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            (d as any).fx = (d as any).x;
            (d as any).fy = (d as any).y;
          })
          .on('drag', (event, d) => {
            (d as any).fx = event.x;
            (d as any).fy = event.y;
          })
          .on('end', (event, d) => {
            if (!event.active) simulation.alphaTarget(0);
            (d as any).fx = null;
            (d as any).fy = null;
          })
      );

    node.append('circle')
      .attr('r', 18)
      .attr('fill', (d) => colorMap[d.type])
      .attr('stroke', '#fff')
      .attr('stroke-width', 2);

    node.append('text')
      .attr('dy', 32)
      .attr('text-anchor', 'middle')
      .attr('font-size', '10px')
      .attr('fill', '#334155')
      .attr('font-weight', '500')
      .text((d) => d.label);

    node.on('click', (event, d) => {
      event.stopPropagation();
      onNodeClick(d);

      node.selectAll('circle')
        .attr('stroke', '#fff')
        .attr('stroke-width', 2)
        .attr('opacity', 0.2);

      link.attr('opacity', 0.1);

      const connectedIds = new Set<string>([d.id]);
      filteredLinks.forEach((l) => {
        if ((l.source as any).id === d.id) connectedIds.add((l.target as any).id);
        if ((l.target as any).id === d.id) connectedIds.add((l.source as any).id);
      });

      node.filter((n) => connectedIds.has(n.id))
        .selectAll('circle')
        .attr('opacity', 1)
        .attr('stroke', '#1e293b')
        .attr('stroke-width', 3);

      link.filter((l: any) => l.source.id === d.id || l.target.id === d.id)
        .attr('opacity', 1)
        .attr('stroke', '#3b82f6')
        .attr('stroke-width', 2);
    });

    svg.on('click', () => {
      onNodeClick(null);
      node.selectAll('circle')
        .attr('stroke', '#fff')
        .attr('stroke-width', 2)
        .attr('opacity', 1);
      link.attr('opacity', 0.6)
        .attr('stroke', '#94a3b8')
        .attr('stroke-width', 1.5);
    });

    simulation.on('tick', () => {
      link
        .attr('x1', (d: any) => d.source.x)
        .attr('y1', (d: any) => d.source.y)
        .attr('x2', (d: any) => d.target.x)
        .attr('y2', (d: any) => d.target.y);

      node.attr('transform', (d: any) => `translate(${d.x},${d.y})`);
    });
  }, [data, filter, onNodeClick]);

  useEffect(() => {
    render();

    const handleResize = () => {
      if (simulationRef.current) {
        simulationRef.current.stop();
      }
      render();
    };

    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
      if (simulationRef.current) {
        simulationRef.current.stop();
      }
    };
  }, [render]);

  return (
    <div
      ref={containerRef}
      className="flex-1 bg-slate-50 relative overflow-hidden"
      style={{ height: 'calc(100vh - 64px)' }}
    />
  );
}
```

- [ ] **Step 4: 组装图谱页**

Modify: `D:/wang/platform/src/app/graph/page.tsx`

```typescript
'use client';

import { useState, useEffect } from 'react';
import type { Metadata } from 'next';
import { GraphSidebar } from '@/components/graph/GraphSidebar';
import { KnowledgeGraph } from '@/components/graph/KnowledgeGraph';
import { GraphData, GraphNode, NodeType } from '@/types/graph';

export default function GraphPage() {
  const [data, setData] = useState<GraphData>({ nodes: [], links: [] });
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
  const [filter, setFilter] = useState<NodeType | 'all'>('all');

  useEffect(() => {
    fetch('/api/graph')
      .then((res) => res.json())
      .then((d: GraphData) => setData(d));
  }, []);

  return (
    <div className="flex pt-16">
      <GraphSidebar
        selectedNode={selectedNode}
        filter={filter}
        onFilterChange={setFilter}
      />
      <KnowledgeGraph
        data={data}
        filter={filter}
        onNodeClick={setSelectedNode}
      />
    </div>
  );
}
```

- [ ] **Step 5: Commit**

Run:
```bash
cd D:/wang/platform
git add src/components/graph/ src/app/graph/page.tsx
git commit -m "$(cat <<'EOF'
feat: implement interactive knowledge graph with D3.js force layout

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

## Task 8: 案例评价页 (`/cases`)

**Files:**
- Create: `D:/wang/platform/src/components/ui/CaseCard.tsx`
- Create: `D:/wang/platform/src/components/ui/TestimonialCard.tsx`
- Create: `D:/wang/platform/src/app/sections/CaseGrid.tsx`
- Create: `D:/wang/platform/src/app/sections/TestimonialCarousel.tsx`
- Modify: `D:/wang/platform/src/app/cases/page.tsx`

- [ ] **Step 1: 写 CaseCard 组件**

Create: `D:/wang/platform/src/components/ui/CaseCard.tsx`

```typescript
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { TrendingUp } from 'lucide-react';

interface CaseCardProps {
  industry: string;
  problem: string;
  solution: string;
  result: string;
}

export function CaseCard({ industry, problem, solution, result }: CaseCardProps) {
  return (
    <Card className="h-full">
      <CardHeader>
        <div className="text-xs font-medium text-blue-600 uppercase tracking-wider mb-1">{industry}</div>
        <CardTitle className="text-lg">{problem}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        <div>
          <span className="text-xs font-medium text-slate-400 uppercase">解决方案</span>
          <p className="text-sm text-slate-600 mt-1">{solution}</p>
        </div>
        <div className="flex items-center gap-2 pt-2 border-t">
          <TrendingUp className="h-4 w-4 text-green-500" />
          <span className="text-sm font-medium text-green-700">{result}</span>
        </div>
      </CardContent>
    </Card>
  );
}
```

- [ ] **Step 2: 写 TestimonialCard 组件**

Create: `D:/wang/platform/src/components/ui/TestimonialCard.tsx`

```typescript
import { Star, User } from 'lucide-react';

interface TestimonialCardProps {
  name: string;
  role: string;
  content: string;
  rating: number;
}

export function TestimonialCard({ name, role, content, rating }: TestimonialCardProps) {
  return (
    <div className="bg-white rounded-xl p-6 shadow-sm border">
      <div className="flex items-center gap-4 mb-4">
        <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center">
          <User className="h-6 w-6 text-slate-400" />
        </div>
        <div>
          <div className="font-semibold text-slate-900">{name}</div>
          <div className="text-sm text-slate-500">{role}</div>
        </div>
      </div>
      <div className="flex gap-0.5 mb-3">
        {Array.from({ length: 5 }).map((_, i) => (
          <Star
            key={i}
            className={`h-4 w-4 ${i < rating ? 'text-amber-400 fill-amber-400' : 'text-slate-200'}`}
          />
        ))}
      </div>
      <p className="text-slate-600 text-sm leading-relaxed">{content}</p>
    </div>
  );
}
```

- [ ] **Step 3: 写 CaseGrid 组件**

Create: `D:/wang/platform/src/app/sections/CaseGrid.tsx`

```typescript
import { CaseCard } from '@/components/ui/CaseCard';
import { SectionTitle } from '@/components/ui/SectionTitle';

const cases = [
  {
    industry: '中小型 Foundry',
    problem: '28nm 节点 SiN 薄膜应力导致晶圆翘曲',
    solution: '通过图谱匹配同工艺历史案例，推荐优化沉积温度梯度与退火参数',
    result: '应力降低 35%，晶圆翘曲达标率从 72% 提升至 96%',
  },
  {
    industry: '功率器件厂商',
    problem: 'IGBT 模块 Al 金属化层粘附性不足',
    solution: '引入 Ti/TiN 阻挡层工艺方案，优化溅射功率与气压参数',
    result: '粘附强度提升 2 倍，模块可靠性通过 AEC-Q101 认证',
  },
  {
    industry: 'MEMS 代工厂',
    problem: '高深宽比结构台阶覆盖差',
    solution: '将 PECVD 切换为 ALD 工艺，调整前驱体脉冲时间',
    result: '台阶覆盖率从 45% 提升至 92%，器件良率提升 18%',
  },
  {
    industry: '存储器厂商',
    problem: '3D NAND 字线钨填充空洞缺陷',
    solution: '优化 WF6 还原工艺，调整 SiH4/WF6 流量比与分步沉积策略',
    result: '空洞缺陷率从 8% 降至 0.5%，产能提升 12%',
  },
];

export function CaseGrid() {
  return (
    <section className="py-20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <SectionTitle title="客户案例" subtitle="真实工艺难题与解决方案" />
        <div className="grid md:grid-cols-2 gap-6">
          {cases.map((c) => (
            <CaseCard key={c.problem} {...c} />
          ))}
        </div>
      </div>
    </section>
  );
}
```

- [ ] **Step 4: 写 TestimonialCarousel 组件**

Create: `D:/wang/platform/src/app/sections/TestimonialCarousel.tsx`

```typescript
import { TestimonialCard } from '@/components/ui/TestimonialCard';
import { SectionTitle } from '@/components/ui/SectionTitle';

const testimonials = [
  {
    name: '张工',
    role: '前 AMAT 工艺工程师',
    content: '这个平台让我多年积累的经验有了量化出口。通过贡献数据获得的积分，我已经兑换了两次 SEMICON China 的门票。',
    rating: 5,
  },
  {
    name: '李总监',
    role: '某 Foundry 工艺整合部',
    content: '审厂预审服务帮我们提前发现了 7 个潜在不符合项，正式审厂一次通过，节省了大量整改时间和成本。',
    rating: 5,
  },
  {
    name: '王博士',
    role: '高校研究员',
    content: '图谱把分散在论文中的工艺参数关系可视化了，对我的研究启发很大。期待更多工艺模块上线。',
    rating: 4,
  },
];

export function TestimonialCarousel() {
  return (
    <section className="py-20 bg-slate-50">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <SectionTitle title="专家评价" subtitle="来自社区成员与企业客户的真实反馈" />
        <div className="grid md:grid-cols-3 gap-6">
          {testimonials.map((t) => (
            <TestimonialCard key={t.name} {...t} />
          ))}
        </div>
      </div>
    </section>
  );
}
```

- [ ] **Step 5: 组装案例评价页**

Modify: `D:/wang/platform/src/app/cases/page.tsx`

```typescript
import type { Metadata } from 'next';
import { CaseGrid } from '../sections/CaseGrid';
import { TestimonialCarousel } from '../sections/TestimonialCarousel';

export const metadata: Metadata = {
  title: '客户案例 | 工艺优化成果与专家评价',
  description: '了解平台如何帮助半导体企业解决工艺难题与提升良率。',
};

export default function CasesPage() {
  return (
    <>
      <div className="bg-white border-b">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-16 pt-24">
          <h1 className="text-3xl font-bold text-slate-900 sm:text-4xl">客户案例与专家评价</h1>
          <p className="mt-4 text-lg text-slate-600">
            已帮助企业解决 50+ 工艺难题 · 平均良率提升 12% · 覆盖 8 家 Foundry
          </p>
        </div>
      </div>
      <CaseGrid />
      <TestimonialCarousel />
    </>
  );
}
```

- [ ] **Step 6: Commit**

Run:
```bash
cd D:/wang/platform
git add src/components/ui/CaseCard.tsx src/components/ui/TestimonialCard.tsx src/app/sections/CaseGrid.tsx src/app/sections/TestimonialCarousel.tsx src/app/cases/page.tsx
git commit -m "$(cat <<'EOF'
feat: implement Cases page with case studies and testimonials

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

## Task 9: 构建与验证

**Files:**
- Modify: `D:/wang/platform/next.config.js` (已配置静态导出)

- [ ] **Step 1: TypeScript 类型检查**

Run:
```bash
cd D:/wang/platform
npx tsc --noEmit
```
Expected: 无类型错误。

- [ ] **Step 2: 构建静态站点**

Run:
```bash
cd D:/wang/platform
npm run build
```
Expected: `dist/` 目录生成，包含 `index.html`、`features/index.html`、`graph/index.html`、`cases/index.html`。

- [ ] **Step 3: 运行开发服务器验证**

Run:
```bash
cd D:/wang/platform
npm run dev
```
Expected: 访问 `http://localhost:3000` 可正常显示 Landing Page，导航栏链接可跳转各页面，图谱页可交互。

- [ ] **Step 4: Commit**

Run:
```bash
cd D:/wang/platform
git add dist/ .next/ || true
git commit -m "$(cat <<'EOF'
chore: build and verify Phase 1 implementation

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)" || echo "Nothing to commit"
```

---

## 自检清单

### 1. Spec 覆盖检查

| Spec 需求 | 对应 Task | 状态 |
|-----------|-----------|------|
| Next.js 14 App Router + TypeScript | Task 1 | 已覆盖 |
| Tailwind CSS + shadcn/ui | Task 1 | 已覆盖 |
| D3.js v7 力导向图 | Task 7 | 已覆盖 |
| Navbar（滚动变色 + 移动端菜单） | Task 4 | 已覆盖 |
| Footer（四栏链接矩阵） | Task 4 | 已覆盖 |
| Landing Page Hero（双 CTA） | Task 5 | 已覆盖 |
| Landing Page TrustBar（统计 + Logo） | Task 5 | 已覆盖 |
| Landing Page 双受众价值主张 | Task 5 | 已覆盖 |
| 功能特性页（Tab 切换） | Task 6 | 已覆盖 |
| 图谱页（力导向图 + 侧边栏筛选 + 节点详情） | Task 7 | 已覆盖 |
| 案例评价页（案例卡片 + 评价轮播） | Task 8 | 已覆盖 |
| API 路由占位（返回静态 JSON） | Task 3 | 已覆盖 |
| SEO metadata（各页面 title/description） | Task 4/6/8 | 已覆盖 |
| 企业咨询表单对话框 | Task 5 | 已覆盖 |

### 2. Placeholder 扫描

- 无 TBD/TODO/fill in details
- 无 "Add appropriate error handling" 类模糊描述
- 所有步骤包含完整代码
- 无 "Similar to Task N" 引用

### 3. 类型一致性检查

- `GraphNode.type` 使用 `NodeType`，在类型定义、组件 props、侧边栏筛选中一致
- `GraphData` 接口在 API 路由、图谱组件、页面状态中一致
- `NodeDetail` 接收 `GraphNode | null`，与 `KnowledgeGraph` 的 `onNodeClick` 签名匹配

---

## 执行交接

**Plan complete and saved to `docs/superpowers/plans/2026-04-23-semiconductor-kg-platform-phase1.md`. Two execution options:**

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
