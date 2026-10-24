$ErrorActionPreference = 'Stop'
$repoDir = Split-Path -Parent $PSScriptRoot
$pptPath = Join-Path $repoDir 'presentaciones/Avances-Experimentales-Simplificados-24-10-2026.pptx'
$pdfPath = Join-Path $repoDir 'presentaciones/Avances-Experimentales-Simplificados-24-10-2026.pdf'
$renderDir = Join-Path $repoDir 'resultados/presentacion_avances_simplificados_24-10-2026'
New-Item -ItemType Directory -Force -Path $renderDir | Out-Null
$pptApp = New-Object -ComObject PowerPoint.Application
$initialCount = $pptApp.Presentations.Count
$deck = $null
try {
    $deck = $pptApp.Presentations.Open($pptPath, -1, 0, 0)
    $overflow = @()
    foreach ($slide in $deck.Slides) {
        $slide.Export((Join-Path $renderDir ('slide-' + $slide.SlideIndex + '.png')), 'PNG', 1600, 900)
        foreach ($shape in $slide.Shapes) {
            if ($shape.HasTextFrame -eq -1 -and $shape.TextFrame.HasText -eq -1) {
                $range = $shape.TextFrame.TextRange
                if ($range.BoundHeight -gt ($shape.Height + 3) -or $range.BoundWidth -gt ($shape.Width + 3)) {
                    $overflow += [pscustomobject]@{slide=$slide.SlideIndex; shape=$shape.Id; height=$shape.Height; textHeight=$range.BoundHeight; width=$shape.Width; textWidth=$range.BoundWidth}
                }
            }
        }
    }
    $deck.SaveAs($pdfPath, 32)
    $audit = [pscustomobject]@{opened_in='Microsoft PowerPoint'; slides=$deck.Slides.Count; overflow=@($overflow); tolerance_points=3; pdf=$pdfPath}
    $audit | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $renderDir 'renderizado.json') -Encoding UTF8
    $audit | ConvertTo-Json -Depth 5
    if ($overflow.Count -gt 0) { throw 'Texto fuera de los cuadros: revisar renderizado.json.' }
} finally {
    if ($null -ne $deck) { $deck.Close() }
    if ($initialCount -eq 0) { $pptApp.Quit() }
    [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($pptApp)
}
