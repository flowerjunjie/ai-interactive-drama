/**
 * 统一分享封装 — 双层 fallback：微信 → 空 provider（静默失败）
 */
interface ShareConfig {
  title?: string
  summary?: string
  href?: string
  imageUrl?: string
}

export function safeShare(config: ShareConfig = {}) {
  const { title = 'AI 互动短剧', summary = '沉浸式分支剧情，体验不一样的人生', href = '', imageUrl = '' } = config
  uni.share({
    provider: 'weixin',
    scene: 'WXSceneSession',
    title,
    summary,
    href,
    imageUrl,
    success: () => {},
    fail: () => {
      // fallback：让用户选择分享到哪儿
      uni.share({
        provider: '' as 'qq' | 'sinaweibo' | 'weixin',
        type: 0,
        title,
        summary,
        href,
        imageUrl,
        success: () => {},
        fail: () => {
          /* silent — 平台不支持分享时什么都不做 */
        },
      })
    },
  })
}