import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/admin/login',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/admin/info',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/admin/logout',
    method: 'post'
  })
}

export function getAllUsers() {
  return request({
    url: '/admin/get_all_users',
    method: 'post'
  })
}

export function getAllModels() {
  return request({
    url: '/admin/get_all_models',
    method: 'post'
  })
}

export function getAllFeedbacks() {
  return request({
    url: '/admin/get_all_feedbacks',
    method: 'post'
  })
}

export function removeModel(data) {
  return request({
    url: '/admin/remove_model',
    method: 'post',
    data
  })
}

export function banUser(data) {
  return request({
    url: '/admin/ban_user',
    method: 'post',
    data
  })
}

export function activateUser(data) {
  return request({
    url: '/admin/activate_user',
    method: 'post',
    data
  })
}
