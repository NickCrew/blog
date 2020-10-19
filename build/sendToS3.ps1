#Requires -Version 7

<#
.SYNOPSIS
    Upload static built blog content to s3 bucket
#>
[CmdletBinding(SupportsShouldProcess=$true)]
param (
    [Parameter(Position = 0, Mandatory = $false)]
    [string]
    $BucketName = 'blog.devbear.net'
)
$ErrorActionPreference = 'Stop'

Import-Module AWSPowerShell.NetCore

$output = Join-Path $PSScriptRoot 'output'
if (-not (Test-Path $output)) {
    throw "${output} not found."
}

Get-ChildItem $output -File | ForEach-Object {
    $params = @{
        BucketName = $BucketName
        File = $_.FullName
        Key = $_.BaseName
        Verbose = $VerbosePreference
    }
    if ($PSCmdlet.ShouldProcess("$($_.BaseName)", "Upload to ${BucketName}")) {
        try {
            Write-S3Object @params
        }
        catch {
            throw $PSItem
        }
    }
}

Get-ChildItem $output -Directory | ForEach-Object {
    $params = @{
        BucketName = $BucketNamek
        Folder = $_.FullName
        KeyPrefix = $_.BaseName
        Verbose = $VerbosePreference
    }
    if ($PSCmdlet.ShouldProcess("$($_.BaseName)", "Upload to ${BucketName}")) {
        try {
            Write-S3Object @params
        }
        catch {
            throw $PSItem
        }
    }
}
