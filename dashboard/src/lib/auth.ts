export function getAuthHeader(rawToken?: string): Record<string, string> | null {
  const token = (rawToken ?? "").trim().replace(/^['"]|['"]$/g, "")
  if (!token) return null

  const authorization = token.toLowerCase().startsWith("bearer ")
    ? token
    : `Bearer ${token}`

  return { Authorization: authorization }
}

