-- 用户表
create table users (
  id uuid primary key default gen_random_uuid(),
  email text unique not null,
  name text,
  plan text default 'free',
  created_at timestamp default now()
);

-- 项目表（每次任务）
create table projects (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references users(id) on delete cascade,
  title text,
  product_desc text,
  goal text,
  platform text,
  created_at timestamp default now()
);

-- Agent 执行任务链
create table tasks (
  id uuid primary key default gen_random_uuid(),
  project_id uuid references projects(id) on delete cascade,
  agent_type text, -- e.g. 'planner', 'copywriter', 'imagegen'
  input_data jsonb,
  output_data jsonb,
  status text default 'pending',
  executed_at timestamp
);

-- 输出内容记录
create table outputs (
  id uuid primary key default gen_random_uuid(),
  project_id uuid references projects(id) on delete cascade,
  type text, -- 'text' | 'image' | 'zip'
  file_url text,
  meta jsonb,
  created_at timestamp default now()
);

-- 用户填写反馈
create table feedbacks (
  id uuid primary key default gen_random_uuid(),
  project_id uuid references projects(id) on delete cascade,
  likes integer,
  comments integer,
  ctr float,
  conversion float,
  submitted_at timestamp default now()
);

-- Stripe 订阅信息
create table subscriptions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references users(id) on delete cascade,
  stripe_id text,
  plan text,
  trial_end timestamp,
  status text default 'active'
);
