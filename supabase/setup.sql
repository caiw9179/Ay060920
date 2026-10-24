-- 小猫的AJ专属赛博图鉴 · Supabase 初始化脚本
-- 用法：Supabase 控制台 > SQL Editor > New query，整段粘贴后点 Run。可重复执行。

-- ========== 1. 表 ==========
create table if not exists public.series (
  id          text primary key,                 -- 客户端生成的 id，离线也能先建
  user_id     uuid not null default auth.uid() references auth.users(id) on delete cascade,
  name        text not null default '',
  sort        integer not null default 0,
  deleted     boolean not null default false,   -- 删除以墓碑同步，便于多设备合并
  updated_at  timestamptz not null default now()
);

create table if not exists public.shoes (
  id          text primary key,
  user_id     uuid not null default auth.uid() references auth.users(id) on delete cascade,
  series_id   text,                             -- 所属展厅 series.id
  name        text not null default '',         -- 完整名称，例如 AJ1 芝加哥
  colorway    text,                             -- 配色部分，例如 芝加哥
  status      text not null default 'unlit' check (status in ('unlit','lit','sailed')),
  got_date    date,                             -- 入柜日期
  memory      text,                             -- 回忆碎片
  sailed_date date,                             -- 远航日期
  photo_path  text,                             -- photos 桶里的路径：<user_id>/<文件名>
  sort        integer not null default 0,
  deleted     boolean not null default false,
  updated_at  timestamptz not null default now()  -- 冲突时以它为准，后写者胜
);

create index if not exists series_user_idx on public.series (user_id);
create index if not exists shoes_user_idx  on public.shoes  (user_id);

-- ========== 2. 行级安全：每个人只能看到、改动自己的行 ==========
alter table public.series enable row level security;
alter table public.shoes  enable row level security;

drop policy if exists "series_select_own" on public.series;
drop policy if exists "series_insert_own" on public.series;
drop policy if exists "series_update_own" on public.series;
drop policy if exists "series_delete_own" on public.series;
create policy "series_select_own" on public.series for select to authenticated using (user_id = auth.uid());
create policy "series_insert_own" on public.series for insert to authenticated with check (user_id = auth.uid());
create policy "series_update_own" on public.series for update to authenticated using (user_id = auth.uid()) with check (user_id = auth.uid());
create policy "series_delete_own" on public.series for delete to authenticated using (user_id = auth.uid());

drop policy if exists "shoes_select_own" on public.shoes;
drop policy if exists "shoes_insert_own" on public.shoes;
drop policy if exists "shoes_update_own" on public.shoes;
drop policy if exists "shoes_delete_own" on public.shoes;
create policy "shoes_select_own" on public.shoes for select to authenticated using (user_id = auth.uid());
create policy "shoes_insert_own" on public.shoes for insert to authenticated with check (user_id = auth.uid());
create policy "shoes_update_own" on public.shoes for update to authenticated using (user_id = auth.uid()) with check (user_id = auth.uid());
create policy "shoes_delete_own" on public.shoes for delete to authenticated using (user_id = auth.uid());

-- ========== 3. 私有照片桶 photos ==========
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('photos', 'photos', false, 5242880, array['image/jpeg','image/png','image/webp'])
on conflict (id) do update set public = false;

-- 只能读写自己文件夹 <user_id>/ 下的文件，读取走签名链接
drop policy if exists "photos_select_own" on storage.objects;
drop policy if exists "photos_insert_own" on storage.objects;
drop policy if exists "photos_update_own" on storage.objects;
drop policy if exists "photos_delete_own" on storage.objects;
create policy "photos_select_own" on storage.objects for select to authenticated
  using (bucket_id = 'photos' and (storage.foldername(name))[1] = auth.uid()::text);
create policy "photos_insert_own" on storage.objects for insert to authenticated
  with check (bucket_id = 'photos' and (storage.foldername(name))[1] = auth.uid()::text);
create policy "photos_update_own" on storage.objects for update to authenticated
  using (bucket_id = 'photos' and (storage.foldername(name))[1] = auth.uid()::text)
  with check (bucket_id = 'photos' and (storage.foldername(name))[1] = auth.uid()::text);
create policy "photos_delete_own" on storage.objects for delete to authenticated
  using (bucket_id = 'photos' and (storage.foldername(name))[1] = auth.uid()::text);
