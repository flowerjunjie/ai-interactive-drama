import request from '@/utils/request'

/** 短剧后台 /api/admin/drama/* */
export function dramaDashboard() {
  return request({ url: '/api/admin/drama/dashboard', method: 'get' })
}

export function listDrama(query) {
  return request({
    url: '/api/admin/drama/dramas',
    method: 'get',
    params: {
      page_num: query.pageNum,
      page_size: query.pageSize,
      title: query.title || undefined,
    },
  })
}

export function addDrama(data) {
  return request({ url: '/api/admin/drama/dramas', method: 'post', data })
}

export function updateDrama(dramaId, data) {
  return request({ url: '/api/admin/drama/dramas/' + dramaId, method: 'put', data })
}

export function delDrama(dramaId) {
  return request({ url: '/api/admin/drama/dramas/' + dramaId, method: 'delete' })
}

export function listVideoNode(query) {
  const params = {
    page_num: query.pageNum,
    page_size: query.pageSize,
  }
  if (query.dramaId != null && query.dramaId !== '') params.drama_id = query.dramaId
  if (query.reviewStatus) params.review_status = query.reviewStatus
  return request({
    url: '/api/admin/drama/video-nodes',
    method: 'get',
    params,
  })
}

export function addVideoNode(data) {
  return request({ url: '/api/admin/drama/video-nodes', method: 'post', data })
}

export function updateVideoNode(nodeId, data) {
  return request({ url: '/api/admin/drama/video-nodes/' + nodeId, method: 'put', data })
}

export function delVideoNode(nodeId) {
  return request({ url: '/api/admin/drama/video-nodes/' + nodeId, method: 'delete' })
}

export function approveVideoNode(nodeId) {
  return request({ url: '/api/admin/drama/video-nodes/' + nodeId + '/moderation/approve', method: 'put' })
}

export function rejectVideoNode(nodeId, data) {
  return request({ url: '/api/admin/drama/video-nodes/' + nodeId + '/moderation/reject', method: 'put', data })
}

export function listPendingVideoNodes(query) {
  return request({
    url: '/api/admin/drama/video-nodes/pending-moderation',
    method: 'get',
    params: { page_num: query.pageNum, page_size: query.pageSize },
  })
}

export function listVideoChoices(nodeId) {
  return request({ url: `/api/admin/drama/video-nodes/${nodeId}/choices`, method: 'get' })
}

export function addVideoChoice(data) {
  return request({ url: '/api/admin/drama/video-choices', method: 'post', data })
}

export function updateVideoChoice(choiceId, data) {
  return request({ url: '/api/admin/drama/video-choices/' + choiceId, method: 'put', data })
}

export function delVideoChoice(choiceId) {
  return request({ url: '/api/admin/drama/video-choices/' + choiceId, method: 'delete' })
}

export function listPendingReviews(query) {
  return request({
    url: '/api/admin/drama/video-reviews',
    method: 'get',
    params: {
      page_num: query.pageNum,
      page_size: query.pageSize,
      status: 'pending',
    },
  })
}

export function auditReview(reviewId, data) {
  return request({ url: `/api/admin/drama/video-reviews/${reviewId}/audit`, method: 'put', data })
}

export function listAds(query) {
  return request({
    url: '/api/admin/drama/ads',
    method: 'get',
    params: { page_num: query.pageNum, page_size: query.pageSize },
  })
}

export function addAd(data) {
  return request({ url: '/api/admin/drama/ads', method: 'post', data })
}

export function updateAd(adId, data) {
  return request({ url: '/api/admin/drama/ads/' + adId, method: 'put', data })
}

export function delAd(adId) {
  return request({ url: '/api/admin/drama/ads/' + adId, method: 'delete' })
}

export function listAppUsers(query) {
  return request({
    url: '/api/admin/drama/app-users',
    method: 'get',
    params: { page_num: query.pageNum, page_size: query.pageSize },
  })
}

export function listUploadFiles(query) {
  return request({
    url: '/api/admin/drama/upload-files',
    method: 'get',
    params: { page_num: query.pageNum, page_size: query.pageSize },
  })
}

export function listDramaComments(query) {
  return request({
    url: '/api/admin/drama/comments',
    method: 'get',
    params: {
      page_num: query.pageNum,
      page_size: query.pageSize,
      drama_id: query.dramaId || undefined,
    },
  })
}

export function delDramaComment(commentId) {
  return request({ url: '/api/admin/drama/comments/' + commentId, method: 'delete' })
}

export function hideDramaComment(commentId, hidden = true) {
  return request({ url: '/api/admin/drama/comments/' + commentId + '/hide', method: 'put', params: { hidden } })
}

export function appUserWatchHistory(userId) {
  return request({ url: `/api/admin/drama/app-users/${userId}/watch-history`, method: 'get' })
}

export function appUserFavorites(userId) {
  return request({ url: `/api/admin/drama/app-users/${userId}/favorites`, method: 'get' })
}
