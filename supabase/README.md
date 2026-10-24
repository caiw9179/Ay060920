# 接入云同步（Supabase，免费版就够用）

不做这一步，图鉴也能完整使用，数据只存在当前设备的浏览器里。接入后可以用邮箱验证码登录，换手机也能找回整个鞋柜。

## 1. 建一个免费项目
1. 打开 https://supabase.com ，点 **Start your project**，用 GitHub 或邮箱注册。
2. 点 **New project**：起个名字（比如 `aj-dex`），设一个数据库密码（自己记下，图鉴用不到），Region 选离你近的（比如 Singapore 或 Tokyo），Plan 选 **Free**。
3. 等一两分钟，项目创建完成。

## 2. 运行建表脚本
1. 左侧菜单点 **SQL Editor**，再点 **New query**。
2. 把本文件夹里 `setup.sql` 的全部内容粘贴进去，点右下角 **Run**。
3. 看到 `Success. No rows returned` 就说明表、权限和照片桶都建好了。可以在 **Table Editor** 看到 `series` 和 `shoes`，在 **Storage** 看到私有桶 `photos`。

## 3. 打开邮箱验证码登录
1. 左侧点 **Authentication**，进入 **Sign In / Providers**（旧版叫 Providers），确认 **Email** 是开启状态。
2. 进入 **Authentication > Emails**（旧版在 Email Templates），打开 **Magic Link** 模板，把正文改成带验证码的版本，例如：
   ```
   <h2>小猫的AJ图鉴</h2>
   <p>你的登录验证码是：<b>{{ .Token }}</b></p>
   <p>10 分钟内有效，不是你本人操作请忽略。</p>
   ```
   模板里有 `{{ .Token }}`，邮件就会带 6 位验证码。如果你的项目验证码长度不是 6 位，到 **Authentication > Sign In / Providers > Email** 里把 **Email OTP Length** 设为 6。
3. （可选）在 **Authentication > URL Configuration** 的 Site URL 填你以后放图鉴的网址。只用验证码登录的话可以不填。

> 免费版自带的发信服务每小时只能发几封，自己用足够。想发更多可以在 **Authentication > SMTP Settings** 接自己的邮箱服务。

## 4. 找到 URL 和 anon key，填进图鉴
1. 左侧点 **Project Settings**（齿轮图标）。
2. **Data API**（旧版在 API）页面里复制 **Project URL**，形如 `https://xxxx.supabase.co`。
3. **API Keys** 页面里复制 **anon public** 那一串（新版也可以用 `sb_publishable_...` 开头的 Publishable key）。这把钥匙可以放在网页里，数据靠第 2 步的行级安全保护。**不要**用 `service_role` / secret key。
4. 用文本编辑器打开 `index.html`，找到最上面这两行，填进去保存：
   ```js
   const SUPABASE_URL = 'https://xxxx.supabase.co';
   const SUPABASE_ANON_KEY = 'eyJhbGciOi...';
   ```

## 5. 试一下
打开图鉴，会出现登录页：输入邮箱，点 **发送验证码**，把邮件里的 6 位数字填进去就登录了。
- 第一次登录时，这台设备上已有的展厅、鞋和照片会自动上传。
- 之后每次改动都会自动同步；没网时照常使用，联网后再补传。
- 两台设备改了同一双鞋，以最后修改的那次为准。
- 设置里可以随时 **立即同步** 或 **退出登录**。
