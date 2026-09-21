# Renderizado real con PowerPoint, sin abrir una ventana de la presentacion.
$ErrorActionPreference = 'Stop'
$repoDir = Split-Path -Parent $PSScriptRoot
$pptPath = Join-Path $repoDir 'presentaciones/Avances-Resumen-Autocontenido-21-09-2026.pptx'
$renderDir = Join-Path $env:TEMP 'mds-pptx-avances-breves-21-09-2026'
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
                if ($range.BoundHeight -gt ($shape.Height + 2) -or $range.BoundWidth -gt ($shape.Width + 2)) {
                    $overflow += [pscustomobject]@{slide=$slide.SlideIndex; shape=$shape.Id; height=$shape.Height; textHeight=$range.BoundHeight; width=$shape.Width; textWidth=$range.BoundWidth}
                }
            }
        }
    }
    $deck.SaveAs((Join-Path $renderDir 'presentacion.pdf'),32)
    $audit = [pscustomobject]@{opened_in='Microsoft PowerPoint'; slides=$deck.Slides.Count; overflow=@($overflow); tolerance_points=2; pdf_pages_expected=5; canva_import_tested=$false}
    $reportPath = Join-Path $repoDir 'documentacion/Verificacion_PPTX_Avances_Breves_21-09-2026.json'
    $report = Get-Content -LiteralPath $reportPath -Raw -Encoding UTF8 | ConvertFrom-Json
    $report | Add-Member -NotePropertyName 'powerpoint_render' -NotePropertyValue $audit -Force
    $report | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $reportPath -Encoding UTF8
    $audit | ConvertTo-Json -Depth 5
    if ($overflow.Count -gt 0) { throw 'Texto fuera de los cuadros: revisar el informe.' }
} finally {
    if ($null -ne $deck) { $deck.Close() }
    if ($initialCount -eq 0) { $pptApp.Quit() }
    [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($pptApp)
}
