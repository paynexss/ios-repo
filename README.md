# paynexss 的个人源

给越狱设备（rootless / Dopamine，`/var/jb`）用的私有包集合，Sileo / Zebra 直接加源即可。

**源地址**：`http://repo.paynexss.fun/`

> 网页版首页（含包列表，可复制源地址）：<http://repo.paynexss.fun/>

## 包含的包

| 包名 | 版本 | 说明 |
| --- | --- | --- |
| `com.paynexc.tweak.egernprounlock` | 2.5.0 | 解锁 Egern Pro（自包含 hook 层，不依赖 CydiaSubstrate） |
| `com.paynexc.tweak.sjjunlock` | 1.2.0-1+debug | 绕过抖音 siwenjiajia 插件授权校验（完全离线；v1.2 免 substrate，可注入轻松签/重打包 IPA） |
| `com.paynexc.tweak.rexprounlock` | 1.8.0 | 解锁 Rex Pro（「PRO 与授权」页解锁 + 授权区文案 + Pro 功能放行） |
| `com.harans.tweak.shortcuttodebug` | 0.2.0-7+debug | 无根越狱下用 3D Touch 快捷方式打开设置的「调试」页 |

## 签名

**本源未签名**：仓库里没有 `InRelease` / `Release.gpg` / `public.key`。

Sileo / Zebra 添加源不需要导入任何公钥，`apt update` 也不会报「无法验证」；代价是走 http 明文时
索引没有防篡改（索引与包均按原样提供，自己判断网络环境）。

## 目录结构

```
Packages / Packages.gz / Packages.bz2   apt 索引
Release                                 索引的元信息（无签名）
CydiaIcon.png                           源图标
debs/                                   所有 .deb（索引里的 Filename 指向这里）
icons/ assets/ sileo/ depictions/       门面：包图标 / 横幅 / Sileo 原生详情页 / 网页详情页
sileo-featured.json                     Sileo 首页横幅轮播
index.html                              网页版首页
```

## 维护

本目录就是发布目录，`repo-build.sh` 一键重建（收包 → 门面 → 索引 → Release）：

```bash
./repo-build.sh          # 用到 ~/Reverse/tools/ios-toolkit 里的 debrepo.sh，可用 IOS_TOOLKIT=… 覆盖
git add -A && git commit -m '源更新' && git push     # push 后 repo.paynexss.fun 生效
```

加包：`.deb` 丢进 `debs/`（或写进 `repo-build.sh` 的 `SRC_DEBS`）再跑一次；删包：删掉 `debs/` 里的
deb 再跑一次，残留的图标/横幅/sileo/depiction 会被自动清掉。

## 说明

- 仅用于自己设备：包都是自用的越狱 tweak / 工具，需要 rootless 越狱环境才能安装。
- 安装前请确认设备架构为 `iphoneos-arm64`；不同越狱环境（rootless vs rootful）路径不同，本源只提供 rootless 包。
- 索引与包均按原样提供，不做任何担保。
