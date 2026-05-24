function e(e){return!Number.isFinite(e)||e<0?"0":e>=1e8?`${(e/1e8).toFixed(1)}亿`:e>=1e4?`${(e/1e4).toFixed(1)}万`:e>=1e3?`${(e/1e3).toFixed(1)}千`:String(Math.floor(e))}export{e as f};
