/** 播放页/首页等数值展示 */
export function formatShortCount(n: number): string {
  if (!Number.isFinite(n) || n < 0) return '0'
  if (n >= 100000000) return `${(n / 100000000).toFixed(1)}亿`
  if (n >= 10000) return `${(n / 10000).toFixed(1)}万`
  if (n >= 1000) return `${(n / 1000).toFixed(1)}千`
  return String(Math.floor(n))
}
