# paynexss 的个人源

给越狱设备（rootless / Dopamine，`/var/jb`）用的私有包集合，Sileo / Zebra 直接加源即可。

**源地址**：`https://paynexss.github.io/ios-repo/`

> 网页版首页（含包列表，可复制源地址）：<https://paynexss.github.io/ios-repo/>

## 包含的包

| 包名 | 版本 | 说明 |
| --- | --- | --- |
| `com.paynexc.appdecrypt` | 1.0.0 | 设备端砸壳 CLI（`task_for_pid` + 内存解密，无需 frida） |
| `com.paynexc.tweak.egernprounlock` | 2.5.0 | 解锁 Egern Pro（自包含 hook 层，不依赖 CydiaSubstrate） |
| `com.paynexc.tweak.sjjunlock` | 1.2.0-1+debug | 绕过抖音 siwenjiajia 插件授权校验（完全离线；v1.2 免 substrate，可注入轻松签/重打包 IPA） |
| `com.paynexc.tweak.rexprounlock` | 1.8.0 | 解锁 Rex Pro（「PRO 与授权」页巳解锁 + 授权区文案 + Pro 功能放行） |
| `com.harans.tweak.shortcuttodebug` | 0.2.0-7+debug | 无根越狱下用 3D Touch 快捷方式打开设置的「调试」页 |
| `com.paynexc.repo-key` | 1.0.0 | 本源签名公钥（引导用，只需装一次） |

## 签名与公钥

仓库索引用 GPG 签名（`Release.gpg` + `InRelease`），公钥指纹：

```
A45A745C173F1682DC28438FCF023C28FAFF571D
```

Sileo 添加源时会提示「无法验证」并在确认后自动导入 `public.key`；想手动信任就装
[`debs/com.paynexc.repo-key_1.0.0_iphoneos-arm64.deb`](debs/) —— 它把公钥放进
`/var/jb/etc/apt/trusted.gpg.d/`，之后 `apt update` 不再报签名错误。

## 目录结构

```
Packages / Packages.gz / Packages.bz2   apt 索引
Release / Release.gpg / InRelease       索引的元信息与签名
public.key                              签名公钥（armored）
CydiaIcon.png                           源图标
debs/                                   所有 .deb（索引里的 Filename 指向这里）
icons/ assets/ sileo/ depictions/       门面：包图标 / 横幅 / Sileo 原生详情页 / 网页详情页
sileo-featured.json                     Sileo 首页横幅轮播
index.html                              网页版首页
```

## 维护

本仓库的内容由 `tools/debrepo.sh`（纯 Python 索引生成 + `gpg` 签名）一键产出，源头在本地：

```bash
# 本地维护仓库（不在本仓库内）
~/iosReverse/repo-build.sh          # 收包 → 门面 → 索引 → 签名 → Pages 结构
cd ~/iosReverse/repo && git add -A && git commit -m '源更新' && git push
```

## 说明

- 仅用于自己设备：包都是自用的越狱 tweak / 工具，需要 rootless 越狱环境才能安装。
- 安装前请确认设备架构为 `iphoneos-arm64`；不同越狱环境（rootless vs rootful）路径不同，本源只提供 rootless 包。
- 索引与包均按原样提供，不做任何担保。
