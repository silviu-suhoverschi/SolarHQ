export async function downloadCsv() {
  const response = await fetch('/api/export/csv')
  if (!response.ok) throw new Error(`Export failed: ${response.status}`)
  const blob = await response.blob()
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'solarhq_export.csv'
  a.click()
  URL.revokeObjectURL(url)
}
