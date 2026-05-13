# 半导体知识图谱平台 Phase 2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在现有 Landing Page 基础上，构建 Phase 2 核心功能：用户认证、专家列表、企业需求提交、数据贡献入口、管理后台，使平台成为一个可对外演示的完整 example。

**Architecture:** Next.js 16 App Router + Auth.js v5 (Credentials/JWT) + Prisma ORM + SQLite。前端继续使用 Tailwind CSS + shadcn/ui。管理后台采用 Server Component + Server Actions。

**Tech Stack:** Next.js 16, TypeScript, Tailwind CSS, shadcn/ui, Prisma, SQLite, Auth.js (next-auth@beta), bcryptjs, D3.js

**项目根目录:** `D:/wang/platform/`

---

## 文件结构总览

```
D:/wang/platform/
├── prisma/
│   └── schema.prisma           # 数据库模型定义
├── src/
│   ├── lib/
│   │   ├── utils.ts            # 已有: cn() 工具
│   │   └── prisma.ts           # Prisma Client 单例
│   ├── types/
│   │   ├── graph.ts            # 已有: 图谱类型
│   │   └── next-auth.d.ts      # NextAuth 类型扩展
│   ├── auth.ts                 # Auth.js 配置
│   ├── middleware.ts           # 路由保护中间件
│   ├── app/
│   │   ├── layout.tsx          # 修改: 加入 SessionProvider
│   │   ├── login/
│   │   │   └── page.tsx        # 登录页
│   │   ├── register/
│   │   │   └── page.tsx        # 注册页
│   │   ├── experts/
│   │   │   ├── page.tsx        # 专家列表
│   │   │   └── [id]/
│   │   │       └── page.tsx    # 专家详情
│   │   ├── profile/
│   │   │   └── page.tsx        # 个人中心
│   │   ├── contribute/
│   │   │   └── page.tsx        # 数据贡献
│   │   ├── inquiry/
│   │   │   └── page.tsx        # 企业需求
│   │   ├── admin/
│   │   │   ├── page.tsx        # 管理后台
│   │   │   └── actions.ts      # Server Actions
│   │   └── api/
│   │       ├── auth/[...nextauth]/
│   │       │   └── route.ts    # Auth.js API 路由
│   │       ├── register/
│   │       │   └── route.ts    # 注册 API
│   │       ├── contributions/
│   │       │   └── route.ts    # 数据贡献 API
│   │       ├── inquiries/
│   │       │   └── route.ts    # 企业需求 API
│   │       └── experts/
│   │           ├── route.ts    # 专家列表 API
│   │           └── seed/
│   │               └── route.ts # 种子数据 API
│   ├── components/
│   │   └── layout/
│   │       └── Navbar.tsx      # 修改: 加入登录状态
│   └── data/
│       └── graph-static.json   # 扩展为 80+ 节点
```

---

## Task 1: 数据库初始化（Prisma + SQLite）

**Files:**
- Create: `prisma/schema.prisma`
- Create: `src/lib/prisma.ts`
- Create: `.env.local`
- Modify: `next.config.js`
- Modify: `package.json`（安装依赖）

### Step 1: 安装依赖

Run:
```bash
cd D:/wang/platform
npm install prisma @prisma/client next-auth@beta bcryptjs
npm install -D @types/bcryptjs
```

Expected: `package.json` 中新增 `prisma`、`@prisma/client`、`next-auth`、`bcryptjs`、`@types/bcryptjs`。

### Step 2: 修改 next.config.js（移除静态导出）

由于 Phase 2 引入 API 路由和数据库，必须使用服务器模式。

Modify: `next.config.js`

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    unoptimized: true,
  },
};

module.exports = nextConfig;
```

### Step 3: 定义数据模型

Create: `prisma/schema.prisma`

```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "sqlite"
  url      = env("DATABASE_URL")
}

model User {
  id            String         @id @default(cuid())
  email         String         @unique
  password      String?
  name          String?
  role          String         @default("USER")
  points        Int            @default(0)
  contributions Contribution[]
  expertProfile ExpertProfile?
  createdAt     DateTime       @default(now())
}

model ExpertProfile {
  id           String         @id @default(cuid())
  userId       String         @unique
  user         User           @relation(fields: [userId], references: [id], onDelete: Cascade)
  bio          String?
  specialties  String         @default("[]")
  location     String?
  availability String?
  casesCount   Int            @default(0)
  rating       Float          @default(0)
  earnings     Int            @default(0)
  reviews      ExpertReview[]
  createdAt    DateTime       @default(now())
}

model ExpertReview {
  id           String        @id @default(cuid())
  expertId     String
  expert       ExpertProfile @relation(fields: [expertId], references: [id], onDelete: Cascade)
  reviewerName String
  content      String
  rating       Int
  createdAt    DateTime      @default(now())
}

model Contribution {
  id             String   @id @default(cuid())
  userId         String
  user           User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  processType    String
  equipmentModel String?
  parameters     String?
  yieldRate      String?
  failureRate    String?
  notes          String?
  status         String   @default("PENDING")
  createdAt      DateTime @default(now())
}

model Inquiry {
  id               String   @id @default(cuid())
  companyName      String
  contactName      String
  email            String
  problemDescription String
  budgetRange      String?
  expectedTimeline String?
  status           String   @default("NEW")
  createdAt        DateTime @default(now())
}
```

### Step 4: 创建 Prisma Client 单例

Create: `src/lib/prisma.ts`

```typescript
import { PrismaClient } from "@prisma/client"

const globalForPrisma = global as unknown as { prisma: PrismaClient }

export const prisma = globalForPrisma.prisma || new PrismaClient()

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma
```

### Step 5: 配置环境变量

Create: `.env.local`

```bash
DATABASE_URL="file:./dev.db"
NEXTAUTH_SECRET="semiconductor-kg-platform-secret-key-2026"
NEXTAUTH_URL="http://localhost:3000"
```

### Step 6: 推送数据库 schema 并生成客户端

Run:
```bash
cd D:/wang/platform
npx prisma db push
npx prisma generate
```

Expected: 生成 `prisma/dev.db` 和 `node_modules/.prisma/client/`。

### Step 7: Commit

Run:
```bash
cd D:/wang/platform
git add prisma/ src/lib/prisma.ts .env.local next.config.js package.json package-lock.json
git commit -m "feat: setup Prisma with SQLite and update next.config for SSR"
```

---

## Task 2: 认证系统（Auth.js v5）

**Files:**
- Create: `src/auth.ts`
- Create: `src/types/next-auth.d.ts`
- Create: `src/middleware.ts`
- Create: `src/app/api/auth/[...nextauth]/route.ts`
- Create: `src/app/api/register/route.ts`
- Create: `src/app/login/page.tsx`
- Create: `src/app/register/page.tsx`
- Modify: `src/app/layout.tsx`

### Step 1: Auth.js 配置

Create: `src/auth.ts`

```typescript
import NextAuth from "next-auth"
import Credentials from "next-auth/providers/credentials"
import { prisma } from "@/lib/prisma"
import bcrypt from "bcryptjs"

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [
    Credentials({
      name: "credentials",
      credentials: {
        email: { label: "邮箱", type: "email" },
        password: { label: "密码", type: "password" }
      },
      authorize: async (credentials) => {
        if (!credentials?.email || !credentials?.password) return null

        const user = await prisma.user.findUnique({
          where: { email: credentials.email as string }
        })

        if (!user || !user.password) return null

        const valid = await bcrypt.compare(
          credentials.password as string,
          user.password
        )

        if (!valid) return null

        return {
          id: user.id,
          email: user.email,
          name: user.name,
          role: user.role
        }
      }
    })
  ],
  callbacks: {
    jwt({ token, user }) {
      if (user) {
        token.id = user.id
        token.role = user.role
      }
      return token
    },
    session({ session, token }) {
      session.user.id = token.id as string
      session.user.role = token.role as string
      return session
    }
  },
  pages: {
    signIn: "/login"
  }
})
```

### Step 2: 类型扩展

Create: `src/types/next-auth.d.ts`

```typescript
import "next-auth"

declare module "next-auth" {
  interface Session {
    user: {
      id: string
      role: string
      email?: string | null
      name?: string | null
      image?: string | null
    }
  }
  interface User {
    role: string
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    role: string
    id: string
  }
}
```

### Step 3: API 路由

Create: `src/app/api/auth/[...nextauth]/route.ts`

```typescript
import { handlers } from "@/auth"
export const { GET, POST } = handlers
```

Create: `src/app/api/register/route.ts`

```typescript
import { NextResponse } from "next/server"
import { prisma } from "@/lib/prisma"
import bcrypt from "bcryptjs"

export async function POST(req: Request) {
  try {
    const { email, password, name, role = "USER" } = await req.json()

    const existing = await prisma.user.findUnique({
      where: { email }
    })

    if (existing) {
      return NextResponse.json(
        { error: "该邮箱已注册" },
        { status: 400 }
      )
    }

    const hashed = await bcrypt.hash(password, 10)
    const user = await prisma.user.create({
      data: { email, password: hashed, name, role }
    })

    return NextResponse.json({
      id: user.id,
      email: user.email,
      name: user.name
    })
  } catch {
    return NextResponse.json(
      { error: "注册失败" },
      { status: 500 }
    )
  }
}
```

### Step 4: 登录页

Create: `src/app/login/page.tsx`

```typescript
"use client"

import { useState } from "react"
import { signIn } from "next-auth/react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export default function LoginPage() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")

    const result = await signIn("credentials", {
      email,
      password,
      redirect: false
    })

    if (result?.error) {
      setError("邮箱或密码错误")
    } else {
      router.push("/")
      router.refresh()
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 px-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle className="text-2xl text-center">登录</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="p-3 text-sm text-red-600 bg-red-50 rounded-md">
                {error}
              </div>
            )}
            <div>
              <label className="block text-sm font-medium text-slate-700">邮箱</label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700">密码</label>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              />
            </div>
            <Button type="submit" className="w-full">登录</Button>
            <p className="text-center text-sm text-slate-600">
              还没有账号？{" "}
              <Link href="/register" className="text-blue-600 hover:underline">立即注册</Link>
            </p>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
```

### Step 5: 注册页

Create: `src/app/register/page.tsx`

```typescript
"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export default function RegisterPage() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [name, setName] = useState("")
  const [role, setRole] = useState("USER")
  const [error, setError] = useState("")
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")

    try {
      const res = await fetch("/api/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password, name, role })
      })

      if (!res.ok) {
        const data = await res.json()
        setError(data.error || "注册失败")
        return
      }

      router.push("/login")
    } catch {
      setError("注册失败，请重试")
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 px-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle className="text-2xl text-center">注册</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="p-3 text-sm text-red-600 bg-red-50 rounded-md">{error}</div>
            )}
            <div>
              <label className="block text-sm font-medium text-slate-700">姓名</label>
              <input
                type="text"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700">邮箱</label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700">密码</label>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700">注册身份</label>
              <select
                value={role}
                onChange={(e) => setRole(e.target.value)}
                className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              >
                <option value="USER">普通用户</option>
                <option value="EXPERT">专家/工程师</option>
              </select>
            </div>
            <Button type="submit" className="w-full">注册</Button>
            <p className="text-center text-sm text-slate-600">
              已有账号？{" "}
              <Link href="/login" className="text-blue-600 hover:underline">立即登录</Link>
            </p>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
```

### Step 6: 中间件（保护管理后台）

Create: `src/middleware.ts`

```typescript
import { auth } from "@/auth"

export default auth((req) => {
  const { nextUrl } = req
  const isLoggedIn = !!req.auth
  const isAdmin = req.auth?.user?.role === "ADMIN"
  const isAdminPage = nextUrl.pathname.startsWith("/admin")

  if (isAdminPage && !isAdmin) {
    return Response.redirect(new URL("/", nextUrl))
  }

  if (!isLoggedIn && nextUrl.pathname === "/profile") {
    return Response.redirect(new URL("/login", nextUrl))
  }
})

export const config = {
  matcher: ["/admin/:path*", "/profile/:path*"]
}
```

### Step 7: 修改根布局

Modify: `src/app/layout.tsx`

```typescript
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import { SessionProvider } from "next-auth/react"
import "./globals.css"
import { Navbar } from "@/components/layout/Navbar"
import { Footer } from "@/components/layout/Footer"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "半导体知识图谱平台 | 薄膜沉积工艺专家社区",
  description: "半导体薄膜沉积领域首个知识图谱平台，连接工艺工程师与企业客户",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="zh-CN">
      <body className={inter.className}>
        <SessionProvider>
          <Navbar />
          <main className="min-h-screen">{children}</main>
          <Footer />
        </SessionProvider>
      </body>
    </html>
  )
}
```

### Step 8: Commit

Run:
```bash
cd D:/wang/platform
git add src/auth.ts src/types/next-auth.d.ts src/middleware.ts src/app/api/auth/ src/app/api/register/ src/app/login/ src/app/register/ src/app/layout.tsx
git commit -m "feat: add Auth.js authentication with login and register pages"
```

---

## Task 3: 专家列表与详情页

**Files:**
- Create: `src/app/api/experts/route.ts`
- Create: `src/app/api/experts/seed/route.ts`
- Create: `src/app/experts/page.tsx`
- Create: `src/app/experts/[id]/page.tsx`

### Step 1: 专家数据 API

Create: `src/app/api/experts/route.ts`

```typescript
import { NextResponse } from "next/server"
import { prisma } from "@/lib/prisma"

export async function GET() {
  const experts = await prisma.expertProfile.findMany({
    include: {
      user: { select: { name: true, email: true } },
      reviews: true
    }
  })
  return NextResponse.json(experts)
}
```

Create: `src/app/api/experts/seed/route.ts`

```typescript
import { NextResponse } from "next/server"
import { prisma } from "@/lib/prisma"
import bcrypt from "bcryptjs"

export async function POST() {
  const count = await prisma.expertProfile.count()
  if (count > 0) {
    return NextResponse.json({ message: "已有专家数据，跳过种子" })
  }

  const experts = [
    {
      email: "expert1@example.com",
      name: "张明华",
      password: await bcrypt.hash("demo123", 10),
      role: "EXPERT",
      profile: {
        bio: "前应用材料（AMAT）资深工艺工程师，15年薄膜沉积经验，专注CVD/PECVD工艺优化与良率提升。",
        specialties: JSON.stringify(["CVD", "PECVD", "良率优化"]),
        location: "上海",
        availability: "周末及工作日晚上",
        casesCount: 12,
        rating: 4.9,
        earnings: 85000
      }
    },
    {
      email: "expert2@example.com",
      name: "李建国",
      password: await bcrypt.hash("demo123", 10),
      role: "EXPERT",
      profile: {
        bio: "泛林集团（LAM）前应用工程师，精通Vector系列CVD设备调试与故障诊断。",
        specialties: JSON.stringify(["LAM Vector", "CVD", "设备调试"]),
        location: "北京",
        availability: "可出差",
        casesCount: 8,
        rating: 4.7,
        earnings: 62000
      }
    },
    {
      email: "expert3@example.com",
      name: "王淑芬",
      password: await bcrypt.hash("demo123", 10),
      role: "EXPERT",
      profile: {
        bio: "东京电子（TEL）前工艺整合工程师，擅长ALD工艺开发与3D NAND字线钨填充。",
        specialties: JSON.stringify(["ALD", "TEL", "3D NAND"]),
        location: "无锡",
        availability: "预约制",
        casesCount: 15,
        rating: 4.8,
        earnings: 120000
      }
    }
  ]

  for (const expert of experts) {
    const { profile, ...userData } = expert
    await prisma.user.create({
      data: {
        ...userData,
        expertProfile: { create: profile }
      }
    })
  }

  return NextResponse.json({ message: "已创建 3 位种子专家" })
}
```

### Step 2: 专家列表页

Create: `src/app/experts/page.tsx`

```typescript
import Link from "next/link"
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import { Star, MapPin, Briefcase } from "lucide-react"
import { SectionTitle } from "@/components/ui/SectionTitle"

async function getExperts() {
  const res = await fetch(`${process.env.NEXTAUTH_URL || "http://localhost:3000"}/api/experts`, {
    next: { revalidate: 60 }
  })
  if (!res.ok) return []
  return res.json()
}

export default async function ExpertsPage() {
  const experts = await getExperts()

  return (
    <div className="pt-24 pb-20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <SectionTitle
          title="认证专家"
          subtitle="平台认证的半导体工艺专家，覆盖薄膜沉积、设备调试、良率优化等领域"
        />

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {experts.map((expert: any) => (
            <Link key={expert.id} href={`/experts/${expert.id}`}>
              <Card className="h-full hover:shadow-md transition-shadow cursor-pointer">
                <CardHeader>
                  <div className="flex items-center gap-4">
                    <div className="w-16 h-16 rounded-full bg-blue-100 flex items-center justify-center text-xl font-bold text-blue-600">
                      {expert.user.name?.[0] || "专"}
                    </div>
                    <div>
                      <h3 className="text-lg font-bold text-slate-900">{expert.user.name}</h3>
                      <div className="flex items-center gap-1 text-amber-500">
                        <Star className="h-4 w-4 fill-current" />
                        <span className="text-sm font-medium">{expert.rating}</span>
                      </div>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-3">
                  <p className="text-sm text-slate-600 line-clamp-3">{expert.bio}</p>
                  <div className="flex flex-wrap gap-2">
                    {JSON.parse(expert.specialties).map((s: string) => (
                      <span key={s} className="px-2 py-1 bg-blue-50 text-blue-700 text-xs rounded-full">{s}</span>
                    ))}
                  </div>
                  <div className="flex items-center gap-4 text-sm text-slate-500 pt-2">
                    <span className="flex items-center gap-1"><MapPin className="h-4 w-4" />{expert.location}</span>
                    <span className="flex items-center gap-1"><Briefcase className="h-4 w-4" />{expert.casesCount} 个案例</span>
                  </div>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>

        {experts.length === 0 && (
          <div className="text-center py-20 text-slate-500">
            暂无专家数据，请先运行种子接口初始化数据
          </div>
        )}
      </div>
    </div>
  )
}
```

### Step 3: 专家详情页

Create: `src/app/experts/[id]/page.tsx`

```typescript
import Link from "next/link"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Star, MapPin, Briefcase, Clock, ArrowLeft, TrendingUp } from "lucide-react"

async function getExpert(id: string) {
  const res = await fetch(`${process.env.NEXTAUTH_URL || "http://localhost:3000"}/api/experts`, {
    next: { revalidate: 60 }
  })
  if (!res.ok) return null
  const experts = await res.json()
  return experts.find((e: any) => e.id === id)
}

export default async function ExpertDetailPage({ params }: { params: { id: string } }) {
  const expert = await getExpert(params.id)

  if (!expert) {
    return (
      <div className="pt-24 text-center">
        <p className="text-slate-500">专家不存在</p>
        <Link href="/experts" className="text-blue-600 hover:underline">返回专家列表</Link>
      </div>
    )
  }

  return (
    <div className="pt-24 pb-20">
      <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
        <Link href="/experts" className="inline-flex items-center text-sm text-slate-600 hover:text-slate-900 mb-6">
          <ArrowLeft className="h-4 w-4 mr-1" />返回专家列表
        </Link>

        <Card>
          <CardHeader>
            <div className="flex items-start justify-between flex-wrap gap-4">
              <div className="flex items-center gap-6">
                <div className="w-24 h-24 rounded-full bg-blue-100 flex items-center justify-center text-3xl font-bold text-blue-600">
                  {expert.user.name?.[0] || "专"}
                </div>
                <div>
                  <h1 className="text-2xl font-bold text-slate-900">{expert.user.name}</h1>
                  <div className="flex items-center gap-1 text-amber-500 mt-1">
                    <Star className="h-5 w-5 fill-current" />
                    <span className="text-lg font-medium">{expert.rating}</span>
                    <span className="text-slate-400 text-sm ml-1">({expert.reviews.length} 条评价)</span>
                  </div>
                </div>
              </div>
              <Button>预约咨询</Button>
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            <div>
              <h3 className="font-semibold text-slate-900 mb-2">专家简介</h3>
              <p className="text-slate-600">{expert.bio}</p>
            </div>

            <div className="grid sm:grid-cols-3 gap-4">
              <div className="flex items-center gap-2 text-slate-600"><MapPin className="h-5 w-5 text-slate-400" /><span>{expert.location}</span></div>
              <div className="flex items-center gap-2 text-slate-600"><Clock className="h-5 w-5 text-slate-400" /><span>{expert.availability}</span></div>
              <div className="flex items-center gap-2 text-slate-600"><Briefcase className="h-5 w-5 text-slate-400" /><span>{expert.casesCount} 个服务案例</span></div>
            </div>

            <div className="grid sm:grid-cols-2 gap-4">
              <Card className="bg-green-50 border-green-100">
                <CardContent className="pt-4">
                  <div className="flex items-center gap-2 text-green-700 mb-1">
                    <TrendingUp className="h-5 w-5" />
                    <span className="font-medium">平台收益</span>
                  </div>
                  <p className="text-2xl font-bold text-green-800">¥{expert.earnings.toLocaleString()}</p>
                </CardContent>
              </Card>
            </div>

            <div>
              <h3 className="font-semibold text-slate-900 mb-2">擅长领域</h3>
              <div className="flex flex-wrap gap-2">
                {JSON.parse(expert.specialties).map((s: string) => (
                  <span key={s} className="px-3 py-1 bg-blue-50 text-blue-700 text-sm rounded-full">{s}</span>
                ))}
              </div>
            </div>

            {expert.reviews.length > 0 && (
              <div>
                <h3 className="font-semibold text-slate-900 mb-3">客户评价</h3>
                <div className="space-y-3">
                  {expert.reviews.map((review: any) => (
                    <Card key={review.id}>
                      <CardContent className="pt-4">
                        <div className="flex items-center justify-between mb-2">
                          <span className="font-medium text-slate-900">{review.reviewerName}</span>
                          <div className="flex text-amber-500">
                            {Array.from({ length: 5 }).map((_, i) => (
                              <Star key={i} className={`h-4 w-4 ${i < review.rating ? "fill-current" : "text-slate-200"}`} />
                            ))}
                          </div>
                        </div>
                        <p className="text-sm text-slate-600">{review.content}</p>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
```

### Step 4: Commit

Run:
```bash
cd D:/wang/platform
git add src/app/api/experts/ src/app/experts/
git commit -m "feat: add expert list and detail pages with seed API"
```

---

## Task 4: 企业需求提交系统

**Files:**
- Create: `src/app/api/inquiries/route.ts`
- Create: `src/app/inquiry/page.tsx`

### Step 1: 企业需求 API

Create: `src/app/api/inquiries/route.ts`

```typescript
import { NextResponse } from "next/server"
import { prisma } from "@/lib/prisma"

export async function GET() {
  const inquiries = await prisma.inquiry.findMany({
    orderBy: { createdAt: "desc" }
  })
  return NextResponse.json(inquiries)
}

export async function POST(req: Request) {
  try {
    const body = await req.json()
    const inquiry = await prisma.inquiry.create({
      data: {
        companyName: body.companyName,
        contactName: body.contactName,
        email: body.email,
        problemDescription: body.problemDescription,
        budgetRange: body.budgetRange,
        expectedTimeline: body.expectedTimeline
      }
    })
    return NextResponse.json(inquiry, { status: 201 })
  } catch {
    return NextResponse.json({ error: "提交失败" }, { status: 500 })
  }
}
```

### Step 2: 需求提交页

Create: `src/app/inquiry/page.tsx`

```typescript
"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { SectionTitle } from "@/components/ui/SectionTitle"

export default function InquiryPage() {
  const [submitted, setSubmitted] = useState(false)
  const [formData, setFormData] = useState({
    companyName: "", contactName: "", email: "",
    problemDescription: "", budgetRange: "", expectedTimeline: ""
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const res = await fetch("/api/inquiries", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      })
      if (res.ok) setSubmitted(true)
    } catch {
      alert("提交失败，请重试")
    }
  }

  if (submitted) {
    return (
      <div className="pt-24 pb-20">
        <div className="mx-auto max-w-2xl px-4 text-center">
          <div className="p-8 bg-green-50 rounded-2xl">
            <h2 className="text-2xl font-bold text-green-800 mb-2">提交成功</h2>
            <p className="text-green-700">我们的专家将在 24 小时内与您联系。</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="pt-24 pb-20">
      <div className="mx-auto max-w-2xl px-4 sm:px-6 lg:px-8">
        <SectionTitle title="提交工艺需求" subtitle="描述您的工艺难题，我们将为您匹配最合适的专家" />

        <Card>
          <CardHeader><CardTitle>企业咨询表单</CardTitle></CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700">公司名称 *</label>
                  <input required value={formData.companyName}
                    onChange={(e) => setFormData({ ...formData, companyName: e.target.value })}
                    className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700">联系人 *</label>
                  <input required value={formData.contactName}
                    onChange={(e) => setFormData({ ...formData, contactName: e.target.value })}
                    className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500" />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700">联系邮箱 *</label>
                <input type="email" required value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500" />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700">工艺问题描述 *</label>
                <textarea required rows={4} value={formData.problemDescription}
                  onChange={(e) => setFormData({ ...formData, problemDescription: e.target.value })}
                  placeholder="请描述您遇到的工艺问题..."
                  className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500" />
              </div>

              <div className="grid sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700">预算范围</label>
                  <select value={formData.budgetRange}
                    onChange={(e) => setFormData({ ...formData, budgetRange: e.target.value })}
                    className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500">
                    <option value="">请选择</option>
                    <option value="1-5万">1-5 万</option>
                    <option value="5-10万">5-10 万</option>
                    <option value="10-30万">10-30 万</option>
                    <option value="30万以上">30 万以上</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700">期望时间</label>
                  <select value={formData.expectedTimeline}
                    onChange={(e) => setFormData({ ...formData, expectedTimeline: e.target.value })}
                    className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500">
                    <option value="">请选择</option>
                    <option value="1周内">1 周内</option>
                    <option value="1-2周">1-2 周</option>
                    <option value="1个月内">1 个月内</option>
                    <option value="3个月内">3 个月内</option>
                  </select>
                </div>
              </div>

              <Button type="submit" className="w-full">提交需求</Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
```

### Step 3: Commit

Run:
```bash
cd D:/wang/platform
git add src/app/api/inquiries/ src/app/inquiry/
git commit -m "feat: add enterprise inquiry submission system"
```

---

## Task 5: 数据贡献入口

**Files:**
- Create: `src/app/api/contributions/route.ts`
- Create: `src/app/contribute/page.tsx`

### Step 1: 数据贡献 API

Create: `src/app/api/contributions/route.ts`

```typescript
import { NextResponse } from "next/server"
import { prisma } from "@/lib/prisma"
import { auth } from "@/auth"

export async function GET() {
  const contributions = await prisma.contribution.findMany({
    where: { status: "APPROVED" },
    include: { user: { select: { name: true } } },
    orderBy: { createdAt: "desc" }
  })
  return NextResponse.json(contributions)
}

export async function POST(req: Request) {
  const session = await auth()
  if (!session?.user?.id) {
    return NextResponse.json({ error: "请先登录" }, { status: 401 })
  }

  try {
    const body = await req.json()
    const contribution = await prisma.contribution.create({
      data: {
        userId: session.user.id,
        processType: body.processType,
        equipmentModel: body.equipmentModel,
        parameters: body.parameters,
        yieldRate: body.yieldRate,
        failureRate: body.failureRate,
        notes: body.notes
      }
    })
    return NextResponse.json(contribution, { status: 201 })
  } catch {
    return NextResponse.json({ error: "提交失败" }, { status: 500 })
  }
}
```

### Step 2: 贡献提交页

Create: `src/app/contribute/page.tsx`

```typescript
"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { SectionTitle } from "@/components/ui/SectionTitle"

export default function ContributePage() {
  const [submitted, setSubmitted] = useState(false)
  const [formData, setFormData] = useState({
    processType: "", equipmentModel: "", parameters: "",
    yieldRate: "", failureRate: "", notes: ""
  })
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const res = await fetch("/api/contributions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      })

      if (res.status === 401) {
        router.push("/login")
        return
      }

      if (res.ok) setSubmitted(true)
    } catch {
      alert("提交失败，请重试")
    }
  }

  if (submitted) {
    return (
      <div className="pt-24 pb-20">
        <div className="mx-auto max-w-2xl px-4 text-center">
          <div className="p-8 bg-green-50 rounded-2xl">
            <h2 className="text-2xl font-bold text-green-800 mb-2">提交成功</h2>
            <p className="text-green-700">感谢您的贡献！我们的审核团队将在 3 个工作日内完成审核。</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="pt-24 pb-20">
      <div className="mx-auto max-w-2xl px-4 sm:px-6 lg:px-8">
        <SectionTitle title="贡献工艺数据" subtitle="分享您的工艺经验，帮助行业共同进步，同时获得积分奖励" />

        <Card>
          <CardHeader><CardTitle>数据提交表单</CardTitle></CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700">工艺类型 *</label>
                <select required value={formData.processType}
                  onChange={(e) => setFormData({ ...formData, processType: e.target.value })}
                  className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500">
                  <option value="">请选择</option>
                  <option value="CVD">CVD</option>
                  <option value="PVD">PVD</option>
                  <option value="ALD">ALD</option>
                  <option value="PECVD">PECVD</option>
                  <option value="LPCVD">LPCVD</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700">设备型号</label>
                <input value={formData.equipmentModel}
                  onChange={(e) => setFormData({ ...formData, equipmentModel: e.target.value })}
                  placeholder="如：AMAT Endura 5500"
                  className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500" />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700">关键工艺参数</label>
                <textarea rows={3} value={formData.parameters}
                  onChange={(e) => setFormData({ ...formData, parameters: e.target.value })}
                  placeholder="如：温度 450°C，压力 2 Torr，气体流量 SiH4 200sccm..."
                  className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500" />
              </div>

              <div className="grid sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700">良率 (%)</label>
                  <input type="number" min="0" max="100" value={formData.yieldRate}
                    onChange={(e) => setFormData({ ...formData, yieldRate: e.target.value })}
                    className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700">失效率 (%)</label>
                  <input type="number" min="0" max="100" value={formData.failureRate}
                    onChange={(e) => setFormData({ ...formData, failureRate: e.target.value })}
                    className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500" />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700">备注说明</label>
                <textarea rows={3} value={formData.notes}
                  onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                  placeholder="其他补充信息，如适用晶圆尺寸、特殊注意事项等"
                  className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500" />
              </div>

              <Button type="submit" className="w-full">提交贡献</Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
```

### Step 3: Commit

Run:
```bash
cd D:/wang/platform
git add src/app/api/contributions/ src/app/contribute/
git commit -m "feat: add data contribution submission system"
```

---

## Task 6: 管理后台（Admin Dashboard）

**Files:**
- Create: `src/app/admin/page.tsx`
- Create: `src/app/admin/actions.ts`

### Step 1: Server Actions

Create: `src/app/admin/actions.ts`

```typescript
"use server"

import { prisma } from "@/lib/prisma"
import { revalidatePath } from "next/cache"

export async function approveContribution(id: string) {
  await prisma.contribution.update({
    where: { id },
    data: { status: "APPROVED" }
  })
  revalidatePath("/admin")
}

export async function rejectContribution(id: string) {
  await prisma.contribution.update({
    where: { id },
    data: { status: "REJECTED" }
  })
  revalidatePath("/admin")
}

export async function updateInquiryStatus(id: string, status: string) {
  await prisma.inquiry.update({
    where: { id },
    data: { status }
  })
  revalidatePath("/admin")
}
```

### Step 2: 管理后台页面

Create: `src/app/admin/page.tsx`

```typescript
import { prisma } from "@/lib/prisma"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { approveContribution, rejectContribution, updateInquiryStatus } from "./actions"

export default async function AdminPage() {
  const pendingContributions = await prisma.contribution.findMany({
    where: { status: "PENDING" },
    include: { user: { select: { name: true, email: true } } },
    orderBy: { createdAt: "desc" }
  })

  const inquiries = await prisma.inquiry.findMany({
    orderBy: { createdAt: "desc" }
  })

  return (
    <div className="pt-24 pb-20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-slate-900 mb-8">管理后台</h1>

        <div className="grid lg:grid-cols-2 gap-8">
          <div>
            <h2 className="text-xl font-semibold text-slate-900 mb-4">待审核贡献 ({pendingContributions.length})</h2>
            <div className="space-y-4">
              {pendingContributions.map((c) => (
                <Card key={c.id}>
                  <CardContent className="pt-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-medium text-slate-900">{c.user.name}</span>
                      <span className="text-xs text-slate-500">{c.processType}</span>
                    </div>
                    <p className="text-sm text-slate-600 mb-1">设备: {c.equipmentModel || "未填写"}</p>
                    <p className="text-sm text-slate-600 mb-3">参数: {c.parameters || "未填写"}</p>
                    <div className="flex gap-2">
                      <form action={async () => { "use server"; await approveContribution(c.id) }}>
                        <Button type="submit" size="sm" variant="outline" className="text-green-600 border-green-200 hover:bg-green-50">通过</Button>
                      </form>
                      <form action={async () => { "use server"; await rejectContribution(c.id) }}>
                        <Button type="submit" size="sm" variant="outline" className="text-red-600 border-red-200 hover:bg-red-50">拒绝</Button>
                      </form>
                    </div>
                  </CardContent>
                </Card>
              ))}
              {pendingContributions.length === 0 && (
                <p className="text-slate-500 text-center py-8">暂无待审核贡献</p>
              )}
            </div>
          </div>

          <div>
            <h2 className="text-xl font-semibold text-slate-900 mb-4">企业需求 ({inquiries.length})</h2>
            <div className="space-y-4">
              {inquiries.map((i) => (
                <Card key={i.id}>
                  <CardContent className="pt-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-medium text-slate-900">{i.companyName}</span>
                      <span className={`text-xs px-2 py-1 rounded-full ${
                        i.status === "NEW" ? "bg-blue-50 text-blue-700" :
                        i.status === "CONTACTED" ? "bg-amber-50 text-amber-700" :
                        "bg-green-50 text-green-700"
                      }`}>{i.status}</span>
                    </div>
                    <p className="text-sm text-slate-600 mb-1">联系人: {i.contactName} ({i.email})</p>
                    <p className="text-sm text-slate-600 mb-3">{i.problemDescription.slice(0, 100)}...</p>
                    <div className="flex gap-2">
                      {i.status === "NEW" && (
                        <form action={async () => { "use server"; await updateInquiryStatus(i.id, "CONTACTED") }}>
                          <Button type="submit" size="sm" variant="outline">标记已联系</Button>
                        </form>
                      )}
                      {i.status !== "RESOLVED" && (
                        <form action={async () => { "use server"; await updateInquiryStatus(i.id, "RESOLVED") }}>
                          <Button type="submit" size="sm" variant="outline" className="text-green-600 border-green-200 hover:bg-green-50">标记已解决</Button>
                        </form>
                      )}
                    </div>
                  </CardContent>
                </Card>
              ))}
              {inquiries.length === 0 && (
                <p className="text-slate-500 text-center py-8">暂无企业需求</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
```

### Step 3: Commit

Run:
```bash
cd D:/wang/platform
git add src/app/admin/
git commit -m "feat: add admin dashboard with Server Actions for contribution approval and inquiry management"
```

---

## Task 7: 个人中心（Profile）

**Files:**
- Create: `src/app/profile/page.tsx`

### Step 1: 个人中心页面

Create: `src/app/profile/page.tsx`

```typescript
import { auth } from "@/auth"
import { prisma } from "@/lib/prisma"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { redirect } from "next/navigation"

export default async function ProfilePage() {
  const session = await auth()
  if (!session?.user?.id) redirect("/login")

  const user = await prisma.user.findUnique({
    where: { id: session.user.id },
    include: {
      contributions: { orderBy: { createdAt: "desc" } },
      expertProfile: true
    }
  })

  if (!user) redirect("/login")

  const approvedCount = user.contributions.filter((c) => c.status === "APPROVED").length
  const pendingCount = user.contributions.filter((c) => c.status === "PENDING").length

  return (
    <div className="pt-24 pb-20">
      <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-slate-900 mb-8">个人中心</h1>

        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <Card className="bg-blue-50 border-blue-100">
            <CardContent className="pt-4">
              <p className="text-sm text-blue-600 font-medium">积分</p>
              <p className="text-3xl font-bold text-blue-800">{user.points}</p>
            </CardContent>
          </Card>
          <Card className="bg-green-50 border-green-100">
            <CardContent className="pt-4">
              <p className="text-sm text-green-600 font-medium">已通过贡献</p>
              <p className="text-3xl font-bold text-green-800">{approvedCount}</p>
            </CardContent>
          </Card>
          <Card className="bg-amber-50 border-amber-100">
            <CardContent className="pt-4">
              <p className="text-sm text-amber-600 font-medium">审核中</p>
              <p className="text-3xl font-bold text-amber-800">{pendingCount}</p>
            </CardContent>
          </Card>
        </div>

        {user.role === "EXPERT" && user.expertProfile && (
          <Card className="mb-8">
            <CardHeader>
              <CardTitle>专家档案</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <p className="text-slate-600">{user.expertProfile.bio}</p>
              <div className="flex flex-wrap gap-2">
                {JSON.parse(user.expertProfile.specialties).map((s: string) => (
                  <span key={s} className="px-2 py-1 bg-blue-50 text-blue-700 text-xs rounded-full">{s}</span>
                ))}
              </div>
              <p className="text-sm text-slate-500">收益: ¥{user.expertProfile.earnings.toLocaleString()}</p>
            </CardContent>
          </Card>
        )}

        <h2 className="text-xl font-semibold text-slate-900 mb-4">我的贡献记录</h2>
        <div className="space-y-3">
          {user.contributions.map((c) => (
            <Card key={c.id}>
              <CardContent className="pt-4">
                <div className="flex items-center justify-between">
                  <span className="font-medium text-slate-900">{c.processType} - {c.equipmentModel || "未填写设备"}</span>
                  <span className={`text-xs px-2 py-1 rounded-full ${
                    c.status === "APPROVED" ? "bg-green-50 text-green-700" :
                    c.status === "PENDING" ? "bg-amber-50 text-amber-700" :
                    "bg-red-50 text-red-700"
                  }`}>
                    {c.status === "APPROVED" ? "已通过" : c.status === "PENDING" ? "审核中" : "已拒绝"}
                  </span>
                </div>
                <p className="text-sm text-slate-500 mt-1">{new Date(c.createdAt).toLocaleDateString("zh-CN")}</p>
              </CardContent>
            </Card>
          ))}
          {user.contributions.length === 0 && (
            <p className="text-slate-500 text-center py-8">暂无贡献记录</p>
          )}
        </div>
      </div>
    </div>
  )
}
```

### Step 2: Commit

Run:
```bash
cd D:/wang/platform
git add src/app/profile/
git commit -m "feat: add profile page with points, contributions, and expert profile"
```

---

## Task 8: 导航栏认证状态

**Files:**
- Modify: `src/components/layout/Navbar.tsx`

### Step 1: 修改导航栏

Modify: `src/components/layout/Navbar.tsx`

读取现有 Navbar 代码，然后添加：
1. 使用 `useSession()` 获取登录状态
2. 已登录显示用户名称下拉菜单（个人中心 / 管理后台 / 登出）
3. 未登录显示登录/注册按钮
4. 登出调用 `signOut()`

关键代码片段：

```typescript
"use client"

import { useSession, signOut } from "next-auth/react"
import Link from "next/link"
import { useState } from "react"
import { Button } from "@/components/ui/button"

export function Navbar() {
  const { data: session, status } = useSession()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [userMenuOpen, setUserMenuOpen] = useState(false)

  const isAdmin = session?.user?.role === "ADMIN"

  return (
    // ... existing navbar structure ...
    // In the right side of navbar, replace static buttons with:
    
    {status === "loading" ? (
      <div className="h-8 w-20 bg-slate-200 animate-pulse rounded" />
    ) : session?.user ? (
      <div className="relative">
        <button
          onClick={() => setUserMenuOpen(!userMenuOpen)}
          className="flex items-center gap-2 text-sm font-medium text-slate-700 hover:text-slate-900"
        >
          <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold">
            {session.user.name?.[0] || "U"}
          </div>
          <span>{session.user.name}</span>
        </button>
        {userMenuOpen && (
          <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-slate-100 py-1 z-50">
            <Link href="/profile" className="block px-4 py-2 text-sm text-slate-700 hover:bg-slate-50">个人中心</Link>
            {isAdmin && (
              <Link href="/admin" className="block px-4 py-2 text-sm text-slate-700 hover:bg-slate-50">管理后台</Link>
            )}
            <button
              onClick={() => signOut({ callbackUrl: "/" })}
              className="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50"
            >
              退出登录
            </button>
          </div>
        )}
      </div>
    ) : (
      <div className="flex items-center gap-3">
        <Link href="/login" className="text-sm font-medium text-slate-600 hover:text-slate-900">登录</Link>
        <Link href="/register">
          <Button size="sm">注册</Button>
        </Link>
      </div>
    )}
  )
}
```

### Step 2: Commit

Run:
```bash
cd D:/wang/platform
git add src/components/layout/Navbar.tsx
git commit -m "feat: update Navbar with auth state, user dropdown, and admin link"
```

---

## Task 9: 图谱数据扩展（80-120 节点）

**Files:**
- Modify: `src/data/graph-static.json`

### Step 1: 扩展图谱数据

将现有约 28 个节点的数据扩展至 80-120 个节点，覆盖更多工艺、设备、材料、参数和常见问题。

需要新增的领域：
- **工艺**: SACVD, HDPCVD, MOCVD, 溅射 PVD, 蒸发 PVD, 离子束沉积
- **设备**: TEL Certas, LAM Altus, AMAT Producer, Veeco 离子束
- **材料**: TiN, TaN, Co, Ru, Mo, W 填充, 低 k 介质, high-k 介质
- **参数**: RF 功率, 偏压, 温度梯度, 气体比例, 沉积速率
- **问题**: 颗粒缺陷, 台阶覆盖不足, 应力开裂, 附着力差, 电阻率异常

数据格式保持与现有 `GraphData` 类型一致：
```typescript
interface GraphNode {
  id: string;
  label: string;
  type: "process" | "equipment" | "material" | "parameter" | "issue";
}

interface GraphLink {
  source: string;
  target: string;
  label?: string;
}
```

### Step 2: Commit

Run:
```bash
cd D:/wang/platform
git add src/data/graph-static.json
git commit -m "feat: expand knowledge graph from 28 to ~100 nodes covering more processes and materials"
```

---

## Task 10: 构建配置与部署

**Files:**
- Modify: `package.json`（scripts）
- Create: `.env.production`（模板）
- Modify: `next.config.js`

### Step 1: 更新构建脚本

Modify: `package.json` scripts section

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "prisma generate && next build",
    "start": "next start",
    "lint": "next lint",
    "db:push": "prisma db push",
    "db:studio": "prisma studio",
    "seed": "curl -X POST http://localhost:3000/api/experts/seed"
  }
}
```

### Step 2: 生产环境变量模板

Create: `.env.production` (or `.env.example`)

```bash
# 复制为 .env.local 后填写实际值
DATABASE_URL="file:./dev.db"
NEXTAUTH_SECRET="your-production-secret-key-min-32-chars"
NEXTAUTH_URL="https://your-domain.com"
```

### Step 3: 最终 next.config.js

Modify: `next.config.js`

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    unoptimized: true,
  },
  experimental: {
    // Next.js 16 默认已包含 App Router
  }
}

module.exports = nextConfig
```

### Step 4: 部署前检查清单

1. 运行 `npm run build` 验证构建成功
2. 确保 `prisma/dev.db` 已创建（首次部署需运行 `npx prisma db push`）
3. 设置强密码的 `NEXTAUTH_SECRET`
4. 生产环境建议使用 PostgreSQL 替代 SQLite（修改 `schema.prisma` 中 `datasource db` 的 `provider`）
5. 如需部署到 Vercel：
   - 在 Vercel Dashboard 添加环境变量
   - 将 `build` 脚本设为 `prisma generate && next build`
   - 数据库建议使用 Vercel Postgres 或 Neon

### Step 5: Commit

Run:
```bash
cd D:/wang/platform
git add package.json .env.production next.config.js
git commit -m "chore: add build scripts, production env template, and deployment docs"
```

---

## 执行建议

### 方式 A：Subagent 并行执行（推荐）

使用 `superpowers:subagent-driven-development` 技能，按任务列表逐任务执行。每个 Task 可独立提交，便于回滚。

### 方式 B：顺序单线程执行

在当前会话中逐个执行 Task 1-10，适合需要频繁调整的场景。

### 验证清单（全部完成后）

- [ ] 可以注册新用户（USER 和 EXPERT 角色）
- [ ] 可以登录/登出
- [ ] 未登录用户访问 `/contribute` 会跳转登录
- [ ] 非管理员访问 `/admin` 会跳转首页
- [ ] 专家列表页展示 3 位种子专家
- [ ] 专家详情页展示简介、评价、收益
- [ ] 企业需求表单可以提交并在管理后台查看
- [ ] 数据贡献表单提交后出现在管理后台待审核列表
- [ ] 管理员可以通过/拒绝贡献
- [ ] 管理员可以标记企业需求状态
- [ ] 个人中心显示积分和贡献记录
- [ ] 导航栏根据登录状态变化
- [ ] 知识图谱展示 80+ 节点且可交互

---

*Plan written: 2026-05-08*
*Scope: Phase 2 core features for demo-ready semiconductor KG platform*
