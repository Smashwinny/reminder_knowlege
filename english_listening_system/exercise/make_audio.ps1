[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$InputPath,
    [Parameter(Mandatory = $true)][string]$OutputPath
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
$text = [System.IO.File]::ReadAllText($InputPath, [System.Text.Encoding]::UTF8).Trim()
if (-not $text) { throw 'Input material is empty.' }

$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
try {
    $synth.Rate = -1
    $synth.Volume = 100
    $synth.SetOutputToWaveFile($OutputPath)
    $synth.Speak($text)
}
finally {
    $synth.Dispose()
}

$bytes = (Get-Item -LiteralPath $OutputPath).Length
"Created: $OutputPath"
"Bytes: $bytes"
