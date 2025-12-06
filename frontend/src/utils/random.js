export const randomSecret = (len = 32) => {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  let result = ''
  const array = new Uint8Array(len)
  crypto.getRandomValues(array)
  for (let i = 0; i < len; i += 1) {
    result += chars[array[i] % chars.length]
  }
  return result
}
