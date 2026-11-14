# Recorded full-test Exact Match

These are aggregate results of completed local runs, not a newly executed experiment in this PR. Raw records, per-sample outputs and trained weights are not published.

| Repository | Per-repository matches / total | EM (%) | Global matches / total | EM (%) |
|---|---:|---:|---:|---:|
| OVERALL | 1011 / 1663 | 60.79 | 559 / 1668 | 33.51 |
| 52North/SOS | 47 / 157 | 29.94 | 0 / 91 | 0.00 |
| Azure/autorest | 172 / 172 | 100.00 | 0 / 0 | N/A |
| Azure/azure-sdk-for-java | 150 / 185 | 81.08 | 0 / 0 | N/A |
| RumbleDB/rumble | 103 / 276 | 37.32 | 305 / 1274 | 23.94 |
| apache/cloudstack | 43 / 106 | 40.57 | 1 / 2 | 50.00 |
| apache/sis | 53 / 119 | 44.54 | 1 / 1 | 100.00 |
| micdoodle8/Galacticraft | 94 / 135 | 69.63 | 0 / 0 | N/A |
| molgenis/molgenis | 106 / 151 | 70.20 | 1 / 1 | 100.00 |
| orientechnologies/orientdb | 100 / 105 | 95.24 | 203 / 219 | 92.69 |
| sleuthkit/autopsy | 76 / 140 | 54.29 | 23 / 38 | 60.53 |
| spring-projects/spring-boot | 67 / 117 | 57.26 | 25 / 42 | 59.52 |

Per-repository split macro EM: 61.82%. Global split macro EM: 60.84% (repositories without test records excluded).

Counting every exception fallback as failure, with the same full denominators: 1010/1663 (60.73%) and 559/1668 (33.51%). The primary per-repository result includes one empty fallback matching an empty reference.

The global test is dominated by RumbleDB/rumble (1274/1668 records). Auto-merge and classifier contributions are recorded separately in each behavior_breakdown.json; overall EM is not solely neural classification accuracy.
